# Theming

DocKit-FP provides exactly System, Light and Dark modes. System follows the
browser preference; an explicit selection is retained in local storage when
available and otherwise safely falls back to System.

Projects customise identity through two semantic tokens, `accent` and
`accent_secondary`. The shared CSS uses them for links, focus and active
navigation while retaining its own structural layout. Teal (`#0f766e` / `#0891b2`),
blue (`#2563eb` / `#0ea5e9`), ocean (`#0369a1` / `#0284c7`) and purple
(`#7c3aed` / `#a855f7`) are all ordinary configurations, not project-specific
branches of the stylesheet.

An optional banner has a project-relative safe path and meaningful `alt` text.
Use it for identity, not for structural customisation.

The shared layout intentionally keeps the documentation tree on the left and
the page outline on the right. The article adds a reading-progress indicator
and previous/next-page links.
Code blocks include a copy control when the browser permits clipboard access.
