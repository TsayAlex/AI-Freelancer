"""ALEX AI QA Factory v1.2 — local, evidence-first ZIP inbox monitor.

No content of uploaded projects is executed. Only parse, CRC checks and
optional `node --check` syntax parsing (not `node` execution).
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import io
import json
import os
import re
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from qa_engine import (ScanError, scan_zip_bytes, scan_html, add, finish,
                       make_report, safe_path, SEVERITIES)
from reports import (make_html, make_markdown, make_csv, make_pdf, make_docx,
                     test_plan_markdown, cases_csv, release_checklist, bilingual_report, review_prompt)

ROOT = Path(__file__).resolve().parent
MAX_ARCHIVE_BYTES = 600*1024*1024
MAX_EXPANDED = 1600*1024*1024
MAX_ENTRIES = 12000
MAX_SCAN_FILES = 350
MAX_TEXT_FILE = 16*1024*1024
MAX_TOTAL_TEXT = 45*1024*1024
MAX_RATIO = 500
SKIP_EXT = {'.mp3','.mp4','.png','.jpg','.jpeg','.webp','.gif','.woff','.woff2','.otf','.ttf','.wasm','.ogg','.wav','.avi','.mov'}
CRITICAL_FILENAMES = {'.env','.env.production','.env.local','id_rsa','credentials.json','secrets.json','service-account.json'}


def utcnow(): return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha256_file(path):
    h=hashlib.sha256()
    with path.open('rb') as fd:
        for block in iter(lambda:fd.read(2*1024*1024),b''):h.update(block)
    return h.hexdigest()


def inspect_archive(path:Path, full_crc:bool=True):
    """Stream ZIP from disk; preflight untrusted sizes before decompressing."""
    if path.stat().st_size>MAX_ARCHIVE_BYTES:
        raise ScanError('Archive exceeds local safety limit (600 MB).')
    r=make_report('zip',path.name)
    evidence={'source_sha256':sha256_file(path),'source_size_bytes':path.stat().st_size,
              'method':'static safe ZIP inspection + optional full CRC; never execute project code'}
    try: z=zipfile.ZipFile(path)
    except (zipfile.BadZipFile,ValueError,zipfile.LargeZipFile) as exc:
        raise ScanError('Invalid ZIP archive: '+str(exc)[:160]) from exc
    with z:
        entries=[e for e in z.infolist() if not e.is_dir()]
        if len(entries)>MAX_ENTRIES:raise ScanError('ZIP file count over 12000 entry limit')
        expanded=sum(e.file_size for e in entries)
        if expanded>MAX_EXPANDED:raise ScanError('Archive expanded size exceeds 1.6 GB safety limit')
        for e in entries:
            if not safe_path(e.filename):raise ScanError('Unsafe ZIP member path: '+e.filename[:100])
            if (e.external_attr>>16)&0o170000==0o120000:
                raise ScanError('Symlink entries are forbidden')
            if e.flag_bits & 1: raise ScanError('Encrypted archives not supported')
            if e.file_size>15*1024*1024 and e.compress_size and e.file_size/max(1,e.compress_size)>MAX_RATIO:
                raise ScanError('Suspicious ZIP expansion ratio')
        present=set(e.filename for e in entries)
        r['metrics'].update({'files_total':len(entries),'expanded_bytes':expanded,
                             'nested_zip_count':sum(e.filename.lower().endswith('.zip') for e in entries),
                             'source_size_bytes':path.stat().st_size})
        r['checked'].append('ZIP structure, filenames, traversal protection, decompressed-size preflight')
        if full_crc:
            # Check CRC on streaming data, only after all entries pass the bounds above.
            corrupt=z.testzip()
            if corrupt:
                add(r,'ZIP_CRC','critical','ZIP member CRC mismatch',corrupt,'CRC verification passes','CRC verification failed','Re-export archive; review integrity')
            else:r['checked'].append('Full ZIP CRC verification')
        else:r['warnings'].append('Full CRC not performed (--fast).')
        text_count=0;text_bytes=0;skipped_large=0;skipped_count=0;external_assets=0
        for entry in entries:
            filename=entry.filename
            if Path(filename).name.lower() in CRITICAL_FILENAMES:
                add(r,'SENSITIVE_FILE','major','Sensitive-looking filename in release archive',filename,'No private secrets included','Name requires manual verification','Inspect offline and remove or rotate actual secrets',confidence='medium')
            ext=Path(filename).suffix.lower()
            if ext in SKIP_EXT: external_assets+=1;continue
            if ext not in ('.html','.htm','.js','.mjs','.cjs','.json','.css','.svg','.xml','.webmanifest'):
                continue
            if entry.file_size>MAX_TEXT_FILE or text_count>=MAX_SCAN_FILES or text_bytes+entry.file_size>MAX_TOTAL_TEXT:
                skipped_large+=1;continue
            try:
                b=z.read(entry)
            except (zipfile.BadZipFile,RuntimeError,EOFError) as exc:
                add(r,'ZIP_READ','critical','ZIP member could not be read',filename,'Entry readable',str(exc),'Rebuild release ZIP')
                continue
            text_count+=1;text_bytes+=len(b)
            src=b.decode('utf-8',errors='replace')
            if ext in ('.html','.htm'):
                scan_html(r,filename,src,present)
                # Detect syntax errors in inline scripts without executing the content.
                # Ignore non-executable JSON and other data scripts.
                from shutil import which
                if which('node'):
                    import subprocess
                    for index,match in enumerate(re.finditer(r'<script\b([^>]*)>([\s\S]*?)</script\s*>',src,re.I)):
                        attrs=match.group(1);body=match.group(2)
                        if re.search(r'\bsrc\s*=',attrs,re.I) or not body.strip():continue
                        typem=re.search(r'\btype\s*=\s*[\"\']?([^\"\'\s>]+)',attrs,re.I)
                        typ=typem.group(1).lower() if typem else ''
                        if typ and typ not in ('module','text/javascript','application/javascript'):continue
                        if len(body.encode('utf-8'))>12*1024*1024:
                            r['warnings'].append(f'Inline JS block {index+1} in {filename} exceeds 12MB parse limit')
                            continue
                        with tempfile.TemporaryDirectory(prefix='alexqa_inline_') as td:
                            target=Path(td)/('check.mjs' if typ=='module' else 'check.js')
                            target.write_text(body,encoding='utf-8')
                            try:
                                cp=subprocess.run(['node','--check',str(target)],capture_output=True,text=True,timeout=10)
                                if cp.returncode:
                                    add(r,'INLINE_JS_SYNTAX','major','Inline JavaScript cannot be parsed',f'{filename}:script-{index+1}','Valid inline JavaScript',cp.stderr[-320:],'Correct inline JavaScript syntax')
                                r['checked'].append(f'{filename}:script-{index+1} [Node syntax only]')
                            except (OSError,subprocess.TimeoutExpired):
                                r['warnings'].append(f'Inline JavaScript parse could not complete in {filename}:script-{index+1}')
            elif ext in ('.json','.webmanifest'):
                try:json.loads(src);r['checked'].append(filename+' [JSON parsed]')
                except json.JSONDecodeError as exc:
                    add(r,'INVALID_JSON','major','Invalid JSON syntax',f'{filename}:{exc.lineno}','Valid JSON',exc.msg,'Fix JSON structure')
            elif ext in ('.js','.mjs','.cjs'):
                # Node parser only; no script execution and no package scripts.
                from shutil import which
                import subprocess
                if which('node'):
                    with tempfile.TemporaryDirectory(prefix='alexqa_') as td:
                        p=Path(td)/('script'+ext)
                        p.write_bytes(b)
                        try:
                            cp=subprocess.run(['node','--check',str(p)],capture_output=True,text=True,timeout=5)
                            if cp.returncode:
                                add(r,'JS_SYNTAX','major','JavaScript cannot be parsed',filename,'Valid JavaScript',cp.stderr[-350:],'Correct JS syntax')
                            r['checked'].append(filename+' [Node parse-only]')
                        except (OSError,subprocess.TimeoutExpired):
                            r['warnings'].append('Node parser timeout: '+filename[:100])
                elif skipped_count==0:
                    skipped_count+=1
                    r['warnings'].append('Node.js unavailable; JS syntax not checked')
            elif ext=='.css':r['checked'].append(filename+' [CSS file read, not validated]')
        r['metrics'].update({'text_files_checked':text_count,'text_bytes_checked':text_bytes,
                             'text_files_skipped':skipped_large,'binary_assets_not_static_scanned':external_assets})
        if skipped_large:r['warnings'].append(f'{skipped_large} candidate text files not checked due to file/time/size caps')
        if r['metrics']['nested_zip_count']:
            r['warnings'].append(f'{r["metrics"]["nested_zip_count"]} nested ZIPs found; individual contents NOT scanned by this outer scan')
        if not text_count:r['warnings'].append('No source files were eligible for this level of static inspection')
    finish(r)
    r['autopilot']={**evidence,'completed_at':utcnow(),
                    'coverage':'PARTIAL' if (r['metrics']['text_files_skipped'] or r['metrics']['nested_zip_count'] or not full_crc or any('Node.js unavailable' in w or 'exceeds 12MB parse limit' in w for w in r['warnings'])) else 'STATIC_ONLY',
                    'release_assurance':'Not a functional or security certification'}
    if r['autopilot']['coverage']=='PARTIAL' and r['quality_gate'] in ('NO_DETECTED_ISSUES','WARNINGS'):
        r['quality_gate']='INCOMPLETE'
    return r


def unique_key(issue):
    # Stable enough to compare same project across incremental revisions; does not
    # count number of candidate issues as number of confirmed bugs.
    loc=re.sub(r':\d+$','',issue['location'])
    return (issue['code'],loc,issue['actual'][:100])


def delta(new,old):
    n={unique_key(f):f for f in new.get('findings',[])}
    o={unique_key(f):f for f in old.get('findings',[])} if old else {}
    return {'new_candidates':[n[k]['id'] for k in n.keys()-o.keys()],
            'resolved_candidates':[o[k]['id'] for k in o.keys()-n.keys()],
            'unchanged_candidates':len(n.keys()&o.keys()),
            'basis':'Heuristic candidate differences, not confirmed bug fixes'}


def report_release_dir(out:Path,report:dict,previous:Optional[dict]=None):
    out.mkdir(parents=True,exist_ok=True)
    report['autopilot']['delta']=delta(report,previous)
    (out/'QA_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'QA_REPORT.html').write_text(make_html(report),encoding='utf-8')
    (out/'QA_REPORT.md').write_text(make_markdown(report),encoding='utf-8')
    (out/'BUGS.csv').write_text(make_csv(report),encoding='utf-8-sig')
    (out/'TEST_PLAN_EN_RU.md').write_text(test_plan_markdown(report),encoding='utf-8')
    (out/'TEST_CASES.csv').write_text(cases_csv(report),encoding='utf-8')
    (out/'RELEASE_CHECKLIST_EN_RU.md').write_text(release_checklist(report),encoding='utf-8')
    (out/'QA_REPORT_EN_RU.md').write_text(bilingual_report(report,'ru'),encoding='utf-8')
    (out/'QA_REPORT_EN_UA.md').write_text(bilingual_report(report,'uk'),encoding='utf-8')
    (out/'AI_REVIEW_WORKSHEET_EN_RU.md').write_text(review_prompt(report),encoding='utf-8')
    pdf=make_pdf(report)
    if pdf:(out/'QA_REPORT.pdf').write_bytes(pdf)
    word=make_docx(report)
    if word:(out/'QA_REPORT.docx').write_bytes(word)
    return out


def clean_name(name):return re.sub(r'[^a-zA-Z0-9._-]+','-',name)[:70] or 'project'


def family_of(name):
    stem=Path(name).stem
    stem=re.sub(r'(?i)[_-]?(?:v|version)[_-]?\d+(?:[._]\d+)*','',stem)
    stem=re.sub(r'(?i)[_-]?(?:FINAL|LIGHT|MASTER|DEPLOY|UPDATED|BUILD|RELEASE|COMPLETE|TURBO|FIXED|QA|RC\d+)+','',stem)
    return clean_name(stem).lower().strip('-_.') or clean_name(Path(name).stem).lower()


def load_state(output):
    p=output/'state.json'
    if not p.exists():return {'files':{},'families':{},'updated_at':None}
    try:
        state=json.loads(p.read_text(encoding='utf-8'))
        if isinstance(state.get('files'),dict) and isinstance(state.get('families'),dict):return state
    except (ValueError,OSError,TypeError):pass
    raise ScanError('State file cannot be read; preserve it and recover from backup')


def persist_state(output,state):
    state['updated_at']=utcnow()
    tmp=output/'state.json.tmp'
    tmp.write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
    tmp.replace(output/'state.json')


def build_dashboard(output,state):
    rows=[]
    for p,v in state['files'].items():
        if not (output/v['report_path']/'QA_REPORT.json').exists():continue
        rows.append({'name':Path(p).name,'hash':v['sha256'][:12], 'gate':v['gate'],
                     'candidates':v['candidates'],'last_scan':v['scanned_at'],
                     'path':(v['report_path']+'/QA_REPORT.html').replace('\\','/'),
                     'coverage':v.get('coverage','UNKNOWN')})
    rows.sort(key=lambda x:x['last_scan'],reverse=True)
    (output/'dashboard.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    cards=''.join(f'<a class="card" href="{html.escape(x["path"],quote=True)}"><strong>{html.escape(x["name"])}</strong><span>{html.escape(x["gate"])} · {x["candidates"]} candidates</span><small>SHA {x["hash"]} · {html.escape(x["coverage"])}</small><small>{html.escape(x["last_scan"])}</small></a>' for x in rows)
    page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ALEX QA AUTOPILOT — результаты</title><style>
    :root{{color-scheme:dark}}body{{font:16px system-ui,sans-serif;background:#081426;color:#e8f7ff;max-width:1100px;margin:auto;padding:24px}}h1{{color:#65e8df}}p{{color:#b0cad6}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}}.card{{background:#11253e;border:1px solid #29485c;border-radius:14px;padding:19px;color:inherit;text-decoration:none;display:grid;gap:10px;overflow-wrap:anywhere}}.card:hover{{border-color:#54e1d2}}.card span{{color:#f8cd80}}small{{color:#b0cad6}}
    </style></head><body><h1>🧪 ALEX QA AUTOPILOT v1.2</h1><p>EN: Local automated static QA with evidence. RU: Локальный автоматический QA с доказательствами.</p><p>Not a guarantee of correctness. Не является гарантией отсутствия ошибок.</p><p>Checked releases / Проверенные релизы: <strong>{len(rows)}</strong></p><div class="cards">{cards or '<p>Drop ZIPs into QA_INBOX and start the watcher. / Перемести ZIP в QA_INBOX и запусти наблюдение.</p>'}</div></body></html>'''
    (output/'OPEN_DASHBOARD.html').write_text(page,encoding='utf-8')


def scan_inbox(inbox:Path,output:Path,full_crc=True,verbose=True):
    inbox.mkdir(parents=True,exist_ok=True);output.mkdir(parents=True,exist_ok=True)
    state=load_state(output)
    summary={'scanned':0,'skipped_unchanged':0,'failed':0,'errors':[],'files_seen':0}
    for p in sorted(inbox.glob('*.zip')):
        if not p.is_file():continue
        summary['files_seen']+=1
        try:
            digest=sha256_file(p)
            key=p.name
            oldfile=state['files'].get(key)
            if oldfile and oldfile.get('sha256')==digest and (output/oldfile.get('report_path','')/'QA_REPORT.json').exists():
                summary['skipped_unchanged']+=1;continue
            family=family_of(key)
            family_record=state['families'].get(family)
            previous=None
            if family_record:
                prev=output/family_record['report_path']/'QA_REPORT.json'
                if prev.is_file():previous=json.loads(prev.read_text(encoding='utf-8'))
            report=inspect_archive(p,full_crc=full_crc)
            dest_rel=f'reports/{clean_name(p.stem)}-{digest[:12]}'
            report_release_dir(output/dest_rel,report,previous)
            item={'sha256':digest,'scanned_at':utcnow(),'report_path':dest_rel,
                  'gate':report['quality_gate'],'candidates':len(report['findings']),
                  'coverage':report['autopilot']['coverage'],'family':family}
            state['files'][key]=item
            state['families'][family]={'report_path':dest_rel,'name':key}
            persist_state(output,state)
            summary['scanned']+=1
            if verbose:print(f'[QA] SCANNED {p.name}: {report["quality_gate"]}, {len(report["findings"])} candidates')
        except Exception as exc:
            summary['failed']+=1;msg=f'{p.name}: {type(exc).__name__}: {str(exc)[:190]}'
            summary['errors'].append(msg)
            if verbose:print('[QA] FAILED',msg,file=sys.stderr)
    build_dashboard(output,state)
    (output/'last_run.json').write_text(json.dumps({'timestamp':utcnow(),**summary},indent=2,ensure_ascii=False),encoding='utf-8')
    return summary


def main(argv=None):
    p=argparse.ArgumentParser(description='ALEX AI QA Factory Autopilot — automatically scan incoming ZIPs')
    p.add_argument('mode',nargs='?',choices=['once','watch'],default='once')
    p.add_argument('--inbox',type=Path,default=ROOT/'QA_INBOX')
    p.add_argument('--output',type=Path,default=ROOT/'QA_RESULTS')
    p.add_argument('--fast',action='store_true',help='Skip CRC verification (clearly marked as incomplete)')
    p.add_argument('--interval',type=int,default=15,help='Watch interval, seconds (minimum 5)')
    args=p.parse_args(argv)
    print('ALEX AI QA FACTORY AUTOPILOT —',args.mode.upper())
    print('Inbox:',args.inbox.resolve());print('Output:',args.output.resolve())
    if args.mode=='once':
        r=scan_inbox(args.inbox,args.output,not args.fast)
        print(json.dumps(r,ensure_ascii=False));return 1 if r['failed'] else 0
    print('Watcher runs ONLY while this terminal remains open; Ctrl+C stops.')
    try:
        while True:
            scan_inbox(args.inbox,args.output,not args.fast)
            time.sleep(max(5,args.interval))
    except KeyboardInterrupt:print('Watcher stopped.');return 0

if __name__=='__main__':raise SystemExit(main())
