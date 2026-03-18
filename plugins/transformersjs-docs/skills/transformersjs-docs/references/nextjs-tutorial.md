# Building a Next.js Application with Transformers.js

Build a Next.js application that performs sentiment analysis using Transformers.js. Since Transformers.js can run in the browser or in Node.js, choose between client-side or server-side inference. Both approaches use the App Router.

## Prerequisites

- Node.js version 18+
- npm version 9+

---

## Client-Side Inference

### Step 1: Initialize the Project

Create a new Next.js application:

```bash
npx create-next-app@latest
```

Recommended selections for this tutorial:

- Project name: `next`
- TypeScript: No
- ESLint: Yes
- Tailwind CSS: No
- `src/` directory: Yes
- App Router: **Yes**
- Customize import alias: No

### Step 2: Install and Configure Transformers.js

Install from NPM:

```bash
npm i @huggingface/transformers
```

Update `next.config.js` to ignore node-specific modules when bundling for the browser:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
    // (Optional) Export as a static site
    output: 'export', // Feel free to modify/remove this option

    // Override the default webpack configuration
    webpack: (config) => {
        config.resolve.alias = {
            ...config.resolve.alias,
            "sharp$": false,
            "onnxruntime-node$": false,
        }
        return config;
    },
}

module.exports = nextConfig
```

### Create the Worker

Create a Web Worker for ML code to prevent blocking the main thread. Using `Xenova/distilbert-base-uncased-finetuned-sst-2-english`, a ~67M parameter sentiment analysis model.

Create `./src/app/worker.js`:

```js
import { pipeline, env } from "@huggingface/transformers";

// Skip local model check
env.allowLocalModels = false;

// Use the Singleton pattern to enable lazy construction of the pipeline.
class PipelineSingleton {
    static task = 'text-classification';
    static model = 'Xenova/distilbert-base-uncased-finetuned-sst-2-english';
    static instance = null;

    static async getInstance(progress_callback = null) {
        if (this.instance === null) {
            this.instance = pipeline(this.task, this.model, { progress_callback });
        }
        return this.instance;
    }
}

// Listen for messages from the main thread
self.addEventListener('message', async (event) => {
    // Retrieve the classification pipeline. When called for the first time,
    // this will load the pipeline and save it for future use.
    let classifier = await PipelineSingleton.getInstance(x => {
        // Track model loading progress.
        self.postMessage(x);
    });

    // Perform the classification
    let output = await classifier(event.data.text);

    // Send the output back to the main thread
    self.postMessage({
        status: 'complete',
        output: output,
    });
});
```

### Step 3: Design the User Interface

Modify `./src/app/page.js` to connect to the worker. Use the `'use client'` directive for client-side rendering:

```jsx
'use client'

import { useState, useEffect, useRef, useCallback } from 'react'

