---
description: >-
  Mine long, specific questions from Google Search Console with the 8+ word regex, cluster them by intent, answer them on existing or new pages, and spot demand for free mini-tools. Use when given a Search Console export, or asked for long-tail queries, FAQ topics, content gaps from Search Console, or calculator and checker ideas.
argument-hint: "[path to Search Console export]"
---

# Long-tail questions from Search Console

Export: $ARGUMENTS

Queries of eight or more words are mostly specific questions, and they read like prompts to an AI assistant, so answering them helps both search and AEO.

## 1. Get the data

Work from real data, never from invented queries. If there is no export, give the user these steps and wait:

1. In Search Console, open Performance, then Search results.
2. Add a Query filter, choose Custom (regex), and enter:

   ```text
   ^(?:\S+\s+){7,}\S+$
   ```

3. Pick a long date range and export.

The filter uses RE2 syntax. The regex splits on spaces, so it also works for German, Greek and other languages that use them. Search Console leaves rare, anonymized queries out of its report, so the list is a sample, not the whole demand.

The Queries tab of an export doesn't pair queries with pages. To learn which page ranks for a question, filter the report by page, or match by content and mark the match as your inference.

## 2. Cluster by intent

Group queries that a single answer would satisfy. For each cluster, record the queries, total impressions and clicks, average position, and the page that ranks or fits best.

## 3. Decide per cluster

- **A page already ranks or fits:** add an FAQ-style H2 or H3 in the question's words, with the direct answer in the first sentence.
- **No page fits and the demand is real:** propose a new page. Avoid near-duplicate pages per query.
- **The site can't answer truthfully:** say so. Facts come from the site's own content or the owner, never from guesses.

Follow the repo's rules for where copy lives and how language versions are handled.

## 4. Spot mini-tool demand

Look in the list, and in other Search Console data, for "X calculator", "X checker", "X generator" and the local-language equivalents next to the product. A candidate becomes one single-purpose tool on one page, with explanatory text and a FAQ. This tactic is a practice note with no primary source, so present candidates with their demand numbers and let the user decide.

## 5. Report

| Cluster | Example queries | Impressions | Clicks | Position | Page | Action |
|---|---|---|---|---|---|---|

Then list the mini-tool candidates and any questions the site can't answer yet.

**Sources:** https://developers.google.com/search/blog/2021/06/regex-negative-match · https://developers.google.com/search/docs/monitor-debug/search-console-start
