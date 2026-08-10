# Slate bundle — NASCAR
_Generated 2026-08-09 13:20 · slug `nascar` · sport `nascar`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nascar.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NAS $8K Rainbow Warrior** (SE): field 392, my entries 1/1, prize multiple 0.85x
  - **NAS $6K Engine Block [Single Entry, $1K to 1st] (Cup)** (SE): field 588, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **SE** (across your 6 past SE contests): SHAPE: the field reliably piles onto ~8 names per contest; the field reliably crowds **Christopher Bell (in 6 of 6), Denny Hamlin (in 5 of 6), Bubba Wallace (in 5 of 6), William Byron (in 4 of 6), Kyle Larson (in 4 of 6), Zane Smith (in 2 of 6), Noah Gragson (in 2 of 6), AJ Allmendinger (in 2 of 6)**; recurring fish-traps: **William Byron (in 5 of 6), Bubba Wallace (in 4 of 6), AJ Allmendinger (in 3 of 6), Chase Elliott (in 3 of 6), Ryan Blaney (in 3 of 6), Erik Jones (in 3 of 6), Kyle Larson (in 3 of 6), Denny Hamlin (in 2 of 6)**; the field PAIRS **Denny Hamlin + Tyler Reddick (in 2 of 6), Christopher Bell + Zane Smith (in 2 of 6), Christopher Bell + Tyler Reddick (in 2 of 6), Christopher Bell + Denny Hamlin (in 2 of 6), Tyler Reddick + Zane Smith (in 2 of 6)** — a dupe-magnet stack; leverage lives in breaking it; from the full-field captures (2 contests): only **79.6% of entries were unique rosters**, the most-copied lineup appeared **85 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **18.8%** of lineups.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your nascar shark envelope:** own/slot **34.962**, leverage **4.954%**, anchor-exposure **0.677**, unique **97.523%**. You run: own/slot 28.73, leverage 2.39%, anchor 0.42 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 7 | 3/7 | 22.9 | 37.14 | 0.5 | ~22.9% own/slot |
