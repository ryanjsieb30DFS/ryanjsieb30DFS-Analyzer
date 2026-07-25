# Post-autopsy review — 2026 Open Championship (Royal Birkdale), logged 2026-07-22

PGA $15K Eagle 5-Max, field 3,567, 5 entries. Best finish 838 (23.5 pctile). Leverage capture 0.5 (2/4 slate-definers rostered somewhere). Standings-only autopsy.

## Process scorecard

**Pre-flight checks — honored, judged by the strategy's substance.**

- **Venue file:** honored. `courses/royal_birkdale.md` was created pre-slate (marked UNVERIFIED) and the strategy's Slate-at-a-glance carries its substance (redesign, pot-bunker penalty, defenseless-conditions read). The birdie-fest read held (winning score 479).
- **Anchor-Equivalence:** honored, first line of Edges & tensions (Scheffler 25.4% / Rory 24.3% substitutable), and executed structurally — 2/5 Scheffler, 2/5 Rory, neither zeroed. Scheffler (81.5) anchored two top-10 winners.
- **Open lessons:** the doc visibly applied `vendor-independent-ceiling-scan` (Hatton/Clark/Spaun/Griffin surfaced as "named by no article"), `fade-needs-ownership-to-materialize` (the Hovland fade written WITH the inline materialization check), `single-vendor-overweight-self-erosion` (the MacIntyre steam trigger), `dose-darts-to-course-variance` ("the ~2–2.5-dart end"), and the mandatory low-owned-definer screen. No open lesson was silently ignored at the doc level.

**Did the analysis hold up against the DK actuals? Largely yes — the best doc of the sample.**

- **The strategy NAMED the slate's #1 definer for the first time in five slates.** Cameron Young (96.5 FPTS @ 8.72% own, in 44.4% of the top-36 winners, the overall winner's leverage carrier) was the FIRST name on the definer screen, with the exact ceiling case ("the 'no links experience' fade got him last time — runner-up at St Andrews"). The Memorial→RBC→Shinnecock→Travelers streak of the definer living outside the doc broke here.
- **Fade calls were right.** Hovland (FADE): 23.5 FPTS at 24.2% own — the #2 fish trap. Fleetwood (UNDERWEIGHT, not fade): hit 88.0 and anchored the winner, but the call was explicitly conditional and soft; no violation of the doc's own logic. Cantlay (LEAN FADE): 26.0 FPTS, correct.
- **The big analytical miss was Sam Burns** (92.0 @ 13.6%, in 66.7% of top-36 winners — the single most common winner piece), who appears nowhere in the strategy. A mid-band elite ETR was cool on — precisely the residual the vendor-independent ceiling board exists to catch. Logged against `vendor-independent-ceiling-scan` as the shape of its next required confirmation.
- **The second miss was tier-placement, not coverage: Matt Fitzpatrick as Core.** His ownership steamed 25.5%→37.6% and he busted 22.0, finishing as the slate's #1 fish trap (54.1% of fish lineups, 2.8% of winners). The doc quoted the writer's "if own holds" caveat and then didn't act on it. This is the second mechanism failure of the codified coffin-driven trap/value split — see Proposed codifications.
- **Where the finish was actually lost: execution, not analysis.** The doc said "the definers screen is this slate's priority — most bullets carry one." The entered lineups covered 6/12 screen names but left the TOP of the screen (Young, Rose, Bryson) at 0/5, and the near-miss counterfactual is blunt: best single swap was Fitzpatrick→Young (+74.5), and 3 swaps separated the best lineup from the winner. Meanwhile two lineups spent dart slots on four OFF-screen names (Sullivan, Reed, Smith, Detry) and finished 69.2 / 82.8 — the portfolio's two worst.
- **Pool calibration:** tiers ordered for the first tracked slate (Core 58.0 > Good 57.5 > Okay 49.3 > Fade 32.5 ✓). Leakage: five Fade-tier players scored 60+, worst Rasmus Neergaard-Petersen (85.5, buried in Fade yet present in two top-10 winning lineups). Board discipline is working; the Fade tail needs a ceiling check before burial.
- **Grader validation:** positive signal — the one pre-lock-flagged lineup (the Hovland fade violation) finished 69.2 pctile, worse than 3 of 4 clean lineups. The calibrated gates pointed the right way this slate.

