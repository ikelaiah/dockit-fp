"""The public `dockit-fp` command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tempfile

from .build import build_site
from .archive import write_offline_archive
from .config import load_config
from .errors import DocKitError
from .versions import build_all, check_release, load_manifest


def _root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root (default: current directory)")


def _init(root: Path) -> None:
    docs = root / "docs"
    files = {
        "dockit.json": {"schema_version": 1, "project": {"name": root.name or "MyLibrary-FP", "description": "Project documentation"}, "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"}},
        "layout.json": {"schema_version": 1, "navigation": [{"title": "Getting started", "pages": [{"title": "Introduction", "path": "index.md"}]}]},
    }
    existing = [name for name in (*files, "index.md") if (docs / name).exists()]
    if existing:
        raise DocKitError(f"Refusing to initialise {docs}: existing files would be overwritten ({', '.join(existing)}).")
    docs.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (docs / name).write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")
    (docs / "index.md").write_text(f"# {root.name or 'MyLibrary-FP'}\n\nWelcome to the documentation.\n", encoding="utf-8")


def _check(root: Path):
    with tempfile.TemporaryDirectory(prefix="dockit-fp-check-") as temporary:
        result = build_site(root=root, output=Path(temporary) / "site", release="preview")
    return result


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
            messages.append("Next: run dockit-fp check-release before publishing.")
            if shutil.which("git") is None:
                messages.append("ERROR: Git is required for build-all")
        except DocKitError as error:
            messages.append(f"ERROR: {error}")
    else:
        messages.append("Versions: no versions.json (single-release preview only)")
        messages.append("Status: preview-ready")
        messages.append("Next: edit docs/index.md, then run dockit-fp check.")
    return messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dockit-fp", description="Build versioned Free Pascal documentation sites.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("build", "build current documentation"), ("build-all", "build every immutable release"), ("check", "validate documentation"), ("check-release", "validate release refs"), ("init", "create minimal documentation files"), ("doctor", "diagnose project setup")):
        command = commands.add_parser(name, help=help_text)
        _root_argument(command)
        if name == "build":
            command.add_argument("--output", type=Path, help="Output directory (default: build/docs-site)")
            command.add_argument("--release", help="Display release (default: manifest current or preview)")
            command.add_argument("--offline-archive", type=Path, help="Also write a deterministic offline ZIP")
        if name == "build-all":
            command.add_argument("--output", type=Path, help="Output directory (default: build/docs-site)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "init":
            _init(root)
            print(f"Initialised {root / 'docs'}")
            print("Next: edit docs/index.md, then run dockit-fp check.")
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
