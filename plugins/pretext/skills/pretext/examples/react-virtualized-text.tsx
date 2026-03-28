import { useEffect, useMemo, useRef, useState } from "react";
import {
  prepareWithSegments,
  layoutWithLines,
  type PreparedTextWithSegments,
  type LayoutLinesResult,
} from "@chenglou/pretext";

// --- Custom hooks ---

function usePreparedText(
  text: string,
  font: string
): PreparedTextWithSegments {
  return useMemo(() => prepareWithSegments(text, font), [text, font]);
}

function useContainerWidth(ref: React.RefObject<HTMLElement | null>): number {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry) setWidth(entry.contentRect.width);
    });

    observer.observe(el);
    return () => observer.disconnect();
  }, [ref]);

  return width;
}

// --- TextBlock component ---

interface TextBlockProps {
  text: string;
  font: string;
  lineHeight: number;
  className?: string;
}

export function TextBlock({ text, font, lineHeight, className }: TextBlockProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const width = useContainerWidth(containerRef);
  const prepared = usePreparedText(text, font);

  const layoutResult: LayoutLinesResult | null = useMemo(
    () => (width > 0 ? layoutWithLines(prepared, width, lineHeight) : null),
    [prepared, width, lineHeight]
  );

  return (
    <div
      ref={containerRef}
      className={className}
      style={{
        font,
        lineHeight: `${lineHeight}px`,
        minHeight: layoutResult ? `${layoutResult.height}px` : undefined,
      }}
    >
      {layoutResult?.lines.map((line, i) => (
        <div key={i} style={{ whiteSpace: "pre" }}>
          {line.text}
        </div>
      ))}
    </div>
  );
}

// --- Usage ---

function App() {
  const longText =
    "Pretext is a pure JavaScript/TypeScript library for multiline text " +
    "measurement and layout that operates without DOM measurements, avoiding " +
    "expensive layout reflow operations. It supports CJK, Thai, Arabic, " +
    "emoji, and mixed bidirectional text with perfect accuracy across " +
    "Chrome, Safari, and Firefox.";

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <TextBlock text={longText} font="16px Inter, sans-serif" lineHeight={24} />
    </div>
  );
}

export default App;
