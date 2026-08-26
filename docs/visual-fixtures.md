# Visual fixtures

The maintained project in `examples/visual-fixtures` exercises typography,
lists, inline code, fenced Pascal, tables, callouts, search, theme controls,
page navigation, a long document and the reading-progress indicator.

Build it locally:

```powershell
$env:PYTHONPATH='src'
python -m dockit_fp build `
  --root examples/visual-fixtures `
  --output build/visual-fixtures
```

Open `build/visual-fixtures/index.html`, then verify this matrix. Browser
content is expected to remain fully local and the console should have no
errors or warnings.

| View | Width | Checks |
| --- | ---: | --- |
| Phone | 360px | Native navigation disclosure, visible copy control, no page overflow |
| Tablet | 768px | Search and controls wrap cleanly, readable table scrolling |
| Desktop | 1440px | Sidebar, article and on-page outline align without crowding |
| Long document | 1024px or wider | Heading rhythm, reading progress and sticky local navigation |

At each useful width, switch among Classic, Paper and Midnight and repeat with
Light and Dark. Use only the keyboard to focus search with `/`, move among
results with Arrow keys/Home/End, close results with Escape, and tab through
version, visual-theme and colour controls. Every focus indicator must be
visible and every control must retain an accessible name.

The fixture sets `layout.content_width` to `wide` so table and code behavior is
easy to inspect. Change it to `compact` and `comfortable` when reviewing the
semantic width contract.
