# Contributing

Use Python 3.10 or newer. Run the complete suite before proposing a change:

```powershell
python -m unittest discover -s tests -t . -v
```

Keep changes dependency-free unless there is a documented reason otherwise.
Changes to CLI options, JSON schemas, generated paths, theme token names,
search-index format or reusable-workflow inputs are compatibility changes and
need an accompanying documentation update.
