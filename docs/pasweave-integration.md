# PasWeave integration

PasWeave understands Pascal source, declarations, documentation comments,
coverage and API symbols. DocKit-FP understands Markdown documentation sites.
The integration seam is simply generated API Markdown placed beside handwritten
guides:

```text
Pascal source -> PasWeave -> generated API Markdown --+
handwritten guides ----------------------------------+-> DocKit-FP -> site
```

Neither package depends on the other in 0.1.0. DocKit-FP never parses Pascal;
use PasWeave when source-derived API documentation is needed.
