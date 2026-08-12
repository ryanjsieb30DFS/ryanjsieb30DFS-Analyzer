# Post-autopsy review — Iowa Corn 350, Iowa Speedway (2026-08-09)

## Process scorecard

This section grades HOW you played the slate — the decisions, not the results.

**The reading gets an A-. The hand-off gets a D. This is the third slate in a row with that exact split.**

**The pre-flight prep was honored.** The venue file for Iowa did not exist before this slate, so the strategy built one from the DFR data images and marked it unverified — that is exactly what the ritual asks for. The rule that two similar chalk anchors are really one bet (Anchor-Equivalence) was surfaced twice: the Bell/Byron/Hamlin price cluster, and the Elliott-vs-Larson identical-projection pair. The open lessons were applied in the text: the strategy treated Blaney's 52% projected ownership as a floor, not an estimate, and it warned that the cheap value would jam at lock.

**The strategy's reads were mostly right — some spectacularly so.**

- The top tier (Core) was the best board this tool has produced. Its three names averaged 95.1 real points: Bell scored 115.1 (the highest score in the race), Blaney 101.0, Hamlin 69.3. Bell and Blaney were in the winning lineup of BOTH contests.
- The ownership-jam call was right. The strategy said Blaney's 52% "could be 60" at lock. It went to 74-82% — about 4 of every 5 teams had him — and he was still worth it.
- The low-owned decider list (the leverage screen) found winners AGAIN — for the fifth slate running. Nemechek (named on the list at 5% projected) was in the 588-field winning lineup. Stenhouse (named at 2%) was in the 392-field winning lineup.

**Three reads missed, and they share a shape.**

- Logano was tiered Good; he became the single biggest trap of the slate. About half of the losing half of the field had him (46-49%), zero winners did, and he scored just 25.6.
- Both "same projection, fewer teams" alternatives busted: the strategy pointed at Reddick over Bubba (Reddick scored -26.0, Bubba 65.0 and was in both winners) and at Larson over Elliott (Larson -17.1, Elliott 51.3). One slate of the coin landing the other way is variance, not a broken rule — but note that in both cases the crowd's side hit.
- Gibbs was tiered only Okay at 20% projected ownership; he jammed to 41-44% at lock, scored 66.7, and was in every one of the 392 field's top-5 lineups.

**The entries are where the slate was lost, and each entry lost it a different way.**

- The 392-field entry (finished 254th of 392 — worse than 64% of the field) dropped consensus anchors with no stated reason. It left out Bell (the top score) and Gibbs, and spent those slots on Byron (a known trap in your fields, 0% of winners) and Reddick (-26.0). That is the fish shape your Indy lesson describes: dropping correct anchors for middle-owned substitutes.
- The 588-field entry (finished 238th of 588 — middle of the pack) made the OPPOSITE error. It held six popular names, nothing else — average ownership 38.4% per slot, zero low-owned pieces. Three other entrants had the IDENTICAL roster (duplicated 4 times). The strategy had warned, with counts, that a Blaney-plus-another-popular-name shell is shared with about a hundred opponents. All chalk with no separator cannot win even when the chalk hits.
- The one-swap check (near-miss) confirms these were structural losses, not bad luck: the best single swap still would not have won either contest; you were 2-3 swaps away in both.

**What to do about it:** the fix is not better reading — the reading found both winners' key pieces. The fix is the build-time gate proposed below: no entry locks without a name from the strategy's own decider list.

