# Lesson-ledger hygiene review — NASCAR

Generated from the deterministic hygiene pre-pass. **Every item below is a PROPOSAL.**
Nothing in `lessons.yaml`, `framework.md`, or `philosophy.md` has been edited. Approve in the app to apply.

Ledger state: 32 lessons — codified 25, hypothesis 6, validated 1.

---

## Retire candidates

Two stale hypotheses flagged (0 confirmations, born 2026-05-01, ~59 days / 2 logged slates since). Both are **pre-lock process** lessons whose confirmation requires reconstructing a pre-lock decision that the **standings-only autopsy does not capture** — so 0 confirmations here is an observability gap, not a mechanism failure. GPP guard applies: untested ≠ contradicted.

- **`nascar-2026-05-01-portfolio-gaps-addressed-pre-lock` → KEEP.**
  Mechanism reason: the rule is testable and sound — an identified-but-unaddressed gap that then pays (origin: Suarez 35.35) is a real, recurring failure mode. It has gone unconfirmed only because no autopsy since born has surfaced a *named pre-lock gap left unaddressed that subsequently scored* — that conjunction is what a "relevant slate" means here, and the standings-only autopsy rarely reconstructs which gaps we diagnosed pre-lock. Not retired. **Watch-for:** next autopsy, explicitly check whether any pre-lock-flagged hole scored 20+ and was rostered nowhere.

- **`nascar-2026-05-01-ownership-shift-full-reevaluation` → KEEP.**
  Mechanism reason: the trigger is a *specific* event — a major, strategy-altering ownership swing between projection loads (origin: Blaney 54%→39%). That precise condition may simply not have recurred at a magnitude that demanded full re-evaluation, and even when it does the autopsy (standings only, no pre-lock projection history) cannot observe whether we re-ran the chalk-structure math. Untested for lack of an observable relevant occurrence, not failed. **Note:** this is the weaker of the two — if two further slates pass with a clear projection-ownership swing logged and still no confirmation, reconsider for retirement then.

No retirements proposed this pass.

---

## Near-promotion (2 of 3 confirming slates)

Each below sits at origin + 1 mechanism confirmation. Naming the exact third-slate mechanism so the next autopsy knows what to watch.

