import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest

from dockit_fp.cli import main


class CliTests(unittest.TestCase):
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
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("Status: versioned release configured", output.getvalue())
            self.assertIn("Next: run dockit-fp check-release before publishing.", output.getvalue())

    def test_check_and_build_report_success_for_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertEqual(0, main(["check", "--root", str(root)]))
            self.assertEqual(0, main(["build", "--root", str(root), "--output", str(root / "site")]))
            self.assertTrue((root / "site" / "index.html").exists())
