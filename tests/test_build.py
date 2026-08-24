import json
from pathlib import Path
import tempfile
import unittest

from dockit_fp.build import build_site
from dockit_fp.errors import DocKitError


class BuildSiteTests(unittest.TestCase):
    def test_builds_modern_navigation_search_and_theme_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "guides").mkdir(parents=True)
            (docs / "index.md").write_text("# Welcome\n\nA **safe** start.", encoding="utf-8")
            (docs / "guides" / "pascal.md").write_text(
                "# Pascal\n\n```pascal\nWriteLn('hello');\n```", encoding="utf-8"
            )
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Demo-FP", "description": "Demo docs", "repository_url": "https://example.test/demo"},
                "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Start", "pages": [
                    {"title": "Welcome", "path": "index.md"},
                    {"title": "Pascal", "path": "guides/pascal.md"},
                ]}],
            }), encoding="utf-8")

            result = build_site(root=root, output=root / "site", release="dev")

            self.assertEqual(2, result.page_count)
            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('style="--dk-accent:#0f766e;--dk-accent-secondary:#0891b2"', home)
            self.assertIn("System", home)
            self.assertIn("search-index.json", home)
            self.assertTrue((root / "site" / "guides" / "pascal.html").exists())
            search = json.loads((root / "site" / "search-index.json").read_text(encoding="utf-8"))
            self.assertEqual(["index.html", "guides/pascal.html"], [entry["url"] for entry in search])

    def test_uses_readme_as_home_for_configuration_free_legacy_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Old documentation\n\nThe original home.", encoding="utf-8")
            (docs / "CHEATSHEET.md").write_text("# Cheat sheet", encoding="utf-8")

            result = build_site(root=root, output=root / "site", release="1.0.0")

            self.assertTrue(result.legacy)
            self.assertEqual("README.md", result.home_document)
            self.assertIn("Old documentation", (root / "site" / "index.html").read_text(encoding="utf-8"))
            self.assertTrue((root / "site" / "CHEATSHEET.html").exists())

    def test_rejects_broken_heading_fragments_and_unsafe_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Old\n\n[Broken](other.md#absent)", encoding="utf-8")
            (docs / "other.md").write_text("# Present", encoding="utf-8")

            with self.assertRaisesRegex(DocKitError, "heading fragment"):
                build_site(root=root, output=root / "site", release="1.0.0")

            (docs / "README.md").write_text("# Old\n\n[Unsafe](javascript:alert(1))", encoding="utf-8")
            with self.assertRaisesRegex(DocKitError, "unsafe URL"):
                build_site(root=root, output=root / "site", release="1.0.0")

    def test_escapes_configuration_values_in_the_html_shell(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Safe", encoding="utf-8")
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1, "project": {"name": "<script>x</script>", "description": "\" onload=alert(1)"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "<bad>", "pages": [{"title": "<bad>", "path": "index.md"}]}]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("<script>x</script>", page)
            self.assertIn("&lt;script&gt;x&lt;/script&gt;", page)
