# Slate bundle — PGA RD4 Showdown
_Generated 2026-08-09 00:21 · slug `pga_rd4_sd` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_rd4_sd.md`.

## Contests
- 2 contest(s), 2 total entries
  - **PGA TOUR Showdown $4K Dogleg [Single Entry] (Round 4 TOUR)** (SE): field 141, my entries 1/1, payout **Flat**, prize multiple 0.86x
  - **PGA TOUR Showdown $4K Dogleg [Single Entry] (Round 4 TOUR)** (SE): field 141, my entries 1/1, prize multiple 0.86x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.316**, leverage **51.502%**, anchor-exposure **0.4**, unique **90.454%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 7 | 3/7 | 22.9 | 37.14 | 0.5 | ~22.9% own/slot |
| **PetrGibbons** | 1 | 0/1 | 15.2 | 100.0 | 0.67 | carries a sub-5% leverage piece in most lineups, ~15.2% own/slot |
| **youdacao** | 2 | 0/2 | 22.6 | 40.0 | 0.43 | ~22.6% own/slot |

## Process trend — your last 2 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 4.5 → 26.1
- **Leverage capture** (slate-defining low-owned plays we rostered): 0% → 100%
- **Bust exposure** (top underperformers we rostered): 60% → —
- **Own-strategy adherence:** fade calls violated per slate: 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 1 of 1 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_rd4_sd/2026-08-09__ETR PGA RD4 SD Article.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_rd4_sd/2026-08-09__PGA RD4 SD Update 8.10.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DK PGA RD4 SD — `DK PGA Round 4 Showdown Projections (11).csv` (81 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Tom Kim | 10400 | 41.7 | 57.09 |
| Alex Smalley | 8200 | 40.0 | 52.67 |
| Michael Brennan | 9400 | 39.6 | 55.72 |
| Beau Hossler | 7800 | 40.0 | 52.46 |
| Hideki Matsuyama | 10500 | 18.5 | 51.63 |
| Alex Noren | 8000 | 35.0 | 51.0 |
| Kevin Yu | 7600 | 21.5 | 48.1 |
| Davis Thompson | 9700 | 24.6 | 51.57 |
| Nicolas Echavarria | 6600 | 19.3 | 45.339999999999996 |
| Jordan L. Smith | 8800 | 19.3 | 48.56 |
| Justin Thomas | 9500 | 15.2 | 47.14 |
| Harry Hall | 6800 | 13.4 | 44.73 |
| Jackson Koivun | 10300 | 11.2 | 48.25 |
| Sungjae Im | 8500 | 11.1 | 44.67 |
| Cameron Young | 10900 | 9.6 | 44.470000000000006 |
| Michael Kim | 7900 | 7.1 | 42.370000000000005 |
| Matt Wallace | 7300 | 14.5 | 43.36 |
| Ben Kohles | 9000 | 9.0 | 45.07 |
| Eric Cole | 8100 | 7.8 | 42.93 |
| Bud Cauley | 8000 | 7.2 | 42.17 |
| Jordan Spieth | 7500 | 9.1 | 42.68 |
| Billy Horschel | 7500 | 9.5 | 43.37 |
| Benjamin James | 8700 | 10.5 | 45.010000000000005 |
| Brandt Snedeker | 6500 | 8.2 | 40.53 |
| Kris Ventura | 6800 | 5.3 | 39.77 |
| Keegan Bradley | 8400 | 5.7 | 41.36 |
| Jackson Suber | 7900 | 6.3 | 42.81 |
| Zachary Bauchou | 7400 | 8.8 | 42.769999999999996 |
| Doug Ghim | 9200 | 8.4 | 43.92 |
| Christiaan Bezuidenhout | 7300 | 6.5 | 41.27 |
| Lee Hodges | 6500 | 3.8 | 39.1 |
| Kevin Roy | 7100 | 7.1 | 42.199999999999996 |
| Sahith Theegala | 8600 | 7.1 | 44.84 |
| Chandler Phillips | 7100 | 5.3 | 41.39 |
| Aaron Rai | 9100 | 4.8 | 42.31 |
| John Parry | 6600 | 4.2 | 39.44 |
| Denny McCarthy | 7800 | 5.3 | 42.28 |
| Ricky Castillo | 7400 | 3.8 | 39.87 |
| Rico Hoey | 7600 | 5.5 | 41.77 |
| Andrew Novak | 7200 | 5.4 | 40.55 |
| Joel Dahmen | 7000 | 6.7 | 40.84 |
| Nick Taylor | 7200 | 2.8 | 38.51 |
| Matthew McCarty | 7300 | 3.8 | 39.2 |
| Patrick Fishburn | 6700 | 3.2 | 39.0 |
| Thorbjorn Olesen | 6400 | 3.4 | 38.45 |
| Keith Mitchell | 8300 | 2.4 | 39.76 |
| Neal Shipley | 6100 | 2.6 | 37.45 |
| Erik Van Rooyen | 6300 | 5.6 | 40.260000000000005 |
| Austin Smotherman | 6600 | 2.4 | 38.22 |
| Chris Kirk | 7400 | 2.6 | 38.16 |
| Alex Fitzpatrick | 9600 | 2.3 | 40.96 |
| Matti Schmid | 7700 | 1.4 | 38.81 |
| Andrew Putnam | 6700 | 2.4 | 37.79 |
| Austin Eckroat | 7000 | 2.3 | 38.72 |
| Webb Simpson | 6000 | 3.8 | 37.82 |
| Mackenzie Hughes | 6800 | 1.3 | 36.69 |
| Marco Penge | 6400 | 1.4 | 35.94 |
| Maverick McNealy | 9300 | 1.3 | 39.64 |
| Rasmus Hojgaard | 7200 | 1.0 | 36.68 |
| Taylor Pendrith | 7000 | 0.7 | 36.18 |
| Max Greyserman | 7700 | 0.7 | 36.99 |
| Tony Finau | 6700 | 1.2 | 36.11 |
| Brooks Koepka | 8900 | 0.8 | 38.4 |
| Tom Hoge | 7500 | 1.0 | 36.81 |
| Kevin Streelman | 6200 | 0.8 | 35.41 |
| Justin Lower | 6200 | 1.3 | 35.42 |
| Davis Chatfield | 6400 | 0.9 | 34.95 |
| Trace Crowe | 6300 | 0.3 | 34.480000000000004 |
| Joe Highsmith | 6500 | 0.6 | 35.32 |
| David Skinns | 7100 | 1.7 | 38.38 |
| Pontus Nyholm | 6100 | 0.2 | 33.71 |
| Adrien Saddier | 6900 | 0.1 | 34.21 |
| Peter Malnati | 6000 | 0.0 | 32.9 |
| Chad Ramey | 6900 | 0.3 | 34.86 |
| Hayden Springer | 6900 | 0.3 | 34.97 |
| Kensei Hirata | 6000 | 0.0 | 32.54 |
| Danny Walker | 6200 | 0.0 | 32.1 |
| Kihei Akina | 6100 | 0.0 | 31.67 |
| Rafael Campos | 6300 | 0.1 | 32.51 |
| Patton Kizzire | 6000 | 0.1 | 30.79 |
| Tyler Collet | 6200 | 0.0 | 27.88 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Ben Kohles — $9,000, 9% own, proj 45.1, ceiling 45.1
- Sahith Theegala — $8,600, 7% own, proj 44.8, ceiling 44.8
- Cameron Young — $10,900, 10% own, proj 44.5, ceiling 44.5
- Doug Ghim — $9,200, 8% own, proj 43.9, ceiling 43.9
- Billy Horschel — $7,500, 10% own, proj 43.4, ceiling 43.4
- Eric Cole — $8,100, 8% own, proj 42.9, ceiling 42.9
- Jackson Suber — $7,900, 6% own, proj 42.8, ceiling 42.8
- Zachary Bauchou — $7,400, 9% own, proj 42.8, ceiling 42.8
- Jordan Spieth — $7,500, 9% own, proj 42.7, ceiling 42.7
- Michael Kim — $7,900, 7% own, proj 42.4, ceiling 42.4
- Denny McCarthy — $7,800, 5% own, proj 42.3, ceiling 42.3
- Aaron Rai — $9,100, 5% own, proj 42.3, ceiling 42.3

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Tom Kim + Beau Hossler** — 41.7% × 40.0% ≈ 16.7% of the field (~24 lineups of 141)
- **Tom Kim + Alex Smalley** — 41.7% × 40.0% ≈ 16.7% of the field (~24 lineups of 141)
- **Tom Kim + Michael Brennan** — 41.7% × 39.6% ≈ 16.5% of the field (~23 lineups of 141)
- **Beau Hossler + Alex Smalley** — 40.0% × 40.0% ≈ 16.0% of the field (~23 lineups of 141)
- **Beau Hossler + Michael Brennan** — 40.0% × 39.6% ≈ 15.8% of the field (~22 lineups of 141)
- **Alex Smalley + Michael Brennan** — 40.0% × 39.6% ≈ 15.8% of the field (~22 lineups of 141)

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_rd4_sd/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_rd4_sd/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_rd4_sd/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_rd4_sd/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_rd4_sd/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_rd4_sd/results.jsonl` — cross-slate results ledger (process notes only)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/detroit_golf_club.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/muirfield_village.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/royal_birkdale.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/sedgefield_country_club.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/shinnecock_hills.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_deere_run.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_river_highlands.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_toronto_osprey_valley.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_twin_cities.md`

**Output target:** write the slate strategy to `data/slate_analysis/pga_rd4_sd.md`.
