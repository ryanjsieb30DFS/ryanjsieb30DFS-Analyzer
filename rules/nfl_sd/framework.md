# NFL Showdown Framework

**Seeded 2026-09-09 from docs/nfl_game_theory.md (Part 2). Updated 2026-09-10 with the ETR research digest (`docs/etr_research/DIGEST_2026-09-10_nfl_sd.md`) — user-approved.**
Sources: ETR Showdown 101 + winner studies, ETR 2025 Wildcat/Field General sim study (33 slates, 1,000–1,500-entry fields), ETR kicker study (2020–25), Fantasy Team Advisors' 163-winner study (2024–26), PFF Showdown Primer, Stokastic. Numbers below are cross-vendor winner data, not this repo's own logged results — the local ledger starts at zero SD slates.

## The format

DK single-game. Six spots: 1 Captain (CPT — 1.5x points at a distinct, higher CPT salary) + 5 FLEX (any position: QB/RB/WR/TE/K/DST). $50,000 cap. Both teams must be represented. The same six players with a different captain is a DIFFERENT DK entry. This is NOT PGA RD4 SD — the captain is real here.

NFL scoring note (unique among this repo's sports): **0.0 FPTS is a real score** (a blanked WR3, a kicker with no attempts) and **a DST can go negative**. Never read a 0.0 as a scratch. (The tier-calibration scratch exclusion carries an nfl carve-out in `src/pool_calibration.py`; the counterfactual swap engine is NOT captain-aware yet, so NFL autopsies run its points-only mode — `salary_checked: False` — rather than shipping flat-priced cap math.)

## The captain decision (the whole game)

CPT costs 1.5x for 1.5x points, so the multiplier itself buys nothing — the captain call is about ceiling and about what the field over-pays for.

| Winning captain's position | FTA (163 winners) | ETR top-1% study |
|---|---|---|
| WR | 33% | 33% |
| RB | 28% | 27% (biggest edge vs field's 24%) |
| QB | 21% | 24% |
| TE | 9% | — |
| DST | 6% | field ~2.5% |
| K | 3% | field ~0.8% |

- **Check whether the field over-captains the QB — it is not automatic.** He is optimal about 1 in 5. On 9/10/26 the field captained both quarterbacks under 8% and both contest winners captained Purdy; when a QB's captain ownership sits well under 20%, he belongs on the captain menu. Confirmed 9/13 (Dart 18.8%, 39.9, won both contests) and 9/21 (Mahomes 13.3%, 47.97 as captain, the best captain score on the board, blocked only by the $15,000 price beside the other stars, so his $9,300 catcher Kelce wore the tag and won). When the QB captain cannot fit, his cheapest-captained top catcher is the same bet (codified 9/21/26, lesson nfl_sd_qb_cpt_under_base_rate). On every completed pass the catcher out-scores the thrower — the QB's own receivers systematically out-captain him. **WR + RB = 61%+ of winning captains.**
- **Winning captains are not obscure**: median winning-captain own ~11%, average price ~$13,000, ~23.6 CPT points. The edge is the right member of the chalk cluster, not a 2% punt.
- Cheap captains under $7,500 won only with genuine slate-topping ceiling (goal-line RB, deep threat) — never as a salary trick. Winning sub-$7,500 captains scored 26.4 CPT points, 2.6x their median projection: reaching "value" is not enough, the punt needs a path to the slate's top raw score.
- **Captain ownership lives in the 5–25% band (codified 9/15/26).** All three logged winners captained inside it: Purdy 6.7% (9/10), Dart 18.8% (9/13), Walker 16.3% (9/14). Sub-5% captains filled top-10 spots on two of those slates (Deebo, Likely 41.7 CPT) and won none; the sub-5% captain chosen for ownership alone is the documented single-entry leak. Low ownership is a tiebreaker, never the thesis.
- **Captain position leans RB, not TE.** In the 2025 mid-field study RB was the only position that beat its projection on average (+0.2, 45% beat rate; WR −1.5, TE −3.1 with a 30% beat rate). Sim ROI by captain: RB +8%, WR +4.5%, QB −3%, TE −12%. Winning players ran CPT RB 31% and CPT TE 7%.
- Kicker captains are rare (2.4% of lineups in 2025) but no longer a throwaway: the win index moved from 0.78x to 1.05x as kicker ceilings rose. Use only when the salary relief buys the slate's top scorers.
- CPT DST: the field cannot tell good defense spots from bad (r² of CPT DST ownership vs points = 0.09), so it only pays when it comes without ownership — and it is 13.6% of winning 5-1/1-5 lineups vs 3.3% of every other shape.

## What the winning multi-entry players do (ETR 2025, 1,000–1,500-entry fields)

Across 33 slates of DK's $333/$444 showdown contests, the players who profit (+8% actual ROI, +12% sim ROI) build differently from single-entry players (−22% actual, −10.5% sim) in five measurable ways. None is a rule; each is a question to ask of a built lineup.

1. **Captain position leans RB.** See above: 31% CPT RB, 7% CPT TE.
2. **Captain ownership sits in the 5–25% band.** The sub-5% captain is the single-entry leak.
3. **The construction states the bet.** 3-3 is the low-conviction default and the worst-simming shape (−4.9% sim ROI; single-entry players use it 38%, pros 27%). 5-1 (+20% sim ROI, 24% "very good", 5% "horrid") and 1-5 are used about twice as often by pros. The strongest single combo measured: **CPT RB + his own DST + 5-1 = +24.6% sim ROI, 27.5% very good, 3.5% horrid** — one bet on one script (favorite controls the game on the ground, defense holds).
4. **Six skill players is a choice, not a default.** No-K-no-DST lineups were the worst configuration for both cohorts (single-entry: 54% of lineups, −17% sim ROI, −32% actual). DST + K together was +17% sim ROI and a 1.87% top-1% rate for pros, who run it in 20% of lineups.
5. **Projection band 90–95% of slate max.** Pros put over half their lineups there (54% vs 42%). The top-1% projection band at 200%+ cumulative own averages 15 dupes (90th percentile 42); the 2–5% band at 180–200% own averages 4 (90th percentile 11).

**How pros hold ownership:** 40% of their FLEX spots sit within 0.75–1.25x of field ownership — they are not big faders. They overweight sub-5% FLEX pieces (1.85x) and slightly underweight the 5–10% band (not cheap enough on dupes, too much projection given up).

## Correlation shapes (pre-lock CHECKS — information, never gates)

These are checks to run against a built lineup, phrased as what the winner data says. None of them is a rule that costs a grade; only a call THIS slate's strategy makes can do that.

1. Pocket-QB captain → did the lineup carry 2–3 of his own pass-catchers? (A rushing QB needs only 1.)
2. WR captain → is his QB in FLEX, with at most ONE more same-team pass-catcher? (Only 8% of winners ran CPT WR + 2+ extra teammates.)
3. Passing-script build → is there a bring-back (an opposing pass-catcher)? **89% of passing-build winners had one.**
4. Kicker → paired with his own DST (the slog stack) rather than his own captain QB? (K appears in 34% of top lineups overall, only 19% next to his own CPT QB.)
5. DST → at most 3 players from the offense it faces (89% of winners).
6. Hard shape fact: **max 2 combined K+DST pieces**; 3+ won ~1% of the time. Never two kickers.
7. Double-QB (both QBs rostered, one or both at FLEX) is PFF's "closest thing to a cheat code"; ≥1 QB appears in ~96% of top lineups. Zero-QB wins ~5% — a large-field script bet only.
8. CPT RB → is his QB rostered (61% of winners), and are same-team WR/TE held to ≤2 (0 → 17%, 1 → 55%, 2 → 25%, 3 → 3%)?
9. Naked CPT WR (no own QB — 14% of winners, usually a high-volume short-target WR or a salary squeeze) → is the OPPOSING QB in the build, and are extra same-team catchers at zero? If a build wants CPT WR + two same-team catchers, the better lineup is usually CPT QB.
10. CPT QB → 2 own WR/TE is the mode (46%; 1 → 29%, 3 → 19%, 0 → 5%); one own RB 44%; bring-back 80%; his own kicker (21.5%) beats the opposing kicker (17.5%). A rushing QB (20%+ team rush share) goes unstacked 12% vs 6% and triple-stacks less.
11. CPT TE → his QB in 89% of winners, exactly one more same-team catcher 58% (TE ceilings are touchdown-driven, so they share the passing game more than a CPT WR does).
12. Onslaught (5-1) → captain from the 5 side (95%), the 5-side QB rostered (95%, CPT 28%), two 5-side WR/TE (47%), one 5-side RB (68%), the 5-side DST (58%); the lone bring-back is a pass-catcher (50%) — never the opposing DST (0.4%).
13. 4-2 / 2-4 → captain from the 4 side (77%); the two-player side is a WR/TE (exactly one: 69%) plus an RB (43%), rarely a DST (4%) or K (11%).
14. DST → paired with 3–4 teammates in 79% of winning DST lineups; never the lone bring-back.
15. Dupe-cheap anti-correlations the field over-avoids: CPT vs the opposing DST (5% of winners, duplicated 5.6x vs 15.7x — don't group it out); two same-team RBs (6.6 dupes vs 8.5).

## Game scripts, weighted by Vegas

Every lineup is a story of how ONE game goes. Winner data by Vegas total:

- **Slog (total ≤42):** RB captains win 46% (WR 31%, QB 12%). Workhorse RBs, kickers, both DSTs.
- **Kickers (updated 2025):** the blanket kicker edge is gone — the field now uses a FLEX kicker in 37% of lineups (win index 1.02x, from 1.15x pre-2025) and DK raised the median kicker salary from $4,000 to $5,000 while every skill position got cheaper. Kickers still out-score their salary tier (8.4 pts vs same-priced TE 7.7 / WR 7.2 / DST 6.6 / RB 5.6; they beat same-priced RBs on 71% of slates). No environment or ownership clause has predicted on this repo's five logged slates (dome: Pineiro 11.0, Mevis 1.0 and 4.0, Zvada 8.0; outdoors: Zvada 4.0, Lutz 4.0, Butker 17.0, Shrader 14.0). Judge a kicker by his salary tier on the sheet like any other piece (retired 9/26/26, lesson nfl_sd_kicker_conditional). The favored kicker in 5-1 builds is now crowded (42% of 5-1 lineups) — look elsewhere for the sixth piece.
- **Middle (42.5–48.5):** near-uniform — WR 29% / RB 27% / QB 25%. Mixed portfolio.
- **Shootout (49+):** WR captains win 47%. Double stack + bring-back. At 51+, RB captains are the leverage (the field rotates all-pass).
- **By spread:** favorite captains ~62% overall (same as the field — not leverage). At spreads of 7+, favorite captains win 80%, while underdog WRs (garbage-time script) carried ~40% fewer dupes — the dupe-cheap contrarian shape in blowout-priced games.
- **Team splits of 163 winners:** 3-3 (34%) and 4-2 (31%) dominate — because they are BUILT most. Per lineup, 3-3 is the worst-simming shape and the single-entry default (see "What the winning multi-entry players do"); a 3-3 needs a named story as much as a 5-1 does. 5-1/6-0 onslaught wins ~1 in 8–10 (the blowout bet — same logic as the NASCAR drafting-track chalk-dom carve-out). **2-4 tilted AWAY from the captain's team is the most under-used winning shape** (only 16% of the field builds it).

## Duplication — the format's defining problem

~30 relevant players means the chalk build is copied at scale (the 231-dupe Packers–Lions Milly winner). **Dupes are predicted by the PRODUCT of the six ownerships, not the sum.** Spending exactly $50,000 raises dupes; the captain's own ownership barely matters.

**Dupe predictors, ranked (ETR 2025, correlation with actual dupes):** product of ownerships 0.43, cumulative ownership 0.39, relative projection (how close the lineup's total projection sits to the slate's max) 0.38. Lineups get copied because everyone using the same projections lands on the same near-max build. A cash at 11x+ duplication returns 60% less than a unique cash (156% vs 396% ROI); in the best sim bucket, low-dupe lineups returned +19.5% and 6+-dupe lineups −30%. Rule of thumb: **a 15% sim-ROI lineup with 2 projected dupes beats a 20% lineup with 10.** The captain's own ownership barely moves dupes; a CPT WR + his QB stack roughly doubles them (5.1 → 10.1), so push harder on product ownership and salary-left when the stack is in.

Uniqueness levers, roughly cheapest first: leave salary (**median winner left $1,400; only 7% of winners spent the full cap** — the opposite of Classic. **A RATE across the set, never a per-lineup salary_max in Build rules (codified 9/21/26):** a $49,500 ceiling blocked the 9/13 4th-place build ($49,800) and the 9/14 winner ($49,700); on 9/21 with no ceiling the Sim pool held the $49,700 winner); one sub-3% FLEX piece (41% of winners); the 90–95%-of-max projection band instead of the top 1%; the 2-4 split; two same-team RBs (~25% fewer dupes); a kicker or DST the field is under-using on THIS slate (no longer a blanket lever — see the kicker note above). One punt is a lever — three is a dead lineup (zero top-1% lineups carried 3+ min-priced players).

## Ownership envelope

Median winning lineup totaled **~45–48% per roster spot (codified 9/21/26).** Logged tops: 47.0% / 45.6% (9/13 top-20), 40.9% (9/14 top 1%), 48.0% (9/21 top 1%); the bottom half runs 40%. The top five names sit at 42–76% each, so four stars plus a cheap captain averages 48%; winners differ by the captain tag and the $3,400–$3,800 sixth piece, not by fading stars. Under 40% per spot is under-owning the chalk, not being sharp. A rate across the set, never a per-lineup quota. — Showdown winners are chalkier per-slot than Classic (~13%), the same way RD4 SD and MMA run chalkier than their classic formats. Moderate chalk + one or two real leverage pieces, never an all-contrarian card. This is a RATE across winners, never a per-lineup quota (the codified sharp-envelope lesson applies here from day one).

`rules/shared/shark_baseline.json` has **no nfl_showdown block** — the user's NFL standings archive is Classic-only, so no SD envelope can be mined yet. The Grade tab degrades to "no envelope data" and the envelope accrues from logged SD autopsies (`shark_accumulate` under the `nfl_showdown` key).

## The user's contest profile

**5–20 entries in LARGE-field lotto contests** (unlike the SE/3-Max home game in other sports). That means:
- A **script portfolio**: one lineup per game story (shootout / slog / blowout-onslaught / garbage-time), weights set by the Vegas total + spread — never one "best" lineup entered repeatedly.
- Dupe awareness is load-bearing at these field sizes: product-of-ownership, salary-left, and the under-used shapes (2-4 split, kicker) are where large-field equity lives.
- Set diversity doctrine applies in full (`rules/shared/set_diversity.md`): diversity is a property of the SET, judged pairs-of-picks down.

**Thesis vocabulary (named shapes).** Every Showdown lineup's one-sentence thesis names ONE of these shapes, so the portfolio can be read at a glance and the autopsy can score each shape by name. The names come from TwoGun's showdown presets (a 3x Milly Maker winner); the data behind each shape is already in this doc. This is naming only — no shape is required, banned, or graded.
- **Blowout 5-1** — the favorite runs away with it: favorite captain, the favorite's QB + two pass-catchers + RB or DST, one bring-back pass-catcher (never the opposing DST). Real when the spread is 7+.
- **Upset 5-1** — the same onslaught on the underdog's side: dog captain, dog QB + catchers, the dog DST, one favorite bring-back. The dupe-cheap version of the onslaught.
- **Garbage-time build** — the favorite leads early, the loser throws late: a 2-4 tilted away from the captain's team, underdog pass-catchers carrying the volume, favorite RB or DST as the early-game anchor. Under-built by the field (16%) and ~40% fewer dupes in 7+ spreads.
- **Ground-and-pound** — the slog (total 42 or less): RB captain + his own DST + a kicker, few pass-catchers. The strongest single combo measured (CPT RB + own DST + 5-1 = +24.6% sim ROI).
- **Shootout double-stack** — total 49+: QB + two of his catchers + a bring-back catcher, both offenses live. WR captains won 47% here; at 51+ the RB captain is the leverage.
- **Salary punt** — any of the above with a sub-3% piece and $1,400+ left, bought for uniqueness, not points.
- **Off-position captain** — TE, kicker or DST wearing the 1.5x. Only pays when it comes without ownership (CPT DST is 13.6% of winning 5-1/1-5 lineups vs 3.3% elsewhere).

**Portfolio shape, scaled from the winning multi-entry players (ETR 2025):** about 8–9 unique captains per slate on a 33 / 22 / 15 / 10 / 7 / 5 / 4 / 3% exposure ladder, scaled down to the entry count (at 5 entries that is roughly 2-1-1-1 across four captains); construction mix roughly 5-1 21% / 4-2 26% / 3-3 27% / 2-4 18% / 1-5 8% — covering the distribution of how the game can go, not one script repeated. The target is a set with **zero "horrid" lineups** (pros 7%, single-entry 28%), not a set of only peak lineups.

**Contest-selection flag (ETR 2025):** single- and low-entry players in multi-entry showdown contests posted −21.6% actual ROI against a max-entry cohort building better lineups at volume. A 5–20 entry set in a lotto field is competing against 150-max portfolios; either lean on the dupe levers harder than they can, or route part of the bankroll to single-entry showdown contests where the structural gap is smaller. Declare the entry-max with each contest so this is visible at declaration time.

## Pre-lock checks (information for the strategy writer, not gates)

- What are the script weights from the Vegas total + spread, and does each entered lineup name its script?
- Who is the over-captained player (CPT own vs the ~1-in-5 QB reality), and where do CPT own and FLEX own diverge on the vendor sheet?
- Does each passing build carry a bring-back?
- What is the highest-ownership-product chalk combination (the dupe magnet), and how many entries share it?
- Salary left: is any entry at exactly $50,000, and is that on purpose?
- K+DST count ≤2 per lineup; kicker not next to his own CPT QB unless the build says why.
- Anchor-Equivalence: which chalk anchors sit at similar own (including CPT-slot own) and are substitutable?
- Is any captain under 5% projected own, and if so, what is the one-sentence ceiling case (not the ownership case)?
- **A 3-3 build must name its story or it is not entered (codified 9/14/26, lesson nfl_sd_three_three_default).** Across 33 ETR slates and both logged slates the unbalanced shapes took the top spots more often than 3-3; on 9/14 the top 3 in both contests were 2-4 toward the Giants. A 3-3 with no story is a bet on nothing; the 2-4 tilted toward the captain's opponent is the under-built winning shape.
- **Six skill players with no K and no DST is a choice, not a default (codified 9/15/26).** On 2 of 3 logged slates the top lineups carried a K or DST more often than the user's entries (9/10: 6 of 10 per contest, Pineiro 11.0; 9/14: all 84 winning copies, Chiefs DST 12.0); on the third (9/13) every K and DST busted. A rate across the set, never a per-lineup quota.
- **Every UNDERWEIGHT call and every max_entries_with / max_exposure_pct cap in the Build rules is counted against the ENTERED set before lock, across every entry and every contest, against the field's lock-time ownership where DK shows it (codified 9/26/26, lesson nfl_sd_underweight_across_entries).** Logged misses: Ferguson 2 of 2 (9/10), Walker 65% vs a 60% cap (9/21), four caps on 9/21 MNF (Nabers 75% vs 50%).

**Pre-submit questions (ETR, asked of every lineup before it goes in):** Is there a clear game-script decision behind the captain? Does the team split match the bet? Is a DST or K in FLEX, and if not, why? Is the projection competitive without being one of the most obvious builds on the slate? Do I know where each piece sits vs field ownership, and is that position intentional?
