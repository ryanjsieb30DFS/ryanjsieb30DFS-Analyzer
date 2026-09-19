# Post-autopsy review — NFL Showdown, Broncos at Chiefs (MNF), 9/14/26

## What happened

This section says how the night went, in plain words.

1. You entered five lineups in the $200K Flea Flicker (47,562 entries, up to 150 per player) and your best finished 120th, beating 99.7% of the field.
2. First place was an 84-way tie at 124.61 points, and every one of those 84 lineups was the same six: captain Kenneth Walker III ($15,900 as captain, 37.1 points, 55.65 as captain), Patrick Mahomes, Rashee Rice, Travis Kelce, the Chiefs defense and Evan Engram.
3. Your 120th-place entry was those same six except Pat Bryant ($3,200, 8.2 points) in place of Engram ($3,400, 14.3 points), a gap of exactly 6.1 points.
4. The two pieces that decided the slate were cheap and mid-owned: Engram (14.3 points, owned by 18% of entries, in 100% of the top lineups) and the Chiefs defense ($4,400, 12.0 points, 14%, in 92% of them).
5. Your other four entries finished between 27,626th and 43,867th because all four carried Bo Nix (7.4 points, the most-owned player at 74%), and three carried Jaylen Waddle (1.2 points, 45% owned).
6. The 84 winners split places 1 through 84 for about $1,240 each instead of $50,000, which is the duplication problem in one number.

## Process scorecard

This section grades HOW you played the slate, the decisions and not the results.

**The build rule blocked the winning six (grade: D, second slate running).** The winner cost $49,700. The strategy's machine-readable rule said no lineup over $49,500, taken from "the median winner leaves $1,400 unspent." The Sim's 10,000-lineup pool, built under that rule, topped out at 121.41, and your best entry was the winning six with the $200-cheaper filler swapped in. On 9/14 the same rule blocked the 4th-place build at $49,800. Next slate: state salary-left as a portfolio rate ("most entries under $49,500"), never a per-lineup ceiling.

**The cheap-spot call went with the crowd (grade: C).** The strategy marked Engram UNDERWEIGHT ("Bryant is $200 cheaper and projects higher") even though Engram (17.5% projected) was already the less-owned Denver filler and Bryant (22.9%) was the crowd's pick. That is an ownership call made on a 0.5-point projection gap, and it pointed the cheap spot at the copied filler. Next slate: between two same-price fillers, the LESS-owned one is the one to keep, or it is not a leverage call.

**The twin call flipped by lock (grade: C).** The two quarterbacks were named substitutes (anchor-equivalence, the mandatory check, was surfaced), and the strategy leaned to Nix as the less-owned twin on ETR's 64.3% versus Mahomes' 69.7%. At lock Nix was 74.4% and Mahomes 66.8%, so your 4-of-5 Nix exposure (80%) was heavier than the crowd's. Nix scoring 7.4 is variance, not the point. Next slate: check the ownership drift panel before entering, and measure "less owned" on the lock sheet.

**Whether your entries followed your own plan (adherence): clean (grade: A).** Xavier Worthy (LEAN FADE) was in zero entries and scored 4.8. Butker, the Broncos defense and Engram were 1 of 5 each. Mahomes at 3 of 5 (60%) sits exactly at the strategy's own 60% cap; the tool flags it on a fixed 50% line, the tool contradicting the rule block again, not a miss. The strategy named 12 low-owned players who could decide the slate and you carried none, the third slate running (0, 1, 0 of 12). This slate that cost nothing: the top 1% of the field carried 0% sub-5% pieces, the bottom half 17%. Next slate: the dart is a rate set per field size, not a reflex.

**The 45%-ownership target was applied and held (grade: A).** The 9/14 lesson set the target at 35–45% per roster spot instead of 28%; the top 1% of this field averaged 40.9%, the winner 39.3%, your set 41.65%. Winners separated by the captain tag and one mid-priced piece, not by fading stars. Keep this.

