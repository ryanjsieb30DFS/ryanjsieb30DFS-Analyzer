# Red Team — MLB Classic (6.13.26) — 2-lineup SE portfolio (post-FIX)

Adversarial pre-lock review. The original portfolio drew a **portfolio FIX** (both entries shared a LAD-5 + Yamamoto core). The FIX was taken: **L1 re-selected to a non-LAD build (#902, BAL/CIN)**. This is the re-reviewed, decoupled portfolio. Findings only — the red team does not rewrite lineups.

## Verdict summary
| Lineup | Contest | Verdict | The one thing |
|---|---|---|---|
| L1 — "Win when LAD doesn't" (#902) | Rally Cap ($2K-to-1st) | **SHIP** | Off-the-field BAL/CIN leverage; pool-high ceiling (178) + best clean Rally ROI (+0.279) |
| L2 — "LAD + ARI both hit" (#1164) | Chin Music (flat SE) | **SHIP** | Pool-high Saber (+15.5), +ROI both contests, real low-own leverage |
| **Portfolio** | both | **SHIP (decoupled)** | Original shared-stack flaw resolved — entries now win in different worlds |

---

## Portfolio-level findings
**The shared-failure flaw is resolved.**
- L1 is now **BAL-5 / CIN-3, LAD-0**; L2 is **LAD-5 / ARI-2**. The two single-entries are stacked on **different games entirely** — a LAD shutout (Burke contains them) kills L2 but L1 is built for exactly that world, and a Camden/GABP dud kills L1 while L2 survives on LAD. You now have **two real swings**, not one bet in two jerseys.
- **One shared piece remains — Yamamoto — and it's correct.** He anchors both as the condensing #1 ace. Fading him is a ~55–60% binary against the slate's best pitching spot (analysis Decision 1), so pinning both entries to him is a deliberate floor decision, not a diversification miss. The lever that mattered (the correlated *offense*) is decoupled.
- **Field duplication:** both show **0.0 SaberSim sim-dupes** — low-duplication builds. No concern.

## Anchor-Equivalence re-run
Both lineups run the cheap-SP2 route (Chandler) and are **off all three crowded arms** — Suarez (29.3%), Skubal (27.8%), deGrom (25.5%). AE resolves clean per analysis Decision 4 — no second premium arm forced. ✓

---

## L1 — "Win when LAD doesn't" (#902) → Rally Cap — SHIP
**Thesis under attack:** The two weak-pitching games the field is under on (BAL@Camden, CIN@GABP) both hit, winning a top-heavy SE from outside the chalk.
- **Steelman:** Directly expresses Edge #3 (BAL > SD as the Camden side, a third of the ownership) plus the GABP bandbox. **LAD-0** → fully decoupled from L2 and from the field's two most-owned stacks (LAD/SD). Pool-high-tier ceiling (**99th = 178.4**), **best clean Rally-Cap sim ROI (+0.279), win-rate 0.23%.** $50,000 exact, own-pitcher clean.
- **Refutation attempts:**
  - **Total own ~118% is the highest of the two** (Basallo 17.6%, Henderson 14.1% are semi-popular BAL bats). Still avg ~11.8%/player — inside the pivot-budget band, and the cheap BAL/CIN pieces (Alexander 3.9%, O'Neill/Stewart 5.0%) carry real leverage. Not chalk in costume.
  - **CIN is the lower-implied side of the bandbox** (CIN 4.50 vs ARI 5.25) — the secondary is on the weaker offense of that game. Mitigation: GABP lifts both sides, and the CIN bats are genuinely cheap leverage (Arroyo $2.0K/5.3%, Stewart $4.8K/5.0%). A minor knock, not a kill; an ARI secondary would be higher-ceiling but also higher-owned and would re-introduce overlap with L2's ARI mini.
  - **Two-game dependency:** needs Camden OR GABP to deliver — but that's the point of a leverage entry, and both are weak-arm parks. Acceptable risk for $2K-to-1st.
- **Verdict: SHIP.** This is the correct top-heavy leverage entry and it does the decoupling job.

## L2 — "LAD + ARI both hit" (#1164) → Chin Music — SHIP
**Thesis under attack:** Two live stacks (LAD pivot + ARI bandbox) give floor + ceiling for a flatter, bigger SE field.
- **Steelman:** **Pool-high Saber (+15.5)**, the only candidate with **positive sim ROI in both contests** (Rally +0.031, Chin +0.056). Genuine low-own leverage: Tucker 3.7%, Ward 4.0%, Cowser 4.9%.
- **Refutation attempts:** ARI is chalk (~85% combined; Marte 13.9% here) — trims leverage vs a pure-punt secondary, but the analysis endorses ARI as "the chalk you can live with," and the flatter Chin Music payout rewards the added floor. Not a kill.
- **Verdict: SHIP.** Best-constructed lineup of the pair; correct home (the flatter contest).

---

## Leverage-math check (vs vendor own)
- L1 ~118% / L2 ~108% total projected own (avg ~11–12%/player) — both inside the analysis's pivot-budget band. Real leverage.
- Yamamoto tagged ~35.5% in the sim own, but the analysis's mechanism call is **~55–60% actual** (condensation) — holding him is *higher-floor* than these own numbers imply, strengthening both.
- SD exposure: **0 in both** — correctly under the 96%-owned field stack. ✓

## Pre-flight audit (line by line)
- **Slate confirmed** ✓ — building from the 6.13.26 analysis, this slate.
- **Pool/source** ✓ — both rosters resolve to real SaberSim rows (#902, #1164); salaries verified **$50,000 each**.
- **Open lessons** — condensation (Yam held) ✓; salary-enabler SP2 (Chandler, not 2nd ace) ✓; **pivot-budget** (one leverage axis per lineup — L1 BAL/CIN games, L2 LAD) ✓. The earlier "both LAD-5, no 4-man hedge" flag is **moot** now: L1 is a BAL-5/CIN-3, a different shape entirely.
- **Anchor-Equivalence** ✓ — both off the crowded trio.
- **Own-pitcher rule** ✓ — no bats face Yamamoto (CWS) or Chandler (MIA) in either.
- **Prior results** — best-pct trend only; nothing contradicts this build.

**Bottom line:** Decoupled and shippable. Two single-entries that win in genuinely different worlds (BAL/CIN leverage vs LAD/ARI), sharing only the correctly-locked condensing ace. Lock both.
