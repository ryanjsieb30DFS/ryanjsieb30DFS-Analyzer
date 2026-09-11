# Slate bundle — NASCAR
_Generated 2026-09-06 15:51 · slug `nascar` · sport `nascar`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nascar.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NAS $5K Engine Block** (SE): field 490, my entries 1/1, prize multiple 0.85x
  - **NAS $15K Engine Block** (SE): field 1,470, my entries 1/1, prize multiple 0.85x
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **NAS $5K Engine Block** (your 3 past logs of THIS contest): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 46.5% ownership (range 24.9-68.4%); your opponents reliably pile onto **Denny Hamlin (in 3 of 3), Christopher Bell (in 3 of 3), William Byron (in 2 of 3), Bubba Wallace (in 2 of 3), Kyle Larson (in 2 of 3)** — a map of where THEY go, not a read on the players; trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 11 of 13 were 25%+ owned (traps here are usually popular players who fail, not long shots); 14 of 24 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (10 of 24); recurring opponents: avgjo (in 2 of 3); winners trending sharper (-1.1 own/slot vs earlier); from the full-field captures (1 contest): only **79.6% of entries were unique rosters**, the most-copied lineup appeared **30 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **18.8%** of lineups.
- **NAS $15K Engine Block** (your 2 past logs of THIS contest): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 45.1% ownership (range 25.6-66.3%); your opponents reliably pile onto **Kyle Larson (in 2 of 2), Christopher Bell (in 2 of 2), Bubba Wallace (in 2 of 2)** — a map of where THEY go, not a read on the players; trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 9 of 9 were 25%+ owned (traps here are usually popular players who fail, not long shots); 9 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Studs ($10k+) salary tier (5 of 16); winners trending chalkier (+5.5 own/slot vs earlier); from the full-field captures (1 contest): only **70.4% of entries were unique rosters**, the most-copied lineup appeared **85 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **18.7%** of lineups.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your nascar shark envelope:** own/slot **34.92**, leverage **4.293%**, anchor-exposure **0.668**, unique **97.853%**. You run: own/slot 28.73, leverage 2.39%, anchor 0.42 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 16 | 6/16 | 29.8 | 25.0 | 0.53 | ~29.8% own/slot |
| **Hunter4ever89** | 4 | 3/4 | 40.8 | 0.0 | 0.83 | rides the chalk anchors, little-to-no leverage, ~40.8% own/slot |
| **totoroll33** | 4 | 3/4 | 40.0 | 0.0 | 0.67 | little-to-no leverage, ~40.0% own/slot |
| **SpartyOn34** | 1 | 1/1 | 32.3 | 0.0 | 0.67 | little-to-no leverage, ~32.3% own/slot |
| **JRSobeski** | 2 | 1/2 | 33.3 | 0.0 | 0.5 | little-to-no leverage, ~33.3% own/slot |
| **3rd_and_schlong** | 1 | 1/1 | 45.2 | 0.0 | 1.0 | rides the chalk anchors, little-to-no leverage, ~45.2% own/slot |
| **vishy2773** | 1 | 0/1 | 33.8 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~33.8% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 56.9 → 7.4 → 25.5 → 40.5 → 53.1
- **Leverage capture** (slate-defining low-owned plays we rostered): 50% → 100% → 0% → 33% → 0%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → 20%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 4 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 1 of 4 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-09-06__DDD 9.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-09-06__DFR 1 9.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-09-06__DFR 2 9.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-09-06__DFR 3 9.6.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan NASCAR — `DailyFan-Projections-Sheet-NASCAR-DK-6.csv` (38 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Denny Hamlin | 11000 | 24.0 | 63.25 |
| Tyler Reddick | 10500 | 50.0 | 71.5 |
| Ryan Blaney | 10200 | 27.0 | 56.5 |
| Kyle Larson | 10000 | 35.0 | 62.4 |
| Chase Briscoe | 9800 | 28.0 | 59.15 |
| Christopher Bell | 9600 | 12.0 | 43.7 |
| William Byron | 9400 | 17.0 | 47.35 |
| Joey Logano | 9200 | 7.0 | 33.35 |
| Chase Elliott | 9000 | 12.0 | 37.0 |
| Ty Gibbs | 8800 | 39.0 | 50.35 |
| Chris Buescher | 8600 | 46.0 | 57.35 |
| Bubba Wallace | 8500 | 15.0 | 39.35 |
| Brad Keselowski | 8300 | 13.0 | 40.25 |
| Ross Chastain | 8100 | 14.0 | 36.0 |
| Carson Hocevar | 7900 | 36.0 | 47.0 |
| Corey Heim | 7700 | 15.0 | 33.0 |
| Erik Jones | 7500 | 47.0 | 47.0 |
| Austin Cindric | 7200 | 5.0 | 25.0 |
| Ryan Preece | 7000 | 4.0 | 29.25 |
| Josh Berry | 6900 | 6.0 | 21.0 |
| Alex Bowman | 6800 | 5.0 | 27.0 |
| Daniel Suarez | 6700 | 4.0 | 23.25 |
| Shane Van Gisbergen | 6500 | 18.0 | 34.35 |
| Austin Dillon | 6300 | 3.0 | 18.0 |
| Zane Smith | 6200 | 34.0 | 34.35 |
| Riley Herbst | 6100 | 5.0 | 13.0 |
| John H. Nemechek | 6000 | 6.0 | 26.0 |
| Austin Hill | 5900 | 8.0 | 22.0 |
| Michael McDowell | 5800 | 2.0 | 10.0 |
| Connor Zilisch | 5700 | 10.0 | 27.0 |
| Todd Gilliland | 5600 | 6.0 | 19.0 |
| AJ Allmendinger | 5500 | 18.0 | 26.0 |
| Noah Gragson | 5400 | 13.0 | 23.0 |
| Ricky Stenhouse Jr | 5300 | 2.0 | 15.0 |
| Cole Custer | 5100 | 3.0 | 8.0 |
| Ty Dillon | 5000 | 5.0 | 15.0 |
| Cody Ware | 4700 | 4.0 | 12.0 |
| Chad Finchum | 4500 | 2.0 | 11.0 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Joey Logano — $9,200, 7% own, proj 33.4, ceiling 33.4
- Ryan Preece — $7,000, 4% own, proj 29.2, ceiling 29.2
- Alex Bowman — $6,800, 5% own, proj 27.0, ceiling 27.0
- John H. Nemechek — $6,000, 6% own, proj 26.0, ceiling 26.0
- Austin Cindric — $7,200, 5% own, proj 25.0, ceiling 25.0
- Daniel Suarez — $6,700, 4% own, proj 23.2, ceiling 23.2
- Austin Hill — $5,900, 8% own, proj 22.0, ceiling 22.0
- Josh Berry — $6,900, 6% own, proj 21.0, ceiling 21.0
- Todd Gilliland — $5,600, 6% own, proj 19.0, ceiling 19.0
- Austin Dillon — $6,300, 3% own, proj 18.0, ceiling 18.0
- Ricky Stenhouse Jr — $5,300, 2% own, proj 15.0, ceiling 15.0
- Ty Dillon — $5,000, 5% own, proj 15.0, ceiling 15.0

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Tyler Reddick + Erik Jones** — 50.0% × 47.0% ≈ 23.5% of the field (~345 lineups of 1,470)
- **Tyler Reddick + Chris Buescher** — 50.0% × 46.0% ≈ 23.0% of the field (~338 lineups of 1,470)
- **Erik Jones + Chris Buescher** — 47.0% × 46.0% ≈ 21.6% of the field (~318 lineups of 1,470)
- **Tyler Reddick + Ty Gibbs** — 50.0% × 39.0% ≈ 19.5% of the field (~287 lineups of 1,470)
- **Erik Jones + Ty Gibbs** — 47.0% × 39.0% ≈ 18.3% of the field (~269 lineups of 1,470)
- **Tyler Reddick + Carson Hocevar** — 50.0% × 36.0% ≈ 18.0% of the field (~265 lineups of 1,470)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **AJ Allmendinger** — $5,500, 18.0% own: the crowd pays 12 ranks more ownership than his projection earns (owned ahead of projection).
- **Noah Gragson** — $5,400, 13.0% own: the crowd pays 10 ranks more ownership than his projection earns (owned ahead of projection).
- **Zane Smith** — $6,200, 34.0% own: the crowd pays 9 ranks more ownership than his projection earns (owned ahead of projection).
- **Erik Jones** — $7,500, 47.0% own: the crowd pays 7 ranks more ownership than his projection earns (owned ahead of projection).
- **Shane Van Gisbergen** — $6,500, 18.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).
- **Corey Heim** — $7,700, 15.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/set_diversity.md` — set-level diversity + dupe-avoidance doctrine (build loose, pick strict)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/results.jsonl` — cross-slate results ledger (process notes only)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/atlanta_motor_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/charlotte_motor_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/chicagoland_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/darlington_raceway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/daytona_international_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/indianapolis_motor_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/iowa_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/nashville_superspeedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/naval_base_coronado.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/north_wilkesboro_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/pocono_raceway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/richmond_raceway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/sonoma_raceway.md`

**Output target:** write the slate strategy to `data/slate_analysis/nascar.md`.
