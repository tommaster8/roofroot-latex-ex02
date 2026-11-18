---
name: qa-table
description: Checks LaTeX tables in the RoofRoot document — alignment, column order in RTL, header styling, stripes, numeric consistency with the data model. Use when a chapter contains tabular/tabularx or quotes numbers.
---
# qa-table — tables and numbers

## Checklist
- [ ] Table uses the class style: `\rrstripes`, header row `\rrtablehead`, header cells `\rrth{}`.
- [ ] `tabularx` at `\linewidth`; text column type `Y` (RTL ragged); numeric columns `r`.
- [ ] In RTL the **first** column is on the **right** — the label column must be first.
- [ ] Caption **above or below consistently** (class default: below), with `\label{tab:...}` and a `\ref` in text.
- [ ] Generated tables (`tab_*.tex`) are `\input` whole — never paste their rows (INC-002: `\rowcolor` must be the first token of a row).
- [ ] **N1 — single source of truth:** any number that exists in `figures/generated/numbers.tex` must be written with its macro (`\RRrevFinal`), never typed by hand. `qa_scan.py` flags violations.
- [ ] Numbers ≥ 1,000 use thousands separators; currency unit stated once in the header.
- [ ] No row overflows the right margin (check Overfull hbox in log).
