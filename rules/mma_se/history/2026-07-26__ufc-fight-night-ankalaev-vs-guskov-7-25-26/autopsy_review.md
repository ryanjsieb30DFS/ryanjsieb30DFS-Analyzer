# Post-autopsy review — UFC Fight Night: Ankalaev vs Guskov 7.25.26

_Three contests: $5K Flying Knee SE (rank 72/490), $5K Clinch SE (rank 229/1,189), $2K Sprawl 3-Max (best rank 21/594 — top 3.5%). Reviewed 2026-07-26._

## Process scorecard

**The analysis was strong. The build gave one fight back to the field, and it cost two wins.**

- **Pre-flight was honored in substance.** The strategy surfaced Anchor-Equivalence as required (Dulatov vs Tuchalov, near-identical price and ownership). It applied the open leverage-screen lesson correctly, pushing leverage up from the sub-10% fliers into the low-owned converting favorites. MMA has no venue file, so no venue check applies.

- **The slate read held up.** The strategy predicted the field would jam the expensive finishers and pair the chalk. The winners did exactly the opposite of dart-throwing: all three winning rosters were six mid-to-high-owned favorites with zero sub-10% pieces (average ownership 30.9–35.2%). That is precisely the winning shape the 7/19 lesson describes, and this slate confirms it (see ledger changes).

- **The Anchor-Equivalence call paid, but not by its own mechanism.** The user took the Tuchalov side (96.2 FPTS, in 3 lineups) over Dulatov. Dulatov scored 0.0 — but his fight was **scratched** (his ownership collapsed from 32% projected to 12.6% actual, and both fighters scored zero). A cancelled fight is not the equivalence mechanism resolving, so this is NOT logged as a confirmation. It still saved every lineup that would have carried him.

- **The "tier ordering BROKE" flag was scratch-contaminated — now CORRECTED in the record (7/26).** The original calibration showed Core averaging 48.1 because Dulatov's cancelled fight counted as a real 0.0. The scratch-exclusion fix shipped and this slate's records were recomputed: `pool_calibration.json`, `results.jsonl`, and `autopsies.md` now read Core 96.2 (Tuchalov) vs Good 98.9 with Dulatov and Turman listed as excluded scratches. The 2.7-point Core-vs-Good gap is effectively a tie, not a broken board — no boundary action needed. The Sim's vendor-accuracy row was corrected the same way (Dulatov is no longer DailyFan's "worst miss"; Saidov's real +62.6 overshoot is).

- **The leverage-candidate miss (0 of 2) is half-moot and otherwise correct.** Turman's fight was scratched — rostering him would have been a zero. Ribeiro busted (17.84 at 4.7% own). The winners skipped both too. Not rostering the sub-10 fliers was the right call this week, which is the 7/19 "sharp envelope is a rate, not a quota" point playing out again.

- **THE finding: the user took the field's side of the one fight the strategy called for leverage.** The strategy tiered **Zaynukov** Good · Leverage (21% projected own, 138-point volume ceiling) and named him the definer of his fight. The user instead carried his opponent **Rzepecki** — the field's "safe value" at ~35% actual ownership — in 3 of 5 lineups. Zaynukov won and scored 78.22; Rzepecki scored 23.66. Removing Rzepecki was the best swap in BOTH one-swap-from-winning contests, and the direct Rzepecki→Zaynukov swap alone would have won the 3-Max (587.26 + 54.6 = 641.8 vs the 619.62 winner). Adherence shows all fades honored — this leak is invisible to the adherence grade because only fades and sub-10 candidates are tracked. A new hypothesis lesson captures the mechanism.

- **Shark head-to-head: structurally even, and you won it.** One tracked shark was in the Clinch field. Your entry's fingerprint was nearly identical (30.5 vs 30.4 ownership per slot, both zero leverage pieces, both unique), and you finished a hair ahead (19.26th vs 19.76th percentile). No recurring structural axis fired this slate — `own_per_slot`, the past leak, was dead even.

- **Adherence: clean on discipline.** Walker (lean fade) capped at 40%, Patterson (lean fade) at 20%, Saidov (underweight) at 40% — all within bounds. Honest note: Walker (91.07), Patterson (116.04), and Saidov (114.06) all hit, and Saidov was in every winning roster. Results don't grade discipline, and none of these were mechanism failures — each fade named the world it needed and that world showed up. But the Saidov underweight was the closest call: a 29%-owned debutant the strategy discounted for "no proven UFC ceiling" proved a 114-point ceiling immediately.

