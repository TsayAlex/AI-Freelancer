"""ALEX AI QA FACTORY v1.0: local-only API and polished UI. Python 3.10+."""
from __future__ import annotations
import argparse
import io
import json
import os
from pathlib import Path
import shutil
import threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs,unquote
import webbrowser

from qa_engine import ScanError,scan_zip_bytes,scan_url,scan_public_github_repo,finish,MAX_ZIP_BYTES
from reports import make_html,archive_report
from browser_check import run_preview

ROOT=Path(__file__).resolve().parent
RUNS=ROOT/'data'/'runs';RUNS.mkdir(parents=True,exist_ok=True)
UI=ROOT/'ui'/'index.html'


def load_report(run_id):
    if not (len(run_id)==12 and all(c in '0123456789abcdef' for c in run_id)):
        raise FileNotFoundError('Invalid scan ID')
    path=RUNS/run_id/'report.json'
    if not path.is_file():raise FileNotFoundError('Unknown scan ID')
    return json.loads(path.read_text(encoding='utf-8'))

def store_report(report):
    evidence=report.pop('_evidence_bytes',{})
    folder=RUNS/report['id'];folder.mkdir(parents=True,exist_ok=True)
    for name,content in evidence.items():
        if Path(name).name==name and name.endswith('.png'):
            (folder/name).write_bytes(content)
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

