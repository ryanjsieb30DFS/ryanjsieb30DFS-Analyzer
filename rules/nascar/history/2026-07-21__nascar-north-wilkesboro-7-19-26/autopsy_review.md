# Post-autopsy review — North Wilkesboro 7/19/26 (logged 2026-07-21)

Two SE bullets: **$15K Engine Block (1,470)** — rank 109, top 7.4%, cashed. **$5K Engine Block (490)** — rank 404, top 82.4%. Winning scores 447–452; Joey Logano's 180.75 at 18.9% ownership decided the slate.

## Process scorecard

**Pre-flight checks: honored.** The strategy's substance shows every silent check ran. The venue file was created and used (the front-row-dominator DFR data and the 450-lap dominator framing anchor the whole doc). Anchor-Equivalence appears at the top of Edges & tensions (Blaney 47% / Bell 46% as the substitutable coin flip). Open lessons were visibly applied: the mid-pack-PD lesson drove the Gilliland/Stenhouse definer picks, the codified "MME or fade = fade in SE" rule drove the SVG/Suárez/Hocevar/Chastain fade cluster, and the process-trend read-back ("your leverage capture went 0% and 50%") was quoted in the doc itself.

**The analysis was good; the hand-off to the entered lineups was the failure.** Scorecard by call:

| Strategy call | Actual | Verdict |
|---|---|---|
| Logano Good tier, "GPP Fav," 24% own | 180.75, race-winner of the slate; in 100% of $15K top lineups | ✅ The call that cashed the $15K bullet |
| "Dominator pool lives at the front" | Logano/Hamlin (64.5)/Gibbs (60.5) all front-runners | ✅ Held (Briscoe from P30 the exception) |
| Sub-10% definer list (12 names) | SVG 61.0 @ 9.5%, Suárez 45.05 @ 5.6%, Gilliland 46.9 @ 5.1% all on it; $15K winner carried three sub-10% pieces | ✅ Screen worked / ❌ **0 of 12 entered** |
| Anchor-Equivalence: "split the two bullets across the Blaney/Bell coin flip" | Bell in BOTH bullets, Blaney in neither; Bell 17.9 @ 66–68% actual | ❌ **Execution violation of a codified rule** |
| Core tier: Bell / Blaney / Bowman | 17.9 / 23.6 / 15.9 — Core averaged 19.1, the worst tier on the board | ❌ Tier ordering broke (Good 53.9 > Okay 32.2 > Fade 21.8 > Core 19.1) |
| Reddick as the prime sub-10% definer (vendor 34.4 proj vs DDD fade) | −7.15 | ❌ The one spot where the article fade beat the vendor number — and the contract-parser bug that mislabeled him "fade" accidentally kept him out |
| Briscoe UNDERWEIGHT / Bubba LEAN FADE (2-of-2 fish-trap history) | 80.05 and 64.5 — both hit, both in the $15K winner | First loss for the fish-trap signal. The mechanism (ownership outrunning projection) was priced correctly; outcome went the other way. Evidence, not contradiction. |

**The two bullets shared 4 of 6 players** (Bell, Zane Smith, Herbst + overlap patterns), so the portfolio was effectively one thesis entered twice — and that thesis was the busted 68% anchor. The $5K bullet carried two near-zeros (Bell 17.9, Berry −3.0) by lap 200.

**Pool calibration:** the board buried five Fade-tier players who out-scored the Core average (Bubba 64.5, SVG 61.0, Suárez 45.0, Ty Dillon 33.5, Hocevar 26.4) — four of the five were buried BY the codified "MME or fade" rule, which took its first SE mechanism contradiction this slate (logged in the ledger).

### 1b. Shark gap

**Versus the tracked pros: no gap this week — and the pros whiffed.** The 5 named-shark entries in the $15K ran 35.8% own/slot vs your 35.7 (delta −0.1), 0% sub-5% leverage vs your 0%, and their best finish was top 12.1% vs your 7.4% — you beat every tracked shark in the field. The chalk-comfortable shark envelope (34%/slot, leverage rare) lost this slate to a 3-leverage-piece winner at 17.9% avg own.

