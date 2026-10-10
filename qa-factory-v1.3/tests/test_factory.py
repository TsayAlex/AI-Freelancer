import io, json, os, sys, threading, unittest, zipfile
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.request import urlopen,Request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qa_engine import scan_zip_bytes,scan_url,ScanError,safe_path,normalize_local,validate_address,scan_public_github_repo
from reports import make_html,make_markdown,make_csv,archive_report
from server import Handler,RUNS

ROOT=Path(__file__).resolve().parents[1]
def zip_bytes(files):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        for k,v in files.items():z.writestr(k,v)
    return b.getvalue()

class EngineTests(unittest.TestCase):
    def test_known_broken(self):
        blob=(ROOT/'sample_projects'/'broken_demo.zip').read_bytes()
        r=scan_zip_bytes(blob,'broken_demo.zip')
        codes={f['code'] for f in r['findings']}
        for x in ('BROKEN_REFERENCE','MOBILE_VIEWPORT','SEO_TITLE','LANG','EMAIL_TYPE','IMAGE_ALT'):
            self.assertIn(x,codes)
        self.assertEqual(r['quality_gate'],'REVIEW_REQUIRED')
        self.assertGreaterEqual(len(r['findings']),6)
    def test_clean(self):
        blob=(ROOT/'sample_projects'/'clean_demo.zip').read_bytes()
        r=scan_zip_bytes(blob,'clean_demo.zip')
        self.assertEqual(r['metrics']['findings_total'],0)
        self.assertEqual(r['quality_gate'],'NO_DETECTED_ISSUES')
    def test_unsafe_zip_path(self):
        for name in ('../private.txt','/absolute.html','C:/file.html','a/../../x.html'):
            with self.subTest(name=name):
                with self.assertRaises(ScanError):scan_zip_bytes(zip_bytes({name:'x'}))
    def test_invalid_json(self):
        r=scan_zip_bytes(zip_bytes({'index.html':'<html lang="en"><title>A</title><meta name="viewport" content="width=device-width"><meta name="description" content="x"><h1>Hello</h1></html>','data.json':'{"bad":'}))
        self.assertIn('INVALID_JSON',{f['code'] for f in r['findings']})
    def test_ssrf(self):
        for url in ('http://127.0.0.1','http://169.254.169.254','file:///etc/passwd','http://10.0.0.1'):
            with self.subTest(url=url):
                with self.assertRaises(ScanError):validate_address(url)
    def test_local_resolution(self):
        self.assertEqual(normalize_local('pages/index.html','../assets/logo.png'),'assets/logo.png')
        self.assertEqual(normalize_local('index.html','../private'), '__OUTSIDE__')
        self.assertFalse(safe_path('x/../z'))
    def test_github_input_restrictions(self):
        for bad in ('http://github.com/x/y', 'https://evil.com/x/y','https://github.com/x', 'https://github.com/x/y?token=x'):
            with self.subTest(url=bad):
                with self.assertRaises(ScanError):scan_public_github_repo(bad)
    def test_browser_preview_offline(self):
        try:import playwright
        except ImportError:self.skipTest('Optional Playwright not installed')
        from browser_check import run_preview
        r=scan_zip_bytes((ROOT/'sample_projects'/'broken_demo.zip').read_bytes(),browser=True,on_browser=run_preview)
        self.assertEqual(set(r['evidence']),{'desktop.png','mobile.png'})
        self.assertGreater(len(r['_evidence_bytes']['desktop.png']),1000)
        self.assertIn('EMAIL_BROWSER_VALIDATION',{x['code'] for x in r['findings']})
    def test_local_url_crawler(self):
        class Site(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(404 if self.path=='/missing.html' else 200)
                self.send_header('Content-Type','text/html');self.end_headers()
                self.wfile.write(("<html lang='en'><head><title>URL Test</title><meta name='viewport' content='width=device-width'><meta name='description' content='x'></head><body><h1>Hello</h1><a href='/missing.html'>Dead</a></body></html>").encode())
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Site);t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
        try:
            r=scan_url(f'http://127.0.0.1:{server.server_port}/',allow_local=True,max_pages=3)
            self.assertIn('HTTP_STATUS',{f['code'] for f in r['findings']})
            self.assertEqual(r['metrics']['pages_visited'],2)
        finally:server.shutdown();server.server_close();t.join(timeout=2)
    def test_exports(self):
        r=scan_zip_bytes((ROOT/'sample_projects'/'broken_demo.zip').read_bytes())
        self.assertIn('BROKEN_REFERENCE',make_markdown(r))
        self.assertIn('<html',make_html(r))
        self.assertIn('id,code,severity',make_csv(r))
        b=archive_report(r)
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            for n in ('QA_REPORT.json','QA_REPORT.html','QA_REPORT.md','BUGS.csv'):
                self.assertIn(n,z.namelist())
            self.assertGreater(len(z.read('QA_REPORT.html')),500)

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)
    def test_frontend_and_health(self):
        self.assertIn('ALEX AI QA FACTORY',urlopen(self.base).read().decode())
        h=json.load(urlopen(self.base+'/api/health'))
        self.assertTrue(h['ok']);self.assertTrue(h['features']['zip'])
    def test_api_zip_history_triage_exports(self):
        data=(ROOT/'sample_projects'/'broken_demo.zip').read_bytes()
        req=Request(self.base+'/api/scan-zip',data=data,headers={'Content-Type':'application/zip','X-File-Name':'demo.zip'},method='POST')
        scanned=json.load(urlopen(req));r=scanned['report'];rid=r['id']
        self.assertGreater(len(r['findings']),0)
        history=json.load(urlopen(self.base+'/api/history'))
        self.assertTrue(any(x['id']==rid for x in history['items']))
        issue=r['findings'][0]['id'];body=json.dumps({'id':rid,'finding_id':issue,'status':'confirmed'}).encode()
        review=json.load(urlopen(Request(self.base+'/api/triage',data=body,headers={'Content-Type':'application/json'},method='POST')))
        self.assertEqual(review['report']['findings'][0]['review'],'confirmed')
        archive=urlopen(self.base+'/api/download?id='+rid).read()
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            self.assertIn('QA_REPORT.html',z.namelist())
        self.assertIn(b'demo.zip',urlopen(self.base+'/api/report-html?id='+rid).read())

if __name__=='__main__':unittest.main()
