# Post-autopsy review — Coke Zero Sugar 400, Daytona (8/29/26)

## What happened

This section says how the night went, in plain words.

1. Your $4K entry finished 266th of 392 (it beat only 32% of the field), and your $12K entry finished 625th of 1,176 (it beat 47%).
2. Both entries carried Ryan Blaney ($10,500, picked by 30% of teams), who wrecked and scored -3.85 — the biggest bust the losing half bought in both contests.
3. The $4K winner (edd0h, 335.25) held the three most-picked deep starters — Christopher Bell, Denny Hamlin and Ricky Stenhouse Jr — plus Austin Dillon ($7,300, 17% picked, 62.15) and Daniel Suarez ($6,700, 10% picked, 64.35).
4. The $12K winner (ElGuapo386, 324.2) held the same Bell–Hamlin–Stenhouse core plus Dillon and Tyler Reddick ($9,700, 13.5% picked, 57.15).
5. The slate was decided by Stenhouse (70.3, the top score) and Austin Dillon, who sat in 75% to 85% of the top-20 lineups in both contests.
6. Your entries had neither, and no driver picked by under 10% of teams — the strategy named Suarez as its clearest low-owned play and he reached the winning lineup, not yours.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**Pre-flight: B.** The venue file was read and used (the 77.7%-from-20th-or-worse chart drove the whole doc), Anchor-Equivalence was surfaced (Allmendinger vs Gragson), and the open pack-track idea was applied: the strategy said several popular strong cars finish together here, so a sharp does not cap himself at one. That read was right — both winners held Bell, Hamlin AND Stenhouse. Next slate: keep applying the pack-track stack read at Talladega and Atlanta.

**The fade section: D — the trap screen flagged the winners.** Seven UNDERWEIGHT calls: three held (Zane Smith 16.1, Allmendinger 20.7, Hocevar -4.05) and three failed badly — Hamlin (53.7, in 8 of the top 10 in both contests), Stenhouse (70.3, in both winners) and Austin Dillon (62.15, in 75-85% of the top-20). Reddick was LEAN FADE and was the $12K winner's low-owned carrier at 57.15. The three failed calls all rested on "picked more than his projection rank earns", which at a pack track is the field correctly buying a proven deep-start ceiling, not a trap. Next slate at a superspeedway: an underweight needs a reason the driver's CEILING is capped, never just an ownership-vs-projection rank gap.

**The strategy's own edge was ignored by its own tiers: C.** Edge #3 said 11th-20th is the dead zone (14.8% of best-lineup spots), and the Field-vs-Sharp section said the field runs 36% on Blaney "in the thinnest scoring band". Then Top plays tiered Blaney Good and the fade section never named him. Blaney was the #1 or #2 losing-half trap in both contests (46% of the bottom half, 0% of the top). Next slate: when an edge names a dead start band, the highest-projected chalk sitting in that band must get a verdict in Fades.

**Shark gap (the main way pros looked different from you): flat this time.** The five tracked pros averaged 34.2% ownership per roster spot; you averaged 34.5% — a 0.3-point gap, nothing. Neither side carried a sub-5% piece. The difference was WHICH chalk: the pros held Hamlin in 4 of 5 lineups and finished best at the top 1.4%; you held Blaney twice and Hamlin zero times. This axis (ownership per slot) has led 5 of the last 6 slates, but the gap has now oscillated from -15.7 to +3.3 to +0.3 — your SHAPE now matches the pros; the leak has moved to anchor selection plus an empty differentiation slot.

**Discipline (did entries follow the plan): A for the letter, F for the spirit.** Zero fade violations, and every underweight was honored (as it happens, honoring Hamlin/Stenhouse/Dillon at zero cost you the slate — results do not launder discipline, and following bad calls is still following). But the strategy named 12 low-owned drivers who could decide the slate, and your entries carried 0 of 12 — the SIXTH straight slate at 0/12 (0%, 50%, 0/12, 0/12, 0/12, 0/12). Suarez was tiered Core · Leverage on the board, was the $4K winner's carrier, and never reached an entry. Next slate: at least one entry carries one name from that list, no exceptions.

