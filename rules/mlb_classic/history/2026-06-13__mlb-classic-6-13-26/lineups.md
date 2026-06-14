# MLB Classic — Lineups (6.13.26) — selected from the SaberSim pool

**Method:** Selected (not built) from your 5,024-lineup SaberSim export, filtered to the slate analysis's winning shape — Yamamoto locked + cheap SP2 enabler + LAD pivot, off SD chalk, no TEX/BOS bats — then ranked on ceiling/leverage for the two SE contests. SaberSim sim metrics (ceiling percentiles, Saber Score, per-contest ROI) are supporting evidence, **not** the selector (sim-rank-not-gospel).

## Pre-flight checklist
- [x] Slate confirmed: building from `data/slate_analysis/mlb_classic.md` (6.13.26, this slate) — 8-game 4:05/4:10 main.
- [x] Selecting from pool: SaberSim `lineups_dk_...405pm.csv` (5,024 lineups); IDs resolved against the SaberSim/SIN session pool.
- [x] Venue read (via analysis): Rate Field is the open-air hitting game (87°/15mph wind out) — underpins the LAD blowup read.
- [x] Open lessons applied: condensation (hold Yamamoto), salary-enabler-pitcher (cheap SP2 not 2nd ace), five-man-primary-conditional-on-blowup (LAD-5 justified by the Rate weather), pivot-budget (one leverage axis = LAD).
- [x] Framework pre-lock — **Anchor-Equivalence:** both lineups are OFF all three crowded arms (Suarez 29% / Skubal 28% / deGrom 25.5%) by running a cheap SP2 → AE satisfied per analysis Decision 4 (no 2nd premium arm forced).
- [x] Prior results scanned: best-pct trend only; SIN calibration weightable (own MAE 3.28). GPP framing throughout.

---

