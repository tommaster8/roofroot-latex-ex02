# INC-005 — Citation brackets reversed: "]3[", period jumps across "[2]."

| | |
|---|---|
| **Found by** | qa-detector, red-team round 1 (findings #3, #4), proved with `pdftotext -bbox-layout` |
| **Severity** | MAJOR |
| **Fixed in** | `roofroot.cls` v1.2 |

## What happened
- In a Hebrew sentence, `\cite{a,b}.` rendered with the period on the wrong side of `[2]`.
- In the caption of the figure "לפי \cite{barbosa2015}", the reference became `]3[`, both on the page and in the List of Figures.

## Root cause
biblatex prints `[`, the number and `]` as separate characters. Brackets and periods are *neutral* in the Unicode bidi algorithm, so they take the direction of the surrounding RTL paragraph. The digits are LTR, so the brackets end up mirrored and swapped around them.

## Why it was not detected earlier
- The class test page (v1.0) contained no citations.
- The writers' isolated builds print the same defect, but no agent rendered and inspected them. The writer brief only required a successful compile.

## Fix
`\cite` is redefined, robustly, as `\babelsublr{\origcite{..}}`. This makes it a single LTR box, so the bidi algorithm moves it as one unit, and the following `.` is resolved by the Hebrew paragraph. Variant `{\textdir TLT ...}` was tested and **rejected**, because it still produced `]1[`. The result is now verified: the probe shows `[1],` `[2]` `.`

## Prevention
- writer-he-en rule C3 forbids citations inside captions.
- The qa-super grep checks for `\caption{...\cite`.
- The writer brief now requires a writer to *look* at their isolated PDF, not just compile it.
