# Skill Sources

This document records the function, source, and local customization notes for
each skill in this repository.

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
