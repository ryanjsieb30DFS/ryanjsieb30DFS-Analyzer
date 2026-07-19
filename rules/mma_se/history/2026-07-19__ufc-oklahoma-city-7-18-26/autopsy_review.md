# Post-autopsy review — UFC Oklahoma City 7.18.26 (logged 2026-07-19)

Two SE contests: **UFC $8K Flying Knee** (784 entries, top-heavy) — rank **18/784, 2.3%ile**, and **UFC $5K Clinch** (1,189 entries, flat) — rank **629/1189, 52.9%ile**. The Flying Knee entry was **one swap from winning $2,000**: swapping Austin Bashi (42.90) for RJ Harris (106.70) reproduces the 705.91 winning lineup exactly.

## Process scorecard

**Pre-flight checks — honored, judged by the strategy's substance.**
- **Anchor-Equivalence surfaced** as required: the DDP (45%) / McMillen (42%) pair, plus the Hooper/Bashi/Usman second cluster, in `## Edges & tensions`. The user acted on it (McMillen-not-DDP in both entries) and it was the single best decision of the slate — McMillen 168.11 vs DDP 85.20, and both contest winners carried McMillen.
- **Open lessons were visibly applied**: the mandatory per-fight low-owned-definer screen (the Ofli lesson) covered all 12 fights; the finish-capable-favorite exemption was explicitly cited for McMillen and Bashi; field-tendencies (in-2-of-2 counts) and chalk combos were surfaced with numbers; the sharp-envelope section was anchored to observed shark data. No checklist was printed, per format.
- **Venue file**: not applicable — MMA has no venue file by design.
- **Gap in the run**: `player_pool.md` was never generated (listed in manifest `missing`), so there is **no player-pool board and no tier calibration** (`pool_calibration.json` absent) for this slate, and `lineup_grade.md` is also missing — the Grade tab was not used pre-lock. Two learning-loop instruments were dark this slate.

**Did the synthesized edges hold up?**
- **Held — the fade block was 4-for-5.** DDP UNDERWEIGHT (85.20, inside the predicted 90–100 volume-decision band — a remarkably precise call), Ko UNDERWEIGHT (37.40, the #1 fish trap in the Clinch: 51.2% of fish, 0% of winners), Coria UNDERWEIGHT (69.90 at $9.8K, exactly the "100–110 isn't 130" world), Delgado UNDERWEIGHT (69.40 — decision win busting at $8.3K, as written). The Usman skepticism also held (38.90; fish trap in both contests).
- **Held — the Good tier's converters**: Barbosa 106.73 (the winner's leverage carrier in BOTH contests), Elliott 115.23, Franco 110.13 — all three in both winning lineups.
- **Missed — Kline LEAN FADE.** She scored **109.40 and sat in the 1,189-field winning lineup**. The "80–90 cash score" cap was derived purely from her low finish probability (+285 ITD) — the exact distance-implies-low-ceiling error the 7/12 lesson named. First confirmation of that lesson (now validated).
- **Missed — Bashi Core.** 42.90 at 46–47% actual own; the slate's biggest fish trap in the Flying Knee (51.8% of fish, **0% of winners**) and the exact piece that cost the $2K (Bashi→Harris = the winning lineup). The article's "crushes in wins" read inherited the article's matchup error.
- **Missed — every leverage lean.** Ramirez ("leverage against Hooper") 0.80 and a fish trap; Montes 22.4; Anderson 7.41; both true darts lost (Nicoll 5% own — Coria won; Melisano 8% — Barbosa won); Ricci and Cannonier lost too. **Every board piece under 15% projected own lost.** The slate was decided in the 20–30% converter tier (Harris 106.70, Kline 109.40, Barbosa, Franco) — see the new six-winners hypothesis.
- **Missed — the ownership map at the top.** The strategy read the field as paying for the DDP marquee; the field's real chalk was **McMillen at 66.8–69.8% actual vs 42% projected**, and the real #1 pair was Bashi+McMillen (34.6% of lineups) — the strategy's pair estimates, built on projected own, ran at half the actual convergence (DDP+McMillen est. ~18.9%, actual 34.4%). New hypothesis birthed.

