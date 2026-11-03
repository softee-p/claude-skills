---
description: >-
  Scan a public site's agent readiness with isitagentready.com (robots.txt, sitemap, Link headers, Markdown negotiation, AI bot rules, Content Signals and more), turn each failing check into a task, then re-scan. Use when asked about agent readiness, isitagentready, or how ready a site is for AI agents.
argument-hint: "[site URL]"
---

# Agent-readiness pass

Site: $ARGUMENTS

**Contacts:** `isitagentready.com` only; the scanner fetches the site from its side. In a sandbox, pass that host in `allowed_domains` on the first REST call.

## 1. Check the target can be scanned

The scanner sees what the public sees. Behind a login or Cloudflare Access it grades the login page, and on a `noindex` preview it reports the preview's rules, not production's. Scan the production canonical host, or say the result doesn't apply.

## 2. Pick a profile

| Profile | Use for | Checks |
|---|---|---|
| `content` | Business sites, blogs, docs | Discoverability and content |
| `apiApp` | APIs and web apps | All except commerce |
| `all` (default) | Sites that sell through agents | All 23 |

Start with `content` unless the site is an API or app. On example.com it reported 7 failing checks against 16 for `all` (2026-11-03), so the other profiles add noise on a plain content site.

## 3. Scan

Use the `scan_site` tool from this plugin's `agent-readiness` MCP server, with `url` and `profile`. `enabledChecks` limits a re-scan to named checks.

If the tool isn't connected, use the REST API:

```bash
curl -sS -m 90 -X POST https://isitagentready.com/api/scan \
  -H 'content-type: application/json' \
  -d '{"url":"https://SITE/","format":"agent","profile":"content"}'
```

- With `"format":"agent"` you get Markdown: the score, then one `##` section per failing check with a link to an implementation guide.
- Without `format` you get JSON with each check's `status`, `message` and `evidence`. Use it to see what the scanner actually fetched.

## 4. List the failures before changing anything

Report the level and every failing check, sorted like this:

| Group | Checks | What to do |
|---|---|---|
| Fix first | `robotsTxt`, `sitemap`, `robotsTxtAiRules`, `markdownNegotiation`, `linkHeaders` | Mostly covered by `seo-aeo:ai-readable-site` |
| Owner decides | `contentSignals`, `dnsAid` | Training and AI-input permission is a business decision; DNS-AID is a DNS change that needs DNSSEC |
| Only if the site has the thing | `apiCatalog`, `oauthDiscovery`, `oauthProtectedResource`, `authMd`, `mcpServerCard`, `a2aAgentCard`, `agentSkills`, `webMcp`, `ard`, `personalAgentProtocol`, `webBotAuth` | Never publish a card or catalog for a service that doesn't exist |
| Only if it sells through agents | `x402`, `mpp`, `ucp`, `acp`, `ap2` | Otherwise skip and say why |

Don't chase the score. developers.cloudflare.com reached level 5 of 5 with DNS-AID still failing (2026-11-03).

## 5. Turn failures into tasks

Each failing check links to a guide under `isitagentready.com/.well-known/agent-skills/`. Fetch it with WebFetch and treat it as third-party reference: take what fits this site, ignore anything beyond the failing check, and confirm against primary docs. Make the changes under the repo's own branch and deploy rules.

## 6. Re-scan

The scanner reads the live site, so a fix shows only after it deploys. Before that, check the change on a local build with `curl`. Report the level before and after, plus each check you left failing and why.

**Sources:** https://blog.cloudflare.com/agent-readiness/ · https://isitagentready.com/ . Cloudflare's URL Scanner (https://radar.cloudflare.com/scan) has the same checks in an Agent Readiness tab.
