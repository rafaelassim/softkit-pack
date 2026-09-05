"""Regression checks for pack/project boundaries and persisted workflow links."""
import shutil
import os
import runpy
from unittest.mock import patch
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = Path('.softkit/scripts')


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

    def test_old_entry_points_delegate(self):
        old = self.root / '.agents/skills/softkit-orchestrator/scripts'
        for name, args in [('bootstrap_softkit.py', []),
                           ('create_work_item.py', ['--title', 'Old CLI', '--objective', 'Compatibility']),
                           ('scan_sources.py', []), ('validate_softkit.py', ['--mode', 'project'])]:
            result = subprocess.run([sys.executable, str(old / name), '--root', str(self.root), *args],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_noninteractive_missing_arguments_fail_without_creation(self):
        for args in ([], ['--title', 'Incomplete'], ['--title', ' ', '--objective', 'Text']):
            result = subprocess.run([sys.executable, str(self.root / SCRIPTS / 'create_work_item.py'), *args],
                                    cwd=self.root, input='', capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'specs').exists())

    @unittest.skipUnless(os.name == 'posix', 'PTY scenario requires POSIX')
    def test_interactive_terminal_retries_and_defaults(self):
        import pty
        master, slave = pty.openpty()
        try:
            process = subprocess.Popen([sys.executable, str(self.root / SCRIPTS / 'create_work_item.py')],
                                       cwd=self.root, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True)
            try:
                os.write(master, b'\n\nInteractive title\nObjective\nbad-origin\n\n\nbad-priority\n\n')
                out, err = process.communicate(timeout=10)
                self.assertEqual(process.returncode, 0, out + err)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate()
        finally:
            os.close(master)
            os.close(slave)
        data = yaml.safe_load((self.root / 'specs/00_Project_Control/work-items/WI-001.yaml').read_text())
        self.assertEqual(data['title'], 'Interactive title')
        self.assertEqual(data['priority'], 'medium')
        self.assertEqual(data['origin']['type'], 'user-request')
        self.assertEqual(data['status'], 'proposed')

    def test_interactive_cancellation_creates_nothing(self):
        for cancellation in (EOFError, KeyboardInterrupt):
            with patch.object(sys, 'argv', ['create_work_item.py']), patch('sys.stdin.isatty', return_value=True), \
                 patch('builtins.input', side_effect=['Title', cancellation]):
                with self.assertRaises(SystemExit) as caught:
                    runpy.run_path(str(self.root / SCRIPTS / 'create_work_item.py'), run_name='__main__')
                self.assertEqual(caught.exception.code, 130)
            self.assertFalse((self.root / 'specs').exists())

    def test_cli_preserves_literal_backslashes(self):
        self.run_helper('create_work_item.py', '--title', r'Path \new', '--objective', 'Keep text')
        data = yaml.safe_load((self.root / 'specs/00_Project_Control/work-items/WI-001.yaml').read_text())
        self.assertEqual(data['title'], r'Path \new')

    def test_change_request_routing_and_lifecycle_ids(self):
        for folder, name in [('applied', 'CR-040-old.md'), ('rejected', 'CR-042.md')]:
            path = self.root / 'softkit-input/changes' / folder / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Historical record')
        self.run_helper('create_work_item.py', '--artifact-type', 'change-request',
                        '--title', 'New request', '--objective', 'Requested behavior')
        path = self.root / 'softkit-input/changes/inbox/CR-043.md'
        text = path.read_text()
        data = yaml.safe_load(text.split('---')[1])
        self.assertEqual(data['id'], 'CR-043')
        self.assertEqual(data['status'], 'inbox')
        self.assertEqual(data['authority'], 'proposed')
        self.assertIn('Requested behavior', text)
        self.assertFalse((self.root / 'specs').exists())

    def test_origin_does_not_change_artifact_type(self):
        self.run_helper('create_work_item.py', '--origin-type', 'change-request',
                        '--origin-id', 'CR-001', '--title', 'Work', '--objective', 'Implement')
        data = yaml.safe_load((self.root / 'specs/00_Project_Control/work-items/WI-001.yaml').read_text())
        self.assertEqual(data['origin']['type'], 'change-request')
        self.assertFalse((self.root / 'softkit-input/changes/inbox').exists())

    def test_arrow_selection_and_cancellation(self):
        import curses
        from unittest.mock import MagicMock
        module = runpy.run_path(str(self.root / SCRIPTS / 'create_work_item.py'))
        screen = MagicMock()
        screen.getch.side_effect = [curses.KEY_DOWN, 10]
        with patch.dict(os.environ, {'TERM': 'xterm'}), patch('sys.stdout.isatty', return_value=True), \
             patch('curses.wrapper', side_effect=lambda callback: callback(screen)):
            self.assertEqual(module['select']('Type', ('work-item', 'change-request'), 'work-item'), 'change-request')
            screen.getch.side_effect = [ord('q')]
            with self.assertRaises(KeyboardInterrupt):
                module['select']('Type', ('work-item', 'change-request'), 'work-item')

    def test_numbered_selection_retries(self):
        module = runpy.run_path(str(self.root / SCRIPTS / 'create_work_item.py'))
        with patch('sys.stdout.isatty', return_value=False), patch('builtins.input', side_effect=['invalid', '9', '2']):
            self.assertEqual(module['select']('Type', ('work-item', 'change-request'), 'work-item'), 'change-request')

    def install(self, destination, expected=0, *extra):
        result = subprocess.run([sys.executable, str(self.root / SCRIPTS / 'bootstrap_softkit.py'),
                                 str(destination), *extra], cwd=self.temp.name,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_install_new_nested_destination_and_reexecute(self):
        self.bootstrap('Source project')
        history = self.root / 'specs/00_Project_Control/work-items/WI-900.yaml'
        history.write_text('source history')
        destination = self.root / 'new project'
        self.install(destination)
        self.assertFalse((destination / 'specs/00_Project_Control/work-items/WI-900.yaml').exists())
        state = destination / 'specs/00_Project_Control/project-state.yaml'
        data = yaml.safe_load(state.read_text())
        self.assertEqual(data['project']['name'], 'new project')
        self.assertEqual(data['work_items'], [])
        self.assertEqual(tomllib.loads((destination / 'module.toml').read_text())['modules'], [])
        self.assertIn('status: draft', (destination / 'softkit-input/project-primitives.md').read_text())
        before = {p.relative_to(destination): p.read_bytes() for p in destination.rglob('*') if p.is_file()}
        self.install(destination)
        self.assertEqual(before, {p.relative_to(destination): p.read_bytes() for p in destination.rglob('*') if p.is_file()})
        for mode in ('pack', 'project'):
            result = subprocess.run([sys.executable, str(destination / SCRIPTS / 'validate_softkit.py'), '--mode', mode],
                                    cwd=destination, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(destination / '.agents/skills/softkit-orchestrator/scripts/create_work_item.py'),
                                 '--title', 'Installed', '--objective', 'Works'], cwd=destination, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_install_conflict_is_detected_before_copy(self):
        destination = self.root / 'conflict'
        destination.mkdir()
        (destination / 'AGENTS.md').write_text('Custom instructions')
        self.install(destination, 1)
        self.assertEqual(list(destination.iterdir()), [destination / 'AGENTS.md'])
        self.assertEqual((destination / 'AGENTS.md').read_text(), 'Custom instructions')

    def test_install_preserves_existing_project_data(self):
        destination = self.root / 'existing'
        destination.mkdir()
        (destination / 'module.toml').write_text('custom manifest')
        (destination / 'app.py').write_text('custom code')
        self.install(destination)
        self.assertEqual((destination / 'module.toml').read_text(), 'custom manifest')
        self.assertEqual((destination / 'app.py').read_text(), 'custom code')

    def test_install_incomplete_source_writes_nothing(self):
        (self.root / '.agents/skills/softkit-qa/SKILL.md').unlink()
        destination = self.root / 'not-created'
        self.install(destination, 1)
        self.assertFalse(destination.exists())

    def test_install_rejects_ambiguous_arguments_and_blocked_directory(self):
        destination = self.root / 'ambiguous'
        self.install(destination, 2, '--root', str(self.root))
        self.assertFalse(destination.exists())
        destination.mkdir()
        (destination / 'specs').write_text('Not a directory')
        self.install(destination, 1)
        self.assertFalse((destination / '.agents').exists())


if __name__ == '__main__':
    unittest.main()
