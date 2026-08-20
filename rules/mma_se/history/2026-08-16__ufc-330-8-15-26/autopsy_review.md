# Post-autopsy review — UFC 330 8.15.26 (logged 2026-08-16)

## What happened

This section says how the slate went, in plain words.

1. You entered five lineups across three contests for $29; your best beat 88.2% of its field (rank 105 of 891 in the 3-Max).
2. Your two one-entry contests finished top 30% (rank 353 of 1,176) and bottom third (rank 1,612 of 2,378).
3. Both one-entry contests were won by the same six fighters scoring 623.24: Makhachev ($9,200, 117.5), Dern ($9,000, 106.84), Turner ($8,600, 128.75 — the slate's top score), Donte Johnson ($8,800, 104.4), Njokuani ($7,300, 93.16, on only about 7 of 100 teams), and Charles Johnson ($6,900, 72.59).
4. The 3-Max winner (629.11) swapped in Stoltzfus ($6,700, 106.26, on about 5 of 100 teams) — a low-owned decider your strategy named but no entry carried.
5. The crowd's heaviest picks mostly failed: Fernandes (46.6% of the big field) scored 0.8, and Orolbai (57% owned, your board's #1 Core) scored just 50.0.
6. Winners ran six fighters who all won plus one low-owned winner; your entries carried losing mid-priced picks instead — Brahimaj 26.95, Alvarez 30.78, Luque 20.52.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**The written strategy was mostly right, but its #1 ranking was the big miss.** The Fernandes trap call (use him less than the crowd) was exactly right — he scored 0.8 at 46.6% owned, and only 1 of your 5 entries had him. The Charles Johnson call was half right: his 72.59 was the lowest score in the winning lineup, but every winner still used him as the salary saver. The real miss was Orolbai as the board's #1 Core: the most-picked fighter in the big field (57%) scored 50.0 and appeared in almost no winning lineups. Next slate: when both articles and the projections crown the same lock, check his points-per-dollar against the tier below before ranking him #1.

**The board buried the deciders in the middle tier again.** Turner (128.75, the slate's top score), Donte Johnson (104.4) and Charles Johnson (72.59) — all in every winning lineup — sat in `Okay`, a bucket holding 15 of 24 fighters (63%). `Okay` averaged 63.6 while `Good` averaged 47.9, so tier order broke for the fourth straight slate. This is the third slate confirming the "Okay tier is a dumping ground" idea — it goes to promotion below.

**Two of your five fade-section calls silently vanished from every tool.** The strategy wrote "C. Johnson — UNDERWEIGHT" and "D. Johnson — UNDERWEIGHT" with shortened names; the contract parser matched neither (two Johnsons on the slate), so the pick gate and the plan-following grade (adherence) tracked only 3 of 5 calls. Donte Johnson then sat in every winning lineup, ungraded. Fix: write full names in `## Fades` and `## Leverage`, always.

**The pros beat you on picks, not structure — again.** The one tracked pro in the big field ran 37.8% average ownership per roster spot to your 38.8, same anchors, same zero darts — yet finished 22.7%ile to your 67.8%ile. Fourth straight slate where the structural gap was ≤1.3 ownership points and the whole difference was WHICH fighters.

**Discipline (following your own plan) was clean; the leverage list went 0-for-3.** No fade was violated. Fernandes-at-zero in both one-entry contests was flagged, but he scored 0.8 — and note the tools disagree: the pick gate FORCES zero underweight exposure in one-entry picks while the adherence checker flags that same zero. None of your entries carried Wells, Stoltzfus, or Barboza (the three named sub-10% plays), and Stoltzfus decided the 3-Max. The trend reads 0/2, 0/2, 1/1, 2/2, 0/3 — the dart is optional by rule, but 106 points at 5% owned is why the option exists.

**The Sim pool was good; the pick engine was fine; the hand edit was the leak.** The pool's best lineup (647.24) beat both winning scores, so generation was not the problem. Untouched picks beat the pool average by +26.9 ($12K) and +44.2 (3-Max) points. But the same pool lineup (#2209) got saved as the pick for ALL THREE contests — the one-lineup-one-contest guard should have blocked that — so you hand-swapped for the Clinch: Turner→Orolbai and Alvarez→Luque cost 89.0 points and that entry ran 62.1 points BELOW the pool average. Meanwhile all four sim ranking numbers predicted the real scores at basically zero (correlations 0.002 to −0.025) for the second straight slate: treat the sim as a filter, not a ranking. Next slate: if the same lineup appears picked twice, re-run the pick — never hand-swap slots.

## Lesson ledger changes

This section lists each lesson touched, one line each.

- `winning-se-shape-six-winners-mid-own-converters` — 5th confirmation: all three winners were six winning fighters plus one low-owned CONVERTER (Njokuani 7%, Stoltzfus 5%).
- `projected-own-understates-consensus-chalk-convergence` — confirmation with boundary: favorites converged up (Orolbai +17, C. Johnson +15), the projected #1 Makhachev only +4-5.
- `exact-roster-duplication-is-superlinear-in-consensus` — 2nd confirmation: the $12K winning roster was entered 3× (naive estimate 0.46), first prize split three ways; now 3 slates.
- `okay-tier-is-a-dumping-ground` — 3rd confirmation (Turner/D. Johnson/C. Johnson all buried); promotion proposed.
- `grade-gates-have-no-discriminating-power-in-mma` — 2nd confirmation: zero flags on 5 lineups spanning 11.8–67.8%ile (~115 straight clean); promotion proposed.
- `sharp-envelope-is-a-rate-not-a-per-bullet-quota` — 4th axis-is-noise confirmation (shark delta 1.0 own-point, 45-percentile outcome gap).
- NEW hypotheses: `abbreviated-names-drop-contract-calls`, `duplicate-pick-across-contests-forces-hand-edits`, `sim-rankings-are-a-threshold-not-an-ordering`.

## Venue file changes

This section covers what the slate taught about the place it was held.

MMA keeps no venue files by design (only NASCAR tracks and PGA courses have them), so nothing was created or edited. Venue-adjacent note: a 12-fight title card won on control and volume, not a knockout parade.

## Ledger hygiene

This section records one decision per flagged ledger-maintenance item.

- KEEP `confirmed-vs-speculative-news` — fires only on a lock-window news swap; no logged slate since 5/9 has had one, so it is untested, not wrong.
- KEEP `showdown-trust-cpt-own-not-projected-overall-own` and KEEP `showdown-captain-the-ceiling-pair-the-smash` — both fire only on captain-mode cards; none has run since 6/14.
- PROMOTE `exact-roster-duplication-superlinear`, `okay-tier-is-a-dumping-ground`, `grade-gates-have-no-discriminating-power` — each reached its 3rd confirming slate here (edits below).
- HOLD `field-value-side-vs-your-named-converter` at 2 of 3 — the mechanism never fired: you rostered the named side (Chapolin, 4 of 5 entries), not the field's opposite.
- PROMOTE `sharp-envelope-is-a-rate-not-a-per-bullet-quota` (overdue, 3 slates — edit below); DECLINE promoting `showdown-cap-single-favorite-exposure` — its 8/2 confirmation is marked non-counting (same Cepo event credited elsewhere), so it truly sits at 2 of 3.
- KEEP-SEPARATE all 33 merge pairs as a class — they are deliberate `[[id]]` cross-links between distinct mechanisms, not duplicate statements; the one real duplicate was already merged 8/2.
- No lesson depends on a removed feature; no removed-feature retirements.

## Proposed codifications

This section proposes framework edits; nothing is applied until you approve.

1. **Okay tier** → add to framework.md: "The Okay Tier Is a Verdict, Not a Shrug (8/16/26 — 3-slate validated): cap `Okay` at ~1/3 of the board; every other fighter gets `Good` or `Fade` with a one-line reason; check the tier-order flag each autopsy."
2. **Grade gates** → add to framework.md: "A Clean MMA Grade Carries No Information (8/16/26): ~115 straight flag-free lineups spanning the whole field; rebuild MMA gates on convergence-adjusted ownership and add a no-win-path-slot gate; until then ignore clean grades."
3. **Duplication** → add to framework.md: "Exact-Roster Duplication Is Superlinear (8/16/26): before locking a top-heavy SE, multiply the roster's ownership product × field size × the measured MMA 1.7–6.6× factor; a double-digit copy count is a build-defining flag (the 8/16 $12K winner split first place three ways)."
4. **Sharp envelope** → add to framework.md + philosophy.md: "Envelope Targets Are Rates (8/16/26): state pro targets as 'in N of 10 lineups'; on 1–3 bullets the dart is optional; treat shark-gap axis deltas ≤2 ownership points as noise — the gap is selection."

## What this means for next slate

This section is the short list to carry forward.

1. Write every fade and leverage name in full — shortened names silently vanish from the tools that enforce them.
2. If the same lineup shows up as the pick for two contests, re-run the pick; never hand-swap slots.
3. Keep building six fighters who can all win, and make the one low-owned piece a winner-type — that decided all three contests.
4. Shrink the Okay tier before trusting the board's ranking.
5. Treat sim rankings as a cut line, not an order.
