from pathlib import Path
import tempfile
import unittest

from dockit_fp.cli import main


class CliTests(unittest.TestCase):
    def test_init_creates_a_non_destructive_minimal_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertTrue((root / "docs" / "dockit.json").exists())
            self.assertEqual(1, main(["init", "--root", str(root)]))

    def test_check_and_build_report_success_for_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertEqual(0, main(["check", "--root", str(root)]))
            self.assertEqual(0, main(["build", "--root", str(root), "--output", str(root / "site")]))
            self.assertTrue((root / "site" / "index.html").exists())
