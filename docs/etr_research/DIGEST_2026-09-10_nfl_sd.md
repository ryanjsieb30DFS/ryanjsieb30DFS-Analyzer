# ETR Research Digest — NFL Showdown (2026-09-10)

**Status: APPLIED 2026-09-10 (user approved "apply everything"). Sections C + D1–D4 are live in `rules/nfl_sd/framework.md`, `philosophy.md`, `lessons.yaml`, and `docs/dfs_research_library.md` Ch.9. D5 (contest selection) is a flag in the framework's contest-profile section. Section E (code) is still backlog — neither repo supports NFL SD in code.**

Five Establish The Run articles, saved as PDFs in this folder (text sidecars `.txt` beside each):

| # | Article | Author / date | Data behind it | Field type |
|---|---|---|---|---|
| 1 | How to Beat DFS: NFL Showdown 101 | Cody Main, re-posted 9/5/26 (written 2022) | DK flagship primetime GPP, 2020–22 | LARGE (lotto, 150k+) |
| 2 | NFL Showdown Large-Field Tournament Strategy | Cody Main, 9/5/25 | Top-1% lineups, 3 seasons of primetime | LARGE |
| 3 | Should We Be Playing Kickers More in NFL Showdown? | Cody Main, 8/29/26 | 22.4M weighted entries, ~200 slates 2020–25 + play-by-play kick data 2021–25 | LARGE |
| 4 | NFL Showdown DFS: What Are the Sims Saying? (Part 1) | Cody Main, 9/4/26 | 49,146 lineups, 33 slates, DK Wildcat ($333) + Field General ($444), 2025 Wk5–SB | **MID (1,000–1,500 entries, 37-max)** |
| 5 | NFL Showdown: Playing Like a Pro (Part 2) | Cody Main, 9/7/26 | Same 33-slate Wildcat/Field General set | **MID** |

Field-size note: articles 4 and 5 are the closest ETR has ever come to the user's actual contest size. They are still multi-entry, mid-stakes fields, not SE/3-max. Per the research-library rule, the user's own small-field data wins on any conflict once the local NFL SD ledger has slates.

---

## A. What these articles CONFIRM (already in `rules/nfl_sd/framework.md`)

Already in the framework from the 9/9 seed, and re-confirmed here without change: captain position rates (WR ~33%, RB ~27%, QB ~24%); the field over-captains the QB; winning captains are chalk-cluster players (~$13,000, ~10% own); cheap captains only win with slate-topping ceiling; product-of-ownership predicts dupes better than the sum; leave salary; max 2 K+DST pieces; CPT WR with at most one more same-team pass-catcher; DST with at most 3 opposing players; kicker anti-correlates with his own CPT QB; the 2-4 split is under-used; underdog captains at 9+ spreads carry ~40% fewer dupes.

Nothing in section A needs editing.

---

## B. NEW findings, by article

### B1. Article 5 — what the winning (max-entry) players actually do

The most useful piece of the five. ETR split the 33-slate Wildcat/Field General field into single-entry players and max-entry players (31+ lineups) and compared their lineups on post-lock sim numbers AND real results.

The gap:

| Cohort | Sim ROI / lineup | Cash rate | Top-1% rate | Actual ROI | "Horrid" lineups (< -30% sim ROI) |
|---|---|---|---|---|---|
| Single-entry | -10.5% | 21.1% | 0.92% | -21.6% | 28.5% |
| Max-entry (31+) | +12.0% | 23.1% | 1.37% | +8.0% | 9.3% |

What the pros do differently, each a small edge that stacks:

1. **CPT RB is the best-simming captain position.** Pros use CPT RB in 31.1% of lineups (single-entry 24.9%). Sim ROI by CPT position: RB +8.0%, WR +4.5%, QB -3.3%, **TE -12.0%**. Pros use CPT TE only 7.2% (single-entry 11.4%). Real results agreed: CPT RB lineups posted +24.8% actual ROI across all users; CPT TE lineups -53.0%.
   - Why: over the 33 slates, **RBs were the only position to beat their projection on average** (+0.2 pts, 45% beat rate). WRs scored 1.5 under, TEs 3.1 under with a 30% beat rate.
   - CPT RB lineups also have the best shape: 16.9% "Very Good" (≥40% sim ROI), 12.9% "Horrid". CPT TE: 6.1% Very Good, 27.8% Horrid.
