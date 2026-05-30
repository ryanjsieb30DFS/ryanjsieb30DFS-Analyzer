# NASCAR Slate Framework

The repeatable process for analyzing every Cup Series slate. Walk through each step explicitly when given a new slate.

*Last updated: 5/17/26 — Dover All-Star slate*

## Standard Inputs

Each slate, expect:
- **Track preview / deep dive** (Dustin's Deep Dive PDF or similar)
- **Projection sheet** with salary, starting position, projected points, projected ownership (DailyFan or similar)
- **Historical track data** (optimal lineups, laps led by start position, fast laps by start, top-10 DK score distribution)
- **Practice/qualifying results**
- **Contest entry plan** (field sizes, prize structure, number of entries)

If any are missing, flag it before proceeding.

## Step 1: Track Profile Assessment

Answer these before tiering anyone:

| Question | Why It Matters |
|---|---|
| Track length and type? | Determines dominator point structure |
| NextGen-era caution rate? | High = more PD upside from back; low = front-runners win |
| Dominator point distribution? | Concentrated (1 main dom) vs. spread (3+ split laps led) |
| Race length? | Shorter races = fewer dominator points available |
| Optimal PD starting range? | Per historical data, where do optimal lineup spots come from? |
| Tire wear / pit strategy? | High strategy variance changes the mid-pack PD math |
| **Format-driven scoring overlays?** (Dover lesson) | All-Star, stage races, inverts, eliminations — these break normal scoring assumptions |

**Output:** A 3-5 sentence track profile that frames every later decision.

## Step 2: Driver Tiering

Build six tiers with explicit ownership and salary:

**Tier 1 — Primary Dominators**
Top-tier cars with leading-lap and fast-lap equity. At least one in every lineup. Usually 3-5 drivers.

**Tier 2 — Secondary / Contrarian Dominators**
Lower-owned dominators with realistic dom upside. **Pivots, not anchors.**

**Tier 3 — Core PD Floor Plays**
Deep starters (worse than 25th) with top-15 upside and chalk-level ownership. Floor plays.

**Tier 4 — Mid-Pack Flex (Best Leverage Tier)**
Drivers starting 14th-25th with top-10 upside. Historically the most efficient leverage tier.

**Tier 5 — Salary Savers / Punts**
Sub-$6,000. Sort by ownership and floor. Prefer sub-10% over 15%+ when floors are similar **AND when Dustin endorses both equally.** A sub-10% punt with a "MME or fade" warning from Dustin is not a leverage play for single entry.

**Tier 6 — Avoids**
Overpriced, no upside, or structural issue (qualifying spot wrong, mechanical concern, narrative trap).

## Step 3: Ownership Leverage Map

Build a table:

| Driver | Salary | Start | Proj Own | Tier | Lever |
|---|---|---|---|---|---|

For each chalk play above 35%, apply the four-question check (see philosophy.md):
1. Price/start math at minimum threshold?
2. Historical track data on this profile?
3. What does ownership imply?
4. Positive evidence or absence of confidence?

Decide for each: **fade / field rate / overweight.** Default to field rate unless conviction.

For each viable sub-15% play:
- Is it a pivot or potential anchor? (It should be a pivot.)
- Does it correlate with anything else in your portfolio?
- **What does Dustin's exact language say?** (Dover lesson — "MME or fade" means fade in single entry)

## Step 4: Contest-Specific Construction

For each contest, decide before building:

- **Target cumulative ownership** (lower for larger fields)
- **Required differentiation levers** (1 for <500, 1-2 for mid, 2+ for 1000+)
- **Required dominator paths** (always ≥2)

Then build:
1. Anchor with 1-2 dominators
2. Add Tier 3 / Tier 4 floor plays
3. Add 1-2 leverage pivots
4. Fill with Tier 5 punt
5. Confirm salary, ownership distribution, dom paths

**Single Entry vs MME construction (Dover lesson):**

- Build SE separately from MME. They are different lineup archetypes.
- SE: 1-2 leverage spots, all with positive evidence. No "MME or fade" drivers.
- SE: max 2 must-advance drivers in any format with stage cuts. Single Entry cannot absorb correlated bust risk.
- MME: variance via 20+ lineups means individual lineups can hold higher-risk pieces. The portfolio absorbs the variance the SE cannot.

## Step 5: Portfolio Review

Cross-lineup checks:

- [ ] **No single driver in 100% of lineups** (over-exposure risk)
- [ ] **Chalk above 50% in at least 33% of lineups** (the 50% Chalk Rule)
- [ ] **Each lineup has unique identity** (not three near-duplicates)
- [ ] **Top 5 chalk exposures roughly track field rates ±20%** (overweight or underweight specific spots, not all)
- [ ] **No single load-bearing leverage play** (Anchor vs. Pivot rule)
- [ ] **Thesis-count check (Watkins Glen lesson):** Count the *theses* behind overweights, not the drivers. If 3+ overweights all bet on the same outcome (e.g. "Toyota wins" or "front-runners get caught in stage games"), that is ONE bet, not three. Reduce exposure on at least one driver to break the correlated stack.
- [ ] **Must-advance concentration check (Dover lesson):** In format-driven slates with stage cuts, count drivers per lineup who must advance to score. 3+ must-advance per lineup is acceptable for MME variance but never for single entry.

## Iteration Discipline (Watkins Glen lesson — updated 5/17/26)

When using an optimizer to build a portfolio, the temptation is to keep iterating. Iteration is allowed, but it must be principled.

- **No hard cap on number of builds, but every build must be justified by a diagnosed structural problem.** Acceptable diagnosed problems include: a key driver at 0% when target was 15%+; chalk over-correlation (single driver above 70%); mutual exclusion rule failure; missing thesis coverage; salary inefficiency. Unacceptable reasons: "feels off," "want to see one more," "could be a bit more leveraged."

- **Before each new build, articulate the specific structural problem being solved AND the specific adjustment (boost/dock/rule change) that addresses it.** If you cannot articulate both, do not build.

- **If three consecutive builds satisfy the same strategic criteria with only marginal differences, marginal differences are noise. Lock the first satisfying build.** This is the original Watkins Glen rule and it still applies.

- **The "I just want to build one more set" impulse is a signal, not a strategy.** It reflects discomfort with the locked thesis, not a diagnosed problem. When this impulse appears, the answer is one of:
  1. Lock the current build
  2. Re-evaluate the strategic thesis (not the construction)

- **Optimizer outputs don't validate or invalidate strategy.** A clean build of a wrong thesis still loses. Ten builds of optimizer tuning cannot save a portfolio whose foundational thesis is incorrect.

- **Conservative boost/dock first (Dover lesson).** Use ±1 adjustments before reaching for ±5. Large adjustments cascade through the optimizer in unpredictable ways (e.g., docking Hamlin -3 pushed Elliott to 75% at Dover; Bell +1 failed to crack him into the portfolio, requiring +2 to break through). Small adjustments isolate the variable being tested. The boost/dock cascade is a real optimizer behavior — respect it.

## The Solver — Rule Mechanics Reference

**Mutual exclusion via IF-THEN:**
- IF lineup `Contains ANY` → [Driver A]
- THEN use `At Most` `0` → [Driver B]
- Result: A and B never appear in the same lineup.

**Forced pairing via IF-THEN:**
- IF lineup `Contains ANY` → [Driver A]
- THEN use `At Least` `1` → [Driver B]
- Result: every lineup with A must also have B (use for floor protection on leverage plays).

**Stats-By-Lineup restrictions:**
- `At Least 2, All Players, where Salary is At Least 8500` → forces 2+ dominator-tier drivers per lineup
- `At Least 1, All Players, where Salary is At Most 5800` → forces a salary saver per lineup

**Boost/Dock vs Min/Max:**
- Min/Max are hard caps that can over-constrain the optimizer.
- Boost/Dock is the preferred mechanism for nudging exposure — ±1 to ±5 in either direction.
- Use Min/Max only for hard fades (set Max = 0) or rule enforcement.

## Step 6: Pre-Lock Sanity Check

Ask before locking:

1. **If the chalkiest version of the slate hits, do I cash at all?**
2. **If the highest-leverage version hits, can I win 1st?**
3. **Are any of my lineups built on a single load-bearing leverage play?**
4. **Have I covered the deep-PD chalk in at least one lineup?**
5. **Is my Tier 1 dominator coverage diversified across at least 2 drivers in the portfolio?**
6. **For single entry: are any "MME or fade" drivers in the lineup?** (If yes, swap.)
7. **For format-driven slates: how many must-advance drivers per lineup, and is that acceptable per contest type?**

### Mandatory enforced checks (added post-Charlotte 600 — 4-slate Anchor-Equivalence confirmation)

8. **Anchor-Equivalence:** For every chalk-tier (≥20% projected own) dominator candidate, identify the equivalent-profile alternative (within ±10% own, similar salary tier). **At least one lineup MUST run the alternative.** No exceptions — this has cost 4 consecutive slates across 2 sports.
9. **Sleeper-spike floor:** At least 2 of N lineups MUST contain a sub-15% own / sub-$6K driver projected for ≥15 SP (place differential). Charlotte 600 had 10 such plays score 23+ FPTS; zero coverage was a structural floor violation.
10. **Chalky-Combos-to-Avoid scrub:** Open the Lineups tab → Sim-Rank Exposure section → Chalky-Combos-to-Avoid expander. Any 2-player combo appearing in **2+ of your selected lineups** must be dropped from at least one of them. The Hocevar+Chastain combo at Charlotte ran in 3 of 5 entered lineups; both were 0/50 in winners.
11. **Sim ROI rank is informational, not a selector:** Verify lineup picks have lift > 1.5 on chalk-tier players (Exposure-tab lift column). If selecting by Sim ROI rank alone, you are using a metric that was Spearman −0.054 vs actual on Charlotte. Use lift + chalky-combos as primary selectors.
12. **Post-slate, use `post_roi_pct` (not one-shot actual rank) as the gold-standard retroactive equity metric.** On Charlotte 600, top-10 by post_roi exactly matched top-10 by actual (10/10) and top-50 had 44/50 overlap — post-sim is well-calibrated and gives a more stable equity estimate than the single real field. When asking "did this lineup have real equity?" or "was my loss bad luck or bad selection?", anchor on post_roi. All 5 entered Charlotte lineups had post_roi = −100% across 500 iterations — proves the loss was selection-skill, not variance.

If any check 8-11 fails, **swap the offending lineup before locking** — these are no longer optional.

## Step 7: Post-Slate Autopsy

After every slate, write a new entry in `autopsies.md` following the existing template:
- Final lineup performance and ranks
- Slate's optimal construction and winning archetypes
- "What we got right" / "What we got wrong" tables
- Lessons that generalize vs. slate-specific outliers
- Process notes (decisions, ownership update reactions, etc.)

This is non-optional. The compounding edge comes from the autopsy database.

## Quick-Reference Decision Heuristics

- **50%+ chalk → ≥33% portfolio exposure** unless definitive reason
- **Structurally sound 60%+ chalk → near field rate, not floor rate** (Watkins Glen lesson — when price/start/track all align on chalk)
- **Sub-15% play → pivot only**, never anchor
- **Single-dominator lineup → only if track explicitly rewards it**
- **Three leverage spots → no.** Maximum two per lineup.
- **Punt selection → prefer sub-10% over 15%+** when floors match AND Dustin endorses both (Texas Ty Dillon + Glen Austin Dillon confirmed at chaotic tracks; Dover lesson: don't extrapolate to high-banked concrete with "MME or fade" warning)
- **HMS + intermediates → consider double-up** (Texas confirmed)
- **HMS + road courses → fade** (Glen confirmed: Bowman 20, Larson 19, Byron -17, Elliott 21)
- **Backup-car driver → don't auto-fade** (Texas Bubba lesson)
- **Toyota road course double-up → use Reddick/Briscoe over Bell** (Glen lesson: Reddick 50.8, Briscoe 45.45, Gibbs 54.05 hit; Bell 8.00 busted)
- **Optimizer builds → unlimited, but each must solve a diagnosed structural problem** (Dover lesson). Use boost/dock at ±1 first before ±5.
- **Same thesis behind 3+ overweights → that is 1 bet, not 3** (Glen lesson — correlated leverage stacks)
- **"MME or fade" in Dustin = fade in single entry** (Dover lesson — Ty Dillon swap)
- **Autopsy patterns require mechanism check before re-application** (Dover lesson — Texas pattern didn't transfer to concrete)
- **Format-driven slates (All-Star, eliminations, inversions) break normal scoring assumptions** — Step 1 track profile must explicitly map format overlays before tiering
