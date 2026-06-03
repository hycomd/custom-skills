---
name: html-standalone
version: "3.0.0"
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

Write the HTML to `OUT_PATH` using the template below. For images, use **placeholders** — do NOT try to base64-encode anything yourself.

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

### HTML Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{TITLE} · html-standalone</title>
<meta name="description" content="{DESCRIPTION}" />
<meta name="generator" content="html-standalone" />
<style>
  :root {
    --ground: {GROUND};
    --ink: {INK};
    --accent: {ACCENT};
    --mute: {MUTE};
    --hair: {HAIR};
    --panel: {PANEL};
    --sidebar-w: 280px;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--ground); color: var(--ink); }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; -webkit-font-smoothing: antialiased; }

  /* Layout */
  .layout { display: flex; min-height: 100vh; }

  /* Sidebar TOC */
  .sidebar {
    width: var(--sidebar-w);
    flex-shrink: 0;
    position: fixed;
    top: 0; left: 0; bottom: 0;
    background: #FAFAFA;
    border-right: 1px solid var(--hair);
    overflow-y: auto;
    padding: 32px 0;
    z-index: 10;
  }
  .sidebar-header {
    padding: 0 24px 20px 24px;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    border-bottom: 1px solid var(--hair);
    margin-bottom: 12px;
  }
  .toc { list-style: none; padding: 0; margin: 0; }
  .toc li { margin: 0; }
  .toc a {
    display: block;
    padding: 8px 24px;
    font-size: 13.5px;
    line-height: 1.5;
    color: var(--ink);
    text-decoration: none;
    border-left: 3px solid transparent;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
  }
  .toc a:hover { background: var(--panel); color: var(--accent); }
  .toc a.active { border-left-color: var(--accent); background: #EEF2FF; color: var(--accent); font-weight: 600; }
  .toc .toc-h2 { font-weight: 600; }
  .toc .toc-h3 { padding-left: 40px; font-weight: 400; color: var(--mute); font-size: 13px; }
  .toc .toc-h3:hover { color: var(--accent); }

  /* Main content */
  .main-area { margin-left: var(--sidebar-w); flex: 1; min-width: 0; }

  /* Typography */
  a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
  a:hover { text-decoration-thickness: 2px; }
  .wrap { max-width: 900px; margin: 0 auto; padding: 64px 56px 80px 56px; display: flex; flex-direction: column; gap: 48px; }
  .eyebrow { display: flex; align-items: center; gap: 12px; font-weight: 500; font-size: 11px; letter-spacing: 0.2em; color: var(--mute); text-transform: uppercase; }
  .eyebrow .dot { width: 7px; height: 7px; background: var(--accent); border-radius: 50%; display: inline-block; }
  h1.display { font-size: 64px; line-height: 68px; letter-spacing: -0.03em; margin: 0; font-weight: 900; }
  h2 { font-size: 32px; line-height: 38px; letter-spacing: -0.02em; margin: 0 0 16px 0; font-weight: 800; }
  h3 { font-size: 20px; line-height: 26px; letter-spacing: -0.01em; margin: 0 0 10px 0; font-weight: 700; }
  p { font-size: 16px; line-height: 26px; margin: 0 0 16px 0; max-width: 72ch; }
  ul, ol { padding-left: 24px; }
  li { font-size: 16px; line-height: 26px; margin-bottom: 8px; }
  code { font-family: 'Cascadia Code', 'Consolas', monospace; font-size: 14px; background: var(--panel); padding: 2px 6px; border-radius: 3px; }
  pre { background: var(--panel); padding: 16px 20px; overflow-x: auto; font-size: 13px; line-height: 20px; font-family: 'Cascadia Code', 'Consolas', monospace; border-radius: 4px; margin: 0 0 16px 0; }
  blockquote { border-left: 4px solid var(--accent); padding: 4px 20px; margin: 16px 0; color: var(--mute); font-style: normal; }
  .thesis { display: flex; gap: 0; }
  .thesis .strip { width: 6px; background: var(--accent); flex-shrink: 0; border-radius: 3px; }
  .thesis .body { padding: 20px 28px; flex: 1; }
  .section { padding-top: 28px; border-top: 1px solid var(--hair); }
  .card { padding: 20px 0; border-top: 1px solid var(--hair); display: flex; flex-direction: column; gap: 10px; }
  .meta-row { display: flex; gap: 24px; align-items: baseline; flex-wrap: wrap; font-family: 'Cascadia Code', 'Consolas', monospace; font-size: 13px; color: var(--mute); }
  .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0 20px 0; font-size: 14px; }
  th { background: var(--panel); font-weight: 700; text-align: left; padding: 10px 14px; border-bottom: 2px solid var(--ink); }
  td { padding: 10px 14px; border-bottom: 1px solid var(--hair); vertical-align: top; }
  tr:hover td { background: #FAFAFA; }
  .img-container { margin: 24px 0; }
  .img-container img { max-width: 100%; height: auto; border-radius: 4px; border: 1px solid var(--hair); }
  .img-container figcaption { font-size: 13px; color: var(--mute); margin-top: 8px; font-style: italic; }
  footer { padding-top: 32px; border-top: 2px solid var(--ink); font-size: 13px; color: var(--mute); display: flex; justify-content: space-between; align-items: baseline; gap: 16px; flex-wrap: wrap; }

  /* Scroll offset for anchor links */
  [id] { scroll-margin-top: 24px; }

  /* Mobile */
  @media (max-width: 900px) {
    .sidebar { display: none; }
    .main-area { margin-left: 0; }
    .wrap { padding: 40px 24px; gap: 32px; }
    h1.display { font-size: 40px; line-height: 44px; }
    .grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<div class="layout">
  <!-- Sidebar TOC -->
  <nav class="sidebar" id="sidebar">
    <div class="sidebar-header">{TOC_TITLE}</div>
    <ul class="toc" id="toc">
      {TOC_ITEMS}
    </ul>
  </nav>

  <!-- Main Content -->
  <div class="main-area">
    <main class="wrap">

      <div class="eyebrow">
        <span class="dot"></span>
        <span>{EYEBROW}</span>
        <span style="margin-left:auto;color:var(--mute);">Standalone</span>
      </div>

      <h1 class="display">{HEADLINE}</h1>

      {THESIS_BLOCK}

      {BODY_SECTIONS}

      <footer>
        <span>Generated by html-standalone · {DATE}</span>
        <span>{SOURCE_HINT}</span>
      </footer>

    </main>
  </div>
</div>

<script>
// TOC active state on scroll
(function() {
  const tocLinks = document.querySelectorAll('.toc a');
  const sections = [];
  tocLinks.forEach(function(link) {
    const id = link.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) sections.push({ el: el, link: link });
  });
  function update() {
    const scrollY = window.scrollY + 80;
    let current = sections[0];
    for (let i = 0; i < sections.length; i++) {
      if (sections[i].el.offsetTop <= scrollY) current = sections[i];
    }
    tocLinks.forEach(function(l) { l.classList.remove('active'); });
    if (current) current.link.classList.add('active');
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
})();
</script>

</body>
</html>
```

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

Write the HTML via the Write tool.

## Phase 2: Embed images

After writing the HTML, run the bundled script to replace all image placeholders with base64 data URIs:

```bash
python3 "<SKILL_DIR>/scripts/embed-images.py" "$OUT_PATH" --content-dir "$CONTENT_DIR"
```

Where `<SKILL_DIR>` is the directory containing this skill file:
- On this system: `C:/Users/hongsa/.claude/skills/html-standalone`

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