2. **The compounding combo: CPT RB + same-team DST + 5-1 build = +24.6% sim ROI, 27.5% Very Good, 3.5% Horrid.** All three are one bet on one game script (the favorite controls the game on the ground and the defense holds).
3. **Single-entry players over-chase low-owned captains.** They put 25.4% of captains in the sub-5% own range (pros 16.3%). Pros spread captains across the 5–25% own range, where sim ROI is most consistently positive. Sub-5% captains were the pros' LOWEST-ROI bucket (+5%). Low ownership alone is never the reason to captain someone.
4. **3-3 is the worst-simming construction (-4.9% sim ROI)** and single-entry players use it most (38.0% vs pros 26.8%). It is the low-conviction default. Pros use 5-1 at 20.6% (single-entry 11.9%): +20.2% sim ROI, 24.2% Very Good, 5.2% Horrid. Pros use 1-5 at 8.5% (single-entry 3.3%).
   - Reconcile with the framework's "3-3 (34%) and 4-2 (31%) dominate winners": 3-3 wins most often because it is BUILT most often. Per-lineup, it is the weakest bet. Both statements are true and the framework should say both.
5. **No DST and no K in the lineup is the weakest build.** Single-entry players run six skill players in 53.9% of lineups (-17.2% sim ROI, -32% actual ROI). Pros do it 32.7% of the time, and even their versions are their weakest config (+5.6%). Pros run BOTH a DST and a K in 20.5% of lineups: +16.9% sim ROI, 1.87% top-1% rate. Single-entry players do that 8.6% of the time. Six skill players should be a deliberate choice, never a default.
6. **Dupe predictors, ranked (r with actual dupes):** product ownership +0.43, cumulative ownership +0.39, relative projection (how close the lineup's total projection sits to the slate's theoretical max) +0.38. Concrete: a lineup at 200%+ cumulative own that projects in the top 1% of the slate averaged 15 dupes (90th percentile 42). A lineup in the top 2–5% projection band at 180–200% own averaged 4 dupes (90th percentile 11). **Pros put 53.7% of their lineups in the 90–95%-of-slate-max projection band** (single-entry 41.8%).
7. **Pro portfolio shape (11 users, 33 slates, 9 of 11 profitable):** ~19% Very Good, 25% Solid (10–40%), 7% Horrid. The goal is a set with no bad lineups, not a set of only the best ones. Construction mix 5-1 21% / 4-2 26% / 3-3 27% / 2-4 18% / 1-5 8%. **Captains: 8.7 unique per slate; exposure ladder 33 / 22 / 15 / 10 / 7 / 5 / 4 / 3%.**
8. **Pros are not big faders.** 40.5% of their FLEX spots sit within 0.75–1.25x of field ownership. They overweight sub-5% FLEX players (+1.85x) and slightly underweight the 5–10% band (not cheap enough on dupes, too much projection given up).
9. **Pre-submit questions** (verbatim intent): Is there a clear game-script decision behind the CPT? Does the construction match the bet? Is a DST or K in FLEX, and if not, why? Is the projection competitive without being one of the most obvious builds? Do I know where my CPT and FLEX sit vs field ownership, and is that intentional?

### B2. Article 4 — what post-lock sims can and cannot tell you (mid field)

1. **Cash rate is well calibrated.** Lineups simmed at 30%+ cash cashed 31.1%; 18–21% bucket cashed 20.8%.
2. **Sims do NOT pick winners.** Only 13 of 33 contest winners (39.4%) had a positive sim ROI at lock, below the 50.5% field base rate. 16 of the 33 winners came from max-entry players (portfolio volume finds the odd lineup).
3. **Sims DO find the top 10.** 222 of 375 top-10 finishers (59.2%) simmed positive; average sim ROI of top-10 lineups +6.7% vs field +1.5%. Positive-sim lineups were 1.17x as likely to finish top 10, negative-sim 0.82x.
4. **The worst bucket is truly bad.** Sim ROI ≤ -40%: 16.1% cash, -42.0% actual ROI, and the fewest dupes (1.79). Avoid these.
5. **The middle is noise plus dupes.** The -25 to -10% bucket beat every positive bucket on actual ROI (+13.8%) because positive-sim lineups get duplicated (peak 4.73 dupes in the 0–10% bucket). Among cashing lineups, unique entries averaged 396% ROI; 11x+ duplicated entries 156% (a 60% haircut). In the ≥40% sim bucket, low-dupe (1–2) lineups returned +19.5%, 6+ dupes -30%.
6. **Rule of thumb:** a 15% sim-ROI lineup with 2 projected dupes beats a 20% lineup with 10.
7. **Contest selection:** single- and low-entry players in multi-entry mid-stakes contests are structurally behind (-21.6% actual ROI). ETR's advice: move those dollars to single-entry contests at lower buy-ins.

