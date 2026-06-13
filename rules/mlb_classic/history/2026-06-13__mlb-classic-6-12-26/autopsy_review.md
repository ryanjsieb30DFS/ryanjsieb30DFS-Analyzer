# Post-autopsy review — MLB Classic 6.12.26

_Reviewed 2026-06-13. Archived slate: `rules/mlb_classic/history/2026-06-13__mlb-classic-6-12-26`. Two SE contests entered (980 + 1,783 field), one tracked lineup in each. Best finish 34.6th pct (rank 617/1,783) and 37.0th pct (rank 363/980) — mid-pack, down from the 6/11 ledger-best top 4.4%. GPP guard applies throughout: the mid-pack results and the MIL bust are variance, not evidence; only mechanism outcomes are graded._

## Process scorecard

**Pre-flight checklists — present and mostly honest, with one real dishonesty and two gaps.**

- Both `slate_analysis.md` and `lineups.md` open with full six-line checklists, specifics attached. The cross-checks were genuine work (SIN pool omissions found and one omitted starter rostered; duplicate-Muncy artifact caught; weather lesson rejected with its precondition correctly named absent). Salaries re-add correctly ($49,600 / $50,000). Own-pitcher blocks hold on both rosters. Both entered lineups match the tracked portfolio — the **tracked-entry HARD RULE held a 4th straight direction** (positive case again, like 6/11).
- **Dishonest justification (heeded by neither the build nor the fix):** L1's audit claimed its 6 sub-10% density "matches the 6/11 ledger-best build exactly." The red team proved this false (6/11 was 4 sub-10 at 16.8% avg own; L1 was 6 sub-10 at 10.3%) and instructed it be struck regardless of whether the lineup changed. It was **not struck** — the false claim is still in the archived `lineups.md` (shape note + rule-compliance section). This is the kind of wrong-number defense of a band breach the audit exists to catch, and it survived to lock. Logged as a process miss.
- **Open-lessons miscount:** checklist said "5 open"; the ledger held 6 (5 hypothesis + 1 validated). All six were in fact named and applied-or-rejected — cosmetic miscount, real work underneath.
- **Venue ritual — partial.** Only the axis-game park (`las_vegas_ballpark.md`) was read. L1's thesis game (MIL at American Family Field) had **no park file and none was created** — a ritual violation, since L1's entire EV case rested on a MIL blowup at an unread park. L2's thesis game (Rogers Centre) had a file that **went unread**. On a 13-game slate the two parks that actually drove the portfolio's theses were the two that weren't covered.

**Lessons applied vs ignored:**

- **Applied correctly:** `sin-projection-pool-omissions` (cross-check run, Jacob Wilson rostered in L2 from Stone data — and Wilson hit winning lineups, see ledger); `five-man-primary-conditional-on-blowup` (no 5-stack anywhere — vindicated, no team erupted); `late-build-bailout` (lineups landed ~14 min pre-lock but the tracked portfolio was entered with no untracked swap — adherence, like 6/11); `untracked-entry-bypasses-loop` (honored); `blank-own-snapshot-artifact` (cross-check run, Muncy duplicate caught, not rostered); `weather-proof-dome-stack-pivot` (rejected, precondition genuinely absent).
- **Misapplied — the slate's one process-attributable error:** the build used `se-chalk-pitcher-own-condensation` but bet the condensation would land on the **affordable** arm (Yesavage $8.5K) and constructed L2 to fade him. It landed on the **projected-own #1** (Misiorowski $12K, 25.2→55.6%), exactly as the prior two condensation events did and exactly as the red team warned. The "affordability" reasoning was a fresh inference the build layered on top of the lesson — not part of the lesson — and it was wrong. This is the headline mechanism finding (new hypothesis born; see ledger).

**Red-team verdict adherence & accuracy in hindsight:**

