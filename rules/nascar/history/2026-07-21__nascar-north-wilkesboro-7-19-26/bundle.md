# Slate bundle — NASCAR
_Generated 2026-07-19 15:34 · slug `nascar` · sport `nascar`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nascar.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NAS $15K Engine Block** (SE): field 1,470, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
  - **NAS $5K Engine Block** (SE): field 490, my entries 1/1, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **SE** (across your 2 past SE contests): the field reliably crowds **Zane Smith (in 2 of 2), AJ Allmendinger (in 2 of 2), Christopher Bell (in 2 of 2), Bubba Wallace (in 2 of 2), Noah Gragson (in 2 of 2), William Byron (in 2 of 2), Denny Hamlin (in 2 of 2), Tyler Reddick (in 2 of 2)**; recurring fish-traps: **AJ Allmendinger (in 2 of 2), Austin Hill (in 2 of 2), Bubba Wallace (in 2 of 2), William Byron (in 2 of 2), Denny Hamlin (in 2 of 2), Chase Briscoe (in 2 of 2)**; the field PAIRS **Denny Hamlin + Tyler Reddick (in 2 of 2), Christopher Bell + Zane Smith (in 2 of 2), Christopher Bell + Tyler Reddick (in 2 of 2), Tyler Reddick + Zane Smith (in 2 of 2), Christopher Bell + Denny Hamlin (in 2 of 2)** — a dupe-magnet stack; leverage lives in breaking it.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your nascar shark envelope:** own/slot **34.136**, leverage **5.855%**, anchor-exposure **0.655**, unique **99.345%**. You run: own/slot 28.73, leverage 2.39%, anchor 0.42 — that delta is the gap to close.

## Process trend — your last 4 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 4.0 → 0.3 → 27.1 → 56.9
- **Leverage capture** (slate-defining low-owned plays we rostered): 100% → 100% → 0% → 50%
- **Bust exposure** (top underperformers we rostered): 40% → — → — → —

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-19__DDD 7.19.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-19__DFR Image 1 7.19.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-19__DFR Image 2 7.19.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-19__DFR Image 3 7.19.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-19__DFR Image 4 7.19.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nascar/2026-07-19__DFR Image 5 7.19.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan NASCAR — `DailyFan-Projections-Sheet-NASCAR-DK-3-1.csv` (37 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Denny Hamlin | 11000 | 27.0 | 61.75 |
| Ryan Blaney | 10700 | 47.0 | 68.0 |
| Kyle Larson | 10500 | 38.0 | 64.0 |
| Christopher Bell | 10200 | 46.0 | 77.0 |
| William Byron | 9900 | 29.0 | 54.0 |
| Chase Elliott | 9700 | 16.0 | 46.3 |
| Joey Logano | 9500 | 24.0 | 54.25 |
| Tyler Reddick | 9200 | 8.0 | 34.4 |
| Chase Briscoe | 8900 | 37.0 | 53.05 |
| Carson Hocevar | 8700 | 9.0 | 23.0 |
| Ty Gibbs | 8500 | 22.0 | 44.75 |
| Chris Buescher | 8300 | 7.0 | 24.0 |
| Ross Chastain | 8100 | 6.0 | 28.75 |
| Bubba Wallace | 7900 | 36.0 | 48.15 |
| Ryan Preece | 7700 | 18.0 | 37.8 |
| Brad Keselowski | 7600 | 15.0 | 36.9 |
| Daniel Suarez | 7400 | 8.0 | 15.0 |
| Austin Cindric | 7200 | 18.0 | 40.7 |
| Josh Berry | 7100 | 24.0 | 42.35 |
| Alex Bowman | 7000 | 28.0 | 41.35 |
| Shane Van Gisbergen | 6800 | 7.0 | 25.0 |
| Erik Jones | 6600 | 5.0 | 15.0 |
| Zane Smith | 6500 | 15.0 | 34.0 |
| Michael McDowell | 6400 | 3.0 | 14.0 |
| Austin Dillon | 6300 | 4.0 | 23.0 |
| Austin Hill | 6100 | 13.0 | 23.0 |
| Connor Zilisch | 6000 | 16.0 | 30.0 |
| Riley Herbst | 5800 | 22.0 | 34.0 |
| Noah Gragson | 5700 | 11.0 | 27.0 |
| Todd Gilliland | 5600 | 6.0 | 23.0 |
| AJ Allmendinger | 5500 | 10.0 | 23.0 |
| John H. Nemechek | 5400 | 4.0 | 13.0 |
| Ricky Stenhouse Jr | 5200 | 8.0 | 20.0 |
| Cole Custer | 5100 | 4.0 | 16.0 |
| Ty Dillon | 5000 | 3.0 | 10.0 |
| Cody Ware | 4800 | 4.0 | 15.0 |
| Chad Finchum | 4500 | 2.0 | 14.0 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Tyler Reddick — $9,200, 8% own, proj 34.4, ceiling 34.4
- Ross Chastain — $8,100, 6% own, proj 28.8, ceiling 28.8
- Shane Van Gisbergen — $6,800, 7% own, proj 25.0, ceiling 25.0
- Chris Buescher — $8,300, 7% own, proj 24.0, ceiling 24.0
- Carson Hocevar — $8,700, 9% own, proj 23.0, ceiling 23.0
- Austin Dillon — $6,300, 4% own, proj 23.0, ceiling 23.0
- Todd Gilliland — $5,600, 6% own, proj 23.0, ceiling 23.0
- Ricky Stenhouse Jr — $5,200, 8% own, proj 20.0, ceiling 20.0
- Cole Custer — $5,100, 4% own, proj 16.0, ceiling 16.0
- Cody Ware — $4,800, 4% own, proj 15.0, ceiling 15.0
- Daniel Suarez — $7,400, 8% own, proj 15.0, ceiling 15.0
- Erik Jones — $6,600, 5% own, proj 15.0, ceiling 15.0

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Ryan Blaney + Christopher Bell** — 47.0% × 46.0% ≈ 21.6% of the field (~318 lineups of 1,470)
- **Ryan Blaney + Kyle Larson** — 47.0% × 38.0% ≈ 17.9% of the field (~263 lineups of 1,470)
- **Christopher Bell + Kyle Larson** — 46.0% × 38.0% ≈ 17.5% of the field (~257 lineups of 1,470)
- **Ryan Blaney + Chase Briscoe** — 47.0% × 37.0% ≈ 17.4% of the field (~256 lineups of 1,470)
- **Christopher Bell + Chase Briscoe** — 46.0% × 37.0% ≈ 17.0% of the field (~250 lineups of 1,470)
- **Ryan Blaney + Bubba Wallace** — 47.0% × 36.0% ≈ 16.9% of the field (~248 lineups of 1,470)

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
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/nashville_superspeedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/naval_base_coronado.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/north_wilkesboro_speedway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/pocono_raceway.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nascar/tracks/sonoma_raceway.md`

**Output target:** write the slate strategy to `data/slate_analysis/nascar.md`.
