# Slate bundle — MMA
_Generated 2026-07-18 13:14 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 2 total entries
  - **UFC $8K Flying Knee ($2K to 1st)** (SE): field 784, my entries 1/1, prize multiple 0.85x
  - **UFC $5K Clinch** (SE): field 1,189, my entries 1/1, payout **Flat**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **SE** (across your 2 past SE contests): the field reliably crowds **Paddy Pimblett (in 2 of 2), Benoit Saint Denis (in 2 of 2), Damian Pinas (in 2 of 2), King Green (in 2 of 2), Terrance McKinney (in 2 of 2), Ryan Gandra (in 2 of 2), Max Holloway (in 2 of 2), Gable Steveson (in 2 of 2)**; recurring fish-traps: **Zach Reese (in 2 of 2), Benoit Saint Denis (in 2 of 2), Conor McGregor (in 2 of 2), Terrance McKinney (in 2 of 2), Cory Sandhagen (in 2 of 2), Nikita Krylov (in 2 of 2), Kai Kamaka III (in 2 of 2)**; the field PAIRS **Max Holloway + Terrance McKinney (in 2 of 2), Max Holloway + Paddy Pimblett (in 2 of 2), King Green + Max Holloway (in 2 of 2)** — a dupe-magnet stack; leverage lives in breaking it.

## Process trend — your last 4 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 0.2 → 1.7 → 1.3 → 26.1
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 100% → 60% → 0%
- **Bust exposure** (top underperformers we rostered): 100% → 100% → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 2 of the last 4 slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-18__DailyFan MMA Matchups 7.18.2026.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-18__DailyFan MMA Top Plays 7.18.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-53.csv` (24 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Dricus Du Plessis | 9000 | 45.0 | 78.45 | 0.6465000000000001 | Kamaru Usman |
| Kamaru Usman | 7200 | 37.0 | 60.25 | 0.35350000000000004 | Dricus Du Plessis |
| Christian Leroy Duncan | 9100 | 28.0 | 74.85 | 0.7619 | Jared Cannonier |
| Jared Cannonier | 7100 | 15.0 | 38.0 | 0.23809999999999998 | Christian Leroy Duncan |
| Chase Hooper | 9200 | 35.0 | 79.22 | 0.7612000000000001 | Mitch Ramirez |
| Mitch Ramirez | 7000 | 15.0 | 36.65 | 0.23879999999999998 | Chase Hooper |
| Fatima Kline | 9300 | 21.0 | 79.83 | 0.7983 | Tabatha Ricci |
| Tabatha Ricci | 6900 | 13.0 | 37.35 | 0.20170000000000002 | Fatima Kline |
| Tommy McMillen | 8200 | 42.0 | 68.705 | 0.6067 | Alberto Montes |
| Alberto Montes | 8000 | 24.0 | 50.77 | 0.3933 | Tommy McMillen |
| Jose Delgado | 8300 | 21.0 | 53.19 | 0.4474 | Austin Bashi |
| Austin Bashi | 7900 | 36.0 | 60.89 | 0.5526 | Jose Delgado |
| Seokhyeon Ko | 8800 | 30.0 | 68.68 | 0.6067 | Jean-Paul Lebosnoyani |
| Jean-Paul Lebosnoyani | 7400 | 25.0 | 44.7 | 0.3933 | Seokhyeon Ko |
| Levi Rodrigues Jr. | 8600 | 26.0 | 60.6 | 0.5657 | Felipe Franco |
| Felipe Franco | 7600 | 24.0 | 46.39 | 0.4343 | Levi Rodrigues Jr. |
| Alden Coria | 9800 | 22.0 | 88.99 | 0.8832 | Stewart Nicoll |
| Stewart Nicoll | 6400 | 5.0 | 30.05 | 0.1168 | Alden Coria |
| Alvin Hines | 8400 | 24.0 | 59.25 | 0.5108 | RJ Harris |
| RJ Harris | 7800 | 26.0 | 50.1 | 0.4892 | Alvin Hines |
| Dione Barbosa | 9400 | 24.0 | 85.04 | 0.8258 | Anna Melisano |
| Anna Melisano | 6800 | 8.0 | 26.76 | 0.17420000000000002 | Dione Barbosa |
| Damien Anderson | 8500 | 25.0 | 63.4 | 0.5304 | Ezra Elliott |
| Ezra Elliott | 7700 | 29.0 | 56.1 | 0.4696 | Damien Anderson |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Stewart Nicoll — $6,400, 5% own, proj 30.1, ceiling 96.9
- Anna Melisano — $6,800, 8% own, proj 26.8, ceiling 85.8

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Dricus Du Plessis + Tommy McMillen** — 45.0% × 42.0% ≈ 18.9% of the field (~225 lineups of 1,189)
- **Dricus Du Plessis + Kamaru Usman** — 45.0% × 37.0% ≈ 16.7% of the field (~199 lineups of 1,189)
- **Dricus Du Plessis + Austin Bashi** — 45.0% × 36.0% ≈ 16.2% of the field (~193 lineups of 1,189)
- **Dricus Du Plessis + Chase Hooper** — 45.0% × 35.0% ≈ 15.8% of the field (~188 lineups of 1,189)
- **Tommy McMillen + Kamaru Usman** — 42.0% × 37.0% ≈ 15.5% of the field (~184 lineups of 1,189)
- **Tommy McMillen + Austin Bashi** — 42.0% × 36.0% ≈ 15.1% of the field (~180 lineups of 1,189)

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/results.jsonl` — cross-slate results ledger (process notes only)

**Output target:** write the slate strategy to `data/slate_analysis/mma_se.md`.
