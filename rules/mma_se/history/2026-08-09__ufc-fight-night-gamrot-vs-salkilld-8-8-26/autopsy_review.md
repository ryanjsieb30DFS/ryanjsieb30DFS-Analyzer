# Post-autopsy review — UFC Fight Night: Gamrot vs. Salkilld (8/8/26)

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**The one-line verdict: the analysis was very good, and the single-entry lineup ignored it.** Your best entry in the big contest beat 99% of 47,562 people (top 1.0%) and was ONE fighter swap from winning the whole thing. Your single-entry lineup beat only 7.9% of a 784-person field (92.1st percentile) — your worst single-entry finish ever logged. Same strategy, same night, opposite outcomes. The difference was which lineup followed the plan.

**The strategy's big calls, checked against what actually happened:**

- **The Gamrot warning was the call of the slate.** The strategy said the crowd's favorite play (Gamrot, the most-picked fighter) still loses his fight almost half the time by the vendor's own numbers. He lost, scored 1.8 points, and the autopsy's losing-half analysis (the fish — the bottom half of the field) shows 62.6% of losing entries carried him while ZERO winning entries did. The strategy named the exact trap that decided the contest. Then your single-entry lineup carried him anyway.
- **The two "underowned favorites" both won, and one of them won the whole contest for someone.** The strategy flagged Johns (16% picked, 61% to win) and Foro (14% picked, 67% to win) as the same bet as the popular favorites at a third of the popularity. Both won. Miles Johns (104.9 points at 14.2% actual) was the low-owned piece inside the 47,562-field WINNING lineup — and your best entry carried him too.
- **The substitutable-anchors read (Anchor-Equivalence, the mandatory check) was surfaced and it paid.** The 31-36% cluster and its cheap twins both won; the cheap side was the leverage. This is now the rule's 10th validation.
- **One codified rule misfired: the ownership-convergence adjustment.** The rule says the field piles even harder than projected onto the consensus name, so the strategy assumed Gamrot at "60%+ real." He actually came in at 39-41% — the crowd concentrated on Thainara (32% projected, 56.8% actual) and Salkilld instead. This is that rule's first recorded mechanism failure (details in the ledger section). To be clear: the strategy APPLIED the rule correctly; the rule itself was wrong this time.
- **The Salkilld "carry him less than the field" call was wrong but honestly wrong.** The fade said his win probably looks like an 80-point decision, and named the world where the fade loses: an early knockout of Gamrot. That exact world happened (Gamrot's 1.8 points means the fight ended fast). A fade that names its losing world and loses there is variance, not a process error.

**Pre-flight checks, judged by the strategy's substance:** open lessons were visibly applied (the dart-is-optional rate lesson is quoted in the build section; the leverage screen produced the converter tier; no hard fade was made without a measurable mechanism, honoring the structural-fades rule). Anchor-Equivalence appeared as required. MMA has no venue file by design, so that check does not apply. Pre-flight: honored.

**Discipline (did the entries follow the plan — adherence):** the plan made 2 under-carry calls and named 2 low-owned candidates. Zero calls were violated, and for the first time both named leverage candidates (Elkins, Oliveira) were rostered somewhere — the trend on this metric is 0-of-2, 0-of-2, 1-of-1, now 2-of-2. Two per-contest flags fired: Salkilld and Vazquez were at ZERO in the single-entry contest while under-carried (not zeroed) in the big one. The Vazquez zero was fine (he lost). The Salkilld zero mattered: with one entry, zeroing him while carrying Gamrot meant your one bullet picked the losing side of the main event. Note for reading these flags: in a one-lineup contest an "underweight at zero" flag is really "you picked the other side of the fight" — the flag is doing its job, but the decision it exposes is side-picking, not exposure math.

**You vs the tracked pros (shark gap):** one tracked pro played your 784 field. Your structure and theirs were nearly identical — 28.8% vs 29.8% average ownership per slot (a 1-point gap, which is nothing), same anchor exposure, both unique, both with zero sub-5% pieces. They finished 43.5th percentile; you finished 92.1st. When two structurally identical lineups finish 49 percentile points apart, the gap is WHICH fighters were picked, not how the lineup was shaped. This is the third straight slate where the structural gap measured essentially zero — the recurring lesson is that for you in MMA, there IS no structural leak; the leak is win-side selection. That finding was logged as the third confirmation of your rate-not-quota lesson (see below).

**Was the miss in building the pool or in picking from it (Sim autopsy)?** The Sim's 10,728-lineup pool contained a 632.85-point lineup — enough to WIN BOTH contests. So generation was fine. Selection split sharply by contest. Big contest: only 43 of 10,728 pool lineups (0.4%) beat your best entry — with 5,000+ lineups hindsight always finds a few gems, and 0.4% is an excellent rate, so picking was fine there. Single entry: 84.2% of the pool beat your entered lineup, which scored 82 points BELOW the pool's average. That is not bad luck — a random pull from your own pool would have beaten your hand-picked bullet five times out of six. The single-entry miss was pure SELECTION. On the pre-lock rankings (rank signal): every sim metric's correlation with actual scores was near zero this slate (Top-1% 0.07, ROI 0.03, Win% -0.03, Cash% 0.19). This is the first slate with this measurement, so one slate is noise — no lesson yet, but it goes on the watch list: if the same metrics read near zero next slate too, the sim rankings are a floor-filter, not an ordering.

**Codified-rule check (rules already promoted into your framework):**

| Codified rule | This slate |
|---|---|
| Binary leverage weak in small fields | Triggered and VIOLATED in execution — strategy assigned the darts to the big field; the SE bullet carried Goff (17.0) anyway. Mechanism held; confirmation logged. |
| Winning SE shape (six winners, mid-own converters) | Mechanism held again in both field sizes — 4th confirmation logged. The SE bullet did not follow it. |
| Convergence adjustment on the consensus favorite | Applied correctly, mechanism FAILED (Gamrot 53% projected → 39-41% actual). First contradiction logged; not a demotion yet (needs 2). |
| Structural fades only (+ ITD carve-out) | Followed — "No hard FADE this week" with the mechanism bar stated; the Salkilld underweight cited volume-allowance data, not finish price alone. |
| Leverage screen: converters, not named dogs | Followed and paid — the 14-16% converter tier (Johns/Foro/Miranda) contained the field-winner's carrier. |
| Anchor-Equivalence (shared rule) | Surfaced as required; 10th validation logged. |
| Asymmetric anchor-equivalence weighting | Trigger condition (chalkiest play AND knockout-or-bust) unmet — correctly did not fire. |
| Distance ≠ low ceiling | No distance-based fade was made — correctly did not fire. |
| Finish-capable favorite is not secondary chalk | Followed — the 29-36% favorites stayed playable and averaged 104 points. |
| The cheap slot decides the lineup | The SE cheap slot (Goff, $7.0K, knockout-or-bust) violated it in a small field; covered under the binary-leverage confirmation. |
| SE bullet is the differentiated build | The bullet WAS differentiated (unique, dup count 1) — but differentiated through losing slots. Not a clean test of this rule. |
| Ceiling threshold / one-leverage-swing / others | Not measurable or not triggered this slate (no salary or projection totals in standings). |

**What to do about the one real failure:** the single-entry bullet is where four straight slates of rule-breaking slots have landed. Next slate, build the bullet FIRST, run it against the strategy's own pre-lock question ("how does each of the six WIN?"), and consider picking it from the Sim pool's contest slice instead of free-hand. A new hypothesis lesson now tracks exactly this.

## Lesson ledger changes

This section lists what changed in your book of lessons (the lesson ledger), and why. A "confirmation" means the slate showed the lesson's reason-why (its mechanism) working; a "contradiction" means the mechanism failed. Losing money is never evidence by itself.

**Confirmations added (5):**
1. `binary-leverage-weak-in-small-fields` (codified) — 7th confirmation. The small-field knockout-or-bust dart (Goff) scored 17.0 and helped sink the bullet, while the same darts were harmless in the big field where the strategy budgeted them.
2. `winning-se-shape-six-winners-mid-own-converters` (codified) — 4th confirmation. The SE winner: 38% average ownership, zero sub-10% pieces, mid-own difference-makers. The big-field winner's carrier was a named CONVERTER at 14.2%, confirming the "converter at any ownership" clause.
3. `sharp-envelope-is-a-rate-not-a-per-bullet-quota` (validated) — 3rd confirmation → promotion proposed below. The dart-is-optional framing was right again, and the shark-gap axis measured a meaningless 1-point delta for the third straight time while the real gap was fighter selection.
4. `anchor-equivalence-fifth-validation` (codified) — 10th validation: the cheap twins (Johns, Foro) of the expensive cluster both won, and Johns carried the 47k-field winner.
5. `exact-roster-duplication-is-superlinear-in-consensus` (was hypothesis, now **validated**) — the most-copied consensus roster in your SE hit 614 points and finished 8th split ELEVEN ways, about 2.5-3x what naive math predicts. A consensus build is capped in prize value before the fights start.

**Promotions from hypothesis to validated (2 more):**
6. `okay-tier-is-a-dumping-ground` — the board again put half the fighters (12 of 23) in `Okay`, and that bucket again hid the slate-deciders: Montanha (98.6, in BOTH winners) and Salkilld (104.7, the main-event winner) were buried there next to 1.5-point busts. Tier ordering came back out of order for the third straight graded slate.
7. `grade-gates-have-no-discriminating-power-in-mma` — the self-check re-graded all 101 entered lineups with perfect hindsight and flagged NONE of them, across finishes from top 1% to bottom 2%. About 110 straight clean lineups is a checker that cannot tell good from bad. Treat a clean MMA grade as no information until a gate is fixed.

**Contradiction added (1):**
8. `projected-own-understates-consensus-chalk-convergence` (codified) — FIRST mechanism failure (1 of the 2 needed before a demotion proposal). The rule said adjust the consensus name's ownership UP; Gamrot (both articles' #1 AND the projected leader at 53%) came in at 39-41%, while the crowd concentrated on Thainara instead (+25 over projection). Boundary worth testing before any narrowing: this was the first slate where the consensus name was an UNDERDOG — the field may only over-converge on consensus favorites.

**New hypothesis born (1):**
9. `the-single-bullet-gets-the-least-disciplined-build` — across four straight slates, the rule-breaking slots landed in the single-entry bullets (McGregor 7/12, the dead coin-flips 7/19, the Cowan punt 8/2, Goff/Sutherland/Gamrot 8/9) while the multi-entry blocks stayed inside the rules. The Sim data makes it measurable: 84% of your own pool beat the hand-picked bullet, while the 100-entry block sat at pool average. Rule to test: bullet first, pre-lock check on it, prefer the Sim-pool pick flow.

**Not updated, on purpose:** `field-value-side-vs-your-named-converter` (2 of 3) — you mostly rostered the named converters this slate, so the error it describes never occurred; a non-event is not a confirmation. `cap-single-favorite-exposure` — no favorite exceeded the ~60% cap in the 100-entry block (Salkilld topped out at 38%), so no test.

## Venue file changes

This section covers what the slate taught you about the place it was held.

MMA keeps no venue files by design (only NASCAR tracks and PGA courses have them — fight outcomes do not depend on the building), so no file was created or edited. For the record, the one venue-adjacent observation: this was a 12-fight UFC Apex card and the winning scores came from volume and control (winners' fighters scored 98-129 with several decisions), not from a knockout parade — and in the main event the vendor's win probability (Salkilld 55%) beat both articles' narrative lean (Gamrot). That is a sources note, not a venue note.

## Ledger hygiene

This section is housekeeping on your book of lessons: each flagged entry gets a keep-or-cut decision. The ledger held 30 lessons at flag time (now 31 with the new hypothesis). No lesson references a removed feature, so no feature-based retirements.

### Stale ideas (0 confirmations, been around a while) — 4 flagged, ALL KEEP

- `confirmed-vs-speculative-news` — **KEEP.** Its trigger (speculative injury news breaking near lock) simply has not happened in 8 slates; this week's only news was confirmed and priced. An untested idea is not a wrong idea.
- `showdown-trust-cpt-own-not-projected-overall-own` — **KEEP.** Captain-mode showdown has not run since 6/14; the lesson cannot fire on classic cards. Format-gated, not stale.
- `showdown-captain-the-ceiling-pair-the-smash` — **KEEP.** Same reason: no showdown card since the merge that created it.
- `exact-roster-duplication-is-superlinear-in-consensus` — **KEEP, and it is no longer stale:** it earned its first confirmation this slate (the 11-way-duplicated roster splitting 8th place) and was promoted to validated.

### Near promotion (2 of 3 confirming slates) — what the third slate must show

- `sharp-envelope-is-a-rate-not-a-per-bullet-quota` — **the third confirmation arrived this slate.** Promotion proposed below.
- `field-value-side-vs-your-named-converter` — **KEEP at 2 of 3.** The third slate must show the specific mechanism: the strategy names a low-owned converting favorite as the leverage side of one fight, the entries roster that fight's HIGHER-owned opposite instead, and the named side's result shows the double loss (lost the fight AND handed back the leverage). This slate you took the named sides, so it went untested.

### Overdue promotion (≥3 confirming slates, not codified) — 1 flagged, HOLD

- `showdown-cap-single-favorite-exposure` — **HOLD, do not codify yet.** The counter sees 3 slates, but the ledger's own 8/2 note (user-approved) says the 8/2 confirmation is the same Cepo event already credited to the asymmetric-weighting lesson, and one event should not buy two promotions. Independent count: 2 of 3. This slate provided no test (no favorite above the cap). It codifies the first time an over-carried favorite (>~60% of a multi-entry block) busts and sinks the block. The draft edit is pre-written in the proposals section so it is ready when that slate arrives.

### Merge candidates — 30 pairs flagged, ALL KEEP-SEPARATE

Every flagged pair is a deliberate `[[cross-link]]` — two lessons that reference each other because their mechanisms touch, which is exactly what the ledger's linking convention asks for. Reviewed by cluster:

- **Leverage-definition cluster** (secondary-plays / binary-leverage / low-own-finisher / finish-capable-favorite / winning-se-shape / distance-not-low-ceiling / fade-on-structure and their pairs) — distinct mechanisms at different steps: what leverage IS, where it fails by field size, who fills the slot, and how fades are justified. Merging would blur codified rules that fire at different moments. KEEP-SEPARATE.
- **Portfolio-correlation cluster** (no-identical-cores / cap-single-favorite / shared-coin-flip-slots / flex-spine [already merged & retired 8/2]) — three live lessons about three different objects: shared anchors, one over-carried favorite, shared binary slots. The true duplicate in this cluster was already merged on 8/2. KEEP-SEPARATE.
- **Ownership-measurement cluster** (trust-cpt-own / projected-own-understates-convergence / exact-roster-duplication / grade-gates) — one is showdown-only, one is classic-format, one is about roster-level duplication, one is about the Grade tab's inputs. Same theme, four different measurements. KEEP-SEPARATE.
- **Envelope cluster** (rate-not-quota / one-leverage-swing / field-size-calibration and their pairs) — rate-not-quota is proposed for codification below; folding others into it now would muddy what the user is approving. KEEP-SEPARATE.
- **Okay-tier pairs** (okay-tier ↔ finish-capable-favorite / winning-se-shape) — the board-quality lesson and the play-quality lessons grade different artifacts (the player pool vs the build). KEEP-SEPARATE.

## Proposed codifications

This section proposes permanent rule changes. Nothing here is applied until you click Approve.

**1. Codify `mma-se-2026-07-19-sharp-envelope-is-a-rate-not-a-per-bullet-quota` (3 mechanism confirmations: 7/19 origin, 8/2, 8/9).**

Add to `framework.md`, after the "Step 3 — Field-Size Calibration" section:

> ### Sharp-Envelope Targets Are Rates, Not Quotas (8/9/26 — 3-slate validated)
>
> A pro's observed envelope (e.g. "a sub-5% piece in 15% of lineups") describes a RATE across a large portfolio. Never restate it as a per-lineup quota on a 1-3 bullet slate.
> - State every envelope target as "in ~N of 10 lineups."
> - On a 1-3 bullet slate, any sub-50% rate is OPTIONAL: take the dart only when its win equity clears the mid-own converter it would replace. The modal sharp MMA lineup carries NO dart (winners' dart rate measured 0.0 in the last four slates' contests).
> - Treat the shark-gap axis ranking as noise unless BOTH are true: a tracked pro was actually in-field, and the measured delta is material (several ownership points, not ≤1.3). Three straight slates of ≤1-point deltas alongside 49-point finish gaps show the MMA leak is win-side selection, not structure.

Also update the lesson's `status` to `codified` and `codified_in` accordingly on approval.

**2. HOLD (pre-written, not proposed this slate): `showdown-cap-single-favorite-exposure`.** When an independent third slate confirms (an over-carried favorite busting a multi-entry block), add to `framework.md` under diversification: "Cap any single favorite at ~60% of a multi-entry block, and always carry ≥2 entries that fade the chalkiest favorite. Cap, never zero — zero exposure on both sides of an equivalence pair is an anchor-equivalence breach (6/20)." Not for approval today; recorded so the review that gets the third confirmation can propose it verbatim.

**3. Demotions: none.** The convergence-adjustment rule took its FIRST contradiction (threshold for a narrowing proposal is 2). Watch item for next slate: if the consensus name is again an underdog and again comes in under projection, propose narrowing the rule to consensus FAVORITES only.

**4. Merges: none** (all 30 flagged pairs kept separate — see Ledger hygiene).

## What this means for next slate

1. Build the single-entry bullet FIRST, and make every one of its six fighters answer "how does he WIN?" — the bullet has carried the rule-breaking slots four slates running, and this week it cost you your worst SE finish while your disciplined 100-entry block was one swap from winning $20K.
2. Try picking the SE bullet from the Sim pool's per-contest pick flow instead of by hand — 84% of your own already-built pool would have beaten this week's hand-picked bullet.
3. Keep trusting the converter screen — the 14-16% underowned favorites (Johns, Foro) were the slate's real leverage again, and the field winner was carried by exactly the fighter your strategy named.
4. Stop trusting a clean lineup grade in MMA — the checker has now passed ~110 straight lineups including your worst ones, so a clean grade means nothing until the no-win-path gate exists.
5. Approve the rate-not-quota codification, and next slate double-check the "assume the consensus name runs 60%+" adjustment if the consensus play is an underdog — the crowd walked away from Gamrot this week instead of piling on.