**Tooling finding (needs a code fix — not applied in this run).** `strategy_contract.json` recorded **zero calls** (`calls: []`, `fades: []`) despite the strategy containing five explicit verdicts. Root cause: the fade bullets used the format `**Dricus Du Plessis — UNDERWEIGHT.**` (verdict inside the bold, no salary/paren/digit), and `_leading_name` (`src/player_pool.py:144`) only splits on ` at/vs/over/on `, `(`, `$`, `,`, or a digit — so the name survives as "Dricus Du Plessis — UNDERWEIGHT." and then fails resolution against the projections universe in `src/strategy_contract.py:47-57`, silently dropping every call. Consequences: the Sim-tool hand-off carried no calls, and `adherence.json`'s `fades_violated: 0` was graded against an **empty contract** (vacuous). Suggested fix: strip a trailing ` — <VERDICT-TOKEN>` tail in `_leading_name` (or split on the em-dash when the remainder is a verdict token). Until fixed, any strategy using verdict-inside-bold formatting silently disables the fade contract, adherence fade-grading, and the Grade tab's fade checks.

**Shark gap (1b).** No tracked pros were in either field this slate (`shark_gap.json`: `sharks_in_field: false`, 0 entries) — **no new axis measurement**. The previously recurring axis, `own_per_slot` (top gap in 2 of the last 4 slates), carried noise-level deltas (6/27: 1.3 pts; 7/12: 0.1 pts), and this slate the user's own-per-slot (39.4% / 33.2%) sat *inside* the winners' envelope (37.5 / 37.1). Conclusion: the recurring leak is **not structural ownership anymore** — structure has converged on the winning shape; the separating axis is **win-side selection in the mid-own tier** (Bashi/Hines/Anderson lost where Harris/Kline/Barbosa won). That mechanism is now carried by the new `winning-se-shape-six-winners-mid-own-converters` hypothesis rather than a shark-axis lesson, since no shark data exists this slate to anchor one.

