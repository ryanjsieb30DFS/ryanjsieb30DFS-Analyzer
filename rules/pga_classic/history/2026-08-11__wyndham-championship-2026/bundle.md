# Slate bundle — PGA Classic
_Generated 2026-08-05 20:41 · slug `pga_classic` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_classic.md`.

## Contests
- 2 contest(s), 101 total entries
  - **PGA Tour $35K Albatross** (SE): field 3,431, my entries 1/1, prize multiple 0.85x
  - **PGA TOUR $30K mini-MAX [150 Entry Max]** (150-Max): field 71,343, my entries 100/150, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_**LARGE-FIELD CONTEST(S) DECLARED** (PGA TOUR $30K mini-MAX [150 Entry Max] (150-Max)) — the strategy MUST include the `## Field attack plan` section (see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.041**, leverage **49.482%**, anchor-exposure **0.403**, unique **90.056%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 6 | 2/6 | 30.4 | 26.67 | 0.53 | ~30.4% own/slot |
| **PetrGibbons** | 1 | 0/1 | 15.2 | 100.0 | 0.67 | carries a sub-5% leverage piece in most lineups, ~15.2% own/slot |
| **youdacao** | 2 | 0/2 | 22.6 | 40.0 | 0.43 | ~22.6% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 51.9 → 98.3 → 23.5 → 3.4 → 1.1
- **Leverage capture** (slate-defining low-owned plays we rostered): 33% → 0% → 50% → 60% → 100%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `leverage_pct` was your biggest structural gap vs the pros in 4 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 1 → 0 → 1 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 2 of 3 graded slates — the board's boundaries are suspect.
- **Grader validation:** lineups the pre-lock checks would flag finished median 62.7%ile (n=7) vs clean 39.1%ile (n=28) — the checks are earning their keep.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Coffin List 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Course Preview 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Large Field Breakdown 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Models 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Ownership Analysis 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Top Plays 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__ETR Golf Value Report 8.6.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-05__Establish-The-Green-Wyndham-Championship-1.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR PGA — `DK PGA DFS Projections (16).csv` (147 players)
| name | salary | ownership | proj_points | ceiling |
| --- | --- | --- | --- | --- |
| Cameron Young | 10400 | 44.6 | 90.4 | 128.1 |
| Jackson Koivun | 10100 | 20.2 | 80.9 | 117.9 |
| Hideki Matsuyama | 9500 | 24.6 | 80.8 | 119.5 |
| Aaron Rai | 8800 | 23.8 | 79.0 | 116.0 |
| Ryan Gerard | 9300 | 21.5 | 77.3 | 118.1 |
| Ben Griffin | 9100 | 19.1 | 76.2 | 114.5 |
| Justin Thomas | 9400 | 18.2 | 75.7 | 114.5 |
| Tom Kim | 9200 | 18.3 | 73.7 | 109.3 |
| Harris English | 8300 | 14.3 | 73.6 | 112.6 |
| Doug Ghim | 7800 | 16.0 | 70.4 | 105.3 |
| Keegan Bradley | 8900 | 9.1 | 70.2 | 109.4 |
| Ben Kohles | 7700 | 15.7 | 70.2 | 105.4 |
| Davis Thompson | 8400 | 12.7 | 70.0 | 106.4 |
| Sungjae Im | 7700 | 15.9 | 69.9 | 108.1 |
| Maverick Mcnealy | 9000 | 16.1 | 69.7 | 107.4 |
| Mac Meissner | 8100 | 13.1 | 69.5 | 106.6 |
| J.T. Poston | 7400 | 10.1 | 68.5 | 110.4 |
| Alex Fitzpatrick | 8700 | 14.3 | 68.5 | 109.0 |
| Jordan L. Smith | 7500 | 12.6 | 68.4 | 105.2 |
| Brian Harman | 8200 | 8.2 | 68.1 | 105.2 |
| Ryo Hisatsune | 7300 | 11.7 | 67.3 | 103.8 |
| Emiliano Grillo | 7300 | 6.6 | 66.8 | 106.8 |
| Rasmus Neergaard-Petersen | 7300 | 5.8 | 66.8 | 102.8 |
| Bud Cauley | 7400 | 11.1 | 66.7 | 104.5 |
| Nick Taylor | 7300 | 5.6 | 66.6 | 104.4 |
| Christiaan Bezuidenhout | 7500 | 7.0 | 66.6 | 100.3 |
| Michael Kim | 7300 | 9.0 | 66.5 | 108.3 |
| Blades Brown | 7800 | 11.9 | 66.2 | 101.0 |
| Matt Wallace | 7500 | 6.7 | 65.8 | 104.5 |
| Keith Mitchell | 7900 | 9.9 | 65.3 | 104.4 |
| Alex Noren | 7900 | 5.9 | 65.3 | 104.1 |
| Alex Smalley | 7600 | 6.4 | 65.3 | 104.4 |
| Matthew McCarty | 6900 | 4.5 | 63.7 | 103.8 |
| Denny Mccarthy | 7200 | 3.9 | 63.4 | 96.7 |
| Jordan Spieth | 8000 | 5.0 | 62.7 | 102.3 |
| Benjamin James | 7400 | 7.8 | 62.5 | 101.2 |
| Chris Kirk | 7400 | 4.6 | 62.2 | 99.3 |
| Zac Blair | 7200 | 3.8 | 62.2 | 100.1 |
| Ricky Castillo | 7100 | 3.7 | 62.0 | 99.6 |
| Nicolas Echavarria | 7000 | 2.9 | 61.8 | 101.3 |
| Jackson Suber | 7200 | 6.8 | 61.8 | 100.4 |
| Eric Cole | 7400 | 6.3 | 61.8 | 103.6 |
| Michael Brennan | 8600 | 4.6 | 61.5 | 101.8 |
| Marco Penge | 7200 | 1.8 | 61.0 | 101.6 |
| Kevin Yu | 7100 | 3.0 | 60.9 | 97.8 |
| Brooks Koepka | 8500 | 8.2 | 60.6 | 100.2 |
| Max Mcgreevy | 7000 | 2.5 | 60.5 | 98.5 |
| Kris Ventura | 6800 | 3.5 | 60.3 | 99.7 |
| Lee Hodges | 7000 | 2.7 | 59.8 | 97.3 |
| Sahith Theegala | 7300 | 2.7 | 59.8 | 99.3 |
| Johnny Keefer | 7200 | 2.8 | 59.7 | 100.0 |
| Kevin Roy | 7100 | 1.2 | 59.5 | 97.8 |
| Billy Horschel | 7100 | 4.4 | 59.4 | 97.9 |
| John Parry | 6700 | 1.3 | 59.3 | 96.6 |
| Andrew Novak | 6900 | 1.8 | 58.9 | 97.8 |
| William Mouw | 6800 | 2.1 | 58.8 | 98.5 |
| Andrew Putnam | 6700 | 2.6 | 58.6 | 96.7 |
| Beau Hossler | 7000 | 2.1 | 58.4 | 94.7 |
| Sepp Straka | 7300 | 2.6 | 58.3 | 98.1 |
| Chandler Phillips | 6600 | 0.9 | 57.6 | 96.8 |
| Lucas Glover | 6800 | 2.7 | 57.6 | 96.3 |
| Stephan Jaeger | 6900 | 1.4 | 57.6 | 99.5 |
| Max Greyserman | 7400 | 3.1 | 57.5 | 95.8 |
| Rasmus Hojgaard | 7600 | 2.7 | 57.4 | 97.4 |
| Sam Stevens | 6900 | 2.4 | 57.3 | 97.3 |
| Jason Day | 7200 | 1.4 | 57.1 | 95.9 |
| Rico Hoey | 7100 | 3.8 | 57.0 | 94.0 |
| Zachary Bauchou | 7000 | 3.0 | 56.6 | 95.0 |
| Zecheng Dou | 6700 | 0.8 | 56.5 | 93.7 |
| Pierceson Coody | 7200 | 2.3 | 56.5 | 96.3 |
| Joel Dahmen | 6500 | 1.6 | 56.5 | 93.3 |
| Harry Hall | 7000 | 1.4 | 56.0 | 95.2 |
| Mackenzie Hughes | 7000 | 1.0 | 56.0 | 92.8 |
| Chandler Blanchet | 6700 | 0.6 | 55.9 | 95.3 |
| Thorbjorn Olesen | 6900 | 1.0 | 55.8 | 95.1 |
| Brandt Snedeker | 6500 | 1.0 | 55.2 | 95.0 |
| Matti Schmid | 6800 | 1.4 | 55.2 | 96.8 |
| Austin Smotherman | 6600 | 0.8 | 55.1 | 94.1 |
| Seamus Power | 6800 | 0.9 | 55.0 | 94.6 |
| Steven Fisk | 6900 | 0.7 | 55.0 | 92.9 |
| Tony Finau | 7100 | 1.7 | 55.0 | 94.6 |
| Austin Eckroat | 7100 | 0.9 | 54.9 | 92.3 |
| Patrick Fishburn | 6700 | 0.9 | 54.8 | 94.3 |
| David Lipsky | 6500 | 0.6 | 54.6 | 92.0 |
| Tom Hoge | 6700 | 0.9 | 54.3 | 92.6 |
| Matt Kuchar | 6500 | 0.8 | 54.3 | 91.5 |
| Mark Hubbard | 6600 | 0.8 | 54.3 | 91.1 |
| Neal Shipley | 6700 | 0.4 | 53.7 | 91.8 |
| Davis Chatfield | 6300 | 1.8 | 53.7 | 87.6 |
| Jesper Svensson | 6800 | 0.3 | 53.3 | 93.5 |
| Aldrich Potgieter | 6800 | 0.5 | 53.3 | 93.5 |
| Taylor Pendrith | 7100 | 0.6 | 52.5 | 90.7 |
| Takumi Kanaya | 6500 | 0.4 | 52.4 | 88.3 |
| Luke Clanton | 6900 | 1.3 | 52.3 | 89.9 |
| Karl Vilips | 6600 | 0.3 | 51.6 | 90.6 |
| Hao-Tong Li | 6700 | 0.4 | 51.2 | 90.0 |
| A.J. Ewart | 6600 | 0.4 | 51.1 | 87.7 |
| Matthieu Pavon | 6400 | 0.3 | 51.0 | 89.4 |
| Patrick Rodgers | 6400 | 0.4 | 50.4 | 90.3 |
| Webb Simpson | 6600 | 0.5 | 50.0 | 86.2 |
| Hank Lebioda | 6300 | 0.1 | 49.6 | 86.8 |
| Brice Garnett | 6100 | 0.2 | 49.3 | 84.9 |
| Adrien Saddier | 6400 | 0.0 | 49.0 | 86.6 |
| Aaron Wise | 6500 | 0.6 | 49.0 | 86.8 |
| Erik Van Rooyen | 6300 | 0.5 | 48.8 | 86.4 |
| Adrien Dumont De Chassart | 6800 | 0.1 | 48.8 | 86.0 |
| Brian Campbell | 6200 | 0.7 | 48.6 | 86.5 |
| Justin Lower | 6400 | 0.1 | 48.4 | 85.4 |
| Troy Merritt | 0 | 0.0 | 48.0 | 86.3 |
| Ben Silverman | 6300 | 0.1 | 47.4 | 82.3 |
| Davis Riley | 6700 | 0.7 | 47.3 | 86.5 |
| Kevin Streelman | 6200 | 0.1 | 46.9 | 83.2 |
| Joe Highsmith | 6200 | 0.1 | 46.8 | 83.4 |
| Lanto Griffin | 6400 | 0.1 | 46.8 | 83.6 |
| John VanDerLaan | 6200 | 0.0 | 46.5 | 83.7 |
| Trace Crowe | 6300 | 0.3 | 45.6 | 82.2 |
| Chad Ramey | 6400 | 0.1 | 45.6 | 81.4 |
| Pontus Nyholm | 6300 | 0.0 | 45.6 | 83.4 |
| Hayden Springer | 6200 | 0.1 | 45.4 | 82.0 |
| Gordon Sargent | 6200 | 0.1 | 45.4 | 82.9 |
| Stefano Mazzoli | 6100 | 0.1 | 45.3 | 84.7 |
| Adam Svensson | 6400 | 0.2 | 45.2 | 80.5 |
| Dylan Wu | 6200 | 0.1 | 44.8 | 80.2 |
| David Skinns | 6500 | 0.0 | 44.3 | 80.7 |
| Cameron Davis | 6100 | 0.3 | 43.2 | 80.0 |
| Jimmy Stanger | 6100 | 0.0 | 43.1 | 79.4 |
| Vince Whaley | 6400 | 0.4 | 42.8 | 76.9 |
| Nick Dunlap | 6300 | 0.1 | 42.6 | 79.3 |
| Adam Schenk | 6100 | 0.0 | 42.6 | 78.4 |
| C.T. Pan | 6300 | 0.3 | 42.6 | 78.5 |
| Kensei Hirata | 6100 | 0.0 | 42.3 | 77.3 |
| Peter Malnati | 6100 | 0.1 | 42.2 | 79.0 |
| Marcelo Rozo | 6000 | 0.0 | 41.5 | 78.9 |
| Jeffrey Kang | 6200 | 0.0 | 41.2 | 75.6 |
| Luke List | 6200 | 0.0 | 40.9 | 74.9 |
| Danny Walker | 6100 | 0.0 | 39.9 | 75.2 |
| Kihei Akina | 6500 | 0.1 | 39.8 | 74.9 |
| Camilo Villegas | 6100 | 0.0 | 39.2 | 72.1 |
| Alejandro Tosti | 6000 | 0.0 | 39.0 | 73.1 |
| Rafael Campos | 6000 | 0.0 | 37.4 | 70.0 |
| Patton Kizzire | 6000 | 0.0 | 36.4 | 65.6 |
| Christo Lamprecht | 6000 | 0.0 | 33.6 | 57.5 |
| William Mcgirt | 6000 | 0.0 | 31.6 | 51.5 |
| Keenan Huskey | 6000 | 0.0 | 31.2 | 52.0 |
| Tyler Collet | 6000 | 0.0 | 28.6 | 44.8 |
| Lorenzo Rodriguez | 6000 | 0.0 | 25.7 | 37.6 |
| Cooper Hrabak | 6000 | 0.0 | 22.4 | 32.5 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Keegan Bradley — $8,900, 9% own, proj 70.2, ceiling 109.4
- Michael Kim — $7,300, 9% own, proj 66.5, ceiling 108.3
- Emiliano Grillo — $7,300, 7% own, proj 66.8, ceiling 106.8
- Brian Harman — $8,200, 8% own, proj 68.1, ceiling 105.2
- Matt Wallace — $7,500, 7% own, proj 65.8, ceiling 104.5
- Keith Mitchell — $7,900, 10% own, proj 65.3, ceiling 104.4
- Alex Smalley — $7,600, 6% own, proj 65.3, ceiling 104.4
- Nick Taylor — $7,300, 6% own, proj 66.6, ceiling 104.4
- Alex Noren — $7,900, 6% own, proj 65.3, ceiling 104.1
- Matthew McCarty — $6,900, 4% own, proj 63.7, ceiling 103.8
- Eric Cole — $7,400, 6% own, proj 61.8, ceiling 103.6
- Rasmus Neergaard-Petersen — $7,300, 6% own, proj 66.8, ceiling 102.8

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Cameron Young + Hideki Matsuyama** — 44.6% × 24.6% ≈ 11.0% of the field (~7,848 lineups of 71,343)
- **Cameron Young + Aaron Rai** — 44.6% × 23.8% ≈ 10.6% of the field (~7,562 lineups of 71,343)
- **Cameron Young + Ryan Gerard** — 44.6% × 21.5% ≈ 9.6% of the field (~6,849 lineups of 71,343)
- **Cameron Young + Jackson Koivun** — 44.6% × 20.2% ≈ 9.0% of the field (~6,421 lineups of 71,343)
- **Cameron Young + Ben Griffin** — 44.6% × 19.1% ≈ 8.5% of the field (~6,064 lineups of 71,343)
- **Cameron Young + Tom Kim** — 44.6% × 18.3% ≈ 8.2% of the field (~5,850 lineups of 71,343)

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/results.jsonl` — cross-slate results ledger (process notes only)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/detroit_golf_club.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/muirfield_village.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/royal_birkdale.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/sedgefield_country_club.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/shinnecock_hills.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_deere_run.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_river_highlands.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_toronto_osprey_valley.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_twin_cities.md`

**Output target:** write the slate strategy to `data/slate_analysis/pga_classic.md`.
