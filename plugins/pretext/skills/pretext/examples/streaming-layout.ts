import {
  prepareWithSegments,
  layoutNextLine,
  layout,
  prepare,
  type LayoutCursor,
  type LayoutLine,
} from "@chenglou/pretext";

// --- Streaming text layout for chat/LLM interfaces ---

class StreamingTextLayout {
  private font: string;
  private maxWidth: number;
  private lineHeight: number;
  private currentText = "";
  private onUpdate: (lines: LayoutLine[], height: number) => void;

  constructor(
    font: string,
    maxWidth: number,
    lineHeight: number,
    onUpdate: (lines: LayoutLine[], height: number) => void
  ) {
    this.font = font;
    this.maxWidth = maxWidth;
    this.lineHeight = lineHeight;
    this.onUpdate = onUpdate;
  }

  /** Call as new text chunks arrive from the stream */
  append(chunk: string) {
    this.currentText += chunk;
    this.relayout();
  }

  /** Call when container resizes */
  resize(maxWidth: number) {
    this.maxWidth = maxWidth;
    this.relayout();
  }

  private relayout() {
    const prepared = prepareWithSegments(this.currentText, this.font);
    const lines: LayoutLine[] = [];
    let cursor: LayoutCursor = { segmentIndex: 0, graphemeIndex: 0 };

    while (true) {
      const line = layoutNextLine(prepared, cursor, this.maxWidth);
      if (!line) break;
      lines.push(line);
      cursor = line.end;
    }

    this.onUpdate(lines, lines.length * this.lineHeight);
  }
}

// --- Example: simulated LLM stream ---

const container = document.getElementById("chat-message")!;
const font = "16px Inter, sans-serif";
const lineHeight = 24;

const streamLayout = new StreamingTextLayout(
  font,
  container.clientWidth,
  lineHeight,
  (lines, height) => {
    // Update DOM with laid-out lines
    container.style.height = `${height}px`;
    container.innerHTML = lines
      .map((line) => `<div style="white-space: pre">${line.text}</div>`)
      .join("");

    // Auto-scroll to bottom
    container.scrollTop = container.scrollHeight;
  }
);

// Handle container resize
new ResizeObserver((entries) => {
  const width = entries[0].contentRect.width;
  streamLayout.resize(width);
}).observe(container);

// Simulate streaming chunks
const fullText =
  "Pretext uses a two-phase approach to text layout. " +
  "First, prepare() segments the text and measures grapheme widths using canvas. " +
  "This is the slow step, taking about 17ms for 500 texts. " +
  "Then, layout() performs pure arithmetic line-breaking on the cached widths. " +
  "This is the fast step, taking only 0.10ms for 500 texts.";

// Simulate word-by-word streaming
const words = fullText.split(" ");
let wordIndex = 0;

const interval = setInterval(() => {
  if (wordIndex >= words.length) {
    clearInterval(interval);
    return;
  }
  const chunk = (wordIndex === 0 ? "" : " ") + words[wordIndex];
  streamLayout.append(chunk);
  wordIndex++;
}, 50);

// --- Height-only tracking (lighter weight) ---

function trackStreamingHeight(
  text: string,
  font: string,
  maxWidth: number,
  lineHeight: number
): number {
  const prepared = prepare(text, font);
  const { height } = layout(prepared, maxWidth, lineHeight);
  return height;
}
