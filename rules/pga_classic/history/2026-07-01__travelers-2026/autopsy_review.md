# Post-autopsy review — Travelers Championship (TPC River Highlands), 2026-07-01

_No-cut Signature Event · two Single-Entry contests: $35K Albatross (field 3,431) and $50K Dogleg (field 1,766) · 1 entry each · standings-only autopsy (no projections at autopsy time)._

**Headline:** worst finish of the sample — **98.3 pct** (Albatross, rank 3,373/3,431) and **99.7 pct** (Dogleg, rank 1,760/1,766). **Zero of the six slate-defining plays were rostered** on either lineup (`edge_leverage_capture` = 0.0). The two biggest scores on the board — **Viktor Hovland 144.0 @ ~7.6% own** and **Collin Morikawa 124.0 @ ~18% own** — never appeared *anywhere in the strategy doc*. This is the fourth straight slate the actual definer was outside our single-vendor lens, and the first time it produced a bottom-of-field result.

## Process scorecard

**Checklist present & honest — YES, and genuinely thorough.** The pre-flight checklist was complete: slate confirmed against dates (correctly distinguished the in-PDF US Open *recap* from this slate), venue file created + flagged UNVERIFIED, all 11 open lessons walked apply-or-reject, framework pre-lock checks run, Anchor-Equivalence named, prior results scanned, sharp envelope stated. The honesty prong holds — nothing was fabricated and the recurring "cheap definer missing" risk was explicitly named ("name the cheap smash here"). The checklist was not the failure point.

**Lessons applied vs ignored:**
- **Applied well:** `dose-darts` (~2-3 darts for a no-cut birdie-fest), `contrarian-needs-leverage-anchor` (Poston as the leverage floor), `single-vendor-overweight-self-erosion` (correctly sized Rai as a note, not the biggest bet — Rai busted, so this was directionally right), `leverage-spine-needs-sub20-combined-own` (correctly declined to call Poston+Rai a "spine" at ~21% combined).
- **Applied but WRONG on this slate — the major-pedigree rejection.** The checklist *rejected* `major-pedigree-in-form-leverage` as "out of scope — Travelers is not a major," and used that to justify fading Matt Fitzpatrick. Fitzpatrick (in-form 2022 U.S. Open champ, 9.74% own) then posted **121.0 and anchored the overall Albatross winner**. The lesson's "majors only" scope was the error, not its application — see Lesson ledger changes.
- **`entered-lineups-must-trace-to-plan` — silently ignored at build time.** The written Decisions were not executed: Decision 2 mandated "carry Scottie in SE-B (never zero the #1)" and "Tommy as the alternative in SE-A." Actual: **Scottie zeroed entirely**, Tommy moved to SE-B, and three players never recommended in the doc were inserted — **Ludvig Aberg** (named only as ranked *below* Tommy) and **Gary Woodland** in SE-A, **Jordan Spieth** in SE-B. No pre-lock rationale was recorded for any of them.

**Did the Top plays / PLAY-PASS-MIX decisions hold up vs DK actuals?**
- **Decision 1 — PLAY Poston both (lead leverage): MISS.** Poston was not a definer; rostered on both, contributed nothing to a takedown.
- **Decision 2 — Anchor-Equivalence Scottie/Tommy: not executed, and moot.** Neither Scottie nor Tommy was *the* defining anchor — **Morikawa** was (in ~60-65% of top lineups). Tommy *did* anchor the Dogleg overall winner (jewcup 690.5), so the anchor read wasn't wrong; but the winner paired Tommy with **Morikawa + Hovland + Harman + Bhatia + Conners**, none of which our SE-B carried. Anchor right, supporting cast entirely wrong.
- **Decision 3 — Si Woo both (core value): MISS.** The panel's "unanimous best play" was not a definer.
- **Decision 4 — cheap value tier + one sub-5% smash: partial.** Conners *was* correctly named in the doc (114.5 @ 7.3% — a genuine definer) but was **left off both lineups**. The named sub-5% smashes (Ben James / Snedeker / Cole) did not hit; the actual sub-10% smash (Hovland) was never named.
- **Decision 5 — PASS bomber chalk + Cam Young: broadly OK but not where the slate was decided.** Bombers weren't the story (a couple in top-10 tails). The costlier fades were the narrative "traps" **Harman and Keegan**, both of whom landed in multiple winning lineups.

**Structure vs selection.** The build sat *on* the winning envelope — 13.9% avg own vs winners' 12.8%, 2 sub-10% vs 2.5 (`shark_gap_top` own_per_slot delta just −0.2). The finish was not a structure failure; it was a **player-identification failure**, upstream in the strategy doc itself. Six definers (Hovland, Morikawa, Fitzpatrick, Bhatia, Conners, Hideki) — one named-but-not-rostered (Conners), one actively faded (Fitzpatrick), four never mentioned (Hovland, Morikawa, Bhatia, Hideki).

