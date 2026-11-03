# Site audit rules

Checked against the sources on 2026-11-04. Each rule names its source; the list is at the end. Google's rules are the strongest evidence. Rules marked **(vendor)** or **(study)** rest on weaker evidence, so say so when you report them. If one conflicts with Google, follow Google.

## Technical

| ID | Rule | Source |
|---|---|---|
| T1 | Main content, navigation links, titles, canonicals and structured data are in the server's HTML. "Not all bots can run JavaScript." In December 2024 Vercel's data showed none of the major AI crawlers rendering it **(vendor, dated)** | js, vercel |
| T2 | Links are `<a href>` with a real URL, not script events or `javascript:`. "Every page you care about should have a link from at least one other page" | links |
| T3 | One canonical per page, self-referencing unless the page is a deliberate variant. JavaScript doesn't change it | js |
| T4 | Missing pages return a real 404, with no soft 404s. Internal links point at the final URL, not at redirects or errors | js, move |
| T5 | `noindex` is deliberate, is off on production, and isn't set or removed by JavaScript | js |
| T6 | `robots.txt` doesn't block search crawlers or the assets pages need, keeps private routes out, and names the sitemap. The sitemap lists each language's canonical URLs and no redirects | ai, move |
| T7 | Each language version lists itself and all others. Return links exist on both sides, URLs are absolute, codes are valid, and `x-default` covers unmatched languages | hreflang |
| T8 | One language per page, with no side-by-side translations. No automatic redirect by language or IP | multi |
| T9 | Code that builds titles and descriptions doesn't cut them mid-phrase, doesn't fill them from body or legal text, and localises them | title, snippet |
| T10 | Structured data is "a true representation of the page content", marks up nothing hidden, stays current, has its required properties, and validates. No self-written reviews | sd, gen-ai |
| T11 | Don't add `FAQPage` markup for a rich result: Google stopped showing FAQ rich results on 7 May 2026. Report existing markup as a note, not an error | updates |
| T12 | Content images use `<img>` with a fallback `src`, sit near relevant text, and have short, descriptive filenames. Google doesn't index CSS images | images |
| T13 | Old URLs redirect permanently to their real equivalent, directly, for at least a year. Many URLs must not point to one irrelevant page such as the home page | move |
| T14 | Routes use real paths, not `#` fragments, to load different content | js |
| T15 | The main content is easy to tell apart from the rest of the page, for instance with `<main>` | ai-blog |

Speed belongs to `/seo-aeo:perf-audit`, not this audit.

## Copy

| ID | Rule | Source |
|---|---|---|
| C1 | The page gives something a generic page couldn't: original information, first-hand experience, specifics. Google asks for "unique, non-commodity content" | helpful, ai-blog |
| C2 | It's clear who is behind the content. Bylines are accurate where readers expect them, and no creator is fabricated | helpful |
| C3 | Titles are descriptive and concise, end cleanly rather than cut off mid-phrase, and have no repeated keywords or boilerplate. The brand appears briefly at the start or end | title |
| C4 | Title, H1 and description agree with each other **(vendor)** | ms |
| C5 | Descriptions are unique to the page, say what's on it, read as complete sentences in the page's language, and aren't strings of keywords | snippet |
| C6 | Headings are specific and work like chapter titles. Where people ask a question, the heading can be that question **(vendor)** | ms |
| C7 | Under such a heading, the first one or two sentences answer it, and they make sense when lifted out on their own **(vendor)** | ms |
| C8 | Claims are measurable: a specific figure, not "cutting-edge" **(vendor)** | ms |
| C9 | Steps and comparisons use lists or tables, and there are no long walls of text **(vendor)** | ms |
| C10 | Key facts aren't only in PDFs, in images, or in content a crawler can't see **(vendor)** | ms |
| C11 | Link text is descriptive and makes sense read alone, unlike "click here". Keywords aren't crammed in | links |
| C12 | Alt text is useful, not stuffed with keywords. On image links it serves as the link text | images, links |
| C13 | No thin near-duplicate pages made to catch queries. Many generated pages without added value can count as scaled content abuse | gen-ai, spam |
| C14 | Each language version is in that language throughout: body, labels, units, and text from a database or CMS. Google asks for one language per page and warns against translating only the boilerplate | multi |
| C15 | Dates change only when the content has substantially changed | helpful |
| C16 | Text is easy to understand and flows well: this gained 15–30% in one study, while keyword stuffing did worse than no change **(study)** | geo |

## AEO

Google says no special optimisation or schema is needed for AI Overviews or AI Mode, so none of this is a Google ranking factor. The rest aims at getting read and cited by assistants generally.

| ID | Rule | Source |
|---|---|---|
| A1 | A reader can quickly find who the business is, what it offers and where. The name is the same everywhere, and the Organization data matches the page | sd, ai |
| A2 | Pages answer the follow-up questions people ask, not just the first one. Use real queries if the repo or owner has them, and don't invent demand | ai-blog |
| A3 | Sources, quotations and statistics gained 30–40% in one study, but results varied by domain. Only suggest ones that are real and sourced; ask the owner for them **(study)** | geo |
| A4 | Text is supported by high-quality images and video where they help | ai, ai-blog |
| A5 | `nosnippet`, `data-nosnippet` and `max-snippet` aren't limiting what can be quoted, unless that's intended | ai, ai-blog |
| A6 | AI crawler rules match the owner's recorded decision | ai |
| A7 | If `llms.txt` exists, it follows the spec and agrees with the site. It's optional, and not a Google factor | llms |
| A8 | Structured data supports the text and doesn't replace it | sd, ai |

## Facts

| ID | Rule | Source |
|---|---|---|
| F1 | One fact has one value everywhere: across pages, languages, metadata, structured data and `llms.txt`. Check names, addresses, phone numbers, prices, dates, counts and specifications | sd, gen-ai |
| F2 | Nothing is stale: past years or seasons, old prices, "new" on old things | sd, helpful |
| F3 | Nothing unfinished ships: placeholders, TODOs, test data, or preview text that production would show | helpful |
| F4 | Strong claims such as "best", "award-winning" or any figure can be backed up. If the repo shows no proof, ask the owner; don't call it false | helpful, ms |
| F5 | Reviews and testimonials are real, not self-written | sd, spam |
| F6 | Facts the repo marks as unconfirmed are reported as unconfirmed, not treated as true | gen-ai |
| F7 | Text and metadata written by AI have been checked by a person | gen-ai |

## Sources

| Key | Source |
|---|---|
| ai | https://developers.google.com/search/docs/appearance/ai-features |
| ai-blog | https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search |
| gen-ai | https://developers.google.com/search/docs/fundamentals/using-gen-ai-content |
| geo | Aggarwal et al., KDD 2024: https://arxiv.org/abs/2311.09735. Tested mainly on the authors' own engine, with a Perplexity subset |
| helpful | https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| hreflang | https://developers.google.com/search/docs/specialty/international/localized-versions |
| images | https://developers.google.com/search/docs/appearance/google-images |
| js | https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics |
| links | https://developers.google.com/search/docs/crawling-indexing/links-crawlable |
| llms | https://llmstxt.org/ |
| move | https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes |
| ms | https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers |
| multi | https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites |
| sd | https://developers.google.com/search/docs/appearance/structured-data/sd-policies |
| snippet | https://developers.google.com/search/docs/appearance/snippet |
| spam | https://developers.google.com/search/docs/essentials/spam-policies |
| title | https://developers.google.com/search/docs/appearance/title-link |
| updates | https://developers.google.com/search/updates |
| vercel | https://vercel.com/blog/the-rise-of-the-ai-crawler |
