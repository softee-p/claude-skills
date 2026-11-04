# seo-aeo

A Claude Code plugin for improving a site's search rankings and its visibility in AI answers. It stays within Google's spam policies and marks unproven tactics as unproven.

## Install

```text
/plugin marketplace add softee-p/claude-skills
/plugin install seo-aeo@mkw-claude-plugins
```

Then:

```text
/seo-aeo:improve https://example.com
```

If the site isn't public yet, `improve` skips the scans and works from the old site's data and the copy instead.

In the VS Code extension, `/plugin` isn't available: type `/plugins` to open the Manage plugins dialog, or run these from a terminal with `claude plugin marketplace add softee-p/claude-skills` and `claude plugin install seo-aeo@mkw-claude-plugins`.

To update, run these from a terminal, then restart Claude Code. This marketplace doesn't auto-update unless you turn that on:

```bash
claude plugin marketplace update mkw-claude-plugins
claude plugin update seo-aeo@mkw-claude-plugins
```

## Cloud sessions

A cloud session doesn't load plugins installed on your machine, or plugins that a repository's `.claude/settings.json` turns on. **Tested:** a plugin synced from claude.ai loads in a claude.ai cloud session, with its skills and agents; `site-audit` and `perf-audit` still start only from their slash commands. Without that, try installing it from the cloud environment's setup script (Claude Code v2.1.292 or later). **The setup script hasn't been tested yet:**

```bash
#!/bin/bash
claude plugin install seo-aeo --marketplace softee-p/claude-skills
```

If that doesn't work, a repository can commit copies to `.claude/skills/` and `.claude/agents/`, which cloud sessions do load. References to `${CLAUDE_PLUGIN_ROOT}` would then need changing, and the copies would need keeping in step with the plugin.

What each skill needs there:

| Skill | In a cloud session |
|---|---|
| `site-audit`, `perf-audit` | Need the repository to build and serve locally in the session's VM. `site-audit`'s crawl and summary scripts ran there. A real browser for `perf-audit` isn't guaranteed; claude.ai cloud sessions have shipped with Chromium and Playwright |
| `long-tail-questions`, `aeo-measure` | Need the exports committed or otherwise available in the session |
| `agent-readiness` | `isitagentready.com` isn't on the default Trusted list, so add it with Custom network access |
| `ai-readable-site` | Works for code changes; the checks need the local build |
| `rendered-crawl` | Needs a signed-in `cf`, which a cloud session doesn't have. Run it locally |

## What's in it

| Skill | What it does |
|---|---|
| `/seo-aeo:improve` | Sets the order of work and the limits, and hands each part to the skills below |
| `/seo-aeo:agent-readiness` | Scans with isitagentready.com, sorts the failures, and re-scans after fixes |
| `/seo-aeo:ai-readable-site` | Adds Markdown versions, llms.txt, AI crawler rules and JSON-LD, after a plan you approve |
| `/seo-aeo:rendered-crawl` | Crawls with Cloudflare Browser Run and summarises status, titles, canonicals, noindex and links |
| `/seo-aeo:site-audit` | Audits your source code and written copy from a local build, with no live site needed, then fixes what you approve. Four read-only `site-auditor` subagents check technical markup, copy, AI-answer readiness and fact consistency. You start this one by hand |
| `/seo-aeo:perf-audit` | Runs four read-only `perf-auditor` subagents, fixes in one pass, and measures Core Web Vitals again. You start this one by hand |
| `/seo-aeo:long-tail-questions` | Clusters 8+ word Search Console queries into answers, and spots mini-tool demand |
| `/seo-aeo:aeo-measure` | Compares Search Console, Clarity and Cloudflare AEO data with your pages, run by run |

The full playbook, with a source for every tactic, is in `skills/improve/references/playbook.md`.

## What it needs

| Need | Used by | Notes |
|---|---|---|
| `isitagentready.com` | `agent-readiness` | The bundled MCP server is available in every session while the plugin is enabled. A REST fallback is documented in the skill |
| `cf` CLI, signed in | `rendered-crawl` | Uses `cf`'s own login. Browser Run is limited to 10 minutes a day on Workers Free |
| Python 3 | `rendered-crawl`, `site-audit` | Standard library only |
| A local build | `site-audit` | Built and served the way your repo documents |
| Your exports | `long-tail-questions`, `aeo-measure` | Search Console, Clarity and Cloudflare AEO data. The skills never log in for you |
| The target site, `www.googleapis.com` | `ai-readable-site`, `perf-audit` | For `curl` checks and PageSpeed Insights |

In a network sandbox, allow these hosts up front. A scanner or crawler can't see past a login or Cloudflare Access; it sees the login page.

## What it leaves to you

- Whether training bots may crawl, and your Content Signals values
- Zone settings, DNS and adding analytics scripts
- Sending anything to a third party; outreach is drafted, never sent

It won't recommend parasite SEO, self-made review domains, hidden content or vendor backlinks.

## What it doesn't cover

Local search, such as a Google Business Profile, isn't in the playbook. `site-audit` can't show real rankings or AI citations; those need live data.
