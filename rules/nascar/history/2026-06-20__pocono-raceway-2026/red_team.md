# Red Team — NASCAR Pocono Raceway (Cup) · NAS $100K Chrome Horn (20-Max, field 29,726, 10 entries)

_Adversarial pre-lock review of `data/lineups/nascar.md` (8 selected lineups). Job: kill these before lock. Ownership is single-source DailyFan (no `vendor_calibration.jsonl` exists — only the deprecated `calibrations.jsonl`, ignored), so every ownership number below is a note, not a weighted edge — but the field-vs-portfolio exposure math still holds regardless of source accuracy._

## Verdict summary

| Lineup | Verdict | One-line reason |
|---|---|---|
| L1 — Chalk-core eater | **FIX** | Only single-dom lineup AND the highest field-duplication (4 of top-5 chalk); capped ceiling in a 29.7K field. |
| L2 — Larson anchor-equiv pivot | **SHIP** | Lowest-own multi-dom, clean thesis; but carries the Hocevar+Buescher shared core (see portfolio). |
| L3 — Hamlin top-heavy, Preece faded | **SHIP** | Coherent top-heavy Hamlin build; the 36% Preece fade is a priced edge, not a flaw. |
| L4 — Hamlin + Briscoe two-dom | **SHIP** | Differentiated 2nd-dom on the chalk anchor; venue-supported two-dom shape. |
| L5 — Larson + Briscoe + Gragson | **SHIP** | Distinct high-variance no-Hamlin build; survives as its own thesis. |
| L6 — Max-leverage multi-dom | **FIX** | The Larson+Briscoe correlated-leverage twin of L5; first cut if trimming, and it triples down on secondary-dom-must-lead. |
| L7 — Hamlin + Byron + Cindric | **SHIP** | The cleanest Hamlin-anchored differentiation; lowest-own value PD route. |
| L8 — Reddick completion + Kes split | **SHIP** | Only Reddick + only solo-Kes lineup; genuinely answers a question no other lineup does. |

**No KILLs** — every lineup has a real independent win path. The damage here is at the **portfolio layer** (concentration), not in any single fatal lineup.

---

## Lineup attacks