- **L1 → FIX (swap the 6th sub-10 Slater for double-digit-own glue; strike the false 6/11 claim): IGNORED.** Slater stayed in the entered lineup; the false claim stayed in the file. In hindsight the band-discipline half of the FIX was not the proximate cause of L1's mid-pack finish (MIL simply didn't blow up — variance), so ignoring the *swap* cost little. But the **strike-the-false-claim** half should have happened unconditionally and did not — that's the ledger-worthy adherence miss, an honesty fix declined.
- **L2 → SHIP: heeded (entered as-is), and correct per the rule set** (it was the mandatory Anchor-Equivalence lineup with genuine zero-own NYY leverage). BUT the red team's most important content was not the verdict — it was the **embedded warning**, repeated three times (L1 attack #3, L2 attack #1, portfolio finding #6): _"if the field condenses on Misiorowski (the projected-own leader, where it landed both prior slates), L2's fade halves in value."_ That warning was **dead right** and was **overruled** by the affordability hypothesis. Heeding it would have meant holding Misiorowski in both lineups rather than building L2 around a Yesavage-specific bust — and L2 (Joe Ryan) structurally missed the 58.65-point Misiorowski smash. **Strong evidence the red team's pattern-match beat the build's fresh inference; logged as evidence against over-trusting a novel corollary over the red team's historical pattern.**

**Bottom line:** the spine of the process was real (cross-checks happened, blocks held, tracked-entry honored, red team produced on time). Two process faults: (1) a false density justification that the red team flagged and that survived to lock, and (2) overruling the red team's correct condensation-direction warning with an unvalidated affordability inference — the one decision that genuinely cost EV (L2 off the slate's defining play). The mid-pack results themselves are variance.

## Lesson ledger changes

- **`mlb-classic-2026-06-11-se-chalk-pitcher-own-condensation` (validated):** added the 6/12 confirmation — **3rd confirming slate** (origin 6/10 Detmers + 6/11 Scott + this). Misiorowski 25.2→55.6/53.1%, +30 over projection, identical magnitude to the prior two, and he smashed (58.65). Meets the 3-confirming-slate promotion bar → codification proposed below. Confirmation entry also records the **direction correction**: condensation hit the projected-own #1, not the affordable arm.
- **`mlb-classic-2026-06-12-five-man-primary-conditional-on-blowup` (hypothesis → validated):** added 6/12 confirmation. No team erupted (overperformers scattered across HOU/TOR/BOS), rank-1 in both contests was a fully-spread 1-1-1-1-1-1-1-1 no-stack at 9.2% own, 5-man primaries rare in winners. L1's MIL-4 stacked for a blowup that didn't arrive. 2nd confirming slate → validated.
- **`mlb-classic-2026-06-12-sin-projection-pool-omissions` (hypothesis → validated):** added 6/12 confirmation. SIN pool omitted Thomas/Wilson/Williams; the cross-check caught it and Wilson was rostered — and Wilson appeared in the **rank-2 winning lineups in BOTH contests**, confirming the "omitted cheap stud = invisible leverage" mechanism. 2nd confirming slate → validated.
- **`mlb-classic-2026-06-10-pivot-budget-small-field-se` (codified — watch note only, no status/evidence change):** density band drifted high this slate (contest-1 winners 6.2 sub-10 at 14.2% avg own; contest-2, above scope, 7.6 sub-10 at 10.3%), and the user's near-band builds finished mid-pack while spread builds won. GPP guard + larger fields + the chalk-ace-smash dynamic mean this is **not** logged as a contradiction — recorded as a watch on whether the 3–5 density band is field-size- and chalk-ace-dependent.
- **New hypothesis `mlb-classic-2026-06-13-condensation-target-projected-leader`:** condensation lands on the projected-own #1 arm, not the cheapest viable chalk arm (price isn't the convergence driver, consensus rank is). Born from this slate's affordability mis-call; the red team flagged it pre-lock.
- **New hypothesis `mlb-classic-2026-06-13-chalk-ace-smash-compresses-pitcher-leverage`:** when the consensus ace both condenses and smashes, the pitcher slot stops differentiating and winning shifts to wide bat-spread; the mandatory Anchor-Equivalence alternative-anchor lineup carries real cost on such slates and should be treated as a deliberate ace-bust hedge.

