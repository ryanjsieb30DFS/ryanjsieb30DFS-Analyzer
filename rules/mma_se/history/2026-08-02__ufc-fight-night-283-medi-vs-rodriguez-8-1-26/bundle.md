# Slate bundle — MMA
_Generated 2026-07-31 20:48 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 4 total entries
  - **UFC $6K Flying Knee** (SE): field 588, my entries 1/1, payout **Top-heavy**, prize multiple 0.00x
  - **UFC $2K Sprawl** (3-Max): field 594, my entries 3/3, payout **Balanced**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **SE** (across your 6 past SE contests): the field reliably crowds **Damian Pinas (in 2 of 6), Max Holloway (in 2 of 6), Gable Steveson (in 2 of 6), Terrance McKinney (in 2 of 6), Ryan Gandra (in 2 of 6), Paddy Pimblett (in 2 of 6), King Green (in 2 of 6), Benoit Saint Denis (in 2 of 6)**; recurring fish-traps: **Conor McGregor (in 2 of 6), Cory Sandhagen (in 2 of 6), Terrance McKinney (in 2 of 6), Kai Kamaka III (in 2 of 6), Zach Reese (in 2 of 6), Nikita Krylov (in 2 of 6), Benoit Saint Denis (in 2 of 6), Damien Anderson (in 2 of 6)**; the field PAIRS **Max Holloway + Paddy Pimblett (in 2 of 6), King Green + Max Holloway (in 2 of 6), Max Holloway + Terrance McKinney (in 2 of 6), Dricus Du Plessis + Tommy McMillen (in 2 of 6), Austin Bashi + Tommy McMillen (in 2 of 6)** — a dupe-magnet stack; leverage lives in breaking it; from the full-field captures (2 contests): only **79.3% of entries were unique rosters**, the most-copied lineup appeared **11 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **9.1%** of lineups, **2.5%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 5 | 2/5 | 30.4 | 24.0 | 0.59 | ~30.4% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 1.7 → 1.3 → 26.1 → 2.3 → 3.5
- **Leverage capture** (slate-defining low-owned plays we rostered): 100% → 60% → 0% → — → —
- **Bust exposure** (top underperformers we rostered): 100% → — → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 1 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-31__MMA Matchups 8.1.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-31__MMA Top Plays 8.1.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-58.csv` (28 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Uros Medic | 9400 | 42.0 | 84.5 | 0.759 | Daniel Rodriguez |
| Daniel Rodriguez | 6800 | 21.0 | 30.38 | 0.24100000000000002 | Uros Medic |
| Navajo Stirling | 9000 | 23.0 | 71.82 | 0.7402 | Jan Blachowicz |
| Jan Blachowicz | 7200 | 17.0 | 40.96 | 0.25980000000000003 | Navajo Stirling |
| Aleksandar Rakic | 9300 | 13.0 | 72.89 | 0.7526999999999999 | Marcin Tybura |
| Marcin Tybura | 6900 | 14.0 | 34.04 | 0.2473 | Aleksandar Rakic |
| Robert Valentin | 8500 | 25.0 | 64.44 | 0.5798 | Dusko Todorovic |
| Dusko Todorovic | 7700 | 28.0 | 50.07 | 0.4202 | Robert Valentin |
| Vlasto Cepo | 9100 | 36.0 | 78.93 | 0.7526999999999999 | Gilbert Urbina |
| Gilbert Urbina | 7100 | 15.0 | 31.42 | 0.2473 | Vlasto Cepo |
| Milos Janicic | 8200 | 26.0 | 55.58 | 0.4783 | Noah Gugnon |
| Noah Gugnon | 8000 | 34.0 | 58.27 | 0.5217 | Milos Janicic |
| Ludovit Klein | 8800 | 21.0 | 69.26 | 0.7051000000000001 | Tofiq Musayev |
| Tofiq Musayev | 7400 | 18.0 | 42.79 | 0.2949 | Ludovit Klein |
| Michael Oliveira | 9200 | 30.0 | 78.35 | 0.7526999999999999 | Oban Elliott |
| Oban Elliott | 7000 | 14.0 | 33.17 | 0.2473 | Michael Oliveira |
| Borislav Nikolic | 8400 | 27.0 | 67.91 | 0.6548 | Mark Vologdin |
| Mark Vologdin | 7800 | 20.0 | 52.53 | 0.3452 | Borislav Nikolic |
| Bogdan Grad | 8600 | 23.0 | 69.01 | 0.6345000000000001 | Dennis Buzukja |
| Dennis Buzukja | 7600 | 18.0 | 45.1 | 0.3655 | Bogdan Grad |
| Mateusz Rebecki | 9600 | 30.0 | 87.16 | 0.8411 | Kyle Prepolec |
| Kyle Prepolec | 6600 | 7.0 | 28.67 | 0.1589 | Mateusz Rebecki |
| Nina Milosevic | 9500 | 16.0 | 80.44 | 0.7983 | Hailey Cowan |
| Hailey Cowan | 6700 | 10.0 | 36.71 | 0.20170000000000002 | Nina Milosevic |
| Jovan Leka | 8700 | 28.0 | 68.99 | 0.6984 | Alexander Poppeck |
| Alexander Poppeck | 7500 | 17.0 | 40.76 | 0.3016 | Jovan Leka |
| Stephanie Luciano | 8900 | 13.0 | 71.93 | 0.738 | Marina Spasic |
| Marina Spasic | 7300 | 14.0 | 38.52 | 0.262 | Stephanie Luciano |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Kyle Prepolec — $6,600, 7% own, proj 28.7, ceiling 89.6

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Uros Medic + Vlasto Cepo** — 42.0% × 36.0% ≈ 15.1% of the field (~90 lineups of 594)
- **Uros Medic + Noah Gugnon** — 42.0% × 34.0% ≈ 14.3% of the field (~85 lineups of 594)
- **Uros Medic + Michael Oliveira** — 42.0% × 30.0% ≈ 12.6% of the field (~75 lineups of 594)
- **Uros Medic + Mateusz Rebecki** — 42.0% × 30.0% ≈ 12.6% of the field (~75 lineups of 594)
- **Vlasto Cepo + Noah Gugnon** — 36.0% × 34.0% ≈ 12.2% of the field (~72 lineups of 594)
- **Uros Medic + Dusko Todorovic** — 42.0% × 28.0% ≈ 11.8% of the field (~70 lineups of 594)

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