### B3. Article 3 — kickers, updated through 2025 (large field)

1. **The old "kickers are under-used" edge is GONE in 2025.** Pre-2025: K in FLEX won at 1.15x its usage, no-K 0.93x, K at CPT 0.78x. 2025: K in FLEX 1.02x, no-K 0.99x, **K at CPT 1.05x**. The field moved (K-in-FLEX usage 33.5% → 37.2%) and DK repriced (median K salary $4,000 → $5,000 while every skill position got cheaper).
2. **Kickers still out-score their salary tier.** At a $4,400 median, kickers average 8.39 DK pts vs same-priced TE 7.70, WR 7.18, DST 6.61, RB 5.62. Kickers beat same-priced RBs on 71.4% of slates and same-priced WRs 59.3%.
3. **Real-game scoring is up** (kickoff rule 2024/25 + K-ball rule): FGA/game 1.91 → 2.04, avg distance 38.6 → 40.5 yds, 55+ yd attempts doubled with make rate 52.8% → 63.2%, DK avg 7.61 → 8.31, 15+ pt games 7.0% → 10.3%.
4. **Where ETR says the kicker edge now lives:**
   - **Dome games:** kickers average 9.2 pts in domes vs 7.9 outdoors; 15+ pt rate 12.0% vs 6.7%. Target when ownership is not already elevated.
   - **Close spreads (≤7):** winning and losing kickers score the same (8.3 vs 8.4), but the underdog kicker is owned less (18.8% vs 23.4%). Buy the dog kicker in tight games.
   - **Favored K in 5-1 builds is now crowded** (41.6% of 5-1 lineups in 2025); the advantage over no-kicker onslaughts vanished. Look elsewhere for the 5-1 sixth piece.
   - **K at CPT is no longer a throwaway** (2.4% usage, 1.05x win index). Not a target, but not auto-removed from the captain pool either.

### B4. Article 2 — conditional stack rates for top-1% large-field lineups

Finer than what the framework holds. Read each as "given this captain, how the winners filled the other five."

**CPT QB:** exactly 2 same-team WR/TE 46.3%, exactly 3 18.9%, exactly 1 28.9%, 0 5.1%. Exactly 1 same-team RB 44.0%. At least one opposing WR/TE 79.7% (exactly 1: 54.4%; exactly 2: 23.5%). Own kicker 21.5% vs opposing kicker 17.5%. Rushing QBs (20%+ team rush share) go unstacked 11.6% vs 5.6% for pocket passers, and triple-stack less (11.6% vs 17.8%).

**CPT RB:** own QB rostered 60.8%. Same-team WR/TE: 0 → 16.7%, 1 → 55.4%, 2 → 24.6%, 3 → 3.0%. Construction 3-3 36.3%, 4-2 34.2%. Working rule: at most 2 same-team WR/TE with a CPT RB.

**CPT WR:** same-team WR/TE 0 → 38.1%, 1 → 50.4%, 2+ → 9.2%. At least one opposing WR/TE 83.7% (exactly one 54.4%). **Without his own QB 13.9%** — happens with high-volume, low-depth WRs and when salary forces a choice; in naked-WR builds prioritize the OPPOSING QB and skip extra same-team catchers. If a build wants CPT WR + two same-team catchers, the better lineup is usually CPT QB instead.

**CPT TE:** own QB 89.4%; exactly 1 same-team WR/TE 58.4%. TEs pair with their QB more than WRs do (TD-driven ceilings).

**Onslaught (5-1 / 1-5):** CPT from the 5 side 94.7%. Onslaught QB rostered 95.1% (CPT QB 28.3%). Exactly 2 onslaught WR/TE 47.3%; exactly 1 onslaught RB 67.8%; onslaught DST 58.4%. The lone bring-back is an opposing WR/TE 50.1% of the time; **opposing DST as the lone bring-back 0.4%.** **CPT DST is 13.6% of winning 5-1/1-5 lineups vs 3.3% in every other shape** (the salary relief pays when one side dominates).

**4-2 / 2-4:** CPT from the 4 side 77.1%. Exactly 1 opposing WR/TE 69.4%; exactly 1 opposing RB 43.2%; opposing DST 4.4% and opposing K 11.4% are rare bring-backs.

**DST:** paired with 3 teammates 39.3%, 4 teammates 39.9%; 79.2% of DST lineups carry 3+ teammates.

