# DFS Slate Analyzer

Article-driven, multi-sport DFS slate-strategy tool for DraftKings (PGA Classic, PGA RD4 Showdown, MMA, NASCAR, MLB Classic). Upload the slate's articles → Claude writes the slate strategy (top plays, how to approach the slate, themes, leverage & fades, decisions). No projections, no lineup building — construction lives in the sim tool.

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py --server.port 8601
```

Open http://localhost:8601.

## Workflow (3 tabs)

1. **Slate Data** — upload the slate's articles / notes / data files / photos / screenshots (e.g. DailyFan). These are the only input Claude reads.
2. **Slate Strategy** — declare your contests, then **Generate slate strategy**. Claude reads your uploaded articles + strategy docs and writes the strategy (pre-flight checklist, slate at a glance, top plays, how to approach the slate, key themes, leverage & fades, decisions). It renders at the bottom of this tab.
3. **Autopsy** — after the contest, upload DK contest-standings CSV(s); the autopsy grades your entries vs the winners and the sharks (no projections), logs lessons to `rules/<slug>/autopsies.md`, archives the slate, and runs the post-autopsy learning review.

See `CLAUDE.md` for architecture and conventions.
