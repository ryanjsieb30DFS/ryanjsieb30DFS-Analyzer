# Post-autopsy review — UFC Fight Night: Hernandez vs. Rodrigues 8.22.26

## What happened

This section is the plain story of the slate, start to finish.

1. Your best entry finished 3rd out of 1,426 in the $6K Clinch — it beat 99.8% of the field, the best finish in your logged history.
2. Four of your five entries landed in the top 10%: 3rd of 1,426, 10th of 784, and 11th and 26th of 594.
3. The Clinch was won by kpro790 with 720.92 points; you scored 704.50, a gap of 16.4 points.
4. The slate turned on the main event: Gregory Rodrigues ($7,600, on 33.7% of teams) knocked out Anthony Hernandez ($8,600, on 56.9% of teams) for 148.2 points to Hernandez's 74.4.
5. Hernandez was the crowd's trap of the day — he sat on 67.0% of the bottom-half teams and only 7.1% of the winning ones, and none of your five entries had him.
6. Your one real miss was Chris Padilla ($8,000, 111.35 points): your own strategy told you to use him less than the crowd, so the pick tool banned him, and he was in two of the three winning lineups.

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**The pre-slate prep held.** MMA keeps no venue files, so that check does not apply. The rule about two chalk anchors being the same bet (Anchor-Equivalence) appeared where it must, in `## Edges & tensions`: the strategy named Anthony Wint ($9,900, 24%), Marcio Barbosa ($9,800, 25%) and Lerryan Douglas ($9,300, 38%) as near-identical knock-them-out-early favorites, and Shanelle Dyer ($9,700, 9%) as the same bet at one-third the crowd. Dyer scored 107.52 and Douglas scored 5.6. **Next slate:** keep naming the cheap twin of the expensive chalk — that single line was worth the slate.

**Every entry came from the Sim pool, untouched — and that is the headline.** All five rosters saved in `lineup_selection.json` (pool rows 6025, 3009, 4482, 1771, 2778) match the five lineups in the standings fighter-for-fighter. No hand-swaps. Compare that to the two slates before: the hand-built 8/9 bullet finished 92.1%ile, and the hand-swapped 8/16 Clinch entry finished 67.8%ile. The Sim's own numbers agree — picking beat the average of its 6,500 lineups by 183.3, 224.9 and 272.2 points, and only 15 of 6,500 pool lineups (0.23%) out-scored your Clinch entry. **Next slate:** never hand-edit a pick; if one is displaced, re-run the pick for that contest.

**Was the miss in building or in choosing? Neither — it was in the gate.** The Sim's pool contained a lineup worth 720.92 points, exactly the Clinch winning score, so the building was fine. The choosing was fine too. What removed that lineup was your own strategy: it called Chris Padilla UNDERWEIGHT, and the gate turns that into a total ban, so every Padilla lineup was cut from all three contests before the pick was made. Padilla scored 111.35 at 49.7% ownership and was in the winners of both the 784 and 1,426 fields. UNDERWEIGHT is supposed to mean "less than the crowd, never zero" — the gate reads it as zero. **Next slate:** treat FADE as a ban and UNDERWEIGHT as a soft rule the gate drops first.

**Two of your five fade calls were wrong, and both broke the same way.** Chris Padilla was called down because his fight was "-190 to go the distance," and Vitor Petrino because his was "only -160 to end early" and both fighters' last wins scored under 75. Both scored big anyway (111.35 and 99.01) and both were in the 784-field winner. The three fades built on a real, measurable reason all paid: Wes Schultz 17.4, Kennedy Nzechukwu 1.2, Mason Jones 38.1. This is the fourth time a ceiling capped purely on "unlikely to finish" has been wrong on a slate-deciding fighter. **Next slate:** a low finish price is only a real reason to fade when the fighter is ALSO projected for low volume and low control.

**Discipline was clean.** Your entries broke none of the strategy's five fade or under-own calls, in any contest. Of the five named low-owned fighters who could decide the slate you carried one, Shanelle Dyer, who scored 107.52 and carried the 594-field winner. The four skipped (Terrance Chatman, Ryan Kuse, Jeisla Chaves, Elise Reed) had 13-18% win chances and Chaves scored 4.0, so skipping them was right. **Next slate:** judge a leverage candidate by its win path, not by the 1-of-5 count.

**The board's `Okay` tier is fixed; `Core` is now the broken one.** `Okay` held 9 of 26 fighters (35%, down from 52-63%) and sorted correctly at 74.3, between `Good` at 120.1 and `Fade` at 30.5. But `Core` held only Hernandez and Douglas — the slate's two chalk anchors — and averaged 40.0. Your entries carried zero Core fighters. **Next slate:** a fighter already in the crowd's top three cannot be `Core` unless he has an edge the crowd is not paying for.

