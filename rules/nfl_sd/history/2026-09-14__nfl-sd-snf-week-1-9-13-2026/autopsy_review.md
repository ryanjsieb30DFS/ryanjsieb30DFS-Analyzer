# Post-autopsy review — NFL Showdown, Cowboys at Giants (SNF), 9/13/26

## What happened

This section says how the night went, in plain words.

1. You entered one lineup in each of two single-entry contests and finished 1,514th of 1,960 in the Dimeback (beat 22.8% of the field) and 689th of 1,902 in the Huddle (beat 63.8%).
2. The same lineup won both contests with 135.2 points: tajohn53 captained Jaxson Dart ($9,600, 26.6 points, 39.9 as captain) and added Dak Prescott, Javonte Williams, Cam Skattebo, Isaiah Likely and Devin Singletary, spending every dollar.
3. The player who decided the slate was tight end Isaiah Likely ($6,400, 27.8 points, the night's top raw score), captained by only about 1 team in 20 (4.95%) yet the captain on 7 of the 10 best Dimeback lineups.
4. The winner's cheap piece was Devin Singletary ($1,400, 13.8 points, 3.2% owned), who sat in 40-45% of the top-20 lineups in both contests.
5. Your Dimeback entry (captain Williams, Dak, Pickens, Skattebo, Zvada, Beckham) got 9.8 points from its last three spots: George Pickens 5.8, Dominic Zvada 4.0, Odell Beckham 0.0.
6. Your Huddle entry (captain Skattebo, Lamb, Dart, Williams, Zvada, Theo Johnson) was the same Giants-side story as the winner but held Johnson (1.9) and Zvada (4.0) where the winner held Likely and Singletary.

## Process scorecard

This section grades HOW you played the slate, the decisions and not the results.

**The fades and the captain check were right (grade: A).** All four fade calls busted: Brandon Aubrey 2.0 at 34% owned, Ryan Flournoy 4.2, Tyrone Tracy 0.4, Giants defense 3.0. The board's tiers held in order (Core 22.1, Good 15.2, Okay 3.2, Fade 0.8). The lesson from last slate was applied: the strategy checked both quarterbacks against the 1-in-5 base rate and put Dart (13.3% projected captain) on the menu, and he won both contests. NFL has no venue file, and the two chalk receivers (anchor-equivalence) were named as one bet. Next slate, keep this exact routine.

**The captain menu missed the quarterback's catcher (grade: C).** The menu was Williams, Lamb or Pickens, Dart, Skattebo, Nabers, Dak. Likely sat in Good at rank 8 with Silva's own line that he "could lead this game in receiving," but his 3.0% captain ownership never became a captain candidate. The framework already says the catcher out-scores the thrower on every completed pass, so a Dart captain at 13% and a Likely captain at 3% are the same bet at a quarter of the ownership. Next slate: whenever a quarterback is on the menu, his top catcher goes on it too if captained under 5%.

**The cheap spot was addressed but not solved (grade: C).** Singletary got one Leverage line ("third Giants back, ceiling 7.7") and rank 23 on the board. He scored 13.8, almost double his printed ceiling, because one short touchdown is 6 points on a 2.7 projection. Your entries filled that slot with Beckham (9.4% owned, 0.0) and Johnson (19.2% owned, 1.9), the crowd's fillers. Next slate: judge the cheapest spot by who has a path to a touchdown, not by the sheet's ceiling.

**Discipline (adherence): clean on fades, empty on leverage (grade: B).** No fade call was broken. The three under-own calls (Aubrey, Flournoy, Tracy) were at zero in both entries, which the tool flags because underweight means "less than the crowd, never zero," but at 2.0, 4.2 and 0.4 points it cost nothing. The strategy named 12 low-owned players who could decide the slate; your entries carried one (Beckham, 0.0) and no piece under 5%, while the winner's Singletary was 3.2%. Next slate: each entry carries one named sub-5% piece with a role path, never the same one in both.

**The ownership target was 15 points too low (grade: D).** The strategy told a sharp to sit near 28-30% ownership per roster spot. The top-20 averaged 47.0% (Dimeback) and 45.6% (Huddle); your entries were 39.4% and 40.0%. On a ~30-player slate where the top five sit at 45-74% each, any lineup with four of them averages ~45%, so the winners were chalkier than you and separated by the captain tag and one cheap dart. Next slate: the target is ~45% per spot with one dart, not 28%.

**You versus the tracked pros (shark gap, Dimeback only):** four tracked pro entries carried a sub-5% piece in 1 of 4 against your 0 of 1, and sat at 42.0% ownership per spot against your 39.4%. Last slate the biggest gap was ownership per spot, so nothing is recurring yet. The pros' best entry beat 28.9% of the field, so the gap cost nothing this time.

**Pool versus picking: the build barely held a winner, and there was no Claude pick to judge.** The Sim's 10,000-lineup pool topped out at 135.8 against the winning 135.2, and exactly 1 row reached the winning score (last slate 11-12). That is a thin build. Both entries were hand-entered, so no table was archived to check. Your Dimeback entry beat 43.3% of the pool; your Huddle entry beat 81.2%. The Dimeback entry has sat below the pool's middle two slates running, both times as the favorite's story while the underdog's story won. Worth watching, not a lesson yet.

**Sim ranking signal:** the sim's cash chance predicted real scores best (0.278 correlation, where 1.0 is perfect and 0 is none) and its chance-to-finish-first read 0.145, after 0.19 last slate. Weak but positive twice is not a calibration lesson yet.

**Open lessons applied vs ignored:** the quarterback-captain lesson was applied and won. The 3-3 warning was half-honored: your 2-4 Huddle entry beat 63.8% of the field, your 3-3 Dimeback entry 22.8%, and the top 3 in both contests were 2-4. The kicker-or-defense idea was obeyed (Zvada in both) and was wrong: 0 of the top 20 lineups carried one. No codified rules exist yet for this sport.

## Lesson ledger changes

This section lists each lesson this slate touched.

- **nfl_sd_qb_cpt_under_base_rate → validated.** Applied and held: Dart at 18.8% captain ownership (under the 20% base rate) won both contests with 39.9 captain points.
- **nfl_sd_three_three_default — second confirmation, now 3 of 3.** Huddle top-10 unbalanced 6 of 10, Dimeback a 5-5 tie, top 3 in both contests 2-4; codification proposed below.
- **nfl_sd_six_skill_default — contradiction logged, stays validated.** 0 of 20 top lineups carried a kicker or defense; all four such pieces scored 4.0 or less.
- **nfl_sd_kicker_conditional — partial, not counted.** Under-owned underdog kicker Zvada (11.8% vs Aubrey's 34.3%) beat Aubrey 4.0 to 2.0 but did not out-score his $4,800 tier.
- **nfl_sd_sub5_cpt_leak — contradiction logged (second).** Sub-5% captains took 8 of 10 Dimeback top-ten spots (Likely 4.95%, 41.7 CPT); both winners still captained in the 5-25% band. Narrowing proposed below.
- **nfl_sd_cpt_rb_lean — contradiction logged (second).** RB captains were 2 of 10 and 3 of 10 top-ten captains against ~30% of the captain pool. Retirement proposed below.
- **nfl_sd_cheap_side_catchers, nfl_sd_pick_override_inside_band, nfl_sd_underweight_across_entries, nfl_sd_dupe_over_sim — untested** (no cheap side, no Claude pick, under-own calls at zero, no per-lineup sim data).
- **NEW nfl_sd_qb_catcher_captain (hypothesis).** A menu quarterback's top catcher belongs on the captain menu when captained under 5%. Likely: 4.95%, 41.7 CPT.
- **NEW nfl_sd_punt_slot_role_path (hypothesis).** The cheap spot is judged by a touchdown path, not the sheet's ceiling. Singletary: 13.8 points on a 7.7 ceiling.
- **NEW nfl_sd_winner_envelope_45_per_slot (hypothesis).** ~2,000-entry SE Showdown winners average ~45% ownership per spot, not 28%. Top-20: 47.0% and 45.6%.

## Venue file changes

This section is about the stadium file. NFL Showdown has no venue file, so nothing was written.

## Ledger hygiene

This section records one decision per flagged lesson.

- **nfl_sd_sub5_cpt_leak — KEEP, but the "near promotion" flag is wrong in substance.** Its one counted confirmation was partial, and the "sub-5% captains underperform" half has failed twice (Deebo/Robinson 9/10, Likely/Singletary 9/14). A third slate must confirm the narrowed statement: the WINNING captain sits in the 5-25% band while sub-5% captains fill top-10 spots without winning.
- **nfl_sd_three_three_default — PROMOTE.** Third confirming slate reached; edit below. One game usually tips to one side, so a 3-3 without a story is a bet on nothing.
- **nfl_sd_six_skill_default — KEEP, not promoted.** A third slate must show top-10 lineups carrying a kicker or defense more often than your entries did, after 0 of 20 this slate.
- **nfl_sd_kicker_conditional — KEEP, not promoted.** A third slate must show a dome, close-spread or under-owned kicker out-scoring his salary tier; Zvada beat Aubrey but scored only 4.0.
- **nfl_sd_cpt_rb_lean — RETIRE proposed.** RB captains sat below their captain-pool share on both slates (1-2 of 10, then 2-3 of 10).
- No stale hypotheses and no merge pairs were flagged; nothing references a removed feature.

## Proposed codifications

This section lists rule changes for you to approve; nothing here is applied yet.

**1. Codify nfl_sd_three_three_default** (ETR study + 9/10 + 9/14; the 9/14 Dimeback was a 5-5 tie, the Huddle 6-4, the top 3 in both contests 2-4). In `rules/nfl_sd/framework.md`, "Pre-lock checks", replace "Does every 3-3 build name the story it is betting on, or is it the default?" with:
"**A 3-3 build must name its story or it is not entered (codified 9/14/26).** Across 33 ETR slates and both logged slates the unbalanced shapes took the top spots more often than 3-3; on 9/14 the top 3 in both contests were 2-4 toward the Giants. A 3-3 with no story is a bet on nothing; the 2-4 tilted toward the captain's opponent is the under-built winning shape."

**2. Retire nfl_sd_cpt_rb_lean** (two mechanism contradictions). Set `status: retired`, `retired_reason: "RB captains sat below their ~30% share of the captain pool in the top ten on both logged slates (1-2 of 10 on 9/10, 2-3 of 10 on 9/14)."` No framework edit; its RB-lean line is already a question, not a rule.

**3. Narrow nfl_sd_sub5_cpt_leak** (two contradictions of one half). New statement: "The WINNING captain sits in the 5-25% band (2 of 2 winners: Purdy 6.7%, Dart 18.8%); sub-5% captains fill top-10 spots (4 of 10 on 9/10, 8 of 10 on 9/14) but have not won. Why: a sub-5% captain needs the slate's top raw score AND the right five around him." Reset its evidence to the two winners; stays a hypothesis.

## What this means for next slate

This section is the short list to carry forward.

1. When a quarterback is on the captain menu, put his top catcher on it too if fewer than 1 in 20 teams captain him.
2. Aim each entry at about 45% ownership per spot with one piece under 5%, not the 28% target the framework prints.
3. Fill the cheapest spot with a player who has a path to a touchdown, never with the crowd's highest-projected filler.
4. Give the underdog's story at least one entry, and never enter a 3-3 without saying what it bets on.
5. Keep the fade routine exactly as it is; it went 4 for 4.

## Added 9/14 evening — the salary cap and three tool bugs

This section was added after a second read of both repos' autopsy records.

**The $500-unspent rule blocked the 4th-place build.** Your Huddle entry (captain Skattebo, Lamb, Dart, Williams, Zvada, Theo Johnson) becomes the exact lineup that finished 4th in both contests (128.95 points) by swapping Zvada + Johnson for Likely + Singletary. That build costs $49,800. The strategy's build rule `salary_max: 49500` ("leave at least $500 unspent", taken from a median-winner stat) made it un-buildable in the Sim. The actual winner spent all $50,000. One slate, so this is an observation to watch, not a rule change: track whether the salary_max rule blocks a top-5 lineup again.

**Tool bugs found in tonight's records (fixes scheduled after the 9/14 MNF lock):**
1. Sim autopsy "What we got wrong" labels Devin Singletary "FADED" at 3.2% owned. He was a Leverage line, never a fade. Any unrostered player is being labeled FADED.
2. Analyzer adherence check warns Aubrey / Flournoy / Tracy were "zeroed in one contest" and defines underweight as one bullet in EACH contest. The strategy's own portfolio rules say `max_entries_with: 1`, judged across both entries. The grader contradicts the rule block it was handed.
3. Analyzer "Slate-defining plays" lists Emari Demercado at 0.7 points and 14.7% owned. The definer filter passes a player who scored nothing.
