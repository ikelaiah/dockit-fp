# Implementation Plan: DocKit-FP 0.1.0

## Architecture

The pipeline is `configuration/source discovery -> validation -> Markdown
rendering -> version-aware HTML shell/assets/search -> owned output`. Historical
builds resolve Git refs before extracting a temporary source tree. The CLI
coordinates these library operations without embedding project-specific rules.

## Phases

1. Foundation: packaging, models/configuration, safe paths/output, CLI skeleton.
2. Content: Markdown subset, navigation discovery, link validation and renderer.
3. Site: shared responsive assets, themes, version selector and search.
4. History: ref validation, immutable multi-version builds, deterministic offline archives.
5. Delivery: fixtures, user docs, ADRs, CI/Pages workflow and quality review.

## Risks

| Risk | Mitigation |
| --- | --- |
| Historical tags lack modern files | Discover Markdown and deterministically choose a legacy homepage. |
| Output cleanup damages user data | Require and test a marker before replacement. |
| Markdown brings unsafe HTML/URLs | Escape source HTML and reject unsafe schemes/traversal. |
| Site behaviour diverges again | Put CSS, JavaScript and renderer inside the package; expose tokens only. |
