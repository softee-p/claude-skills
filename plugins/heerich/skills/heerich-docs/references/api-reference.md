# Heerich API Reference

## Constructor

```javascript
import { Heerich } from 'heerich'

const h = new Heerich(options?)
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tile` | `[width, height]` | `[40, 40]` | Tile dimensions in pixels |
| `style` | StyleObject | `{fill:"#aaaaaa", stroke:"#000000", strokeWidth:1}` | Default face styling |
| `camera` | CameraOptions | `{type:'oblique', angle:45, distance:15}` | Camera configuration |

### Camera Options

**Oblique projection** (isometric-like):
```javascript
{ type: 'oblique', angle: 45, distance: 15 }
```

**Perspective projection** (vanishing point):
```javascript
{ type: 'perspective', position: [5, 5], distance: 10 }
```

---

## Shape Methods

All shape methods accept these common options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `'union'\|'subtract'\|'intersect'\|'exclude'` | `'union'` | Boolean operation mode |
| `style` | StyleParam | — | Per-face styles (object or function) |
| `content` | string | — | Raw SVG to render instead of polygon faces |
| `opaque` | boolean | `true` | Whether voxel occludes neighbors |
| `meta` | object | — | Emitted as `data-*` attributes on polygons |
| `rotate` | `{axis, turns, center?}` | — | Rotate coordinates before placement |

### addBox / removeBox

```javascript
h.addBox({
  position: [x, y, z],  // origin corner
  size: [w, h, d],       // dimensions
  style: { default: { fill: '#6699cc' }, top: { fill: '#88bbee' } }
})

h.removeBox({
  position: [1, 0, 1],
  size: [1, 2, 1]
})
```

### addSphere / removeSphere

```javascript
h.addSphere({
  center: [5, 5, 5],  // center point
  radius: 3,           // radius in voxels
  style: { default: { fill: 'gold' } }
})

h.removeSphere({ center: [5, 5, 5], radius: 1.5 })
```

### addLine / removeLine

```javascript
h.addLine({
  from: [0, 0, 0],
  to: [10, 5, 0],
  radius: 2,              // thickness (default: 0 = single voxel line)
  shape: 'rounded',       // 'rounded' (default) or 'square' cross-section
  style: { default: { fill: 'blue' } }
})

h.removeLine({ from: [3, 0, 0], to: [7, 0, 0] })
```

### addWhere / removeWhere

```javascript
// Add voxels where a test function returns true
h.addWhere({
  bounds: [[-6, -6, -6], [6, 6, 6]],  // search volume [min, max]
  test: (x, y, z) => {
    const d = x*x + y*y + z*z
    return d <= 25 && d >= 16  // hollow sphere shell
  },
  style: { default: { fill: '#cc6644' } }
})

// Remove voxels matching test
h.removeWhere({
  bounds: [[0, -6, -6], [6, 6, 6]],
  test: () => true  // remove entire half
})
```

---

## Styling Methods (In-Place)

Restyle existing voxels without adding or removing them.

```javascript
h.styleBox({
  position: [0, 0, 0],
  size: [3, 3, 3],
  style: { top: { fill: 'red' } }
})

h.styleSphere({
  center: [5, 5, 5],
  radius: 2,
  style: { default: { fill: 'gold' } }
})

h.styleLine({
  from: [0, 0, 0],
  to: [10, 0, 0],
  radius: 1,
  style: { default: { fill: 'blue' } }
})
```

---

## Rendering Methods

### toSVG(options?)

Renders the scene to an SVG string with hidden-face removal and depth sorting.