**Pool vs picking (was the miss in building or choosing): choosing, but the sim could not find it either.** The Sim's 10,000-lineup pool held a 336.2 — above BOTH winning scores — so generation was fine. Your picks scored 182 and 189 while 31% and 27% of the pool beat them, and picking added about 29-36 points over a random pool row (picking_edge positive). For the first time on NASCAR the pre-lock sim numbers did predict real scores (rank agreement 0.27 for Top-1%, 0.32 for Cash and ROI — the best NASCAR reading on file), yet the top-100 rows by any metric averaged only 186 — right where your picks landed. The 336 row was not at the top of any column. Next slate: the sim is a threshold that gets you to ~186, not to 335; the extra 150 points come from the definer list, which the picker never reads for.

**The picker itself: C.** Both rationales argued at length about Bell vs Keselowski and never once argued Blaney, the driver the strategy's own edge had placed in the dead band. The picker's ranking rewards ownership positively and seats projection/cash rows first, so the two rows it chose were six 20%+ names each. The tool is now reproducing the hand-off leak the ledger has tracked for six slates. Next slate: read the pick's `why` for whether every 30%+ driver in it was argued, not just the anchor swap.

**Codified rules check.** Mid-pack PD is the meat — HELD (Suarez P23, Berry P24, Dillon P29, Hamlin P30 supplied the winners' whole edge; your deep-back Zane Smith from P34 scored 16.1). SE lock-ownership floor — HELD (Bell 48% → 63.5%, Hamlin 38% → 50.8%, while co-anchor Blaney fell 36% → 30% and Elliott 29% → 18.6%). Definer hand-off gate (#11) — NOT APPLIED, sixth slate. Sleeper-spike floor (#9) — NOT APPLIED; McDowell ($6,100, 4% picked) scored 56.7 and sat in the #3 lineup of both contests. Board tiers — ORDERED for the first time in four slates (Core 39.8 > Good 30.5 > Okay 24.6 > Fade 1.8); the one Fade-tier leak was Ryan Preece (50.6 from a 4th-place start at 3-7% picked).

## Lesson ledger changes

This section lists each stored lesson touched and why.

- `superspeedway-doms-correlate-not-substitute` — CONFIRMED, promoted to validated: both winners stacked Bell + Hamlin + Stenhouse (the field's top three), the pair the strategy said a sharp refuses was in the winner and #3, #7, #8, #9 of the $4K.
- `anchors-held-differentiate-in-sixth-slot` — third confirming slate: you dropped Hamlin/Stenhouse for Blaney/Elliott/Bubba and filled the sixth slot with Gilliland (24%), not a definer. Promotion proposed below.
- `definer-screen-must-reach-entries` — post-codification evidence, sixth slate at 0/12; the leak now runs through the picker.
- `fade-tier-buries-ceiling-tagged-definers` — CONFIRMED by the fix working: Suarez held in Core · Leverage, McDowell in Okay · Leverage, and the tiers ordered. Promoted to validated.
- `se-actual-own-concentrates-on-consensus` — post-codification note: mechanism held again (Bell +15, Hamlin +13, Blaney -6).
- NEW hypothesis `nascar-2026-08-30-rank-gap-is-not-a-trap-at-pack-tracks` — the ownership-ahead-of-projection screen flagged Hamlin, Stenhouse and Dillon.
- NEW hypothesis `nascar-2026-08-30-dead-band-chalk-needs-a-verdict` — Blaney: the edge named the band, no section named the driver.
- NEW hypothesis `nascar-2026-08-30-picker-reproduces-the-handoff-leak` — two chalk-only picks, Blaney unargued in both.

## Venue file changes

Appended a 2026-08-29 results-verified observation to `rules/nascar/tracks/daytona_international_speedway.md`: winners ran the top-three chalk together plus two 10-17% deep starters; the 21st-30th band and one front-row survivor (Preece, P4, 50.6) paid; the $10K+ car in the 11-20 band (Blaney) was the trap; both winners spent $49,700+.

## Ledger hygiene

This section decides what to do with the stored lessons the pre-pass flagged.

- `roadcourse-deepback-revives-on-strategy` — KEEP: no road course has run since Sonoma, so it has not had a test.
- `narrative-suppressed-elite-is-leverage` — KEEP: no intermediate with a shared org-demotion narrative has run since Chicagoland.
- `superspeedway-doms-correlate-not-substitute` — no longer stale; confirmed tonight (see above).
- `multiyear-lapsled-weak-perrace-signal` — MERGE into `superspeedway-doms-correlate-not-substitute` (surviving id): one pack-track dominator lesson — stack the chalk doms because they finish together, and pick them by the day's speed, not career laps led. Tonight neither strategy nor winners used laps-led at all.
- `fade-tier-buries-ceiling-tagged-definers` — no longer stale; confirmed by the fix working.
- NEAR PROMOTION `anchors-held-differentiate-in-sixth-slot` — reached 3 slates tonight; proposal below.
- Merge pairs: MERGE `multiyear-lapsled` → `superspeedway-doms-correlate` (above). MERGE `anchor-equivalence` ↔ `anchor-equivalence-not-parity` — KEEP-SEPARATE, both already codified in different framework spots. All other 22 pairs KEEP-SEPARATE: each links a cause to a different rule (the definer screen, the sixth-slot rule, the field-size band and the sleeper floor are four different levers).

## Proposed codifications

This section lists rule changes for you to approve; nothing is applied yet.

1. **Codify `nascar-2026-07-26-anchors-held-differentiate-in-sixth-slot`** (Indy + Iowa + Daytona). Add to `framework.md` Step 6 mandatory checks as **#12 — Anchors held, sixth slot differentiates:** "An SE entry keeps every consensus anchor (the top 3 projected-ownership names) unless the Fades section states a CEILING case for dropping that driver; differentiation lives in the sixth slot (a definer-list name), never in the anchor slots. Mid-owned (15-40%) pivots in anchor slots are the fish shape."

2. **Merge `nascar-2026-07-14-multiyear-lapsled-weak-perrace-signal` into `nascar-2026-07-14-superspeedway-doms-correlate-not-substitute`**, retire the former with reason "merged into superspeedway-doms-correlate-not-substitute".

3. **Narrow `rules/shared/anchor_equivalence.md`** with one line: "At drafting tracks (Daytona, Talladega, Atlanta) chalk anchors are a correlated stack, not substitutes — the at-most-one cap does not apply." (Now 2 confirming slates: Atlanta 7/12, Daytona 8/29 — proposal only; a third slate would meet the bar.)

**APPROVED & APPLIED 2026-08-30 (all 3, user directive):** #1 → framework.md Step 6 check #12 added, lesson marked codified. #2 → lapsled lesson retired ("merged into superspeedway-doms-correlate-not-substitute"), day's-speed guidance folded into the survivor's statement. #3 → drafting-track carve-out added to rules/shared/anchor_equivalence.md (approved at 2 confirming slates by user directive) + pointer in framework check #8.

## What this means for next slate

This section is the short list to carry forward.

1. One entry must carry one name from the low-owned definer list — six slates at zero is the whole leak.
2. Keep the top three most-picked drivers unless you can say why one's CEILING is capped; an ownership-vs-projection gap is not a reason.
3. If an edge says a start band is dead, the expensive chalk in that band gets a written verdict.
4. At pack tracks, stack the chalk anchors together; they finish together.
5. Read the pick's reasoning for the driver it did not argue — that was Blaney twice.
