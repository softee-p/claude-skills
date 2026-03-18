# Claude Skills

A curated marketplace of plugins for [Claude Code](https://claude.ai/claude-code) — each one independently installable, so you only load what you need.

## Plugins

| Plugin | What it does |
|--------|-------------|
| **rwsdk-toolkit** | Full-stack RedwoodSDK development — docs lookup, frontend debugging, shadcn/ui management, production auditing, and doc sync for React Server Components on Cloudflare Workers |
| **practical-typography** | Applies the key rules from Butterick's *Practical Typography* — proper punctuation, dashes, emphasis, spacing, and layout guidance for any reader-facing text |
| **transformersjs-docs** | Build with Transformers.js — run ML models for NLP, vision, and audio directly in the browser or Node.js, with patterns for React, Next.js, and vanilla JS |
| **wsl-chrome-patch** | Patches Claude Code to enable the `/chrome` command on WSL2 — fixes the "not supported in WSL" error and browser tool connectivity issues |

## Install

Add the marketplace, then install the plugins you want:

```
/plugin marketplace add softee-p/claude-skills
```

```
/plugin install rwsdk-toolkit@claude-skills
/plugin install practical-typography@claude-skills
/plugin install transformersjs-docs@claude-skills
/plugin install wsl-chrome-patch@claude-skills
```

To update all plugins later:

```
/plugin marketplace update claude-skills
```

## Manage

Disable a plugin without uninstalling it:

```
/plugin disable practical-typography@claude-skills
```

Re-enable it:

```
/plugin enable practical-typography@claude-skills
```

---

*This README was typeset with the help of the **practical-typography** plugin.*

## Acknowledgments

- **practical-typography** — based on [*Practical Typography*](https://practicaltypography.com) by Matthew Butterick
- **rwsdk-toolkit** — built around the official [RedwoodSDK](https://rwsdk.com/) documentation
- **transformersjs-docs** — based on [Transformers.js](https://github.com/huggingface/transformers.js) by Hugging Face

## License

MIT — see [LICENSE](LICENSE) for details.
