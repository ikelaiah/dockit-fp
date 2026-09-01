# Make code documentation people can use

DocKit-FP turns Markdown into a searchable, responsive documentation website.
It is geared towards Free Pascal and Lazarus, but you can use it for another
language too: the input is ordinary Markdown, not Pascal source code.

> [!TIP] New here? Start with [Your first DocKit-FP site](beginners-guide.md).
> It takes you to a working local preview and explains each step.

## Pick one goal

- **I want a working site first.** Follow the
  [beginner's guide](beginners-guide.md).
- **I want to write clearer guides.** Read
  [Write documentation people can use](writing-great-docs.md).
- **I want to add or reorder pages.** Open [Configuration](configuration.md).
- **I want to change the look.** Try [Themes](themes.md) or
  [customize the home page](homepage-recipes.md).
- **I want to publish.** Choose a path in [GitHub Pages](github-pages.md).
- **A word is unfamiliar.** Check the [glossary](glossary.md).

## What stays simple

Your project owns its words, Markdown files and visual identity. DocKit-FP owns
the shared page layout, search, themes, validation and publishing machinery.
Everything needed to browse a built site is stored locally, so the site does
not depend on a hosted JavaScript or CSS service.

DocKit-FP does not extract API descriptions from source code. Free Pascal
projects can use [PasWeave](pasweave-integration.md) for that job and feed the
resulting Markdown into DocKit-FP.
