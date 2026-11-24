PASS

# Investor review round 1 (investor-critic, Seed partner)

**Verdict: PASS (as written).** Would take a first call again after one roof has 3 months of real data.
**Overall score: 12 / 30.**

| Lens | Score | One-line reason |
|---|---|---|
| 1 The ask | 2 | NIS 6M, no valuation, no ownership %, and the "reserve" is not a reserve |
| 2 Unit economics | 2 | 1.9-year payback is a mature-year figure; the whole model is one unvalidated product, yield x price |
| 3 Market | 2 | TAM/SAM are unsourced "team estimates"; SOM is the plan's own output, not a share of anything |
| 4 Competition and moat | 1 | No named competitor; the moat (RootOS) is 9 lines of pseudocode with zero data behind it |
| 5 Execution risk | 2 | Permits, tenant vote, liability and insurance are one line each; no pilot before the money |
| 6 Narrative | 3 | Honest, clean, readable; but it tells me up front that nothing is validated |

**The single change that would most move my decision:** split the NIS 6M into a staged round whose first tranche (about NIS 0.5-0.8M) funds ONE instrumented pilot roof plus two or three signed LOIs (one building committee, two restaurants), with explicit go/no-go thresholds (kg/m2/yr, NIS/kg, opex per roof, weeks from signature to first harvest) that release the remaining capex. Today the plan commits 4 roofs (2027) and 8 more (2028, NIS 1.44M of capex) before any roof has produced a measurable harvest. Owner: Orchestrator (data/use_of_funds.csv, plan.csv) and the chapter-writer for 11-investment.

## Top 3 issues

1. **Nothing the model rests on has been tested, and the money is spent before it is.** `09-financials.tex:106`: "תפוקה של 30 ק"ג למ"ר ומחיר של 24 ש"ח לק"ג עדיין לא אומתו". `01-executive-summary.tex:23`: "אין עדיין הכנסות בפועל". No LOI, no signed committee, no pilot roof, no restaurant quote. A Seed round at this stage normally buys the pilot; here the "pilot" is 4 commercial roofs financed by the round.
2. **The financial case does not look like a venture return.** From `tab_pnl.tex` and `assumptions.csv`: 2031 EBITDA 3,204k x 8 = EV about NIS 25.6M, against NIS 20M of equity raised, i.e. about 1.3x before dilution, before any Seed investor's share. Net income in 2031 is 249k. NPV 4.3M is entirely terminal value (PV of terminal about 14.5M, so PV of the cash flows is about -10.2M). `09-financials.tex:90` admits "חלק גדול ממנו מגיע משווי היציאה". Nowhere does the plan show an exit path that returns a Seed fund.
3. **The 72k opex per roof and the 250 m2 net area look optimistic against the plan's own team chart.** `data/headcount.csv` shows 5 growers + 2 installers for 12 roofs in 2028, while the model charges only 576k of roof opex that year (4 mature x 72k + 8 half-year x 36k). Seven field FTE cost well above 576k before nutrients, water, power, delivery and lab tests. Either the staff sit in HQ overhead (then the headline "58% gross margin" is overstated), or opex per roof is understated.

---

## Lens 1: The ask (2/5)

Evidence:
- `11-investment.tex:4`: "גגון מגייסת 6 מיליון ₪ בסבב Seed ב-2027... סבב Series A של 14 מיליון ₪ מתוכנן ל-2029". Amount and use are stated. Missing: pre-money, % sold, option pool, instrument (equity / SAFE / convertible), lead or co-investor structure. A partner cannot even compute the entry price. `grep` for pre-money, dilution, shares: nothing in any chapter except `08-team.tex:7` ("מחזיקים בחלק העיקרי של ההון").
- Use of funds (`tab_use_of_funds.tex`): 2,160 + 1,500 + 1,300 + 600 + 440 = 6,000. OK arithmetically, but the "reserve" is cosmetic. HQ overhead for 2027-28 in `plan.csv` is 1,600 + 2,200 = 3,800k, while the three HQ lines total 3,400k. The 440k "reserve" therefore absorbs a 400k overhead gap and leaves about 40k. The reported minimum cash of 976k (`\RRminCash` = 1.0) exists only because the model books 936k of gross profit from 12 unvalidated roofs in 2027-28. `11-investment.tex:15` ("הרזרבה... נועדה לשמור על יתרת מזומנים בטוחה") is therefore misleading.
- Runway: 2028 burn is EBITDA -1,451k plus capex 1,440k = about 2.9M a year, or about 240k a month. Minimum cash 976k is about 4 months of runway at the exact moment Series A must close. In 2029 EBITDA is -858k and capex 2,880k, so cash is negative within the first quarter of 2029 unless Series A has already closed. Series A is in effect part of the Seed plan, but the Seed milestones (`11-investment.tex:19-20`) give the Series A investor only roofs that are 12-24 months old.
- `10-risks.tex:38` and `09-financials.tex:71` promise that Series A is "מועבר בתשלומים לפי אבני דרך". A company does not get to dictate that to its Series A investor; and the thresholds ("רצפה שקבע הדירקטוריון") are not numbers anywhere.