```javascript
const svg = h.toSVG()
const svg = h.toSVG({ padding: 40 })
const svg = h.toSVG({ viewBox: [0, 0, 800, 600] })
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `padding` | number | `20` | ViewBox padding in pixels |
| `faces` | Face[] | — | Pre-computed faces (skips internal rendering) |
| `viewBox` | `[x,y,w,h]` | auto | Custom viewBox override |
| `offset` | `[dx, dy]` | `[0, 0]` | Translate all geometry |
| `prepend` | string | — | Raw SVG inserted before face polygons |
| `append` | string | — | Raw SVG inserted after face polygons |
| `faceAttributes` | `(face) => object` | — | Per-face SVG attribute callback |

Generated polygons include data attributes:
```html
<polygon data-voxel="2,3,1" data-x="2" data-y="3" data-z="1" data-face="top" ... />
```

Voxels with `meta: { id: 'wall' }` also get `data-id="wall"`.

### getFaces()

Returns an array of projected 2D face objects. Results are cached until the scene is modified.

```javascript
const faces = h.getFaces()
// Each face: { type, voxel, points, depth, style }
```

### getFacesFrom(options)

Stateless face generation from a test function — no voxels stored in the map.

```javascript
const faces = h.getFacesFrom({
  bounds: [[-10, -10, -10], [10, 10, 10]],
  test: (x, y, z) => x*x + y*y + z*z <= 100,
  style: (x, y, z, faceName) => ({
    fill: faceName === 'top' ? '#fff' : '#ccc'
  })
})

const svg = h.toSVG({ faces })
```

Also accepts `regions` instead of `bounds` for multiple disjoint volumes:
```javascript
regions: [
  [[-5, -5, -5], [5, 5, 5]],
  [[10, 0, 0], [20, 10, 10]]
]
```

### getViewBoxBounds() / getOptimalViewBox(padding?, faces?)

```javascript
const { x, y, w, h } = h.getViewBoxBounds()
const [vbX, vbY, vbW, vbH] = h.getOptimalViewBox(30)
```

---

## Camera Control

```javascript
h.setCamera({ type: 'oblique', angle: 30, distance: 20 })
h.setCamera({ type: 'perspective', position: [10, 8], distance: 12 })
```

Calling `setCamera()` invalidates the face cache — next `toSVG()` or `getFaces()` re-renders.

---

## Scene Rotation

```javascript
h.rotate({ axis: 'y', turns: 1 })                    // 90 degrees around Y
h.rotate({ axis: 'x', turns: 2, center: [5, 5, 5] }) // 180 degrees around center
```

| Option | Type | Description |
|--------|------|-------------|
| `axis` | `'x'\|'y'\|'z'` | Rotation axis |
| `turns` | integer | Number of 90-degree increments |
| `center` | `[x,y,z]` | Optional rotation center (default: origin) |

Per-shape rotation (applied before placement):
```javascript
h.addBox({
  position: [0, 0, 0],
  size: [5, 1, 3],
  rotate: { axis: 'z', turns: 1 }
})
```

---

## Querying

```javascript
h.getVoxel([2, 3, 1])       // voxel data object or null
h.hasVoxel([2, 3, 1])       // boolean
h.getNeighbors([2, 3, 1])   // { top, bottom, left, right, front, back } (each voxel|null)
h.forEach((voxel, [x, y, z]) => { /* ... */ })
```

---

## Serialization

```javascript
const data = h.toJSON()
const json = JSON.stringify(data)

const restored = Heerich.fromJSON(JSON.parse(json))
```

**Note:** Functional styles (style functions) cannot be serialized and are omitted with a console warning.

---

## Boolean Operation Modes

| Mode | Description |
|------|-------------|
| `'union'` | Add voxels (default) |
| `'subtract'` | Remove overlapping voxels |
| `'intersect'` | Keep only voxels that overlap with existing |
| `'exclude'` | XOR — keep non-overlapping voxels from both |

```javascript
// Intersect: keep only where new shape overlaps existing
h.addBox({ position: [0,0,0], size: [5,5,5] })
h.addSphere({ center: [2,2,2], radius: 3, mode: 'intersect' })
// Result: rounded cube (only voxels in both box AND sphere)
```

---

## Coordinate System

- **x**: left/right
- **y**: up/down (increases downward in screen space)
- **z**: depth (front/back)
- **Range**: -512 to 511 on each axis (packed into 30-bit integer key)
