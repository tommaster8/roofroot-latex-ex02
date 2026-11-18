# Prompt 04 — Red team round (qa-detector)

**Model:** Sonnet · **Agent:** `.claude/agents/qa-detector.md`

```text
Red-team round N on main.pdf. Follow .claude/skills/qa-super/SKILL.md step by step.
You are NOT allowed to fix anything. Render every page at 60 dpi and look at it.
Try hard to break it: reversed parentheses, minus signs on the wrong side, English
words in the wrong order, a number in the text that disagrees with a chart or table,
text overflowing a TikZ box, a figure referenced before it is defined, an orphan
heading at the bottom of a page, a citation that does not support the claim.
Write qa-reports/round-N.md with severity, evidence and proposed systemic fix.
```
