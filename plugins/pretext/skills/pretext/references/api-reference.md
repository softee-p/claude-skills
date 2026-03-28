# Pretext API Reference

Complete reference for all types and functions exported from `@chenglou/pretext`.

## Types

### PreparedText

```typescript
type PreparedText = { readonly [preparedTextBrand]: true }
```

Opaque branded type returned by `prepare()`. Contains cached segmentation and measurement data. Use with `layout()` and `countPreparedLines()`.

Cannot be serialized or inspected directly — treat as an opaque handle.

### PreparedTextWithSegments

```typescript
type PreparedTextWithSegments = PreparedText & { segments: string[] }
```

Extended prepared text returned by `prepareWithSegments()`. Exposes the `segments` array for custom rendering pipelines. Required by `layoutWithLines()`, `layoutNextLine()`, and `walkLineRanges()`.

The `segments` array contains text segments after normalization, analysis, and splitting. These are the atomic units used for line breaking.

### LayoutCursor

```typescript
type LayoutCursor = {
  segmentIndex: number
  graphemeIndex: number
}
```

Tracks position within prepared text. Used by `layoutNextLine()` for incremental layout and present in `LayoutLine.start` / `LayoutLine.end` for line boundary positions.

- `segmentIndex` — index into the segments array
- `graphemeIndex` — index of the grapheme cluster within that segment

### LayoutResult

```typescript
type LayoutResult = {
  lineCount: number
  height: number
}
```

Returned by `layout()`. Contains the number of lines and total height (computed as `lineCount * lineHeight`).

### LayoutLine

```typescript
type LayoutLine = {
  text: string
  width: number
  start: LayoutCursor
  end: LayoutCursor
}
```

Represents a single laid-out line with materialized text content.

- `text` — the text content of this line (after normalization, with trailing spaces trimmed)
- `width` — the measured width of this line's content in pixels
- `start` — cursor position at the beginning of this line
- `end` — cursor position at the end of this line

### LayoutLineRange

```typescript
type LayoutLineRange = {
  width: number
  start: LayoutCursor
  end: LayoutCursor
}
```

Like `LayoutLine` but without the `text` field. Used by `walkLineRanges()` for geometry-only passes where text materialization is unnecessary (e.g., virtual scrolling, hit testing).

### LayoutLinesResult

```typescript
type LayoutLinesResult = LayoutResult & {
  lines: LayoutLine[]
}
```

Returned by `layoutWithLines()`. Combines the overall layout result (`lineCount`, `height`) with an array of individual `LayoutLine` objects.

### PrepareProfile

```typescript
type PrepareProfile = {
  analysisMs: number
  measureMs: number
  totalMs: number
  analysisSegments: number
  preparedSegments: number
  breakableSegments: number
}
```

Diagnostic timing and count data returned by `profilePrepare()`.

- `analysisMs` — time spent segmenting and analyzing text (script detection, break classification)
- `measureMs` — time spent measuring grapheme widths via canvas
- `totalMs` — total preparation time (`analysisMs + measureMs`)
- `analysisSegments` — number of segments produced by text analysis
- `preparedSegments` — number of segments after preparation
- `breakableSegments` — number of segments that can be broken across lines

## Preparation Functions

### prepare

```typescript
function prepare(text: string, font: string): PreparedText
```

Segments text via `Intl.Segmenter`, measures grapheme widths through canvas, and returns a cached `PreparedText` handle for width-independent layout operations.

**Parameters:**
- `text` — the text string to prepare. Whitespace is normalized (`white-space: normal` behavior).
- `font` — a valid CSS font shorthand string (e.g., `"16px Arial"`, `"bold 14px Menlo"`). Must include size.

**Returns:** `PreparedText` — an opaque handle for use with `layout()` and `countPreparedLines()`.

**Behavior:**
- Normalizes whitespace (collapses runs, trims leading/trailing)
- Detects and handles CJK (per-character breaking), Thai, Arabic, Myanmar
- Applies emoji correction for macOS canvas inflation
- Merges punctuation with preceding segments where appropriate
- Results are cached internally — calling with the same `(text, font)` reuses cached data

### prepareWithSegments

```typescript
function prepareWithSegments(text: string, font: string): PreparedTextWithSegments
```

Rich variant of `prepare()` that exposes segment structural data. Required for `layoutWithLines()`, `layoutNextLine()`, and `walkLineRanges()`.

**Parameters:** Same as `prepare()`.

**Returns:** `PreparedTextWithSegments` — includes a `segments: string[]` array alongside all internal data.

### profilePrepare

```typescript
function profilePrepare(text: string, font: string): PrepareProfile
```

Diagnostic helper that runs preparation while separating analysis and measurement phases with timing information.

