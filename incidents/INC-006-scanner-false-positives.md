# INC-006 — The Detector's own scanner cried wolf (7 of 8 findings were false)

| | |
|---|---|
| **Found by** | qa-detector, round 1 (section A of its report) — the red team audited its own tool |
| **Severity** | MINOR (no defect in the PDF), but dangerous: noisy tools train people to ignore them |
| **Fixed in** | `scripts/qa_scan.py::check_numbers` |

## What happened
Rule N1 ("use the macro, not the literal") flagged every `2028` and `2030` in the hiring plans and
timelines, because `\RRminCashYear = 2028` and `\RRbreakEvenYear = 2030`. It also flagged `2,400`
(the capex line) because `\RRtam = 2,400`. That last match was a coincidence, but it led the
Detector to a *real* defect: the capex figure itself was wrong (#7).

## Root cause
The scanner matched a *value* without its *meaning*. Calendar years are not model outputs.

## Fix
Year-valued macros (1990–2100) are excluded from N1. The real protection for derived values is
now in the generator: macros exist for every derived number, the generated use-of-funds table
replaces the hand-written one, and the pricing assertion fails the build if channel prices do not
average to the model price.

## Lesson
A red team needs a red team. A false positive is a defect of the QA system, and it gets an
incident like any other defect.
