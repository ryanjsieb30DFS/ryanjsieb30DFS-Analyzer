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

The venv is at `.venv/`. Python 3.9 (system Python). Streamlit, pandas, plotly, pyyaml.

## Architecture

| Path | Purpose |
|---|---|
| `app.py` | Streamlit UI: 5 tabs (Projections, Landscape, Projections Diff, Articles, Autopsy) |
| `src/projections.py` | CSV loader with vendor auto-detection + canonical schema normalization |
| `src/vendors.py` | Vendor column signatures (ETR, Ship It Nation, DailyFan PGA/MMA/NASCAR, DK PGA RD4 SD) |
| `src/sessions.py` | Per-sport JSON persistence at `data/sessions/<slug>.json` |
| `src/landscape.py` | Chalk tiers, leverage table, anchor-equivalence check |
| `src/projections_diff.py` | Cross-vendor disagreement detector |
| `src/autopsy.py` | DK contest-standings parser |
| `src/diagnostics.py` | Player-tier helpers used by landscape |
| `rules/<slug>/` | Philosophy / framework / autopsies docs per contest type — Claude reads these as context |
| `articles/<slug>/` | Per-contest-type research uploads (PDFs, notes) |
| `templates/` | Canonical projection CSV templates per sport |
| `data/sessions/` | Per-sport session JSON (gitignored) |

## Contest types

| Sidebar selector | `slug` | Sport | Notes |
|---|---|---|---|
| PGA Classic | `pga_classic` | golf | 6 golfers, 2 days + cut |
| PGA RD4 Showdown | `pga_rd4_sd` | golf | 6 golfers, **flat — NO captain, NO 1.5x** |
| MMA | `mma_se` | mma | SE rules |
| NASCAR | `nascar` | nascar | 6 drivers; **always check `rules/nascar/tracks/<slug>.md`** |

## Vendor auto-detection

Drop any of the user's vendor exports into the Projections tab — the loader detects:
- **ETR PGA** (`NAME, SAL, PROJ, CEIL, OWN, PT/$`)
- **Ship It Nation PGA** (`Golfer, Round 1 Tee Time, DK Salary, ...`)
- **DailyFan NASCAR** (`Driver, Salary, Starting Position, ...`)
- **DailyFan MMA** (`Fighter, Matchup, Win %, Salary DK, ...`)
- **DK PGA RD4 SD** (`Golfer, Tee Time, Salary, Points, Ownership, ...`)

To add a new vendor: edit `VENDOR_SIGNATURES` in `src/vendors.py`.

## Workflow per slate

1. **Projections** — upload one or more vendor CSVs (auto-detected), inspect rows
2. **Landscape** — read the slate-level structural story (chalk tiers, leverage, anchor-equivalence pre-lock check)
3. **Projections Diff** — when 2+ vendors uploaded, see where they materially disagree
4. **Articles** — upload PDFs/notes for the slate
5. *(After contest ends)* **Autopsy** — upload DK contest-standings CSV, view field summary, log lessons to `rules/<slug>/autopsies.md`

## Writing the slate analysis

When the user says **"review the articles and write the slate analysis"** (or "refresh the slate analysis", or similar):

