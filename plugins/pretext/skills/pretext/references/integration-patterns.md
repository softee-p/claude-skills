# Pretext Integration Patterns

Detailed patterns for integrating `@chenglou/pretext` into different application contexts.

## React Integration

### Custom Hooks

Create hooks that separate preparation (memoized by text/font) from layout (runs on resize):

```typescript
import { useMemo, useState, useEffect, useRef, useCallback } from "react";
import {
  prepareWithSegments,
  layoutWithLines,
  type PreparedTextWithSegments,
  type LayoutLinesResult,
} from "@chenglou/pretext";

function usePreparedText(text: string, font: string): PreparedTextWithSegments {
  return useMemo(() => prepareWithSegments(text, font), [text, font]);
}

function useTextLayout(
  prepared: PreparedTextWithSegments,
  maxWidth: number,
  lineHeight: number
): LayoutLinesResult | null {
  const [result, setResult] = useState<LayoutLinesResult | null>(null);

  useEffect(() => {
    if (maxWidth > 0) {
      setResult(layoutWithLines(prepared, maxWidth, lineHeight));
    }
  }, [prepared, maxWidth, lineHeight]);

  return result;
}
```

### ResizeObserver Pattern

Track container width changes and re-layout:

```tsx
function TextBlock({ text, font, lineHeight }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(0);
  const prepared = usePreparedText(text, font);
  const layoutResult = useTextLayout(prepared, width, lineHeight);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry) setWidth(entry.contentRect.width);
    });

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={containerRef} style={{ font, lineHeight: `${lineHeight}px` }}>
      {layoutResult?.lines.map((line, i) => (
        <div key={i}>{line.text}</div>
      ))}
    </div>
  );
}
```

### Height-Only Optimization

When only the container height is needed (no custom line rendering), use `prepare()` + `layout()` instead of `prepareWithSegments()` + `layoutWithLines()` for better performance:

```tsx
import { prepare, layout } from "@chenglou/pretext";

function useTextHeight(text: string, font: string, maxWidth: number, lineHeight: number) {
  const prepared = useMemo(() => prepare(text, font), [text, font]);
  return useMemo(
    () => (maxWidth > 0 ? layout(prepared, maxWidth, lineHeight) : null),
    [prepared, maxWidth, lineHeight]
  );
}
```

## Canvas Rendering

### Drawing Laid-Out Text

Use `layoutWithLines()` to get per-line content, then draw with `ctx.fillText()`:

```typescript
import { prepareWithSegments, layoutWithLines } from "@chenglou/pretext";

function drawText(
  ctx: CanvasRenderingContext2D,
  text: string,
  font: string,
  maxWidth: number,
  lineHeight: number,
  x: number,
  y: number
) {
  ctx.font = font;
  ctx.textBaseline = "top";

  const prepared = prepareWithSegments(text, font);
  const { lines } = layoutWithLines(prepared, maxWidth, lineHeight);

  for (let i = 0; i < lines.length; i++) {
    ctx.fillText(lines[i].text, x, y + i * lineHeight);
  }
}
```

### High-DPI Canvas

Scale for `devicePixelRatio`:

```typescript
function setupHiDPICanvas(canvas: HTMLCanvasElement, width: number, height: number) {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  const ctx = canvas.getContext("2d")!;
  ctx.scale(dpr, dpr);
  return ctx;
}
```

### Right-Aligned and Centered Text

Use line width information for alignment:

```typescript
const { lines } = layoutWithLines(prepared, maxWidth, lineHeight);

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  // Right-aligned
  const xRight = maxWidth - line.width;
  // Centered
  const xCenter = (maxWidth - line.width) / 2;

  ctx.fillText(line.text, xCenter, y + i * lineHeight);
}
```

## Virtual Scrolling

### Geometry-Only Pass

Use `walkLineRanges()` to compute line positions without materializing text — efficient for large documents with virtual scroll:

```typescript
import { prepareWithSegments, walkLineRanges } from "@chenglou/pretext";

interface LinePosition {
  y: number;
  width: number;
  start: { segmentIndex: number; graphemeIndex: number };
  end: { segmentIndex: number; graphemeIndex: number };
}

function computeLinePositions(
  text: string,
  font: string,
  maxWidth: number,
  lineHeight: number
): LinePosition[] {
  const prepared = prepareWithSegments(text, font);
  const positions: LinePosition[] = [];

  walkLineRanges(prepared, maxWidth, (line) => {
    positions.push({
      y: positions.length * lineHeight,
      width: line.width,
      start: { ...line.start },
      end: { ...line.end },
    });
  });

  return positions;
}
```

