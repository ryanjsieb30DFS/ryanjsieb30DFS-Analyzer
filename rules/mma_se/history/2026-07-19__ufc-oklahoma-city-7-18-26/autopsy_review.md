# Post-autopsy review — UFC Oklahoma City 7.18.26 (logged 2026-07-19)

_Third pass, run 2026-07-26. Passes 1 (7/19) and 2 (7/26) are compressed into `## Prior passes — applied` at the bottom; nothing settled there is re-litigated here. This pass does three things: it quantifies the duplication finding pass 2 named but never wrote into the ledger, it decides the three new merge pairs the hygiene pre-pass surfaced, and it repairs a schema hole in `lessons.yaml`._

Two SE contests. **UFC $8K Flying Knee** (784 entries, $2K to 1st) — rank **18/784, 2.3%ile**, 642.11 points. **UFC $5K Clinch** (1,189 entries, flat payout) — rank **629/1,189, 52.9%ile**, 431.96 points.

## Process scorecard

### New this pass — duplication was super-linear, and that is the whole finding

Pass 2 spotted that the rank-18 roster was mass-produced (`dup_count: 10`, the field's **#3 exact-roster dupe magnet** at count 9) while the winning roster was entered twice. It stopped there. The arithmetic underneath is sharper than the observation:

| | User, rank 18 | Winner, dapope27 |
|---|---|---|
| Roster | Hooper / McMillen / **Bashi** / Franco / Barbosa / Elliott | Hooper / McMillen / **Harris** / Franco / Barbosa / Elliott |
| Differs by | — | one fighter |
| Ownership product × 784 (naive) | 1.93 | **1.19** (matches the tool's `expected_dupes`) |
| Actual entries of that exact roster | **10** | **2** |
| Realized ÷ naive | **5.2×** | 1.7× |

The two lineups differ by a single swap: Bashi (47.3% owned) for RJ Harris (29.1%). Independence says that swap should cut expected duplicates about **1.6×**. It actually cut them **5×**. Duplication does not track ownership linearly — it concentrates on whichever pieces the field *agrees about*, so the consensus roster runs several multiples above its own ownership math.

The consequence the ownership view hides: **even if Bashi had won, first prize splits ten ways.** In a top-heavy SE, a bullet assembled entirely from consensus pieces is capped in *value* before the first fight, independent of what it scores. That is a different failure from "picked the wrong fighter," and it is the one the process had no check for.

Worth naming plainly: the two edges pointed the same direction. The swap that adds 63.8 points is the same swap that cuts duplication 5×. The mid-own-converter screen and the duplication check are not competing constraints — which is what makes this cheap to act on. Recorded as `mma-se-2026-07-19-exact-roster-duplication-is-superlinear-in-consensus`.

And the pre-lock tooling **did** fire. `grader_validation.json` flagged `crowded_pair` on both entries; the pair was Bashi+McMillen, the field's #1 combo at 34.6% / 32.5%. The flag was overridden at build time.

### Second new finding — MMA field-tendency history transfers as shape, never as names

The strategy spent a full bullet mapping the forward-fed `## Field tendencies` block onto this card, and had to concede mid-sentence that "none of those names fight tonight." That is structural, not incidental: the block is **name-keyed**, and MMA rosters turn over ~100% between slates. The 7/12 crowd list (Holloway, Pimblett, Steveson, Pinas) shares **zero fighters** with the 7/19 card.

What transferred was the shape, and the strategy read it correctly — in both slates the field's #1 duplicated pair was the single most-owned anchor plus another top-five chalk favorite (7/12 Holloway+Pimblett 30.7%; 7/19 Bashi+McMillen 34.6%), and the strategy did name a McMillen-anchored pair as the analogue. Only the **magnitude** failed: it estimated ~18.9% against 34.4% actual, because it was computed from projected own.

This is a corollary of an existing lesson rather than a new one, so it was folded into `mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence` instead of birthing a 27th entry: read the MMA field-tendency block for shape only, and size duplication from this slate's own chalk-combo math with an upward convergence adjustment.

### Pre-flight checks — honored (verified again, unchanged)

- **Anchor-Equivalence** was surfaced as required (DDP 45% / McMillen 42%, plus the Hooper/Bashi/Usman cluster), and acting on it was the best decision of the slate — McMillen 168.11 vs DDP 85.20, both contest winners on McMillen.
- **Open lessons were visibly applied**: the per-fight low-owned-definer screen covered all 12 fights, the finish-capable-favorite exemption was cited by name, chalk combos and field tendencies were surfaced with counts.
- **Venue file**: not applicable — MMA has no venue directory by design.
- **Two instruments were dark**: no `player_pool.md` was generated (hence no `pool_calibration.json` — tier calibration is unavailable for this slate), and no `lineup_grade.md` (the Grade tab was not run pre-lock, though its calibration still ran retroactively at log time and produced the `crowded_pair` flag above).

### Did the synthesized edges hold up?

Held: the fade block went 4-for-5 (DDP 85.20, inside the predicted 90–100 band; Ko 37.40 and the Clinch's #1 fish trap; Coria 69.90; Delgado 69.40), and the Good tier's converters all landed (Barbosa 106.73, Elliott 115.23, Franco 110.13 — all three in both winning lineups).

Missed: Kline LEAN FADE (109.40, in the 1,189 winner), Bashi Core (42.90), every leverage lean (Ramirez 0.80, Montes 22.4, Anderson 7.41), and both darts. All recorded on 7/19; not re-litigated.

### 1b — Shark gap: still no measurement, and the conclusion stands

**No tracked pro was in either field** (`shark_gap.json`: `sharks_in_field: false`), so there is no axis measurement and no shark-axis lesson can be anchored to this slate. The axis history: 6/27 Baku `own_per_slot` delta **1.3 pts**, 7/12 UFC 329 `own_per_slot` delta **0.1 pts**, 6/20 and 7/19 unmeasured. `own_per_slot` ranked "top" only because every other dimension measured exactly 0.0. **There is no recurring structural shark leak in MMA — there is a two-observation sample where the user and the pro built nearly identically.**

Re-verified this pass, since pass 2's headline claim rested on it: `rules/shared/shark_baseline.json` contains **no `mma` key** — the frozen 63-contest seed covers nascar, golf and showdown only. There is no observed MMA envelope to calibrate a dart target against. That finding is carried by `mma-se-2026-07-19-sharp-envelope-is-a-rate-not-a-per-bullet-quota`.

### 1c — Adherence: discipline graded apart from results

- **Fades honored.** None of the five faded/underweighted names (DDP, Ko, Kline, Coria, Delgado) appeared in either entry.
- **Leverage candidates 0/2 rostered** (Nicoll, Melisano). Both lost. Per 1b the prescription was miscalibrated, not the execution — a target to fix, not a discipline charge.
- **The shared spine remains the clean discipline finding.** Both bullets shared 4 of 6 fighters including *every* conviction anchor; only the two cheapest slots differed. `no-identical-conviction-cores` is codified, was violated, and the predicted mechanism realized — Bashi failed once and damaged both entries at once. Recorded 7/26 as a confirmation-by-violation.
- **Cross-slate violation trend: still not computable.** `adherence.json` exists for this slate only, and `results.jsonl` carries `adherence_*` fields on the 7/19 row and nothing earlier. Re-check at the next MMA log.

### 1d — Codified-rule check

Fourteen codified rules. Verdicts are unchanged from pass 2; the table is compressed to the rows that carry a live verdict.

| Codified rule | This slate | Mechanism verdict |
|---|---|---|
| no-identical-conviction-cores | Violated (4/6 spine, all anchors shared) | Held — confirmation in the ledger |
| secondary-plays-are-not-leverage | Applied | **1 of 2 contradictions.** Its instruction ("swap anything 20%+ out of the leverage slot") would have removed every winner's differentiator: Harris 27.8–29.1%, Kline 21.6%, Barbosa 20.4–23.9%, Franco 23.7–25.9% |
| one-leverage-swing-conviction-core | Followed in neither entry | **1 of 2 contradictions.** Neither winner carried a sub-20% piece (lowest 23.85% / 20.35%; `dart_pct` 0.0 in both). The conviction-anchor half held |
| anchor-equivalence (shared) | Applied, decisive | Held — 8th validation |
| binary-leverage-weak-in-small-fields | Applied | Held |
| finish-capable-favorite-is-not-secondary-chalk | Applied | Split: McMillen 168.11 held; Bashi 42.90 is a lost fight, not a mechanism failure (GPP guard) |
| fade-on-structure-not-narrative | Applied | Held with refinement: the Kline cap was a narrative fade in structural clothing |
| leverage-is-the-low-own-finisher-not-the-named-dog | Codified 7/19 from this slate | No independent re-test available |
| ceiling-threshold-discipline | Not verifiable (no build-time ceiling sums archived) | No verdict |
| verify-submission · asymmetric-anchor-equivalence · se-bullet-selection · ceiling-gate-underrates-low-own-finishers · field-size-calibration | Not triggered, or applied without incident | — |

**Two codified rules sit at 1 of the 2 contradictions needed for a demotion proposal.** Neither gets one this slate, and both point the same way: `secondary-plays-are-not-leverage` and `one-leverage-swing-conviction-core` each define differentiation by an ownership *threshold*, and on consecutive slates (7/12, 7/19) the winning structure differentiated through mid-owned **converters** instead. If the next MMA slate reproduces that, the proposal is to narrow both — not delete them. Draft edits are held in `## Proposed codifications`.

The duplication finding above cuts across both of those watches and is worth flagging for whoever reads them next: it supplies a *non-ownership* reason to avoid the consensus roster, which is exactly the ground the two threshold rules were trying to defend with the wrong instrument.

### Process trend (results.jsonl, last 5)

Best percentile **0.2 → 1.7 → 1.3 → 26.1 → 2.3**. Healthy, and consistent with the strategy's own call to spend the differentiation budget on the top-heavy Flying Knee — which is where the 2.3%ile landed.

Leverage capture **1.0 → 0.6 → 0.0 → n/a**. `null` this slate because `projections.available` was false at autopsy time (0 of 24 fighters matched) — the projections session had been cleared before the standings were logged. Three of the last four MMA slates now have a hole in that series. Logging the autopsy before clearing the slate keeps `edge_leverage_capture` populated.

Bust exposure and tier calibration: unavailable (no projections at autopsy, no player-pool board generated).

## Lesson ledger changes

Applied directly to `rules/mma_se/lessons.yaml` this pass:

1. **Born `mma-se-2026-07-19-exact-roster-duplication-is-superlinear-in-consensus`** (hypothesis) — exact-roster duplication rises super-linearly in field consensus (user 5.2× its independence estimate, winner 1.7×), so a top-heavy SE bullet built from consensus pieces is value-capped before the fights start. Carries the pre-lock test: ownership product × field size × the sport's measured concentration factor, with a double-digit result treated as build-defining.
2. **Amended `mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence`** — added the field-tendency corollary: the block is name-keyed and MMA turns its roster over ~100% between slates, so it transfers shape only; magnitudes must be re-derived from this slate's chalk-combo math with an upward convergence adjustment.
3. **Schema repair on `mma-se-2026-05-30-ceiling-gate-underrates-low-own-finishers`** — the entry was missing `contradictions`, `codified_in` and `retired_reason` entirely, so a `codified` lesson had no recorded framework anchor and no field for a future contradiction to land in. Set to `[]`, `framework.md — Win-Case Ceiling Under-Rates Low-Own Finishers (5/30/26 — UFC Macau)` (the section exists, verified at `framework.md:171`), and `null`. No evidence was added or changed.

Ledger now stands at **26 lessons** — codified 14, validated 3, hypothesis 8, retired 1.

## Venue file changes

**None.** MMA has no venue directory — venue knowledge is tracked for NASCAR tracks and PGA courses only (`rules/{nascar/tracks,pga_classic/courses}/`), per CLAUDE.md. No stub was created: a per-arena MMA file would accumulate observations with no mechanism to act on, since the cage, the scoring and the fight-night structure are identical in Oklahoma City and anywhere else. If venue ever matters in MMA it will be through altitude or short-notice travel, which belongs in the framework rather than a per-arena file.

## Ledger hygiene

The pre-pass flagged 4 stale hypotheses, 3 near-promotion, 0 overdue, and 19 merge pairs. Sixteen of those pairs were decided in passes 1 and 2 and are carried forward unchanged; the three new ones are all consequences of `sharp-envelope-is-a-rate-not-a-per-bullet-quota` being born last pass.

### Stale hypotheses (4) — all KEEP, unchanged

- `mma-se-2026-05-09-confirmed-vs-speculative-news` — **KEEP.** The mechanism needs a late-breaking-news swap decision to fire; no slate since 5/9 has produced one. GPP guard applies squarely — untested for lack of a relevant slate.
- `mma-se-2026-06-14-showdown-flex-spine-diversity` — **KEEP.** Captain-mode-only; every slate since 6/14 has been classic format.
- `mma-se-2026-06-14-showdown-captain-the-ceiling-pair-the-smash` — **KEEP.** Same — the CPT-slot assembly mechanism cannot fire on a classic slate.
- `mma-se-2026-06-14-showdown-trust-cpt-own-not-projected-overall-own` — **KEEP, merge pending.** Pass 2 proposed folding it into the classic-format lesson; that proposal is still awaiting approval and is restated below rather than re-derived.

**Sunset note (carried).** All three showdown hypotheses are format-locked, and the tool's scope is SE / 3-Max / 5-Max classic. If no captain-mode slate is played by roughly the end of 2026-09 they should be retired as untestable. That is a scope judgment for the user, not a mechanism failure, so no retirement is proposed.

### Near promotion (3) — the exact mechanism a third slate must confirm

- `mma-se-2026-06-14-showdown-cap-single-favorite-exposure` (validated, 2/3) — needs a slate with **≥3 entries** where the chalkiest favorite is capped at ≤60% of lineups *and* ≥2 deliberate fade builds exist, and that structure either dodges a chalk bust or costs nothing when the chalk hits. This slate cannot count: 2 entries, McMillen in both (100%, uncapped), and he smashed.
- `mma-se-2026-06-14-showdown-cheap-slot-prefer-floor-or-live-dog` (validated, 2/3) — needs a slate where the cheap slot holds a decision-floor fighter or a live finishing dog and outscores a pure salary-relief piece, **with salaries available**. This slate rhymed (the winners' cheap pieces Franco/Harris converted; the user's relief-tier Hines 4.40 and Anderson 7.41 busted) but DK standings carry no salary column, so it is not cleanly gradable. Making it gradable means joining the archived strategy's salary table to the standings at log time.
- `mma-se-2026-07-12-distance-fight-is-not-low-ceiling` (validated, 2/3) — needs a third slate where a fighter projected to win a **high-pace, high-control decision** at low ownership scores 100+, or where a low-finish-probability favorite is correctly *not* ceiling-capped. Kline (7/19) was the second. The clean test needs a recorded method, since standings alone cannot separate a finish from a dominant decision.

### Merge candidates (19)

**New this pass (3) — all involve the newly-born `sharp-envelope-is-a-rate-not-a-per-bullet-quota`:**

- `sharp-envelope-is-a-rate` ↔ `winning-se-shape-six-winners-mid-own-converters` — **KEEP-SEPARATE.** They cite the same evidence (`dart_pct` 0.0 in both winners) and reach different claims. One is a rule about how to *read a statistic* — a portfolio rate is not a per-bullet quota; the other is a claim about what the winning roster *looks like*. Merging would bury a measurement-interpretation rule inside a build-shape target, where it would stop applying to the next envelope number the tool forward-feeds.
- `leverage-is-the-low-own-finisher-not-the-named-dog` ↔ `sharp-envelope-is-a-rate` — **KEEP-SEPARATE.** The first is codified into framework.md; the second is an unconfirmed hypothesis with zero confirming slates. Merging would launder unvalidated content into a codified rule — the same reasoning applied to this pairing's siblings in pass 2.
- `one-leverage-swing-conviction-core` ↔ `sharp-envelope-is-a-rate` — **KEEP-SEPARATE now, merge-on-demotion.** These two are genuinely converging: both ask whether a mandatory low-own slot belongs in a single bullet, one from the philosophy side and one from the shark-envelope side. But the codified rule sits at 1 of 2 contradictions. If it takes a second and gets narrowed, the hypothesis is the natural source of the replacement language and the merge should happen *then*, as part of the demotion — not now, which would pre-empt the user's approval of a demotion that hasn't been proposed yet.

**Carried from pass 2 (4), unchanged:** `showdown-trust-cpt-own` ↔ `projected-own-understates` — **MERGE** (proposal below, still pending approval). `finish-heavy-small-fields` ↔ `winning-se-shape` — KEEP-SEPARATE, no-op (the former is retired; the cross-link is the audit trail). `leverage-is-the-low-own-finisher` ↔ `winning-se-shape` — KEEP-SEPARATE (search rule vs shape target; codified vs unconfirmed). `binary-leverage` ↔ `winning-se-shape` — KEEP-SEPARATE (field-size EV rule vs roster-shape target).

**Carried from pass 1 (12), all KEEP-SEPARATE, reasons unchanged:** cap-single-favorite ↔ flex-spine; captain-the-ceiling ↔ flex-spine; captain-the-ceiling ↔ trust-cpt-own; secondary-plays ↔ fade-on-structure; secondary-plays ↔ finish-capable-favorite; binary-leverage ↔ leverage-is-the-low-own-finisher; cheap-slot ↔ leverage-is-the-low-own-finisher; finish-capable-favorite ↔ leverage-is-the-low-own-finisher; leverage-is-the-low-own-finisher ↔ distance-fight; fade-on-structure ↔ distance-fight; and the two pairs involving `finish-heavy-small-fields`, resolved by its retirement.

**Removed-feature check:** no lesson's mechanism references a removed feature. The three showdown lessons depend on a contest format the user has not played recently, not on tooling that no longer exists — that is the sunset question above, not a removed-feature retirement.

**Bloat note.** 19 merge flags across 26 lessons is mostly the `[[id]]` cross-linking convention doing its job, not real duplication — every KEEP-SEPARATE above rests on the two lessons making different claims from shared evidence. Worth watching, though: nine of the nineteen now involve one of the four 7/19-born entries. If the next pass flags a fourth 7/19 cross-link cluster, the right move is consolidating the 7/19 cohort into a single "what the OKC slate taught" lesson with sub-claims, rather than deciding pairs one at a time.

## Proposed codifications

_(Proposals only. Nothing below has been applied to `framework.md`, `philosophy.md`, or any lesson's status. Approve via the app.)_

**1. MERGE `mma-se-2026-06-14-showdown-trust-cpt-own-not-projected-overall-own` into `mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence`** — carried from pass 2, still pending, restated in full so the approve action has a complete target.

Surviving id: **`mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence`** (the live, testable one). The showdown entry becomes `status: retired`, `retired_reason: "Merged into mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence — same mechanism (projected own% does not describe real field concentration), with the sign determined by format."` Proposed combined statement:

> Vendor projected own% does not describe where the field actually concentrates, and the direction of the error is set by the contest format. In **captain-mode showdown** the field fragments across captains, so projected OVERALL own% massively **overstates** real exposure — Hokit projected ~75 overall but drew 12.6% actual captain own, and the upset finisher who won (Gaethje) hid behind 44% projected / 7.9% actual; DailyFan's CAPTAIN-own column was well calibrated by comparison. In **classic SE** the error inverts: the field converges harder than projected on the single narrative-consensus favorite — DailyFan projected McMillen 42% (second to DDP's 45%) and he drew 66.8–69.8% actual, becoming the field's true chalk by 20 points, while DDP landed near projection. Downstream math inherits the error in both formats: the 7/19 DDP+McMillen pair estimate (~18.9% of lineups) was half the actual 34.4%, and the real #1 pair (Bashi+McMillen, 34.6%) was never flagged. Rule to test: make leverage, fade and duplication calls off the ownership column that matches the format's decision structure (CPT-own in showdown), and in classic treat "similar projected ownership" at the top of the board as unverified until an actual-convergence check — the consensus signal is more trustworthy than the projected gap between the top two anchors.

The field-tendency corollary added to the surviving lesson this pass (shape transfers, names do not) should ride along with the merge.

**2. No promotions this slate.** No lesson reached 3 confirming mechanism slates. The two that did on 7/19 (`leverage-is-the-low-own-finisher-not-the-named-dog`, `fade-on-structure-not-narrative`) were codified then and appear under `## Prior passes — applied`. The three near-promotion lessons each need one more slate, with the exact test named in `## Ledger hygiene`.

**3. No demotions this slate — two watches remain open.** `mma-se-2026-05-16-secondary-plays-are-not-leverage` and `mma-se-2026-05-17-one-leverage-swing-conviction-core` each carry **1 of the 2** mechanism contradictions required. Per codification-is-not-tenure, if the next MMA slate reproduces the pattern (winners differentiating through 20–30% converters with no sub-20 piece), the proposal will be to **narrow both, not retire them** — the conviction-anchor core of each is sound and untouched. The edits that would then be proposed:

> `framework.md` — Step 2, *Secondary Plays Are Not Leverage*: replace the fixed "20%+ is not leverage" line with "leverage is defined **relative to this slate's chalk concentration**: when the top anchor draws 2x the field's second-most-owned play, the differentiating tier moves up to roughly a third of the top anchor's ownership. Audit the leverage slot against that ratio, not against a fixed 15–20% number."
>
> `philosophy.md` — *Conviction vs. Contrarian in SE*: replace "include exactly ONE sub-20%-owned leverage swing" with "include exactly ONE **differentiating** play — a fighter the field under-trusts on the win side. Ownership is how you check that you found one, not what defines it; in a field whose chalk runs 45–70%, a 20–30%-owned converter differentiates and a sub-10% dart usually just adds a dead slot."

**4. Nothing proposed for the duplication finding.** `mma-se-2026-07-19-exact-roster-duplication-is-superlinear-in-consensus` is one slate old with zero confirmations, and one contest is not enough to fix a concentration multiplier. It stays a hypothesis. The pre-lock check it describes already exists in the Grade tab, which flagged this exact roster — so the near-term value is in *heeding* the existing flag, not in writing a new framework rule around a single measurement.

## Prior passes — applied

_(Audit trail. Nothing here is re-proposed.)_

**Pass 1 (2026-07-19).** Approved proposals applied: (1) codified `mma-se-2026-06-27-leverage-is-the-low-own-finisher-not-the-named-dog` → framework.md "The Leverage Screen: Converters, Not Named Dogs (7/19/26 — 3-slate validated)"; (2) codified `mma-se-2026-06-20-fade-on-structure-not-narrative` → framework.md "Structural Fades Only (7/19/26 — 3-slate validated)"; (3) retired `mma-se-2026-06-27-finish-heavy-small-fields-still-won-by-differentiation` with its proposed retired_reason (surviving half carried by `winning-se-shape-six-winners-mid-own-converters`). All hygiene decisions were KEEP / KEEP-SEPARATE; no merges applied; no philosophy.md edits proposed or made.

Ledger evidence added 7/19: `anchor-equivalence-fifth-validation` (8th validation, McMillen-not-DDP, with the projected-own-parity boundary); `binary-leverage-weak-in-small-fields`; `leverage-is-the-low-own-finisher-not-the-named-dog` (third confirming slate); `finish-heavy-small-fields` (second contradiction); `distance-fight-is-not-low-ceiling` (first confirmation, Kline 109.40, promoted to validated); `fade-on-structure-not-narrative` (chalk-piece refinement). Born: `winning-se-shape-six-winners-mid-own-converters`, `projected-own-understates-consensus-chalk-convergence`.

**Pass 2 (2026-07-26).** Wrote to the ledger four findings pass 1 had left in prose: the `no-identical-conviction-cores` confirmation-by-violation (4/6 shared spine, shared Bashi loss damaging both entries at once); the first mechanism contradiction of `secondary-plays-are-not-leverage`; the first mechanism contradiction of `one-leverage-swing-conviction-core`; and birthed `sharp-envelope-is-a-rate-not-a-per-bullet-quota`. Proposed the trust-cpt-own merge (restated above, still pending). Established that no tracked pro was in either field and that the "own_per_slot is your recurring gap" line rested on deltas of 1.3 and 0.1 points.

**Tooling.** The 7/19 finding that `strategy_contract.json` shipped empty — `_leading_name` could not strip an em-dash verdict tail, making `adherence.json`'s `fades_violated: 0` a grade against an empty contract — is **fixed in code** (`src/player_pool.py:152`). The archived contract for this slate stays vacuous as a historical artifact; the failure mode cannot recur.
