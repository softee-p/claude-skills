---
description: >-
  Measure AI visibility: combine Search Console long-tail queries, Microsoft Clarity grounding queries and cited pages, Cloudflare AEO citation and mention rates, and AI Crawl Control data, compare them with the site's pages, propose new or expanded pages, and track the change run by run. Use when given these exports, or asked to track AI citations, share of voice or grounding queries.
argument-hint: "[paths to exports]"
---

# AEO measurement loop

Exports: $ARGUMENTS

Run this weekly. The inputs are files or numbers the user provides; do not log in to these dashboards with credentials.

## 1. Collect what exists

| Source | What to get | How |
|---|---|---|
| Search Console | Queries of 8+ words | `seo-aeo:long-tail-questions` step 1 |
| Microsoft Clarity, AI Visibility, Citations | Grounding queries, cited pages, page citations, share of authority (branded and non-branded), AI referral traffic, query topics | The user copies or exports it |
| Cloudflare AEO tab | Citation Rate, Prominence, Mention Rate, Share of Voice | The user copies the numbers. It was in early access in the August 2026 post, which mentions no API or export |
| Cloudflare AI Crawl Control | Requests, status codes and paths per AI crawler. 403, 429 and 404 answers show crawlers being turned away | The user copies the numbers. It's on all plans; referral numbers need a paid plan |

Name any source that is missing, and carry on with the rest. Never fill a gap with a guess.

**Setting up Clarity is the owner's decision.** It is a third-party analytics script, so check consent and the privacy policy before adding it. Without it, the loop still runs on the other sources; you just lose the grounding queries.

## 2. Read the numbers correctly

- **Grounding queries** are what AI systems searched for before citing a page. They can differ from what people typed. Prefer them over invented keyword lists.
- **Share of authority** is calculated per day and counts only days on which the domain was cited for the query. Microsoft notes this can read higher than broader calculations, so compare it with itself over time.
- **Cloudflare AEO** sends its own category prompts to Claude and GPT. Those are probes, not observed queries, so keep them apart from Clarity's data.
- **High Mention Rate with low Citation Rate:** people know the brand, but the site's content isn't being used as the source.
- **High branded with low non-branded share of authority:** visibility rests on the brand, not on topical authority.

## 3. Compare with the site

Get the page list from the sitemap or the repo. For each query or topic, mark it **covered**, **thin** or **missing**. Use Clarity's Cited Page filter to see which queries bring up a page.

## 4. Propose

For each thin or missing topic that matters to the business, propose an expanded or new page, and give the evidence behind it. Writing the copy is a separate step for the user to approve. Facts come from the site or the owner.

## 5. Keep a dated snapshot

Save the numbers and proposals as a dated file in a folder the user chooses, then compare with the previous snapshot and report what moved. Store aggregates only, with no visitor or session data. If this is the first run, say there is no baseline to compare with yet.

Only set up a recurring run if the user asks.

## 6. Test recommendations directly

To check how assistants recommend the brand, run the same category prompts in each assistant and record the results by hand, with the date. Treat claims like "11 optimizations got us recommended first" as unverified.

**Sources:** https://learn.microsoft.com/en-us/clarity/ai-visibility/citations-dashboard · https://blog.cloudflare.com/aeo/
