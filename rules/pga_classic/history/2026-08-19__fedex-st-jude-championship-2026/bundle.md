# Slate bundle — PGA Classic
_Generated 2026-08-12 22:23 · slug `pga_classic` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_classic.md`.

## Contests
- 1 contest(s), 2 total entries
  - **PGA TOUR $12K Scramble [5 Entry Max]** (5-Max): field 705, my entries 2/5, payout **Top-heavy**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.677**, leverage **49.539%**, anchor-exposure **0.408**, unique **91.161%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 11 | 4/11 | 27.8 | 32.73 | 0.5 | ~27.8% own/slot |
| **PetrGibbons** | 1 | 0/1 | 15.2 | 100.0 | 0.67 | carries a sub-5% leverage piece in most lineups, ~15.2% own/slot |
| **youdacao** | 3 | 0/3 | 17.6 | 26.67 | 0.4 | fades the chalk anchors, ~17.6% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 98.3 → 23.5 → 3.4 → 1.1 → 14.0
- **Leverage capture** (slate-defining low-owned plays we rostered): 0% → 50% → 60% → 100% → 100%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `leverage_pct` was your biggest structural gap vs the pros in 4 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 1 → 0 → 1 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 2 of 4 graded slates — the board's boundaries are suspect.
- **Grader validation:** lineups the pre-lock checks would flag finished median 62.7%ile (n=8) vs clean 50.7%ile (n=128) — the checks are earning their keep.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR DK Ownership Model Golf 8.13.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR Golf Coffin List 8.16.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR Golf Course Fits & Preview 8.13.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR Golf Models 8.13.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR Golf Value Report 8.13.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR PGA Large Field Breakdown 8.13.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_classic/2026-08-12__ETR PGA Top Plays 8.13.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR PGA — `DK PGA DFS Projections (17).csv` (69 players)
| name | salary | ownership | proj_points | ceiling |
| --- | --- | --- | --- | --- |
| Scottie Scheffler | 13500 | 27.0 | 102.3 | 132.5 |
| Rory Mcilroy | 11500 | 13.2 | 93.1 | 124.3 |
| Cameron Young | 9700 | 23.0 | 90.6 | 119.3 |
| Xander Schauffele | 10000 | 16.7 | 88.5 | 115.6 |
| Tommy Fleetwood | 10200 | 14.8 | 88.5 | 113.0 |
| Sam Burns | 9500 | 21.4 | 87.9 | 115.8 |
| Justin Thomas | 8100 | 24.0 | 86.2 | 112.8 |
| Patrick Cantlay | 8800 | 16.8 | 86.2 | 113.9 |
| Matt Fitzpatrick | 9900 | 10.4 | 86.1 | 114.7 |
| Collin Morikawa | 9300 | 16.9 | 85.6 | 113.0 |
| Viktor Hovland | 8400 | 20.8 | 85.5 | 115.2 |
| Hideki Matsuyama | 9000 | 19.1 | 85.3 | 112.6 |
| Si Woo Kim | 8700 | 16.8 | 85.3 | 111.7 |
| Ludvig Aberg | 9100 | 14.7 | 84.1 | 110.0 |
| Russell Henley | 8600 | 12.0 | 83.2 | 110.3 |
| Chris Gotterup | 8900 | 10.2 | 83.2 | 109.9 |
| Maverick Mcnealy | 7600 | 12.3 | 82.3 | 108.0 |
| Michael Thorbjornsen | 7500 | 14.6 | 82.2 | 107.5 |
| Ryan Gerard | 7400 | 16.6 | 82.1 | 108.8 |
| Aaron Rai | 6800 | 13.5 | 81.5 | 104.6 |
| Robert Macintyre | 8300 | 9.8 | 81.3 | 105.6 |
| Jackson Koivun | 8200 | 11.4 | 81.0 | 105.4 |
| Rickie Fowler | 7500 | 8.9 | 80.2 | 103.3 |
| J.J. Spaun | 7800 | 8.7 | 79.9 | 103.3 |
| Ben Griffin | 7700 | 8.0 | 79.9 | 104.3 |
| Tom Kim | 7900 | 13.5 | 79.8 | 103.3 |
| Wyndham Clark | 8500 | 5.7 | 79.6 | 103.8 |
| Sungjae Im | 6700 | 11.9 | 78.3 | 101.0 |
| Min Woo Lee | 7700 | 5.9 | 78.2 | 102.2 |
| Kurt Kitayama | 7600 | 6.6 | 78.2 | 101.8 |
| J.T. Poston | 6300 | 7.9 | 77.6 | 103.7 |
| Michael Brennan | 7400 | 11.4 | 77.5 | 102.2 |
| Jacob Bridgeman | 7200 | 6.5 | 77.4 | 100.0 |
| Alex Fitzpatrick | 6800 | 10.5 | 77.1 | 100.3 |
| Corey Conners | 6700 | 9.0 | 76.9 | 100.1 |
| Shane Lowry | 7300 | 6.0 | 76.9 | 98.0 |
| Akshay Bhatia | 7300 | 10.4 | 76.7 | 100.5 |
| Michael Kim | 6500 | 6.4 | 76.6 | 100.1 |
| Justin Rose | 8000 | 4.3 | 76.6 | 99.2 |
| Alex Smalley | 7000 | 7.1 | 76.4 | 99.2 |
| Eric Cole | 6600 | 6.6 | 76.3 | 100.6 |
| Adam Scott | 7000 | 4.9 | 76.2 | 99.0 |
| Harris English | 6900 | 3.6 | 76.2 | 99.7 |
| Keith Mitchell | 6900 | 5.5 | 76.0 | 98.9 |
| Alex Noren | 7100 | 3.9 | 75.8 | 98.8 |
| Jake Knapp | 7000 | 5.3 | 75.7 | 99.2 |
| Kristoffer Reitan | 7100 | 4.0 | 75.3 | 98.2 |
| Sahith Theegala | 6600 | 5.5 | 75.0 | 98.0 |
| Brian Harman | 6500 | 3.5 | 75.0 | 95.8 |
| Bud Cauley | 6500 | 5.1 | 75.0 | 96.0 |
| Jordan L. Smith | 6600 | 7.3 | 74.6 | 95.1 |
| Nicolai Hojgaard | 7200 | 3.2 | 74.3 | 97.4 |
| Jordan Spieth | 6900 | 4.6 | 73.8 | 95.6 |
| Matthew McCarty | 6100 | 3.6 | 73.5 | 95.3 |
| Ryo Hisatsune | 6300 | 4.1 | 73.5 | 93.3 |
| Gary Woodland | 6700 | 2.6 | 73.4 | 95.7 |
| Nicolas Echavarria | 6300 | 3.2 | 73.1 | 95.2 |
| Harry Hall | 6400 | 4.0 | 72.7 | 95.4 |
| Sepp Straka | 6200 | 2.3 | 72.5 | 94.1 |
| Nick Taylor | 6400 | 1.5 | 72.3 | 93.6 |
| Ryan Fox | 6800 | 4.0 | 72.1 | 94.3 |
| Ricky Castillo | 6200 | 1.1 | 70.6 | 91.0 |
| Max Homa | 6400 | 1.7 | 70.4 | 89.5 |
| Pierceson Coody | 6000 | 0.7 | 69.5 | 91.6 |
| Sam Stevens | 6100 | 0.8 | 69.4 | 91.0 |
| Sudarshan Yellamaraju | 6200 | 1.0 | 69.4 | 90.6 |
| Matti Schmid | 6000 | 1.0 | 69.4 | 92.0 |
| Aldrich Potgieter | 6100 | 0.5 | 68.4 | 90.3 |
| Patrick Rodgers | 6000 | 0.2 | 65.4 | 85.4 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Robert Macintyre — $8,300, 10% own, proj 81.3, ceiling 105.6
- Ben Griffin — $7,700, 8% own, proj 79.9, ceiling 104.3
- Wyndham Clark — $8,500, 6% own, proj 79.6, ceiling 103.8
- J.T. Poston — $6,300, 8% own, proj 77.6, ceiling 103.7
- Rickie Fowler — $7,500, 9% own, proj 80.2, ceiling 103.3
- J.J. Spaun — $7,800, 9% own, proj 79.9, ceiling 103.3
- Min Woo Lee — $7,700, 6% own, proj 78.2, ceiling 102.2
- Kurt Kitayama — $7,600, 7% own, proj 78.2, ceiling 101.8
- Eric Cole — $6,600, 7% own, proj 76.3, ceiling 100.6
- Corey Conners — $6,700, 9% own, proj 76.9, ceiling 100.1
- Michael Kim — $6,500, 6% own, proj 76.6, ceiling 100.1
- Jacob Bridgeman — $7,200, 6% own, proj 77.4, ceiling 100.0

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Scottie Scheffler + Justin Thomas** — 27.0% × 24.0% ≈ 6.5% of the field (~46 lineups of 705)
- **Scottie Scheffler + Cameron Young** — 27.0% × 23.0% ≈ 6.2% of the field (~44 lineups of 705)
- **Scottie Scheffler + Sam Burns** — 27.0% × 21.4% ≈ 5.8% of the field (~41 lineups of 705)
- **Scottie Scheffler + Viktor Hovland** — 27.0% × 20.8% ≈ 5.6% of the field (~39 lineups of 705)
- **Justin Thomas + Cameron Young** — 24.0% × 23.0% ≈ 5.5% of the field (~39 lineups of 705)
- **Scottie Scheffler + Hideki Matsuyama** — 27.0% × 19.1% ≈ 5.2% of the field (~37 lineups of 705)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Alex Fitzpatrick** — $6,800, 10.5% own: the crowd pays 12 ranks more ownership than his projection earns (owned ahead of projection).
- **Sungjae Im** — $6,700, 11.9% own: the crowd pays 12 ranks more ownership than his projection earns (owned ahead of projection).
- **Tom Kim** — $7,900, 13.5% own: the crowd pays 11 ranks more ownership than his projection earns (owned ahead of projection).
- **Akshay Bhatia** — $7,300, 10.4% own: the crowd pays 10 ranks more ownership than his projection earns (owned ahead of projection).
- **Justin Thomas** — $8,100, 24.0% own: the crowd pays 9 ranks more ownership than his projection earns (owned ahead of projection).
- **Michael Brennan** — $7,400, 11.4% own: the crowd pays 8 ranks more ownership than his projection earns (owned ahead of projection).

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
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_southwind.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_toronto_osprey_valley.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_twin_cities.md`

**Output target:** write the slate strategy to `data/slate_analysis/pga_classic.md`.
