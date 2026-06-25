# Post-Autopsy Review — PGA Classic: U.S. Open at Shinnecock Hills (6/18/2026)

_Archived slate: `rules/pga_classic/history/2026-06-24__pga-us-open-2026`. Reviewed 2026-06-24. Run from DK contest-standings alone (no projections in the autopsy). Contests: **$10K Eagle** 5-Max (2,378) + **$20K Mulligan** 5-Max (2,941), 3 entries each. Best finish ~52nd pct (rank 1266/2378). ROI tracked in the user's third-party app — winnings null by design, NOT a gap._

---

## Process scorecard

**Overall: strong process discipline, one high-cost analytic miss, one recurring blind spot.** This was the cleanest-executed slate in three weeks — and the first that is fully process-gradeable.

**What went right (process):**
- **Traceability gap CLOSED (first time in 3 slates).** All six entered lineups trace exactly to the archived `lineups.md` (E1=L6, E2=L4, E3=L5, M1=L2, M2=L1, M3=L3). `lineups.md` AND `red_team.md` were both archived (`manifest "missing": []`). The red team's single FIX verdict (L1: Woodland → Kitayama) actually reached the entered M2 — the safety net functioned end to end. This is the corrective the Memorial and RBC autopsies kept asking for. (Confirms `entered-lineups-must-trace-to-plan` and `act-on-redteam-portfolio-findings-on-ship`.)
- **Pre-flight checklists present in BOTH `slate_analysis.md` and `lineups.md`, and largely honest.** The red team audited them line-by-line and graded them "honest work, not a rubber stamp." Open lessons were explicitly named at the thesis they shaped (Rai 0/6 for self-erosion; Si Woo/Fitz never paired for the spine rule; sub-5 darts skill-gated; exposures designed first).
- **Structure was on-envelope.** User per-player avg own ~12.5% vs winners' ~14.7% (we were slightly MORE contrarian, not over-chalky); sub-10% count 2.67–3.0 vs winners' ~2.1–2.7; all six unique (dup 1). The shape was sound.
- **Several calls held up:** Fitz-over-Si-Woo (Edge 4) — Fitz was a slate-definer, carried 2/6 ✅. Rejecting the pure course-history narratives (Cam Smith / Uihlein / Rodgers) and the sub-40%-MC amateurs — all correctly avoided, none hit ✅. Never-zero on Rory/Fitz (both in winning structures) ✅.

**What went wrong (where the slate was actually decided):**
- **THE miss — Wyndham Clark, absent everywhere.** The slate-definer was a ~10%-owned mid-priced multiplier: Clark, **102.0 FPTS at ~9.9–10.5% own, in 70.8–79.3% of ALL winning lineups across both contests.** He appears NOWHERE in `slate_analysis.md` and on NONE of the 6 entered lineups. The entire ~52nd-pct ceiling traces to this single zero. He was a recent U.S. Open champion (2023) in current form — an identifiable profile the lone vendor (ETR) under-projected and the analysis never independently scanned for. This is the **third straight slate** where the actual cheap/mid slate-definer was absent from our pool (Memorial: Poston/Cole; RBC: Fox/Yellamaraju; Shinnecock: Clark).
- **The one bad DECISION — Sam Burns PASS.** The analysis full-faded Burns (PASS) by invoking `single-vendor-overweight-self-erosion` to override ETR's coffin "HAMMER Burns." Burns came in at **19.18% actual vs 19.2% projected (flat — zero own-drift)** and **hit (77.0 FPTS, in 62.5% of Eagle top-24 winners)** — the slate's #2 definer. The self-erosion mechanism (own inflates → overweight compresses) demonstrably did not fire, and the fade cost a slate-definer. (Logged as the first mechanism contradiction on that lesson — see below.)
- **Hatton named but unrostered.** Tyrrell Hatton (69.5, 14.9%, 33% of top lineups) was correctly identified as a leverage dart in the analysis but carried 0/6 — a player-selection/exposure miss on a correctly-named play.

**Honest checklist nits the red team already caught (none flip a verdict):** the `slate_analysis.md`/`lineups.md` checklists overstated the value-spine application (Kitayama/English were 0/6 until the FIX — P1); under-counted L1's sub-5 pieces (4, not "2"); claimed "all sub-5 ≥55% MC" while Poston was 54%; and never surfaced the venue-file stickiness conflict (file assumed 0.42, analysis used 0.06 — P3). The build then **smuggled course history back in** on L3 ("Brooks won here 2018") at the same 0.06-noise course it called noise everywhere else — and Brooks duly busted.

**Edge-capture metrics (from autopsy.json):** `edge_leverage_capture` = 0.333 (we caught 1 of 3 slate-defining plays — Burns, via the 1/6 standalone exception; missed Clark and Hatton). `shark_gap_top`: leverage_pct delta **53.3** — the single biggest us-vs-field gap, driven almost entirely by the Clark zero.

