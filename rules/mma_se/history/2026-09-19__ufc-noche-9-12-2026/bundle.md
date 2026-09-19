# Slate bundle — MMA
_Generated 2026-09-12 13:12 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 3 contest(s), 5 total entries
  - **UFC $2K Sprawl [3 Entry Max]** (3-Max): field 594, my entries 3/3, prize multiple 0.84x
  - **UFC $5K Clinch [Single Entry]** (SE): field 1,189, my entries 1/1, prize multiple 0.84x
  - **UFC $8K Flying Knee ($2K to 1st)** (SE): field 784, my entries 1/1, prize multiple 0.85x
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **3-Max** (across your 4 past comparable 3-Max contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 36.2% ownership (range 31.1-55.2%); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 19 of 22 were 25%+ owned (traps here are usually popular players who fail, not long shots); 21 of 32 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (17 of 32); from the full-field captures (3 contests): only **76.4% of entries were unique rosters**, the most-copied lineup appeared **9 times**, the average opponent entered **2.2 lineups**, **36.6% of opponents were single-entry**, the top-3 chalk players landed together in **10.9%** of lineups, **2.6%** of entries carried a structurally dead build.
- **SE** (across your 10 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 37.6% ownership (range 26.1-69.8%); your opponents reliably pile onto **Tommy McMillen (in 2 of 10)** — a map of where THEY go, not a read on the players; trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 47 of 67 were 25%+ owned (traps here are usually popular players who fail, not long shots); 51 of 80 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (46 of 80); from the full-field captures (8 contests): only **68.7% of entries were unique rosters**, the most-copied lineup appeared **22 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **11.6%** of lineups, **3.6%** of entries carried a structurally dead build.
- **UFC $8K Flying Knee ($2K to 1st)** (your 3 past logs of THIS contest): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 39.4% ownership (range 29.1-69.8%); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 14 of 20 were 25%+ owned (traps here are usually popular players who fail, not long shots); 16 of 24 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (13 of 24); winners trending sharper (-6.2 own/slot vs earlier); from the full-field captures (2 contests): only **68.7% of entries were unique rosters**, the most-copied lineup appeared **22 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **12.6%** of lineups, **3.6%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 19 | 7/19 | 29.8 | 26.32 | 0.5 | ~29.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 92.1 → 11.8 → 0.2 → 35.3 → 16.3
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 60% → 83% → 67% → 25%
- **Bust exposure** (top underperformers we rostered): — → 100% → 0% → 60% → 60%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 4 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 5 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-09-12__MMA Matchups 9.12.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-09-12__MMA Top Plays 9.12.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-73.csv` (26 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Jean Silva | 9300 | 42.0 | 89.7 | 0.7748 | Jose Delgado |
| Jose Delgado | 6900 | 21.0 | 43.835 | 0.22519999999999998 | Jean Silva |
| Joseph Morales | 8300 | 32.0 | 60.3 | 0.5089 | Brandon Moreno |
| Brandon Moreno | 7900 | 18.0 | 50.94 | 0.4911 | Joseph Morales |
| Tommy McMillen | 8600 | 48.0 | 69.69 | 0.5963 | Marwan Rahiki |
| Marwan Rahiki | 7600 | 36.0 | 53.58 | 0.40369999999999995 | Tommy McMillen |
| Manon Fiorot | 8900 | 16.0 | 69.06 | 0.6995 | Alexa Grasso |
| Alexa Grasso | 7300 | 14.0 | 44.24 | 0.3005 | Manon Fiorot |
| Waldo Cortes Acosta | 8700 | 26.0 | 67.31 | 0.6345000000000001 | Curtis Blaydes |
| Curtis Blaydes | 7500 | 26.0 | 46.69 | 0.3655 | Waldo Cortes Acosta |
| David Martinez | 9200 | 13.0 | 70.34 | 0.7619 | Dan Ige |
| Dan Ige | 7000 | 14.0 | 36.2 | 0.23809999999999998 | David Martinez |
| Edgar Chairez | 8800 | 24.0 | 68.98 | 0.6589 | Tim Elliott |
| Tim Elliott | 7400 | 27.0 | 49.56 | 0.3411 | Edgar Chairez |
| Ignacio Bahamondes | 9500 | 25.0 | 83.03 | 0.8148000000000001 | Muslim Salikhov |
| Muslim Salikhov | 6700 | 8.0 | 27.17 | 0.1852 | Ignacio Bahamondes |
| Yousri Belgaroui | 9700 | 20.0 | 86.48 | 0.8559 | Djorden Santos |
| Djorden Santos | 6500 | 7.0 | 33.67 | 0.1441 | Yousri Belgaroui |
| Tommy Gantt | 9400 | 43.0 | 86.99 | 0.7864 | Drakkar Klose |
| Drakkar Klose | 6800 | 9.0 | 30.6 | 0.21359999999999998 | Tommy Gantt |
| Rong Rongzhu | 8500 | 23.0 | 63.46 | 0.5915 | Rafa Garcia |
| Rafa Garcia | 7700 | 30.0 | 55.3 | 0.40850000000000003 | Rong Rongzhu |
| Sean King III | 8400 | 38.0 | 69.22 | 0.6772 | Jessie Rosas |
| Jessie Rosas | 7800 | 16.0 | 47.6 | 0.32280000000000003 | Sean King III |
| Regina Tarin | 9100 | 15.0 | 70.64 | 0.7120000000000001 | JJ Aldrich |
| JJ Aldrich | 7100 | 9.0 | 40.99 | 0.28800000000000003 | Regina Tarin |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Muslim Salikhov — $6,700, 8% own, proj 27.2, ceiling 94.7
- Djorden Santos — $6,500, 7% own, proj 33.7, ceiling 93.0
- Drakkar Klose — $6,800, 9% own, proj 30.6, ceiling 90.3
- JJ Aldrich — $7,100, 9% own, proj 41.0, ceiling 84.4

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Tommy McMillen + Tommy Gantt** — 48.0% × 43.0% ≈ 20.6% of the field (~245 lineups of 1,189)
- **Tommy McMillen + Jean Silva** — 48.0% × 42.0% ≈ 20.2% of the field (~240 lineups of 1,189)
- **Tommy McMillen + Sean King III** — 48.0% × 38.0% ≈ 18.2% of the field (~216 lineups of 1,189)
- **Tommy Gantt + Jean Silva** — 43.0% × 42.0% ≈ 18.1% of the field (~215 lineups of 1,189)
- **Tommy McMillen + Marwan Rahiki** — 48.0% × 36.0% ≈ 17.3% of the field (~206 lineups of 1,189)
- **Tommy Gantt + Sean King III** — 43.0% × 38.0% ≈ 16.3% of the field (~194 lineups of 1,189)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Rafa Garcia** — $7,700, 30.0% own: the crowd pays 10 ranks more ownership than his projection earns (owned ahead of projection).
- **Manon Fiorot** — $8,900, 16.0% own: the crowd pays 7 ranks more ownership than his projection earns (owned ahead of projection).
- **Sean King III** — $8,400, 38.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).
- **Rong Rongzhu** — $8,500, 23.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).
- **Alexa Grasso** — $7,300, 14.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).
- **Curtis Blaydes** — $7,500, 26.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/set_diversity.md` — set-level diversity + dupe-avoidance doctrine (build loose, pick strict)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/results.jsonl` — cross-slate results ledger (process notes only)

**Output target:** write the slate strategy to `data/slate_analysis/mma_se.md`.