**Captain menu (grade: B).** The strategy wanted a sub-6% pass-catcher captain (Kelce 5.4%, Sutton 5.1%, Dobbins 5.7%); they scored 10.1, 3.1 and 3.6 as regular players. The winner captained Walker, the crowd's #1 captain at 16.3%, and so did your 5-1 Chiefs entry, the "Chiefs-control script" line. Both quarterbacks sat under the 20% captain base rate and were left off the menu (the 9/10 lesson was not applied); it cost nothing, since a Mahomes captain tops out near your 120th-place score. Next slate: run the quarterback base-rate check even when the QB is chalk.

**The board's tiers held (grade: B).** Core averaged 13.9 points, Good 9.5, Okay 3.9, Fade 1.1, in order. But both slate-deciders sat in Okay (Engram rank 18, Chiefs defense rank 13) while Waddle sat at rank 2 as Core · Leverage and scored 1.2 (62% of the bottom half had him, 5% of the top 1%). Next slate: a "cheaper twin that projects higher" (the Chiefs D over the Broncos D) belongs in Good.

**You versus the tracked pros:** no shark head-to-head file was written this slate. None of the named pros were found in this 47,562-entry field, so there is no gap to name and no recurring axis to check.

**Was the miss in building or in picking?** Building. The pool never held a 124.61 lineup (its best real score was 121.41), and the salary rule above is the likeliest reason. Picking was fine: only 3 of 10,000 pool rows beat your best entry, and your five averaged 68.9 against the pool's 69.9. No Claude pick was made, so there is no table to check. Sim signal watch: the sim's chance-to-finish-first number has predicted real scores less each slate (0.19, 0.145, 0.101, where 1.0 is perfect and 0 is none) while its cash chance led on two of three. Not a lesson yet.

**Codified rule check:** "a 3-3 build must name its story" was applied (five entries, five named scripts) and its reason held: the game tipped to the Chiefs and the winner was 5-1 Chiefs. Your one 3-3 beat 42% of the field; your 5-1 beat 99.7%.

## Lesson ledger changes

This section lists each lesson this slate touched.

- **nfl_sd_sub5_cpt_leak → validated, third confirmation.** Winning captain Walker at 16.3% projected captain ownership, inside the 5–25% band; 3 of 3 winners now.
- **nfl_sd_six_skill_default — second confirmation (3 confirming slates, 1 contradiction).** Chiefs DST 12.0, the best piece priced $4,000–$5,200, in all 84 winning lineups.
- **nfl_sd_kicker_conditional — contradiction logged.** Close spread, under-owned underdog kicker Lutz (21.9% vs Butker 27.1%) scored 4.0 to Butker's 7.0 and sat in 0% of the top 1%.
- **nfl_sd_winner_envelope_45_per_slot → validated.** Top 1% at 40.9% per spot, winner 39.3%, in a 47k field; scope widening proposed.
- **nfl_sd_three_three_default (codified) — applied, reason held.** Winner 5-1 Chiefs.
- **nfl_sd_qb_cpt_under_base_rate — not applied, untested.** Both QBs under 20% captain and off the menu; cost nothing.
- **nfl_sd_punt_slot_role_path — not counted.** Emmett Johnson ($2,600, 5.4%) scored 8.8 over a 7.9 ceiling, but the winner carried no sub-$2,500 piece and Bryant beat his projection.
- **nfl_sd_cheap_side_catchers, nfl_sd_qb_catcher_captain, nfl_sd_underweight_across_entries, nfl_sd_pick_override_inside_band, nfl_sd_dupe_over_sim — did not trigger / untested** (notes added).
- **NEW nfl_sd_salary_left_is_a_rate (validated: 9/14 + 9/15).** A $49,500 lineup ceiling deleted the $49,700 winner and the 9/14 $49,800 4th-place build.
- **NEW nfl_sd_twin_drift_to_consensus (hypothesis).** The projected less-owned twin (Nix 64.3%) closed as the most-owned player (74.4%).

## Venue file changes

This section is about the stadium file. NFL Showdown has no venue file, so nothing was written.