**Against the pros, the gap finally mattered — and it was yours.** One tracked pro was in the Clinch. He averaged 34.1% ownership per roster spot and had two of the three chalk anchors; you averaged 21.2% and had none. He finished 29.03%ile, you 0.21%ile. Four straight slates measured gaps of 1.3 points or less; this one was 12.9 and pointed the other way. **Next slate:** the ownership gap is a description, never a target — it only reads as a leak when the chalk anchors actually win.

**The Sim's rankings worked this slate.** Across 6,500 lineups each pre-lock number lined up with the real scores at 0.27 to 0.32, unlike 8/16's near-zero. The top 100 by win chance averaged 526.84 points against a pool average of 432.31. **Next slate:** keep logging it; two good slates running would make the ranking usable on wide-open cards.

## Lesson ledger changes

This section lists what changed in your book of lessons.

- `distance-fight-is-not-low-ceiling` — 4th confirmation: Padilla 111.35, Petrino 99.01.
- `fade-on-structure-not-narrative` — confirmed: 3 of 3 measurable fades paid, 0 of 2 finish-price fades did.
- `winning-se-shape-six-winners-mid-own-converters` — 6th confirmation: all three winners were six winners at 19-27% ownership per spot.
- `leverage-is-the-low-own-finisher-not-the-named-dog` — 5th confirmation: Dyer (9% owned, 107.52) hit; Chaves and the other darts were skipped.
- `field-value-side-vs-your-named-converter` — THIRD confirming slate: Gaziev 100.8 over the field's Nzechukwu 1.2. Promotion proposed below.
- `the-single-bullet-gets-the-least-disciplined-build` — hypothesis → validated: five untouched picks, best slate on record.
- `duplicate-pick-across-contests-forces-hand-edits` — hypothesis → validated: five distinct picks, no forced hand-edits.
- `sim-rankings-are-a-threshold-not-an-ordering` — FIRST contradiction: all four metrics gave real signal (0.27-0.32).
- `projected-own-understates-consensus-chalk-convergence` — SECOND contradiction: Hernandez adjusted to ~70%, came in 56.9%. Narrowing below.
- `okay-tier-is-a-dumping-ground` — 4th confirmation, of the FIX: `Okay` held to 35% and sorted correctly.
- `grade-gates-have-no-discriminating-power-in-mma` — 3rd confirmation: zero flags again, this time on the best slate ever.
- `showdown-cap-single-favorite-exposure` — boundary note only: Dyer at 100% exposure cost nothing, because she scores in a decision.
- NEW `core-tier-mirrors-the-field-chalk` — `Core` uses the same evidence the crowd does, so it reproduces the chalk.
- NEW `underweight-gate-deletes-a-whole-pool-branch` — one soft call banned the branch holding the Clinch winner.

## Venue file changes

This section covers what the slate taught about the place it was held.

MMA keeps no venue files by design (only NASCAR tracks and PGA courses have them), so nothing was created or edited. Venue-adjacent note: a 13-fight card billed as a knockout parade was decided by fighters who won on volume and control, not by the early finishers.

## Ledger hygiene

This section is housekeeping on your book of lessons.

- KEEP `confirmed-vs-speculative-news` — untested only because no late injury-news swap has come up in 10 slates.
- MERGE `showdown-trust-cpt-own-not-projected-overall-own` into `showdown-captain-the-ceiling-pair-the-smash` — both dormant 10 slates, both about reading a captain-mode card. Edit below.
- KEEP `showdown-captain-the-ceiling-pair-the-smash` — showdown-only, none has run since 6/14; it is the merge survivor.
- KEEP `shared-coin-flip-slots-not-shared-players-kill-a-portfolio` — APPLIED this slate (the third 3-Max entry carried no main-event fighter) but untested, because Rodrigues won.
- NOT OVERDUE `showdown-cap-single-favorite-exposure` — the tool counts 3 slates, but 8/2 excluded one as shared evidence; still 2 of 3.
- KEEP-SEPARATE, all 35 other merge pairs — each is a `[[id]]` cross-link between healthy distinct lessons, not duplication.

## Proposed codifications

These are changes to your permanent rulebook. Nothing here is applied until you approve it.

*Revised 2026-08-28 after checking each proposal against all 15 MMA cards with a
vendor sheet and a standings file in `~/Downloads`, rather than the 3 slates the
review was written from. Proposal 2 reversed direction under the wider sample and
proposal 1 gained a scope limit. Re-run the measurement any time with
`python scripts/mma_salary_bands.py` in the Sim repo.*

