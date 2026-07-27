# Slate bundle — NASCAR
_Generated 2026-07-26 12:12 · slug `nascar` · sport `nascar`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nascar.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NAS $5K Engine Block** (SE): field 490, my entries 1/1, prize multiple 0.85x
  - **NAS $15K Engine Block** (SE): field 1,470, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **NAS $5K Engine Block** (your 2 past logs of THIS contest): the field reliably crowds **Denny Hamlin (in 2 of 2), Christopher Bell (in 2 of 2)**; recurring fish-traps: **AJ Allmendinger (in 2 of 2), William Byron (in 2 of 2)**; recurring opponents: avgjo (in 2 of 2); winners trending sharper (-1.6 own/slot vs earlier).
- **SE** (across your 4 past SE contests): the field reliably crowds **Christopher Bell (in 4 of 4), Denny Hamlin (in 3 of 4), Bubba Wallace (in 3 of 4), Zane Smith (in 2 of 4), Noah Gragson (in 2 of 4), AJ Allmendinger (in 2 of 4), Tyler Reddick (in 2 of 4), William Byron (in 2 of 4)**; recurring fish-traps: **William Byron (in 4 of 4), AJ Allmendinger (in 3 of 4), Denny Hamlin (in 2 of 4), Bubba Wallace (in 2 of 4), Austin Hill (in 2 of 4), Chase Briscoe (in 2 of 4), Riley Herbst (in 2 of 4), Ryan Blaney (in 2 of 4)**; the field PAIRS **Denny Hamlin + Tyler Reddick (in 2 of 4), Christopher Bell + Zane Smith (in 2 of 4), Tyler Reddick + Zane Smith (in 2 of 4), Christopher Bell + Denny Hamlin (in 2 of 4), Christopher Bell + Tyler Reddick (in 2 of 4)** — a dupe-magnet stack; leverage lives in breaking it.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your nascar shark envelope:** own/slot **34.275**, leverage **5.367%**, anchor-exposure **0.65**, unique **99.4%**. You run: own/slot 28.73, leverage 2.39%, anchor 0.42 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 2 | 1/2 | 33.3 | 20.0 | 0.6 | ~33.3% own/slot |
| **vishy2773** | 1 | 0/1 | 33.8 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~33.8% own/slot |
| **JRSobeski** | 1 | 0/1 | 31.0 | 0.0 | 0.33 | fades the chalk anchors, little-to-no leverage, ~31.0% own/slot |
| **Hunter4ever89** | 1 | 0/1 | 40.8 | 0.0 | 0.67 | little-to-no leverage, ~40.8% own/slot |
| **totoroll33** | 1 | 0/1 | 40.0 | 0.0 | 1.0 | rides the chalk anchors, little-to-no leverage, ~40.0% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 4.0 → 0.3 → 27.1 → 56.9 → 7.4
- **Leverage capture** (slate-defining low-owned plays we rostered): 100% → 100% → 0% → 50% → 100%
- **Bust exposure** (top underperformers we rostered): 40% → — → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 2 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 1 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__DDD 7.26.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__DFR Rankings 7.26.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__image-35.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__image-36.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__image-37.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__image-38.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__image-39.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-26__image-40.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan NASCAR — `DailyFan-Projections-Sheet-NASCAR-DK-12-1.csv` (39 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Denny Hamlin | 11000 | 34.0 | 54.05 |
| Ryan Blaney | 10700 | 13.0 | 39.9 |
| Kyle Larson | 10500 | 27.0 | 52.55 |
| Tyler Reddick | 10200 | 20.0 | 46.35 |
| Christopher Bell | 10000 | 38.0 | 51.25 |
| William Byron | 9700 | 35.0 | 49.25 |
| Chase Elliott | 9500 | 36.0 | 46.9 |
| Chase Briscoe | 9200 | 10.0 | 39.0 |
| Bubba Wallace | 9000 | 41.0 | 46.0 |
| Ty Gibbs | 8800 | 13.0 | 39.8 |
| Joey Logano | 8700 | 11.0 | 36.0 |
| Chris Buescher | 8500 | 13.0 | 40.35 |
| Carson Hocevar | 8300 | 30.0 | 41.85 |
| Corey Heim | 8100 | 9.0 | 28.0 |
| Austin Cindric | 7900 | 40.0 | 40.0 |
| Brad Keselowski | 7700 | 8.0 | 33.0 |
| Shane Van Gisbergen | 7500 | 15.0 | 30.0 |
| Erik Jones | 7300 | 17.0 | 36.8 |
| Ross Chastain | 7100 | 13.0 | 33.9 |
| Alex Bowman | 7000 | 9.0 | 30.35 |
| Daniel Suarez | 6900 | 11.0 | 29.8 |
| Ryan Preece | 6700 | 44.0 | 39.0 |
| John H. Nemechek | 6600 | 17.0 | 35.8 |
| Riley Herbst | 6500 | 6.0 | 25.0 |
| Josh Berry | 6300 | 4.0 | 22.0 |
| Connor Zilisch | 6200 | 10.0 | 27.0 |
| Michael McDowell | 6100 | 4.0 | 19.0 |
| Zane Smith | 6000 | 19.0 | 29.35 |
| Todd Gilliland | 5900 | 15.0 | 30.0 |
| Austin Dillon | 5800 | 6.0 | 25.0 |
| AJ Allmendinger | 5600 | 5.0 | 20.0 |
| Austin Hill | 5500 | 7.0 | 26.0 |
| Noah Gragson | 5400 | 6.0 | 19.0 |
| Ricky Stenhouse Jr | 5300 | 4.0 | 22.0 |
| Cole Custer | 5100 | 2.0 | 17.0 |
| Ty Dillon | 5000 | 4.0 | 18.0 |
| Cody Ware | 4800 | 2.0 | 19.0 |
| Casey Mears | 4700 | 1.0 | 17.0 |
| Daniel Dye | 4500 | 1.0 | 16.0 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Brad Keselowski — $7,700, 8% own, proj 33.0, ceiling 33.0
- Alex Bowman — $7,000, 9% own, proj 30.4, ceiling 30.4
- Corey Heim — $8,100, 9% own, proj 28.0, ceiling 28.0
- Austin Hill — $5,500, 7% own, proj 26.0, ceiling 26.0
- Austin Dillon — $5,800, 6% own, proj 25.0, ceiling 25.0
- Riley Herbst — $6,500, 6% own, proj 25.0, ceiling 25.0
- Ricky Stenhouse Jr — $5,300, 4% own, proj 22.0, ceiling 22.0
- Josh Berry — $6,300, 4% own, proj 22.0, ceiling 22.0
- AJ Allmendinger — $5,600, 5% own, proj 20.0, ceiling 20.0
- Michael McDowell — $6,100, 4% own, proj 19.0, ceiling 19.0
- Noah Gragson — $5,400, 6% own, proj 19.0, ceiling 19.0
- Cody Ware — $4,800, 2% own, proj 19.0, ceiling 19.0

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Ryan Preece + Bubba Wallace** — 44.0% × 41.0% ≈ 18.0% of the field (~265 lineups of 1,470)
- **Ryan Preece + Austin Cindric** — 44.0% × 40.0% ≈ 17.6% of the field (~259 lineups of 1,470)
- **Ryan Preece + Christopher Bell** — 44.0% × 38.0% ≈ 16.7% of the field (~245 lineups of 1,470)
- **Bubba Wallace + Austin Cindric** — 41.0% × 40.0% ≈ 16.4% of the field (~241 lineups of 1,470)
- **Ryan Preece + Chase Elliott** — 44.0% × 36.0% ≈ 15.8% of the field (~232 lineups of 1,470)
- **Bubba Wallace + Christopher Bell** — 41.0% × 38.0% ≈ 15.6% of the field (~229 lineups of 1,470)

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
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/nashville_superspeedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/naval_base_coronado.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/north_wilkesboro_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/pocono_raceway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/sonoma_raceway.md`

**Output target:** write the slate strategy to `data/slate_analysis/nascar.md`.
