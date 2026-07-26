# Slate bundle — MMA
_Generated 2026-07-24 19:42 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 2 total entries
  - **UFC $5K Flying Knee** (SE): field 490, my entries 1/1, payout **Top-heavy**, prize multiple 0.85x
  - **UFC $5K Clinch** (SE): field 1,189, my entries 1/1, prize multiple 0.84x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## How to approach the slate`; never a play/fade command._
_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **SE** (across your 4 past SE contests): the field reliably crowds **Damian Pinas (in 2 of 4), Paddy Pimblett (in 2 of 4), King Green (in 2 of 4), Terrance McKinney (in 2 of 4), Ryan Gandra (in 2 of 4), Benoit Saint Denis (in 2 of 4), Gable Steveson (in 2 of 4), Max Holloway (in 2 of 4)**; recurring fish-traps: **Conor McGregor (in 2 of 4), Nikita Krylov (in 2 of 4), Cory Sandhagen (in 2 of 4), Terrance McKinney (in 2 of 4), Zach Reese (in 2 of 4), Benoit Saint Denis (in 2 of 4), Kai Kamaka III (in 2 of 4), Seokhyeon Ko (in 2 of 4)**; the field PAIRS **Max Holloway + Paddy Pimblett (in 2 of 4), Max Holloway + Terrance McKinney (in 2 of 4), King Green + Max Holloway (in 2 of 4), Kamaru Usman + Tommy McMillen (in 2 of 4), Austin Bashi + Tommy McMillen (in 2 of 4)** — a dupe-magnet stack; leverage lives in breaking it.

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 0.2 → 1.7 → 1.3 → 26.1 → 2.3
- **Leverage capture** (slate-defining low-owned plays we rostered): — → 100% → 60% → 0% → —
- **Bust exposure** (top underperformers we rostered): 100% → 100% → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 2 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 (0 = you followed your own fades).

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-24__MMA Matchups 7.25.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-07-24__MMA Top Plays 7.25.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-55.csv` (26 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Magomed Ankalaev | 9500 | 27.0 | 84.26 | 0.8181999999999999 | Bogdan Guskov |
| Bogdan Guskov | 6700 | 21.0 | 32.23 | 0.1818 | Magomed Ankalaev |
| Steve Erceg | 8200 | 21.0 | 56.92 | 0.5 | Ramazan Temirov |
| Ramazan Temirov | 8000 | 28.0 | 60.43 | 0.5 | Steve Erceg |
| Islam Dulatov | 9800 | 32.0 | 93.57 | 0.8756999999999999 | Wellington Turman |
| Wellington Turman | 6400 | 5.0 | 19.49 | 0.1243 | Islam Dulatov |
| Magomed Zaynukov | 9200 | 21.0 | 75.69 | 0.7106999999999999 | Damian Rzepecki |
| Damian Rzepecki | 7000 | 24.0 | 50.77 | 0.2893 | Magomed Zaynukov |
| Rizvan Kuniev | 9000 | 16.0 | 71.2 | 0.7428 | Tyrell Fortune |
| Tyrell Fortune | 7200 | 21.0 | 37.52 | 0.2572 | Rizvan Kuniev |
| Abubakar Vagaev | 8900 | 23.0 | 72.2 | 0.6728000000000001 | Saygid Izagakhmaev |
| Saygid Izagakhmaev | 7300 | 18.0 | 43.1 | 0.3272 | Abubakar Vagaev |
| Valter Walker | 8800 | 34.0 | 67.815 | 0.6429 | Thomas Petersen |
| Thomas Petersen | 7400 | 27.0 | 40.27 | 0.35710000000000003 | Valter Walker |
| Dustin Jacoby | 8700 | 21.0 | 62.31 | 0.6067 | Muhammad Saidov |
| Muhammad Saidov | 7500 | 29.0 | 51.43 | 0.3933 | Dustin Jacoby |
| Sam Patterson | 9400 | 32.0 | 80.04 | 0.8017 | Santiago Ponzinibbio |
| Santiago Ponzinibbio | 6800 | 16.0 | 30.79 | 0.19829999999999998 | Sam Patterson |
| Axel Sola | 8600 | 26.0 | 67.35 | 0.6620999999999999 | Ismael Bonfim |
| Ismael Bonfim | 7600 | 26.0 | 46.56 | 0.3379 | Axel Sola |
| Magomed Tuchalov | 9700 | 29.0 | 92.26 | 0.8791 | Brendson Ribeiro |
| Brendson Ribeiro | 6500 | 6.0 | 20.4 | 0.1209 | Magomed Tuchalov |
| Nurullo Aliev | 8500 | 28.0 | 70.09 | 0.6620999999999999 | Mike Davis |
| Mike Davis | 7700 | 26.0 | 47.03 | 0.3379 | Nurullo Aliev |
| Abdul Hussein | 9300 | 29.0 | 81.53 | 0.8088 | Cody Gibson |
| Cody Gibson | 6900 | 14.0 | 35.21 | 0.1912 | Abdul Hussein |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Brendson Ribeiro — $6,500, 6% own, proj 20.4, ceiling 98.0
- Wellington Turman — $6,400, 5% own, proj 19.5, ceiling 89.3

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Valter Walker + Sam Patterson** — 34.0% × 32.0% ≈ 10.9% of the field (~130 lineups of 1,189)
- **Valter Walker + Islam Dulatov** — 34.0% × 32.0% ≈ 10.9% of the field (~130 lineups of 1,189)
- **Sam Patterson + Islam Dulatov** — 32.0% × 32.0% ≈ 10.2% of the field (~121 lineups of 1,189)
- **Valter Walker + Abdul Hussein** — 34.0% × 29.0% ≈ 9.9% of the field (~118 lineups of 1,189)
- **Valter Walker + Magomed Tuchalov** — 34.0% × 29.0% ≈ 9.9% of the field (~118 lineups of 1,189)
- **Valter Walker + Muhammad Saidov** — 34.0% × 29.0% ≈ 9.9% of the field (~118 lineups of 1,189)

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
