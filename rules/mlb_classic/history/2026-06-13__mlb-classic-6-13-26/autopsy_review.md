# Post-autopsy review — MLB Classic 6.13.26

Slate: 8-game DK MAIN (4:05/4:10 ET). Two SE contests entered: **Rally Cap** ($8, 882, top-heavy $2K-to-1st) → **L1** (BAL-5/CIN-3, #902) finished **rank 383 / 43.4%**; **Chin Music** ($5, 1,426, flatter) → **L2** (LAD-5/ARI-2, #1164) finished **rank 220 / 15.4%**. Best percentile **15.4** (L2). ROI tracked off-repo (winnings null, by design). Method: SELECTED from a 5,024-lineup SaberSim pool, decoupled per a red-team FIX.

## Process scorecard

**Grade: A− (strong, honest process; one structural decision — the cross-contest decouple — is worth re-examining).**

- **Pre-flight checklist — PRESENT and HONEST, both files.** `slate_analysis.md` and `lineups.md` each open with a full six-line checklist with specifics. Slate confirmed against bundle timestamp (14:56) and Stone/screenshot dates; off-slate 7:10/10:05 games correctly excluded. Venue handling honest: read citi_field, created three UNVERIFIED stubs (rate_field, camden_yards, great_american_ball_park) and flagged them as built from this slate's articles only. No checklist theater — claims were real.
- **Open lessons — APPLIED and NAMED, not rubber-stamped.** Condensation (held Yamamoto), salary-enabler (cheap Chandler SP2, not a 2nd ace), pivot-budget (one leverage axis), five-man-conditional, Anchor-Equivalence (off all three crowded arms via cheap SP2), sin-projection-pool-omissions (cross-checked, no omission this slate), blank-own-artifact (verified the 0.0% rows were real low-own bats). The `weather-proof-dome-stack-pivot` lesson was correctly **rejected with the mechanism reason** (no rain concentrating field own; Rate is the open-air hitting game, not a dome refuge). Textbook lesson-review discipline.
- **Lessons that paid:** condensation → Yamamoto held and smashed (34.15); enabler → Chandler 17.75 (slate-defining); Anchor-Equivalence clean (off Suarez/Skubal/deGrom). No applied lesson backfired.
- **Untracked-entry rule — HONORED (4th positive case).** Both entered lineups match the archived `lineups.md` player-for-player (Rally = L1 #902; Chin = L2 #1164). Every entered lineup carried a thesis, passed red team, and was in the portfolio audit. The loop graded exactly what was played.
- **Red team — RAN; FIX HEEDED.** Original portfolio drew a portfolio FIX (both entries shared a LAD-5 + Yamamoto core); the FIX was taken (L1 re-selected to BAL/CIN, LAD-0), then re-reviewed SHIP/SHIP. Verdict adherence: clean. **Verdict accuracy in hindsight — the nuance below.**
- **Selection deviation from the analysis (minor miss):** L2's LAD-5 was Freeman/Muncy/Betts/Ward/Tucker — it **omitted Ohtani**, whom the analysis explicitly named as the LAD anchor to "build the 4-man around." Ohtani went 22.0 at 3.5-5.5% own (a slate-defining play). Neither entry rostered him. Not fatal (L2 still got Muncy), but the build deviated from its own stated anchor.

### Red-team verdict accuracy in hindsight (the headline finding)

The FIX correctly diagnosed a real flaw (two entries on the same LAD-5 + Yamamoto core). But the **resolution** decoupled L1 entirely off LAD — the analysis's **#1 edge** and the home of the **slate-defining play** (Max Muncy $4,500, 39 pts, 9% own, in 65-70% of top-20 winners and the rank-1 lineup in BOTH contests). L1 landed on the two games that died (Camden, GABP) and finished **43.4%**; the LAD-holding L2 finished **15.4%** — the better of the two. So the heeded FIX, while structurally defensible (a high-ceiling off-chalk build is the correct shape for a top-heavy Rally Cap), drove the leverage entry off the slate's best game.

This surfaces a deeper question the red team's portfolio framing missed: **the two entries are in SEPARATE contests with independent prize pools, so decoupling them from EACH OTHER buys nothing.** Each should be the best single build for its own field/payout; differentiation that matters is per-contest (ceiling→top-heavy, floor+ceiling→flat), which is compatible with both holding LAD. Born as a hypothesis this review (see below). **GPP guard:** one slate, and the off-LAD ceiling build WAS the contest-appropriate shape — the loss is not the evidence; the independent-payout structure is.

### Other mechanism observations
- **Condensation magnitude undershot.** Yamamoto (projected-own #1, 35.3%) condensed to only 37.4%/43.3% — up, but +2 to +8, not the flat +30 the codified lesson applies (which led the analysis to price his fade as "a ~55-60% binary"; real fade was 37-43%). He sat in a tight 3-arm premium tier (deGrom 25.5, Skubal 27.8) — a candidate moderator. Magnitude refinement logged; direction is now 4-for-4.
- **Pitcher slot stayed live** because condensation was mild — Manaea (NYM, $5,900, low own) 19.1 and Soroka populated many winners. Consistent with chalk-ace-smash compression scaling on condensation magnitude (the contrast case to 6/12's hard-condensing Misiorowski). Promoted that hypothesis to validated.
- **Blanket low-total bat fade left a spike on the table:** the analysis PASS'd all TEX/BOS bats ("avoid bats"); Samad Taylor (TEX, $2,500) went 24.0 at ~7% own, a slate-defining play in 40-45% of top-20. Even the lowest-total game produced a cheap spike — a note, not a process failure (the game-level fade was a reasonable prior).

## Lesson ledger changes

Edited `rules/mlb_classic/lessons.yaml`:

- **`se-chalk-pitcher-own-condensation` (codified)** — added 6/13 confirmation: up-DIRECTION confirmed a 4th time (Yamamoto 35.3→37-43%), but MAGNITUDE muted (+2-8 vs the flat +30). Calibration flag; candidate moderator (tier isolation) named.
- **`chalk-ace-smash-compresses-pitcher-leverage` (hypothesis → VALIDATED)** — added 6/13 confirmation as the contrast case: mild condensation (Yamamoto 37-43%) left the pitcher slot live, winners diverged on pitcher (Soroka/Manaea), and bat-spread was correspondingly milder (5.3-5.7 sub-10 vs 6/12's 7.6). The compression scales monotonically with condensation magnitude. Practical upgrade: gate "lean bats MORE spread" on the ace actually condensing hard, not merely being chalk.
- **`pivot-budget-small-field-se` (codified)** — added 6/13 confirmation: band held (top-20 winners 12.6-13.4% own / 5.3-5.7 sub-10) and the 6/12 high-density drift did NOT persist; the 7.6 extreme tracked a 1,783 field + hard-condensing smash ace, not field size alone. Partially resolves the standing WATCH NOTE.
- **`salary-enabler-pitcher-chalk` (codified)** — added 6/13 enabler-keep confirmation (4th): Chandler $6,200 kept as cheap SP2 in both entries, 17.75 pts (slate-defining). Leash clause untested this slate.
- **`untracked-entry-bypasses-loop` (codified)** — added 6/13 confirmation (4th, positive): both entries tracked and audited; the loop graded what was played.
- **NEW hypothesis `independent-se-no-cross-decouple`** — separate SE contests don't share a prize pool, so portfolio-decouple discipline doesn't transfer across them; each entry should be the best build for its own field even if both express the same top edge. Scope boundary (not contradiction) of `distinct-thesis-per-lineup`. Mechanism evidence: the cross-contest decouple drove L1 off the #1 edge/Muncy into dead games (43.4%) while the LAD-holding L2 finished 15.4%.
- **NEW hypothesis `condensation-magnitude-vs-tier-isolation`** — condensation magnitude scales with how isolated the consensus #1 arm is; the three +30 events were each a lone #1, while Yamamoto in a tight 3-arm tier condensed only +2-8. Size pitcher fades to tier isolation, not a flat +30.

## Venue file changes

- **`rate_field.md`** — appended 6/13 result: the wind-out "GOOD HITTING" read CONFIRMED for the favorite (LAD produced Muncy 39 / Ohtani 22 / Betts 15; CWS contained, Yamamoto smashed). Takeaway: with wind out + strong favorite offense, treat Rate as the slate's premier hitting environment even at price-suppressed ownership.
- **`camden_yards.md`** — appended 6/13 result: the two-sided live-game read mostly did NOT deliver (Alonso 24 the lone BAL bat; SD middling, Sheets 16 / Tatis 9). Two weak starters ≠ guaranteed eruption; played near-neutral — a leverage trap this slate.
- **`great_american_ball_park.md`** — appended 6/13 result: the bandbox did NOT carry the offenses (CIN punt side dead — Stewart/Bleday 0.0; ARI unremarkable). The park reputation oversold a 5.25 total; don't over-weight the tag when the cheap side is the leverage angle.

## Proposed codifications

**None this slate.** No lesson newly reached the 3-mechanism-confirmation promotion bar (the two new lessons are 1-slate hypotheses; `chalk-ace-smash` promoted to *validated* on its 2nd observing slate but needs a 3rd before a framework proposal). No lesson reached a 2nd mechanism contradiction (the enabler leash clause stayed at 1; this slate did not test it). The condensation-magnitude refinement and the cross-contest-decouple scope boundary are mechanism-based but unconfirmed — they need a 2nd and 3rd slate before being proposed for `framework.md`. Codified lessons accrued confirming evidence only; no framework/philosophy edits proposed.
