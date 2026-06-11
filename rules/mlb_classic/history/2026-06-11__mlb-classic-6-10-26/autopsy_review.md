# Post-autopsy review — MLB Classic 6.10.26

_Reviewed 2026-06-11 (chat session, with the user's account of the lock-time swap).
Results: $6K Base Hit rank 236/588 (top 40.1%), $4K SE rank 203/392 (top 51.8%).
Best-percentile trend: 39.9% (6/9) → 40.1% (6/10) — flat._

## Process scorecard

**The build process was the best of the young MLB sample — and none of it was
entered.** Per the user: the build landed 18:49 ET against a 19:07 lock after a
long spinner; with no time to review, both DK entries were swapped to untracked
SaberSim imports. Everything below grades the two halves separately.

**Pre-lock process (slate_analysis.md + lineups.md): A-.**
- Both pre-flight checklists present, specific, and honest on audit — file dates,
  calibration caveats (own corr 0.819 trusted, proj corr 0.261 not), and the 6/9
  stale-article trap all called correctly.
- All 4 open lessons genuinely applied, not checkbox-applied: pivot-budget shaped
  L2 (chalk frame + ONE pivot, 5 sub-10%), salary-enabler kept Detmers and dodged
  the Scherzer leash-trap (Scherzer: 0.7 pts — the trap call was right two slates
  running), blank-own artifact caught again (Nicky Lopez row discarded), and
  Anchor-Equivalence discharged at both the stack level (PHI/HOU vs the 77–92%
  cluster) and the pitcher level (Lambert as within-class alternative).
- The analysis's central read — "weather is the slate's hidden axis and the field
  isn't pricing it"; PHI dome stack = "best risk-adjusted pivot on the slate" —
  was exactly the winning axis in both contests. L2 shared 6 of 10 players with
  the $4K winner and the full winning skeleton (PHI-5 + Luzardo + Detmers).
- Honest-flag discipline: the portfolio audit voluntarily flagged Luzardo 3-for-3
  exposure with a mechanism justification. That's the audit working as intended.
- The one pre-lock miss: **no red team was run** (manifest lists red_team.md as
  missing). With 18 minutes of clock, there was no time — see below.

**Lock-time execution: F, and it's the whole story of the slate.**
- The lineups.md checklist explicitly applied `untracked-entry-bypasses-loop`
  ("whichever lineups are entered must come from this file") — and then both
  entries came from outside the file. The lesson was applied on paper and
  violated in execution, the exact failure mode it describes, second slate
  running.
- The swap didn't just lose the PHI pivot. The $6K SaberSim entry ran a **TEX
  5-stack** (Duran/Jung/Langford/Pederson/Seager) — the precise stack the
  analysis flagged as "the chalk to be underweight" (82% owned, 41%-rain game,
  zero exposure across the built portfolio). The $4K entry ran the ATH/MIL heat
  game (Turang 0.0, Bauers 0.0). Both entries were chalkier than the winning
  band (21.3%/21.4% avg own, 1 and 4 sub-10% plays vs winners' 15.4–16.0% and
  ~5) and finished 40th/52nd percentile.
- Root cause is process, not discipline: the build arriving 18 minutes before
  lock left no time for the red team or even a read-through, so the portfolio's
  trust collapsed exactly when it couldn't be rebuilt. Tracked as the new
  `late-build-bailout` hypothesis. The fix is scheduling (build ≥60–90 min
  before lock), plus a default rule: a late build that passed its audit gets
  ENTERED, not replaced by lineups that bypassed every check.

**Red team verdict adherence: N/A** — no red_team.md in the archive. Worth noting:
this is the second consecutive slate without one, and both slates' failures
(over-pivoting on 6/9, the bailout on 6/10) are exactly what a red-team pass is
designed to catch or pre-empt.

## Lesson ledger changes

_Applied to `rules/mlb_classic/lessons.yaml` during this session (user-directed:
"log whatever lessons you think will help us")._

**Confirmations added (status hypothesis → validated):**
- `pivot-budget-small-field-se` — winners again near-field + one pivot (15.4%/16.0%
  avg own, ~5 sub-10% plays); the pivot was the PHI stack. 2 of 3 slates needed
  for codification.
- `salary-enabler-pitcher-chalk` — Detmers kept per the lesson, 31.15 pts at 68.7%
  own; winners all ran the chalk arm pair and spent savings on PHI bats. 2 of 3.
- `untracked-entry-bypasses-loop` — second straight slate of untracked entries;
  this time the abandoned tracked build held the winning skeleton. 2 of 3.

**New hypotheses born:**
- `se-chalk-pitcher-own-condensation` — Detmers 38.0% projected → 68.7% actual;
  P1 fade math must assume condensation in small SE fields.
- `weather-proof-dome-stack-pivot` — rain-heavy slate + underowned dome stack =
  the structural pivot; PHI won both contests from 4.80 implied at ~27% combined own.
- `late-build-bailout` (process) — builds landing <30 min before lock collapse
  trust when nothing can be re-checked; default to entering the audited portfolio.

**Deliberately NOT logged:** L3's HOU strike busting (Detmers smashed, HOU bats
died) is not a contradiction of anything — it was a sized binary and the GPP
guard applies. No contradiction entries this slate.

## Venue file changes

- **Created `rules/mlb_classic/parks/rogers_centre.md`** (UNVERIFIED profile) —
  the slate's defining venue: closed roof = the only guaranteed 27 outs on a
  three-rain-game slate; the field left it unowned at 4.80 implied and it won
  both contests.
- **Updated `coors_field.md`** — Coors was supporting cast (CHC/COL pieces only as
  1–2 man fills in winners; Carrigg 14.2% the repeatable cheap one-off); CHC
  favorite-side ownership (76.9%) failed to pay a second straight slate.
- **Updated `las_vegas_ballpark.md`** — the 14.7 heat total did not decide the
  slate; MIL busted outright (Turang 0.0 again), ATH paid only as fills. First
  evidence the heat-total hype is an ownership tax, not a scoring guarantee.

## Proposed codifications

None this slate. Three lessons are now at 2 of 3 confirming slates
(`pivot-budget-small-field-se`, `salary-enabler-pitcher-chalk`,
`untracked-entry-bypasses-loop`) — one more mechanism confirmation each and the
review should write the exact framework.md edit for user approval. No retirement
candidates (no lesson has a mechanism contradiction).

One non-framework process recommendation, no approval needed: start the
Analyze → Build sequence at least 60–90 minutes before lock so a red-team pass
fits inside the clock. Two slates, two failure modes a red team addresses.
