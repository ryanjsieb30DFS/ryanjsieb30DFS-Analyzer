# Slate bundle — MMA
_Generated 2026-09-05 09:16 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 2 total entries
  - **UFC $6K Flying Knee** (SE): field 588, my entries 1/1, prize multiple 0.00x
  - **UFC $4k Clinch** (SE): field 951, my entries 1/1, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **SE** (across your 8 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 37.8% ownership (range 26.1-69.8%); its 7 past crowd name(s) are NOT on this card — apply the shape to THIS card's consensus favorites (sized in `## Chalk combos`); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 33 of 50 were 25%+ owned (traps here are usually popular players who fail, not long shots); 41 of 64 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (35 of 64); from the full-field captures (6 contests): only **79.3% of entries were unique rosters**, the most-copied lineup appeared **11 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **11.6%** of lineups, **3.6%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 16 | 6/16 | 29.8 | 25.0 | 0.53 | ~29.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 11.6 → 92.1 → 11.8 → 0.2 → 35.3
- **Leverage capture** (slate-defining low-owned plays we rostered): 50% → — → 60% → 83% → 67%
- **Bust exposure** (top underperformers we rostered): — → — → 100% → 0% → 60%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 5 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-09-05__MMA Matchups 9.5.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-09-05__MMA Top Plays 9.5.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-71.csv` (28 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Salahdine Parnasse | 9500 | 45.0 | 93.43 | 0.8181999999999999 | Dan Hooker |
| Dan Hooker | 6700 | 8.0 | 40.62 | 0.1818 | Salahdine Parnasse |
| Fares Ziam | 8600 | 25.0 | 62.33 | 0.5828 | Axel Sola |
| Axel Sola | 7600 | 25.0 | 52.6 | 0.4172 | Fares Ziam |
| Michael Page | 8700 | 13.0 | 50.07 | 0.6193 | Nursulton Ruziboev |
| Nursulton Ruziboev | 7500 | 24.0 | 48.31 | 0.3807 | Michael Page |
| Daniil Donchenko | 9000 | 38.0 | 75.94 | 0.6736 | Punahele Soriano |
| Punahele Soriano | 7200 | 20.0 | 45.115 | 0.3264 | Daniil Donchenko |
| Kurtis Campbell | 9300 | 29.0 | 79.87 | 0.7619 | Trevor Peek |
| Trevor Peek | 6900 | 9.0 | 34.53 | 0.23809999999999998 | Kurtis Campbell |
| Losene Keita | 9200 | 26.0 | 76.14 | 0.7512000000000001 | Muhammad Naimov |
| Muhammad Naimov | 7000 | 9.0 | 37.24 | 0.2488 | Losene Keita |
| Felipe Lima | 8900 | 16.0 | 67.15 | 0.6365999999999999 | Morgan Charriere |
| Morgan Charriere | 7300 | 19.0 | 47.61 | 0.36340000000000006 | Felipe Lima |
| Mario Pinto | 9100 | 32.0 | 74.83 | 0.7492 | Ryan Spann |
| Ryan Spann | 7100 | 17.0 | 38.67 | 0.25079999999999997 | Mario Pinto |
| Oumar Sy | 8800 | 22.0 | 67.81 | 0.6942 | Modestas Bukauskas |
| Modestas Bukauskas | 7400 | 15.0 | 40.62 | 0.30579999999999996 | Oumar Sy |
| Nathaniel Wood | 9200 | 16.0 | 74.6 | 0.716 | Pavel Andrusca |
| Pavel Andrusca | 7000 | 14.0 | 46.95 | 0.284 | Nathaniel Wood |
| Michael Aljarouj | 8400 | 22.0 | 60.68 | 0.5255 | Fabia Sintes |
| Fabia Sintes | 7800 | 22.0 | 55.38 | 0.47450000000000003 | Michael Aljarouj |
| Nora Cornolle | 8300 | 16.0 | 58.29 | 0.4789 | Klaudia Sygula |
| Klaudia Sygula | 7900 | 16.0 | 49.94 | 0.5211 | Nora Cornolle |
| Matthieu Duclos | 8200 | 36.0 | 55.64 | 0.5255 | Luis Felipe Dias |
| Luis Felipe Dias | 8000 | 35.0 | 54.07 | 0.47450000000000003 | Matthieu Duclos |
| Delphine Benouaich | 8500 | 14.0 | 59.21 | 0.5564 | Sofia Montenegro |
| Sofia Montenegro | 7700 | 17.0 | 55.05 | 0.4436 | Delphine Benouaich |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Dan Hooker — $6,700, 8% own, proj 40.6, ceiling 106.7
- Trevor Peek — $6,900, 9% own, proj 34.5, ceiling 94.5
- Muhammad Naimov — $7,000, 9% own, proj 37.2, ceiling 92.4

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Salahdine Parnasse + Daniil Donchenko** — 45.0% × 38.0% ≈ 17.1% of the field (~163 lineups of 951)
- **Salahdine Parnasse + Matthieu Duclos** — 45.0% × 36.0% ≈ 16.2% of the field (~154 lineups of 951)
- **Salahdine Parnasse + Luis Felipe Dias** — 45.0% × 35.0% ≈ 15.8% of the field (~150 lineups of 951)
- **Salahdine Parnasse + Mario Pinto** — 45.0% × 32.0% ≈ 14.4% of the field (~137 lineups of 951)
- **Daniil Donchenko + Matthieu Duclos** — 38.0% × 36.0% ≈ 13.7% of the field (~130 lineups of 951)
- **Daniil Donchenko + Luis Felipe Dias** — 38.0% × 35.0% ≈ 13.3% of the field (~126 lineups of 951)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Fares Ziam** — $8,600, 25.0% own: the crowd pays 13 ranks more ownership than his projection earns (owned ahead of projection).
- **Nursulton Ruziboev** — $7,500, 24.0% own: the crowd pays 12 ranks more ownership than his projection earns (owned ahead of projection).
- **Sofia Montenegro** — $7,700, 17.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Klaudia Sygula** — $7,900, 16.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Axel Sola** — $7,600, 25.0% own: the crowd pays 7 ranks more ownership than his projection earns (owned ahead of projection).
- **Oumar Sy** — $8,800, 22.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).

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
