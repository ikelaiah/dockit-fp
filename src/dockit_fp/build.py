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


def _page_navigation(*, page: Page, config, current_route: str) -> str:
    position = config.pages.index(page)
    links: list[str] = []
    for label, item in (("Previous", config.pages[position - 1] if position else None), ("Next", config.pages[position + 1] if position + 1 < len(config.pages) else None)):
        if item is not None:
            href = html.escape(_relative(current_route, _route(item.path, config.home_document)), quote=True)
            links.append(f'<a class="page-{label.lower()}" href="{href}"><small>{label}</small><span>{html.escape(item.title)}</span></a>')
    return f'<nav class="page-navigation" aria-label="Page navigation">{"".join(links)}</nav>' if links else ""


def _shell(*, body: str, headings: tuple[tuple[int, str, str], ...], page: Page, config, current_route: str, version_options: str, banner: str | None) -> str:
    nav = "".join(f'<h2>{html.escape(section)}</h2>' + "".join(
        f'<a class="{"active" if item.path == page.path else ""}" href="{html.escape(_relative(current_route, _route(item.path, config.home_document)), quote=True)}">{html.escape(item.title)}</a>'
        for item in config.pages if item.section == section
    ) for section in dict.fromkeys(item.section for item in config.pages))
    banner_html = f'<img class="banner" src="{html.escape(banner, quote=True)}" alt="{html.escape(config.banner_alt or "", quote=True)}">' if banner else ""
    style = f"--dk-accent:{config.accent};--dk-accent-secondary:{config.accent_secondary}"
    brand_mark = '<svg class="brand-mark" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3 1.5h6l4 4v9H3zM9 1.5v4h4M5.5 9h5M5.5 11.5h4"/></svg>'
    capability_strip = '''<ul class="capability-strip" aria-label="DocKit-FP capabilities"><li><strong>Offline</strong><span>Local assets, no CDN.</span></li><li><strong>Versioned</strong><span>Release history stays browsable.</span></li><li><strong>KaTeX</strong><span>Mathematics renders locally.</span></li><li><strong>Pascal-ready</strong><span>Made for FP and Lazarus docs.</span></li></ul>''' if page.path == config.home_document else ""
    if capability_strip:
        title_end = body.find("</h1>")
        insert_at = title_end + len("</h1>") if title_end >= 0 else 0
        paragraph_start = body.find("<p>", insert_at)
        if paragraph_start >= 0 and not body[insert_at:paragraph_start].strip():
            insert_at = body.find("</p>", paragraph_start) + len("</p>")
        body = body[:insert_at] + capability_strip + body[insert_at:]
    toc_links = "".join(
        f'<a class="toc-level-{level}" href="#{html.escape(identifier, quote=True)}">{html.escape(text)}</a>'
        for level, text, identifier in headings if level > 1
    )
    toc = f'<p class="toc-title">On this page</p>{toc_links}' if toc_links else '<p class="toc-title">Documentation</p><p class="toc-empty-copy">Browse the sections in the navigation.</p>'
    page_navigation = _page_navigation(page=page, config=config, current_route=current_route)
    footer_links = "".join(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>' for label, url in config.project_links)
    footer = f'<footer class="site-footer"><span>{html.escape(config.footer or config.name)}</span>{footer_links}</footer>' if config.footer or footer_links else ""
    return f'''<!doctype html><html lang="en" style="{style}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(config.description, quote=True)}"><title>{html.escape(page.title)} — {html.escape(config.name)}</title><link rel="stylesheet" href="{html.escape(_relative(current_route, 'assets/site.css'), quote=True)}"><link rel="stylesheet" href="{html.escape(_relative(current_route, 'assets/katex/katex.min.css'), quote=True)}"></head><body><div class="reading-progress" aria-hidden="true"><span></span></div><header class="site-header"><div class="topbar"><a class="brand" href="{html.escape(_relative(current_route, 'index.html'), quote=True)}">{brand_mark}<span>{html.escape(config.name)}</span> <em>docs</em></a><div class="search-control"><input id="search" type="search" placeholder="Search docs, commands, and versions" aria-label="Search documentation, commands, and versions" aria-controls="search-results" aria-expanded="false" autocomplete="off" data-search-index="{html.escape(_relative(current_route, 'search-index.json'), quote=True)}"><kbd aria-hidden="true" title="Press / to search">/</kbd></div><select id="version-select" aria-label="Documentation version">{version_options}</select><select id="theme-select" aria-label="Colour theme"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></div><div id="search-results" class="search-results" role="region" aria-label="Search results" aria-live="polite" hidden></div></header><details class="mobile-nav"><summary>Browse documentation</summary>{nav}</details><div class="shell"><nav class="sidebar" aria-label="Documentation navigation">{nav}</nav><main class="prose" id="content">{banner_html}{body}{page_navigation}</main><aside class="toc" aria-label="On this page">{toc}</aside></div>{footer}<script src="{html.escape(_relative(current_route, 'assets/katex/katex.min.js'), quote=True)}"></script><script src="{html.escape(_relative(current_route, 'assets/math.js'), quote=True)}"></script><script src="{html.escape(_relative(current_route, 'assets/site.js'), quote=True)}"></script></body></html>'''


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
        path.write_text(_shell(body=rendered.html, headings=rendered.headings, page=page, config=config, current_route=current_route, version_options=version_options, banner=page_banner), encoding="utf-8")
        entries.append({"title": rendered.title, "section": page.section, "url": current_route, "text": rendered.text})
    (output / "search-index.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "release.json").write_text(json.dumps({"schema_version": 1, "release": release, "page_count": len(entries)}, indent=2) + "\n", encoding="utf-8")
    return BuildResult(len(entries), config.legacy, config.home_document)
