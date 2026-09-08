# rwsdk-shadcn-update Skill

A general-purpose shadcn/ui component management assistant for RedwoodSDK projects.

## Overview

This skill helps you safely manage shadcn/ui components in ANY RedwoodSDK project with React Server Components (RSC). It automatically detects custom components, handles updates while preserving customizations, and integrates with both the shadcn MCP server and RedwoodSDK documentation.

### Key Features

1. **shadcn MCP Integration** - Detects and offers to install the shadcn MCP server for enhanced functionality
2. **Dynamic Documentation** - Fetches latest shadcn/ui guide from RedwoodSDK docs using `rwsdk-docs` skill
3. **Custom Component Detection** - Automatically analyzes your project to identify custom/modified components
4. **Safe Update Workflow** - Backup, update, restore, and validate in one automated flow
5. **Package Manager Agnostic** - Works with pnpm, yarn, or npm
6. **RSC Compliance** - Ensures proper React Server Components usage

## How It Works

### Phase 0: Setup & Prerequisites

1. **Check for shadcn MCP server**
   - If available: Use MCP tools for enhanced reliability
   - If not available: Ask user if they want to install it
   - If user declines: Fall back to shadcn CLI

2. **Fetch RedwoodSDK documentation**
   - Use `rwsdk-docs` skill to get latest shadcn/ui guide
   - Get RSC best practices
   - Understand component usage patterns

### Phase 1: Project Analysis

The skill analyzes your specific project to:

1. **Read components.json** - Understand path aliases, RSC settings, style variants
2. **Detect existing components** - List all shadcn components in your UI directory
3. **Classify components**:
   - **Custom components** - Never update via CLI (e.g., custom DatePicker compositions)
   - **Modified components** - Backup before updating (e.g., button.tsx with data-slot attributes)
   - **Standard components** - Safe to update anytime

4. **Create component inventory** - Output summary and document in customizations.md

### Phase 2: Component Operations

Based on your project's needs:

- **Update components** - Quick update (standard only) or safe update (all components)
- **Add components** - With automatic RSC compliance checks
- **Validate changes** - Type check, build check, visual testing plan

## Usage

When a user asks to update or add shadcn components:

1. **Invoke the skill**: Use skill name `rwsdk-shadcn-update`
2. **Follow Phase 0**: Check MCP server, fetch docs
3. **Analyze project**: Run Phase 1 to detect custom components
4. **Execute operation**: Update or add components using Phase 2 workflows
5. **Validate thoroughly**: Run automated checks and manual testing

## Dependencies

### Required

- **RedwoodSDK project** with shadcn/ui configured
- **rwsdk-docs skill** - Provides access to RedwoodSDK documentation

### Optional

- **shadcn MCP server** - Enhanced component management (recommended)
  - Installation guide: https://ui.shadcn.com/docs/mcp
  - The skill will offer to help install if not available

## Files Structure

```
rwsdk-toolkit/skills/rwsdk-shadcn-update/
├── SKILL.md                          # Main skill instructions
├── README.md                         # This file
├── scripts/
│   ├── _common.sh                    # Shared detection helpers (sourced, not run)
│   ├── backup-components.sh          # Snapshot the whole UI directory
│   ├── restore-components.sh         # Restore files from the latest snapshot
│   └── safe-update.sh                # Snapshot → update → change report → validate
└── references/
    └── customizations.md             # TEMPLATE to copy into your project
```

## Scripts

**Run every script from your project root** (the directory containing `package.json`). They
act on the current working directory and take arguments — **none of them needs editing.**

The UI directory is resolved from `components.json` (`aliases.ui`), falling back to
`src/app/components/ui`, `src/components/ui`, `app/components/ui`, `components/ui`.
Override with `SHADCN_UI_DIR`; override the backup location with `SHADCN_BACKUP_DIR`.

### backup-components.sh

```bash
bash .../scripts/backup-components.sh
```

- Copies the **entire** UI directory to `.shadcn-backup/<timestamp>/`, so nothing can be
  missed by a stale hand-maintained list
- Each run is a new timestamped snapshot; safe to run repeatedly
- No emojis (uses text markers: [INFO], [SUCCESS])

### restore-components.sh

```bash
bash .../scripts/restore-components.sh --list
bash .../scripts/restore-components.sh button.tsx card.tsx
bash .../scripts/restore-components.sh --all
```

- Restores from the most recent snapshot, selectively or wholesale
- Warns about manual merge needs for modified components
- Safe to run multiple times

### safe-update.sh

```bash
bash .../scripts/safe-update.sh input alert label
```

1. Snapshots the UI directory
2. Runs `shadcn@latest add <components> --overwrite --yes`
3. **Reports exactly which files are `[NEW]` or `[MODIFIED]`** against the snapshot
4. Runs the project's `types` script, if present
5. Runs the project's `build` script, if present

