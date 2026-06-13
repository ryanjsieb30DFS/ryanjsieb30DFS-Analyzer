# CLAUDE.md — DFS Slate Analyzer

Multi-sport DFS slate analyzer for DraftKings. Streamlit web app. Personal-use, single user (`ryanjsieb30`).

## What this is

A pre-slate / post-slate analysis tool for **PGA Classic, PGA RD4 Showdown, MMA, NASCAR**. The user uploads vendor projections; the Analyzer surfaces the structural read of the slate (chalk tiers, leverage candidates, anchor-equivalence pre-lock check, cross-vendor disagreements). After the contest, the user uploads DK contest-standings and the Analyzer drives a post-mortem.

Lineups come from two places, both landing in `data/lineups/<slug>.md`: Claude builds them on request (Analyze tab's Build lineups button) and the user hand-builds them in the **Handbuild** tab — handbuilt lineups carry a `(handbuilt)` tag in their heading. The tool does not run Monte Carlo or simulate contests.

## Run

```bash
cd ~/Desktop/Repo/ryanjsieb30DFS-Analyzer
.venv/bin/streamlit run app.py --server.port 8601    # http://localhost:8601
```

The venv is at `.venv/`. Python 3.9 (system Python). Streamlit, pandas.

## Architecture

| Path | Purpose |
|---|---|
| `app.py` | Streamlit UI: 6 tabs (Projections, Slate Data, Sim Data, Analyze, Handbuild, Autopsy) |
| `src/projections.py` | CSV loader with vendor auto-detection + canonical schema normalization |
| `src/vendors.py` | Vendor column signatures (ETR, Ship It Nation, DailyFan PGA/MMA/NASCAR, DK PGA RD4 SD) |
| `src/sessions.py` | Per-sport JSON persistence at `data/sessions/<slug>.json` |
| `src/landscape.py` | Chalk tiers, leverage table, anchor-equivalence check |
| `src/slate_analysis.py` | Auto-snapshot computations (`snapshot`, `top_chalk`, `sport_signals`) + persisted-analysis read/write at `data/slate_analysis/<slug>.md` |
| `src/projections_diff.py` | Cross-vendor disagreement detector |
| `src/contests.py` | Per-sport contest registry at `data/contests/<slug>.json` |
| `src/sim_data.py` | Generic sim-data store: saves the raw upload + a light summary at `data/sim_data/` |
| `src/bundle.py` | `build_bundle` — consolidates all inputs into `data/bundle/<slug>.md` for Claude to read |
| `src/analysis_runner.py` | `run_analysis` + `run_build_lineups` + `run_red_team` + `run_handbuild_analysis` + `run_autopsy_review` + `run_apply_proposals` — build the bundle, run `claude -p` headlessly (subscription auth). Power the Analyze tab's "Generate slate analysis" / "Build lineups" / "Red team the lineups" buttons, the Handbuild tab's "🧠 Claude analyze" button, and the Autopsy tab's review/approve buttons |
| `src/lineups.py` | Read/clear `data/lineups/<slug>.md` + `data/red_team/<slug>.md` + `data/handbuild_analysis/<slug>.md`, plus the Handbuild engine: `ROSTER_SPECS` (DK roster shapes + $50K cap per slug), `validate_lineup` (always-on house rules incl. MLB own-pitcher block + thesis required), `append_handbuilt_lineup` (appends `(handbuilt)`-tagged lineups in the Claude-built format, numbering continued), `load_handbuild_analysis` (parses the Thesis/'What if?' lines from Claude's handbuild analysis for the save flow) |
| `src/strategy.py` | Loads per-sport philosophy/framework/autopsies + recent lessons (read by `bundle.py`; no UI tab) |
| `src/autopsy.py` | DK contest-standings parser |
| `src/history.py` | Per-slate archive (`rules/<slug>/history/`) + cross-slate results ledger (`rules/<slug>/results.jsonl`) — written by the Autopsy tab's Log button BEFORE the workspace clears |
| `rules/<slug>/` | Philosophy / framework / autopsies docs per contest type — Claude reads these as context (no UI tab; surfaced via the bundle) |
| `rules/<slug>/lessons.yaml` | The lesson ledger — structured lessons with a lifecycle (hypothesis → validated → codified/retired). Claude-edited during the post-autopsy review; user approves codifications |
| `rules/<slug>/history/` | One folder per archived slate: manifest, slate analysis, lineups, bundle, contests, autopsy records, results, and the autopsy review |
| `rules/<slug>/results.jsonl` | Append-only, app-written results ledger (one row per slate: buy-in, winnings, ROI, best percentile). Claude reads it, never edits it. **Winnings/ROI fields are OPTIONAL and usually null — the user tracks ROI in a third-party app.** Never ask to backfill winnings and never grade missing winnings as a process miss; the in-repo scoreboard is best-percentile trend + process/mechanism metrics |
| `rules/<slug>/vendor_calibration.jsonl` | Append-only, app-written vendor accuracy ledger (proj/own MAE vs DK actuals, largest-field contest per slate). Claude reads it, never edits it. **Legacy `calibrations.jsonl` (plural) files are deprecated sim artifacts — ignore them** |
| `data/red_team/` | `<slug>.md` — adversarial pre-lock review of the built lineups (Claude-written via the Analyze tab's Red team button; cleared on autopsy log, archived to history) |
| `rules/{nascar/tracks,pga_classic/courses,mlb_classic/parks}/` | Venue knowledge — one file per track/course/park, accumulating date-stamped per-slate observations. Both PGA slugs share `pga_classic/courses/` |
| `articles/<slug>/` | Per-contest-type "Slate Data" uploads — PDFs, notes, and photos/screenshots (e.g. DailyFan). Tab label is "Slate Data"; the on-disk dir stays `articles/`. Per-slate: deleted on autopsy log and on the sidebar "Clear this sport's slate" button (filenames survive in the archive's `manifest.json`). |
| `templates/` | Canonical projection CSV templates per sport |
| `data/sessions/` | Per-sport session JSON (gitignored) |
| `data/sim_data/` | Per-slate sim upload: `<slug>__<filename>` (raw) + `<slug>_summary.json` (light summary for Claude). Optional. |
| `data/bundle/` | `<slug>.md` — the consolidated "Bundle for Claude" written from the Analyze tab. |

## Contest types

| Sidebar selector | `slug` | Sport | Notes |
|---|---|---|---|
| PGA Classic | `pga_classic` | golf | 6 golfers, 2 days + cut |
| PGA RD4 Showdown | `pga_rd4_sd` | golf | 6 golfers, **flat — NO captain, NO 1.5x** |
| MMA | `mma_se` | mma | SE rules |
| NASCAR | `nascar` | nascar | 6 drivers; **always check `rules/nascar/tracks/<slug>.md`** |
| MLB Classic | `mlb_classic` | mlb | 10 players (P, P, C, 1B, 2B, 3B, SS, OF×3), $50K; **team-stack driven** |

## Vendor auto-detection

Drop any of the user's vendor exports into the Projections tab — the loader detects:
- **ETR PGA** (`Golfer, Round 1 Tee Time, DK Salary, Proj, Small/Large Field Own, DK Ceiling, Make Cut Odds, ...`) — ETR renamed `DK Points` → `Proj` in June 2026; both headers are accepted
- **PGA Simple (unconfirmed vendor)** (`NAME, SAL, PROJ, CEIL, OWN, PT/$`) — vendor unverified; the user labels projection sources going forward
- **DailyFan NASCAR** (`Driver, Salary, Starting Position, ...`)
- **DailyFan MMA** (`Fighter, Matchup, Win %, Salary DK, ...`)
- **DK PGA RD4 SD** (`Golfer, Tee Time, Salary, Points, Ownership, ...`)
- **Ship It Nation MLB Projections** (`NAME, TM, OPP, POS, SAL, PROJ, PT/$, OWN, SLATE`) — SIN's single-file projections export, hitters + pitchers together; team names are abbreviations (CHC, MIL) — the MLB signals normalize these against the stack file's nicknames when merging
- **Ship It Nation MLB Rankings** (`#, Name, Team, Opp, Pos, H, Salary, Proj, Own, Slate`) — SIN's hitter + pitcher rankings, two files with identical headers. These are **rankings (slate context), not the player pool** — uploaded via the Slate Data tab, saved to `articles/<slug>/` for Claude to read
- **Ship It Nation MLB Stacks** (`#, Team, Proj, Own %, Stack Salary, Slate`) — team-level stack rankings; uploaded via the **Slate Data** tab (not Projections), stored as session team-data and merged into the MLB team-stack signals as `vendor_stack_*` columns
- **SaberSim MLB Projections** (`DFS ID, Name, Pos, Team, Opp, Salary, SS Proj, My Own, Adj Own, Saber Total, dk_points, dk_std, dk_95_percentile, ...`) — SaberSim's single-file DK player-pool export, hitters + pitchers together. Maps `SS Proj` → proj_points, `My Own` → ownership (`Adj Own` is the user's exposure target, left as a passthrough), `dk_std` → stddev (a real vendor stddev — no 30% fallback needed), `dk_95_percentile` → ceiling, `DFS ID` → dk_id. Coexists with the SIN projections pool so the Analyze tab's cross-vendor disagreement table compares them

To add a new vendor: edit `VENDOR_SIGNATURES` in `src/vendors.py`.

## Workflow per slate

1. **Projections** — upload vendor **player-projection** CSVs only (auto-detected), inspect rows
2. **Slate Data** — everything that isn't player projections: PDFs/notes/photos (e.g. DailyFan screenshots), misc data CSVs (vegas odds, course/track history, matchup data), and team-level vendor files (SIN MLB stack rankings — auto-detected here and routed to session team data feeding the stack signals)
3. **Sim Data** *(optional)* — upload a sim export CSV; stored as-is for Claude. Note: a SaberSim **projections** export (full player pool) is now an auto-detected **Projections** vendor — only a SaberSim **lineup/sim** export belongs here
4. **Analyze** — declare contests, review the auto-snapshot (chalk tiers, leverage, anchor-equivalence, sport signals, vendor disagreement), then click **Generate slate analysis** — the app builds the bundle and runs `claude -p` headlessly to write + render the analysis (no chat needed)
5. *(optional)* **Handbuild** — click-to-build, two panels: click players in the pool table (left) and they populate the lineup panel (right) with live salary/remaining/rem-per-player/proj/own% totals; MLB slots are auto-assigned (multi-eligibility aware). The user never types a thesis: **🧠 Claude analyze** runs `run_handbuild_analysis` headlessly — Claude steelmans + attacks the handbuild and writes `data/handbuild_analysis/<slug>.md` (Verdict SHIP/FIX/KILL, `**Thesis:**`, `**What if?**`, analysis; cleared on save/clear/autopsy log alongside a `<slug>_lineup.json` snapshot used to detect lineup edits). **💾 Save lineup** requires a current analysis and appends the lineup with Claude's thesis/'What if?' to the portfolio file (tagged `(handbuilt)`), so red team / archive / review cover it
6. *(optional, pre-lock)* **Red team** — click **🔪 Red team the lineups**: an adversarial headless run tries to refute each lineup's thesis (Claude-built AND handbuilt); verdicts SHIP / FIX / KILL render below the lineups. Findings only — fix via rebuilding or chat
7. *(After contest ends)* **Autopsy** — upload DK contest-standings CSV(s), link each to its declared contest (winnings optional — ROI is tracked in the user's third-party app), view field summary, log lessons to `rules/<slug>/autopsies.md`. **Log autopsy** archives the slate to `rules/<slug>/history/<date>__<slate>/`, appends `rules/<slug>/results.jsonl`, and calibrates every vendor vs actuals into `rules/<slug>/vendor_calibration.jsonl` before clearing the workspace
8. **Post-autopsy review** — click **Run post-autopsy review** (Autopsy tab): grades the build process (including red-team verdict adherence), updates `lessons.yaml` + the venue file, proposes framework changes. Click **Approve & apply proposals** to accept them

## Writing the slate analysis

This normally runs **in-app**: the Analyze tab's **Generate slate analysis** button calls `src/analysis_runner.py::run_analysis`, which builds the bundle and invokes `claude -p` headlessly (subscription auth, no API key) with the prompt to read the bundle + referenced files and write `data/slate_analysis/<slug>.md`. That headless Claude loads this `CLAUDE.md` and follows the steps below. The same can be triggered manually from a chat (fallback): click the button once to build the bundle, then ask **"read the bundle and write the slate analysis"**. Either way the steps are:

1. Read the bundle: `data/bundle/<slug>.md` — it consolidates the contest config, projections read (chalk/leverage/anchor/sport-signals), cross-vendor disagreement, and absolute paths to everything else below. Start here.
2. Read the slate-data files it lists under `articles/<slug>/` — `*.pdf`, `*.txt`/`*.md`, `*.csv` (misc data like vegas odds or course/track history — read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (use the Read tool — it reads images visually, so DailyFan screenshots work; PDFs may require poppler — note in the file if anything couldn't be parsed)
3. Read strategy: `rules/<slug>/{philosophy,framework,autopsies}.md` + `rules/shared/anchor_equivalence.md` (paths are in the bundle)
4. Read recent autopsies: tail of `rules/<slug>/autopsy_data.jsonl`
5. If sim data exists, read the raw file at the path in the bundle's "Sim data" section — see where the sims agree/disagree with the articles' read (e.g., a low-owned play the sims love, or chalk they fade)
6. For NASCAR: also read `rules/nascar/tracks/<track>.md`
7. Synthesize:
   - Where do the articles + auto-snapshot agree? Where do they disagree?
   - Which qualitative overrides should beat the quantitative signal?
   - What's the Anchor-Equivalence call?
   - What conviction-core duplication / ceiling-threshold / binary-leverage warnings apply (per the sport's framework)?
8. Write to `data/slate_analysis/<slug>.md` in the **handbuild-first format** below (all sports, always on). The user hand-builds lineups — every section must answer *who to play, and if played, how the rest of the roster shapes around them*, with no prose-to-decision translation required. It renders in the Analyze tab with a "Last updated" timestamp and is cleared automatically when the user logs an autopsy.

### Slate analysis format (handbuild-first — mandatory, all sports)

The file contains these sections, in order. GPP-framed throughout; concise and scannable.

1. `## Pre-flight checklist` — first, always (see Pre-flight ritual).
2. `## Slate at a glance` — brief facts table (games/fights/races, implied totals or win probs, weather, contests + field sizes). Keep it short.
3. `## The N decisions that define this slate` (N = 2–5) — the structural calls a hand-builder must make, in priority order. Each decision gets:
   - **PLAY / PASS / MIX** verdict + one-sentence mechanism.
   - Ownership adjusted for known patterns (e.g. SE chalk-pitcher condensation — name the lesson).
   - **If played →** the concrete roster-shaping consequences: remaining salary and per-slot math, who pairs with them, who conflicts (own-pitcher blocks, same-fight conflicts, duplicated-core risk), which framework rules/lessons activate.
   - **If faded →** the world that bet needs to win (a fade is a bet too — price it, including condensation-adjusted ownership).
   - The **Anchor-Equivalence call** appears here as one of the decisions (still mandatory on every slate).
4. `## Player board` — tiered table covering the decision-relevant set (full chalk tier + every named leverage candidate + traps + any player the vendors and I disagree on — NOT the whole pool; close with one line naming what was left off and why):
   - **PLAY** — belongs in most builds. **MIX** — situational; say exactly when. **PASS** — trap; say why, and what to do if the user plays them anyway.
   - Every row: salary, proj, own% (condensation-adjusted where a lesson applies), call, and an **"If played →"** shaping note.
   - Sport-specific columns matching the Handbuild pool: golf — ceiling, make-cut; MMA — win%, finish mix; NASCAR — start pos, dominator pts; MLB — team/stack role.
5. `## Where I disagree with the vendors` — MANDATORY, never omitted. Each entry: the vendor's claim → my call → the mechanism, weighted by `rules/<slug>/vendor_calibration.jsonl` (small-sample guard applies). Disagreeing with the data is encouraged when the mechanism supports it — that's where edges come from. If there are genuinely no disagreements, say so in one line.
6. `## Edges to exploit` — ranked. Each edge states the **expression**: the concrete way to put it in a lineup (named players, stack shape/salary route), not just the observation.

Roster-shaping logic is sport-specific — derive it from `rules/<slug>/framework.md` + open lessons (MLB: stack pairing + own-pitcher blocks; golf: salary-tier routes after an anchor; MMA: never both sides of a fight, conviction-anchor separation; NASCAR: dominator math + position differential).

Compact example of the shape (MLB, abbreviated):

```markdown
## The 3 decisions that define this slate
### 1. Christian Scott ($8,300 · 44% proj own → expect 55–65% per se-chalk-pitcher-own-condensation)
PLAY — right chalk; the fade is really a ~60% fade.
- If played → $41,700 for 9 spots ($4,633/spot). Stack his OWN bats (they pair, not fight); SP2 from the 22–25% class.
- If faded → you need the world where 60%-owned chalk busts AND your alternative arm smashes — price it as the binary it is.

## Player board
| Player | Sal | Proj | Own% | Call | If played → |
|---|---|---|---|---|---|
| Scott | $8.3K | 14.7 | 44→~60 | PLAY | stack NYM bats with him |
| Phillips | $6.2K | 11.3 | 22 | PASS | (if anyway: full-chalk bats, zero other pivots) |

## Where I disagree with the vendors
- The Stone ranks Phillips P#1 — I pass: <mechanism>. (SIN own MAE 3.0 over 3 slates — trust their ownership, question their arm ranks.)

## Edges to exploit
1. NYM 34.7% combined own vs the board's biggest favorite — expression: NYM-4/5 with Scott, $2.6K Young as the value engine.
```

## Building lineups

Normally triggered **in-app**: the Analyze tab's **Build lineups** button calls `src/analysis_runner.py::run_build_lineups`, which runs `claude -p` headlessly to build the portfolio from the slate analysis and write `data/lineups/<slug>.md` (rendered back in the tab). It requires a slate analysis to exist first. The count is `portfolio_summary.unique_lineups_needed` (default 2; entry caps SE / 3-Max / 5-Max / 20-Max / 150-Max), but **build fewer if the slate supports fewer distinct theses — never pad with filler**. Each lineup needs: a one-sentence thesis ("how it wins"), a roster table with total salary verified ≤ $50,000, and a distinct "what if?" question (lineups in a portfolio must answer DIFFERENT questions — `feedback_no_competing_lineups`). Apply the Anchor-Equivalence rule explicitly, and for MMA SE differ on at least one conviction anchor across lineups (never duplicate the same full core). Read `rules/<slug>/{framework,autopsies}.md` for the sport's construction rules (e.g. RD4 SD is a flat 6-golfer lineup, no captain; **MLB Classic is a 10-man, team-stack-driven roster — P,P,C,1B,2B,3B,SS,OF×3 — never roster a hitter against your own pitcher**). End with a Portfolio audit section.

### Ranking candidate lineups (construction coach)

Roster construction is the user's weakest area, so the **Handbuild tab's "📊 Rank candidate lineups"** is a coaching tool, not a builder. The user pastes lineups they built elsewhere (SaberSim, etc.) as DK player IDs; the app resolves them via the pool's `dk_id` column, validates each, and the **Rank** button calls `src/analysis_runner.py::run_rank_lineups`, which runs `claude -p` headlessly to write `data/lineup_ranking/<slug>.md`. These are **candidates the user is deciding between, NOT a portfolio** — the headless run RANKS and TEACHES; it must never edit `data/lineups/<slug>.md`. Output sections, in order: `## Ranking` (best→worst table, one-line reason each — ties allowed when two genuinely answer different questions), `## Per-lineup construction notes` (salary efficiency, correlation/shape, ownership/leverage vs vendor-projected own with the numbers named, and the implicit thesis; cross-reference the slate analysis `## Player board` calls each follows/violates), `## Cross-set findings` (redundant builds, shared blind spots, Anchor-Equivalence across the set), and `## Construction principles` (a short transferable lesson the user can reuse). The run ALSO writes `data/lineup_ranking/<slug>_theses.json` — a real thesis + 'what if?' per candidate label. GPP framing throughout — judge on how each WINS, never on cashing. Golf/MMA pools carry `dk_id`; MLB (SIN) does not yet, so the tab disables ranking for MLB.

**Saving keepers (thesis + red team are mandatory).** A lineup the user keeps from the ranker isn't a side-channel that bypasses discipline: the Handbuild tab's per-lineup **💾 Save** appends it to `data/lineups/<slug>.md` tagged `(from uploaded pool)`, carrying the ranker's thesis from the sidecar (save is disabled until a thesis exists — same gate as the handbuild analyze-before-save). Once saved it is reviewed by the Analyze tab's 🔪 Red team button exactly like any Claude-built or handbuilt lineup. The same rule binds the future "build around a core" feature: every lineup it produces must emit a thesis and feed red team.

## Pre-flight ritual (mandatory — every slate analysis AND every lineup build)

Before writing `data/slate_analysis/<slug>.md` or `data/lineups/<slug>.md`, in order:

1. **Confirm the slate.** Compare the bundle's generation timestamp and the article file dates against today. If projections/articles look like a prior slate (stale dates, low projection match), SAY SO in the checklist instead of analyzing stale data. The current slate's data drives everything; past results are reference only.
2. **Read the venue file** (nascar → `rules/nascar/tracks/`, golf → `rules/pga_classic/courses/` for BOTH pga slugs, mlb → `rules/mlb_classic/parks/`; mma has none). If missing, create a stub from this slate's articles, mark it `**UNVERIFIED — built from this slate's articles only**`, and flag it in the checklist.
3. **Read `rules/<slug>/lessons.yaml`.** Every lesson with status `hypothesis` or `validated` must be either applied (name where) or rejected (name the mechanism reason). Codified lessons live in framework.md already; retired ones are ignored.
4. **Run the framework pre-lock checks** for the sport, always including Anchor-Equivalence (`rules/shared/anchor_equivalence.md`).
5. **Scan `rules/<slug>/results.jsonl`** (last 3 slates) for recent process notes.
6. **Check vendor calibration.** When vendors disagree, prefer the vendor with lower MAE in `rules/<slug>/vendor_calibration.jsonl` (inlined in the bundle) — projection MAE for point calls, ownership MAE for leverage calls. **Small-sample guard: a vendor with <3 calibrated slates is a note, not a weight.**
7. **Open the output file with the `## Pre-flight checklist` block** — six lines (slate confirmed / projections loaded / venue file read / open lessons applied-or-rejected / framework pre-lock checks / prior results scanned), each checked `[x]` with specifics or unchecked `[ ]` with the reason. No checklist block, no valid output.

Checklist format example:

```markdown
## Pre-flight checklist
- [x] Slate confirmed: nascar — Nashville Superspeedway — bundle generated 2026-05-31 14:02; article dates match
- [x] Projections loaded: DailyFan NASCAR (38 players); session data is for THIS slate
- [x] Venue file read: rules/nascar/tracks/nashville_superspeedway.md
- [x] Open lessons reviewed: 4 open — applied: spread-dominators (Lineup 2); rejected: sleeper-spike (mechanism needs carnage, low-DNF track)
- [x] Framework pre-lock checks: Anchor-Equivalence → Bell/Reddick at similar own, alternative run in L3; ceiling-threshold OK
- [x] Prior results scanned: results.jsonl (last 3 slates; ROI sample too small to read)
```

## Lesson ledger (`rules/<slug>/lessons.yaml`)

Structured lessons with a lifecycle: `hypothesis` → `validated` → `codified` (or `retired`). Each lesson: `id`, `born` date, `origin` (history dir), `statement`, `status`, `confirmations[]`, `contradictions[]`, `codified_in`, `retired_reason`.

- Claude updates evidence/status during the post-autopsy review.
- **Codifying into framework.md/philosophy.md and retiring both require user approval** — the review writes proposals; the user clicks "Approve & apply" in the Autopsy tab.
- Promotion criteria: 3 total confirming slates (origin + 2 confirmations of the MECHANISM, not just the result) → propose codifying. 2 mechanism contradictions → propose retiring.
- **GPP guard: a lost contest is never evidence by itself** — only mechanism confirmations/contradictions count. Variance is the game.

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

## Red Team review

Triggered by the Analyze tab's **🔪 Red team the lineups** button after lineups exist → `run_red_team` → writes `data/red_team/<slug>.md` (cleared on autopsy log, archived to history). Adversarial standards:

- **Attack the thesis**: enumerate everything that must be true for each lineup to win, steelman it, then refute with evidence from the slate's inputs.
- **Verify the leverage math** against vendor-projected ownership (weighted by `vendor_calibration.jsonl`) — name the numbers; a 15%-owned "leverage play" is chalk wearing a costume.
- **Hunt shared failure modes** across the portfolio and field-duplication risk (obvious cores everyone builds).
- **Re-run Anchor-Equivalence** and check open `lessons.yaml` lessons the build ignored.
- **Audit the pre-flight checklist line by line** — verify claims, don't trust checkmarks.

Output format: `## Verdict summary` table, then per-lineup `SHIP / FIX (the one specific change) / KILL (the fatal flaw)` attacks, portfolio-level findings, pre-flight audit. SHIP is a legitimate verdict — manufactured objections are as useless as rubber stamps. **Hard rule: the red team never rewrites lineups.md** — findings only; the user decides.

## Post-autopsy ritual

Triggered by the Autopsy tab's **Run post-autopsy review** button after **Log autopsy** (which archives the slate to `rules/<slug>/history/<date>__<slate>/` and appends `rules/<slug>/results.jsonl`). The headless run:

1. Grades the archived slate's process (checklist honesty, lessons applied vs ignored). If the archive contains `red_team.md`, also grades verdict adherence and verdict accuracy in hindsight — heeded FIXes that saved points, ignored KILLs that cost lineups, and wrong verdicts that were rightly overruled are all ledger-worthy evidence.
2. Updates `lessons.yaml` evidence/statuses and births new hypotheses (mechanism-based, not result-based).
3. Updates/creates the venue file with a date-stamped per-slate observation.
4. Writes `<history_dir>/autopsy_review.md` with `## Process scorecard`, `## Lesson ledger changes`, `## Venue file changes`, `## Proposed codifications` — proposed (NOT applied) framework changes; the user approves via the app.

The slate's scoreboard is **best-percentile trend + process/mechanism metrics** — ROI is tracked in the user's third-party app, so winnings/ROI in `results.jsonl` are optional and usually null. Never flag missing winnings as a gap, never ask the user to backfill them, and never conclude from ROI even when present (high-variance GPP data).

## Hard rules

- **No scraping.** DK ToS prohibits it; never build scrapers. Use user-pasted/uploaded data only.
- **GPP-only framing.** Leverage / ceiling / contrarian. Never propose cash-game features.
- **Anchor-Equivalence Rule** is a **mandatory pre-lock check** on every slate — surfaced as a warning in the Analyze tab. 4-slate-validated structural leak: if 2+ chalk-tier anchors at similar own%, ≥1 lineup must run the alternative.
- **Venue check before any analysis**: read the sport's venue file (NASCAR tracks / PGA courses / MLB parks) per the Pre-flight ritual. For NASCAR specifically, if `rules/nascar/tracks/<slug>.md` is missing, proactively ask the user for the track description.
- **Pre-flight ritual is mandatory** for every slate analysis and lineup build — chat sessions included, not just headless runs.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x multiplier**. Never reference "CPT" for this contest type.
- **No stddev required.** Vendors don't ship it; loader auto-derives (`(ceiling − proj) / 1.28` or 30% of proj).
- **No NFL/NBA.** Out of scope. (MLB Classic is supported as of 2026-06.)
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.

## Useful file paths

- **Sample vendor CSVs**: `~/Downloads/DK PGA DFS Projections (6).csv` (ETR, old `DK Points` header) + `~/Downloads/DK PGA DFS Projections (9).csv` (ETR, new `Proj` header), `~/Downloads/PGA Projections DK.csv` (simple format, vendor unconfirmed), `~/Downloads/DailyFan-Projections-Sheet-MMA-DK-38.csv`, `~/Downloads/DailyFan-Projections-Sheet-NASCAR-DK-12 (1).csv`, `~/Downloads/DK PGA Round 4 Showdown Projections (5).csv`, `~/Downloads/DK-hitter-rankings-DK-MAIN.csv` + `~/Downloads/DK-pitcher-rankings-DK-MAIN.csv` + `~/Downloads/DK-stack-rankings-DK-MAIN.csv` (Ship It Nation MLB, 3-file set), `~/Downloads/MLB_2026-06-13-405pm_DK_Main.csv` (SaberSim MLB Projections export)
- **Sample DK contest-standings**: `~/Downloads/contest-standings-190402324.csv`
- **GitHub**: https://github.com/ryanjsieb30DFS/ryanjsieb30DFS-Analyzer (`main` branch)
