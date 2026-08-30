# DFS Slate Analyzer

Article-driven, multi-sport DFS slate-strategy tool for DraftKings (PGA Classic, PGA RD4 Showdown, MMA, NASCAR). Upload the slate's articles + vendor projections → Claude writes the slate strategy (top plays, how to approach the slate, themes, leverage & fades, decisions) and a tiered player board. No lineup building — construction lives in the sibling Sim tool.

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py --server.port 8601
```

Open http://localhost:8601.

## Workflow (5 tabs)

1. **Projections** — upload vendor projection CSVs (or pull the Sim's uploads), with a breakdown of edges, leverage, chalk tiers, and cross-vendor disagreement.
2. **Slate Data** — upload the slate's articles / notes / data files / photos / screenshots (e.g. DailyFan). These are the only input the strategy reads.
3. **Slate Strategy** — declare your contests, then **Generate slate strategy**. Claude reads your uploaded articles + strategy docs and writes the strategy (short version, slate at a glance, edges & tensions, field vs sharp, top plays, leverage, fades, build steps — the pre-flight prep runs silently and is never printed) plus the tiered player board. It renders at the bottom of this tab.
4. **✅ Grade** — pull the Sim's pool and entries, get a per-contest Claude pick beside the Sim diversifier's set, and grade both against this slate's own strategy calls (the strategy is a guide — rule breaks are priced and argued, not banned).
5. **Autopsy** — after the contest, upload DK contest-standings CSV(s); the autopsy grades your entries vs the winners and the sharks (no projections), logs lessons to `rules/<slug>/autopsies.md`, archives the slate, and runs the post-autopsy learning review.

See `CLAUDE.md` for architecture and conventions.
