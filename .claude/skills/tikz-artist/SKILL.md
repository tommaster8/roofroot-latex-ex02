---
name: tikz-artist
description: Conventions for TikZ illustrations in the RoofRoot RTL document (cover, BMC, SWOT, architecture, timeline, org chart). Use when drawing or fixing a TikZ figure.
---
# tikz-artist — illustrations in code

- One picture per file in `figures/tikz/`, header comment saying what it shows.
- Colours only from the palette (`rrForest, rrLeaf, rrTerra, rrCream, rrSky, rrStone, rrInk`).
- RTL: babel `layout=graphics` keeps TikZ coordinates LTR. For reading order "start on the right", use `x=-1cm` (see timeline.tex) — do not mirror by hand.
- Hebrew text in nodes: give `text width` + `align=right`; keep `\scriptsize`–`\small`; verify no overflow in the render.
- Bullets inside nodes: `$\bullet$` (B6).
- Never `\foreach` with `\ifnum` on a float variable — pass the value in the list instead (lesson from timeline.tex build error).
- **Alignment is mirrored in RTL** (INC-004): TikZ `align=right` uses `\raggedleft`, which in a
  right-to-left paragraph is *flush left*. For Hebrew blocks that must hug the right edge use
  `align=left`; verify with the render.
