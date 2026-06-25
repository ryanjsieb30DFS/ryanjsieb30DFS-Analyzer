# Red Team — PGA Classic: U.S. Open at Shinnecock Hills (R1 Thu 6/18/2026)

_Adversarial pre-lock review of the **current** 6-lineup portfolio in `data/lineups/pga_classic.md` ($20K Mulligan + $10K Eagle, both 5-Max 3/5). This supersedes the prior red-team pass, which attacked an earlier version (Suber in L1, Herbert in L2) that the build has since re-selected out (rows 1567 / 4037). Ownership/make-cut numbers are pulled from the ETR slate analysis + bundle, not the lineup file's restatements. Vendor note: ETR has **1 calibrated slate** (own MAE 0.94) — every ownership number here is an uncalibrated single-vendor projection, a note not a weight. Findings only — the red team never rewrites lineups._

## Verdict summary

| Lineup | Verdict | One-line reason |
|---|---|---|
| L1 — Scottie + Fleetwood + all-skill value tier | **FIX** | Scottie ($14.9K) behind FOUR sub-5% cut-coinflips is the exact structure the analysis's Decision #1 forbids; swap one for Kitayama (also closes the 0/6 value-engine gap). |
| L2 — Fitz-over-Si-Woo + mid-band | **SHIP** | Clean Anchor-Equivalence value build; 13.8 own sits on the codified ~13% winning envelope. |
| L3 — Bryson + Brooks two-champ chaos | **SHIP** | Roster is sound (sub-20 combined leverage pair + Fitz floor); thesis must be re-grounded — see attack. |
| L4 — Rahm + Xander + cheap-skill spine | **SHIP** | Anchor-Equiv alt with genuine 1.3% Conners leverage; triple mid-chalk is a mild correlation, not fatal. |
| L5 — Mid-owned band, Scottie floor | **SHIP** | Direct autopsy-gap fix; Scottie-floor build, 1 sub-5 is correct here. |
| L6 — Si Woo engine + elite irons | **SHIP** | Chalk-leaning coverage slot; Si Woo capped/standalone, Morikawa leverage taken. |

**Net: 1 FIX, 5 SHIP** — but two portfolio findings (Kitayama/English 0/6, and total tee-time/draw blindness on a wind-defense major) deserve a documented pre-lock response even on the SHIP'd lineups (`act-on-redteam-portfolio-findings-on-ship`).

---

## Lineup attacks

### L1 — Scottie + Fleetwood, all-skill-floored value tier — **FIX**

**What must ALL be true:** (1) Scottie ($14.9K) posts a ceiling despite being the analysis's own course-fit dock #4 / majors dock #5 at the most edge-neutralizing setup of the year; (2) Fleetwood pays; (3) **all four** of Woodland / Mitchell / Noren / Hall survive a 36-hole U.S. Open cut **and** 2–3 of them spike.

**Steelman:** two genuine cut-locks up top + four accurate, penal-fit ball-strikers (all ≥55% MC, none amateurs); 10.1 avg own; perfect $50,000.

**Break it:** The slate analysis's Decision #1 says verbatim that a $14.9K Scottie "forces the rest of the roster into the $5–6K cut-risk swamp" and to **"pair him with proven-floor $6–7K names (Kitayama, English, McNealy), NOT $5K darts."** L1 does the opposite — Scottie sits behind **four** $6.2–6.6K darts at 55/55/56/61% make-cut, four near-coin-flips on the binary that zeroes the whole roster. On a penal cut course the live failure mode isn't scoring variance, it's 2–3 of those four missing the weekend and gutting the lineup behind two anchors. This is the most cut-exposed build in the set and it contradicts the very analysis it claims to express.

**Leverage audit:** the four sub-5% pieces (3.0 / 4.1 / 4.9 / 1.4) are honestly contrarian — no chalk in a costume. But they're cheap value/skill *floors*, not conviction leverage; L1's differentiation rests entirely on the cut surviving, while the top (Scottie 24.3 + Fleetwood 22.9) is the most-built two-anchor field core on the slate.

