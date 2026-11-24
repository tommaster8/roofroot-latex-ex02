# Prompt 07 — Investor review (investor-critic)

**Model:** Sonnet · **Agent:** `.claude/agents/investor-critic.md`

**Why this agent exists:** every other reviewer on the team checks that the document is
*correct* (typesetting, BiDi, numbers equal to the model). The PRD names the Seed investor
as the primary reader, yet no agent read the plan as that investor. A plan can pass the red
team with 0 MAJOR findings and still fail to raise money. This agent closes that gap.

**When:** after the red team writes PASS (a broken PDF is not worth an investor's time), and
again after the writers revise.

```text
Investor review round N. You are a skeptical Seed VC; follow
.claude/agents/investor-critic.md. Read the plan in investor order, score the six
lenses 1–5 with evidence, list your 10 hardest meeting questions as
ANSWERED / WEAK / MISSING, and write qa-reports/investor-N.md with a verdict
(INVEST / SECOND MEETING / PASS) and the one change that would most move you.
Route each point to its owner: data assumption → Orchestrator, argument → the
chapter-writer who owns that chapter. Do not edit anything outside qa-reports/.
```

**Loop:** the Orchestrator turns `MISSING`/`WEAK` items into writer tasks (prompt 03) or data
changes (`data/*.csv` → `make`), then the red team re-checks formatting (prompt 04) and the
investor-critic re-reads (round N+1). Exit when the verdict is `SECOND MEETING` or better and
no question is `MISSING`.
