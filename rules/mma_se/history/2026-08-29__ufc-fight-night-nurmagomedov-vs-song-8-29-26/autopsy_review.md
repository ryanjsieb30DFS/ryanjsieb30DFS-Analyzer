# Post-autopsy review — UFC Fight Night: Nurmagomedov vs. Song (8/29/26)

## What happened
This section says in plain words how the slate went.

1. You played two single-entry contests and finished 231st of 392 and 252nd of 713 — beating 41% of the first field and 65% of the second.
2. Your lineups scored 339.10 and 392.29 points; the two winners scored 649.47 and 631.88.
3. The 392-entry winner, homanga, played Denise Gomes, Rei Tsuruya, Sean Woodson, Cam Nelson, Francesco Nuzzi and Liu Ce — six fighters who all won.
4. One man decided your slate: Umar Nurmagomedov, $9,500, the board's highest projection at 99.4 points, owned by 56% of the field, scored 15.74.
5. He was in both your lineups, and he was the field's biggest trap — 72% of the bottom-half entries had him and none of the 392-field winners did.
6. The two cheap fighters who actually won both contests were Francesco Nuzzi ($7,600, 25% owned, 129.66 points) and Denise Gomes ($7,700, 47% owned, 107.60) — and your own strategy told you to use Nuzzi less than the crowd.

## Process scorecard
This section grades HOW you played the slate — the decisions, not the results.

**The prep was done properly.** Anchor-Equivalence (two similar anchors the field treats as the same bet) led `## Edges & tensions` with Hasan $9,600 / Tsuruya $9,700 / Asakura $9,400 at nearly identical projections. The full-pool leverage screen ran and paid: Hector Santiago ($7,100, named as the sneaky target at 16% projected) scored 92.61 at 11.7% real ownership and you had him in both lineups. Keep doing exactly this.

**The one codified rule you broke is the one that cost the slate.** Your framework says a fight going to a decision is NOT the same as a low ceiling. The strategy still wrote Francesco Nuzzi as UNDERWEIGHT because he was "+325 to finish ... points to a low-scoring decision" — a pure finish-price ceiling cap, the exact form the rule bans. Nuzzi scored 129.66, the day's biggest beat on projection (+80.17), and sat in BOTH winning lineups. That is the fifth slate running this cap has been wrong on a winner-defining fighter. Next slate: any fade written on finish odds alone must also show low projected volume and low projected control, or it does not get written.

**Your board's top tier just copied the crowd.** The player pool named exactly two `Core` fighters and they were the board's #1 and #3 most-owned: Umar (45% projected) and Liu Ce (38%). `Core` averaged 74.8 points against `Good`'s 78.6, so the tiers came out in the wrong order for the sixth graded slate straight. Worse, across the twelve slots in the two winning rosters, ONE was `Core`, three `Good`, six `Okay` and two `Fade` — your bottom two tiers held two-thirds of the winning slots. Next slate: a fighter already projected top-3 in ownership only gets `Core` if you can name an edge the crowd is not already paying for.

**You broke the right pair on the wrong side.** The strategy correctly flagged Umar + Liu Ce as the field's top duplicated pair and said a sharp refuses both. You did break it — but you kept Umar (56% owned) and dropped Liu Ce (38% owned). Splitting a pair only buys separation if you keep the LIGHTER half. Next slate: the strategy must say which half to drop, and the default is the more-owned one.

**Discipline was clean, and the metric that says so is broken.** `adherence.json` reports zero fade violations for the seventh slate running and 0 of 2 low-owned candidates rostered — both of those (Rojas 7%, Borjas 7%) were knockout-or-nothing darts your board tiered `Fade`, and neither winner carried any sub-10% fighter. Separately, all three UNDERWEIGHT calls threw per-contest flags, which is arithmetic, not indiscipline: "less than the crowd, never zero" cannot be expressed in a one-bullet contest, where the only options are 0% and 100%.

**The pool had the winner; the picking missed it.** The Sim's 7,500-lineup pool topped out at 699.33 points, above both winning scores, so generation was fine both times. In the 392 field 56% of the pool beat your entry and the pick came in 18.59 points UNDER the pool average; in the 713 field the pick beat the pool average by 34.60. The sim's pre-lock rankings did carry real signal this slate — the top 100 lineups by ROI averaged 444.58 actual points against a pool average of 357.69 — but only weakly (correlations 0.067 to 0.240).

