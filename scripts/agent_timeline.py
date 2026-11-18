"""Render docs/screenshots/agents-in-action.png from docs/agent-runs.csv (real run stats)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(ROOT / "docs/agent-runs.csv")))
COL = {"write": "#1F4D3A", "red team": "#D9663B", "fix": "#8CC63F"}
fig, ax = plt.subplots(figsize=(8, 0.55 * len(rows) + 1.2))
start = {}
for i, r in enumerate(rows):
    o = int(r["order"])
    x0 = start.setdefault(o, sum(max(float(q["minutes"]) for q in rows if int(q["order"]) == k)
                                 for k in range(1, o)))
    ax.barh(i, float(r["minutes"]), left=x0, color=COL[r["phase"]], height=0.6)
    ax.text(x0 + float(r["minutes"]) + 0.1, i,
            f'{r["model"]} · {int(r["tokens"]) / 1000:.0f}k tok · {r["tool_calls"]} tools · {r["output"]}',
            va="center", fontsize=8)
ax.set_yticks(range(len(rows)), [r["agent"] for r in rows])
ax.invert_yaxis()
ax.set_xlabel("minutes (parallel agents share a start time)")
ax.set_xlim(0, ax.get_xlim()[1] * 1.9)
ax.set_title("RoofRoot agent team in action — real run log", color="#1F4D3A", fontweight="bold")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(ROOT / "docs/screenshots/agents-in-action.png", dpi=130)
