# Configure your site

You can build a useful site with the files created by `dockit-fp init`. Change
one thing at a time, run `dockit-fp check`, and keep the last working version in
Git when possible.

## The three configuration files

| File | What it controls | When you need it |
| --- | --- | --- |
| `docs/dockit.json` | Project name, colours and optional homepage choices | Created by `init` |
| `docs/layout.json` | Page order and left navigation | Created by `init` |
| `docs/versions.json` | Published release history | Only for a historical site |

These files use JSON. Keep the commas, quotation marks and braces exactly
paired. Every file starts with `"schema_version": 1`; leave that value alone.
If the punctuation is wrong, `dockit-fp check` names the file and error.

## Project name and colours

Edit `docs/dockit.json`:

```json
{
  "schema_version": 1,
  "project": {
    "name": "MyLibrary-FP",
    "description": "Useful Pascal tools"
  },
  "theme": {
    "preset": "teal"
  }
}
```

The supported colour presets are `blue`, `teal`, `ocean` and `purple`. Start
with a preset. You can choose exact colours later in [Themes](themes.md).

## Pages and navigation

Edit `docs/layout.json` to choose which pages appear and in what order:

```json
{
  "schema_version": 1,
  "navigation": [
    {
      "title": "Get started",
      "pages": [
        {"title": "Overview", "path": "index.md"},
        {"title": "Quick start", "path": "quick-start.md"}
      ]
    },
    {
      "title": "Reference",
      "pages": [
        {"title": "Commands", "path": "reference/commands.md"}
      ]
    }
  ]
}
```

Each `path` starts inside `docs/`. For example,
`"path": "reference/commands.md"` means the file is
`docs/reference/commands.md`.

List every Markdown file under `docs/`. This prevents a useful page from
becoming invisible. If a file is missing or unlisted, `dockit-fp check` tells
you which path to add, create or correct.

## Reading width

Add `layout` inside `docs/dockit.json` when the default width does not suit the
content:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "layout": {
    "content_width": "wide"
  }
}
```

Choose:

- `compact` for short, prose-led tutorials;
- `comfortable` for the balanced default;
- `wide` for large tables and code samples.

Omit this setting to keep `comfortable`.

## Footer links

You can add a short footer and a few useful links inside `docs/dockit.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "identity": {
    "footer": "Built for Free Pascal maintainers.",
    "links": [
      {"label": "Source code", "url": "https://github.com/example/library"}
    ]
  }
}
```

Link URLs must begin with `https://` or `http://`. DocKit-FP safely escapes the
visible text.

## Homepage choices

The default homepage works without extra configuration. When you want to
change its cards or visible sections, add a `homepage` object to
`docs/dockit.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "homepage": {
    "capabilities": [
      {"title": "Offline", "description": "Every asset ships locally."},
      {"title": "Stable API", "description": "Guides follow each release."}
    ],
    "sections": {
      "release_context": true
    }
  }
}
```

Each card needs a non-empty `title` and `description`. An empty
`capabilities` list hides all cards. The optional section names are
`capabilities`, `banner`, `introduction` and `release_context`, and each accepts
`true` or `false`.

Start from a complete example in [Homepage recipes](homepage-recipes.md).

## Release history can wait

Do not add `docs/versions.json` for a local preview or a single-version site.
Add it only when you decide to preserve documentation for older releases. The
[GitHub Pages guide](github-pages.md) helps you choose, and the
[glossary](glossary.md) explains terms such as tag, source ref and immutable.
