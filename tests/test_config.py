import json
from pathlib import Path
import tempfile
import unittest

from dockit_fp.config import load_config
from dockit_fp.errors import DocKitError


class ConfigurationDiagnosticsTests(unittest.TestCase):
    def _write_config(self, root: Path, document: dict, layout: dict) -> None:
        docs = root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("# Home", encoding="utf-8")
        (docs / "dockit.json").write_text(json.dumps(document), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")

    def test_explains_how_to_fix_an_invalid_accent_colour(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}, "theme": {"accent": "blue"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocKitError, r"theme\.accent.*Use a #RRGGBB colour"):
                load_config(root)

    def test_names_the_section_and_next_step_for_an_empty_navigation_group(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Guides", "pages": []}]},
            )

            with self.assertRaisesRegex(DocKitError, r"section 'Guides'.*Add at least one page"):
                load_config(root)

    def test_explains_how_to_fix_a_missing_navigation_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Install", "path": "install.md"}]}]},
            )

            with self.assertRaisesRegex(DocKitError, r"navigation page 'install\.md'.*Create docs/install\.md or correct its path"):
                load_config(root)

    def test_loads_a_colour_preset_and_supported_project_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "theme": {"preset": "purple"},
                    "identity": {
                        "footer": "Built for Pascal maintainers.",
                        "links": [{"label": "Source code", "url": "https://example.test/source"}],
                    },
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            config = load_config(root)

            self.assertEqual("#7c3aed", config.accent)
            self.assertEqual("Built for Pascal maintainers.", config.footer)
            self.assertEqual((("Source code", "https://example.test/source"),), config.project_links)

    def test_loads_a_supported_visual_theme(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}, "theme": {"style": "midnight"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            self.assertEqual("midnight", load_config(root).theme_style)

    def test_loads_homepage_cards_and_section_switches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {
                        "capabilities": [
                            {"title": "API reference", "description": "Every public unit."},
                            {"title": "Offline", "description": "No CDN."},
                        ],
                        "sections": {
                            "capabilities": True,
                            "banner": False,
                            "introduction": False,
                            "release_context": True,
                        },
                    },
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            homepage = load_config(root).homepage

            self.assertEqual(("API reference", "Every public unit."), homepage.capabilities[0])
            self.assertFalse(homepage.show_banner)
            self.assertFalse(homepage.show_introduction)
            self.assertTrue(homepage.show_release_context)

    def test_names_an_invalid_homepage_card_field_and_correction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {"capabilities": [{"title": "", "description": "Useful."}]},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocKitError, r"homepage\.capabilities\[0\]\.title.*Use a non-empty string"):
                load_config(root)

    def test_names_an_invalid_homepage_section_field_and_correction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {"sections": {"banner": "no"}},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocKitError, r"homepage\.sections\.banner.*Use true or false"):
                load_config(root)

    def test_rejects_an_unknown_homepage_section_with_the_supported_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {"sections": {"introducton": False}},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocKitError, r"homepage\.sections\.introducton.*Use one of"):
                load_config(root)

    def test_explains_the_schema_compatibility_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 2, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocKitError, r"schema version 1.*migration"):
                load_config(root)