**GPP guard applied throughout:** the 98.3/99.7 result is not itself treated as evidence. Every ledger change below is anchored to a falsified *mechanism* (a fade whose own never materialized; a scope claim contradicted by a non-major definer; a slate-defining elite absent from the source lens), not to the loss or a null ROI.

## Lesson ledger changes

- **`pga-classic-2026-07-01-vendor-independent-ceiling-scan` — NEW hypothesis (born this slate).** The strategy is built off one vendor's coffin-overweight list (ETR) + one panel's named "best plays" (ETG), a lens that systematically omits in-form studs the vendor doesn't flag as leverage. Hovland (144 @ 7.6%) and Morikawa (124 @ 18%) are top-25 OWGR elites, not obscure darts, yet neither entered the doc. Fourth straight slate the definer sat outside this lens (Memorial: Poston/Cole; RBC: Fox/Yellamaraju; Shinnecock: Clark; Travelers: Hovland/Morikawa). Proposed guard: run a vendor-independent top-~15-ceiling scan *before* writing Top plays, then reconcile against the coffin/panel so no top-of-board stud is silently omitted. Ties together the identification, single-vendor, and pedigree lessons.
- **`pga-classic-2026-06-24-major-pedigree-in-form-leverage` — +1 CONTRADICTION (scope too narrow).** The "at a major specifically" boundary was used to reject flagging Fitzpatrick at a non-major; Fitz then defined a non-major. Falsified prong = the scope claim, not the loss. Refinement logged: broaden to *any* event — an in-form proven closer at sub-15% own is a blind spot regardless of major status. Still a hypothesis (1 contradiction; retirement needs 2).
- **`pga-classic-2026-06-17-mid-owned-value-spine-over-darts` — +1 CONFIRMATION → promoted `hypothesis` → `validated`.** Slate decided entirely by ~7-20%-owned multipliers (Hovland/Morikawa/Fitz/Bhatia/Conners/Hideki), zero deep darts among definers; we sat in the band yet caught none — the "necessary not sufficient" caveat firing again. Origin (RBC) + Shinnecock + Travelers = 3 mechanism slates.
- **`pga-classic-2026-06-10-fade-needs-ownership-to-materialize` — +1 CONFIRMATION (2nd; 3 slates total).** Fitzpatrick "faded" at −7.0 but came in 9.74% own — a sub-10% "fade" is not a fade; he was mispriced leverage and hit for 121, anchoring the winner. Origin (Memorial) + RBC + Travelers.
- **`pga-classic-2026-06-10-entered-lineups-must-trace-to-plan` — +1 CONFIRMATION (3rd; negative direction — gap re-opened).** Three off-plan players (Aberg/Woodland/Spieth) with no recorded thesis; Scottie zeroed against an explicit Decision. Mechanism confirmed (deviation forfeits process-grading); GPP guard noted (the deviation didn't demonstrably cost the slate because the plan also missed everything).
- **`pga-classic-2026-06-13-leverage-play-mandatory` (codified) — +1 CONFIRMATION.** The 96%-of-slates structural truth held (Hovland the sub-20% smash, 80-85% of winners) but the scan again failed to NAME him — reinforces "the scan must name the candidate."
- **`pga-classic-2026-06-13-dose-darts-to-course-variance` — +1 data point.** No-cut birdie-fest winners ran ~2.5 sub-10%; mild support for the no-cut branch running ~2.5 rather than a flat 2. Our 2.0 was a touch light; count close, selection was the miss.

## Venue file changes

Upgraded `rules/pga_classic/courses/tpc_river_highlands.md` header from **UNVERIFIED → VERIFIED (1 in-repo autopsy)** and appended a `## Per-slate observations` block dated **2026-07-01**:
- Birdie-fest + accuracy/approach archetype **confirmed** (winning totals 681 / 690.5; definers were precision ball-strikers, not bombers).
- **Elite talent > the vendor course-fit list** — only Conners (on the list) hit; Poston and Rai (#1 fit) busted; Hovland/Morikawa (the two biggest scores) were not on the fit list at all. Treat the fit list as a tiebreaker, not a definer source.
- Dose-darts: no-cut birdie-fest winners at ~2.5 sub-10%.
- Chalk that hit (Morikawa ~18%) — all-fade-the-studs is a non-starter here; the narrative "trap" fades (Harman, Keegan) both landed in winners.
- Our result + the identification-not-structure diagnosis.

## Proposed codifications

_Proposals only — not applied. User approves via the Autopsy tab. Two lessons cleared the 3-slate promotion bar this slate; a third promotion (traceability) is proposed with a discipline caveat; standing prior proposals are referenced but not re-litigated._

### 1. Promote `pga-classic-2026-06-17-mid-owned-value-spine-over-darts` (3 mechanism slates: RBC, Shinnecock, Travelers)
Proposed edit to **framework.md — Section 2 Slate Diagnostics** (append to the mandatory low-owned-smash scan):

> **The 10-16% mid-owned band is where Classic slates are decided, not the sub-5% tier alone.** Guarantee explicit PLAY/PASS coverage of *every* mid-priced play projecting a 100+ ceiling in the ~7-20% own band before adding deep darts. Caveat (necessary-not-sufficient): owning the band is required but does not itself win — four straight slates we sat in the band and missed the actual hitters, so this rule must be paired with the vendor-independent ceiling scan (proposal #3) that governs *which* members of the band get rostered.

### 2. Promote `pga-classic-2026-06-10-fade-needs-ownership-to-materialize` (3 mechanism slates: Memorial, RBC, Travelers)
Proposed edit to **framework.md — Section 6 Anchor Selection Logic (Trap chalk vs value chalk)** and **philosophy.md — Section 5 Chalk Has a Purpose**:

> **A fade is conditional on the ownership materializing.** Before locking any coffin/writer fade, sanity-check the player's actual/late ownership read: if it is sub-~12%, the fade premise is void and the player is mispriced leverage, not trap chalk. A sub-10% "fade" is not a fade — it just zeroes cheap upside. (Repeatedly cost slate-definers: Reitan/Clark at the Memorial, Reitan at the RBC, Fitzpatrick at the Travelers.)

### 3. Promote `pga-classic-2026-06-10-entered-lineups-must-trace-to-plan` (origin + 3 confirmations across 4 slates), with a discipline caveat
Promotion was already proposed at Shinnecock (gap had closed); this slate the gap **re-opened**, which strengthens rather than weakens the case to codify the *discipline* — adherence is currently coin-flip slate-to-slate. Proposed edit to **framework.md — Section 9 Pre-Submission Checklists**:

> **Every entered lineup must trace to the written plan, or the deviation is logged pre-lock with a one-line rationale.** A checklist line at submission: for each entered lineup, name the plan lineup/Decision it maps to; any player not in the plan requires a recorded reason. Undocumented deviations forfeit the process grade and any red-team/portfolio safety net (Memorial, RBC, and Travelers all off-plan with no `lineups.md`; Shinnecock on-plan and fully gradeable — the discipline is the difference).

### 4. Not yet — held as hypotheses this slate
- `pga-classic-2026-07-01-vendor-independent-ceiling-scan` (born this slate, 0 confirmations) — this is the single most important finding, but it is one slate old. Do NOT codify yet; carry it as the primary pre-slate discipline to test next slate.
- `pga-classic-2026-06-24-major-pedigree-in-form-leverage` — 1 contradiction (scope), broadened but not retired (retirement needs 2).
- Standing prior proposal from the Shinnecock review — codifying `pga-classic-2026-06-10-ch-scan-needs-skill-gate` (3 slates) — remains pending user approval; not re-litigated here (not tested this slate). Its counterpart `pga-classic-2026-05-17-course-history-sub5-scan` remains the retirement/revision candidate it was at Shinnecock.

## Applied

_User approved proposals #1, #2, #3 on 2026-07-01; applied to framework.md / philosophy.md and lessons.yaml. Proposal #4 items remain hypotheses (no edits)._

- **#1 — `pga-classic-2026-06-17-mid-owned-value-spine-over-darts`** → `validated` → **`codified`**. Added the "10-16% mid-owned band is where Classic slates are decided" rule (with the necessary-not-sufficient caveat) to **framework.md — Section 2 Slate Diagnostics**. `codified_in` set accordingly. (Codified text renders the review's "(proposal #3)" cross-reference as "the vendor-independent ceiling scan (the primary pre-slate identification discipline)" so no dangling review-internal pointer lands in the framework.)
- **#2 — `pga-classic-2026-06-10-fade-needs-ownership-to-materialize`** → `validated` → **`codified`**. Added the "a fade is conditional on the ownership materializing" rule to **framework.md — Section 6 Anchor Selection Logic (Trap chalk vs value chalk)** and **philosophy.md — Section 5 Chalk Has a Purpose** (identical text in both). `codified_in` set accordingly.
- **#3 — `pga-classic-2026-06-10-entered-lineups-must-trace-to-plan`** → `validated` → **`codified`**. Added the "every entered lineup must trace to the written plan, or the deviation is logged pre-lock with a one-line rationale" rule to **framework.md — Section 9 Pre-Submission Checklist** (section-level, above the SE checklist). `codified_in` set accordingly.
- **#4 — held, no edits.** `pga-classic-2026-07-01-vendor-independent-ceiling-scan` (0 confirmations, carry as primary pre-slate discipline next slate) and `pga-classic-2026-06-24-major-pedigree-in-form-leverage` (1 contradiction, broadened not retired) remain hypotheses. Standing Shinnecock proposals (`ch-scan-needs-skill-gate` codify / `course-history-sub5-scan` retire-revise) were not part of this approval and are unchanged.
