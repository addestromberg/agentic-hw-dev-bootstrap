"""Exercise personal installation using an isolated home and mocked discovery."""
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT=Path(__file__).with_name('install_personal.py').resolve()
SOURCE=SCRIPT.parents[1]

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.home=Path(self.temp.name)
        self.codex=self.home/'.codex';self.codex.mkdir()
        self.agent=self.codex/'AGENTS.md';self.agent.write_text('Existing collaborator instructions.\n')
        self.link=self.codex/'skills/electronics-development'

    def run_installer(self,*args):
        with patch('pathlib.Path.home',return_value=self.home), patch('os.environ.get',side_effect=lambda key,default=None:default), patch.object(sys,'argv',[str(SCRIPT),*map(str,args)]):
            runpy.run_path(str(SCRIPT),run_name='__main__')

    def test_install_preserves_instructions_and_is_idempotent(self):
        self.run_installer();before=self.agent.read_bytes()
        self.run_installer()
        self.assertEqual(self.link.resolve(),SOURCE)
        self.assertEqual((self.home/'.agents/skills/electronics-development').resolve(),SOURCE)
        self.assertIn('Existing collaborator instructions.',self.agent.read_text())
        self.assertEqual(before,self.agent.read_bytes())
        self.assertEqual(self.agent.read_text().count('<!-- electronics-development:start -->'),1)

    def test_refuses_conflicting_directory(self):
        self.link.mkdir(parents=True)
        with self.assertRaises(SystemExit):self.run_installer()
        self.assertEqual(self.agent.read_text(),'Existing collaborator instructions.\n')

    def test_explicit_old_link_migration(self):
        old=self.home/'old-source';self.link.parent.mkdir(parents=True);self.link.symlink_to(old)
        with self.assertRaises(SystemExit):self.run_installer()
        self.run_installer('--replace-link-from',old)
        self.assertEqual(self.link.resolve(),SOURCE)

if __name__=='__main__':unittest.main()
