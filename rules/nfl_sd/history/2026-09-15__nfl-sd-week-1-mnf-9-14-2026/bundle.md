# Slate bundle — NFL Showdown
_Generated 2026-09-14 19:36 · slug `nfl_sd` · sport `nfl`_
_**DraftKings only.** Ignore every FanDuel (FD) section, column, price, ownership number, or roster rule in any file below — the user never plays FD._

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nfl_sd.md`.

## Contests
- 1 contest(s), 5 total entries
  - **NFL Showdown $200K Flea Flicker** (150-Max): field 47,562, my entries 5/150, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## Slate at a glance`; never a play/fade command._
_**LARGE-FIELD CONTEST(S) DECLARED** (NFL Showdown $200K Flea Flicker (150-Max)) — the strategy MUST include the **big-field attack step** inside `## Build it like a sharp` (one evidence-backed line per field mistake; replaced the separate `## Field attack plan` section 8/9/26, see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 21 | 9/21 | 29.8 | 28.57 | 0.51 | ~29.8% own/slot |
| **youdacao** | 6 | 2/6 | 17.6 | 50.0 | 0.47 | carries a sub-5% leverage piece in most lineups, ~17.6% own/slot |
| **ShaidyAdvice** | 3 | 1/3 | 23.8 | 33.33 | 0.78 | ~23.8% own/slot |
| **needlunchmoney** | 1 | 0/1 | 45.0 | 0.0 | 0.67 | little-to-no leverage, ~45.0% own/slot |

## Process trend — your last 2 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 16.4 → 36.2
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 0%
- **Bust exposure** (top underperformers we rostered): 75% → 40%
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 2 of 2 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-14__Evan Silva’s Matchups_ Broncos at Chiefs _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-14__Showdown Breakdown_ Broncos at Chiefs _ Establish The Run.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR NFL Showdown — `DK NFL Showdown Projections(1).csv` (31 players)
| name | salary | ownership | proj_points | ceiling | team | position |
| --- | --- | --- | --- | --- | --- | --- |
| Patrick Mahomes | 9600 | 69.7 | 17.7 | 26.8 | KC | QB |
| Bo Nix | 9800 | 64.3 | 17.4 | 27.0 | DEN | QB |
| Kenneth Walker III | 10600 | 55.9 | 17.2 | 29.8 | KC | RB |
| Rashee Rice | 9400 | 48.9 | 14.7 | 26.4 | KC | WR |
| Jaylen Waddle | 9000 | 40.9 | 13.6 | 25.5 | DEN | WR |
| Travis Kelce | 7000 | 32.7 | 10.9 | 20.2 | KC | TE |
| Courtland Sutton | 8000 | 28.3 | 10.0 | 19.9 | DEN | WR |
| J.K. Dobbins | 6400 | 30.4 | 9.9 | 19.9 | DEN | RB |
| Xavier Worthy | 6600 | 25.8 | 9.6 | 19.3 | KC | WR |
| RJ Harvey | 7400 | 21.9 | 9.1 | 17.7 | DEN | RB |
| Harrison Butker | 5000 | 26.5 | 8.5 | 14.4 | KC | K |
| Wil Lutz | 5200 | 22.1 | 8.2 | 14.4 | DEN | K |
| Pat Bryant | 3200 | 22.9 | 6.7 | 14.4 | DEN | WR |
| Chiefs | 4400 | 18.4 | 6.3 | 13.4 | KC | DST |
| Evan Engram | 3400 | 17.5 | 6.2 | 12.8 | DEN | TE |
| Broncos | 4800 | 19.6 | 6.0 | 12.9 | DEN | DST |
| Tyquan Thornton | 3600 | 11.6 | 5.0 | 12.6 | KC | WR |
| Noah Gray | 2000 | 7.5 | 3.5 | 8.7 | KC | TE |
| Marvin Mims Jr. | 3000 | 5.6 | 3.1 | 8.1 | DEN | WR |
| Cyrus Allen | 4000 | 4.7 | 2.9 | 8.0 | KC | WR |
| Emmett Johnson | 2600 | 4.9 | 2.9 | 7.9 | KC | RB |
| Jonah Coleman | 2400 | 4.4 | 2.8 | 7.7 | DEN | RB |
| Adam Trautman | 1600 | 4.2 | 2.4 | 6.6 | DEN | TE |
| Brashard Smith | 1400 | 4.0 | 2.2 | 6.5 | KC | RB |
| Troy Franklin | 2800 | 3.5 | 1.9 | 6.0 | DEN | WR |
| Nate Adkins | 600 | 1.9 | 1.7 | 5.1 | DEN | TE |
| Adam Prentice | 200 | 0.3 | 0.6 | 2.3 | DEN | RB |
| Jake Briningstool | 200 | 0.5 | 0.3 | 1.3 | KC | TE |
| Jalen Royals | 1200 | 0.6 | 0.1 | 0.6 | KC | WR |
| Nikko Remigio | 800 | 0.3 | 0.1 | 0.6 | KC | WR |
| Ben VanSumeren | 200 | 0.1 | 0.1 | 0.5 | KC | RB |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Noah Gray — $2,000, 8% own, proj 3.5, ceiling 8.7
- Marvin Mims Jr. — $3,000, 6% own, proj 3.1, ceiling 8.1
- Cyrus Allen — $4,000, 5% own, proj 2.9, ceiling 8.0
- Emmett Johnson — $2,600, 5% own, proj 2.9, ceiling 7.9
- Jonah Coleman — $2,400, 4% own, proj 2.8, ceiling 7.7
- Adam Trautman — $1,600, 4% own, proj 2.4, ceiling 6.6
- Brashard Smith — $1,400, 4% own, proj 2.2, ceiling 6.5
- Troy Franklin — $2,800, 4% own, proj 1.9, ceiling 6.0
- Nate Adkins — $600, 2% own, proj 1.7, ceiling 5.1
- Adam Prentice — $200, 0% own, proj 0.6, ceiling 2.3
- Jake Briningstool — $200, 0% own, proj 0.3, ceiling 1.3
- Jalen Royals — $1,200, 1% own, proj 0.1, ceiling 0.6

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Patrick Mahomes + Bo Nix** — 69.7% × 64.3% ≈ 44.8% of the field (~21,308 lineups of 47,562)
- **Patrick Mahomes + Kenneth Walker III** — 69.7% × 55.9% ≈ 39.0% of the field (~18,549 lineups of 47,562)
- **Bo Nix + Kenneth Walker III** — 64.3% × 55.9% ≈ 35.9% of the field (~17,075 lineups of 47,562)
- **Patrick Mahomes + Rashee Rice** — 69.7% × 48.9% ≈ 34.1% of the field (~16,219 lineups of 47,562)
- **Bo Nix + Rashee Rice** — 64.3% × 48.9% ≈ 31.4% of the field (~14,934 lineups of 47,562)
- **Patrick Mahomes + Jaylen Waddle** — 69.7% × 40.9% ≈ 28.5% of the field (~13,555 lineups of 47,562)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Patrick Mahomes** — $9,600, 69.7% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Harrison Butker** — $5,000, 26.5% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Broncos** — $4,800, 19.6% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/set_diversity.md` — set-level diversity + dupe-avoidance doctrine (build loose, pick strict)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/results.jsonl` — cross-slate results ledger (process notes only)

**Output target:** write the slate strategy to `data/slate_analysis/nfl_sd.md`.
