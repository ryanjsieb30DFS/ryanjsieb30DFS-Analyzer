# Slate bundle — PGA Classic
_Generated 2026-07-15 23:00 · slug `pga_classic` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_classic.md`.

## Contests
- 1 contest(s), 5 total entries
  - **PGA $15K Eagle [5 Entry Max]** (5-Max): field 3,567, my entries 5/5, payout **Flat**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.19**, leverage **48.76%**, anchor-exposure **0.4**, unique **90.54%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.

## Process trend — your last 4 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 3.5 → 5.0 → 51.9 → 98.3
- **Leverage capture** (slate-defining low-owned plays we rostered): — → — → 33% → 0%
- **Bust exposure** (top underperformers we rostered): — → — → — → —

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR PGA Coffin List 7.16.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR PGA Course Fit 7.16.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR PGA Large Field Breakdown 7.16.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR PGA Models 7.16.2026.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR PGA Sim Analysis 7.16.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR PGA Value Report 7.16.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-07-15__ETR Top Plays Gold 7.16.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR PGA — `DK PGA DFS Projections (13).csv` (156 players)
| name | salary | ownership | proj_points | ceiling |
| --- | --- | --- | --- | --- |
| Scottie Scheffler | 13300 | 25.4 | 77.6 | 109.7 |
| Rory Mcilroy | 11900 | 24.3 | 70.7 | 106.6 |
| Tommy Fleetwood | 10500 | 26.0 | 69.0 | 98.2 |
| Matt Fitzpatrick | 10000 | 25.5 | 66.3 | 99.9 |
| Jon Rahm | 9700 | 19.4 | 64.3 | 101.2 |
| Robert Macintyre | 8000 | 20.7 | 63.6 | 95.0 |
| Xander Schauffele | 9800 | 13.8 | 62.0 | 93.5 |
| Viktor Hovland | 8300 | 20.0 | 60.8 | 98.3 |
| Ludvig Aberg | 9300 | 10.7 | 59.0 | 92.9 |
| Collin Morikawa | 8700 | 18.2 | 57.5 | 90.4 |
| Si Woo Kim | 6900 | 24.2 | 57.5 | 89.4 |
| Tyrrell Hatton | 8900 | 13.3 | 57.2 | 92.0 |
| Chris Gotterup | 8500 | 15.3 | 57.0 | 89.9 |
| Cameron Young | 9000 | 8.9 | 56.3 | 89.3 |
| Justin Rose | 9100 | 9.5 | 56.2 | 88.5 |
| Wyndham Clark | 8200 | 15.5 | 56.0 | 88.7 |
| Alex Fitzpatrick | 7400 | 11.9 | 55.8 | 86.8 |
| Russell Henley | 7700 | 14.1 | 55.6 | 88.6 |
| Shane Lowry | 7900 | 8.4 | 55.4 | 84.5 |
| Patrick Cantlay | 7000 | 14.2 | 54.5 | 87.7 |
| Aaron Rai | 7100 | 10.0 | 54.5 | 84.8 |
| Min Woo Lee | 6900 | 12.6 | 54.4 | 87.1 |
| Tom Kim | 6800 | 13.9 | 54.1 | 84.2 |
| Justin Thomas | 7500 | 11.9 | 54.0 | 85.6 |
| Sam Burns | 7800 | 15.7 | 54.0 | 84.8 |
| Joaquin Niemann | 7300 | 13.7 | 53.4 | 88.7 |
| Ben Griffin | 6800 | 8.1 | 52.9 | 83.4 |
| Harris English | 6700 | 5.3 | 52.6 | 83.6 |
| J.J. Spaun | 6700 | 7.2 | 52.1 | 82.2 |
| Kurt Kitayama | 6500 | 6.4 | 51.4 | 86.1 |
| Patrick Reed | 7000 | 10.7 | 51.4 | 82.4 |
| Rickie Fowler | 6500 | 4.7 | 51.4 | 80.4 |
| Nicolai Hojgaard | 6600 | 7.1 | 50.7 | 84.8 |
| Bryson Dechambeau | 8400 | 4.9 | 49.5 | 83.8 |
| Maverick Mcnealy | 6700 | 6.6 | 49.0 | 79.9 |
| Akshay Bhatia | 6600 | 5.4 | 48.7 | 80.1 |
| Keegan Bradley | 6500 | 2.9 | 48.6 | 79.0 |
| Alex Noren | 6400 | 4.5 | 48.5 | 79.7 |
| Brian Harman | 6600 | 3.8 | 48.5 | 79.8 |
| Kristoffer Reitan | 6500 | 3.7 | 48.5 | 81.2 |
| Victor Perez | 6400 | 5.0 | 48.4 | 77.7 |
| Adam Scott | 6500 | 4.8 | 48.3 | 80.6 |
| Ryan Gerard | 6400 | 3.9 | 48.0 | 80.2 |
| Corey Conners | 6800 | 4.1 | 47.6 | 78.9 |
| Hideki Matsuyama | 6900 | 6.4 | 47.5 | 76.8 |
| Michael Thorbjornsen | 6100 | 3.2 | 47.3 | 79.4 |
| Jordan Spieth | 7200 | 4.4 | 47.0 | 80.2 |
| Michael Kim | 5800 | 1.0 | 46.8 | 77.0 |
| Jordan L. Smith | 6100 | 2.8 | 46.5 | 75.5 |
| Matt Wallace | 6300 | 1.6 | 46.5 | 77.9 |
| Eugenio Lopez-Chacarra | 6700 | 1.7 | 46.4 | 77.1 |
| Ryan Fox | 6300 | 1.8 | 46.4 | 76.3 |
| J.T. Poston | 6100 | 2.0 | 46.3 | 80.8 |
| Bud Cauley | 6000 | 1.6 | 45.6 | 75.4 |
| Eric Cole | 6000 | 0.9 | 45.6 | 79.0 |
| Jacob Bridgeman | 6400 | 1.8 | 45.5 | 77.2 |
| Alex Smalley | 6000 | 1.1 | 45.4 | 75.9 |
| Jake Knapp | 6700 | 1.8 | 45.3 | 79.8 |
| Gary Woodland | 6300 | 1.4 | 45.3 | 78.4 |
| Nick Taylor | 5900 | 1.8 | 45.2 | 77.0 |
| Tom Mckibbin | 6000 | 1.4 | 44.9 | 72.9 |
| Max Homa | 6400 | 1.9 | 44.9 | 73.6 |
| Brooks Koepka | 7600 | 4.4 | 44.8 | 77.5 |
| Jason Day | 6400 | 1.6 | 44.7 | 76.8 |
| Keith Mitchell | 6100 | 2.2 | 44.7 | 75.5 |
| Thomas Detry | 6100 | 1.3 | 44.6 | 73.6 |
| Sahith Theegala | 6200 | 1.6 | 44.6 | 77.5 |
| Angel Ayora Fanegas | 6200 | 0.6 | 44.5 | 75.4 |
| Andrew Novak | 5900 | 0.5 | 44.4 | 74.1 |
| Sepp Straka | 6600 | 1.7 | 43.6 | 76.0 |
| Casey Jarvis | 6000 | 0.5 | 43.4 | 77.0 |
| Max Greyserman | 6000 | 0.5 | 43.4 | 75.0 |
| Sungjae Im | 6200 | 0.9 | 43.3 | 75.2 |
| Ryo Hisatsune | 6100 | 1.3 | 43.2 | 72.6 |
| Daniel Hillier | 5900 | 0.2 | 43.1 | 73.1 |
| Jackson Suber | 5700 | 0.8 | 43.1 | 74.3 |
| David Puig | 6500 | 1.2 | 43.0 | 77.0 |
| Johnny Keefer | 6000 | 1.0 | 43.0 | 73.0 |
| Harry Hall | 6300 | 1.0 | 43.0 | 73.5 |
| Matthew McCarty | 5600 | 0.6 | 42.7 | 75.1 |
| Hao-Tong Li | 6200 | 1.3 | 42.3 | 75.8 |
| Sam Stevens | 5700 | 0.7 | 42.1 | 73.8 |
| Pierceson Coody | 5900 | 0.5 | 42.0 | 73.6 |
| John Parry | 5800 | 0.6 | 42.0 | 71.6 |
| Cameron Smith | 6800 | 2.4 | 41.8 | 74.1 |
| Stewart Cink | 5500 | 0.6 | 41.7 | 73.4 |
| Andy Sullivan | 5500 | 0.3 | 41.6 | 70.7 |
| Michael Brennan | 5900 | 0.6 | 41.3 | 71.6 |
| Laurie Canter | 5600 | 0.4 | 41.1 | 71.4 |
| Marco Penge | 6700 | 0.5 | 41.0 | 73.8 |
| Nicolas Echavarria | 5500 | 0.6 | 40.8 | 71.7 |
| Lucas Herbert | 6100 | 0.4 | 40.8 | 73.9 |
| Daniel Berger | 6200 | 0.7 | 40.7 | 71.4 |
| Francesco Molinari | 5600 | 0.8 | 40.6 | 68.7 |
| Daniel Brown | 5600 | 0.5 | 40.5 | 73.0 |
| Keita Nakajima | 5400 | 1.0 | 40.2 | 72.1 |
| Hennie Du Plessis | 5700 | 0.3 | 40.0 | 70.2 |
| Jesper Svensson | 5700 | 0.5 | 40.0 | 73.0 |
| Scott Vincent | 5800 | 0.5 | 39.6 | 69.6 |
| Rasmus Hojgaard | 6300 | 0.8 | 39.4 | 70.7 |
| Bernd Wiesberger | 5800 | 0.3 | 39.4 | 71.6 |
| Rasmus Neergaard-Petersen | 6200 | 0.6 | 39.2 | 67.2 |
| Matthew Jordan | 5700 | 1.0 | 39.1 | 70.4 |
| Jayden Trey Schaper | 6200 | 0.4 | 39.0 | 66.4 |
| Kota Kaneko | 5400 | 0.4 | 38.4 | 68.4 |
| Sami Valimaki | 5700 | 0.2 | 38.0 | 67.6 |
| Aldrich Potgieter | 6200 | 0.2 | 37.7 | 69.9 |
| Billy Horschel | 5800 | 0.4 | 37.3 | 67.8 |
| Shaun Norris | 5500 | 0.2 | 37.0 | 69.0 |
| Joe Dean | 5600 | 0.3 | 36.5 | 65.4 |
| Dan Bradbury | 5400 | 0.1 | 35.7 | 64.9 |
| Antoine Rozner | 5500 | 0.3 | 35.4 | 66.2 |
| Adrien Saddier | 5300 | 0.1 | 35.2 | 64.0 |
| Martin Couvra | 5400 | 0.1 | 34.7 | 63.6 |
| Josele Ballester | 5600 | 0.1 | 34.7 | 64.1 |
| Kazuma Kobori | 5400 | 0.4 | 34.3 | 64.2 |
| Henrik Stenson | 5200 | 0.5 | 34.1 | 61.8 |
| Francesco Laporta | 5600 | 0.0 | 33.6 | 65.1 |
| Joakim Lagergren | 5300 | 0.0 | 31.8 | 60.4 |
| Padraig Harrington | 5500 | 0.4 | 31.6 | 60.0 |
| Michael Hollick | 5300 | 0.1 | 30.4 | 58.4 |
| Frederic Lacroix | 5800 | 0.1 | 30.4 | 59.0 |
| Sam Bairstow | 5200 | 0.1 | 30.2 | 59.8 |
| Travis Smyth | 5200 | 0.1 | 30.2 | 58.1 |
| James Nicholas | 5200 | 0.1 | 29.9 | 58.3 |
| MJ Daffue | 5400 | 0.1 | 29.4 | 59.0 |
| Matthew Southgate | 5300 | 0.3 | 29.2 | 56.1 |
| Alistair Docherty | 5500 | 0.2 | 29.1 | 56.9 |
| Ren Yonezawa | 5200 | 0.2 | 28.8 | 56.5 |
| Caleb Surratt | 5400 | 0.1 | 28.3 | 55.8 |
| Matthew Baldwin | 5200 | 0.2 | 28.0 | 54.1 |
| Kazuki Higa | 5200 | 0.1 | 27.9 | 54.2 |
| Darren Clarke | 5100 | 0.1 | 27.4 | 53.2 |
| Jeongwoo Ham | 5300 | 0.1 | 26.6 | 51.8 |
| Austen Truslow | 5100 | 0.1 | 26.5 | 52.0 |
| Peter Uihlein | 5600 | 0.1 | 26.3 | 50.4 |
| Ryutaro Nagano | 5100 | 0.1 | 26.0 | 50.8 |
| Tim Wiedemeyer | 5200 | 0.0 | 25.8 | 51.0 |
| Baard Bjoernevik Skogen | 5000 | 0.4 | 25.2 | 47.8 |
| Lev Grinberg | 5100 | 0.0 | 24.6 | 46.6 |
| Jack Mcdonald | 5100 | 0.2 | 24.2 | 46.3 |
| Stuart Grehan | 5100 | 0.0 | 24.0 | 44.5 |
| Naoyuki Kataoka | 5300 | 0.1 | 23.1 | 43.0 |
| Tiger Christensen | 5100 | 0.1 | 22.9 | 41.6 |
| Jack Buchanan | 5300 | 0.0 | 22.1 | 39.7 |
| Alejandro De Castro Piera | 5000 | 0.1 | 21.6 | 38.6 |
| Cameron John | 5200 | 0.0 | 21.6 | 38.6 |
| Mason Howell | 5100 | 0.1 | 21.3 | 39.7 |
| Marcus Plunkett | 5100 | 0.0 | 19.9 | 34.4 |
| Nevill Ruiter | 5000 | 0.0 | 19.5 | 33.5 |
| Jiho Yang | 5000 | 0.0 | 19.2 | 33.6 |
| Fifa Laopakdee | 5000 | 0.1 | 18.4 | 31.6 |
| David Duval | 5000 | 0.1 | 18.3 | 30.1 |
| Mateo Pulcini | 5000 | 0.1 | 18.1 | 30.8 |
| Thomas Sloman | 5000 | 0.0 | 17.1 | 27.8 |
| David Howard | 5000 | 0.1 | 13.7 | 22.0 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Cameron Young — $9,000, 9% own, proj 56.3, ceiling 89.3
- Justin Rose — $9,100, 10% own, proj 56.2, ceiling 88.5
- Kurt Kitayama — $6,500, 6% own, proj 51.4, ceiling 86.1
- Nicolai Hojgaard — $6,600, 7% own, proj 50.7, ceiling 84.8
- Shane Lowry — $7,900, 8% own, proj 55.4, ceiling 84.5
- Bryson Dechambeau — $8,400, 5% own, proj 49.5, ceiling 83.8
- Harris English — $6,700, 5% own, proj 52.6, ceiling 83.6
- Ben Griffin — $6,800, 8% own, proj 52.9, ceiling 83.4
- J.J. Spaun — $6,700, 7% own, proj 52.1, ceiling 82.2
- Kristoffer Reitan — $6,500, 4% own, proj 48.5, ceiling 81.2
- J.T. Poston — $6,100, 2% own, proj 46.3, ceiling 80.8
- Adam Scott — $6,500, 5% own, proj 48.3, ceiling 80.6

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Tommy Fleetwood + Matt Fitzpatrick** — 26.0% × 25.5% ≈ 6.6% of the field (~235 lineups of 3,567)
- **Tommy Fleetwood + Scottie Scheffler** — 26.0% × 25.4% ≈ 6.6% of the field (~235 lineups of 3,567)
- **Matt Fitzpatrick + Scottie Scheffler** — 25.5% × 25.4% ≈ 6.5% of the field (~232 lineups of 3,567)
- **Tommy Fleetwood + Rory Mcilroy** — 26.0% × 24.3% ≈ 6.3% of the field (~225 lineups of 3,567)
- **Tommy Fleetwood + Si Woo Kim** — 26.0% × 24.2% ≈ 6.3% of the field (~225 lineups of 3,567)
- **Matt Fitzpatrick + Rory Mcilroy** — 25.5% × 24.3% ≈ 6.2% of the field (~221 lineups of 3,567)

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

**Output target:** write the slate strategy to `data/slate_analysis/pga_classic.md`.
