# Publish with GitHub Pages

GitHub Pages can host the files built by DocKit. Your documentation should
work locally before you begin this page.

You need a GitHub repository and permission to change its settings. If Git or
GitHub Actions is new to you, the [glossary](glossary.md) explains the terms.

## Choose one publishing path

| Choose | When it fits | What readers see |
| --- | --- | --- |
| **Single-version** | You only need the latest documentation | One site that updates when `main` changes |
| **Historical** | Readers use several released versions | A version selector and one site per release tag |

When you are unsure, choose single-version. You can add release history later.

## Single-version site: the simpler choice

Do not create `docs/versions.json` for this path.

Create `.github/workflows/documentation.yml` with this complete file:

```yaml
name: Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  documentation:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.13.0
    with:
      versioned: false
      release: latest
```

The workflow runs after a push to `main`. `workflow_dispatch` also adds a button
for starting it manually from GitHub's Actions page.

Check the same path locally:

```bash
dockit-fp doctor
dockit-fp check
dockit-fp build --release latest --output build/docs-site
```

The final command should say how many pages it built. Open the result locally
before pushing. The maintained
[single-version example](https://github.com/ikelaiah/dockit-fp/tree/v0.13.0/examples/single-version)
contains the same setup.

## Historical site for versioned projects

Choose this path when old documentation must stay available. You need Git tags
and `docs/versions.json`. A tag is a stable name for one saved Git commit; see
[Historical documentation](historical-docs.md) for the manifest.

Create `.github/workflows/documentation.yml` with this complete file:

```yaml
name: Documentation

on:
  push:
    tags: ["v*"]
  workflow_dispatch:

jobs:
  documentation:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.13.0
```

The workflow runs when you push a tag such as `v1.2.0`. Historical mode is the
default, so it does not need a `with` section.

Check the release locally after creating its tag and before pushing it:

```bash
dockit-fp doctor
dockit-fp check
dockit-fp check-release
dockit-fp build-all --output build/docs-site
```

Follow the [pre-publish checklist](pre-publish-checklist.md) for the exact
commit, tag, check and push order. The maintained
[historical example](https://github.com/ikelaiah/dockit-fp/tree/v0.13.0/examples/historical)
shows a small two-release project.

## Enable Pages in the repository

Do this once for either path:

1. Open the repository on GitHub.
2. Select **Settings**, then **Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push the workflow and the trigger for your chosen path.
5. Open the repository's **Actions** page and wait for the Documentation run.

A green run includes check, build, upload and deploy steps. GitHub shows the
public site URL after deployment.

## If the workflow does not run

- Confirm the file is inside `.github/workflows/` and ends in `.yml` or `.yaml`.
- For single-version mode, confirm you pushed the configured branch.
- For historical mode, confirm you pushed a tag beginning with `v`.
- Open the failed Actions step and read its final error before retrying.
- Run the same DocKit command locally; local errors are usually faster to
  correct.

Always pin a released workflow such as `@v0.13.0`. Do not use `@main` for a
published site: a future DocKit change could alter your site without a
deliberate upgrade.
