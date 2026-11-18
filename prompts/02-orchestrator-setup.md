# Prompt 02 — Orchestrator: skeleton, class, data

**Model:** Opus

```text
Read PRD.md. Build the smallest project that compiles, then grow it:
1. roofroot.cls (LuaLaTeX only): palette from PRD, Culmus + TeX Gyre + Fira fonts
   loaded by file name (no system fonts), babel bidi=basic with Hebrew main,
   chapter opener as a TikZ band with the number, full-width header banner with the
   chapter name, footer with title + page bubble, tcolorbox family (insightbox,
   riskbox, keynumber), pythonbox (LTR!), table helpers, biblatex IEEE.
   Put a version + CHANGELOG at the top; every later fix bumps it.
2. A 1-page test.tex exercising every feature. Compile, render to PNG, LOOK at it.
   Fix every visual defect in the cls, not in the test.
3. data/assumptions.csv + data/plan.csv → figures/python/model.py (5-year model,
   unit economics, NPV with terminal value, sensitivity) → make_figures.py producing
   7 charts (PDF+PNG), the LaTeX tables and numbers.tex macros.
4. TikZ: cover skyline with green roofs, BMC, SWOT, RootOS architecture, timeline,
   org chart, agent-team diagram.
5. main.tex, references.bib (real sources only, with DOI where possible),
   scripts/build.sh, Makefile, scripts/qa_scan.py.
```
