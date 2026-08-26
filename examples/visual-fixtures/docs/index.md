# Visual component fixture

Use this maintained page to inspect every built-in visual theme at phone,
tablet and desktop widths in both light and dark colour modes.

> [!IMPORTANT] Keyboard focus must remain visible on every control and link.

## Typography and lists

Readable documentation needs a clear hierarchy, comfortable measure and
predictable rhythm. Inline `PascalCase` identifiers should remain distinct from
body copy, while **strong text** and [useful links](long-form.md) retain enough
contrast.

- [x] Theme tokens stay semantic.
- [ ] Inspect the current viewport.
- Nested lists keep a readable indent.

## Reference table

| Element | Compact | Comfortable | Wide |
| --- | --- | --- | --- |
| Prose | Focused guides | Default reading | API tables |
| Code | Scrolls safely | Scrolls safely | Shows more context |
| Navigation | Responsive | Responsive | Responsive |

## Code block

```pascal
procedure Greet(const Name: string);
begin
  WriteLn('Hello, ', Name);
end;
```

## Callout variants

> [!NOTE] Notes provide supporting context without interrupting the task.

> [!WARNING] Warnings identify a recoverable risk before publication.

> [!TIP] Tips identify a safer or faster way to complete a task.
