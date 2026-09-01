# Customising sections and identity

Use configuration to rename sections, choose colours, add project links and use
a small project mark in the header.
DocKit keeps the page layout and accessibility behaviour working, so you do
not need to copy or maintain its CSS.

## Before and after: navigation

Before, a small site has one section:

```json
{"navigation": [{"title": "Getting started", "pages": [{"title": "Overview", "path": "index.md"}]}]}
```

After, the left navigation has deliberate groups in the same written order:

```json
{"navigation": [
  {"title": "Getting started", "pages": [{"title": "Overview", "path": "index.md"}]},
  {"title": "Reference", "pages": [{"title": "API", "path": "reference/api.md"}]}
]}
```

## Before and after: project identity

Start with the default blue pair, then use a curated preset and small,
meaningful footer links:

```json
{
  "theme": {"preset": "purple"},
  "identity": {
    "logo": "docs/assets/logo.svg",
    "footer": "Example-FP documentation",
    "links": [{"label": "Project", "url": "https://example.test"}]
  }
}
```

The result changes the highlight colour, header mark, visible footer and
project link. The phone layout, keyboard focus and System/Light/Dark modes
continue to work.

## Add a header logo

`identity.logo` is an optional repository-local path to an SVG or PNG. The
image is copied into the generated site and appears immediately before the
project name in the header:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "identity": {
    "logo": "docs/assets/my-library-mark.svg"
  }
}
```

Create the image at that exact path before building. Paths must stay inside the
repository; absolute paths, parent-directory traversal and other image formats
are rejected. The logo is constrained to a small square header area and uses
`object-fit: contain`, so unusually wide or tall marks keep their aspect ratio
without pushing the title or controls out of place.

The project name remains the accessible name of the header link. The image is
decorative because the adjacent text already names the project. Omit
`identity.logo` to retain DocKit's built-in document mark.
