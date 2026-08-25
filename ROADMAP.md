# DocKit-FP roadmap

DocKit-FP is for Free Pascal projects that want polished, versioned Markdown
documentation without maintaining a site generator. This roadmap is a guide to
direction, not a promise of dates. Feedback from library maintainers will set
the order within each milestone.

## Shipped in 0.1.0

- Safe Markdown-to-site builds with explicit navigation.
- Responsive light, dark and system themes, plus two project accent tokens.
- Local search, offline KaTeX mathematics and downloadable offline archives.
- Immutable historical builds and GitHub Pages publication from release tags.

## Next: make the first site effortless

The immediate focus is the path from an empty repository to a confident first
publication.

- [ ] Keep the beginner guide short, copyable and accurate.
- [ ] Improve `init` and `doctor` guidance so the next useful command is always
      obvious.
- [ ] Offer a small, well-explained example project for trying themes,
      navigation and a first additional page.
- [ ] Make validation messages more actionable for common configuration errors.

## Then: customise without CSS forks

Projects should feel recognisably theirs while retaining the reliable DocKit-FP
shell.

- [ ] Extend documented identity options beyond the two accent tokens where a
      semantic option is genuinely reusable.
- [ ] Provide supported choices for banners, footer information and project
      links instead of asking users to copy CSS.
- [ ] Add visual examples for each supported customisation in the documentation.

## Later: authoring and release confidence

- [ ] Expand safe Markdown authoring features based on real Pascal-project
      documentation needs.
- [ ] Improve search quality and keyboard navigation while keeping all assets
      local.
- [ ] Add release-oriented checks and examples for multi-version sites.
- [ ] Publish compatibility expectations and a stable upgrade policy on the
      path to 1.0.

## Non-goals

DocKit-FP will not become a Pascal source parser or API extractor. PasWeave
remains the companion tool for that job. DocKit-FP also will not require a
hosted service, JavaScript framework or CDN to build a useful documentation
site.

## How to influence it

Open an issue with the project structure you have, the command you expected to
run, and the result you wanted. Concrete documentation pain points are more
useful than feature votes: they help us decide which small improvement makes
the next project easier to document.