Routing:
- Orchestrator (data): add pre-money, instrument and ownership table to the model; reconcile `use_of_funds.csv` with `overhead_ils` (the reserve should be stated as about 40k or the overhead lines raised).
- Chapter-writer 11-investment: delete "הרזרבה... בטוחה" or restate it; add the Seed-to-Series-A bridge in months of runway.

## Lens 2: Unit economics (2/5)

Evidence (all from `assumptions.csv` and the P&L):
- Roof contribution 93.6k = 180k x (1 - 0.08) - 72k. Contribution margin 52%. Payback 180/93.6 = 1.92 years (`\RRroofPayback`, repeated in `01:6`, `01:20`, `05:51`, `09:18`, `11:15`, `11:34`).
- That figure is a mature-year simple payback. With the model's own first-year ramp (50% utilisation, opex also halved: `tab_pnl.tex` 2027 ops cost 144k = 4 x 36k) payback is about 2.4 years. If opex does not scale down in year 1 (labour is not variable), it is about 2.8 years. The plan should show the ramped figure; the 1.9 is the best case.
- It also excludes HQ overhead (3.8M in 2030) and the engineer's survey for the 40% of buildings that fail it (`06-marketing.tex:27`, conversion 60%). The cost of failed surveys is not in capex (R1 says the survey cost is "נכללת בהשקעה לגג", i.e. only for passed roofs).
- Fragility: the model is one assumption, `yield_kg_m2_yr` x `price_ils_kg` x `grow_area_m2` = revenue, against a roughly fixed 72k cost. Contribution = 0.92 R - 72. Break-even revenue per roof is 78.3k, i.e. 43.5% of the assumed 180k. At -20% price (19.2 NIS/kg) payback is about 3.0 years before ramp. At half the yield (15 kg/m2) contribution is 10.8k and payback 16.7 years, longer than the 5-year contract. The tornado (`09:94-103`) varies price x yield by +/-20% only; a 50% miss is the realistic range for a first commercial NFT roof.
- Assumptions I doubt:
  1. `grow_area_m2` = 250 m2 net on "6-8 floor" buildings (assumptions.csv note). A Gush Dan residential roof is shared with solar water heaters, AC units, antennas, stairwell and lift housings. 250 m2 of net channel area implies a very large clear roof. Need: a survey of 20-30 real roofs with measured usable area; `fig` or table with the median.
  2. `yield_kg_m2_yr` = 30. `03-solution.tex:66` correctly says Barbosa's 41 kg/m2/yr is for lettuce (hydroponic), but the plan sells a mixed basket of herbs where yield per m2 differs, on an exposed Israeli roof in summer (heat is R5, rated 3x4). Need: one season of data from an Israeli rooftop NFT system, or the grower's own greenhouse record.
  3. `price_ils_kg` = 24 with restaurants at 22 and basket at 26.9 per kg (`05:38-39`). Need: written price quotes from 3 restaurants and the retail price of comparable herbs and baby leaves in Tel Aviv. The 140 NIS/month basket works out to 26.9 NIS/kg on 1.2 kg/week, which is a premium to supermarket leaves; churn target is only "<5% a month" (`06:53`).
  4. `opex_per_roof_ils` = 72,000 vs the headcount chart (Top issue 3). Need: a bottom-up opex line (labour hours per roof per week, cost per grower, delivery cost per kg).
  5. Volume feasibility: 7,500 kg/roof/year x 60% B2B = 86 kg/week of restaurant demand per mature roof. `06-marketing.tex:8` anchors the first 4 roofs on "שלושה עד חמישה מסעדנים"; at 50% utilisation that is about 170 kg/week across 4 roofs, i.e. 35-58 kg/week per restaurant. Residents: 40% of volume = 3,000 kg/year = about 48 basket subscribers per roof, more than the apartments in many 6-8 floor buildings. Neither check is in the plan.
