"""A deliberately small, safe Markdown renderer for documentation prose."""

from __future__ import annotations

from dataclasses import dataclass
import html
import re
from collections.abc import Callable

from .errors import DocKitError

LinkResolver = Callable[[str], str]
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^```\s*([\w+-]*)\s*$")
LIST = re.compile(r"^\s*[-*+]\s+(.+)$")
ORDERED = re.compile(r"^\s*\d+[.)]\s+(.+)$")
LINK = re.compile(r"\[([^]]+)]\(([^)]+)\)")
CODE = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class RenderedMarkdown:
    html: str
    title: str
    headings: tuple[tuple[int, str, str], ...]
    text: str


def slugify(text: str) -> str:
    value = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-") or "section"


def _plain(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*_`]+", "", value)).strip()


def _inline(value: str, resolve: LinkResolver) -> str:
    escaped = html.escape(value, quote=False)
    escaped = LINK.sub(lambda match: f'<a href="{html.escape(resolve(html.unescape(match.group(2))), quote=True)}">{match.group(1)}</a>', escaped)
    escaped = CODE.sub(r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return re.sub(r"(?<!\*)\*([^*]+)\*", r"<em>\1</em>", escaped)


def render_markdown(source: str, resolve_link: LinkResolver) -> RenderedMarkdown:
    lines = source.splitlines()
    output: list[str] = []
    plain: list[str] = []
    headings: list[tuple[int, str, str]] = []
    paragraph: list[str] = []
    seen: set[str] = set()
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph)
            output.append(f"<p>{_inline(text, resolve_link)}</p>")
            plain.append(_plain(text))
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        fence = FENCE.match(line)
        heading = HEADING.match(line)
        if fence:
            flush_paragraph()
            language = fence.group(1).lower() or "text"
            index += 1
            code: list[str] = []
            while index < len(lines) and not FENCE.match(lines[index]):
                code.append(lines[index])
                index += 1
            if index == len(lines):
                raise DocKitError("Markdown: unclosed fenced code block")
            output.append(f'<pre class="language-{html.escape(language, quote=True)}"><code>{html.escape("\n".join(code))}</code></pre>')
            plain.extend(code)
        elif heading:
            flush_paragraph()
            level, text = len(heading.group(1)), _plain(heading.group(2))
            identifier = slugify(text)
            if identifier in seen:
                raise DocKitError(f"Markdown: duplicate heading id {identifier!r}")
            seen.add(identifier)
            headings.append((level, text, identifier))
            output.append(f"<h{level} id=\"{identifier}\">{_inline(heading.group(2), resolve_link)}</h{level}>")
            plain.append(text)
        elif line.startswith("> [!") and "]" in line:
            flush_paragraph()
            kind, text = line[4:].split("]", 1)
            kind = kind.strip().lower()
            if kind not in {"note", "tip", "important", "warning"}:
                raise DocKitError(f"Markdown: unsupported admonition {kind!r}")
            output.append(f'<aside class="admonition {kind}"><strong>{kind.title()}</strong><p>{_inline(text.strip(), resolve_link)}</p></aside>')
            plain.append(_plain(text))
        elif LIST.match(line) or ORDERED.match(line):
            flush_paragraph()
            ordered = bool(ORDERED.match(line))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while index < len(lines):
                match = ORDERED.match(lines[index]) if ordered else LIST.match(lines[index])
                if not match:
                    break
                items.append(f"<li>{_inline(match.group(1), resolve_link)}</li>")
                plain.append(_plain(match.group(1)))
                index += 1
            output.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        elif "|" in line and index + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1]):
            flush_paragraph()
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            header_html = "".join(f"<th>{_inline(cell, resolve_link)}</th>" for cell in headers)
            body_html = "".join("<tr>" + "".join(f"<td>{_inline(cell, resolve_link)}</td>" for cell in row) + "</tr>" for row in rows)
            output.append(f'<div class="table-scroll"><table><thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table></div>')
            plain.extend(headers)
            plain.extend(cell for row in rows for cell in row)
            continue
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line)
        index += 1
    flush_paragraph()
    title = next((text for level, text, _ in headings if level == 1), "Documentation")
    return RenderedMarkdown("\n".join(output), title, tuple(headings), re.sub(r"\s+", " ", " ".join(plain)).strip())
