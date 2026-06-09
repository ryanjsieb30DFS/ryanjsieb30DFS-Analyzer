# CLAUDE.md — DFS Slate Analyzer

Multi-sport DFS slate analyzer for DraftKings. Streamlit web app. Personal-use, single user (`ryanjsieb30`).

## What this is

A pre-slate / post-slate analysis tool for **PGA Classic, PGA RD4 Showdown, MMA, NASCAR**. The user uploads vendor projections; the Analyzer surfaces the structural read of the slate (chalk tiers, leverage candidates, anchor-equivalence pre-lock check, cross-vendor disagreements). After the contest, the user uploads DK contest-standings and the Analyzer drives a post-mortem.

This tool does not build lineups, run Monte Carlo, or simulate contests. It surfaces the **read**; lineup construction is left to the user.

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
.venv/bin/streamlit run app.py --server.port 8601    # http://localhost:8601
```

The venv is at `.venv/`. Python 3.9 (system Python). Streamlit, pandas.

## Architecture

| Path | Purpose |
|---|---|
| `app.py` | Streamlit UI: 5 tabs (Projections, Slate Data, Sim Data, Analyze, Autopsy) |
| `src/projections.py` | CSV loader with vendor auto-detection + canonical schema normalization |
| `src/vendors.py` | Vendor column signatures (ETR, Ship It Nation, DailyFan PGA/MMA/NASCAR, DK PGA RD4 SD) |
| `src/sessions.py` | Per-sport JSON persistence at `data/sessions/<slug>.json` |
| `src/landscape.py` | Chalk tiers, leverage table, anchor-equivalence check |
| `src/slate_analysis.py` | Auto-snapshot computations (`snapshot`, `top_chalk`, `sport_signals`) + persisted-analysis read/write at `data/slate_analysis/<slug>.md` |
| `src/projections_diff.py` | Cross-vendor disagreement detector |
| `src/contests.py` | Per-sport contest registry at `data/contests/<slug>.json` |
| `src/sim_data.py` | Generic sim-data store: saves the raw upload + a light summary at `data/sim_data/` |
| `src/bundle.py` | `build_bundle` — consolidates all inputs into `data/bundle/<slug>.md` for Claude to read |
| `src/analysis_runner.py` | `run_analysis` + `run_build_lineups` — build the bundle, run `claude -p` headlessly (subscription auth), write `data/slate_analysis/<slug>.md` / `data/lineups/<slug>.md`. Power the Analyze tab's "Generate slate analysis" + "Build lineups" buttons |
| `src/lineups.py` | Read/clear the hand-built lineups at `data/lineups/<slug>.md` (Claude writes them via the headless run) |
| `src/strategy.py` | Loads per-sport philosophy/framework/autopsies + recent lessons (read by `bundle.py`; no UI tab) |
| `src/autopsy.py` | DK contest-standings parser |
| `rules/<slug>/` | Philosophy / framework / autopsies docs per contest type — Claude reads these as context (no UI tab; surfaced via the bundle) |
| `articles/<slug>/` | Per-contest-type "Slate Data" uploads — PDFs, notes, and photos/screenshots (e.g. DailyFan). Tab label is "Slate Data"; the on-disk dir stays `articles/`. |
| `templates/` | Canonical projection CSV templates per sport |
| `data/sessions/` | Per-sport session JSON (gitignored) |
| `data/sim_data/` | Per-slate sim upload: `<slug>__<filename>` (raw) + `<slug>_summary.json` (light summary for Claude). Optional. |
| `data/bundle/` | `<slug>.md` — the consolidated "Bundle for Claude" written from the Analyze tab. |

## Contest types

| Sidebar selector | `slug` | Sport | Notes |
|---|---|---|---|
| PGA Classic | `pga_classic` | golf | 6 golfers, 2 days + cut |
| PGA RD4 Showdown | `pga_rd4_sd` | golf | 6 golfers, **flat — NO captain, NO 1.5x** |
| MMA | `mma_se` | mma | SE rules |
| NASCAR | `nascar` | nascar | 6 drivers; **always check `rules/nascar/tracks/<slug>.md`** |
| MLB Classic | `mlb_classic` | mlb | 10 players (P, P, C, 1B, 2B, 3B, SS, OF×3), $50K; **team-stack driven** |

## Vendor auto-detection

Drop any of the user's vendor exports into the Projections tab — the loader detects:
- **ETR PGA** (`NAME, SAL, PROJ, CEIL, OWN, PT/$`)
- **Ship It Nation PGA** (`Golfer, Round 1 Tee Time, DK Salary, ...`)
- **DailyFan NASCAR** (`Driver, Salary, Starting Position, ...`)
- **DailyFan MMA** (`Fighter, Matchup, Win %, Salary DK, ...`)
- **DK PGA RD4 SD** (`Golfer, Tee Time, Salary, Points, Ownership, ...`)
- **Ship It Nation MLB** (`#, Name, Team, Opp, Pos, H, Salary, Proj, Own, Slate`) — hitters and pitchers ship as **two separate files** with identical headers; both detect as this vendor and are auto-combined into one pool for analysis
- **Ship It Nation MLB Stacks** (`#, Team, Proj, Own %, Stack Salary, Slate`) — team-level stack rankings; stored as session team-data (not a player source) and merged into the MLB team-stack signals as `vendor_stack_*` columns

To add a new vendor: edit `VENDOR_SIGNATURES` in `src/vendors.py`.

## Workflow per slate

