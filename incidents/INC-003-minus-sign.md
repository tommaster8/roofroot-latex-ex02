# INC-003 — Minus sign on the wrong side in the P&L table

| | |
|---|---|
| **Found by** | Human lead, looking at the render of the P&L table |
| **Severity** | MAJOR (a financial number that reads wrong) |
| **Fixed in** | `make_figures.py::ils_k()` |

## What happened
`-1,413` displayed as `1,413-`. Also `-0` appeared for zero tax.

## Root cause
In an RTL paragraph, a leading `-` is a weak/neutral character; the bidi algorithm placed it at the
visual end of the number run.

## Why it was not detected
No QA lens owned "numbers in RTL"; the agent read the `.tex`, where the value is correct.

## Fix
`ils_k()` wraps every number in `\en{}` (LTR) and prints `0` instead of `-0`.
## Prevention
`qa_scan.py::check_bidi` flags any bare negative number in chapter text; rule B3 in `qa-BiDi`.
