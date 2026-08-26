# Your first DocKit-FP site

This guide takes a small Free Pascal project from no documentation site to a
local preview. You need Python 3.10 or newer. Git is only needed when you are
ready to publish a versioned release.

## 1. Install and initialise

From your project root:

```bash
python -m pip install "dockit-fp==0.2.0"
dockit-fp init
```

`init` creates a safe preview-ready starting point and refuses to overwrite an
existing `docs/` tree. It creates these three files:

```text
docs/
├── dockit.json
├── layout.json
└── index.md
```

## 2. Read the three files

`docs/index.md` is your home page. Write normal Markdown there.

`docs/dockit.json` is your project identity. Start by changing the name and
description:

```json
{
  "schema_version": 1,
  "project": {
    "name": "MyLibrary-FP",
    "description": "A useful Free Pascal library."
  },
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#0891b2"
  }
}
```

Those two colours are the supported way to make the site feel like your
project. You do not need to copy or maintain DocKit-FP's CSS.

`docs/layout.json` controls the order and labels in the navigation.

The repository's [minimal example](../examples/minimal/) is the same complete
structure with a second page and two supported colour choices. Copy it when
you want a starting point, then replace its project name and words.

## 3. Add your first page

Create `docs/quick-start.md`:

```markdown
# Quick start

Install the library, then create your first value.
```

Add it to `docs/layout.json`:

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
    }
  ]
}
```

Every page in the navigation must be a Markdown file inside `docs/`. This is
intentional: it makes broken navigation an early, readable error instead of a
surprise on the published site.

## 4. Preview before publishing

Check first, then build:

```bash
dockit-fp check
dockit-fp build --output build/docs-site
python -m http.server 8000 --directory build/docs-site
```

Open `http://localhost:8000`. The preview includes the theme picker, search,
mobile navigation and local KaTeX mathematics. Stop the web server with
`Ctrl+C` when you are done.

## 5. Add a banner only when it helps

An optional project-local image can appear on the home page. Give it useful
alternative text:

```json
{
  "banner": {
    "path": "assets/project-banner.svg",
    "alt": "MyLibrary-FP logo"
  }
}
```

Add this object alongside `project` and `theme` in `docs/dockit.json`. Keep the
image in your repository; DocKit-FP copies it into the built site.

## 6. Publish a version only when you are ready

Local previews do not need version metadata. Before publishing, choose an
immutable release name such as `v1.0.0`, add this manifest, commit it, then tag
that commit:

```json
{
  "schema_version": 1,
  "current": "1.0.0",
  "versions": [
    {"release": "1.0.0", "source_ref": "v1.0.0"}
  ]
}
```

Save it as `docs/versions.json`, then:

```bash
git add docs/versions.json
git commit -m "Prepare v1.0.0 documentation"
git tag -a v1.0.0 -m "v1.0.0"
git push origin main v1.0.0
```

Use the reusable GitHub Pages workflow described in [GitHub Pages](github-pages.md).
It builds the exact tagged source, so later edits on `main` never rewrite a
published release.

## When something does not work

Run:

```bash
dockit-fp doctor
```

It reports whether DocKit-FP found modern configuration, legacy Markdown, and
release metadata. Then run `dockit-fp check`; its errors name the file and
field that need attention, and suggest the next corrective action for common
configuration mistakes.
