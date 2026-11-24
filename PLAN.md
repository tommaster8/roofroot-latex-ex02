# PLAN — תוכנית עבודה

## ארכיטקטורת הצוות

```
                   ┌──────────────────────────┐
                   │  Human Lead (ראש הצוות)  │  חזון, אישור PRD, חקר אירועים
                   └────────────┬─────────────┘
                                │
                   ┌────────────▼─────────────┐
                   │  Orchestrator (Opus)     │  CLS, build, נתונים, אינטגרציה
                   └──┬─────────┬─────────┬───┘
         ┌────────────┘         │         └─────────────┐
┌────────▼────────┐  ┌──────────▼───────┐  ┌────────────▼────────┐
│ writer-strategy │  │ writer-market    │  │ writer-finance      │   (Sonnet, במקביל)
│ פרקים 1–3       │  │ פרקים 4–6        │  │ פרקים 7–10 + נספח   │
└────────┬────────┘  └──────────┬───────┘  └────────────┬────────┘
         └──────────────┬───────┴───────────────────────┘
               ┌────────▼────────┐        ┌──────────────────┐
               │ qa-detector     │──────▶ │ qa-fixer         │
               │ (צוות אדום)     │ דוח    │ CLS / Skill בלבד │
               └────────▲────────┘        └────────┬─────────┘
                        └──────── סבב חוזר ─────────┘
                                 │ PASS
                       ┌─────────▼─────────┐
                       │ investor-critic   │  משקיע Seed ספקן: שכנוע ולוגיקה עסקית
                       │ (Sonnet)          │──▶ שאלות פתוחות חוזרות לכותבים / לנתונים
                       └───────────────────┘
```

## שלבים

| # | שלב | תוצר | אחראי | מודל |
|---|---|---|---|---|
| 0 | ועדת מומחים | `PRD.md` | Orchestrator בחמישה "כובעים" | Opus |
| 1 | שלד מינימלי שמתקמפל | `main.tex`, `roofroot.cls`, `build.sh` | Orchestrator | Opus |
| 2 | מקור אמת לנתונים | `data/*.csv`, `figures/python/*.py` | Orchestrator | Opus |
| 3 | איורי TikZ | `figures/tikz/*.tex` | Orchestrator | Opus |
| 4 | Skills ו-Agents | `.claude/skills/*`, `.claude/agents/*` | Orchestrator | Opus |
| 5 | כתיבת פרקים במקביל | `chapters/*.tex` | 3 writers | Sonnet |
| 6 | אינטגרציה וקומפילציה | `main.pdf` | Orchestrator | Opus |
| 7 | צוות אדום, סבב 1 | `qa-reports/round-1.md` | qa-detector | Sonnet |
| 8 | תיקון | עדכוני CLS ו-Skill | qa-fixer / Orchestrator | Opus |
| 9 | צוות אדום, סבב 2 (אימות) | `qa-reports/round-2.md` | qa-detector | Sonnet |
| 9.5 | ביקורת משקיע | `qa-reports/investor-N.md` | investor-critic | Sonnet |
| 10 | README, צילומי מסך, GitHub | `README.md`, `docs/screenshots` | Orchestrator | Opus |

## ניהול משאבים
- **Opus**: החלטות ארכיטקטורה ו-CLS (מעט טוקנים, דיוק גבוה).
- **Sonnet**: כתיבה ובקרה (הרבה טקסט, עלות נמוכה יותר).
- הכותבים מקבלים **מדריך סגנון אחד** (`prompts/03-writer-brief.md`) ולא את כל ההיסטוריה, כדי לחסוך בהקשר.
- לכל היותר 3 סוכנים רצים במקביל (זיכרון ודיסק).
