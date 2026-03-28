---
name: pretext
description: This skill should be used when the user asks about "pretext", "@chenglou/pretext", "text measurement without DOM", "DOM-free text layout", "multiline text measurement", "line breaking in JavaScript", "canvas text measurement", "prepare text for layout", "layoutWithLines", "layoutNextLine", "walkLineRanges", "PreparedText", "text height calculation without reflow", "measure paragraph height", or needs guidance on text layout, line-breaking algorithms, i18n text segmentation, bidi text handling, CJK line breaking, or integrating pretext into React, canvas, or streaming applications.
version: 1.0.0
---

# Pretext: DOM-Free Text Measurement and Layout

## Overview

Pretext (`@chenglou/pretext`) is a pure JavaScript/TypeScript library for multiline text measurement and layout that operates without DOM measurements, avoiding expensive layout reflow operations.

The core invariant: **prepare once, layout many times.** The `prepare()` phase segments text and measures graphemes via canvas (slow, ~17ms for 500 texts). The `layout()` phase performs pure arithmetic on cached widths (fast, ~0.10ms for 500 texts). On every resize, call only `layout()` — never re-prepare.

Install with `npm install @chenglou/pretext`. Import from `@chenglou/pretext`.

## Choosing the Right API

Select the function based on what information is needed:

| Need | Function | Input Type |
|------|----------|------------|
| Line count and total height only | `layout()` | `PreparedText` |
| Per-line text content and widths | `layoutWithLines()` | `PreparedTextWithSegments` |
| One line at a time (streaming) | `layoutNextLine()` | `PreparedTextWithSegments` |
| Line geometry without materializing text | `walkLineRanges()` | `PreparedTextWithSegments` |
| Just the line count | `countPreparedLines()` | `PreparedText` |

**Preparation functions:**
- `prepare(text, font)` returns `PreparedText` — sufficient for `layout()` and `countPreparedLines()`
- `prepareWithSegments(text, font)` returns `PreparedTextWithSegments` — required for `layoutWithLines()`, `layoutNextLine()`, and `walkLineRanges()`

Always match the preparation function to the layout function being used. Calling `layoutWithLines()` with a plain `PreparedText` will fail.

## Critical Rules

### Font String Safety

The font parameter must be a valid CSS font shorthand string including the size:
- Correct: `"16px Arial"`, `"bold 14px Menlo"`, `"16px/1.2 Helvetica Neue, sans-serif"`
- Wrong: `"Arial"` (missing size), `"16"` (missing family)

**Never use `system-ui` as the font on macOS.** The `system-ui` alias resolves to different physical fonts across platforms, producing inconsistent measurements. Use named fonts: `"16px -apple-system, Helvetica Neue, sans-serif"` or `"16px Helvetica"`.

### Prepare Once, Layout Many

Call `prepare()` or `prepareWithSegments()` exactly once per unique `(text, font)` pair. Cache the result. On resize or container width changes, call only `layout()` with the cached prepared text.

```typescript
// Correct: prepare once
const prepared = prepare(text, "16px Arial");

// Correct: layout on every resize
function onResize(newWidth: number) {
  const result = layout(prepared, newWidth, 20);
  updateHeight(result.height);
}
```

Re-preparing on every render is the most common performance mistake. Use `profilePrepare()` to diagnose — if `totalMs` is high and called frequently, preparation is being repeated unnecessarily.

### Locale Configuration

Call `setLocale()` before `prepare()` when text contains Thai or other locale-sensitive segmentation. CJK text does not require a locale override — it is handled automatically via Unicode range detection.

```typescript
setLocale("th"); // For Thai text
const prepared = prepare(thaiText, font);

setLocale(undefined); // Reset to default
```

### Canvas Requirement

Pretext requires a canvas context for measurement. In browsers, this works automatically via `OffscreenCanvas` or a DOM `<canvas>`. In Node.js or headless environments, provide canvas support or use HarfBuzz-based server-side measurement (see `src/measure-harfbuzz.ts` in the pretext repo).

### Cache Management

Pretext caches grapheme measurements internally. For bulk operations processing thousands of distinct texts, call `clearCache()` afterward to free memory. For typical interactive use, caching improves performance and no manual clearing is needed.

## Common Patterns

### Container Height Calculation

The most common use case — measure how tall a text block will be at a given width:

```typescript
import { prepare, layout } from "@chenglou/pretext";

const prepared = prepare("Long paragraph text...", "16px Arial");
const { lineCount, height } = layout(prepared, containerWidth, lineHeight);
container.style.height = `${height}px`;
```

### Custom Line Rendering

Render each line individually to canvas, SVG, or custom DOM:

```typescript
import { prepareWithSegments, layoutWithLines } from "@chenglou/pretext";

const rich = prepareWithSegments("Long paragraph text...", "16px Arial");
const { lines } = layoutWithLines(rich, containerWidth, lineHeight);
for (const line of lines) {
  renderLine(line.text, line.width);
}
```

### Streaming / Progressive Layout