- CAC and LTV: not computed anywhere. `06-marketing.tex:52` lists CAC as a KPI with no number. A committee sale that converts 3.6% of mapped buildings (`06:35`), with a 5-9 month cycle, has a real CAC that is missing from both HQ overhead and the P&L. The marketing line in use of funds is NIS 600k in total.
- Gross margin: "58%" (`01:29`) includes SaaS revenue with no cost of revenue (tab_pnl: SaaS 1,620k, no hosting, support or LLM inference line). Produce-only gross margin in 2031 is (11,700 - 936 - 4,680) / 11,700 = 52%.
- Depreciation = contract = 5 years, so every roof is fully written off exactly when the committee gains negotiating leverage. No renewal, removal or churn assumptions exist; the 2027 cohort expires in 2032, just outside the horizon.

Routing:
- Orchestrator (data): add a sensitivity at -40/-50% on yield, a "ramped payback" output, SaaS cost of revenue, a failed-survey cost line, and a measured-roof-area input. Show opex split labour / consumables / logistics.
- Chapter-writer 05-business-model: replace "החזר... 1.9" with the ramped figure, or label it "simple, mature year".

## Lens 3: Market (2/5)

Evidence:
- `04-market.tex:7`: "כל הנתונים בסעיף זה הם הערכת צוות... מבוססים על ספירת בניינים". TAM 2,400M and SAM 380M (`04:10-11`) have no derivation, no source, no formula. The "building count" is mentioned but never shown. This is neither top-down (no Central Bureau of Statistics / import / consumption data, no cite) nor bottom-up (no number of eligible buildings x roofs x revenue per roof).
- SOM is not a market share: `04:12` "13.3 מיליון... על בסיס 80 גגות" is simply the plan's 2031 revenue, and it includes 1.62M of SaaS, which is outside a leafy-greens SAM (the text now admits this in brackets). The "3.5% of SAM" insight (`04:25`) is circular.
- Year-3 credibility: the plan's year 3 (2029) is 28 roofs and 3.87M revenue. The binding constraint is not market size but the funnel: `06-marketing.tex:35` says 28 mapped buildings give one signed contract. 8 roofs in 2028 means screening about 224 buildings; 30 roofs in 2031 means about 840. With no sales head until 2029 (`08-team.tex:36`; only one B2B account manager from 2028, who sells produce, not committee contracts) and a COO doing committee sales, I do not see who runs this funnel in 2028.
- SaaS: 15 external farms in 2029 and 90 by 2031 (`plan.csv`). Who are they? No count of Israeli hydroponic operators, no pricing test of 1,500 NIS/month, no explanation of why a farm running its own system buys a rooftop-NFT agent. This is 12% of 2031 revenue and carries 100% margin in the model, and about 0.6M of the 2031 EBITDA is plausibly attributable to it only if support cost is zero.
- Haifa and Beer Sheva have been removed, good; but the SAM is Gush Dan only, so 80 roofs must be found inside it with a 1 km radius constraint per roof. No map of restaurant density.

Routing:
- Orchestrator (data): add a bottom-up sheet to the model: eligible buildings (height, roof area, ownership type) x conversion funnel x revenue per roof, and a restaurant-demand check in kg/week per 1 km radius. Source: municipal GIS / Tel Aviv-Yafo building database, CBS building stock.
- Chapter-writer 04-market: cut the sentence "התוכנית אינה דורשת נתח שוק גבוה" (`04:15`), since the SOM is the plan, not a share. Replace with the building-count funnel.

