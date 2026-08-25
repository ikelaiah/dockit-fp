# v0.2.0 task list

- [x] Task 1: Add short, actionable `init` and `doctor` next-step guidance.
  - Acceptance: preview and versioned-release states have distinct, accurate advice.
  - Verify: focused CLI tests and full test suite.
  - Files: `src/dockit_fp/cli.py`, `tests/test_cli.py`, beginner guide.

- [ ] Task 2: Improve diagnostics for the most common layout and configuration mistakes.
  - Acceptance: errors name the corrective action as well as the offending field.
  - Verify: focused configuration tests and `dockit-fp check` fixtures.

- [ ] Task 3: Add a small maintained example project.
  - Acceptance: a newcomer can copy its documented layout and build it offline.
  - Verify: build it in CI and link it from the beginner guide.

- [ ] Checkpoint: review the first downstream project's onboarding feedback before widening customisation.
