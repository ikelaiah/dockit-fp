# Implementation Plan: v0.12.0 — Beautiful by Default

## Overview

Refine DocKit-FP's existing generated site so a minimally configured Markdown
project feels publication-ready in Classic by default, while Paper and
Midnight remain coherent. The work stays inside the existing shell, homepage,
navigation, theme-token and local-asset systems; it adds no theme engine,
dependency, configuration key or alternate landing-page architecture.

## Architecture decisions

- Keep the shared visual contract in the generated `site.css` and use semantic
  data attributes from the existing HTML shell only where CSS needs page/card
  context.
- Preserve the current search, theme, version, navigation and copy behavior;
  improve their grouping, states and responsive layout through markup hooks and
  CSS/vanilla JavaScript only.
- Use the existing `examples/visual-fixtures` project and DocKit-FP's own docs
  as the visual acceptance surfaces. Keep visual regression assertions focused
  on generated semantics and stable design tokens rather than brittle pixel
  snapshots.

## Task list

### Phase 1: shared foundation

- [ ] Task 1: Add release regression coverage for the generated shell.
  - Acceptance: tests assert active navigation semantics, homepage/card context,
    grouped header controls, and the refined token/selectors without changing
    existing schemas.
  - Verification: focused build tests fail before the hooks exist, then pass.
  - Dependencies: None.

- [ ] Task 2: Refine shared layout tokens and document rhythm.
  - Acceptance: Classic has a calmer header, deliberate typography rhythm,
    readable content measure, restrained surfaces, and responsive 2/3/4-card
    homepage layouts; existing themes inherit the same semantic structure.
  - Verification: focused build tests, full unit suite, generated CSS review.
  - Dependencies: Task 1.

### Checkpoint: foundation

- [ ] Generated HTML remains valid and accessible by inspection.
- [ ] Full test suite and current docs build remain green.

### Phase 2: component polish

- [ ] Task 3: Polish code, tables and admonitions across theme/mode variants.
  - Acceptance: Pascal code remains readable, copy controls are discoverable,
    long lines scroll intentionally, tables retain readable row rhythm, and
    callouts are distinguishable without relying on colour alone.
  - Verification: fixture build plus browser screenshots at 360, 768 and
    1440px; no console warnings.
  - Dependencies: Task 2.

- [ ] Task 4: Polish search, outline, page navigation and mobile navigation.
  - Acceptance: existing keyboard flow and accessible names remain intact;
    selected/hover/focus states and mobile touch targets are clear; no page
    overflow occurs outside intentional code/table scrollers.
  - Verification: browser keyboard flow, DOM/accessibility inspection, focused
    generated-shell tests.
  - Dependencies: Task 2.

### Checkpoint: component coverage

- [ ] Classic/Paper/Midnight and Light/Dark combinations render coherently.
- [ ] Fixture covers homepage cards, banner/no-banner, long prose, API/code,
      tables, callouts, search and previous/next navigation.

### Phase 3: dogfood and release documentation

- [ ] Task 5: Update maintained fixture and DocKit-FP dogfood content only where
      needed to exercise v0.12 states.
  - Acceptance: fixture documentation describes the review matrix and the
    project's own homepage demonstrates the default result.
  - Verification: documentation check and fixture/current docs builds.
  - Dependencies: Tasks 3–4.

- [ ] Task 6: Update ROADMAP and CHANGELOG with concise v0.12 release notes.
  - Acceptance: v0.12 goal and user-facing improvements are documented without
    creating a new theming manual.
  - Verification: documentation tests and `dockit-fp check --root .`.
  - Dependencies: Task 5.

### Checkpoint: complete

- [ ] Full test suite passes.
- [ ] Current docs, visual fixture and historical release validation pass.
- [ ] Git diff reviewed for scope, accessibility and accidental dependencies.
- [ ] Release/PR/tag/Pages actions are reported separately if external GitHub
      authority is unavailable in this workspace.

## Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| CSS changes regress one of three visual themes | High | Retain semantic tokens, exercise all themes/modes in the fixture and inspect browser output. |
| Header or search polish breaks keyboard flow | High | Keep IDs and native controls, add generated semantics, test keyboard paths in a browser. |
| Wide content causes phone overflow | High | Keep min-width only on intentional scrollers and check computed document width at phone sizes. |
| Visual work becomes a broad redesign | Medium | No new schemas/dependencies/engines; cut P2 personality work if P0/P1 is not solid. |
| Release operations require remote authority | Medium | Complete local implementation/validation and report unperformed PR/tag/Pages steps honestly. |

## Open questions

- None required to start; the existing Classic/Paper/Midnight contract and
  current homepage configuration are sufficient for this release.
