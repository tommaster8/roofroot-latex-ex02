---
name: writer-he-en
description: House style for writing RoofRoot business-plan chapters in Hebrew with embedded English, in LaTeX for roofroot.cls. Use whenever writing or editing chapters/*.tex.
---
# writer-he-en — house style for chapter writers

## Voice
Investor-grade Hebrew: short declarative sentences, active voice, numbers before adjectives.
"גג אחד מחזיר את ההשקעה בו תוך 1.9 שנים" ✔  — "הפתרון החדשני והמהפכני שלנו" ✘.
Every section ends with a "so what" for the investor.

## LaTeX contract
- One file per chapter: `\chapter{...}\label{ch:...}` then `\section`s. No `\documentclass`, no preamble.
- English terms: `\en{...}` (see qa-BiDi B1–B3). Prefix: `ה-\en{SaaS}`.
- Numbers from the model: **macros only** (`\RRrevFinal{}` מיליון \shekel). List: `figures/generated/numbers.tex`.
- Currency: `\shekel` (e.g. `\RRprice~\shekel{} לק"ג`).
- Boxes: `insightbox` (takeaway), `riskbox` (risk), `\keynumber{value}{label}` (three in a row with `\hfill`).
- Figures: `\begin{figure}[htbp]\centering ... \caption{...}\label{fig:...}\end{figure}`;
  Python charts: `\includegraphics[width=0.92\linewidth]{fig_name}`;
  TikZ: `\resizebox{\linewidth}{!}{\input{figures/tikz/name.tex}}`.
- Generated tables: `\begin{table}[htbp]\centering\small\input{figures/generated/tab_x.tex}\caption{}\label{}\end{table}`.
- Hand tables: `\rrstripes\begin{tabularx}{\linewidth}{...}\rrtablehead\rrth{..}&..\\ ...\end{tabularx}`.
- Equations: `\begin{equation}...\label{eq:...}\end{equation}`, variables explained in a list after it.
- Citations: `\cite{key}` with keys **only** from `references.bib`. Never invent a source; market figures that are our estimates are labelled "הערכת צוות".
- Lists: `itemize`/`enumerate` (never `\textbullet`).

## Rules added after red-team round 1
- **C2 — a citation must support *this* sentence.** Before `\cite{k}`, read the title of `k` in `references.bib`; a heat-island paper does not support a claim about produce freshness (round 1 #11, #16).
- **C3 — no citations inside `\caption`.** Put the cite in the body; captions are copied to the List of Figures.
- **N2 — derived numbers are macros too.** If you compute a number from model values (8% × 180 = 14.4; 13.3 / 380 = 3.5%), ask for a macro instead of typing it. Ask the Orchestrator for one if it is missing (round 1 #7–#9).
- **V1 — evidence words.** "מוכח / מובטח / מוכחת / היחיד / לראשונה" need a citation or must be removed. Pre-revenue plans have *expected* demand.
- **G1 — glossary.** ESG = סביבה, חברה וממשל תאגידי. Governance ≠ ממשלתי.