| **3rd_and_schlong** | 1 | 1/1 | 45.2 | 0.0 | 1.0 | rides the chalk anchors, little-to-no leverage, ~45.2% own/slot |
| **Hunter4ever89** | 2 | 1/2 | 44.4 | 0.0 | 0.83 | rides the chalk anchors, little-to-no leverage, ~44.4% own/slot |
| **totoroll33** | 2 | 1/2 | 45.2 | 0.0 | 1.0 | rides the chalk anchors, little-to-no leverage, ~45.2% own/slot |
| **vishy2773** | 1 | 0/1 | 33.8 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~33.8% own/slot |
| **JRSobeski** | 1 | 0/1 | 31.0 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~31.0% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 0.3 → 27.1 → 56.9 → 7.4 → 25.5
- **Leverage capture** (slate-defining low-owned plays we rostered): 100% → 0% → 50% → 100% → 0%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 2 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 2 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-09__DFR Image 1 8.9.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-09__DFR Image 2 8.9.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-09__DFR Image 3 8.9.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-09__DFR Image 4 8.9.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-09__DFR Image 5 8.9.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-08-09__ETR PGA RD4 SD Article.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan NASCAR — `DailyFan-Projections-Sheet-NASCAR-DK-15 (3).csv` (36 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Denny Hamlin | 11100 | 32.0 | 64.85 |
| Christopher Bell | 10700 | 35.0 | 67.0 |
| Ryan Blaney | 10500 | 52.0 | 74.25 |
| William Byron | 10000 | 33.0 | 57.55 |
| Kyle Larson | 9700 | 22.0 | 50.75 |
| Joey Logano | 9500 | 31.0 | 59.0 |
| Chase Briscoe | 9200 | 18.0 | 45.8 |
| Chase Elliott | 9000 | 35.0 | 50.8 |
| Tyler Reddick | 8500 | 16.0 | 45.4 |
| Ty Gibbs | 8200 | 20.0 | 46.4 |
| Bubba Wallace | 8000 | 30.0 | 46.35 |
| Brad Keselowski | 7900 | 5.0 | 17.0 |
| Carson Hocevar | 7700 | 12.0 | 41.25 |
| Chris Buescher | 7500 | 15.0 | 36.0 |
| Alex Bowman | 7300 | 18.0 | 37.0 |
| Austin Cindric | 7200 | 22.0 | 39.6 |
| Ross Chastain | 7100 | 12.0 | 36.6 |
| Ryan Preece | 7000 | 34.0 | 40.0 |
| Josh Berry | 6900 | 24.0 | 46.85 |
| Austin Dillon | 6800 | 4.0 | 20.0 |
| Daniel Suarez | 6700 | 22.0 | 34.35 |
| Erik Jones | 6600 | 4.0 | 21.0 |
| Shane Van Gisbergen | 6500 | 14.0 | 32.9 |
| Michael McDowell | 6400 | 4.0 | 18.0 |
| Zane Smith | 6300 | 9.0 | 33.25 |
| John H. Nemechek | 6200 | 5.0 | 19.0 |
| AJ Allmendinger | 6100 | 7.0 | 21.0 |
| Riley Herbst | 5900 | 18.0 | 28.0 |
| Todd Gilliland | 5800 | 22.0 | 31.8 |
| Connor Zilisch | 5700 | 3.0 | 17.0 |
| Austin Hill | 5600 | 4.0 | 12.0 |
| Ricky Stenhouse Jr | 5500 | 2.0 | 16.0 |
| Noah Gragson | 5300 | 2.0 | 15.0 |
| Ty Dillon | 5200 | 6.0 | 17.0 |
| Cole Custer | 5100 | 6.0 | 18.0 |
| Cody Ware | 5000 | 2.0 | 13.0 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Zane Smith — $6,300, 9% own, proj 33.2, ceiling 33.2
- Erik Jones — $6,600, 4% own, proj 21.0, ceiling 21.0
- AJ Allmendinger — $6,100, 7% own, proj 21.0, ceiling 21.0
- Austin Dillon — $6,800, 4% own, proj 20.0, ceiling 20.0
- John H. Nemechek — $6,200, 5% own, proj 19.0, ceiling 19.0
- Michael McDowell — $6,400, 4% own, proj 18.0, ceiling 18.0
- Cole Custer — $5,100, 6% own, proj 18.0, ceiling 18.0
- Brad Keselowski — $7,900, 5% own, proj 17.0, ceiling 17.0
- Ty Dillon — $5,200, 6% own, proj 17.0, ceiling 17.0
- Connor Zilisch — $5,700, 3% own, proj 17.0, ceiling 17.0
- Ricky Stenhouse Jr — $5,500, 2% own, proj 16.0, ceiling 16.0
- Noah Gragson — $5,300, 2% own, proj 15.0, ceiling 15.0

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Ryan Blaney + Christopher Bell** — 52.0% × 35.0% ≈ 18.2% of the field (~107 lineups of 588)
- **Ryan Blaney + Chase Elliott** — 52.0% × 35.0% ≈ 18.2% of the field (~107 lineups of 588)
- **Ryan Blaney + Ryan Preece** — 52.0% × 34.0% ≈ 17.7% of the field (~104 lineups of 588)
- **Ryan Blaney + William Byron** — 52.0% × 33.0% ≈ 17.2% of the field (~101 lineups of 588)
- **Ryan Blaney + Denny Hamlin** — 52.0% × 32.0% ≈ 16.6% of the field (~98 lineups of 588)
- **Ryan Blaney + Joey Logano** — 52.0% × 31.0% ≈ 16.1% of the field (~95 lineups of 588)

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
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/indianapolis_motor_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/iowa_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/nashville_superspeedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/naval_base_coronado.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/north_wilkesboro_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/pocono_raceway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/sonoma_raceway.md`

**Output target:** write the slate strategy to `data/slate_analysis/nascar.md`.
