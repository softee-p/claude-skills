---
description: Create a new interactive map view or page using mapcn components
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: <description-of-map-view>
---

Use the mapcn-docs skill to look up the component reference before proceeding.

The user wants to create: $ARGUMENTS

**Workflow:**

1. Read the mapcn-docs component reference for relevant components
2. Explore the existing project structure to understand conventions (file naming, directory layout, routing)
3. Determine which mapcn components are needed:
   - Basic map display: `Map`, `MapControls`
   - Location pins: `MapMarker`, `MarkerContent`, `MarkerPopup`, `MarkerTooltip`
   - Navigation paths: `MapRoute`
   - Large datasets: `MapClusterLayer`
   - Info overlays: `MapPopup`
4. Check which components are already installed (look in `components/ui/map.tsx`)
5. Install any missing components using `npx shadcn@latest add @mapcn/<component>`
6. Implement the map view following the project's conventions:
   - Import from `@/components/ui/map`
   - Wrap `Map` in a sized container (Card, div with height)
   - Use controlled viewport if state sync is needed
   - Keep coordinate data separate from render logic
7. Verify with type checking
