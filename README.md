# 🧰 DocKit-FP

DocKit-FP is a Free Pascal-oriented toolkit for building, validating and publishing modern, versioned documentation sites from Markdown and historical Git releases.

Built for Free Pascal and Lazarus libraries that want:

- 📱 a responsive documentation website;
- 🌓 System / Light / Dark themes;
- 🎨 project-specific colour identity;
- ∑ bundled offline KaTeX mathematics;
- 🔎 navigation and search;
- 🏷️ version selectors;
- 🕰️ preserved historical documentation;
- 🚀 GitHub Pages publishing;
- ✅ documentation validation;
- ✂️ minimal duplicated infrastructure.

DocKit-FP builds the documentation site.

It does **not** parse Pascal source or extract API documentation from Pascal declarations.

For API extraction from Pascal source, use [PasWeave](https://github.com/ikelaiah/pasweave).

---

# 🚀 Quick start

## 1. Install DocKit-FP

Pin a released version rather than using `main`.

For example:

```bash
python -m pip install "dockit-fp==0.1.0"
```

During development of DocKit-FP itself, installation directly from Git may also be possible:

```bash
python -m pip install \
  "git+https://github.com/ikelaiah/dockit-fp.git@v0.1.0"
```

Use a released version in CI whenever possible.

---

# 2. 🏁 Initialise documentation

From the root of your Free Pascal project:

```bash
dockit-fp init
```

This should create a minimal documentation structure such as:

```text
docs/
├── dockit.json
├── versions.json
├── layout.json
└── index.md
```

If your project already contains Markdown documentation, you may create these files manually instead.

DocKit-FP should never overwrite existing documentation without explicit permission.

---

# 3. 🎨 Project configuration

Create:

```text
docs/dockit.json
```

Example:

```json
{
  "schema_version": 1,
  "project": {
    "name": "MyLibrary-FP",
    "description": "A useful Free Pascal library.",
    "repository_url": "https://github.com/example/mylibrary-fp",
    "site_url": "https://example.github.io/mylibrary-fp"
  },
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#0891b2"
  }
}
```

The project supplies its identity.

DocKit-FP supplies the shared layout and behaviour.

Do not copy DocKit-FP CSS into your repository merely to change colours.

Use theme tokens instead.

---

# 4. ✍️ Add documentation

A typical project may look like:

```text
docs/
├── dockit.json
├── versions.json
├── layout.json
├── index.md
│
├── start/
│   ├── installation.md
│   └── quick-start.md
│
├── guides/
│   ├── strings.md
│   └── parsing.md
│
└── reference/
    └── api-overview.md
```

These Markdown files remain owned by your project.

DocKit-FP does not move them into a central repository.

---

# 5. 🧭 Configure navigation

Modern documentation can define explicit navigation using:

```text
docs/layout.json
```

Example:

```json
{
  "schema_version": 1,
  "navigation": [
    {
      "title": "Getting Started",
      "pages": [
        {
          "title": "Overview",
          "path": "index.md"
        },
        {
          "title": "Installation",
          "path": "start/installation.md"
        },
        {
          "title": "Quick Start",
          "path": "start/quick-start.md"
        }
      ]
    },
    {
      "title": "Guides",
      "pages": [
        {
          "title": "Working with Strings",
          "path": "guides/strings.md"
        }
      ]
    },
    {
      "title": "Reference",
      "pages": [
        {
          "title": "API Overview",
          "path": "reference/api-overview.md"
        }
      ]
    }
  ]
}
```

DocKit-FP validates that configured documents exist.

---

# 6. 🏗️ Build the documentation

Build the current documentation:

```bash
dockit-fp build
```

The output will normally be written somewhere such as:

```text
build/docs-site/
```

Open:

```text
build/docs-site/index.html
```

or the appropriate versioned path.

---

# 7. ✅ Check documentation

Before publishing:

```bash
dockit-fp check
```

DocKit-FP should validate things such as:

* missing Markdown files;
* broken links;
* broken heading anchors;
* invalid navigation;
* unsafe URLs;
* invalid project assets;
* malformed configuration.

Example error:

```text
docs/layout.json:
navigation page "guides/hash.md" does not exist
```

---

# 🕰️ Versioned documentation

One of DocKit-FP's main features is preserving documentation for historical releases.

## 8. Define versions

Create:

```text
docs/versions.json
```

Example:

```json
{
  "schema_version": 1,
  "current": "1.4.0",
  "site_url": "https://example.github.io/mylibrary-fp",
  "repository_url": "https://github.com/example/mylibrary-fp",
  "versions": [
    {
      "release": "1.4.0",
      "source_ref": "v1.4.0"
    },
    {
      "release": "1.3.0",
      "source_ref": "v1.3.0"
    },
    {
      "release": "1.2.0",
      "source_ref": "v1.2.0"
    }
  ]
}
```

The version selector is generated from this manifest.

---

# 9. 🏗️ Build all releases

Run:

```bash
dockit-fp build-all
```

DocKit-FP checks out each historical Git ref and builds documentation from the files that actually existed at that release.

Example output:

```text
build/docs-site/
├── 1.4.0/
├── 1.3.0/
└── 1.2.0/
```

The documentation site can then provide a selector such as:

```text
v1.4.0 (current)
v1.3.0
v1.2.0
```

---

# 🏛️ Historical documentation policy

DocKit-FP intentionally preserves historical documentation.

If version `1.2.0` contained only:

```text
README.md
CHEATSHEET.md
```

then the `1.2.0` documentation site should contain only those historical documents.

DocKit-FP does not copy current documentation into old releases.

This allows the documentation site to show how the project evolved over time.

---

# 📚 Legacy releases

Older releases do not need to contain DocKit-FP configuration.

For example, an old Git tag might contain:

```text
docs/
├── README.md
├── CHEATSHEET.md
├── List.md
└── Dictionary.md
```

with no:

```text
layout.json
dockit.json
```

DocKit-FP can treat this as legacy documentation.

It discovers the Markdown files that existed in that tag and generates simple navigation automatically.

There is no need to modify old Git tags.

---

# Homepage selection for old releases

For legacy releases, DocKit-FP may select the documentation homepage in roughly this order:

1. `index.md`
2. `README.md`
3. a recognised documentation home
4. Getting Started
5. another suitable Markdown document

Historical content is never invented merely to create a homepage.

---

# 🎨 Project colours

Each project can retain its own visual identity.

For example:

```json
{
  "theme": {
    "accent": "#2563eb",
    "accent_secondary": "#0ea5e9"
  }
}
```

Another project may use:

```json
{
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#06b6d4"
  }
}
```

And another:

```json
{
  "theme": {
    "accent": "#7c3aed",
    "accent_secondary": "#a855f7"
  }
}
```

The shared DocKit-FP design remains the same.

Only project identity changes.

Projects should not normally copy or fork DocKit-FP's structural CSS.

---

# 🌓 Themes

Every DocKit-FP site supports:

* System
* Light
* Dark

System follows the operating system/browser preference.

Explicit user choice is remembered locally where browser storage is available.

Project accent colours are mapped appropriately into both light and dark modes.

---

# 📱 Responsive design

DocKit-FP provides the responsive site shell centrally.

Consuming projects should not have to implement separate mobile CSS.

The generated documentation should work cleanly at common widths such as:

```text
360px   phone
768px   tablet
1024px  small desktop
1440px  desktop
```

DocKit-FP handles:

* responsive navigation;
* mobile sidebar/menu;
* readable content width;
* scrolling code blocks;
* usable tables;
* version selector;
* search;
* theme controls;
* responsive banners.

---

# 🚀 GitHub Pages

A project should ideally need only a small workflow.

For example:

```text
.github/workflows/documentation.yml
```

Using DocKit-FP's reusable workflow:

```yaml
name: Documentation

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  documentation:
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.1.0
```

The exact workflow inputs may depend on the DocKit-FP release.

Always pin a stable DocKit-FP version.

Avoid:

```yaml
@main
```

for production documentation.

---

# 📌 Why pin DocKit-FP?

Do this:

```yaml
uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.1.0
```

Not:

```yaml
uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@main
```

Pinning prevents an unrelated future DocKit-FP change from unexpectedly changing every project's documentation site.

Upgrade deliberately.

---

# ⬆️ Updating DocKit-FP

Suppose your project currently uses:

```text
DocKit-FP v0.2.1
```

and you want to move to:

```text
v0.3.0
```

Update the pinned version, rebuild locally and run:

```bash
dockit-fp check
dockit-fp build-all
```

Then inspect the generated documentation before merging.

Treat DocKit-FP upgrades like ordinary dependencies.

---

# 🔁 Using DocKit-FP with an existing project

If your repository already contains documentation:

```text
docs/
├── README.md
├── CHEATSHEET.md
├── List.md
└── Dictionary.md
```

you do **not** need to rewrite the documents.

Add the minimal DocKit-FP configuration around them.

Then run:

```bash
dockit-fp build
```

You can introduce explicit navigation gradually.

---

# 🧳 Migrating a repository that copied an older documentation engine

Some projects may currently contain:

```text
tools/build_docs.py
tools/build_all_docs.py
tools/check_built_docs.py
tools/docs_assets/
```

These are exactly the kinds of files DocKit-FP is intended to replace.

A migration should generally follow this process:

1. install and pin DocKit-FP;
2. add project configuration;
3. make the shared DocKit-FP build reproduce the existing site;
4. compare navigation, themes, search and historical versions;
5. update GitHub Pages workflow;
6. run all documentation checks;
7. only after behaviour matches, remove duplicated local builder code.

Do not delete the existing builder first.

Prove equivalence before removing it.

---

# 🌱 Starting a completely new Free Pascal library

For a new project, the intended flow is:

```bash
git clone <your-project>
cd <your-project>

python -m pip install dockit-fp

dockit-fp init
```

Then write:

```text
docs/index.md
docs/start/quick-start.md
docs/guides/...
```

Configure navigation and theme.

Build:

```bash
dockit-fp build
```

Check:

```bash
dockit-fp check
```

When releasing versions, add them to:

```text
docs/versions.json
```

Then:

```bash
dockit-fp build-all
```

---

# 🧵 Using PasWeave together with DocKit-FP

DocKit-FP does not extract documentation from Pascal source.

For projects that want generated API documentation, use PasWeave upstream.

Conceptually:

```text
src/*.pas
    │
    ▼
 PasWeave
    │
    ▼
generated API Markdown
    │
    ├───────────────┐
    │               │
handwritten guides  │
    │               │
    └───────┬───────┘
            ▼
        DocKit-FP
            │
            ▼
      complete website
```

This separation keeps both tools focused:

**PasWeave understands Pascal.**

**DocKit-FP understands documentation sites.**

---

# 🧱 What stays in your project?

Your Free Pascal repository owns:

```text
Markdown documentation
navigation configuration
version manifest
project metadata
project colours
banner/logo
Git tags
```

DocKit-FP owns:

```text
HTML renderer
CSS design system
responsive layout
theme system
search
version selector
historical build engine
validation
GitHub Pages publishing infrastructure
```

That division is intentional.

---

# 🚫 What should NOT be copied?

Do not copy these from DocKit-FP into every project:

```text
renderer source
CSS
JavaScript
search implementation
version builder
Git worktree implementation
site validator
GitHub Pages implementation
```

If a common behaviour needs fixing, fix it in DocKit-FP and release a new DocKit-FP version.

Then consuming repositories can upgrade deliberately.

---

# 🗂️ Recommended project structure

A typical Free Pascal library may eventually look like:

```text
myproject-fp/
├── src/
│   └── ...
│
├── tests/
│   └── ...
│
├── docs/
│   ├── dockit.json
│   ├── versions.json
│   ├── layout.json
│   ├── index.md
│   │
│   ├── start/
│   │   ├── installation.md
│   │   └── quick-start.md
│   │
│   ├── guides/
│   │   └── ...
│   │
│   └── reference/
│       └── ...
│
├── assets/
│   └── project-banner.svg
│
└── .github/
    └── workflows/
        └── documentation.yml
```

No local documentation engine should normally be necessary.

---

# ⚡ The short version

For an existing Free Pascal repository:

```bash
pip install dockit-fp
dockit-fp init
dockit-fp build
dockit-fp check
```

For versioned documentation:

```bash
dockit-fp build-all
dockit-fp check-release
```

For GitHub Pages:

```yaml
uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@<pinned-version>
```

Write your documentation.

DocKit-FP handles the machinery.