**Shared failure mode:** Scottie merely makes the cut without spiking → kills L1 **and** L5 (the only two Scottie builds; they also share Mitchell — the portfolio's 2/6 overlap).

**THE ONE FIX:** replace **Gary Woodland ($6,600 / 3.0% / 55% MC)** with **Kurt Kitayama ($6,500 / 12.4% / +16.2 coffin / 61% MC)** — salary −$100 (→ $49,900, valid). This (a) drops L1 from four to three sub-5% cut-coinflips, (b) installs the proven $6–7K floor Decision #1 demands, (c) adds the single biggest mid-owned value multiplier on the board, and (d) single-handedly closes the Kitayama-0/6 portfolio gap (Finding P1). Nudges L1 toward the ~13% winning envelope without breaking the sub-5 requirement (Mitchell/Noren/Hall remain).

### L2 — Fitz over Si Woo, NO Scottie, mid-band — **SHIP**

**What must ALL be true:** Fitz (the lower-owned half of the value-chalk coin) outscores Si Woo; Rory pays; Gotterup (16.0) + Spaun (11.2) carry; Cauley survives and spikes.

**Steelman + attack:** textbook expression of Edge #4 (Fitz-over-Si-Woo) and Edge #2 (own the value band); Anchor-Equivalence satisfied (Fitz without Si Woo); 13.8 avg own is dead on the codified ~13% winning structure; the re-selection correctly removed the sub-50%-MC Herbert dart. The only nit is Gotterup flagged "rising own" — but it's a multiplier, not an anchor. No legal single-roster change improves it. **SHIP.**

**Shared failure mode:** mid-owned band busts → also dents L5 and L6 (shared Hovland/Spaun thesis); offset by L1/L3/L4 on the darts/champs side.

### L3 — Bryson + Brooks (two USO champs), Fitz floor — **SHIP (re-ground the thesis)**

**What must ALL be true:** Bryson (6.1%) and/or Brooks (7.2%) detonate; Fitz floors it; Straka + Hojgaard survive the cut.

**Steelman:** Bryson + Brooks = **13.3% combined own** — a legitimate sub-20% leverage pair (passes `leverage-spine-needs-sub20-combined-own`); Bryson is the mandated Anchor-Equivalence alternative to the top cluster; Fitz keeps it from going all-coin-flips (`contrarian-needs-leverage-anchor`). Deepest-leverage no-Scottie build at 8.8 own. No roster change needed.

**Break the framing (not the roster):** the thesis sells two mechanisms the build's own logic rejects:
1. **"Brooks won Shinnecock '18 / detonate at a venue built for their profiles"** is a *course-history narrative* — and the slate analysis is explicit that **Shinnecock stickiness = 0.06 → course history is NOISE**, the exact basis on which it PASSes Cam Smith / Uihlein / Rodgers. Brooks is a fine 7.2% major-pedigree skill dart (63% MC, majors boost); just don't ground him on the 2018 trophy the build elsewhere calls noise.
2. **Fitz is labeled "leverage-grade floor" at 25.1% own** — the second-highest-owned player on the slate. That's the brief's "15%-owned leverage play is chalk wearing a costume," doubled. Fitz is a *chalk floor* doing its job; the label is wrong, the play isn't.

Neither is a legal roster change, so per the SHIP definition this is **SHIP** — but re-ground the thesis (Brooks on skill/majors-form; Fitz as a chalk floor) before entry, or it can't be honestly process-graded later.

### L4 — Rahm + Xander, cheap skill-leverage spine — **SHIP**

**What must ALL be true:** Rahm (16.7%, LIV-suppressed) and Xander (19.8%) clear ~70+; Conners (1.3%) and Noren (4.9%) deliver; Henley/Spieth fill.

**Attack + survival:** three mid-chalk anchors (Rahm 16.7 + Xander 19.8 + Henley 16.9 ≈ 53% across three) is a correlation cluster — if the expensive accuracy chalk underperforms together, only Conners/Noren/Spieth carry. But avg own is 10.9 with a genuine 1.3% leverage piece, the bottom is well-differentiated, and Conners is the cleanest skill-floored sub-5% on the board (elite accuracy = exact penal fit; Edge #3). One lineup carrying this concentration across a 6-build set is acceptable diversification. **SHIP.**

### L5 — Mid-owned ceiling band, Scottie floor — **SHIP**

**What must ALL be true:** the 9–12% band (Hovland, McNealy, Adam Scott) smashes while Scottie floors it; Mitchell survives.

**Attack + survival:** the direct cure for the last-two-autopsies gap (zero mid-owned-multiplier exposure). Only one sub-5% piece (Mitchell 4.1) — correct for a $14.9K-anchored build; you don't stack cut-risk behind the Scottie tax. Real concern is overlap, not construction: L5 shares **Scottie + Mitchell** with L1 (the max 2/6 overlap), so a flat-Scottie + Mitchell-cut-miss world dents both at once. Two of six is inside tolerance (4/6 are no-Scottie). **SHIP.**

### L6 — Si Woo engine + Morikawa/Rory, deep dart — **SHIP**

**What must ALL be true:** Si Woo's price is right and value-chalk pays; Morikawa's irons fit the approach test; Poston survives.

**Attack + survival:** chalkiest build (14.2 own) — and rightly the chalk-leaning coverage slot. Si Woo correctly capped 1/6 and standalone (not with Burns/Cantlay — honoring the writer flag and `leverage-spine-needs-sub20-combined-own`). Morikawa at 11.6% is the coffin-fade-I-take leverage, defensible. One nit: **Poston is 54% MC**, just under the ≥55% gate the checklist claims for "every sub-5% piece" — but Poston is the explicit form/value-engine profile (`ch-scan-needs-skill-gate`, the Memorial lesson) and survives on form, not pedigree. Not a fix. **SHIP.**

---

## Portfolio-level findings

**P1 — Kitayama AND English are 0/6 (strongest finding).** Edge #2 names **Kitayama ($6.5K/+16.2 coffin), English ($6.7K/+6.4), Spaun, McNealy, Morikawa** to make "near-permanent… design these exposures FIRST." Actual: Spaun 2/6, Morikawa 1/6, McNealy 1/6, **Kitayama 0/6, English 0/6** — the two highest-coffin value engines, the literal headliners of the autopsy-proven win condition, are zeroed and replaced by sub-5% skill darts. This is the **exact** RBC failure the build claims to be curing (zero Fox/Yellamaraju → ~70 points short, per `mid-owned-value-spine-over-darts`). The L1 FIX (Woodland→Kitayama) closes half; English should also get a home (e.g. L5 or L1's remaining dart slot). The checklist's `design-exposures-before-lineups` claim is therefore **overstated** — the spine was named, not guaranteed.

**P2 — Total tee-time / draw blindness on a wind-defense coastal major.** Shinnecock's stated defense is **wind**; the bundle ships full AM/PM wave data (the 7:52 wave avg 49.9 proj / 15.4 own vs the 14:42 wave 11.7 / 0.02). Not one of the six lineups references which side of the Thursday draw its golfers sit on. If one wave gets wind-hammered (a recurring U.S. Open outcome over R1/R2), every lineup loaded into that wave craters together — an **un-analyzed shared failure mode across the whole portfolio.** Caveat: a 2-day-plus-cut Classic spreads draw risk over R1+R2, so this is a documented note, not necessarily a re-build — but "we never looked at the draw" on a wind-defense links setup is a portfolio blind spot.

**P3 — Internal stickiness contradiction.** The checklist cites the venue file as "read"; the venue file assumes **above-average** stickiness (0.42 analog). The analysis instead uses **0.06 = noise** and builds its whole "reject course history" stance on it. The build sides with 0.06 (defensible — the article beats the UNVERIFIED stub) — then **L3 smuggles course history back in** ("Brooks won here 2018"). Pick a lane. Reconcile the 0.42-assumption-vs-0.06-actual gap in the venue file post-slate.

**P4 — Anchor-Equivalence: two of three bundle clusters explicitly checked, third only de-facto.** Top cluster (19.5–24.3) → Bryson alternative in L3 ✅, 4/6 no-Scottie ✅. Si Woo/Fitz pair (25.1–29.6) → Fitz without Si Woo (L2/L3) ✅. **Third bundle cluster (Burns/Henley/Rahm/Gotterup/Cantlay, 15.8–19.2)** is never named in the doc — de-facto satisfied (Henley + Rahm in L4, Gotterup in L2), so no violation, but the checklist should name it.

**P5 — Mid-band concentration vs chaos (acceptable, logged).** The portfolio splits 3-3: value-band thesis (L2/L5/L6, all leaning Hovland/Spaun-type multipliers) vs darts/champs (L1/L3/L4). Healthy coverage — but the value-band three share Hovland (L5, L6) and Spaun (L2, L6), so a mid-band whiff dents 2–3 lineups at once. Counterbalanced by L3's deep darts and L4's cheap-skill spine. No action.

**P6 — Field-duplication on L1 (and L6).** Scottie + Fleetwood (24.3 + 22.9) is among the most obvious two-anchor cores the field will build; L1's uniqueness rests entirely on its four cheap pieces. L6 (Si Woo + Rory chalk, 14.2 own) is the second. Two of six is acceptable because L3/L4/L5 diversify hard — the P1/L1 fix (adding 12.4%-owned Kitayama) marginally helps L1.

**Open-lessons check:** `single-vendor-overweight-self-erosion` ✅ (Rai 0/6, the exact RBC bust honored); `never-zero-value-chalk-anchor` ✅ (Scottie 2/6, Rory 2/6, Fitz 2/6); `leverage-spine-needs-sub20-combined-own` ✅ (no chalk pair labeled/run as a spine; Si Woo isolated); `contrarian-needs-leverage-anchor` ✅ (L3 floored by Fitz); `mid-owned-value-spine-over-darts` / `design-exposures-before-lineups` — **only partially executed** (P1: Kitayama/English 0/6); `se-leverage-cap-two` — N/A to 5-Max but L1's four sub-5% pieces are the spiritual cousin of that capped failure mode (addressed by the FIX); `act-on-redteam-portfolio-findings-on-ship` — **this review IS that trigger**; the 5 SHIPs do not absolve P1/P2.

---

## Pre-flight audit (line by line, skeptical)

- **"Slate confirmed: U.S. Open, Shinnecock, pool 6-18 6:35am"** — ✅ verified. Pool date, $14.9K Scheffler / 156-man field, contest config (Mulligan 2,941 / Eagle 2,378, both 5-Max 3/5) all match the bundle. Not stale.
- **"Projections loaded: ETR (156), resolved by dk_id"** — ✅ plausible; cited own%/ceiling/salary match the analysis rows. Standing caveat: ETR is uncalibrated (1 slate), so every leverage call rests on a single-vendor ownership projection — a note, not a weight.
- **"Venue file read: shinnecock_hills.md (UNVERIFIED stub)"** — ⚠️ **half rubber-stamp.** File exists and IS marked UNVERIFIED (honest on that), but the checklist's characterization is selective: the file assumes **above-average** stickiness, contradicting the build's 0.06-noise basis, and the conflict isn't surfaced. The penal-prior is also applied selectively to justify the Bryson anchor while the file's own "accuracy gates distance, a bomber who sprays loses fast" argues mildly the other way. See P3.
- **"Open lessons applied (each named)"** — ⚠️ **mostly honest, overstated on two.** Major lessons genuinely executed, but `design-exposures-before-lineups` and `mid-owned-value-spine-over-darts` are claimed while the two headline value engines (Kitayama, English) are 0/6 (P1). The spine was named, not guaranteed.
- **"Framework pre-lock checks / Anchor-Equivalence"** — ✅ on the top cluster and the Si Woo/Fitz pair; ⚠️ third bundle cluster unaddressed in text (P4). **Inaccuracy:** the audit states overlap "L1∩L5 = Scottie+Mitchell; others ≤1" — **false: L2∩L6 = Rory+Spaun = 2.** The 2/6-max claim still holds; the enumeration is wrong. All salaries ≤ $50K verified (L1 = exactly $50,000).
- **"Prior results scanned"** — ✅ honest. RBC best 5.0%, Memorial 3.5% match results.jsonl; sample <10 = process only, correctly stated.
- **"Sharp envelope: ≥1 sub-5% in 6/6; avg own 8.8–14.2; all sub-5 ≥55% MC"** — sub-5-in-6/6 ✅ verified (L1=4, L2=1, L3=2, L4=2, L5=1, L6=1); avg-own range ✅ recomputed (L3=8.83, L6=14.23). **Two false sub-claims:** (1) the checklist's "L1/L3/L4 carry 2" undercounts **L1, which carries 4** (the portfolio-audit section even contradicts it, correctly saying 4); (2) "all ≥55% make-cut" is false — **Poston is 54% MC** (L6). Both minor, neither flips a verdict — but exactly the unchecked self-report the audit exists to catch.

**Bottom line:** the checklist is honest work, not a rubber stamp — but it overstates the value-spine application (the real P1 miss), mischaracterizes the venue-file stickiness, and carries two small factual errors. Fix L1 (Woodland→Kitayama), find a home for English, document a draw-exposure note, and re-ground L3's thesis, then re-run the red team to confirm. The user decides what to act on.
