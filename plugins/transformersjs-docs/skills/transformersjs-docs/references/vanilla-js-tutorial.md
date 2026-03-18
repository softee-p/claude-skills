# Building a Vanilla JavaScript Application with Transformers.js

Build a web application that detects objects in images using Transformers.js with plain HTML, CSS, and JavaScript.

## How It Works

The user clicks "Upload image" and selects an image. After analysis with an object detection model, predicted bounding boxes are overlaid on the image.

## Prerequisites

- A code editor
- A browser
- A simple server (e.g., VS Code Live Server)

## Step 1: HTML and CSS Setup

Create `index.html` with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
  <title>Transformers.js Object Detection</title>
</head>
<body>
  <main class="container">
    <label for="file-upload" class="custom-file-upload">
      <input type="file" accept="image/*" id="file-upload">
      Upload image
    </label>
    <div id="image-container"></div>
    <p id="status"></p>
  </main>
</body>
</html>
```

**Markup breakdown:**

- `<input>` element with `type="file"` that accepts images - allows users to select an image from their file system
- The input is wrapped in a `<label>` so we can hide the input and style the label as a button
- Empty `<div id="image-container">` for displaying the image
- Empty `<p id="status">` for status updates during model download and inference

Create `style.css`:

```css
html, body {
    font-family: Arial, Helvetica, sans-serif;
}

.container {
    margin: 40px auto;
    width: max(50vw, 400px);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.custom-file-upload {
    display: flex;
    align-items: center;
    gap: 10px;
    border: 2px solid black;
    padding: 8px 16px;
    cursor: pointer;
    border-radius: 6px;
}

#file-upload {
    display: none;
}

.upload-icon {
    width: 30px;
}

#image-container {
    width: 100%;
    margin-top: 20px;
    position: relative;
}

#image-container>img {
    width: 100%;
}
```

## Step 2: JavaScript Setup

Add the script to `index.html` at the end of `<body>`:

```html
<script type="module" src="index.js"></script>
```

The `type="module"` attribute enables JavaScript modules with imports and exports.

Create `index.js` and import Transformers.js:

```js
import { pipeline, env } from "https://cdn.jsdelivr.net/npm/@huggingface/transformers";
```

Since downloading the model from the Hugging Face Hub, skip the local model check:

```js
env.allowLocalModels = false;
```

Create references to DOM elements:

```js
const fileUpload = document.getElementById("file-upload");
const imageContainer = document.getElementById("image-container");
const status = document.getElementById("status");
```

## Step 3: Create an Object Detection Pipeline

A pipeline is a high-level interface to perform a specific task. Create an object detection pipeline with the `pipeline()` helper function.

Update the status to inform the user:

```js
status.textContent = "Loading model...";
```

**Note:** For simplicity, this tutorial loads and runs the model on the main (UI) thread. This is not recommended for production - the UI will freeze during these operations. Use a Web Worker for production applications.

Create the pipeline:

```js
const detector = await pipeline("object-detection", "Xenova/detr-resnet-50");
```

Arguments to `pipeline()`:

1. **task**: `"object-detection"` - other tasks include `text-generation`, `sentiment-analysis`, `summarization`, `automatic-speech-recognition`
2. **model**: `Xenova/detr-resnet-50` - a ~40MB model for detecting objects in images

After the model loads:

```js
status.textContent = "Ready";
```

## Step 4: Create the Image Uploader

Listen for "change" events on the file input:

```js
fileUpload.addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();

  // Set up a callback when the file is loaded
  reader.onload = function (e2) {
    imageContainer.innerHTML = "";
    const image = document.createElement("img");
    image.src = e2.target.result;
    imageContainer.appendChild(image);
    // detect(image); // Uncomment this line to run the model
  };
  reader.readAsDataURL(file);
});
```

The `FileReader` loads the image, then `reader.onload` creates an `<img>` element and appends it to the container.

## Step 5: Run the Model

Uncomment `detect(image)` from the previous code, then define the function:

```js
async function detect(img) {
  status.textContent = "Analysing...";
  const output = await detector(img.src, {
    threshold: 0.5,
    percentage: true,
  });
  status.textContent = "";
  console.log("output", output);
  // ...
}
```

**Options explained:**

- `threshold: 0.5` - Model must be at least 50% confident to report a detection. Lower = more detections (possible misidentifications); higher = fewer detections (may miss objects)
- `percentage: true` - Return bounding boxes as percentages instead of pixels

**Example output** (for an image with two elephants):

```js
[
  {
    label: "elephant",
    score: 0.98,
    box: { xmin: 0.1, ymin: 0.2, xmax: 0.5, ymax: 0.8 }
  },
  {
    label: "elephant",
    score: 0.95,
    box: { xmin: 0.5, ymin: 0.25, xmax: 0.9, ymax: 0.75 }
  }
]
```

## Step 6: Render the Boxes

At the end of the `detect()` function, render boxes for each detection:

```js
output.forEach(renderBox);
```

The `renderBox` function:

```js
// Render a bounding box and label on the image
function renderBox({ box, label }) {
  const { xmax, xmin, ymax, ymin } = box;

  // Generate a random color for the box
  const color = "#" + Math.floor(Math.random() * 0xffffff).toString(16).padStart(6, 0);

  // Draw the box
  const boxElement = document.createElement("div");
  boxElement.className = "bounding-box";
  Object.assign(boxElement.style, {
    borderColor: color,
    left: 100 * xmin + "%",
    top: 100 * ymin + "%",
    width: 100 * (xmax - xmin) + "%",
    height: 100 * (ymax - ymin) + "%",
  });

  // Draw the label
  const labelElement = document.createElement("span");
  labelElement.textContent = label;
  labelElement.className = "bounding-box-label";
  labelElement.style.backgroundColor = color;

  boxElement.appendChild(labelElement);
  imageContainer.appendChild(boxElement);
}
```

Add styles for the bounding box and label in `style.css`:

```css
.bounding-box {
    position: absolute;
    box-sizing: border-box;
    border-width: 2px;
    border-style: solid;
}

