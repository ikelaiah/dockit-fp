# Spec: Configurable homepage capability cards

## Objective

Let a documentation-site owner replace, reorder, or hide the home-page
capability cards through `docs/dockit.json`, without editing DocKit-FP Python.

## Configuration contract

```json
{
  "homepage": {
    "capabilities": [
      {"title": "Offline", "description": "Local assets, no CDN."},
      {"title": "API reference", "description": "Guides for every public unit."}
    ]
  }
}
```

- Omitting `homepage.capabilities` preserves the current four default cards.
- An empty list hides the strip.
- Entries remain in listed order and require non-empty string `title` and
  `description` fields.
- Cards render only on the configured home page; all values are HTML escaped.

## Commands

- Focused test: `python -m unittest tests.test_config tests.test_build -v`
- Full suite: `python -m unittest discover -s tests -t . -v`
- Documentation check: `$env:PYTHONPATH='src'; python -m dockit_fp check --root .`

## Project structure

- `src/dockit_fp/models.py` owns the typed configuration model.
- `src/dockit_fp/config.py` validates configuration.
- `src/dockit_fp/build.py` renders the home page.
- `tests/test_config.py` and `tests/test_build.py` prove validation and output.
- `docs/configuration.md` documents the public API.

## Boundaries

- Always: validate and escape values, preserve current defaults, test before commit.
- Ask first: add dependencies or change schema version.
- Never: require users to edit generator Python or copied CSS.

## Success criteria

- A project can replace all four cards in `dockit.json`.
- A project can hide the strip with an empty list.
- Invalid entries identify the field and corrective action.
- Existing sites retain the default cards unchanged.
