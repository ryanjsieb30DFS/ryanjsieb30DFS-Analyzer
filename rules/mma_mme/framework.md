# MMA DFS Framework — MME (150-Max GPP)

**Contest Type:** Multi-Entry / 150-Max GPP
**Document Type:** Operational Process & Solver Configuration
**Last Updated:** May 17, 2026
**Companion Files:** MME_mma_philosophy_2026-05-17.md, MME_mma_autopsies_2026-05-17.md

---

Operational process for working a UFC slate as a 150-lineup MME. This is the playbook; philosophy is the why.

## Pre-Slate Workflow

### Step 1 — Slate Structure Inventory

Before any analysis, build a one-page summary:
- Total fights
- Championship/main event/co-main fights
- Salary distribution (how many studs, how many true punts)
- Fight-pair list (the never-stack-opponents reference)
- Time slots (relevant for late-swap MME)

### Step 2 — Source Aggregation

Cross-reference at least two sources. Default sources:
- **DailyFanMMA** — projections + ownership (load into The Solver)
- **Brett Gordo / Establish The Run** — qualitative matchup reads, leverage spots, contrarian plays
- **DraftKings odds + ITD lines** — finish equity, win probability anchors

When projections and qualitative analysis diverge sharply, that fighter goes on the watch list. The optimizer alone is not sufficient.

### Step 3 — Ownership Tier Build

Group fighters into tiers:
- Mega chalk (40%+) — accept some, fade some, never blindly stack all
- High chalk (25-39%) — primary targets for fading or pivoting
- Mid (15-24%) — usually the workhorse range
- Low (8-14%) — leverage piece candidates
- Punt/contrarian (<8%) — dart throws, used sparingly

Document ownership tiers BEFORE building. Build off this, not against it.

## MME Build Strategy

- Build is portfolio-level. Lineups are tickets in a basket.
- Single optimizer run is preferred over multiple batches because exposure caps don't compound cleanly across runs in The Solver.
- Optional secondary run (30-50 lineups) on a different criterion (Finish Odds %, Ceiling) can layer thematic variety, but verify cross-batch exposures before submitting.
- Average summed lineup ownership target: 165-195%. Below 165 = portfolio is too contrarian. Above 195 = portfolio is field-correlated. (Range widened 5/16/26 to reflect flat-ownership slates without true mega-chalk locks.)

## The Solver Configuration

### Confirmed Settings (Baseline)

```
ROSTER PANEL
- Salary Cap %: 95-100
- Unique Players: 2 (3 risks "unable to find more lineups" error)
- Allow Fighters Same Fight: UNCHECKED (critical opponent rule)
- Variance %: 8
- Bounce %: 6
- Max Player Exposure (global backstop): 65 By Pos, After Each Lineup

OPTIMIZER PANEL
- Optimize By: Proj 50%/Ceil 50% (primary)
  Alternative: Ceiling for pure GPP
  Alternative: Finish Odds % for KO-heavy MMA-specific edge
- Lineups: 150

PLAYER POOL
- Lock conviction picks via padlock icon (only if Chimaev-tier conviction)
- Verify locked fighter's opponent is at 0% after first lineup
```

### Stats By Lineup (Leverage Forcing)

Required rule: "At Least 1 F where Own % is Less Than 16"

**Threshold of 16% (not 18%) is critical.** With 18%, fighters at 19-20% ownership become "fake leverage anchors" — Kopylov at 20% satisfied an 18% rule across 16 lineups in Build 2 without providing real differentiation. The 16% threshold forces a true low-owned fighter into every lineup.

**Salary qualifier consideration (added 5/16/26):** On slates where mid-tier fighters dominate the sub-16% pool, the rule produces "fake leverage" from cheap-to-fit mid-tier fighters rather than from genuine punt-tier ceiling plays. Consider tightening: "At Least 1 F where Own % is Less Than 16 AND Salary Less Than $8000" to force the leverage anchor into the punt/salary-saver tier where real GPP leverage lives.

### Optimizer Rule Constraints (The Solver — applies across all sports)

**IF/THEN rules CANNOT use:**
- Percentages ("X% of lineups")
- Aggregate ownership thresholds ("if 4+ fighters owned >25%")
- Compound AND conditions ("IF A AND B both in lineup THEN...")

**IF/THEN only supports:** Simple "IF player A in lineup THEN player B must/cannot be in lineup."

Mutual exclusion across a group (e.g., "at most 1 of these 4 fighters") is a **Min/Max group rule, NOT an IF/THEN rule.**

Pairing preferences must be expressed as **exposure caps or boosts, not as conditional percentages.**

### Player Groups (Hard Caps)

Reserve for high-conviction caps only. Don't try to set caps for every fighter — Bounce + Variance handle distribution organically. Examples that worked:
- Chimaev locked (100%)
- Stephens Min 12 / Max 30 (force punt-tier leverage)
- Volkov Min 6 / Max 18 (asymmetric ownership-vs-win-equity)
- Taira / Dawson / Sabatini Max caps (chalk control)

**Conviction expression — use Boost over Min cap (5/16/26 lesson).** When the optimizer's natural exposure for a conviction play is lower than your target, prefer Boost +1 or +2 over a Min cap. Min caps eliminate the optimizer's natural hedge against the projection being right. Reserve Min caps for fighters whose natural exposure trends dangerously low (15%+ under target) AND whose conviction case is iron-clad (Chimaev-tier). On the 5/16/26 slate, a Santos Min 40% cap forced 45% exposure on a 49%-win-rate fighter who lost — eliminating the Santos-light builds that the optimizer's projection model was hedging toward. Boost +2 would have produced similar conviction expression without removing the hedge.

