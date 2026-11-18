---
name: qa-BiDi
description: Checks right-to-left / left-to-right correctness in mixed Hebrew–English LaTeX (babel bidi=basic, LuaLaTeX). Use when reviewing Hebrew text that contains English terms, numbers, code or punctuation.
---
# qa-BiDi — bidirectional text

## Rules (what correct looks like)
| # | Rule | Wrong | Right |
|---|---|---|---|
| B1 | English term in Hebrew sentence → `\en{}` when it has spaces, digits or punctuation | `Business Model Canvas.` | `\en{Business Model Canvas}.` |
| B2 | Hebrew prefix + English → maqaf hyphen | `ה\en{SaaS}` | `ה-\en{SaaS}` |
| B3 | Negative numbers / ranges in Hebrew context are LTR | `-1,413` (renders `1,413-`) | `\en{-1,413}` |
| B4 | Code is always LTR (`pythonbox` forces it via cls hook) | Python in plain verbatim | `\begin{pythonbox}` |
| B5 | Parentheses must mirror correctly — check the PDF, not the source | `)RootOS(` | `(RootOS)` |
| B6 | `\textbullet` has no glyph in David CLM | `\textbullet` | `itemize` or `$\bullet$` |
| B7 | Units/currency: `\shekel` after the number in Hebrew | `₪24` in Hebrew | `24~\shekel` |
| B8 | Chart labels are English (matplotlib cannot shape RTL); captions are Hebrew | Hebrew in matplotlib | English axis + Hebrew `\caption` |

## How to check
1. `grep -nP '[\x{05D0}-\x{05EA}]\\en\{' chapters/*.tex` (B2)
2. Render pages and look at every line that mixes scripts: is the reading order right-to-left with English islands read left-to-right?
3. Check table columns with negative numbers, footer, header banner, TOC entries with English.

## Known root causes (from incidents)
- INC-001: listings lines inherited RTL → fixed by `\lst@AddToHook{Init}{\selectlanguage{english}...}` in cls.
- INC-003: minus sign jumped to the right in tables → generator wraps numbers in `\en{}`.

## Objective probe (don't trust your eyes at 60 dpi)
Visual order of a mixed run is easy to misread in a low-res render. Confirm with glyph coordinates:
```bash
pdftotext -bbox-layout main.pdf - | grep -o '>[^<]*rowcolor[^<]*<'   # → >\rowcolor<  = correct LTR island
```
`pdftotext` rebuilds each word from glyph x-positions, so `>1,413-<` proves a real reversal while
`>-1,413<` proves the run is fine. (Lesson from a false alarm during appendix review.)
- INC-004: babel `layout=counters` under `bidi=basic` reversed every compound number (3.1 → 1.3).
  Guard: `pdftotext -bbox-layout main.pdf - | grep -c '>[0-9]\+\.[0-9]\+<'` must be > 0
  (automated in `qa_scan.py::check_pdf_numbers`). Test with **asymmetric** numbers (≥ 3.1), never 1.1.
