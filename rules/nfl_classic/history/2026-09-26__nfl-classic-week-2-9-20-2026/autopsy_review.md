# Post-autopsy review — NFL Classic Week 2 (Sunday, September 20, 2026)

_One DraftKings contest: the $20K Screen Pass 3-Max (1,568 teams, 3 entries). DraftKings only. The slate-day process log (`history/2026-09-20__.../process_review_notes.md`) was read alongside the archive._

## What happened

This section tells the story of the slate in plain words.

1. Your best team finished 516th of 1,568, which beat 67% of the field (top 32.9%); the other two finished top 68.8% and top 72.3%.
2. The winner, abbyml, scored 205.28 with Brock Purdy ($6,200, 28.48 points, on 11% of teams) throwing to George Kittle ($4,600, 18.0, on 4% of teams).
3. The winner's separating piece was DeVonta Smith ($6,800, 30.7 points, on 2% of teams), a receiver almost nobody had.
4. The slate's top scorer was Jaxon Smith-Njigba ($8,100, 45.5 points, on 7% of teams), and the top defense was the Panthers ($2,700, 26.0, on 6% of teams).
5. The crowd's favorite, Bijan Robinson ($8,200, 11.1 points, on 53% of teams), sank half the field: 55% of the bottom-half teams had him and only 12% of the top 1% did.
6. The crowd's tight end, Dalton Schultz ($3,200, 29.0 points, on 37% of teams), was in 8 of the top 10 lineups, and you had him in none.

## Process scorecard

This section grades HOW you played the slate, meaning the decisions, not the results.

**The strategy read the games right.** It named WAS@DAL and MIA@SF as the two stack games and Dak Prescott and Purdy as their quarterbacks. Those two were the slate's deciding plays (29.76 and 28.48, in 9 of the top 10 lineups), and both were tiered Core. Jaxon Smith-Njigba was named on the leverage line before he scored 45.5. Next slate: keep the game-first read, it is working.

**The strategy printed the wrong sharp target, and that ignored an open lesson.** The Week 1 review birthed an idea we are still testing (a hypothesis lesson) that the pros in your small fields run 19 to 20% average ownership per roster spot. The strategy still told you "about 14% per slot," the seeded number from the bundle. You built to 12.8% per spot; the nine tracked-pro entries ran 17.4% and the top 20 ran 18.9%. This is the main way winning lineups looked different from yours, and it cost you Schultz (29.0) and Aaron Jones (13.5). Next slate: the target line must quote the in-field pro number from the ledger, not the seed.

**Discipline grade: A on fades, but every underweight was held at zero.** Zero hard fades broken (the Ravens defense, LEAN FADE, was out of all three). The strategy defined UNDERWEIGHT as "one entry, not two, never zero," and you ran zero of three on five of the seven underweights: Wentz, Jones, Schultz, Andrews, Golden. Treating underweight as fade is what pushed the set to 12.8% per spot. Next slate: one entry carries each underweight that projects top-5 at his position, as the strategy says. (New lesson born below.)

**Leverage coverage stayed at a quarter, two slates running.** The strategy named 12 low-owned players who could decide the slate (leverage candidates); your entries carried 3 (Purdy, Maye, Achane), the same 3 of 12 as Week 1. Smith-Njigba (45.5) was named and unrostered. Next slate: each of the three entries carries a different named leverage piece.

**Shape: you ran the field's chalk build, not the sharp one.** All 3 entries were a quarterback plus two of his own teammates (a double stack) with three running backs. In this field the double stack was the CROWD shape (47.5% of the field, 37.5% of the top 1%, 22.2% of the pros) and so was the three-back build (57.0% of the field, 37.5% of the top 1%). The winner ran two backs and two tight ends. Next slate: at least one entry runs a single stack and at least one runs a receiver or tight end in the flex.

**The pre-lock plan held zero of the top game, and the late swap rescued it.** The process log shows the entered set at noon carried no WAS@DAL piece "by deliberate hold," against the strategy's one-WAS@DAL-entry rule. The 3:20 PM late swap moved entry 2/3 onto Dak, Lamb and Pickens, and that entry became your best (132.76, with 90.7 of its points from Dak, Lamb and McCaffrey). The other six spots scored 42 points, led by J.K. Dobbins ($5,000, 3.6) and Caleb Douglas ($3,700, 3.9), the cheap fillers the log flagged as "salary artifacts" before lock. Next slate: no non-defense filler under $4,000 unless the strategy names him.

