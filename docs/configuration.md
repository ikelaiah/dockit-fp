# Configuration

Modern documentation uses three optional-to-required-in-combination JSON files.
Every configuration object has `"schema_version": 1`; an unknown version is an
error so schema evolution is explicit.

`docs/dockit.json` owns project identity:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP", "description": "Useful Pascal tools"},
  "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"}
}
```

`docs/layout.json` owns ordered navigation. Every listed `.md` path must be a
safe path beneath `docs/` and must exist. `docs/versions.json` declares
published releases, their immutable tag or full commit SHA, and the current
release. Development `build` may use the working tree; published `build-all`
does not.

Navigation is rendered in the order written: each object is one left-side
section, and each page is rendered in its listed order. To regroup or reorder
pages, edit only `navigation`; every section must have a title and at least one
existing Markdown page. Errors name the section or page and tell you whether to
add, create or correct it.

`dockit.json` also supports project identity without copied CSS:

```json
{
  "identity": {
    "footer": "Built for Free Pascal maintainers.",
    "links": [{"label": "Source code", "url": "https://github.com/example/library"}]
  }
}
```

Footer text and links are escaped and links must be absolute HTTP(S) URLs.
Configuration is not a CSS escape hatch: structural site styling remains in
DocKit-FP.
