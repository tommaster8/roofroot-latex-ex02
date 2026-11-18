---
name: qa-img
description: Checks figures in the RoofRoot document — placement, captions, sizing, source (no copyrighted images), legibility. Use for any figure, TikZ drawing or matplotlib chart.
---
# qa-img — figures

- **Source rule:** only TikZ (`figures/tikz/*.tex`) or Python (`figures/generated/fig_*.pdf`). No downloaded images, ever.
- Every figure: `[htbp]`, `\centering`, width relative to `\linewidth` (≤ 1.0), `\caption{}` in Hebrew, `\label{fig:...}`, referenced in text **before** it appears ("ראו איור~\ref{fig:x}").
- Charts are vector PDF; fonts ≥ 7pt after scaling (a 6.4in chart scaled to `\linewidth` ≈ 0.95 is fine).
- TikZ inside RTL: class loads babel `layout=graphics`; if a TikZ picture looks mirrored, fix in cls, not by negating coordinates in one file.
- No figure may float past its chapter (use `\FloatBarrier` via cls if needed).
- Text inside TikZ nodes must not overflow its shape (inspect the render).
