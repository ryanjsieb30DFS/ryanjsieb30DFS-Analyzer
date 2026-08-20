# Post-autopsy review — FedEx St. Jude Championship 2026 (PGA Classic, logged 2026-08-19)

## What happened

This section says how the contest went, in plain words.

1. You entered 2 lineups in a 705-entry 5-Max; your best finished 189th, beating 73% of the field (top 26.8%), and the other finished 621st (bottom 12%).
2. IrieAllStars won with 521 points: Scottie Scheffler ($13,500, 125.5 points, on 27% of teams) plus Si Woo Kim (95.0), Alex Noren (90.5, on only 4.5% of teams), Sungjae Im (88.5), J.J. Spaun, and 0.4%-owned Sudarshan Yellamaraju.
3. The slate was decided by four mid-priced players who scored 85+: Si Woo Kim, Noren, Im, and Viktor Hovland — your entries carried none of them.
4. Your Scheffler entry's other five players scored 50.5–72.5 each, so even the slate's best anchor could not lift it past 189th; the winner was 68 points and 3 player-swaps away.
5. Your no-Scheffler entry (Cameron Young 69.0, Collin Morikawa 51.5, Spaun 60.5 all under-scored) hit only 77% of its projected points and sank to 621st.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**Analysis: B — the strategy named the deciders; the entries didn't carry them.** The doc pre-named 3 of the 4 slate-defining plays: Noren in the Leverage list (a pure board catch — "#5 fit boost at under 4% picked"), and Si Woo Kim and Hovland tiered Good. The fade board was sharp too: Justin Thomas ($8,100, UNDERWEIGHT) scored 52.0 and was the field's #1 losing-half magnet (a fish trap) — on 35.3% of bottom-half lineups and 0% of winners — and Bhatia (42.5) and Brennan (59.0) busted as called. The one wrong verdict: Sungjae Im ($6,700) was LEAN-FADED because his projected pick-rate ran 12 ranks ahead of his projection; he scored 88.5 and sat in 65% of the top-10 lineups. Next step: in the cheap tier, demand a second trap signal before a lean-fade (new hypothesis below).

**Capture: F — the plan's hits never reached an entry.** After two straight slates catching every named definer (leverage capture 1.0 at the Rocket and Wyndham), this slate captured 0 of 4. Entries covered 5 of the bundle's 12 leverage candidates (Poston, Spaun, Conners, Michael Kim, Bridgeman) — the wrong five. The screen listed 18 low-owned names with no ranking, so with only 2 entries the sim tie-break, not conviction, chose which darts got the slots, and the doc's own best catch (Noren) went 0-for-2. Next step: on 1–2 bullet slates, rank the top 3 leverage plays and require one of THEM on an entry.

**Shark gap: the same axis, sixth slate running.** The main way the tracked pros' lineups differed from yours was again the rarely-picked-player rate: 1 of your 2 lineups carried a sub-5%-owned player (50%) vs the pros' 30% (+20 after +53.3, +60, +20, +16.4, −50). Your average ownership per roster spot (14.0%) also ran below the pros' 16.0% again — the recurring mechanism is "the pros buy slightly more of the crowd's proven chalk per slot and win on mid-tier selection, not dart count." Honest caveat: this slate a sub-5% piece (Noren) WAS the winner's carrier — the leak is which names fill the low-owned slots, not how many.

**Discipline (did entries follow the plan): A−, with one undocumented swap.** Zero of 7 fade/underweight calls were violated (adherence.json), both bullets carried the per-entry 2+ sub-10% floor from the 8/11 lesson, and the never-zero rule was executed (one Scheffler entry, one without — the Scheffler one finished far better, 26.8 vs 88.1 percentile). The blemish: the entered Scheffler lineup deviated from the saved Claude pick by one player — Michael Kim ($6,500) swapped out for Corey Conners ($6,700) — with no recorded reason. Conners scored 50.5, that entry's worst score, and the exact slot the counterfactual flags (Conners → Im would have gained 38 points). Sixth confirmation of the trace-to-plan lesson: log every deviation pre-lock.

**Pool vs picking: not measurable.** No sim_autopsy.json was pushed this slate, so whether the 10,000-lineup pool held a Noren/Si Woo/Im winner the picks skipped cannot be answered. Next step: push the Sim hand-off before logging.

**Codified rules: applied and mostly held.** The board's Core tier ran 5 crowding-gated names and, for the first time in three slates, the tiers graded in order (Core 83.2 > Good 69.7 > Okay 63.6 > Fade 62.7) even through a full McIlroy bust (50.5). Winners matched the 168-slate structure again (top-20: 14.1% avg own, 2.35 sub-10%, all unique). Fade-tier leakage worth naming: Im (88.5) and Jake Knapp (84.5) out-scored the Fade average by 25+.

## Lesson ledger changes

This section lists each lesson (a logged idea with evidence) touched, one line each.

