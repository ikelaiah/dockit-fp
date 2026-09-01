import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from dockit_fp import __version__
from dockit_fp.cli import main
from dockit_fp.github_pages import WORKFLOW_RELATIVE_PATH, render_workflow


class GitHubPagesCommandTests(unittest.TestCase):
    def _git(self, root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)

    def _run(self, root: Path, *arguments: str) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(["github-pages", *arguments, "--root", str(root)])
        return result, output.getvalue()

    def test_initialises_a_readme_only_git_repository_and_creates_a_pinned_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            readme = root / "README.md"
            readme.write_text("# Existing documentation\n", encoding="utf-8")

            result, output = self._run(root)

            self.assertEqual(0, result)
            self.assertEqual("# Existing documentation\n", readme.read_text(encoding="utf-8"))
            layout = json.loads((root / "docs" / "layout.json").read_text(encoding="utf-8"))
            self.assertEqual({"path": "README.md", "source": "root"}, layout["home"])
            self.assertEqual(render_workflow(f"v{__version__}"), (root / WORKFLOW_RELATIVE_PATH).read_text(encoding="utf-8"))
            self.assertIn("DocKit is ready for GitHub Pages.", output)
            self.assertIn("git add .", output)
            self.assertIn("git push", output)

    def test_preserves_existing_configuration_and_is_idempotent_without_a_remote(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Existing home", encoding="utf-8")
            config = docs / "dockit.json"
            layout = docs / "layout.json"
            config.write_text('{"schema_version": 1, "project": {"name": "Kept"}}\n', encoding="utf-8")
            layout.write_text('{"schema_version": 1, "home": {"path": "index.md"}, "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}]}\n', encoding="utf-8")
            before = {path: path.read_text(encoding="utf-8") for path in (config, layout)}

            self.assertEqual(0, self._run(root)[0])
            workflow = root / WORKFLOW_RELATIVE_PATH
            configured = {path: path.read_text(encoding="utf-8") for path in (*before, workflow)}
            result, output = self._run(root)

            self.assertEqual(0, result)
            self.assertEqual(before, {path: path.read_text(encoding="utf-8") for path in before})
            self.assertEqual(configured, {path: path.read_text(encoding="utf-8") for path in configured})
            self.assertIn("No changes required.", output)
            self.assertIn("not connected to GitHub yet", output)

    def test_requires_explicit_update_for_an_outdated_managed_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            self.assertEqual(0, self._run(root)[0])
            workflow = root / WORKFLOW_RELATIVE_PATH
            workflow.write_text(render_workflow("v0.12.1"), encoding="utf-8")
            layout = root / "docs" / "layout.json"
            layout_before = layout.read_text(encoding="utf-8")

            result, output = self._run(root)

            self.assertEqual(0, result)
            self.assertEqual(render_workflow("v0.12.1"), workflow.read_text(encoding="utf-8"))
            self.assertEqual(layout_before, layout.read_text(encoding="utf-8"))
            self.assertIn("--update", output)
            result, output = self._run(root, "--update")
            self.assertEqual(0, result)
            self.assertEqual(render_workflow(f"v{__version__}"), workflow.read_text(encoding="utf-8"))
            self.assertEqual(layout_before, layout.read_text(encoding="utf-8"))
            self.assertIn("Updated", output)

    def test_refuses_to_overwrite_an_unmanaged_or_malformed_workflow(self) -> None:
        for contents, expected in (("name: Personal Pages\n", "not managed by DocKit"), ("# DocKit managed workflow: github-pages v1\nname: Broken\n", "malformed")):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._git(root, "init")
                workflow = root / WORKFLOW_RELATIVE_PATH
                workflow.parent.mkdir(parents=True)
                workflow.write_text(contents, encoding="utf-8")

                result, output = self._run(root)

                self.assertEqual(1, result)
                self.assertEqual(contents, workflow.read_text(encoding="utf-8"))
                self.assertFalse((root / "docs").exists())
                self.assertIn(expected, output)

    def test_rejects_invalid_existing_dockit_configuration_without_repairing_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            docs = root / "docs"
            docs.mkdir()
            config = docs / "dockit.json"
            config.write_text('{"schema_version": 1, "project": {"name": "Broken"}}\n', encoding="utf-8")

            result, output = self._run(root)

            self.assertEqual(1, result)
            self.assertIn("existing DocKit configuration is invalid", output)
            self.assertFalse((root / WORKFLOW_RELATIVE_PATH).exists())
            self.assertEqual('{"schema_version": 1, "project": {"name": "Broken"}}\n', config.read_text(encoding="utf-8"))