**Pool versus picking: the build held a winner, and the pick beat the pool.** The Sim's pool of 49,208 lineups topped out at 207.28, above the winning 205.28, but only 3 lineups in 49,208 reached the winning score, so the build was barely good enough. 17.6% of the pool beat your best entry, your best entry beat 82.4% of the pool, and picking added about 2.6 points over the pool average. No Claude pick table was archived (no lineup_selection file), so the table step cannot be graded. The pre-lock sim numbers: Cash% predicted real scores best (0.15, its top 100 rows averaged 128.8 against a pool average of 111.1), Top-1% 0.13, ROI 0.14, and Win% 0.10 with its top 100 rows scoring BELOW the pool average. Win% has now read near zero on both logged slates. Next slate: pick inside the Cash%-and-Top-1% good set and ignore Win% rank.

**Board calibration held, and the Fade tier buried five quarterbacks.** Core averaged 17.3 points, Good 12.9, Okay 9.8, Fade 6.4, in order. Every buried player was a Fade-tier quarterback: Tyler Shough 22.4, Drew Lock 21.4, Kirk Cousins 21.2, C.J. Stroud 20.0, Deshaun Watson 19.7. Week 1 buried Bryce Young (35.44) the same way. Next slate: a quarterback is tiered Fade only for a volume or injury reason, never for a quality read. (New lesson born below.)

**Rules that have proven themselves and live in the framework (codified): none exist yet for NFL Classic**, so nothing can be demoted. Anchor-Equivalence appeared as edges 2 and 3 and it paid: Purdy (11% owned) won it over Dak (17%), and Jones (33%) beat Henry (35%) and Javonte (28%, 8.0) in the top 10. NFL has no venue file.

## Lesson ledger changes

This section lists every idea-we-are-testing (lesson) that this slate touched.

- `nfl_classic_double_stack_edge` — first contradiction: top 1% ran double stacks 37.5% vs the field's 47.5%.
- `nfl_classic_rb_chalk_sturdy` — contradiction (partial): Bijan (53%, 11.1) in 1 of the top 10; Jones and McCaffrey held.
- `nfl_classic_cheap_qb_leverage` — contradiction: 1 of the top 10 ran a sub-$6,000 quarterback (Lock).
- `nfl_classic_three_rb_underowned` — contradiction: three backs was the chalk shape (57% of field, 37.5% of top 1%).
- `nfl_classic_full_cap` — third confirmation: top 20 averaged $49,880; codification proposed.
- `nfl_classic_dome_stack_tiebreaker` — third confirmation (soft): dome Dak +8.1 / Lamb +19.5 over projection vs outdoor Purdy +7.4.
- `nfl_classic_dst_chalk_fragile` → validated: Buccaneers (16% owned) scored 2.0, Panthers (6%) 26.0 in 5 of the top 10.
- `nfl_classic_small_field_pros_run_chalkier` → validated: pros 17.4% per spot, Bijan held 67%.
- `nfl_classic_bringback_fade_needs_a_reason` — confirmation: the winner skipped the Miami bring-back and bought Lamb + DeVonta Smith.
- `nfl_classic_one_game_cap_by_field` — confirmation (soft): 0 of the top 16 had 5+ from one game vs 8.9% of the field.
- `nfl_classic_shootout_opposing_qb_not_fade` — confirmation (soft): Shough, Fade-tiered in an "up in pace" game, scored 22.4.
- `nfl_classic_te_bring_back` — contradiction (soft): 0 of the top 10 carried an opposing tight end.
- `nfl_classic_chalk_bringback_inside_stack` — contradiction: Lamb (38.3) was naked in 4 of the top 10, including the winner.
- `nfl_classic_forced_value_stampede` — contradiction: Schultz rose only 5.6 points of ownership and paid 29.0.
- `nfl_classic_dst_pressure_not_points_allowed` — contradiction (soft): Panthers 26.0 on a backup-QB read; Buccaneers mismatch 2.0.
- NEW `nfl-classic-2026-09-26-underweight-is-not-zero` (hypothesis): five underweights held at zero, Schultz in 8 of the top 10.
- NEW `nfl-classic-2026-09-26-qb-fade-tier-too-deep` (hypothesis): five Fade-tier quarterbacks scored 19.7 to 22.4.
- Untouched (not testable this slate): `positive_sim_wins_more`, `ownership_miss_three_checks`, `week1_ownership_premium`, `fangio_tree_volume_drag`, `set_shares_one_game` (applied: no two entries shared two pieces from one game, finishes spread 32.9 to 72.3).

