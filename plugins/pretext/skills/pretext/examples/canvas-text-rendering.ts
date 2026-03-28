import { prepareWithSegments, layoutWithLines } from "@chenglou/pretext";

// --- Setup high-DPI canvas ---

function setupCanvas(
  canvas: HTMLCanvasElement,
  width: number,
  height: number
): CanvasRenderingContext2D {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  const ctx = canvas.getContext("2d")!;
  ctx.scale(dpr, dpr);
  return ctx;
}

// --- Draw text with pretext layout ---

function drawText(
  ctx: CanvasRenderingContext2D,
  text: string,
  font: string,
  maxWidth: number,
  lineHeight: number,
  x: number,
  y: number,
  align: "left" | "center" | "right" = "left"
) {
  ctx.font = font;
  ctx.textBaseline = "top";
  ctx.fillStyle = "#1a1a1a";

  const prepared = prepareWithSegments(text, font);
  const { lines } = layoutWithLines(prepared, maxWidth, lineHeight);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let drawX = x;

    if (align === "right") {
      drawX = x + maxWidth - line.width;
    } else if (align === "center") {
      drawX = x + (maxWidth - line.width) / 2;
    }

    ctx.fillText(line.text, drawX, y + i * lineHeight);
  }

  return lines.length * lineHeight;
}

// --- Example: render a paragraph on canvas ---

const canvas = document.getElementById("canvas") as HTMLCanvasElement;
const width = 600;
const height = 400;
const ctx = setupCanvas(canvas, width, height);

// Clear background
ctx.fillStyle = "#ffffff";
ctx.fillRect(0, 0, width, height);

const paragraph =
  "Pretext performs multiline text measurement and layout without DOM. " +
  "It uses a two-phase approach: prepare() segments and measures text once, " +
  "then layout() performs pure arithmetic on cached widths for every resize. " +
  "This makes it ideal for canvas rendering, game UIs, and custom text editors.";

// Draw left-aligned paragraph
const usedHeight = drawText(ctx, paragraph, "16px Georgia, serif", 500, 22, 50, 30, "left");

// Draw centered paragraph below
drawText(
  ctx,
  "Centered text with full CJK, emoji, and bidi support.",
  "bold 14px Arial",
  400,
  20,
  100,
  30 + usedHeight + 20,
  "center"
);
