# Architecture

DocKit-FP has five small layers: configuration discovery, validation, safe
Markdown rendering, static-site generation, and immutable-version orchestration.
The package carries the CSS and browser code so consuming projects do not copy
the implementation. `build` renders a working tree for preview; `build-all`
archives every declared Git tag or full SHA into an isolated temporary tree.

The public compatibility contract consists of CLI commands/options, JSON schema
versions, generated route and search-index shapes, semantic theme token names,
and reusable-workflow inputs. Breaking any of these requires a SemVer major
release. Downstream projects should pin released tags such as `v0.1.0`, never
the main branch.
