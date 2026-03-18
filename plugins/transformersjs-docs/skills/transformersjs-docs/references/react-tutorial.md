# Building a React Application with Transformers.js

Build a multilingual translation app using Transformers.js in React.

## Prerequisites

- Node.js version 18+
- npm version 9+

## Step 1: Initialize the Project

Use Vite to create a React project:

```bash
npm create vite@latest react-translator -- --template react
```

If prompted to install `create-vite`, type y and press Enter.

Enter the project directory and install dependencies:

```bash
cd react-translator
npm install
```

Test the application:

```bash
npm run dev
```

## Step 2: Install and Configure Transformers.js

Install Transformers.js from NPM:

```bash
npm install @huggingface/transformers
```

For this application, we use `Xenova/nllb-200-distilled-600M`, which performs multilingual translation among 200 languages. Key considerations:

1. ML inference is computationally intensive - run models in a separate thread from the main UI thread
2. The model is large (>1 GB) - only download when the user clicks "Translate"

Achieve both goals using a Web Worker and React hooks.

### Create the Worker File

Create `src/worker.js` - this handles loading and running the translation pipeline using the singleton pattern:

```javascript
import { pipeline, TextStreamer } from '@huggingface/transformers';

class MyTranslationPipeline {
  static task = 'translation';
  static model = 'Xenova/nllb-200-distilled-600M';
  static instance = null;

  static async getInstance(progress_callback = null) {
    this.instance ??= pipeline(this.task, this.model, { progress_callback });
    return this.instance;
  }
}
```

### Modify App.jsx

Set up the web worker reference using hooks:

```jsx
import { useEffect, useRef, useState } from 'react'
import './App.css'

function App() {
  // Create a reference to the worker object.
  const worker = useRef(null);

  // Set up the worker as soon as the App component is mounted.
  useEffect(() => {
    // Create the worker if it does not yet exist.
    worker.current ??= new Worker(new URL('./worker.js', import.meta.url), {
        type: 'module'
    });

    // Create a callback function for messages from the worker thread.
    const onMessageReceived = (e) => {
      // TODO: Will fill in later
    };

    // Attach the callback function as an event listener.
    worker.current.addEventListener('message', onMessageReceived);

    // Define a cleanup function for when the component is unmounted.
    return () => worker.current.removeEventListener('message', onMessageReceived);
  });

  return (
    // TODO: Rest of our app goes here...
  )
}

export default App
```

## Step 3: Design the User Interface

Create a `components` folder in `src` with these files:

### LanguageSelector.jsx

```jsx
const LANGUAGES = {
  "Acehnese (Arabic script)": "ace_Arab",
  "Acehnese (Latin script)": "ace_Latn",
  "Afrikaans": "afr_Latn",
  // ... full list of 200+ languages
  "Zulu": "zul_Latn",
}

export default function LanguageSelector({ type, onChange, defaultLanguage }) {
  return (
    <div className="language-selector">
      <label>{type}: </label>
      <select onChange={onChange} defaultValue={defaultLanguage}>
        {Object.entries(LANGUAGES).map(([key, value]) => {
          return <option key={value} value={value}>{key}</option>
        })}
      </select>
    </div>
  )
}
```

### Progress.jsx

```jsx
export default function Progress({ text, percentage }) {
  percentage = percentage ?? 0;
  return (
    <div className="progress-container">
      <div className="progress-bar" style={{ width: `${percentage}%` }}>
        <span className="progress-text">{text} ({`${percentage.toFixed(2)}%`})</span>
      </div>
    </div>
  );
}
```

### Update App.jsx with Components

Import and use the components:

```jsx
import LanguageSelector from './components/LanguageSelector';
import Progress from './components/Progress';
```

Add state variables at the beginning of the App function:

```jsx
function App() {
  // Model loading
  const [ready, setReady] = useState(null);
  const [disabled, setDisabled] = useState(false);
  const [progressItems, setProgressItems] = useState([]);

  // Inputs and outputs
  const [input, setInput] = useState('I love walking my dog.');
  const [sourceLanguage, setSourceLanguage] = useState('eng_Latn');
  const [targetLanguage, setTargetLanguage] = useState('fra_Latn');
  const [output, setOutput] = useState('');

  // rest of the code...
}
```

The return statement:

```jsx
return (
  <>
    <h1>Transformers.js</h1>
    <h2>ML-powered multilingual translation in React!</h2>

    <div className="container">
      <div className="language-container">
        <LanguageSelector type="Source" defaultLanguage="eng_Latn" onChange={x => setSourceLanguage(x.target.value)} />
        <LanguageSelector type="Target" defaultLanguage="fra_Latn" onChange={x => setTargetLanguage(x.target.value)} />
      </div>

      <div className="textbox-container">
        <textarea value={input} rows={3} onChange={e => setInput(e.target.value)} />
        <textarea value={output} rows={3} readOnly />
      </div>
    </div>

    <button disabled={disabled} onClick={translate}>Translate</button>

    <div className="progress-bars-container">
      {ready === false && (
        <label>Loading models... (only run once)</label>
      )}
      {progressItems.map(data => (
        <div key={data.file}>
          <Progress text={data.file} percentage={data.progress} />
        </div>
      ))}
    </div>
  </>
)
```

