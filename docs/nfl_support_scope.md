# NFL Support — Scope for Both Repos

_Written 2026-09-09. Companion to `docs/nfl_game_theory.md` (the strategy foundation). This scopes what it takes to make NFL Classic and NFL Showdown first-class citizens of both tools: the Sim/builder repo (`ryanjsieb30DFS`, port 8501) and this Analyzer (`ryanjsieb30DFS-Analyzer`, port 8601). Built from a full coupling audit of both codebases plus an inventory of the NFL data already on this machine._

---

## The short version

- **The vendor problem is already solved.** `~/Downloads` holds **55 ETR "NFL DFS Projections — Main Slate" files and 38 ETR Showdown files** from past seasons. Classic files carry Name/Team/Opponent/Position/Salary/Projection/Ownership/Floor/Ceiling (stddev auto-derives from Ceiling, per the existing loader convention). Showdown files carry **CPT Salary / CPT Projection / CPT Own** directly. Your existing ETR subscription covers NFL — no vendor search needed.
- **The Analyzer is cheap to extend; the Sim is not.** The Analyzer is slug-parameterized nearly everywhere — its NFL work is mostly registration, seed content, and prompt authoring. The Sim's entire pipeline assumes a **flat 6-player positionless lineup** (`LINEUP_SIZE = 6`, `optimize.py:23`) with **no correlation machinery** — NFL Classic breaks both assumptions at once.
- **Recommended order: Analyzer Classic first (playable by Week 3), Sim Classic second, Showdown third, learning loop fourth.** The Analyzer alone supports real NFL Sundays (slate strategy, pool synthesis, grading, autopsy) while you build lineups by hand or in a third-party optimizer; the Sim's correlated engine is the long pole and shouldn't block playing.
- **Backtest fuel already exists**: ~90 historical ETR projection files + the 69-contest NFL standings archive mean the sim engine and shark envelope can be validated on past slates before Week 1 money rides on them — satisfying the gate-on-the-live-task rule despite NFL having no logged autopsy history yet.

---

## Phase 0 — Unblockers (both repos, small, mechanical)

Nothing works until these land. All are add-entries work, no design:

| Item | Sim repo | Analyzer |
|---|---|---|
| Contest-type registry | `src/rules.py:10-18` add `nfl_classic` + `nfl_sd` | `app.py:47-52` add the same two; `src/sim_link.py:345` `_SLUG_SPORT` |
| **Lineup-string parser regex** | `src/autopsy.py:95` `_SLOT_MARKER_RE` | `src/autopsy.py:101` `_parse_lineup_string` |
| ETR NFL vendor signatures (Classic + Showdown CPT/Flex) | `src/vendors.py` | `src/vendors.py` — **must land in BOTH or `test_cross_repo_parity.py` fails** (it enforces identical signatures and slug maps) |
| Projections schema | add `position`/`team`/`opponent` + Showdown CPT columns to optional-column lists (`src/projections.py:29-38`) | schema **already has** position/team/opponent/team_total (MLB fossil); add an `nfl` branch to `warn_missing_for_sport` |

The parser regex is 20 minutes of work but 100% of the autopsy pipeline is silently garbage without it: today's marker pattern `(CPT|UTIL|FLEX|[GDF])` doesn't know `QB/RB/WR/TE/DST`, and the lone `D` would mis-split inside `DST`. Multi-character tokens must come first in the alternation.

Two conventions conflict with NFL and need explicit carve-outs while in here:

- **0.0 FPTS = "scratched/didn't compete"** (both repos, scored-pool exclusion + vendor calibration). In NFL, 0.0 is a real score (a shut-down WR, a benched player) and DSTs can go **negative**. The scratch convention needs an NFL exception, and the sim's zero-floor on simulated scores (`simulate.py:211-213`) needs one too.
- **Lineup identity = set of names** (dedup, dupe estimation, min-uniques, `roster_key`). Fine for Classic; breaks for Showdown, where the same six names with a different captain is a different DK entry. Deferred to Phase 3 but the assumption is worth flagging now.

## Phase 1 — Analyzer NFL Classic (medium; the fast path to playing)

Goal: full Analyzer workflow for a Sunday main slate — projections upload, articles, slate strategy, player board, Grade, autopsy — with no Sim dependency.