**Process trend (results.jsonl):** best percentile 51.9 (Shinnecock) → 98.3 (Travelers) → 23.5 (Open); leverage capture 0.33 → 0.0 → 0.5. Direction is right, and the improvement is traceable to process (definer named in doc, tiers ordered, fades correct), not variance alone.

## Shark gap

**Axis: `leverage_pct`, delta +60 — and it is RECURRING in the same direction.** This slate 80% of your lineups carried a sub-5% piece vs the tracked in-field pros' 20%; at Shinnecock the same axis topped the gap at +53.3. Two of the last three slates, same axis, same sign: **you out-dart the pros, and it isn't paying** (their best bullet 8.3 pctile vs your 23.5; your leverage capture 0.5 despite the higher dart rate).

The mechanism, stated as process: **in a 3.5K-field 5-Max your five bullets are already 100% unique, so extra sub-5% darts buy no uniqueness — they only add bust risk — while the actual definers keep landing in the 8–19% mid-owned band (Young 8.7%, Burns 13.6%; zero definers sub-5% this slate), which is where the pros concentrate (own/slot 20.1 vs your 16.5, chalk-anchor exposure 0.6 vs your 0.4).** The differentiation budget is being spent one tier too low. Note the nuance: the sharp-playbook envelope says "≥1 sub-5% piece in MOST lineups" — the leak is not carrying darts, it's carrying them in nearly every lineup and sourcing them off-screen. Birthed as `pga-classic-2026-07-22-dart-rate-exceeds-in-field-pros` (hypothesis).

## Adherence (discipline, graded separately from analysis)

