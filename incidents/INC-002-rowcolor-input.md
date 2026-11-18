# INC-002 — Generated table failed: "Misplaced \noalign"

| | |
|---|---|
| **Found by** | Orchestrator, compile of figure test |
| **Severity** | CRITICAL (build error) |
| **Fixed in** | `figures/python/make_figures.py` → `write_table()` |

## What happened
`\begin{tabularx}...\input{tab_pnl.tex}\end{tabularx}` → `! Misplaced \noalign` ×3.

## Root cause
`\rrtablehead` = `\rowcolor{...}`, which uses `\noalign` and must be the first token of a row.
`\input` is not expandable in that position, so `\rowcolor` was no longer first.

## Why it was not detected
The class test used a hand-written table; generated tables were never tested inside `tabular`.

## Fix
The generator now writes the **whole** environment (`\rrstripes` + `tabularx` + rows), and chapters
`\input` it inside `table`. Rule added to `qa-table` and to the writer brief.