- `never-zero-value-chalk-anchor` (codified): 6th confirmation — Scheffler split honored; he hit 125.5 and anchored 7 of the top 10.
- `entered-lineups-must-trace-to-plan` (codified): 6th confirmation — the undocumented Michael Kim → Conners pick swap.
- `mid-owned-value-spine-over-darts` (codified): 6th confirmation — three of four definers in the 17–20% band; you owned the band but the wrong members.
- `dart-rate-exceeds-in-field-pros` (codified): axis fired a 6th straight slate (+20).
- `vendor-independent-ceiling-scan` (codified): confirmed — Noren was a board-only catch, named pre-lock.
- `winning-structure-13own-2to3-darts` + `dose-darts-to-course-variance` (codified): winners on baseline again (14.1% own, 2.35 darts, no-cut ~2–2.5 branch).
- `core-tier-must-price-crowding` (validated): 2nd confirmation — 5-name gated Core, first ordered board in three slates → promotion proposed.
- `leverage-floor-is-per-contest` (hypothesis → **validated**): per-bullet floor written into the pick why and satisfied by both entries.
- NEW hypothesis `cheap-tier-own-ahead-not-standalone-fade`: born from the Im miss vs the correct Thomas/Bhatia/Brennan fades.
- NEW hypothesis `rank-the-leverage-screen-at-small-n`: born from Noren named-but-unrostered at 2 entries.

## Venue file changes

This section notes the course-file update. `courses/tpc_southwind.md`: appended a 2026-08-19 observation — accuracy archetype and long-driver docks verified (winner built on Si Woo/Noren/Im irons; docked McIlroy 50.5, Brennan 59.0), fit beat course history, Scheffler chalk held at a no-cut playoff; UNVERIFIED banner cleared.

## Ledger hygiene

This section records one line per ledger-maintenance decision from the deterministic flags.

- Near-promotion `contrarian-needs-leverage-anchor`: KEEP at validated — no true contrarian build entered this slate; the third slate must show a leverage-floor anchor holding (or its absence collapsing) a mid-range contrarian build.
- Near-promotion `unprojected-cheap-steam-screen`: KEEP — no vendor-under-projected name went unaddressed this slate (weak positive, not counted); the third slate must show the screen catching a 15%+ crowd name the vendor priced under ~10%.
- Near-promotion `equivalence-take-the-discounted-half`: KEEP — untested; both halves of both named twin pairs (Schauffele/Fleetwood, Si Woo/Cantlay) were zeroed, so no exposure direction existed to grade.
- Near-promotion `core-tier-must-price-crowding`: PROMOTE — confirmed this slate; codification below.
- All 16 merge-candidate pairs: KEEP-SEPARATE — every flagged link is a deliberate partner/evidence cross-reference between distinct mechanisms (e.g. per-lineup dart count vs portfolio dart rate), or involves an already-merged/retired entry (spine-sub20, major-pedigree, darts-come-from-the-screen) whose links are the preserved evidence trail.
- No stale hypotheses; no lesson references a removed feature.

## Proposed codifications

This section proposes framework edits; nothing is applied until you approve.

**Codify `pga-classic-2026-08-03-core-tier-must-price-crowding`** (origin Rocket + Wyndham + FedEx = 3 mechanism slates). Proposed edit — framework.md, Section 2 Slate Diagnostics, add under the player-pool/board guidance:

> **Core-tier gate (codified 2026-08-19).** The board's Core tier carries 5–6 names, never 3. No player inside the slate's top-3 projected-ownership tier may be tiered Core unless his row states the crowding cost in the same line ("at 33–35% he is pure chalk to size"). Core reads as "start here," so an ungated Core label converts a tiering error straight into a duplication error (Gotterup, Rocket 2026); a 3-name Core lets one bust invert the whole board (English, Wyndham 2026); the 5-name gated Core held ordered through a McIlroy bust (FedEx St. Jude 2026).

Mark the lesson `codified_in: framework.md Section 2` on approval. No demotions: no codified rule took a new mechanism contradiction this slate.

## What this means for next slate

This section is the short list to carry forward.

1. When entries are 1–2, rank the leverage screen's top 3 and put at least one on an entry — naming the hit (Noren) means nothing if it rides zero lineups.
2. Never swap a saved pick without writing one line saying why (the Conners-for-Kim swap cost grading, and likely points).
3. In the sub-$7K tier, ownership ahead of projection alone is not a fade — ask for a second trap signal first (the Im miss).
4. Keep the per-bullet floor, but re-check each bullet's dart count against a late ownership read, not just projections.
5. Push the Sim's autopsy payload before logging so pool-vs-picking can be graded.

## Applied

Approved proposals applied 2026-08-19: added the **Core-tier gate (codified 2026-08-19)** paragraph to `framework.md` Section 2 (Slate Diagnostics), exactly as proposed; set `pga-classic-2026-08-03-core-tier-must-price-crowding` to `status: codified` with `codified_in: framework.md Section 2 (Slate Diagnostics) — Core-tier gate (codified 2026-08-19)` in `lessons.yaml`. Ledger hygiene: no retires or merges — all near-promotion lessons (`contrarian-needs-leverage-anchor`, `unprojected-cheap-steam-screen`, `equivalence-take-the-discounted-half`) and all 16 merge-candidate pairs were KEEP / KEEP-SEPARATE and left untouched. No philosophy.md changes were proposed; no demotions.
