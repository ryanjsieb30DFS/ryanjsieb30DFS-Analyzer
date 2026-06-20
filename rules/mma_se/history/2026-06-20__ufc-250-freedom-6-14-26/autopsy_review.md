# Post-Autopsy Review — MMA · UFC Freedom 250 (White House) · 6/14/26

> Captain-mode showdown (1 CPT 1.5× + 5 FLEX, $50K). Contest: **UFC Captain $25K Arm Bar — 150-Max, 5,945 field, 10 entries.** Winning score **618.43**. **Best lineup: rank 14 / 5,945 = top 0.24% (615.37).** ROI not tracked in-repo (third-party app). Reviewed inputs: manifest, slate_analysis.md, lineups.md, red_team.md, autopsy.json, results.json, autopsy_data.jsonl (latest), lessons.yaml.

## Process scorecard

**Headline: a near-win and the best percentile in the MMA ledger to date (top 0.24%).** The build correctly identified captain mode (not classic SE), inverted the binary-leverage rule for the large field, cleared the ceiling gate, and genuinely satisfied Anchor-Equivalence. The user's best lineup (L4: Hokit-CPT, Bo, Lopes, Gane, Zahabi, Gaethje) was the winning structure minus one fighter (Ruffy-for-Lopes) and finished rank 14.

