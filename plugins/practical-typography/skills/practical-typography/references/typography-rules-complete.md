# Practical Typography — Complete Rules Reference

Comprehensive reference adapted from Butterick's *Practical Typography*
(practicaltypography.com). This document provides detailed explanations,
rationale, and implementation guidance for every rule.

## Table of Contents

1. [Curly Quotes](#1-curly-quotes)
2. [Apostrophes](#2-apostrophes)
3. [Hyphens and Dashes](#3-hyphens-and-dashes)
4. [Ellipses](#4-ellipses)
5. [One Space Between Sentences](#5-one-space-between-sentences)
6. [No Multiple Word Spaces](#6-no-multiple-word-spaces)
7. [Trademark and Copyright Symbols](#7-trademark-and-copyright-symbols)
8. [Foot and Inch Marks](#8-foot-and-inch-marks)
9. [Nonbreaking Spaces](#9-nonbreaking-spaces)
10. [Paragraph and Section Marks](#10-paragraph-and-section-marks)
11. [Bold and Italic](#11-bold-and-italic)
12. [Underlining](#12-underlining)
13. [All Caps](#13-all-caps)
14. [Centered Text](#14-centered-text)
15. [Exclamation Points and Question Marks](#15-exclamation-points-and-question-marks)
16. [Ampersands](#16-ampersands)
17. [Body Text Fundamentals](#17-body-text-fundamentals)
18. [Point Size](#18-point-size)
19. [Line Spacing](#19-line-spacing)
20. [Line Length](#20-line-length)
21. [Font Selection](#21-font-selection)
22. [System Fonts](#22-system-fonts)
23. [Kerning and Letterspacing](#23-kerning-and-letterspacing)
24. [Small Caps](#24-small-caps)
25. [Paragraph Separation and First-Line Indents](#25-paragraph-separation-and-first-line-indents)
26. [Justified Text and Hyphenation](#26-justified-text-and-hyphenation)

---

## 1. Curly Quotes

Curly quotes (also called typographer's quotes or smart quotes) are the
standard in professionally typeset text. Straight quotes are a
typewriter legacy and should never appear in finished text.

### The Characters

| Purpose | Correct (Curly) | Wrong (Straight) |
|---------|-----------------|------------------|
| Opening double quote | `"` U+201C | `"` U+0022 |
| Closing double quote | `"` U+201D | `"` U+0022 |
| Opening single quote | `'` U+2018 | `'` U+0027 |
| Closing single quote | `'` U+2019 | `'` U+0027 |

### Rules

- Double quotes enclose primary quotations. Single quotes enclose
  quotations nested inside double quotes.
- In American English, periods and commas go inside closing quotation
  marks. Colons and semicolons go outside. Question marks and exclamation
  points go inside if they belong to the quoted material, outside if they
  belong to the enclosing sentence.
- Most word processors and web platforms auto-convert straight quotes to
  curly. In HTML, use `&ldquo;` `&rdquo;` `&lsquo;` `&rsquo;` or the
  Unicode code points directly.

### Common Mistakes

- Using straight quotes anywhere in finished prose.
- Using backtick-style quotes (`` ` ``) in place of proper opening
  single quotes.
- Forgetting that an apostrophe is the same character as a closing single
  quote (`'` U+2019), not a straight mark.

---

## 2. Apostrophes

The apostrophe is identical to the closing single quotation mark:
`'` (U+2019). It always curves to the right (toward the omitted letters).

### Rules

- Contractions: `don't`, `it's`, `I'm`, `you're`, `they've`.
- Possessives: `the writer's`, `James's`, `the Joneses'`.
- Omitted characters: `rock 'n' roll`, `the '90s`.

### The Leading-Apostrophe Trap

When a word starts with an apostrophe (like `'90s` or `'tis`), many
auto-correct systems insert an opening single quote (`'`) instead of an
apostrophe (`'`). This is wrong — the character should curl to the right
because it replaces omitted characters, not because it opens a
quotation. Manual correction is often required.

---

## 3. Hyphens and Dashes

Three marks that look similar but serve entirely different purposes.
Approximating them is a hallmark of amateur typography.

### Hyphen (`-`)

- Used in compound words (`well-known`, `editor-in-chief`), phrasal
  adjectives before a noun (`high-quality work`), and for word breaks at
  the end of a line.
- No spaces on either side in compound words.
- The only one available on a standard keyboard.

### En Dash (`–` U+2013)

- Indicates ranges: `2010–2020`, `pages 40–50`, `Monday–Friday`.
- Shows a connection or contrast between pairs: `New York–London flight`,
  `liberal–conservative debate`.
- Typically no spaces around it in ranges, though some style guides
  prefer spaces when used as a sentence pause (British convention).
- In HTML: `&ndash;`
- On Mac: `Option + Hyphen`
- On Windows: `Alt + 0150`

### Em Dash (`—` U+2014)

- The sentence-level punctuation mark — it creates a break stronger than
  a comma but less formal than a colon.
- Can replace commas, colons, parentheses, or semicolons for variety and
  emphasis.
- Typically used without spaces in American English. Some British and
  European styles use spaces.
- In HTML: `&mdash;`
- On Mac: `Option + Shift + Hyphen`
- On Windows: `Alt + 0151`

### What to Avoid

- Double hyphens (`--`) as a substitute for em dashes. This is a
  typewriter habit.
- Triple hyphens (`---`) for em dashes. Same problem.
- Using en dashes where em dashes belong, or vice versa.

---

## 4. Ellipses

The ellipsis indicates omitted material or a trailing-off thought.

### Rules

- Use the single ellipsis character `…` (U+2026), not three separate
  periods (`...`). Three periods produce uneven spacing and can break
  across lines.
- In HTML: `&hellip;`
- When the ellipsis follows a complete sentence, place a period first,
  then the ellipsis: `The trial ended. … The verdict came later.`
- Add a space before and after the ellipsis in running text.

### Usage

- Indicating omitted words in a quotation.
- Showing a thought trailing off: `I was thinking …`
- Do not use ellipses to create suspense in formal writing. They are for
  omission, not dramatic effect.

---

## 5. One Space Between Sentences

Put exactly one space between sentences — never two. This is the single
most common typographic error and also the easiest to fix.

### Why One Space

- Two spaces create distracting white gaps that disrupt the visual
  texture of a paragraph.
- They can produce "rivers" — vertical streams of whitespace — in
  justified text.
- Every major style guide mandates single spacing: The Chicago Manual of
  Style (rule 2.9), Robert Bringhurst's *Elements of Typographic Style*,
  and James Felici's *Complete Manual of Typography* all agree.

### Historical Context

Two spaces originated with monospaced typewriter fonts where every
character (including the period) occupied the same width, making sentence
boundaries hard to spot. Proportional fonts render this unnecessary
because the period already occupies less horizontal space than letters.

### Exception

Two spaces are tolerable (but still unnecessary) only in monospaced
fonts like Courier, where the original typewriter rationale still
loosely applies.

### How to Fix

- Find and replace `  ` (two spaces) with ` ` (one space) globally.
- Repeat until no double spaces remain (replacing two with one may leave
  residual doubles if there were three or more).

---

## 6. No Multiple Word Spaces

Never use more than one consecutive word space. This extends the
one-space-between-sentences rule to all text. Multiple spaces create
visual holes and misalignment.

### Common Violations

- Using spaces to align text in columns (use tabs or tables instead).
- Adding extra spaces after colons or other punctuation.
- Using spaces to create indentation (use proper indent settings).

---

## 7. Trademark and Copyright Symbols

Use the real Unicode symbols, not alphabetic approximations.

### The Symbols

| Symbol | Unicode | HTML | Keyboard (Mac) | Keyboard (Win) |
|--------|---------|------|-----------------|-----------------|
| © | U+00A9 | `&copy;` | Opt+G | Alt 0169 |
| ™ | U+2122 | `&trade;` | Opt+2 | Alt 0153 |
| ® | U+00AE | `&reg;` | Opt+R | Alt 0174 |

### Rules

- No space before ™ or ® (they attach to the preceding word like
  superscripts): `Kleenex®`.
- Use a nonbreaking space between © and the year: `©`&nbsp;`2024`.
- Never write `(c)`, `(TM)`, or `(R)` — these are ASCII workarounds
  from an era when the real symbols were unavailable.

---

## 8. Foot and Inch Marks

Foot marks (′) and inch marks (″) are straight/prime characters, not
curly quotation marks.

### The Characters

| Symbol | Meaning | Unicode | HTML |
|--------|---------|---------|------|
| ′ | Prime (feet, arcminutes) | U+2032 | `&prime;` |
| ″ | Double prime (inches, arcseconds) | U+2033 | `&Prime;` |

### Rules

- `He was 6′2″ tall` — use primes.
- `She said "hello"` — use curly quotes.
- Smart-quote features may incorrectly curl prime marks. Watch for this
  in contexts mixing quotations with measurements.
- If true prime characters are unavailable, straight ASCII `'` and `"`
  are acceptable fallbacks for measurements.

---

## 9. Nonbreaking Spaces

A nonbreaking space prevents a line break between two elements that
should stay together on the same line.

### When to Use

- After `§` and `¶` marks: `§ 12` should never split.
- Between a number and its unit: `25 kg`, `100 m`.
- Between `©` and the year: `© 2024`.
- Between components of proper names: `Dr. Smith`.
- Between month and day in dates: `January 1`.

### How to Insert

- HTML: `&nbsp;`
- Unicode: U+00A0
- Mac: `Option + Space`
- Windows: `Ctrl + Shift + Space`

---

## 10. Paragraph and Section Marks

### Section Mark (`§` U+00A7)

- Used to refer to specific sections: `§ 5`, `§§ 12–14` (doubled for
  plural).
- Always follow with a nonbreaking space.
- Spell out "Section" at the start of a sentence.

### Paragraph Mark (`¶` U+00B6)

- Used to refer to specific paragraphs: `¶ 3`, `¶¶ 7–9`.
- Same spacing rules as the section mark.
- Spell out "Paragraph" at the start of a sentence.

### In HTML

- `&sect;` for §
- `&para;` for ¶

---

## 11. Bold and Italic

Bold and italic are the two standard methods of emphasis in typeset text.

### Rules

- Use one or the other, **never both simultaneously**. If bold italic
  were needed, type designers would make it a separate style.
- **Bold** creates strong emphasis. It works well in both serif and
  sans-serif text.
- *Italic* creates gentle emphasis. It works best in serif fonts because
  serif italics have distinctive letterforms. Sans-serif italics are
  often just slanted versions of the roman forms and may not provide
  enough visual contrast.
- Keep emphasized passages short — a word, a phrase, perhaps a sentence.
  Emphasizing entire paragraphs defeats the purpose.
- If you need emphasis beyond what bold or italic provides, consider
  restructuring the text rather than adding more formatting.

### Common Mistakes

- Using bold and italic together for "extra" emphasis.
- Emphasizing too much text, which dilutes the impact of all emphasis.
- Using bold for entire paragraphs.
- Neglecting emphasis entirely, producing flat, monotonous text.

---

## 12. Underlining

**Never underline.** It is ugly, it reduces readability, and it is a
relic of the typewriter era.

### Why Underlining Is Bad

- Underlining was a typewriter convention invented because typewriters
  could not produce bold or italic. There is no longer any excuse.
- Underlines collide with descenders (the tails of g, j, p, q, y),
  making text harder to read.
- No professionally typeset book, newspaper, or magazine uses
  underlining for emphasis.

### Alternatives to Underlining

- **Bold** for strong emphasis
- *Italic* for gentle emphasis
- ALL CAPS for headings (sparingly)
- Small caps where available
- Larger or different-weight type for hierarchy

### The Hyperlink Exception

Underlined hyperlinks on the web are the one context where underlining
is widely accepted. Even here, many major publications (The New York
Times, The Washington Post, The Guardian, Google, Apple, Microsoft) use
underlines sparingly or not at all, preferring color to indicate links.

---

## 13. All Caps

ALL CAPS can work in small doses — headings, labels, acronyms, captions.
They fail completely for body text.

### Why All Caps Hurts Readability

- Readers recognize words partly by their shape (ascenders and
  descenders create distinctive silhouettes). All caps eliminates these
  shapes, producing uniform rectangles.
- Reading speed drops significantly for text set entirely in capitals.
- It also conveys SHOUTING in digital communication.

### Rules

- Limit all caps to one line or a few words.
- When using all caps, add **5–12% letterspacing**. Capital letters are
  designed to sit next to lowercase letters; when placed next to each
  other, they feel cramped without extra space.
- In CSS: `text-transform: uppercase; letter-spacing: 0.05em;`
- Never set body text in all caps.

---

## 14. Centered Text

Centering creates two ragged edges instead of one, making text harder to
read and harder to scan.

### When Centering Works

- Short titles and headings
- Single-line captions
- Invitations and formal announcements
- Poetry (traditionally)

### When Centering Fails

- Body paragraphs
- Lists
- Any text block longer than a few lines
- Navigation and UI elements (usually better left-aligned)

### Default

Left-aligned (flush left, ragged right) is the safest and most readable
alignment for body text. Use it as the default; deviate only with good
reason.

---

## 15. Exclamation Points and Question Marks

### Exclamation Points

Give yourself a budget of **one exclamation point per document** for
anything longer than three pages. Their power comes from rarity.

- Never stack multiple exclamation points (`!!!`).
- Never combine exclamation and question marks (`?!`) except in the most
  casual contexts.
- If your writing needs exclamation points to convey energy, the writing
  itself needs work. Strong words carry their own emphasis.

### Question Marks

Question marks are underused. You can make a topic sentence pithier and
more engaging by presenting it as a question.

- Weak: `This section discusses the benefits of solar energy.`
- Strong: `Why is solar energy so beneficial?`

Questions create a contract with the reader — they promise an answer is
coming, which builds momentum.

### The Interrobang

The interrobang (`‽` U+203D) combines `?` and `!` into a single glyph.
Invented in 1962, it remains a curiosity rather than a standard mark.
Avoid it in formal writing.

---

## 16. Ampersands

The ampersand (`&`) is a ligature of the Latin word *et* ("and"). It is
decorative but should be used sparingly.

### Rules

- Use `&` only in proper names and trademarks: `AT&T`,
  `Johnson & Johnson`, `Tiffany & Co.`
- In running text, write out "and."
- The more formal the document, the fewer ampersands.
- Acceptable in headings, tables, and other space-constrained contexts.

---

## 17. Body Text Fundamentals

Body text is the most common element of any document. Getting it right
is the single most impactful thing you can do for typography.

### The Four Pillars

Every body-text design decision flows from four choices:

1. **Font** — The typeface family
2. **Point size** — How large the characters are
3. **Line spacing** — Vertical distance between baselines
4. **Line length** — How many characters fit on one line

Set these first. Everything else in the document flows from them.

### Workflow

1. Choose a font appropriate to the medium (print vs. screen) and tone.
2. Set the point size.
3. Adjust line spacing to 120–145% of the point size.
4. Constrain line length to 45–90 characters.
5. Then design headings, captions, and other elements relative to the
   body text.

---

## 18. Point Size

### For Print

- Body text: **10–12 points**
- This is smaller than most people expect. Word-processor defaults of
  12 pt often produce text that looks too large in professional contexts.
- The "right" size depends on the font — some fonts run large at a given
  point size, others small.

### For the Web

- Body text: **15–25 pixels**
- Screen resolution is lower than print, so text needs to be larger for
  equivalent readability.
- `1 px ≈ 0.75 pt` as a rough conversion.

### Testing

- Print a test page and read it at the intended distance.
- On screen, view at 100% zoom on the target device.
- Never judge point size by how it looks in your word processor at a
  non-100% zoom level.

---

## 19. Line Spacing

Line spacing (leading) is the vertical distance between baselines of
successive lines of text.

### Optimal Range

**120–145% of the point size.** For 12 pt text, that means 14.4–17.4 pt
of line spacing.

### Why Defaults Are Wrong

- "Single spacing" in word processors is typically 120% — the bare
  minimum of the acceptable range.
- "Double spacing" is 240% — far too much for anything except draft
  manuscripts.
- "1.5 spacing" is 180% — still above the optimal range.

### Implementation

- **Word**: Format → Paragraph → Line Spacing → "Exactly" with a fixed
  measurement. Or use "Multiple" with values of 1.03–1.24.
- **CSS**: `line-height: 1.4;` (unitless values are preferred because
  they scale with font size).
- **Pages**: "Exactly" for fixed, or "Lines" with 1.03–1.29.

### Considerations

- Fonts that render small at a given point size may need slightly less
  line spacing.
- Longer lines need more line spacing (the eye needs help tracking back
  to the left margin).
- Shorter lines can tolerate less line spacing.

---

## 20. Line Length

Line length (measure) is the horizontal width of a text block, typically
counted in characters per line.

### Optimal Range

**45–90 characters per line**, including spaces. The ideal is around
65–75 characters.

### Why It Matters

- Lines that are too short cause excessive hyphenation and too many eye
  jumps.
- Lines that are too long make it hard for the eye to find the beginning
  of the next line (a phenomenon called "doubling").
- This is why books, newspapers, and magazines use columns — to keep
  line lengths within the optimal range.

### Implementation

- **Print**: Adjust page margins to control line length.
- **CSS**: Use `max-width` on the text container. A `max-width` of
  `33em` produces roughly 66 characters per line.
- **Responsive web**: Ensure line length stays in range across screen
  sizes. Media queries can adjust `max-width` at breakpoints.

---

## 21. Font Selection

### Print Body Text

- **Prefer serif typefaces.** The vast majority of books, newspapers, and
  magazines use serif fonts for body text. This is the standard and the
  safest choice.
- Professional serif fonts: Equity, Miller, Minion, Sabon, Garamond,
  Baskerville, Charter.

### Web Body Text

- Both serif and sans-serif work on modern screens. Screen resolution has
  improved enough that serif fonts render cleanly.
- Professional web fonts: Concourse, Source Sans, IBM Plex Sans,
  Fira Sans, Equity, Source Serif, Charter.

### Fonts to Avoid

- **Comic Sans**: Universally derided in professional contexts.
- **Arial**: A design-inferior clone of Helvetica that gained dominance
  only through Microsoft bundling. The "sans serif of last resort."
- **Papyrus**: Associated with amateurism.
- **Times New Roman**: Not terrible but so overused as a default that it
  signals "I didn't bother to choose a font."
- **Monospaced fonts** (Courier, Consolas): Only for code. Never for
  body text.
- **Decorative/novelty fonts**: Script, handwriting, and display fonts
  are not for body text.

### Free Alternatives

If budget is a constraint:

- **Charter** (by Matthew Carter) — excellent free serif
- **Source Serif Pro** (by Adobe) — professional-quality free serif
- **IBM Plex** (by IBM) — comprehensive free family with serif, sans,
  and mono
- **Cooper Hewitt** (by Chester Jenkins) — clean free sans-serif

### Helvetica and Arial Alternatives

If you need a neutral sans-serif but want to avoid the blandness of
Helvetica or the inferiority of Arial:

- **Neue Haas Grotesk** — faithful revival of Helvetica's original design
- **Concourse** — neutral without being dull
- **Atlas** — excellent contemporary alternative
- **Source Sans Pro** — free, professional-quality neutral sans

---

## 22. System Fonts

System fonts (fonts pre-installed on your OS) have three problems:

1. **Quality**: Many are poorly designed. Arial is a cheap Helvetica
   knock-off; many decorative system fonts are amateurish.
2. **Screen optimization trade-offs**: Fonts designed for screen
   legibility at small sizes sacrifice the design details that make type
   beautiful in print.
3. **Overexposure**: Billions of computers have the same fonts.
   Using them signals "default" rather than "chosen."

### Tiered Rankings

**A tier (generally tolerable)**:
Helvetica, Garamond, Charter, Palatino — acceptable for print work.

**B tier (OK in limited contexts)**:
Calibri, Futura, Segoe UI — adequate for screen display, drafts,
and internal documents.

**C tier (use with caution)**:
Georgia, Times New Roman, Baskerville — technically competent but
overexposed or optimized for screen at the expense of print quality.

**F tier (fatal to credibility)**:
Comic Sans, Arial, Papyrus, Brush Script, Curlz, Jokerman, and all
novelty/decorative system fonts.

### Recommendation

Professional writers should invest in professional fonts. System fonts
are acceptable for screen-based work (email, internal documents, web
drafts) but fall short for any published or printed material.

---

## 23. Kerning and Letterspacing

### Kerning

Kerning adjusts the space between specific pairs of letters to create
visually even spacing. Without it, certain pairs (like `AV`, `To`, `Wa`)
look awkwardly spaced.

- **Always turn kerning on.** There is no reason to disable it.
- In CSS: `font-kerning: normal;` or `font-feature-settings: "kern";`
- In Word: Format → Font → Advanced → check Kerning

### Letterspacing (Tracking)

Letterspacing adjusts the spacing uniformly across all characters in a
word or block.

- **All caps and small caps**: Add 5–12% extra letterspacing. Capitals
  are designed to sit beside lowercase letters; without extra space, a
  block of capitals looks cramped.
- **Lowercase body text**: Never letterspace. It destroys the word
  shapes that make text readable.
- In CSS: `letter-spacing: 0.05em;` (for caps)

---

## 24. Small Caps

Small caps are uppercase letterforms designed at the height of lowercase
letters. They are used for abbreviations (NASA, FBI), acronyms in body
text, and stylistic applications.

### Rules

- Only use **true small caps** — letterforms specifically designed by the
  type designer.
- **Never use fake small caps** generated by the word processor (which
  simply shrinks full capitals). Faked small caps have thinner strokes
  than surrounding text and look visibly wrong.
- If the font lacks true small caps, do not use small caps at all.
  Regular capitals at a slightly smaller point size are a better fallback.
- In CSS: `font-variant: small-caps;` (only works if the font has real
  small caps in its OpenType features).

---

## 25. Paragraph Separation and First-Line Indents

Paragraphs need a visual signal to show where one ends and the next
begins. There are two methods — use one, never both.

### Method 1: First-Line Indents

- Indent the first line of each paragraph by **1–4× the point size**.
  For 12 pt text, a 12–48 pt indent (0.17–0.67 inches).
- **Do not indent the first paragraph** after a heading or subheading —
  the reader already knows where it starts.
- Do not use tabs or multiple spaces for indentation. Use the
  paragraph-formatting tools in your software.
- Adjust the indent size to the line length: narrower columns warrant
  smaller indents, wider columns can accommodate larger ones.

### Method 2: Space Between Paragraphs

- Add **4–10 points** of space after each paragraph.
- No first-line indent when using this method.
- This is the standard approach for web content, email, and screen-based
  documents.

### What Not to Do

- **Never combine both methods.** Using first-line indents and paragraph
  spacing simultaneously is a common mistake that creates visual clutter.
- **Never use a full blank line** between paragraphs in print. A full
  line is too much space.

### Implementation

- **CSS**: `p { margin-bottom: 0.5em; text-indent: 0; }` for paragraph
  spacing, or `p { text-indent: 1.5em; margin-bottom: 0; }` for indents.
- **Word**: Format → Paragraph → Indents and Spacing → set "First line"
  or "Space After."

---

## 26. Justified Text and Hyphenation

Justification (flush left and flush right) creates a clean, formal look
but introduces a critical dependency: hyphenation.

### The Rule

**If you justify text, you must enable hyphenation.** Without it, the
word-processor stretches word spaces to fill each line, producing
grotesque gaps — especially in narrow columns.

### Hyphenation Guidelines

- Enable automatic hyphenation in your software or CSS.
- In CSS: `hyphens: auto;` with `lang` attribute set on the HTML element.
- Limit consecutive hyphens to 2–3 lines maximum.
- Avoid hyphenating proper nouns, headings, and captions.

### Left-Aligned Text

Left-aligned (ragged right) text does not strictly require hyphenation,
but enabling it can reduce the raggedness of the right edge, producing
a more polished appearance.

### Recommendation

For most body text, **left-aligned with optional hyphenation** is the
safest choice. It avoids the word-spacing problems of justification while
maintaining excellent readability. Reserve justification for formal
documents, books, and contexts where the clean right edge is important.

---

## Summary of Key Rules at a Glance

| # | Rule | Quick Check |
|---|------|-------------|
| 1 | Curly quotes | `"` `"` `'` `'` not `"` `'` |
| 2 | Proper apostrophes | `'` (U+2019) not `'` |
| 3 | Correct dashes | `-` `–` `—` (three distinct marks) |
| 4 | Ellipsis character | `…` not `...` |
| 5 | One space after periods | `. Word` not `.  Word` |
| 6 | No multiple spaces | One space everywhere |
| 7 | Real symbols | `©` `™` `®` not `(c)` `(TM)` `(R)` |
| 8 | Straight primes | `′` `″` for feet/inches |
| 9 | Nonbreaking spaces | After `§` `¶`, between `©` and year |
| 10 | Section/paragraph marks | `§` `¶` with nonbreaking space |
| 11 | Bold or italic, not both | Pick one emphasis method |
| 12 | Never underline | Use bold, italic, or restructure |
| 13 | All caps ≤ 1 line | Add 5–12% letterspacing |
| 14 | Centered text sparingly | Left-align by default |
| 15 | One `!` per document | Use `?` more often |
| 16 | `&` only in proper names | Write out "and" otherwise |
| 17 | Four pillars of body text | Font, size, spacing, length |
| 18 | Point size | 10–12 pt print, 15–25 px web |
| 19 | Line spacing | 120–145% of point size |
| 20 | Line length | 45–90 characters per line |
| 21 | Professional fonts | Avoid Arial, Comic Sans, defaults |
| 22 | System font awareness | Tier your font choices |
| 23 | Kerning on, letterspacing caps | 5–12% for all caps |
| 24 | True small caps only | Never fake them |
| 25 | Indent OR spacing, not both | Skip indent on first paragraph |
| 26 | Justified = must hyphenate | Left-aligned is safest default |
