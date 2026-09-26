# Slate bundle — NFL Showdown
_Generated 2026-09-21 19:22 · slug `nfl_sd` · sport `nfl`_
_**DraftKings only.** Ignore every FanDuel (FD) section, column, price, ownership number, or roster rule in any file below — the user never plays FD._

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nfl_sd.md`.

## Contests
- 1 contest(s), 20 total entries
  - **NFL Showdown $70K First Down** (20-Max): field 83,234, my entries 20/20, payout **Balanced**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## Slate at a glance`; never a play/fade command._
_**LARGE-FIELD CONTEST(S) DECLARED** (NFL Showdown $70K First Down (20-Max)) — the strategy MUST include the **big-field attack step** inside `## Build it like a sharp` (one evidence-backed line per field mistake; replaced the separate `## Field attack plan` section 8/9/26, see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 22 | 9/22 | 29.8 | 27.27 | 0.49 | ~29.8% own/slot |
| **youdacao** | 6 | 2/6 | 17.6 | 50.0 | 0.47 | carries a sub-5% leverage piece in most lineups, ~17.6% own/slot |
| **ShaidyAdvice** | 3 | 1/3 | 23.8 | 33.33 | 0.78 | ~23.8% own/slot |
| **needlunchmoney** | 1 | 0/1 | 45.0 | 0.0 | 0.67 | little-to-no leverage, ~45.0% own/slot |

## Process trend — your last 4 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 16.4 → 36.2 → 0.3 → 17.3
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 0% → 100% → 100%
- **Bust exposure** (top underperformers we rostered): 75% → 40% → 80% → 100%
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 4 of 4 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-21__Evan Silva’s Matchups_ Giants at Rams _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-21__Showdown Breakdown_ Giants at Rams _ Establish The Run.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR NFL Showdown — `DK NFL Showdown Projections(2).csv` (31 players)
| name | salary | ownership | proj_points | ceiling | team | position |
| --- | --- | --- | --- | --- | --- | --- |
| Jaxson Dart | 9800 | 72.9 | 19.4 | 29.0 | NYG | QB |
| Matthew Stafford | 10000 | 71.4 | 18.5 | 28.0 | LAR | QB |
| Davante Adams | 8800 | 62.4 | 17.4 | 31.2 | LAR | WR |
| Kyren Williams | 9600 | 57.5 | 16.4 | 28.6 | LAR | RB |
| Malik Nabers | 9000 | 51.6 | 15.4 | 28.1 | NYG | WR |
| Cam Skattebo | 9400 | 37.1 | 12.0 | 22.2 | NYG | RB |
| Isaiah Likely | 7400 | 29.0 | 10.6 | 19.9 | NYG | TE |
| Colby Parkinson | 3600 | 32.8 | 10.1 | 19.5 | LAR | TE |
| Blake Corum | 4600 | 27.3 | 9.6 | 18.9 | LAR | RB |
| Harrison Mevis | 5000 | 23.2 | 9.3 | 15.1 | LAR | K |
| Dominic Zvada | 4800 | 14.5 | 7.8 | 13.7 | NYG | K |
| Terrance Ferguson | 1800 | 22.9 | 7.8 | 16.6 | LAR | TE |
| Rams | 4200 | 19.4 | 7.4 | 14.9 | LAR | DST |
| Malachi Fields | 5600 | 11.6 | 6.2 | 13.7 | NYG | WR |
| Xavier Smith | 200 | 11.0 | 5.4 | 12.7 | LAR | WR |
| Devin Singletary | 3000 | 6.9 | 5.3 | 11.9 | NYG | RB |
| Darnell Mooney | 3800 | 8.6 | 4.8 | 11.4 | NYG | WR |
| Konata Mumpfield | 1000 | 9.7 | 4.7 | 11.6 | LAR | WR |
| Giants | 3200 | 9.3 | 4.0 | 10.5 | NYG | DST |
| Theo Johnson | 2400 | 5.0 | 3.3 | 8.5 | NYG | TE |
| Tyler Higbee | 2800 | 4.5 | 3.2 | 8.7 | LAR | TE |
| Najee Harris | 2000 | 5.0 | 2.2 | 6.5 | NYG | RB |
| Davis Allen | 1600 | 2.1 | 2.2 | 6.6 | LAR | TE |
| Tutu Atwell | 800 | 2.7 | 1.8 | 6.1 | LAR | WR |
| Odell Beckham Jr. | 1200 | 0.6 | 1.5 | 4.9 | NYG | WR |
| Patrick Ricard | 400 | 0.3 | 0.6 | 2.4 | NYG | RB |
| Ronnie Rivers | 1400 | 0.3 | 0.4 | 1.4 | LAR | RB |
| Tyrone Tracy Jr. | 3400 | 0.3 | 0.3 | 1.0 | NYG | RB |
| Chris Manhertz | 600 | 0.3 | 0.3 | 1.1 | NYG | TE |
| Max Klare | 200 | 0.1 | 0.3 | 1.2 | LAR | TE |
| Braxton Berrios | 200 | 0.0 | 0.2 | 1.0 | NYG | WR |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Devin Singletary — $3,000, 7% own, proj 5.3, ceiling 11.9
- Konata Mumpfield — $1,000, 10% own, proj 4.7, ceiling 11.6
- Darnell Mooney — $3,800, 9% own, proj 4.8, ceiling 11.4
- Giants — $3,200, 9% own, proj 4.0, ceiling 10.5
- Tyler Higbee — $2,800, 4% own, proj 3.2, ceiling 8.7
- Theo Johnson — $2,400, 5% own, proj 3.3, ceiling 8.5
- Davis Allen — $1,600, 2% own, proj 2.2, ceiling 6.6
- Najee Harris — $2,000, 5% own, proj 2.2, ceiling 6.5
- Tutu Atwell — $800, 3% own, proj 1.8, ceiling 6.1
- Odell Beckham Jr. — $1,200, 1% own, proj 1.5, ceiling 4.9
- Patrick Ricard — $400, 0% own, proj 0.6, ceiling 2.4
- Ronnie Rivers — $1,400, 0% own, proj 0.4, ceiling 1.4

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Jaxson Dart + Matthew Stafford** — 72.9% × 71.4% ≈ 52.1% of the field (~43,365 lineups of 83,234)
- **Jaxson Dart + Davante Adams** — 72.9% × 62.4% ≈ 45.5% of the field (~37,871 lineups of 83,234)
- **Matthew Stafford + Davante Adams** — 71.4% × 62.4% ≈ 44.6% of the field (~37,122 lineups of 83,234)
- **Jaxson Dart + Kyren Williams** — 72.9% × 57.5% ≈ 41.9% of the field (~34,875 lineups of 83,234)
- **Matthew Stafford + Kyren Williams** — 71.4% × 57.5% ≈ 41.1% of the field (~34,209 lineups of 83,234)
- **Jaxson Dart + Malik Nabers** — 72.9% × 51.6% ≈ 37.6% of the field (~31,296 lineups of 83,234)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Matthew Stafford** — $10,000, 71.4% own: the crowd pays 3 ranks more ownership than his projection earns (owned ahead of projection).
- **Jaxson Dart** — $9,800, 72.9% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).
- **Colby Parkinson** — $3,600, 32.8% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).
- **Harrison Mevis** — $5,000, 23.2% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).

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
