# Slate bundle — MMA
_Generated 2026-08-08 12:09 · slug `mma_se` · sport `mma`_

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/mma_se.md`.

## Contests
- 2 contest(s), 101 total entries
  - **UFC $8K Flying Knee ($2K to 1st)** (SE): field 784, my entries 1/1, prize multiple 0.85x
  - **UFC $20K mini-MAX** (150-Max): field 47,562, my entries 100/150, prize multiple 0.84x
_**LARGE-FIELD CONTEST(S) DECLARED** (UFC $20K mini-MAX (150-Max)) — the strategy MUST include the `## Field attack plan` section (see CLAUDE.md): the large-field game is exploiting the field's recurring mistakes, entry by entry. The small-field guidance below still applies to any SE/3-Max/5-Max contests on the same slate — the two games never blend._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Field tendencies — how the field plays YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's enough history, else by contest type). The field reliably piles into these — that is where leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface it as a tension; do NOT tell the user to fade anyone.
- **SE** (across your 7 past SE contests): SHAPE: the field reliably piles onto ~8 names per contest, arriving around 39.8% ownership (range 33.3-51.9%); its 8 past crowd name(s) are NOT on this card — apply the shape to THIS card's consensus favorites (sized in `## Chalk combos`); from the full-field captures (2 contests): only **79.3% of entries were unique rosters**, the most-copied lineup appeared **11 times**, the average opponent entered **1.0 lineups**, **100.0% of opponents were single-entry**, the top-3 chalk players landed together in **9.1%** of lineups, **2.5%** of entries carried a structurally dead build.

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 6 | 2/6 | 30.4 | 26.67 | 0.53 | ~30.4% own/slot |

## Process trend — your last 5 slates (oldest → newest)
FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure climbing, the same shark-gap axis) is a process leak the strategy below should account for. GPP guard: one bad percentile is variance, not signal.
- **Best percentile:** 1.3 → 26.1 → 2.3 → 3.5 → 11.6
- **Leverage capture** (slate-defining low-owned plays we rostered): 60% → 0% → — → — → 50%
- **Bust exposure** (top underperformers we rostered): — → — → — → — → —
- **Recurring shark-gap axis:** `own_per_slot` was your biggest structural gap vs the pros in 3 of the last 5 slates.
- **Own-strategy adherence:** fade calls violated per slate: 0 → 0 → 0 (0 = you followed your own fades).
- **Player-pool tier calibration:** tier ordering held in 0 of 2 graded slates — the board's boundaries are suspect.

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-08__MMA Matchups 8.8.26.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/mma_se/2026-08-08__MMA Top Plays 8.8.26.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### DailyFan MMA — `DailyFan-Projections-Sheet-MMA-DK-62.csv` (24 players)
| name | salary | ownership | proj_points | win_prob | opponent |
| --- | --- | --- | --- | --- | --- |
| Quillan Salkilld | 8300 | 42.0 | 72.01 | 0.5467 | Mateusz Gamrot |
| Mateusz Gamrot | 7900 | 53.0 | 66.96 | 0.4533 | Quillan Salkilld |
| Diego Ferreira | 8700 | 24.0 | 70.57 | 0.6106 | Billy Quarantillo |
| Billy Quarantillo | 7500 | 29.0 | 54.72 | 0.38939999999999997 | Diego Ferreira |
| Yadier del Valle | 9600 | 34.0 | 91.82 | 0.8567 | Darren Elkins |
| Darren Elkins | 6600 | 7.0 | 27.5 | 0.1433 | Yadier del Valle |
| Alexia Thainara | 8800 | 32.0 | 74.61 | 0.6947 | Amanda Lemos |
| Amanda Lemos | 7400 | 15.0 | 38.86 | 0.3053 | Alexia Thainara |
| Ty Miller | 9200 | 33.0 | 79.97 | 0.7653 | Billy Ray Goff |
| Billy Ray Goff | 7000 | 14.0 | 42.45 | 0.2347 | Ty Miller |
| Steven Asplund | 9000 | 36.0 | 78.4 | 0.7269 | Guilherme Pat |
| Guilherme Pat | 7200 | 14.0 | 35.78 | 0.2731 | Steven Asplund |
| Diyar Nurgozhay | 8400 | 29.0 | 63.42 | 0.5798 | Bruno Lopes |
| Bruno Lopes | 7800 | 23.0 | 49.29 | 0.4202 | Diyar Nurgozhay |
| Louie Sutherland | 8500 | 32.0 | 63.6 | 0.6548 | Jose Montanha |
| Jose Montanha | 7700 | 23.0 | 45.8 | 0.3452 | Louie Sutherland |
| Manoel Sousa | 9100 | 31.0 | 74.3 | 0.7328 | Richie Miranda |
| Richie Miranda | 7100 | 16.0 | 41.84 | 0.2672 | Manoel Sousa |
| Miles Johns | 8600 | 16.0 | 60.77 | 0.6106 | Gianni Vazquez |
| Gianni Vazquez | 7600 | 25.0 | 49.32 | 0.38939999999999997 | Miles Johns |
| Juliana Miller | 8900 | 29.0 | 74.13 | 0.7243999999999999 | Ravena Oliveira |
| Ravena Oliveira | 7300 | 9.0 | 36.89 | 0.2756 | Juliana Miller |
| Carol Foro | 9300 | 14.0 | 71.5 | 0.6668000000000001 | Gigi Canuto |
| Gigi Canuto | 6900 | 20.0 | 41.7 | 0.3332 | Carol Foro |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Darren Elkins — $6,600, 7% own, proj 27.5, ceiling 100.6
- Ravena Oliveira — $7,300, 9% own, proj 36.9, ceiling 86.4

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Mateusz Gamrot + Quillan Salkilld** — 53.0% × 42.0% ≈ 22.3% of the field (~10,606 lineups of 47,562)
- **Mateusz Gamrot + Steven Asplund** — 53.0% × 36.0% ≈ 19.1% of the field (~9,084 lineups of 47,562)
- **Mateusz Gamrot + Yadier del Valle** — 53.0% × 34.0% ≈ 18.0% of the field (~8,561 lineups of 47,562)
- **Mateusz Gamrot + Ty Miller** — 53.0% × 33.0% ≈ 17.5% of the field (~8,323 lineups of 47,562)
- **Mateusz Gamrot + Alexia Thainara** — 53.0% × 32.0% ≈ 17.0% of the field (~8,086 lineups of 47,562)
- **Mateusz Gamrot + Louie Sutherland** — 53.0% × 32.0% ≈ 17.0% of the field (~8,086 lineups of 47,562)

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
