# Customising sections and identity

DocKit-FP keeps the reading shell stable while letting a project name its own
sections, colours and links. These are supported configuration changes, not
CSS forks.

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

The result changes the accent, visible footer and project link while retaining
the responsive layout, keyboard focus treatment and System/Light/Dark modes.