### B5. Article 1 — small additions beyond the 9/9 seed

- Sub-$7,500 winning captains scored 26.4 CPT pts on average, 2.6x their 9.9 median projection. "Reaching value" is not enough; the punt must have a path to the slate's top raw score.
- Average CPT ownership in winning lineups 10.3%; CPT own has minimal correlation with dupe count. Dupes come from the whole roster.
- CPT WR + his QB raises expected dupes from 5.1 to 10.1. When the stack is there, push harder on product ownership and salary left; when the stack is deliberately absent, more chalk and salary are affordable elsewhere.
- Two same-team RBs: 6.6 dupes vs 8.5 with one.
- CPT vs opposing DST: 5.4% of winners, duplicated 5.6x vs 15.7x. Do not group it out.
- Spread ≥9: favorite captains 75.4% of winners; underdog WR captains 10.2% with 39.9% fewer dupes.
- CPT DST ownership vs CPT DST points r² = 0.09: the field cannot tell good DST spots from bad, so use CPT DST only when it comes without ownership.
- ETR's own stance: no rigid groups. Every rule adjusts slate by slate.

---

## C. CORRECTIONS to existing repo docs

1. **`framework.md` "Duplication" + `nfl_game_theory.md` 2.4 say a kicker is "massively under-used" (in 40% of winners).** That was true through 2024. Article 3's 2025 data shows the field caught up (37.2% usage, win index 1.02x) and DK repriced kickers up $1,000. Proposed rewrite: kicker is a NEUTRAL piece by default; the edge is conditional (dome, close spread with the dog kicker, low-owned). Drop "massively under-used".
2. **`framework.md` "Game scripts": "3-3 (34%) and 4-2 (31%) dominate."** Add the per-lineup view: 3-3 is the worst-simming shape and the single-entry default. Winners use it most because everyone uses it most.
3. **`framework.md` captain table** says kicker captains "cap the ceiling" and the game-theory doc says "remove them from the captain pool". 2025 data (1.05x win index, longer FGs) softens this to "rarely, and only when the salary relief buys the slate's top scorers".
4. **`philosophy.md` belief 1** says the default leverage move is the right chalk-cluster player at CPT. Article 5 adds a second half: the sub-5% captain is the single-entry leak. Belief holds; add the guardrail.

---

## D. PROPOSED additions (draft text, for approval)

### D1. `rules/nfl_sd/framework.md`

Add a section **"What the winning multi-entry players do (ETR 2025, 1,000–1,500-entry fields)"** after "The captain decision":

> Across 33 slates of the $333/$444 DK showdown contests, the players who profit build differently from single-entry players in five measurable ways. None is a rule; each is a question to ask of a built lineup.
> 1. **Captain position leans RB.** RB is the only position that beats its projection on average; CPT TE is the worst-simming captain. Pros: 31% CPT RB, 7% CPT TE.
> 2. **Captain ownership sits in the 5–25% band.** The sub-5% captain is the single-entry leak (25% of their captains vs 16% for pros) and the pros' lowest-ROI bucket.
> 3. **The construction states the bet.** 3-3 is the low-conviction default and the worst-simming shape. 5-1 (+20% sim ROI) and 1-5 are used twice as often by pros. The strongest single combo measured: CPT RB + his own DST + 5-1.
> 4. **Six skill players is a choice, not a default.** No-K-no-DST lineups were the worst config for both cohorts; DST + K together was +17% sim ROI for pros.
> 5. **Projection band 90–95% of slate max.** The top-1% projection band at 200%+ cumulative own averages 15 dupes; the 2–5% band at 180–200% averages 4. Pros put over half their lineups in the second band.

Add to **"Duplication"**: the three ranked dupe predictors (product own 0.43, cumulative own 0.39, relative projection 0.38), the 15-vs-4 dupe table, and the 60% cash haircut on 11x-duplicated lineups. Replace the kicker sentence per C1.

Add to **"Correlation shapes"** as checks 8–11 (information, not gates):
> 8. CPT RB → is his QB rostered (61% of winners), and are same-team WR/TE held to ≤2?
> 9. Naked CPT WR (no own QB, 14% of winners) → is the OPPOSING QB in the build, and are same-team catchers at zero?
> 10. Onslaught (5-1) → captain from the 5 side (95%), the 5-side QB rostered (95%), and the lone bring-back a pass-catcher, never the opposing DST (0.4%)?
> 11. 4-2 → captain from the 4 side (77%), the two-player side a WR/TE plus RB, not DST/K?

