# Post-autopsy review — NFL Classic Week 1 (Sunday, September 13, 2026)

_First logged NFL Classic slate. Two DraftKings contests: the $25K Fair Catch single-entry (2,450 teams, 1 entry) and the $25K Screen Pass 3-Max (1,960 teams, 3 entries). An earlier archive folder for the same slate (without the `__2` suffix) is a superseded duplicate of this one; the results ledger holds one row._

## What happened

This section tells the story of the slate in plain words.

1. Your single-entry team finished 1,748th of 2,450, which beat only 29% of the field (top 71.3%).
2. Your best 3-Max team finished 219th of 1,960, which beat 89% of the field (top 11.2%), and the other two finished near the middle (top 41.4% and 49.3%).
3. The single-entry winner, dankepka, scored 228.56 with Lamar Jackson ($6,800, 28.96 points, on 7% of teams) throwing to Zay Flowers, plus Jonathan Taylor (26.1) and Jalen Coker.
4. The 3-Max winner, FearSweetPea, scored 249.34 with Bryce Young ($5,200, 35.44 points, on under 5% of teams), Ashton Jeanty ($6,600, 35.7), D'Andre Swift ($6,100, 35.4) and Coker.
5. The slate was decided by the Bears–Panthers game: Jalen Coker ($4,600, 36.8 points, on about 9% of teams) was in 6 of every 10 top lineups in both contests, and Caleb Williams (37.26) was the top quarterback.
6. The crowd's second favorite, Ja'Marr Chase ($7,800, 3.2 points, on 38% of teams), sank half the field: 53% of the bottom-half teams had him and almost no top team did.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**The strategy read the games right and the players inside them wrong.** It named Bears–Panthers as the best low-owned stack (edge 6) and Caleb Williams as its quarterback, and your 3/3 lineup built exactly that and was your best finish (182.06). But the strategy's named pieces of that game were Colston Loveland (0.0 points) and Luther Burden III (10.5), while the points went to Swift (35.4), Coker (36.8) and the other quarterback, Bryce Young (35.44). Next slate: when a game is called a shootout, put its running back and its cheapest catcher on the leverage line, not only the tight end.

**The board buried the winning quarterback.** Bryce Young ($5,200, projected to be on 1.6% of teams) was tiered Fade while his catchers McMillan and Coker were named as bring-back plays for a Williams stack. That is a contradiction: a bring-back only scores if the other quarterback throws. Young was the quarterback in 7 of the 20 top-10 lineups across both contests. Next slate: the second quarterback of any shootout game never sits in Fade. (New lesson born below.)

**The single-entry pick followed the strategy's first suggestion, and that game busted.** The strategy's step 1 led with Burrow + Chase + Higgins, and your SE ran exactly that with Godwin as the bring-back: Burrow 15.2, Chase 3.2, Higgins 8.9, Godwin 8.3, or 35.6 points from four spots. This is a losing result, not a bad decision — the highest-total game with the top-projected receiver is a fair single-entry story. The process fault is elsewhere: your 3-Max 2/3 also carried Higgins + Godwin, so half your money rode one game. Next slate: check that no two entries share two pieces from the same game.

**The pre-flight checks were honored.** Anchor-Equivalence appeared as edge 2 (five quarterbacks within one projected point) and it paid: the twins Lamar (28.96) and Hurts (24.72) beat Goff (16.44). There is no venue file for NFL, and no lesson was yet validated, so nothing was ignored. The 5th-grader and length rules held (about 3,900 words).

**Your own fade and underweight calls were honored (discipline grade: A).** Zero hard fades broken; the Jets defense (LEAN FADE, 9.0 points) and Jeanty (LEAN FADE) were out of all four lineups. Jeanty then scored 35.7 as the 3-Max winner's leverage piece, which is a lost bet, not a broken rule — the fade cited a real price argument (Bijan projected 3 points higher at lower ownership, and Bijan scored 31.3). The four per-contest underweight flags are mostly noise: a one-lineup single-entry cannot hold "at least one bullet" of six underweight players at once. The strategy named 12 low-owned players who could decide the slate (leverage candidates) and your entries carried 3 of them: Hurts, Williams, DeVonta Smith. Josh Allen (0.7% owned, 38.66 points, the top scorer on the slate) was on the list and in none of your lineups — a coverage hit for the strategy and a miss for the set.

**The pros looked like you this week, and lost too.** The three tracked pros in the single-entry (moklovin, youdacao, ShaidyAdvice) ran 19.6% average ownership per roster spot against your 20.8%, and all three held Gibbs and Chase; their best finish was top 22%. The biggest measured gap — "share of lineups with a sub-5% piece" at 100% versus 67% — is an artifact of one lineup versus three, not a leak. First NFL Classic slate, so no recurring axis exists yet. The real finding is a calibration one: the bundle told the strategy the sharp target was 13.7% per spot, and the pros in this exact field ran 6 points chalkier. (New lesson born below.)