## Ledger hygiene

This section records one decision per flagged lesson.

- **nfl_sd_dupe_over_sim — RETIRE (proposed).** Its test needs sim ROI for the field's top finishers, which no archive can hold, so it has been untestable three slates running; its content already lives in framework.md's Duplication section.
- **nfl_sd_six_skill_default — PROMOTE (proposed, as a rate).** Third confirming slate reached (Chiefs DST 12.0 in every winning copy) against one contradiction (9/14, every K/DST busted); the edit below says both.
- **nfl_sd_qb_cpt_under_base_rate — KEEP.** Not applied this slate, so not tested; a third slate must show a QB under the 20% captain base rate on the menu who wins or lands top-10 at or above his share.
- **nfl_sd_sub5_cpt_leak — PROMOTE (proposed).** Three logged winners in the 5–25% band: Purdy 6.7%, Dart 18.8%, Walker 16.3%.
- **nfl_sd_kicker_conditional — KEEP, NARROW (proposed).** Outdoor close-spread underdog kickers are 0 for 2 (Zvada 4.0, Lutz 4.0); the only confirmation was a roofed stadium.
- No merge pairs were flagged; no lesson references a removed feature.

## Proposed codifications

This section lists rule changes for you to approve; nothing here is applied yet.

**1. Codify nfl_sd_sub5_cpt_leak.** In `rules/nfl_sd/framework.md`, "The captain decision", replace the line beginning "**Captain ownership lives in the 5–25% band.**" with:
"**Captain ownership lives in the 5–25% band (codified 9/15/26).** All three logged winners captained inside it: Purdy 6.7% (9/10), Dart 18.8% (9/13), Walker 16.3% (9/14). Sub-5% captains filled top-10 spots on two of those slates (Deebo, Likely 41.7 CPT) and won none; the sub-5% captain chosen for ownership alone is the documented single-entry leak. Low ownership is a tiebreaker, never the thesis."

**2. Codify nfl_sd_six_skill_default as a rate.** In "Pre-lock checks", replace "Is any lineup six skill players with no K and no DST, and is that deliberate?" with:
"**Six skill players with no K and no DST is a choice, not a default (codified 9/15/26).** On 2 of 3 logged slates the top lineups carried a K or DST more often than the user's entries (9/10: 6 of 10 per contest, Pineiro 11.0; 9/14: all 84 winning copies, Chiefs DST 12.0); on the third (9/13) every K and DST busted. A rate across the set, never a per-lineup quota."

**3. Retire nfl_sd_dupe_over_sim.** Set `status: retired`, `retired_reason: "Untestable: the archive never holds sim ROI for the field's top finishers (3 slates). Content already codified in framework.md Duplication (a 15% sim-ROI lineup with 2 dupes beats a 20% lineup with 10)."` No framework edit.

**4. Narrow nfl_sd_kicker_conditional.** New statement: "The kicker edge exists in DOME games and when the vendor sheet shows the kicker under-owned; the outdoor close-spread underdog kicker is NOT an edge (0 for 2: Zvada 4.0, Lutz 4.0; the one confirmation, Pineiro 11.0, was a roofed stadium)." In framework.md "Game scripts", after the **close spreads** kicker clause add: "— unconfirmed outdoors on this repo's slates (0 for 2)."

**5. Salary-left (new lesson, 2 slates, not yet promotable).** No framework edit yet; flagged so the next strategy writes salary-left as a portfolio rate, not a `salary_max` lineup rule.

## What this means for next slate

This section is the short list to carry forward.

1. Never write "leave $500" as a per-lineup rule; say "most entries under $49,500" so the near-max chalk build can exist.
2. When two cheap fillers are a coin flip on projection, keep the LESS-owned one; do not call the less-owned one the underweight.
3. Check the ownership drift panel before lock and measure the twin call on the lock sheet, not the morning sheet.
4. Keep the 35–45% per-spot target and the five named scripts; both held.
5. Run the quarterback captain check against the 20% base rate every slate, even when the QB is chalk.
