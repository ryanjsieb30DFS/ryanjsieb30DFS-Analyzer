# Post-Autopsy Review — Memorial Tournament at Muirfield Village (PGA Classic 6.4.2026)

*Reviewed 2026-06-10. Archive: `rules/pga_classic/history/2026-06-10__pga-classic-6-4-2026`. Contests: $35K Albatross SE (3,431 entries, best 2,653rd / 77.3%) + $60K Birdie 20-Max (23,781 entries, 15 lineups, best 829th / top 3.5%). Winnings not recorded in results.json (null) — ROI ungradeable this slate.*

## Process scorecard

| Item | Grade | Evidence |
|---|---|---|
| Pre-flight checklist in slate_analysis.md | **FAIL** | No `## Pre-flight checklist` block anywhere in the archived analysis. Per CLAUDE.md: "No checklist block, no valid output." |
| Venue file read/created | **FAIL** | `rules/pga_classic/courses/` contained only the README at analysis time — no Muirfield Village file existed and no stub was created. (Created now by this review.) |
| Lineups.md / portfolio audit | **FAIL** | Manifest lists `lineups.md` as **missing** — the 16 entered lineups were never built or saved through the tool, so no theses, no portfolio audit, no exposure verification exists. |
| Red team | **NOT RUN** | `red_team.md` missing. Nothing to grade for verdict adherence — but this is itself the cost of the missing lineups.md: with no lineup file there was nothing to red-team, and the entered SE (see below) is exactly the kind of lineup a red team would have flagged. |
| Analysis substance | **PASS** | Despite the missing checklist block, the analysis substantively performed the ritual's content: anchor-equivalence section explicitly run (Scottie/Aberg/Young + Spaun/Rory clusters), codified lessons visibly applied (JT+Keegan spine, 2-leverage SE cap, trap-vs-value chalk split, CH-sub5 scan, exposure caps, Truist/PGA-Champ autopsies cited), course read built from stickiness data. |
| Open lessons applied | **PARTIAL** | The one open hypothesis (`contrarian-needs-leverage-anchor`) was honored in spirit (the chaos block distributes JT/Keegan/Rai) but never named, applied-or-rejected. All codified lessons were applied. |
| Entered lineups vs written plan | **FAIL (SE) / UNTRACEABLE (20-Max)** | The entered SE (Fitzpatrick / Si Woo / Smalley / Kitayama / Straka / Rai, 305 pts, 77.3 percentile) shares **zero** of six players with the analysis's recommended SE and is structurally over-chalky for the field: 17.74% avg own with 1 sub-10% play vs the SE winners' 12.25% / 2.24. The written SE's components (Scottie, JT, Keegan, Lowry, Nick Taylor, Eric Cole) almost all appear in winning structures. The 20-Max lineups loosely track the analysis (Scottie-led, Rai/Keegan/JT sprinkled) and the best one hit top 3.5% — but with no lineups.md, none of it traces. |
| Vendor calibration | **FAIL (tooling/timing)** | autopsy.json shows `projections.available: false, matched 0/73` — no projections in session at autopsy time, so no `vendor_calibration.jsonl` row was written. ETR/SIN accuracy on this slate is lost. |
| Results ledger | PASS (partial) | results.jsonl row written; winnings left null. |

### Hindsight on the analysis's key calls

- **Scottie as primary anchor, Aberg as forced equivalence hedge:** right on both counts. Scottie anchored the SE winner and 5 of the top-10 20-Max winners; Aberg busted. The asymmetric structure (carry chalk, hedge cheap) worked as designed.
- **JT + Keegan spine:** vindicated. The pair appears together in the rank-3 20-Max winner (537 pts); Keegan is in 3 of the top-10 20-Max winners.
- **JT divergence resolution (middle path, ~25-30%):** reasonable in hindsight — JT hit but wasn't slate-defining; neither slam nor zero was right.
- **Coffin fade side:** the week's biggest miss. Reitan (−5.1), Burns (−6.2), and writer-fade Wyndham Clark all landed in winning structures (Reitan 96.5 @ ~11%, Clark 102 @ 7.5%) — and all came in at 7-11% *actual* own, meaning the "over-owned trap" premise never materialized.
- **CH-boost sub-5% darts (Vegas/Echavarria/Horschel):** all busted; the actual sub-5% slate-definers (Poston 115.5 @ 2.7%, Cole in the 20-Max winner) came from the value/form engine the analysis listed but underweighted.
- **Blind spots:** Ryan Gerard (110 pts, 73.5% of SE top-34 winners, 66% of 20-Max top-100) and J.T. Poston appear nowhere in the analysis. The user's own hand-built 20-Max lineups captured both — the best entry (457.5, top 3.5%) carried Gerard + Poston + Rai.

## Lesson ledger changes

Applied directly to `rules/pga_classic/lessons.yaml`:

- **`never-zero-value-chalk-anchor`** — +1 confirmation (2nd): Scottie carried per the rule and anchored the winners; the Aberg hedge cost little. (Already codified.)
- **`leverage-spine-pairing`** — +1 confirmation (1st): JT+Keegan together in the rank-3 20-Max winner. (Already codified.)
- **`track-slate-lock-stat`** — +1 confirmation (2nd): Gerard/Poston winner-appearance stats tracked and converted into this review's new hypotheses. (Already codified.)
- **`trap-vs-value-chalk`** — +1 contradiction (1st): fade side mis-sorted Reitan/Burns/Clark on ownership that never materialized. Watch — 2 mechanism contradictions proposes retirement/amendment.
- **`course-history-sub5-scan`** — +1 contradiction (1st): at a 0.42-stickiness course the scan surfaced only bottom-skill busts and missed every actual cheap slate-definer. Watch.
- **`contrarian-needs-leverage-anchor`** — unchanged (hypothesis): no clean mechanism evidence either way this slate; lineup failures alone are variance per the GPP guard.
- **New hypothesis `ch-scan-needs-skill-gate`**: gate the CH×sub-5% scan on a minimum skill baseline; treat the form/value engine as a co-equal sub-5% leverage source (Poston/Cole vs Vegas/Echavarria/Horschel).
- **New hypothesis `fade-needs-ownership-to-materialize`**: projected-ownership fades are conditional on the ownership materializing; sub-12% actual voids the trap premise.
- **New hypothesis `entered-lineups-must-trace-to-plan`**: entered lineups must trace to a saved plan or carry a logged pre-lock deviation rationale; the untraceable SE was structurally over-chalky in exactly the way the written plan avoided.

## Venue file changes

Created `rules/pga_classic/courses/muirfield_village.md` (did not exist — itself a pre-flight miss). Physical profile sourced from this slate's archived analysis; appended a 2026-06-10 per-slate observation: elite-anchor thesis confirmed at the top of the board, but 0.42 stickiness did **not** rescue bottom-skill CH darts — course history adds weight on top of a skill baseline at Muirfield, it doesn't substitute for one.

## Proposed codifications

None this slate.

- No hypothesis-status lesson has reached 3 mechanism confirmations (this slate's confirmations all landed on already-codified lessons).
- No lesson has reached 2 mechanism contradictions. **Watch list:** `trap-vs-value-chalk` and `course-history-sub5-scan` each picked up their first — one more mechanism contradiction on either triggers a retirement/amendment proposal.
- Process recommendation outside the ledger (no approval needed, flagged for awareness): the missing pre-flight checklist block, missing venue stub, missing lineups.md, and the un-calibrated autopsy (projections absent at log time) were the slate's four process leaks. The first two are headless-run discipline; the last two are workflow — save lineups through the tool and keep projections loaded until the autopsy is logged.
