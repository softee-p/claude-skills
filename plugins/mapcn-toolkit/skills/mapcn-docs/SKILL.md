---
name: mapcn-docs
description: >
  This skill should be used when the user is building, debugging, or asking questions about
  interactive map components using mapcn (mapcn.dev). Covers all mapcn components: Map,
  MapControls, MapMarker, MarkerContent, MarkerPopup, MarkerTooltip, MarkerLabel, MapPopup,
  MapRoute, MapClusterLayer, and the useMap hook. Also applies when the user wants to add
  interactive maps to a React/Next.js project with Tailwind CSS and shadcn/ui, asks about
  map clusters, routes, markers, popups, heatmaps, delivery tracker maps, analytics maps,
  logistics maps, geospatial React components, free map tiles, CARTO basemaps, MapLibre,
  or OpenFreeMap styles.
---

# mapcn Documentation Skill

mapcn is a React component library for building interactive maps. Built on MapLibre GL, styled with Tailwind CSS, compatible with shadcn/ui. Free CARTO tiles by default — no API key needed.

## How to Use This Skill

Read the component reference file based on the user's question:

**Primary reference:** `${CLAUDE_PLUGIN_ROOT}/skills/mapcn-docs/references/components.md`

This file contains:
- Installation commands for all components
- Complete props tables with types and defaults
- Usage examples for every component
- Block (template) installation commands

**Lookup strategy:**
1. Match the user's question to the relevant component section
2. For "how do I get started" questions, start with the Installation and Map sections
3. For specific component questions, jump to that component's section
4. For "show me a template" or "pre-built" questions, see the Blocks section

## Quick Reference

| Component | Install | Purpose |
|-----------|---------|---------|
| `Map` | `npx shadcn@latest add @mapcn/map` | Root container, initializes MapLibre GL |
| `MapControls` | `npx shadcn@latest add @mapcn/controls` | Zoom, compass, locate, fullscreen buttons |
| `MapMarker` | `npx shadcn@latest add @mapcn/marker` | DOM-based markers (< few hundred) |
| `MapPopup` | `npx shadcn@latest add @mapcn/popup` | Standalone popups at coordinates |
| `MapRoute` | `npx shadcn@latest add @mapcn/route` | Lines/paths between coordinates |
| `MapClusterLayer` | `npx shadcn@latest add @mapcn/cluster` | Native clustering for large datasets |

| Block | Install |
|-------|---------|
| Analytics Map | `npx shadcn@latest add @mapcn/analytics-map` |
| Logistics Network | `npx shadcn@latest add @mapcn/logistics-network` |
| Heatmap | `npx shadcn@latest add @mapcn/heatmap` |
| Delivery Tracker | `npx shadcn@latest add @mapcn/delivery-tracker` |

**Prerequisites:** Tailwind CSS + shadcn/ui must be configured in the project.

All components import from `@/components/ui/map`.
