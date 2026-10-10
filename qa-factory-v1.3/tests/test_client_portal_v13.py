import io,json,sys,tempfile,threading,unittest,urllib.request,urllib.error,zipfile
from http.server import ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import client_portal

class PortalTests(unittest.TestCase):
 def test_local_end_to_end(self):
  old=(client_portal.DB,client_portal.INBOX,client_portal.RESULTS)
  try:
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    client_portal.DB=root/'requests'/'orders.json';client_portal.INBOX=root/'in';client_portal.RESULTS=root/'out'
    server=ThreadingHTTPServer(('127.0.0.1',0),client_portal.Handler);server.qa_token='test-token'
    thr=threading.Thread(target=server.serve_forever,daemon=True);thr.start()
    base='http://127.0.0.1:'+str(server.server_port)
    def req(endpoint,post=None,token='test-token',ctype='application/json'):
     hdr={'X-QA-Token':token}
     if post is not None:hdr['Content-Type']=ctype
     with urllib.request.urlopen(urllib.request.Request(base+endpoint,data=post,headers=hdr,method='POST' if post is not None else 'GET'),timeout=40) as f:
      blob=f.read();return json.loads(blob) if f.headers['Content-Type'].startswith('application/json') else blob
    try:
     with self.assertRaises(urllib.error.HTTPError) as e:req('/api/orders',token='invalid')
     self.assertEqual(e.exception.code,403)
     with self.assertRaises(urllib.error.HTTPError) as e:req('/api/new',json.dumps({'project':'Sample','authorized':False}).encode())
     self.assertEqual(e.exception.code,400)
     info=req('/api/new',json.dumps({'project':'Sample QA Customer','authorized':True}).encode())
     oid=info['order']['id']
     buf=io.BytesIO()
     with zipfile.ZipFile(buf,'w') as z:z.writestr('index.html','<!doctype html><html lang="en"><head><title>QA</title></head><body><h1>Test</h1></body></html>')
     self.assertEqual(req('/api/upload?id='+oid,buf.getvalue(),ctype='application/zip')['status'],'UPLOADED')
     result=req('/api/scan',json.dumps({'id':oid}).encode())
     self.assertEqual(result['order']['status'],'COMPLETE')
     self.assertEqual(result['order']['release_decision'],'HOLD_FOR_REVIEW')
     data=req('/api/export?id='+oid)
     with zipfile.ZipFile(io.BytesIO(data)) as z:self.assertIn('RELEASE_GATE.json',z.namelist())
    finally:
     server.shutdown();server.server_close();thr.join(timeout=4)
  finally:client_portal.DB,client_portal.INBOX,client_portal.RESULTS=old
if __name__=='__main__':unittest.main()
