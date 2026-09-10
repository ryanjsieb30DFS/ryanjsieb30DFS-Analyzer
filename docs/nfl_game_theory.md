# NFL Game Theory — Classic + Showdown (GPP only)

_Written 2026-09-09. This is the strategy foundation for NFL, the biggest open gap in both repos. It covers DraftKings NFL Classic and NFL Showdown, tournaments (GPPs) only — no cash games, matching how you play. Sources: published research (Establish The Run, 4for4, FantasyLabs, Stokastic, RotoGrinders, the MIT DFS paper) plus a fresh empirical pass over your own 69 NFL contest-standings files (2024–25) in `~/Desktop/DFS/DFS NFL Past Slate Data/`. Everything here is written to plug into the existing framework: the Sharp Playbook envelope, set-diversity doctrine, and the anchor-equivalence rule._

---

## Part 0 — What your own data says (69 real contests, 2024–25)

Before any theory: I parsed the winner of every NFL standings file you own. Your archive splits into 41 huge contests (median field 150,000+ entries — Milly Maker size) and 28 small ones (median field ~2,300 — close to your SE/3-max world).

**The winning lineup profile, from your own files:**

| Measure | Small fields (<10k) | Large fields (150k+) |
|---|---|---|
| Winner's total ownership (8 scored slots) | ~94% | ~107% |
| Average ownership per player | ~12% | ~13% |
| Players under 10% owned | 4 | 4 |
| Players under 5% owned | 2 | 2 |
| Highest-owned player in the lineup | ~30% | ~34% |
| Winner duplicated by someone else | 2 of 69 total | (same — 67 of 69 winners were one of a kind) |

**Three reads that drive everything below:**

1. **Winners are balanced, not contrarian.** They anchor a ~30% chalk player (a player huge numbers of people used) AND carry about four sub-10% pieces. Only 1 of 69 winners had zero sub-10% players. This is the Sharp Playbook's "moderate ownership" rule showing up again, now in the winners themselves.
2. **The winning shape barely changes with field size.** Small-field winners look almost identical to Milly Maker winners. Field size changes your odds and how much uniqueness you need, not the shape of the lineup that wins.
3. **Uniqueness is nearly free and nearly mandatory.** 67 of 69 winners were completely unique in their field — even at 150,000 entries. Sharing a win splits the prize; the data says winners almost never share.

These numbers match the published Milly Maker studies (winner average ~116% total ownership, ~2.3 sub-5% players, ~1.9 players at 20%+) almost exactly. Independent data, same answer — treat this profile as solid.

---

# PART 1 — NFL CLASSIC

Roster: QB, 2 RB, 3 WR, TE, FLEX (RB/WR/TE), DST. $50,000 cap.

## 1.1 The core idea: points come in bundles, so buy the bundle

In golf, six golfers score independently. In NFL, they don't — when a QB throws a touchdown, one of his receivers catches it. Two roster spots score off one play. "Stacking" (rostering a QB with his own pass-catchers) costs no extra salary and no median projection, but it fattens the right tail: when the passing game hits its ceiling, you get paid twice. GPPs are won in the tail (Sharp Playbook rule 4), so correlation is free ceiling.

**The measured correlations, strongest first** (4for4 / FantasyLabs / RotoGrinders composites):

| Pair | Correlation | What it means |
|---|---|---|
| QB ↔ opposing QB | **+0.58** | The strongest link in football. Shootouts lift both sides — this is why you add an opposing receiver ("bring-back") |
| QB ↔ his WR1 | +0.31 to +0.46 | The best same-team partner, clearly ahead of the rest |
| QB ↔ his WR2 or TE1 | a step below WR1 | Both fine; WR3 only slightly behind them |
| RB ↔ his own DST | mild positive | Team leads → runs the clock → defense plays ahead. Wants a solid favorite (spread −3 or better) |
| RB ↔ his own WR | −0.07 | Basically zero. The old "never pair a RB with his own receivers" rule is overstated |
| QB ↔ opposing DST | **−0.46** | The worst pair on the board. Never roster a defense against your own stack |

## 1.2 What the winning stack actually is

Establish The Run's multi-year Milly Maker studies compared winning lineups to the field. The gaps are the edge:

