# Configure your site

You can build a useful site with the files created by `dockit-fp init`. Change
one thing at a time, run `dockit-fp check`, and keep the last working version in
Git when possible.

## The three configuration files

| File | What it controls | When you need it |
| --- | --- | --- |
| `docs/dockit.json` | Project name, colours and home-page presentation | Created by `init` |
| `docs/layout.json` | Published pages, navigation order and the home page | Created by `init` |
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

`layout.json` decides what is public and which published page is the front door.
`home` selects the Markdown page generated as `index.html`; the `homepage`
object in `dockit.json` only controls how that selected home page is presented.

```json
"home": {"path": "getting-started.md"}
```

The target must already be listed in `navigation`. For the repository-root
README, use `"home": {"path": "README.md", "source": "root"}`. Existing
layouts without `home` keep the compatible inference: root README, then
`docs/index.md`, then the first listed page.

Edit `docs/layout.json` to choose which pages appear and in what order:

```json
{
  "schema_version": 1,
  "unlisted": "exclude",
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

Each default `path` starts inside `docs/`. For example,
`"path": "reference/commands.md"` means the file is
`docs/reference/commands.md`.

`unlisted` controls what happens to Markdown under `docs/` that is not in
navigation:

- `"error"` is the default and preserves existing strict validation. A missing
  page is reported by `dockit-fp check`.
- `"exclude"` publishes only listed pages. `check` succeeds and reports the
  number of unlisted documents excluded from the site.

New layouts made by `dockit-fp init` use `"exclude"`. Existing layouts are
never rewritten; add the field only when you want this explicit publication
policy. There are no include/exclude patterns: the navigation list is the
complete publication decision.

## Existing repositories and root README

On its first run, `dockit-fp init` considers only `README.md` at the repository
root and Markdown under `docs/`. It does not modify either one. Ancillary root
files such as `CHANGELOG.md` and `CONTRIBUTING.md` are deliberately excluded;
detection is not permission to publish.

The generated layout uses this narrow entry for a root README:

```json
{"title": "Overview", "path": "README.md", "source": "root"}
```

`"source": "root"` supports only the exact repository-root `README.md`; it
does not permit `../README.md`, another root file, or any path outside the
repository. A README can link to a configured `docs/` page and a docs page can
link back to the README. Historical builds read the README from the matching
Git release archive.
Only the repository-root `README.md` has special root-source support. Other
Markdown you want to publish should live under `docs/`.

After `layout.json` exists it is authoritative. DocKit will not discover new
pages, alter order or titles, add ancillary files, or reorganise sections. Add
an ancillary page only by deliberately listing an allowed docs-path in the
layout (for example, after copying or authoring a public docs version yourself).

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

Link URLs must begin with `https://` or `http://`. DocKit safely escapes the
visible text.

## Home-page presentation

The default home page works without extra configuration. When you want to
change that page's cards or visible sections, add a `homepage` object to
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

Start from a complete example in [Customize the home page](homepage-recipes.md).

## Release history can wait

Do not add `docs/versions.json` for a local preview or a single-version site.
Add it only when you decide to preserve documentation for older releases. The
[GitHub Pages guide](github-pages.md) helps you choose, and the
[glossary](glossary.md) explains terms such as tag, source ref and immutable.
