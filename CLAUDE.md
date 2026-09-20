# CLAUDE.md — DFS Slate Analyzer

Article-driven, multi-sport DFS slate-strategy tool for DraftKings. Streamlit web app. Personal-use, single user (`ryanjsieb30`). Dated history behind every rule: `docs/changelog.md`.

**DRAFTKINGS ONLY — IGNORE FANDUEL (user directive 9/12/26: "ignore ignore ignore").** The user never plays FanDuel. Articles, ETR files, and research PDFs carry FD columns/sections/prices/ownership/advice; every prompt, digest, framework edit, and vendor profile drops them (`analysis_runner.DK_ONLY_NOTE` is prepended to every headless run; the bundle header repeats it; ETR vendor profiles drop `fd_*` columns). Never cite an FD number, never propose an FD-only rule.

## What this is

A pre-slate / post-slate **slate-strategy** tool for **PGA Classic, PGA RD4 Showdown, MMA, NASCAR, NFL Showdown, NFL Classic**. The user uploads the slate's **articles** (PDFs, notes, data files, screenshots) AND vendor **projections**; Claude writes a **slate strategy** synthesized from everything uploaded, cross-checked against the strategy docs. After the contest the user uploads DK contest-standings and the Analyzer runs a post-mortem + learning loop. Five tabs: **Projections → Slate Data → Slate Strategy (+ Player pool board) → ✅ Grade → Autopsy**.

- **No lineup building. No ranking, red-teaming, or fixing lineups** — construction lives solely in the Sim tool. The **autopsy is standings-only** (never requires projections; salary/proj fill best-effort from still-loaded projections, else None). The Projections tab stores vendor CSVs per slate, computes the **Breakdown** (chalk tiers, leverage board, own-vs-ceiling mispricing, value-by-tier, tee-wave split, boom/bust, edge flags, cross-vendor disagreement) and folds them into the bundle.
- **Selection is not construction.** The Analyzer NEVER authors, edits, swaps, or fixes a roster; PICKING among the Sim's already-built, already-simmed pool lineups is permitted in the Grade tab's per-contest flow ONLY (`src/lineup_selection.py` + `run_contest_selection`): claude reads that contest's candidate slice (real pool rows with THAT contest's sim numbers) + strategy + open lessons and picks exactly `my_entries` rows BY ID; `parse_pick` rejects fabricated ids, modified rosters, wrong counts, rosters already picked for another contest — a bad pick saves NOTHING.
- **The pick follows the slate strategy (user directive 8/15/26), as a GUIDE since 8/29/26:** every row carries its `cost`; a rule-breaking pick is accepted only as an explained OVERRIDE (logged to `rules/<slug>/strategy_overrides.jsonl`, scored by `override_outcomes`); a silent override is rejected. No strategy contract → no pick (button disabled).
- **One lineup, one contest (user directive 8/15/26, ALL sports):** a pool lineup is picked ONCE per slate; picked rosters are cut from every other contest's slice and re-rejected by roster identity.
- **Two opinions per contest (user directive 8/22/26):** the Sim pushes its DIVERSIFIED portfolio (`data/sim_entries/<slug>.json`); each contest shows it beside claude's pick, both A-F graded on the same calibration, `compare_sets` counting agreement. The pick is **BLIND** to the Sim's set. Overlap is a fine outcome, never an error. Sim entries are never gated away — a strategy-breaking one is FLAGGED, still gradeable/loadable. The user decides in DK; nothing flows back to the Sim. The strategy, player-pool, and thesis-grade runners never select.
- **Grade tab is PER-CONTEST** (`match_contests` merges Sim-pool + declared contests): 🎯 pick, A-F letter (`grader.letter_grade` + `contest_calibration`), optional `claude -p` thesis check (`run_grade` → `data/grade/<slug>__<key>.md`); bottom expander = portfolio view (leverage table + duplicate check — a lineup in two contests is a ⚠️ warning). Grades and names weaknesses only.
- **Player pool:** a Claude-ranked, annotated board of every rosterable player tiered **Core / Good / Okay / Fade** (+ orthogonal `· Leverage`), built with the strategy or standalone ("🏆 Rank players (all data)"). The primary build reference.

