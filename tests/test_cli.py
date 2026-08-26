import io
from contextlib import redirect_stdout
from pathlib import Path
import subprocess
import tempfile
import unittest

from dockit_fp.cli import main


class CliTests(unittest.TestCase):
    def _git(self, root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)

    def test_init_creates_a_non_destructive_minimal_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertTrue((root / "docs" / "dockit.json").exists())
            self.assertIn("Next: edit docs/index.md, then run dockit-fp check.", output.getvalue())
            self.assertEqual(1, main(["init", "--root", str(root)]))

    def test_doctor_explains_the_next_preview_step(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("Status: preview-ready", output.getvalue())
            self.assertIn("Next: edit docs/index.md, then run dockit-fp check.", output.getvalue())

    def test_doctor_explains_the_next_release_step(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            (root / "docs" / "versions.json").write_text(
                '{"schema_version": 1, "current": "0.2.0", "versions": [{"release": "0.2.0", "source_ref": "v0.2.0"}]}',
                encoding="utf-8",
            )
            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.test")
            self._git(root, "config", "user.name", "Tests")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "release")
            self._git(root, "tag", "v0.2.0")
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("Status: versioned release configured", output.getvalue())
            self.assertIn("Release refs: verified; current v0.2.0 matches HEAD", output.getvalue())
            self.assertIn("Next: follow the pre-publish checklist before publishing.", output.getvalue())

    def test_doctor_reports_a_missing_current_release_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            (root / "docs" / "versions.json").write_text(
                '{"schema_version": 1, "current": "0.9.0", "versions": [{"release": "0.9.0", "source_ref": "v0.9.0"}]}',
                encoding="utf-8",
            )
            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.test")
            self._git(root, "config", "user.name", "Tests")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "prepare release")
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(1, main(["doctor", "--root", str(root)]))

            self.assertIn("ERROR: Release refs:", output.getvalue())
            self.assertIn("Create the tag", output.getvalue())

    def test_check_and_build_report_success_for_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, main(["check", "--root", str(root)]))
            self.assertIn("Documentation check passed: 1 section(s), 1 page(s)", output.getvalue())
            self.assertEqual(0, main(["build", "--root", str(root), "--output", str(root / "site")]))
            self.assertTrue((root / "site" / "index.html").exists())