**1. Promote `field-value-side-vs-your-named-converter`, scoped to the LINEUP (3 confirming slates: 7/26, 8/2, 8/23).** Add to `framework.md`, new section **Never Buy the Other Side of Your Own Leverage Fight (8/23/26 — consistency rule)**:

"When the strategy names a fighter as the leverage side of a specific fight, putting his OPPONENT in the same lineup is a double loss — you take the side you argued against and you hand back the leverage. This rests on **consistency, not on results**: if you reasoned your way to a side, holding the other one means one of your two positions is wrong. That argument needs no outcome data, which matters because the three cited cases all happen to be ones where the leverage call was RIGHT (7/26 Zaynukov 78.22 vs Rzepecki 23.66; 8/2 Urbina 113.86 vs Cepo 2.8; 8/23 Gaziev 100.8 vs Nzechukwu 1.2) — a sample selected on the outcome cannot measure how often the call is right, so do not read the rule as evidence that it usually is.

**Scope: the LINEUP, never the PORTFOLIO.** Pre-lock check: no single lineup holds both sides of a fight the strategy called. Across a multi-entry set, deliberately splitting a fight between entries is CORRECT and is required elsewhere in this framework — see `shared-coin-flip-slots-not-shared-players-kill-a-portfolio`. The 8/23 3-Max did exactly that (one entry carried no main-event fighter) and it is why the both-dogs-lose branch still finished top 12-16% instead of dying as a block. A portfolio-level version of this rule would forbid that hedge, so it is deliberately not written."

**2. Sharpen — do NOT replace — `Convergence Adjustment on the Consensus Favorite`, and narrow the lesson `projected-own-understates-consensus-chalk-convergence` (measured on 15 cards).**

The review originally proposed replacing this section with "apply the upward adjustment to the CHEAP consensus tier." **That proposal is withdrawn — 15 cards say it points the wrong way.** Ownership miss (actual minus projected) by salary band: `$9,000+ +0.3` · `$7,500-8,999 +0.2` · `under $7,500 **-1.1**`. There is no tier-wide convergence at all, and the cheap tier is the one that comes in BELOW projection. Shifting a whole tier up would be an error, and shifting the cheapest tier up would be the largest error available.

The existing section's core claim is CORRECT and confirmed: the field does pile onto one consensus name, and it is usually not the projected #1 (the projected #1-owned fighter finished BELOW projection on 8 of 15 cards, averaging just +0.4). Keep the section and replace its adjustment instruction with:

"**Exactly one fighter per card runs hot, and he is findable.** On 15 of 15 measured cards one fighter beat his projected ownership by an average of **+14.9 points** — every card had one, the smallest was +6.5. He came from the **$7,500-8,999** band on **12 of 15** cards ($9,000+ twice, under $7,500 once), and he was already projected at **25-45%** own: a fighter the crowd likes, that the crowd then likes more. Recent examples: Bukauskas $8,300 45→65.3, Reyes $8,500 29→53.7, Pimblett $7,700 29→53.3, Thainara $8,800 32→56.8, Padilla $8,000 34→44.6.

**Adjust that ONE name, never a tier.** Band averages are flat (+0.3 / +0.2 / -1.1) because everyone else absorbs the offset — a tier-wide adjustment moves 20 fighters to model an effect that lands on one. Identify the single mid-priced name with the strongest narrative agreement, add roughly +15 to his projected ownership, and leave every other projection alone. Note the cost of getting it wrong is asymmetric in the direction 8/23 showed: Padilla's real own was 44.6-49.7% against a 34% projection, and the UNDERWEIGHT call built on the low number removed the winning branch of the pool."

**3. Merge (ledger hygiene).** Unchanged from the original review. Retire `mma-se-2026-06-14-showdown-trust-cpt-own-not-projected-overall-own` with reason "merged into mma-se-2026-06-14-showdown-captain-the-ceiling-pair-the-smash (2026-08-23 ledger hygiene)", and append its content verbatim to the survivor as clause **(c) READ SHOWDOWN OWNERSHIP OFF THE CAPTAIN COLUMN, NOT PROJECTED OVERALL OWN** — the field fragments across captains, so overall own% massively overstates real exposure (Hokit ~75 projected overall, 12.6% actual captain own).

**Note for the apply step:** `framework.md` already gained a **Salary Buys Floor, Not Ceiling** section on 8/23 (committed `db0a8f2`), and lesson `mma-se-2026-08-23-salary-buys-floor-not-ceiling` is already `validated` with `codified_in` set. Do not re-add or duplicate either. The three proposals above are the only outstanding changes.

