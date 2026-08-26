# v0.2.0 onboarding release plan

## Objective

Make the first ten minutes with DocKit-FP clear enough that a Free Pascal
maintainer can initialise documentation, understand the generated files and
know the next command without reading source code. The first shipped slice is
actionable CLI guidance after `init` and in `doctor`.

## Commands

- Test: `python -m unittest discover -s tests -t . -v`
- Validate documentation: `python -m dockit_fp check --root .`
- Build preview: `python -m dockit_fp build --root . --output build/docs-site`

## Project structure

- `src/dockit_fp/cli.py` owns public command output.
- `tests/test_cli.py` covers CLI behaviour.
- `docs/beginners-guide.md` teaches the supported beginner path.
- `tasks/todo.md` is the ordered implementation checklist for this release.

## Boundaries

- Always keep `init` non-destructive and preserve offline-only output.
- Ask before adding dependencies, changing release infrastructure or expanding
  customisation beyond semantic options.
- Never weaken immutable release checks or copy another project's branding,
  assets or source code.

## Success criteria

- [x] `dockit-fp init` states the next edit and validation command.
- [x] `dockit-fp doctor` distinguishes a normal preview project from one with a
      versioned release configuration and gives one next action.
- [x] Common colour and navigation errors name a corrective action.
- [x] The maintained minimal example changes a colour, adds a page and builds offline.
- [x] The beginner guide links the example and describes the complete publish path.
- [x] Existing command behaviour and safety checks remain unchanged.
- [x] CLI tests and documentation validation pass.

## Release direction

1. Onboarding guidance and a maintained example path.
2. Actionable validation feedback for common configuration mistakes.
3. Supported project identity options, documented with visual examples.
4. Release quality gate, documentation review, `v0.2.0` tag and Pages build.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Guidance becomes stale | Assert the public text in CLI tests and link the beginner guide. |
| More output overwhelms experts | Keep it to a short `Next:` block and omit it on errors. |
| Preview and release workflows blur | Name the two states explicitly and retain immutable release checks. |
