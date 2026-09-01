# Customize the home page

The homepage is not another Markdown document. It is your existing home
document rendered as the site's `index.html`: normally the repository-root
`README.md` or `docs/index.md`, depending on your configuration. The
`homepage` settings in `docs/dockit.json` only change how that first page is
presented. You do not need them unless you want to customise the landing page.

The examples below are `homepage` values to add to your existing
`docs/dockit.json`; keep your `schema_version`, `project` and other settings.

## See it in DocKit-FP

DocKit-FP uses the same configuration on this site. Its
[`docs/dockit.json`](https://github.com/ikelaiah/dockit-fp/blob/v0.11.4/docs/dockit.json)
contains capability cards and release context:

```json
{
  "homepage": {
    "capabilities": [
      {"title": "Existing-project friendly", "description": "Start with the README and docs you already have."},
      {"title": "Offline/local assets", "description": "Built sites work without a CDN."}
    ],
    "sections": {"release_context": true}
  }
}
```

```text
docs/dockit.json
        ↓
homepage.capabilities
        ↓
capability cards below the opening summary on the DocKit-FP home page

homepage.sections.release_context
        ↓
the current release label above the DocKit-FP home page
```

Open the generated [DocKit-FP home page](index.md) to see both effects.

## Library

Use this when a library home page should make installation and API confidence
easy to scan. It adds three capability cards below the opening introduction
and shows the current release.

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

Use this when the home page should lead with a product banner and story. After
you add the image at the configured path, it shows the banner and introduction
but hides capability cards.

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

Use this when readers should reach a reference-oriented home page quickly. It
hides the opening introduction, adds two reference cards, and shows the
current release label.

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
