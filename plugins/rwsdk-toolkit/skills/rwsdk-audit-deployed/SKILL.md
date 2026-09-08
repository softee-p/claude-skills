---
name: rwsdk-audit-deployed
description: >
  This skill should be used when the user asks to "audit my deployed app", "check production
  errors", "is my worker healthy", "check logs", "investigate production issues", "analyze
  worker performance", or any request to inspect a deployed RedwoodSDK/Cloudflare Worker
  application. Trigger on mentions of production errors, Cloudflare Worker logs, observability,
  metrics, latency issues, error rates, deployment health checks, or "pnpm release" follow-up
  verification. Also trigger when the user asks "is everything working" or wants to verify a
  recent deployment succeeded. Uses whichever Cloudflare observability/developer-platform MCP
  is available for worker telemetry — falling back to the wrangler CLI when none is — plus the
  rwsdk-docs skill for best practice verification. Provides a structured 6-phase audit workflow
  with automated report generation.
---

# RedwoodSDK Deployed Application Audit

Methodically audit a deployed RedwoodSDK application on Cloudflare Workers.

## Prerequisites

**Step 0 — determine which telemetry source is available.** Check the actual tool list; do
not assume a server name. In rough order of usefulness:

| Source | Look for | Covers |
|---|---|---|
| Cloudflare observability MCP | a tool matching `*observability*` with an `observability_query`-style call | Phases 2–5 in full |
| Cloudflare Developer Platform MCP | `mcp__*Cloudflare*__workers_list`, `workers_get_worker`, `workers_get_worker_code` | Phase 1, plus code inspection in Phase 6 |
| `wrangler` CLI | `npx wrangler --version` succeeds | Fallback for Phases 1–4 (see below) |

Server names differ between installs — the same tools may appear as
`mcp__cloudflare-observability__*`, `mcp__claude_ai_Cloudflare_Developer_Platform__*`, or
another prefix entirely. **Match on the tool's suffix, not the full name.**

**Announce which source you are using before starting**, and say plainly which phases will
be degraded or skipped. Never present a wrangler-based audit as if it had the full 7-day
analytics behind it.

- **rwsdk-docs skill** - For verifying code against best practices (always available)

### Fallback: no observability MCP

`wrangler` covers a useful subset. It needs `wrangler login` or `CLOUDFLARE_API_TOKEN`, and
`wrangler tail` is a **live** stream — it shows nothing until new requests arrive, so it
cannot answer "what happened in the last 24h".

```bash
npx wrangler deployments list                       # Phase 1: recent versions
npx wrangler deployments status                     # Phase 1: what is live now
npx wrangler tail <worker-name> --format json \
  --status error --once                             # Phases 2-4: live errors only
```

With this fallback: Phase 1 works, Phases 2–4 become live-tail sampling over a window you
must wait out, and **Phase 5 (7-day metrics) is not available** — say so in the report
rather than omitting the section silently. Phase 6 works regardless, since it only reads
source code.

## Audit Workflow

Execute these phases in order. Use TodoWrite to track progress.

### Phase 1: Setup & Discovery

1. **Auto-detect worker name** (if in a project):
   - Check `wrangler.jsonc` or `wrangler.toml` for `name` field
   - Note any `env.*` sections — a staging worker is usually `<name>-staging`
   - If found, use it as the default worker name
2. List workers: the `workers_list` tool on whichever Cloudflare MCP is present
   (fallback: `npx wrangler deployments list`)
3. Confirm worker name with user if:
   - Multiple workers exist
   - No wrangler config found
   - User specifies a different worker
4. Get worker details: the `workers_get_worker` tool
   (fallback: `npx wrangler deployments status`)

### Phase 2: Error Analysis (24h)

Query recent errors (observability MCP; with the wrangler fallback use
`npx wrangler tail <worker> --format json --status error` instead and note the reduced window):
```json
{
  "view": "events",
  "queryId": "errors-24h",
  "limit": 20,
  "parameters": {
    "filters": [
      {"key": "$metadata.service", "operation": "eq", "type": "string", "value": "<worker-name>"},
      {"key": "$metadata.level", "operation": "eq", "type": "string", "value": "error"}
    ]
  },
  "timeframe": {"reference": "<current-iso-time>", "offset": "-24h"}
}
```

