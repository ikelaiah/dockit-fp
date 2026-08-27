# ADR 0005: Highlight fenced code locally

DocKit-FP highlights a small set of common documentation languages while it
builds each page: JSON, Free Pascal, Python, Bash, YAML and Markdown. The
renderer escapes every source token before adding its semantic span, and an
unknown language remains plain escaped code. This keeps generated sites fully
offline and avoids a large browser dependency or a CDN while giving Pascal and
configuration examples useful visual structure.
