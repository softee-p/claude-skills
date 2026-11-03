---
description: >-
  Audit a site's source code and written copy against SEO and AEO best practices from a local build, with no live site or data exports needed, then fix what the user approves. Four read-only subagents check technical markup, copy, AI-answer readiness and fact consistency.
argument-hint: "[focus, such as one section or language]"
disable-model-invocation: true
---

# Source and copy audit

Focus: $ARGUMENTS

This reads the repo and a local build, so it works before launch and on sites behind a login. It changes nothing until the user approves. The user starts it by hand because it spawns four subagents.

It can't tell you real rankings or AI citations; those need live data (`seo-aeo:aeo-measure`). The rules are in `${CLAUDE_SKILL_DIR}/references/checklist.md`, each with its source.

**Contacts:** the local server only. Never log in, submit a form, or use a live site's credentials.

## 1. Map the repo

Read the repo's own instructions first; they override this skill. Then note:

- Framework, routes and page templates
- Where copy, titles, descriptions, structured data, the sitemap and `robots.txt` come from: files, a CMS or a database
- Languages, and how each version is built
- What existing tests already check, so you don't re-audit it
- Which facts are confirmed and which are waiting on the owner
- Decisions already made, such as AI crawler access or analytics. Don't reopen them
- Whether the stack may change before launch. If it may, mark framework-only fixes as later; copy carries over

## 2. Crawl a local build

Build and serve the site the way the repo documents. Exclude non-page routes, and pass the production origin so its links count as internal. In a sandbox, a server stops when its command ends, so start it and crawl in one command:

```bash
mkdir -p "$TMPDIR/site-audit"
START_SERVER_HERE & SERVER=$!
# wait here until http://localhost:PORT/ answers
python3 -I "${CLAUDE_SKILL_DIR}/scripts/local_crawl.py" http://localhost:PORT \
  --origin https://www.example.com --exclude /admin --exclude /api --exclude /login \
  --out "$TMPDIR/site-audit/crawl.json"
kill $SERVER
python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/rendered-crawl/scripts/summarize_crawl.py" \
  --origin https://www.example.com --text-dir "$TMPDIR/site-audit/pages" \
  "$TMPDIR/site-audit/crawl.json" > "$TMPDIR/site-audit/summary.md"
```

The crawl runs no JavaScript, so it shows what a crawler without a browser gets. `summary.md` lists the mechanical issues and notes. `pages/` holds each page's main text, link text and alt text, indexed in `pages/INDEX.tsv`. Don't read `crawl.json` into the conversation; it holds every page's HTML.

Some notes are expected off production, such as `noindex` everywhere or an empty sitemap. For those, read the code that switches them on production.

If the site won't build, audit the source alone and say what that leaves unchecked.

## 3. Audit in parallel

Start four `seo-aeo:site-auditor` agents in one message, one per area: **technical**, **copy**, **aeo**, **facts**. Give each one:

- The repo path, the paths to `summary.md` and `pages/`, and the map from step 1
- The focus, if the user gave one
- How to sample: every hand-written page, and for templated pages, the template plus two or three instances per language

They only read and report.

## 4. Report, then stop

Merge the results, remove duplicates, and drop anything without evidence. Sort into:

| Group | Meaning |
|---|---|
| Blocker | Stops pages being indexed, or tells visitors something false |
| High | Affects a key page or many pages |
| Medium | Worth doing, smaller effect |
| Low | Polish |

Under each finding give the evidence, the rule and its source, the fix, and who does it: Claude, the owner, or Claude drafting for the owner to approve. Mark rules that rest on one study or on vendor advice. List questions for the owner separately. A finding can matter beyond search, such as a compulsory cost shown as optional, so say when it does.

Save the report where the repo keeps such records, or ask where. Keep it out of public repos, because it quotes the site's content and code. Then show the groups and **stop for approval**. The user may approve some groups and not others.

## 5. Improve what was approved

Make the changes in the main thread, under the repo's own rules for branches, deploys and where copy lives. Don't deploy.

**Code:** fix each pattern at its source, such as the helper that builds titles, not page by page. Add a test where the repo has a place for one.

**Copy:**

- Never invent a fact, price, claim, quotation, statistic, review or credential. If the page needs one you can't source to the repo or the owner, add it to the owner's questions instead of writing it.
- Leave legal texts, prices and anything awaiting the owner's confirmation unchanged, and propose edits instead.
- Keep the site's voice. Improve what's there rather than rewriting it into generic marketing.
- Edit every language version, in natural wording for that language, and flag it for a native speaker.
- Don't generate pages in bulk to cover queries. Google treats many pages without added value as scaled content abuse.
- Show each change as before and after. Google says it's "critical to manually factcheck and review all AI-generated content", including titles, descriptions, structured data and alt text, so tell the user what to check.

## 6. Check the result

Run the crawl and summary again, then the repo's own tests. Report the counts before and after, what changed, what is still open, and the owner's list.

**Next:** `/seo-aeo:perf-audit` covers speed, which this skill leaves out.