---

## Lesson ledger changes

Edits applied directly to `rules/pga_classic/lessons.yaml` this review:

**New confirmations:**
- `pga-classic-2026-06-10-ch-scan-needs-skill-gate` (validated) → **+2026-06-24 confirmation.** Cleanest yet: a controlled natural experiment on one slate. Koepka had the strongest possible course-history signal (2018 Shinnecock winner) but no current form → busted at 7.2%; Clark (2023 USO champ, in form) → slate-definer at ~10%. Pedigree gated on form is the play; raw pedigree is a lottery. **Now origin (Memorial) + 2 confirmations (RBC, Shinnecock) = 3 mechanism slates → promotion candidate.**
- `pga-classic-2026-06-17-mid-owned-value-spine-over-darts` (hypothesis) → **+confirmation** (cross-archetype: held at a penal major). The slate was won by the ~10–16% multiplier band (Clark/Burns/Hatton), not anchors or deep darts. Caveat keeping it a hypothesis: owning the band is necessary, not sufficient — we keep owning the WRONG members.
- `pga-classic-2026-06-17-design-exposures-before-lineups` (hypothesis) → **+confirmation.** Exposures-first was actually executed (red-team-enforced); the RBC failure mode (a rogue quadruple-chalk-anchor build slipping in) did NOT recur — even the worst entry (M3, 142.5) was a *deliberately designed* contrarian build, not an accident.
- `pga-classic-2026-06-17-act-on-redteam-portfolio-findings-on-ship` (hypothesis) → **+confirmation** (procedural). P1 (Kitayama/English 0/6) got a documented pre-lock response that reached the entered lineup. Caveat: acting on a finding only helps if the finding names the right player — both build and red team were inside the single-vendor bubble and neither surfaced Clark.
- `pga-classic-2026-06-10-entered-lineups-must-trace-to-plan` (validated) → **+confirmation** (the converse/positive demonstration — gap closed, full gradeability, safety net functioned). **Now 3 mechanism slates (Memorial origin + RBC negative + Shinnecock positive) → meets the count** (see Proposed codifications for the post-pivot caveat).
- `pga-classic-2026-05-11-never-zero-value-chalk-anchor` (codified) → **+confirmation** (4th). Fitz, the Anchor-Equivalence alt, carried 2/6 and was a slate-defining anchor.
- `pga-classic-2026-06-13-leverage-play-mandatory` (codified) → **+confirmation.** Clark was the mandatory sub-20% smash (the 96%-of-slates truth held); the cost this time was the scan confirming "a smash exists" without NAMING the candidate.

**New contradiction:**
- `pga-classic-2026-06-17-single-vendor-overweight-self-erosion` (hypothesis) → **+1 mechanism contradiction (Burns).** The own-inflation prong was falsified (own held flat at 19.2%) and the override fade cost the slate's #2 definer. Refined guard added: only let self-erosion override "play the coffin overweight" when there is a concrete reason to expect the own to *inflate* (trendy/rising); a floored value-chalk play at stable projected own is not a self-erosion fade. Discriminator vs the RBC origin (Rai): Rai's own drew UP and he busted; Burns's own stayed flat and he hit. Still a hypothesis (1 contradiction; retirement bar is 2).

**New observation (no status change):**
- `pga-classic-2026-06-13-dose-darts-to-course-variance` (hypothesis) → **+observation.** A tough course predicted ~3 darts, but winners ran ~2.1–2.7 sub-10% — the 36-hole CUT caps how many cut-coinflips are safe. Proposed refinement: branch the dart count on cut format too (tough+cut ≈ 2–2.5, not 3).

**New hypothesis born:**
- `pga-classic-2026-06-24-major-pedigree-in-form-leverage` (hypothesis) — at a major, a recent major champion who is ALSO in current form but drawing sub-15% own is a systematic, single-vendor-invisible leverage blind spot (Clark this slate; Fitzpatrick at RBC + here as supporting). Mechanism-based scan proposed: at every major, list recent major champs, gate on a current-form floor, flag sub-15%-own survivors — do not rely on the lone vendor's projection to surface them.

**No retirements.** `trap-vs-value-chalk` was NOT given a 2nd contradiction: the Burns mis-call was the analyst OVERRIDING that lesson (which said play the coffin overweight) with self-erosion — so trap-vs-value-chalk would have gotten Burns *right*; the contradiction belongs to self-erosion, not to it.

---

## Venue file changes

