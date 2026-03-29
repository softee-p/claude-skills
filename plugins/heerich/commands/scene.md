---
description: Generate a 3D voxel scene as SVG using the heerich library from a text description
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: <scene description>
---

Use the heerich-docs skill to ensure correct API usage. Read the references before writing code.

The user wants to generate a voxel scene: $ARGUMENTS

## Workflow

1. **Read the references** for correct API usage:
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/heerich-docs/references/api-reference.md` for method signatures
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/heerich-docs/references/recipes.md` for patterns and templates
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/heerich-docs/references/styling-and-cameras.md` if the user requests specific visual effects

2. **Interpret the scene description** — break it into voxel operations:
   - Identify distinct objects (buildings, terrain, characters, trees, etc.)
   - Determine approximate dimensions and positions
   - Choose appropriate colors and styles for each element
   - Decide on camera angle (oblique for isometric look, perspective for dramatic depth)

3. **Generate `generate-scene.mjs`** — a complete Node.js ESM script that:
   - Imports `Heerich` from `'heerich'` and `writeFileSync` from `'node:fs'`
   - Constructs the scene using appropriate methods
   - Uses descriptive comments for each section
   - Writes SVG output to `scene.svg`
   - Logs a completion message

4. **Design guidelines**:
   - Default to oblique camera with angle 45 unless the user requests otherwise
   - Use tile `[40, 40]` for detailed scenes, `[20, 20]` for larger/complex scenes
   - Apply distinct colors to different faces (top, front, right) for visual depth
   - Use style functions for gradients or patterns when appropriate
   - Keep coordinates reasonable (most scenes fit within -20 to 20 per axis)
   - Use `removeBox`/`removeSphere` for architectural details (doors, windows, arches)
   - Add a ground plane or platform when it improves the composition

5. **Run the script**:
   - Check if heerich is installed: `npm ls heerich 2>/dev/null || npm install heerich`
   - Run: `node generate-scene.mjs`
   - Confirm the SVG was created and report the output file path