History: see docs/changelog.md (What this is).

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
.venv/bin/streamlit run app.py --server.port 8601    # http://localhost:8601
```

Venv `.venv/`, Python 3.9, Streamlit + pandas. **Restart the server after any code change** (Streamlit caches `src`). Headless runs use `analysis_runner.CLAUDE_MODEL` (env `ANALYZER_CLAUDE_MODEL`, default `"opus"`) with `--max-turns 60` / `--max-budget-usd 15` on every run.

## Architecture

| Path | Purpose |
|---|---|
| `app.py` | Streamlit UI: 5 tabs (Projections, Slate Data, Slate Strategy, ✅ Grade, Autopsy) |
| `src/grader.py` | Grade-tab letters. Only a call THIS slate's strategy made costs a letter: FADE violation / over-cap salary / 4+ warnings = hard F, else warns 0→A/1→B/2→C/3→D (board `Fade` tier = the one 1-warn check); one-step sim nudge when the roster is a pool row; section headline = WORST letter; every statistic (own envelope, no-leverage note, crowded pair, expected dupes — corpus-corrected MMA/NASCAR only, naive for golf) is INFO and never costs a letter. `retro_grade` self-validates at each autopsy log. `leverage_md` display-only. Never builds/swaps/fixes |
| `src/projections.py` | Vendor CSV loader → canonical schema (`load_projections`, `warn_missing_for_sport`) |
| `src/vendors.py` | Vendor signature auto-detection (ETR / Ship It Nation / DailyFan / DK) |
| `src/sessions.py` | Per-slug projection session `data/sessions/<slug>.json`; cleared with the slate |
| `src/landscape.py` | Breakdown + `breakdown_flags`; ceiling panels only with a real vendor `ceiling` (`has_real_ceiling`) — never fabricate one |
| `src/projections_diff.py` | Cross-vendor disagreement (`flagged_disagreements`) when ≥2 sources |
| `src/player_pool.py` | Player pool board (table first, write-ups below): full rosterable universe, fades kept tiered `Fade`; `run_player_pool`; `data/player_pool/<slug>.md`; never builds |
| `src/contests.py` | Contest registry `data/contests/<slug>.json`; Sim is the naming authority (`add_contest` → `canonical_contest_name`); UI mirrors the Sim (payout-ladder paste, verbatim-ported parsers) |
| `src/contest_templates.py` | Saved-contest templates per slug |
| `src/bundle.py` | `build_bundle` → `data/bundle/<slug>.md` |
| `src/analysis_runner.py` | All headless `claude -p` runs (strategy, pool, review, apply, grade, contest pick): builds the bundle, refreshes the trimmed ledger views, shells `CLAUDE_MODEL` at 60 turns / $15 |
| `src/lessons_view.py` | Regenerates `rules/<slug>/lessons_open.md` + `autopsies_recent.md` before every run (derived, gitignored) |
| `src/lessons_lint.py` | Lints `lessons.yaml` after the review; errors roll the review back |
| `src/slate_analysis.py` | Strategy read/write/clear `data/slate_analysis/<slug>.md` |
| `src/ledger_hygiene.py` | Deterministic ledger flags (stale / near-promotion / overdue / merge / `cross_sport_candidates`) fed into the review, applied by `run_apply_proposals` |
| `src/autopsy.py` | DK standings parser + structural analysis (`proj_frame_for_autopsy` enriches best-effort) |
| `src/accuracy.py` | Self-grade: did ENTERED lineups capture leverage / slate-defining plays |
| `src/shark_gap.py` | Us-vs-sharks fingerprint; handles = `rules/shared/shark_handles.yaml` ∪ `shark_handles_learned.yaml` |
| `src/shark_dossier.py` | Per-pro dossier `rules/shared/shark_dossier.jsonl`; `promote`; `shark_reality_block` → bundle `## Shark reality`. Descriptive only |
| `src/field_analysis.py` | Field/fish read (`field_profile`, `fish_traps` = PRICE conditions; a trap is a price, not a player) |
| `src/field_tendencies.py` | Append-only `rules/<slug>/field_tendencies.jsonl` (dedup by contest_id; trap = condition dicts, NO cross-slate trap NAME count; crowd names = opponent behavior; 0.5×-2× field-size gate); `bundle_block` → `## Field tendencies` |
| `src/shark_accumulate.py` | Shark envelope: `shark_observations.jsonl` → `refresh_baseline()` → `shark_baseline.json` (frozen seed + observations); Analyzer-only |
| `src/history.py` | Archive `rules/<slug>/history/` + `results.jsonl`; write-time dedup by DK contest id; `process_trend_block` → `## Process trend` |
| `src/adherence.py` | Did ENTERED lineups honor the contract's calls, per contest (`zeroed_in`, `over_in`); summarized in results.jsonl |
| `src/mme_portfolio.py` | MMA big-field (≥5,000) portfolio read — SHARED VERBATIM with the Sim; `mme_report` / `mme_summary`. Descriptive only |
| `src/counterfactual.py` | `near_miss` (salary-cap aware when projections loaded) + `winner_story`; standings-only |
| `src/pool_calibration.py` | Board tiers vs actual FPTS at log time (`tier_summary`, `tiers_ordered`) |
| `src/drift.py` | Leverage-candidate ownership drift vs the contract snapshot; display-only |
| `src/sim_data.py`, `src/dk_ids.py` | DORMANT — old Sim Data tab; unreferenced |
| `src/sim_link.py` | Sim → Analyzer read bridge (see Cross-repo contracts); every helper degrades to None without the sibling repo |
| `src/lineup_selection.py` | Pick engine: `candidate_slice` (two-stage, cap 500, coverage fill), `blend_scores` (top1 0.45 / cash 0.28 / proj 0.17 / own 0.10 — NEVER re-tune on correlation-with-score), `lineup_families`, `strategy_gate` (hard: no fade/lean_fade, ≥2 Core, never both of `chalk_pairs[0]`; underweight SOFT; leverage NOT a rule), `contract_conflicts` (🛑), `rule_price`, `metric_resolution` (Top-1% is a band — look DOWN the table), `parse_pick` (+ override log; one hard stop: the same underweight player in EVERY entry of a multi-entry contest), `taken_roster_keys`, `contest_divergence`, `match_contests`/`as_declared`, payout-shape fallback. Picks `data/lineup_selection/<slug>.json`; cleared with the slate |
| `src/slate_breakdown.py` | Renders any archived history dir (archived-slate picker, pinned review target) |
| `src/picker_check.py` | POOL/SLICE/PICK chain at Log Autopsy → `picker_check.json` (pool miss = BUILD, slice miss = TABLE, rows-above-pick = PICK); trend `scripts/picker_report.py` |
| `src/git_backup.py` | `commit_and_push(push=False)` at Log time; explicit backup button = `unpushed_summary` + `push_only` |
| `src/sim_sessions.py` | Slate-clear sweep of leftover `data/sim_data/` files only |
| `src/strategy_contract.py` | Analyzer → Sim contract `data/strategy_contract/<slug>.json`: calls from `## Fades` + `## Leverage`, leverage candidates, `chalk_pairs`, `anchor_pairs`, `structure_rules` (conservative prose parser, numbers only), `parse_build_rules`. Cleared + archived with the slate |
| `src/contest_selection.py` | Contest screener (`screen_declared`, `screen_md`) — INFORMATION ONLY; focus and MME never blend |
| `articles/<slug>/` | "Slate Data" uploads; deleted on autopsy log / slate clear (names kept in `manifest.json`) |
| `rules/<slug>/` | philosophy / framework / autopsies per contest type; framework/philosophy/venue files owned HERE (Sim mirrors read-only); autopsies.md NOT synced |
| `rules/<slug>/lessons.yaml`, `history/`, `results.jsonl` | Lesson ledger (below); one folder per archived slate; append-only results (app-written, Claude reads only; winnings/ROI optional + usually null — never ask to backfill, never grade missing winnings) |
| `rules/{nascar/tracks,pga_classic/courses}/` | Venue files, date-stamped observations; both PGA slugs share `pga_classic/courses/` |
| `rules/nascar/_archive/` | Retired `metrics.yaml` + `metric_performance.jsonl` (metric tracker deleted 9/19/26) |
| `data/bundle/`, `data/slate_analysis/` | `<slug>.md` bundle for Claude / written strategy |

