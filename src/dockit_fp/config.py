"""Versioned configuration loading and legacy-document discovery."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .errors import DocKitError
from .models import Page, SiteConfig

DEFAULT_ACCENT = "#2563eb"
DEFAULT_SECONDARY = "#0ea5e9"
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DocKitError(f"{path}: invalid JSON: {error}") from error
    if not isinstance(value, dict):
        raise DocKitError(f"{path}: expected a JSON object")
    if value.get("schema_version") != 1:
        raise DocKitError(f"{path}: field 'schema_version' must be 1")
    return value


def safe_document_path(value: object, source_name: str) -> str:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise DocKitError(f"{source_name}: path must be a non-empty relative path")
    path = Path(value)
    if any(part in {"", ".", ".."} for part in path.parts) or path.suffix.lower() != ".md":
        raise DocKitError(f"{source_name}: invalid Markdown path {value!r}")
    return path.as_posix()


def _home_page(paths: list[str]) -> str:
    priorities = ("index.md", "README.md", "readme.md", "start/index.md", "getting-started.md")
    for candidate in priorities:
        if candidate in paths:
            return candidate
    return paths[0]


def _title_from_path(path: str) -> str:
    return Path(path).stem.replace("-", " ").replace("_", " ").title()


def _legacy_config(docs: Path) -> SiteConfig:
    paths = sorted(path.relative_to(docs).as_posix() for path in docs.rglob("*.md"))
    if not paths:
        raise DocKitError(f"{docs}: no Markdown documents found")
    home = _home_page(paths)
    pages = tuple(Page(path, _title_from_path(path)) for path in paths)
    return SiteConfig(
        name="Documentation", description="Historical documentation", repository_url=None,
        site_url=None, accent=DEFAULT_ACCENT, accent_secondary=DEFAULT_SECONDARY,
        banner=None, banner_alt=None, pages=pages, legacy=True, home_document=home,
    )


def load_config(root: Path) -> SiteConfig:
    """Load a modern `docs/dockit.json` tree or discover a legacy tree."""
    docs = root / "docs"
    primary = docs / "dockit.json"
    layout_path = docs / "layout.json"
    if not primary.exists() and not layout_path.exists():
        return _legacy_config(docs)
    if not primary.exists():
        raise DocKitError(f"{primary}: required when modern documentation configuration exists")
    data = _read_json(primary)
    project = data.get("project")
    if not isinstance(project, dict) or not isinstance(project.get("name"), str) or not project["name"].strip():
        raise DocKitError(f"{primary}: field 'project.name' must be a non-empty string")
    theme = data.get("theme", {})
    if not isinstance(theme, dict):
        raise DocKitError(f"{primary}: field 'theme' must be an object")
    accent = theme.get("accent", DEFAULT_ACCENT)
    secondary = theme.get("accent_secondary", DEFAULT_SECONDARY)
    if not isinstance(accent, str) or not HEX_COLOR.fullmatch(accent):
        raise DocKitError(f"{primary}: field 'theme.accent' must be a #RRGGBB colour")
    if not isinstance(secondary, str) or not HEX_COLOR.fullmatch(secondary):
        raise DocKitError(f"{primary}: field 'theme.accent_secondary' must be a #RRGGBB colour")
    if not layout_path.exists():
        raise DocKitError(f"{layout_path}: required for modern documentation")
    layout = _read_json(layout_path)
    navigation = layout.get("navigation")
    if not isinstance(navigation, list) or not navigation:
        raise DocKitError(f"{layout_path}: field 'navigation' must be a non-empty list")
    pages: list[Page] = []
    for section in navigation:
        if not isinstance(section, dict) or not isinstance(section.get("title"), str):
            raise DocKitError(f"{layout_path}: each navigation section needs a title")
        entries = section.get("pages")
        if not isinstance(entries, list) or not entries:
            raise DocKitError(f"{layout_path}: navigation section {section['title']!r} needs pages")
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("title"), str):
                raise DocKitError(f"{layout_path}: navigation page needs a title")
            path = safe_document_path(entry.get("path"), f"{layout_path}: navigation page")
            if not (docs / path).is_file():
                raise DocKitError(f"{layout_path}: navigation page {path!r} does not exist")
            if any(page.path == path for page in pages):
                raise DocKitError(f"{layout_path}: navigation page {path!r} appears more than once")
            pages.append(Page(path, entry["title"], section["title"]))
    banner = data.get("banner")
    if banner is not None and (not isinstance(banner, dict) or not isinstance(banner.get("path"), str) or not isinstance(banner.get("alt"), str)):
        raise DocKitError(f"{primary}: field 'banner' needs string path and alt fields")
    banner_path = banner["path"] if banner else None
    if banner_path and (Path(banner_path).is_absolute() or ".." in Path(banner_path).parts):
        raise DocKitError(f"{primary}: banner path is unsafe")
    if banner_path and not (root / banner_path).is_file():
        raise DocKitError(f"{primary}: banner asset {banner_path!r} does not exist")
    home = "index.md" if any(page.path == "index.md" for page in pages) else pages[0].path
    return SiteConfig(
        name=project["name"].strip(), description=str(project.get("description", "")),
        repository_url=project.get("repository_url"), site_url=project.get("site_url"),
        accent=accent, accent_secondary=secondary, banner=banner_path,
        banner_alt=banner.get("alt") if banner else None, pages=tuple(pages),
        legacy=False, home_document=home,
    )