**Shark head-to-head (the tracked pros in your 588 field).** The pros ran 35.1% average ownership per roster slot; you ran 38.4%. For the first time since tracking began, you were MORE chalky than the pros — every prior gap ran the other way (Atlanta -15.7, Indy -11.4, Chicagoland's gap was on low-owned pieces). The axis keeps being the same one — how ownership is spread across the six slots — and you keep oscillating around the pros' shape instead of copying it. The mechanism, stated plainly: the pros hold every consensus anchor and make exactly one slot do the differentiating; you either drop anchors (the old leak) or, this week, kept all the anchors and gave NO slot the differentiating job. This recurring axis is now recorded as a confirmed lesson (promoted to validated below). Worth knowing: even the pros only reached the top 21% here — the winners were untracked locals — so the envelope is a shape target, not a guarantee.

**Discipline (did the entries follow the strategy's own plan — adherence).** No hard fades existed, so none were violated. But the per-contest view shows 3 flags the averages hide:

- Byron was called UNDERWEIGHT (own him less than the field). He was in 100% of your 392-field entries (1 of 1) — over the cap inside that contest — and 0% of your 588-field entries. Pooled, that averages to "followed"; per contest it was one violation and one zero. The violation cost: Byron was 0% of that contest's winners.
- Bubba Wallace, same pattern: 100% in one contest, 0% in the other. That one happened to score (Bubba 65.0, in both winners) — but a broken own-call that scores well is still a broken own-call; results do not launder discipline.
- Elliott was called UNDERWEIGHT and got ZERO in both contests. Underweight means "less than the field," not "none" — zeroing is a silent hard fade the strategy never argued. Elliott scored 51.3 while the pivot the strategy preferred (Larson) scored -17.1.
- The leverage screen: 12 low-owned deciders named, 0 reached an entry. Third straight slate at 0 of 12. This is the headline discipline finding and the promotion driver below.

**Pool tiers (did the board's rankings hold up — pool calibration).** Out of order for the third straight slate, but for a new reason. Core averaged 95.1 — excellent. But Good (18.6 average) finished BELOW Okay (26.5), dragged down by Larson (-17.1), Reddick (-26.0) and Logano (25.6). The Fade tier stayed at the bottom (12.5) with no leakage — and note the board APPLIED the Indy lesson correctly this time: the ceiling-tagged low-owned plays (Keselowski and friends) were held in Okay with a Leverage label instead of being buried in Fade, and no buried definer burned you. The remaining tier problem is that the Good tier absorbed the ownership-discount picks; one slate is not enough to birth a lesson on that, but it goes on watch.

**Pool vs picking (Sim measurements).** No sim_autopsy.json was archived for this slate, so there is no pool-vs-picking or sim-metric check to run this time.

**Grader check.** The pre-lock grader called both lineups clean and they finished 64.8th and 40.5th percentile. A clean grade on a 4-times-duplicated all-chalk lineup is a calibration note for the grader's dupe warning, worth watching next slate.

## Lesson ledger changes

This section lists what changed in your notebook of lessons (the ledger), in plain words.

1. **"The decider list must reach the entries" (`nascar-2026-07-21-definer-screen-must-reach-entries`) — second confirmation added; now at 3 confirming slates and proposed for codifying.** The list named two winners' pieces (Nemechek, Stenhouse) and for the third straight slate zero of its 12 names reached an entry. A rule that hits promotion (3 slates confirming the reason it works) gets a proposal below; you approve it in the app.
2. **"Real lock ownership piles onto the consensus harder than the vendor projects" (`nascar-2026-07-21-se-actual-own-concentrates-on-consensus`) — second confirmation added; now at 3 confirming slates and proposed for codifying.** Blaney went 52% projected → 74-82% actual; Gibbs 20% → 41-44%; meanwhile Byron, Hamlin, Larson and Reddick all deflated. The near-tie resolved into a landslide exactly as the lesson predicts, in a third different field size.
3. **"Hold the anchors, differentiate in the sixth slot" (`nascar-2026-07-26-anchors-held-differentiate-in-sixth-slot`) — first confirmation added; promoted from an idea being tested (hypothesis) to a proven-once idea (validated).** Both halves of its mechanism fired, one per contest: the 392 entry dropped correct anchors (the old fish shape), and the 588 entry held anchors but gave no slot the differentiating job and got duplicated 4 times.
4. **"A diagnosed gap must reach a roster" (`nascar-2026-05-01-portfolio-gaps-addressed-pre-lock`, already codified) — post-codification evidence added.** The gap was diagnosed in writing a third time and forfeited a third time. The rule is right; codifying it did not change behavior, which is why the build-time gate in item 1 matters.
5. **New idea to test (hypothesis) born: "The decider band widens in small fields" (`nascar-2026-08-09-definer-band-scales-with-field-size`).** The 588-field winner separated entirely with three 10-18%-owned pieces (Chastain, Nemechek, Buescher) — no sub-10% dart at all — because in a field that small, three mid-teens pieces already make a roster effectively unique. The reason (the mechanism): expected copies of a roster scale with field size times how popular its players are. In bigger fields the sub-10% dart is still required.

## Venue file changes

This section says what was added to the Iowa Speedway track notes.

Appended a date-stamped post-race observation to `rules/nascar/tracks/iowa_speedway.md`: the front-tier dominator read held a third straight year (Bell 115.1 + Blaney 101.0 carried both winners; winning totals matched the 2025 optimal almost exactly); the winners' separation came from the 10-18%-owned band (Chastain, Nemechek, Buescher) plus one true dart in the smaller field (Stenhouse — an Iowa winner's piece in 2024 and 2026, as was Chastain in 2025 and 2026); the jammed recency value (Gilliland, Cindric, Bowman, Logano) all busted; and the lock-ownership jam numbers. The file keeps its "unverified track description" header — that flag is about the track write-up itself, which still awaits your confirmation.

## Ledger hygiene

This section is notebook maintenance: which stalled ideas to keep or throw out, which are close to graduating, and which overlapping entries to combine.

**Stale hypotheses (ideas with zero confirmations that have had chances) — all four KEEP.** Every one of them is conditioned on a track type that has not raced since the idea was born (the slates since have been flat ovals, one intermediate and one superspeedway at birth). An idea untested because no relevant slate occurred is kept, not retired:

- `nascar-2026-06-28-roadcourse-deepback-revives-on-strategy` — KEEP. Needs a road course; none has run since Sonoma.
- `nascar-2026-07-12-narrative-suppressed-elite-is-leverage` — KEEP. Needs an article-plus-field narrative demoting an elite org at a track type where it holds a codified edge; no slate since has presented that trigger.
- `nascar-2026-07-14-superspeedway-doms-correlate-not-substitute` — KEEP. Needs a drafting track (Daytona/Talladega/Atlanta); none since its birth slate.
- `nascar-2026-07-14-multiyear-lapsled-weak-perrace-signal` — KEEP. Same: superspeedway-only mechanism, untestable since Atlanta.

**Near promotion (2 of 3 confirming slates) — both graduated this slate.** `definer-screen-must-reach-entries` needed a third slate where the screen produced real deciders and the entries carried none: Iowa was exactly that (Nemechek and Stenhouse in the winners, 0 of 12 entered). `se-actual-own-concentrates-on-consensus` needed a third slate where the consensus side jammed and the co-anchors deflated: Blaney 52→82 and the Bell/Byron/Hamlin landslide delivered it. Both codification proposals are below.

**Merge candidates (21 pairs) — KEEP-SEPARATE, all 21.** Every flagged pair is linked by a deliberate `[[id]]` cross-reference, and in each case the link marks a relationship — one lesson scopes, extends, or complements the other — not a duplicate statement. Merging would erase the scoping (which track types a rule applies to) that several of these pairs exist to record. Pair-by-pair:

| Pair | Verdict | Why (one line) |
|---|---|---|
| midpack-pd ↔ roadcourse-deepback-revives | KEEP-SEPARATE | The second is the road-course exception still being tested; folding it in would bury an untested claim inside a codified rule. |
| anchor-equivalence ↔ anchor-equivalence-not-parity | KEEP-SEPARATE | One says "cover the twin," the other says "don't hedge 50/50" — opposite failure modes of the same rule. |
| bet-sizing-reflects-inverse ↔ anchor-equivalence-not-parity | KEEP-SEPARATE | Bet-sizing is general; not-parity is its anchor-specific case. Both are codified in different doc sections. |
| carry-a-sub5-dart-mme ↔ midpack-pd | KEEP-SEPARATE | Where the dart comes from vs that a dart must exist — different decisions. |
| backup-car-not-auto-fade ↔ injury-narrative-not-a-fade | KEEP-SEPARATE (already done) | The second is already retired-as-merged into the first; nothing left to do. |
| hms-intermediate-double-up ↔ narrative-suppressed-elite | KEEP-SEPARATE | One is an HMS track-type edge; the other is a general rule about narratives suppressing ANY codified edge. |
| mechanism-check ↔ narrative-suppressed-elite | KEEP-SEPARATE | Meta-rule vs a specific instance class. |
| anchor-equivalence ↔ narrative-suppressed-elite | KEEP-SEPARATE | Linked only because the Chicagoland story touched both. |
| anchor-equivalence ↔ superspeedway-doms-correlate | KEEP-SEPARATE | The second EXEMPTS pack tracks from the first — a scoping record that must stay visible on its own. |
| mechanism-check ↔ superspeedway-doms-correlate | KEEP-SEPARATE | Meta-rule vs instance. |
| multiyear-lapsled ↔ superspeedway-doms-correlate | KEEP-SEPARATE | Dominator-picking signal vs dominator-stacking structure — same track type, different decisions. |
| carry-a-sub5-dart-mme ↔ definer-screen-must-reach-entries | KEEP-SEPARATE | MME portfolio rate vs SE per-bullet gate; the SE rule is codifying now and should stand alone. |
| portfolio-gaps-addressed ↔ definer-screen | KEEP-SEPARATE | Principle (codified) vs its mechanical enforcement (codifying now) — the pairing is the point. |
| mme-or-fade-means-fade-in-se ↔ definer-screen | KEEP-SEPARATE | What qualifies as a definer vs that one must be entered. |
| anchor-equivalence ↔ se-actual-own-concentrates | KEEP-SEPARATE | The second predicts how equivalence pairs RESOLVE at lock; it refines, not repeats. |
| ownership-shift-full-reevaluation ↔ se-actual-own-concentrates | KEEP-SEPARATE (already done) | The first is already retired-as-merged into the second. |
| sound-chalk-toward-field-rate ↔ anchors-held-differentiate | KEEP-SEPARATE | Exposure rate on one chalk piece vs the whole-roster shape rule. |
| anchor-equivalence ↔ anchors-held-differentiate | KEEP-SEPARATE | Substitution between anchors vs never dropping the anchor tier at all. |
| definer-screen ↔ anchors-held-differentiate | KEEP-SEPARATE | The two halves of the winning shape (the definer slot; the anchor slots) — each graded separately every slate. |
| mme-or-fade-means-fade-in-se ↔ fade-tier-buries-definers | KEEP-SEPARATE | Article-tag reading vs board-tiering behavior; the second is a tool-calibration lesson. |
| definer-screen ↔ fade-tier-buries-definers | KEEP-SEPARATE | Entering a definer vs where the board displays it. |

**Removed-feature check:** no live lesson references a removed feature. The two that did (Sim-ROI selector, post-ROI gold standard) were already retired with the SaberSim pipeline.

## Proposed codifications

This section proposes permanent rule-book changes. Nothing here is applied until you click Approve in the app.

**1. Codify `nascar-2026-07-21-definer-screen-must-reach-entries` (3 confirming slates: North Wilkesboro origin + Indy + Iowa).**

Proposed framework.md edit — add to Step 6 mandatory checks:

> **#11 — Definer hand-off gate (codified 2026-08-09, NW + Indy + Iowa).** Before any SE bullet is entered, it must carry EXACTLY ONE driver from the strategy's sub-10% definer list (the Grade tab's no-leverage flag is the checkpoint; in sub-600 fields a 10-18%-owned listed PD play may serve as the definer — see the field-size hypothesis). Five-slate evidence: the screen named slate-deciders every time (SVG/Suarez/Gilliland at NW; Heim/Keselowski at Indy; Nemechek/Stenhouse at Iowa — the latter two in both Iowa winners) while entered-lineup usage ran 0%, 50%, 0/12, 0/12, 0/12. The analysis reliably produces the edge; only a build-time gate transfers it.

Proposed philosophy.md edit — add to On Process Discipline:

> **A list is not a lineup.** Three consecutive slates diagnosed the leverage gap in writing and entered zero of 36 named deciders while five of them sat in winning lineups. Analysis without a build-time gate transfers zero equity; the entered roster is the only artifact that scores.

**2. Codify `nascar-2026-07-21-se-actual-own-concentrates-on-consensus` (3 confirming slates: North Wilkesboro origin + Indy + Iowa, across 392-1,470 field sizes).**

Proposed framework.md edit — add to Quick-Reference Decision Heuristics:

> **SE lock-ownership floor rule (codified 2026-08-09).** In small SE fields, treat the vendor's projected ownership on (a) the top-projected consensus anchor and (b) the loudest article-endorsed cheap value as a FLOOR, not an estimate — expect +15 to +30 points at lock (NW: Bell 46→67, Herbst 22→50; Indy: Gilliland 15→46; Iowa: Blaney 52→82, Gibbs 20→44). Expect projected near-ties between equivalent anchors to resolve into a landslide (one side jams, the others deflate: Iowa's 35/33/32 trio locked at 38/25/18). Any leverage case built on a projected ownership number must survive the jammed version of that number.

**3. No demotions.** No codified rule recorded a mechanism failure this slate — the codified chalk rules (50%+ chalk toward field rate) were confirmed by Blaney at 82% scoring 101, and the track-type-scoped rules did not trigger on a flat oval. Nothing meets the 2-contradiction bar.

## What this means for next slate

This section is the whole review in five sentences.

1. Before you enter any lineup, check it carries one name from the strategy's decider list — three straight slates the list held a winner's piece and your entries held none, and that one check is worth more than every other improvement combined.
2. Hold the popular anchors the data confirms AND make exactly one slot low-owned — this week one entry broke the first half (dropped Bell, the race's top scorer) and the other broke the second half (six chalk names, duplicated 4 times).
3. An "own him less than the field" call (underweight) means less, not zero and not everywhere — put the player in the entry where the payout tolerates him, not 100% in one contest and 0% in the other.
4. Treat projected ownership on the consensus anchor and the loud cheap value as the minimum, not the estimate — Blaney's 52% became 82% at lock, and the jammed cheap value (Gilliland, Cindric, Bowman, Logano) is where the losing half of the field lived.
5. In your small fields, a 10-18%-owned player with a real points path can be the separator — the 588-field winner used three of them and no sub-10% dart at all — so judge "is this lineup different enough" by expected copies, not by one ownership cutoff.

## Applied

Applied 2026-08-09 (user-approved). Codification 1: added mandatory check **#11 — Definer hand-off gate** to framework.md Step 6 (the check-failure line now reads "checks 8-11") and the **"A list is not a lineup"** paragraph to philosophy.md's On Process Discipline. Codification 2: added the **SE lock-ownership floor rule (codified 2026-08-09)** blockquote to framework.md's Quick-Reference Decision Heuristics. lessons.yaml: `nascar-2026-07-21-definer-screen-must-reach-entries` and `nascar-2026-07-21-se-actual-own-concentrates-on-consensus` both set to `codified` with `codified_in` naming those doc sections. Ledger hygiene: all decisions were KEEP / KEEP-SEPARATE (4 stale hypotheses kept as untestable-since-birth; all 21 merge-candidate pairs kept separate), so no retirements or merges were applied. No demotions.