**Analyze patterns:**
- Route-specific errors (`$metadata.trigger`)
- Version-specific (`$workers.scriptVersion.id`) - different versions indicate deployment changes
- Error fingerprints for grouping

### Phase 3: Warning Analysis

Query warnings (cross-request promise issues common in rwsdk):
```json
{
  "view": "events",
  "queryId": "warnings-24h",
  "limit": 10,
  "parameters": {
    "filters": [
      {"key": "$metadata.service", "operation": "eq", "type": "string", "value": "<worker-name>"},
      {"key": "$metadata.level", "operation": "eq", "type": "string", "value": "warn"}
    ]
  },
  "timeframe": {"reference": "<current-iso-time>", "offset": "-24h"}
}
```

### Phase 4: Current Health Check

Verify no recent errors (confirms if issues resolved):
```json
{
  "view": "calculations",
  "queryId": "errors-1h",
  "parameters": {
    "filters": [
      {"key": "$metadata.service", "operation": "eq", "type": "string", "value": "<worker-name>"},
      {"key": "$metadata.level", "operation": "eq", "type": "string", "value": "error"}
    ],
    "calculations": [{"operator": "count", "alias": "error_count"}]
  },
  "timeframe": {"reference": "<current-iso-time>", "offset": "-1h"}
}
```

### Phase 5: Performance Metrics (7d)

**Requires the observability MCP** — there is no wrangler equivalent. If unavailable, state
that in the report instead of dropping the section.

Query health and performance by outcome:
```json
{
  "view": "calculations",
  "queryId": "health-7d",
  "parameters": {
    "filters": [{"key": "$metadata.service", "operation": "eq", "type": "string", "value": "<worker-name>"}],
    "calculations": [
      {"operator": "count", "alias": "total"},
      {"operator": "avg", "key": "$workers.wallTimeMs", "keyType": "number", "alias": "avg_latency"},
      {"operator": "p99", "key": "$workers.wallTimeMs", "keyType": "number", "alias": "p99_latency"}
    ],
    "groupBys": [{"type": "string", "value": "$workers.outcome"}]
  },
  "timeframe": {"reference": "<current-iso-time>", "offset": "-7d"}
}
```

### Phase 6: Code Quality (If Errors Found)

When errors reference code paths:

1. **Use rwsdk-docs skill** to verify patterns against docs. Also read its
   `CHANGELOG.md` and `DOC-ACCURACY.md`: a production error is often an old pattern that a
   newer `rwsdk` changed, and DOC-ACCURACY.md covers behavior the docs do not mention yet
   (post-deploy chunk 404s and stranded client navigations both surface as production
   symptoms).
2. **Read source files** from error stack traces
3. **Check the deployed `rwsdk` version** in `package.json` against the release notes — a
   symptom may already be fixed upstream
4. **Check common issues** - See [references/common-issues.md](${CLAUDE_PLUGIN_ROOT}/skills/rwsdk-audit-deployed/references/common-issues.md)

## Report Structure

```markdown
# Audit Report: <worker-name>

## Executive Summary
**Status**: [HEALTHY | DEGRADED | CRITICAL]
**Telemetry source**: [observability MCP | Cloudflare MCP + wrangler | wrangler only]
**Coverage gaps**: [phases that could not run, and why — omit only if there are none]

## Health Metrics (7 Days)
| Outcome | Count | % |
|---------|-------|---|

**Performance:** Avg: Xms, P99: Xms

## Issues Found
### [RESOLVED | ACTIVE]: <Title>
**Error:** <message>
**Route:** <trigger>
**Root Cause:** <explanation>

## Performance by Route
| Route | Avg | P99 | Notes |

## Code Quality
| Pattern | Status | Notes |

## Recommendations
```

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | >2% | >5% |
| P99 latency | >3s | >5s |
| Canceled rate | >10% | >15% |

**Version mismatch in errors** = Recent deployment likely fixed/caused issue
