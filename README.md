<p align="center">
  <br>
  <strong><code>claude-skills</code></strong>
  <br>
  A curated marketplace of plugins for <a href="https://claude.ai/claude-code">Claude Code</a>
  <br>
  <sub>Each plugin is independently installable — load only what you need.</sub>
  <br>
  <br>
</p>

---

<br>

## Plugins

### `rwsdk-toolkit`

A Claude Code plugin for building full-stack apps with [RedwoodSDK](https://rwsdk.com) — React Server Components on Cloudflare Workers.

**Skills** auto-load based on what you're working on — no invocation needed. When you ask about routing, styling, components, or production issues, the relevant skill activates automatically. **Slash commands** are explicit multi-step workflows you invoke when you want a structured task executed from start to finish.

<details>
<summary>6 commands &ensp;·&ensp; 5 skills</summary>
<br>

| Command | What it does |
|---------|-------------|
| `/rwsdk:new` | Scaffold a new project or add a route/page/component |
| `/rwsdk:fix` | 4-phase visual frontend debugging |
| `/rwsdk:components` | Add or update shadcn/ui components safely |
| `/rwsdk:audit` | 6-phase production health audit |
| `/rwsdk:docs` | Look up a specific documentation topic |
| `/rwsdk:sync` | Sync docs with the latest official RedwoodSDK docs |

<br>

| Skill | What it does |
|-------|-------------|
| `rwsdk-docs` | Full official docs (50+ `.mdx` files) — routing, RSC, auth, storage, email, queues, cron, hosting, and all frontend guides |
| `rwsdk-frontend` | 4-phase visual debugging — opens the dev server, inspects viewports, creates a fix plan from visual evidence |
| `rwsdk-shadcn-update` | Add or update shadcn/ui components while preserving customizations and enforcing RSC compliance |
| `rwsdk-audit-deployed` | 6-phase production audit via cloudflare-observability MCP — HEALTHY / DEGRADED / CRITICAL report |
| `update-rwsdk-docs` | Shallow-clones the official SDK repo and refreshes the bundled docs |

<br>

| What you type | Skill that loads |
|--------------|-----------------|
| "How do I add middleware to my route?" | `rwsdk-docs` |
| "My mobile layout is broken" | `rwsdk-frontend` |
| "Add a shadcn Dialog component" | `rwsdk-shadcn-update` |
| "Is my worker healthy after the deploy?" | `rwsdk-audit-deployed` |
| "The docs seem outdated, refresh them" | `update-rwsdk-docs` |

</details>

<br>

### `practical-typography`

Applies the key rules from Butterick's *Practical Typography* — proper punctuation, dashes, emphasis, spacing, and layout guidance for any reader-facing text.

> *"Straight quotes" are for code. "Curly quotes" are for people.*
>
> *Two hyphens aren't a dash. Three periods aren't an ellipsis.
> And two spaces after a period haven't been correct since the typewriter.*
>
> This plugin teaches Claude the difference — so every em dash, en dash,
> apostrophe, and ellipsis lands exactly right.

<details>
<summary>What it fixes</summary>
<br>

| Before | After | Rule |
|--------|-------|------|
| `"Hello"` | "Hello" | Curly quotes, not straight |
| `it's` | it's | Proper apostrophe (U+2019) |
| `2020--2025` | 2020–2025 | En dash for ranges |
| `Wait -- what?` | Wait — what? | Em dash for breaks |
| `etc...` | etc.… | Proper ellipsis character |
| `(c) 2026` | ©&nbsp;2026 | Real symbols, not fakes |

</details>

<br>

### `transformersjs-docs`

Build with Transformers.js — run ML models for NLP, vision, and audio directly in the browser or Node.js, with patterns for React, Next.js, and vanilla JS.

<details>
<summary>Framework references</summary>
<br>

Includes tutorials for **React**, **Next.js**, **vanilla JavaScript**, and **Node.js** — each with pipeline setup, Web Workers for non-blocking inference, model loading with progress tracking, and deployment patterns.

</details>

<br>

### `pretext`

DOM-free multiline text measurement and layout with [`@chenglou/pretext`](https://github.com/chenglou/pretext) — the two-phase prepare/layout API, font safety, i18n text handling, and integration patterns for React, canvas rendering, and streaming.

<details>
<summary>1 skill</summary>
<br>

Covers API selection (layout vs layoutWithLines vs layoutNextLine vs walkLineRanges), critical rules (font string safety, prepare-once pattern, locale config), and complete reference docs with working examples for React, canvas, virtual scrolling, and streaming layout.

</details>

<br>

### `heerich`

Build 3D voxel scenes rendered as crisp SVG using [heerich.js](https://github.com/meodai/heerich) — a zero-dependency engine for isometric and perspective voxel art. Named after sculptor Erwin Heerich.

<details>
<summary>1 command &ensp;·&ensp; 1 skill</summary>
<br>

| Command | What it does |
|---------|-------------|
| `/heerich:scene` | Generate a 3D voxel SVG scene from a text description — writes a Node.js script, runs it, outputs an SVG file |

<br>

| Skill | What it does |
|-------|-------------|
| `heerich-docs` | Full API reference — constructor, shape methods (box/sphere/line/where), boolean operations, camera projections, per-face styling, style functions, content voxels, serialization |

<br>

References cover the complete API, styling and cameras, and 9 ready-to-use recipes (buildings, terrain, characters, domes, boolean ops, animation frames, and more).

</details>

<br>

### `mapcn-toolkit`

Interactive map components for React with [mapcn](https://www.mapcn.dev/) — built on MapLibre GL, Tailwind CSS, and shadcn/ui. Free tiles, zero config, automatic dark mode.

<details>
<summary>3 commands &ensp;·&ensp; 1 skill</summary>
<br>

| Command | What it does |
|---------|-------------|
| `/mapcn-toolkit:add` | Install mapcn components or blocks into the current project |
| `/mapcn-toolkit:new` | Scaffold a new interactive map view or page |
| `/mapcn-toolkit:blocks` | Install and customize a pre-built map template |

<br>

| Skill | What it does |
|-------|-------------|
| `mapcn-docs` | Full component reference — Map, MapControls, MapMarker, MarkerContent, MarkerPopup, MarkerTooltip, MarkerLabel, MapPopup, MapRoute, MapClusterLayer, useMap hook, advanced usage (refs, events, custom GeoJSON layers), and 4 blocks (analytics-map, logistics-network, heatmap, delivery-tracker) |

</details>

<br>

### `wsl-chrome-patch`

Patches Claude Code to enable the `/chrome` command on WSL2 — fixes the "not supported in WSL" error and browser tool connectivity issues.

<details>
<summary>Details</summary>
<br>

Includes a patch script and an optional hook that checks patch status on session start. Proactively detects when a Claude Code update has overwritten the patch.

</details>

<br>

---

## Install

Add the marketplace:

```
/plugin marketplace add softee-p/claude-skills
```

Then install what you need:

```
/plugin install rwsdk-toolkit@mkw-claude-plugins
/plugin install practical-typography@mkw-claude-plugins
/plugin install transformersjs-docs@mkw-claude-plugins
/plugin install pretext@mkw-claude-plugins
/plugin install heerich@mkw-claude-plugins
/plugin install mapcn-toolkit@mkw-claude-plugins
/plugin install wsl-chrome-patch@mkw-claude-plugins
```

Update later:

```
/plugin marketplace update mkw-claude-plugins
```

<details>
<summary>Enable &amp; disable</summary>
<br>

```
/plugin disable practical-typography@mkw-claude-plugins
/plugin enable  practical-typography@mkw-claude-plugins
```

</details>

---

<br>

<p align="center">
  <sub>
    <strong>Acknowledgments</strong>
    <br>
    <a href="https://practicaltypography.com"><em>Practical Typography</em></a> by Matthew Butterick
    &ensp;·&ensp;
    <a href="https://rwsdk.com/">RedwoodSDK</a>
    &ensp;·&ensp;
    <a href="https://github.com/huggingface/transformers.js">Transformers.js</a> by Hugging Face
    &ensp;·&ensp;
    <a href="https://github.com/chenglou/pretext">Pretext</a> by chenglou
    &ensp;·&ensp;
    <a href="https://github.com/meodai/heerich">Heerich</a> by meodai
    &ensp;·&ensp;
    <a href="https://www.mapcn.dev/">mapcn</a> by Anmoldeep Singh
  </sub>
</p>

<p align="center">
  <sub>
    MIT — see <a href="LICENSE">LICENSE</a> for details.
    <br>
    <br>
    <em>This README was typeset with the help of the <strong>practical-typography</strong> plugin.</em>
  </sub>
</p>