History: see docs/changelog.md (Architecture — per path).

## Contest types

**SE / 3-Max / 5-Max is the HOME GAME; 20-Max / 150-Max is a SEALED parallel track.** `FOCUS_CONTEST_TYPES` drives framing, sharp-envelope target, grading, dossier, results headline. `MME_CONTEST_TYPES` (`infer_type`: cap ≤20 → 20-Max, else 150-Max) are declarable/loggable but NEVER blend: headline `best_rank`/`best_percentile` from focus only (MME gets `_mme` fields); shark/grading accumulators gate on FOCUS. A declared large-field contest adds the **big-field attack step** inside `## Build it like a sharp` (8-error catalog, `docs/mme_plan.md`). Large-field = FIELD EXPLOITATION, not portfolio mechanics; construction stays in the Sim.

| Sidebar | `slug` | Sport | Notes |
|---|---|---|---|
| PGA Classic | `pga_classic` | golf | 6 golfers, 2 days + cut |
| PGA RD4 Showdown | `pga_rd4_sd` | golf | 6 golfers, **flat — NO captain, NO 1.5x** |
| MMA | `mma_se` | mma | Home game = 150-max mini-MAX (100 entries a night); one slug for SE and MME; field size ≥5,000 routes the `mme_portfolio` read; framework's `## The MME (150-max) track` wraps the SE process |
| NASCAR | `nascar` | nascar | 6 drivers; **always check `rules/nascar/tracks/<slug>.md`** |
| NFL Showdown | `nfl_sd` | nfl | 1 CPT (1.5x, higher salary) + 5 FLEX, $50K, both teams; same 6 + different captain = different entry. **0.0 FPTS is REAL, DSTs go negative — never a scratch.** Profile: 5–20 entries, large-field lotto, script portfolio + dupe awareness. No venue. `rules/nfl_sd/` |
| NFL Classic | `nfl_classic` | nfl | QB, RB, RB, WR, WR, WR, TE, FLEX (RB/WR/TE), DST; $50K; ≥2 games; NO captain; identity = set of 9 names. Same 0.0/negative-DST note. Profile: smallest fields (SE/3/5-Max), no Classic MME. Stack-first. Vendor ETR "Main Slate" (`ownership` = Small Field, `own_large`). No venue. `rules/nfl_classic/` |

