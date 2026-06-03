---
name: beautiful-svg-whiteboard
description: Create polished, editable SVG whiteboards, infographics, diagrams, posters, or visual explainers using a curated catalogue of colour palette styles. Use when the user wants content turned into a beautiful standalone SVG file, wants a specific visual vibe or named style, needs Chinese text to render correctly in SVG/Inkscape, or asks for a whiteboard-style visual artifact with local file delivery.
---

# Beautiful SVG Whiteboard

Create a finished **standalone SVG** as the final artifact. Use the bundled style catalogue for
palette and mood, compose the layout yourself, render and inspect the SVG, then deliver the SVG path
and any generated preview image.

## Workflow

1. **Understand the artifact.** Identify the content, purpose, audience, language, and desired format
   such as system map, timeline, comparison, funnel, stages, poster, or explanatory board. If the
   request is unclear, ask one short question before building.
2. **Choose the vibe.** If the user names a style, use it. Otherwise infer the desired mood,
   formality, and colour direction; when unsure, pick a versatile balanced style and say which one
   you chose in one line.
3. **Read the resources.** Always read [`RULES.md`](RULES.md), then use [`CATALOG.md`](CATALOG.md)
   and the chosen [`templates/<slug>/design.md`](templates/) file.
4. **Build the SVG.**
   - Work in a logical coordinate space about 1600 to 1700 px wide unless the user requested a
     specific size.
   - Use editable SVG primitives: `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polyline>`,
     `<polygon>` only for simple geometric accents, and `<text>/<tspan>` for all labels.
   - Put a font stack on the root SVG, especially for Chinese text:
     `<svg ... font-family="Source Han Sans SC, Noto Sans SC, Microsoft YaHei, sans-serif">`.
   - Put only the finished content on the canvas. Do not echo the user's prompt, source notes,
     chosen style name, file paths, tool names, or process metadata into the visual.
5. **Render and inspect.** Produce a PNG preview when possible, open or inspect it, and fix text
   overflow, poor padding, accidental overlaps, clipping, weak contrast, or awkward spacing. Iterate
   until the artifact is clean.
6. **Deliver.** Return the SVG file path and, if created, the preview image path. Mention that the
   user can edit the SVG in Inkscape or another SVG editor and can ask for a style swap.

## Files

- [`RULES.md`](RULES.md): hard SVG design, editability, typography, and verification rules.
- [`CATALOG.md`](CATALOG.md): style catalogue with vibe and formality guidance.
- [`templates/<slug>/design.md`](templates/): colour palette and usage notes for each style.
