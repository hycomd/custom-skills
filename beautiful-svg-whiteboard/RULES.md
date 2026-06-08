# SVG Whiteboard Rules

These rules apply to every artifact. A template gives palette and mood; this file gives the
medium constraints for a polished, editable standalone SVG.

## Hard Rules

- **Final output is SVG only.** Create a `.svg` file as the sole deliverable. Do not generate
  PNG, JPEG, or any raster image format.
- **Deliver a local editable artifact.** Return the SVG file path. The user edits the SVG later in
  Inkscape or any SVG editor if more changes are needed.
- **Set a Chinese-capable font stack.** Put `font-family` on the root `<svg>` so Chinese text opens
  correctly in editors:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" width="1680" height="1120" viewBox="0 0 1680 1120"
       font-family="Source Han Sans SC, Noto Sans SC, Microsoft YaHei, sans-serif">
  ```
  Prefer `Source Han Sans SC` when Chinese is prominent. Do not outline text as paths unless the
  user explicitly asks for a non-editable print export.
- **Text lives in `<text>` / `<tspan>`.** Keep labels editable. Wrap long lines manually with
  `<tspan x="..." dy="...">` rather than shrinking text until it becomes cramped.
- **Use editable primitives.** Build the visual mainly from `<rect>` with optional `rx`, `<circle>`,
  `<ellipse>`, straight `<line>`, right-angled `<polyline>`, simple `<polygon>`, and `<text>`.
  Avoid complex paths for structural elements when simple primitives can do the job.
- **Use paths sparingly.** SVG supports paths, but complex decorative paths are harder to edit.
  If a reference style feels organic, keep its palette and rebuild the layout with rectangles,
  circles, simple lines, and clear geometry.
- **Avoid fragile effects.** Do not rely on filters, blur shadows, masks, clip paths, patterns, or
  gradients unless the user explicitly asks for them. Flat solid colour is more portable across
  editors and renderers.
- **Use solid tints, not opacity, for important colour relationships.** Opacity can behave
  differently across editors and exports. For pale fills, choose a lighter hex colour directly.
- **Hard offset shadows are allowed.** Draw a duplicate of the same shape, offset behind the real
  shape, using a solid darker colour. Match the real shape's size, `rx`, and transform.
- **Arrows use markers.** Put arrowheads on `<line>` or `<polyline>` with `marker-end` and, when
  needed, `marker-start`. Keep connectors straight or right-angled.
  ```svg
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="4"
            orient="auto" markerUnits="strokeWidth">
      <path d="M0 0 L10 4 L0 8 z" fill="context-stroke"/>
    </marker>
  </defs>
  <line x1="100" y1="80" x2="360" y2="80" stroke="#0D4FA8" stroke-width="3"
        marker-end="url(#arrow)"/>
  ```
- **Transforms are acceptable when simple.** Use `translate`, `rotate`, and `scale`. Avoid complex
  `matrix(...)` transforms unless unavoidable.
- **Let content define the canvas.** Default to a logical canvas about 1600 to 1700 px wide, but
  choose height based on content. Do not force 16:9 unless requested.
- **No decorative metadata.** Every visible label must be part of the artifact. Do not print the
  prompt, source filename, chosen style, generation notes, date, token count, or tool instructions
  on the canvas.
- **Never echo the user's instructions.** A title may name the subject, but the canvas must not say
  things like "整理范围", "来源", "based on the attached doc", "style:", or "summary of". Put that
  context in the chat reply if needed.
- **Design for readable editability.** Keep text at practical sizes, use generous padding, align to
  a visible grid, and leave enough whitespace around dense groups.

## Self-Check

Before delivering the SVG, review it mentally for common failures:

- text overflowing boxes or canvas edges
- cramped top or side padding
- accidental overlaps between labels, connectors, and shapes
- clipped content at right or bottom edges
- weak contrast, especially small text on saturated fills
- inconsistent spacing or alignment

If you spot any issue, fix the SVG and re-check.

## Composition Guidance

- Pick a narrative structure before drawing: stages, map, comparison, timeline, stack, quadrant,
  loop, hierarchy, or poster.
- Use the selected template for colour hierarchy, background, accent rhythm, border weight, and
  mood. Do not copy sample content from templates.
- Use a small number of visual roles: background, primary panels, secondary chips, connectors,
  highlights, and annotations.
- Prefer strong information hierarchy over decoration. Large subject titles, clear grouping, and
  consistent spacing make the SVG feel designed.
- For Chinese-heavy boards, assume CJK characters occupy about 1em each and wrap lines early.
  Mixed Latin/CJK text often needs more horizontal padding than it appears to need.

## Delivery

Return the SVG path. Mention that the SVG is the final editable artifact and can be adjusted by the
user in Inkscape or another SVG editor.
