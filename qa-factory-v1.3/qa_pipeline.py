#!/usr/bin/env python3
"""One-command continuous QA pipeline with conservative release gating.
Browser testing runs *only* when --trusted-game-browser is supplied.
"""
from __future__ import annotations
import argparse, csv, html, json, time
from datetime import datetime, timezone
from pathlib import Path
from qa_autopilot import scan_inbox
from release_gate import evaluate
from game_regression_lab import run_game,identify

ROOT=Path(__file__).resolve().parent

def once(inbox:Path,output:Path,trusted_game_browser=False,verbose=True):
    inbox.mkdir(parents=True,exist_ok=True);output.mkdir(parents=True,exist_ok=True)
    summary=scan_inbox(inbox,output,full_crc=True,verbose=verbose)
    try: state=json.loads((output/'state.json').read_text(encoding='utf-8'))
    except (OSError,ValueError):state={'files':{}}
    rows=[]
    for key,s in sorted(state['files'].items()):
        full_inbox=inbox/key
        report_dir=output/s['report_path']
        static_file=report_dir/'QA_REPORT.json'
        if not full_inbox.exists() or not static_file.exists():continue
        static=json.loads(static_file.read_text(encoding='utf-8'))
        game_file=report_dir/'GAME_QA.json'
        game=None
        if trusted_game_browser and identify(key)!='unknown':
            if not game_file.exists() or json.loads(game_file.read_text(encoding='utf-8')).get('sha256')!=s['sha256']:
                if verbose:print('[GAME] Browser test:',key,flush=True)
                game=run_game(full_inbox,report_dir,viewport='both',max_screenshots=2)
            else: game=json.loads(game_file.read_text(encoding='utf-8'))
        elif game_file.exists():
            potential=json.loads(game_file.read_text(encoding='utf-8'))
            if potential.get('sha256')==s['sha256']: game=potential
        approvals_dir=output/'APPROVALS';approvals_file=approvals_dir/(s['sha256'][:12]+'.json')
        approvals=json.loads(approvals_file.read_text(encoding='utf-8')) if approvals_file.is_file() else {}
        gate=evaluate(static,game,approvals)
        (report_dir/'RELEASE_GATE.json').write_text(json.dumps(gate,indent=2,ensure_ascii=False),encoding='utf-8')
        counts=(game or {}).get('summary',{})
        rows.append({'project':key,'sha256':s['sha256'],'decision':gate['decision'],'coverage':gate['coverage'],
                     'candidates':len(static.get('findings',[])),'game_pass':counts.get('PASS',0),
                     'game_fail':counts.get('FAIL',0)+counts.get('ERROR',0),'game_not_run':counts.get('NOT_RUN',0),
                     'reasons':'; '.join(gate['reasons']),'report_path':s['report_path']+'/QA_REPORT.html'})
    (output/'RELEASE_MATRIX.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with (output/'RELEASE_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['project','sha256','decision','coverage','candidates','game_pass','game_fail','game_not_run','reasons','report_path']);w.writeheader();w.writerows(rows)
    cards=''.join(f'<article class="card"><h2>{html.escape(r["project"])}</h2><b class="status">{html.escape(r["decision"])}</b><p>Static: {r["candidates"]} candidates · Browser PASS {r["game_pass"]} / FAIL {r["game_fail"]} / NOT_RUN {r["game_not_run"]}</p><p>{html.escape(r["reasons"])}</p><a href="{html.escape(r["report_path"],quote=True)}">QA report / Отчёт →</a></article>' for r in rows)
    page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>QA Release Matrix</title><style>:root{{color-scheme:dark}}body{{font:16px system-ui;background:#081427;color:#eaf5ff;max-width:1160px;margin:auto;padding:25px}}h1{{color:#54e9de}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:15px}}.card{{padding:18px;background:#142d43;border:1px solid #31536a;border-radius:17px}}.card h2{{font-size:17px;overflow-wrap:anywhere}}p{{color:#aebfd0}}a{{color:#7ee8f5}}.status{{color:#ffd989}}</style></head><body><h1>🔍 QA FACTORY v1.3 — RELEASE MATRIX</h1><p>EN: Evidence-based release decisions. RU: Решения о выпуске на основании проверок, а не предположений.</p><p><strong>READY_FOR_STAGING</strong> does NOT mean production-certified / не означает полностью готовый продукт.</p><p>Reports: {len(rows)}</p><div class="grid">{cards}</div></body></html>'''
    (output/'OPEN_RELEASE_MATRIX.html').write_text(page,encoding='utf-8')
    summary['release_matrix_count']=len(rows)
    summary['release_state_counts']={state:sum(r['decision']==state for r in rows) for state in ('BLOCKED','HOLD_FOR_REVIEW','READY_FOR_STAGING')}
    (output/'pipeline_run.json').write_text(json.dumps({'date':datetime.now(timezone.utc).isoformat(),'summary':summary},indent=2,ensure_ascii=False),encoding='utf-8')
    return summary

def main(argv=None):
    p=argparse.ArgumentParser(description='QA Factory v1.3 Pipeline')
    p.add_argument('mode',choices=('once','watch'),nargs='?',default='once')
    p.add_argument('--inbox',type=Path,default=ROOT/'QA_INBOX');p.add_argument('--output',type=Path,default=ROOT/'QA_RESULTS')
    p.add_argument('--trusted-game-browser',action='store_true',help='EXPLICIT opt-in to execute packaged JavaScript in isolated offline Chromium')
    p.add_argument('--interval',type=int,default=30)
    args=p.parse_args(argv)
    if args.mode=='once':
        result=once(args.inbox,args.output,args.trusted_game_browser)
        print(json.dumps(result,ensure_ascii=False));return 1 if result['failed'] or result['release_state_counts']['BLOCKED'] else 0
    print('Watching local ZIP folder, Ctrl+C exits. / Наблюдение за ZIP-папкой. Ctrl+C — выход.')
    try:
        while True:once(args.inbox,args.output,args.trusted_game_browser);time.sleep(max(10,args.interval))
    except KeyboardInterrupt:return 0
if __name__=='__main__':raise SystemExit(main())
