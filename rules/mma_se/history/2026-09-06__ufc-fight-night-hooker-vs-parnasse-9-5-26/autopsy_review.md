# Post-autopsy review — UFC Fight Night: Hooker vs. Parnasse, 9/5/26

## What happened

This section is the plain story of the night.

1. You played two one-entry contests: you finished 487th of 588 (bottom 17%) in the $6K Flying Knee and 155th of 951 (top 16.3%) in the $4K Clinch.
2. The Flying Knee winner, mbland15 (684.39 points), was carried by Kurtis Campbell ($9,300, 153.2) and Delphine Benouaich ($8,500, 143.03) — only about 1 in 9 teams had Benouaich.
3. The Clinch winner, zak11b (678.34), separated from the crowd with Modestas Bukauskas ($7,400, 93.05), picked by about 1 in 10 teams.
4. Your plan told you to mostly avoid Benouaich (a lean fade) and the player board ranked Bukauskas in its worst tier, so neither entry could hold either winning separator.
5. Your Flying Knee entry died on Luis Felipe Dias ($8,000, 9.99 points at ~40% ownership) and Nathaniel Wood ($9,200, 27.27) — Wood was the strategy's #1 edge.
6. The slate was decided by cheap-ish finishers the plan had waved off — Benouaich 143.03, Bukauskas 93.05, Axel Sola 103.66 (in BOTH winning lineups) — while every true long shot the plan liked (Dan Hooker 5.6, Muhammad Naimov 1.6) lost.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**The pre-flight prep was honored, and the anchor call was right.** The substitutable-anchors tension (Anchor-Equivalence) was surfaced — Campbell ($9,300, 29% owned), Keita, and Pinto named as near-identical bets — and the entries anchored on Campbell, who scored 153.2, the day's best. Wood, the strategy's headline mispricing (72% win chance at 16% ownership vs Pinto's 75% at 32%), was the RIGHT KIND of bet that simply lost, scoring 27.27; a lost coin-flip is not a process error, so no lesson charged.

**The fade list was the leak, not the discipline.** Whether your entries followed your own plan (adherence): perfect — 0 of 6 avoid-calls violated, third clean slate running. But the plan's Fade layer held both contests' winning separators: Benouaich was lean-faded on a price argument (Brett: "even 100 strikes won't be enough at this price tag"), Bukauskas had his knockout path named in the strategy's own Leverage list yet sat in the board's Fade tier, and Sola's lean fade leaned on "owned 7 ranks ahead of projection." The Fade tier averaged 56.5 points against the Okay tier's 41.9 — the board's worst tier out-scored the tier above it, and tier order broke for the seventh straight graded slate. Next step: a fade on a fighter under ~15% ownership with live finish odds must name the dead path (he can't win, or his win can't score) — a price complaint is not a fade case. This is the slate's new hypothesis lesson.

**The pros were not the story this week.** One tracked pro played your Clinch, at 25.5% average ownership per roster spot against your 28.3 — a 2.8-point gap, and you finished AHEAD of them (top 16.3% vs their 31.8%). Last slate's gap ran the other direction (−1.0), so no recurring structural leak fired.

**Building was fine; one of the two picks was the miss.** The Sim's 10,000-lineup pool topped out at 731.21, above both winning scores, with 12–15 rows at or above them — generation worked. The Clinch-labeled pick scored 339.22, worse than 72.7% of the whole pool (61.5 points below the pool's average lineup); on the 500-row table Claude was shown, 392 rows outscored it, and that table even held a 731-point row — a PICK miss on a table that had the goods. The other pick scored 515.97, beating 87.2% of the pool (+115.3 vs average); its table's best row (678.9) sat 5.5 points under the winning 684.4 — a small TABLE miss, not a pick error. The sim's pre-lock rankings carried real ordering signal again (Cash% correlation ~0.25 in both contests, third wide-dispersion card in a row) — but the two picks had near-identical sim credentials (~3.2% Top-1% each) and finished 60 pool-percentiles apart, so a sim rank still says almost nothing about one row.

**Execution: the two picks were entered into each other's contests.** The Parnasse/Wood pick, argued specifically for the 951-field top-heavy Clinch, went into the 588 Flying Knee, and the Hooker build argued for the 588 went into the Clinch. Cost was roughly neutral this time, but every contest-specific argument in the rationales was voided at entry — the codified read-back-before-lock rule exists for exactly this and did not run. Next step: after entering, check each DK lineup against its saved pick.

**Codified rules held where applied.** The winning shape was the codified six-mid-owned-winners build an eighth time (winners at 31.7%/32.5% average ownership, each carried by a ~10%-owned finisher who WON). The binary-dog rule held again by violation: Hooker ($6,700, the cheap slot of the Clinch entry) was a pure knockout-or-nothing bet in a small field and scored 5.6 — also a breach of the codified cheap-slot rule (floor or live finisher, never a no-floor dart). The two-entry diversity doctrine was applied perfectly: zero shared fighters, opposite sides of three fights, and the entries' fates were fully independent.

