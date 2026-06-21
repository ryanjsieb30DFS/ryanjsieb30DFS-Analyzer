# Red Team — MMA UFC Fight Night 6/20/2026 (Classic, 10-lineup pool selection)

_Adversarial pre-lock review. I tried to kill each lineup against the slate analysis, framework, lessons.yaml, anchor-equivalence rule, and the raw pool. All 10 cited pool rows were decoded by `dk_id` and **every roster matches its cited row** — traceability is clean (one salary-label error on L7, below). No vendor_calibration weight applies (only DailyFan, 1 slate, MAE n/a — note not weight). Ownership numbers below are SIN/The Stone (what the build used)._

## Verdict summary

| Lineup | Verdict | One-line reason |
|---|---|---|
| L1 — SE bullet ($8K Flying Knee, 784) | **FIX** | No sub-20% leverage piece (everything ≥20%) AND drops the Horiguchi floor the analysis prescribed for the SE cheap slot; chalk-leaning in a field the framework puts in the "needs differentiation" band. |
| L2 — SE bullet ($5K Clinch, 1,189) | **FIX** | Anchors the *differentiated* SE on Stirling — the analysis's explicitly weakest/distance-prone debut — giving it the lowest-but-one sim ceiling (99th 586 < the 600 SE threshold for a 1,189 field). |
| L3 — mini-MAX | **SHIP** | Highest sim ceiling in the pool (634.7); coherent Lima+Chokheli double-finish + Rodriguez leverage + Mullins sub-10% punt. |
| L4 — mini-MAX | **SHIP** | Bolanos punt-leverage thesis is the analysis's named best punt; ceiling clears 600 (616.8). (Note: two PASS-rated fillers.) |
| L5 — mini-MAX | **SHIP** | "Owns every PLAY call" smash; Mesquita+Magomedov double-stud, real Bolanos punt, unique core. |
| L6 — mini-MAX | **SHIP** | Double-R1 ceiling + Borjas punt + Rodriguez-free hedge — a genuine portfolio role, ceiling 604.6. |
| L7 — mini-MAX | **FIX** | Salary line is **wrong** (Amil $7,800 not $7,500; real total $49,800, not the stated $49,500) and it stacks Nascimento (PASS) + a one-off Amil-dart for the lowest-tier ceiling (586.7). |
| L8 — mini-MAX | **FIX** | Stacks four analysis-discounted pieces (Stirling weight-under + Nascimento PASS + Santos fade-lean + Mullins punt) → 2nd-lowest ceiling (582.7) and violates Edge 2 (Rosa-over-Santos). |
| L9 — mini-MAX | **SHIP** | The analysis's leverage-dog ceiling build executed cleanly — Lima/Rodriguez + double sub-20 dog (Baghdasaryan 18 / Shahbazyan 20), no pure punt, ceiling 602.8. |
| L10 — mini-MAX | **SHIP** | The reserved field-fade build (no premium debut, no top stud); lowest ceiling is inherent to the fade-all-debuts angle, which Edge 3/4 sanctions as ≥1 build. |

**Net: 0 KILL / 4 FIX / 6 SHIP.** No lineup is fatally broken; the FIXes are real structural/role mismatches, not manufactured.

---

## Lineup attacks

