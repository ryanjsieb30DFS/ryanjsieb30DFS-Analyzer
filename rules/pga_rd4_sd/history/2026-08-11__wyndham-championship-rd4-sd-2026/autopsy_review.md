# Post-autopsy review — Wyndham Championship RD4 SD 2026 (2026-08-11)

## What happened

This section says how the day went in plain words.

1. You WON the 294-entry contest — first place out of 294 teams.
2. Your other entry finished 19th of 141, better than 86.5% of that field.
3. Both contests were decided by Benjamin James, a $8,700 golfer picked by fewer than 1 in 12 teams, who posted the day's top score (84.25).
4. Your winning team had James; your other team did not — and one legal swap (Jordan L. Smith for James, which fits the salary cap) would have won that contest too. (Corrected 8/11: the original sentence proposed Ventura for James, but that swap costs $1,900 more than the lineup's $200 of cap room — it was never possible.)
5. Both contest winners were built the way your plan described: mostly popular golfers, plus one or two low-picked ones doing the heavy lifting.
6. The thing that decided the slate was owning the cheap mid-priced scorer the crowd skipped — exactly the pocket your strategy flagged before lock.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

- **Plan quality: A.** The strategy named the winning pocket before lock — the lightly-picked $8,300–$9,200 salary tier — and Benjamin James lived there. It also named the target build shape (roughly 16–23% average ownership, one low-picked piece), and both contest winners matched it. Next: keep this exact prep.
- **Discipline (whether your entries followed your own plan): A.** Zero fade violations — Hossler and Thompson both held at 0% in both entries. Thompson busted (30.6), so that fade paid. Hossler scored 52.6 and sat in the 141-field winner, so that fade cost you one contest — but it was a named, accepted bet, which is good process. Only 1 of the 12 named low-owned candidates was rostered (Spieth, who scored 51.9 in your winner) — with just two entries that count is expected, not a miss.
- **The big correction landed.** Last slate your single entry ran ~7% average ownership with five darts and got buried. This slate both entries sat at 22–23% with exactly one dart — the fix your ledger prescribed — and the gap to the tracked pros (average ownership per roster spot) narrowed from 15.6 points lighter to 5.6. You beat the lone tracked pro in the field (you: top 0.3%; them: 77.9th percentile). Next: keep building the single bullet at this envelope.
- **Anchor twins: split correctly.** Brennan (71.45) crushed his near-twin Kim (39.05). The entry holding Brennan without Kim won; the entry carrying both finished 19th. Next: keep putting one entry on each side of the twin pair.
- **Player board: ordered, with one blind spot.** The tiers graded in the right order (Core 55.9 > Good 41.0 > Okay 38.6 > Fade 36.9). The blind spot was **Benjamin James** ($8,700): the day's top scorer at 84.25 points, ranked 17th on the board in the Okay tier with a 45.0 projection. The board's own write-up saw the shape — "a strong projection in the squeezed tier at 1-in-10 ownership" — but the sub-10% leverage screen skipped him because his printed ownership was 10.5%, half a point over the line (his real ownership came in around 8%, fewer than 1 in 12 teams). He decided both contests: he was in your Albatross winner and in the Dogleg winner you finished 27.8 points behind. Next: also scan the 8–12% printed-ownership band for the definer, since printed ownership runs a couple points high exactly where the screen's cutoff sits.
- **Pool vs picking: the pick was excellent.** (Updated 8/11 late — the Sim's measurement arrived after this review was first written.) In the 294-entry Albatross, only 8 of the 15,000 pool lineups (0.05%) would have beaten the entry you picked — and you won the contest outright (360.4; the pool's best was 384.1). In the 141-entry Dogleg, 5.35% of the pool beat your pick (802 of 15,000; pool best 370.0 vs your 290.85). Your picks beat the pool's average by 123.2 and 67.1 points. The pre-lock sim rankings were weakly predictive this slate — better than the near-zero readings on the Classic side: Top 1% correlated 0.149/0.218 with real scores, ROI 0.171/0.246, Cash% strongest at 0.235/0.318, Win% weakest at 0.056/0.098. Still watch, don't act — the sim-ranking trend needs ~5 slates.
- **Codified rules: five fired, all held** (build envelope, one-dart mandate, mid-tier score source, anchor twins, chasers-past-the-leaders). None showed a mechanism failure.

## Lesson ledger changes

This section lists every ledger entry touched, one line each.

- `anchor-equivalence` — confirmation added: the twins diverged 71.45 vs 39.05, and the split-the-pair entry won.
- `winning-structure-19own-1to2-darts` — confirmation added: both winners at 22.2%/25.8% average ownership with 1–2 low-owned pieces.
- `leverage-play-still-mandatory` — confirmation added: James (6–8% owned, 84.25) carried both winners.
- `sub15-midtier-birdiefest-score-source` — confirmation added: the squeezed $8,700 tier again supplied the winning score; the slot works, the individual names stay coin flips.
- `contention-extends-past-54hole-leaders` — confirmation added: chasers JT (55.9) and Hideki (60.0) beat leaderboard chalk Kim (39.05).
- `single-bullet-gets-envelope-not-darts` — promoted from testing (hypothesis) to confirmed (validated): first live confirmation, now 2 of 3 slates toward a framework rule.
- NEW hypothesis `own-outrunning-projection-trap-shape` — the losing half's shared buys were golfers whose real ownership ran far past the printed number (Van Rooyen 5.6%→20%, Koivun 11%→25%, Thompson 25%→36%), all at 0% of winners.

## Venue file changes

Appended a 2026-08-11 RD4 observation to the Sedgefield file: on a soft Sunday the whole page can score, leaderboard chalk (Kim 39.05) was not the score source, and the $8–9K wedge-week tier (James 84.25) decided both contests.

## Ledger hygiene

This section records the keep-or-retire calls on the ledger's flagged entries.

- `repeated-punt-needs-thesis` (stale, 0 confirmations in 3 slates / 79 days) — **RETIRE (proposal; needs your approval).** Reason: its risk is already policed by two rules that proved themselves — every-lineup-needs-its-own-thesis and the single-bullet envelope — and it never confirmed even on the 34-entry 8/8 slate where repeated punts were possible.
- `sim-winpct-weak-ranking-signal` — **KEEP.** No Sim measurement file arrived this slate, so it is untested only because no relevant slate occurred.
- `single-bullet-gets-envelope-not-darts` — **NEAR-PROMOTION (2 of 3).** The third slate must confirm the same reason it works: an envelope-built single entry (~19–23% ownership, 1–2 darts) finishing ahead of dart-heavy builds, or an off-envelope entry paying for it again.

## Proposed codifications

This section lists changes that need your approval — nothing here is applied yet.

- **Retire `pga-rd4-sd-2026-05-24-repeated-punt-needs-thesis`.** Exact edit: in `lessons.yaml`, set its `status: retired` and `retired_reason: "Absorbed by codified rules (one-thesis-per-bullet + single-bullet envelope); 0 confirmations in 3 slates including a 34-entry portfolio."` No framework.md edit needed — it was never codified.
- No promotion qualifies yet. `single-bullet-gets-envelope-not-darts` sits at 2 of 3 confirming slates; if the next SE slate confirms, propose adding to framework.md under Historical Winning Structure: "The lone single-entry bullet IS the modal-shape bet: ~19–23% average per-slot ownership, exactly 1–2 sub-10% pieces; dart-heavy construction belongs only in multi-entry sets."

## What this means for next slate

The short list to carry forward.

1. Build the single entry at 19–23% average ownership with exactly one low-picked golfer — this shape just won a contest.
2. Keep splitting near-twin anchors, one entry per side.
3. The slate-deciding cheap scorer often sits at 8–12% printed ownership, not just under 10% — scan that band on the board.
4. Golfers whose real ownership runs far past the printed number were the losing half's favorite buys — treat a popular name's printed ownership as a floor.
5. A fade can cost one contest and still be right process — keep naming the world each fade needs.

## Applied

Approved proposals applied 2026-08-11: `pga-rd4-sd-2026-05-24-repeated-punt-needs-thesis` set to `retired` in `lessons.yaml` with retired_reason "Absorbed by codified rules (one-thesis-per-bullet + single-bullet envelope); 0 confirmations in 3 slates including a 34-entry portfolio." No framework.md or philosophy.md edits were proposed (the retired lesson was never codified; `single-bullet-gets-envelope-not-darts` remains at 2 of 3 confirmations, promotion deferred). Ledger-hygiene KEEP decisions (`sim-winpct-weak-ranking-signal`) left untouched; no merges proposed.