## Lens 4: Competition and moat (1/5)

Evidence:
- `04-market.tex:42`: "לא זיהינו מתחרה ישיר... אנו מציגים קטגוריות כלליות ואיננו מנקבים בשמות של חברות." A partner reads this as "we did not do the research". Rooftop and urban-farm operators exist and are the obvious reference class (for example Lufa Farms in Montreal is the rooftop-greenhouse-plus-subscription-basket model; Gotham Greens on US roofs), and the sector's recent failures (AeroFarms, AppHarvest, Bowery) are the base rate an investor will bring to the table. The plan cites the vertical-farm literature (Kozai, Benke) but never mentions that well-funded indoor farms went bankrupt on exactly the cost-of-capex-and-energy problem the plan says it avoids.
- `04:66` and `04:76`: the moat is "חוזים ל-5 שנים... נתוני גידול של RootOS ויתרון מיקום". Each fails the 6-month copy test: (a) contracts are bilateral and do not stop a rival signing the next building (and the committee can ask the rival for 12% instead of 8%); (b) the data moat does not exist until roofs run, and the 2027 cohort will have 12 months of data at most; (c) location advantage is per roof, not defensible.
- RootOS: `03-solution.tex:42-53` shows a rule: read EC, if in band do nothing, else ask an LLM for a dose and escalate large doses to a human. That is a thin wrapper over standard hydroponic controllers and a general-purpose model. The plan spends NIS 1.5M (25% of the round) on a "production version" without saying what is proprietary: a leaf-disease vision model trained on what dataset? Labelled by whom? Which agronomic model reduces labour from 2.4 roofs per grower (headcount chart) to the "many roofs per grower" claimed in `01:26`?
- The building committee as competitor is not addressed: a committee that sees 180k of roof revenue and 14.4k of rent (`05:66`, about NIS 480 per apartment per year for 30 apartments) can hire a grower directly or sell to a rival.
- Imports and conventional produce are listed in the table (`04:55`) as "זול" but there is no price comparison per kg, which is the thing the restaurant decides on.

Routing:
- Chapter-writer 04-market: name at least 5 competitors (rooftop and urban farms, Israeli CEA players, controller vendors) with funding and status; add one row per comparable with price per kg and business model.
- Chapter-writer 03-solution / Orchestrator: state what RootOS owns (dataset size by 2028, model, integrations) and what happens if a competitor buys an off-the-shelf controller.

## Lens 5: Execution risk (2/5)

Evidence:
- Regulation: `07-operations.tex:11` has one line, "בקשה לרשות המקומית, אישור כיבוי אש ובטיחות, והסכמת הדיירים", inside a process that is said to take about 6 weeks from signature (`07:7`). Permit, fire-brigade and tenants' consent steps are placed inside that 6-week window, while the funnel itself (`06:25-29`) shows 5-6 months before signature. R6 (permit delay) is rated likelihood 2, impact 3 (`risks.csv`); I would rate it 4 x 4 for a first-of-kind rooftop use in Israeli municipalities. I am not a lawyer; the plan must carry a written legal opinion on (a) whether a rooftop agricultural structure needs a building permit or change-of-use, (b) the owner-consent threshold for use of common property (the plan says only "רוב", `06:17`), (c) Water Authority and Ministry of Health treatment of a commercial food source on a residential roof.
- Roof load: `risks.csv` R1 mitigates with "<60 kg/m2". The plan does not say what the design live load of a typical Gush Dan roof is, or how much of the stock passes. The funnel assumes a 60% pass rate (`06:27`) with no source.
- Liability and insurance: not mentioned in any chapter (grep). Water leakage into apartments, a worker falling, a pump fire, a food-borne contamination: who is liable, who insures, and what does it cost per roof? A single leak claim hits the "אין פשרות" reputation point in R1 across all committees.
- Heat and power: R5 (heat/outage, 3 x 4) mitigated by shade nets and battery; no cost in capex 180k (`assumptions.csv` capex: "structural survey + NFT system + sensors + shade net": battery missing).
- Team gaps: three founders, no named hydroponics grower with commercial roof experience (CEO is an agronomist, ex greenhouse manager, `08:14`); no one owns committee sales and legal until a head of sales in 2029; the advisory board is "ללא שמות בשלב זה" (`08:51`). Founders' full-time status and vesting are not stated. COO background is food delivery, fine for logistics but not construction. 2027 installers and engineer are contractors (`08:34`), so scale-up of installation is subcontracted at the exact point where the plan says growth is "מוגבלת על ידי קצב ההתקנה" (`07:38`).
- Riskiest assumption: the combined yield x price x opex of an Israeli rooftop (Lens 2). Does a pilot test it? The plan says "ייבדק בפיילוט" 7 times but no pilot is scheduled, sized or funded separately from the 4-roof rollout, and no success threshold is stated. `11-investment.tex:27` says the plan "תלויה בהוכחת הנחות היסוד בפיילוט", then commits 1.44M of capex for 2028 before the pilot has a full harvest cycle.
- R8 (funding gap, 3 x 5) is the largest risk by the plan's own matrix and its mitigation is another financing event.

