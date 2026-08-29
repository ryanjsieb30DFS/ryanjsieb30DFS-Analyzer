# Slate bundle — MMA
_Generated 2026-08-29 00:14 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 2 total entries
  - **UFC $3K Clinch [Single Entry]** (SE): field 713, my entries 1/1, payout **Top-heavy**, prize multiple 0.84x
  - **UFC $4K Flying Knee [Single Entry]** (SE): field 392, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **SE** (across your 9 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 37.6% ownership (range 27.8-69.8%); its 8 past crowd name(s) are NOT on this card — apply the shape to THIS card's consensus favorites (sized in `## Chalk combos`); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 38 of 49 were 25%+ owned (traps here are usually popular players who fail, not long shots); 45 of 72 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (41 of 72); from the full-field captures (6 contests): only **68.7% of entries were unique rosters**, the most-copied lineup appeared **22 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **10.2%** of lineups, **3.1%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 15 | 5/15 | 29.8 | 26.67 | 0.52 | ~29.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 3.5 → 11.6 → 92.1 → 11.8 → 0.2
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 50% → — → 60% → 83%
- **Bust exposure** (top underperformers we rostered): — → — → — → 100% → 0%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 4 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 5 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-28__MMA Matchups 8.29.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-28__MMA Top Plays 8.29.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-69.csv` (26 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Umar Nurmagomedov | 9500 | 45.0 | 99.38 | 0.8181999999999999 | Yadong Song |
| Yadong Song | 6700 | 18.0 | 41.99 | 0.1818 | Umar Nurmagomedov |
| Yan Xiaonan | 8500 | 16.0 | 60.88 | 0.5710999999999999 | Denise Gomes |
| Denise Gomes | 7700 | 31.0 | 57.3 | 0.4289 | Yan Xiaonan |
| Kai Asakura | 9400 | 21.0 | 80.05 | 0.79 | Aori Aoriqileng |
| Aori Aoriqileng | 6800 | 14.0 | 32.88 | 0.21 | Kai Asakura |
| Su Sumudaerji | 8800 | 24.0 | 64.84 | 0.6668000000000001 | Alex Perez |
| Alex Perez | 7400 | 21.0 | 43.38 | 0.3332 | Su Sumudaerji |
| Liu Ce | 8700 | 38.0 | 66.21 | 0.6288 | Levi Rodrigues Jr. |
| Levi Rodrigues Jr. | 7500 | 25.0 | 39.2 | 0.3712 | Liu Ce |
| Bilal Hasan | 9600 | 29.0 | 90.19 | 0.8545999999999999 | Nilson Rojas |
| Nilson Rojas | 6600 | 7.0 | 25.24 | 0.1454 | Bilal Hasan |
| Andre Lima | 9000 | 20.0 | 70.86 | 0.6984 | Namsrai Batbayar |
| Namsrai Batbayar | 7200 | 18.0 | 40.22 | 0.3016 | Andre Lima |
| Rei Tsuruya | 9700 | 25.0 | 91.64 | 0.8476 | Kevin Borjas |
| Kevin Borjas | 6500 | 7.0 | 24.2 | 0.1524 | Rei Tsuruya |
| Sean Woodson | 8400 | 25.0 | 64.96 | 0.5487 | Jack Jenkins |
| Jack Jenkins | 7800 | 28.0 | 53.39 | 0.45130000000000003 | Sean Woodson |
| Xiao Long | 8600 | 22.0 | 67.47 | 0.5963 | Francesco Nuzzi |
| Francesco Nuzzi | 7600 | 24.0 | 49.49 | 0.40369999999999995 | Xiao Long |
| Lawrence Lui | 9100 | 32.0 | 76.09 | 0.718 | Hector Santiago |
| Hector Santiago | 7100 | 16.0 | 41.81 | 0.282 | Lawrence Lui |
| Julia Polastri | 8900 | 19.0 | 69.455 | 0.6792 | Xiong Jingnan |
| Xiong Jingnan | 7300 | 16.0 | 46.75 | 0.3208 | Julia Polastri |
| Ding Meng | 8300 | 28.0 | 63.2 | 0.5710999999999999 | Cam Nelson |
| Cam Nelson | 7900 | 31.0 | 52.3 | 0.4289 | Ding Meng |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Nilson Rojas — $6,600, 7% own, proj 25.2, ceiling 94.6
- Kevin Borjas — $6,500, 7% own, proj 24.2, ceiling 85.2

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Umar Nurmagomedov + Liu Ce** — 45.0% × 38.0% ≈ 17.1% of the field (~122 lineups of 713)
- **Umar Nurmagomedov + Lawrence Lui** — 45.0% × 32.0% ≈ 14.4% of the field (~103 lineups of 713)
- **Umar Nurmagomedov + Cam Nelson** — 45.0% × 31.0% ≈ 14.0% of the field (~100 lineups of 713)
- **Umar Nurmagomedov + Denise Gomes** — 45.0% × 31.0% ≈ 14.0% of the field (~100 lineups of 713)
- **Umar Nurmagomedov + Bilal Hasan** — 45.0% × 29.0% ≈ 13.1% of the field (~93 lineups of 713)
- **Umar Nurmagomedov + Ding Meng** — 45.0% × 28.0% ≈ 12.6% of the field (~90 lineups of 713)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Sean Woodson** — $8,400, 25.0% own: the crowd pays 13 ranks more ownership than his projection earns (owned ahead of projection).
- **Jack Jenkins** — $7,800, 28.0% own: the crowd pays 12 ranks more ownership than his projection earns (owned ahead of projection).
- **Su Sumudaerji** — $8,800, 24.0% own: the crowd pays 9 ranks more ownership than his projection earns (owned ahead of projection).
- **Denise Gomes** — $7,700, 31.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Francesco Nuzzi** — $7,600, 24.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Julia Polastri** — $8,900, 19.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).

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
