---
name: practical-typography
description: >
  Helps agents produce well-typeset text by applying the key rules from
  Butterick's Practical Typography. Use this skill whenever writing or
  editing prose, documentation, web content, HTML/CSS, or any
  reader-facing text. It covers proper punctuation characters, emphasis,
  spacing, capitalization, layout fundamentals, and font guidance.
---

# Practical Typography

Apply the following typography rules whenever you produce or edit text.
These rules are adapted from Butterick's *Practical Typography*
(practicaltypography.com). Consult `references/typography-rules-complete.md`
for detailed explanations, character codes, and implementation guidance.

## Text & Punctuation Rules

### 1. Curly Quotes, Not Straight

Always use curly (typographer's) quotation marks and apostrophes, never
straight (typewriter) marks.

- Opening double: `"` (U+201C) — Closing double: `"` (U+201D)
- Opening single: `'` (U+2018) — Closing single / apostrophe: `'` (U+2019)
- Straight marks `"` and `'` are only correct for foot (′) and inch (″) marks.

### 2. Proper Apostrophes

Apostrophes always curve downward (same character as a closing single
quote: `'` U+2019). Watch for leading apostrophes in contractions of
years or omitted letters (`'90s`, not `'90s`).

### 3. Hyphens and Dashes — Never Fake Them

Three distinct marks exist — use them correctly:

| Mark | Character | Usage |
|------|-----------|-------|
| Hyphen | `-` | Compound words, phrasal adjectives, line breaks |
| En dash | `–` (U+2013) | Ranges (1990–2000, pages 15–20), connections |
| Em dash | `—` (U+2014) | Sentence breaks — stronger than a comma, softer than a period |

Never approximate dashes with double hyphens (`--`) or triple hyphens (`---`).

### 4. Proper Ellipsis Character

Use the single ellipsis character `…` (U+2026), not three periods (`...`).
Typically add a space before and after: `word … word`.

### 5. One Space Between Sentences

Always put exactly one space after a period (or any punctuation). Never
two. The two-space habit is a typewriter-era relic with no place in
modern typography.

### 6. No Multiple Consecutive Spaces

Never use multiple word spaces in a row. One space between words, always.

### 7. Trademark and Copyright Symbols

Use the real symbols — never alphabetic approximations:

- `©` (U+00A9) not `(c)` — `™` (U+2122) not `(TM)` — `®` (U+00AE) not `(R)`
- No space before ™ or ®. Use a nonbreaking space between © and the year.

### 8. Foot and Inch Marks

Foot (′) and inch (″) marks must be straight/prime characters, never
curly quotes. Use `′` (U+2032) and `″` (U+2033), or straight ASCII
quotes as a fallback: `5'10"`.

### 9. Nonbreaking Spaces

Use a nonbreaking space (`&nbsp;` in HTML) to glue together elements
that should never split across lines: after § and ¶ marks, between
numbers and units, and between © and the year.

### 10. Paragraph and Section Marks

Use `§` (U+00A7) for section references and `¶` (U+00B6) for paragraph
references. Always follow with a nonbreaking space. Double them for
plurals: `§§ 12–14`. Spell out the word at the start of a sentence.

## Emphasis & Formatting Rules

### 11. Bold or Italic — Sparingly, Never Together

- Use **bold** or *italic* for emphasis, but not both simultaneously.
- In serif text, prefer *italic* for gentle emphasis, **bold** for strong.
- In sans-serif text, prefer **bold** (sans italic is often too subtle).
- If everything is emphasized, nothing is. Keep emphasized passages short.

### 12. Never Underline

Underlining is a typewriter-era workaround. Modern text has bold and
italic. The only acceptable underline is for web hyperlinks, and even
that is debatable.

### 13. All Caps: One Line Maximum

ALL CAPS are acceptable for short headings, labels, and captions — never
for entire paragraphs. They reduce readability because capital letters
have uniform rectangular shapes, eliminating the distinctive word
contours readers rely on.

When using all caps, add 5–12% letterspacing for readability.

### 14. Centered Text: Use Sparingly

Centered text works for short titles and headings. Never center entire
paragraphs or text blocks — both edges become ragged, hurting
readability. Left-aligned is the default for body text.

### 15. Exclamation Points: Budget Strictly

For any document longer than three pages, one exclamation point is
plenty. Never stack multiple exclamation points (`!!!`). Their impact
comes from scarcity.

### 16. Ampersands: Only in Proper Names

Use `&` in proper names and brand identities (AT&T, Johnson & Johnson).
In running text, write out "and." The more formal the document, the
fewer ampersands.

## Layout & Typesetting Rules

Apply these when generating HTML/CSS, document templates, or advising on
document design.

### 17. The Four Pillars of Body Text

The four most important typographic decisions for body text:

1. **Point size**: 10–12 pt in print; 15–25 px on the web
2. **Line spacing**: 120–145% of the point size
3. **Line length**: 45–90 characters per line (including spaces)
4. **Font**: A professional typeface suited to the medium

### 18. Font Selection

- Prefer professional fonts over system defaults.
- Avoid goofy fonts (novelty, script, handwriting), monospaced fonts for
  body text, and overused defaults (Times New Roman, Arial, Comic Sans).
- For print body text, prefer serif. For web, both serif and sans-serif
  work well on modern screens.
- If a free font is needed: Charter, Source Serif, IBM Plex, or Cooper
  Hewitt are solid choices.

### 19. Kerning and Letterspacing

- **Kerning** (pair-level spacing) should always be turned on.
- **Letterspacing**: Add 5–12% extra space for ALL CAPS and small caps.
  Never letterspace lowercase body text.

### 20. Small Caps

Only use real small caps (designed into the font), never faked ones
generated by the word processor. If the font lacks true small caps,
don't use small caps at all.

### 21. Paragraph Separation

Use **either** first-line indents **or** space between paragraphs — never
both.

- First-line indents: 1–4× the point size. Skip the indent on the first
  paragraph after a heading.
- Paragraph spacing: 4–10 pt of space after each paragraph.

### 22. Justified Text Requires Hyphenation

If text is justified (flush left and right), hyphenation must be enabled.
Without it, word spacing becomes grotesquely uneven. Left-aligned text
does not require hyphenation but may benefit from it.

## Quick Reference: Characters

| Character | Unicode | HTML | Mac | Windows |
|-----------|---------|------|-----|---------|
| " (open double quote) | U+201C | `&ldquo;` | Opt+[ | Alt 0147 |
| " (close double quote) | U+201D | `&rdquo;` | Opt+Shift+[ | Alt 0148 |
| ' (open single quote) | U+2018 | `&lsquo;` | Opt+] | Alt 0145 |
| ' (close single / apostrophe) | U+2019 | `&rsquo;` | Opt+Shift+] | Alt 0146 |
| – (en dash) | U+2013 | `&ndash;` | Opt+- | Alt 0150 |
| — (em dash) | U+2014 | `&mdash;` | Opt+Shift+- | Alt 0151 |
| … (ellipsis) | U+2026 | `&hellip;` | Opt+; | Alt 0133 |
| © (copyright) | U+00A9 | `&copy;` | Opt+G | Alt 0169 |
| ™ (trademark) | U+2122 | `&trade;` | Opt+2 | Alt 0153 |
| ® (registered) | U+00AE | `&reg;` | Opt+R | Alt 0174 |
| § (section) | U+00A7 | `&sect;` | Opt+6 | Alt 0167 |
| ¶ (paragraph) | U+00B6 | `&para;` | Opt+7 | Alt 0182 |
| ′ (prime / foot) | U+2032 | `&prime;` | — | — |
| ″ (double prime / inch) | U+2033 | `&Prime;` | — | — |
| (nonbreaking space) | U+00A0 | `&nbsp;` | Opt+Space | Ctrl+Shift+Space |
