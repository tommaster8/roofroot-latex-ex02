---
name: qa-infra
description: Checks the RoofRoot project structure and reproducibility — required files, one .tex per chapter, build script, no orphan files. Use before submission or after adding files.
---
# qa-infra — project structure

Required (assignment §3.3 + PRD TR-07):
```
main.tex  roofroot.cls  references.bib  PRD.md PLAN.md TODO.md README.md
chapters/NN-*.tex (one per chapter, all \input in main.tex)
figures/python/*.py → figures/generated/   figures/tikz/*.tex
data/*.csv   scripts/build.sh   Makefile   requirements.txt
.claude/skills/*/SKILL.md   .claude/agents/*.md   prompts/*.md   incidents/*.md
```
- Reproducibility test: `git clone` into a temp dir → `make venv && make` → PDF builds with no system fonts.
- `.gitignore` excludes `*.aux *.log *.bcf ... .venv/` but **keeps** `main.pdf` and `figures/generated/`.