1. Read projections for the active sport: `data/sessions/<slug>.json`
2. Read **contests** for the active sport: `data/contests/<slug>.json` — this drives total lineup count and per-contest entry caps (SE, 3-Max, 5-Max, 20-Max, 150-Max)
3. Read uploaded articles: `articles/<slug>/*.pdf` and `*.txt`/`*.md` (use the Read tool; PDFs may require poppler — note in the file if anything couldn't be parsed)
4. Read strategy: `rules/<slug>/{philosophy,framework,autopsies}.md` + `rules/shared/anchor_equivalence.md`
5. Read recent autopsies: tail of `rules/<slug>/autopsy_data.jsonl`
6. For NASCAR: also read `rules/nascar/tracks/<track>.md`
7. Synthesize:
   - Where do the articles + auto-data agree? Where do they disagree?
   - Which qualitative overrides should beat the quantitative signal (mirror the King Green pattern from `rules/mma_mme/autopsies.md`)?
   - What's the Anchor-Equivalence call?
   - What conviction-core duplication / ceiling-threshold / binary-leverage warnings apply (per SE framework)?
7. Write to `data/slate_analysis/<slug>.md` — concise, scannable, GPP-framed, with a player-by-player call where the auto-data and the articles diverge

The file is rendered at the top of the Slate Analysis tab with a "Last updated" timestamp. It's cleared automatically when the user logs an autopsy for the sport.

## Building lineups (hand-built, not optimized)

When the user says **"build lineups for the current slate"** (or "rebuild lineups", or similar):

1. Read **contests**: `data/contests/<slug>.json` — drives **total lineup count** (`portfolio_summary.unique_lineups_needed`) and **contest assignment per lineup** (which contests each lineup is entered into). Lineup quality comes from the projections + articles + framework reads, not from a configurable ceiling target.
2. Read the slate analysis: `data/slate_analysis/<slug>.md` (if missing, write it first via the workflow above)
3. Read projections: `data/sessions/<slug>.json`
4. Read recent autopsies for SE-specific discipline rules (`rules/<slug>/autopsies.md` + `autopsy_data.jsonl`)
5. Build N lineups (where N = `unique_lineups_needed` from contests; default 2 if no contests declared) — each with:
   - One-sentence **thesis** ("how it wins")
   - **Roster** as a markdown table (player, salary, win%, win-case proj, role)
   - **Total salary** verified ≤ $50,000 (do the math, show it)
   - **Opponent check** — verify no opponent-stacking
   - **"What if?"** line stating which scenario this lineup answers
5. Lineups in a portfolio MUST answer DIFFERENT "what if?" questions (`feedback_no_competing_lineups`)
6. For MMA SE specifically: never duplicate the same 3+ conviction-core players across multiple lineups (5/16/26 lesson)
7. Apply the Anchor-Equivalence rule explicitly: if chalk anchors at similar own, ≥1 lineup must run the alternative
8. Apply ceiling-threshold discipline: sum top-6 `proj_win` values, target ≥600 for SE
9. Write to `data/lineups/<slug>.md` with a final **Portfolio audit** section summarizing player overlap, fight hedges, and framework-rule compliance

The file is rendered in the Lineups tab. Cleared automatically when the user logs an autopsy.

## Hard rules

- **No scraping.** DK ToS prohibits it; never build scrapers. Use user-pasted/uploaded data only.
- **GPP-only framing.** Leverage / ceiling / contrarian. Never propose cash-game features.
- **Anchor-Equivalence Rule** is a **mandatory pre-lock check** on every slate — surfaced as a warning in the Landscape tab. 4-slate-validated structural leak: if 2+ chalk-tier anchors at similar own%, ≥1 lineup must run the alternative.
- **NASCAR**: before any NASCAR analysis, check `rules/nascar/tracks/<slug>.md`. If missing, proactively ask the user to fill it in.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x multiplier**. Never reference "CPT" for this contest type.
- **No stddev required.** Vendors don't ship it; loader auto-derives (`(ceiling − proj) / 1.28` or 30% of proj).
- **No NFL/NBA/MLB.** Out of scope.
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.

## Useful file paths

- **Sample vendor CSVs**: `~/Downloads/PGA Projections DK.csv` (ETR), `~/Downloads/DK PGA DFS Projections (6).csv` (Ship It Nation), `~/Downloads/DailyFan-Projections-Sheet-MMA-DK-38.csv`, `~/Downloads/DailyFan-Projections-Sheet-NASCAR-DK-12 (1).csv`, `~/Downloads/DK PGA Round 4 Showdown Projections (5).csv`
- **Sample DK contest-standings**: `~/Downloads/contest-standings-190402324.csv`
- **GitHub**: https://github.com/ryanjsieb30DFS/ryanjsieb30DFS-Analyzer (`main` branch)
