# Quick start

Change the accent colours in `dockit.json` and rename the `Getting started`
section in `layout.json`, then run:

```bash
dockit-fp check
dockit-fp build --output build/docs-site
```

To add another page, create a Markdown file inside `docs/` and add it to the
ordered `navigation` list in `layout.json`.
