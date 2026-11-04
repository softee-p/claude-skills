#!/usr/bin/env python3
"""Summarise saved crawl results for an SEO audit.

Usage: summarize_crawl.py [--origin URL] [--max N] [--thin WORDS] [--text-dir DIR]
                          crawl-1.json [crawl-2.json ...]

Each file is a saved `cf browser-run crawl get` response or local_crawl.py
output; the records need HTML. Issues break a rule; notes are worth a look but
may be fine. --origin is the production origin, for a crawl of another host.
--text-dir writes each page's main text to its own file, so copy can be read
without its HTML. Standard library only; the HTML is parsed, never executed.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlsplit

SKIP = {"script", "style", "noscript", "template", "svg"}
BLOCK = {"p", "div", "section", "article", "aside", "header", "footer", "nav", "ul", "ol", "li",
         "table", "tr", "td", "th", "br", "dl", "dt", "dd", "blockquote", "figure", "figcaption", "form"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
CONTAINERS = {"main", "article", "section"}
GENERIC_ANCHORS = {"click here", "here", "read more", "learn more", "more", "link", "this page",
                   "hier", "hier klicken", "mehr", "weiterlesen", "mehr erfahren",
                   "εδώ", "περισσότερα", "διαβάστε περισσότερα"}
HREFLANG = re.compile(r"^(x-default|[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*)$")
ELLIPSIS = ("…", "...")


def primary_lang(lang):
    """The language without its region: "de-AT" -> "de"."""
    return (lang or "").split("-")[0].lower()


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self.description = None
        self.canonicals = []
        self.robots = ""
        self.headings = []
        self.links = []
        self.alternates = {}
        self.jsonld = []
        self.images = []
        self.no_href = 0
        self._stack_skip = 0
        self._in_title = False
        self._main = 0
        self._has_main = False
        self._heading = None
        self._anchor = None
        self._jsonld = None
        self._chrome = 0
        self._containers = 0
        self._main_parts, self._body_parts = [], []

    def _emit(self, text):
        if self._main:
            self._main_parts.append(text)
        if not self._chrome:
            self._body_parts.append(text)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "script" and "ld+json" in a.get("type", ""):
            self._jsonld = []
        if tag in SKIP:
            self._stack_skip += 1
            return
        if tag in CONTAINERS:
            self._containers += 1
        if tag == "nav" or tag == "footer" or (tag == "header" and not self._containers):
            self._chrome += 1
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "main":
            self._main += 1
            self._has_main = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.description = a.get("content", "").strip()
            elif name in ("robots", "googlebot"):
                self.robots += " " + a.get("content", "").lower()
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(a.get("href", ""))
            elif "alternate" in rel and a.get("hreflang"):
                self.alternates[a["hreflang"]] = a.get("href", "")
        elif tag == "a":
            if a.get("href"):
                self._anchor = {"href": a["href"], "text": []}
                self.links.append(self._anchor)
            else:
                self.no_href += 1
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt") if "alt" in a else None,
                                "sized": ("width" in a and "height" in a)})
            if self._anchor is not None and a.get("alt"):
                self._anchor["text"].append(a["alt"])
        if tag in HEADINGS:
            self._heading = {"level": int(tag[1]), "text": []}
            self._emit("\n")
        elif tag in BLOCK:
            self._emit("\n- " if tag == "li" else "\n")

    def handle_endtag(self, tag):
        if tag == "script" and self._jsonld is not None:
            self.jsonld.append("".join(self._jsonld))
            self._jsonld = None
        if tag in SKIP:
            self._stack_skip = max(0, self._stack_skip - 1)
            return
        if tag in CONTAINERS:
            self._containers = max(0, self._containers - 1)
        if tag == "nav" or tag == "footer" or (tag == "header" and not self._containers):
            self._chrome = max(0, self._chrome - 1)
        if tag == "title":
            self._in_title = False
        elif tag == "main":
            self._main = max(0, self._main - 1)
        elif tag == "a":
            self._anchor = None
        elif tag in HEADINGS and self._heading:
            text = " ".join(" ".join(self._heading["text"]).split())
            self.headings.append((self._heading["level"], text))
            self._emit("\n" + "#" * self._heading["level"] + " " + text + "\n")
            self._heading = None
        elif tag in BLOCK:
            self._emit("\n")

    def handle_data(self, data):
        if self._jsonld is not None:
            self._jsonld.append(data)
            return
        if self._stack_skip:
            return
        if self._in_title:
            self.title += data
            return
        if self._anchor is not None:
            self._anchor["text"].append(data)
        if self._heading is not None:
            self._heading["text"].append(data)
            return
        self._emit(data)

    def main_text(self):
        raw = "".join(self._main_parts if self._has_main else self._body_parts)
        lines = (" ".join(line.split()) for line in raw.splitlines())
        return "\n".join(line for line in lines if line and line != "-")


def load(path):
    """The records of one saved file, and its sitemap URLs and robots.txt if it has them."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data, None, None
    result = data.get("result", data)
    if isinstance(result, list):
        return result, None, None
    return result.get("records", []), result.get("sitemapUrls"), result.get("robotsTxt")


