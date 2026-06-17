---
name: html-standalone
version: "3.1.0"
description: "Convert Markdown (with images), JSON, plain text, or a URL into a single fully self-contained HTML page. All local and remote images are base64-encoded and embedded inline — zero external dependencies, portable anywhere. Use this skill whenever the user wants a standalone HTML file, a portable document with embedded images, or mentions 'self-contained HTML', 'offline HTML', 'embed images in HTML', or wants to share a complete HTML document with no missing assets."
argument-hint: 'html-standalone <file-path> | html-standalone <url> | html-standalone (then paste)'
allowed-tools: Bash, Read, Write, WebFetch, Glob, Grep
homepage: https://github.com/hycomd/custom-skills/tree/main/html-standalone
repository: https://github.com/hycomd/custom-skills
source: https://github.com/iharnoor/html-everything
source-skill: skills/html-everything/SKILL.md
license: MIT
user-invocable: true
---

# /html-standalone

Convert any input into a single self-contained HTML file with all images embedded as base64 data URIs. Works offline, portable anywhere.

The process has two phases:
1. **Phase 1** — Generate HTML with image placeholders (Claude does this)
2. **Phase 2** — Run `embed-images.py` to replace placeholders with base64-encoded images (script does this)

This separation keeps the HTML generation clean and lets the script handle all binary encoding work.

## Phase 1: Generate HTML

### Step 1 — Resolve input

| Pattern | Action |
|---|---|
| `^https?://` | `WebFetch` the URL, ask for raw text |
| existing file path | `Read` the file |
| anything else | treat as inline content |
| empty | ask the user to paste content, wait |

After resolution, set:
- `CONTENT` = the text content
- `CONTENT_DIR` = parent directory of input file (for resolving relative image paths), or `.` if no file
- `OUT_DIR` = `${HTML_STANDALONE_OUTPUT_DIR:-$HOME/Documents/html-standalone}` and `mkdir -p`
- `SLUG` = short kebab-case from first heading/line (max 50 chars)
- `OUT_PATH` = `$OUT_DIR/$SLUG.html`

### Step 2 — Detect content type

| Signal | Type |
|---|---|
| `{` or `[` start, parses as JSON | `json` |
| `# ` headings, `**bold**`, `- ` bullets, `[text](url)` | `markdown` |
| `key: value` lines without markdown | `key-value` |
| otherwise | `prose` |

### Step 3 — Pick a mood

Scan topic, pick ONE mood:

| Topic signal | Mood | Ground | Accent | Ink | Mute | Hair | Panel |
|---|---|---|---|---|---|---|---|
| AI / dev / tech | **editorial** | `#FFFFFF` | `#0029FF` | `#0A0A0A` | `#6B6B6B` | `#E5E5E5` | `#F5F5F5` |
| finance / markets | **bookish** | `#F5F0E6` | `#1A1A2E` | `#2C2C2C` | `#8B7E6A` | `#D4CFC4` | `#EBE6D8` |
| sports | **signage** | `#FFFFFF` | `#FFB300` | `#1A1A1A` | `#7A7A7A` | `#E0E0E0` | `#F8F8F8` |
| politics / policy | **mineral** | `#EDEAE3` | `#5C4033` | `#2C2420` | `#8A7D72` | `#D5D0C8` | `#E5E0D6` |
| product / consumer | **highlighter** | `#FFFFFF` | `#FFEA00` | `#0A0A0A` | `#6B6B6B` | `#E5E5E5` | `#F5F5F5` |
| nightlife / music | **nocturnal** | `#1A1A1A` | `#FF1493` | `#E8E8E8` | `#888888` | `#333333` | `#242424` |
| science / data | **alpine** | `#F8FAFC` | `#0F4C5C` | `#1E293B` | `#64748B` | `#E2E8F0` | `#F1F5F9` |
| nothing fits | **editorial** | same as editorial |

### Step 4 — Generate HTML with image placeholders

Read the bundled `template.html` (in the same directory as this `SKILL.md`) — it contains the full page layout and CSS. Fill its placeholders per the rules below. For images, use **placeholders** — do NOT try to base64-encode anything yourself.

**Image placeholder format:**

When you encounter `![alt](path)` in markdown, render it as:

```html
<figure class="img-container">
  <img src="__IMG__:path/to/image.png__" alt="alt text" loading="lazy" />
  <figcaption>alt text</figcaption>
</figure>
```

The placeholder syntax is: `__IMG__:{path-or-url}__`

- For relative paths: keep as-is → `__IMG__:images/photo.png__`
- For absolute paths: keep as-is → `__IMG__:/absolute/path/photo.png__`
- For remote URLs: keep as-is → `__IMG__:https://example.com/photo.png__`
- If no alt text: omit `<figcaption>`

**Why placeholders?** The bundled `embed-images.py` script will read the HTML, find all `__IMG__:...__` tokens, base64-encode each image, and replace them with `data:` URIs. This keeps the HTML generation clean and avoids handling binary data in context.