History: see docs/changelog.md (Contest types).

## Workflow per slate

1. **Slate Data** — upload article PDFs, notes (`.txt`/`.md`), misc CSVs (vegas, course/track history, matchups, DailyFan exports), photos/screenshots — the only input the strategy reads.
2. **Slate Strategy** — declare contests (field size frames how contrarian to be), click **Generate slate strategy** (bundle + headless `claude -p`).
3. *(After the contest)* **Autopsy** — upload DK standings CSV(s), link each to its declared contest (winnings optional), review field summary / your entries / winners-vs-you / leverage capture / shark gap (standings only), log lessons to `rules/<slug>/autopsies.md`. **Log autopsy** archives to `rules/<slug>/history/<date>__<slate>/`, appends `results.jsonl`, clears the workspace.
4. **Post-autopsy review** — **Run post-autopsy review** grades the process, updates `lessons.yaml` + venue file, proposes framework changes; **Approve & apply proposals** accepts them.

## Writing the slate strategy

Runs in-app via `run_analysis` (bundle → headless `claude -p`, this CLAUDE.md loaded → `data/slate_analysis/<slug>.md`). Chat fallback: click the button once to build the bundle, then ask "read the bundle and write the slate strategy". Either way:

1. Read the bundle `data/bundle/<slug>.md` (contests, absolute `articles/<slug>/` paths, `## Projections` tables, strategy-doc paths).
2. Read EVERY listed slate-data file — `*.pdf`, `*.txt`/`*.md`, `*.csv` (as text tables), `*.png`/`*.jpg`/`*.jpeg` (Read tool reads images; note in the file anything unparsable). Then the `## Projections` tables.
3. Read `rules/<slug>/{philosophy,framework,autopsies}.md` + `rules/shared/{anchor_equivalence,sharp_playbook,set_diversity}.md`.
4. Read the tail of `rules/<slug>/autopsy_data.jsonl`.
5. NASCAR: also `rules/nascar/tracks/<track>.md`.
6. Synthesize ARTICLES + projections together, cross-checked against framework + open lessons: where do they DISAGREE (article vs article, vendor vs vendor, article vs projection — that gap is the edge)? Which qualitative reads drive the build and where do numbers confirm/challenge them? The Anchor-Equivalence call? Which framework rules / open lessons activate?
7. Write `data/slate_analysis/<slug>.md` in the format below (cleared when the autopsy is logged).

**Coverage rule:** read EVERY uploaded file, never silently skip one, and read them **silently** (no printed checklist); the Player pool ends with a `## Sources read` line (count + any unparsable).

**Source-of-truth rule:** synthesize from EVERYTHING uploaded; cite each number from its source (**article OR vendor**); surface vendor-vs-vendor / vendor-vs-article gaps as leverage signal. **No lineup tables, no rosters.**

**Leverage-coverage rule:** EVERY player in the bundle's `## Leverage candidates to address` (`landscape.leverage_candidates`, sub-10% own, high ceiling) MUST be ADDRESSED in `## Leverage` or `## Edges & tensions` with a one-line leverage/ceiling synthesis (no play/fade command required); the Player pool confirms each in its `## Leverage candidates addressed` footer (`· Leverage`, or `Fade` with a reason). The app warns on any omission.

**Chalk-combo duplication rule:** the bundle's `## Chalk combos` (`landscape.chalky_combos`) top pairs MUST appear in `## Edges & tensions` as a plain-English duplication tension ("the field will pair X + Y in ~6.6% of lineups, ~235 in this field") — descriptive only.

**Field-tendency coverage rule:** when the bundle has `## Field tendencies` (≥2 comparable autopsies), surface it in `## Edges & tensions`. **A TRAP IS A PRICE, NOT A DRIVER (user directive 8/9/26):** trap history renders ONLY as the trap SHAPE (chalk share, owned-ahead-of-projection share, salary tier, k-of-t counts), never a player name; a cross-slate name count is NEVER fade/underweight evidence — every fade cites THIS slate's numbers (the bundle's `## Trap-shaped prices`; naming today's prices is fine). CROWD names are OPPONENT behavior / leverage-away only (in-N-of-M, never player quality), tagged `(field crowds)` in the Player pool, shown only when on the CURRENT slate; the coverage-gap warning fires only for on-slate crowd names. No fade commands.

### Slate strategy format (mandatory, all sports)

**SYNTHESIS-FIRST, tight, scannable. This tool ORGANIZES and SYNTHESIZES — it does NOT tell the user who to play.** No imperative play/fade commands, no roster shaping. **NO pre-flight/checklist section is printed.**

**Hard writing rules, all sections — WRITE FOR A SMART 5TH GRADER (user directive 7/27/26) AND KEEP IT SHORT (user directive 8/9/26). Applies to EVERY generated output (strategy, player pool, grade, review) and EVERY STRING THE USER READS (user directive 8/29/26):** app captions, `gate_summary`, `contract_conflicts`, banners, table help, diagnostics. No bare statistics vocabulary ("how many teams will pick him", not "ownership priced against win probability"; "about 1 in 30", not "sims at 3.3%"), no internal identifiers, every number carries its plain meaning in the same sentence, every named column says what it means. The pick rationale has its own contract (below).

