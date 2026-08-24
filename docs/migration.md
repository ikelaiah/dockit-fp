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
