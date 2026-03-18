# Server-Side Inference in Node.js with Transformers.js

Build a Node.js API that uses Transformers.js for sentiment analysis. Covers both ECMAScript modules (ESM) and CommonJS.

## Why Use Transformers.js on the Server?

While the Python Transformers library is available for server-side inference, using Transformers.js means all code can be written in JavaScript without setting up a separate Python process.

## Module Systems

- **ECMAScript modules (ESM)**: The official standard format for JavaScript modules. Uses `import` and `export`. Stable in Node.js since version 13.2.0.
- **CommonJS**: The default module system in Node.js. Uses `require()` and `module.exports`.

## Prerequisites

- Node.js version 18+
- npm version 9+

## Getting Started

Create a new Node.js project and install Transformers.js:

```bash
npm init -y
npm i @huggingface/transformers
```

Create `app.js` as the entry point.

---

## ECMAScript Modules (ESM)

### Configure package.json

Add `"type": "module"` to `package.json`:

```json
{
  "type": "module"
}
```

### Imports

Add to the top of `app.js`:

```javascript
import http from 'http';
import querystring from 'querystring';
import url from 'url';
```

### Pipeline Singleton

Import Transformers.js and define the singleton class:

```javascript
import { pipeline, env } from '@huggingface/transformers';

class MyClassificationPipeline {
  static task = 'text-classification';
  static model = 'Xenova/distilbert-base-uncased-finetuned-sst-2-english';
  static instance = null;

  static async getInstance(progress_callback = null) {
    if (this.instance === null) {
      // NOTE: Uncomment this to change the cache directory
      // env.cacheDir = './.cache';

      this.instance = pipeline(this.task, this.model, { progress_callback });
    }

    return this.instance;
  }
}
```

---

## CommonJS

### Imports

Add to the top of `app.js`:

```javascript
const http = require('http');
const querystring = require('querystring');
const url = require('url');
```

### Pipeline Singleton

Since Transformers.js is an ESM module, dynamically import it using `import()`:

```javascript
class MyClassificationPipeline {
  static task = 'text-classification';
  static model = 'Xenova/distilbert-base-uncased-finetuned-sst-2-english';
  static instance = null;

  static async getInstance(progress_callback = null) {
    if (this.instance === null) {
      // Dynamically import the Transformers.js library
      let { pipeline, env } = await import('@huggingface/transformers');

      // NOTE: Uncomment this to change the cache directory
      // env.cacheDir = './.cache';

      this.instance = pipeline(this.task, this.model, { progress_callback });
    }

    return this.instance;
  }
}
```

---

## Creating the HTTP Server

This code works for both ESM and CommonJS:

```javascript
// Define the HTTP server
const server = http.createServer();
const hostname = '127.0.0.1';
const port = 3000;

// Listen for requests made to the server
server.on('request', async (req, res) => {
  // Parse the request URL
  const parsedUrl = url.parse(req.url);

  // Extract the query parameters
  const { text } = querystring.parse(parsedUrl.query);

  // Set the response headers
  res.setHeader('Content-Type', 'application/json');

  let response;
  if (parsedUrl.pathname === '/classify' && text) {
    const classifier = await MyClassificationPipeline.getInstance();
    response = await classifier(text);
    res.statusCode = 200;
  } else {
    response = { 'error': 'Bad request' }
    res.statusCode = 400;
  }

  // Send the JSON response
  res.end(JSON.stringify(response));
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

### Preload the Pipeline (Optional)

Since lazy loading is used, the first request loads the pipeline. To load it when the server starts instead:

```javascript
MyClassificationPipeline.getInstance();
```

Add this line after defining `MyClassificationPipeline`.

### Start the Server

```bash
node app.js
```

### Test the API

Visit `http://127.0.0.1:3000/` - shows:

```json
{"error":"Bad request"}
```

Visit `http://127.0.0.1:3000/classify?text=I%20love%20Transformers.js` - shows:

```json
[{"label":"POSITIVE","score":0.9996721148490906}]
```

---

## Customization Options

### Model Caching

By default, models are cached in `./node_modules/@huggingface/transformers/.cache/`. Change the location:

```javascript
env.cacheDir = './.cache';
```

### Use Local Models

Set a custom path for local model files:

```javascript
// Specify a custom location for models (defaults to '/models/').
env.localModelPath = '/path/to/models/';
```

Disable loading remote models:

```javascript
// Disable the loading of remote models from the Hugging Face Hub:
env.allowRemoteModels = false;
```

---

## Complete ESM Example

```javascript
import http from 'http';
import querystring from 'querystring';
import url from 'url';
import { pipeline, env } from '@huggingface/transformers';

class MyClassificationPipeline {
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

// Optional: Preload the pipeline
// MyClassificationPipeline.getInstance();

const server = http.createServer();
const hostname = '127.0.0.1';
const port = 3000;

server.on('request', async (req, res) => {
  const parsedUrl = url.parse(req.url);
  const { text } = querystring.parse(parsedUrl.query);

  res.setHeader('Content-Type', 'application/json');

  let response;
  if (parsedUrl.pathname === '/classify' && text) {
    const classifier = await MyClassificationPipeline.getInstance();
    response = await classifier(text);
    res.statusCode = 200;
  } else {
    response = { 'error': 'Bad request' }
    res.statusCode = 400;
  }

  res.end(JSON.stringify(response));
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

---

## Complete CommonJS Example

```javascript
const http = require('http');
const querystring = require('querystring');
const url = require('url');

class MyClassificationPipeline {
  static task = 'text-classification';
  static model = 'Xenova/distilbert-base-uncased-finetuned-sst-2-english';
  static instance = null;

  static async getInstance(progress_callback = null) {
    if (this.instance === null) {
      let { pipeline, env } = await import('@huggingface/transformers');
      this.instance = pipeline(this.task, this.model, { progress_callback });
    }
    return this.instance;
  }
}

// Optional: Preload the pipeline
// MyClassificationPipeline.getInstance();

const server = http.createServer();
const hostname = '127.0.0.1';
const port = 3000;

server.on('request', async (req, res) => {
  const parsedUrl = url.parse(req.url);
  const { text } = querystring.parse(parsedUrl.query);

  res.setHeader('Content-Type', 'application/json');

  let response;
  if (parsedUrl.pathname === '/classify' && text) {
    const classifier = await MyClassificationPipeline.getInstance();
    response = await classifier(text);
    res.statusCode = 200;
  } else {
    response = { 'error': 'Bad request' }
    res.statusCode = 400;
  }

  res.end(JSON.stringify(response));
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```
