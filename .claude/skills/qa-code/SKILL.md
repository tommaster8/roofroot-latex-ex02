---
name: qa-code
description: Checks code listings (pythonbox) in the RoofRoot LaTeX document for overflow, direction and correctness. Use when a chapter contains a pythonbox or any code.
---
# qa-code — code boxes

- Code lives only in `\begin{pythonbox}[title] ... \end{pythonbox}` (defined in cls).
- Max **72 characters per line** (box width at 11pt Fira Mono). Longer → refactor the code, do not shrink the font.
- No Hebrew inside code (comments in English). Hebrew explanation goes in the prose around it.
- Code must be **runnable Python** consistent with `figures/python/model.py` (same names, same formulas).
- Visual check: background cream, frame forest green, line numbers on the left, LTR order, parentheses not mirrored (INC-001).
- No tabs; 4-space indentation.
