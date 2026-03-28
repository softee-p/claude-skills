import {
  prepare,
  prepareWithSegments,
  layout,
  layoutWithLines,
  profilePrepare,
  clearCache,
  setLocale,
} from "@chenglou/pretext";

// --- Basic: get line count and height ---

const font = "16px Arial";
const lineHeight = 20;
const text =
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";

const prepared = prepare(text, font);
const result = layout(prepared, 300, lineHeight);
console.log(`Lines: ${result.lineCount}, Height: ${result.height}px`);

// --- Rich: get per-line content ---

const rich = prepareWithSegments(text, font);
const linesResult = layoutWithLines(rich, 300, lineHeight);

for (const line of linesResult.lines) {
  console.log(`"${line.text}" (width: ${line.width.toFixed(1)}px)`);
}

// --- Resize handler: only re-layout, never re-prepare ---

const container = document.getElementById("text-container")!;
const preparedForResize = prepare(text, font);

const observer = new ResizeObserver((entries) => {
  const width = entries[0].contentRect.width;
  const { height } = layout(preparedForResize, width, lineHeight);
  container.style.height = `${height}px`;
});
observer.observe(container);

// --- Locale: Thai text ---

setLocale("th");
const thaiPrepared = prepare("สวัสดีครับ ยินดีต้อนรับสู่ประเทศไทย", font);
const thaiResult = layout(thaiPrepared, 200, lineHeight);
console.log(`Thai lines: ${thaiResult.lineCount}`);
setLocale(undefined); // reset

// --- Diagnostics ---

const profile = profilePrepare(text, font);
console.log(
  `Analysis: ${profile.analysisMs.toFixed(2)}ms, ` +
    `Measure: ${profile.measureMs.toFixed(2)}ms, ` +
    `Total: ${profile.totalMs.toFixed(2)}ms`
);
console.log(
  `Segments: ${profile.analysisSegments} analyzed, ` +
    `${profile.preparedSegments} prepared, ` +
    `${profile.breakableSegments} breakable`
);

// --- Cleanup after bulk operations ---

clearCache();
