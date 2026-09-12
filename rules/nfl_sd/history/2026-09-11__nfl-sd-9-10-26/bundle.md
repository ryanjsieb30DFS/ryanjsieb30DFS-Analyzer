# Slate bundle — NFL Showdown
_Generated 2026-09-10 19:54 · slug `nfl_sd` · sport `nfl`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nfl_sd.md`.

## Contests
- 2 contest(s), 2 total entries
  - **NFL Showdown $10K Dimeback [Single Entry]** (SE): field 1,960, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
  - **NFL Showdown $10K Huddle [Single Entry]** (SE): field 2,378, my entries 1/1, payout **Top-heavy**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-10__NFL SD Matchups 9.10.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-10__SD Breakdown 9.10.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR NFL Showdown — `DK NFL Showdown Projections.csv` (30 players)
| name | salary | ownership | proj_points | ceiling | team | position |
| --- | --- | --- | --- | --- | --- | --- |
| Puka Nacua | 11200 | 65.5 | 22.2 | 37.0 | LAR | WR |
| Christian McCaffrey | 10600 | 65.0 | 21.3 | 35.5 | SF | RB |
| Matthew Stafford | 9800 | 58.9 | 19.9 | 30.0 | LAR | QB |
| Brock Purdy | 9400 | 52.5 | 18.8 | 29.0 | SF | QB |
| Davante Adams | 9200 | 34.8 | 14.9 | 28.0 | LAR | WR |
| Kyren Williams | 8600 | 37.2 | 14.7 | 26.2 | LAR | RB |
| Mike Evans | 8200 | 27.7 | 12.4 | 24.0 | SF | WR |
| Blake Corum | 4600 | 29.5 | 9.0 | 17.9 | LAR | RB |
| George Kittle | 7400 | 19.5 | 8.9 | 18.1 | SF | TE |
| Deebo Samuel Sr. | 7000 | 17.5 | 8.9 | 17.8 | SF | WR |
| Harrison Mevis | 5000 | 21.1 | 8.7 | 14.5 | LAR | K |
| Eddy Pineiro | 4800 | 21.3 | 8.4 | 14.6 | SF | K |
| De'Zhaun Stribling | 6600 | 18.2 | 7.3 | 15.4 | SF | WR |
| Rams | 4000 | 24.5 | 6.8 | 14.4 | LAR | DST |
| Terrance Ferguson | 3200 | 24.3 | 6.5 | 14.4 | LAR | TE |
| Colby Parkinson | 3600 | 20.9 | 5.8 | 12.8 | LAR | TE |
| Tyler Higbee | 2600 | 10.2 | 4.4 | 10.8 | LAR | TE |
| 49ers | 3400 | 12.1 | 4.1 | 10.3 | SF | DST |
| Jake Tonges | 4400 | 4.8 | 3.5 | 8.9 | SF | TE |
| Demarcus Robinson | 3800 | 4.8 | 3.1 | 8.6 | SF | WR |
| Jordan Whittington | 2800 | 3.4 | 2.7 | 7.6 | LAR | WR |
| Kyle Juszczyk | 1400 | 7.9 | 2.6 | 7.3 | SF | RB |
| Kaelon Black | 3000 | 3.9 | 2.0 | 6.1 | SF | RB |
| Konata Mumpfield | 1200 | 6.5 | 1.3 | 4.6 | LAR | WR |
| Davis Allen | 600 | 2.2 | 1.2 | 4.3 | LAR | TE |
| Luke Farrell | 1800 | 1.2 | 0.8 | 3.1 | SF | TE |
| Xavier Smith | 200 | 2.9 | 0.3 | 1.4 | LAR | WR |
| Ronnie Rivers | 400 | 0.7 | 0.2 | 1.0 | LAR | RB |
| Jacob Cowing | 1000 | 0.3 | 0.1 | 0.6 | SF | WR |
| KhaDarel Hodge | 200 | 0.9 | 0.1 | 0.6 | SF | WR |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Jake Tonges — $4,400, 5% own, proj 3.5, ceiling 8.9
- Demarcus Robinson — $3,800, 5% own, proj 3.1, ceiling 8.6
- Jordan Whittington — $2,800, 3% own, proj 2.7, ceiling 7.6
- Kyle Juszczyk — $1,400, 8% own, proj 2.6, ceiling 7.3
- Kaelon Black — $3,000, 4% own, proj 2.0, ceiling 6.1
- Konata Mumpfield — $1,200, 6% own, proj 1.3, ceiling 4.6
- Davis Allen — $600, 2% own, proj 1.2, ceiling 4.3
- Luke Farrell — $1,800, 1% own, proj 0.8, ceiling 3.1
- Xavier Smith — $200, 3% own, proj 0.3, ceiling 1.4
- Ronnie Rivers — $400, 1% own, proj 0.2, ceiling 1.0
- Jacob Cowing — $1,000, 0% own, proj 0.1, ceiling 0.6
- KhaDarel Hodge — $200, 1% own, proj 0.1, ceiling 0.6

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Puka Nacua + Christian McCaffrey** — 65.5% × 65.0% ≈ 42.6% of the field (~1,013 lineups of 2,378)
- **Puka Nacua + Matthew Stafford** — 65.5% × 58.9% ≈ 38.6% of the field (~918 lineups of 2,378)
- **Christian McCaffrey + Matthew Stafford** — 65.0% × 58.9% ≈ 38.3% of the field (~911 lineups of 2,378)
- **Puka Nacua + Brock Purdy** — 65.5% × 52.5% ≈ 34.4% of the field (~818 lineups of 2,378)
- **Christian McCaffrey + Brock Purdy** — 65.0% × 52.5% ≈ 34.1% of the field (~811 lineups of 2,378)
- **Matthew Stafford + Brock Purdy** — 58.9% × 52.5% ≈ 30.9% of the field (~735 lineups of 2,378)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Rams** — $4,000, 24.5% own: the crowd pays 5 ranks more ownership than his projection earns (owned ahead of projection).
- **Terrance Ferguson** — $3,200, 24.3% own: the crowd pays 4 ranks more ownership than his projection earns (owned ahead of projection).
- **Colby Parkinson** — $3,600, 20.9% own: the crowd pays 3 ranks more ownership than his projection earns (owned ahead of projection).
- **Blake Corum** — $4,600, 29.5% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Eddy Pineiro** — $4,800, 21.3% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).
- **Harrison Mevis** — $5,000, 21.1% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/set_diversity.md` — set-level diversity + dupe-avoidance doctrine (build loose, pick strict)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_sd/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**

**Output target:** write the slate strategy to `data/slate_analysis/nfl_sd.md`.
