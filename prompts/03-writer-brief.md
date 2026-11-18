# Prompt 03 — Writer brief (sent to all three chapter-writer agents)

**Model:** Sonnet ×3 in parallel · each gets this brief + its own chapter list

```text
You are writing chapters of "גגון / RoofRoot — תוכנית עסקית 2027", a seed-stage
business plan for investors. Language: Hebrew, with English terms where natural.
Project root: /Users/tomrubin/Desktop/pdf latex

THE VENTURE (shared facts — do not contradict):
- RoofRoot installs NFT hydroponic systems on the roofs of 6+ floor residential
  buildings in Gush Dan, under 5-year agreements with the building committee
  (ועד בית), which receives \RRrentShare% of the roof's revenue.
- Each roof: \RRarea m² growing area, \RRyield kg/m²/yr leafy greens & herbs,
  \RRroofKg kg/yr, average price \RRprice ILS/kg → \RRroofRevenue thousand ILS/yr,
  capex \RRcapexRoof thousand ILS, payback \RRroofPayback years.
- Customers: restaurants & cafés within 1 km (B2B), residents' "סל ירוק"
  subscription, and from 2029 external farms licensing the RootOS software.
- RootOS: an AI agent (LLM planner + leaf-vision model) reading pH/EC/temperature/
  flow sensors, acting on pumps/shade/irrigation, escalating unusual actions to a
  human grower (human-in-the-loop), with a digital-twin yield forecast.
- Plan: \RRroofsFirst roofs in 2027 → \RRroofsFinal in 2031; revenue
  \RRrevFinal M ILS in 2031; EBITDA positive in \RRbreakEvenYear; NPV \RRnpv M ILS.
- Funding: Seed \RRseed M ILS now (2027), Series A \RRseriesA M ILS in 2029.
- Founding team (fictional): CEO נועה ברק (agronomist, ex-greenhouse manager),
  CTO עידו שחר (ML engineer, robotics), COO מאיה לוי (operations, ex-food-delivery).

READ FIRST: .claude/skills/writer-he-en/SKILL.md, .claude/skills/qa-BiDi/SKILL.md,
figures/generated/numbers.tex (all macros), references.bib (allowed cite keys).

ASSETS YOU MUST USE IN YOUR CHAPTERS (each exactly once, in the listed chapter):
  Python charts (figures/generated): fig_resources (ch3), fig_market (ch4),
    fig_unit_waterfall (ch5), fig_revenue_mix, fig_cash_curve, fig_tornado (ch9),
    fig_risk_map (ch10)
  TikZ (figures/tikz): architecture (ch3), swot (ch4), bmc (ch5),
    timeline (ch7), orgchart (ch8)
  Generated tables: tab_assumptions, tab_pnl (ch9), tab_risks (ch10)

HARD RULES
 R1 Numbers that exist as macros MUST use the macro. Never type 13.3, 2030 (as the
    break-even year), 7,500 etc. by hand. Text numbers not in the model must be
    consistent with it.
 R2 Cite only keys in references.bib. Market sizes are "הערכת צוות". No invented
    statistics attributed to real organisations.
 R3 Each chapter ≥ 1.5 pages of real content (exec summary: exactly 2 pages),
    at least one insightbox or riskbox, at least one \ref to a figure/table.
 R4 Labels: ch:<name>, fig:<name>, tab:<name>, eq:<name>. Reference before the float.
 R5 No \textbullet, no [H], no hard \\ line breaks in prose, no \vspace hacks.
 R6 Hand-made tables use \rrstripes + \rrtablehead + \rrth.
 R7 After writing, run scripts/check-chapter.sh <file-stem> for EACH of your chapters
    and LOOK at the rendered PDF (pdftoppm -r 50); compiling is not enough (INC-005).
    (isolated build in build/; never run scripts/build.sh — other writers run in
    parallel). It must compile with no errors. Fix errors in YOUR files only.
 R8 Do not edit roofroot.cls, main.tex, data/, figures/ or other writers' chapters.
    If you think the class needs a change, say so in your final report.

FINAL REPORT (≤ 15 lines): files written, approx. pages each, any doubts.
```

## Chapter assignment
| Agent | Chapters |
|---|---|
| writer-strategy | 01-executive-summary, 02-problem, 03-solution, 11-investment |
| writer-market | 04-market, 05-business-model, 06-marketing, 07-operations |
| writer-finance | 08-team, 09-financials, 10-risks |
