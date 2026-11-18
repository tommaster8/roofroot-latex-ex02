---
name: qa-cls-version
description: Verifies roofroot.cls version consistency — \ProvidesClass date/version, \rr@clsversion, CHANGELOG entry, and PDF metadata. Use whenever roofroot.cls changes.
---
# qa-cls-version — template version control

Every change to `roofroot.cls` must:
1. bump `\ProvidesClass{roofroot}[YYYY/MM/DD vX.Y ...]`
2. bump `\def\rr@clsversion{X.Y}` to the same value
3. add a `%%  vX.Y  <what and why, incident id>` line at the end of the CHANGELOG block
4. the PDF metadata (`pdfcreator`) then shows the version automatically.

Check: `grep -nE "ProvidesClass|rr@clsversion|^%%  v" roofroot.cls` — all three must agree.
A fix that touched the cls without a version bump = MAJOR (it breaks traceability of the red-team loop).
