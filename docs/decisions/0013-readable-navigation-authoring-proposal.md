# Decision 0013: A readable navigation authoring format

## Status

Proposed. This file describes a possible next change; `layout.json` remains
the supported format in v1.1.10.

## Problem

Navigation is an ordered outline, but `layout.json` expresses every page as an
object inside nested `pages` arrays. As a site grows, authors spend more time
moving braces and commas than arranging pages. `docsprout init` previously
made this worse by spreading each generated page over several lines. Compact
generated page objects help, but they do not change the authoring model.

The format must keep the current publication rule explicit: only listed pages
are published when `unlisted` is `exclude`. It must also represent the home
page, display titles, order, sections, one level of collapsible groups, the
root README, and a group's `expanded` setting.

## Recommendation

Explore an optional `docs/layout.md` as a single, constrained outline format.
For example:

```markdown
Layout-Version: 1
Home: index.md
Unlisted: exclude

# Start here
- [Overview](index.md)

## Quickstart
- [Your first site](beginners-guide.md)
- [Build and inspect](building.md)

# Reference
- [Configuration](configuration.md)
```

The headings express sections and groups; links express page titles, paths and
order. The top lines express publication settings. A root README would use the
exact relative target `../README.md`, never arbitrary traversal. A simple
group attribute, such as `## Quickstart {expanded}`, could preserve the
existing expansion option. The precise syntax needs a separate specification
before implementation, especially escaping in titles and paths and useful
line-numbered errors.

`layout.json` must continue to load unchanged throughout v1.x. A project
would use exactly one of `layout.json` and `layout.md`; both present would be
an error. The new outline would map into the same validated navigation model,
so publishing, auditing, search, and routes would not gain a second set of
rules. An explicit converter could help large existing sites migrate without
rewriting their content.

## Alternatives

- **Replace JSON with TOML:** comments and fewer commas help small settings,
  but repeated arrays of tables remain cumbersome for ordered pages inside
  groups. Python 3.10 support also needs a TOML parser dependency or a raised
  minimum Python version. TOML is better suited to site metadata than to this
  outline.
- **Put navigation in each page's front matter:** adding a page becomes easy,
  but global order and publication become distributed across many files.
  Reviewing the site map would require reading or generating another view.
- **Keep only JSON:** compact entries improve the generated file, but nested
  editing remains the main authoring task.

## Acceptance criteria for a follow-up implementation

- Existing schema-1 `layout.json` sites build without changes.
- The two formats produce identical site models for equivalent layouts.
- `layout.md` is treated as configuration during discovery and unlisted-page
  checks, never as publishable documentation content.
- Ambiguous dual files, duplicate pages, invalid paths, unsupported nesting,
  and malformed outline lines fail with file and line context.
- `init`, `serve`, `check`, `audit`, historical builds, examples, and user docs
  handle the chosen format consistently.
- A maintainer can add, move, or rename a page by editing one outline line.
