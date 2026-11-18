"""Generate every chart, auto-table and number macro for the RoofRoot plan.

    python figures/python/make_figures.py

Outputs (all in figures/generated/):
  fig_*.pdf      vector charts, English labels (BiDi decision, see PRD §1)
  tab_*.tex      LaTeX table bodies built from the same model
  numbers.tex    \\newcommand macros for every number quoted in the text
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle

import model as m

OUT = m.ROOT / "figures" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ style
FOREST, LEAF, TERRA, CREAM, SKY, INK, STONE = (
    "#1F4D3A", "#8CC63F", "#D9663B", "#F6F1E7", "#CFE6E2", "#22312B", "#8A8F87")


def _register_lato() -> str:
    """Use Lato from the TeX distribution so charts need no system fonts."""
    import subprocess
    for name in ("Lato-Regular.ttf", "Lato-Bold.ttf"):
        try:
            path = subprocess.run(["kpsewhich", name], capture_output=True,
                                  text=True, check=True).stdout.strip()
            if path:
                font_manager.fontManager.addfont(path)
        except (OSError, subprocess.CalledProcessError):
            return "DejaVu Sans"
    return "Lato"


plt.rcParams.update({
    "font.family": _register_lato(),
    "font.size": 10,
    "axes.edgecolor": STONE,
    "axes.labelcolor": INK,
    "axes.titleweight": "bold",
    "axes.titlesize": 11,
    "axes.titlecolor": FOREST,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": "#E3E0D8",
    "grid.linewidth": 0.6,
    "xtick.color": INK,
    "ytick.color": INK,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "figure.dpi": 150,
})

A = m.load_assumptions()
YEARS = m.run(A)
X = [y.year for y in YEARS]
MILL = 1e6


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", dpi=110)  # README previews
    plt.close(fig)


# ------------------------------------------------------------------ 1 revenue mix + EBITDA
def fig_revenue_mix() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    prod = np.array([y.rev_produce for y in YEARS]) / MILL
    saas = np.array([y.rev_saas for y in YEARS]) / MILL
    ebitda = np.array([y.ebitda for y in YEARS]) / MILL
    ax.bar(X, prod, color=FOREST, width=0.6, label="Produce (B2B + subscriptions)")
    ax.bar(X, saas, bottom=prod, color=LEAF, width=0.6, label="RootOS SaaS licences")
    ax.plot(X, ebitda, color=TERRA, marker="o", lw=2.2, label="EBITDA")
    ax.axhline(0, color=INK, lw=0.8)
    for x, p, s in zip(X, prod, saas):
        ax.text(x, p + s + 0.25, f"{p + s:.1f}", ha="center", fontsize=8.5, color=INK)
    ax.set_ylabel("ILS million")
    ax.set_title("Revenue mix and EBITDA, 2027-2031")
    ax.legend(loc="upper left", fontsize=8.5)
    ax.set_xticks(X)
    save(fig, "fig_revenue_mix")


# ------------------------------------------------------------------ 2 cash J-curve
def fig_cash_curve() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    fcf = np.array([y.free_cash_flow for y in YEARS]) / MILL
    cum_fcf = np.cumsum(fcf)
    cash = np.array([y.cash_end for y in YEARS]) / MILL
    ax.fill_between(X, cum_fcf, 0, color=TERRA, alpha=0.15)
    ax.plot(X, cum_fcf, color=TERRA, lw=2, marker="s", label="Cumulative free cash flow")
    ax.plot(X, cash, color=FOREST, lw=2.4, marker="o", label="Cash balance (with equity)")
    for y in YEARS:
        if y.equity_in:
            ax.annotate(f"+{y.equity_in / MILL:.0f}M equity", (y.year, y.cash_end / MILL),
                        xytext=(14, 10) if y.year > 2027 else (28, -18), textcoords="offset points", ha="left",
                        fontsize=8.5, color=FOREST, fontweight="bold",
                        arrowprops=dict(arrowstyle="-", color=FOREST, lw=0.6))
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_ylim(min(cum_fcf) * 1.15, max(cash) * 1.3)
    ax.set_ylabel("ILS million")
    ax.set_title("Cash: the J-curve and how the two rounds cover it")
    ax.legend(loc="lower left", fontsize=8.5)
    ax.set_xticks(X)
    save(fig, "fig_cash_curve")


# ------------------------------------------------------------------ 3 unit economics waterfall
def fig_unit_waterfall() -> None:
    u = m.roof_unit_economics(A)
    steps = [("Revenue", u["revenue"]), ("Roof rent", -u["rent"]),
             ("Operating cost", -u["opex"]), ("Depreciation", -u["depreciation"])]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    level = 0.0
    for i, (label, val) in enumerate(steps):
        bottom = level if val >= 0 else level + val
        ax.bar(i, abs(val) / 1e3, bottom=bottom / 1e3, width=0.6,
               color=FOREST if val >= 0 else TERRA)
        ax.text(i, (level + max(val, 0)) / 1e3 + 4, f"{val / 1e3:+.0f}k",
                ha="center", fontsize=8.5)
        level += val
    ax.bar(len(steps), level / 1e3, width=0.6, color=LEAF)
    ax.text(len(steps), level / 1e3 + 4, f"{level / 1e3:.0f}k", ha="center",
            fontsize=9, fontweight="bold", color=FOREST)
    ax.set_xticks(range(len(steps) + 1), [s[0] for s in steps] + ["Roof profit"])
    ax.set_ylabel("ILS thousand / year")
    ax.set_title("Unit economics of one mature roof (250 m2)")
    save(fig, "fig_unit_waterfall")


# ------------------------------------------------------------------ 4 TAM / SAM / SOM
MARKET = {"TAM": (2400, "Israeli fresh leafy greens & herbs"),
          "SAM": (380, "Premium urban demand, Gush Dan"),
          "SOM": (m.run(A)[-1].revenue / MILL, "RoofRoot revenue, 2031")}


def fig_market() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.set_aspect("equal")
    ax.axis("off")
    radii = [2.0, 1.15, 0.45]
    colors = [SKY, LEAF, FOREST]
    for (key, (val, desc)), r, c in zip(MARKET.items(), radii, colors):
        ax.add_patch(Circle((0, r - 2.0), r, color=c, ec="white", lw=2))
        y_lab = 2 * r - 2.0 - 0.32
        txt_color = "white" if key == "SOM" else FOREST
        ax.text(0, y_lab if key != "SOM" else -1.55, f"{key}", ha="center",
                fontweight="bold", color=txt_color, fontsize=10)
        ax.text(2.35, 2 * r - 2.3, f"{key}  ILS {val:,.0f}M\n{desc}", fontsize=8.5,
                va="center", color=INK)
        ax.plot([0.3, 2.3], [2 * r - 2.3] * 2, color=STONE, lw=0.6)
    ax.set_xlim(-2.2, 5.6)
    ax.set_ylim(-2.15, 2.15)
    ax.set_title("Market sizing (team estimates, ILS per year)")
    save(fig, "fig_market")


# ------------------------------------------------------------------ 5 sensitivity tornado
def fig_tornado() -> None:
    base = m.npv(YEARS, A["discount_rate"], A["exit_ebitda_multiple"]) / MILL
    rows = [(lbl, lo / MILL, hi / MILL) for lbl, lo, hi in m.sensitivity(A)]
    rows.sort(key=lambda r: abs(r[2] - r[1]))
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for i, (lbl, lo, hi) in enumerate(rows):
        ax.barh(i, lo - base, left=base, color=TERRA, height=0.55,
                label="Driver -20%" if i == 0 else None)
        ax.barh(i, hi - base, left=base, color=FOREST, height=0.55,
                label="Driver +20%" if i == 0 else None)
    ax.axvline(base, color=INK, lw=1)
    ax.text(base, -0.85, f"base NPV {base:.1f}M", ha="center", fontsize=8.5,
            color=INK, fontweight="bold")
    ax.set_ylim(-1.1, len(rows) - 0.4)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlabel("NPV, ILS million (12% discount, exit 8x EBITDA)")
    ax.set_title("What moves the valuation? (+/-20% per driver)")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.grid(axis="y", visible=False)
    save(fig, "fig_tornado")


# ------------------------------------------------------------------ 6 risk heat map
def fig_risk_map() -> None:
    risks = m.load_risks()
    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    grid = np.add.outer(np.arange(1, 6), np.arange(1, 6))
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("rr", [SKY, CREAM, "#F2B38F", TERRA])
    ax.imshow(grid, origin="lower", extent=(0.5, 5.5, 0.5, 5.5), cmap=cmap, alpha=0.85)
    cells: dict[tuple[int, int], list[str]] = {}
    for r in risks:
        cells.setdefault((int(r["likelihood"]), int(r["impact"])), []).append(r["id"])
    for (li, im), ids in cells.items():
        for k, rid in enumerate(ids):
            x = li + 0.36 * (k - (len(ids) - 1) / 2)
            ax.scatter(x, im, s=330, color=FOREST, ec="white", lw=1.5, zorder=3)
            ax.text(x, im, rid, color="white", ha="center", va="center",
                    fontsize=7.5, fontweight="bold", zorder=4)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xlabel("Likelihood (1 = rare, 5 = almost certain)")
    ax.set_ylabel("Impact (1 = minor, 5 = critical)")
    ax.set_title("Risk heat map")
    ax.grid(False)
    save(fig, "fig_risk_map")


# ------------------------------------------------------------------ 7 resource comparison
def fig_resources() -> None:
    """Barbosa et al. (2015), lettuce, Yuma AZ: hydroponic vs conventional."""
    labels = ["Land yield\n(kg/m2/yr)", "Water use\n(L/kg/yr)", "Energy use\n(kJ/kg/yr, x1000)"]
    conv = [3.9, 250, 1.1]
    hydro = [41, 20, 90]
    fig, axes = plt.subplots(1, 3, figsize=(6.4, 2.6))
    for ax, lbl, c, h in zip(axes, labels, conv, hydro):
        ax.bar([0, 1], [c, h], color=[STONE, FOREST], width=0.6)
        ax.set_xticks([0, 1], ["Field", "Hydro"])
        ax.set_title(lbl, fontsize=9)
        for i, v in enumerate([c, h]):
            ax.text(i, v * 1.02, f"{v:g}", ha="center", fontsize=8.5)
        ax.set_ylim(0, max(c, h) * 1.22)
        ax.grid(axis="x", visible=False)
    fig.suptitle("Hydroponics: 10x land and 12x water efficiency, paid for in energy",
                 color=FOREST, fontweight="bold", fontsize=10)
    save(fig, "fig_resources")


# ------------------------------------------------------------------ tables + macros
TORNADO_HE = {
    "Price x yield (revenue/kg)": "המחיר והיבול לק\"ג",
    "HQ overhead": "עלות המטה",
    "Opex per roof": "עלות התפעול לגג",
    "Roof rollout speed": "קצב פריסת הגגות",
    "Capex per roof": "ההשקעה ההונית לגג",
    "Roof rent share": "דמי הגג",
}

def ils_k(v: float) -> str:
    """Thousands of ILS, wrapped LTR so a minus sign stays on the left (INC-003)."""
    k = round(v / 1e3)
    return f"\\en{{{k:,.0f}}}" if k else "0"


def write_table(name: str, colspec: str, lines: list[str]) -> None:
    """Emit a complete tabularx: \\rowcolor must be the first token of a row,
    which breaks when a bare row list is \\input inside tabular (INC-002)."""
    body = ["% AUTO-GENERATED by figures/python/make_figures.py — do not edit by hand.",
            "\\rrstripes",
            f"\\begin{{tabularx}}{{\\linewidth}}{{{colspec}}}"]
    body += lines + ["\\end{tabularx}"]
    (OUT / f"{name}.tex").write_text("\n".join(body) + "\n")


def write_tables() -> None:
    rows = [
        ("גגות פעילים (סוף שנה)", lambda y: f"{y.roofs_total}"),
        ("הכנסות תוצרת", lambda y: ils_k(y.rev_produce)),
        ("הכנסות \\en{SaaS}", lambda y: ils_k(y.rev_saas)),
        ("\\textbf{סך הכנסות}", lambda y: f"\\textbf{{{ils_k(y.revenue)}}}"),
        ("דמי גג לוועד הבית", lambda y: ils_k(-y.roof_rent)),
        ("עלות תפעול גגות", lambda y: ils_k(-y.opex_roofs)),
        ("\\textbf{רווח גולמי}", lambda y: f"\\textbf{{{ils_k(y.gross_profit)}}}"),
        ("מטה והנהלה", lambda y: ils_k(-y.overhead)),
        ("\\textbf{\\en{EBITDA}}", lambda y: f"\\textbf{{{ils_k(y.ebitda)}}}"),
        ("פחת", lambda y: ils_k(-y.depreciation)),
        ("מס", lambda y: ils_k(-y.tax)),
        ("\\textbf{רווח נקי}", lambda y: f"\\textbf{{{ils_k(y.net_income)}}}"),
    ]
    lines = ["\\rrtablehead \\rrth{\\shekel\\ אלפים} & " +
             " & ".join(f"\\rrth{{{y.year}}}" for y in YEARS) + " \\\\"]
    for label, fn in rows:
        lines.append(label + " & " + " & ".join(fn(y) for y in YEARS) + " \\\\")
    write_table("tab_pnl", "Y" + "r" * len(YEARS), lines)

    u = m.roof_unit_economics(A)
    assum = [
        ("שטח גידול נטו לגג", f"{A['grow_area_m2']:.0f}", "מ\"ר"),
        ("יבול שנתי", f"{A['yield_kg_m2_yr']:.0f}", "ק\"ג למ\"ר"),
        ("מחיר ממוצע משוקלל", f"{A['price_ils_kg']:.0f}", "\\shekel\\ לק\"ג"),
        ("ניצולת בשנה הראשונה של גג", f"{A['first_year_utilisation'] * 100:.0f}\\%", "—"),
        ("דמי גג לוועד הבית", f"{A['roof_rent_share'] * 100:.0f}\\%", "מההכנסות"),
        ("עלות תפעול לגג", ils_k(A['opex_per_roof_ils']), "אלפי \\shekel\\ לשנה"),
        ("השקעה הונית לגג", ils_k(A['capex_per_roof_ils']), "אלפי \\shekel"),
        ("רישיון \\en{RootOS}", f"{A['saas_price_ils_month']:,.0f}", "\\shekel\\ לחודש"),
        ("שיעור היוון", f"{A['discount_rate'] * 100:.0f}\\%", "—"),
        ("מכפיל יציאה", f"{A['exit_ebitda_multiple']:.0f}×", "\\en{EBITDA}"),
    ]
    lines = ["\\rrtablehead \\rrth{הנחה} & \\rrth{ערך} & \\rrth{יחידה} \\\\"]
    lines += [f"{a} & {b} & {c} \\\\" for a, b, c in assum]
    write_table("tab_assumptions", "Ycc", lines)

    risks = m.load_risks()
    lines = ["\\rrtablehead \\rrth{\\en{ID}} & \\rrth{סיכון} & \\rrth{ס.} & \\rrth{ה.} & \\rrth{מיתון} \\\\"]
    for r in risks:
        lines.append(f"{r['id']} & {r['name_he']} & {r['likelihood']} & {r['impact']} & "
                     f"{r['mitigation_he']} \\\\")
    write_table("tab_risks", ">{\\raggedright}p{6mm}>{\\raggedright\\arraybackslash}p{3.4cm}cc"
                ">{\\raggedright\\arraybackslash\\small}X", lines)

    # use of funds: roof capex is derived from the plan (red team #7), the rest from CSV
    import csv
    with open(m.DATA / "use_of_funds.csv", newline="") as f:
        uses = [(r["item_he"], float(r["amount_ils"])) for r in csv.DictReader(f)]
    seed = YEARS[0].equity_in
    seed_years = [y for y in YEARS if y.year < next(y.year for y in YEARS[1:] if y.equity_in)]
    capex_seed = sum(y.capex for y in seed_years)
    roofs_seed = sum(y.roofs_new for y in seed_years)
    uses = [(f"התקנת {roofs_seed} גגות ({seed_years[0].year}--{seed_years[-1].year})", capex_seed)] + uses
    reserve = seed - sum(v for _, v in uses)
    assert reserve > 0, "use of funds exceeds the seed round"
    uses.append(("רזרבה תפעולית", reserve))
    lines = ["\\rrtablehead \\rrth{שימוש} & \\rrth{אלפי \\shekel} & \\rrth{שיעור} \\\\"]
    lines += [f"{name} & {ils_k(v)} & \\en{{{v / seed * 100:.0f}\\%}} \\\\" for name, v in uses]
    lines.append(f"\\textbf{{סה\"כ}} & \\textbf{{{ils_k(seed)}}} & \\en{{100\\%}} \\\\")
    write_table("tab_use_of_funds", "Yrr", lines)

    basket_kg = A["basket_price_ils_month"] / (A["basket_kg_week"] * 52 / 12)
    weighted = A["restaurant_price_ils_kg"] * A["b2b_share"] + basket_kg * (1 - A["b2b_share"])
    assert abs(weighted - A["price_ils_kg"]) < 0.5, (
        f"channel prices give {weighted:.2f} ILS/kg but the model assumes {A['price_ils_kg']}")
    with open(m.DATA / "headcount.csv", newline="") as f:
        headcount = sum(int(r["count_2028"]) for r in csv.DictReader(f))
    sens = m.sensitivity(A)
    ranking = [lbl for lbl, lo, hi in sorted(sens, key=lambda r: -abs(r[2] - r[1]))]
    first, last = YEARS[0], YEARS[-1]
    be = next((y.year for y in YEARS if y.ebitda > 0), None)
    min_cash = min(YEARS, key=lambda y: y.cash_end)
    equity = sum(y.equity_in for y in YEARS)
    npv_v = m.npv(YEARS, A["discount_rate"], A["exit_ebitda_multiple"])
    macros = {
        "RRroofsFinal": f"{last.roofs_total}",
        "RRroofsFirst": f"{first.roofs_total}",
        "RRrevFinal": f"{last.revenue / MILL:.1f}",
        "RRrevFirst": f"{first.revenue / MILL:.2f}",
        "RRebitdaFinal": f"{last.ebitda / MILL:.1f}",
        "RRebitdaMarginFinal": f"{last.ebitda / last.revenue * 100:.0f}",
        "RRgrossMarginFinal": f"{last.gross_profit / last.revenue * 100:.0f}",
        "RRbreakEvenYear": f"{be}",
        "RRnpv": f"{npv_v / MILL:.1f}",
        "RRseed": f"{YEARS[0].equity_in / MILL:.0f}",
        "RRseriesA": f"{sum(y.equity_in for y in YEARS[1:]) / MILL:.0f}",
        "RRequityTotal": f"{equity / MILL:.0f}",
        "RRminCash": f"{min_cash.cash_end / MILL:.1f}",
        "RRminCashYear": f"{min_cash.year}",
        "RRroofKg": f"{u['kg']:,.0f}",
        "RRroofRevenue": f"{u['revenue'] / 1e3:,.0f}",
        "RRroofContribution": f"{u['contribution'] / 1e3:,.1f}",
        "RRroofPayback": f"{u['payback_years']:.1f}",
        "RRcapexRoof": f"{A['capex_per_roof_ils'] / 1e3:,.0f}",
        "RRprice": f"{A['price_ils_kg']:.0f}",
        "RRyield": f"{A['yield_kg_m2_yr']:.0f}",
        "RRarea": f"{A['grow_area_m2']:.0f}",
        "RRrentShare": f"{A['roof_rent_share'] * 100:.0f}",
        "RRdiscount": f"{A['discount_rate'] * 100:.0f}",
        "RRexitMultiple": f"{A['exit_ebitda_multiple']:.0f}",
        "RRsaasFarmsFinal": f"{last.saas_farms}",
        "RRkgFinal": f"{last.produce_kg / 1e3:,.0f}",
        "RRtam": f"{MARKET['TAM'][0]:,.0f}",
        "RRsam": f"{MARKET['SAM'][0]:,.0f}",
        "RRsom": f"{MARKET['SOM'][0]:.1f}",
        "RRsomShareSam": f"{MARKET['SOM'][0] / MARKET['SAM'][0] * 100:.1f}",
        "RRroofRent": f"{u['rent'] / 1e3:.1f}",
        "RRsaasRevFinal": f"{last.rev_saas / MILL:.2f}",
        "RRcapexSeed": f"{capex_seed / 1e3:,.0f}",
        "RRroofsSeed": f"{roofs_seed}",
        "RRreserve": f"{reserve / 1e3:,.0f}",
        "RRcontractYears": f"{A['contract_years']:.0f}",
        "RRdepYears": f"{A['depreciation_years']:.0f}",
        "RRrestPrice": f"{A['restaurant_price_ils_kg']:.0f}",
        "RRbtwoBshare": f"{A['b2b_share'] * 100:.0f}",
        "RRbasketMonth": f"{A['basket_price_ils_month']:.0f}",
        "RRbasketKgWeek": f"{A['basket_kg_week']:.1f}",
        "RRbasketKgPrice": f"{basket_kg:.1f}",
        "RRweightedPrice": f"{weighted:.1f}",
        "RRheadcount": f"{headcount}",
        "RRtornadoFirst": TORNADO_HE[ranking[0]],
        "RRtornadoSecond": TORNADO_HE[ranking[1]],
        "RRtornadoThird": TORNADO_HE[ranking[2]],
        "RRtornadoLast": TORNADO_HE[ranking[-1]],
        "RRhydroYield": "41", "RRfieldYield": "3.9",
        "RRhydroWater": "20", "RRfieldWater": "250",
        "RRhydroEnergy": "90,000", "RRfieldEnergy": "1,100",
    }
    body = ["% AUTO-GENERATED by figures/python/make_figures.py — do not edit by hand.",
            "% Numbers in the text must use these macros (qa-table / writer rule N1)."]
    body += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in macros.items()]
    (OUT / "numbers.tex").write_text("\n".join(body) + "\n")


if __name__ == "__main__":
    fig_revenue_mix()
    fig_cash_curve()
    fig_unit_waterfall()
    fig_market()
    fig_tornado()
    fig_risk_map()
    fig_resources()
    write_tables()
    print("generated:", ", ".join(sorted(p.name for p in OUT.iterdir())))
