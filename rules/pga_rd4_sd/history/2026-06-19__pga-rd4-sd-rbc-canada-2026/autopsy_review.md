# Post-autopsy review — PGA RD4 Showdown, RBC Canadian Open R4 (TPC Toronto Osprey Valley)

_Slate 2026-06-19. Contest: PGA Tour SD $40K Drive the Green, 150-Max, field 9,512, 6 entries. Winning score 336.4. Best finish: rank 428 / 9,512 = **4.5 pct** (L3). Winnings/ROI tracked off-repo — not graded._

## Process scorecard

**Headline:** A clean, disciplined build that finished top-5% on its best bullet — but capped there by one structural blind spot shared across the analysis AND the red team: a hard "T-10 starters only" position gate that **faded the -9 / 3-back chasers who were the actual slate-definers.** The winning lineup (336.4) was Fitzpatrick + Hovland + Cauley + Fox + Taylor Moore + Keita Nakajima; **Fitzpatrick (65.4 from -9, 15.55% own) was THE slate-definer — in 67.4% of top lineups — and the build rated him MIX-down and PASSED Hovland, both explicitly because they sat -9 (T12), not -10-or-better.** The user rostered neither in any of 6 lineups.

| Dimension | Grade | Evidence |
|---|---|---|
| Checklist present | ✅ Pass | Full 7-line pre-flight in BOTH `slate_analysis.md` and `lineups.md`. |
| Checklist honesty | ✅ Strong | Flagged the Suber 37.6% DK/ETR vs 15.1% Stone ownership conflict and sided correctly with DK/ETR; documented the venue "easy" reputation override with observed evidence; named the Cadillac/Truist/CJ-Cup scar tissue and why it tilted tough but kept hedges. No rubber-stamps. |
| Lessons applied | ✅ Mostly | anchor-equivalence (Clark 3 / Burns 2 / Tommy 2, none at 0%) ✓; coffin (Suber, the #1 coffin, = 0 lineups) ✓; ruleset-split (4 tough / 2 birdie, tilt justified by observed scoring) ✓; correct-chalk-concentration (L2) ✓; winning-structure / leverage-mandatory (≥1 sub-10 every lineup) ✓; sub5-spike-portfolio-clause (L5/L6) ✓. |
| Lesson mis-applied | ⚠️ The leak | `ceiling-math-ruleset-dependent` was **over-extended into a position gate**: it correctly excludes way-back darts on a tough course, but here it was used to fade the -9 (3-back) tier as "not T-10 starters." On a bunched leaderboard where Sunday reopened, 3-back chasers had full ceiling and won. The gate threw out the winning tier. → new hypothesis `contention-extends-past-54hole-leaders`. |
| Over-leverage | ⚠️ Cost the tail | The two most contrarian builds finished worst: **L4 (avg own 10.08% / 4 sub-10 darts) → 99.8 pct; L6 (13.68% / 3) → 91.7 pct.** The near-19%-envelope builds finished best (L2 21.3% → 12.4; L3 15.66% → 4.5; L5 16.2% → 9.7). RD4 SD punished the Classic-grade contrarian dose. |
| Red-team adherence | ✅ Heeded | Final review was 6× SHIP, nothing to act on. Prior-round FIXes WERE heeded: dropping the +6 Nick Taylor (position fabricated from tee time) and the 2.7% way-back Pavon dart. The de-Pavon'd L3 became the **best finish (428th)** — a heeded FIX that helped. |
| Red-team accuracy (hindsight) | ⚠️ Shared blind spot | The red team re-affirmed the position gate ("all in the red, exclude way-back") and praised L4's cum-own-57 as "the portfolio's true leverage" — L4 finished **dead last**. The red team never questioned fading the -9 block, so it could not catch the leak. Koepka's 0.0 (WD) was partly variance, but the structural over-leverage call was the deeper miss. Evidence against over-trusting "lowest cum own = best leverage" in RD4 SD. |

**Edge-capture metrics (from results.json):** leverage_capture 0.0 (the user's sub-5 leverage — Koepka/Bezuidenhout/McGreevy/Thorbjornsen — all busted; the winning leverage Nakajima 1.39%/Taylor Moore went unrostered), overperformer_capture 0.2, bust_exposure 0.6 (Koepka 0.0, Theegala 22.85, Burns 30.8), lineup_avg_ratio 0.969. The leverage was real in shape but **mis-aimed at bucket-3 way-back darts instead of bucket-2 chasers.**

**Net:** Process was honest and rule-compliant; the 4.5-pct finish is a genuinely solid showdown result driven by the Cauley/modal-anchor core. The ceiling was capped by a single, identifiable mechanism (position gate fading 3-back chasers) — now captured as a hypothesis to test next tough/bunched RD4 SD.

## Lesson ledger changes

- **NEW hypothesis** `pga-rd4-sd-2026-06-19-contention-extends-past-54hole-leaders` — final-round contention extends 2-4 shots past the 54-hole leaders; a hard "T-10 starter" position gate is a ceiling leak. Three buckets: leaders/T-10 (chalk), in-contention chasers 2-4 back (full ceiling, the real leverage tier), way-back darts (the only bucket to exclude on a tough course). Birdie hedges should use bucket-2 chasers, not bucket-3 lottery darts. Born + first confirmation this slate (Fitzpatrick/Hovland -9 won; user rostered neither).
- **`pga-rd4-sd-2026-06-13-leverage-play-still-mandatory`: hypothesis → VALIDATED.** First non-mining live confirmation: slate-definer Fitzpatrick at 15.55% own (<20%) in 67.4% of top lineups; rank-1 winner ran ~2 sub-10 darts (Taylor Moore, Nakajima). Leverage mandatory AND sat at the ~19% envelope.
- **`winning-structure-19own-1to2-darts` (codified): +1 confirmation.** Top-95 winners avg 17.21% / 1.63 sub-10 / 82.1% unique — on the envelope. The user's own 6 entries showed the gradient: nearest-19% builds finished best, deep-contrarian builds worst.
- **`format-leverage-gap-vs-classic` (codified): +1 confirmation.** The user's two Classic-grade contrarian builds (L4/L6) finished last — concrete cost of importing Classic's dart-heavy dose into RD4 SD.
- No contradictions added. `sub15-midtier-birdiefest-score-source` was rule-set-gated to the hedges (Theegala busted) — a tough/hybrid course, not the birdie-fest the mechanism requires, so **not** a contradiction (GPP guard + rule-set gate).

## Venue file changes

`rules/pga_classic/courses/tpc_toronto_osprey_valley.md` — appended a `2026-06-19 — RBC Canadian Open R4 SD (showdown autopsy)` observation:
- Confirms the "Sunday reopened scoring" resolution from a showdown lens — the win came from -9/3-back chasers (Fitzpatrick 65.4, Hovland), not the 54-hole leaders alone.
- RD4 SD venue lesson: the easy/birdie-fest baseline + soft weather compresses the leaderboard, so the "T-10 only / fade the -9 block" gate fades the tier that wins here; treat -9-and-better as in contention on this course.
- Cauley reconfirmed as the venue's value-tier slate-definer (68.15 from -12, ~26% own), consistent with the 06-17 Classic note.

## Proposed codifications

**None this slate.** No lesson meets the 3-confirming-slate promotion bar and none meets the 2-mechanism-contradiction retirement bar.

- Closest: `leverage-play-still-mandatory` was promoted hypothesis → validated this slate (mining study + 1 live confirmation). It needs **one more live mechanism confirmation** before proposing codification into framework.md — flag to watch next tough RD4 SD.
- The headline finding (`contention-extends-past-54hole-leaders`) is a fresh hypothesis with a single confirmation; it must repeat on 2 more slates before any framework edit is proposed. Do not codify on one slate.
