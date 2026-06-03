# Skill Sources

This document records the function, source, and local customization notes for
each skill in this repository.

## beautiful-svg-whiteboard

### Function

`beautiful-svg-whiteboard` creates polished, editable standalone SVG
whiteboards, infographics, diagrams, posters, and visual explainers.

It is designed for local SVG delivery and later editing in SVG tools:

- final output is a `.svg` file, with optional PNG preview for inspection
- Chinese-capable SVG font stack is required on the root `<svg>`
- text remains editable as `<text>` / `<tspan>` instead of outlined paths
- layouts use simple editable SVG primitives where possible
- style selection is limited to 10 retained templates

### Upstream Source

| Field | Value |
|---|---|
| Upstream repository | `https://github.com/zarazhangrui/beautiful-feishu-whiteboard.git` |
| Upstream GitHub page | <https://github.com/zarazhangrui/beautiful-feishu-whiteboard> |
| Upstream skill path | `SKILL.md` |
| Upstream skill name | `beautiful-feishu-whiteboard` |
| Upstream version observed | `1.1.0` |
| Upstream commit observed | `363ad62` |
| Upstream license | MIT |
| Local skill path | `beautiful-svg-whiteboard/SKILL.md` |
| Local skill version | unversioned |

### Local Customization

Compared with upstream `beautiful-feishu-whiteboard`, this local skill is
customized for standalone SVG creation:

- renamed from `beautiful-feishu-whiteboard` to `beautiful-svg-whiteboard`
- changes the final deliverable from an online editable board to a local SVG
  file
- removes publishing, authentication, document, and remote update workflows
- rewrites the medium rules for portable editable SVG artifacts
- adds a Chinese-capable root font stack recommendation:
  `Source Han Sans SC, Noto Sans SC, Microsoft YaHei, sans-serif`
- keeps only these 10 templates:
  `specimen-bold`, `mint-brut`, `crayon-stack`, `court-press`,
  `soft-editorial`, `checker-bloom`, `reading-room`, `macchiato`,
  `long-table`, and `avocado-press`
- rewrites `CATALOG.md` to list only the retained templates
- updates template metadata and wording for standalone SVG usage

### Sync Policy

Future upstream changes should be reviewed manually instead of merged blindly.
Use this flow:

1. Check upstream changes in
   `https://github.com/zarazhangrui/beautiful-feishu-whiteboard.git`.
2. Compare upstream `SKILL.md`, `RULES.md`, `CATALOG.md`, and retained
   `templates/<slug>/design.md` files against the local skill.
3. Port only palette, layout, or SVG-editability guidance that still fits the
   local goal: a standalone editable SVG file.
4. Do not reintroduce removed templates unless intentionally expanding the
   retained style set.
5. Update this document whenever the upstream version, source, or customization
   list changes.

### Attribution

This skill is derived from `zarazhangrui/beautiful-feishu-whiteboard`, which
is licensed under MIT. The original copyright notice is preserved in
`THIRD_PARTY_NOTICES.md`.

## html-standalone

### Function

`html-standalone` converts Markdown, JSON, plain text, pasted content, or a URL
into one fully self-contained HTML file.

It is designed for portable sharing and offline reading:

- local and remote images are embedded inline as base64 `data:` URIs
- generated HTML uses system fonts and avoids CDN dependencies
- links remain clickable
- a table of contents is generated from headings
- output defaults to `~/Documents/html-standalone` unless
  `HTML_STANDALONE_OUTPUT_DIR` is set

### Upstream Source

| Field | Value |
|---|---|
| Upstream repository | `https://github.com/iharnoor/html-everything.git` |
| Upstream GitHub page | <https://github.com/iharnoor/html-everything> |
| Upstream skill path | `skills/html-everything/SKILL.md` |
| Upstream skill name | `html-everything` |
| Upstream version observed | `0.1.0` |
| Upstream license | MIT |
| Local skill path | `html-standalone/SKILL.md` |
| Local skill version | `3.0.0` |

### Local Customization

Compared with upstream `html-everything`, this local skill is customized for
offline, standalone documents:

- renamed from `html-everything` to `html-standalone`
- changes output directory from `HTMLE_OUTPUT_DIR` /
  `~/Documents/html-everything` to `HTML_STANDALONE_OUTPUT_DIR` /
  `~/Documents/html-standalone`
- removes Google Fonts and uses system fonts only
- adds image placeholder handling with `__IMG__:{path-or-url}__`
- adds `scripts/embed-images.py` to embed images as base64 data URIs
- adds support for resolving relative image paths from the input file directory
- adds sidebar table-of-contents generation for `##` and `###` headings
- expands the visual template with offline-friendly styles and no external
  assets
- keeps the upstream content-detection and mood-selection idea

### Sync Policy

Future upstream changes should be reviewed manually instead of merged blindly.
Use this flow:

1. Check upstream changes in `https://github.com/iharnoor/html-everything.git`.
2. Compare `skills/html-everything/SKILL.md` against
   `html-standalone/SKILL.md`.
3. Port only changes that still fit the local goal: one offline HTML file with
   embedded images and no external runtime dependencies.
4. Update this document whenever the upstream version, source, or customization
   list changes.

### Attribution

This skill is derived from `iharnoor/html-everything`, which is licensed under
MIT. The original copyright notice is preserved in
`THIRD_PARTY_NOTICES.md`.
