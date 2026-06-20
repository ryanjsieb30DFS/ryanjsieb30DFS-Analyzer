# Lineups — MMA · UFC Freedom 250 (White House) · 6/14/26

> **Captain Mode (DK Showdown):** 1 CPT (1.5× salary, 1.5× points) + 5 FLEX, $50K cap. Contest: **UFC Captain $25K Arm Bar — 150-Max, field 5,945, 10 entries.** All 10 lineups below were **SELECTED from the uploaded SaberSim pool**, not built from scratch. Source file: `lineups_dk_ufc_showdown_6-14-2026_800pm.csv` (5,000 rows · sims present). Row indices are 1-based data rows (after the header) for traceability. Sim columns existed but were **not** used as the quality filter — selection is edge-fit first (slate-analysis Player-board calls + edges), ceiling second.

## Pre-flight checklist
- [x] Slate confirmed: mma_se — UFC Freedom 250, 7 fights, captain mode — bundle generated 2026-06-14 18:15; projections + 8 article files all dated 6/14; pool file dated 6-14. Current slate.
- [x] Projections loaded: DailyFan MMA (CPT/Flex) (14 fighters); every pool row resolved via `dk_id_cpt`/`dk_id` (CPT ids 43247050–63, FLEX ids 43247036–49). All 10 selections salary-verified ≤ $50,000 by hand below.
- [x] Venue file read: MMA has no venue file by design (CLAUDE.md) — N/A, UFC card.
- [x] Open lessons reviewed: 1 open hypothesis `confirmed-vs-speculative-news` — **rejected** (no injury/weigh-in news on this card, mechanism never triggers). Codified lessons applied: **asymmetric-anchor-equivalence-weighting** (Gane/Pereira repped both sides, captained both, neither in 8/10 at CPT), **ceiling-gate-underrates-low-own-finishers** (L2 Daukaus dog-captain + L7 Ruffy low-own + L8 Garcia war-stack are the reserved field-fade tier), **binary-leverage-weak-in-small-fields** (INVERTED — 5,945 is large, so low-CPT-own leverage captains are correct; expressed via Daukaus 6% / Ruffy 3% / Garcia 9% dog-and-low-own captains, with O'Malley's low own taken in flex per the analysis), **no-identical-conviction-cores** (no two lineups share a full core; all 10 unique — incl. the two Hokit-CPT builds, which share only Lopes/Zahabi).
- [x] Framework pre-lock checks: Anchor-Equivalence → Gane(48%)/Pereira(52%) captained on **both** sides (L5 Gane-CPT, L6 Pereira-CPT) and neither captained in the other 8; Lopes/Gane/Pereira 47–52 cluster split across the portfolio. No within-lineup same-fight conflict in any of the 10 except the **intentional** Garcia/Lopes (fight 7) war-stack in L8. Ceiling-gate: every lineup sums ~620–652 win-case (≥600 threshold).
- [x] Prior results scanned: autopsies 5/09, 5/16, 5/30 + results.jsonl — all small-field classic SE; transferable read = 5/30 Macau (don't let the ceiling gate zero out cheap low-own finishers → drives L7/L8). No MMA `vendor_calibration.jsonl` yet (0 slates → notes only).
- [x] Sharp envelope: 10 all-unique lineups, **9 distinct captains (Hokit ×2 — L1 + L4, distinct cores)**; captain mix: 2 Hokit chalk (L1/L4), top-ceiling Topuria (L10) + Ruffy (L7), dog-captain leverage Daukaus (L2) + Garcia (L3), co-main Gane (L5) + Pereira (L6), Lopes war-stack (L8), Bo (L9). Low-own leverage captains = Ruffy 3 / Daukaus 6 / Garcia 9; O'Malley's low own kept in **flex** (analysis: flex, not CPT); captain ceiling covered (Topuria 135 / Hokit 128 ×2 / Ruffy 127 / Bo 117); judged on the ~600+ ceiling, not the median.

---

## Lineup 1 — Hokit-CPT chalk-correct core (the "in the building" bullet)
**Thesis:** Captain the slate's best floor+ceiling fighter (Hokit) and surround him with the top scorer (Topuria) and the live co-main, the build most of the 5,945-field winners will share — your must-have-exposure bullet (applies `binary-leverage` correctly: chalk-correct, no manufactured fade).
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 456._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Josh Hokit | $13,500 | 16 / 75 | Anchor — best floor+ceiling on board |
| FLEX | Ilia Topuria | $9,600 | — / 68 | Top scorer (proj 90), flex not CPT |
| FLEX | Diego Lopes | $8,400 | — / 47 | 115+ ceiling |
| FLEX | Alex Pereira | $7,400 | — / 52 | Co-main, Pereira side |
| FLEX | Aiemann Zahabi | $5,800 | — / 30 | Decision-floor salary saver |
| FLEX | Michael Chandler | $5,000 | — / 44 | Cheapest, makes the math work |

Salary: 13,500 + 9,600 + 8,400 + 7,400 + 5,800 + 5,000 = **$49,700** ✓ (win-case ceiling ≈ 646)
**What if?** — *The chalk is simply right and the slate plays to form.* This is the lineup you lose to if you don't have it.

---

## Lineup 2 — Daukaus-CPT dog-captain leverage (edge #1) _(re-selected; fixes the red-team FIX on O'Malley-CPT)_
**Thesis:** The dog-captain edge #1 the analysis names: **Daukaus is the live upset** (SIN picks him to beat Bo; line bled −370→−300) and at **6% CPT own** he's true leverage where it counts. The cheap dog captain frees salary to load the studs (Topuria + Hokit) in flex and keeps **O'Malley's low-own flex leverage** (which the analysis endorses — flex, not captain). If Daukaus pulls the upset, almost no one has him at captain and the studs score underneath.
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 393. Replaces the prior O'Malley-CPT — the analysis explicitly says PASS O'Malley at captain (distance fight, capped ~112 ceiling); his low-own value belongs in flex, where it's kept here._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Kyle Daukaus | $9,300 | 6 / 31 | Dog-captain leverage (SIN pick-to-win, live upset) |
| FLEX | Ilia Topuria | $9,600 | — / 68 | Top scorer |
| FLEX | Sean O'Malley | $9,200 | — / 23 | Low-owned favorite — flex leverage (analysis-endorsed) |
| FLEX | Josh Hokit | $9,000 | — / 75 | Floor+ceiling anchor |
| FLEX | Ciryl Gane | $7,600 | — / 48 | Co-main ceiling |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 9,300 + 9,600 + 9,200 + 9,000 + 7,600 + 5,000 = **$49,700** ✓ (ceiling ≈ 635)
**What if?** — *Daukaus shocks Bo and the studs (Topuria/Hokit) score underneath the cheapest live captain on the board.* Dog-captain leverage (edge #1) — distinct question from every favorite-captain lineup. Matchups: Daukaus(6)/Topuria(1)/O'Malley(3)/Hokit(4)/Gane(2)/Chandler(5) — no two from one fight (Bo, Daukaus's opponent, is correctly off this lineup).

---

## Lineup 3 — Garcia-CPT leverage captain (loaded favorite flex)
**Thesis:** Garcia is the best value captain on the board (win equity well above his 9% CPT own); his cheap captain price ($9.9K) buys a flex of Topuria + Hokit + Bo, so it wins big the moment Garcia upsets Lopes (edge #1).
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 93._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Steve Garcia | $9,900 | 9 / 41 | Leverage captain — cheapest-winner upside |
| FLEX | Ilia Topuria | $9,600 | — / 68 | Top scorer |
| FLEX | Josh Hokit | $9,000 | — / 75 | Floor+ceiling |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Ciryl Gane | $7,600 | — / 48 | Co-main, Gane side |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 9,900 + 9,600 + 9,000 + 8,800 + 7,600 + 5,000 = **$49,900** ✓ (ceiling ≈ 647)
**What if?** — *Garcia wins the closest fight on the card and is the optimal captain priced below the studs.* (SIN: Garcia-in-a-win is optimal more than anyone on the slate.)

---

## Lineup 4 — Hokit-CPT #2, wrestling/HW-ceiling core _(2nd chalk-correct captain, distinct from L1)_
**Thesis:** Second shot at the chalk-correct captain (Hokit — field's #1 captain, highest floor) but built on a **different core than L1**: the grappling/heavyweight ceilings **Bo Nickal + Gane** (instead of L1's Topuria/Lopes/Pereira striker core). It's a different fight-outcome bet — Hokit holds AND the wrestling/HW favorites convert. Replaces the prior Lewis-CPT dog (its bet-against-Hokit conflicts with doubling down on Hokit).
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 896._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Josh Hokit | $13,500 | 16 / 75 | Chalk-correct anchor (2nd build) |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Diego Lopes | $8,400 | — / 47 | 115+ ceiling |
| FLEX | Ciryl Gane | $7,600 | — / 48 | Co-main ceiling |
| FLEX | Aiemann Zahabi | $5,800 | — / 30 | Decision-floor saver |
| FLEX | Justin Gaethje | $5,400 | — / 44 | Salary relief |

Salary: 13,500 + 8,800 + 8,400 + 7,600 + 5,800 + 5,400 = **$49,500** ✓ (ceiling ≈ 706)
**What if?** — *Hokit captains AND the grappling/HW ceilings (Bo, Gane) carry it — the same chalk-correct captain as L1 but a different set of favorites underneath.* Shares only Lopes/Zahabi with L1 (no Topuria/Pereira/Chandler), so it answers a genuinely different question. Matchups: Hokit(4)/Bo(6)/Lopes(7)/Gane(2)/Zahabi(3)/Gaethje(1) — no two from one fight.

---

## Lineup 5 — Gane-CPT co-main winner (Anchor-Equivalence, side A)
**Thesis:** The field over-owns the co-main in flex but *under-captains* it — captaining the winner is the cheapest-winner edge; this takes the Gane side of the pick'em (anchor-equiv presence requirement, side A).
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 113._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Ciryl Gane | $11,400 | 10 / 48 | Co-main winner-CPT (side A) |
| FLEX | Ilia Topuria | $9,600 | — / 68 | Top scorer |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Diego Lopes | $8,400 | — / 47 | 115+ ceiling |
| FLEX | Aiemann Zahabi | $5,800 | — / 30 | Decision-floor saver |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 11,400 + 9,600 + 8,800 + 8,400 + 5,800 + 5,000 = **$49,000** ✓ (ceiling ≈ 630)
**What if?** — *Gane wins the HW title coin flip and the field had him in flex, not at captain.*

---

## Lineup 6 — Pereira-CPT co-main winner (Anchor-Equivalence, side B)
**Thesis:** The Pereira mirror of L5 — same under-captained-co-main edge, opposite side of the coin flip (anchor-equiv presence, side B) — surrounded by a different stud core (O'Malley/Hokit/Bo) so it isn't a clone of L5.
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 17._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Alex Pereira | $11,100 | 12 / 52 | Co-main winner-CPT (side B) |
| FLEX | Sean O'Malley | $9,200 | — / 23 | Lowest-owned favorite |
| FLEX | Josh Hokit | $9,000 | — / 75 | Floor+ceiling |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Steve Garcia | $6,600 | — / 41 | Live dog, leverage |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 11,100 + 9,200 + 9,000 + 8,800 + 6,600 + 5,000 = **$49,700** ✓ (ceiling ≈ 642)
**What if?** — *Pereira wins the title and you captained the right side of the coin flip while the field flex-owned both.*

---

## Lineup 7 — Ruffy-CPT low-own ceiling captain (field-fade tier) _(re-selected to fix captain mis-allocation)_
**Thesis:** Ruffy is the **#3 ceiling on the board (127 CPT pts, ~85% win)** at just **3% CPT own** — an elite low-owned leverage captain. When he wins, his 1.5× separates from the entire field; paired with Bo/Gane ceilings, Garcia leverage, and cheap relief. Carries the lowest cumulative ownership in the portfolio (the field-fade role the 5/30 Macau lesson mandates).
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 648._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Mauricio Ruffy | $15,000 | 3 / 27 | Low-owned ceiling captain (1.5× at 3% CPT own) |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Ciryl Gane | $7,600 | — / 48 | Co-main ceiling |
| FLEX | Steve Garcia | $6,600 | — / 41 | Dog leverage |
| FLEX | Aiemann Zahabi | $5,800 | — / 30 | Decision-floor saver |
| FLEX | Justin Gaethje | $5,400 | — / 44 | Salary relief |

Salary: 15,000 + 8,800 + 7,600 + 6,600 + 5,800 + 5,400 = **$49,200** ✓ (ceiling ≈ 676)
**What if?** — *Ruffy smashes as a 3%-owned captain — the lowest-owned ceiling captain on the board hits.* Matchups: Ruffy(5)/Bo(6)/Gane(2)/Garcia(7)/Zahabi(3)/Gaethje(1) — no two from one fight; lowest cumulative own in the set.

---

## Lineup 8 — Lopes-CPT + Garcia war-stack (the Garcia/Lopes fight-stack, field-fade)
**Thesis:** Reserve one lineup for the slate's closest, both-finishers fight — roster BOTH Garcia and Lopes (the intentional opponent stack) so a back-and-forth war with knockdowns/takedowns both ways pays off no matter who gets the nod (edge #3).
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 598._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Diego Lopes | $12,600 | 11 / 47 | War-stack captain |
| FLEX | Ilia Topuria | $9,600 | — / 68 | Top scorer |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Alex Pereira | $7,400 | — / 52 | Co-main, Pereira side |
| FLEX | Steve Garcia | $6,600 | — / 41 | War-stack partner (fight 7) |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 12,600 + 9,600 + 8,800 + 7,400 + 6,600 + 5,000 = **$50,000** ✓ (ceiling ≈ 648)
**What if?** — *The Garcia/Lopes fight is a knockdown-trading war and both sides post big — the exact miss (Amorim/Vera) the Macau lesson says to never fade.* The only lineup running both sides of a fight (deliberate).

---

## Lineup 9 — Bo-Nickal-CPT wrestling-ceiling captain
**Thesis:** Bo's 100-point wrestling/ground-and-pound ceiling is a captain path the field underrates at 7% CPT own — if he takes Daukaus to the mat for 15 minutes he laps the slate, anchored by Topuria + Hokit underneath.
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 396._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Bo Nickal | $13,200 | 7 / 45 | Wrestling-ceiling captain |
| FLEX | Ilia Topuria | $9,600 | — / 68 | Top scorer |
| FLEX | Josh Hokit | $9,000 | — / 75 | Floor+ceiling |
| FLEX | Alex Pereira | $7,400 | — / 52 | Co-main, Pereira side |
| FLEX | Aiemann Zahabi | $5,800 | — / 30 | Decision-floor saver |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 13,200 + 9,600 + 9,000 + 7,400 + 5,800 + 5,000 = **$50,000** ✓ (ceiling ≈ 644)
**What if?** — *Bo grinds out a dominant wrestling clinic (TD + control + GnP) and posts the slate's top single score from the captain slot.*

---

## Lineup 10 — Topuria-CPT top-scorer captain (the missing ceiling play) _(re-selected to fix captain mis-allocation)_
**Thesis:** The slate's **#1 projected scorer (135 CPT pts)** captained at only **9% CPT own** — the field flexes Topuria at 68% but won't captain him. When he finishes Gaethje in the main event his 1.5× is the **highest score on the board** and uncontested at the captain slot; Bo/Lopes/Pereira ceilings underneath.
_Selected from `lineups_dk_ufc_showdown_6-14-2026_800pm.csv`, row 270._

| Slot | Fighter | Salary | Own% (CPT/overall) | Role |
|---|---|---|---|---|
| CPT | Ilia Topuria | $14,400 | 9 / 68 | Top-scorer captain — highest ceiling (1.5× = ~135) |
| FLEX | Bo Nickal | $8,800 | — / 45 | Wrestling ceiling |
| FLEX | Diego Lopes | $8,400 | — / 47 | 115+ ceiling |
| FLEX | Alex Pereira | $7,400 | — / 52 | Co-main ceiling |
| FLEX | Aiemann Zahabi | $5,800 | — / 30 | Decision-floor saver |
| FLEX | Michael Chandler | $5,000 | — / 44 | Salary relief |

Salary: 14,400 + 8,800 + 8,400 + 7,400 + 5,800 + 5,000 = **$49,800** ✓ (ceiling ≈ 695)
**What if?** — *The top scorer is the optimal captain — Topuria runs through the main event and almost no one captained him.* Matchups: Topuria(1)/Bo(6)/Lopes(7)/Pereira(2)/Zahabi(3)/Chandler(5) — no two from one fight; highest ceiling in the set.

---

## Portfolio audit

**Count & uniqueness:** 10 lineups, all unique rosters, **9 distinct captains — Hokit captained twice (L1 + L4) with deliberately different cores** (L1 = Topuria/Lopes/Pereira striker core; L4 = Bo/Gane wrestling-HW core), so the two share only Lopes/Zahabi and answer different questions — not a clone. All selected from the single uploaded SaberSim pool (L1–L10 rows: 456, 393, 93, 896, 113, 17, 648, 598, 396, 270), deduped — no two identical.

**Captain leverage (where the slate's leverage lives):**
| Captain | Lineups | CPT own% | Tier |
|---|---|---|---|
| Hokit | L1, L4 | 16 | chalk-correct anchor (×2, distinct cores) |
| Daukaus | L2 | 6 | dog-captain leverage (SIN pick-to-win) |
| Garcia | L3 | 9 | dog leverage |
| Gane | L5 | 10 | co-main winner (equiv A) |
| Pereira | L6 | 12 | co-main winner (equiv B) |
| Ruffy | L7 | 3 | low-own ceiling captain |
| Lopes | L8 | 11 | war-stack |
| Bo Nickal | L9 | 7 | wrestling ceiling |
| Topuria | L10 | 9 | top-scorer ceiling captain |

8 of 10 captain slots are sub-12% CPT own; the low-own leverage captains are Ruffy (3), Daukaus (6), Garcia (9). **Captain ceiling + leverage both covered** — top ceilings Topuria (135, L10) and Ruffy (127, L7); dog-captain leverage via Daukaus (L2, edge #1) and Garcia (L3); two highest-floor in Hokit ×2 (L1/L4). **Hokit captained twice** is intentional chalk-correct conviction (16% CPT, best floor) with two distinct cores — capped at 2 to avoid over-indexing the field's favorite captain. O'Malley's low-own value is kept in **flex** (L2/L6), per the analysis ("flex, not CPT").

**Anchor-Equivalence compliance:** the mandatory Gane(48%)/Pereira(52%) co-main pair is captained on **both** sides — **L5 Gane-CPT** and **L6 Pereira-CPT** — and neither is captained in the other 8 lineups (presence + both-sides + not-one-sided all satisfied). Across flex, Gane appears in L2/L3/L4/L7 and Pereira in L1/L8/L9/L10, so both sides are repped throughout. The Lopes/Gane/Pereira 47–52 cluster is split, not concentrated.

**Hedges & player overlap:**
- **Co-main hedge:** Gane captained (L5) vs Pereira captained (L6) — you hold whichever wins the title coin flip.
- **Garcia/Lopes fight (the leverage fight):** Garcia-CPT upset in L3 (no Lopes); Lopes-CPT war-stack with Garcia in L8 (both sides); Garcia also flexes in L7; Lopes as ceiling flex in L1/L8/L10. The fight is expressed from every angle.
- **Hokit/Lewis fight (4):** Hokit captained **twice** (L1 + L4, distinct cores) and flexed (L2/L3/L6/L9) as the chalk anchor; Lewis is no longer rostered — the bet-against-Hokit was dropped to double down on the chalk-correct captain.
- **No unintended same-fight conflicts:** every lineup uses 6 distinct fights **except L8**, whose Garcia+Lopes double is the intentional, analysis-endorsed war-stack.
- Topuria (flex in 8) and Hokit (cap/flex in 6) are the portfolio's load-bearing favorites — appropriate for MMA, where favorites convert and the differentiation is in the captain slot, not in fading the studs.

**Slate-analysis edges expressed:**
1. *Dog-captain leverage* (edge #1) → **L2 (Daukaus, SIN pick-to-win)**, L3 (Garcia). *High-ceiling leverage captains* → L7 (Ruffy 3% CPT), L10 (Topuria 9% CPT) — the slate's top two captain ceilings. *Chalk-correct captain conviction* → L1 + L4 (Hokit ×2, distinct cores).
2. *Hokit-CPT chalk-correct core* (edge #2) → L1 + L4 (Hokit ×2, distinct cores).
3. *Garcia + Lopes fight-stack* (edge #3) → L8 (both sides), supported by L3.
4. *Co-main winner-CPT, fight under-captained* (edge #4) → L5 (Gane), L6 (Pereira).
5. *Ruffy / O'Malley low-own favorites* (edge #5) → **Ruffy CPT-leverage in L7 (3% CPT)**; **O'Malley as FLEX leverage in L2 + L6** (analysis-endorsed — flex, not captain).

**Field-fade secondary tier (5/30 Macau lesson):** L7 (Ruffy-CPT, lowest cumulative own in the set) and L8 (Garcia war-stack) are the reserved cheap-low-own-finisher lineups — the ceiling gate did not zero them out.

**Ceiling check:** every lineup's summed win-case projection lands ≈ 620–652, clearing the ~600+ tournament target for this field.
