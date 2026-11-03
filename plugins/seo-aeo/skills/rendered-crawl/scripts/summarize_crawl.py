#!/usr/bin/env python3
"""Summarise saved Cloudflare Browser Run crawl results for an SEO audit.

Usage: summarize_crawl.py [--max N] crawl-1.json [crawl-2.json ...]

Each file is one saved `cf browser-run crawl get` response. The records need
HTML (`"formats": ["html"]`); response headers such as X-Robots-Tag are not in
them. Standard library only; the crawled HTML is parsed, never executed.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.description = None
        self.canonical = None
        self.robots = ""
        self.h1 = 0
        self.links = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href", "")
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.description = a.get("content", "").strip()
            elif name in ("robots", "googlebot"):
                self.robots += " " + a.get("content", "").lower()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def records_from(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    result = data.get("result", data)
    if isinstance(result, list):
        return result
    return result.get("records", [])


def normal(url):
    """Compare URLs without fragment, default path or trailing slash."""
    url = urldefrag(url)[0]
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    query = f"?{parts.query}" if parts.query else ""
    return f"{parts.scheme}://{parts.netloc.lower()}{path}{query}"


def http_status(record):
    meta = (record.get("metadata") or {}).get("status")
    if isinstance(meta, int):
        return meta
    status = record.get("status")
    return status if isinstance(status, int) else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--max", type=int, default=20, help="URLs listed per issue")
    args = ap.parse_args()

    records, seen = [], set()
    for path in args.files:
        for record in records_from(path):
            url = record.get("url")
            if url and url not in seen:
                seen.add(url)
                records.append(record)

    issues = defaultdict(list)
    titles, descriptions = defaultdict(list), defaultdict(list)
    statuses, states = Counter(), Counter()
    by_url, inbound = {}, Counter()
    links_from = {}
    no_html = 0

    for record in records:
        url = record["url"]
        status = http_status(record)
        state = record.get("outcome") or record.get("status")
        states[str(state)] += 1
        statuses[str(status) if status else "none"] += 1
        by_url[normal(url)] = status

        if isinstance(state, str) and state not in ("completed", "success"):
            issues[f"not fetched: {state}"].append(url)
            continue
        if status and status >= 400:
            issues[f"HTTP {status}"].append(url)
            continue
        if status and 300 <= status < 400:
            issues[f"HTTP {status} (redirect)"].append(url)
            continue

        html = record.get("html")
        if not html:
            no_html += 1
            continue
        page = Page()
        page.feed(html)
        title = " ".join(page.title.split())
        if title:
            titles[title].append(url)
        else:
            issues["missing title"].append(url)
        if page.description:
            descriptions[page.description].append(url)
        else:
            issues["missing meta description"].append(url)
        if page.h1 == 0:
            issues["no H1"].append(url)
        if "noindex" in page.robots:
            issues["noindex in meta robots"].append(url)
        if page.canonical is None:
            issues["no canonical"].append(url)
        elif normal(urljoin(url, page.canonical)) != normal(url):
            issues["canonical points elsewhere"].append(
                f"{url} -> {urljoin(url, page.canonical)}"
            )

        host = urlsplit(url).netloc.lower()
        targets = set()
        for href in page.links:
            absolute = urljoin(url, href)
            parts = urlsplit(absolute)
            if parts.scheme in ("http", "https") and parts.netloc.lower() == host:
                targets.add(normal(absolute))
        links_from[url] = targets
        for target in targets:
            if target != normal(url):
                inbound[target] += 1

    for text, urls in titles.items():
        if len(urls) > 1:
            issues["duplicate title"].append(f"{text!r}: {', '.join(urls)}")
    for text, urls in descriptions.items():
        if len(urls) > 1:
            issues["duplicate meta description"].append(f"{text!r}: {', '.join(urls)}")

    not_crawled = set()
    for url, targets in links_from.items():
        for target in targets:
            if target not in by_url:
                not_crawled.add(target)
            elif by_url[target] and by_url[target] >= 400:
                issues["internal link to an error page"].append(f"{url} -> {target}")
    if links_from:
        for key, status in by_url.items():
            if status and status < 300 and not inbound[key] and urlsplit(key).path != "/":
                issues["no internal links from crawled pages"].append(key)

    print(f"# Crawl summary\n\nRecords: {len(records)}")
    print("HTTP status: " + (", ".join(f"{k}: {v}" for k, v in sorted(statuses.items())) or "none"))
    print("Crawl state: " + (", ".join(f"{k}: {v}" for k, v in sorted(states.items())) or "none"))
    if no_html:
        print(f"\nWARNING: {no_html} fetched records had no HTML, so they were not checked. "
              'Crawl with "formats": ["html"].')
    if not_crawled:
        print(f"\nInternal links not in this crawl: {len(not_crawled)} (limit, patterns or robots; status unknown)")
    if not issues:
        print("\nNo issues found in the checked fields.")
    for name in sorted(issues):
        items = issues[name]
        print(f"\n## {name} ({len(items)})")
        for item in items[: args.max]:
            print(f"- {item}")
        if len(items) > args.max:
            print(f"- ... and {len(items) - args.max} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
