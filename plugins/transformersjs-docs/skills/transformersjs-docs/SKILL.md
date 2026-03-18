---
name: transformersjs-docs
description: Guidance for building applications with Transformers.js, a library for running machine learning models (NLP, vision, audio) directly in the browser or Node.js. Use when implementing on-device ML inference with Transformers.js in React, Next.js, vanilla JavaScript, or Node.js applications. Covers pipeline setup, Web Workers for non-blocking inference, model loading with progress tracking, and deployment patterns.
---

# Transformers.js Documentation

## Workflow

**IMPORTANT: Always determine the user's framework first before proceeding.**

### Step 1: Identify the Framework

Detect the framework from the user's project or ask if unclear:

| Detection Method | Framework | Reference to Read |
|------------------|-----------|-------------------|
| `package.json` has `react` + `vite` | React (Vite) | `references/react-tutorial.md` |
| `package.json` has `next` | Next.js | `references/nextjs-tutorial.md` |
| `package.json` exists, no framework | Node.js | `references/nodejs-tutorial.md` |
| No `package.json`, HTML files only | Vanilla JS | `references/vanilla-js-tutorial.md` |
| User mentions React/Vite | React (Vite) | `references/react-tutorial.md` |
| User mentions Next.js | Next.js | `references/nextjs-tutorial.md` |
| User mentions Node/Express/server | Node.js | `references/nodejs-tutorial.md` |
| User mentions plain JS/HTML/no framework | Vanilla JS | `references/vanilla-js-tutorial.md` |

**If framework is unclear:** Ask the user which environment they're using before proceeding.

### Step 2: Read the Framework Reference

Once the framework is identified, read the corresponding reference file:

- **React (Vite)** → Read `references/react-tutorial.md`
  - Web Worker setup with Vite
  - React hooks for worker communication
  - Progress tracking with useState
  - Component-based UI patterns

- **Vanilla JavaScript** → Read `references/vanilla-js-tutorial.md`
  - CDN import (no build tools)
  - Direct DOM manipulation
  - Simple event-based architecture
  - No Web Worker (simpler but blocks UI)

- **Next.js** → Read `references/nextjs-tutorial.md`
  - Choose client-side OR server-side inference
  - Client: Web Worker + webpack config for browser
  - Server: Route Handlers + external packages config
  - App Router patterns

- **Node.js** → Read `references/nodejs-tutorial.md`
  - ESM vs CommonJS module syntax
  - HTTP server API pattern
  - Model caching configuration
  - No Web Workers (server context)

### Step 3: Apply Framework-Specific Patterns

Follow the patterns from the reference file. Key differences by framework:

| Aspect | React | Vanilla JS | Next.js Client | Next.js Server | Node.js |
|--------|-------|------------|----------------|----------------|---------|
| Install | npm | CDN | npm | npm | npm |
| Web Worker | Yes | No | Yes | No | No |
| Blocks UI | No | Yes | No | N/A | N/A |
| Config needed | No | No | webpack alias | external packages | ESM/CJS |

## Core Concepts (All Frameworks)

### Pipeline Pattern

```javascript
import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline('task-name', 'model-name', { progress_callback });
const result = await classifier(input);
```

Common tasks: `text-classification`, `translation`, `object-detection`, `sentiment-analysis`, `summarization`, `automatic-speech-recognition`

### Singleton Pattern

Reuse loaded models:

```javascript
class MyPipeline {
  static instance = null;

  static async getInstance(progress_callback = null) {
    if (this.instance === null) {
      this.instance = pipeline('task', 'model', { progress_callback });
    }
    return this.instance;
  }
}
```

### Environment Configuration

```javascript
import { env } from '@huggingface/transformers';

env.cacheDir = './.cache';           // Custom cache location
env.localModelPath = '/models/';     // Local model path
env.allowRemoteModels = false;       // Disable remote loading
env.allowLocalModels = false;        // Skip local check (browser)
```

## Reference Files

| File | When to Use |
|------|-------------|
| `references/react-tutorial.md` | React + Vite projects, SPAs |
| `references/vanilla-js-tutorial.md` | Plain HTML/JS, no build tools |
| `references/nextjs-tutorial.md` | Next.js App Router (client or server) |
| `references/nodejs-tutorial.md` | Node.js servers, REST APIs |
