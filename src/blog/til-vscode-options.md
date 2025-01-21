---
title: "TIL: Handy VS Code options"
date: 2025-01-21
tags:
  - vscode
  - code
  - editors
---

Here are a couple of quick tips that I learned today (well, technically a few days ago).

### Fixing missing breakpoints

When using VS Code with Python, if tests are ignoring breakpoints it might be because `coverage` is
enabled by default. To disable it, and make breakpoints work again, add the following to
`.vscode/settings.json`:

```json
{
  "python.testing.pytestArgs": ["--no-cov"]
}
```

### Customizing the title bar

With a lot of projects it can be helpful to have a visual indicator to hint at which one is active.
You can customize the title bar background color with the following added to `settings.json`:

```json
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#35257d"
  }
}
```