### CSS Styles

**index.css:**

```css
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  color: #213547;
  background-color: #ffffff;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1;
}

h1, h2 {
  margin: 8px;
}

select {
  padding: 0.3em;
  cursor: pointer;
}

textarea {
  padding: 0.6em;
}

button {
  padding: 0.6em 1.2em;
  cursor: pointer;
  font-weight: 500;
}

button[disabled] {
  cursor: not-allowed;
}

select, textarea, button {
  border-radius: 8px;
  border: 1px solid transparent;
  font-size: 1em;
  font-family: inherit;
  background-color: #f9f9f9;
  transition: border-color 0.25s;
}

select:hover, textarea:hover, button:not([disabled]):hover {
  border-color: #646cff;
}

select:focus, select:focus-visible,
textarea:focus, textarea:focus-visible,
button:focus, button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}
```

**App.css:**

```css
#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.language-container {
  display: flex;
  gap: 20px;
}

.textbox-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  width: 800px;
}

.textbox-container>textarea, .language-selector {
  width: 50%;
}

.language-selector>select {
  width: 150px;
}

.progress-container {
  position: relative;
  font-size: 14px;
  color: white;
  background-color: #e9ecef;
  border: solid 1px;
  border-radius: 8px;
  text-align: left;
  overflow: hidden;
}

.progress-bar {
  padding: 0 4px;
  z-index: 0;
  top: 0;
  width: 1%;
  overflow: hidden;
  background-color: #007bff;
  white-space: nowrap;
}

.progress-text {
  z-index: 2;
}

.selector-container {
  display: flex;
  gap: 20px;
}

.progress-bars-container {
  padding: 8px;
  height: 140px;
}

.container {
  margin: 25px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
```

## Step 4: Connect Everything Together

### Define the translate Function

Add before the return statement in App:

```jsx
const translate = () => {
  setDisabled(true);
  setOutput('');
  worker.current.postMessage({
    text: input,
    src_lang: sourceLanguage,
    tgt_lang: targetLanguage,
  });
}
```

### Complete the Worker (src/worker.js)

Add the message listener:

```javascript
// Listen for messages from the main thread
self.addEventListener('message', async (event) => {
  // Retrieve the translation pipeline. When called for the first time,
  // this will load the pipeline and save it for future use.
  const translator = await MyTranslationPipeline.getInstance(x => {
      // Add a progress callback to track model loading.
      self.postMessage(x);
  });

  // Capture partial output as it streams from the pipeline
  const streamer = new TextStreamer(translator.tokenizer, {
      skip_prompt: true,
      skip_special_tokens: true,
      callback_function: function (text) {
          self.postMessage({
              status: 'update',
              output: text
          });
      }
  });

  // Perform the translation
  const output = await translator(event.data.text, {
      tgt_lang: event.data.tgt_lang,
      src_lang: event.data.src_lang,
      streamer,
  });

  // Send the output back to the main thread
  self.postMessage({
      status: 'complete',
      output,
  });
});
```

### Complete the onMessageReceived Function

Fill in the callback in App.jsx inside useEffect:

```jsx
const onMessageReceived = (e) => {
  switch (e.data.status) {
    case 'initiate':
      // Model file start load: add a new progress item to the list.
      setReady(false);
      setProgressItems(prev => [...prev, e.data]);
      break;

    case 'progress':
      // Model file progress: update one of the progress items.
      setProgressItems(
        prev => prev.map(item => {
          if (item.file === e.data.file) {
            return { ...item, progress: e.data.progress }
          }
          return item;
        })
      );
      break;

    case 'done':
      // Model file loaded: remove the progress item from the list.
      setProgressItems(
        prev => prev.filter(item => item.file !== e.data.file)
      );
      break;

    case 'ready':
      // Pipeline ready: the worker is ready to accept messages.
      setReady(true);
      break;

    case 'update':
      // Generation update: update the output text.
      setOutput(o => o + e.data.output);
      break;

    case 'complete':
      // Generation complete: re-enable the "Translate" button
      setDisabled(false);
      break;
  }
};
```

Run the application with `npm run dev`.

## Step 5: Build and Deploy

Build the application:

```bash
npm run build
```

This bundles the application and outputs static files to the `dist` folder.

To deploy as a static Hugging Face Space:

1. Create a new Space at huggingface.co/new-space and select "Static" as the space type
2. Go to "Files" > "Add file" > "Upload files"
3. Drag the `index.html` file and `public/` folder from `dist` into the upload box
4. Click "Commit changes to main"

The application will be live at `https://huggingface.co/spaces/<your-username>/<space-name>`.
