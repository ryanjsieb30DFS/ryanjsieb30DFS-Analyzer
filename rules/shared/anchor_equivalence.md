# Anchor-Equivalence Rule

**4-slate-validated structural leak. Mandatory pre-lock check, not a recurring lesson.**

## The rule

If a slate has **2+ chalk-tier anchors at similar projected ownership**, at least **one lineup in the portfolio MUST run the alternative anchor** — i.e., the lower-projected or contrarian one of the equivalent pair.

## Why it exists

Chalk-tier anchors at equivalent ownership are mathematically substitutable: the field treats them as interchangeable, so the lineup that picks the LESS popular one captures uncontested leverage if that anchor outperforms. Not running the alternative concentrates portfolio risk on a coin flip the field has already mispriced.

## How to apply

- During the build brief, identify any pair (or trio) of anchors at the same tier with own% within ~5 percentage points of each other.
- Confirm at least one recommended lineup uses the alternative.
- Call this out explicitly in `analysis/build_brief.md` under a heading "Anchor-Equivalence Check".

## Applies cross-sport

PGA (similarly-priced top-tier golfers), MMA (chalk favorites at similar own%), NASCAR (dominator candidates at similar own%).

## Scope caution (2026-08-08)

**Equivalence requires profile equivalence, not just price and ownership proximity.** Rocket RD4 8/8: Kirk/Wallace were true twins and the cheap side paid (52.8 vs 37.5); Xander/Si Woo sat $400 apart at similar ownership and were NOT the same bet (59.2 vs 16.2 — Si Woo was the slate's biggest fish trap). Surface the pair always; auto-taking the cheaper side is not the rule.

## Pairing key caution — MMA (2026-08-29)

**Ownership proximity is one pairing key, not the only one.** This rule pairs anchors that sit at *similar ownership*. On MMA 8/29 the decisive pair was matched on **win probability** and sat 20 ownership points apart, so an ownership-matched pass could not see it: Umar Nurmagomedov 82% win / 45% own (lost, 15.7) against Rei Tsuruya 85% / 25% (won, 129.1) and Bilal Hasan 86% / 29% (won, 108.7).

In MMA, run the win-probability-matched pass **as well** — different fights, win chances within ~6 points, one owned 1.6× the other or more, floored at a 55% win chance. See `mma_se/framework.md` → *Win-Probability Equivalence, Not Ownership Equivalence*. The 8/8 scope caution above still governs the output: surface the pair, never auto-take the cheaper side.

Cross-sport status: MMA only for now. Golf and NASCAR have no per-player win probability on the vendor sheets, so there is nothing to match on there.