### Visible Range Rendering

Only materialize text for visible lines:

```typescript
import { layoutNextLine, type LayoutCursor } from "@chenglou/pretext";

function renderVisibleLines(
  prepared: PreparedTextWithSegments,
  maxWidth: number,
  lineHeight: number,
  scrollTop: number,
  viewportHeight: number
) {
  const firstVisible = Math.floor(scrollTop / lineHeight);
  const lastVisible = Math.ceil((scrollTop + viewportHeight) / lineHeight);

  // Skip to the first visible line
  let cursor: LayoutCursor = { segmentIndex: 0, graphemeIndex: 0 };
  for (let i = 0; i < firstVisible; i++) {
    const line = layoutNextLine(prepared, cursor, maxWidth);
    if (!line) return [];
    cursor = line.end;
  }

  // Materialize only visible lines
  const visibleLines = [];
  for (let i = firstVisible; i <= lastVisible; i++) {
    const line = layoutNextLine(prepared, cursor, maxWidth);
    if (!line) break;
    visibleLines.push({ ...line, y: i * lineHeight });
    cursor = line.end;
  }

  return visibleLines;
}
```

## Streaming / Chat Layout

### Progressive Layout with layoutNextLine

For chat interfaces receiving text from an LLM stream, use `layoutNextLine()` to update layout incrementally:

```typescript
import {
  prepareWithSegments,
  layoutNextLine,
  type LayoutCursor,
  type LayoutLine,
} from "@chenglou/pretext";

class StreamingTextLayout {
  private lines: LayoutLine[] = [];
  private font: string;
  private maxWidth: number;

  constructor(font: string, maxWidth: number) {
    this.font = font;
    this.maxWidth = maxWidth;
  }

  update(fullText: string): { lines: LayoutLine[]; height: number; lineHeight: number } {
    const lineHeight = 20;
    const prepared = prepareWithSegments(fullText, this.font);

    // Re-layout from scratch (fast since layout is arithmetic-only)
    this.lines = [];
    let cursor: LayoutCursor = { segmentIndex: 0, graphemeIndex: 0 };

    while (true) {
      const line = layoutNextLine(prepared, cursor, this.maxWidth);
      if (!line) break;
      this.lines.push(line);
      cursor = line.end;
    }

    return {
      lines: this.lines,
      height: this.lines.length * lineHeight,
      lineHeight,
    };
  }
}
```

**Note:** Even though `prepareWithSegments()` is called on each update, pretext's internal caching means segments already measured are reused. The `layout` phase remains sub-millisecond.

### Height Tracking for Auto-Scroll

Track height changes to trigger auto-scroll in chat UIs:

```typescript
import { prepare, layout } from "@chenglou/pretext";

function getStreamingHeight(
  fullText: string,
  font: string,
  maxWidth: number,
  lineHeight: number
): number {
  const prepared = prepare(fullText, font);
  const { height } = layout(prepared, maxWidth, lineHeight);
  return height;
}
```

## Server-Side Usage

### HarfBuzz-Based Measurement

For headless environments (Node.js, Bun) without canvas, pretext's repository includes a HarfBuzz-based measurement module at `src/measure-harfbuzz.ts`. This loads font files directly and produces deterministic cross-platform measurements.

Key characteristics:
- Loads explicit font files (`.ttf`, `.otf`) rather than relying on system fonts
- Measurements are deterministic across platforms
- Requires the `harfbuzzjs` npm package
- Suitable for SSR pre-computation and research applications

### Pre-Computing Layout for SSR

Compute layout data on the server and send it to the client to avoid layout shift:

```typescript
// Server: compute layout with known viewport width
const prepared = prepare(text, font);
const result = layout(prepared, estimatedWidth, lineHeight);

// Send height to client for initial render
const ssrData = { height: result.height, lineCount: result.lineCount };
```

The client can use this pre-computed height for initial container sizing, then refine with actual measurements after hydration.

## Variable-Width Layout

### Different Widths Per Section

For layouts where the available width varies (e.g., text flowing around an image), prepare once and layout multiple times:

```typescript
const prepared = prepare(text, font);

// Full width for first 3 lines, narrower after (text wrapping around image)
const fullWidthResult = layout(prepared, 600, lineHeight);
const narrowResult = layout(prepared, 400, lineHeight);
```

For more precise control over variable widths per line, use `layoutNextLine()` with different `maxWidth` values for different cursor positions.