1. **Projections** — upload one or more vendor CSVs (auto-detected), inspect rows
2. **Slate Data** — upload PDFs/notes/photos (e.g. DailyFan screenshots) for the slate
3. **Sim Data** *(optional)* — upload a sim export CSV (e.g. SaberSim); stored as-is for Claude
4. **Analyze** — declare contests, review the auto-snapshot (chalk tiers, leverage, anchor-equivalence, sport signals, vendor disagreement), then click **Generate slate analysis** — the app builds the bundle and runs `claude -p` headlessly to write + render the analysis (no chat needed)
5. *(After contest ends)* **Autopsy** — upload DK contest-standings CSV, view field summary, log lessons to `rules/<slug>/autopsies.md`

## Writing the slate analysis

This normally runs **in-app**: the Analyze tab's **Generate slate analysis** button calls `src/analysis_runner.py::run_analysis`, which builds the bundle and invokes `claude -p` headlessly (subscription auth, no API key) with the prompt to read the bundle + referenced files and write `data/slate_analysis/<slug>.md`. That headless Claude loads this `CLAUDE.md` and follows the steps below. The same can be triggered manually from a chat (fallback): click the button once to build the bundle, then ask **"read the bundle and write the slate analysis"**. Either way the steps are:

1. Read the bundle: `data/bundle/<slug>.md` — it consolidates the contest config, projections read (chalk/leverage/anchor/sport-signals), cross-vendor disagreement, and absolute paths to everything else below. Start here.
2. Read the slate-data files it lists under `articles/<slug>/` — `*.pdf`, `*.txt`/`*.md`, and `*.png`/`*.jpg`/`*.jpeg` (use the Read tool — it reads images visually, so DailyFan screenshots work; PDFs may require poppler — note in the file if anything couldn't be parsed)
3. Read strategy: `rules/<slug>/{philosophy,framework,autopsies}.md` + `rules/shared/anchor_equivalence.md` (paths are in the bundle)
4. Read recent autopsies: tail of `rules/<slug>/autopsy_data.jsonl`
5. If sim data exists, read the raw file at the path in the bundle's "Sim data" section — see where the sims agree/disagree with the articles' read (e.g., a low-owned play the sims love, or chalk they fade)
6. For NASCAR: also read `rules/nascar/tracks/<track>.md`
7. Synthesize:
   - Where do the articles + auto-snapshot agree? Where do they disagree?
   - Which qualitative overrides should beat the quantitative signal?
   - What's the Anchor-Equivalence call?
   - What conviction-core duplication / ceiling-threshold / binary-leverage warnings apply (per the sport's framework)?
8. Write to `data/slate_analysis/<slug>.md` — concise, scannable, GPP-framed, with a player-by-player call where the auto-snapshot and the articles diverge. It renders in the Analyze tab with a "Last updated" timestamp and is cleared automatically when the user logs an autopsy.

## Building lineups

Normally triggered **in-app**: the Analyze tab's **Build lineups** button calls `src/analysis_runner.py::run_build_lineups`, which runs `claude -p` headlessly to build the portfolio from the slate analysis and write `data/lineups/<slug>.md` (rendered back in the tab). It requires a slate analysis to exist first. The count is `portfolio_summary.unique_lineups_needed` (default 2; entry caps SE / 3-Max / 5-Max / 20-Max / 150-Max), but **build fewer if the slate supports fewer distinct theses — never pad with filler**. Each lineup needs: a one-sentence thesis ("how it wins"), a roster table with total salary verified ≤ $50,000, and a distinct "what if?" question (lineups in a portfolio must answer DIFFERENT questions — `feedback_no_competing_lineups`). Apply the Anchor-Equivalence rule explicitly, and for MMA SE differ on at least one conviction anchor across lineups (never duplicate the same full core). Read `rules/<slug>/{framework,autopsies}.md` for the sport's construction rules (e.g. RD4 SD is a flat 6-golfer lineup, no captain; **MLB Classic is a 10-man, team-stack-driven roster — P,P,C,1B,2B,3B,SS,OF×3 — never roster a hitter against your own pitcher**). End with a Portfolio audit section.

## Hard rules

- **No scraping.** DK ToS prohibits it; never build scrapers. Use user-pasted/uploaded data only.
- **GPP-only framing.** Leverage / ceiling / contrarian. Never propose cash-game features.
- **Anchor-Equivalence Rule** is a **mandatory pre-lock check** on every slate — surfaced as a warning in the Analyze tab. 4-slate-validated structural leak: if 2+ chalk-tier anchors at similar own%, ≥1 lineup must run the alternative.
- **NASCAR**: before any NASCAR analysis, check `rules/nascar/tracks/<slug>.md`. If missing, proactively ask the user to fill it in.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x multiplier**. Never reference "CPT" for this contest type.
- **No stddev required.** Vendors don't ship it; loader auto-derives (`(ceiling − proj) / 1.28` or 30% of proj).
- **No NFL/NBA.** Out of scope. (MLB Classic is supported as of 2026-06.)
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.

## Useful file paths

- **Sample vendor CSVs**: `~/Downloads/PGA Projections DK.csv` (ETR), `~/Downloads/DK PGA DFS Projections (6).csv` (Ship It Nation), `~/Downloads/DailyFan-Projections-Sheet-MMA-DK-38.csv`, `~/Downloads/DailyFan-Projections-Sheet-NASCAR-DK-12 (1).csv`, `~/Downloads/DK PGA Round 4 Showdown Projections (5).csv`, `~/Downloads/DK-hitter-rankings-DK-MAIN.csv` + `~/Downloads/DK-pitcher-rankings-DK-MAIN.csv` + `~/Downloads/DK-stack-rankings-DK-MAIN.csv` (Ship It Nation MLB, 3-file set)
- **Sample DK contest-standings**: `~/Downloads/contest-standings-190402324.csv`
- **GitHub**: https://github.com/ryanjsieb30DFS/ryanjsieb30DFS-Analyzer (`main` branch)