class Handler(BaseHTTPRequestHandler):
    server_version='AlexQA/1.0'
    def log_message(self,format,*args):
        print('[QA]',format%args)
    def headers_common(self):
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY')
        self.send_header('Cache-Control','no-store')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; img-src 'self' data:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
    def send_bytes(self,status,body,mime='application/json; charset=utf-8',filename=None):
        self.send_response(status);self.send_header('Content-Type',mime)
        self.headers_common();self.send_header('Content-Length',str(len(body)))
        if filename:self.send_header('Content-Disposition',f'attachment; filename="{filename}"')
        self.end_headers()
        try:self.wfile.write(body)
        except (ConnectionResetError,BrokenPipeError):pass
    def respond(self,code,obj): self.send_bytes(code,json.dumps(obj,ensure_ascii=False).encode('utf-8'))
    def do_GET(self):
        p=urlparse(self.path);query=parse_qs(p.query)
        try:
            if p.path in ('/','/index.html'):
                self.send_bytes(200,UI.read_bytes(),'text/html; charset=utf-8');return
            if p.path=='/api/health':
                try:import playwright;pw=True
                except ImportError:pw=False
                try:import reportlab;pdf=True
                except ImportError:pdf=False
                try:import docx;doc=True
                except ImportError:doc=False
                self.respond(200,{'ok':True,'version':'1.0.0','local_only':True,'features':{'zip':True,'url':True,'github_public':True,'browser':pw,'pdf':pdf,'docx':doc,'node_syntax':bool(shutil.which('node'))}});return
            if p.path=='/api/demo-zip':
                demo=ROOT/'sample_projects'/'broken_demo.zip'
                if not demo.is_file():raise FileNotFoundError('Demo ZIP unavailable')
                self.send_bytes(200,demo.read_bytes(),'application/zip','ALEX_QA_BROKEN_DEMO.zip');return
            if p.path=='/api/history':
                items=[]
                for f in sorted(RUNS.glob('*/report.json'),key=lambda x:x.stat().st_mtime,reverse=True)[:60]:
                    try:
                        r=json.loads(f.read_text(encoding='utf-8'))
                        items.append({'id':r['id'],'name':r['name'],'started_at':r['started_at'],'kind':r['kind'],'issues':len(r['findings']),'gate':r['quality_gate']})
                    except (OSError,ValueError,KeyError):pass
                self.respond(200,{'items':items});return
            if p.path in ('/api/result','/api/download','/api/report-html'):
                run=query.get('id',[''])[0];r=load_report(run)
                if p.path=='/api/result':self.respond(200,r);return
                if p.path=='/api/report-html':
                    page=make_html(r)
                    for evidence in r.get('evidence',[]):
                        page=page.replace(f'href="evidence/{evidence}"',f'href="/api/evidence/{run}/{evidence}"')
                    self.send_bytes(200,page.encode(),'text/html; charset=utf-8');return
                self.send_bytes(200,archive_report(r,RUNS/run),'application/zip',f'ALEX_QA_{run}.zip');return
            if p.path.startswith('/api/evidence/'):
                bits=p.path.split('/')
                if len(bits)!=5 or bits[-1] not in ('desktop.png','mobile.png'):raise FileNotFoundError('Not found')
                r=load_report(bits[3]);file=RUNS/r['id']/bits[4]
                if not file.is_file():raise FileNotFoundError('Screenshot unavailable')
                self.send_bytes(200,file.read_bytes(),'image/png');return
            self.respond(404,{'error':'Not found'})
        except FileNotFoundError as e:self.respond(404,{'error':str(e)})
        except Exception as e:
            print('GET error',repr(e));self.respond(500,{'error':'Internal server error'})
    def read_payload(self,limit):
        try:size=int(self.headers.get('Content-Length','0'))
        except ValueError:raise ScanError('Invalid request size')
        if size<=0 or size>limit:raise ScanError(f'Body must be 1–{limit//(1024*1024)} MB.')
        return self.rfile.read(size)
    def do_POST(self):
        # Reject cross-origin browser POSTs to this local unauthenticated service.
        origin=self.headers.get('Origin')
        if origin:
            op=urlparse(origin)
            target=f'http://127.0.0.1:{self.server.server_port}'
            if origin!=target:
                self.respond(403,{'error':'Cross-origin requests are not allowed.'});return
        p=urlparse(self.path)
        try:
            if p.path=='/api/scan-zip':
                blob=self.read_payload(MAX_ZIP_BYTES)
                rawname=self.headers.get('X-File-Name','uploaded.zip')
                # File name is display-only; not used as filesystem path.
                name=Path(unquote(rawname).replace('\\','/')).name[:100] or 'uploaded.zip'
                do_browser=self.headers.get('X-Browser-Preview','false').lower()=='true'
                report=scan_zip_bytes(blob,name,do_browser,run_preview)
                store_report(report);self.respond(200,{'id':report['id'],'report':report});return
            if p.path=='/api/scan-repo':
                payload=json.loads(self.read_payload(8000))
                link=str(payload.get('url',''))[:1000]
                branch=str(payload.get('branch',''))[:120]
                report=scan_public_github_repo(link,branch,False,None)
                store_report(report);self.respond(200,{'id':report['id'],'report':report});return
            if p.path=='/api/scan-url':
                payload=json.loads(self.read_payload(8000))
                url=str(payload.get('url',''))[:1000]
                report=scan_url(url,allow_local=os.environ.get('ALEX_ALLOW_LOCAL_URL')=='1',max_pages=min(12,max(1,int(payload.get('pages',8)))))
                store_report(report);self.respond(200,{'id':report['id'],'report':report});return
            if p.path=='/api/triage':
                payload=json.loads(self.read_payload(16000));r=load_report(str(payload.get('id','')))
                status=str(payload.get('status',''))
                if status not in ('candidate','confirmed','rejected'):raise ScanError('Invalid review status')
                found=next((x for x in r['findings'] if x['id']==payload.get('finding_id')),None)
                if not found:raise ScanError('Issue not found')
                found['review']=status;finish(r);store_report(r);self.respond(200,{'report':r});return
            self.respond(404,{'error':'Unknown endpoint'})
        except (ScanError,ValueError,TypeError,KeyError) as e:self.respond(400,{'error':str(e)})
        except Exception as e:
            print('POST error',repr(e));self.respond(500,{'error':'Unexpected scan error. See local terminal for details.'})


def main():
    parser=argparse.ArgumentParser(description='ALEX AI QA FACTORY — local browser app')
    parser.add_argument('--port',type=int,default=8787);parser.add_argument('--no-open',action='store_true')
    args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    url=f'http://127.0.0.1:{server.server_port}'
    print('\nALEX AI QA FACTORY v1.0 — RUNNING')
    print('Open in browser:',url)
    print('Local-only server. ZIP files remain on this computer. Ctrl+C stops.\n')
    if not args.no_open:threading.Timer(1.1,lambda:webbrowser.open(url)).start()
    try:server.serve_forever()
    except KeyboardInterrupt: print('Stopping...')
    finally:server.server_close()

if __name__=='__main__':main()