### L1 — SE BULLET (Mesquita / Oliveira / Rodriguez / Santos / Raposo / Shahbazyan) → FIX
**What must ALL be true to win:** Mesquita delivers her ~115 win-case; Rodriguez beats Amil; Santos wins the coin flip; Raposo upsets (+142); Shahbazyan upsets (+310); and this clears a 784-entry SE without a differentiator.
**Steelman:** It's the chalk-correct safe-floor bullet — Mesquita is the safest ceiling on the card, and Santos+Raposo are real value-favorite floors per the framework's SE cheap-slot rule. Salary verified ($49,300).
**Refute:**
- **Leverage audit fails.** Lowest ownership on the roster is **20%** (Shahbazyan 20, Raposo 20, Rodriguez 21). The framework's codified `secondary-plays-are-not-leverage` is explicit: "a 20%+-owned play is not leverage, it is secondary chalk; true SE leverage is sub-15% (ideally sub-12%)." **L1 has zero sub-20% pieces** — the build's own checklist admits it "sits at the 20% line." For a 784 field (the framework's 500–1,500 "needs genuine differentiation" band, not the <500 "can be chalk-leaning" band), an all-≥20% lineup can't separate.
- **It dropped the prescribed floor.** Analysis Decision 1+4 named Horiguchi the SE cheap-slot value-favorite floor *first*; L1 fades him (the 47%-owned grappling-floor favorite who already beat Kape) and instead carries Shahbazyan, a +310 binary dog with no floor — the opposite of what the SE win-condition wants.
**Shared failure mode:** Shares the all-portfolio main-event fade (below) and the Rodriguez-loss mode (6/10).
**FIX (one change):** Swap Shahbazyan ($7.1K, +310 dog, no floor, no leverage value at 20%) → **Horiguchi ($7.6K)**, +$500 to $49,800. That restores the SE's prescribed value-favorite floor, is chalk-correct for a small SE, and simultaneously dents the portfolio's 0% Horiguchi problem.

### L2 — SE BULLET (Stirling / Oliveira / Rodriguez / Rosa / Raposo / Baghdasaryan) → FIX
**What must ALL be true:** Stirling — a debut with the "toughest matchup" who has shown he'll go the distance — posts a finish ceiling; Rodriguez and Rosa (coin flip) both convert; Baghdasaryan (+285) spikes; and it wins a 1,189-entry SE.
**Steelman:** Per `se-bullet-is-the-differentiated-build`, the SE bullet should be the *differentiated* build when the chalk anchor is boom/bust — and Stirling is the least-defaulted of the debut trio, so anchoring him is on-thesis. It carries a genuine sub-20% piece (Baghdasaryan 18) and zero sub-$7.2K punts.
**Refute:**
- **Ceiling is structurally short for its field.** SaberSim 99th-percentile = **586** — the lowest of any SE-eligible build except L8/L10. Framework Pre-Submission item 7 sets the 1,189-field SE threshold at **>600**. L2 is "built to cash, not to win" — the exact 5/16/26 failure the ceiling-threshold lesson exists to prevent.
- **The differentiation comes from the wrong axis.** The analysis says weight Stirling **under** ("weakest of the three," "boom/bust, will go distance"). `se-bullet-is-the-differentiated-build` wants the *highest-conviction* differentiated build — L2 instead puts the single must-win SE bullet on the **lowest-conviction, lowest-ceiling** debut. Differentiation bought at the cost of both conviction and ceiling.
**Shared failure mode:** Carries Rodriguez (6/10) AND Rosa (6/10) — needs a favorite *and* a coin flip simultaneously, the same double-dependency as L5/L10.
**FIX (one change):** Anchor on **Magomedov** (37%, R1-finish ceiling) instead of Stirling. It still differs from L1's Mesquita anchor (so the two SEs stay non-twinned), lifts the win-case ceiling above the 600 line, and trades distance-risk for finish equity. Stirling stays repped in L8, so the debut-trio rotation survives.

### L3 — (Lima / Chokheli / Oliveira / Rodriguez / Cutelaba / Mullins) → SHIP
**Win condition:** Both elite finishers (Lima domination + Chokheli R1) hit, and a sub-10% piece (Mullins) frees the salary.
**Attack & survival:** Highest sim ceiling in the pool (99th **634.7**), the only build that clears the framework's most aggressive thresholds. Genuine leverage (Mullins 10%). The one blemish is **Cutelaba** — a PASS-rated "rising-own trap" the analysis likes "least" — but it's confined to a mini-MAX dart exactly as the player board permits ("if played anyway: mini-MAX dart only"). The Lima+Chokheli double-debut is high variance, but that's the stated thesis and the field can't all build it. **SHIP.**

### L4 — (Chokheli / Oliveira / Nascimento / Rosa / Tanzilovi / Bolanos) → SHIP
**Win condition:** Bolanos lands the +330 KO vs hittable Aswell, freeing salary for the Chokheli/Rosa core.
**Attack & survival:** This is the analysis's Edge 5 expressed correctly — Bolanos is the named best punt with a live striking path, and he's in a mini-MAX, not an SE. Ceiling clears 600 (616.8). **Caveat (not fatal):** it carries **two** PASS-rated pieces (Nascimento + Tanzilovi) as salary geometry, which caps the non-Bolanos ceiling — but the thesis is the punt freeing studs, and a coverage lineup is allowed one such shape. **SHIP** (watch the PASS fillers as a portfolio pattern, below).

### L5 — (Mesquita / Magomedov / Rodriguez / Rosa / Raposo / Bolanos) → SHIP
**Win condition:** Both top-tier finishers smash AND both 20–21% leverage favorites convert.
**Attack & survival:** Coherent "own every PLAY call" build, unique core, real punt (Bolanos 13%). Its risk is needing Rodriguez (favorite) and Rosa (coin flip) to both hit — but that IS the thesis, and at the mini-MAX scale that concentration is the point. Ceiling 599.9 (right at the line, acceptable for mini-MAX). **SHIP.**

### L6 — (Mesquita / Magomedov / Oliveira / Rosa / Cutelaba / Borjas) → SHIP
**Win condition:** A finish-heavy slate where Mesquita+Magomedov+Oliveira form a triple-finisher front and a sub-12% punt (Borjas) separates — without needing Rodriguez.
**Attack & survival:** The **Rodriguez-free hedge** is a genuine, deliberate portfolio role (4 lineups fade Rodriguez — good adherence to `cap-single-favorite-exposure`). Ceiling 604.6, real leverage (Borjas 11%). Cutelaba again PASS-rated but mini-MAX-confined. **SHIP.**

### L7 — (Aswell / Magomedov / Nascimento / Rosa / Amil / Borjas) → FIX
**Win condition:** Amil's pace produces a volume ceiling on the side opposite Rodriguez, Magomedov is the live debut, and Borjas punt hits.
**Steelman:** A legitimate distinct angle — the only build that plays the Amil side of the Rodriguez/Amil fight, betting volume over the favorite. Anchor-equivalence-flavored coverage of that fight.
**Refute:**
- **Factual error — the salary line is wrong.** The roster table lists **Amil at $7,500** and totals **$49,500**. Amil's real salary is **$7,800** (session/pool), so the true total is **$49,800**. Still legal, but the checklist's "Salary ≤$50,000 each (verified below)" is **false as written for L7** — the kind of unverified claim this review exists to catch.
- **Lowest-tier ceiling.** 99th = **586.7**. The analysis endorsed Amil only as "a one-off mini-MAX dart" and rates Nascimento a **PASS** ("low-volume, struggle to crush in a win, salary-inefficient"). Stacking the dart + the PASS-glue + a punt (Borjas) is three ceiling-suppressing pieces in one lineup.
**FIX (one change):** Correct the salary line to $49,800, and to earn the slot's ceiling, swap **Nascimento ($8.8K PASS glue) → Collins ($8.5K, finish-dependent favorite)** (frees $300, lifts the finish ceiling, keeps the Amil-pivot thesis intact).

### L8 — (Lima / Stirling / Nascimento / Santos / Fili / Mullins) → FIX
**Win condition:** The two most expensive anchors (Lima + Stirling) both dominate while the field is over on cheaper debuts.
**Steelman:** A real spine-diversifier — Rodriguez-free AND Rosa-free, the only build whose mid-tier is fully distinct, and one of two Santos lineups (legit coverage of the Rosa/Santos pick'em's other side).
**Refute:**
- **Four analysis-discounted pieces in one roster:** Stirling (weight **under** — used here as a *primary* anchor), Nascimento (**PASS**), Santos (**fade-lean** — the analysis says "I go further, fade-lean," and Edge 2 is explicitly Rosa-over-Santos), and Mullins (pure punt). That's two-thirds of the lineup built on pieces the analysis told you to discount.
- **Ceiling 582.7** — 2nd-lowest in the pool, and the thesis ("two most expensive anchors dominate") leans on the *least-trusted* expensive anchor (Stirling).
**FIX (one change):** Swap **Santos ($7.9K, fade-lean) → Horiguchi ($7.6K)** (−$300 to $49,200). Removes the documented fade, adds a decision floor, keeps the Lima/Stirling spine distinct, and contributes to fixing the portfolio's 0% Horiguchi.

### L9 — (Lima / Oliveira / Collins / Rodriguez / Baghdasaryan / Shahbazyan) → SHIP
**Win condition:** Both sub-20% dogs (Baghdasaryan 18 + Shahbazyan 20) spike alongside a Lima/Rodriguez core.
**Attack & survival:** This is Edge-aligned leverage executed honestly — a double sub-20 dog swing, no pure punt, ceiling 602.8. The dogs are genuinely the lower-owned tier (not chalk in costume). Highest-variance of the SHIPs, but that's the explicit contrarian-tail thesis and it's only 1 of 10. **SHIP.**

### L10 — (Aswell / Nascimento / Rodriguez / Rosa / Fili / Shahbazyan) → SHIP
**Win condition:** The debut-heavy chalk all busts and a debut-free leverage build is the last structure standing.
**Attack & survival:** This is the reserved **field-fade build** (Edge 3/4 sanction ≥1). Its lowest-in-pool ceiling (577.6) is the *inherent cost* of fading every high-ceiling debut — you can't both fade the ceiling tier and have the highest ceiling. As the single such build it's defensible. The Nascimento PASS-glue is the weak point, but the angle justifies it. **SHIP** (note it's the floor of the portfolio's ceiling distribution — acceptable for exactly one lineup).

---

## Portfolio-level findings

1. **The main event is faded 0/10 — this contradicts the analysis's own Decision 1 and is the dominant shared failure mode.** Decision 1 calls Horiguchi a **PLAY** ("the value-favorite floor / cheap-slot fix for SE," **cap ≤~6/10** — i.e. roster him in ~6). The build rosters him **0/10** and Kape 0/10. "Cap ≤6" means *up to* 6, not zero; the checklist's reframe ("faded entirely = extreme of run the alternative") is not what the cap or the Anchor-Equivalence rule says. The literal anchor-equivalence requirement ("≥1 lineup MUST run the alternative anchor") is **unmet** — no lineup runs Horiguchi *or* Kape. Worse, Horiguchi (47% chalk, already beat Kape, grappling **decision floor**) is the chalk *least* likely to bust, so this is maximum leverage aimed at the most reliable favorite on the card. Every one of the 10 lineups needs the 89%-field-exposure main event to bust or go flat — one game-state (Horiguchi simply wins/floors) damages the **entire** portfolio at once. Edge 3 scoped this as **≥1** mini-MAX build, not 10/10. **Restore Horiguchi to the two SE bullets + ~3 mini-MAX (the analysis's ~6/10), keep ~3-4 as the deliberate ME-fade.**

2. **Oliveira 6/10 (60%) is unearned chalk concentration.** The analysis rates him MIX and says outright "25% own is secondary, not leverage." He's carried at the *same* 60% exposure as the two deliberate leverage edges (Rodriguez, Rosa) with none of the leverage benefit. If Oliveira (-285) loses, six lineups eat it for nothing, and the Rodriguez+Oliveira mid-spine (together in L1/L2/L3/L9) is exactly the "smart-money" core a sharp 47k field converges on. **Trim Oliveira to ~3-4.**

3. **Rosa 6/10 = 60% of the portfolio on a literal coin flip (-108 pick'em).** Correct *side* (Rosa over Santos), wrong *dose*: ~half the time Rosa loses and 6/10 are crippled simultaneously. L2/L5/L10 stack Rosa **and** Rodriguez, needing a coin flip and a favorite together. For a portfolio judged on ceiling this concentration is the single biggest variance driver — consider ~4-5.

4. **Nascimento (PASS) at 40% anchors the bottom of the portfolio.** Analysis PASS: "salary-inefficient, low-volume, struggle to crush in a win." He's the $8.8K glue in L4/L7/L8/L10 — and **the three lowest-ceiling lineups (L8 582, L7 587, L10 578) all carry him.** The analysis said better mid-tier options exist; the build leaned on the piece it told itself to avoid.

5. **"Leverage" is over-labeled.** Rodriguez (21%) and Rosa (20%) are repeatedly called "leverage favorites," but both fail the framework's codified `secondary-plays-are-not-leverage` line ("20%+ is secondary chalk; true leverage is sub-15%"). Genuinely sub-15% leverage (the punts Mullins/Borjas/Bolanos) appears in only **6/10**; L1 has nothing under 20%. This is largely a **slate constraint** (the analysis is honest that the leverage floor is ~10%), so it's not fully fixable — but the portfolio should not be read as leverage-rich, and L1 is the one lineup where it's a correctable miss.

6. **Open-lessons adherence is mixed.** `cap-single-favorite-exposure` is well applied to Rodriguez (held at 6, four Rodriguez-free builds) ✓. But the same lesson's "fade the chalkiest favorite in ≥2 lineups" is over-applied to 10/10 on the main event (finding 1), and `cheap-slot-prefer-floor-or-live-dog` is applied as the *live-dog* half (Shahbazyan/Baghdasaryan) in the SE slots when Decision 4 explicitly wanted the *decision-floor* half there. `flex-spine-diversity` analog (all-unique cores, max overlap 3) is satisfied ✓.

7. **Field-duplication risk:** the Rodriguez+Oliveira mid-spine (4 lineups) and the Rodriguez/Rosa pairing are the obvious sharp-field cores; across a 47,562 field these don't separate. The genuine separators (Mullins/Borjas/Bolanos punts, the double-dog L9) are where the differentiation actually lives — lean into those, not the mid-chalk spine.

---

## Pre-flight audit (line by line, skeptical)

- **"Slate confirmed"** — ✅ **TRUE.** Bundle generated 2026-06-20, analysis same date, contest fields match (784 / 1,189 / 47,562). This is the correct classic 6-fighter slate.
- **"Projections loaded (SIN The Stone + DailyFan)"** — ⚠️ **TRUE but single-sourced for ownership.** All leverage/own calls use SIN numbers only. DailyFan ownerships differ materially and were never reconciled: Stirling **35→25**, Horiguchi **47→42**, Fili **17→22**, Cutelaba **17→21**, Oliveira **25→28**. With DailyFan calibration <3 slates this is a permissible default, but Rodriguez-21/Rosa-20 "leverage" rests entirely on one vendor's unverified ownership — if DailyFan is closer, several "leverage" labels weaken further.
- **"Venue file N/A"** — ✅ **TRUE.** MMA has no venue files per CLAUDE.md; nothing to read or stub. Not a rubber stamp.
- **"Open lessons applied"** — ⚠️ **PARTIAL.** Rodriguez cap ✓. But (a) Horiguchi "faded entirely" is mislabeled as honoring the ≤6 cap (the cap means roster ~6, not 0), and (b) the cheap-slot lesson is applied as "live dog," not the "decision floor" the analysis's Decision 4 specified for SE. See findings 1 & 6.
- **"Framework pre-lock: Anchor-Equivalence / salary ≤$50K"** — ⚠️ **TWO inaccuracies.** (a) "Horiguchi/Kape faded across all 10 (extreme of run the alternative)" does **not** satisfy the rule, which requires running the alternative in ≥1 — zero lineups run either side. Debut-trio and Mesquita/Lima rotations ARE correctly done ✓. (b) "Salary ≤$50,000 each (verified below)" is **false for L7**: Amil is listed $7,500 but is $7,800; true total $49,800, not the stated $49,500 (still legal, but unverified). The other 9 salary totals check out against the pool rows.
- **"Prior results scanned"** — ✅ **TRUE.** results.jsonl = 1 slate (6/14 Freedom), correctly treated as process-note-only.
- **"Sharp envelope"** — ✅ **MOSTLY ACCURATE / HONEST.** "9/10 carry a sub-20% piece" verified true (only L1 lacks one). own/slot ~23.3 verified. The app's computed ⚠️ (own/slot vs 14–19 target, 0% sub-5%) is the *generic* shark envelope; per the analysis's MMA-specific calibration (~28–30% norm, no sub-5% play exists — lowest available own is Mullins 10%), 23.3% is genuinely *more* contrarian than both the MMA norm and the user's historical 29.9%, and 0% sub-5% is a true slate constraint, not a build failure. This line is not a rubber stamp.

**Bottom line:** The build is well-constructed mechanically (all-unique, traceable, salary-legal, debut rotation correct, Rodriguez cap honored) and 6 of 10 survive attack. The recurring theme in the 4 FIXes and the portfolio findings is the **same over-correction**: the analysis's "fade/cap/leverage" guidance was pushed to extremes — Horiguchi 0/10 (vs ≤6), a 10/10 main-event fade (vs ≥1), the differentiated SE on the weakest anchor — while three analysis-PASS/fade pieces (Nascimento 40%, Santos, Oliveira 60%) quietly carry the bottom of the portfolio. The single highest-value action is **restoring Horiguchi to ~6 lineups** (fixes L1, L8, the anchor-equivalence violation, and the dominant shared failure mode at once).
