# CLAUDE.md — DFS Slate Analyzer

Article-driven, multi-sport DFS slate-strategy tool for DraftKings. Streamlit web app. Personal-use, single user (`ryanjsieb30`).

## What this is

A pre-slate / post-slate **slate-strategy** tool for **PGA Classic, PGA RD4 Showdown, MMA, NASCAR, MLB Classic**. The user uploads the slate's **articles** (PDFs, notes, data files, screenshots) AND vendor **projections**, and Claude synthesizes a written **slate strategy**: top plays, how to approach the slate, key themes, leverage & fades, and the decisions that define the slate. After the contest, the user uploads DK contest-standings and the Analyzer drives a post-mortem + learning loop.

**No lineup building. No selecting, ranking, red-teaming, or fixing lineups.** Lineup construction lives solely in the separate sim tool. This tool is a strategy doc the user hand-builds from — the **slate strategy is derived from everything uploaded (articles + every loaded vendor projection)**, cross-checked against the strategy docs. The **autopsy stays standings-only** (no projections exist at autopsy time).

There is a **Projections** tab for uploading vendor projection CSVs (auto-detected, stored per slate). Besides storing/viewing them it computes a **Breakdown** that surfaces non-obvious edges (chalk tiers + concentration, leverage board, ownership-vs-ceiling mispricing, value-by-tier, AM/PM tee-wave split, boom/bust, auto-flagged "edges to notice", and cross-vendor disagreement when ≥2 sources are loaded). The loaded projections are **also folded into the bundle** so the slate strategy reads them alongside the articles. The autopsy still does NOT read projections.