**IF/THEN rules — restrict to same-fight stack decisions (5/16/26 lesson).** Reserve IF/THEN for fighter pairs in the *same fight* (anti-stack enforcement, already auto-handled) or true correlated outcomes. **Do not use IF/THEN to express "I like both these fighters" preferences for fighters in different fights.** Different-fight IF/THEN rules create artificial portfolio correlation that the underlying fight outcomes don't share. On the 5/16/26 slate, the Santos→Gantt IF/THEN rule made the portfolio behave as if Santos+Gantt were one play; when Santos lost (independent outcome) the rule forced Gantt's 129-pt score to carry every Santos-loss lineup as dead weight. Use individual exposure boosts to express different-fight preferences instead.

### Boost/Dock Calibration (added 5/16/26)

The Solver's Boost/Dock scale ranges from -5 to +5 per fighter. Empirical calibration from 7 builds on the 5/16/26 slate:

- **Dock -1:** Mild underweight; expect ~5-10% reduction from natural exposure
- **Dock -2:** Meaningful underweight; expect ~15-20% reduction
- **Dock -3:** Strong fade; expect ~25-35% reduction (Bukauskas went 36% → ~20%)
- **Dock -4:** Near-elimination; expect 80%+ reduction
- **Dock -5:** Effective ban; fighter rarely appears unless absolutely needed for salary

Same calibration applies to Boosts in reverse. **A Boost +2 produces similar magnitude to Dock -2 in the opposite direction.**

**Rule of thumb:** Halve your instinct on first attempts. If you think you want -3, start with -1 or -2. The scale is more sensitive than it appears.

## Late-Breaking News Protocol

A standing rule earned the hard way: **do not over-react to late news without time to verify.**

1. **Confirm the source.** Twitter rumors, "may be hurt" reports, and unconfirmed insider tweets are not the same as official UFC announcements. If the news is hedged ("may be," "reportedly," "expected to be limited"), treat it as a signal, not a fact.

2. **Watch the field reaction.** A 5-10% ownership shift is mild. A 15%+ shift means the field believes the news. The bigger the field reaction, the more pressure to either follow or contrarian-fade.

3. **Calibrate the swap aggression to news certainty.**
   - Confirmed injury / weight miss / pull: full reaction (move 80%+ of exposure)
   - Reported but not confirmed: partial reaction (move 30-50% of exposure)
   - Rumor / speculative: monitor, do not move

4. **Asymmetry of news risk:** if the news is wrong and you reacted, you've eaten EV; if the news is right and you didn't react, you've also eaten EV. The expected value of reacting is roughly equal to (probability news is true × EV of reaction). When in doubt, partial moves preserve optionality.

## Pre-Build Adjustment Audit (added 5/16/26)

Before running any optimizer build after the first, review the prior build's Boost/Dock and Min/Max settings. **Default action: remove every adjustment. Only re-add the ones still strategically justified by current information.**

This prevents legacy-adjustment contamination — the 5/16/26 slate kept a Veretennikov +2 boost from Build 2 across five subsequent builds without explicit re-evaluation, contributing to 33% over-exposure on a fighter who scored 6.60.

Process:
1. Open the prior build's adjustment panel
2. For each Boost/Dock and Min/Max cap, ask: "Does this adjustment still address a current problem?"
3. If yes, keep it. If no or uncertain, remove it.
4. Run the new build with only the surviving adjustments plus any new ones the prior build's exposure report justified.

## Pre-Submission Checklist

After the final 150 lineups generate:

1. Locked fighter at 100% exposure (if any)
2. Locked fighter's opponent at 0% (auto-excluded)
3. Zero opponent-stack violations across all 150 lineups
4. All salaries between $48,500 and $50,000
5. Zero exact duplicate lineups
6. Sub-16%-owned slot count > 14% of total slots (for leverage rule compliance)
7. Lineups with NO sub-16% fighter: should be 0
8. Average summed lineup ownership: 165-195% range
9. Top-2 chalk fighters: between 35-55% exposure each
10. Punt-tier fighters: limited to one per lineup (no stacked-punt builds)

If any check fails, isolate the cause and adjust *one* setting before re-running. Do not stack adjustments.

**Build-stopping heuristic (added 5/16/26):** Stop building at the first build where the pre-submission checklist fully passes. Additional iterations beyond the first all-pass build are process drift unless new information arrives. The 5/16/26 slate ran seven builds when Build 4 was the first all-pass; Builds 5-7 traded one slight overexposure for another without materially improving EV.

## Post-Slate Review

Within 48 hours of every slate:
1. Compare actual ownership to projected ownership (where did the field move?)
2. Compare actual scores to projected scores (which projections were materially off?)
3. Identify the slate's optimal lineup (winner) and gap to your best lineup
4. Catalog specific decisions that moved EV: what did you correctly fade, what did you wrongly fade, what did you correctly play, what did you wrongly play
5. Update `MME_mma_autopsies` with the slate-specific lessons

A losing slate where the process was sound goes in the autopsy with that note. A winning slate where the process was sloppy goes in the autopsy with that note too. The goal of the autopsy is process improvement, not result celebration.
