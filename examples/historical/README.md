# Historical Pages example

This example demonstrates a two-tag history. To recreate it in a new repository:

1. Commit `releases/v1.0.0/docs` as `docs` and tag that commit `v1.0.0`.
2. Replace `docs` with this example's current `docs`, commit, and tag it `v1.1.0`.
3. Copy `.github/workflows/documentation.yml`, enable GitHub Pages with
   **GitHub Actions** as the source, and push both tags.
4. Run `dockit-fp check-release` and `dockit-fp build-all` before publication.

The current release must match `HEAD`; historical content remains sourced from
the immutable tags.
