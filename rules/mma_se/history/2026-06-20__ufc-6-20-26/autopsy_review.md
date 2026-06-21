# Post-Autopsy Review — UFC Fight Night 6/20/2026 (Classic 6-fighter)

_Archive: `rules/mma_se/history/2026-06-20__ufc-6-20-26`. Reviewed: slate_analysis.md, lineups.md (selected-from-pool), red_team.md, autopsy.json, accuracy.json, shark_gap.json, results.json. GPP guard applied throughout: a lost contest / bad ROI is never evidence — only mechanism confirmations and failures count._

## Process scorecard

**Result (reference only, not graded):** best 553.52 → rank 799/47,562 = **1.7%ile** (mini-MAX); $8K Flying Knee 494.96 = 16.1%ile (784); $5K Clinch 449.54 = 31.8%ile (1,189). 2 of 24 graded lineups in the top 10%; avg points/proj ratio 1.05. ROI tracked in the user's third-party app (null here by design).

| Check | Grade | Notes |
|---|---|---|
| Pre-flight checklist present (analysis) | ✅ | 7-line block, all items addressed; slate correctly confirmed as CLASSIC 6-fighter (not showdown), dates matched. |
| Pre-flight checklist present (lineups) | ✅ | 7-line block present and specific. |
| Checklist HONESTY | ⚠️ | Two false-as-written claims the red team caught: (a) "Horiguchi/Kape faded across all 10 = extreme of run the alternative" **mislabels Anchor-Equivalence** — the rule requires running the alternative in ≥1; 0/10 satisfies neither side. (b) "Salary ≤$50,000 each (verified)" was **false for L7** (Amil listed $7,500, actual $7,800; true total $49,800). Checkmarks outran the verification. |
| Open lessons applied | ⚠️→✅ | Most applied correctly (Rodriguez cap 6/10 + 4 Rodriguez-free hedges; debut-trio rotation; punts confined to mini-MAX; SE no-pure-punts). Two misapplications, both **caught by red team and fixed pre-lock**: the main-event Anchor-Equivalence violation, and `cheap-slot-prefer-floor-or-live-dog` applied as the live-DOG half (Shahbazyan, no floor) in the SE where the analysis's Decision 4 wanted the decision-FLOOR half (Horiguchi). |
| Anchor-Equivalence (main event) | ❌ build / ✅ recovered | The built portfolio ran NEITHER main-event side in 10/10 — a literal rule breach. The red team flagged it as the dominant finding; the user **restored the main event before lock** (actual entries: Horiguchi ~22.7%, Kape in the SEs + several mini-MAX). The recovery, not the build, is what got entered. |
| Red-team verdict adherence | ✅ | 0 KILL / 4 FIX / 6 SHIP. The actual entered lineups differ materially from lineups.md — Horiguchi restored to both SE cheap slots, Kape/Santos reintroduced to mini-MAX — i.e. the FIXes (L1 Shahbazyan→Horiguchi; portfolio finding #1 restore-the-main-event) were **heeded**. |

**Verdict accuracy in hindsight (red-team grading):**
- **FIX on L1 (restore Horiguchi to the SE cheap slot) — RIGHT, and heeded.** Shahbazyan (the no-floor +310 dog the build used instead) scored **0.0**. The restored-Horiguchi SE entries cleared their fields (16.1% / 31.8%). A heeded FIX that removed a 0-point hole. ✅
- **Portfolio finding #1 (the 0/10 main-event fade is the dominant shared failure mode; restore to ~6) — heeded, and the restoration produced the user's BEST lineup** (553.52, 1.7%ile, which carried Kape). The *severity framing* was partly overstated, though: the 47,562-field WINNER (606.69) **also** faded the main event entirely, so fading it was not fatal in itself — the breach was the *anchor-equivalence* rule (zero exposure to either side), not "the slate punished the fade." Net: directionally correct and correctly heeded.
- **Finding #2 (Oliveira 60% is "unearned chalk concentration" — trim to 3-4) — WRONG in hindsight.** Oliveira was a slate-defining overperformer (122.51, +44.05 vs proj) and was in BOTH the field winner and the user's best lineup. Trimming him would have weakened the portfolio's two best builds. → Evidence against over-trusting the red-team "trim secondary chalk" heuristic; births a new hypothesis (below). The user correctly did **not** act on this one.
- **FIX on L7 (salary line wrong) — RIGHT, mechanical.** A real unverified-claim catch; non-fatal but exactly the class of error the audit exists for.

**What the slate proved/disproved (mechanism only):**
- Reserved field-fade / punt-leverage builds **worked**: Bolanos (71.86) and Borjas (50.84) were the two slate-defining plays; Borjas (sub-12% own) anchored both the field winner and the user's best lineup. Confines-punts-to-the-big-field discipline validated in both directions.
- The narrative fades (Santos "best opponent faced"; Stirling "weight under, distance-prone") cut against the pieces that actually won — both were in the field winner. **Variance, not a contradiction** (the pick'em could resolve either way; the boom/bust debut boomed), but a real signal about fade *quality* → new hypothesis.
- Lima was the build's biggest realized cost (24.83, −59.37; carried in three build lineups) — a chalk-tier domination favorite that simply lost. Bust exposure was unavoidable given broad coverage; not a process miss.

## Lesson ledger changes

Edited `rules/mma_se/lessons.yaml`:

**Confirmations added (codified lessons — strengthen, no status change):**
- `mma-se-2026-05-30-ceiling-gate-underrates-low-own-finishers` — +confirmation: the reserved field-fade builds carried the two slate-defining punts (Bolanos/Borjas); Borjas was in the field winner and the user's best lineup. The rule produced the winning structure.
- `mma-se-2026-05-16-binary-leverage-weak-in-small-fields` — +confirmation (both directions in one slate): SEs correctly used value-favorite floors (no pure punts) and cleared their fields; the big-field mini-MAX correctly housed the binary punts, which hit.

**Status promotions hypothesis → validated (mechanism confirmation now exists):**
- `mma-se-2026-06-14-showdown-cap-single-favorite-exposure` → **validated**, +confirmation with a **boundary correction**: Rodriguez cap (6/10 + 4 hedges) confirmed; but the rule's "always fade the main-event chalk" was over-pushed to 0/10 exposure, breaching Anchor-Equivalence. Refinement logged: *cap the favorite; do not zero it.* (1 confirmation — not yet at the 3-confirmation promotion bar.)
- `mma-se-2026-06-14-showdown-cheap-slot-prefer-floor-or-live-dog` → **validated**, +confirmation: format split validated — live-finishing-dog half won the big field (Borjas/Bolanos), decision-floor half was the right SE fill (red team restored Horiguchi over the no-floor Shahbazyan, who scored 0.0). (1 confirmation.)

**New hypotheses born (mechanism-based):**
- `mma-se-2026-06-20-fade-on-structure-not-narrative` — distinguish structural fades (measurable edge) from narrative fades (soft scouting read); only fade a live, real-ceiling chalk piece when the fade has a structural mechanism. Born from Santos/Stirling (narrative fades, both in the winner) vs Kape (structural fade, neutral-correct).
- `mma-se-2026-06-20-finish-capable-favorite-is-not-secondary-chalk` — exempt a finish-capable favorite in a clean matchup from the "trim the secondary chalk" instinct; high exposure to such a piece is legitimate. Born from the wrong-in-hindsight red-team Oliveira-trim finding.

## Venue file changes

**None — by design.** MMA has no venue files (`CLAUDE.md`: tracks/courses/parks exist for NASCAR/PGA/MLB only; "mma has none"). The slate_analysis and red_team both correctly recorded "Venue file: N/A." Nothing to create or stub.

## Proposed codifications

**None this slate.** No lesson reached the 3-mechanism-confirmation promotion bar that is not already codified, and there are no retirement candidates (zero mechanism contradictions — only variance outcomes, which the GPP guard excludes).

- `cap-single-favorite-exposure` and `cheap-slot-prefer-floor-or-live-dog` advanced **hypothesis → validated** this slate (1 confirmation each); each needs 2 more mechanism confirmations before a codification proposal.
- The two codified lessons that gained confirmations (`ceiling-gate-underrates-low-own-finishers`, `binary-leverage-weak-in-small-fields`) are already in framework.md — no edit proposed.
- Watch-item for a future codification proposal (no edit yet): if `cap-single-favorite-exposure` reaches promotion, the codified text must carry the **boundary** surfaced here — "cap the chalkiest favorite at ~≤60% AND carry ≥2 fades, but never drive either side of an Anchor-Equivalent pair to 0% exposure; zeroing a side is an Anchor-Equivalence breach, not extra leverage."
