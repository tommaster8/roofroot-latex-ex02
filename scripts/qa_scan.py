"""qa_scan — the automated half of the qa-detector (red team).

Runs every mechanical check that the qa-* Skills define and writes
qa-reports/scan-latest.md.  Exit code 1 if any CRITICAL/MAJOR finding.

    python scripts/qa_scan.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / "chapters"
findings: list[tuple[str, str, str, str]] = []   # (severity, skill, where, message)


def add(sev: str, skill: str, where: str, msg: str) -> None:
    findings.append((sev, skill, where, msg))


def chapter_files() -> list[Path]:
    return sorted(CH.glob("*.tex"))


# ------------------------------------------------------------ qa-infra
def check_infra() -> None:
    required = ["main.tex", "roofroot.cls", "references.bib", "PRD.md", "PLAN.md",
                "TODO.md", "README.md", "Makefile", "scripts/build.sh",
                "figures/python/make_figures.py", "data/assumptions.csv"]
    for r in required:
        if not (ROOT / r).exists():
            add("MAJOR", "qa-infra", r, "required file missing")
    main = (ROOT / "main.tex").read_text()
    for f in chapter_files():
        if f"chapters/{f.stem}" not in main:
            add("MAJOR", "qa-infra", f.name, "chapter file is not \\input in main.tex")
    for m in re.findall(r"\\input\{chapters/([^}]+)\}", main):
        if not (CH / f"{m}.tex").exists():
            add("CRITICAL", "qa-infra", "main.tex", f"\\input of missing chapter {m}")


# ------------------------------------------------------------ qa-cls-version
def check_cls_version() -> None:
    cls = (ROOT / "roofroot.cls").read_text()
    m = re.search(r"\\ProvidesClass\{roofroot\}\[\S+ v([\d.]+)", cls)
    d = re.search(r"\\def\\rr@clsversion\{([\d.]+)\}", cls)
    log = re.findall(r"%%\s+v([\d.]+)\s", cls)
    if not (m and d):
        add("MAJOR", "qa-cls-version", "roofroot.cls", "version line missing")
        return
    if m.group(1) != d.group(1):
        add("MAJOR", "qa-cls-version", "roofroot.cls",
            f"\\ProvidesClass v{m.group(1)} != \\rr@clsversion {d.group(1)}")
    if not log or log[-1] != m.group(1):
        add("MINOR", "qa-cls-version", "roofroot.cls",
            f"CHANGELOG last entry v{log[-1] if log else '?'} != class v{m.group(1)}")


# ------------------------------------------------------------ qa-typeset (log)
def check_log() -> None:
    logf = ROOT / "main.log"
    if not logf.exists():
        add("CRITICAL", "qa-typeset", "main.log", "no log — document not compiled")
        return
    log = logf.read_text(errors="ignore")
    for m in re.finditer(r"Overfull \\hbox \(([\d.]+)pt too wide\)[^\n]*lines? (\d+)", log):
        if float(m.group(1)) > 1.0:
            add("MAJOR" if float(m.group(1)) > 5 else "MINOR", "qa-typeset",
                f"line {m.group(2)}", f"Overfull hbox {m.group(1)}pt")
    for m in re.finditer(r"Overfull \\vbox \(([\d.]+)pt too high\)", log):
        if float(m.group(1)) > 2.0:
            add("MINOR", "qa-typeset", "main.log", f"Overfull vbox {m.group(1)}pt")
    for pat, sev in [(r"Reference `([^']+)' on page \d+ undefined", "MAJOR"),
                     (r"Citation '([^']+)' on page \d+ undefined", "MAJOR"),
                     (r"Missing character: There is no (\S+)", "MAJOR")]:
        for m in sorted(set(re.findall(pat, log))):
            add(sev, "qa-typeset", "main.log", f"{pat.split('(')[0].strip()}: {m}")
    if "There were undefined references" in log:
        add("MAJOR", "qa-typeset", "main.log", "undefined references remain")


# ------------------------------------------------------------ qa-BiDi
def check_bidi() -> None:
    for f in chapter_files():
        for i, line in enumerate(f.read_text().splitlines(), 1):
            s = line.split("%")[0] if not line.lstrip().startswith("%") else ""
            if "\\textbullet" in s:
                add("MAJOR", "qa-BiDi", f"{f.name}:{i}",
                    "\\textbullet has no glyph in David CLM — use itemize or $\\bullet$")
            # negative number in Hebrew context renders as '5-' unless LTR-wrapped
            bare = re.sub(r"\\en\{[^}]*\}|\$[^$]*\$", "", s)
            for m in re.finditer(r"(?<![\w-])-\d[\d,.]*", bare):
                add("MINOR", "qa-BiDi", f"{f.name}:{i}",
                    f"bare negative number '{m.group()}' — wrap in \\en{{}} or math")
            # Hebrew prefix glued to an English word without the maqaf-hyphen
            if re.search(r"[\u05d0-\u05ea]\\en\{", s):
                add("MINOR", "qa-BiDi", f"{f.name}:{i}",
                    "Hebrew letter glued to \\en{} — write ה-\\en{...} with a hyphen")
            if re.search(r"\(\s*\\en\{[^}]*\}\s*$", s):
                add("MINOR", "qa-BiDi", f"{f.name}:{i}", "parenthesis split across lines")


# ------------------------------------------------------------ qa-table / numbers
def check_numbers() -> None:
    nums = ROOT / "figures/generated/numbers.tex"
    if not nums.exists():
        return
    vals = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", nums.read_text()))
    def is_year(v: str) -> bool:   # round-1 false positives: calendar years are not model outputs
        return v.isdigit() and 1990 <= int(v) <= 2100
    numeric = {k: v for k, v in vals.items() if re.fullmatch(r"[\d.,]+", v)}
    distinctive = {v: k for k, v in numeric.items() if not is_year(v) and (
                   len(v.replace(",", "")) >= 3 and "." in v or len(v.replace(",", "")) >= 4)}
    for f in chapter_files():
        text = f.read_text()
        for v, k in distinctive.items():
            for m in re.finditer(rf"(?<![\d.,]){re.escape(v)}(?![\d,]|\.\d)", text):
                line = text[:m.start()].count("\n") + 1
                add("MAJOR", "qa-table", f"{f.name}:{line}",
                    f"hard-coded number {v} — use \\{k} (single source of truth)")


def check_tables_figures() -> None:
    alltext = "\n".join(f.read_text() for f in chapter_files())
    labels = re.findall(r"\\label\{((?:fig|tab|eq):[^}]+)\}", alltext)
    for lab in labels:
        if f"{{{lab}}}" not in alltext.replace(f"\\label{{{lab}}}", ""):
            add("MINOR", "qa-img" if lab.startswith("fig") else "qa-table",
                lab, "label is never referenced in the text")
    for f in chapter_files():
        text = f.read_text()
        for env in re.finditer(r"\\begin\{(figure|table)\}(.*?)\\end\{\1\}", text, re.S):
            body = env.group(2)
            line = text[:env.start()].count("\n") + 1
            sk = "qa-img" if env.group(1) == "figure" else "qa-table"
            if "\\caption" not in body:
                add("MAJOR", sk, f"{f.name}:{line}", f"{env.group(1)} without caption")
            if "\\label" not in body:
                add("MINOR", sk, f"{f.name}:{line}", f"{env.group(1)} without label")
            if env.group(1) == "figure" and re.search(r"\\includegraphics(?!\[)", body):
                add("MINOR", "qa-img", f"{f.name}:{line}", "includegraphics without width")
            if "[H]" in text[env.start():env.start() + 20]:
                add("MINOR", sk, f"{f.name}:{line}", "[H] placement forces gaps — prefer [htbp]")


# ------------------------------------------------------------ qa-code
def check_code() -> None:
    for f in chapter_files():
        text = f.read_text()
        for blk in re.finditer(r"\\begin\{pythonbox\}.*?\n(.*?)\\end\{pythonbox\}", text, re.S):
            for j, ln in enumerate(blk.group(1).splitlines()):
                if len(ln) > 72:
                    line = text[:blk.start()].count("\n") + 2 + j
                    add("MAJOR", "qa-code", f"{f.name}:{line}",
                        f"code line {len(ln)} chars > 72 — will overflow the box")
                if re.search(r"[\u0590-\u05ff]", ln):
                    line = text[:blk.start()].count("\n") + 2 + j
                    add("MAJOR", "qa-code", f"{f.name}:{line}", "Hebrew inside code block")


# ------------------------------------------------------------ citations / length
def check_bib_and_length() -> None:
    bib = (ROOT / "references.bib").read_text()
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    used = set()
    for f in chapter_files():
        for group in re.findall(r"\\(?:cite|textcite|parencite)\{([^}]+)\}", f.read_text()):
            used.update(k.strip() for k in group.split(","))
    for k in sorted(used - keys):
        add("CRITICAL", "qa-super", "references.bib", f"cited key '{k}' not in bib")
    for k in sorted(keys - used):
        add("MINOR", "qa-super", "references.bib", f"bib entry '{k}' never cited")
    pdf = ROOT / "main.pdf"
    if pdf.exists():
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        if m and int(m.group(1)) < 15:
            add("CRITICAL", "qa-super", "main.pdf", f"only {m.group(1)} pages (< 15)")


def check_pdf_numbers() -> None:
    """INC-004: compound counters must survive as whole words in the PDF."""
    pdf = ROOT / "main.pdf"
    if not pdf.exists():
        return
    out = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"],
                         capture_output=True, text=True).stdout
    if not re.search(r">\d+\.\d+<", out):
        add("MAJOR", "qa-BiDi", "main.pdf",
            "no compound counter (e.g. 3.1) found as one word — numbering is reversed/split")
    for m in sorted(set(re.findall(r">(\d[\d,.]*-)<", out)))[:10]:
        add("MAJOR", "qa-BiDi", "main.pdf", f"minus sign on the wrong side: '{m}'")


def main() -> int:
    for check in (check_infra, check_cls_version, check_log, check_bidi, check_numbers,
                  check_tables_figures, check_code, check_bib_and_length, check_pdf_numbers):
        check()
    order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}
    findings.sort(key=lambda x: (order[x[0]], x[1], x[2]))
    counts = {s: sum(1 for f in findings if f[0] == s) for s in order}
    lines = ["# qa_scan — automated red-team report", "",
             f"**CRITICAL {counts['CRITICAL']} · MAJOR {counts['MAJOR']} · "
             f"MINOR {counts['MINOR']}**", "",
             "| # | Severity | Skill | Where | Finding |", "|---|---|---|---|---|"]
    lines += [f"| {i} | {s} | {k} | `{w}` | {m} |" for i, (s, k, w, m) in enumerate(findings, 1)]
    out = ROOT / "qa-reports" / "scan-latest.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[2:3]))
    for s, k, w, m in findings:
        print(f"  [{s:8}] {k:15} {w:28} {m}")
    return 1 if counts["CRITICAL"] or counts["MAJOR"] else 0


if __name__ == "__main__":
    sys.exit(main())
