#!/usr/bin/env bash
# One-command reproducible build: data -> figures/tables -> PDF.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-.venv/bin/python}"
[ -x "$PY" ] || PY=python3
echo "▶ 1/4  Python: charts, tables and number macros from data/"
"$PY" figures/python/make_figures.py
echo "▶ 2/4  lualatex (pass 1)"
lualatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null
echo "▶ 3/4  biber"
biber --quiet main
echo "▶ 4/4  lualatex (passes 2-3: references + TOC)"
lualatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null
lualatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null
echo "✔ main.pdf — $(pdfinfo main.pdf 2>/dev/null | awk '/Pages/{print $2}') pages"