## Lineup 1 — "Win when LAD doesn't" (from SaberSim pool · #902) → MLB $6K Rally Cap [$2K-to-1st]
**Thesis:** The two weak-pitching environments the field is *under* on — BAL at Camden (Edge #3, a third of SD's ownership) and the CIN bandbox at GABP — both light up, taking down a top-heavy single-entry from completely outside the field's LAD/SD chalk.

| Slot | Player | Team | Salary | Proj | Own% | Role |
|---|---|---|---|---|---|---|
| P | Yoshinobu Yamamoto | LAD | $10,800 | 19.4 | 35→~55-60 | Floor anchor (condensing #1 ace vs CWS) |
| P | Bubba Chandler | PIT | $6,200 | 12.8 | 15.6 | Cheap SP2 enabler |
| C | Samuel Basallo | BAL | $3,900 | 8.6 | 17.6 | BAL stack (Camden glue) |
| 1B | Pete Alonso | BAL | $5,300 | 9.2 | 9.3 | BAL power (underowned) |
| 2B | Edwin Arroyo | CIN | $2,000 | 6.7 | 5.3 | CIN bandbox punt |
| 3B | Sal Stewart | CIN | $4,800 | 7.7 | 5.0 | CIN bandbox bat |
| SS | Gunnar Henderson | BAL | $5,700 | 10.0 | 14.1 | BAL ceiling anchor |
| OF | Tyler O'Neill | BAL | $2,800 | 7.4 | 5.0 | BAL leverage (low own) |
| OF | Blaze Alexander | BAL | $3,200 | 6.5 | 3.9 | BAL value (very low own) |
| OF | JJ Bleday | CIN | $5,300 | 8.9 | 7.0 | CIN bandbox ceiling |

**Salary:** 10,800+6,200+3,900+5,300+2,000+4,800+5,700+2,800+3,200+5,300 = **$50,000** ✓ (≤ $50,000)
**Stacks:** BAL 5 (Basallo/Alonso/Henderson/O'Neill/Alexander) + CIN 3 (Arroyo/Stewart/Bleday) — **LAD-0, off the field's whole LAD/SD chalk.** **Total own ~118.3%** (avg 11.8%). **Sim:** Saber +11.4, ceiling 95th 147.3 / **99th 178.4**, **Rally Cap sim ROI +0.279 (best clean candidate), win-rate 0.23%, dupes 0.0.**
**What if?** *What if LAD is contained and the day's runs come from the two weak-arm games the field ignored (Camden + GABP)?* — wins in the exact world L2 dies in (true decoupling).

---

## Lineup 2 — "LAD + ARI both hit" (from SaberSim pool · #1164) → MLB $6K Chin Music [Single Entry]
**Thesis:** Two live offenses — the LAD pivot plus the ARI bandbox "chalk you can live with" — give a higher-floor two-stack that still ceilings out, the build that outlasts a bigger flatter field without needing LAD to win alone.

| Slot | Player | Team | Salary | Proj | Own% | Role |
|---|---|---|---|---|---|---|
| P | Yoshinobu Yamamoto | LAD | $10,800 | 19.4 | 35→~55-60 | Floor anchor |
| P | Bubba Chandler | PIT | $6,200 | 12.8 | 15.6 | Cheap SP2 enabler |
| C | Adrian Del Castillo | ARI | $3,000 | 6.6 | 4.9 | ARI mini (cheap glue) |
| 1B | Freddie Freeman | LAD | $5,200 | 8.7 | 5.7 | LAD core |
| 2B | Ketel Marte | ARI | $5,500 | 9.8 | 13.9 | ARI ceiling bat (GABP) |
| 3B | Max Muncy | LAD | $4,500 | 8.3 | 7.4 | LAD core power |
| SS | Mookie Betts | LAD | $4,300 | 8.8 | 12.0 | LAD core |
| OF | Colton Cowser | BAL | $2,700 | 7.1 | 4.9 | Cheap leverage punt (Camden side) |
| OF | Ryan Ward | LAD | $3,200 | 7.1 | 4.0 | LAD value (low own) |
| OF | Kyle Tucker | LAD | $4,600 | 8.0 | 3.7 | LAD ceiling (very low own) |

**Salary:** 10,800+6,200+3,000+5,200+5,500+4,500+4,300+2,700+3,200+4,600 = **$50,000** ✓ (≤ $50,000)
**Stacks:** LAD 5 (Freeman/Muncy/Betts/Ward/Tucker) + ARI 2 (Marte/Del Castillo) + BAL 1. **Total own ~107.5%** (avg 10.8%). **Sim:** Saber **+15.5 (pool-high)**, 99th 168.2, **positive sim ROI in BOTH contests** (Rally +0.031, Chin +0.056, Chin win-rate 0.26%).
**What if?** *What if LAD AND ARI both go and the single-stack builds leave points on the table?* — answers a different question than L1 (correlated two-stack floor, not single-stack max ceiling).

---

## Portfolio audit
- **Decoupled — the two entries win in different worlds:** L1 = BAL-5/CIN-3 (Camden + GABP weak-arm games), **LAD-0**; L2 = LAD-5/ARI-2. A LAD shutout kills L2 but L1 is built for exactly that world, and vice-versa. Different stacks, different games, different pitchers' game-environments. ✓
- **Distinct questions (no competing lineups):** L1 = off-the-field leverage on the two ignored weak-pitching games (top-heavy Rally Cap); L2 = LAD pivot + ARI floor (flatter Chin Music). ✓
- **Anchor-Equivalence:** Both run a cheap SP2 (Chandler) and are OFF all three crowded mid/premium arms (Suarez/Skubal/deGrom) — AE-compliant per analysis Decision 4. ✓
- **Own-pitcher rule:** No bats face Yamamoto (no CWS) or Chandler (no MIA) in either lineup. ✓
- **Off the field's chalk:** Neither stacks SD-5 (the 96%-owned field stack); L1 has zero SD, L2 zero SD. L1 expresses Edge #3 (BAL > SD at Camden); L2 expresses Edge #1 (LAD total-vs-own gap). ✓
- **One shared piece — Yamamoto — by design:** he's in both as the floor anchor. That's deliberate, not the old shared-failure flaw: fading the condensing #1 ace is a ~55-60% binary against the slate's best pitching spot (analysis Decision 1). The correlated *stack* risk — the real red-team finding — is now resolved (L1 off LAD entirely).
- **Both = $50,000 exactly, both hold the condensing ace, low dupes (0.0).** Ready to lock.

_Selected by Claude from the SaberSim pool against the 6.13.26 slate analysis; L1 re-selected to decouple from L2 per the red-team FIX. Red team (SHIP/SHIP, decoupled) renders below in the Analyze tab._