**Versus the winners: the same axis as always — low-owned coverage.** Top-20 ran −8.87 own/slot below you and +1.15 sub-10% pieces per lineup ($15K); your lineups carried zero. This is the third consecutive slate where the separating axis is leverage coverage, not chalk selection: Chicagoland's shark-gap top was `leverage_pct −16.7`, Atlanta's was `own_per_slot −15.7`, and the leverage-list usage sequence is 0% → 50% → 0/12. **The mechanism, stated:** *my entered lineups systematically carry zero sub-10% pieces even when my own strategy names the right ones — the leverage screen lives in the document, not in the build.* This is a RECURRING structural leak and it birthed `nascar-2026-07-21-definer-screen-must-reach-entries`.

### 1c. Adherence

**Fade discipline: perfect. Leverage discipline: zero.** All 9 contract calls followed (Reddick/Hocevar/SVG/Suárez/Hill/AJ/Chastain fades at 0% exposure; Briscoe underweight and Bubba lean-fade at 0%). Leverage candidates rostered: **0 of 12**. Discipline graded separately from analysis: the fade side happened to score well this week (Reddick −7.15), but the leverage side is the standing violation pattern — results.jsonl now shows leverage capture 0.0 (7/12), 0.5 (7/14), and 0/12 candidates covered here. That trend, not this result, is what confirmed `nascar-2026-05-01-portfolio-gaps-addressed-pre-lock` (promoted to validated) and birthed the definer-screen lesson.

**Note the asymmetry as a finding in itself:** the contract's fade half is enforced downstream (the Sim tool auto-applies hard fades) while the leverage half has no enforcement anywhere — which is exactly where the discipline holds and breaks, respectively. Also flagged: the contract parser inverted Reddick (strategy's prime definer → logged as "fade") and Chastain (explicit fade → logged as "pass"); it saved points this week but the `src/strategy_contract.py` VERDICT parse is wrong and already noted in autopsies.md.

### 1d. Codified-rule check

| Codified rule | This slate | Mechanism status |
|---|---|---|
| `anchor-equivalence` (≥1 lineup runs the equivalent alternative) | **Applied in the doc, VIOLATED in the entries** — Bell in both bullets, Blaney in zero | Mechanism intact but incompletely specified: the field resolved the "coin flip" 68/34 (not 47/46), and the actual payer was the third front-runner (Logano) outside the projected-ownership equivalence pair. No contradiction logged; the ownership-concentration wrinkle birthed `se-actual-own-concentrates-on-consensus` |
| `mme-or-fade-means-fade-in-se` | Applied fully (all tagged drivers at 0%) | **First mechanism contradiction** — $15K winner rostered Suárez + Hocevar; SVG was the top leverage score. 1 of 2; stays codified, watch short tracks |
| `sound-chalk-toward-field-rate` / `50-pct-chalk-rule` | Applied — Bell held at field rate as triple-pillar chalk | Bell busted at 66–68% own, but a P3 performance bust is variance, not a price/start-math failure. No contradiction (GPP guard). The real finding is upstream: the 46% projection was a floor, not an estimate |
| `sleeper-spike-floor` (≥2 of N lineups carry a sub-15%/sub-$6K PD driver) | **Not honored in entries** — Herbst (48–51% actual) and Zane Smith don't qualify; Gilliland/Stenhouse unused | Mechanism confirmed by the field: the cheap mid-pack band paid again |
| `midpack-pd-over-deep-back-chalk` (validated, mid-pack half codified) | Applied in the doc (definer list sourced from the 11–30 band) | **Fifth confirmation** — the winners' entire differentiation layer came from that band |
| `hms-intermediate-double-up` / `hms-road-course-fade` / `superspeedway` scoping | Did not trigger (short flat track) | — |
| `anchor-equivalence-not-parity` | Did not trigger as written (the failure was zero coverage, not over-hedging) | — |
| `sim-roi-not-a-selector`, `post-roi-gold-standard`, `conservative-boost-dock-first`, `chalky-combos-scrub` | Did not / cannot trigger — see Ledger hygiene: `post-roi-gold-standard` references the removed Post-Contest Sim Data pipeline | Demotion proposal below for `post-roi-gold-standard` |

