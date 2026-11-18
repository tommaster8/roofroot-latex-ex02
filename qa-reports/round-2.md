PASS

# QA round 2 (red team verification, qa-detector)

Build: main.pdf 42 pages, cls v1.2, not rebuilt. `qa_scan.py` re-run: **CRITICAL 0 · MAJOR 0 · MINOR 0** (verified, scan-latest.md empty table).
Open + new: **CRITICAL 0 · MAJOR 0 · MINOR 4** (3 new, 1 accepted carry-over). Exit criterion met.
Method: scan; all 42 pages rendered at 50 dpi (4-up) plus 90-110 dpi crops of pricing table, org chart, timeline, use-of-funds, bibliography; `pdftotext -bbox-layout` probes for every cite/bibliography claim; model re-run (`model.run`, `model.npv`, `model.sensitivity`); both qa-super content greps.

## A. Verification of round-1 findings

| R1 # | Status | Evidence |
|---|---|---|
| 1 bib label collision | FIXED | bbox p.42: labels `[n]` at x=44-57, entry text starts x=68 on every one of 11 entries; no overlap. Visual check clean. |
| 2 bib overfull | FIXED | `grep -c Overfull main.log` = 0. DOI lines end at x<=437 (margin 527). |
| 3 cite garbled in caption / LoF | FIXED | No `\cite` in any `\caption` (grep empty); fig 3.2 caption on p.12 and LoF p.iv read "(המקור בגוף הטקסט)"; body cites `[3]` with correct brackets. |
| 4 period vs cite order | FIXED | All 18 body cites probed in bbox: bracket token is whole (`[8]`, `[10]`) and the sentence period has smaller x (e.g. p.15 `.`@260 < `[8]`@263; p.18 `.`@? left of `[10]`). No scrambled brackets anywhere. |
| 5 hydro/field yield reversed | FIXED | p.6 text "41 ... לעומת 3.9"; macros `\RRhydroYield=41`, `\RRfieldYield=3.9` match fig 3.2. |
| 6 tornado ranking | FIXED | Re-ran `model.sensitivity`: swings price x yield 24.8M, HQ overhead 12.1M, opex 10.8M, rollout 10.4M, capex 3.7M, rent 2.1M. Macros: first=price/yield, second=HQ, third=opex, last=roof rent. Matches chart p.31 (printed 25). |
| 7 use-of-funds capex | FIXED | Table p.37 (printed 31): 2,160 (4x180 + 8x180 from plan.csv), 1,500+1,300+600+440 -> sum 6,000; % 36/25/22/10/7 = 100. Table generated (`tab_use_of_funds.tex`). Text 12 roofs, 180k each, reserve 440 consistent; min cash 0.976M = "1.0" in 2028 OK. |
| 8 pricing 27 vs 25 | FIXED | Basket 140 ILS/month, 1.2 kg/week -> 140/(1.2x4.33)=26.9; 22x0.6+26.9x0.4=23.96 -> 24.0 = `price_ils_kg`. Table p.19 (printed 13) and text agree; all from macros. |
| 9 SOM share | FIXED | List and insight box (p.14) say "כ-3.5% מה-SAM"; SaaS inclusion in SOM is now stated ("ה-SOM כולל גם הכנסות רישוי"). |
| 10 proven/guaranteed demand | FIXED | grep V1 hits only ch3:73 "מערכת גידול מוכחת (NFT)" (technology, not demand); see new N3. |
| 11 exec-summary cites | FIXED | santamouris/oberndorfer now only in ch2 (heat/ecosystem) and ch5 (general roof cooling); exec summary sentence uncited. |
| 12 headcount | FIXED | headcount.csv sums 14 (1+1+1+5+2+2+1+1); org chart p.26 shows CEO, COO(5 growers + installer/engineer), CTO(2 RootOS), B2B, part-time finance = 14; caption uses `\RRheadcount`; sales head moved to 2029 (hiring list p.26). |
| 13 timeline/milestones | FIXED | Timeline p.24: Seed 2027, 4 pilot roofs Gush Dan, RootOS production 2027, Series A 2029, SaaS 2029, EBITDA 2030, 80 roofs 2031; dot positions checked against ticks. Matches ch11 list. Haifa/Beer Sheva gone. |
| 14 eq labels unreferenced | FIXED | scan 0 findings; `\eqref` present. |
| 15 depreciation 7 vs contract 5 | FIXED | assumptions.csv depreciation_years=5, `\RRdepYears`/`\RRcontractYears` used; EBIT in tab_pnl reflects 5y (model run: 2031 EBIT 324k, NI 249k = table 249). |
| 16 weak cites | FIXED | kozai2020 for lighting energy, yao2023 only for reason-act loop, "לראשונה" removed (grep clean), benke only vertical farming. |
| 17 energy contradiction ch3/ch4 | PARTIAL | ch4 reworded (sunlight; electricity for pumps/sensors). SWOT figure still lists "צריכת חשמל גבוהה ממשאבות ותאורה" (see N1). Minor. |
| 18 SaaS stage 2029 | FIXED | ch6 stage 2 now contains RootOS licence sales "מ-2029". |
| 19 tranche Seed/Series A | FIXED | ch9 insight and ch10 R8 both refer to Series A milestone tranche. |
| 20 ESG governance | FIXED | p.21 (8.4) "ממשל תאגידי". |
| 21 bare team tables | FIXED | Tables 8.1 and 8.2 in floats with caption and refs (p.25-26). |
| 22 English risk register | FIXED | tab_risks / table 10.1 p.33 Hebrew name and mitigation columns; heat-map figure English only. |
| 23 stray scan file | FIXED | `scripts/` contains build.sh, check-chapter.sh, qa_scan.py only. |
| 24 underfull hbox | WONTFIX-MINOR (accepted) | 35 Underfull, none visible at 50-110 dpi; all in paragraphs at main.tex:57 (no layout impact). |
| 25 half-empty chapter-end pages | WONTFIX-MINOR (accepted) | Pages 4, 10 (printed 4, 11) still half blank; no orphan headings. Not a defect. |

