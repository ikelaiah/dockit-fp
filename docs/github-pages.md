# GitHub Pages

Use the reusable workflow pinned to a release, never `main`:

```yaml
jobs:
  documentation:
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.1.0
    permissions:
      contents: read
      pages: write
      id-token: write
```

The workflow checks configuration and immutable release metadata, builds every
version and uploads only a successfully validated site. Ensure checkout has
access to all release tags.

DocKit-FP itself calls this workflow from `deploy-docs.yml`. Its deployment is
triggered by a `v*` release tag (or manually), so a live Pages site always
corresponds to an immutable entry in `docs/versions.json`.