## Lesson ledger changes

- **`nascar-2026-05-17-mme-or-fade-means-fade-in-se`** — added first SE mechanism contradiction (winner rostered Suárez + Hocevar; SVG top leverage score; the tag may mean "low floor, live ceiling" at high-variance short tracks). Stays codified (1 of 2).
- **`nascar-2026-06-20-midpack-pd-over-deep-back-chalk`** — added fifth confirmation (11–30 band supplied the winners' differentiation at a track DFR called PD-unfriendly). Stays validated; codification-completion proposal below.
- **`nascar-2026-05-01-portfolio-gaps-addressed-pre-lock`** — added first mechanism confirmation (the strategy self-diagnosed the leverage gap in writing, named 12 candidates, entered zero; three of them defined the slate). **Promoted hypothesis → validated.**
- **NEW hypothesis `nascar-2026-07-21-definer-screen-must-reach-entries`** — the recurring shark-gap/leverage leak made mechanical: every SE bullet carries exactly one piece from the sub-10% definer list before entry; the Grade tab's flag is the checkpoint.
- **NEW hypothesis `nascar-2026-07-21-se-actual-own-concentrates-on-consensus`** — SE lock ownership concentrates on one anchor + the obvious value far beyond vendor projections (Bell 46→68, Herbst 22→51, Blaney deflating 47→33.5); projected own on the consensus anchor is a floor.

## Venue file changes

`rules/nascar/tracks/north_wilkesboro_speedway.md` — header upgraded from **UNVERIFIED** to **partially verified**; four date-stamped per-slate observations appended: (1) front-dominator thesis held but via the third front-runner, not the polesitter (Logano 180.75; Blaney/Bell busted); (2) mid-pack PD paid heavily despite the DFR base rate, winning shape = one mid-owned front dominator + three sub-10% mid-pack pieces; (3) SE actual ownership concentrated 20–30 points beyond DailyFan projections on the consensus side; (4) 450 green-heavy laps paid functional mid-pack cars, not carnage darts.

## Ledger hygiene

**Stale hypotheses (4):**

- `nascar-2026-05-01-portfolio-gaps-addressed-pre-lock` — **KEEP (now confirmed + validated).** The mechanism finally had a clean test this slate and fired verbatim: a diagnosed, written-down gap left unaddressed forfeited the slate's defining equity.
- `nascar-2026-05-01-ownership-shift-full-reevaluation` — **KEEP.** Untested for lack of a relevant trigger: no slate since birth has had a logged pre-lock ownership re-projection event (single DailyFan upload per slate; the drift module is the path for it to fire). GPP guard: untested ≠ wrong. Cross-linked from the new ownership-concentration hypothesis, which may eventually absorb it.
- `nascar-2026-06-28-roadcourse-deepback-revives-on-strategy` — **KEEP.** Road-course-scoped; the three slates since (intermediate, superspeedway, short flat) could not test it. Next road course is its shot.
- `nascar-2026-06-28-injury-narrative-not-a-fade-thesis` — **KEEP** (no injury-narrative slate has occurred since birth), but see the merge proposal below — its mechanism is the backup-car rule's mechanism.

**Near-promotion:** none flagged.

**Overdue promotion (1):** `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` — 5 confirming slates on the mid-pack half; codification-completion edit in Proposed codifications.

**Merge candidates (11 pairs):**

- `05-24-anchor-equivalence` ↔ `06-20-anchor-equivalence-not-parity` — **KEEP-SEPARATE.** Coverage rule vs sizing calibration; distinct mechanisms, codified in different doc sections, and each carries its own scoping history.
- `05-01-bet-sizing-reflects-inverse` ↔ `06-20-anchor-equivalence-not-parity` — **KEEP-SEPARATE.** General exposure-calibration principle vs the anchor-specific application.
- `06-20-carry-a-sub5-leverage-dart-mme` ↔ `06-20-midpack-pd-over-deep-back-chalk` — **KEEP-SEPARATE.** "Carry a dart" (portfolio floor) vs "where PD lives" (player sourcing); the new definer-screen lesson bridges them without merging them.
- `06-20-midpack-pd` ↔ `06-28-roadcourse-deepback-revives` — **KEEP-SEPARATE.** The latter is a scoping counter-lesson to the former's deep-back half; merging a lesson with its own scope-limiter destroys the contradiction trail.
- `05-01-backup-car-not-auto-fade` ↔ `06-28-injury-narrative-not-a-fade-thesis` — **MERGE.** Same mechanism, one sentence: a physical-risk narrative (backup car, injury) lowers the floor but does not erase the price/start/equipment edge, and when the field already discounts it, the fade is negative leverage. Surviving id: `nascar-2026-05-01-backup-car-not-auto-fade` (the codified one); combined statement and framework edit in Proposed codifications. The injury variant's Sonoma evidence rides along as a confirmation-style note.
- `05-01-hms-intermediate-double-up` ↔ `07-12-narrative-suppressed-elite-is-leverage` — **KEEP-SEPARATE.** Equipment edge vs narrative/ownership mechanism; the second must earn its own confirmations.
- `05-17-mechanism-check-before-reapplying-patterns` ↔ `07-12-narrative-suppressed-elite` — **KEEP-SEPARATE.** Meta-discipline vs a specific pattern.
- `05-24-anchor-equivalence` ↔ `07-12-narrative-suppressed-elite` — **KEEP-SEPARATE.** Cross-link is contextual, not duplicative.
- `05-24-anchor-equivalence` ↔ `07-14-superspeedway-doms-correlate-not-substitute` — **KEEP-SEPARATE.** The superspeedway lesson is the AE rule's track-type scope-out; it must stay distinct until a second drafting slate tests it.
- `05-17-mechanism-check` ↔ `07-14-superspeedway-doms` — **KEEP-SEPARATE.** Same reasoning as above.
- `07-14-multiyear-lapsled-weak-perrace-signal` ↔ `07-14-superspeedway-doms` — **KEEP-SEPARATE.** Dominator *correlation* vs dominator *prediction*; both Atlanta-born but different mechanisms.

**Removed-feature check:** `nascar-2026-05-24-post-roi-gold-standard` anchors on `post_roi_pct` from the Post-Contest Sim Data pipeline, which was removed with the SaberSim retirement — the mechanism can no longer fire in this tool. Retirement proposal below (user-approved, since it is codified). `sim-roi-not-a-selector`, `chalky-combos-scrub`, and the iteration-discipline lessons still have live surfaces (the sim tool, the bundle's chalk-combos section, the Grade tab's pair warnings) — **KEEP**.

## Proposed codifications

*(Proposals only — nothing below applied to framework.md / philosophy.md in this run.)*

1. **Complete the codification of `nascar-2026-06-20-midpack-pd-over-deep-back-chalk`** (5 confirming slates on the mid-pack half). Ledger: set `status: codified`; narrow the statement to the mid-pack half, with the deep-back-fade half explicitly superseded by `roadcourse-deepback-revives-on-strategy`. framework.md — Quick-Reference Decision Heuristics, replace the existing "Mid-pack PD is the leverage meat" line with:
   > **Mid-pack PD is the leverage meat (5-slate rule, all track types tested: intermediate, road, superspeedway, short flat).** Source place-differential from 11th–30th starters with a reachable floor path; do not fade a high-floor mid-pack car on track-fit narrative when its start sits in the venue's optimal band. This says nothing about fading deep-back chalk — deep-back is live alongside mid-pack (see road-course caution-revival lesson), it is just not where the reliable PD meat is.

2. **Merge `nascar-2026-06-28-injury-narrative-not-a-fade-thesis` into `nascar-2026-05-01-backup-car-not-auto-fade`.** Surviving statement:
   > A physical-risk narrative — backup car, injury, or equivalent — is a risk factor, not a fade thesis: it lowers the floor modestly but does not erase the price/start/equipment math (Bubba top-5 from P37 in a backup car at 65.6% own; Bell's fractured-wrist fade landing in Sonoma's #1 overall lineup at 12% own). When the field already discounts the driver for the narrative, the fade is negative leverage. Demand on-track evidence of degradation (practice/qualifying pace) before fading.
   
   framework.md — Quick-Reference Decision Heuristics: change "backup-car driver → don't auto-fade" to "physical-risk narrative (backup car, injury) → risk factor, not fade thesis; demand on-track evidence." Ledger: injury lesson `status: retired`, `retired_reason: "merged into nascar-2026-05-01-backup-car-not-auto-fade"`.

3. **Retire `nascar-2026-05-24-post-roi-gold-standard`** (removed-feature rule, not a mechanism failure). The `post_roi_pct` pipeline (Post-Contest Sim Data tab) no longer exists, so the codified instruction cannot be executed. framework.md: delete Step 6 mandatory check #12; philosophy.md: remove the "use post_roi_pct as the gold-standard retroactive equity metric" line from On Process Discipline. Ledger: `status: retired`, `retired_reason: "references the removed Post-Contest Sim Data / post_roi_pct pipeline; mechanism can no longer fire"`. If a SaberSim Ultimate integration revives an equivalent metric, re-birth as a fresh hypothesis.

4. **No action yet, on watch:** `mme-or-fade-means-fade-in-se` carries its first SE mechanism contradiction (this slate). One more — specifically a tagged driver defining an SE-winnable lineup at a non-chaos track — triggers a demotion/narrowing proposal (likely scope: "MME or fade = fade in SE *except* where the venue's variance profile makes low-floor/live-ceiling the winning SE shape").

## Applied

*User approved; applied 2026-07-21.* (1) `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` codification completed: framework.md's Quick-Reference "Mid-pack PD is the leverage meat" line replaced with the 5-slate-rule wording; ledger status validated → codified, statement narrowed to the mid-pack half with the deep-back-fade half explicitly superseded by `roadcourse-deepback-revives-on-strategy`. (2) Merge applied: `nascar-2026-06-28-injury-narrative-not-a-fade-thesis` retired (`retired_reason: merged into nascar-2026-05-01-backup-car-not-auto-fade`); the surviving backup-car lesson carries the combined physical-risk-narrative statement with the Sonoma Bell evidence as a confirmation note, and framework.md's heuristic now reads "Physical-risk narrative (backup car, injury) → risk factor, not fade thesis; demand on-track evidence." (3) `nascar-2026-05-24-post-roi-gold-standard` retired (removed-feature rule): framework.md Step 6 mandatory check #12 deleted and philosophy.md's "Use `post_roi_pct` as the gold-standard retroactive equity metric" paragraph removed from On Process Discipline; ledger `retired_reason` notes the removed Post-Contest Sim Data / post_roi_pct pipeline. All KEEP / KEEP-SEPARATE hygiene decisions left untouched; proposal 4 (mme-or-fade watch) required no edit.

*Re-verified 2026-07-21 (second apply pass):* all three approved proposals confirmed in place — framework.md Quick-Reference carries the 5-slate mid-pack wording and the physical-risk-narrative heuristic, Step 6's checklist ends at #11 with the post-ROI check deleted, philosophy.md's gold-standard post_roi paragraph is gone, and lessons.yaml shows midpack-pd `codified`, injury-narrative `retired` (merged into backup-car-not-auto-fade, whose statement carries the combined wording + Sonoma evidence), and post-roi-gold-standard `retired`. No further edits were needed.