**LENGTH: slate strategy ≤ 5,000 words (aim 3,000–4,500); post-autopsy review ≤ 1,800.** Extra room is for CLARITY (what a number MEANS, reasoning step by step, what the field does and how the slate beats it), never complexity — more short sentences, not longer ones.

1. **The 5th-grader test is the master rule.** Short sentences, ordinary words, one fact at a time; if a smart 11-year-old would re-read it, rewrite it. Say it ONCE.
2. **Plain meaning FIRST, DFS word in parentheses after — EVERY time, every section** ('the players most teams will pick (the chalk)'). Never assume a term stuck. Covers ownership, chalk, leverage, ceiling, floor, dupe, anchor, anchor-equivalence, fade, dominator, place differential, fish trap, own-per-slot, stars-and-scrubs, punt, and vendor terms (coffin, dock, boost, sim-optimal, steam).
3. **Every section opens with one plain sentence saying what it is for.**
4. **One idea per sentence, ~15 words, hard stop at 25.** No semicolon/dash chains, max two numbers per sentence, no idea said twice.
5. **Explain what every number MEANS** ('34% owned — about 1 of every 3 teams will have him').
6. **Never print a bundle-internal file reference** ('image-35'); describe the thing; spell out initialisms on first use.
7. **Cite everything** (article line OR projection number) in plain words; short tables where they compress.
8. **LENGTH BUDGET: ≤ 5,000 words, aim 3,000–4,500; review 1,800.** Specificity beats brevity (user directive 8/11/26). Per-section: Short version ~250 · At a glance ~150 · Edges & tensions ~500 · Field vs Sharp ~700 · Top plays ~900 · Leverage ~500 · Fades ~350 · Build it like a sharp ~600, headroom where needed. Trim by SELECTION, never by blurring — a finding keeps its names and numbers.
9. **ONE HOME PER PLAYER** — explained in exactly one section (Top plays / Leverage / Fades); elsewhere name + ≤5 words.
10. **NEVER VAGUE (user directive 8/11/26).** Every claim names its subject and numbers — never "the day's top scorer" / "a cheap golfer spiked" / "the screen missed him" without name, salary, score, or the number missed by. Keep words rather than lose a name or number. Strategy AND review.

Sections, in this order:

