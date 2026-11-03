#!/usr/bin/env python3
"""Crawl a local build the way a crawler that runs no JavaScript sees it.

Usage: local_crawl.py BASE_URL [--origin URL] [--exclude PREFIX ...] [--limit N]
                      [--delay SECONDS] --out FILE

Starts at BASE_URL and its sitemap, follows internal links and hreflang
alternates, and records every answer without following redirects, so a chain
stays visible. GET only: it submits no forms and sends no credentials. Writes
the format summarize_crawl.py reads. Standard library only; the HTML is parsed,
never executed.

--origin is the production origin. Pages on a local build often link to it, so
those URLs are treated as this site and fetched from BASE_URL instead.
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlsplit

KEPT_HEADERS = ("content-type", "location", "x-robots-tag", "cache-control", "vary", "link", "content-language")
MAX_BYTES = 5 * 1024 * 1024
USER_AGENT = "seo-aeo-local-crawl (runs no JavaScript)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        elif tag == "link" and a.get("hreflang") and a.get("href"):
            self.hrefs.append(a["href"])
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def is_local(host):
    return host in ("localhost", "127.0.0.1", "::1") or host.endswith(".localhost")


class Crawler:
    def __init__(self, base, origin, excludes, delay):
        self.base = base.rstrip("/")
        self.origin = origin.rstrip("/") if origin else None
        self.excludes = excludes
        host = urlsplit(self.base).hostname or ""
        # Local requests must not go through a sandbox's proxy; anything else may have to.
        proxies = urllib.request.ProxyHandler({}) if is_local(host) else urllib.request.ProxyHandler()
        self.opener = urllib.request.build_opener(proxies, NoRedirect())
        self.delay = delay if is_local(host) else max(delay, 1.0)

    def inside(self, url, page):
        """The URL on BASE_URL if it belongs to this site and isn't excluded, else None."""
        url = urldefrag(urljoin(page, url.strip()))[0]
        if self.origin and (url == self.origin or url.startswith(self.origin + "/")):
            url = self.base + url[len(self.origin):]
        if url == self.base:
            url = self.base + "/"
        if not url.startswith(self.base + "/"):
            return None
        path = urlsplit(url).path or "/"
        if any(path == e or path.startswith(e.rstrip("/") + "/") for e in self.excludes):
            return None
        return url

    def get(self, url):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"})
        try:
            response = self.opener.open(request, timeout=30)
        except urllib.error.HTTPError as error:
            response = error
        return response.getcode(), dict(response.headers.items()), response.read(MAX_BYTES)

    def sitemap_urls(self, url, depth=0):
        try:
            status, _, body = self.get(url)
        except (OSError, ValueError):
            return []
        if status != 200:
            return []
        # A regular expression rather than an XML parser: <loc> is all that's needed.
        text = body.decode("utf-8", "replace")
        is_index = "<sitemapindex" in text
        found = []
        for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", text, re.S):
            loc = html.unescape(loc)
            if not is_index:
                found.append(self.inside(loc, url) or loc)
            elif depth < 2:
                local = self.inside(loc, url)
                found.extend(self.sitemap_urls(local, depth + 1) if local else [])
        return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("base")
    ap.add_argument("--origin", help="production origin, such as https://www.example.com")
    ap.add_argument("--exclude", action="append", default=[], help="path prefix to skip; repeat as needed")
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--delay", type=float, default=0.25, help="seconds between requests")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    crawler = Crawler(args.base, args.origin, args.exclude, args.delay)
    sitemap = crawler.sitemap_urls(crawler.base + "/sitemap.xml")
    try:
        status, _, body = crawler.get(crawler.base + "/robots.txt")
        robots = body.decode("utf-8", "replace") if status == 200 else None
    except OSError:
        robots = None

    queue = deque([crawler.base + "/"])
    queue.extend(u for u in sitemap if u.startswith(crawler.base))
    seen, records = set(queue), []
    while queue and len(records) < args.limit:
        url = queue.popleft()
        record = {"url": url, "status": "completed", "metadata": {"url": url}}
        try:
            status, headers, body = crawler.get(url)
        except (OSError, ValueError) as error:
            record.update(status="errored", outcome=f"error: {type(error).__name__}")
            records.append(record)
            continue
        lower = {k.lower(): v for k, v in headers.items()}
        record["outcome"] = "success"
        record["metadata"]["status"] = status
        record["headers"] = {k: lower[k] for k in KEPT_HEADERS if k in lower}
        targets = []
        if 300 <= status < 400 and lower.get("location"):
            targets.append(lower["location"])
        elif "html" in lower.get("content-type", ""):
            markup = body.decode("utf-8", "replace")
            record["html"] = markup
            page = Links()
            page.feed(markup)
            record["metadata"]["title"] = " ".join(page.title.split())
            if status < 300:
                targets.extend(page.hrefs)
        for target in targets:
            local = crawler.inside(target, url)
            if local and local not in seen:
                seen.add(local)
                queue.append(local)
        records.append(record)
        time.sleep(crawler.delay)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"source": "local_crawl", "base": crawler.base, "robotsTxt": robots,
                   "sitemapUrls": sitemap, "records": records}, f)
    left = len(queue)
    print(f"{len(records)} pages saved to {args.out}; {len(sitemap)} sitemap URLs"
          + (f"; stopped at --limit with {left} URLs left" if left else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
