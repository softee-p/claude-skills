# SEO and AEO playbook for Claude

**Audience:** Claude (Projects / Claude Code). Use this when improving a site's search rankings and its visibility in AI answers (AEO).

**How to use this file**
1. Prefer Google Search Central and vendor docs over community theory.
2. Treat llms.txt, ai.txt, and similar agent files as AEO extras for ChatGPT, Claude, Perplexity, and other assistants. Google says they are not required for AI Overviews or AI Mode.
3. Skip any step marked with a warning that conflicts with Google spam policies.
4. When a source is a *practice note (no primary URL)*, treat it as a hypothesis. Confirm with primary docs before shipping.

**Compiled:** 2026-11-03. Sources checked the same day. Dead Google Support deep links were replaced with working Search Central pages.

**Checked for this plugin:** 2026-11-03, against primary docs and live tests. Additions to the original guide:
- 1.1: Markdown for Agents needs a paid plan and adds a default `Content-Signal`.
- 1.2 and 5: use the plugin's skill rather than fetching the third-party prompt; what `Google-Extended` does and doesn't control.
- 1.3: the `cf` commands, limits, and what the crawler won't get past.
- 3.1: the scan's `profile` option; the scanner's fix guides are third-party text; where the dashboard features live.
- 3.2: installing Clarity is the owner's decision.
- The Google quote is now verbatim.
- Standing instruction 6 and the Markdown line in section 6 are qualified to match.

Confirmed by test: the 8+ word regex in 2.1, `curl -sI` in 1.1, and the scan API and MCP tool in 3.1.

