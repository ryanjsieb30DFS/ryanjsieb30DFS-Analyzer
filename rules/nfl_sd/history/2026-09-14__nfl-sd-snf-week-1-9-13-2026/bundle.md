# Slate bundle — NFL Showdown
_Generated 2026-09-13 19:34 · slug `nfl_sd` · sport `nfl`_
_**DraftKings only.** Ignore every FanDuel (FD) section, column, price, ownership number, or roster rule in any file below — the user never plays FD._

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nfl_sd.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NFL Showdown $10K Dimeback [Single Entry]** (SE): field 1,960, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
  - **NFL Showdown $8K Huddle [Single Entry]** (SE): field 1,902, my entries 1/1, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## Slate at a glance`; never a play/fade command._

## Field tendencies — where your opponents go
RULE — A TRAP IS A PRICE, NOT A DRIVER. No player is ever a trap. A trap is a price shape: a salary, a projection, and an ownership number that do not line up. Those three numbers reset every slate, so trap history below is stated as CONDITIONS (price shapes), never as player names.
The player names below are different. They map where YOUR OPPONENTS reliably go (the same small fields keep entering these contests). Use the names to find room AWAY from the crowd (leverage). Never use them as proof a player is good or bad, and never as a reason to fade him. Surface all of it as tension; do NOT tell the user to fade anyone.
- **SE** (across your 2 past comparable SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 7.7% ownership (range 4-23.8%); its 7 past crowd name(s) are NOT on this card — apply the shape to THIS card's consensus favorites (sized in `## Chalk combos`); trap shape (a trap is a price, not a player — the price conditions the losing half keeps buying): 0 of 16 were 25%+ owned (traps here are usually popular players who fail, not long shots); 6 of 16 were owned ahead of their projection rank (the trap-shaped price); most sat in the Punt (<$6k) salary tier (6 of 16); from the full-field captures (2 contests): only **59.1% of entries were unique rosters**, the most-copied lineup appeared **88 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **36.6%** of lineups.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 19 | 7/19 | 29.8 | 26.32 | 0.5 | ~29.8% own/slot |
| **ShaidyAdvice** | 1 | 0/1 | 6.9 | 100.0 | 0.67 | carries a sub-5% leverage piece in most lineups, ~6.9% own/slot |

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-13__Evan Silva’s Matchups_ Cowboys at Giants _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-13__Showdown Breakdown_ Cowboys at Giants _ Establish The Run.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR NFL Showdown — `DK NFL Showdown Projections (1).csv` (29 players)
| name | salary | ownership | proj_points | ceiling | team | position |
| --- | --- | --- | --- | --- | --- | --- |
| Dak Prescott | 10400 | 66.5 | 19.7 | 29.8 | DAL | QB |
| Jaxson Dart | 9600 | 63.1 | 18.8 | 28.5 | NYG | QB |
| CeeDee Lamb | 10800 | 52.1 | 18.1 | 32.1 | DAL | WR |
| Javonte Williams | 9000 | 55.4 | 17.9 | 31.3 | DAL | RB |
| George Pickens | 9800 | 47.7 | 16.0 | 29.6 | DAL | WR |
| Cam Skattebo | 8400 | 39.1 | 14.5 | 25.6 | NYG | RB |
| Malik Nabers | 9400 | 34.2 | 13.3 | 25.3 | NYG | WR |
| Brandon Aubrey | 5400 | 30.1 | 9.5 | 15.9 | DAL | K |
| Jake Ferguson | 5800 | 23.8 | 9.0 | 17.6 | DAL | TE |
| Isaiah Likely | 6400 | 24.4 | 8.9 | 17.4 | NYG | TE |
| Dominic Zvada | 4800 | 22.1 | 8.4 | 14.5 | NYG | K |
| Cowboys | 4400 | 15.9 | 7.0 | 14.5 | DAL | DST |
| Ryan Flournoy | 3800 | 17.1 | 6.4 | 14.0 | DAL | WR |
| Tyrone Tracy Jr. | 3000 | 16.6 | 6.2 | 13.2 | NYG | RB |
| Malachi Fields | 5000 | 13.5 | 5.7 | 12.9 | NYG | WR |
| Giants | 3400 | 13.6 | 5.4 | 12.5 | NYG | DST |
| Theo Johnson | 1800 | 13.0 | 4.2 | 10.2 | NYG | TE |
| Darnell Mooney | 4000 | 9.8 | 4.0 | 10.0 | NYG | WR |
| KaVontae Turpin | 2600 | 8.3 | 4.0 | 10.1 | DAL | WR |
| Odell Beckham Jr. | 2200 | 8.5 | 3.0 | 8.3 | NYG | WR |
| Devin Singletary | 1400 | 6.9 | 2.7 | 7.7 | NYG | RB |
| Emari Demercado | 1000 | 8.3 | 2.7 | 7.7 | DAL | RB |
| Brevyn Spann-Ford | 1600 | 3.4 | 2.3 | 6.7 | DAL | TE |
| Hunter Luepke | 800 | 2.5 | 2.1 | 6.3 | DAL | RB |
| Luke Schoonmaker | 600 | 1.8 | 1.1 | 3.8 | DAL | TE |
| Jonathan Mingo | 1200 | 0.8 | 0.6 | 2.4 | DAL | WR |
| Braxton Berrios | 200 | 0.7 | 0.5 | 1.9 | NYG | WR |
| Chris Manhertz | 200 | 0.4 | 0.3 | 1.1 | NYG | TE |
| Patrick Ricard | 400 | 0.4 | 0.2 | 0.8 | NYG | RB |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- KaVontae Turpin — $2,600, 8% own, proj 4.0, ceiling 10.1
- Darnell Mooney — $4,000, 10% own, proj 4.0, ceiling 10.0
- Odell Beckham Jr. — $2,200, 8% own, proj 3.0, ceiling 8.3
- Devin Singletary — $1,400, 7% own, proj 2.7, ceiling 7.7
- Emari Demercado — $1,000, 8% own, proj 2.7, ceiling 7.7
- Brevyn Spann-Ford — $1,600, 3% own, proj 2.3, ceiling 6.7
- Hunter Luepke — $800, 2% own, proj 2.1, ceiling 6.3
- Luke Schoonmaker — $600, 2% own, proj 1.1, ceiling 3.8
- Jonathan Mingo — $1,200, 1% own, proj 0.6, ceiling 2.4
- Braxton Berrios — $200, 1% own, proj 0.5, ceiling 1.9
- Chris Manhertz — $200, 0% own, proj 0.3, ceiling 1.1
- Patrick Ricard — $400, 0% own, proj 0.2, ceiling 0.8

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Dak Prescott + Jaxson Dart** — 66.5% × 63.1% ≈ 42.0% of the field (~823 lineups of 1,960)
- **Dak Prescott + Javonte Williams** — 66.5% × 55.4% ≈ 36.8% of the field (~721 lineups of 1,960)
- **Jaxson Dart + Javonte Williams** — 63.1% × 55.4% ≈ 35.0% of the field (~686 lineups of 1,960)
- **Dak Prescott + CeeDee Lamb** — 66.5% × 52.1% ≈ 34.6% of the field (~678 lineups of 1,960)
- **Jaxson Dart + CeeDee Lamb** — 63.1% × 52.1% ≈ 32.9% of the field (~645 lineups of 1,960)
- **Dak Prescott + George Pickens** — 66.5% × 47.7% ≈ 31.7% of the field (~621 lineups of 1,960)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Jaxson Dart** — $9,600, 63.1% own: the crowd pays 3 ranks more ownership than his projection earns (owned ahead of projection).
- **Dak Prescott** — $10,400, 66.5% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Brandon Aubrey** — $5,400, 30.1% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Tyrone Tracy Jr.** — $3,000, 16.6% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).
- **Ryan Flournoy** — $3,800, 17.1% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).
- **Giants** — $3,400, 13.6% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).

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
