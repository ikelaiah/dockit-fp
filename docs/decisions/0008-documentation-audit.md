# Documentation audit

DocKit's existing `check` command validates configuration and builds a site,
but a successful build can still contain a public link to an unpublished page,
a missing fragment or an inaccessible image.

The `audit` command therefore builds a read-only model from configured public
pages, their real source references and renderer heading IDs. It reports only
probable publication mistakes. In particular, unlisted Markdown stays quiet
unless a published page links to it, and external URLs are not network-checked.

This keeps the command deterministic and useful in offline CI while preserving
the established separation: `check` is build correctness; `audit` is
publication-readiness diagnostics.
