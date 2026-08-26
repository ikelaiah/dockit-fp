# Migration

Migrate gradually from local `tools/build_docs.py`, `build_all_docs.py`,
`check_built_docs.py` and `tools/docs_assets/` copies:

1. Pin a released DocKit-FP version.
2. Add `dockit.json` and `layout.json` around the existing Markdown.
3. Reproduce and compare the current site.
4. Add and verify historical `versions.json` entries.
5. Switch the Pages workflow and run `check`, `check-release`, and `build-all`.
6. Delete the old local machinery only after output behaviour matches.

Do not rewrite historical tags or remove the old builder first.

## Configuration compatibility

DocKit-FP configuration is versioned deliberately. v0.5 supports
`"schema_version": 1` for `dockit.json`, `layout.json` and `versions.json`.
Version 1 additions are optional and remain backwards compatible: a project can
adopt presets, identity fields and visual themes one at a time.

Future schema versions will fail clearly rather than being guessed at. A major
schema change will ship with release notes, a migration guide, compatibility
expectations and—when mechanical conversion is safe—a migration command. Keep
each published release manifest on immutable tags while upgrading.

## v0.5.0 to v0.6.0

No migration is required. Existing homepages retain their v0.5.0 output.
Adopt the optional `homepage` object only when you want to replace capability
cards or control homepage sections.

## v0.6.0 to v0.7.0

Modern documentation trees now require every `docs/**/*.md` file to be listed
in `layout.json`. Run `dockit-fp check`; add each reported path to an
appropriate section, or remove documentation that should no longer ship.
Existing Markdown rendering remains compatible, and definition lists are an
optional authoring feature.

## v0.7.0 to v0.7.1

No migration is required. v0.7.1 restores successful `build-all` publication
when an immutable historical tag contains modern documentation authored before
v0.7.0's strict navigation-completeness check. Current documentation remains
subject to that check.

## v0.7.1 to v0.7.2

No migration is required. When the Classic visual theme is selected, System
colour mode now follows a dark operating-system preference as documented.

## v0.7.2 to v0.8.0

No migration is required. Existing sites retain the comfortable content width.
Adopt the optional `layout.content_width` setting only when a compact tutorial
or wide reference layout better suits the documentation. Theme polish applies
through the existing semantic token contract and requires no CSS copies.