Routing:
- Orchestrator (data): re-rate R6 and add R9 (insurance/liability) and R10 (tenant consent) to `risks.csv`; add battery and insurance to capex or opex.
- Chapter-writer 07-operations / 10-risks: separate the funnel timeline (5-6 months before signature) from the 6-week installation, or show where permits sit; add the legal opinion as a stated deliverable of 2027.

## Lens 6: Narrative (3/5)

What works: `01-executive-summary.tex` is complete, short and honest: three key numbers at the top (`01:4-6`), problem, solution, market, unit economics, financials, ask. The language is plain, and there is no inflated claim after the round-1 cleanup ("טרם אומת", `01:26`). `01:23` says "התוכנית היא תוכנית ולא ביצוע" and the risk is correctly identified as rollout speed (`01:35`).

Why it does not get me a second meeting from the summary alone:
- The ask paragraph (`01:32`) gives no valuation and says nothing about what the NIS 6M buys in terms of proof; the milestones are in chapter 11, not on page 1.
- The three advantages (`01:26`) are "נכס זול... ביקוש צפוי (טרם אומת)... RootOS". The first is unproven, the second is declared unproven in the same sentence, the third has no evidence. That is a candid pitch, not a persuasive one.
- The summary does not name a single competitor, customer, LOI, advisor, or number about the team beyond three first names.
- The payback box (`01:35`) repeats 1.9 years as the headline, which is the best-case figure.
- Cut: "הגג הוא נכס ריק" (`01:11`), a slogan; and "ביקוש מקומי צפוי" as an advantage. Replace with one fact: how many committees or restaurants have already said yes.
- The key number "הכנסות ב-2031: 13.3M" is 5 years out. Show instead the number I fund against: month-18 proof (kg/m2/yr measured, NIS/kg achieved, roofs signed).

Routing: chapter-writer 01-executive-summary.

---

## The 10 hardest questions for the meeting

