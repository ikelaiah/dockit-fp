import json
from pathlib import Path
import tempfile
import unittest

from dockit_fp.build import build_site
from dockit_fp.errors import DocKitError


class BuildSiteTests(unittest.TestCase):
    def test_builds_the_maintained_minimal_example(self) -> None:
        root = Path(__file__).resolve().parents[1] / "examples" / "minimal"
        with tempfile.TemporaryDirectory() as temporary:
            result = build_site(root=root, output=Path(temporary) / "site", release="example")

            self.assertEqual(2, result.page_count)
            page = (Path(temporary) / "site" / "quick-start.html").read_text(encoding="utf-8")
            self.assertIn("Change the accent colours", page)

    def test_builds_modern_navigation_search_and_theme_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "guides").mkdir(parents=True)
            (docs / "index.md").write_text(
                "# Welcome\n\nA **safe** start with $x^2$.\n\n## Quick start\n\nBegin here.",
                encoding="utf-8",
            )
            (docs / "guides" / "pascal.md").write_text(
                "# Pascal\n\n```pascal\nWriteLn('hello');\n```", encoding="utf-8"
            )
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Demo-FP", "description": "Demo docs", "repository_url": "https://example.test/demo"},
                "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"},
                "identity": {"footer": "Demo footer", "links": [{"label": "Repository", "url": "https://example.test/demo"}]},
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
            self.assertIn('id="visual-theme"', home)
            self.assertIn('data-visual-theme="classic"', home)
            self.assertIn("System", home)
            self.assertIn("search-index.json", home)
            self.assertIn('placeholder="Search docs, commands, and versions"', home)
            self.assertIn('class="brand-mark"', home)
            self.assertIn('class="capability-strip"', home)
            self.assertIn('aria-label="DocKit-FP capabilities"', home)
            self.assertIn('class="reading-progress"', home)
            self.assertNotIn('class="release-lens"', home)
            self.assertNotIn('<dt>Release</dt>', home)
            self.assertIn('class="page-navigation"', home)
            self.assertIn('class="site-footer"', home)
            self.assertIn('href="https://example.test/demo"', home)
            self.assertIn('class="page-next"', home)
            self.assertIn('<span>Pascal</span>', home)
            self.assertGreater(home.index('class="capability-strip"'), home.index('A <strong>safe</strong> start'))
            self.assertIn('aria-controls="search-results"', home)
            self.assertIn('href="#quick-start"', home)
            self.assertIn("assets/katex/katex.min.css", home)
            self.assertIn('class="math-inline" data-tex="x^2"', home)
            self.assertTrue((root / "site" / "assets" / "katex" / "katex.min.js").exists())
            self.assertTrue((root / "site" / "assets" / "katex" / "LICENSE").exists())
            self.assertTrue((root / "site" / "guides" / "pascal.html").exists())
            pascal = (root / "site" / "guides" / "pascal.html").read_text(encoding="utf-8")
            self.assertIn('class="page-previous" href="../index.html"', pascal)
            site_js = (root / "site" / "assets" / "site.js").read_text(encoding="utf-8")
            self.assertIn("copy-code", site_js)
            self.assertIn("ArrowDown", site_js)
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

    def test_places_home_capabilities_outside_an_initial_admonition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home\n\n> [!IMPORTANT] Read this first.\n\nWelcome.", encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            callout_start = page.index('<aside class="admonition')
            callout_end = page.index("</aside>", callout_start)
            strip_start = page.index('class="capability-strip"')
            self.assertFalse(callout_start < strip_start < callout_end)

    def test_configures_homepage_content_without_changing_other_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home\n\nWelcome to <safe> docs.\n\n## Details\n\nKeep this content.", encoding="utf-8")
            (docs / "guide.md").write_text("# Guide\n\nWelcome to the guide.", encoding="utf-8")
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Demo"},
                "homepage": {
                    "capabilities": [{"title": "<Fast>", "description": "Use <safe> local assets."}],
                    "sections": {"introduction": False, "release_context": True},
                },
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "Start", "pages": [
                {"title": "Home", "path": "index.md"}, {"title": "Guide", "path": "guide.md"},
            ]}]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="0.6.0")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            guide = (root / "site" / "guide.html").read_text(encoding="utf-8")
            self.assertIn("&lt;Fast&gt;", home)
            self.assertIn("Use &lt;safe&gt; local assets.", home)
            self.assertNotIn("<p>Welcome to &lt;safe&gt; docs.</p>", home)
            self.assertIn('class="release-context"', home)
            self.assertIn("0.6.0", home)
            self.assertNotIn('class="capability-strip"', guide)
            self.assertNotIn('class="release-context"', guide)

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
