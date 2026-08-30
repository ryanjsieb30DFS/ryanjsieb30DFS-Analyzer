# Slate bundle — NASCAR
_Generated 2026-08-29 17:52 · slug `nascar` · sport `nascar`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nascar.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NAS $12K Engine Block [Single Entry] (Cup)** (SE): field 1,176, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
  - **NAS $4K Engine Block [Single Entry]** (SE): field 392, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **SE** (across your 3 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 38.6% ownership (range 25.2-74.3%); your opponents reliably pile onto **Christopher Bell (in 3 of 3), Bubba Wallace (in 3 of 3), Kyle Larson (in 2 of 3), Ryan Blaney (in 2 of 3), Ty Gibbs (in 2 of 3), Todd Gilliland (in 2 of 3), Ryan Preece (in 2 of 3)** — a map of where THEY go, not a read on the players; trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 11 of 17 were 25%+ owned (traps here are usually popular players who fail, not long shots); 12 of 24 were owned ahead of their projection rank (the trap-shaped price); most sat in the Upper-mid ($8-10k) salary tier (8 of 24); from the full-field captures (1 contest): only **70.4% of entries were unique rosters**, the most-copied lineup appeared **85 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **18.7%** of lineups.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your nascar shark envelope:** own/slot **34.971**, leverage **4.6%**, anchor-exposure **0.668**, unique **97.7%**. You run: own/slot 28.73, leverage 2.39%, anchor 0.42 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 15 | 5/15 | 29.8 | 26.67 | 0.52 | ~29.8% own/slot |
| **Hunter4ever89** | 3 | 2/3 | 40.8 | 0.0 | 0.78 | little-to-no leverage, ~40.8% own/slot |
| **totoroll33** | 3 | 2/3 | 40.0 | 0.0 | 0.78 | little-to-no leverage, ~40.0% own/slot |
| **3rd_and_schlong** | 1 | 1/1 | 45.2 | 0.0 | 1.0 | rides the chalk anchors, little-to-no leverage, ~45.2% own/slot |
| **vishy2773** | 1 | 0/1 | 33.8 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~33.8% own/slot |
| **JRSobeski** | 1 | 0/1 | 31.0 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~31.0% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 27.1 → 56.9 → 7.4 → 25.5 → 40.5
- **Leverage capture** (slate-defining low-owned plays we rostered): 0% → 50% → 100% → 0% → 33%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 3 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-29__DDD 8.29.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-29__DFR 1 8.29.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-29__DFR 2 8.29.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan NASCAR — `DailyFan-Projections-Sheet-NASCAR-DK-4 (2).csv` (39 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Ryan Blaney | 10500 | 36.0 | 53.3 |
| William Byron | 10400 | 11.0 | 40.35 |
| Christopher Bell | 10200 | 48.0 | 53.35 |
| Joey Logano | 10000 | 14.0 | 45.35 |
| Chase Elliott | 9900 | 29.0 | 47.35 |
| Tyler Reddick | 9700 | 14.0 | 37.35 |
| Kyle Larson | 9500 | 6.0 | 30.35 |
| Austin Cindric | 9300 | 12.0 | 42.35 |
| Denny Hamlin | 9100 | 38.0 | 48.35 |
| Bubba Wallace | 9000 | 26.0 | 48.35 |
| Chase Briscoe | 8900 | 7.0 | 25.9 |
| Carson Hocevar | 8700 | 23.0 | 46.8 |
| Chris Buescher | 8500 | 6.0 | 26.9 |
| Brad Keselowski | 8300 | 32.0 | 52.1 |
| Ricky Stenhouse Jr | 8100 | 37.0 | 47.9 |
| Ty Gibbs | 7900 | 5.0 | 33.25 |
| Corey Heim | 7700 | 3.0 | 29.35 |
| Ryan Preece | 7600 | 5.0 | 27.65 |
| Ross Chastain | 7500 | 8.0 | 20.65 |
| Austin Dillon | 7300 | 22.0 | 39.35 |
| Josh Berry | 7100 | 10.0 | 40.35 |
| Alex Bowman | 6900 | 14.0 | 32.35 |
| Daniel Suarez | 6700 | 9.0 | 37.35 |
| Erik Jones | 6600 | 4.0 | 27.35 |
| Todd Gilliland | 6400 | 21.0 | 39.35 |
| Austin Hill | 6300 | 2.0 | 14.9 |
| Shane Van Gisbergen | 6200 | 3.0 | 17.9 |
| Michael McDowell | 6100 | 4.0 | 27.9 |
| Zane Smith | 5900 | 30.0 | 44.8 |
| Connor Zilisch | 5800 | 3.0 | 18.9 |
| AJ Allmendinger | 5500 | 37.0 | 45.25 |
| Noah Gragson | 5400 | 33.0 | 46.25 |
| John H. Nemechek | 5200 | 13.0 | 40.7 |
| Cole Custer | 5100 | 3.0 | 23.9 |
| Ty Dillon | 5000 | 21.0 | 42.9 |
| Cody Ware | 4900 | 1.0 | 17.9 |
| Joey Gase | 4800 | 3.0 | 32.45 |
| Casey Mears | 4700 | 2.0 | 30.45 |
| Daniel Dye | 4500 | 3.0 | 31.45 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Daniel Suarez — $6,700, 9% own, proj 37.4, ceiling 37.4
- Ty Gibbs — $7,900, 5% own, proj 33.2, ceiling 33.2
- Joey Gase — $4,800, 3% own, proj 32.5, ceiling 32.5
- Daniel Dye — $4,500, 3% own, proj 31.4, ceiling 31.4
- Casey Mears — $4,700, 2% own, proj 30.4, ceiling 30.4
- Kyle Larson — $9,500, 6% own, proj 30.4, ceiling 30.4
- Corey Heim — $7,700, 3% own, proj 29.4, ceiling 29.4
- Michael McDowell — $6,100, 4% own, proj 27.9, ceiling 27.9
- Ryan Preece — $7,600, 5% own, proj 27.6, ceiling 27.6
- Erik Jones — $6,600, 4% own, proj 27.4, ceiling 27.4
- Chris Buescher — $8,500, 6% own, proj 26.9, ceiling 26.9
- Chase Briscoe — $8,900, 7% own, proj 25.9, ceiling 25.9

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Christopher Bell + Denny Hamlin** — 48.0% × 38.0% ≈ 18.2% of the field (~214 lineups of 1,176)
- **Christopher Bell + AJ Allmendinger** — 48.0% × 37.0% ≈ 17.8% of the field (~209 lineups of 1,176)
- **Christopher Bell + Ricky Stenhouse Jr** — 48.0% × 37.0% ≈ 17.8% of the field (~209 lineups of 1,176)
- **Christopher Bell + Ryan Blaney** — 48.0% × 36.0% ≈ 17.3% of the field (~203 lineups of 1,176)
- **Christopher Bell + Noah Gragson** — 48.0% × 33.0% ≈ 15.8% of the field (~186 lineups of 1,176)
- **Christopher Bell + Brad Keselowski** — 48.0% × 32.0% ≈ 15.4% of the field (~181 lineups of 1,176)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Alex Bowman** — $6,900, 14.0% own: the crowd pays 9 ranks more ownership than his projection earns (owned ahead of projection).
- **AJ Allmendinger** — $5,500, 37.0% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).
- **Austin Dillon** — $7,300, 22.0% own: the crowd pays 6 ranks more ownership than his projection earns (owned ahead of projection).
- **Tyler Reddick** — $9,700, 14.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).
- **Todd Gilliland** — $6,400, 21.0% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).
- **Zane Smith** — $5,900, 30.0% own: the crowd pays 4 ranks more ownership than his projection earns (owned ahead of projection).

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/results.jsonl` — cross-slate results ledger (process notes only)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/atlanta_motor_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/charlotte_motor_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/chicagoland_speedway.md`
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