## Lesson ledger changes

This section lists each lesson touched, one line each.

- `verify-submission-before-lock` (codified): confirmation by violation — the two saved picks were entered into each other's contests.
- `binary-leverage-weak-in-small-fields` (codified): confirmed — Hooker (8% projected own, KO-or-bust) scored 5.6; every named dart lost.
- `leverage-is-the-low-own-finisher-not-the-named-dog` (codified): 7th confirmation — the definers were converters Benouaich/Bukauskas/Andrusca, and this time the FADE layer took them off the table.
- `winning-se-shape-six-winners-mid-own-converters` (codified): 8th confirmation, with a boundary — the 588 winner carried one losing slot (Soriano, 37.96) and still won.
- `shared-coin-flip-slots-not-shared-players-kill-a-portfolio`: first confirmation (zero shared fighters → independent outcomes) — promoted to validated.
- `core-tier-mirrors-the-field-chalk` (validated): boundary note, NOT counted — Core did not mirror chalk this slate (Wood at 16%); stays 2 of 3.
- `owned-ahead-of-projection-is-not-a-trap-signal` (hypothesis): FIRST contradiction — the screen went 5-for-6 naming real misses (Ziam 2.8, Sygula 36.0…), though its one miss, Sola (103.66), was in both winners.
- `sim-ordering-scales-with-score-dispersion`: first confirmation (wide card, positive signal; identical-credential picks 60 percentiles apart) — promoted to validated.
- NEW hypothesis: `price-tag-lean-fades-in-the-leverage-band-delete-the-winners-carrier` — a fade under ~15% ownership needs a dead win path, not a price complaint.

## Venue file changes

MMA keeps no venue file (CLAUDE.md: golf has courses, NASCAR has tracks, "mma has none"). Nothing appended.

## Ledger hygiene

This section records the maintenance decisions on the flagged lessons, one line each.

- STALE `confirmed-vs-speculative-news`: KEEP — no confirmed-vs-speculative news pivot has occurred on any logged slate; untested is not disproven.
- STALE `showdown-captain-the-ceiling-pair-the-smash`: KEEP — no captain-mode card since 6/14; the mechanism cannot fire on classic cards.
- STALE `shared-coin-flip-slots…`: no longer stale — confirmed this slate and promoted to validated.
- STALE `abbreviated-names-drop-contract-calls`: KEEP — all six 9/6 calls parsed under full names; the practice prevents the failure, and prevention is not disproof.
- NEAR-PROMOTION `core-tier-mirrors-the-field-chalk`: the third slate must show Core assigned to the board's top-3 projected-ownership names WITHOUT a stated edge the crowd isn't paying for; 9/6 was a boundary, not a confirmation.
- OVERDUE `showdown-cap-single-favorite-exposure`: promotion DECLINED — the ledger's own notes hold it at 2 of 3 (the 8/2 Cepo evidence is shared with the asymmetric-weighting lesson; 8/23 was a boundary); needs one independent slate.
- MERGE candidates (57 pairs): KEEP-SEPARATE as a class — every flag is a `[[id]]` citation link, not a duplicate statement; each pair grades a different decision point (e.g. the two underweight lessons cover the pick gate vs the adherence grader).
- Removed-feature check: nothing retired — no active lesson's mechanism depends on a removed feature.

## Proposed codifications

None this slate. For the record: the flagged "overdue" promotion of `showdown-cap-single-favorite-exposure` is declined on shared-evidence grounds (see Ledger hygiene). When an independent third slate confirms it, the proposed framework.md edit is ready: append to "Step 5 — Diversification": *"Cap any single BINARY favorite — one whose only scoring path is a finish — at ~60% of a multi-entry set, and never zero the alternative anchor (the anchor-equivalence floor). An 85%-win favorite with a decision floor at full exposure is a conviction anchor, not a correlated bet."* And `owned-ahead-of-projection-is-not-a-trap-signal` now carries 1 of the 2 contradictions needed for a retirement proposal — nothing to act on yet.

## What this means for next slate

The plain takeaways, most important first.

1. Before fading any fighter under ~15% ownership who can finish, write one sentence saying why he cannot win — if you can't write it, he's a leverage play, not a fade.
2. Never let the Leverage section and the player board disagree — a fighter with his own leverage line must not sit in the Fade tier (Bukauskas was both at once).
3. After entering on DK, read each lineup back against its saved pick — this week the two picks went into each other's contests.
4. Keep the zero-shared-fighters, opposite-coin-flip-sides habit — it made your two entries truly independent bets.
5. Treat sim numbers as pool-sorters, not row-pickers — two picks with identical sim credentials finished 60 percentiles apart.
