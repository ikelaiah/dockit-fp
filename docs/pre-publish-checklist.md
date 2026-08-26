# Pre-publish checklist

Use this checklist after documentation is ready and before pushing a release
tag. Commands assume the project root is the current directory.

## Every site

- [ ] Run `dockit-fp doctor` and resolve every `ERROR` and moving-ref warning.
- [ ] Run `dockit-fp check` and review the reported section/page totals.
- [ ] Commit the documentation and pinned Pages workflow.
- [ ] Confirm `git status --short` contains no intended release changes.
- [ ] Build locally and inspect phone, tablet, desktop, keyboard and theme flows.
- [ ] Confirm repository Settings → Pages uses **GitHub Actions**.

## Single-version site

- [ ] Omit `docs/versions.json`.
- [ ] Set `versioned: false` in the reusable-workflow call.
- [ ] Run `dockit-fp build --release latest --output build/docs-site`.
- [ ] Push the configured branch and confirm the Pages workflow succeeds.

## Historical site

- [ ] Add the release to `docs/versions.json`, make it `current`, and use the
      immutable tag that will identify this exact commit.
- [ ] Commit release preparation, then create the annotated tag, for example
      `git tag -a v1.2.0 -m "v1.2.0"`.
- [ ] Run `dockit-fp check-release`; the current tag must exist, match `HEAD`,
      and have no uncommitted documentation changes.
- [ ] Run `dockit-fp build-all --output build/docs-site` and inspect each release
      directory, the root redirect, `versions.json` and each `release.json`.
- [ ] Push the commit and tag, then confirm both CI and Pages deployment succeed.

Never move a published tag to repair documentation. Correct the source on a new
release and preserve the historical output.
