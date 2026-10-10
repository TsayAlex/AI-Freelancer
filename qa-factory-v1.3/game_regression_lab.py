#!/usr/bin/env python3
"""Opt-in Chromium browser game UI smoke/regression on known user-owned ZIPs.

WARNING: Executes embedded browser JavaScript from the project; use a trusted
local test machine, never in a shared production server. Network blocked.
Does not evaluate auditory quality or GPU rendering correctness.
"""
from __future__ import annotations
import argparse, hashlib, json, mimetypes, re, shutil, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit,unquote

STORAGE_JS="""() => {for(const k of ['localStorage','sessionStorage']){const db=new Map();Object.defineProperty(window,k,{configurable:true,value:{get length(){return db.size},key(i){return [...db.keys()][i]??null},getItem(k){return db.get(String(k))??null},setItem(k,v){db.set(String(k),String(v))},removeItem(k){db.delete(String(k))},clear(){db.clear()}}})}}"""

def identify(name):
    n=name.upper()
    return ('chess' if 'CHESS4' in n or 'FOUR_KINGDOM' in n else
            'aquarium' if 'AQUARIUM' in n else
            'fight' if 'FIGHT_LEGENDS' in n else 'unknown')

def safe_member(x):
    from pathlib import PurePosixPath
    p=PurePosixPath(x.replace('\\','/'))
    return not p.is_absolute() and '..' not in p.parts and '\x00' not in x

def choose_entry(z,kind):
    names=z.namelist()
    if len(names)>8000:raise ValueError('ZIP entry limit exceeded')
    if any(not safe_member(n) for n in names):raise ValueError('Unsafe archive member path')
    if sum(i.file_size for i in z.infolist())>900_000_000:raise ValueError('Uncompressed ZIP over limit')
    entries=[x for x in names if x.lower().endswith('/index.html') or x.lower()=='index.html']
    # Fight v19 ships index in a prefix; aquarium and chess have flat indexes.
    entries.sort(key=lambda x:(x.count('/'),len(x)))
    if not entries:raise ValueError('No index.html in ZIP')
    return entries[0]

