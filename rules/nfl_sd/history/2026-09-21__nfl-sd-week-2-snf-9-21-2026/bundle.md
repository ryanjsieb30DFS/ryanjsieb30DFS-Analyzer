# Slate bundle — NFL Showdown
_Generated 2026-09-20 19:35 · slug `nfl_sd` · sport `nfl`_
_**DraftKings only.** Ignore every FanDuel (FD) section, column, price, ownership number, or roster rule in any file below — the user never plays FD._

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nfl_sd.md`.

## Contests
- 1 contest(s), 20 total entries
  - **NFL Showdown $40K First Down** (20-Max): field 47,562, my entries 20/20, payout **Balanced**, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## Slate at a glance`; never a play/fade command._
_**LARGE-FIELD CONTEST(S) DECLARED** (NFL Showdown $40K First Down (20-Max)) — the strategy MUST include the **big-field attack step** inside `## Build it like a sharp` (one evidence-backed line per field mistake; replaced the separate `## Field attack plan` section 8/9/26, see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 22 | 9/22 | 29.8 | 27.27 | 0.49 | ~29.8% own/slot |
| **youdacao** | 6 | 2/6 | 17.6 | 50.0 | 0.47 | carries a sub-5% leverage piece in most lineups, ~17.6% own/slot |
| **ShaidyAdvice** | 3 | 1/3 | 23.8 | 33.33 | 0.78 | ~23.8% own/slot |
| **needlunchmoney** | 1 | 0/1 | 45.0 | 0.0 | 0.67 | little-to-no leverage, ~45.0% own/slot |

## Process trend — your last 3 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 16.4 → 36.2 → 0.3
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 0% → 100%
- **Bust exposure** (top underperformers we rostered): 75% → 40% → 80%
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 3 of 3 graded slates.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-20__Evan Silva’s Matchups_ Colts at Chiefs _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_sd/2026-09-20__Showdown Breakdown_ Colts at Chiefs _ Establish The Run.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR NFL Showdown — `DK NFL Showdown Projections (2).csv` (30 players)
| name | salary | ownership | proj_points | ceiling | team | position |
| --- | --- | --- | --- | --- | --- | --- |
| Kenneth Walker III | 10600 | 63.5 | 21.3 | 35.9 | KC | RB |
| Patrick Mahomes | 10000 | 69.3 | 20.2 | 30.4 | KC | QB |
| Jonathan Taylor | 11000 | 55.8 | 19.1 | 32.4 | IND | RB |
| Daniel Jones | 9200 | 42.3 | 15.4 | 23.9 | IND | QB |
| Rashee Rice | 9400 | 37.3 | 14.6 | 26.8 | KC | WR |
| Tyler Warren | 7200 | 36.1 | 12.3 | 22.1 | IND | TE |
| Xavier Worthy | 5400 | 39.2 | 12.0 | 23.3 | KC | WR |
| Travis Kelce | 6200 | 37.5 | 11.6 | 22.0 | KC | TE |
| Josh Downs | 6600 | 30.9 | 11.1 | 20.7 | IND | WR |
| Alec Pierce | 7600 | 23.2 | 9.7 | 20.3 | IND | WR |
| Keenan Allen | 5600 | 26.0 | 9.1 | 17.7 | IND | WR |
| Harrison Butker | 5000 | 27.4 | 9.1 | 15.0 | KC | K |
| Spencer Shrader | 4600 | 23.8 | 8.1 | 14.0 | IND | K |
| Chiefs | 4200 | 22.3 | 7.0 | 14.4 | KC | DST |
| Tyquan Thornton | 3800 | 14.5 | 5.6 | 13.8 | KC | WR |
| Colts | 3200 | 14.3 | 4.9 | 11.7 | IND | DST |
| Emmett Johnson | 3600 | 11.2 | 4.7 | 11.3 | KC | RB |
| Noah Gray | 3000 | 8.7 | 3.6 | 9.2 | KC | TE |
| Seth McGowan | 3400 | 3.1 | 1.9 | 5.9 | IND | RB |
| Mo Alie-Cox | 2400 | 3.4 | 1.7 | 5.3 | IND | TE |
| Laquon Treadwell | 2000 | 3.0 | 1.5 | 4.8 | IND | WR |
| Cyrus Allen | 2800 | 1.6 | 0.7 | 2.6 | KC | WR |
| Jake Briningstool | 1600 | 0.8 | 0.3 | 1.3 | KC | TE |
| Drew Ogletree | 600 | 0.8 | 0.3 | 1.1 | IND | TE |
| Brashard Smith | 400 | 1.0 | 0.3 | 1.1 | KC | RB |
| Jalen Royals | 1200 | 0.6 | 0.2 | 0.6 | KC | WR |
| Nikko Remigio | 800 | 0.6 | 0.2 | 0.6 | KC | WR |
| Ben VanSumeren | 200 | 0.4 | 0.2 | 0.8 | KC | RB |
| Deion Burks | 1000 | 0.6 | 0.1 | 0.5 | IND | WR |
| Anthony Gould | 200 | 1.0 | 0.1 | 0.5 | IND | WR |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Noah Gray — $3,000, 9% own, proj 3.6, ceiling 9.2
- Seth McGowan — $3,400, 3% own, proj 1.9, ceiling 5.9
- Mo Alie-Cox — $2,400, 3% own, proj 1.7, ceiling 5.3
- Laquon Treadwell — $2,000, 3% own, proj 1.5, ceiling 4.8
- Cyrus Allen — $2,800, 2% own, proj 0.7, ceiling 2.6
- Jake Briningstool — $1,600, 1% own, proj 0.3, ceiling 1.3
- Drew Ogletree — $600, 1% own, proj 0.3, ceiling 1.1
- Brashard Smith — $400, 1% own, proj 0.3, ceiling 1.1
- Ben VanSumeren — $200, 0% own, proj 0.2, ceiling 0.8
- Jalen Royals — $1,200, 1% own, proj 0.2, ceiling 0.6
- Nikko Remigio — $800, 1% own, proj 0.2, ceiling 0.6
- Deion Burks — $1,000, 1% own, proj 0.1, ceiling 0.5

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Patrick Mahomes + Kenneth Walker III** — 69.3% × 63.5% ≈ 44.0% of the field (~20,927 lineups of 47,562)
- **Patrick Mahomes + Jonathan Taylor** — 69.3% × 55.8% ≈ 38.7% of the field (~18,406 lineups of 47,562)
- **Kenneth Walker III + Jonathan Taylor** — 63.5% × 55.8% ≈ 35.4% of the field (~16,837 lineups of 47,562)
- **Patrick Mahomes + Daniel Jones** — 69.3% × 42.3% ≈ 29.3% of the field (~13,936 lineups of 47,562)
- **Patrick Mahomes + Xavier Worthy** — 69.3% × 39.2% ≈ 27.2% of the field (~12,937 lineups of 47,562)
- **Kenneth Walker III + Daniel Jones** — 63.5% × 42.3% ≈ 26.9% of the field (~12,794 lineups of 47,562)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Patrick Mahomes** — $10,000, 69.3% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Spencer Shrader** — $4,600, 23.8% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Harrison Butker** — $5,000, 27.4% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Travis Kelce** — $6,200, 37.5% own: the crowd pays 2 ranks more ownership than his projection earns (owned ahead of projection).
- **Xavier Worthy** — $5,400, 39.2% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).
- **Daniel Jones** — $9,200, 42.3% own: the crowd pays 1 rank more ownership than his projection earns (owned ahead of projection).

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
