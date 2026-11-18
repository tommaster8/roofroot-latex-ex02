# Prompt 01 — Expert committee → PRD

**Model:** Opus · **Role:** Orchestrator wearing five hats · **Output:** `PRD.md`

```text
You are convening an expert committee to write the PRD for a LaTeX business plan.
Members (each speaks in turn, then they vote on every requirement):
 1. A VC partner who reads 300 decks a year — what makes a plan credible in 3 minutes?
 2. A Hebrew typographer — what does correct mixed Hebrew/English (BiDi) look like?
 3. A LaTeX engineer — what makes a project reproducible and maintainable?
 4. A data-visualisation designer — how do we avoid "default matplotlib" look?
 5. The course lecturer — what do assignment ex02 and the VIBE-CODING booklet require?

Inputs: the assignment PDF (requirements table §2, folder structure §3.3, skills §5),
the multi-agent guide, and our vision: "a seed-stage plan for RoofRoot — hydroponic
farms on residential roofs in Tel Aviv, run by an AI agent called RootOS".

Produce PRD.md with: vision, "default vs our decision" table (originality),
functional requirements with IDs and acceptance thresholds, technical requirements,
QA/red-team process, definition of done, out of scope.
Every requirement must be testable. Prefer numbers ("≥ 6 charts") to adjectives.
```

**Decisions the human lead locked in after reading the committee output:**
- Palette: "green roof" (forest / leaf / terracotta / cream) — deliberately not the corporate blue an LLM picks by default.
- Single source of truth: every number comes from `data/*.csv` through Python (`numbers.tex` macros).
- BiDi compromise: English chart labels + Hebrew captions (matplotlib cannot shape RTL).