| # | Question | Tag |
|---|---|---|
| 1 | What is the pre-money valuation, what percentage do you sell for NIS 6M, and what do I own after Series A? What return do you show me if EBITDA 2031 is 3.2M and the multiple is 8x (EV about 25.6M on 20M raised)? | **MISSING** (no valuation anywhere; return arithmetic only implied in `09-financials.tex:90`, `assumptions.csv` exit_ebitda_multiple) |
| 2 | Which roof have you measured? What is the net usable area of a real 6-8 floor Gush Dan roof, after boilers, AC and stairwell, and why is it 250 m2? | **WEAK** (`assumptions.csv` grow_area_m2 note; `07-operations.tex:10` mentions survey only as a process step) |
| 3 | What yield do you expect in July on an exposed roof, for a herb-heavy mix, versus the lettuce figure of Barbosa 2015, and what happens to payback at 15 kg/m2? | **WEAK** (`03-solution.tex:66` cites 41 for lettuce; `09-financials.tex:106` says "לא אומתו"; tornado covers only +/-20%, `09:94`) |
| 4 | Who has already said yes: how many committees, restaurants, signed LOIs, quotes at 22 NIS/kg? Where is the 3-5 restaurants anchor, and can 3-5 restaurants absorb 170 kg/week? | **MISSING** (`01-executive-summary.tex:26`, `06-marketing.tex:8` only intent; no LOI) |
| 5 | Your funnel converts 1 in 28 buildings. Who sells to committees in 2028 (no sales head until 2029), what is the CAC per signed roof, and what is the cost of the 40% that fail the structural survey? | **WEAK** (`06-marketing.tex:35`, CAC listed as KPI at `06:52` with no value; `08-team.tex:36`) |
| 6 | Walk me through permits, owner consent threshold, fire brigade, Water Authority, Ministry of Health and insurance. Who is liable if a roof leaks into an apartment? Do you have a legal opinion? | **WEAK** (`07-operations.tex:11` one line; `risks.csv` R6 rated 2x3; insurance **MISSING**) |
| 7 | Why can't a vertical-farm operator, a retail chain, or the building committee itself replicate you in 6 months? What exactly is proprietary in RootOS, which dataset, and what is the 5-year contract worth to the committee against NIS 14.4k a year? | **WEAK** (`04-market.tex:66,76`; `03-solution.tex:42-53` shows a generic rule; no competitor named, `04:42`) |
| 8 | Show me opex per roof bottom-up. With 5 growers and 2 installers for 12 roofs in 2028 and only 576k of roof opex, how is 72k per roof achievable? How many roofs does one grower run? | **WEAK** (`assumptions.csv` opex_per_roof_ils; `headcount.csv`; `01-executive-summary.tex:26` claims "מגדל אחד לגגות רבים" without number) |
| 9 | Month 18: if the 2027 roofs deliver half the plan, what do you do with the 1.44M capex already scheduled for 2028 and 976k cash left? What exactly are the Series A tranche milestones and who decides them? | **WEAK** (`10-risks.tex:38` "רצפה שקבע הדירקטוריון" without number; `11-investment.tex:27`; no stage gate) |
| 10 | Who are the 90 external farms paying 1,500 NIS a month, what is your cost to support them, and what happens to the roofs after the 5-year contract ends in 2032 (renewal, removal, rent renegotiation)? | **MISSING** (SaaS only `05-business-model.tex:47`, `04:35`; no renewal in any chapter; `depreciation_years` = `contract_years` = 5) |

## Consistency points found while reading (for the owning writers; not typos)

| Item | Where | Issue | Route |
|---|---|---|---|
| Reserve | `11-investment.tex:15`, `use_of_funds.csv` vs `plan.csv` | 440k "reserve" absorbs a 400k overhead gap (3,400k lines vs 3,800k overhead); true free reserve about 40k before revenue | Orchestrator (data) |
| Gross margin | `01:29`, `09:31` | 58% blends 100%-margin SaaS; produce-only 52% | Orchestrator, writer 09 |
| Payback | `01:6`, `01:20`, `05:51`, `11:15` | 1.9 is mature-year; ramped payback is about 2.4 | writer 05, 01 |
| Opex ramp | `tab_pnl.tex` 2027: ops cost 144k on 4 roofs | Model halves roof opex in year 1 (36k), while `assumptions.csv` note says labour is part of opex and labour does not halve | Orchestrator (data) |
| Risk register | `risks.csv` R6 | Regulatory delay rated 2; funnel and operations chapters both identify permits and consent as the slowest steps | Orchestrator, writer 10 |
| Capex scope | `assumptions.csv` capex_per_roof_ils | Excludes battery for pumps (R5 mitigation), insurance, failed surveys | Orchestrator |
| Sales head timing | `08-team.tex:35-36` | Committee sales (the hardest step, `06:59`) has no owner until 2029, after 12 roofs must already be signed | writer 08 |

## What would turn this into a SECOND MEETING

1. A pilot roof with logged data (or a comparable grower's data on a real Israeli roof), and two LOIs.
2. A valuation, an ownership table and a return case that reaches at least 10x on the Seed ticket, with a defined 2032+ path beyond the 5-year horizon.
3. A bottom-up market sheet (buildings x roof area x conversion) replacing the unsourced TAM/SAM.
4. A named competitor table including rooftop operators and failed indoor farms, plus one clear sentence on what RootOS owns.
5. A legal and insurance note covering permits, owner consent and liability.
