# Prompt 05 — Fixer

**Model:** Opus · **Agent:** `.claude/agents/qa-fixer.md`

```text
Read qa-reports/round-N.md. For each CRITICAL/MAJOR finding:
 1. Decide the systemic home of the fix: roofroot.cls (bump version + CHANGELOG),
    a Skill (so writers never repeat it), the generator, or — only for content
    errors — the chapter text.
 2. Apply it, rebuild (scripts/build.sh), rerun scripts/qa_scan.py.
 3. Append a "Fix log" section to the round report: finding → where fixed → why there.
 4. If the defect could recur, write incidents/INC-NNN.md (what, why it happened,
    why it was not detected, what changed so it cannot recur).
```
