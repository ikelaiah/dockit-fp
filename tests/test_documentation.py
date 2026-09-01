import json
from pathlib import Path
import unittest


class DocumentationUsabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]

    def test_readme_keeps_one_short_path_to_a_local_preview(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(readme.splitlines()), 150)
        self.assertEqual(1, sum(line.startswith("# ") for line in readme.splitlines()))
        self.assertIn("first site in about 10 minutes", readme)
        self.assertIn("You can stop here", readme)
        self.assertIn("dockit-fp/archive/refs/tags/v0.12.1.zip", readme)
        self.assertNotIn('pip install "dockit-fp==', readme)

    def test_navigation_puts_learning_before_project_internals(self) -> None:
        layout = json.loads((self.root / "docs" / "layout.json").read_text(encoding="utf-8"))
        sections = layout["navigation"]

        self.assertEqual("Start here", sections[0]["title"])
        self.assertEqual(
            ["index.md", "beginners-guide.md", "writing-great-docs.md", "glossary.md"],
            [page["path"] for page in sections[0]["pages"]],
        )
        self.assertGreater(
            next(index for index, section in enumerate(sections) if section["title"] == "Pascal and project internals"),
            next(index for index, section in enumerate(sections) if section["title"] == "Publish safely"),
        )

    def test_writing_guide_is_language_neutral_and_result_focused(self) -> None:
        guide = (self.root / "docs" / "writing-great-docs.md").read_text(encoding="utf-8")
        words = " ".join(guide.split())

        self.assertIn("Pascal, Python, JavaScript or something else", words)
        self.assertIn("This page helps **[person]** to **[result]**", guide)
        self.assertIn("Show what success looks like", guide)

    def test_beginner_add_page_guidance_preserves_the_existing_home_entry(self) -> None:
        beginner = (self.root / "docs" / "beginners-guide.md").read_text(encoding="utf-8")
        configuration = (self.root / "docs" / "configuration.md").read_text(encoding="utf-8")

        self.assertIn("Keep that existing entry unchanged", beginner)
        self.assertIn("Before the change, the file may look like this", beginner)
        self.assertIn("After adding the page, the file may look like this", beginner)
        self.assertIn('"title": "Quick start",\n  "path": "quick-start.md"', beginner)
        self.assertIn('},\n        {\n          "title": "Quick start"', beginner)
        self.assertNotIn('{"title": "Overview", "path": "index.md"}', beginner)
        root_policy = "Only the repository-root `README.md` has special root-source support."
        self.assertIn(root_policy, beginner)
        self.assertIn(root_policy, configuration)

    def test_docs_project_demonstrates_its_homepage_configuration(self) -> None:
        config = json.loads((self.root / "docs" / "dockit.json").read_text(encoding="utf-8"))
        guide = (self.root / "docs" / "homepage-recipes.md").read_text(encoding="utf-8")

        self.assertEqual(
            [
                "Existing-project friendly",
                "Polished with little setup",
                "Versioned documentation",
                "Offline/local assets",
            ],
            [card["title"] for card in config["homepage"]["capabilities"]],
        )
        self.assertTrue(config["homepage"]["sections"]["release_context"])
        self.assertIn("The homepage is not another Markdown document", guide)
        self.assertIn("## See it in DocKit-FP", guide)