.bounding-box-label {
    color: white;
    position: absolute;
    font-size: 12px;
    margin-top: -16px;
    margin-left: -2px;
    padding: 1px;
}
```

## Complete index.js

```js
import { pipeline, env } from "https://cdn.jsdelivr.net/npm/@huggingface/transformers";

env.allowLocalModels = false;

const fileUpload = document.getElementById("file-upload");
const imageContainer = document.getElementById("image-container");
const status = document.getElementById("status");

status.textContent = "Loading model...";
const detector = await pipeline("object-detection", "Xenova/detr-resnet-50");
status.textContent = "Ready";

fileUpload.addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();

  reader.onload = function (e2) {
    imageContainer.innerHTML = "";
    const image = document.createElement("img");
    image.src = e2.target.result;
    imageContainer.appendChild(image);
    detect(image);
  };
  reader.readAsDataURL(file);
});

async function detect(img) {
  status.textContent = "Analysing...";
  const output = await detector(img.src, {
    threshold: 0.5,
    percentage: true,
  });
  status.textContent = "";
  output.forEach(renderBox);
}

function renderBox({ box, label }) {
  const { xmax, xmin, ymax, ymin } = box;

  const color = "#" + Math.floor(Math.random() * 0xffffff).toString(16).padStart(6, 0);

  const boxElement = document.createElement("div");
  boxElement.className = "bounding-box";
  Object.assign(boxElement.style, {
    borderColor: color,
    left: 100 * xmin + "%",
    top: 100 * ymin + "%",
    width: 100 * (xmax - xmin) + "%",
    height: 100 * (ymax - ymin) + "%",
  });

  const labelElement = document.createElement("span");
  labelElement.textContent = label;
  labelElement.className = "bounding-box-label";
  labelElement.style.backgroundColor = color;

  boxElement.appendChild(labelElement);
  imageContainer.appendChild(boxElement);
}
```

The application runs entirely in the browser with no external server, APIs, or build tools required.
