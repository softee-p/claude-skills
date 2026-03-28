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

Full-stack RedwoodSDK development — docs lookup, frontend debugging, shadcn/ui management, production auditing, and doc sync for React Server Components on Cloudflare Workers.

<details>
<summary>6 commands &ensp;·&ensp; 5 skills</summary>
<br>

| Commands | Skills |
|----------|--------|
| `/audit` | rwsdk-docs |
| `/components` | rwsdk-frontend |
| `/docs` | rwsdk-shadcn-update |
| `/fix` | rwsdk-audit-deployed |
| `/new` | update-rwsdk-docs |
| `/sync` | |

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
