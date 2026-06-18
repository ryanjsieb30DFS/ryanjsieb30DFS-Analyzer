# Post-autopsy review — PGA Classic · RBC Canadian Open 6.11.26 · TPC Toronto (Osprey Valley, North)

_Archived slate: `rules/pga_classic/history/2026-06-17__pga-classic-rbc-canada-6-12-26`. Three contests entered (1,494 / 2,225 / 59,453 fields), best finish 5.0% (rank 78/1,494; rank 2,965/59,453). Scoreboard read: best-percentile trend + process — winnings/ROI tracked in the user's third-party app (results.json winnings null by design)._

## Process scorecard

**Grade: B+ on analysis, C on entry discipline.** The written analysis was disciplined and largely correct; the entry step leaked, and the portfolio's biggest bet was an edge the red team correctly flagged as fragile.

| Dimension | Grade | Evidence |
|---|---|---|
| Pre-flight checklist (analysis) | **PASS — honest** | All 7 lines present and specific in `slate_analysis.md`. Red team audited line-by-line and found no rubber-stamps; two disclosed-but-minimized framings (snapshot vs large-field ownership accounting; make-cut threshold-gaming) — both real, neither a fabrication. |
| Pre-flight checklist (lineups) | **CANNOT GRADE** | `lineups.md` was not archived (manifest `"missing": ["lineups.md"]`). Red team verified it existed and audited it at build time (3 SHIPs, all numbers exact), but it is gone from the archive — so the build checklist can't be re-graded here. Same archive gap as the Memorial. |
| Open lessons applied | **STRONG** | All 4 open lessons genuinely addressed, not name-dropped: `ch-scan-needs-skill-gate` (gated to Suber on form — and it PAID), `contrarian-needs-leverage-anchor` (L3 anchored on Finau), `fade-needs-ownership-to-materialize` (Reitan kept 0-1/3, not zeroed — correct), `entered-lineups-must-trace-to-plan` (carried as a process note — then partially violated, see below). |
| Anchor-Equivalence (mandatory) | **PASS — and it won the slate** | Fitzpatrick mandated as the alt anchor in ≥1 lineup. Fitzpatrick (111.5 FPTS, in 50-81% of top winners) was THE slate-defining anchor while primary value-chalk Rai busted. The rule directly produced the user's best results. |
| Entry traceability | **FAIL (recurring)** | The plan + red team covered 3 lineups. The user entered **6 distinct** lineups; **3 were off-plan and red-team-unseen** — including the single BEST (Fleetwood/Hall/Bridgeman/Cole/Cauley/Finau, 495, Rai-free) and the single WORST (Rose/Reitan/Rai/Taylor/Theegala/Pendrith, 349.5, a triple-chalk-anchor build a red team would likely have KILLed). Two-slate pattern now. |
| Red-team verdict adherence | **MIXED** | All 3 covered lineups were SHIP'd and entered as-is — adherence fine. But the red team's **portfolio findings** got no documented pre-lock response, and P1/P2 named the two biggest actual misses (below). |

