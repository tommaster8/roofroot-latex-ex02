---
name: fig-python
description: How to add or change a data chart in the RoofRoot project — matplotlib in figures/python/make_figures.py driven by data/*.csv. Use when a chart, a generated table or a number macro is needed.
---
# fig-python — charts from code

1. Data first: put inputs in `data/*.csv`, logic in `figures/python/model.py`.
2. Add `fig_<name>()` in `make_figures.py`, register it in `__main__`.
3. Style is global (palette FOREST/LEAF/TERRA/…, Lato from TeX tree, `pdf.fonttype=42`): do **not** override colours per chart.
4. Labels in **English** (matplotlib does not shape RTL Hebrew). Hebrew goes in the LaTeX caption.
5. Output both `.pdf` (document) and `.png` (README).
6. A number that the text quotes → add to the `macros` dict → `\RRname`.
7. Run `scripts/build.sh` — never commit a figure that was not regenerated.