Six tabs: **Projections → Slate Data → Slate Strategy → Sim Data → Autopsy → Trends**. **Sim Data** ingests a SaberSim lineup-pool export and surfaces, for any sport, the sim's good plays / bad plays, sim-vs-field leverage, and **chalky combinations** of players — **analytics only, it NEVER builds or picks lineups** (combinations are duplication/leverage signal, not lineups to play). Trends is a cross-sport, read-only "where you win" view — best-percentile by contest type + field size. The Slate Strategy tab also has a **Player pool** below the written strategy — a Claude-generated, ranked, annotated board of every rosterable player (loaded projections minus the fades the strategy names), each with a short GPP write-up. Built automatically as part of the slate-strategy generation (no separate button).

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
.venv/bin/streamlit run app.py --server.port 8601    # http://localhost:8601
```

The venv is at `.venv/`. Python 3.9 (system Python). Streamlit, pandas. **Restart the server after any code change** — Streamlit caches `src` modules.

## Architecture

| Path | Purpose |
|---|---|
| `app.py` | Streamlit UI: 4 tabs (Projections, Slate Data, Slate Strategy, Autopsy) |
| `src/projections.py` | Vendor CSV loader → canonical schema (`load_projections`, `warn_missing_for_sport`); powers the Projections tab only |
| `src/vendors.py` | Vendor signature auto-detection (ETR / Ship It Nation / DailyFan / DK) |
| `src/sessions.py` | Per-slug projection session at `data/sessions/<slug>.json` (`save_source` / `load_sources` / `drop_source` / `merge_same_vendor` / `clear`); cleared with the slate |
| `src/landscape.py` | Projections-tab Breakdown: chalk tiers, leverage board, ownership-vs-ceiling mispricing, value-by-tier, tee-wave split, boom/bust, anchor-equivalence, `breakdown_flags`. **Ceiling-based panels (upside / boom_pct / mispricing-vs-ceiling / ceiling-per-$1k / Boom / Fragile) render ONLY when the vendor ships a real `ceiling` column** (`has_real_ceiling`) — golf (ETR/Ship It) + MLB (95th pct). For NASCAR (DailyFan) and names-only vendors there is no ceiling, so `_upside` returns plain `proj_points` (no fabricated `proj×1.28×stddev`) and those panels are hidden. Never fabricate a ceiling for display |
| `src/projections_diff.py` | Cross-vendor projection disagreement (`flagged_disagreements`) — shown when ≥2 sources loaded |
| `src/player_pool.py` | **Player pool** (Slate Strategy tab, below the written strategy): a Claude-generated **ranked, annotated board**. Membership is computed deterministically — the rosterable universe from the loaded projections (`build_pool`) minus the fades named in the strategy's `## Leverage & fades` → Fades subsection (`extract_fades` / `apply_fades`) — then `analysis_runner.run_player_pool` runs `claude -p` to rank those exact players + write a short write-up each from the documents. **Runs automatically right after `run_analysis`** when the "Generate slate strategy + player pool" button is clicked (chained in app.py; no separate button) — needs projections loaded + the strategy just written for fades. Persisted at `data/player_pool/<slug>.md` (`load_pool`/`save_pool`/`clear_pool`); cleared + archived with the slate |
| `src/contests.py` | Per-sport contest registry at `data/contests/<slug>.json` |
| `src/contest_templates.py` | Reusable saved-contest templates per slug |
| `src/bundle.py` | `build_bundle` — consolidates the declared contests + the `articles/<slug>/` file paths + strategy-doc paths into `data/bundle/<slug>.md` for Claude to read |
| `src/analysis_runner.py` | `run_analysis` (writes the slate strategy) + `run_autopsy_review` + `run_apply_proposals` — build the bundle and run `claude -p` headlessly (subscription auth). Power the Slate Strategy tab's "Generate slate strategy" button and the Autopsy tab's review/approve buttons |
| `src/slate_analysis.py` | Persisted slate-strategy read/write/clear at `data/slate_analysis/<slug>.md` |
| `src/strategy.py` | Loads per-sport philosophy/framework/autopsies + recent lessons (no UI tab) |
| `src/ledger_hygiene.py` | **Lesson-ledger hygiene** (Autopsy tab): deterministic flags over `lessons.yaml` — `stale_hypotheses` (0 confirmations, had their shot), `near_promotion` (2/3 confirming slates), `overdue_promotion` (≥3, not codified), `merge_candidates` (`[[id]]` cross-links or token overlap), `hygiene_report` + `report_md`. Feeds `analysis_runner.run_ledger_review` → `rules/<slug>/ledger_review.md` (proposals) → `run_apply_ledger_proposals` (user-approved) |
| `src/autopsy.py` | DK contest-standings parser + structural analysis (works from standings alone, no projections) |
| `src/accuracy.py` | Self-grade: did our ENTERED lineups capture the leverage / slate-defining plays (graded against DK actuals) |
| `src/shark_gap.py` | Structural us-vs-sharks fingerprint for a contest's standings |
| `src/history.py` | Per-slate archive (`rules/<slug>/history/`) + cross-slate results ledger (`rules/<slug>/results.jsonl`) — written by the Autopsy tab's Log button BEFORE the workspace clears |
| `src/sim_data.py` | **Sim Data tab** analytics (deterministic, all sports): parse a SaberSim lineup-pool CSV (`load_sim_pool` — auto-detects roster slots), per-player `player_exposure` (sim exposure % + field own join), `good_bad_plays` (sim core / sim fades / leverage / traps), `chalky_combinations` (top co-occurring pairs/trios = duplication risk). **Analytics only — never assembles a lineup.** |
| `src/dk_ids.py` | Resolve SaberSim DK ids → names: `parse_id_to_name` (DK Name+ID file), `id_to_name_from_projections` (loaded projections' `dk_id`), `resolve_id_to_name` (projections first, upload fills gaps). Reuses `autopsy._norm_name` |
| `src/sim_sessions.py` | Persist the uploaded sim pool + DK map per slug at `data/sim_data/<slug>__pool.csv`; Claude summary at `data/sim_analysis/<slug>.md`; cleared with the slate |
| `src/contest_selection.py` | **Trends tab** (cross-sport, read-only): flattens every `results.jsonl` into one row per contest, buckets best-percentile by contest **type** + **field-size** (`load_contest_rows` / `by_type` / `by_field_bucket` / `where_you_win`) so the user sees which contest shapes pay them. Best-percentile is the scoreboard; ROI is a coverage count only (usually null) |
| `articles/<slug>/` | Per-contest-type "Slate Data" uploads — PDFs, notes, data CSVs, and photos/screenshots (e.g. DailyFan). Tab label is "Slate Data"; the on-disk dir stays `articles/`. Per-slate: deleted on autopsy log and on the sidebar "Clear this sport's slate" button (filenames survive in the archive's `manifest.json`) |
| `rules/<slug>/` | Philosophy / framework / autopsies docs per contest type — Claude reads these as context (no UI tab; surfaced via the bundle) |
| `rules/<slug>/lessons.yaml` | The lesson ledger — structured lessons with a lifecycle (hypothesis → validated → codified/retired). Claude-edited during the post-autopsy review; user approves codifications |
| `rules/<slug>/history/` | One folder per archived slate: manifest, slate strategy, bundle, contests, autopsy records, results, and the autopsy review |
| `rules/<slug>/results.jsonl` | Append-only, app-written results ledger (one row per slate: buy-in, winnings, ROI, best percentile). Claude reads it, never edits it. **Winnings/ROI fields are OPTIONAL and usually null — the user tracks ROI in a third-party app.** Never ask to backfill winnings and never grade missing winnings as a process miss; the in-repo scoreboard is best-percentile trend + process metrics |
| `rules/{nascar/tracks,pga_classic/courses,mlb_classic/parks}/` | Venue knowledge — one file per track/course/park, accumulating date-stamped per-slate observations. Both PGA slugs share `pga_classic/courses/` |
| `data/bundle/` | `<slug>.md` — the consolidated "Bundle for Claude" written from the Slate Strategy tab |
| `data/slate_analysis/` | `<slug>.md` — the written slate strategy Claude produces |

## Contest types

| Sidebar selector | `slug` | Sport | Notes |
|---|---|---|---|
| PGA Classic | `pga_classic` | golf | 6 golfers, 2 days + cut |
| PGA RD4 Showdown | `pga_rd4_sd` | golf | 6 golfers, **flat — NO captain, NO 1.5x** |
| MMA | `mma_se` | mma | SE rules |
| NASCAR | `nascar` | nascar | 6 drivers; **always check `rules/nascar/tracks/<slug>.md`** |
| MLB Classic | `mlb_classic` | mlb | 10 players (P, P, C, 1B, 2B, 3B, SS, OF×3), $50K; **team-stack driven** |

## Workflow per slate

1. **Slate Data** — upload everything for the slate: article PDFs, notes (`.txt`/`.md`), misc data CSVs (vegas odds, course/track history, matchup data, DailyFan exports), and photos/screenshots. These are the only input the strategy reads.
2. **Slate Strategy** — declare your contests (field size frames how contrarian to be), then click **Generate slate strategy** — the app builds the bundle and runs `claude -p` headlessly to write + render the strategy (no chat needed).
3. *(After the contest ends)* **Autopsy** — upload DK contest-standings CSV(s), link each to its declared contest (winnings optional — ROI is tracked in the user's third-party app), view the field summary / your entries / winners-vs-you / leverage capture / shark gap (all from standings, no projections), and log lessons to `rules/<slug>/autopsies.md`. **Log autopsy** archives the slate to `rules/<slug>/history/<date>__<slate>/` and appends `rules/<slug>/results.jsonl` before clearing the workspace.
4. **Post-autopsy review** — click **Run post-autopsy review** (Autopsy tab): grades the process, updates `lessons.yaml` + the venue file, proposes framework changes. Click **Approve & apply proposals** to accept them.

## Writing the slate strategy

This normally runs **in-app**: the Slate Strategy tab's **Generate slate strategy** button calls `src/analysis_runner.py::run_analysis`, which builds the bundle and invokes `claude -p` headlessly (subscription auth, no API key) to read the bundle + referenced files and write `data/slate_analysis/<slug>.md`. That headless Claude loads this `CLAUDE.md` and follows the steps below. The same can be triggered manually from chat (fallback): click the button once to build the bundle, then ask **"read the bundle and write the slate strategy"**. Either way:

1. Read the bundle: `data/bundle/<slug>.md` — it lists the declared contests, absolute paths to every `articles/<slug>/` file, the `## Projections` tables (every loaded vendor), and the strategy-doc paths. Start here.
2. Read every slate-data file it lists under `articles/<slug>/` — `*.pdf`, `*.txt`/`*.md`, `*.csv` (misc data like vegas odds or course/track history — read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (use the Read tool — it reads images visually, so DailyFan screenshots work; PDFs may require poppler — note in the file if anything couldn't be parsed). Then read the `## Projections` tables in the bundle — every loaded vendor's ownership/projections.
3. Read strategy: `rules/<slug>/{philosophy,framework,autopsies}.md` + `rules/shared/anchor_equivalence.md` + `rules/shared/sharp_playbook.md` (paths are in the bundle).
4. Read recent autopsies: tail of `rules/<slug>/autopsy_data.jsonl`.
5. For NASCAR: also read `rules/nascar/tracks/<track>.md`.
6. Synthesize from the ARTICLES **and the projections together**, cross-checked against the framework + open lessons:
   - What do the articles + projections surface as the top plays, and where do they DISAGREE — article vs article, vendor vs vendor, or article vs projection (that disagreement is the edge)?
   - Which qualitative reads should drive the build, and where do the projection numbers confirm or challenge them? What's the Anchor-Equivalence call?
   - Which framework rules / open lessons activate?
7. Write to `data/slate_analysis/<slug>.md` in the format below. It renders in the Slate Strategy tab with a "Last updated" timestamp and is cleared automatically when the user logs an autopsy.

**Coverage rule:** read EVERY uploaded slate-data file — every article PDF, note, data CSV, AND photo/screenshot — never silently skip one. Both generated outputs must make coverage visible: the slate strategy's pre-flight checklist states how many files were read and lists any it couldn't parse; the Player pool ends with a `## Sources read` line doing the same.

**Source-of-truth rule:** synthesize from EVERYTHING uploaded — the articles AND every loaded vendor projection — cross-checked against the framework and open lessons. Blend the qualitative article reads with the projection ownership/projections; cite each number from its source (name the **article OR the vendor**). Where vendors disagree with each other, or a vendor disagrees with the articles, surface that gap — it is leverage signal. Write **no lineup tables** and build **no rosters**; this is a strategy doc the user hand-builds from.

**Leverage-coverage rule:** when projections are loaded, the bundle includes a `## Leverage candidates to address` section — the sub-10%-owned, high-ceiling plays (`src/landscape.py::leverage_candidates`). **Every** listed player MUST appear in the slate strategy's `## Leverage & fades` or `## Decisions` as an explicit PLAY or PASS with a one-line mechanism, and the Player pool must confirm each in its `## Leverage candidates addressed` footer (ranked or faded-with-reason). A sub-10% high-ceiling play left unmentioned is a coverage leak — the play that decides the slate from nowhere (the Kaan Ofli failure, 6/27 Baku). The app shows a **coverage-gap warning** if the rendered strategy omits any candidate.

### Slate strategy format (mandatory, all sports)

The file contains these sections, in order. GPP-framed throughout; concise and scannable.

1. `## Pre-flight checklist` — first, always (see Pre-flight ritual).
2. `## Slate at a glance` — brief facts table from the articles + projections (games/fights/races, implied totals or win probs, weather, contests + field sizes). Keep it short.
3. `## Top plays` — tiered (e.g. core / pivots / darts). Each play: the **cited ownership** (name the source — article or vendor) + a one-line WHY.
4. `## How to approach the slate` — the plain-English game plan for a hand-builder: what the winning shape looks like, how chalk-vs-contrarian to lean (field-size aware), the sharp-envelope target (≥1 sub-5% leverage piece, ceiling over median, all-unique lineups).
5. `## Key themes` — the structural storylines, INCLUDING **where the articles disagree** with each other — name both sides and which you trust and why.
6. `## Leverage & fades` — the underowned plays worth the leverage and the chalk worth fading, each with the mechanism (a fade is a bet — price the world it needs).
7. `## Decisions` — 2–5 PLAY/PASS/MIX calls, in priority order, each with a one-sentence mechanism. The **Anchor-Equivalence call MUST appear here** as one of the decisions.

## Pre-flight ritual (mandatory — every slate strategy)

Before writing `data/slate_analysis/<slug>.md`, in order:

1. **Confirm the slate.** Compare the bundle's generation timestamp and the article file dates against today. If the articles look like a prior slate (stale dates), SAY SO in the checklist instead of analyzing stale data. The current slate's articles drive everything; past results are reference only.
2. **Read the venue file** (nascar → `rules/nascar/tracks/`, golf → `rules/pga_classic/courses/` for BOTH pga slugs, mlb → `rules/mlb_classic/parks/`; mma has none). If missing, create a stub from this slate's articles, mark it `**UNVERIFIED — built from this slate's articles only**`, and flag it in the checklist.
3. **Read `rules/<slug>/lessons.yaml`.** Every lesson with status `hypothesis` or `validated` must be either applied (name where) or rejected (name the mechanism reason). Codified lessons live in framework.md already; retired ones are ignored.
4. **Run the framework pre-lock checks** for the sport, always including Anchor-Equivalence (`rules/shared/anchor_equivalence.md`).
5. **Scan `rules/<slug>/results.jsonl`** (last 3 slates) for recent process notes.
6. **Note the universal sharp principles** (`rules/shared/sharp_playbook.md` — reverse-engineered from 12 elite players' DK standings) as the target envelope for the hand-builder: every lineup unique; ≥1 sub-5%-owned leverage piece in most; ~12–16% average ownership per roster slot (sport-calibrated); an elite anchor with downstream differentiation; judged on ceiling, not median.
7. **Open the output file with the `## Pre-flight checklist` block** — each line checked `[x]` with specifics or unchecked `[ ]` with the reason. No checklist block, no valid output.

Checklist format example:

```markdown
## Pre-flight checklist
- [x] Slate confirmed: nascar — Nashville Superspeedway — bundle generated 2026-05-31 14:02; article dates match
- [x] Venue file read: rules/nascar/tracks/nashville_superspeedway.md
- [x] Open lessons reviewed: 4 open — applied: spread-dominators (Decision 2); rejected: sleeper-spike (mechanism needs carnage, low-DNF track)
- [x] Framework pre-lock checks: Anchor-Equivalence → Bell/Reddick at similar own per the articles, run the alternative; ceiling-threshold OK
- [x] Prior results scanned: results.jsonl (last 3 slates; ROI sample too small to read)
- [x] Sharp envelope noted: target ≥1 sub-5% piece, ~13% avg own/slot, elite anchor + differentiation, all-unique
```

## Lesson ledger (`rules/<slug>/lessons.yaml`)

Structured lessons with a lifecycle: `hypothesis` → `validated` → `codified` (or `retired`). Each lesson: `id`, `born` date, `origin` (history dir), `statement`, `status`, `confirmations[]`, `contradictions[]`, `codified_in`, `retired_reason`.

- Claude updates evidence/status during the post-autopsy review.
- **Codifying into framework.md/philosophy.md and retiring both require user approval** — the review writes proposals; the user clicks "Approve & apply" in the Autopsy tab.
- Promotion criteria: 3 total confirming slates (origin + 2 confirmations of the MECHANISM, not just the result) → propose codifying. 2 mechanism contradictions → propose retiring.
- **GPP guard: a lost contest is never evidence by itself** — only mechanism confirmations/contradictions count. Variance is the game.

### Lesson-ledger hygiene (Autopsy tab)

As ledgers grow past ~20 lessons/sport, the **Lesson-ledger hygiene** block (Autopsy tab, below the post-autopsy review) keeps them sharp. `src/ledger_hygiene.py` computes deterministic flags instantly — **stale** hypotheses (0 confirmations that have had ≥3 logged slates or ≥30 days), **near-promotion** (2 of 3 confirming slates), **overdue promotion** (≥3 confirming slates, not yet codified), and **merge candidates** (`[[id]]` cross-links or high statement-token overlap). The **🧹 Review ledger** button runs `claude -p` to turn those flags into reasoned proposals at `rules/<slug>/ledger_review.md` (retire / keep / merge / codify, each with a mechanism), editing nothing; **✅ Approve & apply ledger changes** then applies the approved decisions to `lessons.yaml` (+ framework/philosophy for codifications). Same approve-gate + GPP guard as the post-autopsy review: a lesson untested only because no relevant slate occurred is KEEP, not retire.

New ledger file header (when creating lessons.yaml for a sport):

```yaml
# Lesson ledger — one entry per generalizable lesson. Claude edits during the
# post-autopsy review; the user approves codifications/retirements.
# Lifecycle: hypothesis -> validated -> codified | retired.
# Promotion: 3 mechanism confirmations -> propose codifying into framework.md.
# Retirement: 2 mechanism contradictions -> propose retiring.
# GPP guard: a lost contest is NOT a contradiction; only mechanism failures count.
lessons: []
```

## Post-autopsy ritual

Triggered by the Autopsy tab's **Run post-autopsy review** button after **Log autopsy** (which archives the slate to `rules/<slug>/history/<date>__<slate>/` and appends `rules/<slug>/results.jsonl`). The autopsy runs from **DK contest-standings alone** — there are no projections, so there are no proj-vs-actual or vendor-calibration panels. The headless review run:

1. Grades the archived slate's process (checklist honesty, lessons applied vs ignored) and whether the slate strategy's Top plays / PLAY-PASS-MIX decisions held up against the DK actuals (slate-defining low-owned plays, your entries vs the winners, shark gap).
2. Updates `lessons.yaml` evidence/statuses and births new hypotheses (mechanism-based, not result-based).
3. Updates/creates the venue file with a date-stamped per-slate observation.
4. Writes `<history_dir>/autopsy_review.md` with `## Process scorecard`, `## Lesson ledger changes`, `## Venue file changes`, `## Proposed codifications` — proposed (NOT applied) framework changes; the user approves via the app.

The slate's scoreboard is **best-percentile trend + process/mechanism metrics** — ROI is tracked in the user's third-party app, so winnings/ROI in `results.jsonl` are optional and usually null. Never flag missing winnings as a gap, never ask the user to backfill them, and never conclude from ROI even when present (high-variance GPP data).

## Hard rules

- **NEVER create lineups.** This tool builds NO lineups — ever. This includes the **Sim Data tab**: it reads an uploaded SaberSim pool and reports individual-player exposures + chalky **combinations** (duplication/leverage signal) — it must NEVER assemble, rank, or suggest a full lineup, and the `run_sim_review` summary names individual plays + combos-to-fade only. Both generated outputs name **individual plays only**: the slate strategy writes no roster tables / sample builds / "core build" groupings, and the Player pool is a board of single players ranked independently (never combined into a roster, stack, or pairing presented as a build). Applies to in-app generation AND chat sessions. Lineup construction lives solely in the separate sim tool.
- **Slate strategy = everything uploaded (articles + every loaded vendor projection); autopsy stays standings-only.** The generated slate strategy synthesizes the uploaded articles AND the loaded projections (folded into the bundle), cross-checked against the strategy docs. The **autopsy** still derives from DK contest-standings alone — there are no projections at autopsy time. The **Projections tab** is also a standalone upload/reference store — but no sim/lineup pools, no lineup building/selecting/ranking/red-teaming/fixing (that lives in the sim tool).
- **No scraping.** DK ToS prohibits it; never build scrapers. Use user-pasted/uploaded data only.
- **GPP-only framing.** Leverage / ceiling / contrarian. Never propose cash-game features.
- **Anchor-Equivalence Rule** is a **mandatory call** in every slate strategy's `## Decisions`. 4-slate-validated structural leak: if 2+ chalk-tier anchors at similar ownership (per the articles), the build must run the alternative.
- **Venue check before any strategy**: read the sport's venue file (NASCAR tracks / PGA courses / MLB parks) per the Pre-flight ritual. For NASCAR specifically, if `rules/nascar/tracks/<slug>.md` is missing, proactively ask the user for the track description.
- **Pre-flight ritual is mandatory** for every slate strategy — chat sessions included, not just headless runs.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x multiplier**. Never reference "CPT" for this contest type. Position is the live to-par leaderboard score, never the tee time.
- **No NFL/NBA.** Out of scope. (MLB Classic is supported as of 2026-06.)
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.

## Useful file paths

- **Sample DK contest-standings**: `~/Downloads/contest-standings-190402324.csv`
- **GitHub**: https://github.com/ryanjsieb30DFS/ryanjsieb30DFS-Analyzer (`main` branch)
