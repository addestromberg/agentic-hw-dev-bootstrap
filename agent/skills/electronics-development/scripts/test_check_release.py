"""Behavioural tests in isolated temporary projects; no real evidence is promoted."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from check_release import assess, sha, STAGES


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'board.pcb').write_text('fixture design')
        (self.root/'result.txt').write_text('fixture result, not physical evidence')
        self.config = self.root/'config.json'
        self.config.write_text(json.dumps({'schema_version':1,'board':'fixture','revision':'1','project_root':'.',
                                          'design_inputs':['board.pcb'],'evidence_file':'records.json'}))
        r={'status':'passed','kind':'measurement','acceptance':'Fixture criterion','summary':'Fixture outcome',
           'performed_by':'Test fixture','performed_at':datetime.now(timezone.utc).isoformat(),
           'design_inputs_sha256':{'board.pcb':sha(self.root/'board.pcb')},
           'artifacts':[{'path':'result.txt','sha256':sha(self.root/'result.txt')}],
           'board_serial':'fixture','conditions':'fixture only','instruments':'synthetic fixture'}
        self.records={'schema_version':1,'board':'fixture','revision':'1',
                      'checks':{key:copy.deepcopy(r) for group in STAGES.values() for key in group}}
        for key in STAGES['prototype']:
            self.records['checks'][key]['kind']='review'
        self.save()

    def save(self):
        (self.root/'records.json').write_text(json.dumps(self.records))

    def status(self, stage='prototype'):
        self.save()
        return assess(self.config,stage)['status']

    def test_prototype_without_any_physical_records(self):
        self.records['checks']={k:v for k,v in self.records['checks'].items() if k in STAGES['prototype']}
        self.assertEqual(self.status(),'READY')
        self.assertEqual(self.status('bench'),'BLOCKED')

    def test_complete_qualification(self):
        self.assertEqual(self.status('qualified'),'READY')

    def test_failed_skipped_blocked(self):
        for status in ['failed','skipped','blocked']:
            with self.subTest(status=status):
                self.records['checks']['thermal-analysis']['status']=status
                self.assertEqual(self.status(),'BLOCKED')

    def test_missing_required_check(self):
        del self.records['checks']['thermal-analysis']
        self.assertEqual(self.status(),'BLOCKED')

    def test_stale_design(self):
        (self.root/'board.pcb').write_text('changed design')
        self.assertEqual(self.status(),'BLOCKED')

    def test_missing_design(self):
        (self.root/'board.pcb').unlink()
        self.assertEqual(self.status(),'BLOCKED')

    def test_changed_artifact(self):
        (self.root/'result.txt').write_text('changed')
        self.assertEqual(self.status(),'BLOCKED')

    def test_simulation_not_measurement(self):
        self.records['checks']['thermal-measurements']['kind']='simulation'
        self.assertEqual(self.status('qualified'),'BLOCKED')

    def test_measurement_needs_metadata(self):
        del self.records['checks']['logic-bringup']['instruments']
        self.assertEqual(self.status('bench'),'BLOCKED')

    def test_unknown_status_invalid(self):
        self.records['checks']['thermal-analysis']['status']='approved'
        self.save()
        with self.assertRaises(ValueError):assess(self.config,'prototype')

    def test_missing_file_and_cli_exit_codes(self):
        cli=Path(__file__).with_name('check_release.py')
        command=[sys.executable,str(cli),str(self.config),'--stage','prototype']
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,0)
        (self.root/'records.json').unlink()
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,1)
        self.config.write_text('{invalid')
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,2)

    def test_cannot_overwrite_input(self):
        command=[sys.executable,str(Path(__file__).with_name('check_release.py')),str(self.config),
                 '--stage','prototype','--output',str(self.config)]
        before=self.config.read_bytes()
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,2)
        self.assertEqual(before,self.config.read_bytes())

    def test_path_escape_invalid(self):
        cfg=json.loads(self.config.read_text());cfg['design_inputs']=['../escape.pcb'];self.config.write_text(json.dumps(cfg))
        with self.assertRaises(ValueError):assess(self.config,'prototype')

    def test_missing_artifact(self):
        (self.root/'result.txt').unlink()
        self.assertEqual(self.status(),'BLOCKED')

    def test_blank_acceptance_is_blocked(self):
        self.records['checks']['thermal-analysis']['acceptance']=' '
        self.assertEqual(self.status(),'BLOCKED')

    def test_future_evidence_is_blocked(self):
        self.records['checks']['thermal-analysis']['performed_at']='2999-01-01T00:00:00Z'
        self.assertEqual(self.status(),'BLOCKED')

    def test_unknown_schema_invalid(self):
        self.records['schema_version']=2
        self.save()
        with self.assertRaises(ValueError):assess(self.config,'prototype')

    def test_invalid_record_output_cannot_destroy_evidence(self):
        self.records['checks']['thermal-analysis']['status']='unknown'
        self.save()
        record_path=self.root/'records.json';before=record_path.read_bytes()
        command=[sys.executable,str(Path(__file__).with_name('check_release.py')),str(self.config),
                 '--stage','prototype','--output',str(record_path)]
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,2)
        self.assertEqual(before,record_path.read_bytes())

    def test_missing_evidence_is_blocked(self):
        (self.root/'records.json').unlink()
        self.assertEqual(assess(self.config,'prototype')['status'],'BLOCKED')


if __name__=='__main__':unittest.main()
