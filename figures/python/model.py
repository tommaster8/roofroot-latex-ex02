"""RoofRoot five-year financial model.

Single source of truth: data/assumptions.csv + data/plan.csv.
Every chart, every LaTeX table and every number quoted in the text
(via figures/generated/numbers.tex) is derived from this module.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def load_assumptions() -> dict[str, float]:
    with open(DATA / "assumptions.csv", newline="") as f:
        return {row["key"]: float(row["value"]) for row in csv.DictReader(f)}


def load_plan() -> list[dict[str, float]]:
    with open(DATA / "plan.csv", newline="") as f:
        return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]


def load_risks() -> list[dict[str, str]]:
    with open(DATA / "risks.csv", newline="") as f:
        return list(csv.DictReader(f))


@dataclass
class Year:
    year: int
    roofs_total: int
    roofs_new: int
    saas_farms: int
    produce_kg: float = 0.0
    rev_produce: float = 0.0
    rev_saas: float = 0.0
    roof_rent: float = 0.0
    opex_roofs: float = 0.0
    overhead: float = 0.0
    capex: float = 0.0
    depreciation: float = 0.0
    equity_in: float = 0.0
    ebitda: float = 0.0
    ebit: float = 0.0
    tax: float = 0.0
    net_income: float = 0.0
    free_cash_flow: float = 0.0
    cash_end: float = 0.0
    extras: dict = field(default_factory=dict)

    @property
    def revenue(self) -> float:
        return self.rev_produce + self.rev_saas

    @property
    def gross_profit(self) -> float:
        return self.revenue - self.roof_rent - self.opex_roofs


def roof_unit_economics(a: dict[str, float]) -> dict[str, float]:
    """Steady-state economics of one roof for one full year (ILS)."""
    kg = a["grow_area_m2"] * a["yield_kg_m2_yr"]
    revenue = kg * a["price_ils_kg"]
    rent = revenue * a["roof_rent_share"]
    opex = a["opex_per_roof_ils"]
    dep = a["capex_per_roof_ils"] / a["depreciation_years"]
    contribution = revenue - rent - opex
    return {
        "kg": kg,
        "revenue": revenue,
        "rent": rent,
        "opex": opex,
        "contribution": contribution,
        "depreciation": dep,
        "payback_years": a["capex_per_roof_ils"] / contribution,
    }


def run(a: dict[str, float] | None = None, plan: list[dict] | None = None) -> list[Year]:
    a = a or load_assumptions()
    plan = plan or load_plan()
    years: list[Year] = []
    roofs_total, cash, capex_hist = 0, 0.0, []
    per_roof_kg = a["grow_area_m2"] * a["yield_kg_m2_yr"]
    for p in plan:
        new = int(p["new_roofs"])
        mature = roofs_total                      # roofs that existed last year
        roofs_total += new
        y = Year(int(p["year"]), roofs_total, new, int(p["saas_farms"]))
        y.produce_kg = per_roof_kg * (mature + new * a["first_year_utilisation"])
        y.rev_produce = y.produce_kg * a["price_ils_kg"]
        y.rev_saas = y.saas_farms * a["saas_price_ils_month"] * 12
        y.roof_rent = y.rev_produce * a["roof_rent_share"]
        y.opex_roofs = a["opex_per_roof_ils"] * (mature + new * a["first_year_utilisation"])
        y.overhead = p["overhead_ils"]
        y.capex = new * a["capex_per_roof_ils"]
        capex_hist.append(y.capex)
        y.depreciation = sum(capex_hist[-int(a["depreciation_years"]):]) / a["depreciation_years"]
        y.ebitda = y.gross_profit - y.overhead
        y.ebit = y.ebitda - y.depreciation
        y.tax = max(0.0, y.ebit) * a["tax_rate"]
        y.net_income = y.ebit - y.tax
        y.free_cash_flow = y.ebitda - y.tax - y.capex
        y.equity_in = p["equity_in_ils"]
        cash += y.free_cash_flow + y.equity_in
        y.cash_end = cash
        years.append(y)
    return years


def terminal_value(years: list[Year], multiple: float) -> float:
    """Exit value at the end of the plan: final-year EBITDA x multiple."""
    return max(0.0, years[-1].ebitda) * multiple


def npv(years: list[Year], rate: float, multiple: float = 0.0) -> float:
    """NPV of free cash flow (+ discounted terminal value), eq. (npv) in ch. 9."""
    n = len(years)
    flows = sum(y.free_cash_flow / (1 + rate) ** (i + 1) for i, y in enumerate(years))
    return flows + terminal_value(years, multiple) / (1 + rate) ** n


def sensitivity(a: dict[str, float], swing: float = 0.2) -> list[tuple[str, float, float]]:
    """NPV low/high when each driver moves by +/- swing (tornado chart)."""
    base_plan = load_plan()
    drivers = {
        "Price x yield (revenue/kg)": ("price_ils_kg", +1),
        "Opex per roof": ("opex_per_roof_ils", -1),
        "Capex per roof": ("capex_per_roof_ils", -1),
        "Roof rent share": ("roof_rent_share", -1),
    }
    out = []
    for label, (key, _sign) in drivers.items():
        lo, hi = dict(a), dict(a)
        lo[key] *= 1 - swing
        hi[key] *= 1 + swing
        out.append((label,
                    npv(run(lo, base_plan), a["discount_rate"], a["exit_ebitda_multiple"]),
                    npv(run(hi, base_plan), a["discount_rate"], a["exit_ebitda_multiple"])))
    # rollout speed: scale the number of new roofs
    slow = [dict(p, new_roofs=round(p["new_roofs"] * (1 - swing))) for p in base_plan]
    fast = [dict(p, new_roofs=round(p["new_roofs"] * (1 + swing))) for p in base_plan]
    out.append(("Roof rollout speed",
                npv(run(a, slow), a["discount_rate"], a["exit_ebitda_multiple"]),
                npv(run(a, fast), a["discount_rate"], a["exit_ebitda_multiple"])))
    lean = [dict(p, overhead_ils=p["overhead_ils"] * (1 - swing)) for p in base_plan]
    heavy = [dict(p, overhead_ils=p["overhead_ils"] * (1 + swing)) for p in base_plan]
    out.append(("HQ overhead",
                npv(run(a, heavy), a["discount_rate"], a["exit_ebitda_multiple"]),
                npv(run(a, lean), a["discount_rate"], a["exit_ebitda_multiple"])))
    return out