- **1 hard fade violated:** L2 carried Viktor Hovland against the doc's explicit FADE. It was flagged by the grader pre-lock and finished 69.2 pctile — the violation was visible, named, and cost anyway. First slate with adherence tracking, so no cross-slate violation trend yet; the violation is logged as the fourth confirmation on the codified `entered-lineups-must-trace-to-plan` (its modern Grade-tab expression).
- **Soft calls honored:** Fleetwood underweight (0/5 — arguably over-honored; he anchored the winner, but underweight-to-zero is within the call's letter), Si Woo lean-fade (1/5 ✓), Cantlay (0/5 ✓).
- **Leverage candidates: 6 of 12 rostered — but the wrong six were skipped.** Young (the winner's carrier), Rose, Bryson, Reitan, Poston, Scott unrostered; the doc had declared the screen "this slate's priority." Covering half the screen while improvising four off-screen darts is the discipline finding of the slate — logged as the third (promotion-triggering) confirmation on `design-exposures-before-lineups` and as the new `darts-come-from-the-screen` hypothesis.

## Codified-rule check

| Codified rule | This slate | Mechanism vs actuals |
|---|---|---|
| never-zero-value-chalk-anchor | Applied (Scheffler 2/5, Rory 2/5) | Held — Scheffler 81.5 in two top-10 winners |
| leverage-spine-pairing | Not triggered (no overweight pair called a spine) | — (see hygiene: sub-20-combined gate merge) |
| portfolio-exposure-cap | Applied (max 2/5 any player) | Held — the 2/5 Fitzpatrick cap contained the bust |
| track-slate-lock-stat | Applied at autopsy (Burns 66.7%, Young 44.4% of winners) | Held — produced this review's Burns finding |
| course-history-sub5-scan | Not applied as written (post-redesign CH moot); already at 2 contradictions | **Demotion overdue — see Proposed codifications** |
| se-leverage-cap-two | Not triggered (5-Max, SE-scoped rule) | — (note: the winner ran 4 sub-10 pieces in 5-Max; the cap stays SE-only) |
| trap-vs-value-chalk | Applied (Hovland trap ✓) but mis-sorted Fitzpatrick to value | **2nd mechanism failure — demotion/narrowing proposed** |
| two-build-max | Not triggered (no optimizer iteration; hand-built) | — |
| se-primary-contest-selection | Applied (5-Max small-field) | Held |
| fade-needs-ownership-to-materialize | Applied explicitly (Hovland inline check) | Held both directions (Hovland own showed → bust; Si Woo own undershot → hit) |
| entered-lineups-must-trace-to-plan | Partially honored (graded pre-lock; 1 fade violated) | Held — flagged lineup underperformed |
| winning-structure-13own-2to3-darts | Applied ("~13% per-player own, 2–3 sub-10%") | Held dead-on (winners 13.94 / 2.25 / 100% unique) |
| leverage-play-mandatory | Applied — screen NAMED Young | Held; first doc-level identification in 5 slates |
| mid-owned-value-spine-over-darts | Applied (band surfaced) | Held — all 4 definers in the 8–19% band |

## Lesson ledger changes

- `fade-needs-ownership-to-materialize` (codified): **+ confirmation #4** — the check ran inline in the doc; both directions held (Hovland/Si Woo).
- `leverage-play-mandatory` (codified): **+ confirmation** — sub-20% smash defined the slate again AND the scan named him (Young) pre-lock for the first time in five slates.
- `mid-owned-value-spine-over-darts` (codified): **+ confirmation #3** — all four definers in the 8–19% band, zero sub-5%; only Burns missing from the doc (improvement from all-four-missing).
- `winning-structure-13own-2to3-darts` (codified): **+ confirmation** — winners 13.94% / 2.25 sub-10 / 100% unique; user again above the envelope (16.49%).
- `single-vendor-overweight-self-erosion`: **hypothesis → validated, + confirmation #1** — Fitzpatrick own-drift 25.5→37.6 bust and MacIntyre drift 20.9→28.9 confirm the refined (narrative-names-only) drift guard; the Burns discriminator held.
- `vendor-independent-ceiling-scan`: **hypothesis → validated, + confirmation #1** — the scan ran and broke the definer-outside-the-lens streak; the Burns hole names its next test.
- `design-exposures-before-lineups`: **hypothesis → validated, + confirmation (3rd mechanism slate)** — no exposure governor → screen's #1 name 0/5 while off-screen darts got slots. Promotion proposed below.
- `dose-darts-to-course-variance`: **+ confirmation (5th mechanism slate)** — birdie-fest+cut winners ran 2.25 darts, in the predicted ~2–2.5 band. Promotion proposed below.
- `trap-vs-value-chalk` (codified): **+ contradiction #2** — coffin +8.2 sorted Fitzpatrick as value chalk; he was the slate's #1 trap. Demotion/narrowing proposed below.
- `entered-lineups-must-trace-to-plan` (codified): **+ confirmation #4** — the grader-flagged fade violation underperformed 3 of 4 clean lineups.
- **Born (hypothesis):** `pga-classic-2026-07-22-dart-rate-exceeds-in-field-pros` — the recurring shark-gap axis (see 1b), portfolio sub-5% rate vs the pro envelope.
- **Born (hypothesis):** `pga-classic-2026-07-22-darts-come-from-the-screen` — off-screen darts (Sullivan/Reed/Smith/Detry) produced the two worst lineups while the screen's best names sat unrostered.

## Venue file changes

`rules/pga_classic/courses/royal_birkdale.md`: removed the UNVERIFIED marker (first slate now logged) and appended the 2026-07-22 per-slate observation — defenseless-Birkdale/birdie-fest read confirmed (winning 479); winners 13.9% own / 2.25 sub-10 / 100% unique; links-pedigree-gated-on-form was the definer profile (Young, Burns) while narrative steam busted (Fitzpatrick 37.6% own, 22.0); post-redesign CH stayed near-worthless; Monday-qualifier darts didn't decide it; tee-wave edge untestable from standings.

## Ledger hygiene

**Stale hypotheses:**
- `single-vendor-overweight-self-erosion` — **KEEP (and now confirmed/validated).** Not actually stale: this slate produced its first clean mechanism confirmation (Fitzpatrick own-drift steam-bust; MacIntyre drift as predicted). The deterministic flag predates this slate's evidence.
- `leverage-spine-needs-sub20-combined-own` — **KEEP, resolve by MERGE** (below). GPP guard applies: it went unconfirmed only because no strategy since RBC has labeled an overweight PAIR a spine — the trigger never occurred, which is not a mechanism failure. Rather than let a gate-with-no-trigger age forever, fold it into its parent codified rule as a scope condition.

**Near promotion (the exact third-slate mechanism each needs):**
- `contrarian-needs-leverage-anchor` (validated, 2/3) — not triggered this slate. Third confirmation requires: a contrarian build whose coffin-grade leverage-floor anchor demonstrably prevents collapse when the mid-range picks bust around median (or the converse: an anchor-less contrarian build imploding to a near-zero with no path).
- `design-exposures-before-lineups` — **third slate CONFIRMED here** (negative direction: no exposure governor → Young 0/5). Meets the count; codification proposed below.

**Overdue promotions:** both codification edits written below — `ch-scan-needs-skill-gate` (3 slates) and `dose-darts-to-course-variance` (now 5 slates).

**Merge decisions:**
- `course-history-sub5-scan` ↔ `major-pedigree-in-form-leverage` — **KEEP-SEPARATE.** One is a framework scan being demoted/replaced; the other names a champion-pedigree source. Different mechanisms; the cross-link is lineage, not overlap.
- `ch-scan-needs-skill-gate` ↔ `major-pedigree-in-form-leverage` — **KEEP-SEPARATE.** Both are "gate pedigree on form," but one gates the course-history scan, the other names a player-source (recent champions). They compose; neither subsumes the other.
- `mid-owned-value-spine-over-darts` ↔ `major-pedigree-in-form-leverage` — **KEEP-SEPARATE.** WHERE slates are won (the band) vs one SOURCE of band members.
- `mid-owned-value-spine-over-darts` ↔ `vendor-independent-ceiling-scan` — **KEEP-SEPARATE.** The band lesson is codified; the scan is its identification method. Merging a codified rule into a validated one would blur lifecycle state.
- `single-vendor-overweight-self-erosion` ↔ `vendor-independent-ceiling-scan` — **KEEP-SEPARATE.** Both are single-vendor pathologies but opposite failure modes: sizing an edge the vendor over-states vs omitting players the vendor never flags.
- `major-pedigree-in-form-leverage` ↔ `vendor-independent-ceiling-scan` — **MERGE.** Surviving id: `vendor-independent-ceiling-scan`. After the Travelers contradiction broadened major-pedigree beyond majors, its content ("an in-form proven closer/elite at sub-15% own is a systematic blind spot") is exactly one named row of the ceiling board, and this slate both mechanisms fired through the same screen (Lowry the in-form 2019 champ at 8.4% hit 66.0; Young the in-form links pedigree hit 96.5). Combined statement: the vendor-independent ceiling scan's board MUST explicitly include recent tournament/major champions and proven closers gated on a current-form floor, flagging any that survive the gate at sub-15% projected own as leverage — pedigree without form stays lottery-only (Koepka). Merge edit in Proposed codifications; `major-pedigree-in-form-leverage` closes with a pointer, its evidence trail preserved in-file.

**Removed-feature check:** no live lesson's mechanism depends on a removed feature. (`act-on-redteam-portfolio-findings-on-ship` is already retired on those grounds; `entered-lineups-must-trace-to-plan` and `two-build-max` re-expressed cleanly through the Grade tab / hand-build workflow this slate.)

## Proposed codifications

*(Proposals only — nothing below has been applied to framework.md/philosophy.md. Approve via the app.)*

**1. PROMOTE `ch-scan-needs-skill-gate` + DEMOTE `course-history-sub5-scan` (one combined edit — the new rule replaces the failed one).**
In `framework.md` Section 2 (Slate Diagnostics), replace the required scan text "course-history-boost × sub-5% ownership cross-reference" (and its echo in Section 9's pre-submission checklist) with:

> **Gated cheap-leverage scan (required):** cross the course-history/pedigree boost list against sub-5% projected ownership, then GATE on a minimum skill/current-form floor — bottom-decile ball-strikers and cold pedigree names are lottery-slot-only regardless of course stickiness. Treat the form/value engine (hot approach numbers, value-report flags) as a CO-EQUAL source of sub-5% leverage; the slate-defining cheap play has come from the form side in every logged test (Poston, Suber, Clark). Pedigree WITHOUT form = bust (Koepka, Shinnecock); pedigree WITH form = the play (Clark; Young, Birkdale).

Mark `course-history-sub5-scan` retired in the ledger (`retired_reason`: mechanism failed at both a high- and near-zero-stickiness course; superseded by the skill/form-gated version) and `ch-scan-needs-skill-gate` codified.

**2. PROMOTE `dose-darts-to-course-variance` (5 mechanism slates).**
Add to `framework.md` Section 3 (Ownership Tier Framework):

> **Dart-count calibration:** hold ~13% average per-player ownership, and set the per-lineup sub-10% dart count by course archetype: birdie-fest ~2; no-cut birdie-fest ~2.5; tough non-cut ~3; tough or birdie-fest WITH a 36-hole cut, cap at ~2–2.5 (each added cut-coinflip multiplies binary cut-out risk). Verified: mining n=168 plus RBC (~2), Shinnecock (2.1–2.7), Travelers (2.5), Birkdale (2.25).

**3. PROMOTE `design-exposures-before-lineups` (3 mechanism slates).**
Add to `framework.md` Section 7 (Exposure Caps / portfolio construction):

> **Exposures before lineups:** before building any multi-lineup set (and even a single bullet), write target exposures first — the value spine's carry rate, the mid-owned multipliers, the dart pool drawn FROM the strategy's definer screen, and a hard cap per expensive chalk anchor — then fill lineups to those targets. Independent lineup-by-lineup assembly has no governor: the screen's best value loses slot competition (Young 0/5 at Birkdale as the winner's carrier; Fox/Yellamaraju at RBC) and incoherent chalk-stack builds slip through.

**4. DEMOTE (narrow) `trap-vs-value-chalk` — 2nd mechanism contradiction on a codified rule.**
In `framework.md` Section 6 (Anchor Selection Logic, "Trap chalk vs value chalk"), replace "the coffin list is the primary signal for the split" with:

> The coffin list proposes the trap/value split; OWNERSHIP BEHAVIOR disposes it. A coffin fade is void when the projected ownership never materializes (sub-12% actual = mispriced leverage, not trap — Memorial), and a coffin overweight is void when ownership steams past projection on a narrative name (drift toward the published optimal converts "value chalk" into the slate's biggest trap — Rai at RBC, Fitzpatrick at Birkdale: 25.5%→37.6%, 22.0 FPTS, 54.1% of fish vs 2.8% of winners). Before lock, sanity-check both sides of the split against a late-ownership read; a stable, floored name at flat projected own keeps its coffin label (Burns, Shinnecock).

The lesson stays codified with this narrowed text (scope reduction, not retirement — the split itself keeps working at the top of the board).

**5. MERGE `major-pedigree-in-form-leverage` → `vendor-independent-ceiling-scan`** (ledger edit, per Ledger hygiene): append the in-form-proven-closer/champion row to the surviving lesson's statement as written above; set the merged-away id to retired with `retired_reason: "merged into [[pga-classic-2026-07-01-vendor-independent-ceiling-scan]] after the Travelers contradiction broadened its scope beyond majors"`. No framework edit yet — the surviving lesson is validated, not codified.

## Applied

Applied 2026-07-22 (user-approved). **framework.md:** (1) Section 2's un-gated "course-history boost × sub-5% own" required scan replaced with the **Gated cheap-leverage scan** (skill/current-form floor, form/value engine co-equal), with the three Section 9 checklist echoes (9A/9B/9C) updated to the gated version; (2) **Dart-count calibration** added to Section 3 (birdie-fest ~2 / no-cut birdie-fest ~2.5 / tough non-cut ~3 / any 36-hole-cut course capped ~2–2.5); (3) **Exposures before lineups** added to Section 7; (4) Section 6's "Trap chalk vs value chalk" narrowed to "the coffin list proposes; ownership behavior disposes" with the late-ownership sanity check. Last-updated stamp set to 2026-07-22. **lessons.yaml:** `ch-scan-needs-skill-gate` → codified (framework Sections 2 + 9); `course-history-sub5-scan` → retired (mechanism failed at both stickiness extremes; superseded by the gated version); `dose-darts-to-course-variance` → codified (Section 3); `design-exposures-before-lineups` → codified (Section 7); `trap-vs-value-chalk` stays codified with the narrowed statement; `major-pedigree-in-form-leverage` → retired, merged into `vendor-independent-ceiling-scan` (champions/proven-closers row appended to the surviving statement, which stays validated — no framework edit); `leverage-spine-needs-sub20-combined-own` → retired, merged into `leverage-spine-pairing` as its sub-~19%-combined-own scope condition. All KEEP / KEEP-SEPARATE hygiene decisions left untouched. No philosophy.md edits were proposed or made.
