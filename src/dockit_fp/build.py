"""Build a complete static documentation site from a project source tree."""

from __future__ import annotations

from dataclasses import dataclass
import html
import json
from pathlib import Path
import posixpath
import shutil
from urllib.parse import urlsplit

from .assets import MATH_JS, SITE_CSS, SITE_JS
from .config import load_config
from .errors import DocKitError
from .markdown import render_markdown
from .models import Page
from .safety import prepare_output


@dataclass(frozen=True)
class BuildResult:
    page_count: int
    legacy: bool
    home_document: str


def _route(document: str, home: str) -> str:
    return "index.html" if document == home else str(Path(document).with_suffix(".html").as_posix())


def _safe_url(target: str) -> str:
    parsed = urlsplit(target)
    if parsed.scheme and parsed.scheme.lower() not in {"https", "http", "mailto"}:
        raise DocKitError(f"Markdown: unsafe URL scheme in {target!r}")
    if not parsed.scheme and (target.startswith("/") or ".." in Path(parsed.path).parts):
        raise DocKitError(f"Markdown: unsafe local link {target!r}")
    return target


def _relative(source_route: str, target_route: str) -> str:
    return posixpath.relpath(target_route, posixpath.dirname(source_route) or ".")


def _shell(*, body: str, page: Page, config, current_route: str, version_options: str, banner: str | None) -> str:
    nav = "".join(f'<h2>{html.escape(section)}</h2>' + "".join(
        f'<a class="{"active" if item.path == page.path else ""}" href="{html.escape(_relative(current_route, _route(item.path, config.home_document)), quote=True)}">{html.escape(item.title)}</a>'
        for item in config.pages if item.section == section
    ) for section in dict.fromkeys(item.section for item in config.pages))
    banner_html = f'<img class="banner" src="{html.escape(banner, quote=True)}" alt="{html.escape(config.banner_alt or "", quote=True)}">' if banner else ""
    style = f"--dk-accent:{config.accent};--dk-accent-secondary:{config.accent_secondary}"
    return f'''<!doctype html><html lang="en" style="{style}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(config.description, quote=True)}"><title>{html.escape(page.title)} — {html.escape(config.name)}</title><link rel="stylesheet" href="{html.escape(_relative(current_route, 'assets/site.css'), quote=True)}"><link rel="stylesheet" href="{html.escape(_relative(current_route, 'assets/katex/katex.min.css'), quote=True)}"></head><body><header class="site-header"><div class="topbar"><a class="brand" href="{html.escape(_relative(current_route, 'index.html'), quote=True)}">{html.escape(config.name)} <span>docs</span></a><input id="search" type="search" placeholder="Search this version" aria-label="Search documentation" autocomplete="off" data-search-index="{html.escape(_relative(current_route, 'search-index.json'), quote=True)}"><select id="version-select" aria-label="Documentation version">{version_options}</select><select id="theme-select" aria-label="Colour theme"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></div><div id="search-results" class="search-results" role="region" aria-live="polite" hidden></div></header><details class="mobile-nav"><summary>Browse documentation</summary>{nav}</details><div class="shell"><nav class="sidebar" aria-label="Documentation navigation">{nav}</nav><main class="prose" id="content">{banner_html}{body}</main><aside class="toc">{html.escape(config.name)}<br>Free Pascal / Lazarus</aside></div><script src="{html.escape(_relative(current_route, 'assets/katex/katex.min.js'), quote=True)}"></script><script src="{html.escape(_relative(current_route, 'assets/math.js'), quote=True)}"></script><script src="{html.escape(_relative(current_route, 'assets/site.js'), quote=True)}"></script></body></html>'''


def build_site(*, root: Path, output: Path, release: str, versions: tuple[tuple[str, str], ...] = ()) -> BuildResult:
    """Build one release. `root` is never used as an output location."""
    root, output = root.resolve(), output.resolve()
    config = load_config(root)
    docs = root / "docs"
    prepare_output(output)
    assets = output / "assets"
    assets.mkdir()
    (assets / "site.css").write_text(SITE_CSS, encoding="utf-8")
    (assets / "site.js").write_text(SITE_JS, encoding="utf-8")
    (assets / "math.js").write_text(MATH_JS, encoding="utf-8")
    shutil.copytree(Path(__file__).parent / "vendor" / "katex", assets / "katex")
    banner = None
    if config.banner:
        suffix = Path(config.banner).suffix.lower()
        banner = f"assets/banner{suffix}"
        shutil.copyfile(root / config.banner, output / banner)
    routes = {item.path: _route(item.path, config.home_document) for item in config.pages}
    anchors = {
        page.path: {identifier for _level, _text, identifier in render_markdown((docs / page.path).read_text(encoding="utf-8"), lambda target: target).headings}
        for page in config.pages
    }
    entries: list[dict[str, str]] = []
    for page in config.pages:
        source = (docs / page.path).read_text(encoding="utf-8")
        current_route = routes[page.path]
        def resolve(target: str) -> str:
            target = _safe_url(target)
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                return target
            document, marker, fragment = target.partition("#")
            requested = (Path(page.path).parent / document).as_posix() if document else page.path
            requested = str(Path(requested).as_posix())
            if requested not in routes:
                raise DocKitError(f"{docs / page.path}: linked document {document!r} does not exist")
            if marker and fragment not in anchors[requested]:
                raise DocKitError(
                    f"{docs / page.path}: heading fragment #{fragment} does not exist in {requested}"
                )
            url = _relative(current_route, routes[requested])
            return url + (marker + fragment if marker else "")
        rendered = render_markdown(source, resolve)
        path = output / current_route
        path.parent.mkdir(parents=True, exist_ok=True)
        page_banner = banner if page.path == config.home_document else None
        if versions:
            global_current_route = f"{release}/{current_route}"
            version_options = "".join(
                f'<option value="{html.escape(_relative(global_current_route, target), quote=True)}"{" selected" if item_release == release else ""}>{html.escape(item_release)}</option>'
                for item_release, target in versions
            )
        else:
            version_options = f'<option value="index.html">{html.escape(release)}</option>'
        path.write_text(_shell(body=rendered.html, page=page, config=config, current_route=current_route, version_options=version_options, banner=page_banner), encoding="utf-8")
        entries.append({"title": rendered.title, "section": page.section, "url": current_route, "text": rendered.text})
    (output / "search-index.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "release.json").write_text(json.dumps({"schema_version": 1, "release": release, "page_count": len(entries)}, indent=2) + "\n", encoding="utf-8")
    return BuildResult(len(entries), config.legacy, config.home_document)
