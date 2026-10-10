import io,json,sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qa_autopilot import inspect_archive, scan_inbox, delta, family_of, sha256_file
from qa_engine import ScanError

def writezip(path, content):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,source in content.items():z.writestr(name,source)

HTML='<html lang="en"><head><meta name="viewport" content="width=device-width"><meta name="description" content="test"><title>Test</title></head><body><h1>Test</h1></body></html>'
class AutopilotTests(unittest.TestCase):
    def test_archive_real_reports(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'app.zip'
            writezip(p,{'index.html':HTML+'<a href="missing.html">oops</a>','data.json':'{}'})
            r=inspect_archive(p)
            self.assertTrue(r['autopilot']['source_sha256'])
            self.assertIn('BROKEN_REFERENCE',{f['code'] for f in r['findings']})
            self.assertIn('Full ZIP CRC verification',r['checked'])
    def test_large_over_25_megs_supported_without_executing(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'large.zip'
            
            with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_STORED) as z:
                z.writestr('index.html',HTML)
                z.writestr('many.bin',b'0'*26_000_000)
            r=inspect_archive(p,full_crc=False)
            self.assertEqual(r['quality_gate'],'INCOMPLETE')
            self.assertEqual(r['metrics']['text_files_checked'],1)
    def test_unsafe_paths_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'unsafe.zip';writezip(p,{'../private.txt':'x'})
            with self.assertRaises(ScanError):inspect_archive(p)
    def test_incremental_state_and_dashboard(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); inbox=td/'QA_INBOX';out=td/'QA_RESULTS';inbox.mkdir()
            p=inbox/'OUR_SITE_v1.zip';writezip(p,{'index.html':HTML+'<a href="oldmissing.html">dead</a>'})
            first=scan_inbox(inbox,out,verbose=False)
            self.assertEqual(first['scanned'],1)
            second=scan_inbox(inbox,out,verbose=False)
            self.assertEqual(second['skipped_unchanged'],1)
            writezip(p,{'index.html':HTML})
            third=scan_inbox(inbox,out,verbose=False)
            self.assertEqual(third['scanned'],1)
            state=json.loads((out/'state.json').read_text())
            record=state['files']['OUR_SITE_v1.zip']
            report=json.loads((out/record['report_path']/'QA_REPORT.json').read_text())
            self.assertGreaterEqual(len(report['autopilot']['delta']['resolved_candidates']),1)
            self.assertTrue((out/'OPEN_DASHBOARD.html').is_file())
            self.assertTrue((out/record['report_path']/'BUGS.csv').is_file())
    def test_family_diff(self):
        self.assertEqual(family_of('ALEX_AQUARIUM_v9_FINAL.zip'),family_of('ALEX_AQUARIUM_v10_FINAL.zip'))
    def test_unreadable_zip_marked_fail_not_fake_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'in').mkdir()
            (root/'in'/'broken.zip').write_bytes(b'not a zip')
            s=scan_inbox(root/'in',root/'out',verbose=False)
            self.assertEqual(s['failed'],1)
            self.assertTrue(s['errors'])

if __name__=='__main__':unittest.main()
