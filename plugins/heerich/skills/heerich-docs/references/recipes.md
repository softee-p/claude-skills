# Heerich Recipes

Complete examples that can be adapted for common use cases.

## Node.js Script Template

The standard pattern for generating an SVG file from Node.js:

```javascript
import { Heerich } from 'heerich'
import { writeFileSync } from 'node:fs'

const h = new Heerich({
  tile: [40, 40],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

// ... build your scene here ...

writeFileSync('scene.svg', h.toSVG())
console.log('Wrote scene.svg')
```

Save as `.mjs` to use ESM imports without `"type": "module"` in package.json.

---

## Building with Door and Windows

```javascript
const h = new Heerich({
  tile: [30, 30],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

// Walls
h.addBox({
  position: [0, 0, 0],
  size: [8, 6, 6],
  style: {
    default: { fill: '#e8d4b8', stroke: '#333', strokeWidth: 0.5 },
    top: { fill: '#c94c3a', stroke: '#333' }  // red roof
  }
})

// Door (front face, centered)
h.removeBox({ position: [3, 0, 0], size: [2, 3, 1] })

// Windows (front face, left and right)
h.removeBox({ position: [1, 3, 0], size: [1, 1, 1] })
h.removeBox({ position: [6, 3, 0], size: [1, 1, 1] })

// Windows (right face)
h.removeBox({ position: [8, 3, 2], size: [1, 1, 1] })
h.removeBox({ position: [8, 3, 4], size: [1, 1, 1] })

writeFileSync('building.svg', h.toSVG())
```

---

## Terrain / Landscape

Using `addWhere` with a height function for rolling hills:

```javascript
const h = new Heerich({
  tile: [20, 20],
  camera: { type: 'oblique', angle: 40, distance: 15 }
})

h.addWhere({
  bounds: [[-15, 0, -15], [15, 10, 15]],
  test: (x, y, z) => {
    // Sine-wave terrain height
    const height = Math.floor(
      3 + 2 * Math.sin(x * 0.3) + 2 * Math.cos(z * 0.25)
    )
    return y <= height
  },
  style: {
    top: (x, y, z) => ({
      fill: y > 4 ? '#8fbc8f' : '#6b8e23',  // lighter green on peaks
      stroke: '#2e4e2e',
      strokeWidth: 0.3
    }),
    default: (x, y, z) => ({
      fill: y > 2 ? '#8b7355' : '#6b5b3a',  // dirt layers
      stroke: '#3e3222',
      strokeWidth: 0.3
    })
  }
})

writeFileSync('terrain.svg', h.toSVG())
```

---

## Voxel Character

Manual voxel placement for a small figure:

```javascript
const h = new Heerich({
  tile: [40, 40],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

const skin = { default: { fill: '#ffcc99', stroke: '#333' } }
const shirt = { default: { fill: '#4488cc', stroke: '#333' } }
const pants = { default: { fill: '#334455', stroke: '#333' } }
const hair = { default: { fill: '#553311', stroke: '#333' } }
const shoes = { default: { fill: '#222', stroke: '#333' } }

// Feet
h.addBox({ position: [0, 0, 1], size: [1, 1, 1], style: shoes })
h.addBox({ position: [2, 0, 1], size: [1, 1, 1], style: shoes })

// Legs
h.addBox({ position: [0, 1, 1], size: [1, 2, 1], style: pants })
h.addBox({ position: [2, 1, 1], size: [1, 2, 1], style: pants })

// Torso
h.addBox({ position: [0, 3, 1], size: [3, 3, 1], style: shirt })

// Arms
h.addBox({ position: [-1, 3, 1], size: [1, 3, 1], style: shirt })
h.addBox({ position: [3, 3, 1], size: [1, 3, 1], style: shirt })

// Hands
h.addBox({ position: [-1, 3, 1], size: [1, 1, 1], style: skin })
h.addBox({ position: [3, 3, 1], size: [1, 1, 1], style: skin })

// Head
h.addBox({ position: [0, 6, 0], size: [3, 3, 3], style: skin })

// Hair
h.addBox({ position: [0, 8, 0], size: [3, 1, 3], style: hair })

writeFileSync('character.svg', h.toSVG())
```

---

## Hollow Structure (Room)

```javascript
const h = new Heerich({
  tile: [25, 25],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

// Outer shell
h.addBox({
  position: [0, 0, 0],
  size: [10, 8, 10],
  style: { default: { fill: '#b8b8b8', stroke: '#555' } }
})

// Hollow interior (leave 1-voxel walls)
h.removeBox({ position: [1, 1, 1], size: [8, 6, 8] })

// Cut away front wall to reveal interior
h.removeBox({ position: [1, 1, 0], size: [8, 6, 1] })

// Door in back wall
h.removeBox({ position: [4, 0, 9], size: [2, 4, 1] })

writeFileSync('room.svg', h.toSVG())
```

---

## Sphere Operations (Dome)