1. `## The short version` — must stand alone with zero DFS knowledge: 6–9 numbered single sentences, no sub-bullets/tables, max one number per sentence — slate type; where points come from and why; what the crowd does; the ONE separating decision; what a sharp does differently; the biggest trap. Every term explained in-sentence; no tiers, no citations.
2. `## Slate at a glance` — ≤6 lines, short table: games/fights/races, totals/win probs, weather, contests + field sizes. (Stale slate → a single bold `⚠️` line and stop.)
3. `## Edges & tensions` — THE STAR. Numbered, **max 8 lines of ~20 words** (10 if mandates need it): edge/tension · cited data. Candidates: scoring/leverage concentration, own-vs-ceiling mispricing, vendor/article DISAGREEMENT (absorbs the old `## Key themes`), substitutable chalk clusters. Mandates, ONE line each: **Anchor-Equivalence MUST appear** (observation, never "run the alternative"); each reliably-crowded `## Field tendencies` cluster with in-N-of-M + trap-SHAPE line; `## Trap-shaped prices` names; top `## Chalk combos` pair as duplication. NO imperative verbs.
4. `## Field vs Sharp — how this slate gets played` — THREE parts, ~180 words, names only: **(a) How the FIELD plays it** (~2 sentences: ownership + chalk combos + field tendencies); **(b) How a SHARP plays it** (~2 sentences from `## Shark reality`: anchor tier, sub-10% piece, what they refuse to share); **(c) The gap** (1–2 sentences). No per-player essay.
5. `## Top plays` — the ONE home for player write-ups. Tiered **Core / Good / Okay** (Fades in §7), **≤12 players**, best as a table: **player** ($sal, own%) — tier — ONE ~20-word cited sentence — plus a short **sharp stance** for slate-definers. `· Leverage` on low-owned high-ceiling plays.
6. `## Leverage` — own section (user directive 7/27/26: leverage and fades NEVER combined). MANDATORY: for EVERY game/fight/race the single sub-10%-owned high-ceiling play (including ones no article named). ONE flat list, ONE ~15-word line per spot, no sub-headers/bands/paragraphs, NO fade verdicts.
7. `## Fades` — own section. ONE opening sentence defining verdicts (FADE = play nowhere · LEAN FADE = mostly avoid · UNDERWEIGHT = less than the crowd, never zero), then **NAME — VERDICT** — one ~20-word cited sentence (THIS slate's salary + projection + ownership, and the world the fade needs). (`player_pool.parse_calls`/`extract_fades` also read the legacy combined `## Leverage & fades` + `**Fades:**`.)
8. `## Build it like a sharp` — closing section; the user plays SINGLE ENTRY almost exclusively and aims to MIMIC THE SHARPS. Numbered decisions, 1–2 SHORT sentences each, names only: **(1) anchor** (tier + why, 2–3 candidates with ownership, anchor-equivalence twins flagged); **(2) leverage piece** (2–4 candidates, target from `## Shark reality`); **(3) what the field duplicates** (top pair(s) with counts — information; a refusal must cite this slate's own read); **(4) salary shape** (anchor's downstream cost in plain arithmetic, which chalk to drop); **(5) two contests, two different entries** (only if 2+ declared, one-sentence reason each); **(6) big-field attack** (ONLY when 20-Max/150-Max declared: one ~15-word line per field mistake — self-copying, mispriced own, recency, anchor-twin herding, ignored mid-tier, dead builds, news stampedes, trap-shaped prices — mistake · evidence · attack; skip silent ones; close with 'the effective field is smaller than listed'; zero lineups); **(7) pre-lock check** (3–5 yes/no questions). Close with the sharp-envelope target in one line, citing a named pro from `## Shark reality` where one exists.
9. `## Build rules` — machine-readable copy of every rule the strategy stated (user directive 9/12/26). ONE fenced yaml block: `lineup_rules` (at_most / at_least / exactly with `count` + `players`; salary_min / salary_max with `value`) and `portfolio_rules` (min_entries_with / max_entries_with with `count` + `players`; max_exposure_pct with `player` + `value`), each with `why` + `from` (`strategy` or the CODIFIED lesson id). `strategy_contract.parse_build_rules` copies it into the contract; the Sim's Filter gate enforces ONLY this block when present. Never a rule the prose did not state; Anchor-Equivalence is a PORTFOLIO rule (min_entries_with 1 of the alternative anchor), never a per-lineup ban unless step 3 refused the pair for a stated reason; a low-owned RATE is max_entries_with, never a lineup rule; no lineup rule may REQUIRE a low-owned player.

**SUGGESTIONS ARE ALLOWED in sharp-archetype voice** ('a sharp anchors in the $9K tier here'). FORBIDDEN everywhere: telling the USER what to do ('you should play X', 'fade Y'), naming a full roster, presenting any player group as a build.

**The pick rationale** (`**Why these picks:**`, user directive 8/29/26) is a COHESIVE argument, not a caption: FIVE things in ONE connected read — projected points, ownership, Top-1%, sim ROI, and slate dynamics (what the field does and how this lineup beats it — the spine). Where inputs DISAGREE, say which was trusted. 6–12 short sentences, every number with its plain meaning ("1.9% top1 means about a 1-in-50 shot at first"); any `cost` override named and defended. **Set diversity at pick time** (`rules/shared/set_diversity.md`, user directive 8/30/26): with more than one pick, check the SET — shared players per pair, repeated 2-3 player combos, distinct theses, expected dupes ≈ 0 — and name over-concentration in the why. Never reject a lineup over a sub-band Top-1% decimal; look DOWN the table, not just up.

History: see docs/changelog.md (Writing the slate strategy).

## Pre-flight ritual (mandatory prep — every slate strategy, but SILENT)

Before writing `data/slate_analysis/<slug>.md`, do ALL of this — but **it is silent prep; NEVER print a `## Pre-flight checklist` section (the user does not want to see it).** Only the RESULT of each step shows, inside the strategy's sections.

1. **Confirm the slate.** Compare the bundle's generation timestamp and the article file dates against today. If the articles look like a prior slate (stale dates), do NOT analyze stale data — instead open the doc with a single bold `⚠️` warning line and stop. The current slate's articles drive everything; past results are reference only.
2. **Read the venue file** (nascar → `rules/nascar/tracks/`, golf → `rules/pga_classic/courses/` for BOTH pga slugs; mma and nfl have none). If missing, create a stub from this slate's articles and mark it `**UNVERIFIED — built from this slate's articles only**`.
3. **Read `rules/<slug>/lessons.yaml`.** Apply every lesson with status `hypothesis` or `validated` in the decisions where it fits; silently drop the ones whose mechanism doesn't. Codified lessons live in framework.md already; retired ones are ignored.
4. **Run the framework pre-lock checks** for the sport, always including Anchor-Equivalence (`rules/shared/anchor_equivalence.md`) — surfaced as a tension in `## Edges & tensions`.
5. **Scan `rules/<slug>/results.jsonl`** (last 3 slates) for recent process notes.
6. **Note the universal sharp principles** (`rules/shared/sharp_playbook.md` — reverse-engineered from 12 elite players' DK standings) as the target envelope for the hand-builder: every lineup unique; ≥1 sub-5%-owned leverage piece in most; ~12–16% average ownership per roster slot (sport-calibrated); an elite anchor with downstream differentiation; judged on ceiling, not median.
7. **When the slate involves more than one entry, note the set-diversity doctrine** (`rules/shared/set_diversity.md` — user directive 8/30/26): diversity is judged on the SET, multiple layers down (players shared, repeated 2-3 player combos, distinct theses, expected dupes ≈ 0), and stringent rules apply at PICK time while the opto builds loose. Surface any over-concentration as a tension in `## Edges & tensions`.

The strategy opens directly with `## Slate at a glance` (or the `⚠️` stale-slate warning) — never a checklist.

## Lesson ledger (`rules/<slug>/lessons.yaml`)

Structured lessons with a lifecycle: `hypothesis` → `validated` → `codified` (or `retired`). Each lesson: `id`, `born` date, `origin` (history dir), `statement`, `status`, `confirmations[]`, `contradictions[]`, `codified_in`, `retired_reason`.

- Claude updates evidence/status during the post-autopsy review.
- **Codifying into framework.md/philosophy.md and retiring both require user approval** — the review writes proposals; the user clicks "Approve & apply" in the Autopsy tab.
- Promotion criteria: 3 total confirming slates (origin + 2 confirmations of the MECHANISM, not just the result) → propose codifying. 2 mechanism contradictions → propose retiring.
- **GPP guard: a lost contest is never evidence by itself** — only mechanism confirmations/contradictions count. Variance is the game.
- **New lesson ids** follow `<slug-with-dashes>-YYYY-MM-DD-<short-kebab>`; existing legacy ids are never renamed.
- **Headless strategy/pool runs read the generated views**, not the full ledger: `rules/<slug>/lessons_open.md` (open lessons + codified ids) and `rules/<slug>/autopsies_recent.md` (last 6 entries), regenerated by `src/lessons_view.py` before every run and gitignored. The review run edits `lessons.yaml` directly; `src/lessons_lint.py` lints the ledger afterwards (errors roll the review back).

### Lesson-ledger hygiene (Autopsy tab)

As ledgers grow past ~20 lessons/sport, the **Lesson-ledger hygiene** block (Autopsy tab, below the post-autopsy review) keeps them sharp. `src/ledger_hygiene.py` computes deterministic flags instantly — **stale** hypotheses (0 confirmations that have had ≥3 logged slates or ≥30 days), **near-promotion** (2 of 3 confirming slates), **overdue promotion** (≥3 confirming slates, not yet codified), and **merge candidates** (`[[id]]` cross-links or high statement-token overlap). The reasoning over those flags rides the **post-autopsy review** (not a separate button): `run_autopsy_review` recomputes them fresh and writes retire / keep / merge / codify decisions into the review's `## Ledger hygiene` section; the same **✅ Approve & apply proposals** button applies them to `lessons.yaml` (+ framework/philosophy for codifications). Same approve-gate + GPP guard: a lesson untested only because no relevant slate occurred is KEEP, not retire; a lesson whose mechanism references a removed feature is a retire candidate.

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

Triggered by **Run post-autopsy review** after **Log autopsy** (archive to `rules/<slug>/history/<date>__<slate>/` + append `results.jsonl`). The autopsy runs from **DK contest-standings alone** — no proj-vs-actual or vendor-calibration panels. The headless review:

1. Grades the archived slate's process (checklist honesty, lessons applied vs ignored) and whether the strategy's Top plays / PLAY-PASS-MIX decisions held up against DK actuals (slate-defining low-owned plays, your entries vs the winners, shark gap).
2. Updates `lessons.yaml` evidence/statuses and births new hypotheses (mechanism-based, not result-based).
3. Updates/creates the venue file with a date-stamped per-slate observation.
4. Writes `<history_dir>/autopsy_review.md` — **≤ 1,800 words, aim 1,000–1,500; strategy + review pair ≤ 4,000** — every finding keeps its names and numbers (Never-vague: say Benjamin James, $8,700, 84.25 points). Exact headers (the app parses them): `## What happened` (~150 w, ≤6 numbered plain sentences: finish, who won and how, the named deciding thing), `## Process scorecard` (~400 w, the WHY: 2–3 specific sentences per finding with names + numbers), `## Lesson ledger changes` (~120 w, one line per lesson), `## Venue file changes` (~40 w), `## Ledger hygiene` (~150 w, one line per retire/merge/promote, only when flags exist), `## Proposed codifications` (~150 w, proposed NOT applied — the user approves in the app), `## What this means for next slate` (~80 w, 3–5 numbered single-sentence takeaways, most important first). Same 5th-grader + keep-it-short rules as the strategy (Hard writing rules above): each section opens with a plain sentence, ledger/DFS terms plain-meaning-first ('an idea we are still testing (a hypothesis lesson)', 'whether your entries followed your own plan (adherence)'), analyst vocabulary translated ('structural axis' → 'the main way winning lineups looked different from yours'; 'Spearman near 0' → 'this pre-lock number did not predict the real scores at all'), every number's meaning spelled out, every grade with a one-sentence what-to-do, nothing said twice.

Scoreboard = **best-percentile trend + process/mechanism metrics** — ROI lives in the user's third-party app; winnings/ROI in `results.jsonl` are optional and usually null. Never flag missing winnings, never ask to backfill, never conclude from ROI even when present.

History: see docs/changelog.md (Post-autopsy ritual).

## Hard rules

- **NEVER create lineups.** No lineups — ever. Both generated outputs name **individual plays only**: no roster tables / sample builds / "core build" groupings in the strategy; the Player pool is single players ranked independently (never a roster, stack, or pairing presented as a build). Applies in-app AND in chat. **Grading is not building:** the ✅ Grade tab checks USER-built lineups and names weaknesses — never proposes swaps, replacements, or alternative rosters. **Selection is not construction:** the Grade tab's per-contest pick flow may PICK among the Sim's already-built, already-simmed pool lineups by id from that contest's slice, validated by `parse_pick` (fabricated / modified / wrong-count / already-picked-elsewhere picks rejected, nothing saved). **The pick follows the slate strategy (8/15/26)** — as a guide with explained, logged overrides (8/29/26); no strategy → no pick. **One lineup, one contest (8/15/26, all sports).** **Two opinions per contest (8/22/26):** Sim entries beside claude's BLIND pick, both graded, agreement counted; overlap is fine; a strategy-breaking Sim entry is flagged, never hidden. Every roster shown was constructed by the Sim; authoring or modifying a roster stays banned everywhere; the strategy / player-pool / thesis-grade runners never select.
- **Slate strategy = everything uploaded (articles + every loaded vendor projection); autopsy stays standings-only** (best-effort salary/proj enrichment when projections are loaded). The Projections tab is a standalone upload/reference store — no lineup building/ranking/red-teaming/fixing (the Grade tab's per-contest picks over the Sim's pool are the one sanctioned exception).
- **No scraping.** DK ToS prohibits it; never build scrapers. User-pasted/uploaded data only.
- **GPP-only framing.** Leverage / ceiling / contrarian. Never propose cash-game features.
- **Anchor-Equivalence Rule** is a **mandatory surfaced tension** in every strategy's `## Edges & tensions`: if 2+ chalk-tier anchors sit at similar ownership (per the articles), surface that they're substitutable (the user decides — synthesize, don't command).
- **Venue check before any strategy**: read the venue file (NASCAR tracks / PGA courses) per the Pre-flight ritual. NASCAR: if `rules/nascar/tracks/<slug>.md` is missing, proactively ask the user for the track description.
- **Pre-flight ritual is mandatory** for every slate strategy — chat sessions included.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x**. Never reference "CPT". Position is the live to-par leaderboard score, never the tee time.
- **No NBA/MLB.** Out of scope (MLB removed 2026-07-18; NFL Showdown added 2026-09-09, NFL Classic 2026-09-12).
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.
- **Log autopsy commits LOCALLY; it never pushes (7/25/26).** `rules/` is auto-committed at Log time; `git push` publishes EVERY unpushed commit, so publishing is the separate explicit "⬆️ Back up learning log to GitHub" button that first shows what it would send (`git_backup.unpushed_summary`). Never make the push automatic again.
- **DraftKings only** — see the top directive; never cite FD numbers or propose FD-only rules.

History: see docs/changelog.md (Hard rules).

## Cross-repo contracts (Sim tool = `~/Desktop/Repo/ryanjsieb30DFS`)

- **Analyzer → Sim:** `data/strategy_contract/<slug>.json` (calls, leverage candidates, chalk/anchor pairs, `structure_rules`, build rules); framework.md / philosophy.md / venue files are owned HERE and mirrored read-only in the Sim via its "🔄 Refresh rules docs from Analyzer" button (autopsies.md stays a parallel ledger, appended by both).
- **Sim → Analyzer (`src/sim_link.py`):** `data/sim_entries/<slug>.json` (diversified set), `data/sim_pool/<slug>.json` (full simmed pool, `num_simulations`, payout shape), `data/sim_standings/<slug>/` + `data/sim_autopsy/<slug>__<contest_id>.json` (autopsy hand-off), the Sim's raw vendor CSVs (`<sim>/data/uploads/<slug>/` — one vendor upload per slate, "📥 Pull … from the Sim"), "📥 Declare from the Sim pool". All slate-scoped, cleared by `clear_sim_handoff`.
- **Shared VERBATIM modules:** `src/mme_portfolio.py` and `src/nfl_classic_defs.py` are byte-identical in both repos, and the contest payout parsers are verbatim ports — all locked by `tests/test_cross_repo_parity.py`.
- **Single sources:** the Sim is the contest-NAME authority (`canonical_contest_name`); `dk_username` has one source, the Sim's `data/user_config.json` (`sim_link.dk_username`).

## Useful file paths

- **Sample DK contest-standings**: `~/Downloads/contest-standings-190402324.csv`
- **GitHub**: https://github.com/ryanjsieb30DFS/ryanjsieb30DFS-Analyzer (`main` branch)
