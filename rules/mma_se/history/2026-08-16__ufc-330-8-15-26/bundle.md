# Slate bundle — MMA
_Generated 2026-08-15 14:13 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 3 contest(s), 5 total entries
  - **UFC $3K Sprawl [3 Entry Max]** (3-Max): field 891, my entries 3/3, payout **Flat**, prize multiple 0.00x
  - **UFC $12K Flying Knee [Single Entry]** (SE): field 1,176, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
  - **UFC $10K Clinch [Single Entry]** (SE): field 2,378, my entries 1/1, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **3-Max** (across your 2 past comparable 3-Max contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 36.2% ownership (range 32.8-52.7%); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 6 of 6 were 25%+ owned (traps here are usually popular players who fail, not long shots); 10 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (9 of 16); from the full-field captures (1 contest): only **78.6% of entries were unique rosters**, the most-copied lineup appeared **9 times**, the average opponent entered **2.2 lineups**, **38.2% of opponents were single-entry**, the top-3 chalk players landed together in **6.6%** of lineups, **2.4%** of entries carried a structurally dead build.
- **SE** (across your 5 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 37.6% ownership (range 27.8-69.8%); its 8 past crowd name(s) are NOT on this card — apply the shape to THIS card's consensus favorites (sized in `## Chalk combos`); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 17 of 22 were 25%+ owned (traps here are usually popular players who fail, not long shots); 23 of 40 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (25 of 40); from the full-field captures (2 contests): only **69.1% of entries were unique rosters**, the most-copied lineup appeared **22 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **12.6%** of lineups, **3.6%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 11 | 4/11 | 27.8 | 32.73 | 0.5 | ~27.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 26.1 → 2.3 → 3.5 → 11.6 → 92.1
- **Leverage capture** (slate-defining low-owned plays we rostered): 0% → — → — → 50% → —
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 3 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-15__MMA Matchups 8.15.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-15__MMA Top Plays 8.15.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-64.csv` (24 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Islam Makhachev | 9200 | 50.0 | 92.04 | 0.7447 | Ian Machado Garry |
| Ian Machado Garry | 7000 | 19.0 | 38.34 | 0.2553 | Islam Makhachev |
| Mackenzie Dern | 9000 | 44.0 | 85.67 | 0.6302 | Gillian Robertson |
| Gillian Robertson | 7200 | 36.0 | 63.46 | 0.36979999999999996 | Mackenzie Dern |
| Jalin Turner | 8600 | 26.0 | 63.95 | 0.5 | Kaue Fernandes |
| Kaue Fernandes | 7600 | 34.0 | 49.24 | 0.5 | Jalin Turner |
| Mansur Abdul-Malik | 9500 | 16.0 | 87.1 | 0.8329000000000001 | Dustin Stoltzfus |
| Dustin Stoltzfus | 6700 | 8.0 | 26.14 | 0.1671 | Mansur Abdul-Malik |
| Esteban Ribovics | 9400 | 29.0 | 90.22 | 0.8411 | Edson Barboza |
| Edson Barboza | 6800 | 7.0 | 30.21 | 0.1589 | Esteban Ribovics |
| Joel Alvarez | 8900 | 29.0 | 76.74 | 0.7328 | Chidi Njokuani |
| Chidi Njokuani | 7300 | 15.0 | 38.5 | 0.2672 | Joel Alvarez |
| Eduardo Chapolin | 7900 | 17.0 | 59.1 | 0.48700000000000004 | Charles Johnson |
| Charles Johnson | 6900 | 43.0 | 59.4 | 0.513 | Eduardo Chapolin |
| Donte Johnson | 8800 | 26.0 | 75.85 | 0.7243999999999999 | Eric McConico |
| Eric McConico | 7400 | 15.0 | 37.69 | 0.2756 | Donte Johnson |
| Tresean Gore | 8400 | 25.0 | 58.36 | 0.5 | Vicente Luque |
| Vicente Luque | 7800 | 30.0 | 56.43 | 0.5 | Tresean Gore |
| Lucas Fernando | 9100 | 18.0 | 74.8 | 0.6984 | Rafael Tobias |
| Rafael Tobias | 7100 | 15.0 | 43.16 | 0.3016 | Lucas Fernando |
| Ramiz Brahimaj | 8200 | 36.0 | 66.2 | 0.5693 | Neil Magny |
| Neil Magny | 8000 | 17.0 | 45.62 | 0.4307 | Ramiz Brahimaj |
| Myktybek Orolbai | 9600 | 40.0 | 93.5 | 0.8812000000000001 | Jeremiah Wells |
| Jeremiah Wells | 6600 | 5.0 | 27.78 | 0.1188 | Myktybek Orolbai |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Jeremiah Wells — $6,600, 5% own, proj 27.8, ceiling 97.1
- Dustin Stoltzfus — $6,700, 8% own, proj 26.1, ceiling 94.6
- Edson Barboza — $6,800, 7% own, proj 30.2, ceiling 89.1

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Islam Makhachev + Mackenzie Dern** — 50.0% × 44.0% ≈ 22.0% of the field (~523 lineups of 2,378)
- **Islam Makhachev + Charles Johnson** — 50.0% × 43.0% ≈ 21.5% of the field (~511 lineups of 2,378)
- **Islam Makhachev + Myktybek Orolbai** — 50.0% × 40.0% ≈ 20.0% of the field (~476 lineups of 2,378)
- **Mackenzie Dern + Charles Johnson** — 44.0% × 43.0% ≈ 18.9% of the field (~449 lineups of 2,378)
- **Islam Makhachev + Gillian Robertson** — 50.0% × 36.0% ≈ 18.0% of the field (~428 lineups of 2,378)
- **Islam Makhachev + Ramiz Brahimaj** — 50.0% × 36.0% ≈ 18.0% of the field (~428 lineups of 2,378)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Charles Johnson** — $6,900, 43.0% own: the crowd pays 20 ranks more ownership than his projection earns (owned ahead of projection).
- **Kaue Fernandes** — $7,600, 34.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Neil Magny** — $8,000, 17.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).
- **Donte Johnson** — $8,800, 26.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).
- **Eric McConico** — $7,400, 15.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).
- **Eduardo Chapolin** — $7,900, 17.0% own: the crowd pays 4 ranks more ownership than his projection earns (owned ahead of projection).

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