### L1 — Chalk-core eater — **FIX**
**Steelman:** Every MME portfolio wants one "cash if the chalk pileup hits" slot (Pre-Lock Sanity #1). Hamlin P1 + Elliott + Bubba + Kes is the field's exact core, and Erik Jones (7%) is a real differentiator inside it. Salary $49,600, valid.

**Refute — what must ALL be true:** (1) Hamlin dominates from P1; (2) BOTH back-row chalk cars (Bubba P38, Kes P37) top-15 — i.e. you need the **9.5%-frequency worse-than-30th bucket to pay TWICE** (venue file: best-ever NextGen finish from a worse-than-30th starter = Haley 22nd/32); (3) you out-run the hundreds of identical field lineups built on this exact core.
- Condition (2) is the kill vector: L1 is the **only** lineup running Bubba+Keselowski together, deliberately betting the thinnest historical path twice. The analysis's own Edge #5 says don't do this in more than ~3 of 10 — L1 is the one that does, fine, but it pairs that with a **single dominator** (Hamlin only; Elliott is a P23 PD-elite, not a dom). The audit concedes "only L1 is single-dom." Venue file says two-dom is optimal in 9 of last 11 perfect lineups. A single-dom, double-deep-chalk lineup has a **structurally capped ceiling** exactly where you most need ceiling.
- **Duplication:** this is 4 of the top-5 chalk (Hamlin 48, Elliott 42, Bubba 50, Kes 52). In a 29,726-entry field the modal "chalk hits" world is shared with a huge cluster of near-identical lineups — "being in it" means splitting, not winning. Philosophy: "Win first. Cash second."

**Leverage audit:** EJ at 7% is the only sub-15% piece. Herbst (27%) over Preece (36%) is a mild pivot. Cumulative ownership is the highest in the portfolio. This is a low-leverage lineup by construction.

**FIX (one change):** Break the Bubba+Kes double — swap **Keselowski → a second dominator path** (Buescher/Briscoe-tier) to escape single-dom and cut the field duplication. If you keep it as the deliberate 1-of-8 cash-coverage slot, accept that and **cut it first if reducing entries** (not L6).

### L2 — Larson anchor-equivalence pivot — **SHIP**
**Steelman:** The mandatory Hamlin↔Larson alternative (lowest cumulative own), three credible dom paths (Larson/Byron/Buescher), Hocevar as the Preece-fade PD, Gilliland the sleeper floor. Distinct question (lead rotates off Hamlin through HMS/JGR).

**Refute:** Needs Hamlin to NOT wire-to-wire (he's P1, 48%, best track — the single most likely outcome) AND one of Larson/Byron/Buescher to actually lead. That's a real, independent win path, not an inverse-thesis ("Larson grabs the initial lead" is positive evidence per the analysis, not "Hamlin fails"). Survives.

**Shared failure (flag, not a kill):** L2 shares **Hocevar + Buescher** with L3 — two non-anchor pieces that are both portfolio overweights (see portfolio findings). If the secondary-dom/PD-elite tier underperforms, L2 and L3 sag together.

### L3 — Hamlin top-heavy, Preece fully faded — **SHIP**
**Steelman:** Hamlin + Elliott + Hocevar + Buescher top-heavy, Nemechek (5%) + Austin Dillon value, zero Preece. Edge #2 expression.

**Refute:** Must-be-true: Hamlin dominates, Hocevar converts top-5 speed from P26, AND Preece (36%) busts. The Preece fade is the load-bearing leverage — but it's *priced* (practice-speed red flags per DDD, and the DFR3 over-owned-value-busts pattern). Note the genuine counter-risk: venue file shows **deep-PD from elites CAN hit** (Berry P35→12 last year, Elliott P35→10 in 2023) — Preece is a P35 deep-PD play, not a pure trap. But fading a 36% play across the portfolio is the stated Edge #2 and the lineup holds without him. Ships.

### L4 — Hamlin + Briscoe contrarian two-dom — **SHIP**
**Steelman:** Differentiated 2nd dom (Briscoe 13%, won+dominated here last year) on the chalk anchor instead of doubling deep chalk; Hocevar PD + one deep chalk + Nemechek. Venue-supported two-dom shape.

**Refute:** Needs two doms to lead from P1 and P5 — but Decision 1 itself warns "two $9.9k+ doms is hard to make optimal (Hamlin+Briscoe both dominated last year and Hamlin still wasn't optimal)." Here Hamlin is $11k + Briscoe $9.9k = $20.9k on two doms, exactly the shape the analysis cautioned against. Still, with Briscoe at 13% the *leverage* is real if it hits, and it's only one lineup expressing it on the Hamlin anchor. Acceptable variance bet. Ships.

### L5 — Larson + Briscoe + Gragson sleeper — **SHIP** (but see L6)
**Steelman:** Two cheapest credible dom paths (Larson 27% + Briscoe 13%) + Hocevar + Bubba + EJ + Gragson sleeper. Pure no-Hamlin ceiling.

**Refute:** Larson+Briscoe is the **correlated-leverage stack** the Watkins Glen lesson (`correlated-leverage-one-bet`) targets — "two contrarian doms lead" is closer to one bet than two. The audit flags it honestly and argues L5/L6 share only those two drivers. True, but it means the portfolio has **two lineups (L5+L6) riding the same Larson+Briscoe engine** — if neither leads, both die. As its own high-variance thesis (no-Hamlin + caution-flip Gragson), L5 ships; the redundancy is L6's problem.

### L6 — Maximum-leverage multi-dom — **FIX**
**Steelman:** Larson + Briscoe + Buescher (three who can lead) + Elliott + Herbst + Austin Dillon, zero 48%+ chalk. The "win 1st if chalk busts" slot (Pre-Lock #2).

**Refute — what must ALL be true:** Hamlin AND the deep-back chalk all bust, AND **at least one of Larson/Briscoe/Buescher dominates**. This lineup stacks **three secondary/contrarian doms that all must out-run the chalk** — that is the multiplicative-bust risk philosophy warns against ("three leverage spots → no"). Worse, it's the **Larson+Briscoe twin of L5**: the two share that exact correlated engine, so the portfolio's "two highest-leverage builds" are largely **one bet entered twice**. The audit even names L6 as "the first to cut."
- **Concentration math:** Briscoe sits at 3/8 (38% portfolio vs 13% field = **+25pts**, over the codified +10 track-profile-overweight cap); Buescher at 5/8 (63% vs 22% = **+41pts**). L6 carries both of the portfolio's worst overweights in one lineup.

**FIX (one change):** Break the L5/L6 correlation — swap **Briscoe → Byron (15%)** in L6 (or drop L6 entirely and redeploy the entry). That gives L6 an independent contrarian-dom engine instead of re-betting L5's Larson+Briscoe, and trims the Briscoe overweight back under the cap.

### L7 — Hamlin + Byron + Cindric — **SHIP**
**Steelman:** Bell-reallocation into Byron (15%, race-winning practice speed) as the 2nd dom, one deep chalk, Buescher secondary, Cindric (16%) lower-owned value PD. Decision 3 expression.

**Refute:** Cleanest Hamlin-anchored differentiation in the set — field-rate chalk dom + two genuinely low-owned pieces (Byron 15, Cindric 16) the field is light on. Bell fade is correct (one-handed + relief-driver binary; 17% field own underprices it). No load-bearing single-leverage flaw. Ships — arguably the strongest lineup.

### L8 — Reddick completion + Keselowski single-deep-chalk — **SHIP**
**Steelman:** Only lineup with Reddick (29%, completes the Reddick↔Larson↔Herbst pair) and only one splitting Kes from Bubba. Larson primary, Buescher secondary, EJ value, Gilliland sleeper.

**Refute:** Reddick is the analysis's own under-field call ("not a great track for him… no dom equity, $10.3k is rich"). Pairing two $10k+ no-extra-dom cars (Larson $10.5k + Reddick $10.3k = $20.8k) compresses the value tier hard — EJ + Gilliland are doing heavy lifting. But it genuinely answers a question nothing else does (Kes-not-Bubba is the back-row hit + Reddick high floor), which is the point of the slot. Ships as the portfolio's required anchor-equivalence closer.

---

## Portfolio-level findings

**1. Keselowski (52% — the single highest-owned driver on the slate) is BELOW the 50%-Chalk-Rule floor — the audit hides it by aggregation.**
- Kes appears in **L1 and L8 only = 2/8 = 25%**. The 50%-Chalk Rule (`nascar-2026-05-01-50-pct-chalk-rule`, codified) requires ≥33% portfolio exposure on 50%+ chalk absent a definitive fade reason. There is **no definitive reason** — the analysis lists Kes as a core PLAY ("fastest car here last year").
- The portfolio audit asserts the rule passes by writing "deep-PD chalk (Bubba **and/or** Keselowski) appears in 5/8 (63%)." That **and/or aggregation masks a per-driver violation**: Bubba is fine at 4/8 (50%), but Kes — the *higher*-owned, equally-endorsed car — is at 25%. **FIX: add Keselowski to one more lineup** (target 3/8 = 37.5%) or state the definitive reason to underweight him. This is the clearest enforced-rule miss in the build.

**2. Secondary-dom concentration is the portfolio's biggest shared failure mode — Buescher 63%, over the +10 overweight cap.**
- **Buescher: L2, L3, L6, L7, L8 = 5/8 (63%) vs 13–22% field** — a +41-to-50pt overweight, ~5× the codified +10 `track-profile-overweight-cap`. The audit calls it "the heaviest single overweight… note the concentration" but **did not trim it.** Per `correlated-leverage-one-bet`, "Buescher leads/dominates from P6" is **one thesis appearing in 5 lineups.** Track position is king at Pocono and pit strategy routinely flips P6 cars (venue file: Larson led with 44 to go in 2024, finished 13th on a pit-road speeding penalty). **If Buescher runs ~mid-pack, five of your eight lineups lose a dominator path simultaneously.** This is the single game-state that damages the most lineups at once.
- Compounding: **Hocevar at 4/8 (50%) vs 32% field** (+18, also over cap). L2 and L3 carry **both** Hocevar AND Buescher — their fortunes are joined.
- **FIX:** drop Buescher from at least one of L6/L8 (Byron or a different secondary dom), pulling him toward ~3/8. Count theses, not drivers.

**3. The rain/strategy game-state — the most likely deviation on THIS slate — has ZERO dedicated coverage.**
- The slate analysis, venue file, and bundle all flag it: **race moved to 1pm on a real afternoon-rain threat; a halfway/shortened finish is live, which compresses dominator points and amplifies track-position/strategy variance.** Venue file: "teams reach the front via qualifying OR unconventional pit strategy… finishes deviate sharply (Bubba ran 18th in driver rating, top-10'd on fuel strategy)."
- Yet **every one of the 8 lineups is a dominator/deep-PD construction.** A rain-shortened race **simultaneously** (a) compresses the dom edge that 8/8 lineups depend on and (b) **kills the deep-PD chalk** — Bubba P38 and Kes P37 physically cannot make up positions in a shortened race. The portfolio's two structural bets (dominators + deep-back PD) **both fail in the same most-plausible world.**
- The strategy/track-position win path (SVG 13% "strategy-only 40pt path," listed MIX for 1–2 lineups in the analysis) is in **0 lineups.** Gragson/Gilliland are sleeper-spike floor pieces, not the structural strategy build. **This is both the biggest shared failure mode AND the biggest unexploited edge.** Consider one strategy/track-position-leaning lineup (SVG and/or a fuel-strategy mid-pack shape) so the portfolio isn't 8-for-8 dead in a rain-shortened finish.

**4. Anchor-Equivalence: compliant on the pairs, but the Hamlin/Larson split is a near-50/50 hedge, not a leverage expression.**
- All bundle pairs are technically satisfied: Hamlin↔Larson (4 Larson, true alternatives never stacked ✓), Preece↔Hocevar (Hocevar in 4, Preece 0 ✓), Reddick↔Larson↔Herbst (✓), Bubba↔Kes (L8 split ✓), AustinDillon↔Buescher (✓), 15–17 tier carried by Byron/Cindric (✓). **No anchor-equivalence violation.**
- But Edge #1 is "Larson over Hamlin," and it's expressed as **4 Hamlin / 4 Larson** — Hamlin at field rate (50% vs 48%) and Larson heavily overweight (50% vs 27%). That's defensible as overweighting the cheap-own equivalent, but a perfect 4/4 split also means you're **maximally hedged on the dominator coin flip** — which philosophy explicitly warns against ("Not hedge players. Hedging across all outcomes guarantees mediocrity"). Your win equity in the modal Hamlin-dominates world lives in just L1/L3/L4/L7; the 4 Larson lineups need Hamlin to NOT wire-to-wire. Acceptable, but know that the portfolio is built to *survive* the dom coin flip, not to *win* it.

**5. Field-duplication risk concentrates in L1.** The field core (per the analysis: Hamlin + Bubba/Kes + Elliott + Preece) is most closely replicated by L1 (4 of top-5 chalk). Every other lineup pivots the dom or fades Preece — good. L1 is the dup outlier (see L1 FIX).

**6. Entry count: 8 lineups for a declared 10 entries.** The audit defends stopping at 8 ("eight distinct theses beat ten with filler" — aligned with the build instruction). Fine strategically, **but confirm you are entering only 8** — the contest is logged as 10/20 entries. If 10 entries are paid, 2 will go unfilled (or the strategy/Kes FIXes above are exactly where 1–2 *non-filler* lineups could go: a strategy/rain build and a 3rd Keselowski lineup both add distinct theses, not padding).

**7. Open lessons — applied honestly, one questionable rejection.** `correlation-not-substitution`, `backup-car-not-auto-fade`, `sub-10-punts`, `sleeper-spike-floor` (3/8, meets ≥2), `sim-roi-not-a-selector` (correctly NOT used) all applied. **Questionable:** the build rejects `hms-intermediate-double-up` on the grounds "Pocono is not a true intermediate — mechanism absent," yet the venue file classifies Pocono as an "intermediate/superspeedway hybrid" where "practice speed correlates well for the top tier," and the build then **incidentally stacks HMS anyway** (Larson+Byron in L2, Larson+Elliott in L6). Harmless to the lineups, but the rejection rationale contradicts the venue file — the HMS equipment correlation may in fact be live here. Note, not a fix.

---

## Pre-flight audit (verified line by line — don't trust the checkmarks)

- **[x] Slate confirmed** — VERIFIED. Pool dated 6-14 1:19pm, race today. **Minor:** the checklist cites "bundle generated 2026-06-14 12:04," but the actual bundle header says **12:16** and the slate analysis cites 11:35 — three different timestamps. Immaterial to the data, but it's a copied-not-checked detail.
- **[x] Projections loaded (38 drivers, dk_ids 38/38)** — plausible; ownership figures cross-check against the bundle chalk/leverage tables (Kes 52, Bubba 50, Hamlin 48, Elliott 42, Preece 36, Hocevar 32, Reddick 29, Larson 27, Herbst 27, Buescher 22, Byron 15, Cindric 16, Briscoe 13). VERIFIED.
- **[x] Venue file read** — VERIFIED, **not a rubber stamp.** `rules/nascar/tracks/pocono_raceway.md` exists, is marked UNVERIFIED, and actually says what's claimed (11th–30th = 57% of optimal, worse-than-30th = 9.5%, two-dom optimal, value-tier practice speed treacherous). Good.
- **[x] Open lessons reviewed** — VERIFIED applied/rejected as listed, with the one questionable HMS-intermediate rejection above.
- **[x] Framework pre-lock checks** — **PARTIAL / RUBBER-STAMP on the 50%-Chalk Rule.** The line claims "50% Chalk Rule… 5/8 (63%) ✓" — but that aggregates Bubba+Kes and **masks Keselowski at 25%, below the 33% floor** (Finding 1). Anchor-Equivalence and two-dom (7/8, honest disclosure of L1) are accurately reported. The chalky-combo scrub claim (no chalk 2-combo in 2+ lineups) checks out — Bubba+Kes only in L1; the heavy repeats (Buescher/Hocevar) are *leverage* co-occurrence, which the scrub doesn't target, but Finding 2 shows that's the bigger real risk.
- **[x] Prior results scanned** — VERIFIED. `results.jsonl` does not exist; no `vendor_calibration.jsonl` (only the deprecated `calibrations.jsonl`, correctly ignored). DailyFan treated as a note, not a weight — correct.

**Bottom line:** No lineup is fatally broken — ship 6, fix L1 and L6. The portfolio's real exposure is at the structural layer: **Keselowski under the chalk floor (Finding 1), the Buescher 63% correlated overweight (Finding 2), and zero coverage of the rain/strategy game-state that would sink the whole board at once (Finding 3).** If you redeploy the 2 open entries, a strategy/rain build and a 3rd Keselowski lineup are the two highest-value, non-filler additions.
