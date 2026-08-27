# Single-version Pages example

Choose this example when readers only need the latest documentation. The site
updates from `main` and does not use release tags or `docs/versions.json`.

## Try it locally

From the DocKit-FP repository root, run:

```bash
dockit-fp check --root examples/single-version
dockit-fp build --root examples/single-version --release latest --output build/single-version-example
python -m http.server 8000 --directory build/single-version-example
```

Open <http://localhost:8000>. Press `Ctrl+C` to stop the server.

## Use it in your project

1. Copy this example's `docs/` folder and
   `.github/workflows/documentation.yml` file.
2. Replace the project name and words.
3. Run `dockit-fp check` and `dockit-fp build`.
4. In GitHub, set **Settings → Pages → Source** to **GitHub Actions**.
5. Push `main` and confirm the Documentation workflow is green.

The workflow pins DocKit-FP and sets `versioned: false`. Update the pin only
when you deliberately upgrade DocKit-FP.
