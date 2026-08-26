# GitHub Pages

Use the reusable workflow pinned to a release, never `main`. Choose one of the
two supported publication modes.

## Historical multi-version site

Historical mode is the backward-compatible default. It requires
`docs/versions.json`, immutable tags or full commit SHAs, and a current source
that matches the checked-out `HEAD`:

```yaml
jobs:
  documentation:
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.9.0
    permissions:
      contents: read
      pages: write
      id-token: write
```

The workflow checks configuration and release metadata, builds every declared
version, and uploads only a successfully validated site. Trigger it from a
`v*` tag and ensure the repository checkout can read all declared tags. See the
[historical example](https://github.com/ikelaiah/dockit-fp/tree/v0.9.0/examples/historical).

## Single-version site

A project that publishes only the current branch can omit `versions.json` and
opt out of historical mode:

```yaml
jobs:
  documentation:
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.9.0
    with:
      versioned: false
      release: latest
    permissions:
      contents: read
      pages: write
      id-token: write
```

The `release` input is a display label passed safely to the build through an
environment variable. See the [single-version example](https://github.com/ikelaiah/dockit-fp/tree/v0.9.0/examples/single-version).

For either mode, enable Pages with **GitHub Actions** as the source. Run
`dockit-fp doctor` to confirm which workflow mode DocKit-FP detects, then follow
the [pre-publish checklist](pre-publish-checklist.md).

DocKit-FP itself calls the local reusable workflow from `deploy-docs.yml`. Its
deployment is triggered by a `v*` release tag (or manually), so the live Pages
site corresponds to an immutable entry in `docs/versions.json`.
