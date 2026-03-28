# pretext

Claude Code plugin for [`@chenglou/pretext`](https://github.com/chenglou/pretext) — a pure JavaScript/TypeScript library for multiline text measurement and layout without DOM reflow.

## What This Plugin Provides

A single skill that helps Claude correctly use pretext's API when working in codebases that use it:

- **API guidance** — choosing between `layout()`, `layoutWithLines()`, `layoutNextLine()`, and `walkLineRanges()`
- **Critical rules** — font string safety (`system-ui` pitfall), the prepare-once/layout-many pattern, locale configuration
- **Integration patterns** — React hooks with ResizeObserver, canvas rendering, virtual scrolling, streaming/chat layout
- **Pitfall reference** — common mistakes and troubleshooting
- **Working examples** — basic usage, React component, canvas rendering, streaming layout

## Installation

```bash
# Test locally
claude --plugin-dir /path/to/plugins/pretext

# Or install from the marketplace (if published)
claude plugin install pretext@marketplace-name
```

## Plugin Structure

```
pretext/
├── .claude-plugin/plugin.json
├── skills/
│   └── pretext/
│       ├── SKILL.md                      # Core guidance
│       ├── references/
│       │   ├── api-reference.md          # Full API documentation
│       │   ├── integration-patterns.md   # React, canvas, streaming patterns
│       │   └── pitfalls.md               # Common mistakes
│       └── examples/
│           ├── basic-usage.ts
│           ├── react-virtualized-text.tsx
│           ├── canvas-text-rendering.ts
│           └── streaming-layout.ts
└── README.md
```

## Trigger Phrases

The skill activates when asking about: pretext, `@chenglou/pretext`, text measurement without DOM, multiline text layout, canvas text measurement, `layoutWithLines`, `layoutNextLine`, `walkLineRanges`, `PreparedText`, and related topics.
