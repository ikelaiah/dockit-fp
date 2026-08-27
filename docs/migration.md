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

## Upgrade directly from any supported 0.x release

All released 0.x configurations use schema version 1. Upgrade the pinned package
and workflow to v0.10.0, then use this table before running `doctor`, `check`, and
the appropriate publish build.

| Starting release | Required compatibility work |
| --- | --- |
| v0.1.0 | For modern configuration, list every Markdown file in `layout.json`; keep legacy config-free documentation as-is. |
| v0.2.0 | List every modern Markdown file in navigation; existing project colours remain valid. |
| v0.3.0 | List every modern Markdown file in navigation; identity and preset fields remain valid. |
| v0.4.0 | List every modern Markdown file in navigation; Classic, Paper and Midnight names remain valid. |
| v0.5.0 | List every modern Markdown file in navigation; task lists and schema-version-1 files remain valid. |
| v0.6.0 | List every modern Markdown file in navigation; homepage settings remain optional and compatible. |
| v0.7.0, v0.7.1 or v0.7.2 | No configuration change is required. Keep immutable historical tags. |
| v0.8.0 | No configuration change is required; `layout.content_width` remains optional. |
| v0.9.0 | No configuration change is required; v0.9.1 improves guides and examples. |
| v0.9.1 | No configuration change is required; v0.9.2 keeps wrapped list items and callouts together. |
| v0.9.2 | No configuration change is required; v0.10.0 adds offline syntax highlighting. |

For historical publication, v0.9.0 additionally rejects unsafe release path
segments and option-like refs, requires the current source to match `HEAD`, and
requires documentation changes to be committed. These checks make existing
valid manifests more dependable; they do not change generated routes.

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

## v0.8.0 to v0.9.0

Existing versioned workflow callers remain in historical mode by default. The
new `versioned: false` input is only for single-version sites. Update workflow
action pins by consuming the v0.9.0 reusable workflow, run `doctor`, and resolve
any newly reported missing tag, mismatched `HEAD`, uncommitted docs or moving
workflow ref before publication.

## v0.9.0 to v0.9.1

No configuration change is required. Update package and workflow pins to
v0.9.1. The generated site and release validation remain compatible; this
patch release makes the learning and publishing instructions easier to follow.

## v0.9.1 to v0.9.2

No configuration change is required. Update package and workflow pins to
v0.9.2, then rebuild the site. Wrapped list-item text and multi-line
GitHub-style callouts now render as one readable component.

## v0.9.2 to v0.10.0

No configuration change is required. Update package and workflow pins to
v0.10.0, then rebuild the site. Fenced JSON, Pascal, Python, Bash, YAML and
Markdown blocks receive local syntax highlighting; other fence languages stay
safe, readable plain code.
