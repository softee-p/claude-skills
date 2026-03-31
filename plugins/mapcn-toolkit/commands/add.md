---
description: Add mapcn map components or blocks to the current project
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: <component-or-block-name>
---

Use the mapcn-docs skill to look up the component reference before proceeding.

The user wants to add: $ARGUMENTS

**Workflow:**

1. Read the mapcn-docs component reference to find the correct install command
2. Verify prerequisites — check the project has Tailwind CSS and shadcn/ui configured:
   - Look for `tailwind.config.*` or `@tailwind` directives in CSS
   - Look for `components.json` (shadcn config)
   - If missing, guide the user to set these up first
3. Run the appropriate install command:
   - Components: `npx shadcn@latest add @mapcn/<component>`
   - Blocks: `npx shadcn add @mapcn/<block>`
4. Verify the component was installed by checking `components/ui/map.tsx` exists
5. Show a minimal usage example from the reference
