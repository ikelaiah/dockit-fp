# PasWeave integration

PasWeave reads Pascal source and produces API documentation as Markdown.
DocKit-FP combines Markdown pages into a complete documentation website. You
can use either tool alone, or put PasWeave's generated pages beside your
handwritten guides:

```text
Pascal source -> PasWeave -> generated API Markdown --+
handwritten guides ----------------------------------+-> DocKit-FP -> site
```

Add the generated Markdown files to `docs/layout.json`, then run
`dockit-fp check` and `dockit-fp build` as usual. DocKit-FP never parses Pascal
source itself.
