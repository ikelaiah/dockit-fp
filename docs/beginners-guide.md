# Your first DocKit-FP site

This guide starts from an ordinary code project and ends with a documentation
site running on your computer. The example name is Pascal-flavoured, but the
steps work for any project that uses Markdown.

Allow about 10 minutes. You can stop after the preview works; publishing is a
separate task for another day.

## Before you begin

You need:

- Python 3.10 or newer;
- an internet connection for installation;
- a code project, even a tiny practice project;
- a terminal and a text editor.

You do **not** need Git, a GitHub account, a web server or Pascal knowledge for
this guide. When this page says “project folder”, it means the top-level folder
that normally contains `README.md` or `src/`.

## 1. Install DocKit-FP

Open a terminal in your project folder and run:

```bash
python -m pip install "https://github.com/ikelaiah/dockit-fp/archive/refs/tags/v0.12.1.zip"
```

Then check that the command is available:

```bash
dockit-fp --help
```

You should see a list of commands such as `build`, `check`, `init` and `serve`.

> [!NOTE] If your terminal says `dockit-fp` was not found, close and reopen the
> terminal. You can also run `python -m dockit_fp --help`.

## 2. Adopt the Markdown you already have

Run this from the same project folder:

```bash
dockit-fp init
```

You should see a message beginning with `Initialised`. The command detects a
root `README.md`, Markdown inside `docs/`, Git/GitHub details, and common
ancillary Markdown. It never rewrites, moves or copies existing Markdown. It
creates only missing DocKit configuration:

```text
docs/
├── dockit.json   # project name and colours
├── layout.json   # pages and navigation order
└── index.md      # only when there was no README or docs page
```

By default, DocKit publishes only `README.md` and `docs/**/*.md`. It tells you
about `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` and
`CODE_OF_CONDUCT.md`, but leaves them private until you choose to add them.
Only the repository-root `README.md` has special root-source support. Other
Markdown you want to publish should live under `docs/`.

## 3. See the site now

Run:

```bash
dockit-fp serve
```

Open <http://127.0.0.1:8000>. The command validates and builds first, then
starts a local-only preview server. It watches `README.md` and `docs/`, rebuilding
after a saved change; reload the browser to see the new page without restarting
the command. Press `Ctrl+C` to stop it. Use
`dockit-fp serve --port 8000` or `dockit-fp serve --host 127.0.0.1` when you
need a specific local address.

> [!IMPORTANT] You have finished the beginner path. The site works locally.
> You do not need release tags or GitHub Pages until you choose to publish.

## 4. Make the site yours

If `init` created `docs/index.md`, open it and replace its text with something
small. Otherwise edit the existing `README.md` or a page under `docs/`:

```markdown
# Star Mapper

Star Mapper turns telescope readings into a searchable sky map.

## Start here

Read the quick start to make your first map.
```

The first `#` is the page title. A line beginning with `##` is a section title.
That is enough Markdown to begin.

Next, open `docs/dockit.json`. `init` has already inferred safe metadata where
it could, including a GitHub repository URL. Change the project name and description if needed. Leave
`schema_version` unchanged:

```json
{
  "schema_version": 1,
  "project": {
    "name": "Star Mapper",
    "description": "Make a searchable map from telescope readings."
  },
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#0891b2"
  }
}
```

## 5. Control the navigation explicitly

`docs/layout.json` is now maintainer-owned. DocKit never silently adds new
Markdown, reorders sections, renames entries or removes pages after this file
exists. Edit it whenever you want to include, remove, rename or reorder a page.
New layouts set `"unlisted": "exclude"`, which means pages appear only when
they are listed; `check` reports any Markdown it leaves out. Existing layouts
keep strict unlisted-page errors until you explicitly add that setting.
The [Configuration](configuration.md) guide shows the exact format, including
the safe root README entry.

## 6. Check before you publish

Run:

```bash
dockit-fp check
```

Success looks similar to:

```text
Documentation check passed: 1 section(s), 1 page(s)
```

If a check fails, read the final line first. It normally names the file and the
next correction. You can also run `dockit-fp doctor` for a setup summary.

## 7. Add one useful page

Think of the first thing a new user wants to achieve. Create
`docs/quick-start.md` and show that one task:

```markdown
# Quick start

Install Star Mapper, then run `star-mapper import first-light.csv`.

You should see `Created sky-map.html`.
```

Open `docs/layout.json`. Your file may look different from this example: in
particular, its Overview or home entry may use `index.md` instead of the
repository-root `README.md`. Keep that existing entry unchanged.

Before the change, the file may look like this:

```json
{
  "schema_version": 1,
  "unlisted": "exclude",
  "navigation": [
    {
      "title": "Getting started",
      "pages": [
        {
          "title": "Overview",
          "path": "README.md",
          "source": "root"
        }
      ]
    }
  ]
}
```

Add this new page object to the same `pages` list:

```json
{
  "title": "Quick start",
  "path": "quick-start.md"
}
```

After adding the page, the file may look like this:

```json
{
  "schema_version": 1,
  "unlisted": "exclude",
  "navigation": [
    {
      "title": "Getting started",
      "pages": [
        {
          "title": "Overview",
          "path": "README.md",
          "source": "root"
        },
        {
          "title": "Quick start",
          "path": "quick-start.md"
        }
      ]
    }
  ]
}
```

In JSON lists, put a comma after each item except the last one.

Run:

```bash
dockit-fp check
dockit-fp serve
```

Reload the browser. **Quick start** should now appear in the left navigation.

## Where to go next

- Learn a simple, language-neutral writing method in
  [Write documentation people can use](writing-great-docs.md).
- Learn the three configuration files in [Configuration](configuration.md).
- Copy a small working project from the
  [minimal example](https://github.com/ikelaiah/dockit-fp/tree/v0.12.1/examples/minimal).
- When you truly want a public site, choose the simpler or historical path in
  [GitHub Pages](github-pages.md).
- Look up unfamiliar words in the [glossary](glossary.md).
