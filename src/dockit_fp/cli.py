"""The public `dockit-fp` command-line interface."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import tempfile

from .build import build_site
from .archive import write_offline_archive
from .config import load_config
from .discovery import discover_repository, initial_navigation
from .errors import DocKitError
from .versions import build_all, check_release, load_manifest


def _root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root (default: current directory)")


def _init(root: Path) -> list[str]:
    docs = root / "docs"
    discovery = discover_repository(root)
    docs.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    if not discovery.has_dockit_config:
        project = {"name": discovery.project_name, "description": f"Documentation for {discovery.project_name}"}
        if discovery.github_remote_url:
            project["repository_url"] = discovery.github_remote_url
        (docs / "dockit.json").write_text(json.dumps({
            "schema_version": 1, "project": project,
            "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"},
        }, indent=2) + "\n", encoding="utf-8")
        created.append("docs/dockit.json")
    navigation = initial_navigation(discovery)
    if not navigation:
        index = docs / "index.md"
        if not index.exists():
            index.write_text(f"# {discovery.project_name}\n\nWelcome to the documentation.\n", encoding="utf-8")
            created.append("docs/index.md")
        navigation = [{"title": "Getting started", "pages": [{"title": "Introduction", "path": "index.md"}]}]
    if not discovery.has_layout:
        (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": navigation}, indent=2) + "\n", encoding="utf-8")
        created.append("docs/layout.json")
    detected = ["Git repository" if discovery.is_git_repository else "non-Git project"]
    if discovery.github_remote_url:
        detected.append(f"GitHub remote {discovery.github_remote_url}")
    if discovery.has_readme:
        detected.append("root README.md")
    if discovery.documents:
        detected.append(f"{len(discovery.documents)} Markdown document(s) under docs/")
    if discovery.has_dockit_config or discovery.has_layout:
        detected.append("existing DocKit configuration")
    messages = [f"Initialised {docs}", f"Detected: {', '.join(detected)}."]
    if created:
        messages.append(f"Created: {', '.join(created)}.")
    else:
        messages.append("Existing DocKit configuration was left authoritative; no files were changed.")
    messages.append("Published automatically: README.md and Markdown under docs/ only.")
    if discovery.ancillary_documents:
        messages.append(f"Available for explicit inclusion: {', '.join(discovery.ancillary_documents)}.")
    messages.append("Existing Markdown was left untouched.")
    messages.append("Next: run dockit-fp serve.")
    return messages


def _check(root: Path):
    with tempfile.TemporaryDirectory(prefix="dockit-fp-check-") as temporary:
        result = build_site(root=root, output=Path(temporary) / "site", release="preview")
    return result


def _serve(root: Path, host: str, port: int) -> None:
    """Validate, build, and run a local-only documentation preview server."""
    _check(root)
    output = root / "build" / "docs-site"
    release = load_manifest(root).current if (root / "docs" / "versions.json").exists() else "preview"
    build_site(root=root, output=output, release=release)
    handler = partial(SimpleHTTPRequestHandler, directory=str(output))
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving documentation at http://{host}:{port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped documentation server.")
    finally:
        server.server_close()


def _doctor(root: Path) -> list[str]:
    messages = [f"Project root: {root}"]
    if not (root / "docs").is_dir():
        return [*messages, "ERROR: docs directory is missing"]
    try:
        config = load_config(root)
        messages.append(f"Documentation: {'legacy discovery' if config.legacy else 'modern configuration'} ({len(config.pages)} page(s))")
    except DocKitError as error:
        messages.append(f"ERROR: {error}")
    if (root / "docs" / "versions.json").exists():
        try:
            manifest = load_manifest(root)
            messages.append(f"Versions: {len(manifest.versions)} declared; current {manifest.current}")
            messages.append("Status: versioned release configured")
            if shutil.which("git") is None:
                messages.append("ERROR: Git is required for build-all")
            else:
                try:
                    check_release(root)
                    current = next(entry for entry in manifest.versions if entry.release == manifest.current)
                    messages.append(f"Release refs: verified; current {current.source_ref} matches HEAD")
                    messages.append("Next: follow the pre-publish checklist before publishing.")
                except DocKitError as error:
                    messages.append(f"ERROR: Release refs: {error}")
        except DocKitError as error:
            messages.append(f"ERROR: {error}")
    else:
        messages.append("Versions: no versions.json (single-release preview only)")
        messages.append("Status: preview-ready")
        messages.append("Next: run dockit-fp serve.")
    workflows = sorted((root / ".github" / "workflows").glob("*.y*ml"))
    workflow_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in workflows)
    if "publish-docs.yml@" in workflow_text or "./.github/workflows/publish-docs.yml" in workflow_text:
        mode = "single-version" if "versioned: false" in workflow_text else "historical"
        messages.append(f"Pages: DocKit-FP {mode} workflow detected")
        if "publish-docs.yml@main" in workflow_text:
            messages.append("WARNING: Pages workflow uses moving ref @main; pin a released DocKit-FP tag.")
    else:
        messages.append("Pages: no DocKit-FP workflow detected; see the GitHub Pages guide.")
    return messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dockit-fp", description="Build versioned Free Pascal documentation sites.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("build", "build current documentation"), ("build-all", "build every immutable release"), ("check", "validate documentation"), ("check-release", "validate release refs"), ("init", "adopt or create documentation safely"), ("serve", "validate, build, and preview documentation locally"), ("doctor", "diagnose project setup")):
        command = commands.add_parser(name, help=help_text)
        _root_argument(command)
        if name == "build":
            command.add_argument("--output", type=Path, help="Output directory (default: build/docs-site)")
            command.add_argument("--release", help="Display release (default: manifest current or preview)")
            command.add_argument("--offline-archive", type=Path, help="Also write a deterministic offline ZIP")
        if name == "build-all":
            command.add_argument("--output", type=Path, help="Output directory (default: build/docs-site)")
        if name == "serve":
            command.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
            command.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "init":
            print("\n".join(_init(root)))
        elif args.command == "build":
            release = args.release
            if release is None and (root / "docs" / "versions.json").exists():
                release = load_manifest(root).current
            output = args.output or root / "build" / "docs-site"
            result = build_site(root=root, output=output, release=release or "preview")
            if args.offline_archive:
                write_offline_archive(output, args.offline_archive, release or "preview")
            print(f"Built {result.page_count} page(s) in {output}")
        elif args.command == "build-all":
            output = args.output or root / "build" / "docs-site"
            result = build_all(root=root, output=output)
            print(f"Built {result.release_count} release(s), {result.page_count} page(s) total")
        elif args.command == "check":
            result = _check(root)
            print(f"Documentation check passed: {result.section_count} section(s), {result.page_count} page(s)")
        elif args.command == "serve":
            if not 1 <= args.port <= 65535:
                raise DocKitError("serve: port must be between 1 and 65535")
            _serve(root, args.host, args.port)
        elif args.command == "check-release":
            manifest = check_release(root)
            print(f"Release check passed: {len(manifest.versions)} immutable release(s)")
        else:
            messages = _doctor(root)
            print("\n".join(messages))
            return 1 if any(message.startswith("ERROR:") for message in messages) else 0
    except DocKitError as error:
        print(f"dockit-fp: {error}")
        return 1
    return 0
