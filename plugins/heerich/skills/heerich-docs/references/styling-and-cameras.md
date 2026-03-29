# Styling and Cameras

## Style Object Structure

Each face can have these SVG-mapped properties:

```javascript
{
  fill: '#aaaaaa',        // fill color
  stroke: '#000000',      // stroke color
  strokeWidth: 1,         // stroke width
  opacity: 1,             // overall opacity (0-1)
  fillOpacity: 1,         // fill opacity
  strokeOpacity: 1        // stroke opacity
}
```

**Default style** (when none specified): `{ fill: '#aaaaaa', stroke: '#000000', strokeWidth: 1 }`

## Per-Face Styling

Use face name keys to style individual faces. `default` applies to all faces unless a specific face key overrides it.

**Face names:** `default`, `top`, `bottom`, `left`, `right`, `front`, `back`

```javascript
h.addBox({
  position: [0, 0, 0],
  size: [5, 4, 5],
  style: {
    default: { fill: '#e8d4b8', stroke: '#333' },
    top:     { fill: '#c94c3a' },   // red roof
    front:   { fill: '#d4c4a8' },   // slightly different front
    right:   { fill: '#c8b898' }    // darker right side
  }
})
```

## Style Functions

Instead of static objects, pass a function `(x, y, z) => StyleObject` for dynamic per-voxel styling:

```javascript
// Height-based gradient
h.addBox({
  position: [0, 0, 0],
  size: [8, 12, 8],
  style: {
    default: (x, y, z) => ({
      fill: `hsl(${200 + y * 10}, 60%, ${40 + y * 3}%)`,
      stroke: '#222'
    }),
    top: (x, y, z) => ({
      fill: `hsl(${200 + y * 10}, 70%, ${50 + y * 3}%)`,
      stroke: '#222'
    })
  }
})
```

```javascript
// Checkerboard pattern
h.addBox({
  position: [0, 0, 0],
  size: [8, 1, 8],
  style: {
    top: (x, y, z) => ({
      fill: (x + z) % 2 === 0 ? '#fff' : '#333',
      stroke: '#666',
      strokeWidth: 0.5
    })
  }
})
```

```javascript
// Distance-based coloring
h.addSphere({
  center: [0, 0, 0],
  radius: 6,
  style: {
    default: (x, y, z) => {
      const d = Math.sqrt(x*x + y*y + z*z)
      return {
        fill: `hsl(${d * 30}, 70%, 55%)`,
        stroke: '#333',
        strokeWidth: 0.5
      }
    }
  }
})
```

### getFacesFrom Style Function

When using `getFacesFrom()`, the style function receives a fourth argument — the face name:

```javascript
const faces = h.getFacesFrom({
  bounds: [[-5, -5, -5], [5, 5, 5]],
  test: (x, y, z) => x*x + y*y + z*z <= 25,
  style: (x, y, z, faceName) => ({
    fill: faceName === 'top' ? '#88bbee' : '#6699cc',
    stroke: '#234'
  })
})
```

---

## Camera Types

### Oblique Projection

Classic isometric-like view. Good for pixel art, architectural diagrams, and game assets.

```javascript
h.setCamera({ type: 'oblique', angle: 45, distance: 15 })
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `angle` | `45` | Viewing angle in degrees. 45 = classic isometric. Lower = more top-down. Higher = more side-on. |
| `distance` | `15` | Controls the oblique projection slant. Higher = more top visible. |

**Common angle values:**
- `30` — more top-down, good for maps/terrain
- `45` — classic isometric, balanced view
- `60` — more frontal, good for building facades

### Perspective Projection

Vanishing-point depth. Good for dramatic views and realistic scenes.

```javascript
h.setCamera({ type: 'perspective', position: [5, 5], distance: 10 })
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `position` | `[5, 5]` | Camera position `[x, y]` — shifts the viewpoint |
| `distance` | `10` | Foreshortening intensity. Lower = more dramatic perspective. Higher = flatter. |

---

## Content Voxels

Embed arbitrary SVG at voxel positions. Content is depth-sorted with regular faces.

```javascript
h.addBox({
  position: [3, 5, 3],
  size: [1, 1, 1],
  content: '<text font-size="12" text-anchor="middle" fill="#333">A</text>',
  opaque: false  // don't occlude neighbors
})
```

CSS custom properties available inside content: `--x`, `--y`, `--z`, `--scale`, `--tile`.

```javascript
h.addBox({
  position: [0, 0, 0],
  size: [1, 1, 1],
  content: '<circle r="10" fill="red" opacity="0.8" />',
  opaque: false
})
```

---

## Data Attributes on SVG Polygons

Every rendered polygon includes data attributes for interactivity:

```html
<polygon
  data-voxel="2,3,1"
  data-x="2"
  data-y="3"
  data-z="1"
  data-face="top"
  points="..."
  style="fill:#88bbee;stroke:#234;stroke-width:1"
/>
```

Voxels created with `meta` get additional `data-*` attributes:
```javascript
h.addBox({
  position: [0, 0, 0],
  size: [3, 3, 3],
  meta: { id: 'wall', material: 'stone' }
})
// Produces: data-id="wall" data-material="stone"
```

---

## CSS Integration

Since heerich outputs standard SVG with data attributes, you can use CSS for styling and interactivity:

```css
/* Highlight face on hover */
polygon:hover {
  filter: brightness(1.2);
  cursor: pointer;
}

/* Style specific faces */
polygon[data-face="top"] {
  filter: brightness(1.1);
}

/* Target by metadata */
polygon[data-id="wall"]:hover {
  fill: #ff6666 !important;
}

/* Smooth transitions */
polygon {
  transition: filter 0.15s ease, fill 0.15s ease;
}
```

### Interactive Example (Browser)

```javascript
const svg = h.toSVG()
document.body.innerHTML = svg

document.querySelector('svg').addEventListener('click', (e) => {
  const poly = e.target.closest('polygon')
  if (!poly) return

  const x = poly.dataset.x
  const y = poly.dataset.y
  const z = poly.dataset.z
  const face = poly.dataset.face
  console.log(`Clicked voxel (${x},${y},${z}) face: ${face}`)
})
```

---

## faceAttributes Callback

For fine-grained control over rendered SVG attributes:

```javascript
const svg = h.toSVG({
  faceAttributes: (face) => ({
    'class': `face-${face.type}`,
    'data-depth': face.depth.toFixed(2)
  })
})
```
