# DocKit-FP roadmap

DocKit-FP is for Free Pascal projects that want polished, versioned Markdown
documentation without maintaining a site generator. This roadmap is a guide to
direction, not a promise of dates. Feedback from library maintainers will set
the order within each milestone.

The path to 1.0 is guided by three promises:

1. **Easy to customise.** A project owner can shape content, cards, sections,
   identity and theme through documented configuration—not Python edits or CSS
   forks.
2. **Easy to use.** A maintainer can start, author, check and publish a site
   with short commands and useful guidance.
3. **Looks good.** The default site and every supported theme are intentional,
   readable, responsive and keyboard-accessible.

The generator will remain small, offline-friendly and straightforward to
maintain while delivering those promises.

## Shipped in v0.1.0–v0.5.0

- Safe Markdown-to-site builds, local search, offline KaTeX and immutable
  historical Git-release builds.
- A guided first-site path, actionable validation and maintained examples.
- Ordered navigation, identity options, colour presets and visual themes.
- Safe Markdown task lists, keyboard search, GitHub Pages publication and an
  explicit configuration-compatibility policy.

## v0.6.0: customise the homepage without code

The next release closes the gap between the attractive default home page and a
project's own story.

- [x] Make the homepage capability cards configurable, reorderable and
      removable through `dockit.json`.
- [x] Let a project choose whether the homepage shows the capability strip,
      banner, introduction and release context.
- [x] Provide copyable homepage recipes for a library, application and API
      reference site.
- [x] Ensure configuration errors identify the exact card or homepage field and
      suggest a correction.
- [x] Keep the default homepage unchanged for existing projects.

## v0.7.0: make authoring and navigation effortless

Writing and finding documentation should feel faster than maintaining a custom
site generator.

- [x] Add the highest-value safe Markdown features requested by Pascal project
      maintainers, with predictable generated HTML.
- [x] Make navigation editing easier with clear section/page summaries and
      useful checks for unreachable or unlisted content.
- [x] Improve search ranking, result previews and keyboard flows while keeping
      every asset local.
- [x] Add concise authoring recipes for common project documentation structures.

## v0.8.0: polish the visual system

Every built-in theme should look deliberate before custom visual surface area is
expanded.

- [x] Refine typography, spacing, tables, callouts, code blocks and long-form
      reading across Classic, Paper and Midnight.
- [x] Add configuration-level layout choices only where they preserve the
      shared semantic theme-token contract.
- [x] Publish visual fixtures for phone, tablet, desktop, light, dark and long
      document views.
- [x] Verify contrast, focus visibility and keyboard behaviour for every theme.

## v0.9.0: make publishing dependable

Release and hosting workflows should be boring, inspectable and hard to get
wrong.

- [x] Improve `doctor`, release checks and GitHub Pages guidance for common
      repository states.
- [x] Provide release-ready examples for a single-version site and a historical
      multi-version site.
- [x] Add deterministic release fixtures and a clear pre-publish checklist.
- [x] Document upgrade compatibility from every supported 0.x configuration.

## v0.11 — Existing Repo Magic

Safe existing-repository adoption, conservative README/docs discovery, sensible
initial navigation, explicit power-user control, safe root README support, and
`dockit-fp serve`.

## v0.12 — Beautiful by Default

Further visual refinement.

## v0.13 — GitHub in One Command

Reduce GitHub Pages publishing ceremony.

## v0.14 — Documentation Audit

Help maintainers identify documentation weaknesses.

## v0.15 — Qualification

Python/OS/package/ecosystem/accessibility qualification.

## v1.0 — Stable Contract

Version 1.0 is the commitment point: the supported configuration and workflow
become dependable foundations for Free Pascal projects.

- [ ] Declare the stable configuration contract, compatibility policy and
      deprecation process.
- [ ] Complete a full accessibility, responsive-layout and generated-HTML
      verification matrix for every supported configuration.
- [ ] Review public documentation, examples, CLI help and release workflow for
      a maintainer's first successful publication.
- [ ] Publish a migration guide from each 0.x release and a concise 1.0 upgrade
      checklist.
- [ ] Ship only when the three promises—easy to customise, easy to use and
      looks good—are demonstrably true.

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
