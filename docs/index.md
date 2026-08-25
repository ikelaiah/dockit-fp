# Documentation that keeps its history

DocKit-FP builds **fast, offline-friendly, versioned documentation sites** for
Free Pascal and Lazarus projects.

> [!IMPORTANT] DocKit-FP builds and publishes sites from existing Markdown; it does not extract Pascal API documentation from source—use PasWeave for that.

## Why it exists

Free Pascal libraries should not each have to maintain their own renderer,
search, theme switcher, version selector and historical Git build scripts.
DocKit-FP makes that shared machinery one small dependency while every project
keeps its own words, releases and visual identity.

## Start here

- [Configure a modern project](configuration.md)
- [Keep older documentation accurate](historical-docs.md)
- [Choose a project identity without CSS forks](themes.md)
- [Publish safely to GitHub Pages](github-pages.md)
