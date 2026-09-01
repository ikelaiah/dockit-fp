import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

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
            self.assertIn("Next: run dockit-fp serve.", output.getvalue())
            self.assertEqual(0, main(["init", "--root", str(root)]))

    def test_init_adopts_a_readme_and_nested_docs_without_publishing_ancillary_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "getting-started").mkdir(parents=True)
            readme = root / "README.md"
            readme.write_text("# Existing project", encoding="utf-8")
            (docs / "getting-started" / "quick-start.md").write_text("# Quick start", encoding="utf-8")
            (docs / "reference.md").write_text("# API", encoding="utf-8")
            changelog = root / "CHANGELOG.md"
            changelog.write_text("# Changes", encoding="utf-8")
            contributing = root / "CONTRIBUTING.md"
            contributing.write_text("# Contributing", encoding="utf-8")
            before = {path: path.read_text(encoding="utf-8") for path in (readme, changelog, contributing, docs / "getting-started" / "quick-start.md", docs / "reference.md")}
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))

            layout = json.loads((docs / "layout.json").read_text(encoding="utf-8"))
            pages = [page for section in layout["navigation"] for page in section["pages"]]
            self.assertEqual(
                [
                    {"title": "Overview", "path": "README.md", "source": "root"},
                    {"title": "Quick Start", "path": "getting-started/quick-start.md"},
                    {"title": "Reference", "path": "reference.md"},
                ],
                pages,
            )
            self.assertIn("Available for explicit inclusion: CHANGELOG.md, CONTRIBUTING.md", output.getvalue())
            self.assertEqual(before, {path: path.read_text(encoding="utf-8") for path in before})

    def test_init_uses_github_remote_metadata_and_leaves_an_existing_layout_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            self._git(root, "remote", "add", "origin", "git@github.com:example/existing-project.git")
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text("# Existing", encoding="utf-8")
            (docs / "index.md").write_text("# Documentation", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            config = json.loads((docs / "dockit.json").read_text(encoding="utf-8"))
            self.assertEqual("existing-project", config["project"]["name"])
            self.assertEqual("https://github.com/example/existing-project", config["project"]["repository_url"])

            layout_before = (docs / "layout.json").read_text(encoding="utf-8")
            (docs / "new.md").write_text("# New", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertEqual(layout_before, (docs / "layout.json").read_text(encoding="utf-8"))

    def test_init_keeps_an_existing_docs_index_and_excludes_arbitrary_root_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Existing docs home", encoding="utf-8")
            notes = root / "NOTES.md"
            notes.write_text("# Private notes", encoding="utf-8")

            self.assertEqual(0, main(["init", "--root", str(root)]))

            layout = json.loads((docs / "layout.json").read_text(encoding="utf-8"))
            paths = [page["path"] for section in layout["navigation"] for page in section["pages"]]
            self.assertEqual(["index.md"], paths)
            self.assertEqual("# Existing docs home", (docs / "index.md").read_text(encoding="utf-8"))
            self.assertNotIn("NOTES.md", paths)

    def test_serve_validates_then_serves_on_the_requested_host_and_port(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            events: list[tuple[str, object]] = []

            class Server:
                def serve_forever(self) -> None:
                    events.append(("serve", None))

                def server_close(self) -> None:
                    events.append(("close", None))

            def make_server(address, handler):
                events.append(("address", address))
                return Server()

            output = io.StringIO()
            with patch("dockit_fp.cli.ThreadingHTTPServer", side_effect=make_server):
                with redirect_stdout(output):
                    self.assertEqual(0, main(["serve", "--root", str(root), "--host", "127.0.0.1", "--port", "8000"]))

            self.assertEqual(("address", ("127.0.0.1", 8000)), events[0])
            self.assertEqual(["serve", "close"], [event[0] for event in events[1:]])
            self.assertIn("Serving documentation at http://127.0.0.1:8000/", output.getvalue())

    def test_serve_does_not_start_when_validation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "dockit.json").write_text('{"schema_version": 1, "project": {"name": "Broken"}}', encoding="utf-8")
            with patch("dockit_fp.cli.ThreadingHTTPServer") as server:
                self.assertEqual(1, main(["serve", "--root", str(root)]))
            server.assert_not_called()

    def test_doctor_explains_the_next_preview_step(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("Status: preview-ready", output.getvalue())
            self.assertIn("Next: run dockit-fp serve.", output.getvalue())

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