**No pro was in either field.** `shark_gap.json` returns no tracked handles at all, so there is no you-versus-the-pros gap to name — the fourth such slate in seven. The substitute measurement says the same thing: your average ownership per roster spot was 25.93 and 28.38 against winners at 30.31 and 25.53. Your structure was fine. The whole gap was which fighters.

## Lesson ledger changes
One line per lesson touched.

- `distance-fight-is-not-low-ceiling` — 5th confirmation: Nuzzi's finish-price cap was wrong by 80 points and he was in both winners.
- `fade-on-structure-not-narrative` — confirmation with a boundary: the Woodson and Jenkins calls held, the pure finish-price Nuzzi call broke, but Su Sumudaerji's finish-price call was right (55.6), so the carve-out is a warning, not a predictor.
- `winning-se-shape-six-winners-mid-own-converters` — 7th confirmation: both winners were six winning fighters at 25-30% own with zero darts; your structure matched and only the names differed.
- `core-tier-mirrors-the-field-chalk` — 1st confirmation, promoted to **validated**: Core was the board's two most-owned names and averaged below `Good`.
- `okay-tier-is-a-dumping-ground` — 5th confirmation: `Okay` back up to 12 of 26 fighters (46%) and it held Nuzzi, Gomes and Song.
- `grade-gates-have-no-discriminating-power-in-mma` — 4th confirmation, ~122 clean lineups running, plus a correction: the proposed no-win-path gate would not have fired here either.
- `sharp-envelope-is-a-rate-not-a-per-bullet-quota` — 6th confirmation: no pro in field, and the strategy still cited moklovin as the target.
- `projected-own-understates-consensus-chalk-convergence` — 1st test of the narrowed form and it held: Gomes ($7,700, 31% projected) ran +16, from the right salary band; the strategy named Liu Ce instead.
- `leverage-is-the-low-own-finisher-not-the-named-dog` — 6th confirmation: Santiago and Song converted, Rojas and Borjas died.
- `sim-rankings-are-a-threshold-not-an-ordering` — 2nd contradiction: signal was positive again, so retirement is proposed below.
- `the-single-bullet-gets-the-least-disciplined-build` — 2nd confirmation: both bullets were picks entered unmodified with no rule-broken slot.
- `duplicate-pick-across-contests-forces-hand-edits` — 2nd confirmation: two distinct picks, no forced hand-editing.
- `salary-buys-floor-not-ceiling` — 5th confirmation: points per $1,000 fell with price again (Nuzzi 17.06, Liu Ce 15.39, Tsuruya 13.31, Hasan 11.32).
- **New** `break-a-chalk-pair-by-dropping-the-chalkier-half`, `underweight-has-no-meaning-in-a-single-entry-contest`, `owned-ahead-of-projection-is-not-a-trap-signal` — all born as ideas still being tested (hypotheses).

## Venue file changes
None, and none is correct. MMA is the one sport with no venue directory (`CLAUDE.md` — venue files exist only for NASCAR tracks and PGA courses), because UFC cards change city and change every fighter each week, so nothing about Shanghai transfers to next Saturday. No file was created.

## Ledger hygiene
One line per maintenance decision.

- **KEEP** `confirmed-vs-speculative-news` — untested for 11 slates only because no late injury-news swap has come up; no relevant slate is not evidence.
- **KEEP** `showdown-captain-the-ceiling-pair-the-smash` — showdown-only, and no MMA showdown card has run since it absorbed two merges on 8/28.
- **KEEP** `shared-coin-flip-slots-not-shared-players-kill-a-portfolio` — needs a multi-entry portfolio to test, and the last two slates were single-entry only.
- **KEEP-SEPARATE, all 44 merge pairs** — every flag is a deliberate `[[id]]` cross-link, which is how this ledger records that two rules touch the same event; none is a duplicate statement. Two to watch if they drift closer: `secondary-plays-are-not-leverage` versus `finish-capable-favorite-is-not-secondary-chalk` (one defines leverage, the other carves an exemption out of it), and `okay-tier-is-a-dumping-ground` versus `core-tier-mirrors-the-field-chalk` (different tiers, different fixes — keep both until the fixes converge).
- No lesson references a removed feature, so nothing is retired on those grounds.

## Proposed codifications
These are proposals only. Nothing below is applied until you approve it.