def normal(url):
    """Compare URLs without fragment or trailing slash."""
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


def json_types(value):
    """Every @type in a JSON-LD value."""
    found = []
    if isinstance(value, dict):
        kind = value.get("@type")
        found.extend(kind if isinstance(kind, list) else [kind] if kind else [])
        for item in value.values():
            found.extend(json_types(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(json_types(item))
    return [str(t) for t in found]


def group_of(url):
    """A page's section, ignoring a leading language segment."""
    parts = [p for p in urlsplit(url).path.split("/") if p]
    if parts and re.fullmatch(r"[a-z]{2}", parts[0]):
        parts = parts[1:]
    return "/" + parts[0] if parts else "/"


def text_file_name(url):
    parts = urlsplit(url)
    name = parts.path.strip("/").replace("/", "__") or "index"
    if parts.query:
        name += "__" + hashlib.sha1(parts.query.encode()).hexdigest()[:8]
    return re.sub(r"[^\w.-]", "_", name) + ".txt"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--origin", help="production origin, for a crawl of another host")
    ap.add_argument("--max", type=int, default=20, help="items listed per issue")
    ap.add_argument("--thin", type=int, default=150, help="main-text words below which a page is noted")
    ap.add_argument("--text-dir", help="write each page's main text here")
    args = ap.parse_args()
    origin = args.origin.rstrip("/") if args.origin else None

    records, sitemap, robots, seen = [], None, None, set()
    for path in args.files:
        found, file_sitemap, file_robots = load(path)
        sitemap = file_sitemap if file_sitemap is not None else sitemap
        robots = file_robots if file_robots is not None else robots
        for record in found:
            url = record.get("url")
            if url and url not in seen:
                seen.add(url)
                records.append(record)

    def resolve(href, page_url):
        """An absolute URL, moved from the production origin onto the crawled host."""
        url = urljoin(page_url, href.strip())
        if origin and (url == origin or url.startswith(origin + "/")):
            parts = urlsplit(page_url)
            url = f"{parts.scheme}://{parts.netloc}" + url[len(origin):]
        return url

    issues, notes = defaultdict(list), defaultdict(list)
    titles, descriptions, bodies = defaultdict(list), defaultdict(list), defaultdict(list)
    statuses, states, groups, jsonld_types, languages = Counter(), Counter(), Counter(), Counter(), Counter()
    by_url, redirects, inbound, links_from, alternates_of = {}, {}, Counter(), {}, {}
    lang_of = {}
    generic = defaultdict(list)
    no_html, pages_index = 0, []
    fetched_pages, noindexed = 0, set()
    if args.text_dir:
        os.makedirs(args.text_dir, exist_ok=True)

    for record in records:
        url = record["url"]
        status = http_status(record)
        state = record.get("outcome") or record.get("status")
        headers = record.get("headers") or {}
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
            target = headers.get("location", "")
            redirects[normal(url)] = normal(resolve(target, url)) if target else ""
            continue
        if "noindex" in headers.get("x-robots-tag", "").lower():
            noindexed.add(url)

        html = record.get("html")
        if not html:
            if "html" in headers.get("content-type", "html"):
                no_html += 1
            continue

        page = Page()
        page.feed(html)
        text = page.main_text()
        words = len(text.split())
        title = " ".join(page.title.split())
        fetched_pages += 1
        lang_of[normal(url)] = primary_lang(page.lang)
        if "noindex" in page.robots:
            noindexed.add(url)
        if len(page.canonicals) > 1:
            issues["more than one canonical"].append(url)
        if not page.canonicals:
            issues["no canonical"].append(url)
        # A filter or sort URL that names another page as canonical is a variant of that page:
        # it's noted once and left out of the checks below, which apply to the page it names.
        variant = bool(page.canonicals) and normal(resolve(page.canonicals[0], url)) != normal(url)
        if variant:
            notes["canonical points to another URL (check it's intended)"].append(f"{url} -> {page.canonicals[0]}")
        else:
            groups[group_of(url)] += 1
            languages[page.lang or "none"] += 1
            if not page.lang:
                issues["no lang on <html>"].append(url)
            if not page._has_main:
                notes["no <main> element, so the page's main content isn't marked"].append(url)
            if title:
                titles[(page.lang, title)].append(url)
                if len(title) > 70:
                    notes["title over 70 characters (may be truncated)"].append(f"{len(title)}: {url}")
                if title.endswith(ELLIPSIS):
                    notes["title ends in an ellipsis (cut off by the code?)"].append(f"{title[-60:]!r}: {url}")
            else:
                issues["missing title"].append(url)
            if page.description:
                descriptions[(page.lang, page.description)].append(url)
                if len(page.description) > 160:
                    notes["description over 160 characters (Google shortens it for display; fine if it ends on a whole sentence)"].append(
                        f"{len(page.description)}: {url}")
                if page.description.endswith(ELLIPSIS):
                    notes["description ends in an ellipsis (cut mid-sentence?)"].append(f"{page.description[-60:]!r}: {url}")
            else:
                issues["missing meta description"].append(url)
            h1s = sum(1 for level, _ in page.headings if level == 1)
            if h1s == 0:
                issues["no H1"].append(url)
            elif h1s > 1:
                notes["more than one H1"].append(url)
            if words < args.thin:
                notes[f"under {args.thin} words of main text"].append(f"{words}: {url}")
            elif text:
                bodies[hashlib.sha1(text.encode()).hexdigest()].append(url)

        for raw in page.jsonld:
            try:
                kinds = json_types(json.loads(raw))
            except ValueError:
                issues["JSON-LD that doesn't parse"].append(url)
                continue
            jsonld_types.update(kinds)
            if "FAQPage" in kinds:
                notes["FAQPage markup (Google stopped showing FAQ rich results in May 2026)"].append(url)

        unlabelled = [i["src"] for i in page.images if i["alt"] is None]
        if unlabelled:
            issues["images with no alt attribute"].append(f"{len(unlabelled)}: {url}")
        unsized = sum(1 for i in page.images if not i["sized"])
        if unsized:
            notes["images without width and height (fine if CSS reserves the space)"].append(f"{unsized}: {url}")
        if page.no_href:
            notes["<a> without href (not crawlable)"].append(f"{page.no_href}: {url}")

        host = urlsplit(url).netloc.lower()
        targets = set()
        for link in page.links:
            href = link["href"].strip()
            if href.lower().startswith("javascript:"):
                notes["javascript: links (not crawlable)"].append(url)
                continue
            absolute = resolve(href, url)
            parts = urlsplit(absolute)
            if parts.scheme in ("http", "https") and parts.netloc.lower() == host:
                targets.add(normal(absolute))
                label = " ".join(" ".join(link["text"]).split()).lower()
                if label in GENERIC_ANCHORS:
                    generic[label].append(url)
        links_from[url] = targets
        for target in targets:
            if target != normal(url):
                inbound[target] += 1

        if page.alternates and not variant:
            alternates_of[normal(url)] = {lang: normal(resolve(h, url)) for lang, h in page.alternates.items()}
            for lang, href in page.alternates.items():
                if not HREFLANG.match(lang):
                    issues["invalid hreflang code"].append(f"{lang}: {url}")
                if not re.match(r"https?://", href):
                    issues["hreflang URL not absolute"].append(f"{href}: {url}")
            if normal(url) not in alternates_of[normal(url)].values():
                issues["hreflang set doesn't include the page itself"].append(url)
            if "x-default" not in page.alternates:
                notes["hreflang set without x-default"].append(url)

        if args.text_dir and not variant:
            name = text_file_name(url)
            link_lines = sorted({f"{' '.join(' '.join(l['text']).split()) or '(no text)'} -> {l['href']}"
                                 for l in page.links})
            image_lines = sorted({f"{'(no alt attribute)' if i['alt'] is None else i['alt'] or '(empty alt)'} <- {i['src'][:120]}"
                                  for i in page.images})
            with open(os.path.join(args.text_dir, name), "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\nLang: {page.lang}\nWords: {words}\nTitle: {title}\n"
                        f"Description: {page.description or ''}\n\n{text}\n\n"
                        "--- Links on the whole page ---\n" + "\n".join(link_lines) + "\n\n"
                        "--- Images: alt text <- source ---\n" + "\n".join(image_lines) + "\n")
            flat_description = " ".join((page.description or "").split())
            pages_index.append(f"{name}\t{page.lang}\t{words}\t{url}\t{title}\t{flat_description}")

    def duplicates(found, what):
        """The same text twice in one language is an issue; across languages it may be untranslated."""
        langs_of = defaultdict(set)
        for (lang, text), urls in found.items():
            langs_of[text].add(lang)
            if len(urls) > 1:
                issues[f"duplicate {what} within a language"].append(f"{text[:80]!r}: {', '.join(urls)}")
        for text, langs in langs_of.items():
            if len(langs) > 1:
                notes[f"same {what} in more than one language (untranslated?)"].append(
                    f"{'/'.join(sorted(langs))}: {text[:80]!r}")

    duplicates(titles, "title")
    duplicates(descriptions, "meta description")
    if noindexed and len(noindexed) >= fetched_pages:
        notes["every page is noindex (expected off the production host; check the code turns it off there)"].append(
            f"{len(noindexed)} pages")
    else:
        for url in sorted(noindexed):
            issues["noindex"].append(url)
    for urls in bodies.values():
        if len(urls) > 1:
            notes["identical main text"].append(", ".join(urls))
    for label, urls in generic.items():
        notes["generic link text"].append(f"{label!r} on {len(urls)} pages, such as {urls[0]}")

    for page_key, alternates in alternates_of.items():
        for lang, target in alternates.items():
            if target == page_key or target not in alternates_of:
                if target != page_key and by_url.get(target) and by_url[target] >= 300:
                    issues["hreflang points at a redirect or error"].append(f"{page_key} -> {target}")
                continue
            if page_key not in alternates_of[target].values():
                issues["hreflang without a return link"].append(f"{page_key} -> {target}")

    # A link from one language version into another, other than to the page's own alternates
    # (a language switcher), drops the reader into a language they didn't choose.
    crossing = defaultdict(list)
    for url, targets in links_from.items():
        source = normal(url)
        own = lang_of.get(source)
        switcher = set(alternates_of.get(source, {}).values())
        for target in targets:
            other = lang_of.get(target)
            if own and other and other != own and target not in switcher:
                crossing[(own, other, target)].append(url)
    for (own, other, target), sources in sorted(crossing.items(), key=lambda item: -len(item[1])):
        more = f" and {len(sources) - 1} more" if len(sources) > 1 else ""
        notes["internal link into another language (not a language switcher)"].append(
            f"{own} -> {other}: {target}, from {sources[0]}{more}")

    not_crawled = set()
    for url, targets in links_from.items():
        for target in targets:
            if target not in by_url:
                not_crawled.add(target)
            elif by_url[target] and by_url[target] >= 400:
                issues["internal link to an error page"].append(f"{url} -> {target}")
            elif by_url[target] and by_url[target] >= 300:
                notes["internal link to a redirect"].append(f"{url} -> {target}")
    if links_from:
        for key, status in by_url.items():
            if status and status < 300 and not inbound[key] and urlsplit(key).path != "/":
                notes["no internal links from crawled pages"].append(key)
    for start, target in redirects.items():
        if target in redirects:
            issues["redirect chain"].append(f"{start} -> {target} -> {redirects[target]}")

    if sitemap is not None and not sitemap:
        notes["the sitemap listed no URLs (expected off the production host; check it fills on production)"].append("sitemap.xml")
    elif sitemap:
        listed = {normal(u) for u in sitemap}
        for url in sorted(listed):
            status = by_url.get(url)
            if status is not None and status != 200:
                issues["sitemap URL that doesn't answer 200"].append(f"{status}: {url}")
        for key, status in by_url.items():
            if status == 200 and key not in listed and "?" not in key:
                notes["page answers 200 but isn't in the sitemap"].append(key)
    if robots is not None and re.search(r"^\s*Disallow:\s*/\s*$", robots, re.M):
        notes["robots.txt has `Disallow: /` (expected only off the production host)"].append("robots.txt")

    print(f"# Crawl summary\n\nRecords: {len(records)}")
    print("HTTP status: " + (", ".join(f"{k}: {v}" for k, v in sorted(statuses.items())) or "none"))
    print("Crawl state: " + (", ".join(f"{k}: {v}" for k, v in sorted(states.items())) or "none"))
    if languages:
        print("Languages: " + ", ".join(f"{k} ({v})" for k, v in languages.most_common()))
    if groups:
        print("Sections: " + ", ".join(f"{k} ({v})" for k, v in groups.most_common()))
    if jsonld_types:
        print("JSON-LD types: " + ", ".join(f"{k} ({v})" for k, v in jsonld_types.most_common()))
    if redirects:
        print(f"Redirects: {len(redirects)}")
    if no_html:
        print(f"\nWARNING: {no_html} fetched records had no HTML, so they were not checked. "
              'For a Browser Run crawl, use "formats": ["html"].')
    if not_crawled:
        print(f"\nInternal links not in this crawl: {len(not_crawled)} (limit, patterns or robots; status unknown)")

    def section(heading, found):
        print(f"\n## {heading}")
        if not found:
            print("\nNone found in the checked fields.")
        for name in sorted(found):
            items = found[name]
            print(f"\n### {name} ({len(items)})")
            for item in items[: args.max]:
                print(f"- {item}")
            if len(items) > args.max:
                print(f"- ... and {len(items) - args.max} more")

    section("Issues", issues)
    section("Notes", notes)

    if args.text_dir:
        with open(os.path.join(args.text_dir, "INDEX.tsv"), "w", encoding="utf-8") as f:
            f.write("file\tlang\twords\turl\ttitle\tdescription\n" + "\n".join(pages_index) + "\n")
        print(f"\nPage text: {len(pages_index)} files in {args.text_dir}, listed in INDEX.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
