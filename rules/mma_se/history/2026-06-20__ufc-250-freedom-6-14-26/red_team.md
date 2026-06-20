# Red Team — MMA · UFC Freedom 250 (White House) · 6/14/26

> Adversarial pre-lock review of the 10-lineup portfolio in `data/lineups/mma_se.md`. Contest: **UFC Captain $25K Arm Bar — 150-Max, field 5,945, 10 entries.** Captain mode ($50K, CPT 1.5×). Findings only — the red team never rewrites lineups. The user decides what to act on.
>
> **What I verified before attacking** (so the attacks rest on facts, not vibes): every CPT-own% number in the build (O'Malley 2, Ruffy 3, Bo 7, Garcia/Topuria 9, Gane 10, Lopes 11, Pereira 12, Hokit 16) is **real DailyFan vendor data** — confirmed against `ownership_cpt` in `data/sessions/mma_se.json`, not invented. All 10 salaries re-summed by hand: every lineup is ≤ $50,000 and uses the correct 1.5× CPT salary. No illegal same-fight stacks anywhere except L8 (intentional, declared). The leverage math is honest. The portfolio's weaknesses are **structural concentration**, not bad arithmetic.

## Verdict summary

| Lineup | Verdict | One-line reason |
|---|---|---|
| L1 — Hokit-CPT chalk core | **SHIP** | The mandatory "in the building" bullet; chalk-correct, no manufactured fade. |
| L2 — O'Malley-CPT leverage | **FIX** | Captains the one fighter the analysis said PASS-at-CPT; O'Malley's distance-lean caps his CPT ceiling at ~132 (lowest of any captain in the set) on the chalkiest flex base — swap Gaethje for real flex ceiling. |
| L3 — Garcia-CPT leverage | **SHIP** | Genuine 9%-CPT cheapest-winner leverage on a loaded flex; distinct question. |
| L4 — Hokit-CPT #2 (wrestling core) | **SHIP** | Distinct from L1 (Bo/Gane core vs Topuria/Pereira); highest ceiling in the set. |
| L5 — Gane-CPT (equiv A) | **SHIP** | Satisfies the mandatory anchor-equivalence; winner-CPT edge is real. |
| L6 — Pereira-CPT (equiv B) | **SHIP** | The opposite side of the co-main flip on a different core; not a clone of L5. |
| L7 — Ruffy-CPT low-own ceiling | **SHIP** | Best leverage captain on the board (3% CPT, 85% win, 127 ceiling); lowest cumulative own. |
| L8 — Lopes-CPT + Garcia war-stack | **SHIP** | The one intentional, analysis-endorsed opponent stack; field-fade role. |
| L9 — Bo-CPT wrestling ceiling | **FIX** | Bo is already in 9/10 lineups; L9 rides the same 5-fighter spine (Topuria+Pereira+Zahabi+Chandler) as L1 and L10 — differentiate ≥2 flex slots or it's a third captain-hat on one roster. |
| L10 — Topuria-CPT top scorer | **SHIP** | Highest-ceiling captain at 9% CPT; the Topuria-at-captain question is additive despite spine overlap. |

**8 SHIP / 2 FIX / 0 KILL.** No lineup is structurally broken (all clear salary, ceiling, and stack rules). The fixes are about leverage quality (L2) and field-duplication (L9), and the portfolio-level findings below matter more than either single FIX.

---

## Lineup attacks

### L1 — Hokit-CPT chalk-correct core — **SHIP**
**For it to win, all of these must be true:** Hokit beats Lewis (76%) AND posts a captain-worthy score; Topuria beats Gaethje (81%); the chalk slate holds to form.
**Steelman:** Correctly the must-have bullet. Hokit is the board's best floor+ceiling (proj 85, win-case 106, stddev 25.5), captained at only 16% despite being the field's #1 captain — not an over-pay relative to the field. The flex is the field's consensus chalk, which is the *point*: this is the lineup you lose to if you don't have it.
**Attack:** The only real objection is field-duplication — this exact "Hokit-CPT + Topuria + chalk" shape will be among the most common builds in 5,945 entries, so it wins you a share of a crowded pot, not the top. That is the accepted cost of the chalk-correct bullet, not a flaw. **Leverage audit:** none claimed; correctly framed as chalk. **Shared failure:** Pereira (52%, coin-flip co-main) is here and in L6/L8/L9/L10 — a Gane win dents five lineups (see portfolio findings). Survives.

### L2 — O'Malley-CPT forgotten-favorite — **FIX**
**For it to win:** O'Malley beats Zahabi (77%) **and finishes early enough to post 100+**, AND almost no one captained him (true at 2% CPT), AND the chalk base (Hokit/Bo/Gane) also smashes.
**Steelman:** 2% CPT own on a 77% favorite is the single best leverage-by-ownership captain on the board. If O'Malley wins and you're one of a handful who captained him, you separate.
**Break it:** The slate analysis explicitly says **PASS O'Malley at captain** (Decision #1; Player board: "flex leverage, not CPT") because his is **the fight most likely to go the distance** — and the data backs it: O'Malley's win-case projection is **88.16, the lowest of any favorite**, so his 1.5× CPT ceiling is **~132 — the lowest CPT ceiling of any captain in the entire portfolio** (vs Hokit 159 / Topuria 158 / Pereira 156 / Ruffy 150 / Bo 148). Leverage does *not* fix a capped ceiling: a 2%-owned captain topping out at 132 separates *less* than a 9%-owned Topuria topping at 158. Worse, that capped captain sits on **the chalkiest flex in the portfolio** — Hokit 75 / Bo 45 / Gane 48 / Gaethje 44 / Chandler 44 (cumulative ~256). So if O'Malley wins by decision (~88) and the chalk holds, the lineup just *ties the field* — the leverage never cashes because the ceiling isn't there. The build overruled the analysis's PASS without answering the reason the analysis gave.
**Leverage audit:** 2% CPT is genuinely contrarian — that part is honest. The problem is the *expression*, not the number.
**Shared failure:** Gane (coin flip) here + L3/L5/L7 — a Pereira win dents four.
**The ONE change:** keep O'Malley-CPT if you want the 2% bullet, but swap a chalk-dog flex (**Gaethje 44%**, ~20 in a loss, pure salary chalk) for a higher-ceiling piece so the lineup's ceiling doesn't rest entirely on the one capped-ceiling captain in the set.

### L3 — Garcia-CPT leverage captain — **SHIP**
**For it to win:** Garcia upsets Lopes (41%) AND the saved-CPT-salary loaded flex (Topuria/Hokit/Bo) hits.
**Steelman + attack:** The cleanest leverage lineup in the set. Garcia at $9.9K CPT / 9% CPT own is the analysis's #1 edge ("when Garcia wins he's optimal more than anyone on the slate"), and the cheap captain genuinely buys Topuria+Hokit+Bo underneath — a real, not cosmetic, structural advantage. The flex isn't a punt; it's three premiums. The bet (Garcia wins the closest fight on the card, line moved toward him all week) is live at 41%. **Leverage audit:** 9% CPT is real leverage; the flex is chalk but that's the trade for the dog captain. **Shared failure:** Bo + Gane + Chandler shared with the spine; a Bo loss hurts. Survives — best risk-adjusted leverage build.

### L4 — Hokit-CPT #2, wrestling/HW core — **SHIP**
**For it to win:** Hokit holds AND the grappling/HW favorites (Bo, Gane) convert.
**Attack:** The obvious objection is "two Hokit captains." But L4 shares only **Hokit + Lopes + Zahabi** with L1 (the audit's "only Lopes/Zahabi" undersells it — Hokit is shared too, but it's the captain in both, which is the deliberate point) — the Topuria/Pereira/Chandler striker core is gone, replaced by Bo/Gane/Gaethje. It genuinely answers "Hokit + the wrestlers" vs L1's "Hokit + the strikers," and posts the set's top ceiling (~706). Capping Hokit captains at 2 is the right call. **Shared failure:** Bo loss (it's captain-support here) hurts, plus the Gane coin flip. Survives.

### L5 — Gane-CPT co-main winner (equiv A) — **SHIP**
**For it to win:** Gane wins the HW title flip (50%) AND the field, who flexed the co-main, didn't captain it.
**Attack:** A literal coin flip, so a 50% bet by construction — but that's *why* it's required (anchor-equivalence presence, side A) and why captaining the under-captained winner is +EV when the field over-owns the fight in flex (48/52%). The flex (Topuria/Bo/Lopes) is sound. **Leverage audit:** 10% CPT on a coin-flip favorite is legitimately under-captured. **Shared failure:** dies with L2/L3/L7 if Pereira wins instead. Survives — mandatory and well-built.

### L6 — Pereira-CPT co-main winner (equiv B) — **SHIP**
**For it to win:** Pereira wins the flip (50%) AND the differentiated stud core (O'Malley/Hokit/Bo) hits.
**Attack:** Correctly NOT a clone of L5 — opposite captain, and the flex swaps in O'Malley (23%, lowest-owned favorite) + Garcia for L5's Topuria/Lopes/Zahabi. This is where the Pereira side belongs. **Leverage audit:** 12% CPT; O'Malley at 23% in flex adds genuine low-own equity. **Shared failure:** part of the Pereira-side cluster (L1/L8/L9/L10) — a Gane win hits five lineups. Survives.

### L7 — Ruffy-CPT low-own ceiling — **SHIP**
**For it to win:** Ruffy beats Chandler (85%, usually by KO — sniper profile) AND the field didn't captain him (true at 3% CPT).
**Steelman + attack:** The portfolio's best pure-leverage swing, and correct for a 5,945 field (binary-leverage-is-weak inverts in large fields). Ruffy at 3% CPT / 127 ceiling / 85% win is an elite low-owned captain. The honest objection: the flex fades **both** top scorers (no Topuria, no Hokit) and carries three non-favorites (Gane coin-flip, Garcia 41% dog, Gaethje 19% big dog) — so it needs Ruffy + Bo + Gane(win) + Garcia(upset) to all hit. That's a lot, but it's the *intended* deep-leverage bullet and the lowest cumulative own in the set; the ceiling is real if Ruffy snipes. **Leverage audit:** genuinely the lowest-owned captain. Survives.

### L8 — Lopes-CPT + Garcia war-stack — **SHIP**
**For it to win:** The Garcia/Lopes fight (closest on the card, both finishers) is a back-and-forth war so both post big regardless of the decision.
**Attack:** The only intentional opponent stack, explicitly endorsed by the analysis (edge #3) and the 5/30 Macau lesson (don't fade the live cheap-finisher fight). Running both sides of one fight burns ~one slot of equity by construction, but that's the declared bet and it's reserved to exactly 1 of 10. The Topuria/Bo/Pereira flex backs it. **Leverage audit:** 11% CPT Lopes is fine; the stack itself is the differentiation. Survives — correctly the field-fade war lineup.

### L9 — Bo-Nickal-CPT wrestling ceiling — **FIX**
**For it to win:** Bo dominates Daukaus on the mat (74%) from the captain slot AND Topuria + Hokit hit.
**Steelman:** Bo's 100-pt wrestling ceiling captained at 7% is a legitimately under-owned path.
**Break it:** Two problems compound. (1) **Bo is already in 9 of 10 lineups** — captaining him in a 10th adds almost no new exposure; you're tripling down on a fighter the build already saturates. (2) **L9's roster is a near-clone of L1 and L10**: all three carry the **Topuria + Pereira + Zahabi + Chandler** spine. L9 vs L10 differ by exactly one flex (Hokit vs Lopes) plus the captain hat (Bo vs Topuria); L9 vs L1 differ by one flex (Bo vs Lopes) plus the hat. So three of your "9 distinct captains" sit on one essentially-identical roster — a single bet wearing three hats. If Pereira loses the co-main flip OR Topuria busts, L1/L9/L10 crater **together**. **Leverage audit:** 7% CPT Bo is fine in isolation; the issue is portfolio redundancy, not the number.
**The ONE change:** break L9 off the shared spine — swap **≥2 of {Pereira, Zahabi, Chandler}** for pieces not already in L1/L10 (note: you cannot add Daukaus here — he's Bo's opponent). If it can't be meaningfully differentiated, this is the lineup to drop, because Bo-CPT is the least-additive captain in a set where Bo is everywhere.

### L10 — Topuria-CPT top scorer — **SHIP**
**For it to win:** Topuria finishes Gaethje in the main (81%) AND the field, which flexes him at 68% but won't captain him (9% CPT), gets left behind.
**Attack:** Shares 5/6 with L1 (Topuria, Lopes, Pereira, Zahabi, Chandler) — flagged at portfolio level — but unlike L9, the Topuria-at-captain question is genuinely high-value and distinct: it's the board's #1 ceiling (135 at 1.5×) at the captain slot the whole field declines. The captain choice *is* the differentiation, and it's the best one available. Keep it; fix the redundancy at L9 instead. Survives.

---

## Portfolio-level findings

**1. (Biggest hole) Bo Nickal in 9/10 with ZERO Daukaus hedge — and the build ignored its own read.** Bo is rostered in every lineup except L1 (captain in L9, flex in L2/L3/L4/L5/L6/L7/L8/L10). DailyFan gives Daukaus a 26% win shot, and the slate analysis's **own "Where I disagree with the vendors"** section says: *"I shade toward Daukaus being live — SIN explicitly picks him to win… line bled from -370 to -300."* Daukaus is also the un-run alternative in the bundle's Daukaus/Zahabi/Ruffy (27–31%) equivalence trio. Yet the portfolio carries **0% Daukaus**. If Bo loses — a documented ~1-in-4, and the build's own stated lean — 9 of 10 lineups lose their captain or a core flex simultaneously. This is the portfolio's single largest correlated risk and it directly contradicts the build's own analysis. At minimum one lineup should run Daukaus (it can't coexist with Bo, so it would be a Bo-fade build — which the portfolio entirely lacks).

**2. L1 / L9 / L10 are a 5/6-shared cluster — "9 distinct captains" overstates real diversity.** All three carry the **Topuria + Pereira + Zahabi + Chandler** spine; they differ only by one flex and the captain hat. They sink or swim on the same five fighters. A Pereira loss (50% co-main flip) or a Topuria bust takes all three down together. The audit's "no two share a full core" is technically true but hides that three lineups share *five-sixths* of a core. (See L9 FIX.)

**3. Leverage lives only in the captain slot; the flex is uniformly chalk — the Macau field-fade lesson is half-applied.** The lowest-owned fighter rostered anywhere in flex is O'Malley (23%). The genuine cheap upside dogs the analysis identified — **Daukaus (31%, SIN pick-to-win) and Lewis (25%, KO dog)** — are at **0%**. The only dog the build actually uses is **Zahabi (the safe decision-floor one)**, not an upside finisher. The 5/30 Macau lesson (`ceiling-gate-underrates-low-own-finishers`) says reserve ≥1 lineup for *cheap, sub-25%-own fighters with a live finishing path the projections under-rate* — but the build's "field-fade tier" (L7/L8) is actually full of chalk (Bo 45 / Gane 48 / Topuria 68 / Lopes 47). The lesson is cited in the checklist but not really expressed: the cheap-finisher *upside* (Amorim/Vera analogue = Daukaus/Lewis) is missing, replaced by a floor dog. *Mitigant:* MMA showdown offers no sub-5%-owned fighter at all (cheapest is O'Malley 23%), so the sharp "sub-5% piece in most lineups" is format-limited — but the live upside dogs the build itself flagged could still have been carried.

**4. Field-duplication on the cheap slots: Chandler 8/10, Zahabi 6/10.** Chandler (44%) and Gaethje (44%) are exactly the salary-relief chalk the analysis warns "the whole field uses to make lineups work." Leaning on Chandler in 8 lineups means your cheap slots match the field's cheap slots — reducing uniqueness in a 5,945 pool precisely where differentiation is cheapest to find (a $5K dog swap).

**5. Anchor-Equivalence (the mandatory check): PASS — genuinely satisfied.** Gane (48%) and Pereira (52%) are captained on both sides (L5 Gane, L6 Pereira), neither is captained in the other eight, and both are repped across the flex. The Lopes/Gane/Pereira 47–52 cluster is split, not concentrated. No manufactured objection here — this was done correctly.

**6. Open lessons.yaml:** the one open `hypothesis` (`confirmed-vs-speculative-news`) was correctly identified and defensibly rejected (no injury/weigh-in news on this card). No open lesson was silently ignored — but the *codified* `ceiling-gate-underrates-low-own-finishers` is checklisted-as-applied while only half-applied (finding #3).

---

## Pre-flight audit (line by line, skeptically)

- **"Slate confirmed … bundle generated 2026-06-14 … all dated 6/14"** — ✅ **Verified.** Bundle timestamp, projections (14 fighters = 7 fights), and pool file all 6/14. Current slate, not stale.
- **"Projections loaded … every pool row resolved via dk_id_cpt/dk_id … CPT own% O'Malley 2 / Ruffy 3 / Hokit 16 …"** — ✅ **Verified, and credit due.** These CPT-own numbers are **real DailyFan `ownership_cpt` values** in the session data, not invented — I checked every one. The leverage claims throughout the build rest on genuine vendor data. Salaries all re-summed: every lineup ≤ $50K with correct 1.5× CPT salaries.
- **"Venue file read: MMA has no venue file by design — N/A"** — ✅ **Correct.** CLAUDE.md confirms MMA has no track/course/park file. Not a rubber-stamp.
- **"Open lessons reviewed: 1 open hypothesis — rejected"** — ✅ on the hypothesis (only `confirmed-vs-speculative-news` is open; rejection is defensible). ⚠️ **Partial rubber-stamp** on the cited codified lessons: `ceiling-gate-underrates-low-own-finishers` is claimed applied via L7/L8, but L7/L8 are chalk-heavy, not the cheap sub-25%-own finishers the lesson specifies (finding #3). And `asymmetric-anchor-equivalence-weighting` is cited while the relevant live-dog hedge (Daukaus) sits at 0% (finding #1).
- **"Framework pre-lock checks: Anchor-Equivalence → Gane/Pereira both sides …"** — ✅ **Verified true** (finding #5). "Ceiling-gate: every lineup ~620–652 win-case" — plausible and consistent with the per-fighter win-case projections; not independently re-summed line-by-line.
- **"Prior results scanned … 5/30 Macau lesson drives L7/L8"** — ⚠️ Scanned, yes, but the Macau lesson is cited more than it's followed (finding #3). The transferable read (don't let the ceiling gate zero out cheap low-own finishers) was named, but the actual cheap upside finishers were zeroed out anyway.
- **"Sharp envelope: 10 unique, 9 distinct captains; sub-6% CPT-own O'Malley 2 / Ruffy 3; captain ceiling covered"** — ⚠️ **Oversells.** "9 distinct captains" is technically true but masks the L1/L9/L10 5/6-shared spine (finding #2). "Leverage in the captain slot" is real, but only **2 of 10** lineups (L2, L7) carry a sub-6% piece — "≥1 sub-5% piece in most lineups" is **not** met in substance (mitigated by format: no sub-5% fighters exist on this 14-man card). The reframe away from the 12–16%-own/slot target *is* correct for MMA showdown — that part is honest, not a rubber-stamp.

**Bottom line:** The arithmetic, salaries, ownership data, and the mandatory Anchor-Equivalence check are all clean and honestly sourced — no fabrication. The portfolio's real exposure is **correlation, not construction errors**: Bo in 9/10 with zero Daukaus (your own flagged live dog), a 5/6-shared L1/L9/L10 cluster, and leverage confined to the captain slot while the flex matches the field. Acting on the two FIXes (L2 ceiling, L9 redundancy) plus carrying one Bo-fade/Daukaus lineup would address every finding above.
