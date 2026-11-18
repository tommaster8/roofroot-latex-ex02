# INC-004 — Section / figure numbers reversed everywhere ("1.3" for 3.1)

| | |
|---|---|
| **Found by** | **Human lead** — visual pass on the full 42-page build (not reported by any agent) |
| **Severity** | MAJOR — every cross-reference, caption and TOC line was wrong |
| **Fixed in** | `roofroot.cls` v1.1 |

## What happened
Figure 3.1 was captioned "איור 1.3"; subsection 3.1.1 appeared as "1.1.3"; the TOC listed
section 2.1 as "1.2". Only the section number inside the green `\colorbox` was correct.

## Root cause
The class loaded babel with `layout=tabular.counters.graphics`. The `counters` option is meant for
`bidi=default`; under `bidi=basic` it typesets each digit of a compound counter as a separate run,
and the RTL paragraph then orders those runs right-to-left. `\colorbox` was immune because it builds
an `\hbox`, which babel's Lua bidi treats as one unit.

Proven objectively with `pdftotext -bbox-layout`: with `counters`, the PDF contained only
single-digit words (`>1< >3<`); without it, whole numbers (`>3.1< >3.1.1<`).

## Why it was not detected
1. The class test page (v1.0) had only chapter 1 / section 1.1, and "1.1" reads the same in both directions. **The test data could not reveal the bug.**
2. The writers' isolated builds contained a single chapter, which was numbered 1 again.
3. `qa_scan.py` reads `.tex` and `.log`, where nothing is wrong.

## Fix
Removed `counters` from the babel layout options. Bumped the cls version to v1.1, with a CHANGELOG entry.

## Prevention
- The class test now uses chapter ≥ 3 with a subsection and a figure, so that numbers are asymmetric.
- New `qa-BiDi` check: the glyph probe must find multi-digit counter words, e.g. `pdftotext -bbox-layout main.pdf - | grep -c '>[0-9]\+\.[0-9]\+<'` must be > 0.
