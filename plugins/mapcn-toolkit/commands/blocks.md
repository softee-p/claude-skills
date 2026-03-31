---
description: Install and customize a pre-built mapcn block (analytics-map, logistics-network, heatmap, delivery-tracker)
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: <block-name>
---

Use the mapcn-docs skill to look up the blocks reference before proceeding.

The user wants to install block: $ARGUMENTS

**Available blocks:**
- `analytics-map` — Real-time analytics: world map, breakdown cards, device stats
- `logistics-network` — Domestic logistics map with sidebar stats
- `heatmap` — Globe-projected heatmap with zoom-dependent styling
- `delivery-tracker` — Live order tracking: route, courier position, order details

**Workflow:**

1. Read the mapcn-docs component reference (Blocks section) for details
2. Verify prerequisites (Tailwind CSS + shadcn/ui configured)
3. Install the base map component if not already present: `npx shadcn@latest add @mapcn/map`
4. Install the block: `npx shadcn@latest add @mapcn/<block-name>`
5. Explore the installed block files to understand the structure
6. Help the user customize the block for their use case (data sources, styling, layout)
