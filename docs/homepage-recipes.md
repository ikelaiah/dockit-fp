# Homepage recipes

Copy one of these optional `homepage` examples into `docs/dockit.json`, then
change the words for your project. They use supported settings, so you do not
need to copy Python or CSS when DocKit-FP changes.

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

Start directly with the reference navigation instead of a long introduction.
The release label helps readers match the page to the package version they use.

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
