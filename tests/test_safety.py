from pathlib import Path
import tempfile
import unittest

from dockit_fp.errors import DocKitError
from dockit_fp.safety import prepare_output


class OutputSafetyTests(unittest.TestCase):
    def test_refuses_to_replace_an_unowned_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            output.mkdir()
            (output / "important.txt").write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(DocKitError, "not owned"):
                prepare_output(output)

            self.assertEqual("keep", (output / "important.txt").read_text(encoding="utf-8"))

    def test_replaces_a_directory_marked_as_owned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            prepare_output(output)
            (output / "old.html").write_text("old", encoding="utf-8")

            prepare_output(output)

            self.assertFalse((output / "old.html").exists())
            self.assertTrue((output / ".dockit-fp-site").exists())
