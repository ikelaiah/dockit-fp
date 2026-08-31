# ADR 0006: Adopt existing repositories conservatively

DocKit-FP discovers only a root `README.md` and Markdown inside `docs/` when
initialising an existing repository. This provides a useful first site without
accidentally publishing release notes, contribution policies, security guidance
or arbitrary private Markdown. It records ancillary root files only as
available options.

The generated `layout.json` is the boundary between convention and control. It
is created once and then treated as normal maintainer-owned configuration; no
later discovery changes navigation.

The root README uses an explicit `"source": "root"` marker which accepts only
the exact `README.md`. This avoids copied content and parent-path traversal,
while repository-relative source resolution keeps links and immutable
historical builds correct.
