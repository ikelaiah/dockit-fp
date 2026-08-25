# ADR 0003: Publish DocKit-FP pages from release tags

DocKit-FP's own GitHub Pages deployment is triggered by a `v*` tag or an
explicit manual run. Each published site is built from the immutable reference
listed in `docs/versions.json`; ordinary `main` pushes do not change a released
documentation site. This makes the release selector, historical output and
published source agree.
