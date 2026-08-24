# ADR 0001: Site infrastructure is separate from Pascal extraction

PasWeave owns Pascal parsing, declarations and generated API content. DocKit-FP
owns Markdown site presentation and publishing. This prevents competing parsers
and makes either tool independently useful.
