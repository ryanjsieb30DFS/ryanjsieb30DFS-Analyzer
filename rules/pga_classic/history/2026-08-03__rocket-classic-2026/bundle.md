# Slate bundle — PGA Classic
_Generated 2026-07-29 20:43 · slug `pga_classic` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_classic.md`.

## Contests
- 2 contest(s), 25 total entries
  - **PGA $10K Eagle** (5-Max): field 2,378, my entries 5/5, prize multiple 0.84x
  - **PGA TOUR $35K mini-MAX [150 Entry Max]** (150-Max): field 83,234, my entries 20/150, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_**LARGE-FIELD CONTEST(S) DECLARED** (PGA TOUR $35K mini-MAX [150 Entry Max] (150-Max)) — the strategy MUST include the `## Field attack plan` section (see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **5-Max** (across your 2 past 5-Max contests): the field reliably crowds **Scottie Scheffler (in 2 of 2)**.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.139**, leverage **48.868%**, anchor-exposure **0.409**, unique **89.623%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 5 | 2/5 | 30.4 | 24.0 | 0.59 | ~30.4% own/slot |
| **youdacao** | 1 | 0/1 | 22.6 | 0.0 | 0.67 | little-to-no leverage, ~22.6% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 5.0 → 51.9 → 98.3 → 23.5 → 3.4
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 33% → 0% → 50% → 60%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `leverage_pct` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 1 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 2 of 2 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__ETR Golf Coffin List 7.30.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__ETR Golf Course Preview 7.30.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__ETR Golf DK Ownership Analysis 7.30.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__ETR Golf Large Field Breakdown 7.29.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__ETR Golf Model Proj. Inputs 7.30.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__ETR Golf Value Report 7.30.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-29__Establish-The-Green-Rocket-Classic-1.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR PGA — `DK PGA DFS Projections (15).csv` (147 players)
| name | salary | ownership | proj_points | ceiling |
| --- | --- | --- | --- | --- |
| Cameron Young | 10500 | 31.4 | 80.3 | 116.6 |
| Chris Gotterup | 9800 | 27.3 | 76.2 | 113.4 |
| Si Woo Kim | 9600 | 21.1 | 75.2 | 110.2 |
| Xander Schauffele | 10200 | 13.5 | 74.7 | 109.0 |
| Patrick Cantlay | 9100 | 21.4 | 72.3 | 108.0 |
| J.J. Spaun | 8700 | 23.4 | 71.5 | 104.7 |
| Wyndham Clark | 9300 | 20.3 | 71.5 | 108.0 |
| Ben Griffin | 8900 | 21.4 | 70.6 | 106.0 |
| Jackson Koivun | 9400 | 13.7 | 70.1 | 106.3 |
| Russell Henley | 9200 | 11.4 | 69.8 | 105.6 |
| Hideki Matsuyama | 9000 | 21.6 | 69.4 | 103.4 |
| Jake Knapp | 8800 | 23.4 | 68.8 | 107.5 |
| Ryan Gerard | 8600 | 18.6 | 68.3 | 105.0 |
| Rickie Fowler | 8100 | 11.2 | 65.2 | 98.7 |
| Michael Thorbjornsen | 8200 | 14.9 | 65.0 | 99.6 |
| Jacob Bridgeman | 7900 | 15.2 | 64.9 | 100.5 |
| Nicolai Hojgaard | 8300 | 11.6 | 64.4 | 101.0 |
| Akshay Bhatia | 8400 | 12.5 | 63.9 | 99.2 |
| Keegan Bradley | 7800 | 12.2 | 63.8 | 98.9 |
| Harris English | 8500 | 3.8 | 62.5 | 96.0 |
| Davis Thompson | 7700 | 14.6 | 61.5 | 94.2 |
| Corey Conners | 7500 | 12.9 | 61.3 | 96.3 |
| Ryo Hisatsune | 7600 | 10.3 | 61.0 | 94.2 |
| Doug Ghim | 7400 | 6.8 | 60.0 | 91.9 |
| Michael Kim | 7200 | 10.3 | 60.0 | 97.6 |
| Sungjae Im | 7000 | 12.3 | 59.9 | 95.7 |
| Mac Meissner | 7300 | 9.9 | 59.9 | 93.7 |
| Jordan L. Smith | 7200 | 12.3 | 59.8 | 92.1 |
| Rasmus Neergaard-Petersen | 7400 | 6.1 | 59.8 | 91.1 |
| Michael Brennan | 7900 | 9.3 | 59.8 | 95.7 |
| Jackson Suber | 7500 | 10.0 | 59.6 | 94.9 |
| Eric Cole | 7600 | 7.1 | 59.5 | 97.9 |
| Kevin Yu | 7200 | 5.9 | 58.5 | 91.5 |
| Matt Wallace | 7400 | 3.3 | 58.4 | 93.6 |
| Benjamin James | 7300 | 6.5 | 58.3 | 94.0 |
| Ben Kohles | 7300 | 8.5 | 58.3 | 90.9 |
| Max Greyserman | 7300 | 6.8 | 57.8 | 93.4 |
| Marco Penge | 7800 | 5.4 | 57.1 | 93.1 |
| Nick Taylor | 7200 | 2.5 | 57.1 | 92.6 |
| Emiliano Grillo | 7200 | 5.3 | 57.0 | 94.0 |
| Johnny Keefer | 7400 | 5.7 | 56.8 | 93.9 |
| Pierceson Coody | 7400 | 3.1 | 56.5 | 93.8 |
| Christiaan Bezuidenhout | 7300 | 2.2 | 56.4 | 87.9 |
| Aldrich Potgieter | 7300 | 6.7 | 56.4 | 93.4 |
| Andrew Novak | 7100 | 5.1 | 56.4 | 90.6 |
| Sam Stevens | 7200 | 3.5 | 56.3 | 92.3 |
| William Mouw | 6800 | 3.9 | 55.9 | 91.4 |
| Tony Finau | 7100 | 3.5 | 55.9 | 92.0 |
| Jordan Spieth | 7700 | 1.6 | 55.9 | 92.3 |
| Denny Mccarthy | 7500 | 4.8 | 55.6 | 86.1 |
| Zecheng Dou | 6900 | 2.6 | 55.3 | 89.1 |
| Lee Hodges | 6800 | 2.5 | 55.2 | 89.5 |
| Matthew McCarty | 7000 | 1.2 | 54.4 | 91.7 |
| Taylor Moore | 7000 | 0.9 | 54.2 | 87.6 |
| Max Mcgreevy | 6800 | 0.9 | 54.2 | 86.5 |
| Chris Kirk | 6900 | 3.1 | 54.1 | 88.0 |
| Ricky Castillo | 7100 | 1.7 | 54.0 | 87.9 |
| Sudarshan Yellamaraju | 7100 | 2.2 | 54.0 | 89.9 |
| Nicolas Echavarria | 6900 | 1.5 | 54.0 | 88.7 |
| John Parry | 7000 | 0.8 | 53.8 | 87.4 |
| Steven Fisk | 7000 | 0.5 | 53.8 | 87.0 |
| Kevin Roy | 6800 | 1.6 | 53.6 | 88.3 |
| Matti Schmid | 6800 | 1.9 | 53.4 | 91.5 |
| Zachary Bauchou | 6900 | 2.7 | 53.3 | 88.4 |
| Jesper Svensson | 7100 | 0.5 | 53.3 | 89.5 |
| Mackenzie Hughes | 7100 | 0.5 | 53.2 | 85.8 |
| Beau Hossler | 7200 | 0.6 | 53.2 | 85.1 |
| Taylor Pendrith | 7000 | 0.5 | 53.2 | 88.1 |
| Austin Smotherman | 6700 | 1.4 | 53.0 | 86.2 |
| Harry Hall | 7100 | 0.7 | 53.0 | 88.9 |
| Stephan Jaeger | 7100 | 1.0 | 53.0 | 90.5 |
| Keita Nakajima | 7000 | 0.1 | 52.9 | 88.7 |
| Zac Blair | 6800 | 2.4 | 52.4 | 86.6 |
| Rico Hoey | 6900 | 0.5 | 52.1 | 85.7 |
| Chandler Phillips | 6800 | 2.8 | 52.1 | 86.9 |
| Kris Ventura | 6900 | 0.3 | 52.0 | 87.6 |
| Seamus Power | 7300 | 0.6 | 51.8 | 86.7 |
| Lucas Glover | 6900 | 0.7 | 51.6 | 86.4 |
| Billy Horschel | 7000 | 3.2 | 51.6 | 85.3 |
| Rasmus Hojgaard | 6900 | 0.5 | 51.6 | 87.0 |
| Thorbjorn Olesen | 6700 | 0.1 | 50.4 | 86.4 |
| Patrick Fishburn | 6700 | 0.1 | 50.0 | 84.1 |
| Andrew Putnam | 6600 | 0.3 | 50.0 | 83.8 |
| Hao-Tong Li | 6700 | 0.3 | 49.7 | 85.4 |
| Patrick Rodgers | 6600 | 0.1 | 49.1 | 84.2 |
| A.J. Ewart | 6800 | 0.3 | 48.9 | 81.7 |
| Joel Dahmen | 6600 | 0.3 | 48.6 | 81.4 |
| Mark Hubbard | 6400 | 0.1 | 48.4 | 81.2 |
| Austin Eckroat | 6700 | 0.3 | 48.3 | 82.3 |
| Neal Shipley | 6700 | 0.3 | 48.2 | 82.7 |
| Adrien Dumont De Chassart | 6700 | 0.1 | 48.2 | 81.4 |
| Tom Hoge | 6700 | 0.3 | 48.0 | 82.1 |
| Karl Vilips | 6600 | 0.1 | 47.7 | 82.6 |
| Garrick Higgo | 6500 | 0.1 | 47.1 | 81.4 |
| Chandler Blanchet | 6500 | 0.1 | 47.0 | 79.1 |
| Takumi Kanaya | 6500 | 0.1 | 46.6 | 77.9 |
| Matthieu Pavon | 6400 | 0.0 | 46.3 | 80.0 |
| Erik Van Rooyen | 6500 | 0.1 | 45.5 | 78.8 |
| Chad Ramey | 6500 | 0.1 | 45.4 | 77.8 |
| Matt Kuchar | 6400 | 0.0 | 45.1 | 77.3 |
| Hayden Springer | 6500 | 0.0 | 45.1 | 78.1 |
| Pontus Nyholm | 6500 | 0.0 | 45.0 | 79.0 |
| Luke Clanton | 6500 | 0.1 | 45.0 | 77.6 |
| David Lipsky | 6400 | 0.0 | 44.8 | 77.7 |
| Adrien Saddier | 6300 | 0.0 | 44.4 | 77.3 |
| John VanDerLaan | 6300 | 0.0 | 44.2 | 77.7 |
| Lanto Griffin | 6300 | 0.0 | 44.0 | 76.7 |
| Brandt Snedeker | 6300 | 0.0 | 44.0 | 78.2 |
| Vince Whaley | 6400 | 0.1 | 44.0 | 74.6 |
| Davis Chatfield | 6600 | 0.3 | 43.8 | 73.8 |
| Trace Crowe | 6600 | 0.0 | 43.8 | 75.4 |
| Aaron Wise | 6400 | 0.1 | 43.6 | 76.8 |
| Hank Lebioda | 6500 | 0.0 | 43.4 | 76.2 |
| Stefano Mazzoli | 6400 | 0.0 | 43.4 | 79.6 |
| Nick Dunlap | 6400 | 0.0 | 42.8 | 76.2 |
| Dylan Wu | 6100 | 0.0 | 42.8 | 74.6 |
| Kevin Streelman | 6300 | 0.0 | 42.6 | 74.8 |
| Joe Highsmith | 6300 | 0.0 | 42.6 | 74.4 |
| Cameron Davis | 6600 | 0.3 | 42.5 | 76.3 |
| Ben Silverman | 6700 | 0.0 | 42.4 | 73.3 |
| Brice Garnett | 6200 | 0.0 | 41.7 | 72.7 |
| Webb Simpson | 6200 | 0.0 | 41.6 | 72.7 |
| Gordon Sargent | 6200 | 0.0 | 41.3 | 74.8 |
| Adam Schenk | 6000 | 0.0 | 40.9 | 73.3 |
| Justin Lower | 6200 | 0.0 | 40.6 | 72.1 |
| Davis Riley | 6200 | 0.0 | 40.6 | 74.5 |
| Jeffrey Kang | 6200 | 0.0 | 40.4 | 70.9 |
| Alejandro Tosti | 6300 | 0.0 | 40.0 | 71.4 |
| Adam Svensson | 6200 | 0.0 | 40.0 | 71.0 |
| Brian Campbell | 6100 | 0.0 | 39.6 | 71.3 |
| William Jennings | 6100 | 0.0 | 39.3 | 70.6 |
| Danny Walker | 6200 | 0.0 | 39.0 | 71.6 |
| Marcelo Rozo | 6100 | 0.0 | 37.9 | 70.6 |
| Peter Malnati | 6000 | 0.0 | 37.5 | 68.6 |
| Kensei Hirata | 6100 | 0.0 | 37.5 | 67.4 |
| Rafael Campos | 6000 | 0.0 | 35.3 | 64.9 |
| Christo Lamprecht | 6100 | 0.0 | 34.7 | 62.3 |
| Patton Kizzire | 6000 | 0.0 | 34.4 | 61.6 |
| Keenan Huskey | 6100 | 0.0 | 30.4 | 51.1 |
| Patrick Wilkes-Krier | 6000 | 0.0 | 28.8 | 47.4 |
| Brendon Todd | 6000 | 0.0 | 28.3 | 47.9 |
| Ryan Ruffels | 6100 | 0.0 | 27.2 | 43.1 |
| Brad Dalke | 6300 | 0.0 | 25.4 | 39.1 |
| Justin Quiban | 6000 | 0.0 | 24.7 | 38.8 |
| Joe Hooks | 6000 | 0.0 | 21.3 | 31.1 |
| Daniel Azallion | 6000 | 0.0 | 20.9 | 30.4 |
| Ryan Celano | 6100 | 0.0 | 13.5 | 20.4 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Eric Cole — $7,600, 7% own, proj 59.5, ceiling 97.9
- Harris English — $8,500, 4% own, proj 62.5, ceiling 96.0
- Michael Brennan — $7,900, 9% own, proj 59.8, ceiling 95.7
- Emiliano Grillo — $7,200, 5% own, proj 57.0, ceiling 94.0
- Benjamin James — $7,300, 6% own, proj 58.3, ceiling 94.0
- Johnny Keefer — $7,400, 6% own, proj 56.8, ceiling 93.9
- Pierceson Coody — $7,400, 3% own, proj 56.5, ceiling 93.8
- Mac Meissner — $7,300, 10% own, proj 59.9, ceiling 93.7
- Matt Wallace — $7,400, 3% own, proj 58.4, ceiling 93.6
- Aldrich Potgieter — $7,300, 7% own, proj 56.4, ceiling 93.4
- Max Greyserman — $7,300, 7% own, proj 57.8, ceiling 93.4
- Marco Penge — $7,800, 5% own, proj 57.1, ceiling 93.1

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Cameron Young + Chris Gotterup** — 31.4% × 27.3% ≈ 8.6% of the field (~7,158 lineups of 83,234)
- **Cameron Young + J.J. Spaun** — 31.4% × 23.4% ≈ 7.3% of the field (~6,076 lineups of 83,234)
- **Cameron Young + Jake Knapp** — 31.4% × 23.4% ≈ 7.3% of the field (~6,076 lineups of 83,234)
- **Cameron Young + Hideki Matsuyama** — 31.4% × 21.6% ≈ 6.8% of the field (~5,660 lineups of 83,234)
- **Cameron Young + Ben Griffin** — 31.4% × 21.4% ≈ 6.7% of the field (~5,577 lineups of 83,234)
- **Cameron Young + Patrick Cantlay** — 31.4% × 21.4% ≈ 6.7% of the field (~5,577 lineups of 83,234)

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
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/shinnecock_hills.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_deere_run.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_river_highlands.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_toronto_osprey_valley.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_twin_cities.md`

**Output target:** write the slate strategy to `data/slate_analysis/pga_classic.md`.
