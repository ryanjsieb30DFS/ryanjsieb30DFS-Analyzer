# Post-Autopsy Review — NASCAR Pocono Raceway · 2026-06-20

_Contest: NAS $100K Chrome Horn (logged field 25,260 in standings; 20-Max, 10 entries paid). Best finish: **rank 1,023 / 25,260 = 4.0 percentile** (L3 — Hamlin/Elliott/Hocevar/Buescher/Nemechek/A.Dillon, 262.9). Field winner 320.6. Winnings/ROI tracked off-repo (null here, by design)._

## Process scorecard

**Headline:** A solid top-5% result (best 4.0 pct) that was **structurally ceiling-capped by the single defining error: the build read the venue file correctly but overrode it with narrative.** The venue file said the 11th-30th start band is 57% of optimal and worse-than-30th is only 9.5% — yet the portfolio over-rostered deep-back chalk (Bubba 6/10, Keselowski 4/10) and faded the slate's #2 scorer, Reddick (P16, the optimal band), to 1/10 on a track-fit narrative ("not a great track for Reddick"). Every top-10 field lineup was Hamlin + the mid-pack PD cluster (Reddick/Nemechek/Herbst/Chastain); the portfolio captured Nemechek and Herbst but missed Reddick and Chastain (0/10).

**What the process got right:**
- **Nemechek** — the cleanest win. PLAY at 5% projected own ("1000% a legit top-10 threat"), scored 58.55 (9.43% actual own), the slate-defining play (96% of top lineups). In the two best portfolio lineups (L3, L4). Textbook low-owned-value-PD read.
- **Preece fade (Edge #2)** — correct. Preece at 36% was the field's over-owned value trap (DFR3 "2024 Gilliland pattern"); faded in all 10. He busted as called.
- **Erik Jones** — PLAY at 7%, scored 44.2. Independent value engine alongside Nemechek (see ledger: `correlation-not-substitution` confirmed).
- **Bell fade** — correct; the health binary was real, 17% field own underpriced it. Reallocating to Byron/Briscoe was sound process even though those doms didn't pay.
- **Sleeper-spike floor (re-scoped to 11-30)** — Gilliland P29 (35.5) and Stenhouse P21 (34.45) both hit; the venue-conditioned re-scope toward mid-pack starts was correct.

**What the process got wrong (mechanism, not luck):**
- **Reddick faded to 1/10** despite a P16 start squarely in the venue file's 57%-optimal band. The fade was narrative-driven ("not a great track for him… $10.3k rich") and contradicted the structural start-position signal the same analysis cited. Reddick scored 70.55 — the #2 piece on the slate and in the winning lineup. This single under-weight is why the portfolio's ceiling was 263 (L3) vs the field's 320. **Born this slate:** `nascar-2026-06-20-midpack-pd-over-deep-back-chalk`.
- **Over-rostered deep-back chalk.** Bubba P38 / Keselowski P37 (both 50%+) sit in the 9.5% bucket the venue file flags as thinnest. Keselowski busted to 2.0 (52% own, highest on slate); the three lineups doubling Bubba+Keselowski (L1 230.6, L8 166.9, L9 209.8) were the portfolio's weak cluster — vindicating the analysis's own Edge #5 cap, which it nonetheless rode to the edge of (3/10).
- **4/4 Hamlin/Larson dom split** — Anchor-Equivalence needed ≥1 Larson; the build ran 4, fully hedging the dom coin flip. Hamlin (modal, P1) delivered, so half the portfolio's dom equity was parked on the alternative. **Born this slate:** `nascar-2026-06-20-anchor-equivalence-not-parity`.

**Pre-flight checklist honesty:** Present and substantive in both `slate_analysis.md` and `lineups.md`; lessons applied/rejected with named mechanisms (not rubber stamps). Two blemishes: (1) the 8-set checklist claimed the 50%-Chalk Rule passed by aggregating "Bubba and/or Keselowski 5/8" — which masked Keselowski at 25%, below the 33% floor (red team Finding 1); **the 10-set corrected this** (Keselowski → 4/10). (2) Three different bundle-generation timestamps cited across the analysis (11:35), checklist (12:04), and bundle header (12:16) — immaterial to data, but a copied-not-verified detail. Net: honest, self-correcting between revisions.

**Red-team adherence & accuracy (red_team.md reviewed the 8-set; final entered set was 10):**
- **Heeded — correlated-leverage (Finding 2 / L5-L6).** The red team flagged the Larson+Briscoe twin builds. The user dropped both, added 4 new pool rows, drove Larson+Briscoe co-occurrence to 0. Correct adherence; the dropped builds would likely have scored poorly (Larson underdelivered, Briscoe did not hit). **Verdict right, heeded — ledger-supportive of `correlated-leverage-one-bet`.**
- **Heeded — Keselowski under the chalk floor (Finding 1).** Raised to 4/10 (40%). In hindsight Keselowski busted (2.0), so the floor compliance cost points — but this is the GPP guard in action: process-correct, outcome-bad. The deeper lesson is the scoping refinement now logged on the 50%-chalk rule (deep-back chalk ≠ reliable price/start math), not "ignore the rule."
- **Heeded (partial) — rain/strategy gap (Finding 3).** SVG added (L7, L10). The rain threat never materialized (full race, 320.6 normal winning score), so the coverage didn't pay and wasn't needed — a reasonable hedge, neither right nor wrong.
- **L1 FIX — overruled, legitimately.** Kept as the explicit "cash if chalk hits" coverage slot, which the red team allowed. L1 scored 230.6 (19.1 pct) with dup_count 39 — exactly the capped-ceiling/high-dup outcome the red team predicted. Verdict diagnostically right; the override was within the allowance.
- **Red team's blind spot (evidence against over-trusting it):** the red team **rubber-stamped the Reddick under-weight** ("Reddick is the analysis's own under-field call") rather than catching the mid-pack-PD structural error. It shared the analysis's blind spot on the slate's #2 scorer. The red team is strong on portfolio concentration and correlation; it did not independently re-derive the venue's 11-30 optimal-band signal. Worth remembering: the red team attacks theses present in the build, not the thesis that was missing.

**Capture metrics (from results.json):** leverage capture 1.0, overperformer capture 0.8, bust exposure 0.4 (Keselowski in 40% of lineups), lineup_avg_ratio 0.861. Consistent with the read above — strong leverage/overperformer capture, dragged by deep-back-chalk bust exposure.

## Lesson ledger changes

- **`nascar-2026-05-01-correlation-not-substitution`: hypothesis → validated** (+1 confirmation). Nemechek (58.55) AND Erik Jones (44.2) both hit the same slate — two deep-value PD plays at different prices/teams, neither "covering" the other. First mechanism confirmation. (Needs 3 to propose codifying — not yet.)
- **`nascar-2026-05-24-sleeper-spike-floor` (codified): +1 confirmation.** The Pocono re-scope to the 11-30 band held — Gilliland P29 (35.5) and Stenhouse P21 (34.45) both hit; the deep-back (P37/38) version did not (Keselowski 2.0).
- **`nascar-2026-05-01-50-pct-chalk-rule` (codified): +1 contradiction (scoping refinement, not result-based).** Keselowski 52% → 2.0 from P37. The rule's mechanism ("market right about price/START math at extremes") is absent when the chalk's start is deep-back at a thin-back track — there's no reliable start floor, so it's a chalk trap, not market wisdom. **Single mechanism-scoping note — does NOT meet the 2-contradiction retirement bar, and the rule stays codified.** Linked to the new mid-pack lesson.
- **NEW hypothesis `nascar-2026-06-20-midpack-pd-over-deep-back-chalk`.** At tracks where worse-than-30th is a thin optimal bucket and 11-30 is the meat, optimal PD comes from mid-pack high-floor cars; the field's deep-back-chalk habit leaves the 11-30 band as leverage. Mechanism: P11-30 PD ceilings are reachable, P37-38 needs a near-impossible run. Confirms the venue file. (Origin slate; 0 confirmations.)
- **NEW hypothesis `nascar-2026-06-20-anchor-equivalence-not-parity`.** Anchor-Equivalence requires ≥1 alternative for coverage, not a 50/50 dom hedge; expanding to parity (4 Hamlin/4 Larson) caps modal-world equity. Mechanism: hedging both sides of the coin flip forfeits full capitalization on either. Complements anchor-equivalence + bet-sizing-reflects-inverse. (Origin slate; 0 confirmations.)
- **No status change** to `hms-intermediate-double-up`: the analysis's rejection ("Pocono not a true intermediate") was harmless — HMS neither notably hit nor missed (Larson underdelivered, Byron/Elliott middling). Red team's "questionable rejection" note stands as a watch item, not evidence.

## Venue file changes

`rules/nascar/tracks/pocono_raceway.md`:
- Appended **2026-06-20 per-slate observation** recording the race result, which **confirms the venue thesis hard**: the 11th-30th band delivered (winner = Hamlin + Reddick P16 / Chastain P24 / Herbst P25 / Nemechek P8), the worse-than-30th chalk did not (Keselowski 2.0; Bubba middling; doubling them sank lineups), and the value-tier practice-speed leverage held (Preece 36% busted; low-owned value scored). Rain threat did not materialize.
- Upgraded the header note from "UNVERIFIED — built from articles only" to **"2026-06-20 race results confirm the core thesis"** (still single-slate of in-repo evidence; bucket percentages flagged supported-but-single-sample).

## Proposed codifications

**None this slate.**

- `correlation-not-substitution` is now validated with 1 confirmation — needs 2 more mechanism confirmations (3 total) before proposing a framework codification.
- The 50%-Chalk-Rule scoping refinement is a single mechanism-scoping note (needs 2 contradictions to propose retiring; it is not retiring and stays codified). If a second thin-back track repeats the deep-back-chalk bust, the proposal would be to **amend** the codified rule (not retire it) — e.g. "the 33% floor applies to 50%+ chalk with a reliable start floor; for worse-than-30th chalk at tracks where that bucket is historically thin, treat the floor as a ceiling, not a minimum." Holding until that second confirmation.
- Both new Pocono hypotheses are origin-slate only (0 confirmations) — no codification proposal yet.