## Venue file changes

NFL has no venue concept, so there is no venue file to update. Nothing was changed.

## Ledger hygiene

This section records the ledger-maintenance decisions; the pre-pass flagged six lessons two slates from promotion and nothing stale or mergeable.

- `nfl_classic_full_cap` — PROMOTE: third confirming slate; the edit is below.
- `nfl_classic_dome_stack_tiebreaker` — PROMOTE (stack half only): third confirming slate; the defense half stays unmeasured and is noted in the edit.
- `nfl_classic_double_stack_edge` — KEEP at validated: the third slate must show the top 1% double-stack rate ABOVE the field's measured rate, which this slate reversed.
- `nfl_classic_rb_chalk_sturdy` — KEEP at validated: the third slate must show the top-owned back at or above his field rate in the top 10, which Bijan failed.
- `nfl_classic_cheap_qb_leverage` — KEEP at validated: the third slate must show sub-$6,000 quarterbacks in the top 10 above the field's usage.
- `nfl_classic_three_rb_underowned` — KEEP at validated: the third slate must show three-back builds over-represented in the top 1% versus a MEASURED field rate; one more reversal retires it.
- No stale hypotheses, no merges, no lesson references a removed feature.

## Proposed codifications

This section lists edits the user approves in the app; nothing here was applied.

1. **Codify `nfl_classic_full_cap` into framework.md**, section "Roster construction, position by position," bullet "Salary." Append: "Local ledger (codified 2026-09-26): Week 1 top lineups averaged $49,833 (SE) and $49,905 (3-Max); Week 2 top 20 averaged $49,880. Three confirming slates." Set `codified_in: framework.md — Roster construction / Salary`.
2. **Codify `nfl_classic_dome_stack_tiebreaker` (stack half) into framework.md**, section "Pick the game before the players," bullet "Dome tiebreaker." Append: "Local ledger (codified 2026-09-26, stack half only): the dome stack beat projection by more than the outdoor comparison on both logged slates (Week 1 Shough/Olave/St. Brown vs Burrow/Chase; Week 2 Dak +8.1 and Lamb +19.5 vs Purdy +7.4). The dome-DST discount is still unmeasured locally." Set `codified_in: framework.md — Pick the game / Dome tiebreaker`.

No lesson has two contradictions, so there are no retirement proposals.

## What this means for next slate

This section is the short list to carry into Week 3.

1. Build to the pros' 17 to 19% ownership per spot, not the 14% seed, and make the strategy print that number.
2. Every UNDERWEIGHT gets one entry, never zero; Schultz-type cheap volume chalk paid 29 and was in 8 of the top 10.
3. Mix the shapes: one single stack and one non-three-back build, because the double stack and three backs were the crowd's shape this week.
4. Put a different named leverage piece in each of the three entries; 3 of 12 covered is two slates running.
5. Never tier a quarterback Fade for a quality read; five Fade quarterbacks scored 20 or more.

## Applied

Applied 2026-09-26 (user approved). Both codifications are in `rules/nfl_classic/framework.md`: the Salary bullet under "Roster construction, position by position" carries the full-cap local-ledger line (Week 1 $49,833 SE / $49,905 3-Max, Week 2 top 20 $49,880, three confirming slates), and the Dome tiebreaker bullet under "Pick the game before the players" carries the stack-half line (dome-DST discount still unmeasured). In `lessons.yaml`, `nfl_classic_full_cap` and `nfl_classic_dome_stack_tiebreaker` are `codified` with `codified_in` naming those sections. Ledger hygiene: no retire or merge decisions; the four KEEP lessons (`double_stack_edge`, `rb_chalk_sturdy`, `cheap_qb_leverage`, `three_rb_underowned`) stay `validated`. `philosophy.md` unchanged.
