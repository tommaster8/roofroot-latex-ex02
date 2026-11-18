.PHONY: all pdf figures qa clean venv
all: pdf qa
venv:
	python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
figures:
	.venv/bin/python figures/python/make_figures.py
pdf:
	scripts/build.sh
qa:
	.venv/bin/python scripts/qa_scan.py
clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.bcf *.blg *.run.xml