`rules/pga_classic/courses/shinnecock_hills.md` updated:
- Header downgraded from "UNVERIFIED" to **"PARTIALLY CALIBRATED"** (this slate is the first calibrated data point).
- Added a **CALIBRATION CORRECTION** block: the pre-slate profile assumed above-average stickiness (~0.42 Muirfield analog); the slate **disproved it** — stickiness is effectively noise (~0.06). The two strongest pure-course-history plays (Koepka, Bryson) both busted; the slate-definer was won on FORM. Shinnecock pedigree is now flagged **gated on current form**, not a standalone signal.
- Added the **2026-06-18 per-slate observation**: winning scores 420.5/428.5; penal "limit-the-damage" prior confirmed (elite anchors + one mid-owned differentiator); Wyndham Clark the ~10%-owned slate-definer (102.0, 70.8–79.3% of winners); Burns/Hatton secondary; winners' structure ~14.7% own / ~2.1–2.7 sub-10 / 91–93% unique; the cut a real roster-killer. Logged our zero-Clark shortfall and the next-time recent-major-champ-gated-on-form scan.

---

## Proposed codifications

_Proposals only — do NOT apply until the user clicks "Approve & apply" in the Autopsy tab._

### 1. CODIFY `ch-scan-needs-skill-gate` → replace the raw course-history scan in framework.md (and retire the superseded raw scan)

`pga-classic-2026-06-10-ch-scan-needs-skill-gate` now has 3 mechanism slates (Memorial origin + RBC + Shinnecock). Its predecessor, `pga-classic-2026-05-17-course-history-sub5-scan`, already carries **2 mechanism contradictions** (Memorial + RBC) — meeting the retirement bar — and Shinnecock adds a third (Koepka, max course history, busted). Codifying the gate and retiring the raw scan are one paired action.

**Proposed edit — framework.md § 2 "Slate Diagnostics," replace the current line 32:**

> ~~**Course history boost list cross-referenced with sub-5% projected ownership.** This is a required pre-build scan as of May 2026. Players appearing on ETR's course history boost list with sub-5% projected ownership are structurally high-leverage and historically produce slate-defining outcomes (PGA Championship 2026: Smalley and Rai both met this criterion and appeared in 60-73% of top-100 winning lineups). Always check this list explicitly before locking the construction.~~

with:

> - **Course-history scan — SKILL/FORM-GATED (revised June 2026).** A course-history boost is leverage ONLY when paired with a current-form / skill-baseline floor; raw course history alone carries no signal (and at low-stickiness courses, none at all). Cross-reference the CH-boost list with sub-15% own, then KEEP only names that also clear a current-form floor; treat the form/value engine (hot approach/ball-striking, value-report flags, recent results) as a CO-EQUAL and often superior source of the sub-15% slate-definer. Evidence: the un-gated scan missed the actual cheap slate-definer at a high-stickiness course (Memorial 0.42 — qualifiers all bottom-decile skill, all busted; Poston/Cole won it on form) AND a near-zero one (RBC 0.06 — Suber won it on form, his CH boost was noise), and at Shinnecock the strongest possible CH play (Koepka, 2018 winner there) busted with no form while in-form recent champ Wyndham Clark (102 @ ~10%) defined the slate. **Pedigree without form = lottery; pedigree with form = the play.**

**And retire** `course-history-sub5-scan` (set `status: retired`, `retired_reason:` "Mechanism failed at both high- and near-zero-stickiness courses (Memorial, RBC) and again at Shinnecock; superseded by the skill/form-gated `ch-scan-needs-skill-gate`."), removing the un-gated scan references in framework.md § 9 (lines 151, 163, 171) and the tracking stat (line 182) in favor of the gated version.

### 2. CODIFY `entered-lineups-must-trace-to-plan` — MEETS THE COUNT, but recommend DEFER given the workflow pivot

`pga-classic-2026-06-10-entered-lineups-must-trace-to-plan` now has 3 mechanism slates (Memorial origin + RBC negative + Shinnecock positive). The discipline is proven and worth a hard pre-lock gate.

**Proposed edit — framework.md § 9 "Pre-Submission Checklist," add a line:**

> - [ ] **Every entered lineup traces to the written plan / red-teamed build, OR the deviation is logged pre-lock with a one-line rationale.** Undocumented deviations forfeit the red-team and portfolio-audit safety nets and cannot be process-graded.

**CAVEAT — recommend the user defer this one.** The repo pivoted on 2026-06-23 (commit 39b200a) to an **article-driven slate-strategy tool that no longer builds, selects, or enters lineups** — there is no `lineups.md` in the new workflow, so this gate may be vestigial going forward. It earned codification on the old (sim-tool) workflow that produced this slate. Suggest the user decide whether to (a) codify as-is for any residual hand-build use, or (b) mark the lesson `retired` with reason "workflow pivot — lineup entry now lives in the separate sim tool." Either is defensible; this review will not presume.

### 3. Everything else — None this slate.

`single-vendor-overweight-self-erosion` (1 contradiction), `mid-owned-value-spine-over-darts` / `design-exposures-before-lineups` / `act-on-redteam-portfolio-findings-on-ship` (1 confirmation each), and the new `major-pedigree-in-form-leverage` (0) are all below the promotion bar and stay as hypotheses. `dose-darts-to-course-variance` gained only an ambiguous observation. No further codifications proposed.
