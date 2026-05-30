# DFS Slate Analyzer

Streamlit web app for DFS slate analysis. Sister to the sim at `~/Desktop/Repo/ryanjsieb30DFS`.

The sim builds lineups. This tool reads the slate (chalk tiers, leverage, vendor disagreement, post-slate autopsy).

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Open http://localhost:8501.

## Workflow

1. **Projections** — drag-drop vendor CSV(s). Vendor is auto-detected (ETR, Ship It Nation, DailyFan, DK).
2. **Landscape** — chalk tiers, leverage table, anchor-equivalence pre-lock check.
3. **Projections Diff** — when 2+ vendors are uploaded, see where they disagree.
4. **Articles** — upload PDFs / notes for the slate.
5. **Autopsy** — after the contest, upload DK contest-standings CSV, log lessons.

See `CLAUDE.md` for architecture and conventions.
