# Post-Autopsy Review — Chicagoland Speedway (eero 400, raced 2026-07-05, logged 2026-07-12)

Slate: NASCAR — eero 400 at Chicagoland Speedway. First NextGen Cup race here.
Contests: 490 (best 34.9%), 1,176 (best 29.2%), 23,461 3-entry (best 27.1%). Buy-ins/winnings not tracked here (third-party app). Best percentile 27.1%; leverage_pct shark-gap **-16.7**.

## Process scorecard

**Pre-flight checklist: present, thorough, and honest.** All seven sections were filled with specifics. It correctly flagged that the venue was UNVERIFIED and that the NextGen car had never raced here (every track read = extrapolation), listed all 7 open lessons with an applied/rejected verdict + mechanism for each, and named the account's known NASCAR sub-5% leverage leak (19% vs 59% PGA) as the thing to fix. This is the standard to keep. No checklist dishonesty found.

**Decisions that held up (big wins):**
- **FADE Reddick (Anchor-Equivalence, Decision 1) — bullseye.** Reddick was the field's over-owned equivalent Toyota dom (43.6/51.2/54.2% own) and scored **-10.8**, the #1 fish trap in all three fields, 0% of winners. Fading the substitutable anchor and running the alternative was exactly right.
- **PLAY Briscoe as under-owned leverage dom (Top plays + Leverage) — hit.** Briscoe scored **71.85 at 6-10% own**, slate-definer #2, in 30-35% of top lineups. Naming him a PLAY (not just a pivot) was correct.
- **PLAY Hamlin as modal anchor (Decision 2) — hit.** 70.8, in nearly every winning lineup. Sizing him as the near-mandatory anchor rather than hedging to Reddick/Larson preserved modal-world equity while both hedge targets busted (Larson -12.5).
- **PLAY the P11-30 mid-pack PD band (Decision 3) — hit.** Cindric 45.9, Bubba 60.0, Suárez 41.5, Herbst, Gilliland all from the 11-30 band and all over the winning lineups.

**The defining miss — demoting a codified structural lesson on one article's org narrative:**
- The strategy trusted DDD's "JGR/23XI unfuckwithable, HMS a clear step off in 2026" org read and **demoted the codified HMS-intermediate-double-up lesson**, filing **William Byron** as "a leverage double-up for MME, not the primary path." Byron then scored **85.25 — the slate high — at only 10-13% own, in 40-80% of every field's winning lineups.** Alex Bowman (also HMS, also faded by the strategy as "MME or fade") anchored the #1 lineup of the 23,461 field.
- This is the single biggest process leak of the slate: a codified track-type edge was overridden by a single slate's article opinion, and because the field read the same narrative, Byron was left low-owned — i.e. the narrative *created* the leverage the strategy talked itself out of. Born as new hypothesis `nascar-2026-07-12-narrative-suppressed-elite-is-leverage`.

**Lessons applied vs ignored — did ignored ones cost anything?**
- Correctly REJECTED `ownership-shift-full-reevaluation` (one snapshot only) and `injury-narrative-not-a-fade-thesis` (no injury narrative). No cost.
- Correctly APPLIED anchor-equivalence-not-parity, midpack-pd, carry-a-sub5 (partial), portfolio-gaps.
- The codified `hms-intermediate-double-up` was effectively *ignored/overridden* — and it cost the slate's best play. Not an "open lesson ignored" in the checklist sense (it was consciously demoted), but the demotion was the miss.

**Persistent leak (process metric, not a mechanism contradiction):** user avg own ~31 in the 490 field with **0 darts**; leverage_pct shark-gap -16.7; the user leaned into the same Toyota-dominator chalk tier (Larson, Bell) that largely busted, while winners diversified into Byron/Briscoe/Bubba/Herbst/Gilliland at 6-13% own. The account remains too chalky and dart-light in NASCAR single-entry — the exact leak the checklist named but the builds didn't close. GPP guard: the mediocre finish is variance-compatible and is NOT logged as a contradiction of anything; only the mechanism findings above count.

