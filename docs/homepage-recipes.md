# Homepage recipes

These optional `homepage` snippets belong in `docs/dockit.json`. They use only
the supported configuration contract, so they survive DocKit-FP upgrades
without copied Python or CSS.

## Library

Lead with installation and API confidence while retaining the standard
introduction from `index.md`.

```json
{
  "homepage": {
    "capabilities": [
      {"title": "Installable", "description": "Small, versioned Pascal packages."},
      {"title": "Documented API", "description": "Find each public unit quickly."},
      {"title": "Offline", "description": "Build and browse without a CDN."}
    ],
    "sections": {"release_context": true}
  }
}
```

## Application

Use a project banner and focus the home page on the product story. An empty
card list hides the capability strip while leaving the rest of the document
intact.

```json
{
  "banner": {"path": "docs/assets/banner.png", "alt": "The Acme Desktop application"},
  "homepage": {
    "capabilities": [],
    "sections": {"banner": true, "introduction": true}
  }
}
```

## API reference

Start directly with the reference navigation rather than a marketing-style
introduction. Release context helps callers match documentation to a package
version.

```json
{
  "homepage": {
    "capabilities": [
      {"title": "Units", "description": "Organised by namespace and purpose."},
      {"title": "Versions", "description": "Release history remains available."}
    ],
    "sections": {
      "introduction": false,
      "release_context": true
    }
  }
}
```

Run `dockit-fp check` after changing configuration. Its diagnostics identify
the specific card or section field and provide a correction.