1. **Codify** `the-single-bullet-gets-the-least-disciplined-build` (3 slates: 8/9, 8/23, 8/29). Add to `framework.md`: *"Pick the single-entry bullet from the Sim pool's contest slice; never hand-assemble it and never hand-swap a slot after the pick. Two slates of picked-and-unmodified bullets produced the best and the cleanest builds in the ledger; the hand-built 8/9 bullet was the worst."*
2. **Codify** `duplicate-pick-across-contests-forces-hand-edits` (3 slates: 8/16, 8/23, 8/29). Add to `framework.md`: *"One lineup, one contest. If a pick is displaced from a contest, RE-RUN the pick for that contest — never repair it by swapping slots by hand."*
3. **Codify** `salary-buys-floor-not-ceiling` (overdue — 5 confirming slates). Add to `framework.md#salary-buys-floor-not-ceiling`: *"Every $9,000+ slot needs a stated FINISH path, not just a win path. Buy win probability from the $7,500–8,999 band. The most expensive fighter with the highest projection is the crowd's probability buy, not your ceiling buy."*
4. **Retire** `sim-rankings-are-a-threshold-not-an-ordering` (2 mechanism contradictions: 8/23, 8/29). Retired reason: *"the metrics carry no ordering information" is contradicted twice — signal was 0.271–0.322 on 8/23 and 0.067–0.240 on 8/29.* Carry the surviving half forward as a new hypothesis: the ordering signal appears to scale with how widely the card's scores spread out, and a weak correlation across 7,500 lineups still says little about any single row (the 392 pick ranked well and finished 18.59 points below pool average).
5. **Not yet** `showdown-cap-single-favorite-exposure` (flagged overdue at 4 slates). Its own 8/2 and 8/23 notes deliberately do not count two of those, so it stands at 2 of 3 and still needs an independent slate where an over-exposed BINARY favourite sinks a block. No edit proposed.

## What this means for next slate
1. Never write a fade or an underweight because a fight is likely to go the distance — check volume and control first, or do not write it.
2. The most-projected, most-owned fighter is not automatically `Core`; he needs an edge the crowd is not already paying for.
3. When you break a duplicated pair, drop the MORE-owned half, not the cheaper one.
4. On a one-bullet contest, write soft calls as LEAN FADE or PLAY — UNDERWEIGHT cannot be obeyed with a single lineup.
5. Keep picking bullets straight from the Sim pool and entering them untouched; that part of the process is working.

## Applied
Approved by the user on 2026-08-29 and applied. This is what changed on disk.

- `framework.md` — new section **"Pick the Single-Entry Bullet, Never Hand-Build It (8/29/26 — 3-slate validated)"**, added exactly as proposed. Lesson `mma-se-2026-08-09-the-single-bullet-gets-the-least-disciplined-build` → **codified**, `codified_in` naming that section.
- `framework.md` — new section **"One Lineup, One Contest — Re-Run, Never Repair (8/29/26 — 3-slate validated)"**, added exactly as proposed. Lesson `mma-se-2026-08-16-duplicate-pick-across-contests-forces-hand-edits` → **codified**, `codified_in` naming that section.
- `framework.md` — closing **"Codified 8/29/26 (5 confirming slates)"** paragraph added to *Salary Buys Floor, Not Ceiling*: $9,000+ slots need a stated finish path, buy win probability from $7,500–8,999, and the most expensive fighter with the highest projection is the crowd's probability buy. Lesson `mma-se-2026-08-23-salary-buys-floor-not-ceiling` → **codified**, `codified_in` pointing at that paragraph.
- `lessons.yaml` — `mma-se-2026-08-16-sim-rankings-are-a-threshold-not-an-ordering` → **retired**, with the approved reason (two mechanism contradictions: 0.271–0.322 on 8/23, 0.067–0.240 on 8/29).
- `lessons.yaml` — the surviving half carried forward as a NEW hypothesis, `mma-se-2026-08-29-sim-ordering-scales-with-score-dispersion`: the ordering signal appears to scale with the card's score dispersion, and a weak correlation across thousands of lineups still says little about any single row (the 392 pick ranked well and finished 18.59 points under the pool average).
- `framework.md` header date moved to August 29, 2026.
- **Not applied, as proposed:** `showdown-cap-single-favorite-exposure` stays `validated` at 2 of 3 — no edit was proposed for it.
- **Ledger hygiene:** every decision was KEEP or KEEP-SEPARATE, so no lesson was retired or merged on hygiene grounds. `confirmed-vs-speculative-news`, `showdown-captain-the-ceiling-pair-the-smash`, `shared-coin-flip-slots-not-shared-players-kill-a-portfolio` and all 44 merge pairs are untouched.
- `philosophy.md` — no changes proposed, none made.
