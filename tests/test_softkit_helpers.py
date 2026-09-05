"""Regression checks for pack/project boundaries and persisted workflow links."""
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = Path('.agents/skills/softkit-orchestrator/scripts')


class SoftKitHelpersTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('.agents', '.softkit'):
            shutil.copytree(REPO / name, self.root / name)
        shutil.copy(REPO / 'AGENTS.md', self.root)

    def run_helper(self, name, *args, expected=0):
        result = subprocess.run(
            [sys.executable, str(self.root / SCRIPTS / name), '--root', str(self.root), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def bootstrap(self, name='Example'):
        self.run_helper('bootstrap_softkit.py', '--project-name', name)

    def test_pack_does_not_require_consumer_project(self):
        self.run_helper('validate_softkit.py')
        self.assertFalse((self.root / 'module.toml').exists())
        self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)

    def test_bootstrap_does_not_invent_modules_and_preserves_files(self):
        self.bootstrap('A "quoted" \\ project')
        manifest = self.root / 'module.toml'
        self.assertEqual(tomllib.loads(manifest.read_text())['modules'], [])
        state = self.root / 'specs/00_Project_Control/project-state.yaml'
        self.assertEqual(yaml.safe_load(state.read_text())['project']['name'], 'A "quoted" \\ project')
        original = {p: p.read_bytes() for p in (manifest, state)}
        self.bootstrap('Different')
        for path, data in original.items():
            self.assertEqual(path.read_bytes(), data)
        self.run_helper('validate_softkit.py', '--mode', 'project')

    def test_project_rejects_missing_nested_state_key(self):
        self.bootstrap()
        state = self.root / 'specs/00_Project_Control/project-state.yaml'
        data = yaml.safe_load(state.read_text())
        del data['project']['primitives']
        state.write_text(yaml.safe_dump(data))
        output = self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)
        self.assertIn('project.primitives', output)

    def test_project_rejects_wrong_types_and_malformed_yaml(self):
        self.bootstrap()
        state = self.root / 'specs/00_Project_Control/project-state.yaml'
        data = yaml.safe_load(state.read_text())
        data['active_work_items'] = 'WI-001'
        state.write_text(yaml.safe_dump(data))
        self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)
        state.write_text('project: [')
        self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)

    def test_approved_workflow_requires_existing_document(self):
        self.bootstrap()
        self.run_helper('create_work_item.py', '--title', 'Repair', '--objective', 'Repair contracts')
        control = self.root / 'specs/00_Project_Control'
        path = control / 'work-items/WI-001.yaml'
        data = yaml.safe_load(path.read_text())
        data['workflow']['status'] = 'approved'
        path.write_text(yaml.safe_dump(data))
        self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)
        data['workflow']['document'] = 'specs/00_Project_Control/workflows/WI-001.md'
        path.write_text(yaml.safe_dump(data))
        self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)
        (control / 'workflows/WI-001.md').write_text('# Approved plan\n')
        self.run_helper('validate_softkit.py', '--mode', 'project')
        self.run_helper('create_work_item.py', '--title', 'Next', '--objective', 'Next approved cycle')
        self.assertTrue((control / 'work-items/WI-002.yaml').is_file())

    def test_project_rejects_dangling_active_item(self):
        self.bootstrap()
        state = self.root / 'specs/00_Project_Control/project-state.yaml'
        data = yaml.safe_load(state.read_text())
        data['active_work_items'] = ['WI-999']
        state.write_text(yaml.safe_dump(data))
        self.run_helper('validate_softkit.py', '--mode', 'project', expected=1)


if __name__ == '__main__':
    unittest.main()
