# Pretext Common Pitfalls and Troubleshooting

## 1. Using `system-ui` as Font on macOS

**Symptom:** Measurements return incorrect widths. Text overflows or wraps too early on macOS but works on other platforms.

**Cause:** The `system-ui` CSS keyword resolves to different physical fonts on different platforms (San Francisco on macOS, Segoe UI on Windows, etc.). Canvas measurement with `system-ui` produces platform-dependent results that may not match the actual rendered font.

**Fix:** Use named fonts explicitly:

```typescript
// Wrong
const prepared = prepare(text, "16px system-ui");

// Correct
const prepared = prepare(text, "16px -apple-system, Helvetica Neue, sans-serif");
const prepared = prepare(text, "16px Helvetica");
const prepared = prepare(text, "16px Inter");
```

Use a specific font-family name. If cross-platform consistency is critical, use a web font loaded via `@font-face`.

## 2. Re-Preparing on Every Render

**Symptom:** High CPU usage on resize or scroll. `profilePrepare()` shows `totalMs` being called hundreds of times.

**Cause:** Calling `prepare()` inside a render loop, resize handler, or React component body without memoization.

**Fix:** Prepare once, cache the result, and only call `layout()` on resize:

```typescript
// Wrong: prepare called on every resize
function onResize(width: number) {
  const prepared = prepare(text, font); // Expensive!
  return layout(prepared, width, lineHeight);
}

// Correct: prepare once, layout on resize
const prepared = prepare(text, font);
function onResize(width: number) {
  return layout(prepared, width, lineHeight);
}
```

In React, use `useMemo` to memoize the preparation:

```typescript
const prepared = useMemo(() => prepare(text, font), [text, font]);
```

## 3. Using `prepare()` When `prepareWithSegments()` Is Needed

**Symptom:** Runtime error or missing data when calling `layoutWithLines()`, `layoutNextLine()`, or `walkLineRanges()`.

**Cause:** These functions require `PreparedTextWithSegments` (from `prepareWithSegments()`), not plain `PreparedText` (from `prepare()`).

**Fix:** Match the preparation function to the layout function:

```typescript
// For layout() and countPreparedLines() only:
const prepared = prepare(text, font);

// For layoutWithLines(), layoutNextLine(), walkLineRanges():
const prepared = prepareWithSegments(text, font);
```

**Rule of thumb:** If line content or per-line geometry is needed, use `prepareWithSegments()`. If only line count or total height is needed, `prepare()` suffices.

## 4. Invalid Font String Format

**Symptom:** Measurement returns zero or incorrect widths. Canvas `measureText()` fails silently.

**Cause:** The font string must be a valid CSS font shorthand. Common mistakes:

```typescript
// Wrong: missing size
prepare(text, "Arial");

// Wrong: size without family
prepare(text, "16px");

// Wrong: using font-family CSS property syntax
prepare(text, "font-family: Arial");

// Wrong: using object
prepare(text, { family: "Arial", size: 16 });
```

**Fix:** Use valid CSS font shorthand:

```typescript
// Correct examples
prepare(text, "16px Arial");
prepare(text, "bold 14px Menlo, monospace");
prepare(text, "italic 16px/1.5 Georgia, serif");
prepare(text, "600 13px Inter, sans-serif");
```

The format follows the CSS `font` shorthand: `[style] [weight] size[/line-height] family`.

## 5. Thai Text Breaking at Wrong Positions

**Symptom:** Thai text breaks in the middle of words instead of at word boundaries.

**Cause:** Thai script does not use spaces between words. Correct word segmentation requires `Intl.Segmenter` with the Thai locale, which must be set explicitly before preparation.

**Fix:** Call `setLocale("th")` before preparing Thai text:

```typescript
import { setLocale, prepare } from "@chenglou/pretext";

setLocale("th");
const prepared = prepare(thaiText, font);

// Reset after if processing other languages
setLocale(undefined);
```

**Note:** CJK text (Chinese, Japanese, Korean) does not need a locale override — pretext detects CJK characters via Unicode ranges and applies per-character breaking automatically.

## 6. Cache Growth and Memory

**Symptom:** Memory usage grows steadily when processing many distinct texts (e.g., batch processing documents, chat message history).

**Cause:** Pretext caches grapheme measurements internally to speed up repeated prepare/layout calls. With thousands of unique texts, the cache accumulates significant data.

**Fix:** Call `clearCache()` after batch operations:

```typescript
import { prepare, layout, clearCache } from "@chenglou/pretext";

// Process a large batch
for (const doc of documents) {
  const prepared = prepare(doc.text, font);
  const result = layout(prepared, width, lineHeight);
  results.push(result);
}

// Free cached measurement data
clearCache();
```

For typical interactive use (a few hundred texts), caching improves performance and manual clearing is unnecessary.

## 7. OffscreenCanvas Not Available

**Symptom:** Error about missing canvas context in workers or Node.js environments.

**Cause:** Pretext uses `OffscreenCanvas` when available, falling back to DOM `<canvas>`. In environments without either (older workers, Node.js without canvas polyfill), measurement fails.

**Fix options:**

1. **In workers:** Ensure `OffscreenCanvas` is available (supported in modern browsers). Transfer an OffscreenCanvas from the main thread if needed.
2. **In Node.js:** Use a canvas polyfill (e.g., `@napi-rs/canvas` or `node-canvas`).
3. **Server-side without canvas:** Use the HarfBuzz-based measurement approach. See `src/measure-harfbuzz.ts` in the pretext repository for the server-side measurement implementation that loads font files directly.

## 8. Emoji Width Inconsistency on macOS

**Symptom:** Text containing emoji measures wider than expected on macOS, causing premature line breaks.

**Cause:** macOS canvas `measureText()` inflates emoji widths by a constant amount per emoji grapheme. Pretext detects and corrects this automatically via a cached DOM calibration.

**This is handled automatically.** No user action is needed. If emoji measurements seem wrong:

1. Ensure `clearCache()` has not been called immediately before measuring emoji text (the calibration is cached).
2. Verify the font string is correct — emoji rendering varies by font.
3. Check that the text is actually emoji (some symbols look like emoji but are regular Unicode characters).

## 9. Soft Hyphens Not Breaking

**Symptom:** Text with soft hyphens (`\u00AD`) does not break at hyphen positions.

**Cause:** Soft hyphen behavior depends on the engine profile (browser detection). In some environments, the engine profile may not enable soft hyphen support.

**Behavior:** When soft hyphens are supported, pretext breaks lines at `\u00AD` positions and adds a visible hyphen at the break point. When the soft hyphen is not used for a break, it remains invisible (zero-width).

**Verification:** Test with a long word containing embedded `\u00AD` characters at a narrow width. The word should break at the hyphen position with a visible `-` character.