- **Naked QB (no teammates) loses.** 6% of winners vs 17% of the field. Never do it.
- **Single stack (QB + 1 teammate) is neutral.** ~49% of winners AND ~49% of the field. It's the default, so it buys zero leverage.
- **Double stack (QB + 2 teammates) is the biggest measured edge in NFL DFS.** 41% of winners vs 29% of the field. Logic: a monster passing game (4+ TDs) almost never lands in one receiver's hands. Two catchers doubles your capture of the QB's ceiling, and the field underuses it.
- **Triple stack (QB + 3) is slightly losing in Classic.** Only ~60 offensive points exist even in a great game; a fourth same-team piece starts eating its own lineup.
- **Bring-back (QB stack + 1 opposing pass-catcher) is a real but modest edge.** 36% of winners vs 31% of field. It converts a team bet into a game bet — your shootout scenario pays both sides. Two+ opposing pieces shows no edge.
- **The TE bring-back is a documented sharp play.** Tight ends used as the bring-back appear 34% more often in winning builds. TEs are boom-or-bust, and their booms cluster in exactly the high-scoring games your stack is already betting on.

**When to skip the bring-back:** when your stack's ceiling scenario is a blowout, not a shootout — e.g., a huge favorite that wins by steamrolling. There, the opponent's garbage-time points don't arrive in the same universe where your QB smashes.

**The modal winning skeleton:** QB + 2 of his pass-catchers + 1 opposing pass-catcher (often the TE) — four of nine spots tied to one game — plus an expensive chalk RB, and leverage sprinkled through the rest.

## 1.3 Pick the game before you pick the players

Correlation runs through games, so the slate read starts with Vegas, not with players:

- **Total (expected combined points):** games totaling 48+ are natural stack targets. A single team expected to score 24+ is the threshold where stacks actually hit ceiling at meaningful rates (4for4).
- **Spread (expected margin):** small spread + high total = shootout → full game stack with bring-back. Big spread (7+) = blowout risk → favorite's RB + DST pairing instead, or the underdog's receivers alone (trailing teams throw).
- **Pace:** two fast teams = more plays = more raw material for ceilings.
- **The leverage overlay:** ownership floods the slate's top total. The sharp move is the *second or third* highest total with the same shootout shape at half the ownership — or attacking the chalk game through its less obvious pieces (WR2, TE) rather than fading it. The richest leverage in NFL is a low-owned *stack*, not a low-owned player.

## 1.4 Ownership as a price (the leverage math)

Every player has two numbers: how often he appears in the winning lineup (sims can estimate this) and how often the field uses him. **Leverage = win-rate minus ownership.** A star owned above his real win-rate is overpriced even if his projection is elite. A modest player at 2% owned with a 6% win-rate is a bargain. This is the same guide-not-gate logic already in the picker — ownership is information about price, never a rule.

**Chalk comes in two kinds:**

- **Sturdy chalk — eat it.** Ownership built on volume and role: a bell-cow RB (a back who gets nearly every carry), a WR with 12 locked-in targets. RB is the key case: it is the *only* position where winners were CHALKIER than the field, and RB ownership predicts RB points better than at any other position (0.55 correlation). Fading well-founded RB chalk is how you finish 200,000th.
- **Fragile chalk — that's the fade.** Ownership built on last week's highlight, a TD-dependent role, or a "popular defense." Winners diverge from the field hardest at QB, DST, and TE — DST is the least predictable position on the board (0.21 ownership-to-points correlation), which makes chalk defenses the most reliably overpriced thing on any slate.

**The refinement that matters: product, not sum.** Two lineups can both total 100% ownership while one is far more common — the field's builds multiply through the 40%+ guys. Winners hold more players in the 5–15% band and fewer in the 40%+ band at the *same* total ownership. Differentiate by where the ownership sits, not by dragging the sum down.

## 1.5 Roster construction, position by position

Salary first: **winners spend the full cap.** ~84% of winners spent $49,800+. Leaving money on the table has no measured edge — ETR tested it directly. Uniqueness comes from player choices, not leftover salary.

