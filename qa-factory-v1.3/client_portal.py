#!/usr/bin/env python3
"""Local-only QA client intake. Not an internet-hosted SaaS or payment processor."""
from __future__ import annotations
import argparse, hashlib, html, io, json, os, re, secrets, threading, zipfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from qa_pipeline import once

ROOT=Path(__file__).resolve().parent
DB=ROOT/'CLIENT_REQUESTS'/'orders.json'
INBOX=ROOT/'QA_INBOX'
RESULTS=ROOT/'QA_RESULTS'
UI=ROOT/'ui'/'client_portal.html'
LOCK=threading.Lock()
MAX_UPLOAD=150*1024*1024

def utc():return datetime.now(timezone.utc).isoformat()
def load():
    if not DB.is_file():return {}
    return json.loads(DB.read_text(encoding='utf-8'))
def save(data):
    DB.parent.mkdir(parents=True,exist_ok=True)
    temp=DB.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(DB)
def clean(s,limit=90):return re.sub(r'[\x00-\x1f<>\\/]+',' ',str(s))[:limit].strip()
def public_order(x):
    return {k:x.get(k) for k in ('id','project','goal','status','created','filename','report_path','release_decision')}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,fmt,*args):print('[PORTAL]',fmt%args)
    def respond(self,status,body,mime='application/json; charset=utf-8',download=None):
        self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(body)))
        for k,v in {'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'none'; img-src 'self' data:; connect-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"}.items():self.send_header(k,v)
        if download:self.send_header('Content-Disposition','attachment; filename="'+download+'"')
        self.end_headers();self.wfile.write(body)
    def json(self,status,data):self.respond(status,json.dumps(data,ensure_ascii=False).encode())
    def authorized(self):
        origin=self.headers.get('Origin')
        expected='http://127.0.0.1:'+str(self.server.server_port)
        if origin and origin!=expected:return False
        return secrets.compare_digest(self.headers.get('X-QA-Token',''),self.server.qa_token)
    def read_json(self):
        sz=int(self.headers.get('Content-Length','0'))
        if sz<=0 or sz>12_000:raise ValueError('JSON request must be 1–12000 bytes')
        return json.loads(self.rfile.read(sz))
    def do_GET(self):
        u=urlparse(self.path);q=parse_qs(u.query)
        try:
            if u.path in ('/','/index.html'):
                page=UI.read_text(encoding='utf-8').replace('@@QA_CSRF_TOKEN@@',self.server.qa_token)
                self.respond(200,page.encode(),'text/html; charset=utf-8');return
            if u.path=='/api/health':self.json(200,{'ok':True,'local_only':True,'version':'1.3'});return
            if not self.authorized():self.json(403,{'error':'Access denied (local token required)'});return
            if u.path=='/api/orders':
                with LOCK:orders=load()
                self.json(200,{'orders':[public_order(x) for x in orders.values()]});return
            if u.path=='/api/report':
                oid=q.get('id',[''])[0]
                with LOCK:order=load().get(oid)
                if not order or not order.get('report_path'):self.json(404,{'error':'Report not available'});return
                path=RESULTS/order['report_path']/'QA_REPORT.html'
                if not path.is_file():self.json(404,{'error':'Missing report'});return
                self.respond(200,path.read_bytes(),'text/html; charset=utf-8');return
            if u.path=='/api/export':
                oid=q.get('id',[''])[0]
                with LOCK:order=load().get(oid)
                if not order or not order.get('report_path'):self.json(404,{'error':'Report not available'});return
                folder=RESULTS/order['report_path']
                if not folder.is_dir():self.json(404,{'error':'Missing report files'});return
                buffer=io.BytesIO()
                with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED) as z:
                    for p in folder.iterdir():
                        if p.is_file() and p.stat().st_size<15_000_000:z.write(p,p.name)
                self.respond(200,buffer.getvalue(),'application/zip','QA_CLIENT_REPORT_'+oid+'.zip');return
            self.json(404,{'error':'Not found'})
        except Exception as e:self.json(500,{'error':type(e).__name__+': '+str(e)[:100]})
    def do_POST(self):
        if not self.authorized():self.json(403,{'error':'Request rejected. Open the local portal first.'});return
        u=urlparse(self.path);q=parse_qs(u.query)
        try:
            if u.path=='/api/new':
                v=self.read_json()
                if v.get('authorized') is not True:raise ValueError('Permission checkbox required')
                project=clean(v.get('project',''),80)
                if len(project)<3:raise ValueError('Enter a project name of at least 3 characters')
                oid=secrets.token_hex(7)
                info={'id':oid,'project':project,'goal':clean(v.get('goal',''),400),
                      'contact':clean(v.get('contact',''),120),'authorized':True,
                      'created':utc(),'status':'WAITING_FOR_ZIP','filename':None,'report_path':None,'release_decision':None}
                with LOCK:
                    db=load();db[oid]=info;save(db)
                self.json(201,{'order':public_order(info)});return
            if u.path=='/api/upload':
                oid=q.get('id',[''])[0]
                with LOCK: info=load().get(oid)
                if not info:raise ValueError('Unknown request ID')
                length=int(self.headers.get('Content-Length','0'))
                if length<24 or length>MAX_UPLOAD:raise ValueError('ZIP must be between 24 bytes and 150 MB')
                dest=INBOX/(f'CLIENT_{oid}.zip');INBOX.mkdir(parents=True,exist_ok=True)
                temp=dest.with_suffix('.tmp')
                with temp.open('wb') as f:
                    left=length
                    while left:
                        block=self.rfile.read(min(2*1024*1024,left))
                        if not block:raise ValueError('Incomplete upload')
                        f.write(block);left-=len(block)
                if not zipfile.is_zipfile(temp):temp.unlink(missing_ok=True);raise ValueError('Uploaded data is not a ZIP')
                temp.replace(dest)
                with LOCK:
                    db=load();db[oid]['status']='UPLOADED';db[oid]['filename']=dest.name;save(db)
                self.json(200,{'id':oid,'status':'UPLOADED','filename':dest.name});return
            if u.path=='/api/scan':
                oid=str(self.read_json().get('id',''))
                with LOCK:info=load().get(oid)
                if not info or info.get('status') not in ('UPLOADED','COMPLETE'):raise ValueError('Upload a ZIP first')
                # Local-only static checks. Browser-execution intentionally not offered via this endpoint.
                res=once(INBOX,RESULTS,trusted_game_browser=False,verbose=False)
                with LOCK:
                    db=load();info=db[oid];state=json.loads((RESULTS/'state.json').read_text(encoding='utf-8'))
                    entry=state['files'].get(info['filename'])
                    if entry:
                        gate=json.loads((RESULTS/entry['report_path']/'RELEASE_GATE.json').read_text(encoding='utf-8'))
                        info['status']='COMPLETE';info['report_path']=entry['report_path'];info['release_decision']=gate['decision']
                    else:info['status']='SCAN_FAILED'
                    save(db)
                self.json(200,{'order':public_order(info),'scan':res});return
            self.json(404,{'error':'Unknown endpoint'})
        except Exception as exc:self.json(400,{'error':str(exc)[:250]})

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8790);p.add_argument('--no-open',action='store_true');args=p.parse_args(argv)
    DB.parent.mkdir(parents=True,exist_ok=True);INBOX.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.qa_token=secrets.token_urlsafe(28)
    url=f'http://127.0.0.1:{args.port}'
    print('QA CLIENT PORTAL — LOCAL ONLY',url,'\nClose this terminal to stop. Do not deploy to public hosting.')
    if not args.no_open:
        import webbrowser
        threading.Timer(1.0,lambda:webbrowser.open(url)).start()
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=='__main__':main()