Bibliography page (p.42), use-of-funds (p.37), pricing (p.19), org chart (p.26), timeline (p.24), cover (p.1) all visually clean; no overflow, reversed text, or missing glyph. No regressions from the fixes found (numbers 4.3 NPV = model 4.289; break-even 2030; roofs 80; rev 13.3; EBITDA 3.2/24%).

## B. Content greps (qa-super "added after round 1")

1. `grep -nE "מוכח|מובטח|לראשונה|היחידים" chapters/*.tex` -> one hit, `03-solution.tex:73` "מערכת גידול מוכחת (NFT)" (N3).
2. `grep -n "\\\\caption{[^}]*\\\\cite" chapters/*.tex` -> no hits.
Ranking sentences cross-checked against generated data (tornado, section A #6). Chapter 1-2 cites: santamouris/oberndorfer (ch2 heat island, ecosystem services) support; fao2017/specht2014/barbosa2015/resh2012 on topic; yao2023 limited to the reason-act loop; benke/kozai on CEA. No unrelated cite found.

## C. NEW findings

| # | Severity | Skill | File:line / page | Evidence | Proposed systemic fix (CLS/Skill) |
|---|---|---|---|---|---|
| N1 | MINOR | qa-super (content) | `figures/tikz/swot.tex:16`; PDF p.16 (fig 4.2) | SWOT weakness "צריכת חשמל גבוהה ממשאבות ותאורה" while ch4:44 (fixed #17) says the roof system grows by sunlight and electricity is for pumps and sensors; "lighting" re-introduces the contradiction. | **text** (swot.tex): "צריכת חשמל למשאבות וחיישנים". **skill**: qa-super content check "grep figure TikZ text for claims restated in chapters". |
| N2 | MINOR | qa-super (content) | `chapters/11-investment.tex:22`; PDF p.37 | List item reads "2030: EBITDA חיובי (2030)" - year stated twice. | **text**: drop "(\RRbreakEvenYear)" or the bold label. |
| N3 | MINOR | qa-super (content) | `chapters/03-solution.tex:73`; PDF p.11 | "מערכת גידול מוכחת (NFT)" is an uncited superlative-style claim hit by the V1 grep (proven technology, not demand, so low risk). | **text**: "מערכת גידול מקובלת" or add `\cite{resh2012}`; **skill**: add an allowlist mechanism to the V1 grep so reviewed hits are not re-reported. |
| N4 | MINOR (carry-over) | qa-typeset | `main.log` 35 Underfull hbox at main.tex:57; pages 4 and 10 half blank | Accepted as WONTFIX-MINOR (see #24, #25). | none required |

## D. Notes for the Orchestrator
- No CHANGELOG file outside `roofroot.cls`; the cls CHANGELOG block lists v1.0-v1.2 and agrees with `\ProvidesClass` and `\rr@clsversion` (qa-cls-version OK).
- Round-1 false alarm trap repeated: my own 50 dpi/downscaled views suggested indented single-line list items; bbox shows all list lines flush at x=527. No defect. (Use bbox, not scaled screenshots, for alignment claims.)