| Dimension | Grade | Evidence |
|---|---|---|
| Pre-flight checklist present & honest (analysis) | **B+** | Seven-line block present and substantive. Slate confirmation, projections, and framework checks all verified true by the red team. One overstatement: the "sharp envelope" line claimed "9 distinct captains" without disclosing the L1/L9/L10 5/6-shared spine — the red team caught it; it later cost (see below). |
| Pre-flight checklist present & honest (lineups) | **B+** | Present, detailed, salary-verified by hand. Same diversity overstatement carried through. The `ceiling-gate-underrates-low-own-finishers` lesson was checklisted-as-applied (L7/L8) but those lineups were chalk-heavy, not the cheap sub-25%-own finishers the lesson specifies — a half-application the red team flagged. |
| Open-lessons handling | **A–** | The one open hypothesis (`confirmed-vs-speculative-news`) was correctly identified and defensibly rejected (no injury/weigh-in news on the card — mechanism never triggers). No open lesson silently ignored. |
| Anchor-Equivalence (mandatory) | **A** | Gane(48%)/Pereira(52%) captained on both sides (L5/L6), neither captained elsewhere, both repped across flex. Gane won (152.94), Pereira busted (4.8) — the both-sides presence captured the live side. One-sided-on-Pereira would have killed the portfolio. |
| Red-team verdict adherence | **Split** | L2 FIX (O'Malley-CPT → re-select) **heeded** — re-selected to Daukaus-CPT. L9 FIX (break the shared spine) **ignored**. Portfolio finding #1 (carry a Bo-fade/Daukaus lineup) partially heeded via L2. |
| Portfolio construction | **C+** | The two biggest realized leaks were both correlation, not arithmetic: (1) Topuria in 7/10 with no deliberate fade; (2) the L1/L9/L10 shared spine. Both were saved or punished by the same mechanism the red team named. Cheap-slot homogeneity (Chandler 8/10) also cost. |

**Red-team accuracy in hindsight (ledger-worthy):**

- **L9 FIX — ignored, and the red team was RIGHT.** It wrote: *"If Pereira loses the co-main flip OR Topuria busts, L1/L9/L10 crater together."* Both triggers fired (Pereira 4.8; Topuria lost). The trio finished **58.8% / 50.0% / 76.2%** as a block. The ignored FIX cost real differentiation. → births `mma-se-2026-06-14-showdown-flex-spine-diversity`.
- **Cheap-slot finding (#4) — RIGHT.** Chandler (8/10) scored 1.2; the winning roster and the user's best lineup used Zahabi + Gaethje instead. → births `mma-se-2026-06-14-showdown-cheap-slot-prefer-floor-or-live-dog`.
- **L2 FIX — heeded, but a wash in hindsight.** The red team's objection (O'Malley's capped distance-lean ceiling) was sound, but the applied fix swapped the whole captain to Daukaus, a dog-CPT that needed an upset Bo denied (Daukaus 5.6; L2 finished 47.6%). Neither O'Malley-CPT nor Daukaus-CPT was going to cash — the fix neither helped nor hurt. Weak evidence; not ledgered as accuracy either way.
- **Bo-9/10 finding (#1) — did not bite (GPP guard).** Bo won (184.23), so the flagged correlated risk paid this slate. Not a contradiction of the red team — a 74% favorite converting is the expected case. But the *one* Bo-fade lineup the fix produced (L2 Daukaus) busted, a reminder that hedging a heavy favorite costs when it converts. The realized version of this risk was Topuria, not Bo (see below).

**Scoreboard (best-percentile + process, not ROI):** best percentile **0.2** — the strongest MMA result in the ledger (priors were small-field SE). Edge capture: overperformer-capture 1.0, bust-exposure 1.0 (the build had heavy exposure to both the converters and the busts — Pereira/Chandler — because the flex was uniformly chalk). Lineup avg ratio 1.13.

## Lesson ledger changes

**Confirmations added (existing codified lessons):**
- `mma-se-2026-05-30-anchor-equivalence-fifth-validation` — **6th validation (captain-mode).** Both-sides Gane/Pereira presence captured the live side (Gane won, Pereira busted); one-sided-on-Pereira dies.
- `mma-se-2026-05-30-asymmetric-anchor-equivalence-weighting` — **boundary confirmation.** The asymmetric trigger correctly did NOT fire (Pereira wasn't the chalkiest play on the slate); flat 50/50 was right. Validates the rule's specificity.
- `mma-se-2026-05-16-binary-leverage-weak-in-small-fields` — **large-field inverse confirmed.** Gaethje (19% KO dog) upset Topuria and was in the winning lineup; large field rewarded the binary variance.
- `mma-se-2026-05-16-ceiling-threshold-discipline` — **positive confirmation.** Builds summed to ~620–652 vs a ~600 target; the winner scored 618.43 and L4 hit 615.37. The gate targeted the winning range.

**New hypotheses born (mechanism-based):**
- `mma-se-2026-06-14-showdown-flex-spine-diversity` — distinct captains can mask a shared 5/6 flex spine; cap shared flex at ≤4/6 across any pair. (Red-team-predicted L1/L9/L10 crater realized.)
- `mma-se-2026-06-14-showdown-cap-single-favorite-exposure` — a single non-captain favorite in 7–9/10 is a correlated bet; cap flex share ~≤60% and always carry ≥2 chalk-fade lineups. (Topuria in 7/10 lost; only the 2 Topuria-free lineups cleared 500.)
- `mma-se-2026-06-14-showdown-trust-cpt-own-not-projected-overall-own` — projected overall own (sums ~600) overstates real exposure; DailyFan CPT-own calibrated well (Hokit 16→12.6, Bo 7→6.1, Ruffy 3→4.0, Gane 10→7.8). Make leverage calls off CPT-own.
- `mma-se-2026-06-14-showdown-cheap-slot-prefer-floor-or-live-dog` — the cheap relief slot decides lineups; prefer decision-floor (Zahabi) or the live dog (Gaethje) over pure chalk relief (Chandler 8/10 → 1.2).

**Status changes:** none promoted to `validated` (the four confirmations land on already-`codified` lessons; the four new entries enter as `hypothesis`). `confirmed-vs-speculative-news` stays `hypothesis` (inactive this slate). No retirements — no mechanism contradictions this slate (the chalk-heavy field-fade reservations L7/L8 underperformed, but no cheap finisher won, so that is variance, not a mechanism failure — GPP guard).

## Venue file changes

**N/A — MMA has no venue file by design.** Per CLAUDE.md, the venue-knowledge dirs exist only for NASCAR (tracks), PGA (courses), and MLB (parks); MMA is explicitly excluded ("mma has none" in the Pre-flight ritual and Hard rules). A UFC card is a one-off event, not a recurring location, so a per-event "venue" file would carry no cross-slate reuse and would contradict the documented architecture. Nothing created or appended. The transferable, location-independent reads from this slate live in `lessons.yaml` (above) instead, which is the correct home for them.

## Proposed codifications

**None this slate.** No lesson meets the promotion criterion (3 mechanism confirmations) or the retirement criterion (2 mechanism contradictions):

- `anchor-equivalence-fifth-validation` now carries **2** confirmations (Macau + this slate) — strong and trending, but already `codified` in `rules/shared/anchor_equivalence.md`; no further action needed.
- The four lessons that gained confirmations this slate are all already `codified` — confirmations strengthen the evidence trail but propose no new edit.
- The four new hypotheses each have **1** slate of evidence — they need 2 more mechanism confirmations before a framework.md/philosophy.md codification is proposed. Watch especially `showdown-flex-spine-diversity` and `showdown-cap-single-favorite-exposure`: both were red-team-predicted and realized, so a single further confirmation on a future showdown would make a strong codification case for a "showdown portfolio correlation" section in framework.md.