**Template placeholders** (the slots in `template.html` to fill):

*Color variables* — in the template's `:root`, replace these with the hex values from the mood chosen in Step 3:
`{GROUND}` · `{INK}` · `{ACCENT}` · `{MUTE}` · `{HAIR}` · `{PANEL}`

*Content slots:*
- `{TITLE}` / `{DESCRIPTION}` — page `<title>` and meta description (derive from the headline)
- `{TOC_TITLE}` — "目录大纲" for Chinese content, "Contents" for English
- `{TOC_ITEMS}` — generated per the "Sidebar & TOC" rules below
- `{EYEBROW}` — short topic label
- `{HEADLINE}` — the first `# H1` only
- `{THESIS_BLOCK}` — an opening `<div class="thesis">…</div>` if there's a lead statement; otherwise remove the line
- `{BODY_SECTIONS}` — the rendered `## H2` / `### H3` sections (see Markdown rules below)
- `{DATE}` / `{SOURCE_HINT}` — footer date and source attribution

Leave image `__IMG__:path__` placeholders exactly as written — Phase 2 turns them into base64 data URIs.

### Rendering rules

**Sidebar & TOC generation:**
- Generate a `{TOC_TITLE}` — use "目录大纲" for Chinese content, "Contents" for English, or a context-appropriate label
- For every `## H2` heading, generate a TOC entry: `<li><a href="#{slug}" class="toc-h2">{heading text}</a></li>`
- For every `### H3` heading, generate a TOC entry: `<li><a href="#{slug}" class="toc-h3">{heading text}</a></li>`
- Slug generation: lowercase, replace spaces/special chars with `-`, strip leading/trailing `-`, collapse multiple `-`
- The first `<li>` should have `class="active"` added to its `<a>` tag
- Each `##` section gets an `id="{slug}"` on its `<section>` wrapper
- Each `###` card gets an `id="{slug}"` on its `.card` wrapper

**Images:**
- `![alt](path)` → `<figure class="img-container"><img src="__IMG__:path__" alt="alt" loading="lazy" /><figcaption>alt</figcaption></figure>`
- `![](path)` → `<figure class="img-container"><img src="__IMG__:path__" loading="lazy" /></figure>`
- No alt text → omit `<figcaption>`

**Markdown:**
- `# H1` → `<h1 class="display">` (first only, used as page headline)
- `## H2` → `<section class="section" id="{slug}"><h2>...</h2>...</section>`
- `### H3` → `<div class="card" id="{slug}"><h3>...</h3>...</div>`
- Lists, bold, links, quotes, code, tables — standard HTML

**Link rule:** Every URL becomes a clickable `<a>`. Never emit bare URLs.

**Fonts:** System fonts only (no Google Fonts CDN). True offline portability.

Write the filled HTML to `OUT_PATH` via the Write tool.

## Phase 2: Embed images

Run the bundled `scripts/embed-images.py` to replace every image placeholder with a base64 data URI. The script sits in this skill's own directory (next to `SKILL.md`).

Call it by **absolute path** so it runs from any working directory on any OS — use the folder you read this file from:

```bash
python3 "<SKILL_DIR>/scripts/embed-images.py" "$OUT_PATH" --content-dir "$CONTENT_DIR"
```

- `<SKILL_DIR>` — absolute path of this skill's directory (the one containing `SKILL.md`/`template.html`). Derive it at runtime from the path you read; never hardcode it.
- If `python3` is not on PATH (common on Windows), use `python` instead.

The script will:
1. Scan the HTML for all `__IMG__:...__` placeholders
2. For local paths: resolve relative to `--content-dir`, read, base64-encode
3. For remote URLs: download, base64-encode
4. Replace each placeholder with `data:{mime};base64,{data}`
5. Write the updated HTML back in-place
6. Print a summary (embedded count, failed count, total size)

If no placeholders exist, the script exits cleanly (no-op).

## Step 5 — Save + open

After the script completes:

```bash
start "" "$OUT_PATH" 2>/dev/null || open "$OUT_PATH" 2>/dev/null || xdg-open "$OUT_PATH" 2>/dev/null || echo "Wrote: $OUT_PATH"
```

If `--no-open` was passed, skip.

## Step 6 — Reply

Reply with under 200 words:

```
Rendered → {OUT_PATH}
Mood: {mood}  ·  Type: {type}
Sections: {N}  ·  Links: {count}
Images embedded: {count from script output}
Total file size: {size}
```

## Rules

- Never delegate to other heavy skills. The template is the design.
- Never install packages. No `npm install`, no `pip install`.
- Never try to base64-encode images yourself. Use placeholders + the script.
- One HTML file per run. No external assets.
- System fonts only. No CDN.
- Don't show raw HTML in chat unless asked.

## Secret hygiene

- If `CONTENT` contains API key patterns (`sk_…`, `xai-…`, `gho_…`, `AKIA…`), refuse and warn.
- Never include `.env` content.
