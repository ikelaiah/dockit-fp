# Single-version Pages example

Copy `docs/` and `.github/workflows/documentation.yml` into a project that
publishes only its current documentation. Enable GitHub Pages with **GitHub
Actions** as the source, then push `main` or run the workflow manually.

The workflow pins DocKit-FP and explicitly disables historical mode. Update the
pin deliberately when upgrading.