export default function Home() {
  // Keep track of the classification result and the model loading status.
  const [result, setResult] = useState(null);
  const [ready, setReady] = useState(null);

  // Create a reference to the worker object.
  const worker = useRef(null);

  // Set up the worker as soon as the App component is mounted.
  useEffect(() => {
    if (!worker.current) {
      // Create the worker if it does not yet exist.
      worker.current = new Worker(new URL('./worker.js', import.meta.url), {
        type: 'module'
      });
    }

    // Create a callback function for messages from the worker thread.
    const onMessageReceived = (e) => {
      switch (e.data.status) {
        case 'initiate':
          setReady(false);
          break;
        case 'ready':
          setReady(true);
          break;
        case 'complete':
          setResult(e.data.output[0])
          break;
      }
    };

    // Attach the callback function as an event listener.
    worker.current.addEventListener('message', onMessageReceived);

    // Define a cleanup function for when the component is unmounted.
    return () => worker.current.removeEventListener('message', onMessageReceived);
  });

  const classify = useCallback((text) => {
    if (worker.current) {
      worker.current.postMessage({ text });
    }
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-12">
      <h1 className="text-5xl font-bold mb-2 text-center">Transformers.js</h1>
      <h2 className="text-2xl mb-4 text-center">Next.js template</h2>

      <input
        className="w-full max-w-xs p-2 border border-gray-300 rounded mb-4"
        type="text"
        placeholder="Enter text here"
        onInput={e => {
          classify(e.target.value);
        }}
      />

      {ready !== null && (
        <pre className="bg-gray-100 p-2 rounded">
          {(!ready || !result) ? 'Loading...' : JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  )
}
```

Run the application:

```bash
npm run dev
```

### Step 4: Build and Deploy (Optional)

Build the application:

```bash
npm run build
```

Static files output to the `out` folder.

To deploy as a static Hugging Face Space:

1. Create a new Space and select "Static" as the space type
2. Go to "Files" > "Add file" > "Upload files"
3. Drag files from the `out` folder and commit

---

## Server-Side Inference

Use Route Handlers for server-side inference.

### Step 1: Initialize the Project

Create a new Next.js application:

```bash
npx create-next-app@latest
```

Same selections as client-side, but:

- TypeScript: No
- Tailwind CSS: No

### Step 2: Install and Configure Transformers.js

Install from NPM:

```bash
npm i @huggingface/transformers
```

Update `next.config.js` to prevent Webpack from bundling certain packages:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
    // (Optional) Export as a standalone site
    output: 'standalone', // Feel free to modify/remove this option

    // Indicate that these packages should not be bundled by webpack
    experimental: {
        serverComponentsExternalPackages: ['sharp', 'onnxruntime-node'],
    },
};

module.exports = nextConfig
```

### Create the Route Handler

Create two files in a new `./src/app/classify/` directory:

**pipeline.js** - Handles pipeline construction:

```js
import { pipeline } from "@huggingface/transformers";

// Use the Singleton pattern to enable lazy construction of the pipeline.
// NOTE: We wrap the class in a function to prevent code duplication (see below).
const P = () => class PipelineSingleton {
    static task = 'text-classification';
    static model = 'Xenova/distilbert-base-uncased-finetuned-sst-2-english';
    static instance = null;

    static async getInstance(progress_callback = null) {
        if (this.instance === null) {
            this.instance = pipeline(this.task, this.model, { progress_callback });
        }
        return this.instance;
    }
}

let PipelineSingleton;
if (process.env.NODE_ENV !== 'production') {
    // When running in development mode, attach the pipeline to the
    // global object so that it's preserved between hot reloads.
    if (!global.PipelineSingleton) {
        global.PipelineSingleton = P();
    }
    PipelineSingleton = global.PipelineSingleton;
} else {
    PipelineSingleton = P();
}
export default PipelineSingleton;
```

**route.js** - Processes requests to `/classify`:

```js
import { NextResponse } from 'next/server'
import PipelineSingleton from './pipeline.js';

export async function GET(request) {
    const text = request.nextUrl.searchParams.get('text');
    if (!text) {
        return NextResponse.json({
            error: 'Missing text parameter',
        }, { status: 400 });
    }
    // Get the classification pipeline. When called for the first time,
    // this will load the pipeline and cache it for future use.
    const classifier = await PipelineSingleton.getInstance();

    // Perform the classification
    const result = await classifier(text);

    return NextResponse.json(result);
}
```

### Step 3: Design the User Interface

Modify `./src/app/page.js` to make requests to the Route Handler:

```jsx
'use client'

import { useState } from 'react'

export default function Home() {
  // Keep track of the classification result and the model loading status.
  const [result, setResult] = useState(null);
  const [ready, setReady] = useState(null);

  const classify = async (text) => {
    if (!text) return;
    if (ready === null) setReady(false);

    // Make a request to the /classify route on the server.
    const result = await fetch(`/classify?text=${encodeURIComponent(text)}`);

    // If this is the first time we've made a request, set the ready flag.
    if (!ready) setReady(true);

    const json = await result.json();
    setResult(json);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-12">
      <h1 className="text-5xl font-bold mb-2 text-center">Transformers.js</h1>
      <h2 className="text-2xl mb-4 text-center">Next.js template (server-side)</h2>
      <input
        className="w-full max-w-xs p-2 border border-gray-300 rounded mb-4"
        type="text"
        placeholder="Enter text here"
        onInput={e => {
          classify(e.target.value);
        }}
      />

      {ready !== null && (
        <pre className="bg-gray-100 p-2 rounded">
          {(!ready || !result) ? 'Loading...' : JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  )
}
```

Run the application:

```bash
npm run dev
```

### Step 4: Build and Deploy (Optional)

For Docker deployment to Hugging Face Spaces:

1. Create a `Dockerfile` in the project root
2. Create a new Space and select "Docker" as the space type (use "Blank" template)
3. Upload project files (excluding `node_modules` and `.next`)
4. Add to the top of `README.md`:

```yaml
---
title: Next Server Example App
emoji: fire
colorFrom: yellow
colorTo: red
sdk: docker
pinned: false
app_port: 3000
---
```

---

## Key Differences: Client vs Server

| Aspect | Client-Side | Server-Side |
|--------|-------------|-------------|
| Where inference runs | Browser (Web Worker) | Node.js server |
| Webpack config | Alias sharp/onnxruntime-node to false | External packages |
| Output type | Static (`output: 'export'`) | Standalone (`output: 'standalone'`) |
| Communication | postMessage to worker | HTTP fetch to Route Handler |
| Deployment | Static hosting | Docker/Node.js server |
