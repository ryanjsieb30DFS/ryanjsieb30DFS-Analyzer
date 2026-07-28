# The DFS Research Library

*Compiled 2026-07-27 from a six-track deep research pass: GPP theory, MMA, NASCAR, PGA, simulator methodology, and how the pros operate. Written plainly on purpose. Every claim names its source. Anything uncertain says so.*

**How to use this:** this is the reference shelf, not the weekly plan. The slate strategy still comes from each week's articles and projections. Read the chapter for the sport you're playing, and the "What this means for us" section when thinking about the tools. Nothing in here changes the framework automatically — the candidate rules at the bottom are proposals for you to approve or reject.

---

## Chapter 1 — Who actually wins at DFS, and why

The famous McKinsey study found that **1.3% of players won 91% of the profits** (2015 MLB data). The winners' edge came from tools, process, and contest choice — not from knowing sports better than everyone else. (McKinsey, "The Curse of Too Much Skill")

What the documented winners have in common, across every interview found:

1. **A fixed pre-lock routine.** Research, build, check, lock — same order every time.
2. **They treat ownership (how many teams pick a player) as equal in importance to projection** (how many points he'll score). Balancing those two IS the skill, per Alex Baker, a former #1-ranked player.
3. **They pick their contests as carefully as their players.** Adam Levitan of Establish The Run: "the easiest and fastest way to increase your ROI is through game selection."
4. **They review process, not profit.** Xandamere, a small-slate specialist, grades himself on what percent of his lineups land in the top 10% / 5% / 1% of contests — not on whether they cashed. This is exactly your Analyzer's percentile-based approach, independently invented by a documented winner.
5. **The apex players are in YOUR sports.** The player who hit #1 overall in 2022 (moklovin) did it by being elite in PGA and NASCAR at once; another perennial top-5 (papagates) is elite specifically in MMA. Those pools stayed softer than NFL/NBA — which is why individual edge still exists there.

**The losing posture, per every source:** casual multi-entry into the big flagship tournaments. The winning postures are either industrial-scale mass entry (not your game) or **concentrated small-field specialization (your game, and Levitan's exact recommendation).**

---

## Chapter 2 — The math of winning a GPP

### Leverage: why low-owned players are worth more than their projection

Your score only matters compared to the field. When a 35%-owned player scores big, a third of the field rises with him and nobody gains. When an 8%-owned player with the same ceiling scores big, you jump over everyone who skipped him. (Stokastic)

The cleanest published formula (4for4's "leverage score"): figure out how often a player REALLY hits a tournament-winning score, convert that into what his ownership SHOULD be, and compare to what it WILL be. Own more than the field when deserved ownership is higher than actual; own less when it's lower. **Chalk is correct when it deserves its ownership** — that's the whole rule. The academic version (Haugh & Singal, published in *Management Science*): deliberately picking less-popular but still-high-scoring players is provably optimal in top-heavy contests.

### Duplication: the silent tax

If your winning lineup is shared by 10 other people, first place splits 11 ways. The best public numbers (ETR's Showdown study):

- **Multiply the ownerships together — the product predicts duplicates better than anything else** (r² = 0.43). A lineup of 20% + 20% players duplicates far more than 39% + 1%, even though both "add up" to 40%.
- **One truly low-owned player collapses the product.** A single sub-5% piece does more anti-duplicate work than trimming several mid-owned pieces.
- Using every dollar of the $50K cap makes duplication much worse (~65% unique at full salary vs 89-98% when leaving $500-1,000).

**Where dupes matter for you:** MMA and NASCAR (small player pools, concentrated ownership). Golf barely dupes (150+ players spread ownership thin). This is exactly what your Sim's own 577-contest corpus found — the research and your data agree.

### Winning lineups are chalk-anchored AND differentiated — both at once

The largest public study of winning lineups (Levitan's Milly Maker data, NFL large-field):
- 88% of winners had at least one player over 25% owned.
- Winners averaged **1.9 chalk players (20%+) AND 2.3 low-owned players (under 5%)** in the same lineup.
- All-contrarian lineups lose. All-chalk lineups split prizes. The winning shape is: correct chalk core, one or two deliberate low-owned pieces.

**The field-size dial:** how many low-owned pieces you need scales with field size. In the 150,000-entry Milly Maker you need several. In your 500-2,000-entry single-entry contests, you need one or two — and small-field winners run much chalkier (a documented $200 single-entry PGA winner had just ~50% total ownership, which is very chalky for golf). **Your own logged MMA data says the same thing: your SE winners were six mid-owned favorites with zero darts.** Trust your data — it's calibrated to your exact fields.

### Payout shape decides how brave to be

Top-heavy payouts (most money to 1st) reward variance and uniqueness. Flat payouts reward being merely good. The sharp move is BOTH: build bravely, but *enter contests with the flattest payout curves you can find* — minimum cash of 2x your entry, and 10th place paying about 10% of 1st. (Levitan)

---

## Chapter 3 — Contest selection (the most under-used edge)

Levitan's screens, with real numbers:

- **Rake** (the site's cut) runs ~15-16% on small-stakes tournaments, ~13-15% on single-entry, and drops to ~10-12% at higher buy-ins. At 15% rake you need a 17.6% edge just to break even. The $100 single-entry golf "Long Drive" at 9.99% rake vs the standard 15.92% GPP — that gap IS a long-run edge by itself.
- **Single-entry fields are the softest**: "there simply aren't 8,000+ competent players on the site." Multi-entry contests at the same price are sharper because pros multiply themselves.
- **Sweet spot: 1,000-6,000 entry single-entry and 3-max contests** with the flat-top payout screens above. This is precisely your SE/3/5-max lane — the research says you're already fishing in the right pond.
- Small-to-medium fields also mean your results converge to your true skill faster.

### Bankroll and variance — why you can't read your own ROI

The best variance study found (RotoGrinders, million-trial simulation): a player with a TRUE +19% ROI in top-heavy tournaments still has a **48% chance of being down after 100 entries** and a 17% chance after 1,000. It takes roughly 2,600 entries before "am I actually winning?" becomes statistically readable. At your volume (a handful of entries per slate), ROI will not converge within a season. **Percentiles and process metrics are the only readable signal at your sample size** — your no-ROI-tracking rule isn't a preference, it's statistics. Modern bankroll guidance for tournament-only players: roughly 2-5% of bankroll per slate.

---

## Chapter 4 — MMA

### The scoring anatomy (verified across four sources)

- Significant strike +0.4, takedown +5, knockdown +10, control time +1.8/minute.
- **The finish bonuses decide slates**: Round 1 win +90, Round 2 +70, Round 3 +45, decision +30, plus +25 for a sub-60-second finish. The same win is worth 60 more points if it comes in round 1 instead of the scorecards.
- A losing fighter scores ~15-40. A grappler's decision ≈ 88+; a striker's decision struggles to reach 70. **Grapplers have more ways to score** (takedowns + control + ground strikes), so they carry a better floor at a similar ceiling.

### Base rates worth knowing (GrapplerHQ, 8,591 UFC fights)

- **27% of all UFC fights end in round 1** — the +90 bonus is common, not rare.
- Finish rates by weight: heavyweight 66%, light-heavy 61%, middleweight 59%, welter/lightweight ~51%, featherweight and below ~45%, women's divisions 33-39%.
- Apex small-cage events finish ~8-12 points more often than arena cards.

### What wins, and the field-size warning

Public GPP doctrine (large-field): six winners, finishes not decisions, underdogs whose finish odds (ITD) are shorter than +200, and the five-round-fight rule below. The most striking stat found: **the underdog side of five-round fights appeared in ~80% of winning lineups while carrying only ~34% of the ownership** (FantasyLabs, 15-fight sample — small, but large edge).

**But calibrate to YOUR fields:** most of that doctrine is written for 100,000-entry contests. Your own validated lesson — SE winners are six mid-owned converting favorites, zero darts, differentiation from the 15-30% ownership tier — is the SE-calibrated truth and takes precedence. The two pieces that DO transfer cleanly to small fields: the five-round-dog edge, and the +200 ITD filter as the bar any underdog must clear before consideration.

### Process notes

- Never roster both fighters in one fight (only ~5% of optimal lineups ever contained both).
- Main events average ~79% combined ownership, yet a quarter of winning lineups skip the main event entirely — the field's most reliable over-concentration.
- Watch Friday weigh-ins; short-notice replacement fighters get finished at an alarming rate (leverage on their opponent's finish odds).
- Trivia worth knowing: your two vendors share a brain — Brett Appley founded DailyFan AND leads ETR's MMA product.

---

## Chapter 5 — NASCAR

### The scoring anatomy (verified)

- Finish points 45 down to 1; place differential ±1 per position gained/lost; laps led 0.25 each; fastest laps 0.45 each.
- **The asymmetry that drives everything:** a pole-sitter who wrecks scores about −38. A last-place starter literally cannot go negative. Front-starters carry all the downside; deep starters have a protected floor.

### Track type sets the strategy (dominator points available per race)

| Track type | Dominator pts in play | The build |
|---|---|---|
| Superspeedway (Daytona/Talladega) | ~180-200, but scattered | No dominators. Stack deep starters for place differential. Pure chaos, GPP only |
| Intermediate (1.5-mile) | ~187 | 1-2 dominators + 2-3 place-differential plays + value |
| Short track (Bristol/Martinsville) | 280-350 | TWO dominators, leave room for a third. One driver can lead 300+ laps |
| Road course | 42-90 | 0-1 dominators; finish position + specialists; pit strategy adds hidden variance |

### Crash reality (feeds our wreck model)

League-wide: ~5 DNFs per race, ~68% of them crashes (Dr. Diandra, buildingspeed.org). But crash risk concentrates violently by track: Daytona alone produced 18% of a season's DNFs; single wrecks of 20-28 cars happen at superspeedways. Per-driver crash history is real and trackable (one driver: 65% career Daytona DNF rate). **Implication for our sim: the wreck-mix probability should eventually vary by track type — superspeedway q is a different animal from a road-course q.**

### What wins, and where the field errs

- Winning skeleton: one correct dominator + 2-3 place-differential hits the field didn't share. ~300+ DK points typically wins tournaments.
- NASCAR is the chalkiest DFS sport (36-40 drivers only; studs hit 40-60% ownership). You can't win with six chalk — but you also can't skip the right dominator. Differentiate on the PD slots, not the dominator slot.
- The field's repeated mistakes: over-owning front-starting brand names at superspeedways, chasing single-lap practice speed (it predicts qualifying, not race pace — **10-lap averages are the dominator-scouting stat**), and piling onto the one obvious salary value at 35%+.
- Data gap worth knowing: nobody publishes NASCAR winning-lineup ownership studies the way NFL sites do. Our own captured-slate data is genuinely rare evidence — keep logging.

---

## Chapter 6 — PGA (Classic + Round 4 Showdown)

### The scoring anatomy

- Birdie +3 vs par +0.5: **one birdie is worth six pars.** Birdie-bogey beats par-par. DK golf pays volatility, not careful golf.
- Finish points (+30 for the win, decaying fast below the top 10) are only ~20-25% of even a winner's score. Birdie volume is the engine.
- Large-field winning scores run ~500-540 (six golfers averaging ~85-90), which effectively requires all six through the cut.

### The cut and the winning shape

- Only **~9% of entered lineups get all six through the cut** (FantasyData). Losing one golfer forfeits ~8% of your lineup's holes plus all his finish points. Winning lineups are almost always 6/6.
- ETR's winning-lineup dataset (large-field): 96.7% of winners had 3+ golfers under 15% ownership; **89.2% had at least one under 5%**; cumulative ownership under 85%. Small-field calibration again: their profiled single-entry winner ran ~50% cumulative — in small fields chalk condenses and "moderately different" wins.

### Golfer evaluation — what the sharpest model says (Data Golf)

- Skill weighting: ~70% of the predictive weight sits on a golfer's last 50 rounds — long windows with decay, not hot-form streaks.
- **Ball-striking persists; putting doesn't** (persistence: driving 1.2, approach 1.0, around-green 0.9, putting 0.6). A golfer running hot via putting is regression bait; hot via approach play is real.
- **Course history is ~0.1 strokes of signal** — mostly noise the field overprices into ownership. Course *fit* is real but tiny (±0.07 strokes for most golfers). Use both as ownership-fade signals more than projection inputs.
- Ownership explains only ~8% of golf scoring variance, and within a salary tier, chalk golfers show NO more ceiling than low-owned ones (RotoViz) — same-tier pivots off chalk are nearly free leverage.

### Waves and weather

Morning waves play 0.15-0.30 strokes easier even in neutral weather; wind above 10-15 mph adds ~0.3-0.5 strokes. A bad draw costs half a stroke over two days without a bad shot. Weather is an adjustment and an ownership lever, not a thesis — overreact only to big forecast gaps. (Our sim's wave-correlation shock is the right structure per Data Golf's own model.)

### Round 4 Showdown (your Sunday format — flat six golfers, no captain)

- Amplified scoring: birdie +5.75, par +1.5, bogey −1.8. R4 showdowns DO award finish points, but the whole 1st-to-15th spread is 8 points ≈ 1.4 birdies. **A birdie-maker shooting 65 from 30th beats a leader parring his way to the trophy.** Leaders are tiebreakers, never the thesis.
- Buy golfers whose Saturday was good ball-striking + bad putting (positive regression); ownership clumps on the leaderboard top, so birdie upside further down the board is the leverage.
- Leaving salary unspent is explicitly fine in this format (one round doesn't need max projection, and short fields dupe hard).

---

## Chapter 7 — What the sim industry does (and how our tools compare)

The consensus across SaberSim, THE SOLVER, Stokastic, and the academic papers:

1. **Simulate events, not point curves.** Fight outcomes, race outcomes, the cut — let scores fall out of the event. *Our MMA win/loss model, golf cut model, and the new NASCAR wreck-mix are exactly this pattern.*
2. **Correlation comes from shared worlds** — one coherent slate outcome per sim, not bolted-on correlation numbers. *Our golf wave shocks and MMA zero-sum fights follow this; NASCAR's dominator Dirichlet (zero-sum laps budget) is the same idea and already built, waiting on a dominator data column.*
3. **Shrink variance estimates.** Data Golf estimates each golfer's volatility, then pulls it hard toward the tour average because raw individual variance estimates are noisy. *Worth considering for our stddev derivations.*
4. **Field models must match the contest** — stakes bracket, format, field size, with dupes counted. *Our consensus-mass field fit and per-size bands are this, gated on data.*
5. **Trust sim rankings, not sim numbers.** The only public calibration study (ETR's, 35 weeks of a real SE contest) found sims pick winners at 1.65x random — but the ROI numbers themselves were only directionally right. *Your "sim rank not gospel" rule, independently confirmed.*
6. **Portfolios should cover different worlds, not maximize a metric** — the academic result (Hunter/Vielma/Zaman) proves top-N-by-ROI is formally suboptimal; sequential building with overlap caps and a variance floor is the principled recipe. *Our diversifier's world-coverage objective is the same math.*
7. Best code-level reference for our exact stack: chanzer0's open-source PGA-DFS-Tools (Gaussian mixtures for the cut, ownership-sampled fields, payout-curve ROI).

---

## Chapter 8 — The recreational leaks (the field's habits we exploit)

The documented list, each one an edge for whoever doesn't have it:

1. **Recency bias** — the field over-owns whoever spiked last slate. Compare the spike to the long-term baseline.
2. **Crowded "sneaky" punts** — a real leverage play has real projection AND low ownership; a coin-flip punt everyone found is the worst of both.
3. **Slow reaction to late news** — the window between news and field adjustment is pure edge (weigh-ins, qualifying wrecks, withdrawals).
4. **Over-owning popular narratives** — TV fights, leaderboard names, track-history darlings.
5. **Same lineup for cash and tournaments** — different games entirely.
6. **Duplication blindness** on small pools (MMA, showdown) — max salary + the obvious build = sharing your prize.
7. **Bad contest selection** — playing pro-infested formats and never checking rake.

Your autopsies already catch several of these in your own play — that loop is the moat.

---

## Chapter 9 — Candidate rules for the framework (PROPOSALS — nothing applies until you approve)

1. **Five-round-fight rule (MMA):** in every five-round fight, explicitly evaluate the underdog side before lock — the 80%-of-winners-at-34%-ownership stat says this is the most reliable structural leverage in MMA. *(Would slot into the MMA pre-lock checks.)*
2. **ITD +200 bar (MMA):** an underdog only enters consideration if his inside-the-distance odds are shorter than about +200 — "if he wins, does he finish?"
3. **10-lap-average rule (NASCAR):** dominator picks must cite 10/15-lap practice averages, never single-lap speed.
4. **Putting-regression flag (golf):** tag golfers whose recent form is putting-driven (fade candidates) vs ball-striking-driven (trust candidates) in the player board.
5. **Course-history discount (golf):** treat course history in articles as an ownership signal, not a projection signal — worth ~0.1 strokes, priced like it's worth a stroke.
6. **Rake line in contest declarations:** when declaring contests in the Analyzer, note the rake; prefer structures with 2x min-cash and 10th ≈ 10% of 1st.
7. **R4 showdown leader discount:** leaderboard position is worth at most ~1.4 birdies of scoring — the strategy should always say plainly that Sunday's points come from birdies, not from being ahead.

## Chapter 10 — Tool upgrade ideas surfaced by the research (backlog, not commitments)

- **Track-type wreck bands**: when the wreck-mix gate clears, the crash probability should eventually differ by track type (Daytona ≠ road course). Needs more captures per type — far future.
- **frcs.pro** publishes historical DK points by driver/track — an external calibration set for the NASCAR sim's dominator distributions.
- **Variance shrinkage** (Data Golf pattern): pull per-player derived stddevs toward the slate average before simming.
- **Weight-class finish-rate priors (MMA)**: the GrapplerHQ base rates could sanity-check vendor finish odds on thin cards.
- **Dominator data column**: the correlated NASCAR Dirichlet sim is already built and dormant — a laps-led projection source would light it up.

## The source shelf (the best of ~40 sources read)

- **Levitan's Game Selection (ETR)** — contest choice with real rake numbers. The single most actionable doc for your format.
- **ETR Winning Milly Maker Trends** — the base rates of winning lineups (with the field-size caveat).
- **ETR Showdown 101** — the duplication math (ownership products).
- **Data Golf's model methodology** — the sharpest public sports model writeup; golf evaluation truth.
- **Haugh & Singal (Management Science) + Hunter/Vielma/Zaman (MIT)** — the academic proofs behind leverage and portfolio construction.
- **FantasyLabs five-round UFC study** — the 80/20 five-round-dog stat.
- **Dr. Diandra's buildingspeed.org** — NASCAR crash/DNF base rates.
- **Xandamere's OWS interview** — the specialist's process, including percentile-based self-review.
- **RotoGrinders tournament-variance simulation** — why ROI is unreadable at low volume.
- **SaberSim's methodology docs + chanzer0's open-source tools** — the sim state of the art, commercial and code.

## Honest caveats

- Large-field vs small-field calibration is the #1 way to misread this document. Most public GPP content is written for 100,000-entry fields. Your contests are 500-6,000. Where your own logged data disagrees with public doctrine (MMA darts, golf dupes), **your data wins — it's measured on your exact fields.**
- DK scoring values get revised over time and sources disagree on details (golf hole-in-one bonus, NASCAR fastest-lap value). Verify current values in the DK app before hard-coding anything.
- Several popular concepts have no citable source: "flag-planting," "points per percent owned," venue judging bias in MMA, altitude effects. Treat as folklore until measured.
- The five-round-dog stat is a 15-fight sample. Big edge, small evidence.
- DK's own rules pages couldn't be fetched for late-swap confirmation in your three sports; the standard understanding (full lock at first fight/green flag/first tee, no swap) should be verified in-app.