**Red-team accuracy in hindsight (the headline process finding).** All three per-lineup verdicts were SHIP, and that was defensible — no single legal roster swap clearly improved a lineup within the codified rule lattice. But the red team's *portfolio-level* findings were strikingly prescient and went unactioned:
- **P1 (Rai self-eroding overweight) — RIGHT.** The red team flagged that the headline edge (Rai +25.3) was ETR's optimal exposure minus ETR's own ownership projection — a self-referential number with no calibration — and that "Rai could come in at 30%+ and the largest overweight ever logged compresses toward zero." Outcome: Rai came in at ~25-30% actual own (ABOVE projection) **and** busted (31.0 vs 71.2 proj), the single biggest miss of the slate. Carried 2/3, it was the portfolio's largest bet on the most fragile number.
- **P2 (accuracy-thesis monoculture vs a bomber leaderboard) — RIGHT.** The red team warned the build faded the distance scenario almost entirely. Outcome: ETR-docked bombers Potgieter (4.6% own) and Pendrith featured in multiple top-10 winners; the soft/wide venue let length play.
- **P3 (Reitan 0/3 repeats the lesson's pattern) — RIGHT.** Reitan anchored the overall slate winner; the analysis's "prefer Rai at the tier" was backwards.

Lesson: a SHIP-but-flagged red team is a signal to hedge or cap at the portfolio layer, not a clean bill of health. New hypothesis born (`act-on-redteam-portfolio-findings-on-ship`).

**What went right (don't lose it):** the analysis correctly identified the cheap value tier that defined the slate — Cauley, Suber, Bridgeman were all rostered heavily, which is why the best entries reached ~5%. The skill-gated CH scan produced Suber (a genuine slate-definer). The Anchor-Equivalence hedge (Fitzpatrick) captured the win. The miss that kept it out of the top 1% was over-weighting the uncalibrated Rai coffin edge and under-weighting Reitan/Fox/Pendrith.

## Lesson ledger changes

Updated `rules/pga_classic/lessons.yaml`:

**Promoted hypothesis → validated (first mechanism confirmation each):**
- `pga-classic-2026-06-10-ch-scan-needs-skill-gate` — Suber gated in on form at a 0.06-stickiness course returned 102.5 (35% of top winners); the un-gated CH boost carried no signal. Textbook.
- `pga-classic-2026-06-10-fade-needs-ownership-to-materialize` — Reitan kept 0-1/3 instead of full-faded; he anchored the slate winner. (Caveat logged: the lesson fixed the fade *direction* but not the *relative weight* — Rai was still preferred over Reitan and that was wrong.)
- `pga-classic-2026-05-11-contrarian-needs-leverage-anchor` — L3 anchored on Finau did not collapse (376, mid-field) the way the Truist L4 build did.
- `pga-classic-2026-06-10-entered-lineups-must-trace-to-plan` — the traceability gap recurred; best AND worst entries both bypassed the red-team net with no recorded thesis. Mechanism (not result) confirmed.

**Codified lessons — confirmation added:**
- `pga-classic-2026-05-11-never-zero-value-chalk-anchor` — third confirming slate: the Fitzpatrick alt-anchor hedge (111.5, slate-defining) paid while primary value chalk Rai busted.
- `pga-classic-2026-06-13-winning-structure-13own-2to3-darts` — winners ran 12.3-13.6% per-player own, ~1.85-1.95 sub-10% darts, 74-100% unique. Dead-on baseline. User entries ran slightly chalkier (~15-16.5%).
- `pga-classic-2026-06-13-leverage-play-mandatory` — four cheap sub-20% smashes (Cauley/Fox/Suber/Bridgeman) defined the slate, matching the "median 4 per slate."

**Codified lesson — SECOND mechanism contradiction added (retirement/revision bar met):**
- `pga-classic-2026-05-17-course-history-sub5-scan` — the un-gated CH × sub-5% scan has now failed at BOTH a high-stickiness (Memorial 0.42, qualifiers busted on skill) and a near-zero-stickiness (RBC 0.06, CH meaningless; cheap definer Suber came from form) course. The unconditional "CH boost = leverage" mechanism does not hold either way. See Proposed codifications.

**Hypothesis with ambiguous evidence (logged honestly, no verdict forced):**
- `pga-classic-2026-06-13-dose-darts-to-course-variance` — half-confirmation of the ~2-dart end only: a setup that played moderately tough still rewarded ~2 darts because Sunday scoring opened up; not clean evidence for the tough→3 branch.

**New hypotheses born this slate (mechanism-based):**
- `pga-classic-2026-06-17-single-vendor-overweight-self-erosion` — a single uncalibrated vendor's self-referential coffin gap (its optimal minus its own own-projection) self-erodes in that vendor's subscriber contests and must be capped, not made the biggest bet. (From red-team P1, confirmed by Rai.)
- `pga-classic-2026-06-17-leverage-spine-needs-sub20-combined-own` — the leverage-spine multiplier only operates sub-~19% COMBINED own; Rai+Cauley at ~42% was two chalk bets, not a spine. (From red-team L2 attack.)
- `pga-classic-2026-06-17-act-on-redteam-portfolio-findings-on-ship` — red-team P-series findings deserve a documented pre-lock response even when all per-lineup verdicts are SHIP. (From P1/P2 both proving right.)

## Venue file changes

Appended a `2026-06-17 — full autopsy (post-slate)` observation to `rules/pga_classic/courses/tpc_toronto_osprey_valley.md`, resolving the pending R4 tough-vs-birdie question and recording:
- Scoring opened up by Sunday (winning lineup totals 565.5-620.5, multiple sub-$7.5K golfers posting 100+) — moderate, not the locked-down course the 54-hole snapshot feared; "birdie-fest is weather-dependent" caveat retained.
- The slate-definer was a mid-priced accuracy/form value (Cauley $7.8K, 135.5), not a marquee name; the cheap-value tier defined the slate.
- Distance was live despite ETR's accuracy tilt (Potgieter/Pendrith in multiple winners) — vindicates the "light tilt / balanced" read; do not over-apply the accuracy boost here.
- The top accuracy-fit grade (Rai) busted — accuracy-fit at this venue is not a floor.

The file remains marked **UNVERIFIED** (now two slates of data: the 2025 Tour year + this one); keep it flagged until a third slate.

## Proposed codifications

_Proposals only — not applied. The user approves via the Autopsy tab._

### 1. Retire / supersede the unconditional course-history × sub-5% scan (2-contradiction bar met)

`pga-classic-2026-05-17-course-history-sub5-scan` is codified in **framework.md — Section 2 Slate Diagnostics (required scan)** and **Section 9 Pre-Submission Checklists**. It now has two mechanism contradictions (Memorial 0.42 stickiness; RBC 0.06 stickiness). Proposed edit to framework.md Section 2 — replace the unconditional scan with the skill-gated, form-co-equal version:

> **Sub-5% leverage scan (revised).** Do NOT run a bare "course-history boost × sub-5% projected own = leverage" scan — it has failed at both high- and near-zero-stickiness courses. Instead:
> 1. **Gate every CH-boost qualifier on a minimum skill/ball-striking floor.** A bottom-decile ball-striker with a course-history boost is lottery-slot-only regardless of stickiness.
> 2. **Treat the form/value engine as a CO-EQUAL source of sub-5% leverage** (hot approach numbers, recent qualifying/contention, value-report flags). The actual cheap slate-definers — Poston (Memorial), Suber (RBC) — came from form, not course history.
> 3. At sub-~0.15-stickiness courses, weight course history at ~zero and source cheap leverage entirely from form/skill.

This supersedes rather than deletes the original intent (find cheap leverage); the replacement mechanism is `pga-classic-2026-06-10-ch-scan-needs-skill-gate`, now **validated** (1 confirmation). _Note: that replacement lesson has only 1 confirmation, short of the 3-slate codification bar — so the recommended action is to retire the unconditional scan now and provisionally adopt the skill-gated wording, formally codifying the replacement after 2 more confirmations._

### 2. No other codifications this slate

No other lesson has reached the 3-mechanism-confirmation promotion bar:
- `never-zero-value-chalk-anchor` is already codified (this slate is its 3rd confirmation — already in framework/philosophy, no new edit needed).
- The four newly-validated lessons each have exactly 1 confirmation — hold for 2 more before proposing framework edits.
- The three new hypotheses are first-observation only.

**Watch-list for next slate (no action yet):** if `single-vendor-overweight-self-erosion` or `act-on-redteam-portfolio-findings-on-ship` confirms once more, they become strong candidates for a framework rule (cap single-vendor self-referential edges; mandate a documented portfolio-finding response). And the recurring `entered-lineups-must-trace-to-plan` gap is now a two-slate pattern — if it recurs a third time, propose a hard pre-lock gate (no DK entry without a matching `lineups.md` row or a logged deviation).

## Sharp gap analysis (large field — 59,453 entries)

_Added 2026-06-17 (post-autopsy, user-requested). Our 6 builds were also entered in the large field; this section benchmarks them against four named sharp players. Source: `~/Downloads/contest-standings-191094284.csv`. This is a benchmarking read, not a process re-grade._

**Headline:** winner 620.5; our best 495.0 (rank 2,965 / top 5.0%). The slate had a knowable shape and the *winning* sharps read it better at the portfolio layer.

### The slate's winning shape
A **mid-priced, moderately-owned value spine** — Bud Cauley ($7.8K, 135.5, 13.6% own; in **15/15** top lineups), Matt Fitzpatrick (111.5, 14.9%; 14/15), Ryan Fox (103.5, 12.0%; 9/15), Sudarshan Yellamaraju (102, 10.4%; 7/15) — plus **one sub-1% dart**. The expensive chalk mostly busted or met value: Rai (25% → 31.0), Fleetwood (26% → 85.5), Reitan (24% → 66.0), A. Fitzpatrick (24% → 78.0).

### Our 6 builds — the Cauley line is the whole story
| # | Pts | Rank | %ile | Cauley? |
|---|-----|------|------|---------|
| 1 | 495.0 | 2,965 | 5.0% | ✅ Fleetwood/Hall/Bridgeman/Cole/Cauley/Finau |
| 2 | 482.5 | 4,399 | 7.4% | ✅ Fitz/Lowry/Rai/Cauley/Fisk/Suber |
| 3 | 469.5 | 6,298 | 10.6% | ✅ Fitz/Rai/Bridgeman/Meissner/Cauley/Finau |
| 4 | 383.0 | 31,454 | 52.9% | ❌ Fleetwood/Clark/Rai/Greyserman/Finau/James |
| 5 | 376.0 | 33,982 | 57.2% | ❌ Rose/Lowry/Thorbjornsen/Cole/Finau/Potgieter |
| 6 | 349.5 | 42,954 | 72.2% | ❌ Rose/Reitan/Rai/Taylor/Theegala/Pendrith |

Top 3 had Cauley; bottom 3 didn't — a perfect split. Two failures kept us out of the money: **(a) zero exposure to Ryan Fox AND Sudarshan Yellamaraju** (the two mid-owned multipliers in 9/15 and 7/15 top lineups — on none of our 6); **(b) over-anchoring busted chalk** — Aaron Rai (25% → 31.0) on 3 of 6, and our worst build was a Rose+Reitan+Rai+Taylor triple-chalk-anchor.

### The four sharks
| Shark | Entries | Best | Best rank | Top 1% | Top 5% | Read |
|-------|---------|------|-----------|--------|--------|------|
| TheMish | 150 | 578.5 | 60 (0.1%) | 7 | 20 | Best of the four; 31% Cauley backbone + darts |
| Stonesalltheway | 150 | 565.5 | 160 (0.3%) | 5 | 18 | Cleanest pool: Bridgeman 80% / Fitz 75% spine, Hovland 43% / D.Thompson 35% darts |
| cantfademe | **1** | 527.5 | 882 (1.5%) | — | — | **Single bullet beat all 6 of ours** |
| Jsf900 | 150 | 549.0 | 354 (0.6%) | 1 | 13 | Leaned the busted chalk we did (Fleetwood 44% / Rai 35% / Reitan 25%) — worst of the four |

- **cantfademe (model single-entry shape):** Clark / Koepka / Reitan / **Cauley** / **Potgieter (98, 6.4%)** / **Keita Nakajima (80, 0.71%)** — 2 anchors + value spine + a true sub-1% dart. Beat our entire portfolio with one lineup.
- **The cautionary one — Jsf900:** leaned the same expensive chalk we did and finished worst of the four (median rank ~29.5K). Confirms the lesson isn't "sharps are magic" — the *winning* sharp lineups faded the busted chalk; the spine + a sub-1% dart was the edge.

### Sharks found in OUR contests (smaller fields)
Only **Stonesalltheway** crossed over — present in **both** smaller contests (the other three were large-field only). Same 5-lineup pool in each, best 508.5 (top 3.4% / 3.7%). Notably their small-field 5 carried **no Cauley** and still beat our pool on construction tightness (every lineup shared a Bridgeman + Max Greyserman + Davis Thompson/Hovland core). Our best (495, rank 78 / top 5.2%) outscored 4 of their 5 there — we were competitive in the small fields; the real gap was in the large field's tail.

### Net lesson (new)
The miss wasn't anchor selection — it was the **mid-owned value spine**. Fox + Yellamaraju (~10–12% own, both 100+) were core value plays every winning structure shared, and our pool never surfaced them. Logged as hypothesis `pga-classic-2026-06-17-mid-owned-value-spine-over-darts`. cantfademe's 2-anchor / value-spine / 1-sub-1%-dart single is saved as the reference construction shape.

### Controlling for volume — what the sharks did that we did not (besides more lineups)
Entry count (150 vs our 6) buys variance, not edge. With volume held aside, four of the five differences below are reproducible in a 6-lineup OR a 1-lineup build — and cantfademe's single bullet (beating all 6 of ours) is the proof:

1. **Spine on every lineup (exposure-rate, not count).** TheMish 31% Cauley; Stonesalltheway 80% Bridgeman / 75% Fitzpatrick. We had Cauley on only 3/6 and let the bottom 3 drift off the spine entirely (→ 53–72%ile). A 6-build portfolio should carry the spine in 6/6.
2. **Mid-owned multiplier identification.** Fox (12%), Yellamaraju (10.4%), Hovland (6.8%) — all 100+ ceiling, none on any of our 6. A player-ID edge one lineup captures, not a volume edge.
3. **Genuine sub-1% dart depth.** Their winners all carried one true lottery piece (Nakajima 0.71%, Garnett/Stanger 0.08%); our lowest-owned hit stopped at ~11–14%.
4. **The winners faded the busted expensive chalk.** We carried Rai (25%→31.0) on 3/6 incl. a quadruple-chalk-anchor worst build. Caveat already logged: Jsf900 leaned the same chalk and finished worst — so it's "the winners faded it," not "all sharks did."
5. **Designed exposures, not 6 independent guesses (NEW — highest-leverage process fix).** Stonesalltheway's pool shared a deliberate core and rotated only the differentiators — exposures decided first, lineups filled to hit them. Our 6 read as 6 separate ideas with no exposure plan, which is how a triple-chalk-anchor lineup slips in. Logged as hypothesis `pga-classic-2026-06-17-design-exposures-before-lineups`.

One-line: **they out-structured us, not out-volumed us.**
