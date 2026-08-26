import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from dockit_fp.errors import DocKitError
from dockit_fp.versions import build_all, check_release


class VersionedBuildTests(unittest.TestCase):
    def _git(self, root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)

    def _repository(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._git(root, "init")
        self._git(root, "config", "user.email", "tests@example.test")
        self._git(root, "config", "user.name", "Tests")
        docs = root / "docs"
        docs.mkdir()
        (docs / "README.md").write_text("# Version one\n\nOld content.", encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v1")
        self._git(root, "tag", "v1.0.0")
        (docs / "new.md").write_text("# Version two\n\nNew content.", encoding="utf-8")
        (docs / "versions.json").write_text(json.dumps({
            "schema_version": 1, "current": "2.0.0", "versions": [
                {"release": "2.0.0", "source_ref": "v2.0.0"},
                {"release": "1.0.0", "source_ref": "v1.0.0"},
            ],
        }), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v2")
        self._git(root, "tag", "v2.0.0")
        return root

    def _modern_history_repository(self) -> Path:
        """Create an old modern release authored before strict navigation checks."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._git(root, "init")
        self._git(root, "config", "user.email", "tests@example.test")
        self._git(root, "config", "user.name", "Tests")
        docs = root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("# Version one\n\nOld content.", encoding="utf-8")
        (docs / "archive.md").write_text("# Archived note\n\nOld navigation did not list this.", encoding="utf-8")
        (docs / "dockit.json").write_text(json.dumps({
            "schema_version": 1,
            "project": {"name": "Historical docs"},
        }), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "navigation": [{"title": "Docs", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        }), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v1")
        self._git(root, "tag", "v1.0.0")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "navigation": [{"title": "Docs", "pages": [
                {"title": "Overview", "path": "index.md"},
                {"title": "Archive", "path": "archive.md"},
            ]}],
        }), encoding="utf-8")
        (docs / "versions.json").write_text(json.dumps({
            "schema_version": 1, "current": "2.0.0", "versions": [
                {"release": "2.0.0", "source_ref": "v2.0.0"},
                {"release": "1.0.0", "source_ref": "v1.0.0"},
            ],
        }), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v2")
        self._git(root, "tag", "v2.0.0")
        return root

    def test_build_all_uses_each_tag_not_the_current_worktree(self) -> None:
        root = self._repository()
        result = build_all(root=root, output=root / "site")

        self.assertEqual(2, result.release_count)
        old_site = root / "site" / "1.0.0"
        self.assertTrue((old_site / "index.html").exists())
        self.assertFalse((old_site / "new.html").exists())
        self.assertNotIn("New content", (old_site / "index.html").read_text(encoding="utf-8"))
        self.assertIn("Version one", (old_site / "index.html").read_text(encoding="utf-8"))
        self.assertIn('value="../2.0.0/index.html"', (old_site / "index.html").read_text(encoding="utf-8"))

    def test_build_all_allows_unlisted_documents_in_historical_modern_releases(self) -> None:
        root = self._modern_history_repository()

        result = build_all(root=root, output=root / "site")

        self.assertEqual(2, result.release_count)
        self.assertTrue((root / "site" / "1.0.0" / "index.html").exists())

    def test_check_release_rejects_moving_refs(self) -> None:
        root = self._repository()
        manifest = root / "docs" / "versions.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["versions"][0]["source_ref"] = "main"
        manifest.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaisesRegex(DocKitError, "moving source_ref"):
            check_release(root)
