import io,json,sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from release_gate import evaluate
from game_regression_lab import identify,safe_member,choose_entry
from qa_pipeline import once

def fixture():
 return {'name':'sample.zip','quality_gate':'NO_DETECTED_ISSUES','autopilot':{'coverage':'STATIC_ONLY'},'findings':[]}
class GateTests(unittest.TestCase):
 def test_unverified_static_holds(self):
  r=evaluate(fixture());self.assertEqual(r['decision'],'HOLD_FOR_REVIEW')
 def test_confirmed_major_blocks(self):
  r=fixture();r['findings']=[{'severity':'major','review':'confirmed'}]
  self.assertEqual(evaluate(r)['decision'],'BLOCKED')
 def test_failed_game_blocks(self):
  g={'tests':[{'status':'FAIL','test':'smoke'}]}
  self.assertEqual(evaluate(fixture(),g)['decision'],'BLOCKED')
 def test_notrun_holds(self):
  g={'tests':[{'status':'PASS'},{'status':'NOT_RUN'}]}
  self.assertEqual(evaluate(fixture(),g,{'human_qa_approval':True,'security_privacy_review':True,'deployment_target_verified':True})['decision'],'HOLD_FOR_REVIEW')
 def test_approved_stage_is_not_production(self):
  g={'tests':[{'status':'PASS'}]};a={'human_qa_approval':True,'security_privacy_review':True,'deployment_target_verified':True}
  r=evaluate(fixture(),g,a);self.assertEqual(r['decision'],'READY_FOR_STAGING');self.assertIn('NOT production',r['disclaimer_en'])
 def test_candidates_hold_even_with_all_approvals(self):
  r=fixture();r['findings']=[{'severity':'minor','review':'candidate'}]
  g={'tests':[{'status':'PASS'}]};a={'human_qa_approval':True,'security_privacy_review':True,'deployment_target_verified':True}
  self.assertEqual(evaluate(r,g,a)['decision'],'HOLD_FOR_REVIEW')
 def test_game_contract_identify(self):
  for n,v in [('CHESS4_V8.zip','chess'),('ALEX_AQUARIUM_V9.zip','aquarium'),('ALEX_FIGHT_LEGENDS_v19.zip','fight'),('myapp.zip','unknown')]:self.assertEqual(identify(n),v)
 def test_traversal_rejected(self):
  self.assertFalse(safe_member('../bad.txt'))
  with zipfile.ZipFile(io.BytesIO(),'w') as _:pass
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'z.zip'
   with zipfile.ZipFile(p,'w') as z:z.writestr('../index.html','<html></html>')
   with zipfile.ZipFile(p) as z:
    with self.assertRaises(ValueError):choose_entry(z,'chess')
 def test_pipeline_own_inbox_and_report(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);(root/'in').mkdir();p=root/'in'/'example.zip'
   with zipfile.ZipFile(p,'w') as z:z.writestr('index.html','<!doctype html><html lang="en"><head><title>Test</title><meta name="viewport" content="width=device-width"></head><body><h1>Hi</h1></body></html>')
   first=once(root/'in',root/'out',False,False)
   self.assertEqual(first['scanned'],1)
   rows=json.loads((root/'out'/'RELEASE_MATRIX.json').read_text(encoding='utf8'))
   self.assertEqual(len(rows),1);self.assertEqual(rows[0]['decision'],'HOLD_FOR_REVIEW')
   self.assertTrue((root/'out'/'OPEN_RELEASE_MATRIX.html').exists())
   again=once(root/'in',root/'out',False,False)
   self.assertEqual(again['skipped_unchanged'],1)
if __name__=='__main__':unittest.main()
