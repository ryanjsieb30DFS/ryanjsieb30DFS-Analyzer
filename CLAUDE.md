# CLAUDE.md — DFS Slate Analyzer

Multi-sport DFS slate **analyzer** for DraftKings. Streamlit web app. Personal-use, single user (`ryanjsieb30`). Sister tool to the sim at `~/Desktop/Repo/ryanjsieb30DFS`.

## What this is

The **Analyzer reads the slate**. The sim builds lineups. They're complementary:
- **Sim** = PuLP/Monte Carlo lineup construction + contest ROI
- **Analyzer** = pre-slate landscape, vendor disagreement, post-slate review

For **PGA Classic, PGA RD4 Showdown, MMA, NASCAR**. The user uploads vendor projections, the Analyzer surfaces the structural read (chalk tiers, leverage, anchor-equivalence, vendor disagreements), and after the slate the user uploads DK results for a post-mortem.

No lineup optimizer here. No Monte Carlo. If you want lineups → switch to the sim.

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
.venv/bin/streamlit run app.py        # app on http://localhost:8501
```

The venv is at `.venv/`. Python 3.9 (system Python). Streamlit, pandas, plotly, pyyaml.

## Architecture

| Path | Purpose |
|---|---|
| `app.py` | Streamlit UI: 5 tabs (Projections, Landscape, Projections Diff, Articles, Autopsy) |
| `src/projections.py` | CSV loader with vendor auto-detection + canonical schema normalization (copied from sim) |
| `src/vendors.py` | Vendor column signatures (ETR, Ship It Nation, DailyFan PGA/MMA/NASCAR, DK PGA RD4 SD) (copied from sim) |
| `src/sessions.py` | Per-sport JSON persistence at `data/sessions/<slug>.json` |
| `src/landscape.py` | Chalk tiers, leverage table, anchor-equivalence check |
| `src/projections_diff.py` | Cross-vendor disagreement detector |
| `src/autopsy.py` | DK contest-standings parser (copied from sim; only `parse_dk_results` is used) |
| `src/diagnostics.py` | Sim's pre-slate diagnostics (carried over for reuse; not all functions wired) |
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

## Hard rules (mirrors user memory + sim conventions)

- **No scraping.** DK ToS prohibits it; never build scrapers. Use user-pasted/uploaded data only.
- **GPP-only framing.** Leverage / ceiling / contrarian. Never propose cash-game features.
- **Anchor-Equivalence Rule** is a **mandatory pre-lock check** on every slate — surfaced as a warning in the Landscape tab. 4-slate-validated structural leak: if 2+ chalk-tier anchors at similar own%, ≥1 lineup must run the alternative.
- **NASCAR**: before any NASCAR analysis, check `rules/nascar/tracks/<slug>.md`. If missing, proactively ask the user to fill it in.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x multiplier**. Never reference "CPT" for this contest type.
- **No stddev required.** Vendors don't ship it; loader auto-derives (`(ceiling − proj) / 1.28` or 30% of proj).
- **No NFL/NBA/MLB.** Out of scope.
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.

## Sim sync policy

When sim's `src/vendors.py` changes, manually re-copy here. When philosophy/framework/autopsies are updated in either repo, mirror to the other (sim is canonical for now). On every post-slate autopsy here, mirror the lesson to the sim's `rules/<slug>/autopsies.md` too.

## Useful file paths

- **Sample vendor CSVs**: `~/Downloads/PGA Projections DK.csv` (ETR), `~/Downloads/DK PGA DFS Projections (6).csv` (Ship It Nation), `~/Downloads/DailyFan-Projections-Sheet-MMA-DK-38.csv`, `~/Downloads/DailyFan-Projections-Sheet-NASCAR-DK-12 (1).csv`, `~/Downloads/DK PGA Round 4 Showdown Projections (5).csv`
- **Sample DK contest-standings**: `~/Downloads/contest-standings-190402324.csv`
- **GitHub**: https://github.com/ryanjsieb30DFS/ryanjsieb30DFS-Analyzer (`main` branch)
- **Sister sim repo**: `~/Desktop/Repo/ryanjsieb30DFS`