Add to **"Game scripts"** under kickers: the conditional kicker edges (dome 9.2 vs 7.9 pts; close spread → dog kicker at 18.8% vs 23.4% own; favored K in 5-1 now crowded at 41.6%).

Add a **"Portfolio shape (5–20 entries)"** paragraph under the contest profile: 8–9 unique captains per slate at a 33/22/15/10/7/5/4/3 ladder scaled to entry count; construction mix roughly 5-1 21% / 4-2 26% / 3-3 27% / 2-4 18% / 1-5 8%; the target is zero "horrid" lineups, not maximum peak.

Add the five **pre-submit questions** (B1.9) to "Pre-lock checks".

### D2. `rules/nfl_sd/philosophy.md`

Belief 1, append: "The mirror-image leak is the sub-5% captain chosen for ownership alone. Winning captains live in the 5–25% band; low ownership is a tiebreaker, never the thesis."

Belief 2, append: "A 3-3 build with no script behind it is the default of players who lose money. If the lineup cannot say which side wins and how, it is not finished."

### D3. `rules/nfl_sd/lessons.yaml` — candidate hypotheses (status: hypothesis, 0 confirmations, all from ETR mid-field data)

- **nfl_sd_cpt_rb_lean** — RB captains beat projection more than any other position; CPT TE is the weakest. Mechanism: RB usage is stickier than target share. Confirm if RB captains appear in top-10 finishes at ≥ their captain-pool share on logged slates.
- **nfl_sd_sub5_cpt_leak** — captains under 5% projected own underperform captains at 5–25%. Mechanism: the ceiling needed to top the slate is rarer than the ownership discount is worth.
- **nfl_sd_three_three_default** — 3-3 builds without a named script underperform 5-1 / 1-5 / 4-2 builds with one. Mechanism: single NFL games resolve to one side more often than they split.
- **nfl_sd_six_skill_default** — lineups with no K and no DST underperform. Mechanism: K and DST are the highest-scoring pieces in their salary tier and force a script.
- **nfl_sd_kicker_conditional** — kicker edge exists only in domes, close spreads (dog kicker), or when under-owned; blanket kicker use is neutral since 2025.
- **nfl_sd_dupe_over_sim** — at similar sim ROI, the lineup with fewer projected dupes wins on actual ROI. Mechanism: 60% haircut on heavily duplicated cashes.

### D4. `docs/dfs_research_library.md` Chapter 9 — candidate rules to append

8. **Captain ownership band (NFL SD):** the pre-lock check flags any captain under 5% projected own and asks for the ceiling case in one sentence.
9. **Script-named construction (NFL SD):** every entered lineup names its team split (5-1 / 4-2 / 3-3 / 2-4 / 1-5) and the game story that split bets on. A 3-3 with no story is flagged.
10. **Dupe-adjusted pick (Sim tool, NFL SD):** when two candidate lineups are within ~5 points of sim ROI, prefer the one with fewer projected dupes.

### D5. Contest-selection flag (for the user, not a doc change)

Article 4's clearest finding: single- and low-entry players in multi-entry mid-stakes showdown contests lose (-21.6% actual ROI) to the max-entry cohort building better lineups at volume. The user's NFL SD profile is "5–20 entries in large-field lotto contests". That is closer to the lotto field ETR studied in articles 1–3 than to the Wildcat, but the same asymmetry applies: a 5–20 entry set competes against 150-max portfolios. Two honest options, the user's call: (a) keep the lotto entries and lean on the dupe levers in section B1.6 harder than the max-entry players can, or (b) route part of the NFL SD bankroll to single-entry showdown contests where the structural gap is smaller. The Analyzer's contest screener can carry the entry-max field per contest so this shows up at declaration time.

---

## E. Tool implications (backlog, no commitments)

- **Sim tool picker (NFL SD):** article 4 supports the existing "guide not gate" stance and the memory note that sim rank is not a quality filter. Two usable refinements: (1) hard-avoid the ≤ -25% sim-ROI bucket; (2) tiebreak by projected dupes. The Sim already computes dupe penalties for all field sizes (9/7); wiring a dupe tiebreak into the NFL SD pick rationale is a small change once NFL SD is supported at all.
- **Analyzer Grade tab:** the five pre-submit questions map onto the existing per-lineup thesis requirement. Only the ones THIS slate's strategy adopts can cost a grade.
- **Both repos still lack NFL SD support.** Every proposal above is doc-only until the loader / builder / autopsy handle CPT.