def run_game(source:Path,out:Path,viewport='both',max_screenshots=3):
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    kind=identify(source.name)
    output={'schema':'alexqa.game_regression.v1','filename':source.name,'sha256':sha,'game_type':kind,
            'generated_at':datetime.now(timezone.utc).isoformat(),'tests':[],
            'limitations':['Offline headless Chromium only','Browser JS executed ONLY after explicit runner invocation',
              'No verification of physical GPU/WebGL quality, audio listening, real touch latency, multiplayer or server APIs',
              'No external network requests allowed; in-memory storage shim may not reflect real persistence']}
    out.mkdir(parents=True,exist_ok=True)
    def add(name,condition=None,detail='',status=None,evidence=None):
        row={'test':name,'status':status or ('PASS' if condition else 'FAIL'),'detail':str(detail)[:320]}
        if evidence:row['evidence']=evidence
        output['tests'].append(row)
    if kind=='unknown':
        add('Unsupported game archive',status='NOT_RUN',detail='No known game contract for this ZIP')
        return save(out,output)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        add('Browser dependency not installed',status='NOT_RUN',detail='pip install playwright; python -m playwright install chromium')
        return save(out,output)
    try:
        z=zipfile.ZipFile(source)
        entry=choose_entry(z,kind)
        asset_root=entry.rsplit('/',1)[0]+'/' if '/' in entry else ''
        if z.getinfo(entry).file_size>20_000_000:raise ValueError('HTML page exceeds 20MB')
        html=z.read(entry).decode('utf-8',errors='replace')
        if '<head' not in html.lower():raise ValueError('No HTML head')
    except Exception as exc:
        add('Read HTML from ZIP',status='ERROR',detail=str(exc));return save(out,output)
    for viewport_config in (([('desktop',1365,850),('mobile',390,844)] if viewport=='both' else [('mobile',390,844)] if viewport=='mobile' else [('desktop',1365,850)])):
        label,w,h=viewport_config
        ctx=None
        try:
            with sync_playwright() as p:
                options={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage','--disable-gpu-sandbox','--enable-unsafe-swiftshader']}
                binary=shutil.which('chromium') or shutil.which('google-chrome')
                if binary:options['executable_path']=binary
                browser=p.chromium.launch(**options)
                ctx=browser.new_context(viewport={'width':w,'height':h},has_touch=(label=='mobile'),is_mobile=(label=='mobile'),service_workers='block')
                page=ctx.new_page();errors=[];blocked=[]
                page.on('pageerror',lambda exc:errors.append(str(exc)[:250]))
                names=set(z.namelist())
                def route(route):
                    u=urlsplit(route.request.url)
                    if u.hostname!='qa-assets.invalid':
                        blocked.append(route.request.url[:180]);route.abort('blockedbyclient');return
                    path=unquote(u.path).lstrip('/')
                    # A resolved root cannot escape its ZIP package prefix.
                    path=asset_root+path
                    if not safe_member(path) or path not in names:
                        route.fulfill(status=404,body='Not Found');return
                    info=z.getinfo(path)
                    if info.file_size>30_000_000:
                        route.fulfill(status=413,body='Oversized resource');return
                    mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
                    route.fulfill(status=200,body=z.read(path),headers={'Content-Type':mime,'Access-Control-Allow-Origin':'*'})
                page.route('**/*',route)
                page.evaluate(STORAGE_JS)
                page.set_content(re.sub(r'<head([^>]*)>',r'<head\1><base href="https://qa-assets.invalid/">',html,count=1,flags=re.I),wait_until='domcontentloaded',timeout=25000)
                page.wait_for_timeout(230)
                add(label+' HTML loaded',page.locator('body').count()>0)
                if kind=='chess':test_chess(page,add,label)
                if kind=='aquarium':test_aquarium(page,add,label)
                if kind=='fight':test_fight(page,add,label)
                if max_screenshots:
                    dest=out/(kind+'_'+label+'.png')
                    page.screenshot(path=str(dest),animations='disabled',timeout=9000)
                    add(label+' screenshot captured',True,evidence=dest.name)
                add(label+' no uncaught JS exceptions',not errors,json.dumps(errors,ensure_ascii=False)[:300])
                add(label+' external network blocked',True,f'{len(blocked)} blocked external requests')
                ctx.close();browser.close();ctx=None
        except Exception as exc:
            add(label+' runner completed',status='ERROR',detail=repr(exc)[:300])
            if ctx:
                try:ctx.close()
                except Exception:pass
    try:z.close()
    except Exception:pass
    return save(out,output)

def test_chess(pg,add,label):
    add(label+' board has 196 cells',pg.locator('#board .cell').count()==196,pg.locator('#board .cell').count())
    for locale in ('en','uk','ru'):
        try:
            pg.locator('#lang').select_option(locale,timeout=4000)
            add(label+' switch language '+locale,pg.locator('#lang').input_value()==locale)
        except Exception as exc:add(label+' switch language '+locale,detail=repr(exc),status='ERROR')
    try:
        pg.locator('#v8View').select_option('2d',timeout=4000)
        pg.locator('#modePreset').select_option('hotseat',timeout=4000)
        def board():return pg.locator('#board .cell').all_text_contents()
        before=board()
        selected=pg.evaluate("""() => {for (const el of document.querySelectorAll('#board .cell:has(.piece)')) {el.click();if(document.querySelector('#board .cell.to,#board .cell.cap'))return true}return false}""")
        add(label+' selectable legal move',selected)
        if selected:
            pg.locator('#board .cell.to,#board .cell.cap').first.click(timeout=4000)
            add(label+' real move changes board',board()!=before)
            pg.locator('#undoBtn').click(timeout=4000)
            add(label+' undo restores board',board()==before)
    except Exception as exc:add(label+' chess move and undo',status='ERROR',detail=repr(exc))

def test_aquarium(pg,add,label):
    try:
        pg.locator('#startGameBtn').click(timeout=5000)
        add(label+' start game button',not pg.locator('#startGameBtn').is_visible())
        pg.locator('#openFishArtistTop').click(timeout=4500)
        c=pg.locator('#artistCanvas')
        add(label+' editor canvas visible',c.is_visible())
        before=c.evaluate('(x)=>x.toDataURL()')
        box=c.bounding_box()
        if box:
            pg.mouse.move(box['x']+box['width']*.30,box['y']+box['height']*.40)
            pg.mouse.down();pg.mouse.move(box['x']+box['width']*.6,box['y']+box['height']*.53,steps=5);pg.mouse.up()
            pg.wait_for_timeout(100)
            add(label+' draw stroke changes canvas',c.evaluate('(x)=>x.toDataURL()')!=before)
        else:add(label+' draw stroke',status='NOT_RUN',detail='Canvas not laid out')
    except Exception as exc:add(label+' aquarium interaction',status='ERROR',detail=repr(exc))
    # Explicitly not claim WebGL passes on headless machines.
    add(label+' real 3D graphics verified',status='NOT_RUN',detail='Requires GPU-capable real device')

def test_fight(pg,add,label):
    try:
        pg.locator('#trainingBtn').click(timeout=5000)
        add(label+' training UI available',pg.locator('#trainSlow').is_visible())
        mappings=[(['up'],'punch','hammerPunch'),(['up','right'],'kick','mawashiKick'),(['right'],'kick','kick'),(['down','right'],'punch','lowAnglePunch'),(['down'],'punch','crouchPunch'),(['down'],'kick','sweep')]
        for keys,action,expected in mappings:
            got=pg.evaluate('''x=>{const a=ALEX_GAME.fighters[0],b=ALEX_GAME.fighters[1];a.move=null;a.y=0;a.vy=0;a.crouch=x.keys.includes('down');a.face=1;return ALEX_TEST.resolve(a,b,new Set(x.keys),x.action)}''',{'keys':keys,'action':action})
            add(label+' direction '+','.join(keys)+' '+action,got==expected,f'expected={expected}; actual={got}')
    except Exception as exc:add(label+' fight interactions',status='ERROR',detail=repr(exc))
    add(label+' natural music quality evaluated',status='NOT_RUN',detail='Requires human listening on device')

def save(out,report):
    counts={s:sum(x['status']==s for x in report['tests']) for s in ('PASS','FAIL','ERROR','NOT_RUN','SKIPPED','OBSERVED')}
    report['summary']=counts
    (out/'GAME_QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('zip',type=Path);parser.add_argument('--output',type=Path,default=Path('GAME_TEST_REPORTS'))
    parser.add_argument('--viewport',choices=('both','desktop','mobile'),default='both')
    args=parser.parse_args(argv)
    r=run_game(args.zip,args.output,args.viewport)
    print(json.dumps({'source':r['filename'],'summary':r['summary'],'output':str(args.output/'GAME_QA.json')},ensure_ascii=False))
    return 2 if r['summary']['FAIL']+r['summary']['ERROR'] else 0
if __name__=='__main__':raise SystemExit(main())
