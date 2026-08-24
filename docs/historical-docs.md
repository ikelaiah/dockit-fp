# Historical documentation

`dockit-fp build-all` validates each declared `source_ref`, archives that Git
object, and renders from the archive. It never uses the current working-tree
Markdown for an older release. Moving refs such as `main` and `HEAD` are
rejected for published releases.

Older tags may have no DocKit-FP files. Their Markdown is discovered as legacy
documentation, navigation is generated from only the files in that tag, and
the homepage is selected in this order: `index.md`, `README.md`, known start
pages, then the first document. No historic prose or modern pages are invented.
