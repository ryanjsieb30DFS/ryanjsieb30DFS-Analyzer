# NFL Classic Framework

**Seeded 2026-09-12 from docs/nfl_game_theory.md Part 1 + docs/nfl_support_scope.md contest profile. Updated 2026-09-12 with the ETR Classic research digest (`docs/etr_research/DIGEST_2026-09-12_nfl_classic.md`). User-approved 2026-09-12.**
Sources: Establish The Run (Adam Levitan's Milly Maker winner studies, game selection, salary-left test), 4for4 (correlation matrices, stack thresholds), FantasyLabs / Jonathan Bales (ownership-as-price, dupe studies), Stokastic, RotoGrinders, Hunter/Vielma/Zaman (MIT "Picking Winners"), plus an empirical pass over the user's own 69 NFL contest-standings files (2024–25, `~/Desktop/DFS/DFS NFL Past Slate Data/`). Numbers below are cross-vendor winner data plus that archive — the local autopsy ledger starts at zero Classic slates.

## The format

DK main slate. Nine spots: 1 QB, 2 RB, 3 WR, 1 TE, 1 FLEX (a RB, WR or TE), 1 team defense (DST). $50,000 cap, players from at least two games. No captain, no multiplier. Lineup identity is the set of nine names.

NFL scoring note (unique among this repo's sports): **0.0 FPTS is a real score** (a covered WR3, a benched player) and **a DST can go negative**. Never read a 0.0 as a scratch. The tier-calibration scratch exclusion carries an nfl carve-out in `src/pool_calibration.py`; Classic keeps the salary-aware counterfactual (there is no captain to mis-price).

## The build target — what the user's own small fields say

28 of the 69 archived contests are small fields (median ~2,300 entries — the SE/3-Max world). The winner there looks like this:

| Measure | Small fields (<10k) | Large fields (150k+) |
|---|---|---|
| Winner's total ownership (8 scored slots) | ~94% | ~107% |
| Average ownership per player | ~12% | ~13% |
| Players under 10% owned | 4 | 4 |
| Players under 5% owned | 2 | 2 |
| Highest-owned player in the lineup | ~30% | ~34% |
| Winner duplicated by someone else | 2 of 69 total | 67 of 69 winners were one of a kind |

Three reads: winners are balanced, not contrarian (one ~30% anchor AND about four sub-10% pieces; only 1 of 69 had zero sub-10% players); the shape barely changes with field size; uniqueness is nearly free and nearly mandatory. This is a RATE across winners — never a per-lineup quota (the codified sharp-envelope lesson applies from day one). `rules/shared/shark_baseline.json` carries an `nfl` block mined from these 28 files (`scripts/mine_nfl_history.py`); the Grade tab reads its envelope as information.

## The large-field archive (41 Milly-size contests, mined 2026-09-12)

The other 41 files are large fields (median ~147,000 entries). They do NOT feed the shark envelope — the user's Classic play is small-field — but they were mined the same way (`rules/nfl_classic/_mining/slates.csv` holds all 69 rows) and they tell the same story:

| Measure | Small (<10k, n=28) | Large (n=41) |
|---|---|---|
| Winning score, median (min / max) | 215 (182 / 239) | 233 (163 / 282) |
| Rank-1 winner: ownership per slot | 12.4% | 14.7% |
| Rank-1 winner carried a sub-5% piece | 92% | 80% |
| Rank-1 winner: top anchor exposure | 0.30 | 0.37 |
| Rank-1 winner unique in its field | 97% | 99% |
| Tracked sharks in the field (of n) | 28 | 41 |
| Shark envelope: own/slot · sub-5% piece · anchor · unique | 13.7 · 88% · 0.38 · 98.6% | 14.9 · 78% · 0.34 · 98.1% |

Reads: the large-field winner is slightly CHALKIER per slot (14.7 vs 12.4) and needs the sub-5% piece a little less often — a bigger field is won by a higher raw score, not by more weirdness. The winning score runs ~18 points higher because 147,000 tickets sample the tail deeper. Uniqueness is near-total at both sizes. The user's own entries appear in 2 of the 41 large contests (12.7% per slot, a sub-5% piece both times, unique both times) and in none of the small ones, so the small-field user envelope starts empty. These are RATES across winners, never per-lineup quotas.

## Correlation — points come in bundles

Stacking (a QB with his own pass-catchers) costs no salary and no median projection; it fattens the right tail because two roster spots score off one play. Measured pairs (4for4 / FantasyLabs / RotoGrinders composites):

| Pair | Correlation | What it means |
|---|---|---|
| QB ↔ opposing QB | **+0.58** | The strongest link in football. Shootouts lift both sides — the bring-back rationale |
| QB ↔ his WR1 | +0.31 to +0.46 | The best same-team partner |
| QB ↔ his WR2 or TE1 | a step below WR1 | Both fine; WR3 only slightly behind |
| RB ↔ his own DST | mild positive | Team leads → runs the clock → defense plays ahead. Wants a favorite of −3 or better |
| RB ↔ his own WR | −0.07 | Basically zero; "never pair a RB with his receivers" is overstated |
| QB ↔ opposing DST | **−0.46** | The worst pair on the board. Never roster a defense against your own stack |

## The winning stack (checks, never gates)

ETR's multi-year Milly Maker studies, winners vs field:

1. **Naked QB (no teammates): 6% of winners vs 17% of the field.** A losing shape.
2. **Single stack (QB + 1): ~49% of winners AND ~49% of the field.** Neutral — the default buys zero leverage.
3. **Double stack (QB + 2): 41% of winners vs 29% of the field.** The biggest measured edge in the format: a 4-TD passing game almost never lands in one receiver's hands.
4. **Triple stack (QB + 3): slightly losing in Classic.** Only ~60 offensive points exist even in a great game.
5. **Bring-back (stack + 1 opposing pass-catcher): 36% of winners vs 31% of the field.** Real but modest; two or more opposing pieces shows no edge. **The chalk bring-back is fine INSIDE the stack** even at very high conditional ownership (Chase was 66% on Caleb Williams stacks, Week 9 2025, and simmed as well as the 13%-owned pivot) when three things hold: he is the best raw-and-value play at his position, he fits the roster without forcing anything else, and the QB he rides with is not the chalk QB (Caleb was 11%, the 4th-highest-owned QB). **The same chalk WR outside his stack is a negative** (Chase simmed negative on 11 of 15 non-Caleb QBs). A chalk pass-catcher from the chalk game belongs in the stack he correlates with, or not at all.
6. **TE bring-back: +34% in winning builds.** TE booms cluster in exactly the high-scoring games the stack is already betting on.
7. **Skip or fade the bring-back only when the fade buys something.** A blowout-shaped ceiling story (huge favorite steamrolling) is one reason. The other is roster construction: in a 100-entry contest (Week 10 2025) the one Mac Jones stack WITHOUT the obvious Nacua bring-back worked because the freed salary bought three Tier-1 RB values and a WR slot for a mini-correlation, while the nine stacks WITH Nacua were forced into double-TE builds on a slate with no TE value. **Small fields are where this fade counts most** — more opponents hand-build by the correlation rulebook, and one lineup without the bring-back among ten stacks is a measurable edge. A direct 1-for-1 pivot (Nacua for Chase) that changes nothing else raises variance at the same EV; that is allowed, not required.

**Tool rulebook — how BOTH tools count a stack (user decision 9/12/26).** The Sim (builder, sim, modeled field) and the Analyzer (autopsy, counterfactual) share one definition file, `src/nfl_classic_defs.py`, kept byte-identical in both repos by a test. In that rulebook a **stack mate** is ANY non-defense teammate of the quarterback — running back, receiver or tight end — and a **bring-back** is ANY non-defense player from the quarterback's opponent. A defense is never a stack mate or a bring-back. A **game** is the unordered team-and-opponent pair; road and home markers ("@KC", "VS KC") are stripped so both tools see the same game. Every defense spelling a vendor uses ("D", "DEF", "D/ST", "DS") folds to DST and "PK" folds to K. The ETR rates quoted in this document count pass-catchers (receivers and tight ends) only, so a rate the tools compute is not directly comparable to an ETR rate; the modeled field is still drawn with a pass-catcher tilt because that is the basis its multipliers were calibrated on.

**The modal winning skeleton:** QB + 2 of his pass-catchers + 1 opposing pass-catcher (often the TE) — four of nine spots tied to one game — plus an expensive chalk RB, with leverage sprinkled through the rest.

## Pick the game before the players

- **Total:** games totaling 48+ are natural stack targets; a team expected to score 24+ is where stacks reach ceiling at meaningful rates (4for4).
- **Spread:** small spread + high total = shootout → full game stack with bring-back. Spread of 7+ = blowout risk → the favorite's RB + DST pairing, or the underdog's receivers alone (trailing teams throw).
- **Pace:** two fast teams = more plays = more raw material.
- **Team intent:** ETR's Pass Rate Over Expectation (PROE — how much more a team throws than the game situation predicts) is the stable half of future pass rate; game script is the volatile half. Two high-PROE teams in one game is the shootout shape; a high red-zone PROE leans that team's touchdowns to WR/TE. 2026 numbers start after Week 2 (`docs/etr_research/2026-09-12__nfl_classic__etr_pass_rate_over_expectation.pdf`).
- **Dome tiebreaker:** in domes QBs score ~12% more, WR/TE ~6% more (receiving TDs +22%/+33%), and DSTs ~15% LESS. ETR's projections already carry most of this — it breaks ties between two otherwise-equal game environments and counts against the dome DST; it is never added on top.
- **The leverage overlay:** ownership floods the slate's top total. The sharp read is the second or third highest total with the same shootout shape at half the ownership, or attacking the chalk game through its less obvious pieces (WR2, TE). **The richest leverage in NFL is a low-owned stack, not a low-owned player.**

## Ownership as a price

Leverage = win-rate minus ownership — guide-not-gate, ownership is information about price. Chalk comes in two kinds:

- **Sturdy chalk — eat it.** Ownership built on volume and role: a bell-cow RB, a WR with 12 locked-in targets. RB is the only position where winners were CHALKIER than the field, and RB ownership predicts RB points better than at any position (0.55). Fading well-founded RB chalk is how you finish 200,000th.
- **Fragile chalk — that's the fade.** Ownership built on last week's highlight, a TD-dependent role, or a "popular defense." Winners diverge from the field hardest at QB, DST and TE; DST is the least predictable position on the board (0.21), which makes chalk defenses the most reliably overpriced thing on any slate.
- **Product, not sum.** Two lineups can both total 100% ownership while one is far more common — the field's builds multiply through the 40%+ players. Winners hold more players in the 5–15% band and fewer at 40%+ at the SAME total ownership.

## Roster construction, position by position

- **Salary: winners spend the full cap** — ~84% at $49,800+. ETR tested leaving money directly and found no edge. Uniqueness comes from player choices, not leftover salary (the OPPOSITE of Showdown).
- **QB — the price-leverage spot.** Sub-$6,000 QBs won 45% vs 38% field usage; QB scoring is flat relative to price, cheap QBs run low-owned, and the savings buy studs.
- **RB — pay up and eat the chalk.** Half of winners carried a $6,500+ RB. RB is also the winning FLEX (58% of winners flexed a RB).
- **WR — slight pay-up.** Winners average 1.3 receivers at $6,500+; elite WRs are the double-stack ammunition.
- **TE — elite or punt, never the middle.** The lowest-floor, most TD-dependent position: the elite target-hog as a stack piece, or a cheap TE INSIDE a high-total game stack (the bring-back). Winners avoid TE in the FLEX.
- **DST — punt with intent.** Cheap, low-owned, never against your own stack; ideally attached to a favorite alongside its RB. The only hard rules at DST are the negative ones.

**The forced-value problem (this format's trap-shape).** When news makes a $4,000 backup a 15-touch starter, his ownership hits 40–60% because everyone's salary math routes through him:
- Volume locked → the field eats him; differentiate in what the savings BUY (the field spends the freed salary on the same two obvious studs; the third is the read).
- Role shaky (committee, bad matchup) → half the field absorbs a near-zero; one of the highest-leverage spots of the season.
- Inactives drop 90 minutes before lock; the field stampedes onto the obvious pivot. The sharp read is the SECOND-ORDER beneficiary (the passing game that inherits the work). Same pattern the 8/30/26 MMA ownership report measured: the field over-rushes late news by 15–30 points of ownership.

## Duplication — a check, not an engine, at these field sizes

Classic is the most dupe-prone format in DFS (nine slots, pricing that funnels through the same value plays, optimizers converging on max-projection). What creates dupes: exactly $50,000 + the slate's forced value play + the obvious QB-WR1 single stack from the top total + the chalk defense, all in one lineup. Cheap breakers: cap the count of 25%+ owned players; swap within tiers (the $5,700 WR projecting 12.8 instead of the $5,800 projecting 13.0); double stacks and TE bring-backs are inherently dupe-resistant AND +EV. **In the user's small fields a chalk build dupes in low single digits** — name the dupe magnet once and move on; never buy manufactured weirdness for it.

## The user's contest profile

**Classic = the smallest fields the bankroll allows** (SE / 3-Max / 5-Max; the 28-contest small-field archive, median ~2,300 entries, is the representative set). Lotto-style judgment: ceiling only. What that settles:
- The ideal lineup barely changes with field size — build the same balanced-with-leverage shape, never a "safer" SE lineup.
- What changes is the field: chalkier (everyone funnels one bullet into the favorite build) and softer (pros can't fire 150 entries). Less raw uniqueness is needed and more sturdy chalk is eatable; a top-1% score wins.
- **In 3-Max, the three lineups answer three different questions** — three game stacks or scenarios, never three shades of one build (no-competing-lineups rule, MIT portfolio result).
- **Anchor-Equivalence applies at the QB/stack level:** two game environments projecting similarly at similar ownership → at least one entry runs the alternative game.
- No Classic MME; the big-field attack step stays off unless a 20-Max/150-Max contest is actually declared.

## The math that unifies it (MIT paper)

Hunter, Vielma & Zaman: for top-heavy payouts the right objective is maximizing the chance that at least one entry wins. Each lineup internally correlated and high-variance (stack), lineups diversified against each other (min-unique players), ceiling valued over average. That is the spine under the Sharp Playbook, the set-diversity doctrine, and the thesis-required rule.

## Pre-lock checks (information for the strategy writer, not gates)

- Which 2–3 game environments are stackable this week (total, spread, pace), and what does each stack cost in ownership?
- Does each built lineup name its stack shape (QB + how many teammates, bring-back or not) and the game story behind it?
- Is the DST facing the lineup's own stack? (The −0.46 pair.)
- **The three ownership checks** (ETR's post-lock autopsy of a ~275-entry SE field, 35 contests): did the CORRELATED pieces come in above projection? how many lineups share the chalk COMBO (count them — 48 vs 80 lineups is a different contest)? did the DIFFERENTIATION piece stay low? Expect the best pre-lock lineups to give back ~20 points of sim ROI once the real field is in; a lineup that fails all three checks craters, one that passes all three improves.
- **Metrics:** Win% / Top 1% / Top 10% decide; cash rate is calibrated but over-confident at the very top; the sim separates bad from good well (positive-sim lineups won 1.65x chance, negative 0.57x) and very good from best poorly (the three best sim buckets posted the same real ROI) — pick inside the good set, never by ROI rank. AVG and CEILING points are irrelevant; some weeks the winner is a low-scoring slate.
- Which chalk is sturdy (volume) and which is fragile (highlight / TD-dependent / popular DST), with the number that says which?
- Is there a forced-value play, is his role locked, and who is the second-order beneficiary the field is missing?
- Salary used: is the lineup at $49,800+, and if not, why?
- Anchor-Equivalence: which QB stacks / game environments sit at similar projection and ownership and are substitutable?
- Dupe magnet: the exact-$50K + value + top-total single stack + chalk DST build — does any entry carry all of it?
- In 3-Max / 5-Max: do the entries tell different game stories?
