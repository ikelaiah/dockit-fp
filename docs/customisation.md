# Customising sections and identity

Use configuration to rename sections, choose colours and add project links.
DocKit-FP keeps the page layout and accessibility behaviour working, so you do
not need to copy or maintain its CSS.

## Before and after: navigation

Before, a small site has one section:

```json
{"navigation": [{"title": "Getting started", "pages": [{"title": "Overview", "path": "index.md"}]}]}
```

After, the left navigation has deliberate groups in the same written order:

```json
{"navigation": [
  {"title": "Getting started", "pages": [{"title": "Overview", "path": "index.md"}]},
  {"title": "Reference", "pages": [{"title": "API", "path": "reference/api.md"}]}
]}
```

## Before and after: project identity

Start with the default blue pair, then use a curated preset and small,
meaningful footer links:

```json
{
  "theme": {"preset": "purple"},
  "identity": {
    "footer": "Example-FP documentation",
    "links": [{"label": "Project", "url": "https://example.test"}]
  }
}
```

The result changes the highlight colour, visible footer and project link. The
phone layout, keyboard focus and System/Light/Dark modes continue to work.
