---
description: >-
  Crawl a whole site with Cloudflare Browser Run (/crawl) and report status codes, titles, meta descriptions, canonicals, noindex and broken internal links. Also shows one page as an agent sees it, as rendered Markdown, links or a screenshot. Use for SEO crawl audits, especially of JS-rendered sites.
argument-hint: "[site URL]"
---

# Rendered crawl audit

Site: $ARGUMENTS

**Contacts:** `api.cloudflare.com`, through the `cf` CLI. Cloudflare's crawler fetches the site from its side.

## 1. Check the login

Run `cf auth whoami` (or `npx cf auth whoami` where the project has `cf` as a dependency). `cf` uses its own login. Never read a token, or put one in a command, a header or an environment variable. If it isn't signed in, stop and ask the user to run `cf auth login`.

`cf cli search` queries describe the task only: never a domain, ID or token.

`cf` writes a `.cloudflare/` cache into the current folder, and it holds the account's ID and name. Before committing, check that `.cloudflare/` is gitignored or run `cf` from another folder, especially in a public repo.

If the user has no Cloudflare account, fetch the sitemap's URLs with `curl`, run the same checks by hand, and say that JavaScript was not rendered.

## 2. Start the crawl

Set a real `limit`, because the default is 10 pages. Keep results outside the repo, in `$TMPDIR` or the session's scratch folder.

```bash
cf browser-run crawl create --body '{
  "url": "https://SITE/",
  "limit": 200,
  "source": "all",
  "formats": ["html"],
  "options": { "excludePatterns": ["https://SITE/admin/**"] }
}'
```

The command prints the job ID as a JSON string. Add `--dry-run` to preview the request without sending it.

| Field | Values |
|---|---|
| `source` | `all` (default), `sitemaps`, `links`. Use `sitemaps` to test the sitemap and `links` to test internal linking |
| `render` | `true` (default) runs JavaScript. `false` is a fast HTML fetch; use it for a server-rendered site |
| `options` patterns | `*` matches anything except `/`, `**` matches anything. Excludes win over includes |

## 3. Wait and save

```bash
cf browser-run crawl get JOB_ID --limit 1   # read "status"
cf browser-run crawl get JOB_ID > "$TMPDIR/crawl-1.json"
```

Check every 30 seconds or so while `status` is `running`. Other end states: `completed`, `errored`, `cancelled_by_user`, `cancelled_due_to_timeout`, `cancelled_due_to_limits`. If the response has a `cursor`, save the next part with `--cursor` into `crawl-2.json`, and so on. Results are kept for 14 days.

`cf` prints the result object itself, without the API's `success` envelope. In a record, `status` is the crawl state and `metadata.status` is the HTTP code (seen on a real crawl, 2026-11-03; the docs are unclear about this).

## 4. Summarise

Do not read the saved files into the conversation; they hold every page's HTML. Run:

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/summarize_crawl.py" "$TMPDIR"/crawl-*.json
```

It reports status codes, redirects, pages not fetched, missing or duplicate titles and descriptions, missing H1, noindex, missing or mismatched canonicals, links to error pages, and pages no crawled page links to. Add `--max N` to list more URLs per issue.

It can't see response headers, so sample `X-Robots-Tag` with `curl -s -D - -o /dev/null URL`. Judge each finding against the site's intent: a `noindex` on a thank-you page is correct.

## 5. Read the limits into the result

- **robots.txt is respected,** including `crawl-delay`. A record with `disallowed` status is a finding, not an error. Check that the block is intended.
- **Content Signals are enforced.** `400 Crawl disallowed by Content-Signal directive` means the site's `robots.txt` refuses a declared purpose. Declare only what you do: `"crawlPurposes": ["search"]`, and `"contentUse": "reference"` if the use level also conflicts.
- **Bot protection still applies.** Browser Run doesn't bypass CAPTCHAs, Turnstile or WAF rules. An allow rule for the crawler (bot detection ID `128292352`) is the owner's change, not yours.
- **Cloudflare Access:** expect the login page instead of the site. Don't pass a service token through this crawl. Audit production or a local build instead, and report what you could not reach.
- **Free plan:** 10 browser minutes a day, after which jobs end as `cancelled_due_to_limits`. Report a partial crawl as partial.
- The user agent is `CloudflareBrowserRenderingCrawler/1.0` and can't be changed, so a site that treats bots differently may look different to real users.

## One page, as an agent sees it

```bash
cf browser-run quick-action markdown --body '{"url":"https://SITE/page"}'
cf browser-run quick-action links --body '{"url":"https://SITE/page"}'
cf browser-run quick-action screenshot --body '{"url":"https://SITE/page"}'
```

Use `markdown` to see what an agent gets, and `screenshot` to check what is above the fold. Run `cf schema browser-run quick-action screenshot` for its options and how the image comes back.

## Report

Give the crawl settings and coverage (`total`, `finished`, how it ended), then findings grouped by issue with counts and example URLs, then what you would fix first.

**Source:** https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/