## Venue file changes

- `parks/las_vegas_ballpark.md`: appended a **2026-06-13 per-slate observation**. The huge implied total (COL@ATH, 13.85) again produced **none of the slate-defining plays** (those came from HOU/TOR/BOS/ARI/STL) — the ownership-tax pattern held a 2nd straight slate, and the portfolio's "pieces, not mega-stacks" stance on the Vegas game was the right structural read for the park both times. Promoted the note from "lean" toward a working rule (buy the Vegas total in pieces, never as the primary stack), with the explicit caveat that we have not yet observed a slate where this park's big total actually erupted — so the rule is "don't pay the mega-stack tax," not "the park doesn't score." (No file was created for American Family Field or read for Rogers Centre this run — flagged under the process scorecard as a ritual gap, not a venue-file change.)

## Proposed codifications

_Proposals only — not applied. User approves via the Autopsy tab._

**Codify `mlb-classic-2026-06-11-se-chalk-pitcher-own-condensation` into `framework.md` (3 mechanism confirmations: 6/10 Detmers 38→69, 6/11 Scott 44→56-63, 6/12 Misiorowski 25→55).** Add the following bullet to the **`## Construction (codified from the lesson ledger)`** section, after the salary-enabler bullet:

```markdown
- **SE chalk-pitcher ownership condensation:** in small-field SE, the consensus chalk
  pitcher closes far ABOVE vendor projection — a casual field converges on one arm
  because pitcher is the slate's highest-variance single decision and SE fields don't
  diversify it. **The condensation target is the projected-own #1 arm, NOT the
  cheapest viable chalk arm** — price is not the convergence driver, consensus rank is
  (Detmers, Scott, Misiorowski were each the projected #1; the one slate that bet
  affordability instead, 6/12, built its fade on the wrong arm). When sizing any P1
  fade, assume the projected-own #1 closes far above projection: a "25% fade" can be a
  ~55% fade — more leveraged AND more binary than projected. Default is to **keep the
  condensing arm and take the pivot in the bats**, not to fade the arm. *(Codified
  2026-06-13; 3 mechanism confirmations: 6/10, 6/11, 6/12. Ledger:
  mlb-classic-2026-06-11-se-chalk-pitcher-own-condensation, with the projected-leader
  direction from mlb-classic-2026-06-13-condensation-target-projected-leader.)*
```

On approval, set the lesson's `status: codified` and `codified_in: "framework.md — Construction"`, and fold `mlb-classic-2026-06-13-condensation-target-projected-leader` into it as a confirmed corollary (it stays a tracked hypothesis until then).

**No other codifications or retirements this slate.** `five-man-primary-conditional-on-blowup` and `sin-projection-pool-omissions` are now validated at 2 confirming slates each — one more apiece to reach the promotion bar. No lesson has 2 mechanism contradictions, so nothing is a retirement candidate.

## Applied

_User approved 2026-06-13. Changes applied:_

- **`framework.md` — `## Construction`:** added the **SE chalk-pitcher ownership condensation** bullet (after the salary-enabler bullet, before Coors games), exactly as proposed — consensus chalk pitcher closes far above projection; condensation target is the projected-own #1 arm, not the cheapest viable chalk arm; default is keep-the-arm-and-pivot-in-the-bats. Tagged codified 2026-06-13 with the 3 confirmations (6/10, 6/11, 6/12).
- **`lessons.yaml` — `mlb-classic-2026-06-11-se-chalk-pitcher-own-condensation`:** `status: validated → codified`; `codified_in` set to `framework.md — Construction` (user-approved 2026-06-13), naming the 3 confirmations and the folded-in projected-#1 direction.
- **`lessons.yaml` — `mlb-classic-2026-06-13-condensation-target-projected-leader`:** `status: hypothesis → codified`; folded into the condensation lesson as a confirmed corollary, `codified_in` pointing at `framework.md — Construction`.
- No other lesson statuses changed; no retirements.