Customized components are deliberately **not** auto-restored — that would silently discard
the update you just asked for. Roll individual files back with `restore-components.sh`.

- Auto-detects package manager (pnpm/yarn/npm/bun)
- No emojis (uses text markers)


## Per-Project Setup

The scripts need no customization. What *is* project-specific is the **classification** of
your components, which Phase 1 of `SKILL.md` produces:

### 1. Identify your custom components

Run the skill's Phase 1 analysis. It reads `components.json`, lists the UI directory, and
sorts every component into three buckets:

- **Custom** — not in the shadcn registry (compositions, project-specific logic). Never
  update via the CLI.
- **Modified** — a registry component you changed (custom `data-*` attributes, altered
  variants, extra styling). Update deliberately, then check the `[MODIFIED]` report.
- **Standard** — unchanged. Safe to pass to `safe-update.sh`.

### 2. Record the classification in your project

Copy `references/customizations.md` into your repo (e.g. `docs/shadcn-customizations.md`)
and fill it in. **Keep it in the project, not in the plugin directory** — the plugin is
shared across every project on your machine and is replaced on plugin update, so notes left
there are wrong for other projects and lost on the next update.

### 3. Add the backup directory to .gitignore

```
.shadcn-backup/
```


## Sharing This Skill

This skill is designed to be **general-purpose** and can be shared on public repositories:

### Why It's Shareable

1. **No project-specific hardcoded values** - Works with any RedwoodSDK project
2. **Dynamic documentation** - Fetches latest info via `rwsdk-docs` skill
3. **Automatic detection** - Analyzes each project's specific setup
4. **Package manager agnostic** - Works with pnpm, yarn, or npm
5. **Template-based** - Customizations doc adapts to user's components

### To Use in Another Project

1. Copy the entire `rwsdk-toolkit/skills/rwsdk-shadcn-update/` directory to your project
2. Ensure the `rwsdk-docs` skill is available
3. Run Phase 1 analysis to detect your project's custom components
4. Customize the scripts based on your component inventory
5. The skill will adapt to your project's specific needs

### Contributing

When updating this skill:

- Keep it general-purpose (no hardcoded component lists in SKILL.md)
- Use `rwsdk-docs` skill for framework-specific information
- Update reference docs when new patterns emerge
- Test with different project configurations (pnpm/yarn/npm, different path structures)
- Remove emojis from all output (use text markers instead)

## Common Scenarios

### Scenario 1: First-Time User

1. User asks to update shadcn components
2. Skill checks for MCP server (not installed)
3. Skill asks: "Would you like to install the shadcn MCP server?"
4. User says yes → Skill fetches guide from https://ui.shadcn.com/docs/mcp
5. After installation, skill runs Phase 1 analysis
6. Skill creates component inventory and customizations.md
7. User customizes backup/restore scripts based on inventory
8. Skill proceeds with safe update workflow

### Scenario 2: Adding New Component

1. User asks to add "tooltip" component
2. Skill checks MCP server (available) → Uses MCP
3. Skill fetches RedwoodSDK docs for RSC patterns
4. Skill adds component via MCP
5. Skill checks RSC compliance (is "use client" needed?)
6. Skill runs validation (types, build)
7. Skill creates project-specific testing plan

### Scenario 3: Updating Modified Components

1. User asks to update button component
2. Skill runs Phase 1 analysis → Detects button.tsx has data-slot attributes
3. Skill classifies as "Modified Component"
4. Skill runs backup script
5. Skill updates via shadcn CLI or MCP
6. Skill restores from backup
7. Skill warns: "button.tsx restored from backup. Check for new features to manually merge."
8. Skill runs validation

## MCP Server Benefits

When shadcn MCP server is available:

- **Better reliability** - Direct integration with shadcn registry
- **Enhanced features** - Access to additional MCP-specific functionality
- **Faster operations** - Optimized component fetching
- **Consistent behavior** - Less prone to CLI version issues

When MCP server is not available:

- **Falls back to CLI** - Uses `pnpm dlx` / `npx shadcn@latest` commands
- **Still fully functional** - All core features work
- **No degradation** - Same safety guarantees with backup/restore

## Troubleshooting

### "Skill can't detect my custom components"

- Check that component files are in the path specified by `components.json`
- Verify component files have `.tsx` extension
- Look for custom `data-*` attributes or modified variants manually
- Set `SHADCN_UI_DIR=<path>` if the directory is in a non-standard location

### "MCP server installation fails"

- Follow the official guide at https://ui.shadcn.com/docs/mcp
- Check MCP server logs for errors
- Fall back to shadcn CLI if installation is blocked

### "Scripts don't work with my package manager"

- Scripts auto-detect pnpm, yarn, npm, and bun
- Check that your lock file exists (pnpm-lock.yaml, yarn.lock, package-lock.json, bun.lock)
- npm is used as the fallback when no lock file is present

## License

This skill can be freely shared and modified to help the RedwoodSDK community.
