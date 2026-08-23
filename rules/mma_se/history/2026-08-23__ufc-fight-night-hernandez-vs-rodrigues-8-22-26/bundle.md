# Slate bundle — MMA
_Generated 2026-08-22 15:22 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 3 contest(s), 5 total entries
  - **UFC $8K Flying Knee ($2K to 1st)** (SE): field 784, my entries 1/1, prize multiple 0.85x
  - **UFC $2K Sprawl** (3-Max): field 594, my entries 3/3, prize multiple 0.84x
  - **UFC $6K Clinch** (SE): field 1,426, my entries 1/1, payout **Top-heavy**
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **UFC $8K Flying Knee ($2K to 1st)** (your 2 past logs of THIS contest): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 41.6% ownership (range 29.1-69.8%); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 8 of 12 were 25%+ owned (traps here are usually popular players who fail, not long shots); 10 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (10 of 16); from the full-field captures (1 contest): only **65.3% of entries were unique rosters**, the most-copied lineup appeared **22 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **12.6%** of lineups, **3.6%** of entries carried a structurally dead build.
- **UFC $2K Sprawl** (your 2 past logs of THIS contest): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 36.2% ownership (range 32.8-52.7%); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 6 of 6 were 25%+ owned (traps here are usually popular players who fail, not long shots); 10 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (9 of 16); winners trending sharper (-2.9 own/slot vs earlier); from the full-field captures (1 contest): only **78.6% of entries were unique rosters**, the most-copied lineup appeared **9 times**, the average opponent entered **2.2 lineups**, **38.2% of opponents were single-entry**, the top-3 chalk players landed together in **6.6%** of lineups, **2.4%** of entries carried a structurally dead build.
- **SE** (across your 6 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 38.9% ownership (range 27.8-69.8%); its 8 past crowd name(s) are NOT on this card — apply the shape to THIS card's consensus favorites (sized in `## Chalk combos`); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 26 of 35 were 25%+ owned (traps here are usually popular players who fail, not long shots); 27 of 48 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (29 of 48); from the full-field captures (4 contests): only **65.3% of entries were unique rosters**, the most-copied lineup appeared **50 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **18.6%** of lineups, **3.6%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 14 | 5/14 | 29.8 | 28.57 | 0.51 | ~29.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 2.3 → 3.5 → 11.6 → 92.1 → 11.8
- **Leverage capture** (slate-defining low-owned plays we rostered): — → — → 50% → — → 60%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → 100%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 4 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-22__MMA Matchups 8.22.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-22__MMA Top Plays 8.22.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-66.csv` (26 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Anthony Hernandez | 8600 | 56.0 | 82.7 | 0.66 | Gregory Rodrigues |
| Gregory Rodrigues | 7600 | 37.0 | 58.39 | 0.34 | Anthony Hernandez |
| Vitor Petrino | 8500 | 24.0 | 61.12 | 0.5710999999999999 | Serghei Spivac |
| Serghei Spivac | 7700 | 24.0 | 50.22 | 0.4289 | Vitor Petrino |
| Reinier de Ridder | 9200 | 30.0 | 81.7 | 0.7689 | Roman Dolidze |
| Roman Dolidze | 7000 | 13.0 | 41.4 | 0.2311 | Reinier de Ridder |
| Mason Jones | 9000 | 28.0 | 80.265 | 0.7570999999999999 | MarQuel Mederos |
| MarQuel Mederos | 7200 | 18.0 | 49.9 | 0.2429 | Mason Jones |
| Carli Judice | 9400 | 17.0 | 82.72 | 0.8181999999999999 | Jeisla Chaves |
| Jeisla Chaves | 6800 | 7.0 | 43.26 | 0.1818 | Carli Judice |
| Anthony Wint | 9900 | 24.0 | 95.41 | 0.8737 | Terrance Chatman |
| Terrance Chatman | 6300 | 5.0 | 18.49 | 0.1263 | Anthony Wint |
| Lerryan Douglas | 9300 | 38.0 | 83.92 | 0.759 | Jamall Emmers |
| Jamall Emmers | 6900 | 15.0 | 38.23 | 0.24100000000000002 | Lerryan Douglas |
| Shamil Gaziev | 8400 | 22.0 | 61.77 | 0.5217 | Kennedy Nzechukwu |
| Kennedy Nzechukwu | 7800 | 28.0 | 52.53 | 0.4783 | Shamil Gaziev |
| Nasrat Haqparast | 8200 | 23.0 | 61.13 | 0.4805 | Chris Padilla |
| Chris Padilla | 8000 | 34.0 | 62.01 | 0.5195000000000001 | Nasrat Haqparast |
| Marcio Barbosa | 9800 | 25.0 | 92.7 | 0.8525 | Ryan Kuse |
| Ryan Kuse | 6400 | 5.0 | 23.91 | 0.1475 | Marcio Barbosa |
| Gauge Young | 8300 | 27.0 | 69.61 | 0.604 | Stan Dorsainvil |
| Stan Dorsainvil | 7900 | 29.0 | 58.3 | 0.396 | Gauge Young |
| Jackson McVey | 8700 | 28.0 | 68.24 | 0.6106 | Wes Schultz |
| Wes Schultz | 7500 | 28.0 | 45.62 | 0.38939999999999997 | Jackson McVey |
| Shanelle Dyer | 9700 | 9.0 | 89.32 | 0.8512000000000001 | Elise Reed |
| Elise Reed | 6500 | 6.0 | 28.79 | 0.14880000000000002 | Shanelle Dyer |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Terrance Chatman — $6,300, 5% own, proj 18.5, ceiling 100.4
- Shanelle Dyer — $9,700, 9% own, proj 89.3, ceiling 97.4
- Ryan Kuse — $6,400, 5% own, proj 23.9, ceiling 95.4
- Jeisla Chaves — $6,800, 7% own, proj 43.3, ceiling 86.7
- Elise Reed — $6,500, 6% own, proj 28.8, ceiling 86.5

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Anthony Hernandez + Lerryan Douglas** — 56.0% × 38.0% ≈ 21.3% of the field (~304 lineups of 1,426)
- **Anthony Hernandez + Gregory Rodrigues** — 56.0% × 37.0% ≈ 20.7% of the field (~295 lineups of 1,426)
- **Anthony Hernandez + Chris Padilla** — 56.0% × 34.0% ≈ 19.0% of the field (~271 lineups of 1,426)
- **Anthony Hernandez + Reinier de Ridder** — 56.0% × 30.0% ≈ 16.8% of the field (~240 lineups of 1,426)
- **Anthony Hernandez + Stan Dorsainvil** — 56.0% × 29.0% ≈ 16.2% of the field (~231 lineups of 1,426)
- **Anthony Hernandez + Mason Jones** — 56.0% × 28.0% ≈ 15.7% of the field (~224 lineups of 1,426)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Chris Padilla** — $8,000, 34.0% own: the crowd pays 16 ranks more ownership than his projection earns (owned ahead of projection).
- **Wes Schultz** — $7,500, 28.0% own: the crowd pays 10 ranks more ownership than his projection earns (owned ahead of projection).
- **Kennedy Nzechukwu** — $7,800, 28.0% own: the crowd pays 9 ranks more ownership than his projection earns (owned ahead of projection).
- **Vitor Petrino** — $8,500, 24.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Nasrat Haqparast** — $8,200, 23.0% own: the crowd pays 7 ranks more ownership than his projection earns (owned ahead of projection).
- **Mason Jones** — $9,000, 28.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).

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
