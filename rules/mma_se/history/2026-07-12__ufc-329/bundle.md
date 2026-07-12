# Slate bundle — MMA
_Generated 2026-07-11 12:46 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 2 total entries
  - **UFC $10K Counter Punch** (SE): field 291, my entries 1/1
  - **UFC $10K Counter Jab** (5-Max): field 291, my entries 1/5
_Field size frames how contrarian the read should be — bigger field → more ceiling/leverage; smaller field → tighter, higher-floor calls._

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-11__DF Matchups 7.11.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-11__DF Top Plays 7.11.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-50.csv` (28 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Max Holloway | 9000 | 45.0 | 80.76 | 0.6612 | Conor McGregor |
| Conor McGregor | 7200 | 28.0 | 53.82 | 0.33880000000000005 | Max Holloway |
| Benoit Saint Denis | 8500 | 36.0 | 72.58 | 0.5851 | Paddy Pimblett |
| Paddy Pimblett | 7700 | 29.0 | 56.89 | 0.41490000000000005 | Benoit Saint Denis |
| Cory Sandhagen | 8300 | 18.0 | 66.49 | 0.5427000000000001 | Mario Bautista |
| Mario Bautista | 7900 | 17.0 | 54.96 | 0.4573 | Cory Sandhagen |
| Lone'er Kavanagh | 8800 | 17.0 | 70.12 | 0.6675 | Brandon Royval |
| Brandon Royval | 7400 | 15.0 | 47.25 | 0.3325 | Lone'er Kavanagh |
| Terrance McKinney | 8400 | 46.0 | 67.31 | 0.5325 | King Green |
| King Green | 7800 | 28.0 | 48.64 | 0.4675 | Terrance McKinney |
| Robert Whittaker | 8700 | 16.0 | 57.475 | 0.5174 | Nikita Krylov |
| Nikita Krylov | 7500 | 29.0 | 51.98 | 0.4826 | Robert Whittaker |
| Gable Steveson | 9900 | 34.0 | 102.25 | 0.9201999999999999 | Elisha Ellison |
| Elisha Ellison | 6300 | 2.0 | 12.22 | 0.07980000000000001 | Gable Steveson |
| Adrian Yanez | 9400 | 17.0 | 76.63 | 0.7864 | Cody Garbrandt |
| Cody Garbrandt | 6800 | 9.0 | 33.61 | 0.21359999999999998 | Adrian Yanez |
| Luke Riley | 9300 | 11.0 | 72.74 | 0.6620999999999999 | Kai Kamaka III |
| Kai Kamaka III | 6900 | 14.0 | 51.28 | 0.3379 | Luke Riley |
| Wang Cong | 8200 | 16.0 | 56.97 | 0.4892 | Tracy Cortez |
| Tracy Cortez | 8000 | 21.0 | 61.19 | 0.5108 | Wang Cong |
| Damian Pinas | 8900 | 26.0 | 70.79 | 0.698 | Cesar Almeida |
| Cesar Almeida | 7300 | 15.0 | 42.19 | 0.302 | Damian Pinas |
| Farid Basharat | 9600 | 15.0 | 82.99 | 0.8293 | John Garza |
| John Garza | 6600 | 7.0 | 36.23 | 0.1707 | Farid Basharat |
| Ryan Gandra | 8600 | 29.0 | 64.23 | 0.5564 | Zach Reese |
| Zach Reese | 7600 | 27.0 | 52.76 | 0.4436 | Ryan Gandra |
| Alessandro Costa | 9100 | 20.0 | 73.51 | 0.6620999999999999 | Cody Durden |
| Cody Durden | 7100 | 13.0 | 43.58 | 0.3379 | Alessandro Costa |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Decisions` AND the player pool must explicitly PLAY or PASS **each** player below, each with a one-line mechanism. Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Elisha Ellison — $6,300, 2% own, proj 12.2, ceiling 102.2
- John Garza — $6,600, 7% own, proj 36.2, ceiling 90.5
- Cody Garbrandt — $6,800, 9% own, proj 33.6, ceiling 90.3

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/mma_se/results.jsonl` — cross-slate results ledger (process notes only)

**Output target:** write the slate strategy to `data/slate_analysis/mma_se.md`.