```javascript
const h = new Heerich({
  tile: [25, 25],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

// Base platform
h.addBox({
  position: [-7, -1, -7],
  size: [14, 1, 14],
  style: { default: { fill: '#888', stroke: '#444' } }
})

// Solid dome (upper hemisphere)
h.addSphere({
  center: [0, 0, 0],
  radius: 6,
  style: {
    default: { fill: '#d4a574', stroke: '#8b6914' },
    top: { fill: '#e8c49a', stroke: '#8b6914' }
  }
})

// Remove bottom half to make a dome
h.removeBox({ position: [-7, -7, -7], size: [14, 7, 14] })

// Hollow interior
h.removeSphere({ center: [0, 0, 0], radius: 5 })

// Entrance
h.removeBox({ position: [-1, 0, -7], size: [3, 3, 3] })

writeFileSync('dome.svg', h.toSVG())
```

---

## Boolean Intersect (Rounded Cube)

```javascript
const h = new Heerich({
  tile: [30, 30],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

// Start with a box
h.addBox({
  position: [-4, -4, -4],
  size: [8, 8, 8],
  style: { default: { fill: '#6699cc', stroke: '#234' }, top: { fill: '#88bbee' } }
})

// Intersect with sphere to round the corners
h.addSphere({
  center: [0, 0, 0],
  radius: 5,
  mode: 'intersect'
})

writeFileSync('rounded-cube.svg', h.toSVG())
```

---

## Perspective View

```javascript
const h = new Heerich({
  tile: [30, 30],
  camera: { type: 'perspective', position: [8, 6], distance: 12 }
})

// Row of columns
for (let i = 0; i < 5; i++) {
  h.addBox({
    position: [i * 3, 0, 0],
    size: [1, 6, 1],
    style: {
      default: (x, y) => ({
        fill: `hsl(0, 0%, ${60 + y * 4}%)`,
        stroke: '#444'
      })
    }
  })
}

// Lintel across the top
h.addBox({
  position: [0, 6, 0],
  size: [13, 1, 1],
  style: { default: { fill: '#c8b898', stroke: '#444' } }
})

writeFileSync('columns.svg', h.toSVG())
```

---

## Multi-Object Composition

Build distinct objects separately and combine:

```javascript
const h = new Heerich({
  tile: [20, 20],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

// Ground
h.addBox({
  position: [-10, -1, -10],
  size: [20, 1, 20],
  style: { top: { fill: '#7cba5c', stroke: '#4a7a3a', strokeWidth: 0.3 } }
})

// House
h.addBox({
  position: [0, 0, 0],
  size: [5, 4, 4],
  style: { default: { fill: '#e8d4b8', stroke: '#555' }, top: { fill: '#c94c3a' } }
})
h.removeBox({ position: [2, 0, 0], size: [1, 2, 1] }) // door

// Tree (trunk + foliage)
h.addBox({
  position: [-5, 0, 2],
  size: [1, 3, 1],
  style: { default: { fill: '#8b5e3c', stroke: '#444' } }
})
h.addSphere({
  center: [-5, 5, 2],
  radius: 2,
  style: { default: { fill: '#3a7a3a', stroke: '#2a5a2a' } }
})

// Fence
for (let i = -3; i <= 6; i++) {
  h.addBox({
    position: [i, 0, -2],
    size: [1, 2, 1],
    style: { default: { fill: '#c8a87a', stroke: '#555', strokeWidth: 0.3 } }
  })
}

writeFileSync('scene.svg', h.toSVG())
```

---

## Browser Integration

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background: #1a1a2e; }
    svg polygon { transition: filter 0.15s ease; }
    svg polygon:hover { filter: brightness(1.3); cursor: pointer; }
  </style>
</head>
<body>
  <div id="scene"></div>
  <script type="module">
    import { Heerich } from 'heerich'

    const h = new Heerich({
      tile: [30, 30],
      camera: { type: 'oblique', angle: 45, distance: 15 }
    })

    // Build scene...
    h.addBox({
      position: [0, 0, 0],
      size: [5, 5, 5],
      style: {
        default: (x, y, z) => ({
          fill: `hsl(${(x + y + z) * 30}, 70%, 55%)`,
          stroke: '#333'
        })
      }
    })

    document.getElementById('scene').innerHTML = h.toSVG()
  </script>
</body>
</html>
```

---

## Animated Sequence (Multiple SVG Frames)

Generate rotated views for animation:

```javascript
import { Heerich } from 'heerich'
import { writeFileSync } from 'node:fs'

const h = new Heerich({
  tile: [30, 30],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

h.addBox({
  position: [-2, -2, -2],
  size: [4, 4, 4],
  style: {
    default: (x, y, z) => ({
      fill: `hsl(${(x + z) * 40 + 180}, 60%, 55%)`,
      stroke: '#333'
    })
  }
})

// Export 4 rotation frames
for (let i = 0; i < 4; i++) {
  writeFileSync(`frame-${i}.svg`, h.toSVG())
  h.rotate({ axis: 'y', turns: 1 })
}

console.log('Wrote frame-0.svg through frame-3.svg')
```
