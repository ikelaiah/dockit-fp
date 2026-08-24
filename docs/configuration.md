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

Errors identify the relevant file and invalid field. Configuration is not a
CSS escape hatch: structural site styling remains in DocKit-FP.
