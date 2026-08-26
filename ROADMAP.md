# DocKit-FP roadmap

DocKit-FP is for Free Pascal projects that want polished, versioned Markdown
documentation without maintaining a site generator. This roadmap is a guide to
direction, not a promise of dates. Feedback from library maintainers will set
the order within each milestone.

Every milestone must strengthen at least one of these promises:

1. A maintainer can create, learn and publish a documentation site without
   becoming a site-builder expert.
2. A project can organise sections, choose colours and express its identity
   through supported configuration rather than copied CSS.
3. The default site looks intentional, readable and excellent on every screen.
4. The generator stays small, offline-friendly and straightforward to maintain.

## Shipped in 0.1.0

- Safe Markdown-to-site builds with explicit navigation.
- Responsive light, dark and system themes, plus two project accent tokens.
- Local search, offline KaTeX mathematics and downloadable offline archives.
- Immutable historical builds and GitHub Pages publication from release tags.

## v0.2: make the first site effortless

The immediate focus is the path from an empty repository to a confident first
publication. The goal is a useful, good-looking first site in five minutes.

- [x] Improve `init` and `doctor` guidance so the next useful command is always
      obvious.
- [ ] Keep the beginner guide short, copyable and accurate, with one complete
      publish path from an empty directory to GitHub Pages.
- [ ] Offer a small, maintained example project that changes a section, a
      colour and a first additional page without custom CSS.
- [ ] Make validation messages more actionable for common configuration errors.
- [ ] Make every starter site responsive, keyboard-usable and visually polished
      before adding more surface area.

## v0.3: customise sections and identity without CSS forks

Projects should feel recognisably theirs while retaining the reliable DocKit-FP
shell.

- [ ] Define and document a simple navigation contract for adding, grouping and
      reordering left-side sections.
- [ ] Make navigation validation name the exact section, page and corrective
      action when a layout is invalid.
- [ ] Provide supported identity options for banners, footer information and
      project links instead of asking users to copy CSS.
- [ ] Add colour presets and contrast guidance alongside the existing semantic
      accent tokens.
- [ ] Publish visual examples for every supported customisation, including a
      before/after result and copyable configuration.

## v0.4: themes that are easy to choose, switch and extend

- [ ] Keep System, Light and Dark as dependable built-ins, including a clear
      keyboard-accessible switcher.
- [ ] Define a small semantic theme-token contract so new built-in themes do
      not require markup forks.
- [ ] Ship a curated set of visually distinct, accessible starter themes.
- [ ] Document the supported path for adding a theme and verify each theme in
      light, dark, mobile and long-document views.

## v0.5: maintain with confidence

- [ ] Expand safe Markdown authoring features based on real Pascal-project
      documentation needs.
- [ ] Improve search quality and keyboard navigation while keeping all assets
      local.
- [ ] Add release-oriented checks, examples and visual fixtures for
      multi-version sites.
- [ ] Test every supported configuration against generated HTML, responsive
      layout and accessibility expectations.
- [ ] Version configuration schemas deliberately; provide migration guidance,
      compatibility expectations and a stable upgrade policy on the path to 1.0.
- [ ] Keep dependencies, build steps and hosting requirements minimal and
      documented for contributors.

## Quality bar

No release is complete unless it is easy to start, easy to understand, easy to
customise and looks good with the default configuration. New visual features
must work without a CDN or framework, retain keyboard accessibility, respect
the existing responsive breakpoints and include a regression test or fixture.

## Non-goals

DocKit-FP will not become a Pascal source parser or API extractor. PasWeave
remains the companion tool for that job. DocKit-FP also will not require a
hosted service, JavaScript framework or CDN to build a useful documentation
site.

## How to influence it

Open an issue with the project structure you have, the command you expected to
run, the visual result you wanted and the result you received. Concrete
documentation pain points are more useful than feature votes: they help us
decide which small improvement makes the next project easier to document.
