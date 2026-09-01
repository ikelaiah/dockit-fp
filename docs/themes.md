# Choose colours and a visual theme

You do not need CSS to give a DocKit site its own identity. Start with one
colour preset and one visual style in `docs/dockit.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "theme": {
    "preset": "purple",
    "style": "paper"
  }
}
```

## Two choices that do different jobs

Visitors can choose **System**, **Light** or **Dark** mode. System follows their
browser or operating-system preference. You do not need to configure these
modes.

You choose the site's starting visual style:

- `classic` is the clean, dependable default;
- `paper` gives long guides a warm reading surface;
- `midnight` starts with a dark technical look.

Visitors can switch the visual style too. DocKit remembers both choices in
the browser when storage is available.

Classic is the showcase default: it keeps the header, navigation and reading
surface quiet so ordinary Markdown supplies the personality. Paper and
Midnight use the same spacing, typography and semantic states, with their own
reading surfaces. No custom CSS is needed to make any of them publication-ready.

## Pick an accent colour

The supported presets are:

| Preset | Good starting point for |
| --- | --- |
| `blue` | A familiar general-purpose site |
| `teal` | Libraries and developer tools |
| `ocean` | A calm technical site |
| `purple` | A more distinctive project identity |

Each preset provides link and highlight colours for both light and dark modes.

If your project already has accessible brand colours, you can provide exact
hexadecimal values:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#0891b2",
    "style": "classic"
  }
}
```

Test custom colours in both Light and Dark mode. Links, selected navigation and
keyboard focus must remain easy to see. A preset is safer when you are unsure.

## Add a banner only when it helps

A home-page banner can show a project logo or useful illustration. Keep the
image inside your repository and describe it for people who cannot see it:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "banner": {
    "path": "docs/assets/project-banner.svg",
    "alt": "MyLibrary-FP logo"
  }
}
```

The `alt` text should communicate the image's meaning. Use empty `alt` text only
when the image is purely decorative and adds no information.

Run `dockit-fp check` after every configuration change. The maintained
[visual fixtures](visual-fixtures.md) explain how to review phone, tablet,
desktop, keyboard and colour-mode behaviour.
