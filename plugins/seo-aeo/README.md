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
