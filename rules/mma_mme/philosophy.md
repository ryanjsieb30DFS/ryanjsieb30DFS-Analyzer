# MMA DFS Philosophy — MME (150-Max GPP)

**Contest Type:** Multi-Entry / 150-Max GPP
**Document Type:** Core Philosophy
**Last Updated:** May 17, 2026
**Companion Files:** MME_mma_framework_2026-05-17.md, MME_mma_autopsies_2026-05-17.md

---

Core beliefs that guide every MME slate. These don't change based on a single outcome — they're tested over many slates.

## The Win Condition

GPPs are won by ceiling outcomes, not by cash-line lineups. A 21% cash rate contest is not a cash game with extra entrants — it's a tournament where 80% of entrants lose, and the winning lineup almost always contains 1-3 players with sub-15% ownership who either won as dogs or finished as expected favorites the field underweighted. **Build for ceiling, not for floor.**

## Lock vs. Diversify

There are two valid lineup-building philosophies in MMA: lock conviction picks and diversify around them, or diversify the entire slate. They are not interchangeable. Locking Chimaev at 100% on a slate where he's 60% owned and 80% to win is correct — the contest is already weighted toward "Chimaev wins" worlds. Diversifying off conviction plays for the sake of contrarian-ness is process drift. **Conviction earns concentration.**

## Process vs. Outcome

A correct decision can produce a bad result; a wrong decision can produce a good result. The 5/9/26 portfolio decisions were defensible given the information at the time. The outcome was bad. **Do not retroactively rewrite the process based on the outcome.** Review what we knew when we decided. If the same information would lead to the same decisions, the process is fine. If new information would change the decision, capture that lesson — but do not punish a sound decision because variance went the other way.

## Information vs. Information Shift

Late-breaking news (injury reports, ownership flips, late-swap data) is information *and* it is signal that the field has moved. These are different things. **The news might be wrong. The field shift is real.** When the field shifts hard on news, two things are true simultaneously:
1. The fighter's actual win probability may have changed (or not)
2. The fighter's exposure is now mispriced relative to that win probability

The contrarian play is sometimes "ignore the news, the field overreacted." The reactive play is sometimes "the news is real, follow the field down." Treat news as one input, not the deciding input.

## The Optimizer Is a Tool, Not a Source of Truth

Projection-based optimizers solve a math problem: maximize projected score subject to constraints. They do not know:
- That a fighter's recent KO loss inflates their stoppage equity going forward
- That a wrestler's gas tank concerns when matched against a high-pace striker
- That a "decision favorite" with 78% win odds and a low PPD might still smash via volume

The optimizer outputs are the *starting point* of analysis, not the conclusion. **When the optimizer's lineup contradicts qualitative read, the qualitative read is information** — investigate before overriding either way.

## Floor and Ceiling Are Both Real

A 150-lineup MME portfolio needs lineups that win and lineups that cash. These are different lineups. Pure-ceiling optimization produces 150 lineups that all win or all bust together. Pure-projection produces 150 lineups that all cash or all bust together. **Portfolio diversity comes from variance across thematic batches, not from forcing every lineup to balance both.** Use Optimize By: Proj 50%/Ceil 50% as the primary criterion when you want one balanced run; use Ceiling and Finish Odds % for narrative-specific batches.

## Leverage Is Earned, Not Forced

Forcing a sub-15% owned fighter into every lineup creates leverage in name only. If the optimizer's natural projection ranks that fighter low, you're making a math-against-yourself bet. The right time for leverage is when **(a)** the field's ownership is structurally wrong (recency bias, narrative chasing, cap-tier fixation) AND **(b)** the fighter's actual win equity supports it. Otherwise you're paying for differentiation with EV.

## Punt Tier Discipline

The cheapest fighters on a slate ($6,400-$7,000) are usually cheap for a reason. They lose often, and when they lose they score 30-50 DK points. **Multiple punt-tier plays in the same lineup is a structural risk** — if Stephens, Gordon, and Buckley all blank, the lineup is dead regardless of how the studs perform. Limit punt-tier saturation: at most 1 fighter under $7,200 per lineup, ideally with at least one finish-equity story attached.

## Constraints Eliminate Optionality (added 5/16/26)

Every constraint added to an optimizer build — a Min cap, a forced pairing rule, an IF/THEN condition — removes some set of lineups the optimizer would otherwise have considered. This is the *point* of constraints, but it has a cost: **constraints eliminate the optimizer's natural hedge against your own thesis being wrong.**

When the optimizer wants a fighter at 33% and qualitative analysis says 40%, the gap represents real uncertainty about which view is right. A Min 40% cap forces the bet that qualitative is correct. A Boost +2 nudges toward qualitative while preserving some hedge against the optimizer being right. **Boosts preserve optionality; Min caps remove it.**

This is especially important for conviction plays in unfavorable scenarios. The 5/16/26 Santos Min 40% cap forced 45% exposure on a fighter who lost — and the optimizer's natural 33% exposure was hedging against exactly the loss scenario that occurred. The cap *removed the hedge that would have helped us when we were wrong*. Use Min caps only when conviction is iron-clad; use Boosts when conviction is strong but contested.

## Different-Fight Pairings Are Not Correlated Outcomes (added 5/16/26)

Two fighters in different fights produce independent outcomes. When we like both, the temptation is to pair them in lineups — "if I believe in Santos and Gantt, I want lineups with both." But the IF/THEN rule that forces this pairing creates **artificial portfolio correlation** that the underlying fights don't share. When Santos loses (independent of Gantt's outcome), every Santos+Gantt lineup carries a dead-weight Santos slot that Gantt cannot compensate for at half the salary.

**True correlation in MMA is rare** — it exists in same-fight outcomes (opponents lock each other out) and very loosely in card-wide finish-rate environments. Different-fight fighter pairings should be expressed through individual exposure preferences, not conditional rules. Boost both fighters and let natural overlap occur; if both fighters hit, the natural distribution will have produced many lineups with both. Don't force the pairing.

## Bankroll Is the Real Game

Every slate is one trial in a long sequence. A losing slate where the process was sound is part of the math. A winning slate where the process was sloppy is borrowed luck. **Optimize for sustained edge, not for any single result.** Track ROI over 30+ slates before evaluating whether a method works.
