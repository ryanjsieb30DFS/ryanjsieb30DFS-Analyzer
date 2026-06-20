# PGA RD4 Showdown — RBC Canadian Open, Round 4 (TPC Toronto at Osprey Valley)

## Pre-flight checklist
- [x] Slate confirmed: RBC Canadian Open R4 — bundle generated 2026-06-14 00:07; ETR + The Stone articles dated 6.14.26; leaderboard (Suber -13, Cauley -12, Tommy/Clark/Jesper/Garnett -11) matches a live R4. Current slate, not stale.
- [x] Projections loaded: DK PGA RD4 SD (75 players, primary) + pga-sd-projections-dk-20260613.csv (2nd source). The Stone supplies the leaderboard/SG/ceiling read. **Ownership conflict flagged** (Suber 37.6% DK/ETR vs 15.1% Stone — see disagreements).
- [x] Venue file read: rules/pga_classic/courses/tpc_toronto_osprey_valley.md (UNVERIFIED). File says "birdie-fest, easy"; **this week it has NOT played that way** — appending below: through 54 holes the course defended (leader -13 vs 2025's -18 win; multiple +4 rounds; R2 leader B. James fell to ~T40). The venue's easy reputation is overridden by this week's observed scoring.
- [x] Open lessons reviewed: sub15-midtier-birdiefest-score-source (validated) → applied conditionally (only fires on the birdie-hedge lineups, not the tough-course core — mechanism is rule-set-gated); repeated-punt-needs-thesis (hypothesis) → applied (any sub-6% punt in 2+ builds carries a named spike thesis); leverage-play-still-mandatory (hypothesis) → applied (≥1 sub-10% in every build, tough-course dose ~1.9). All codified lessons (anchor-equivalence, never-zero-top3, ruleset-split, 60+ ceiling, ceiling-not-popularity, coffin, correct-chalk-concentration, one-thesis-per-bullet, winning-structure ~19%/1.7-darts) enforced below.
- [x] Framework pre-lock checks: Anchor-Equivalence → Tommy (30.9%) vs Burns (22.6%) vs Clark (24.9%), equivalent top-salary T-10 anchors → ≥1 lineup must run Burns AND ≥1 must run Clark (Decision 2). Rule-set split → tough-course primary, 2 birdie-hedge lineups mandatory (Decision 1). Coffin → max 1 of the 8K leader-chalk per lineup. Mid-tier trap → ≤2 plays at 10–20% own per lineup.
- [x] Prior results scanned: autopsies + results.jsonl — last 3 RD4 SDs all lost at the **rule-set over-commitment to tough-course** decision (Cadillac/Truist/CJ Cup predicted tough, played birdie). This week the course has *demonstrably* played tough (observed, not predicted) — that's the forcing evidence that justifies tilting tough — but the scar tissue mandates keeping a real birdie hedge. Vendor_calibration.jsonl is empty → no weighting, mechanism only.

## Slate at a glance
| Fact | Value |
|---|---|
| Event / round | RBC Canadian Open, final round (no cut, flat 6-golfer, **NO captain, NO 1.5x**) |
| Course | TPC Toronto Osprey Valley North — par 70; reputation easy/birdie, **playing tough this week** |
| 54-hole leaders | Suber -13 · Cauley -12 · Tommy/Clark/Jesper Svensson/Garnett -11 · Burns/Fox/Yella/Horschel/Stanger -10 |
| T-10 & ties (tough-course set) | -10 or better = 11 names; the popular Hovland/Bridgeman/Lowry/MacIntyre/Fitzpatrick/Theegala block sits at **-9, T12 — NOT T-10 starters** |
| Weather | Soft/receptive (rain earlier in week); calm Sunday could re-open scoring — the live risk to a tough-course commit |
| Field | 75 golfers; chalk (≥15% own) = 14; 39 players <5% own |
| Contest | PGA Tour SD $40K Drive the Green — 150-Max, field **9,512**, **6 entries → 6 unique lineups** |

## The 4 decisions that define this slate

### 1. Rule-set: TOUGH-COURSE primary, with a mandatory 2-lineup birdie hedge
**MIX (tilted tough).** Mechanism: the course has already defended for three rounds (leader -13, +4 blow-up rounds, R2 leader collapsed) — that's *observed* scoring distribution, the one input strong enough to override the framework's default 2-2 split. But the venue is inherently easy (par 5s, 73% GIR, wide fairways) and soft from rain; a calm Sunday flips it back to a birdie-fest, which is exactly the world that beat us at Cadillac/Truist/CJ Cup.
- **Tough-course lineups (4 of 6) →** min 2 / max 3 of the T-10 (-10-or-better) set; cum own ~100%; 1–2 sub-10% structural-value starters; lean on the *cheap* T-10 leaders to afford two elite anchors. This is Jeremy's (ETR) explicit read and it's well-supported this week.
- **Birdie-hedge lineups (2 of 6) →** 3–4 of the leaderboard, cum own ~110–113%, and a **mandatory sub-5% way-back spike** (Thorbjornsen 3.2% / McGreevy 5.4%) — the slot that won every recent birdie slate and that we keep skipping. Ceiling math here assumes -19/-20: way-back guys posting -6/-7 are live.
- **If you fully commit tough and Sunday plays birdie →** the field's 8K jam all holds, the cheap leaders get caught, and the way-back guys you faded post 55+. Price that bet as real — it has cashed against us three straight RD4s. Hence the 2 hedges are non-negotiable.

### 2. The anchor — split Tommy / Burns / Clark (Anchor-Equivalence, mandatory)
**PLAY all three across the portfolio; never concentrate on Tommy.** Mechanism: Tommy $10,800 (30.9% own DK; The Stone has him 42.8%), Burns $10,900 (22.6%), and Clark $9,700 (24.9%) are equivalent-profile top-salary anchors all at -10/-11 with 60+ ceilings — the field treats them as interchangeable, so concentrating on the highest-owned (Tommy) is the exact coin-flip leak that cost CJ Cup (where Clark was the alternative that smashed). Re-validated on this week's merits, not last week's: **Clark posted the field's best R3 (-7) and leads the field in SG total (6.44) and SG:OTT** — he is independently the highest-ceiling anchor here.
- **If Tommy played →** $39,200 for 5 spots ($7,840/spot). He's the modal anchor and "choker" sentiment may shade him down — fine to own, but cap at ~2 of 6 and pair with sub-10% leverage, not more chalk.
- **If Burns played →** $39,100 for 5; he's the leverage-of-the-elite-three at 22.6% with the same ceiling — the Anchor-Equivalence requirement. ≥1 lineup.
- **If Clark played →** $40,300 for 5 ($8,060/spot) — **frees ~$1,100 vs Burns/Tommy, the key that lets you roster a SECOND leader** (e.g., Clark + Yella/Fox, or Clark + a cheap T-10). Best form on the board; ≥1 lineup, and he's my single favorite anchor.
- **If all three faded (lower-tier anchor build) →** you need a way-back winner and a near-perfect punt board; legitimate as 1 flag-plant lineup only, and never take all of Tommy/Burns/Clark to 0% (never-zero-top3 rule).

### 3. The 8K leader-chalk jam — play ONE, not the stack
**MIX → effectively PASS the stack.** Mechanism: Suber $8,200 (-13 leader, **~38% own**), Cauley $8,600 (-12, 34.8%), plus Yella/Fox/Hovland/Bridgeman all 20–22% — ETR flags the field is jamming 2+ here. Two ceiling-light 8K leaders in one lineup = coffin stacking (max-1 coffin rule) and pure field-weight with no leverage. The leaders are real (Suber/Cauley have legit 55+ ceilings as the guys in front), but you only need one.
- **If Suber played →** he's the leader with the cleanest path, but **he's the field's most-owned non-anchor at ~38% and ETR calls him "clearly overpriced"** (bumped to $8,200). Own him at most ~2 of 6; he is *the* coffin candidate if he stalls.
- **If Cauley played →** $8,600, 34.8%, but the strongest underlying (win 17.7% / top-5 65.4% on The Stone) — the better of the two leader-chalk plays if you take one.
- **If you take one 8K leader →** pair the second mid-salary slot with a **sub-10% pivot** (Keith Mitchell 8.7%, Theegala 9.9%, Pendrith 6.1% — all ETR-named) instead of a second jammed leader. That's the correct-chalk-vs-coffin distinction: own one connected leader, pivot the rest.
- **If you faded the whole 8K leader tier →** you're betting the leaders all stall on a tough course — plausible in a $20K-to-first lotto where ETR notes "the winner won't be perfect," but it's a big swim; reserve for the contrarian flag-plant only.

### 4. Where the leverage comes from — cheap T-10 starters + one sub-5% spike
**PLAY the cheap leaders as the salary engine; PLAY one way-back spike on the hedges.** Mechanism: tough-course winning structure wants 1–2 sub-25-own structural-value *starters* and ≥1 sub-10% dart (~1.9 on tough courses). The cheap T-10 set does the salary work; the spike does the ceiling work on the birdie hedge.
- **Cheap T-10 leaders → Jesper Svensson $7,500 (-11, 21.4%), Brice Garnett $6,900 (-11, 16.9%), Jimmy Stanger $7,000 (-10, 9.1%).** ETR hard-fades Jesper/Garnett purely on ownership — I partially disagree (see disagreements): they're not *leverage*, but they're genuine -11 starters whose price lets you double up on elite anchors. Use them as mechanism salary-savers, with **Stanger (9.1%) as the leverage version** of the same cheap-leader profile.
- **Sub-5% spike (birdie-hedge only) → Thorbjornsen $7,500 (3.2%, ETR flag-plant), Max McGreevy $7,200 (5.4%), Tom Kim $7,400 (4.0%).** Way-back guys; on a tough course their ceiling math is weak, so they ride ONLY the 2 birdie-shaped lineups — but on those lineups they are mandatory (the slot we skipped at PGA Champ/Truist).
- **If you skip the cheap-leader engine →** you can't afford two elite anchors and you drift into the 8K coffin jam to fill salary — the trap. The cheap leaders exist to keep you out of it.

## Player board
*(Decision-relevant set; own% = DK projections primary, with The Stone in parens where it disagrees materially. Ceiling = The Stone DK Ceil. "-N" = event score through 54.)*

| Player | Sal | Proj | Own% | Ceil | Start | Call | If played → |
|---|---|---|---|---|---|---|---|
| **Wyndham Clark** | $9,700 | 43.2 | 24.9 | 62.0 | -11 | **PLAY** | Best R3 (-7) + best SG on board; cheapest elite anchor — frees $ for a 2nd leader. Anchor-equiv requirement. |
| **Sam Burns** | $10,900 | 48.1 | 22.6 | 66.4 | -10 | **PLAY** | Lowest-owned elite anchor; the Anchor-Equivalence split vs Tommy. ≥1 lineup. |
| **Tommy Fleetwood** | $10,800 | 49.5 | 30.9 (St 42.8) | 67.0 | -11 | **MIX** | Modal anchor; own ≤2/6, pair with sub-10% leverage not more chalk. Don't concentrate. |
| Matt Fitzpatrick | $10,500 | 50.9* | 24.4 | 63.8 | -9 (T12) | MIX | A+ approach, but -9 = NOT a T-10 starter; counts against tough-course "max 3 of T-10." Anchor only on a birdie-hedge build. |
| Collin Morikawa | $9,600 | 47.9* | 12.6 | 59.5 | -7 | MIX | ETR-liked, lowest-owned of the names; -7 needs a low round. Leverage anchor on a birdie build. |
| **Bud Cauley** | $8,600 | 44.3 | 34.8 (St 22.7) | 57.9 | -12 | **MIX** | Best underlying of the leader-chalk (win 17.7%); the ONE 8K leader to take. Coffin if stacked with Suber. |
| **Jackson Suber** | $8,200 | 43.1 | 37.6 (St 15.1) | 55.7 | -13 | **MIX→PASS-heavy** | Leader, real ceiling, but ~38% owned + "overpriced." Cap ~2/6; the slate's #1 coffin. Never stack with Cauley. |
| Sudarshan Yellamaraju | $8,300 | 41.6 | 21.9 | 58.2 | -10 | MIX | Cheaper T-10 leader; fine as the single 8K piece if you skip Suber/Cauley. |
| Ryan Fox | $8,500 | 42.8 | 21.4 | 56.5 | -10 | MIX | Defending champ, -10 starter; decent but ceiling-modest — a body, not a difference-maker. |
| Viktor Hovland | $8,700 | 44.1 | 21.0 | 57.0 | -9 (T12) | PASS | Elite APP but -9 (not T-10) AND 21% owned — field-weight without the starter position. Trap tier. |
| Jacob Bridgeman | $8,100 | 41.9 | 20.0 | 56.7 | -9 (T12) | PASS | Same as Hovland: popular -9, no ceiling edge, counts against your T-10 max. |
| **Keith Mitchell** | $8,900 | 45.5* | 8.7 | 57.7 | -7 | **PLAY** | ETR-named sub-10% pivot off the 8K jam; ceiling (57.7) beats the 20%+ guys around him. |
| **Sahith Theegala** | $8,800 | 44.7* | 9.9 | 55.4 | -9 (T12) | **PLAY** | ETR-named sub-10% mid-tier; the trap-avoiding second mid-salary slot. |
| **Taylor Pendrith** | $7,900 | 42.5* | 6.1 | 53.2 | -7 | **PLAY** | Canadian, ETR-liked, sub-10% — the leverage starter that does ceiling work on tough builds. |
| Jesper Svensson | $7,500 | 38.7 | 21.4 | 54.8 | -11 | MIX | Genuine -11 starter at $7,500 — salary engine, NOT leverage (own ~21%). Use to afford 2 anchors. |
| Brice Garnett | $6,900 | 41.7* | 16.9 | 52.3 | -11 | MIX | Same: cheap -11 leader, mechanism salary-saver. ETR fades on own; I use sparingly as a connector. |
| Jimmy Stanger | $7,000 | 40.7* | 9.1 | 49.8 | -10 | PLAY | The leverage version of the cheap-leader profile — -10 starter at single-digit own. |
| Max Homa | $7,100 | 44.0* | 18.8 | 54.7 | -8 | MIX | Name-brand mid-tier; ceiling OK but 18.8% own pushes the mid-tier-trap limit. Max 1 with another 10–20% play. |
| **Michael Thorbjornsen** | $7,500 | 41.5* | 3.2 | 50.8 | -4 | **MIX (birdie-hedge)** | ETR flag-plant; way-back sub-5% spike. Rides the 2 birdie lineups only — ceiling math needs -19/-20. |
| Max McGreevy | $7,200 | 41.4* | 5.4 | 52.7 | -6 | MIX (birdie-hedge) | ETR-mentioned sub-5% spike; pairs with Thorbjornsen as the rotated way-back dart. |
| Tony Finau / Tom Kim | $7,400 | ~42 | 6.3 / 4.0 | 51.9 / 50.1 | -6 | MIX | Veteran sub-7% ceiling darts for the spike slot; rotate, don't double up unless thesis'd. |

*Proj from The Stone (DK Proj.) where the DK projections chalk table didn't surface the player. Left off the board: the dead-punt tier ($6,000–6,400 way-back, sub-2% — Savoie/Sanderson/Paul/Highsmith) — only relevant via the vendor-disagreement note below, not as standalone plays on a tough course.*

## Where I disagree with the vendors
*(vendor_calibration.jsonl is empty — no MAE weighting available; these are mechanism calls, small-sample caveat applies to all.)*
- **The Stone says Suber 15.1% own; DK projections + ETR's own article say ~38%.** My call: **~38% (full chalk), side with DK/ETR.** Mechanism: ETR's written text independently states "Suber… still taking on 38% ownership" — two of three sources converge high; The Stone's 15.1% is the outlier. Do NOT roster Suber thinking he's a leverage 15% play — he's the most-owned non-anchor on the slate.
- **The Stone has Tommy at 42.8% vs DK's 30.9%.** My call: treat Tommy as the heaviest-owned anchor (~33–43%) regardless — the disagreement only sharpens the Anchor-Equivalence case to split toward Burns/Clark.
- **ETR hard-fades Jesper Svensson (21%) and Brice Garnett (17%).** Partial disagreement: they're correctly NOT leverage, but ETR frames them as avoids — I keep them as **mechanism salary-savers** (genuine -11 starters whose price is the only way to roster two elite anchors). The leverage substitute for the same profile is Stanger (9.1%).
- **The 2nd projection source (pga-sd) pumps the punt tier +15–29% over DK** (Savoie +28%, Sanderson +29%, M. Anderson +21%, Tosti, Hao-Tong Li +17%, McCarthy, Whaley, Highsmith). My call: **ignore on the tough-course core, respect only on the birdie-hedge.** Mechanism: these are way-back, non-T-10 names; their ceiling is real only in a -19/-20 birdie world. Naming the rule-set (Truist lesson) keeps me from rationalizing them onto tough builds where -7 rounds aren't routine.
- **Where I agree with ETR:** the Mitchell/Theegala/Pendrith sub-10% pivot read off the 8K jam, the tough-course rule-set lean, and Thorbjornsen as the flag-plant spike — all adopted.

## Edges to exploit
1. **Anchor-Equivalence split (the codified edge).** Tommy 30.9% vs Burns 22.6% vs Clark 24.9% — equivalent ceilings, mispriced ownership. **Expression:** ≥1 lineup Clark-anchored ($9,700 → frees $1,100 to roster a 2nd T-10 leader like Yella/Fox), ≥1 Burns-anchored, ≤2 Tommy-anchored. Never 0% on any of the three.
2. **Take ONE 8K leader, pivot the rest to sub-10%.** The field jams Suber (~38%) + Cauley (34.8%) together — coffin stacking. **Expression:** Cauley (the better underlying) OR Suber, never both, + Keith Mitchell (8.7%) / Pendrith (6.1%) as the second mid-salary slot. Beats the field-weight 8K double.
3. **Cheap-leader salary engine to double the elite anchors.** **Expression:** Clark $9,700 + Burns $10,900 = $20,600, then Stanger $7,000 (-10, 9.1%) + Pendrith $7,900 + Mitchell $8,900 + a $6–7K dart fits under $50K — two 60+ ceilings the field can't afford together because they're paying up for the 8K jam.
4. **Correct-Chalk Concentration in ≥1 lineup.** Don't scatter the justified core. **Expression:** one tough-course lineup rosters the *connected* moderate-own core together — e.g., Clark + Cauley + Yella + Mitchell + Pendrith + a cheap leader — rather than single legs across six builds (the 5.31 dilution leak).
5. **The mandatory sub-5% spike on the 2 birdie hedges.** **Expression:** Thorbjornsen (3.2%) on one hedge, McGreevy (5.4%) or Tom Kim (4.0%) on the other, each beside 3–4 of the leaderboard at ~110% cum own — the slot that won PGA Champ/Truist and that we keep leaving empty. If Sunday calms and scoring re-opens, this is the only world these two lineups need, and it's the world the tough-course core can't reach.
