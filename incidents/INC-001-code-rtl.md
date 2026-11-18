# INC-001 — Python code rendered right-to-left

| | |
|---|---|
| **Found by** | Orchestrator, visual check of `test.tex` (render to PNG) |
| **Severity** | MAJOR (code unreadable) |
| **Fixed in** | `roofroot.cls` v1.0 (pre-release) → hook in listings |

## What happened
`def yield_kg(area_m2, cycles=12):` appeared as `:(12=cycles ,area_m2)yield_kg def`.
After a first fix the word order was right but parentheses were still mirrored: `yield_kg)area_m2(`.

## Root cause
`listings` typesets each code line in its own box. Under `babel` with `bidi=basic` and Hebrew as
main language, those boxes inherit RTL direction **and** the Hebrew locale; babel's Lua bidi
algorithm then mirrors paired punctuation. Setting `\pardir/\textdir` alone fixed the order but
not the mirroring, because mirroring follows the *locale*, not only the direction.

## Why it was not detected earlier
There was no check yet — this was found by the first visual pass. `qa_scan.py` only reads text,
and the source code looked perfect.

## Fix (systemic)
```latex
\lst@AddToHook{Init}{\selectlanguage{english}\pardir TLT\textdir TLT\bodydir TLT}
```
## Prevention
- `qa-BiDi` rule B4/B5: check code direction and parentheses **in the PDF render**.
- `qa-code`: no Hebrew in code blocks (automated in `qa_scan.py`).