- **Process trend (last 5 slates):** best percentiles 1.7 → 1.3 → 26.1 → 2.3 → 3.5. Small-field results remain consistently strong. Leverage-candidate coverage read 0/2 in both graded slates, but in both weeks the winners carried zero sub-10 pieces — the metric is aimed at the wrong tier for MMA (see Proposed codifications for the eventual fix path; the new lesson tracks the real slot).

## Lesson ledger changes

- **`mma-se-2026-07-19-winning-se-shape-six-winners-mid-own-converters` — confirmation added, promoted hypothesis → validated.** All three winners were six mid-own favorites, zero darts, with a 22–24%-owned converter (Aliev, 116.15) carrying the differentiation in two of three. Now at 2 of the 3 slates needed for codification.
- **`mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence` — confirmation added, promoted hypothesis → validated.** Temirov projected 28%, drew 42–47% actual — the field's true #1 chalk. The projected #1 (Walker 34%) came in at projection; the error is concentration on the consensus side, not a uniform shift. Now at 2 of 3.
- **`mma-se-2026-07-26-field-value-side-vs-your-named-converter` — new hypothesis born.** Rostering the field-value opposite of your own named leverage converter is a double loss: you take the losing side of the fight and hand back the leverage. Rzepecki over Zaynukov, 3 of 5 lineups, worth two contest wins.
- No contradictions logged. Dulatov's zero is a scratch, not evidence against anything.

## Venue file changes

None — MMA has no venue files (venue knowledge exists for NASCAR tracks and PGA courses only).

## Ledger hygiene

**Stale hypotheses (4) — all KEEP.**
- `confirmed-vs-speculative-news` — KEEP. No confirmed-vs-speculative news situation has occurred on a graded slate since it was born; untested-for-lack-of-trigger is not stale.
- `showdown-flex-spine-diversity`, `showdown-trust-cpt-own-not-projected-overall-own`, `showdown-captain-the-ceiling-pair-the-smash` — KEEP all three. Every slate since 6/14 has been classic format; a showdown lesson can only be tested on a showdown card. Retire-review them only if a showdown slate occurs and they fail.

**Near promotion (3) — the third-slate mechanism each needs:**
- `showdown-cap-single-favorite-exposure` (validated, 2/3) — needs a showdown slate where capping a single non-captain favorite's exposure demonstrably de-correlates the portfolio. Format-gated; cannot advance on classic cards. (Cross-format echo noted, not counted: Rzepecki in 3 of 5 classic lineups was a correlated single-fighter bet that damaged three entries at once.)
- `showdown-cheap-slot-prefer-floor-or-live-dog` (validated, 2/3) — needs a showdown slate where the cheap slot decides the lineup and the floor/live-dog choice is the reason. Format-gated.
- `distance-fight-is-not-low-ceiling` (validated, 2/3) — needs one more slate where a distance-leaning fight produces a slate-relevant ceiling score. Watch volume strikers in decision-leaning spots; Zaynukov's profile (78 in a win, 138 ceiling on volume) is the shape that would confirm it.

**Merge candidates (22 pairs) — KEEP-SEPARATE, all.** Every flagged pair is a deliberate `[[id]]` cross-link between related-but-distinct mechanisms, not a duplicate statement; the ledger's linking convention is liberal by design. No pair states the same mechanism twice.

**Watch item:** `secondary-plays-are-not-leverage` is codified with 1 contradiction on record. A second mechanism contradiction triggers a demotion proposal per the retirement rule. Nothing this slate tested it.

## Proposed codifications

None this slate. Both promoted lessons sit at 2 of 3 confirming slates:

- One more slate where the winners are all mid-own converters with zero darts codifies **winning-se-shape** (the framework edit would go in the SE build-shape section: winning MMA SE shape = six winning favorites, differentiation from 15–30% converters, never from darts).
- One more slate where actual ownership concentrates hard on a consensus name the projections spread codifies **projected-own-understates-convergence** (the framework edit would adjust chalk-combo and anchor-equivalence math with an upward convergence factor on the consensus side).

When either codifies, the same edit should consider the adherence-metric gap this slate exposed: coverage of the strategy's NAMED mid-tier converters is the discipline number that matters in MMA SE, not sub-10 flier coverage.