1. **Rules dirs + seed content** (authoring, the real work): create `rules/nfl_classic/` (+`nfl_sd/` shells) with `philosophy.md`, `framework.md`, `autopsies.md`, `lessons.yaml`. Distill `docs/nfl_game_theory.md` Part 1 into the framework: stack-first doctrine (double stack + bring-back), pick-the-game-first, sturdy-vs-fragile chalk by position (eat RB chalk, fade DST chalk), forced-value handling, dupe hygiene. User approves content per the rules-always-on convention.
2. **Shark baseline seed**: `rules/shared/shark_baseline.json` has no `nfl` block, and `shark_accumulate.recompute` only updates blocks that exist — **a new sport never gets an envelope without a seed**. Mine the 69-file archive (precedent: `scripts/mine_pga_history.py`); `shark_handles.yaml` already lists the NFL twelve. This fuels the Grade tab, envelope checks, and shark head-to-head from day 1 — with two seasons of evidence instead of zero.
3. **Prompt work** (`src/analysis_runner.py` — the largest Analyzer item): an NFL-conditional slate-strategy section (correlation-first: game environments, stack menus with bring-backs, dupe warnings) and an NFL player-board column set (`Pos | Team | Sal | Proj | Own | Team total | How it wins | Tier`), following the existing `is_mma` switch pattern. Edges & tensions and synthesis-first rules unchanged — the Analyzer still never names lineups.
4. **Grade tab**: `_baseline_key` mapping (`nfl` for Classic), envelope reads from the new seed. Everything statistical stays guide-not-gate; no new gating design.
5. **Small stuff**: venue enumeration sites (`src/bundle.py:27-31`, runner prompts, CLAUDE.md pre-flight) — **recommend NFL gets NO venue concept** (like MMA); weather/stadium context lives in articles. Anchor-equivalence gets an NFL clause (QB/game-environment anchors). CLAUDE.md contest-type table update. Tests per convention (parser cases, vendor detection, warn cases).

Deliberately deferred from Phase 1: stack-centric autopsy (Phase 4) — the generic player-centric autopsy board works day 1, it just under-learns.

## Phase 2 — Sim NFL Classic (large; the two genuinely new engines)

The two hardest pieces in the whole scope, both in this phase:

1. **Positional roster construction.** The builder is a positionless 6-index sampler; NFL Classic needs slot-constrained sampling (QB×1, RB≥2, WR≥3, TE≥1, FLEX∈{RB,WR,TE}, DST×1, 9 players, ≥2 games). Touches the draw loop and capacity math (`optimize.py`), lineup matrices (`contest.py`), diversifier size assumptions, and DK exports (`dk_export.py:68-89` hard-codes `G1..Gn` headers and positional fill — needs slot-ordered output with FLEX designation). Right fix: make lineup size + slot definitions per-slug data (the `rules/<slug>/rules.yaml` files already carry `lineup_size`/`salary_cap` that code currently ignores) instead of module constants.
2. **Correlated NFL sim + a field that stacks.** Today an unknown sport falls through to independent normals — which for NFL misses the entire game (correlation IS the edge, per the game-theory doc). Needed: a `_simulate_nfl` with a per-game environment factor (total/pace), a team passing factor loading QB and his pass-catchers together, and QB↔opposing-DST anti-correlation. The golf tee-wave shared-shock code is the closest template. Equally important: `generate_field_lineups` must produce position-legal, stacking opponents — a field of random 9-man rosters would make every sim metric fantasy.
   - **Parameter discipline**: no NFL autopsy history exists to fit against, so v1 ships literature-anchored constants (QB-WR1 ≈ +0.35, QB↔oppQB ≈ +0.58, QB↔oppDST ≈ −0.46 from the game-theory doc), **validated by backtest against the ~90 historical ETR files + 69 standings files** (does the sim's top-1% line match real winning scores? do simulated field ownership profiles match real fields?). A pre-registered fitting gate opens only after ~6-8 live logged slates, mirroring the MMA night-shock ritual.
3. Riding along mechanically: 13 sport-gated `app.py` branches reviewed, projections editor position/team columns, templates + sample CSVs, `warn_missing_for_sport`, per-sport tests (`test_optimize_nfl.py`, `test_simulate_nfl.py`).

Exit criteria: builds legal 9-man lineups from a real ETR file, sim reproduces plausible winning-score distributions on ≥5 historical slates, 5-metric contract + diversifier + DK export verified end-to-end.

## Phase 3 — Showdown (medium-large, cross-cutting, both repos)

Showdown is one design problem appearing in many places: **the captain is a different purchase of the same player.**

- **Sim**: CPT slot with 1.5x salary + 1.5x points at every scoring summation (~8 sites in `contest.py`/`diversifier.py`/`lineup_scoring.py` — note DK standings already report CPT rows pre-multiplied, so the autopsy path must not double-apply); captain-aware lineup identity replacing frozenset-of-names in dedup/dupe/min-uniques/`roster_key`; CPT-first DK export with the CPT DK ID; captain UI in grids and exposure tables (CPT vs FLEX exposure separately — this is where the "QB captain trap" leverage from the game-theory doc becomes visible).
- **Analyzer**: ETR Showdown signature (the DailyFan MMA CPT/Flex signature at `vendors.py:133-145` is the exact template); `nfl_showdown` baseline key + envelope seed (Showdown fields run much chalkier — winner median ~28%/slot vs Classic ~13%, same pattern as PGA RD4 SD); CPT-priced salary/ownership in `lineup_profile` joins (grader + autopsy + counterfactual — silently wrong without it); optional Showdown shape rules in `strategy_contract.py` ("CPT from list X", "≥1 bring-back").
- Field generation gets the same treatment (captained, correlated, blowout/slog/shootout script mixture per Part 2.3 of the game-theory doc).

## Phase 4 — The learning loop (medium, after real slates exist)

- **Stack-centric autopsy** — NFL's version of the MMA fight-centric rebuild: join team/position onto parsed standings lineups and read winners as *shapes* (double stack? bring-back? which game environment? which captain?), not just per-player leverage. Autopsy-review prompt asks the NFL questions (was the winning stack constructible from the pool? was the captain contemplated? — the picker-check pattern).
- Calibration accrual: vendor_calibration, field-concentration corpus, consensus-mass fit, contest screener rows — all slug-generic, they fill themselves as slates get logged; dupe-correction stays off until a corpus exists.
- Fitting gate opens: re-fit correlation strengths per the pre-registered plan once n≥6-8 logged slates.

---

## Contest profile (decided 9/9 by user, revised same day)

**The two formats are opposite games:**

- **Classic: the smallest fields bankroll allows.** Few entries, small-field GPPs — the existing SE/3-max/5-max discipline. Judged on ceiling only.
- **Showdown: 5–10, possibly 20 entries into large-field lotto contests** (Milly-style fields), hunting the "nuts."

What that settles, per format:

**Classic (small-field):**
- The 28 small-field contests in the NFL standings archive (median ~2,300 entries) are directly representative. The winner profile measured there (own sum ~94%, 4 sub-10% players, 2 sub-5%, ~30% chalk anchor, winner unique) is THE build target.
- Duplication is a check, not an engine: chalk builds dupe in low single digits at this size. Take the highest-ceiling correlated build (double stack + bring-back) with balanced leverage; don't buy manufactured weirdness.
- No Classic MME. Big-field attack sections stay off for Classic strategy prompts.

**Showdown (large-field, 5–20 entries):**
- **The large-field playbook from the game-theory doc Part 2.4 is fully in scope**: dupe management by product-of-ownership, the salary-leaving band (median winner left $1,400; only 7% spent the full cap), kicker/2-4-split/punt uniqueness levers, and captain exposure spread toward the leverage positions (WR/RB over the chalk QB).
- **5–20 entries = a script portfolio.** One lineup per game story (shootout / slog / blowout-onslaught / underdog-garbage-time), weights set by Vegas total and spread — the set-diversity doctrine and no-competing-lineups rule applied to a single game. This is the Sim diversifier's existing job (outcome tiers, min-uniques, dupe penalty) pointed at a captained format.
- Showdown dupe estimation and the consensus-mass field fit matter HERE — the 41 large-field archive contests are the validation set, and captain-aware lineup identity (Phase 3) is what makes any of those numbers right.
- This raises Phase 3's stakes: Showdown isn't a lighter afterthought — it's the multi-entry portfolio format, and the CPT-identity + dupe machinery is load-bearing for it.

**Both:** lotto-style = ceiling-only judgment. Win% / Top-1% lead the picker; cash% is noise (sim-rank-not-gospel, now formally the NFL default). Contest screener buckets (<500 / 500–2k / 2k–10k / 10k+) already cover both ranges; NFL rows accrue automatically.

## Phase order (decided 9/9)

**Showdown jumped the queue — user plays an SD slate 9/10.** Showdown support (both repos: Sim CPT-aware builder/sim/field + Analyzer SD prompts/grading/rules dirs, plus the Phase-0 unblockers Showdown needs) is being built 9/9. NFL Classic (Analyzer Phase 1, then Sim Phase 2's positional builder) follows for the Sunday main slate. Venue files: none for NFL. Framework content ships as DRAFT pending user approval per rules-always-on.

## Decisions still needed from you

1. **`rules/nfl_sd/` framework/philosophy approval** — seeded from `docs/nfl_game_theory.md` Part 2, marked DRAFT until you sign off.
2. **Classic timing** — Analyzer-side Classic (Phase 1) before Sunday 9/13, or after the first SD slate's autopsy?

## Effort summary

| Phase | Where | Size | Nature |
|---|---|---|---|
| 0 — Unblockers | Both | Small | Mechanical (registries, regex, signatures, schema) — parity test forces lockstep |
| 1 — Analyzer Classic | Analyzer | Medium | Mostly authoring (framework, prompts) + baseline mining; playable outcome |
| 2 — Sim Classic | Sim | **Large** | **New engineering**: positional builder + correlated sim + stacking field model |
| 3 — Showdown | Both | Medium-Large | Cross-cutting CPT identity; MMA CPT/Flex + PGA-SD precedents help |
| 4 — Learning loop | Both | Medium | Stack-centric autopsy; calibration fills itself |

Season timing: it is Week 1 (first Sunday 9/13). Phase 0 + Phase 1 are achievable inside the first weeks of the season; historical ETR files mean early Sundays can also be *replayed* through the Analyzer afterward, so nothing about starting mid-season loses data.
