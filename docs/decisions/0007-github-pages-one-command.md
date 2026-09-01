# ADR 0007: Generate one managed GitHub Pages caller workflow

DocKit's GitHub Pages path must work offline and preserve maintainer control.
`dockit-fp github-pages` therefore reuses existing `init` discovery, then
generates only `.github/workflows/dockit-pages.yml`. The caller is a short,
deterministic workflow that invokes DocKit's reusable workflow at the running
release tag; it never calls a GitHub API, commits, pushes or changes repository
settings.

The caller has a stable DocKit ownership marker. Exact current content is
idempotent, recognised older content is changed only by `--update`, and missing
or malformed ownership evidence is refused rather than overwritten. This avoids
introducing a YAML dependency while making the generated file understandable
and safe to recognise.

The workflow is triggered by pushes and manual dispatch, but its job is gated
to GitHub's default branch from event metadata. This avoids assuming `main` and
prevents Pages deployment from feature branches. It intentionally configures a
single current site; historical tag publishing remains an advanced workflow.

DocKit's own release workflow stays local because it builds immutable history
and cannot consume the new v0.14 reusable workflow until v0.14 itself is
tagged. The checked-in generated-workflow fixture provides pre-release coverage
without a circular self-reference.