- **`nascar-2026-06-20-midpack-pd-over-deep-back-chalk` (hypothesis) — promote only the MID-PACK half.**
  This lesson has two halves with diverging evidence: (a) *mid-pack (P11–30) high-floor cars are the leverage PD source at thin-deep-back venues* — confirmed at Sonoma (Cindric/Preece/Custer/Stenhouse); (b) *fade the deep-back chalk* — **contradicted** at Sonoma (Keselowski P35 in ~7 of top-10). The clean promotion path is half (a) ONLY.
  **Third slate must confirm:** at a venue whose history shows a thin worse-than-30th optimal bucket, the field over-owns deep-back chalk PD AND P11–30 high-floor cars deliver the optimal place-differential (a mid-pack sub-15% starter scores 20+ FPTS and lands in winning lineups) while a deep-back swing is not required for the mid-pack edge to pay.
  **Caveat:** promote the *narrowed* statement (mid-pack PD is leverage; source PD from P11–30 when the field piles into deep-back). Do NOT promote the "fade deep-back chalk" clause — that half is being re-scoped (see Merge #4). See also Overdue section: this stays at 2, not 3.

- **`nascar-2026-06-20-anchor-equivalence-not-parity` (validated) — 1 confirmation, needs 1 more.**
  **Third slate must confirm:** a slate with a clear modal/chalk dominator where sizing the equivalent alternative for *leverage* (1–2 lineups) rather than *parity* (≈50/50) preserved win equity when the modal dom hit — i.e. a counterfactual parity hedge would have capped modal-world equity in half the portfolio. Mechanism to verify: hedging both sides of the dominator coin flip guarantees you cannot fully capitalize on either outcome. (Sonoma confirmed via SVG in ~95% of lineups with Gibbs as the alt; need one more dominator slate where the modal dom delivers.)

- **`nascar-2026-06-20-carry-a-sub5-leverage-dart-mme` (hypothesis) — 1 partial confirmation + open threshold question.**
  **Third slate must confirm two things:** (1) an MME portfolio carrying ≥1 genuine low-owned leverage dart reaches the win tail when a low-owned driver spikes, while a zero-low-own portfolio cannot; AND (2) resolve the threshold Sonoma opened — does the *paying* leverage band track the track type (sub-5% at chaos/superspeedway tracks vs sub-10% at low-chaos road courses, where deep PD needs a caution to materialize)? Mechanism to verify: a portfolio with zero sub-(threshold) exposure cannot reach the win tail on a low-owned spike. Until the threshold is settled, the codified statement must encode the track-conditioned band, not a flat sub-5%.

---

## Overdue promotion (≥3 confirming, not codified)

**None.** No *uncodified* lesson is at ≥3 confirming slates.

- The two lessons that hit 3 (`nascar-2026-05-01-correlation-not-substitution`, `nascar-2026-05-24-sleeper-spike-floor`) are **already `codified`** with `codified_in` populated — not overdue.
- The three near-promotion lessons above all sit at **2 of 3** — not yet eligible.

No codification edits proposed this pass.

---

## Merge candidates

- **#1 `nascar-2026-05-24-anchor-equivalence` ↔ `nascar-2026-06-20-anchor-equivalence-not-parity` → KEEP-SEPARATE (for now).**
  The first (codified) establishes the rule: run the equivalent alternative in ≥1 lineup. The second (validated, 2/3) is a *sizing refinement*: ≥1 lineup as coverage, NOT a parity hedge. Merging a stable codified rule with an in-flight validation would muddy the lifecycle. **Plan:** when `-not-parity` promotes, codify it as a *sizing clause appended to the existing Anchor-Equivalence Rule* (`rules/shared/anchor_equivalence.md` + framework Step 6 check #8) — effectively merging at the framework level rather than in the ledger. Cross-link is correct meanwhile.

- **#2 `nascar-2026-05-01-bet-sizing-reflects-inverse` ↔ `nascar-2026-06-20-anchor-equivalence-not-parity` → KEEP-SEPARATE.**
  Related but distinct objects. `bet-sizing-reflects-inverse` (codified) is the *general* exposure-calibration rule (confidence must be expressed in exposure deltas: high = +10–15 over field, etc.). `-not-parity` is the *specific* application to the dominator coin flip (don't over-size the equivalence alternative to a hedge). The general rule subsumes the specific one mechanically, but the specific one carries its own build-time enforcement and evidence. Keep separate; the cross-link documents the lineage.

- **#3 `nascar-2026-06-20-carry-a-sub5-leverage-dart-mme` ↔ `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` → KEEP-SEPARATE.**
  Different mechanisms, different actions. `carry-a-sub5-leverage-dart-mme` is a *portfolio-level* construction rule (≥1 low-owned dart across a 10-bullet MME set for win-tail reach). `midpack-pd-over-deep-back-chalk` is a *PD-sourcing* rule (where on the starting grid to mine place-differential at thin-deep-back venues). Both touch low ownership but are not duplicative. Cross-link is appropriate.

- **#4 `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` ↔ `nascar-2026-06-28-roadcourse-deepback-revives-on-strategy` → MERGE (recommended).**
  The Sonoma lesson explicitly states "Re-scopes [[midpack-pd-over-deep-back-chalk]]" and directly resolves the open Sonoma contradiction on the *deep-back-fade* half. Holding both produces two partially-contradictory pre-lock instructions ("fade deep-back chalk" vs "deep-back is live") — exactly the bloat hygiene targets.
  **Survivor:** `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` (older, born Pocono, carries the confirmations + the mid-pack mechanism). Retire `nascar-2026-06-28-roadcourse-deepback-revives-on-strategy` into it (`retired_reason: "Folded as the deep-back re-scope clause of nascar-2026-06-20-midpack-pd-over-deep-back-chalk"`).
  **Combined statement:**
  > At tracks whose venue history shows a thin worse-than-30th optimal bucket and a fat 11th–30th band (e.g. Pocono: 9.5% vs 57% of optimal), source place-differential from MID-PACK (P11–30) high-floor cars — that band is reliably reachable while a P37–38 car needs a near-impossible run, and the field's habit of piling into deep-back chalk PD leaves the mid-pack band as the leverage. Do not fade a high-floor mid-pack car on track-fit narrative when its start sits in the optimal band. **The mid-pack PD is ADDITIVE, not a substitute for the deep-back band:** a low multi-year deep-back-optimal rate is a base rate, not a per-race lock — on a road course especially, a single caution/fuel-strategy sequence can compress the field and revive the deep-back PD path within one race (Sonoma: Keselowski P35/24% own in ~7 of top-10, Erik Jones P32 = 28). Pre-lock: ADD mid-pack PD AND treat the deep-back band as live (rosterable alongside, not instead of); reserve the deep-back fade for drivers the FIELD is also low on, not for a deep-back CHALK.
  **Evidence handling:** survivor keeps the Sonoma mid-pack confirmation; the Sonoma "fade deep-back" contradiction is **resolved** (folded as the re-scope clause, its mechanism note preserved in the merge changelog — not erased). Net status: hypothesis, 1 confirmation on the mid-pack half, deep-back-fade half corrected.
  **Alternative if you'd rather not merge a fresh hypothesis:** keep separate one more slate to let `roadcourse-deepback-revives` earn an independent confirmation, then merge. Recommended call remains MERGE — the two already issue conflicting pre-lock guidance today.

- **#5 `nascar-2026-05-01-backup-car-not-auto-fade` ↔ `nascar-2026-06-28-injury-narrative-not-a-fade-thesis` → KEEP-SEPARATE (now); GENERALIZE on first confirmation.**
  Same mechanism, two instances: a *risk-factor narrative* (backup car / physical injury) lowers the floor but does not erase the price/start/equipment edge, and a field-shared narrative fade is negative leverage. But `backup-car` is **codified** and `injury-narrative` is a **0-confirmation hypothesis** — folding a fresh hypothesis into a codified rule is wrong lifecycle order. **Plan:** treat `injury-narrative` as an instance-confirmation of the SAME generalized mechanism; on its first independent confirmation, GENERALIZE the codified backup-car rule and retire `injury-narrative` into it.
  **Generalized statement to codify at that point:**
  > A risk-factor narrative — backup car, physical injury, or similar — is a risk factor, not a fade thesis. It lowers the floor modestly but does not erase the price/start/equipment PD math that put the driver at chalk ownership (Bubba top-5 from P37 in a backup car, 63 pts at 65.58% own; Bell, fractured wrist, #1 overall lineup at Sonoma, only 12% field own). Demand positive evidence the factor actually degraded output (practice speed, qualifying pace) before fading — a narrative alone is not it, and a field-shared narrative fade is negative leverage (an elite driver overcoming a field-discounted narrative is a leverage SPIKE).

---

### Summary of proposed actions
| Item | Proposal |
|---|---|
| `portfolio-gaps-addressed-pre-lock` | KEEP (observability, not failure) |
| `ownership-shift-full-reevaluation` | KEEP (specific trigger may not have recurred) |
| `midpack-pd-over-deep-back-chalk` | Near-promotion — confirm mid-pack half once more; also survivor of Merge #4 |
| `anchor-equivalence-not-parity` | Near-promotion — confirm leverage-not-parity sizing once more |
| `carry-a-sub5-leverage-dart-mme` | Near-promotion — confirm win-tail + settle track-conditioned threshold |
| Overdue promotion | None |
| Merge #1, #2, #3 | KEEP-SEPARATE |
| Merge #4 | MERGE → survivor `midpack-pd-over-deep-back-chalk`, retire `roadcourse-deepback-revives-on-strategy` |
| Merge #5 | KEEP-SEPARATE now; generalize backup-car on injury-narrative's first confirmation |
