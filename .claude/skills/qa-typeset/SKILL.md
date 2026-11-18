---
name: qa-typeset
description: Checks compilation warnings in the RoofRoot LuaLaTeX build — overfull/underfull boxes, undefined refs/citations, missing glyphs, font substitutions. Use after every build.
---
# qa-typeset — compiler warnings

```bash
grep -nE "Overfull|Underfull|undefined|Missing character|Font shape .* undefined" main.log
```
| Warning | Threshold | Typical systemic fix |
|---|---|---|
| Overfull \hbox | > 1pt = MINOR, > 5pt = MAJOR | long English word → `\en{}` allows hyphenation; table → `tabularx` |
| Underfull \hbox (badness 10000) | only if visible | rephrase |
| Reference/Citation undefined | any = MAJOR | run biber + 2 passes; check key spelling |
| Missing character | any = MAJOR | glyph not in font → change command (e.g. `\textbullet`) or font in cls |
| Font shape undefined | any = MINOR | add the shape in `\babelfont` in cls |
