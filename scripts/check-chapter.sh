#!/usr/bin/env bash
# Compile ONE chapter in isolation (build/<stem>.pdf) so parallel writer agents
# never fight over main.aux. Usage: scripts/check-chapter.sh 04-market
set -euo pipefail
cd "$(dirname "$0")/.."
stem="${1:?usage: check-chapter.sh <chapter-stem>}"
mkdir -p build
job="check-$stem"
cat > "build/$job.tex" <<TEX
\\documentclass{roofroot}
\\input{figures/generated/numbers.tex}
\\addbibresource{references.bib}
\\begin{document}
\\input{chapters/$stem}
\\rrbibliography
\\end{document}
TEX
export TEXINPUTS=".:./build:"
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build "build/$job.tex" > /dev/null || {
  echo "✘ compile failed:"; grep -A4 "^!" "build/$job.log" | head -30; exit 1; }
biber --quiet --input-directory=build --output-directory=build "$job" || true
lualatex -interaction=nonstopmode -output-directory=build "build/$job.tex" > /dev/null
lualatex -interaction=nonstopmode -output-directory=build "build/$job.tex" > /dev/null
echo "✔ build/$job.pdf — $(pdfinfo "build/$job.pdf" | awk '/Pages/{print $2}') pages"
grep -E "Overfull|Missing character|undefined" "build/$job.log" | sort | uniq -c | head -20 || true