**Pool versus picking: the build held a single-entry winner, the pick missed it; the 3-Max pool never held a winner.** The Sim's pool of 48,944 lineups topped out at 241.6 points — above the SE winning score of 228.56 but below the 3-Max winner's 249.34, so the 3-Max miss was a BUILD miss. In the SE, 61% of the pool outscored your entry and picking from the pool would have added about 9 points on average — you picked below the pool's middle. In the 3-Max, only 6.8% of the pool beat your best entry and your picks were 24 points better than the pool average. No Claude pick was saved for either contest, so the picker check has nothing to grade. The pre-lock sim numbers: Cash% was the only one that predicted real scores at all (0.18, its top-100 rows averaged 165 points against a 140 pool average); Top-1% read 0.09, ROI 0.10, and Win% 0.02, which is no signal. One slate is noise; watch whether Win% stays near zero.

**Codified rules: none exist yet for NFL Classic**, so there is nothing to demote. The seeded framework rules that DID trigger — RB chalk is sturdy, cheap QBs win, full salary, three-RB builds, dome stacks — all held this slate and are now marked validated in the ledger. The Week 1 ownership-premium idea (the more-popular twin usually wins in Week 1) failed on every matched pair except Gibbs, and got its first contradiction.

**Board calibration held.** Core averaged 21.0 points, Good 17.3, Okay 11.3, Fade 7.2 — in order. Three Fade names scored above the Core average: Young 35.4, Jeanty 35.7, Kyle Monangai 23.4; Young is the one that mattered and is covered above.

## Lesson ledger changes

This section lists every idea-we-are-testing (lesson) that this slate touched.

- `nfl_classic_double_stack_edge` → validated: 10 of 20 top-10 lineups ran QB + two of his catchers (50% vs the 29% external baseline; this slate's field rate not measured).
- `nfl_classic_rb_chalk_sturdy` → validated: Gibbs (57–61% owned, 37.6) in 17 of 20 top lineups; Mayer, Chase, Jets all under their field rate.
- `nfl_classic_cheap_qb_leverage` → validated: 15 of 20 top lineups used a sub-$6,000 QB (Young ×7, Shough ×5).
- `nfl_classic_full_cap` → validated: top lineups averaged $49,833 (SE) and $49,905 (3-Max).
- `nfl_classic_dome_stack_tiebreaker` → validated (stack half): Saints–Lions dome stack beat projection, Bucs–Bengals outdoor stack missed.
- `nfl_classic_three_rb_underowned` → validated: 10 of 20 top lineups ran an RB in the FLEX, including the 3-Max winner.
- `nfl_classic_week1_ownership_premium` — first contradiction: the higher-owned twin lost at QB (Goff 16.44), RB (Hampton 9.3, Barkley 9.0, Achane 10.6) and WR (Chase 3.2).
- `nfl_classic_dst_pressure_not_points_allowed` — no change, mixed: Steelers (No. 3 mismatch) 18 and Jaguars (No. 2) 13 beat the Jets (points-allowed pick) 9, but the Eagles (No. 1) scored 3.
- `nfl_classic_forced_value_stampede` — did not trigger: Mayer's real ownership (47–51%) matched the 47.8% projection.
- NEW `nfl_classic_shootout_opposing_qb_not_fade` (hypothesis): Bryce Young, Fade-tiered, 35.44 as a shootout's second QB.
- NEW `nfl_classic_set_shares_one_game` (hypothesis): 2 of 4 entries shared Higgins + Godwin and sank together.
- NEW `nfl_classic_small_field_pros_run_chalkier` (hypothesis): in-field pros ran 19.6% per spot vs the 13.7% seed.

## Venue file changes

NFL has no venue concept, so there is no venue file to update. Nothing was changed.

## Ledger hygiene

This section records the ledger-maintenance decisions; the pre-pass found nothing flagged (17 hypotheses, none stale, none near promotion, no merge pairs).

- KEEP all 17 seeded hypotheses: this was the first logged slate, so none had a chance to go stale.
- No merges: the three new lessons touch different reasons-it-works (game-story contradiction, set-by-game diversity, envelope calibration).

## Proposed codifications

None this slate. Six lessons moved to validated on one confirming slate each; codification needs three, so the earliest proposal is two slates away. No lesson has two contradictions.

## What this means for next slate

This section is the short list to carry into Week 2.

1. If a game is called a shootout, its cheaper quarterback goes on the leverage line, never in Fade.
2. Before entering, check that no two of your lineups share two players from the same game.
3. Keep Gibbs-type running-back chalk and separate at quarterback and stack — that is exactly what both winners did.
4. Cheap quarterbacks (under $6,000) were in 15 of 20 top lineups; the ownership line for quarterbacks is where the leverage lives.
5. Treat the Sim's Win% as no signal for now and lean on Cash% and Top-1%, until two more slates say otherwise.
