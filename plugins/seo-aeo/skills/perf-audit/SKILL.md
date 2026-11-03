---
description: >-
  Pre-launch speed audit: four read-only subagents check images and fonts, JS and CSS, server and caching, and third-party scripts, then everything is fixed in one pass and Core Web Vitals are measured again.
argument-hint: "[site URL]"
disable-model-invocation: true
---

# Pre-launch speed audit

Site: $ARGUMENTS

The user starts this skill by hand because it spawns four subagents at once.

**Contacts:** the target site, plus `www.googleapis.com` if you use PageSpeed Insights. In a sandbox, pass them in `allowed_domains`.

## Targets

A page passes when all three are good at the 75th percentile of page loads, on mobile and on desktop ([web.dev](https://web.dev/articles/vitals)):

| Metric | Good |
|---|---|
| LCP | 2.5 s or less |
| INP | 200 ms or less |
| CLS | 0.1 or less |

## 1. Measure a baseline

Pick the key page templates, not only the homepage. Then measure with the best method available and note which one you used:

- **Field data** from PageSpeed Insights, which includes Chrome UX Report data when the site has enough traffic. A new or restricted site has none, so say so.
- **Lab data** from Lighthouse or the `cloudflare:web-perf` skill, if installed. Lab runs have no real INP; report Total Blocking Time as a stand-in and label it.

Headless Chrome may not start inside a sandbox. If it doesn't, say so and use PageSpeed Insights or a connected browser.

## 2. Audit in parallel

Start four `seo-aeo:perf-auditor` agents in one message, one per area:

1. Images and fonts
2. JS and CSS
3. Server and caching
4. Third-party scripts

Give each one the URL, the repo path, the baseline and its area. They only read and report.

## 3. Merge

Remove duplicates and rank the findings by the metric each one improves. Drop any finding with no evidence.

## 4. Fix in one pass

Make the fixes yourself in the main thread, so the edits don't collide. Follow the repo's branch and deploy rules. Anything that needs the owner, such as removing a tag they rely on, goes on a list.

## 5. Measure again

Use the same method and pages as the baseline. Report before and after per page and metric, plus anything you could not measure. Lab numbers before launch are not field numbers, so re-check field data once real traffic exists.

The checklists in the agent are general practice. The original note's list of 20 causes isn't available, so don't claim coverage of it.
