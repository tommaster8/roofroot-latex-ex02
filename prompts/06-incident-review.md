# Prompt 06 — Incident review ("חקר אירוע") with the agent

Used whenever the **human** found a defect the agents missed.

```text
I found a defect you did not report: <description + page>.
Do an incident review, blameless format:
 1. What happened (observable symptom).
 2. Root cause — the technical mechanism, not "the model made a mistake".
 3. Why it was not detected — which skill/check should have caught it and why it didn't.
 4. Fix — in the cls / skill / generator, with version bump.
 5. Prevention — the new automated check (qa_scan.py rule or skill checklist line).
Write it to incidents/INC-NNN.md and update the relevant SKILL.md.
```