## Lesson ledger changes

- **`nascar-2026-05-24-anchor-equivalence`** (codified) — +1 mechanism confirmation. Reddick (over-owned equivalent anchor) busted to -10.8 / 0% of winners while alternatives Hamlin (70.8) & Byron (85.25) hit. Stays codified.
- **`nascar-2026-06-20-anchor-equivalence-not-parity`** (validated) — +1 confirmation (Hamlin modal hit; hedged-toward equivalents Reddick -10.8 & Larson -12.5 both busted). **Origin Pocono + Sonoma + Chicagoland = 3 confirming slates → meets promotion criteria** (see Proposed codifications).
- **`nascar-2026-05-01-hms-intermediate-double-up`** (codified) — +1 mechanism confirmation (Byron 85.25 + Bowman at an intermediate); also flagged as the slate's demotion miss. Stays codified.
- **`nascar-2026-06-20-midpack-pd-over-deep-back-chalk`** (hypothesis → **validated**) — +1 confirmation of the mid-pack half (Cindric 45.9, Bubba 60.0, Suárez 41.5, Herbst, Gilliland). **3 confirming slates for the mid-pack half.** The "fade the deep-back CHALK" half again unsupported (Heim P28, 46-59% own, 55.1). See Proposed codifications (codify mid-pack half only).
- **`nascar-2026-06-20-carry-a-sub5-leverage-dart-mme`** (hypothesis → **validated**) — +1 confirmation (Herbst 4% in the #1 lineup of 23,461; broader paying leverage sub-10%: Byron 10-13%, Briscoe 6-10%, Gilliland 6%). Threshold settled at "sub-10%, sub-5% at chaos tracks." 3 confirming slates → see Proposed codifications.
- **NEW `nascar-2026-07-12-narrative-suppressed-elite-is-leverage`** (hypothesis) — born from the Byron/HMS demotion miss. A shared article+field org-narrative compresses ownership on a structurally-elite driver; the codified track-type edge should override a single slate's article org-opinion, and the ownership discount is the edge.

## Venue file changes

`rules/nascar/tracks/chicagoland_speedway.md` — **de-UNVERIFIED** (first NextGen race now autopsied). Appended a dated **Per-slate observations** block: HMS did not step off (Byron 85.25 was the slate); both orgs split hit/bust so dominator selection > org; mid-pack P11-30 PD was the meat; deep-back CHALK (Heim P28) paid — not a trap; winning blueprint = 1-2 doms + a narrative-suppressed HMS leverage dom (Byron) + Bubba + Heim + a P11-30 PD stack. Standing questions marked ANSWERED.

## Proposed codifications

_Proposals only — not applied. User approves in the Autopsy tab. GPP guard respected: each is a mechanism promotion at 3 confirming slates, not a result reaction._

### 1. Codify `nascar-2026-06-20-anchor-equivalence-not-parity` (3 confirming slates: Pocono origin, Sonoma, Chicagoland)

Proposed **philosophy.md — On Process Discipline** addition (under the existing Anchor-Equivalence entry):

> **Coverage, not parity.** The Anchor-Equivalence Rule requires the equivalent alternative in *at least one* lineup as coverage — it is NOT a mandate to split the dominator coin flip 50/50. Size the alternative for leverage (1-2 lineups when the field is mispricing it), and keep the modal dominator as the portfolio anchor. Hedging both sides of the dom coin flip to parity guarantees you cannot fully capitalize on either outcome: at Pocono the 4-Larson hedge capped Hamlin-world equity when Hamlin (modal) delivered; at Chicagoland concentrating on modal Hamlin (70.8) while leverage-sizing the alternatives was right as both hedge-target equivalents busted (Reddick -10.8, Larson -12.5).

Proposed **framework.md — Step 6 mandatory check #8** amendment: append "— run the equivalent alternative in ≥1 lineup as *coverage*; do not hedge the dom coin flip to parity. Keep the modal dominator as anchor; size the alternative for leverage (1-2 lineups)."

### 2. Codify the MID-PACK half of `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` (3 confirming slates: Pocono, Sonoma, Chicagoland) — **and explicitly NOT the deep-back-fade half**

Proposed **framework.md — Quick-Reference Decision Heuristics** addition:

> **Mid-pack PD is the leverage meat (intermediates + PD tracks).** When venue history shows the P11-30 band supplies the bulk of optimal spots (~55% at Chicagoland/Pocono-type tracks), source place-differential from the 11-30 mid-pack band — the field habitually piles into deep-back chalk PD, leaving the mid-pack under-owned. **Do NOT read this as "fade the deep-back chalk"**: deep-back chalk can ALSO pay (Heim P28 55.1 Chicagoland; Keselowski P35 Sonoma) — ADD mid-pack PD, don't substitute it for the deep-back band. The deep-back *fade* is reserved for drivers the FIELD is also low on (see `roadcourse-deepback-revives-on-strategy`).

Note: the parent hypothesis stays open in `lessons.yaml` because its literal "fade the deep-back chalk" wording carries a Sonoma mechanism contradiction; codify only the reframed mid-pack-is-the-meat statement above.

### 3. Codify `nascar-2026-06-20-carry-a-sub5-leverage-dart-mme` (3 confirming slates: Pocono, Sonoma, Chicagoland; threshold now settled)

Proposed **framework.md — Step 5 Portfolio Review** addition:

> **Carry a low-owned leverage dart in MME.** Across a 10+ -bullet NASCAR MME portfolio, at least one lineup must carry a genuinely low-owned leverage driver with real upside (a mid-pack flex or PD sleeper, not chalk relief). Threshold: **sub-10% own, tightening to sub-5% at high-chaos tracks** (Herbst 4% was in the #1 Chicagoland lineup; Byron 10-13% / Briscoe 6-10% / Gilliland 6% were the broader paying leverage). Scope: MME only — a sub-10% punt with a Dustin "MME or fade" tag is not a single-entry leverage play. Track every slate via `src/shark_gap.py` leverage_pct delta; the account's standing gap (-16.7 at Chicagoland) is the single biggest fixable NASCAR leak.

### Retirement candidates

None this slate. No lesson reached 2 mechanism contradictions; the GPP guard held (the mediocre finish is variance, not a mechanism failure).

## Applied

User approved all proposed codifications on 2026-07-12. Applied:

1. **`nascar-2026-06-20-anchor-equivalence-not-parity` → codified.** Added the "Coverage, not parity" paragraph to `philosophy.md — On Process Discipline` (under the Anchor-Equivalence entry) and amended `framework.md — Step 6 mandatory check #8` to require running the equivalent alternative in ≥1 lineup as *coverage* (no parity hedge; keep the modal dominator as anchor, size the alternative for leverage). Lesson `status: validated → codified`; `codified_in` set to both sections.

2. **Mid-pack half of `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` → codified (partial).** Added the "Mid-pack PD is the leverage meat" heuristic to `framework.md — Quick-Reference Decision Heuristics` (source PD from the P11-30 band; ADD mid-pack PD, do NOT substitute it for / fade the deep-back chalk). Per the proposal, the **parent lesson STAYS OPEN** (`status` remains `validated`) because its literal "fade the deep-back chalk" wording carries the Sonoma mechanism contradiction; `codified_in` records the PARTIAL codification of the mid-pack-is-the-meat half only.

3. **`nascar-2026-06-20-carry-a-sub5-leverage-dart-mme` → codified.** Added the "Carry a low-owned leverage dart in MME" check to `framework.md — Step 5 Portfolio Review` (≥1 lineup with a sub-10% / sub-5%-at-chaos-tracks leverage dart across a 10+ -bullet MME portfolio; MME only; tracked via `src/shark_gap.py` leverage_pct delta). Lesson `status: validated → codified`; `codified_in` set to the Step 5 section.

No retirements. `nascar-2026-07-12-narrative-suppressed-elite-is-leverage` remains a `hypothesis` (born this slate).
