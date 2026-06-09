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
2. **Slate Data** — upload articles / notes / photos (e.g. DailyFan screenshots) for the slate.
3. **Sim Data** — *(optional)* upload a sim export CSV (e.g. SaberSim); stored as-is for Claude to read.
4. **Analyze** — set your contests, review the auto-snapshot (chalk tiers, leverage, anchor-equivalence, sport signals, vendor disagreement), then **Bundle for Claude** and ask Claude to write the slate analysis. The written analysis renders at the bottom of this tab.
5. **Autopsy** — after the contest, upload DK contest-standings CSV, log lessons to `rules/<slug>/autopsies.md`.

See `CLAUDE.md` for architecture and conventions.
