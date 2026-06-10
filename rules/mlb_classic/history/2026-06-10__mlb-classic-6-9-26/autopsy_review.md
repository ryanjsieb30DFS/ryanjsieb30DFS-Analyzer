# Post-autopsy review — MLB Classic 6.9.26 (reviewed 2026-06-10)

First archived MLB Classic slate. Two SE entries ($5k Base Hit 490-field, $10K
Base Hit 980-field, $24 total buy-in); best finishes 41.2% and 39.9%, both below
the cash line (96.3 vs 111.35 needed; 95.3 vs 108.6). ROI not recorded
(winnings field empty — assumed no cash). GPP guard applies throughout: the
misses themselves are variance; only the mechanism findings below are evidence.

## Process scorecard

| Check | Grade | Detail |
|---|---|---|
| Pre-flight checklist present | **FAIL** | Neither `slate_analysis.md` nor `lineups.md` contains the mandatory `## Pre-flight checklist` block ("no checklist block, no valid output"). |
| Checklist honesty (informal) | **PARTIAL** | No block to audit, but the analysis did honestly disclose what a checklist would have: framework/philosophy stubs flagged, the snapshot leverage-table data artifact caught and discarded, projected-not-confirmed lineups flagged with named pre-lock pivots, sources footnoted. The substance was mostly there; the ritual was not. |
| Venue file read/created | **FAIL** | `rules/mlb_classic/parks/` contained only the README — no Coors (or any) park file existed and no stub was created pre-lock. Created now by this review (`parks/coors_field.md`). |
| Open lessons applied | **PASS** | All four ledger entries were codified (no hypothesis/validated lessons existed yet). All four were followed: 5-man primary stack built; own-pitcher rule explicitly verified in the lineup notes; single distinct thesis for 1 unique lineup; Anchor-Equivalence explicitly run with named classes and a PASS/PASS resolution. |
| Red team | **NOT RUN** | `manifest.json` lists `red_team.md` as missing — the pre-lock adversarial review was skipped. No verdicts to grade. Worth noting: the most basic red-team check (verify the leverage math against the field size) would likely have flagged the 8-sub-10%-players construction against the analysis's own "one or two structural pivots" directive. |
| Portfolio matches what was entered | **FAIL** | The archived portfolio says "same lineup in both SE contests," but only the $10K entry matches it. The $5k entry (CHC 5-3 Coors chalk: Busch/Bregman/PCA/Suzuki/Ballesteros + Castro/Tovar/McCarthy, Teng+May) appears nowhere in `lineups.md` — an untracked entry with no thesis, no audit, no red-team coverage. |
| Build obeyed its own analysis | **FAIL** | The analysis opened with "Small-field single entry: mostly-sound construction with one or two structural pivots beats full contrarian," then the build stacked three leverage axes at once — full fade of all three mega-stacks, pitcher pivot (Wheeler 9.5%), second leverage arm (Alvarez 8.1%), and punt fills (Wynns/Dubon) — landing at 8 sub-10% plays vs the $10K winners' 4.45 mean. |

### Key calls in hindsight

- **ATL leverage stack — RIGHT (mechanism confirmed).** ATL 5-stacks finished
  rank 2 in the $5k (156.6) and rank 4 in the $10K (151.35); Olson scored 32.0
  (+22.6 vs proj) and was a slate-defining play at 5.5% own. The thesis was the
  correct read; the surrounding construction, not the core, sank the lineup
  (Wheeler over a chalk-class arm, and Wynns/Dubon punts where the winning ATL
  builds used Riley/Albies/Herrera-tier bats).
- **MIL mega-chalk fade — RIGHT.** Turang 0.0 pts at ~31% actual own; MIL
  stacks absent from the winners.
- **Teng fade — RIGHT (mechanism).** The short-leash flag (2.5 avg IP) was the
  stated reason; he busted at 1.8 pts on 27–29% actual own.
- **May "chalk-trap risk" — WRONG.** May anchored 13 of the 20 listed top-10
  lineups across both contests. His chalk was salary-driven, and that salary is
  exactly what unlocked the winning bat structures — an enabler, not a trap.
  Ledgered as a new hypothesis (ownership alone doesn't indict a cheap viable
  P2; workload/leash does).
- **Wheeler pivot — MISSED, scored as variance.** Wheeler appears in only 1 of
  20 top lineups while Cease (31.1 pts at 12.8–16.9% actual own, the
  slate-defining arm) won the pitcher slot from *inside* the chalk class. Not a
  mechanism failure of Anchor-Equivalence, but a caveat recorded on that
  lesson: the alternative anchor can be the lowest-owned member of the class
  itself, and in a small field the pitcher pivot shouldn't be layered on top of
  a stack pivot.

## Lesson ledger changes

Applied directly to `rules/mlb_classic/lessons.yaml`:

1. **`mlb-classic-2026-06-01-team-stacking-core-lever`** (codified) — added a
   2026-06-10 mechanism confirmation: 5-man-primary shapes dominated both
   top-20 boards; the ATL 5-stacks captured Olson's 32-pt game multiple times.
2. **`mlb-classic-2026-06-01-anchor-equivalence-check`** (codified) — added a
   2026-06-10 mechanism confirmation at the stack level (highest-owned
   equivalent busted, named alternative hit top-4 in both contests) with the
   pitcher-level caveat noted above.
3. **NEW hypothesis `mlb-classic-2026-06-10-pivot-budget-small-field-se`** —
   small-field SE wants near-field ownership with ONE structural pivot;
   winners ran ~4–5 sub-10% plays, the build ran 8.
4. **NEW hypothesis `mlb-classic-2026-06-10-salary-enabler-pitcher-chalk`** —
   salary-driven cheap-P2 chalk (May) is an enabler, not a trap; discriminate
   chalk arms by workload/leash (Teng), not ownership.
5. **NEW hypothesis `mlb-classic-2026-06-10-blank-own-snapshot-artifact`** —
   blank vendor Own fields surface as fake 0.0%-own leverage in the
   auto-snapshot; verify the leverage table against article ownership (caught
   pre-lock this slate; candidate for an app-side fix).
6. **NEW hypothesis `mlb-classic-2026-06-10-untracked-entry-bypasses-loop`** —
   every DK entry must exist in `data/lineups/<slug>.md` before lock; the $5k
   entry bypassed the entire loop.

No promotions (nothing has 3 mechanism confirmations) and no retirement
candidates (nothing has 2 contradictions).

## Venue file changes

Created **`rules/mlb_classic/parks/coors_field.md`** (no park file existed —
the pre-flight stub step was skipped pre-lock). Includes the physical profile
from this slate's articles and a 2026-06-10 per-slate observation: the Coors
favorite (CHC, ~90% combined own at 6.80 implied) underpaid its ownership while
the overlooked COL home side carried winning lineups (Goodman 22.0 @ 8.6%,
Castro 11.0 @ 4.3%, Tovar in three $5k top-10s) — Coors leverage lives on the
unowned side of the game.

## Proposed codifications

None this slate. Nothing meets the 3-confirmation promotion bar or the
2-contradiction retirement bar — the two codified-lesson confirmations above
are evidence on already-codified rules, and all four new lessons are
single-slate hypotheses.

Tracking notes for future reviews (not proposals): the two codified index
lessons with no possible counter-evidence path (`team-stacking-core-lever`,
`no-hitter-vs-own-pitcher`) are structural facts more than testable lessons;
and `framework.md`'s Construction section is still a stub — once
`pivot-budget-small-field-se` and `salary-enabler-pitcher-chalk` accumulate
confirmations, they are the natural first entries for it.