**Adherence (1c) — discipline graded separately from analysis.**
- **Fades honored — verified by hand** (the automated grade was vacuous per the contract bug): none of the five faded/underweighted names (DDP, Ko, Kline, Coria, Delgado) appeared in either entered lineup. Genuine discipline, and it happened to be +EV everywhere except Kline.
- **Leverage candidates 0/2 rostered** (Nicoll, Melisano — trend on this metric: capture 1.0 → 0.6 → 0.0 → 0/2 covered). Both darts LOST, so skipping them cost nothing this slate — results don't launder discipline, but the growing evidence (7/12 + 7/19 winners both carried **zero** sub-10 pieces) says the miscalibration is in the *prescription*, not the execution. The strategy's own "roughly one sub-15% piece per bullet" target was violated in both entries (lowest piece ~24%) — and the winners violated it too. Recalibrate the target (six-winners hypothesis) rather than flag the violation as a leak.
- **Codified diversification rule violated**: both SE entries shared a 4/6 spine (Hooper/McMillen/Bashi/Franco) including *all* conviction anchors — `no-identical-conviction-cores` requires differentiating on at least one anchor. The shared Bashi bust dragged both entries, and the grader flagged both lineups `crowded_pair` (no clean cohort to compare, so the grader's self-validation is uninformative this slate). This is the slate's clearest pure-discipline finding.

**Codified-rule check (1d)** — each codified lesson, applied vs triggered, mechanism vs actuals:

| Codified rule | This slate | Mechanism verdict |
|---|---|---|
| verify-submission-before-lock | No evidence either way | Not triggered |
| no-identical-conviction-cores | **Violated** (4/6 shared spine, both anchors shared) | **Held** — shared Bashi bust hit both entries at once |
| ceiling-threshold-discipline | Not verifiable (no build-time sums archived) | No verdict |
| binary-leverage-weak-in-small-fields | Applied (dogs surfaced as candidates, not cores) | **Held** — all binary pieces busted; winners carried none; two dead coin-flip slots buried the Clinch entry. Confirmation added |
| secondary-plays-are-not-leverage | Applied (leverage labels kept sub-15%) | First wobble: the 21–29% "secondary chalk" tier is exactly where this slate was decided. 1 stress point, no demotion |
| asymmetric-anchor-equivalence-weighting | Trigger condition unmet (DDP chalkiest but decision-modal, not KO-or-bust) | Boundary held trivially |
| se-bullet-is-the-differentiated-build | Not triggered (no multi-lineup portfolio behind the SEs) | — |
| anchor-equivalence (shared) | **Applied, decisive win** (McMillen-not-DDP) | **Held** — 8th validation, with the projected-own-parity boundary noted |
| field-size-calibration | Applied (784/1,189 = genuine-differentiation band) | Held broadly; the *currency* of differentiation is refined by the new six-winners hypothesis |
| one-leverage-swing-conviction-core | Followed in neither entry (no sub-20% swing) | **First mechanism miss**: BOTH contest winners also carried zero sub-20% pieces (lowest 20.35% / 23.85%). 1 of the 2 misses needed for a demotion proposal — watch next slate |
| finish-capable-favorite-is-not-secondary-chalk | Applied (McMillen, Bashi held as cores) | Split: McMillen 168.11 (held), Bashi 42.90 (GPP guard: a lost fight isn't a mechanism failure, but note the exemption inherits the article's matchup read — Delgado's "conceded 4 takedowns" tell was in the same article) |
| ceiling-gate-underrates-low-own-finishers | Not triggered (no ceiling-gate build recorded) | — |

**Process trend** (results.jsonl, last 5): best percentile 1.7 → 1.3 → 26.1 → **2.3** — healthy and consistent with the top-heavy/flat split the strategy prescribed (differentiation budget to the Flying Knee, which is where the 2.3%ile landed). Leverage capture 1.0 → 0.6 → 0.0 → n/a (no projections matched at autopsy time this slate — the projections session was already cleared, `projections.available: false`; worth logging the autopsy before clearing next time so `edge_leverage_capture` stays populated).

## Lesson ledger changes

Applied directly to `rules/mma_se/lessons.yaml`:

1. **`anchor-equivalence-fifth-validation`** — added 7/19 confirmation (8th validation): McMillen-not-DDP captured 168.11 vs 85.20 and both winners carried McMillen; boundary noted that the ownership-parity premise held only in projection (McMillen ran 67–70% actual).
2. **`binary-leverage-weak-in-small-fields`** — added 7/19 confirmation: every binary/dog piece busted, winners carried zero, two dead coin-flip slots capped the Clinch entry at 52.9%ile.
3. **`leverage-is-the-low-own-finisher-not-the-named-dog`** — added **third confirming slate** (Ramirez the named dog scored 0.80 while below-spotlight converters Harris/Kline defined the slate) with the boundary that when the only sub-10s carry ~12–17% win equity the definer tier moves up to 15–30%. **Promotion proposed below.**
4. **`finish-heavy-small-fields-still-won-by-differentiation`** — added **second contradiction** of its avg-own-target half (both winners 31.6%/36.4% avg own, 0 darts). **Retirement proposed below.**
5. **`distance-fight-is-not-low-ceiling`** — added first confirmation (the Kline 80–90 cap vs her 109.40 in the winning lineup) and **promoted hypothesis → validated** (with the standings-can't-show-method caveat recorded in the note).
6. **`fade-on-structure-not-narrative`** — added the awaited chalk-piece test as a refinement confirmation: the Kline fade's mechanism was structural-sounding but skipped the pace/volume check, so "structural" must require it. Folded into the codification proposal below.
7. **Born** `mma-se-2026-07-19-winning-se-shape-six-winners-mid-own-converters` (hypothesis) — the winning SE shape is six winners, chalk-anchored, zero darts, differentiated by 2–4 mid-owned converters; evidence 7/12 + both 7/19 winners.
8. **Born** `mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence` (hypothesis) — McMillen 42% projected → 67–70% actual; pair-duplication and equivalence math built on projected own understated real convergence by ~2×.

## Venue file changes

None — MMA has no venue file (venue knowledge exists only for NASCAR tracks and PGA courses, per CLAUDE.md). No stub created.

## Ledger hygiene

**Stale hypotheses (4)** — all KEEP under the GPP guard:
- `confirmed-vs-speculative-news` — **KEEP.** Untested only because no late-breaking-news swap decision has occurred on any slate since 5/9; the mechanism can only fire on a news event, and none has.
- `showdown-flex-spine-diversity` — **KEEP.** Captain-mode-showdown-specific; every slate since 6/14 has been classic format, so no relevant slate has occurred.
- `showdown-trust-cpt-own-not-projected-overall-own` — **KEEP.** Same reason (no showdown since 6/14). Note: this slate produced a classic-format cousin (`projected-own-understates-consensus-chalk-convergence`) — if the showdown variant stays untested while the classic variant validates, revisit merging the pair into one format-agnostic own-calibration lesson.
- `showdown-captain-the-ceiling-pair-the-smash` — **KEEP.** No captain-mode slate since 6/14; the mechanism (CPT-slot assembly) cannot fire on classic slates.

**Near promotion (4)** — the exact mechanism a third slate must confirm:
- `showdown-cap-single-favorite-exposure` (validated, 2/3) — a third slate must show a portfolio (≥3 entries) where capping the chalkiest favorite at ≤60% of lineups plus ≥2 deliberate fade builds either dodges a chalk bust or costs nothing when the chalk hits. This slate carried only 2 entries with McMillen in both (uncapped, 100%); he smashed, so no evidence either way.
- `showdown-cheap-slot-prefer-floor-or-live-dog` (validated, 2/3) — a third slate must show the cheap slot filled with a decision-floor fighter or live finishing dog outperforming a pure salary-relief/no-floor piece. Directionally rhymed this slate (winners' cheapest pieces Franco/Harris were converting floors; the user's relief-tier Hines/Anderson busted) but standings carry no salaries, so it can't be graded cleanly.
- `leverage-is-the-low-own-finisher-not-the-named-dog` (validated) — **third confirmation recorded this slate → moved to Proposed codifications.**
- `finish-heavy-small-fields-still-won-by-differentiation` (hypothesis) — flagged near-promotion, but this slate delivered the **second mechanism contradiction** of its testable half instead → **moved to retirement proposal**. Its confirmed half (catch ≥1 low-owned converter, no losing slots) survives inside the new six-winners hypothesis.

**Overdue promotion (1):**
- `fade-on-structure-not-narrative` (validated, 3 confirming slates) — **promote.** Codification edit below, with the Kline-derived refinement (a structural fade must include the pace/volume/control check) folded in.

**Merge candidates (12 pairs)** — decisions:
- `showdown-cap-single-favorite-exposure` ↔ `showdown-flex-spine-diversity` — **KEEP-SEPARATE**: portfolio-level single-favorite cap vs pairwise spine-overlap cap; different checks, different fixes.
- `showdown-captain-the-ceiling-pair-the-smash` ↔ `showdown-flex-spine-diversity` — **KEEP-SEPARATE**: assembly rule vs diversity rule.
- `showdown-captain-the-ceiling-pair-the-smash` ↔ `showdown-trust-cpt-own-not-projected-overall-own` — **KEEP-SEPARATE**: construction vs data-calibration; the cross-link is context, not overlap.
- `secondary-plays-are-not-leverage` ↔ `fade-on-structure-not-narrative` — **KEEP-SEPARATE**: what counts as leverage vs what counts as a valid fade.
- `secondary-plays-are-not-leverage` ↔ `finish-capable-favorite-is-not-secondary-chalk` — **KEEP-SEPARATE**: rule + its exemption, already codified into different framework sections; merging churns framework text without changing behavior.
- `binary-leverage-weak-in-small-fields` ↔ `leverage-is-the-low-own-finisher-not-the-named-dog` — **KEEP-SEPARATE**: field-size EV rule vs where-to-hunt rule.
- `showdown-cheap-slot-prefer-floor-or-live-dog` ↔ `leverage-is-the-low-own-finisher-not-the-named-dog` — **KEEP-SEPARATE**: slot-specific vs pool-wide screen.
- `finish-capable-favorite-is-not-secondary-chalk` ↔ `leverage-is-the-low-own-finisher-not-the-named-dog` — **KEEP-SEPARATE**: exposure stance vs candidate search.
- `field-size-calibration` ↔ `finish-heavy-small-fields-still-won-by-differentiation` — **resolved by the retirement proposal** for the latter; if approved, the overlap disappears.
- `finish-heavy-small-fields` ↔ `leverage-is-the-low-own-finisher` — same: resolved by the retirement proposal.
- `leverage-is-the-low-own-finisher` ↔ `distance-fight-is-not-low-ceiling` — **KEEP-SEPARATE**: hunting ground vs ceiling-estimation method. If the fade-on-structure codification is approved (it embeds the pace/volume check), consider folding `distance-fight` in at its own promotion time.
- `fade-on-structure-not-narrative` ↔ `distance-fight-is-not-low-ceiling` — **KEEP-SEPARATE** for now, same note as above.

No lesson references a removed feature; no removed-feature retirements.

## Proposed codifications

*(Proposals only — nothing below has been applied to framework.md or philosophy.md. Approve via the app.)*

**1. CODIFY `mma-se-2026-06-27-leverage-is-the-low-own-finisher-not-the-named-dog`** (origin 6/27 + confirmations 7/12, 7/19 = 3 mechanism slates). Proposed framework.md addition:

> ### The Leverage Screen: Converters, Not Named Dogs (7/19/26 — 3-slate validated)
> Before lock, screen EVERY rosterable fighter under ~30% projected ownership for a realistic win path (favorites and dogs alike) and treat the low-owned CONVERTING fighters — the sides that win their fights outright, wherever the articles' spotlight isn't — as the slate's leverage candidates. Never let the leverage slot default to the article-named KO-or-bust dog: on 6/27 the named dog (Walker +425) busted while the unmentioned converters (Ofli 5–9% own, 112.76) won the slates; on 7/12 the strategy faded the definer's whole fight (Bautista, 137.43, in both winners); on 7/19 the named dog (Ramirez 15%, 0.80) was a fish trap while the 21–29% converters (Harris 106.70, Kline 109.40) sat in both winning lineups. Boundary: when the board's only sub-10% pieces carry under ~20% win equity, the definer tier moves UP into the 15–30% converting sides — screen there, and never fade an entire fight out of the search.

**2. CODIFY `mma-se-2026-06-20-fade-on-structure-not-narrative`** (origin 6/20 + confirmations 6/27, 7/12, plus the 7/19 chalk-piece test recorded as a refinement). Proposed framework.md addition:

> ### Structural Fades Only (7/19/26 — 3-slate validated)
> Only fade or underweight a live, real-ceiling piece when the fade rests on a measurable STRUCTURAL mechanism — a genuinely ceiling-capped profile, salary inefficiency, or ownership leverage. A narrative fade ("toughest opponent yet," "will go the distance") is a coin-flip guess, not an edge: on 7/12 two narrative-faded fights produced the slate's #1 score (Bautista 137.43) and a slate-definer (Cong 90.46). And a ceiling-cap claim is structural ONLY after the pace/volume/control check: low finish probability alone is NOT a ceiling cap (Kline, 7/19 — capped at "80–90" off +285 ITD, scored 109.40 in the winning lineup; Bautista, 7/12 — 137.43 in a decision). A high-output fighter favored to dominate carries a 100+ ceiling with no finish. Downgrade any fade that fails this test to a note and keep the piece at neutral exposure.

**3. RETIRE `mma-se-2026-06-27-finish-heavy-small-fields-still-won-by-differentiation`** (2 mechanism contradictions of its testable half: 7/12 and 7/19 — both slates' winning structures were chalk-anchored 31–40% avg-own builds with zero sub-10 pieces, directly contradicting the "hold small fields to 16–20% avg own / ≥1 sub-10" prescription). Proposed ledger edit on approval: set `status: retired`, `retired_reason: "Avg-own-target half contradicted by the winning structure in consecutive slates (7/12, 7/19); the surviving half (catch >=1 low-owned converter, carry no losing slot) is carried forward by mma-se-2026-07-19-winning-se-shape-six-winners-mid-own-converters."` No framework.md text exists for it (never codified), so no framework edit is needed.

No other lesson meets the promotion or retirement criteria this slate.

## Applied

Approved proposals applied 2026-07-19: (1) codified `mma-se-2026-06-27-leverage-is-the-low-own-finisher-not-the-named-dog` → framework.md "The Leverage Screen: Converters, Not Named Dogs (7/19/26 — 3-slate validated)" (status → codified); (2) codified `mma-se-2026-06-20-fade-on-structure-not-narrative` → framework.md "Structural Fades Only (7/19/26 — 3-slate validated)" (status → codified); (3) retired `mma-se-2026-06-27-finish-heavy-small-fields-still-won-by-differentiation` with the proposed retired_reason (surviving half carried by `mma-se-2026-07-19-winning-se-shape-six-winners-mid-own-converters`). Ledger hygiene: all KEEP / KEEP-SEPARATE decisions left untouched; no merges to apply. No philosophy.md edits were proposed; none made.
