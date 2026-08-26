# Theming

DocKit-FP provides exactly System, Light and Dark modes. System follows the
browser preference; an explicit selection is retained in local storage when
available and otherwise safely falls back to System.

Projects customise identity through two semantic tokens, `accent` and
`accent_secondary`. The shared CSS uses them for links and active
navigation while retaining its own structural layout. Teal (`#0f766e` / `#0891b2`),
blue (`#2563eb` / `#0ea5e9`), ocean (`#0369a1` / `#0284c7`) and purple
(`#7c3aed` / `#a855f7`) are all ordinary configurations, not project-specific
branches of the stylesheet.

Use one of those curated pairs with `theme.preset`; an explicit accent token
can still override either colour when a project already has an accessible
palette:

```json
{"theme": {"preset": "purple"}}
```

The supported preset names are `blue`, `teal`, `ocean` and `purple`. Check
link and focus contrast against both Light and Dark before choosing custom
tokens.

## Visual starter themes

Every site has a second, keyboard-accessible **Documentation visual theme**
selector. `classic` is the dependable default; `paper` gives long guides a warm
reading surface, and `midnight` is a deliberately dark technical theme. All
three use the same semantic background, surface, text, border and code tokens,
so adding a built-in theme never needs a markup fork.

Set the initial choice in configuration:

```json
{"theme": {"style": "midnight"}}
```

Visitors may switch among Classic, Paper and Midnight independently of
System, Light and Dark mode; their choice is retained locally. Each visual
theme provides deliberate light and dark surfaces, local font stacks and a
high-contrast focus ring without changing the semantic HTML.

Use the maintained [visual fixtures](visual-fixtures.md) to verify themes at
phone, tablet and desktop widths, with a long document and every colour mode.

An optional banner has a project-relative safe path and meaningful `alt` text.
Use it for identity, not for structural customisation.

The shared layout intentionally keeps the documentation tree on the left and
the page outline on the right. The article adds a reading-progress indicator
and previous/next-page links.
Code blocks include a copy control when the browser permits clipboard access.
