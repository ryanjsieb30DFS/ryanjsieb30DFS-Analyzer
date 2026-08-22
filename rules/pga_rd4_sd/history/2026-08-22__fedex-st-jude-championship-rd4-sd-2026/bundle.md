# Slate bundle — PGA RD4 Showdown
_Generated 2026-08-16 05:24 · slug `pga_rd4_sd` · sport `golf`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/pga_rd4_sd.md`.

## Contests
- 2 contest(s), 2 total entries
  - **PGA TOUR Showdown $4K Dogleg [Single Entry] (Round 4 TOUR)** (SE): field 141, my entries 1/1, prize multiple 0.86x
  - **PGA TOUR Showdown $2K Albatross [Single Entry] (Round 4 TOUR)** (SE): field 196, my entries 1/1, payout **Flat**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **SE** (across your 2 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 33.9% ownership (range 22-56.7%); your opponents reliably pile onto **Michael Brennan (in 2 of 2)** — a map of where THEY go, not a read on the players; trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 6 of 13 were 25%+ owned (traps here are usually popular players who fail, not long shots); 7 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Studs ($10k+) salary tier (5 of 16); from the full-field captures (1 contest): only **95.9% of entries were unique rosters**, the most-copied lineup appeared **7 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **9.0%** of lineups.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your golf shark envelope:** own/slot **16.677**, leverage **49.539%**, anchor-exposure **0.408**, unique **91.161%**. You run: own/slot 15.63, leverage 39.71%, anchor 0.37 — that delta is the gap to close.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 11 | 4/11 | 27.8 | 32.73 | 0.5 | ~27.8% own/slot |
| **PetrGibbons** | 1 | 0/1 | 15.2 | 100.0 | 0.67 | carries a sub-5% leverage piece in most lineups, ~15.2% own/slot |
| **youdacao** | 3 | 0/3 | 17.6 | 26.67 | 0.4 | fades the chalk anchors, ~17.6% own/slot |

## Process trend — your last 3 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 4.5 → 26.1 → 0.3
- **Leverage capture** (slate-defining low-owned plays we rostered): 0% → 100% → 100%
- **Bust exposure** (top underperformers we rostered): 60% → — → 17%
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 2 of the last 3 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 2 of 2 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/pga_rd4_sd/2026-08-16__PGA RD4 SD 8.16.2026.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DK PGA RD4 SD — `DK PGA Round 4 Showdown Projections (12).csv` (68 players)
| name | salary | ownership | proj_points |
| --- | --- | --- | --- |
| Scottie Scheffler | 13400 | 23.7 | 62.91 |
| Sam Burns | 10400 | 36.5 | 54.72 |
| Hideki Matsuyama | 10100 | 20.9 | 49.94 |
| Tommy Fleetwood | 11000 | 11.8 | 50.58 |
| Si Woo Kim | 9100 | 26.2 | 47.99 |
| Viktor Hovland | 9500 | 15.7 | 46.97 |
| Chris Gotterup | 8900 | 16.8 | 46.18 |
| Sungjae Im | 8000 | 49.5 | 50.080000000000005 |
| Xander Schauffele | 10000 | 7.4 | 44.69 |
| Matt Fitzpatrick | 9400 | 7.3 | 44.69 |
| Patrick Cantlay | 9200 | 12.1 | 44.92 |
| Ludvig Aberg | 9800 | 5.2 | 43.16 |
| Jake Knapp | 7900 | 27.6 | 45.68000000000001 |
| Tom Kim | 8500 | 19.8 | 44.15 |
| Rory McIlroy | 10500 | 0.7 | 38.94 |
| Wyndham Clark | 9000 | 8.3 | 43.209999999999994 |
| Kurt Kitayama | 7800 | 19.8 | 43.760000000000005 |
| Russell Henley | 7800 | 12.9 | 41.02 |
| Cameron Young | 9300 | 3.3 | 39.57 |
| Alex Noren | 7400 | 25.9 | 43.79 |
| Jackson Koivun | 8600 | 5.6 | 40.97 |
| Adam Scott | 7600 | 13.0 | 42.03 |
| Maverick McNealy | 8400 | 5.0 | 40.7 |
| Ryan Gerard | 7600 | 8.9 | 39.96 |
| J.J. Spaun | 7700 | 10.2 | 40.379999999999995 |
| Rickie Fowler | 7700 | 9.7 | 40.379999999999995 |
| Justin Thomas | 8700 | 3.2 | 39.02 |
| Brian Harman | 7000 | 27.7 | 42.790000000000006 |
| J.T. Poston | 6300 | 26.6 | 41.160000000000004 |
| Collin Morikawa | 8800 | 1.5 | 37.99 |
| Michael Thorbjornsen | 8300 | 3.1 | 37.69 |
| Jacob Bridgeman | 7500 | 8.3 | 39.75 |
| Nicolas Echavarria | 6900 | 15.7 | 40.71 |
| Jordan Spieth | 7900 | 7.0 | 40.02 |
| Alex Smalley | 8200 | 2.7 | 38.5 |
| Keith Mitchell | 7400 | 6.9 | 39.07 |
| Bud Cauley | 7100 | 7.6 | 37.949999999999996 |
| Aaron Rai | 7300 | 4.6 | 37.12 |
| Ben Griffin | 7500 | 1.8 | 35.69 |
| Gary Woodland | 7200 | 5.6 | 37.879999999999995 |
| Nick Taylor | 6300 | 14.2 | 38.400000000000006 |
| Michael Brennan | 6900 | 3.6 | 35.93 |
| Harry Hall | 6400 | 7.9 | 36.550000000000004 |
| Min Woo Lee | 8100 | 0.3 | 34.75 |
| Michael Kim | 7200 | 1.2 | 35.08 |
| Shane Lowry | 7100 | 2.0 | 34.53 |
| Alex Fitzpatrick | 6800 | 1.5 | 34.22 |
| Corey Conners | 6700 | 2.5 | 34.52 |
| Jordan L. Smith | 6400 | 4.3 | 34.75 |
| Harris English | 6800 | 1.2 | 34.0 |
| Ryo Hisatsune | 6300 | 5.0 | 34.620000000000005 |
| Nicolai Hojgaard | 6600 | 2.5 | 34.12 |
| Eric Cole | 6400 | 1.8 | 33.61 |
| Akshay Bhatia | 7000 | 0.5 | 33.33 |
| Pierceson Coody | 6200 | 6.0 | 35.410000000000004 |
| Sam Stevens | 6100 | 2.9 | 34.08 |
| Sahith Theegala | 6600 | 0.9 | 33.0 |
| Justin Rose | 7300 | 0.6 | 32.949999999999996 |
| Kristoffer Reitan | 6500 | 1.2 | 32.949999999999996 |
| Patrick Rodgers | 6500 | 3.0 | 34.98 |
| Sepp Straka | 6200 | 1.5 | 32.68 |
| Sudarshan Yellamaraju | 6700 | 0.8 | 32.94 |
| Ryan Fox | 6200 | 0.7 | 32.21 |
| Max Homa | 6100 | 3.5 | 33.11 |
| Matti Schmid | 6000 | 1.7 | 32.45 |
| Matthew McCarty | 6000 | 1.4 | 31.64 |
| Ricky Castillo | 6000 | 1.2 | 31.23 |
| Aldrich Potgieter | 6100 | 0.3 | 30.84 |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Xander Schauffele — $10,000, 7% own, proj 44.7, ceiling 44.7
- Matt Fitzpatrick — $9,400, 7% own, proj 44.7, ceiling 44.7
- Ludvig Aberg — $9,800, 5% own, proj 43.2, ceiling 43.2
- Wyndham Clark — $9,000, 8% own, proj 43.2, ceiling 43.2
- Jackson Koivun — $8,600, 6% own, proj 41.0, ceiling 41.0
- Maverick McNealy — $8,400, 5% own, proj 40.7, ceiling 40.7
- Rickie Fowler — $7,700, 10% own, proj 40.4, ceiling 40.4
- Jordan Spieth — $7,900, 7% own, proj 40.0, ceiling 40.0
- Ryan Gerard — $7,600, 9% own, proj 40.0, ceiling 40.0
- Jacob Bridgeman — $7,500, 8% own, proj 39.8, ceiling 39.8
- Cameron Young — $9,300, 3% own, proj 39.6, ceiling 39.6
- Keith Mitchell — $7,400, 7% own, proj 39.1, ceiling 39.1

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Sungjae Im + Sam Burns** — 49.5% × 36.5% ≈ 18.1% of the field (~35 lineups of 196)
- **Sungjae Im + Brian Harman** — 49.5% × 27.7% ≈ 13.7% of the field (~27 lineups of 196)
- **Sungjae Im + Jake Knapp** — 49.5% × 27.6% ≈ 13.7% of the field (~27 lineups of 196)
- **Sungjae Im + J.T. Poston** — 49.5% × 26.6% ≈ 13.2% of the field (~26 lineups of 196)
- **Sungjae Im + Si Woo Kim** — 49.5% × 26.2% ≈ 13.0% of the field (~25 lineups of 196)
- **Sungjae Im + Alex Noren** — 49.5% × 25.9% ≈ 12.8% of the field (~25 lineups of 196)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Nick Taylor** — $6,300, 14.2% own: the crowd pays 20 ranks more ownership than his projection earns (owned ahead of projection).
- **Brian Harman** — $7,000, 27.7% own: the crowd pays 15 ranks more ownership than his projection earns (owned ahead of projection).
- **J.T. Poston** — $6,300, 26.6% own: the crowd pays 15 ranks more ownership than his projection earns (owned ahead of projection).
- **Nicolas Echavarria** — $6,900, 15.7% own: the crowd pays 10 ranks more ownership than his projection earns (owned ahead of projection).
- **Alex Noren** — $7,400, 25.9% own: the crowd pays 7 ranks more ownership than his projection earns (owned ahead of projection).
- **Jake Knapp** — $7,900, 27.6% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).

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
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_southwind.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_toronto_osprey_valley.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/pga_classic/courses/tpc_twin_cities.md`

**Output target:** write the slate strategy to `data/slate_analysis/pga_rd4_sd.md`.
