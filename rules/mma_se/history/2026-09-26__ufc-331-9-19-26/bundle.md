# Slate bundle — MMA
_Generated 2026-09-19 14:34 · slug `mma_se` · sport `mma`_
_**DraftKings only.** Ignore every FanDuel (FD) section, column, price, ownership number, or roster rule in any file below — the user never plays FD._

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 1 contest(s), 100 total entries
  - **UFC $25K Mini Max** (150-Max): field 59,453, my entries 100/150, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## Slate at a glance`; never a play/fade command._
_**LARGE-FIELD CONTEST(S) DECLARED** (UFC $25K Mini Max (150-Max)) — the strategy MUST include the **big-field attack step** inside `## Build it like a sharp` (one evidence-backed line per field mistake; replaced the separate `## Field attack plan` section 8/9/26, see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **150-Max** (across your 2 past comparable 150-Max contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 33.9% ownership (range 26.5-49.2%); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 6 of 16 were 25%+ owned (traps here are usually popular players who fail, not long shots); 9 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (8 of 16); from the full-field captures (2 contests): only **26.5% of entries were unique rosters**, the most-copied lineup appeared **177 times**, the average opponent entered **19.5 lineups**, **45.8% of opponents were single-entry**, the top-3 chalk players landed together in **4.1%** of lineups, **3.4%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 22 | 9/22 | 29.8 | 27.27 | 0.49 | ~29.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 0.2 → 35.3 → 16.3 → 39.1 → —
- **Leverage capture** (slate-defining low-owned plays we rostered): 83% → 67% → 25% → 100% → 100%
- **Bust exposure** (top underperformers we rostered): 0% → 60% → 60% → 60% → 60%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 5 graded slates — the board's boundaries are suspect.
- **150-max portfolio** (how the top 1% and the big stacks built vs you, per slate):
  - 2026-09-19: top 1% summed 189.3% own vs field 168.4%, 0.11 sub-10% pieces per lineup; winner copied 14x; 2.2% of the top 1% were one-of-one; you: 6 entries, top-1% rate 0.0%, cash 16.7% (big-stack median 0.7% / 19.3%)

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-09-19__UFC 331 Beatdown – DailyFanSports.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-09-19__UFC 331 Top Plays_Slate Summary – DailyFanSports.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-75.csv` (24 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Joshua Van | 8300 | 50.0 | 78.66 | 0.5556 | Alexandre Pantoja |
| Alexandre Pantoja | 7900 | 42.0 | 73.01 | 0.44439999999999996 | Joshua Van |
| Arman Tsarukyan | 9100 | 48.0 | 90.28 | 0.7509999999999999 | Mauricio Ruffy |
| Mauricio Ruffy | 7100 | 24.0 | 37.91 | 0.249 | Arman Tsarukyan |
| Dooho Choi | 8900 | 24.0 | 76.1 | 0.7055 | Patricio Pitbull |
| Patricio Pitbull | 7300 | 18.0 | 42.9 | 0.2945 | Dooho Choi |
| Gable Steveson | 9900 | 29.0 | 98.12 | 0.9286 | Sean Sharaf |
| Sean Sharaf | 6300 | 3.0 | 13.8 | 0.07139999999999999 | Gable Steveson |
| Iwo Baraniewski | 8700 | 48.0 | 74.48 | 0.6736 | Alonzo Menifield |
| Alonzo Menifield | 7500 | 26.0 | 37.48 | 0.3264 | Iwo Baraniewski |
| Charles Jourdain | 8800 | 15.0 | 70.45 | 0.6523 | Marlon Vera |
| Marlon Vera | 7400 | 21.0 | 49.79 | 0.3477 | Charles Jourdain |
| Robelis Despaigne | 9600 | 20.0 | 88.11 | 0.8148000000000001 | Tai Tuivasa |
| Tai Tuivasa | 6600 | 5.0 | 21.76 | 0.1852 | Robelis Despaigne |
| JooSang Yoo | 9000 | 12.0 | 72.07 | 0.6431999999999999 | Michael Aswell Jr. |
| Michael Aswell Jr. | 7200 | 26.0 | 49.15 | 0.3568 | JooSang Yoo |
| Ryan Gandra | 9400 | 31.0 | 86.19 | 0.8023 | Ozzy Diaz |
| Ozzy Diaz | 6800 | 6.0 | 24.33 | 0.1977 | Ryan Gandra |
| Edmen Shahbazyan | 8400 | 31.0 | 65.89 | 0.6087 | Brunno Ferreira |
| Brunno Ferreira | 7800 | 31.0 | 44.21 | 0.39130000000000004 | Edmen Shahbazyan |
| Casey O'Neill | 8500 | 36.0 | 71.78 | 0.6620999999999999 | Eduarda Moura |
| Eduarda Moura | 7700 | 29.0 | 52.61 | 0.3379 | Casey O'Neill |
| Joanderson Brito | 9200 | 17.0 | 79.84 | 0.7672 | Giga Chikadze |
| Giga Chikadze | 7000 | 8.0 | 33.54 | 0.2328 | Joanderson Brito |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Sean Sharaf — $6,300, 3% own, proj 13.8, ceiling 102.8
- Ozzy Diaz — $6,800, 6% own, proj 24.3, ceiling 101.1
- Tai Tuivasa — $6,600, 5% own, proj 21.8, ceiling 101.0
- Giga Chikadze — $7,000, 8% own, proj 33.5, ceiling 85.1

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Joshua Van + Arman Tsarukyan** — 50.0% × 48.0% ≈ 24.0% of the field (~14,269 lineups of 59,453)
- **Joshua Van + Iwo Baraniewski** — 50.0% × 48.0% ≈ 24.0% of the field (~14,269 lineups of 59,453)
- **Arman Tsarukyan + Iwo Baraniewski** — 48.0% × 48.0% ≈ 23.0% of the field (~13,674 lineups of 59,453)
- **Joshua Van + Alexandre Pantoja** — 50.0% × 42.0% ≈ 21.0% of the field (~12,485 lineups of 59,453)
- **Arman Tsarukyan + Alexandre Pantoja** — 48.0% × 42.0% ≈ 20.2% of the field (~12,010 lineups of 59,453)
- **Iwo Baraniewski + Alexandre Pantoja** — 48.0% × 42.0% ≈ 20.2% of the field (~12,010 lineups of 59,453)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Casey O'Neill** — $8,500, 36.0% own: the crowd pays 14 ranks more ownership than his projection earns (owned ahead of projection).
- **Eduarda Moura** — $7,700, 29.0% own: the crowd pays 12 ranks more ownership than his projection earns (owned ahead of projection).
- **Michael Aswell Jr.** — $7,200, 26.0% own: the crowd pays 11 ranks more ownership than his projection earns (owned ahead of projection).
- **Brunno Ferreira** — $7,800, 31.0% own: the crowd pays 10 ranks more ownership than his projection earns (owned ahead of projection).
- **Edmen Shahbazyan** — $8,400, 31.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Iwo Baraniewski** — $8,700, 48.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).

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