**Parameters:** Same as `prepare()`.

**Returns:** `PrepareProfile` with millisecond timings and segment counts.

**Use case:** Identifying performance bottlenecks. High `analysisMs` indicates complex text (Arabic, mixed scripts). High `measureMs` indicates many unique graphemes requiring canvas measurement.

## Layout Functions

### layout

```typescript
function layout(
  prepared: PreparedText,
  maxWidth: number,
  lineHeight: number
): LayoutResult
```

Pure arithmetic line-breaking on cached widths. This is the hot-path function — call on every resize.

**Parameters:**
- `prepared` — a `PreparedText` or `PreparedTextWithSegments` from `prepare()` or `prepareWithSegments()`
- `maxWidth` — maximum line width in pixels. Lines break at or before this width.
- `lineHeight` — height of each line in pixels. Total height = `lineCount * lineHeight`.

**Returns:** `LayoutResult` with `lineCount` and `height`.

**Performance:** ~0.0002ms per text. No DOM access, no canvas measurement — pure arithmetic.

### layoutWithLines

```typescript
function layoutWithLines(
  prepared: PreparedTextWithSegments,
  maxWidth: number,
  lineHeight: number
): LayoutLinesResult
```

Extended layout that materializes per-line text content and widths.

**Parameters:**
- `prepared` — must be `PreparedTextWithSegments` from `prepareWithSegments()`. Plain `PreparedText` will not work.
- `maxWidth` — maximum line width in pixels.
- `lineHeight` — height of each line in pixels.

**Returns:** `LayoutLinesResult` with `lineCount`, `height`, and `lines` array.

**Use case:** Custom rendering to canvas, SVG, or any target where per-line text content is needed.

### layoutNextLine

```typescript
function layoutNextLine(
  prepared: PreparedTextWithSegments,
  start: LayoutCursor,
  maxWidth: number
): LayoutLine | null
```

Incremental line-by-line layout. Returns the next line starting from the given cursor, or `null` if all text is consumed.

**Parameters:**
- `prepared` — must be `PreparedTextWithSegments`
- `start` — a `LayoutCursor` indicating where to start. Initialize as `{ segmentIndex: 0, graphemeIndex: 0 }` for the first line.
- `maxWidth` — maximum line width in pixels.

**Returns:** `LayoutLine | null`. The returned line's `end` cursor becomes the `start` for the next call.

**Use case:** Streaming or progressive rendering where lines are consumed one at a time. Useful for chat interfaces receiving text from an LLM stream.

### walkLineRanges

```typescript
function walkLineRanges(
  prepared: PreparedTextWithSegments,
  maxWidth: number,
  onLine: (line: LayoutLineRange) => void
): number
```

Batch geometry pass without materializing line text. Invokes callback for each line.

**Parameters:**
- `prepared` — must be `PreparedTextWithSegments`
- `maxWidth` — maximum line width in pixels.
- `onLine` — callback receiving a `LayoutLineRange` (width + start/end cursors, no text string).

**Returns:** Total line count.

**Use case:** Virtual scrolling, hit testing, or any scenario where line geometry is needed without the overhead of string materialization.

### countPreparedLines

```typescript
function countPreparedLines(
  prepared: PreparedText,
  maxWidth: number
): number
```

Returns the number of lines needed to fit the prepared text within the given width.

**Parameters:**
- `prepared` — a `PreparedText` or `PreparedTextWithSegments`
- `maxWidth` — maximum line width in pixels.

**Returns:** Line count as a number.

### walkPreparedLines

```typescript
function walkPreparedLines(
  prepared: PreparedText,
  maxWidth: number,
  onLine?: (line: LayoutLineRange) => void
): number
```

Walks through all lines, optionally invoking a callback per line. Returns line count.

**Parameters:**
- `prepared` — a `PreparedText` or `PreparedTextWithSegments`
- `maxWidth` — maximum line width in pixels.
- `onLine` — optional callback per line.

**Returns:** Line count.

## Utility Functions

### clearCache

```typescript
function clearCache(): void
```

Clears all internal caches: grapheme segmenter, measurement caches, and line text caches. Call after bulk operations processing thousands of distinct texts to free memory. Not needed for typical interactive use.

### setLocale

```typescript
function setLocale(locale?: string): void
```

Updates the locale used for text analysis and clears dependent caches.

**Parameters:**
- `locale` — a BCP 47 language tag (e.g., `"th"` for Thai, `"ja"` for Japanese). Pass `undefined` to reset to the default locale.

**When to use:** Call before `prepare()` when text contains Thai or other languages requiring locale-specific word segmentation. CJK does not require a locale override — it is detected automatically via Unicode ranges.

**Important:** Changing the locale invalidates cached preparations. Re-prepare text after changing locale.
