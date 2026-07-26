# Slate bundle — PGA Classic
_Generated 2026-07-22 21:08 · slug `pga_classic` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_classic.md`.

## Contests
- 1 contest(s), 4 total entries
  - **PGA Tour $8K Eagle** (5-Max): field 1,902, my entries 4/5, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.368**, leverage **47.453%**, anchor-exposure **0.409**, unique **89.152%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 2 | 1/2 | 33.3 | 20.0 | 0.6 | ~33.3% own/slot |
| **youdacao** | 1 | 0/1 | 22.6 | 0.0 | 0.67 | little-to-no leverage, ~22.6% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 3.5 → 5.0 → 51.9 → 98.3 → 23.5
- **Leverage capture** (slate-defining low-owned plays we rostered): — → — → 33% → 0% → 50%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `leverage_pct` was your biggest structural gap vs the pros in 2 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 1 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 1 of 1 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__ETR Golf Course Preview 7.23.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__ETR Golf Large Field 7.23.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__ETR Golf Leverage 1 - 7.23.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__ETR Golf Leverage 2 - 7.23.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__ETR Golf Models 7.23.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__ETR Golf Value Report 7.23.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-22__Establish-The-Green-3M-Open-1.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR PGA — `DK PGA DFS Projections (14).csv` (144 players)
| name | salary | ownership | proj_points | ceiling |
| --- | --- | --- | --- | --- |
| Scottie Scheffler | 14900 | 25.2 | 105.6 | 140.0 |
| Maverick Mcnealy | 9900 | 23.6 | 78.0 | 114.3 |
| Kurt Kitayama | 9800 | 23.3 | 77.6 | 117.6 |
| Tom Kim | 9300 | 22.4 | 75.3 | 110.4 |
| Hideki Matsuyama | 9700 | 19.8 | 74.8 | 109.8 |
| Jackson Koivun | 9200 | 13.6 | 70.7 | 106.8 |
| Corey Conners | 8700 | 16.2 | 70.2 | 107.3 |
| Keith Mitchell | 9500 | 14.5 | 69.6 | 105.9 |
| Doug Ghim | 9000 | 10.7 | 68.9 | 102.0 |
| Ben Kohles | 7300 | 19.2 | 68.7 | 101.0 |
| Jordan L. Smith | 8300 | 12.3 | 68.6 | 103.7 |
| Sungjae Im | 8500 | 13.6 | 68.4 | 105.9 |
| Pierceson Coody | 9100 | 8.6 | 67.6 | 104.8 |
| Christiaan Bezuidenhout | 7900 | 9.7 | 67.2 | 100.3 |
| Sam Stevens | 8400 | 10.8 | 67.1 | 104.2 |
| Mac Meissner | 8100 | 13.7 | 66.8 | 102.4 |
| Jackson Suber | 8900 | 12.7 | 66.8 | 103.0 |
| Benjamin James | 8000 | 13.6 | 66.8 | 104.4 |
| Jake Knapp | 9400 | 11.1 | 66.2 | 106.7 |
| Brian Harman | 7400 | 11.9 | 66.1 | 102.9 |
| Max Homa | 8600 | 11.3 | 65.7 | 99.1 |
| Casey Jarvis | 7300 | 13.8 | 65.7 | 106.5 |
| Michael Kim | 7200 | 9.4 | 65.6 | 102.1 |
| Gary Woodland | 8800 | 5.3 | 65.5 | 105.2 |
| Johnny Keefer | 7800 | 9.7 | 65.2 | 101.6 |
| Rasmus Neergaard-Petersen | 7700 | 7.7 | 64.8 | 97.5 |
| Max Mcgreevy | 7100 | 10.5 | 64.3 | 98.1 |
| Max Greyserman | 7700 | 7.7 | 63.5 | 101.7 |
| Tony Finau | 8200 | 7.6 | 63.1 | 101.5 |
| Michael Brennan | 7800 | 8.9 | 62.7 | 99.6 |
| Zac Blair | 6900 | 6.9 | 62.6 | 98.7 |
| Kevin Yu | 7400 | 4.3 | 62.5 | 97.4 |
| Emiliano Grillo | 7300 | 9.3 | 62.2 | 101.2 |
| William Mouw | 7500 | 7.6 | 61.5 | 98.3 |
| Keita Nakajima | 7200 | 4.3 | 61.4 | 99.0 |
| Davis Thompson | 7600 | 4.2 | 61.4 | 95.6 |
| Ricky Castillo | 7300 | 6.5 | 61.3 | 96.9 |
| Lee Hodges | 7200 | 4.9 | 61.2 | 97.9 |
| John Parry | 7300 | 3.2 | 61.2 | 97.3 |
| Sudarshan Yellamaraju | 7900 | 5.3 | 61.0 | 99.6 |
| Andrew Putnam | 7000 | 6.5 | 61.0 | 98.1 |
| Taylor Pendrith | 7400 | 2.8 | 60.4 | 97.7 |
| Mackenzie Hughes | 7200 | 4.5 | 60.3 | 95.4 |
| Aldrich Potgieter | 7400 | 3.3 | 60.1 | 98.4 |
| Rico Hoey | 7200 | 7.9 | 60.0 | 94.1 |
| Lucas Glover | 7100 | 5.6 | 59.8 | 97.1 |
| Matti Schmid | 7100 | 3.7 | 59.8 | 97.4 |
| Zachary Bauchou | 7100 | 6.4 | 59.7 | 96.5 |
| Denny Mccarthy | 7100 | 3.6 | 59.4 | 90.8 |
| Beau Hossler | 7300 | 6.4 | 59.2 | 91.9 |
| Steven Fisk | 7500 | 2.8 | 59.1 | 93.6 |
| Austin Smotherman | 7000 | 2.0 | 58.8 | 94.0 |
| Jesper Svensson | 7200 | 3.1 | 58.7 | 97.7 |
| Stephan Jaeger | 7400 | 2.9 | 58.6 | 99.1 |
| Takumi Kanaya | 6700 | 3.1 | 58.6 | 91.2 |
| Seamus Power | 7000 | 2.6 | 58.4 | 94.9 |
| Tom Hoge | 6900 | 2.3 | 58.2 | 94.8 |
| Austin Eckroat | 6900 | 2.2 | 57.8 | 95.3 |
| Thorbjorn Olesen | 7100 | 2.1 | 57.8 | 96.0 |
| Kevin Roy | 6800 | 2.8 | 57.6 | 94.6 |
| Taylor Moore | 7300 | 2.8 | 57.5 | 91.9 |
| Joel Dahmen | 6600 | 3.3 | 57.1 | 93.4 |
| Brandt Snedeker | 6700 | 2.4 | 57.0 | 95.6 |
| Hao-Tong Li | 7100 | 1.1 | 57.0 | 95.6 |
| Billy Horschel | 7000 | 1.7 | 56.7 | 92.1 |
| Preston Stout | 7200 | 2.5 | 56.4 | 90.0 |
| Rasmus Hojgaard | 7500 | 3.1 | 56.4 | 95.0 |
| Matt Kuchar | 7000 | 1.8 | 56.3 | 90.5 |
| Kris Ventura | 6900 | 2.1 | 56.2 | 93.9 |
| Chris Kirk | 7000 | 1.5 | 56.1 | 92.6 |
| Zecheng Dou | 7000 | 1.0 | 55.8 | 91.4 |
| Brice Garnett | 6300 | 3.3 | 55.5 | 89.9 |
| A.J. Ewart | 7100 | 1.6 | 54.7 | 89.1 |
| David Lipsky | 6700 | 2.0 | 54.6 | 90.3 |
| Garrick Higgo | 6900 | 0.4 | 53.9 | 90.8 |
| Karl Vilips | 6800 | 1.4 | 53.8 | 91.8 |
| Chandler Phillips | 6700 | 0.5 | 53.7 | 91.2 |
| Aaron Wise | 6600 | 4.2 | 53.4 | 89.1 |
| Patrick Fishburn | 6900 | 0.7 | 53.1 | 88.8 |
| Paul Peterson | 6400 | 1.1 | 53.1 | 89.2 |
| Davis Chatfield | 6200 | 3.5 | 53.0 | 86.1 |
| Chad Ramey | 6800 | 0.8 | 52.6 | 87.5 |
| Patrick Rodgers | 7000 | 0.9 | 52.2 | 88.6 |
| Lanto Griffin | 6500 | 0.8 | 51.9 | 87.8 |
| Adrien Dumont De Chassart | 7200 | 0.8 | 51.8 | 87.9 |
| Matthieu Pavon | 6800 | 0.8 | 51.8 | 88.3 |
| David Skinns | 6700 | 0.4 | 51.7 | 87.7 |
| Nick Dunlap | 6700 | 0.5 | 51.5 | 88.1 |
| Tyler Duncan | 6200 | 0.9 | 51.4 | 86.5 |
| Adam Svensson | 6300 | 0.8 | 51.4 | 85.9 |
| Neal Shipley | 6800 | 0.7 | 50.8 | 87.0 |
| Stefano Mazzoli | 6500 | 0.9 | 50.6 | 87.9 |
| Mark Hubbard | 6600 | 0.6 | 50.5 | 86.1 |
| Erik Van Rooyen | 6700 | 1.6 | 50.3 | 85.7 |
| Ben Silverman | 6400 | 0.9 | 50.3 | 83.6 |
| Chandler Blanchet | 6500 | 0.4 | 50.1 | 85.5 |
| Luke Clanton | 6800 | 0.6 | 50.1 | 85.5 |
| Joe Highsmith | 6400 | 0.3 | 50.0 | 85.3 |
| Hank Lebioda | 6300 | 0.3 | 50.0 | 84.2 |
| Trace Crowe | 6800 | 0.6 | 49.4 | 83.8 |
| Adam Hadwin | 6500 | 0.7 | 49.3 | 83.8 |
| Pontus Nyholm | 6800 | 0.2 | 49.2 | 86.0 |
| Harry Higgs | 6600 | 0.4 | 48.9 | 85.4 |
| Dylan Wu | 6300 | 0.1 | 48.8 | 82.8 |
| Justin Lower | 6400 | 0.2 | 48.8 | 84.4 |
| Fabian Gomez | 6300 | 0.5 | 48.6 | 82.2 |
| Brian Campbell | 6200 | 0.3 | 48.1 | 84.0 |
| Hayden Springer | 6700 | 0.3 | 47.8 | 83.9 |
| Kevin Streelman | 6300 | 0.3 | 47.8 | 82.5 |
| Cameron Davis | 6400 | 2.1 | 47.7 | 84.3 |
| Vince Whaley | 6500 | 0.7 | 47.6 | 80.6 |
| Troy Merritt | 6100 | 0.6 | 47.4 | 84.0 |
| John VanDerLaan | 6300 | 0.2 | 47.3 | 84.6 |
| Jimmy Stanger | 6500 | 0.1 | 47.2 | 83.2 |
| Kensei Hirata | 6200 | 0.1 | 47.0 | 80.4 |
| Ryder Cowan | 6900 | 0.9 | 46.9 | 81.4 |
| Nick Hardy | 6400 | 0.1 | 46.3 | 81.4 |
| Will Gordon | 6600 | 0.7 | 46.2 | 79.8 |
| Cameron Champ | 6600 | 1.3 | 46.2 | 80.4 |
| Davis Riley | 6200 | 0.3 | 45.9 | 83.5 |
| Peter Malnati | 6200 | 0.2 | 45.4 | 80.7 |
| Luke List | 6500 | 0.2 | 45.0 | 79.2 |
| Adam Schenk | 6100 | 0.1 | 45.0 | 80.3 |
| Gordon Sargent | 6900 | 0.6 | 45.0 | 81.4 |
| Alejandro Tosti | 6400 | 0.1 | 44.6 | 80.1 |
| Jeffrey Kang | 6200 | 0.1 | 44.3 | 77.1 |
| Danny Walker | 6100 | 0.1 | 43.4 | 79.4 |
| Ben Martin | 6100 | 0.1 | 43.1 | 76.2 |
| Marcelo Rozo | 6000 | 0.0 | 42.8 | 79.2 |
| Patton Kizzire | 6000 | 0.1 | 42.8 | 76.9 |
| Camilo Villegas | 6100 | 0.1 | 42.5 | 75.9 |
| Jeremy Paul | 6000 | 0.1 | 42.1 | 76.9 |
| Rafael Campos | 6000 | 0.1 | 41.0 | 75.0 |
| Christo Lamprecht | 6100 | 0.1 | 38.4 | 71.0 |
| Nicholas Lindheim | 6100 | 0.1 | 36.8 | 67.4 |
| Charley Hoffman | 6200 | 0.1 | 36.0 | 65.6 |
| Ryan Brehm | 6200 | 0.0 | 32.9 | 55.6 |
| Sihan Sandhu | 6000 | 0.2 | 30.5 | 49.2 |
| Brannon Fahrny | 6100 | 0.0 | 30.3 | 48.0 |
| Cooper Schultz | 6100 | 0.0 | 29.3 | 45.6 |
| Griffin Wood | 6000 | 0.0 | 28.1 | 42.9 |
| Thomas Campbell | 6000 | 0.2 | 26.9 | 43.9 |
| Jeevan Sihota | 6000 | 0.0 | 23.2 | 34.4 |
| Muzzy Donohue | 6000 | 0.1 | 20.3 | 28.7 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Gary Woodland — $8,800, 5% own, proj 65.5, ceiling 105.2
- Pierceson Coody — $9,100, 9% own, proj 67.6, ceiling 104.8
- Michael Kim — $7,200, 9% own, proj 65.6, ceiling 102.1
- Max Greyserman — $7,700, 8% own, proj 63.5, ceiling 101.7
- Johnny Keefer — $7,800, 10% own, proj 65.2, ceiling 101.6
- Tony Finau — $8,200, 8% own, proj 63.1, ceiling 101.5
- Emiliano Grillo — $7,300, 9% own, proj 62.2, ceiling 101.2
- Christiaan Bezuidenhout — $7,900, 10% own, proj 67.2, ceiling 100.3
- Sudarshan Yellamaraju — $7,900, 5% own, proj 61.0, ceiling 99.6
- Michael Brennan — $7,800, 9% own, proj 62.7, ceiling 99.6
- Stephan Jaeger — $7,400, 3% own, proj 58.6, ceiling 99.1
- Keita Nakajima — $7,200, 4% own, proj 61.4, ceiling 99.0

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Scottie Scheffler + Maverick Mcnealy** — 25.2% × 23.6% ≈ 5.9% of the field (~112 lineups of 1,902)
- **Scottie Scheffler + Kurt Kitayama** — 25.2% × 23.3% ≈ 5.9% of the field (~112 lineups of 1,902)
- **Scottie Scheffler + Tom Kim** — 25.2% × 22.4% ≈ 5.6% of the field (~107 lineups of 1,902)
- **Maverick Mcnealy + Kurt Kitayama** — 23.6% × 23.3% ≈ 5.5% of the field (~105 lineups of 1,902)
- **Maverick Mcnealy + Tom Kim** — 23.6% × 22.4% ≈ 5.3% of the field (~101 lineups of 1,902)
- **Kurt Kitayama + Tom Kim** — 23.3% × 22.4% ≈ 5.2% of the field (~99 lineups of 1,902)

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/results.jsonl` — cross-slate results ledger (process notes only)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/muirfield_village.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/royal_birkdale.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/shinnecock_hills.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_deere_run.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_river_highlands.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_toronto_osprey_valley.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_twin_cities.md`

**Output target:** write the slate strategy to `data/slate_analysis/pga_classic.md`.
