# DFS Slate Analyzer

Streamlit web app for multi-sport DFS slate analysis on DraftKings (PGA Classic, PGA RD4 Showdown, MMA, NASCAR).

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py --server.port 8601
```

Open http://localhost:8601.

## Workflow

1. **Projections** — drag-drop vendor CSV(s). Vendor is auto-detected (ETR, Ship It Nation, DailyFan, DK).
2. **Landscape** — chalk tiers, leverage table, anchor-equivalence pre-lock check.
3. **Projections Diff** — when 2+ vendors are uploaded, see where they disagree.
4. **Articles** — upload PDFs / notes for the slate.
5. **Autopsy** — after the contest, upload DK contest-standings CSV, log lessons.

See `CLAUDE.md` for architecture and conventions.