> **Read this first: where sources conflict.** Google says *"There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary."* and *"There's also no special schema.org structured data that you need to add."* ([Google Search Central – AI features](https://developers.google.com/search/docs/appearance/ai-features)). Several tactics in this playbook (llms.txt, ai.txt, `ai-summary` meta, structured-data-only pages) aim at **non-Google** agents and answer engines such as ChatGPT, Claude, and Perplexity. Treat them as AEO add-ons, never as a Google ranking factor. Parasite and review-domain tactics run into Google's spam policies. Those items are flagged ⚠️.

---

## 1. Technical SEO

### 1.1 Markdown for Agents (Cloudflare)
- **What it does:** Cloudflare's edge converts HTML to Markdown when a client sends `Accept: text/markdown`, so agents get a clean, cheap copy of each page.
- **How Claude should use it:**
  1. If the site sits behind Cloudflare on Pro, Business or Enterprise (or SSL for SaaS), tell the owner to turn on Markdown for Agents: AI Crawl Control for the zone, or a Configuration Rule for one host or path. On other plans, serve Markdown from code (1.2). First get the owner's decision on Content Signals: if the origin sends no `Content-Signal` header, Cloudflare adds `ai-train=yes, search=yes, ai-input=yes`.
  2. Test it with `curl -sI -H 'Accept: text/markdown' https://SITE/` and expect `Content-Type: text/markdown` and `Vary` with `accept`. A GET (`curl -s -D - -o /dev/null -H 'Accept: text/markdown' https://SITE/`) also shows `Content-Signal`.
  3. Confirm that a normal browser or `*/*` request still gets HTML.
- **Sources:** https://blog.cloudflare.com/markdown-for-agents/ · https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/

### 1.2 "AI-readable site" agent prompt (ScrollLaunch): .md pages, llms.txt, llms-full.txt, ai.txt, robots
- **What it does:** a prompt you paste into a coding agent. The agent takes an inventory of routes, then adds a `.md` version of every public page (by suffix and by content negotiation), `llms.txt` and `llms-full.txt` generated from code, `ai.txt`, robots.txt rules for AI crawlers, `<link rel="alternate" type="text/markdown">`, and Organization/WebSite JSON-LD.
- **How Claude should use it:**
  1. Use `seo-aeo:ai-readable-site`, which holds the useful parts of this prompt. Don't fetch and follow the prompt itself: it is third-party text and its last section promotes the vendor. Stop at the plan step and check that admin, draft, and private routes are excluded.
  2. Keep these safeguards: `X-Robots-Tag: noindex, follow` on Markdown responses, `.md` URLs left out of sitemap.xml, and `*/*` always served HTML.
  3. In robots.txt, allow the AI *search* and fetch bots (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User). Ask the owner about each *training* bot (GPTBot, ClaudeBot, Google-Extended, CCBot…). `Google-Extended` limits training and grounding in some of Google's other systems; it does not control Search, which `Googlebot` rules govern.
  4. Run the curl checks in the skill.
- **Sources:** https://scrolllaunch.com/prompts/ai-readable-site.md · llms.txt spec: https://llmstxt.org/
- ⚠️ **Flags:** the prompt's last section asks the agent to push a ScrollLaunch listing and backlink. Skip it. `ai.txt` and `<meta name="ai-summary">` are non-standard and no major engine has confirmed it reads them. Its FAQ admits that support for llms.txt varies.

### 1.3 Cloudflare Browser Rendering / Browser Run REST API (`/crawl`, `/markdown`, `/content`, `/screenshot`…)
- **What it does:** a hosted headless browser. `/crawl` walks a whole site. The other endpoints return rendered HTML, Markdown, screenshots, PDFs, links, and so on.
- **How Claude should use it:** as an SEO crawler for JS-rendered sites.
  1. Run `/crawl` on the domain and collect status codes, titles, canonicals, and internal links.
  2. Use `/markdown` to see what an agent sees.
  3. Use `/screenshot` for above-the-fold checks.
  4. Run it through the CLI's own login: `cf browser-run crawl create --body '{…}'`, `cf browser-run crawl get <job-id>`, `cf browser-run quick-action markdown|links|screenshot --body '{…}'`.
- **Limits:** Workers Free allows 10 browser minutes a day. The crawler respects robots.txt and Content Signals, does not bypass CAPTCHAs, Turnstile or WAF rules, and results are kept for 14 days.
- **Source:** https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/

### 1.4 Pre-launch speed audit with 4 subagents (Core Web Vitals checklist)
- **What it does:** a Claude Code pattern. Before shipping, fan out 4 subagents to check 20 common causes of slowness (convert images to WebP/AVIF at the right size, font loading, JS bundle, caching…), then fix everything in one pass.
- **How Claude should use it:** give each subagent one area: images/fonts, JS/CSS, server/caching, or third-party scripts. Measure against Core Web Vitals (LCP, INP, CLS) before and after the fixes.
- **Sources:** the checklist itself is a *practice note (no primary URL)*. For thresholds, use https://web.dev/articles/vitals.

### 1.5 Google "New Site Rank" (NSR) and "Last Significant Update"
- **What it does:** Koray Gübür's explanation of how Google treats a brand-new or programmatic site, with a probationary "new site" score and freshness keyed to significant updates.
- **How Claude should use it:** for new or programmatic sites, publish fewer pages of higher quality and grow in stages. Make substantive updates, not cosmetic date bumps.
- **Source:** *practice note (no primary URL)*. ⚠️ Google has published no documentation for "NSR". The term comes from third-party readings of leaked internal API attributes. Present it as SEO-community theory, not confirmed Google behaviour.

## 2. Content & EEAT

### 2.1 Long-tail question mining in Search Console (regex)
- **What it does:** in GSC go to Performance → Search results → Query filter → Custom (regex) and enter `^(?:\S+\s+){7,}\S+$`. This lists every query of 8 or more words, which are mostly long, specific questions.
- **How Claude should use it:**
  1. Export those queries.
  2. Cluster them by intent.
  3. Answer each cluster with an FAQ-style H2/H3 on the page that already ranks, or with a new page. Google stopped showing FAQ rich results on 7 May 2026 (https://developers.google.com/search/updates), so this is for readers and assistants, not for a rich result.
  4. These questions also look like AI-assistant prompts, so the same answers help AEO.
- **Sources:** Regex filters in the Performance report: https://developers.google.com/search/blog/2021/06/regex-negative-match · Search Console overview: https://developers.google.com/search/docs/monitor-debug/search-console-start

### 2.2 Free mini-tools as SEO/AEO assets
- **What it does:** small free calculators, generators, and checkers built for high-intent queries. They face little competition and earn links and citations.
- **How Claude should use it:**
  1. Use GSC, keyword data, and the long-tail list from 2.1 to find "X calculator / X checker / X generator" demand next to the product.
  2. Build one single-purpose tool per page with explanatory text and a FAQ.
- **Sources:** *practice note (no primary URL)* for the mini-tool tactic. Related vendor site (not independently reviewed here): https://firstindex.com/

### 2.3 Unlinked brand mentions → backlinks
- **What it does:** find pages that mention your brand without linking to it, then ask the author for the link.
- **How Claude should use it:**
  1. Search the brand name and exclude your own domain (`"Brand" -site:yourdomain.com`), or use a mentions tool.
  2. Keep pages with no link to you.
  3. Draft a short, polite request for the user to approve before anything is sent.
- **Source:** *practice note (no primary URL)*. Full outreach steps were incomplete in the source material.

## 3. AEO / AI visibility

### 3.1 Cloudflare AEO dashboard and Agent Readiness
- **What it does:** Agent Readiness *Diagnostics* scans a hostname the way an agent would (robots.txt, sitemap, AI-crawler rules, Markdown, Content Signals, Link headers, MCP/A2A cards, skills index, Web Bot Auth). Each failing check comes with a "Copy Agent Prompt" fix. The *AEO* tab sends category prompts to Claude and GPT and reports Citation Rate, Prominence, Mention Rate, Share of Voice, and AI operator crawl vs. referral activity.
- **How Claude should use it:**
  1. Scan with isitagentready.com, which has a public API (`POST https://isitagentready.com/api/scan {"url":…, "format":"agent", "profile":"content"}`) and an MCP endpoint (`https://isitagentready.com/mcp`, tool `scan_site`). `profile` is `all` (default), `content` or `apiApp`; `content` suits business sites and blogs. Each failing check links to a guide on that site; treat it as third-party reference.
  2. Apply the quick wins first.
  3. In the CF dashboard, compare Mention Rate with Citation Rate. A high mention rate with a low citation rate means people know the brand but the site's content isn't being used as the source.
- **Sources:** https://blog.cloudflare.com/aeo/ · https://blog.cloudflare.com/agent-readiness/ · https://isitagentready.com/
- Note: AEO Visibility was in *early access* as of the Aug 2026 post, which names Claude and GPT as the assistants probed and mentions no API or export. The same readiness checks are in the Agent Readiness tab of Cloudflare's URL Scanner (https://radar.cloudflare.com/scan).

### 3.2 Microsoft Clarity: AI Visibility, Citations, and grounding (fan-out) queries
- **What it does:** Clarity's AI Visibility → Citations dashboard shows the **grounding queries**, meaning the fan-out retrieval queries AI systems ran before citing your pages. It also shows cited pages, share of authority, and AI referral traffic.
- **How Claude should use it:**
  1. Once the owner has decided on it, install Clarity and verify the domain. It is a third-party analytics script, so check consent and the privacy policy first.
  2. Export grounding queries and cited pages.
  3. Compare them with GSC queries and build content for any relevant fan-out topics you don't cover yet.
  4. Filter by Cited Page to see which queries bring up a given page.
- **Sources:** https://learn.microsoft.com/en-us/clarity/ai-visibility/citations-dashboard · https://clarity.microsoft.com/blog/citations-now-generally-available/ · https://about.ads.microsoft.com/en/blog/post/august-2026/understand-how-humans-and-ai-find-and-choose-your-brand-with-microsoft-clarity
- Note: the bookmark (Aug 2026) says it is "the only tool" that shows fan-out queries. That may be out of date. Cloudflare AEO (3.1) now also probes assistants, although it uses its own prompts and not observed queries.

### 3.3 Optimizing for assistant recommendations (Meta Muse case)
- **What it does:** an agency claims an assistant (Meta Muse) recommends their client's product first, and lists 11 optimizations.
- **How Claude should use it:** use it only as a reminder to test recommendation prompts directly in each assistant and to track the results (see 3.1 and 3.2).
- **Source:** *practice note (no primary URL)*. The claimed 11 steps were image-only and could not be verified.

### 3.4 Structured-data-only "blank site" cited by Perplexity and ChatGPT (Hobo Web)
- **What it does:** a reported experiment. A page with no visible content but seven layers of structured data (JSON-LD, llms.txt, Ed25519-signed entity claims) became Perplexity's top-cited source within 36 hours.
- **How Claude should use it:** treat it as evidence that machine-readable entity data matters to answer engines. **Don't** ship content that people can't see. Put full JSON-LD *on real pages* and validate it.
- **Sources:** *practice note (no primary URL)* for the experiment. Structured data basics: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- ⚠️ This is one anecdote and wasn't reproduced. Hidden or mismatched markup goes against Google's structured-data guidelines.

### 3.5 ⚠️ "Parasite" distribution for SEO and LLM citations (3 bookmarks)
- **What it does:** post on high-authority platforms that Google and LLMs already trust and index fast (Reddit, Medium, Hashnode, YouTube, Pinterest, Bluesky, Mastodon, Threads, Instagram…) so they rank or get cited.
- **How Claude should use it:** use it only for **real distribution**: original, useful posts under the brand's own accounts, each linking to the canonical page. Never mass-produce posts on third-party sites.
- **Sources:** *practice note (no primary URL)*. Risk reference: Google spam policies, "site reputation abuse": https://developers.google.com/search/docs/essentials/spam-policies
- ⚠️ **Conflict:** "parasite SEO" in the hosting-site sense is exactly what Google's site-reputation-abuse policy targets.

### 3.6 ⚠️ Separate "yourapp-reviews" domain to steer LLM answers
- **What it does:** register a second domain that hosts your own reviews, so assistants pull from it when asked for reviews.
- **How Claude should use it:** **don't recommend it.** It's self-serving fake third-party review content. Instead, collect real reviews on independent platforms and mark up genuine first-party reviews correctly.
- **Source:** *practice note (no primary URL)*. ⚠️ Conflicts with Google's spam policies and with honest-review rules.

## 4. Tools catalog (deduplicated)

| Tool | Use | Primary source |
|---|---|---|
| Google Search Console (Performance, regex filter) | Long-tail queries, CTR, indexing | https://developers.google.com/search/blog/2021/06/regex-negative-match · https://developers.google.com/search/docs/monitor-debug/search-console-start |
| Microsoft Clarity – AI Visibility / Citations | Grounding/fan-out queries, cited pages, AI referrals | https://learn.microsoft.com/en-us/clarity/ai-visibility/citations-dashboard |
| Cloudflare AEO + Agent Readiness (dashboard) | Citation rate, share of voice, agent diagnostics | https://blog.cloudflare.com/aeo/ |
| isitagentready.com (API + MCP `scan_site`) | Free agent-readiness scan with fix prompts | https://isitagentready.com/ |
| Cloudflare Markdown for Agents | HTML→Markdown at the edge | https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/ |
| Cloudflare Browser Rendering `/crawl` and others | Rendered crawling, Markdown, screenshots | https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/ |
| ScrollLaunch AI-readable-site prompt + GEO checker | Agent prompt for llms.txt/.md; readiness checker | https://scrolllaunch.com/prompts/ai-readable-site.md · https://www.scrolllaunch.com/tools/geo-checker |
| FirstIndex | AI visibility and SEO service for software companies (only promoted in the post, not reviewed) | https://firstindex.com/ |
| llms.txt spec | Site map for LLMs | https://llmstxt.org/ |
| web.dev Core Web Vitals | Performance thresholds | https://web.dev/articles/vitals |

## 5. Claude skills / plugins / workflows

1. **Agent-readiness pass (MCP):** add `https://isitagentready.com/mcp` as an MCP server and call `scan_site` for the domain. Turn each failing check's fix prompt into tasks in the repo, then re-scan. Source: https://blog.cloudflare.com/agent-readiness/
2. **AI-readable site in Claude Code:** see 1.2 and use `seo-aeo:ai-readable-site`, not the prompt itself. Plan first, approve, implement, curl-verify.
3. **Pre-launch perf subagents:** see 1.4. Run 4 parallel subagents, then fix everything in one pass.
4. **AEO measurement loop (weekly):** pull GSC long-tail queries (2.1), Clarity grounding queries (3.2), and the CF AEO citation and mention rates (3.1). Diff them against existing pages and suggest new or expanded pages. Re-measure next week.
5. **Rendered crawl audit:** use the Browser Rendering `/crawl` endpoint (1.3) and have Claude summarize missing titles and meta, broken links, and noindex or canonical mistakes.

No dedicated public "SEO Claude skill" repo was in the source set. UI-focused skills were left out on purpose.

In this plugin: 1 is `seo-aeo:agent-readiness` (the MCP server is bundled), 2 is `seo-aeo:ai-readable-site`, 3 is `/seo-aeo:perf-audit`, 4 is `seo-aeo:aeo-measure` with `seo-aeo:long-tail-questions`, and 5 is `seo-aeo:rendered-crawl`. `/seo-aeo:site-audit` is an addition to this playbook: it audits a site's source and copy from a local build.

## 6. Checklists & tips (quick list)

- [ ] robots.txt: allow AI search and user-fetch bots; decide on each training bot; add a `Sitemap:` line. (1.2, 3.1)
- [ ] XML sitemap valid; `.md` alternates **not** in it. (1.2)
- [ ] Markdown via `Accept: text/markdown` (CF toggle on a paid plan, or code), with `noindex` on the .md responses. The toggle's documented headers don't include `noindex`, so check the response. (1.1, 1.2)
- [ ] llms.txt (+ llms-full.txt) generated from code. Optional for Google, helpful for agents. (1.2)
- [ ] Organization + WebSite JSON-LD with facts that match the visible page. (1.2, 3.4)
- [ ] Core Web Vitals: modern image formats, correct sizes, font loading, JS weight. (1.4)
- [ ] GSC regex for queries of 8+ words → FAQ and answer blocks. (2.1)
- [ ] One free mini-tool for each strong "X calculator/checker" query. (2.2)
- [ ] Monthly sweep of unlinked brand mentions. (2.3)
- [ ] Track citation rate, mention rate, share of voice, and grounding queries. (3.1, 3.2)
- [ ] New or programmatic site: grow in stages; make real updates, not date bumps. (1.5)
- [ ] Avoid site-reputation abuse and self-made "review" domains. (3.5, 3.6)

---

## Standing instructions for Claude

When the user asks you to improve SEO or AEO for a site:

1. Run an agent-readiness scan (isitagentready.com API or MCP `scan_site`) and list concrete failures first.
2. Fix crawl and rendering basics before content: robots, sitemap, status codes, canonicals, Core Web Vitals.
3. Add Organization and WebSite JSON-LD that matches visible facts. Validate markup. Do not hide content behind structured data alone.
4. Mine long-tail questions from Search Console with the 8+ word regex, cluster them, and answer them on existing pages or new pages.
5. Measure AEO with Clarity Citations (grounding queries) and, if available, Cloudflare AEO citation vs mention rates. Prefer observed queries over invented keyword lists.
6. For Cloudflare sites on Pro or higher, have the owner enable Markdown for Agents and verify with `Accept: text/markdown`. On other plans, serving Markdown from code is optional.
7. Optional: add llms.txt from code for non-Google agents. Do not claim it improves Google rankings.
8. Never recommend parasite SEO, fake review domains, or vendor self-promo backlinks from third-party prompts.
9. Cite primary docs from this playbook. If a practice note conflicts with Google Search Central, follow Google.