Lay out text line-by-line as it arrives from an LLM stream or other source:

```typescript
import { prepareWithSegments, layoutNextLine, type LayoutCursor } from "@chenglou/pretext";

const prepared = prepareWithSegments(fullText, font);
let cursor: LayoutCursor = { segmentIndex: 0, graphemeIndex: 0 };

while (true) {
  const line = layoutNextLine(prepared, cursor, maxWidth);
  if (!line) break;
  renderLine(line.text, line.width);
  cursor = line.end; // advance cursor to start of next line
}
```

### Virtual Scrolling Geometry

Get line positions without materializing text strings — efficient for large documents:

```typescript
import { prepareWithSegments, walkLineRanges } from "@chenglou/pretext";

const prepared = prepareWithSegments(text, font);
const lineWidths: number[] = [];
walkLineRanges(prepared, maxWidth, (line) => {
  lineWidths.push(line.width);
});
```

### React Integration

Memoize preparation by `(text, font)` and run layout on resize:

```typescript
const prepared = useMemo(() => prepareWithSegments(text, font), [text, font]);
const result = useMemo(
  () => (width > 0 ? layoutWithLines(prepared, width, lineHeight) : null),
  [prepared, width, lineHeight]
);
```

Combine with `ResizeObserver` to track container width changes. See `examples/react-virtualized-text.tsx` for a complete component.

## Layout Result Types

`layout()` returns `{ lineCount: number, height: number }`.

`layoutWithLines()` returns `{ lineCount, height, lines }` where each line has:
- `text` — the text content of that line
- `width` — the measured width of that line
- `start` / `end` — `LayoutCursor` positions (`{ segmentIndex, graphemeIndex }`)

`layoutNextLine()` returns a single `LayoutLine | null`, advancing a `LayoutCursor` through the text one line at a time. Return `null` when all text is consumed.

`walkLineRanges()` invokes a callback per line with `{ width, start, end }` but does not materialize the text string — use this for geometry-only passes like virtual scrolling.

## Supported Text and CSS Behavior

Pretext handles all Unicode scripts including CJK (per-character breaking), Thai (word segmentation via `Intl.Segmenter`), Arabic (shaping and RTL), emoji (with macOS inflation correction), and mixed bidirectional text.

The layout matches CSS behavior for:
- `white-space: normal` — whitespace is collapsed, lines wrap at word boundaries
- `word-break: normal` — CJK characters break between any two characters; non-CJK text breaks at word boundaries
- `overflow-wrap: break-word` — unbreakable words are broken if they overflow the container

Soft hyphens (`\u00AD`) are supported — text breaks at soft hyphen positions with a visible hyphen when the break is used.

### Bidirectional Text

Pretext computes bidi embedding levels for mixed LTR/RTL text via `prepareWithSegments()`. The `segments` array and bidi metadata are available for custom rendering pipelines that need to reorder glyphs. For standard layout (line count, height, line text), bidi is handled transparently — no additional configuration is needed.

### Whitespace Normalization

Input text is normalized before preparation:
- Consecutive whitespace characters collapse into single spaces
- Leading and trailing whitespace is trimmed
- Newlines within the text are treated as spaces (matching `white-space: normal`)

To preserve explicit line breaks, split text at newline characters and prepare/layout each paragraph separately.

### Text Analysis Internals

The `prepare()` phase performs:
1. Whitespace normalization
2. Script detection (CJK, Arabic, Thai, Myanmar, Latin, etc.)
3. Word segmentation via `Intl.Segmenter`
4. Grapheme cluster identification
5. Canvas-based width measurement per grapheme
6. Break opportunity classification (text, space, glue, zero-width break, soft hyphen)
7. Emoji detection and macOS width correction

All results are cached by `(text, font)` pair. Subsequent calls with identical inputs return immediately.

## Diagnostics

Use `profilePrepare(text, font)` to get timing breakdowns:
- `analysisMs` — time spent in text segmentation and analysis
- `measureMs` — time spent measuring graphemes via canvas
- `totalMs` — total preparation time
- `analysisSegments` / `preparedSegments` / `breakableSegments` — segment counts

This is useful for identifying performance bottlenecks in complex multilingual text.

## Additional Resources

### Reference Files

For detailed documentation, consult:
- **`references/api-reference.md`** — Complete type signatures and function documentation for all exports
- **`references/pitfalls.md`** — Common mistakes, troubleshooting guide, and platform-specific issues
- **`references/integration-patterns.md`** — Detailed patterns for React, canvas rendering, virtual scrolling, streaming layout, and server-side usage

### Example Files

Working code examples in `examples/`:
- **`examples/basic-usage.ts`** — Prepare, layout, layoutWithLines, and resize handling
- **`examples/react-virtualized-text.tsx`** — React component with memoized preparation and ResizeObserver
- **`examples/canvas-text-rendering.ts`** — Drawing pretext-laid-out text onto a `<canvas>` element
- **`examples/streaming-layout.ts`** — Progressive line-by-line layout using `layoutNextLine` with a cursor
