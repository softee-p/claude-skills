---
name: heerich-docs
description: Guidance for building 3D voxel scenes rendered as SVG using heerich.js. Use when writing code with heerich, creating voxel art, generating isometric or perspective 3D graphics as SVG, using addBox/addSphere/addLine/addWhere/removeBox/removeSphere/toSVG, building architectural models or game assets in voxels, or working with oblique/perspective camera projections for SVG output.
---

# Heerich.js — 3D Voxel SVG Engine

Zero-dependency JavaScript library that builds 3D scenes from voxels (1x1x1 cubes on an integer grid) and renders them as crisp SVG with hidden-face removal and depth sorting.

**npm:** `heerich` | **Import:** `import { Heerich } from 'heerich'`

## Quick Start

```javascript
import { Heerich } from 'heerich'

const h = new Heerich({
  tile: [40, 40],
  camera: { type: 'oblique', angle: 45, distance: 15 }
})

h.addBox({
  position: [0, 0, 0],
  size: [5, 4, 5],
  style: {
    default: { fill: '#e8d4b8', stroke: '#333' },
    top: { fill: '#c94c3a' }
  }
})

h.removeBox({ position: [2, 0, 0], size: [1, 3, 1] }) // carve a door

const svg = h.toSVG()
```

## When to Read References

| Topic | Reference |
|-------|-----------|
| Constructor options, shape methods, output methods, querying, serialization | `${CLAUDE_PLUGIN_ROOT}/skills/heerich-docs/references/api-reference.md` |
| Camera types, face styling, style functions, content voxels, data attributes, CSS integration | `${CLAUDE_PLUGIN_ROOT}/skills/heerich-docs/references/styling-and-cameras.md` |
| Complete examples: buildings, terrain, characters, hollow structures, Node.js script template | `${CLAUDE_PLUGIN_ROOT}/skills/heerich-docs/references/recipes.md` |

**Always read `api-reference.md` first** when writing heerich code. Add `styling-and-cameras.md` when visual design matters. Use `recipes.md` for complete starting patterns.

## Core Concepts

- **Coordinate system:** x (left/right), y (up/down), z (depth). Range: -512 to 511 per axis.
- **Voxel:** a 1x1x1 cube at integer coordinates. Stored in a Map keyed by packed integer.
- **CSG model:** shapes are additive/subtractive. Later operations modify earlier ones. Order matters.
- **Hidden-face removal:** `toSVG()` and `getFaces()` automatically cull occluded faces and depth-sort.
- **Style object:** `{ fill, stroke, strokeWidth, opacity, fillOpacity, strokeOpacity }` per face.
- **Face names:** `default`, `top`, `bottom`, `left`, `right`, `front`, `back`. `default` applies to all unless overridden.

## Method Quick Reference

| Method | Description |
|--------|-------------|
| `addBox({position, size, style?, mode?})` | Add rectangular prism |
| `removeBox({position, size})` | Subtract rectangular prism |
| `addSphere({center, radius, style?, mode?})` | Add voxelized sphere |
| `removeSphere({center, radius})` | Subtract sphere |
| `addLine({from, to, radius?, shape?, style?, mode?})` | Add voxel line |
| `removeLine({from, to, radius?, shape?})` | Subtract line |
| `addWhere({bounds, test, style?, mode?})` | Add voxels where test(x,y,z) returns true |
| `removeWhere({bounds, test})` | Remove voxels where test returns true |
| `styleBox/styleSphere/styleLine({..., style})` | Restyle existing voxels in-place |
| `toSVG(options?)` | Render to SVG string |
| `getFaces()` | Get projected 2D face array (cached) |
| `getFacesFrom({bounds, test, style?})` | Stateless face generation from test function |
| `setCamera({type, angle?, distance?, position?})` | Update camera projection |
| `rotate({axis, turns, center?})` | Rotate all voxels by 90-degree increments |
| `getVoxel([x,y,z])` | Get voxel data or null |
| `hasVoxel([x,y,z])` | Check if voxel exists |
| `getNeighbors([x,y,z])` | Get adjacent voxels |
| `forEach(callback)` | Iterate all voxels |
| `clear()` | Remove all voxels |
| `toJSON()` / `Heerich.fromJSON(data)` | Serialize/deserialize scene |

## Common Shape Options

All add methods accept these shared options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `'union'` \| `'subtract'` \| `'intersect'` \| `'exclude'` | `'union'` | Boolean operation |
| `style` | object or function | — | Per-face styling |
| `content` | string | — | Raw SVG instead of polygon faces |
| `opaque` | boolean | `true` | Whether voxel occludes neighbors |
| `meta` | object | — | Key/value pairs emitted as `data-*` attributes |
| `rotate` | `{axis, turns, center?}` | — | Rotate coordinates before placement |