## What this means for next slate

1. Keep entering the pick tool's lineups exactly as picked — five untouched picks produced your best slate ever.
2. Stop treating "this fight will go the distance" as a reason to fade anyone; it has now cost you four times.
3. Ask the gate to ban only hard FADES — an UNDERWEIGHT call banned the lineup that won the Clinch.
4. A fighter the crowd already loves does not belong in your top tier unless he has an edge the crowd is not paying for.
5. Expect ONE fighter to run about +15 owned past his projection — every one of 15 measured cards had exactly one. Look for him in the **$7,500-8,999** band at 25-45% projected own (12 of 15 came from there), not on the expensive main-event favorite and not on the cheap tier, which actually runs slightly UNDER projection (-1.1). Adjust that one name; leave the rest alone. *(Corrected 8/28 — the original line said "the CHEAP popular names," which 15 cards reverse.)*
6. Salary buys FLOOR, not ceiling — a win scores about the same at any price, so every $9,000+ slot needs a stated FINISH path and you carry 1-2 of them, not more. Codified 8/23 in framework.md.

## Applied

Applied 2026-08-28, user-approved. This section records what actually changed on disk.

**`rules/mma_se/framework.md`**

1. **New section — Never Buy the Other Side of Your Own Leverage Fight (8/23/26 — consistency rule)**, added after *Salary Buys Floor, Not Ceiling*. Written exactly as proposed, including the selection caveat (all three cited cases are ones where the leverage call was right, so the rule rests on consistency, not on outcome evidence) and the **scope limit: the LINEUP, never the PORTFOLIO** — splitting a called fight across entries stays a correct hedge.
2. **Convergence Adjustment on the Consensus Favorite — sharpened, not replaced.** The header, opening claim and the 7/19 / 7/26 / 8/2 table are untouched. Its old numbered adjustment instruction (items 1-4) is replaced by the 15-card form: exactly ONE fighter per card runs hot (15 of 15, average +14.9, smallest +6.5), he comes from the **$7,500-8,999** band on 12 of 15 cards at 25-45% projected own, and you adjust **that one name by ~15 points, never a tier**. The withdrawn "adjust the CHEAP tier" proposal is recorded inside the section with the band misses (+0.3 / +0.2 / **-1.1**) so it is not re-proposed. The duplication-math and Anchor-Equivalence downstream notes are kept as prose. Doc date bumped to August 28, 2026.

No edits were made to `rules/mma_se/philosophy.md` — neither proposal touched it.

**`rules/mma_se/lessons.yaml`**

3. `mma-se-2026-07-26-field-value-side-vs-your-named-converter` — `validated` → **`codified`**, `codified_in` naming *framework.md — Never Buy the Other Side of Your Own Leverage Fight (8/23/26 — consistency rule)* and carrying the lineup-only scope plus the selection caveat.
4. `mma-se-2026-07-19-projected-own-understates-consensus-chalk-convergence` — stays **`codified`**, narrowed. `codified_in` now says the section was NARROWED 2026-08-28 on a 15-card measurement (adjust the single mid-priced consensus name, never a tier). A dated 2026-08-28 note was added beside the two existing contradictions, labeled explicitly as their **RESOLUTION and not a third contradiction**, so the retirement count is not inflated.
5. **Merge applied.** `mma-se-2026-06-14-showdown-trust-cpt-own-not-projected-overall-own` → **`retired`**, reason "merged into mma-se-2026-06-14-showdown-captain-the-ceiling-pair-the-smash (2026-08-23 ledger hygiene, user-approved 2026-08-28)". Its content survives verbatim in the survivor as clause **(c) READ SHOWDOWN OWNERSHIP OFF THE CAPTAIN COLUMN, NOT PROJECTED OVERALL OWN**; the survivor's opening line now states it absorbs the second entry, and its dangling `[[...trust-cpt-own...]]` link was removed since the target is now inside it.

**Left untouched, as decided:** every KEEP (`confirmed-vs-speculative-news`, `showdown-captain-the-ceiling-pair-the-smash` as merge survivor, `shared-coin-flip-slots-not-shared-players-kill-a-portfolio`), the NOT-OVERDUE `showdown-cap-single-favorite-exposure` (still 2 of 3), and all 35 KEEP-SEPARATE merge pairs. The already-codified `Salary Buys Floor, Not Ceiling` section and its lesson were not re-added or duplicated.

*Not verified: the shell was unavailable this session, so `lessons.yaml` was checked by reading the edited regions rather than by running a YAML parse.*
