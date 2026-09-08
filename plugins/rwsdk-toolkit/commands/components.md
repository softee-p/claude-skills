---
description: Safely update or add shadcn/ui components in a RedwoodSDK project with backup/restore
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [component-names...]
---

Use the rwsdk-shadcn-update skill to safely manage shadcn/ui components.

Components: $ARGUMENTS

Follow the rwsdk-shadcn-update skill workflow:

1. **Phase 0: Setup** — Check for shadcn MCP server, fetch latest rwsdk shadcn guide
2. **Phase 1: Analysis** — Read components.json, detect custom/modified/standard components, create inventory. Record findings in the *project* (e.g. `docs/shadcn-customizations.md`), never in the plugin directory
3. **Phase 2: Operations** — For updates: snapshot the UI directory, update the components classified as standard, then review the `[MODIFIED]` report and roll back anything that clobbered a customization. For new components: add and verify RSC compliance
4. **Validation** — Run type check and build, test visually on affected pages

Run all bundled scripts from the project root; they take component names as arguments and
need no editing. Always commit before starting.