- **QB — the punt position.** Winners skew cheap: sub-$6,000 QBs won 45% of the time vs 38% field usage. QB scoring is flat relative to price, cheap QBs run low-owned, and the savings buy RB/WR studs. QB is where you find price leverage.
- **RB — pay up and eat the chalk.** Half of winners carried a $6,500+ RB. Volume is the most bankable thing in football. RB is also the winning FLEX choice (58% of winners flexed a RB).
- **WR — slight pay-up.** Winners average 1.3 receivers at $6,500+. Elite WRs are the double-stack ammunition.
- **TE — elite or punt, never the middle.** The lowest-floor, most TD-dependent position. Use the elite target-hog as a stack piece, or a cheap TE *inside* a high-total game stack (the bring-back). Winners avoid TE in the FLEX (two TEs doubles exposure to the worst distribution on the roster).
- **DST — punt with intent.** Cheap, low-owned, and never against your own stack; ideally attached to a favorite alongside its RB. The only hard rules at DST are the negative ones.

**The forced-value problem (NFL's version of the trap-shape).** When Sunday news makes a $4,000 backup a 15-touch starter, his ownership hits 40–60% — not because the field likes him, but because everyone's salary math routes through him. Game theory:
- If his volume is locked, eat it — and differentiate in what the savings *buy*. The field spends the freed salary on the same two obvious studs; buy the third.
- If his role is shaky (committee, bad matchup), the fade is one of the highest-leverage plays of the season: half the field absorbs a near-zero.
- Inactives drop 90 minutes before lock. The field stampedes onto the obvious pivot; the sharp move is the *second-order* beneficiary (the passing game that inherits the work, not just the backup everyone clicks). This is the same stampede-chalk pattern your 8/30 ownership report found in MMA — the field over-rushes late news by 15–30 points of ownership.

## 1.6 Duplication — the silent prize-splitter

NFL Classic is the most dupe-prone format in DFS: nine slots, pricing that funnels everyone through the same value plays, and optimizers converging on the same max-projection build. In early Milly Makers ~30% of full-salary lineups were exact duplicates. A 500-way duped winner turns $1,000,000 into $2,000.

What creates dupes: exactly $50,000 spent, the slate's forced value play, the obvious QB-WR1 single stack from the top total, and the chalk defense — all in one lineup. What breaks them cheaply:
1. Cap your count of 25%+ owned players (dupes are built from multiplied chalk).
2. Swap within tiers — the $5,700 WR projecting 12.8 instead of the $5,800 projecting 13.0 costs nothing and breaks thousands of copies.
3. Double stacks and TE bring-backs are inherently dupe-resistant AND +EV — structure is the cheapest uniqueness.
4. Your 69 files agree: 67 of 69 winners were unique even in 150k fields.

## 1.7 Small fields (your world: SE / 3-max / 5-max)

The published consensus (ETR/Levitan) plus your own small-field files:

- **The ideal lineup barely changes.** Your data confirms it: small-field winners carry the same 4 sub-10% pieces as Milly winners. Don't build "safer" lineups in SE — build the same balanced-with-leverage shape.
- **What changes is the field.** Small fields run chalkier (everyone funnels one bullet into their favorite build) and softer (pros can't fire 150 entries). You need less raw uniqueness and can eat more sturdy chalk; a top-1% score wins, not a top-0.001% miracle.
- **In 3-max, the three lineups answer three different questions** — three different game stacks or scenarios, never three shades of one build. This is the no-competing-lineups rule and the MIT portfolio result (below) saying the same thing.
- **Anchor-equivalence applies at QB/stack level:** if two game environments project similarly at similar ownership, at least one entry runs the alternative game.

## 1.8 The math that unifies it (MIT paper)

Hunter, Vielma & Zaman (MIT Sloan, "Picking Winners"): for top-heavy payouts, the right objective is maximizing the chance that *at least one* of your entries wins. The solution: each lineup internally correlated and high-variance (stack), lineups diversified against each other (min-unique players between your own entries), ceiling valued over average. That is the mathematical spine under the Sharp Playbook, set-diversity doctrine, and thesis-required rule — one bet per distinct "how it wins" story, each story told with maximum ceiling.

---

# PART 2 — NFL SHOWDOWN

Single game. Six spots: 1 Captain (CPT — scores 1.5x points, costs 1.5x salary) + 5 FLEX (any position, including kicker and defense). $50,000 cap. This is NOT the PGA RD4 flat format — the captain is real here.

## 2.1 The captain is the whole game

Because CPT costs 1.5x salary for 1.5x points, the multiplier itself buys nothing — every player's points-per-dollar is identical at CPT and FLEX. The captain decision is purely about two things: **whose ceiling can top the slate**, and **what the field over-pays for**.

**The QB captain trap — the most documented edge in the format.** The QB is the most popular captain in nearly every Showdown field, but he is the optimal captain only about **one time in five**. Two independent winner studies agree:

| Winning captain's position | FTA (163 winners, 2024–26) | ETR (top-1% study) |
|---|---|---|
| WR | 33% | 33% |
| RB | 28% | 27% (biggest edge vs the field's 24%) |
| QB | 21% | 24% |
| TE | 9% | — |
| DST | 6% | field uses ~2.5% |
| K | 3% | field uses ~0.8% |

Why: on every completed pass, the *catcher* scores more fantasy points than the thrower (the catcher gets the yards plus a full point for the reception; the QB gets a fraction of the yards). So the QB's own receivers systematically out-captain him. **WR and RB together are over 61% of winning captains.**

**Winning captains are not obscure.** Median winning-captain ownership was ~11%, and the average winning captain cost $13,000 and scored 23.6 CPT points. You don't need a 2%-owned captain — you need the *right member of the chalk cluster* (the WR1 or RB instead of the QB). Cheap punt captains under $7,500 only won when they had genuine slate-topping ceiling (a goal-line RB, a deep-threat WR) — never as a salary trick. Kicker captains cap your ceiling; remove them from the captain pool.

## 2.2 Correlation rules inside one game

- **Pocket QB at captain → 2–3 of his own pass-catchers in FLEX.** You don't know which receiver catches the TDs, so buy several. A *rushing* QB needs only 1 — his legs correlate with himself.
- **WR at captain → his QB in FLEX, plus at most ONE more same-team pass-catcher.** Only 8% of winners ran a CPT WR with 2+ extra same-team catchers — the ball can't go everywhere.
- **Bring-back is near-mandatory in passing builds: 89% of winning lineups** with a passing-game captain carried at least one opposing pass-catcher. Shootouts pay both sides.
- **Kicker + his own DST is a real pairing** (the "slog stack"): a low-scoring game means stalled drives → field goals, and stops → defense points. Best correlation a kicker has.
- **Kicker with his own CPT QB is anti-correlated:** touchdowns and field goals eat each other. Kickers appear in 34% of top lineups overall but only 19% next to their own captain QB.
- **DST → at most 3 players from the offense it's facing.** 89% of winners respected this.
- **Hard cap: 2 total kicker+DST pieces per lineup.** Three or more won 1% of the time. Never two kickers.
- **Two RBs from the same team** is theoretically slightly negative but so avoided by the field that it's a cheap uniqueness lever (winners doing it got ~25% fewer duplicates).

## 2.3 Build to a game script, weighted by Vegas

Every Showdown lineup should be a coherent story of how ONE game plays out. The winner data by Vegas total:

- **Slog (total 42 or less):** RB captains win 46% of the time (vs WR 31%, QB 12%). Workhorse RBs, kickers, both defenses.
- **Middle (42.5–48.5):** nearly uniform — WR 29% / RB 27% / QB 25%. Build a mixed portfolio.
- **Shootout (total 49+):** WR captains win 47%. Double stack + bring-back. One sharp wrinkle: at totals of 51+, *RB* captains showed the biggest edge over field usage — everyone rotates to pass-catchers, so the RB punching in three TDs is the leverage.

By spread: winning captains come from the favorite ~62% of the time overall — same as the field, so "captain the favorite" is not leverage. But at spreads of 7+, favorite captains win 80% of the time, while *underdog WRs* (the garbage-time catch-up script) carried 40% fewer duplicates — that's the dupe-cheap contrarian shape in blowout-priced games.

Team split of 163 winners: **3-3 (34%) and 4-2 (31%) dominate.** The 5-1/6-0 "onslaught" (nearly all one team) wins ~1 slate in 8–10 — it's the blowout bet, same reasoning as your NASCAR drafting-track chalk-dom carve-out: when one script dominates, concentration beats balance. The **2-4 split (tilted AWAY from your captain's team) is the most under-used winning shape** — only 16% of the field builds it.

## 2.4 Duplication — Showdown's defining problem

With only ~30 relevant players, the chalk build gets copied at scale. The famous case: a 2021 Packers–Lions Milly Maker winner was duplicated **231 times** — each "winner" took home ~$6,000 instead of $1,000,000. Even ordinary top-1% lineups in big fields average ~16 duplicates.

**What predicts duplicates is the PRODUCT of ownerships, not the sum** (ETR regression, the best single predictor). A lineup of six 20% players dupes far more than one mixing 40% studs with a 2% punt at the same total ownership. Also: spending exactly $50,000 raises dupes; the captain's own ownership barely matters — dupes come from the whole roster.

**Uniqueness levers, roughly cheapest first:** leave salary ($600–$3,000 unspent; the median WINNER left $1,400, and only 7% of winners spent the full cap — note this is the opposite of Classic); one sub-3% FLEX piece (41% of winners had one); a kicker (in 40% of winners, massively under-used); the 2-4 team split; two same-team RBs. One punt is a lever — three is a dead lineup (zero top-1% lineups carried 3+ min-priced players).

**The double-QB note:** rostering BOTH quarterbacks (one or both in FLEX) is described by PFF's multi-year review as "the closest thing to a cheat code" — at least one QB appears in ~96% of top lineups, and it sidesteps the QB-captain trap while keeping full exposure. Zero-QB builds win only ~5% of the time and are a large-field-only script bet (slog/blowout).

## 2.5 Small fields (your world) vs 150-max

Same conclusion as Classic, stated by Stokastic outright: the ideal 3-max lineup and the ideal single-entry lineup are the same lineup. What changes is the field around it:

- **In SE/3-max:** dupes drop to low single digits, so the dupe tax rarely justifies giving up projection. Spend nearly the full cap, take the highest win-probability correlated build, and make **one deliberate leverage decision — usually the captain** (the WR/RB over the chalk QB). Skip the sub-1% punts and the exotic anti-correlation stunts; those are large-field tools.
- **In 150-max:** dupes dominate. That's where salary-leaving, kickers, 2-4 splits, and product-ownership management earn their keep, one lineup per game script.
- The winner ownership profile: median winning lineup totaled **~167% ownership across 6 slots (~28% per slot)** — Showdown winners are notably chalkier per-slot than Classic winners (~13%), the same way your PGA RD4 SD and MMA fields run chalkier than their classic formats. Moderate chalk + one or two real leverage pieces, never an all-contrarian card.

## 2.6 Showdown doctrine in one paragraph

Captain a pass-catcher or RB from the chalk cluster (the field over-captains the QB ~5x his real win rate). Wrap the captain in script-coherent correlation: 2–3 receivers with a pocket-QB captain, a bring-back nearly always, kicker+DST only in slog builds, onslaught only as a blowout bet. Manage duplicates by the product of ownerships, scaled to field size — in your SE/3-max fields that means near-max projection with one leverage call, not manufactured weirdness.

---

## Sources

**Classic:** Establish The Run (Adam Levitan's Milly Maker winner studies, game selection), 4for4 (correlation matrices, stack thresholds), FantasyLabs / Jonathan Bales (ownership-as-price, dupe studies), Stokastic (leverage score, sim ROI), RotoGrinders, Ben Gretch (volume causes correlation), Jordan Cooper (Theory of DFS), Hunter/Vielma/Zaman arXiv:1604.01455 (the MIT portfolio paper).

**Showdown:** Establish The Run "Showdown 101" + year-in-review trend studies (captain rates, dupe regressions, leverage split by CPT/FLEX — Levitan + Mike Leone), Fantasy Team Advisors' 163-winner study 2024–26 (captain-by-total/spread tables, team splits, salary-left), PFF Showdown Primer (double-QB finding, second-RB captain leverage), Stokastic showdown guides (1.5x mechanics, correlation rules by QB type, the 231-dupe Packers–Lions case), RotoGrinders, FTN (zero-QB expected value).

**Local evidence:** the user's own 69-contest NFL standings archive (`~/Desktop/DFS/DFS NFL Past Slate Data/`), analyzed 2026-09-09; shark-envelope numbers from `rules/shared/sharp_playbook.md`.
