# Post-autopsy review — PGA $3M Open 2026 (TPC Twin Cities, logged 2026-07-26)

Contest: PGA Tour $8K Eagle (5-Max), 1,902 entries, 4 bullets. Best finish **rank 64 / 3.4 pctile — the best of the entire logged sample** (prior best 5.0), and the near-miss counterfactual says the best entry was **one swap (Im → Matsuyama) from winning the contest outright**.

## Process scorecard

**Pre-flight checks: honored, and visibly so in the doc's substance.**
- **Venue file:** the TPC Twin Cities profile (skill compression, fit-model boost/dock logic, water trapdoor, random winners) is threaded through every section — Edges & tensions leads with it, the Woodland/Mitchell/Brennan dock analysis and the Chatfield/Bezuidenhout boost analysis come straight from it.
- **Anchor-Equivalence:** surfaced as mandated, correctly located in the $9K tier (McNealy/Kitayama/Tom Kim within $600 and ~1 own point). It graded well: the trio's ceilings were read right (Kitayama tallest on paper) but the tier's actual winner was the CHEAPER equivalence ticket the doc also named — Koivun at half the trio's ownership, who outscored all three.
- **Open lessons applied (by name, in text):** the self-erosion guard (Kohles +11.9 and the whole coffin list sized as "notes, not conviction bets"), the gated CH scan (Cam Davis explicitly gated to "lottery slot"), the vendor-independent ceiling board (Nakajima, "a 99-point ceiling at 4% that NO article mentions"), the dart-rate lesson ("ONE sub-5% dart in about half the bullets — your dart rate has run ABOVE the in-field pros two straight slates"), fade-needs-ownership-to-materialize (the Conners fade written WITH its own void condition: "if under ~12%, this premise is void"). This was the most lesson-saturated strategy doc of the sample. None of the applied lessons misfired.

**Did the synthesis hold up against the DK actuals? Largely yes — the best doc-vs-actuals alignment logged.**
- Slate-defining plays: **Koivun 155.0 @ 16.25%** (55% of top-20) — tiered **Good**, rostered on the best entry. **Matsuyama 126.5 @ 17.25%** (50%) — surfaced as contested, verdict UNDERWEIGHT (see 1c). **Grillo 118.5 @ 13.77%** (30%) — covered at length, rostered 2/4; the doc's lock-window read (9.3% proj vs Sam's 20% steam) split the difference exactly. **Chatfield 100.5 @ 3.94%** (35%) — named on the definers screen and he hit. **Zac Blair 103.0 @ 16.98%** (30%) — **NOT in the doc anywhere**, the slate's one true coverage hole (below).
- Tiers: pool calibration fully ordered — Core 113.8 > Good 79.1 > Okay 63.8 > Fade 47.7. Core was Scheffler (133.5, hit) + Kitayama (94.0, fine). One leakage: **Chandler Phillips, tiered Fade, scored 132.5** — the slate's #3 raw score buried in the bottom tier; noted, but he appears in neither the winners' structure nor the slate-defining list (the field that had him didn't win with him), so it's logged as leakage, not a lesson.
- Fades: Conners (FULL FADE) — own materialized (14.93%), he posted a neutral 78.5; the fade neither paid big nor cost big, though the winner did carry him. Suber (Okay with a steam warning) steamed 12.7→15.7% and busted 30.5 (#3 fish trap) — the warning was right. Kohles UNDERWEIGHT — steamed 19.2→25.7%, posted 103.5; negative leverage at that own, call correct.
- **The misses, honestly:** (1) Blair and **Benjamin James** (19.1% actual own, 31.0 FPTS, the slate's #1 fish trap: 26% of fish, 0% of winners) were the 5th- and 7th-most-owned players in the field and neither existed in the doc — ETR projected both low, so every ownership-keyed screen skipped them simultaneously. One was the trap of the slate, one was a winner piece; the doc could grade neither. New hypothesis born (`unprojected-cheap-steam-screen`). (2) **Denny McCarthy (121.0 @ 2.68%)**, the contest winner's leverage carrier, was not on the 20-name definers screen. (3) **Sungjae Im** (Sky's flag plant, tiered Good) busted 26.5 and was a fish trap — a source-split loss, within variance, but he's also the player whose slot would have won the contest.

**Grader validation:** no lineups flagged; clean pctiles 3.4 / 29.8 / 39.0 / 50.7. Nothing to recalibrate on one slate.

## Shark gap (1b)

**The recurring axis fired a third straight 5-Max: `leverage_pct`, same direction.** 100% of user lineups carried a sub-5% piece vs the in-field pros' 80% (delta +20, after +53.3 at Shinnecock and +60 at Birkdale), and the user out-darted the winners too (3.25 sub-10% per lineup vs the top-20's 2.55, avg own 10.76 vs 12.92). Mechanism, stated plainly: **I spend the differentiation budget below 5% at a higher rate than the pros and the winners do.** This is now a confirmed recurring structural leak — `pga-classic-2026-07-22-dart-rate-exceeds-in-field-pros` promoted to **validated**, with one prong narrowed: this slate two sub-5% pieces WERE slate-relevant (Chatfield, McCarthy), so the durable claim is the RATE gap and dart provenance (from the screen), not "sub-5% never pays."

Two honest counterweights: the gap **narrowed** (60 → 20) with the doc coaching it down, and this was the first logged slate where the user **beat every tracked shark** (best 3.4 vs their 44.7 pctile — the 5 shark entries all landed mid-field). Also note the flip: the historical above-envelope chalk lean is gone; this slate the portfolio sat BELOW the 13% winning envelope. The leak is no longer "too chalky" — it's "one dart too many, and one of them improvised."

## Adherence (1c)

**First fully clean adherence slate: 0 hard-fade violations, 0 soft violations, all 5 contract calls followed; leverage candidates covered 6/12** (same coverage ratio as Birkdale). Trend: Birkdale 1 violation → 3M 0. Discipline improved and the best-ever finish came with it.

But the clean grade exposes a gate limitation that becomes this review's second new hypothesis: the doc called Matsuyama **UNDERWEIGHT** ("genuinely contested… argues for underweight rather than a zero"); the entries took **0/4**, which the adherence gate counts as "followed" (0% < 50%). Matsuyama then hit 126.5, made 50% of the top-20 winners, anchored the contest winner — and the near-miss shows Im → Matsuyama **wins the contest**. At N=4, zero is not underweight; it is a fade the analysis never argued. Results don't launder discipline, and the mirror holds too: this is a process finding even though the portfolio scored well. Born as `underweight-is-not-zero-small-portfolio` (hypothesis — one slate, mechanism-based: the gate cannot distinguish underweight from zero at small N).

Off-contract note: 5 of 24 roster slots went to players appearing nowhere in the doc (Blair, McGreevy, Hodges, Glover, Putnam) — invisible to adherence, which only greps named calls. One (Blair) hit; the doc's cheap-steam hole and the entries' improvisation overlapped on the same name.

## Codified-rule check (1d)

| Codified rule | This slate | Mechanism |
|---|---|---|
| never-zero-value-chalk-anchor | Applied (Scheffler 2/4) | **Held** — 133.5 @ 26.5%; 5th confirmation logged |
| leverage-spine-pairing (w/ sub-19% scope) | No qualifying pair labeled a spine | No trigger |
| portfolio-exposure-cap | Max overlap 2 across 4 bullets | Applied, un-stressed |
| track-slate-lock-stat | Applied (Koivun 55% of top-20 tracked here) | Held |
| se-leverage-cap-two | **Exceeded portfolio-wide** (3.25 sub-10% mean/lineup; L4 ran 4) | Not a mechanism failure this slate (best entry ran 3 and nearly won), but the overage is the same behavior the dart-rate lesson names — watch it, don't demote on a win or a near-win |
| trap-vs-value-chalk (narrowed 7/22) | Applied | **Held in narrowed form** — value chalk Scheffler hit; ownership behavior disposed the split (Suber steam warning right, Kohles sized down on drift). The 7/22 narrowing stands; no further demotion |
| two-build-max / se-primary-contest-selection | Not observable / followed (5-Max) | No trigger |
| ch-scan-needs-skill-gate | Applied both directions | **Held** — Cam Davis (CH, bottom-10 skill) gated to lottery and busted; Chatfield (form/fit) hit; 3rd confirmation logged |
| fade-needs-ownership-to-materialize | Applied prospectively (Conners fade carried its own void condition) | Held — own materialized, fade stood; no new entry logged (evidence thin: Conners was neutral) |
| winning-structure-13own-2to3-darts | Winners 12.92% / 2.55 / 80% unique | **Held** — 4th confirmation; user below envelope for the first time |
| leverage-play-mandatory | Koivun named AND rostered | **Held** — named → rostered → captured for the first time; confirmation logged |
| dose-darts-to-course-variance | Birdie-fest+cut → winners 2.55 | **Held**; confirmation logged |
| mid-owned-value-spine-over-darts | 4 of 5 definers in the 13-18% band | **Held** — 4th confirmation, and the selection finally caught band members |
| entered-lineups-must-trace-to-plan | Graded pre-lock (lineup_grade.md archived), 0 flags | Held via the Grade-tab expression; 5 off-doc slot picks noted above remain the residual gap |

No codified rule has a new mechanism failure; no demotions proposed this slate.

## Lesson ledger changes

- `never-zero-value-chalk-anchor` — **+confirmation** (Scheffler, 5th confirming slate).
- `ch-scan-needs-skill-gate` — **+confirmation** (Cam Davis gated/busted vs Chatfield form-side hit).
- `winning-structure-13own-2to3-darts` — **+confirmation** (12.92/2.55/80%; user below envelope for the first time).
- `leverage-play-mandatory` — **+confirmation** (Koivun: named → rostered → captured; leverage capture 0.6, sample best).
- `dose-darts-to-course-variance` — **+confirmation** (birdie-fest+cut corner, winners 2.55).
- `mid-owned-value-spine-over-darts` — **+confirmation #4** (definers 13-18% band; caveat flipped positive).
- `single-vendor-overweight-self-erosion` — **+confirmation #2 = 3rd mechanism slate** (Kohles drift 19.2→25.7 on the +11.9 coffin; McNealy boundary case logged). **Meets promotion bar → Proposed codifications.**
- `vendor-independent-ceiling-scan` — **+confirmation #2 = 3rd mechanism slate** (top-3 scores all doc-named; board-only catches Nakajima/Chatfield; no vendor-cool elite missed). **Meets promotion bar → Proposed codifications.**
- `dart-rate-exceeds-in-field-pros` — **+confirmation #1, promoted hypothesis → validated** on the narrowed statement (rate gap recurs 3rd slate at +20; "definers never sub-5%" prong dropped).
- `darts-come-from-the-screen` — **untouched** (evidence mixed at lineup level this slate: the all-doc-names entry finished 3.4 but the all-screen-darts entry finished worst of the four while an off-screen improvised dart hit; single-slate ordering is variance, no mechanism verdict).
- **New hypothesis:** `pga-classic-2026-07-26-unprojected-cheap-steam-screen` (Blair/James: the vendor-low, field-crowded cheap tier bypasses every ownership-keyed screen at once).
- **New hypothesis:** `pga-classic-2026-07-26-underweight-is-not-zero-small-portfolio` (Matsuyama 0/4 graded "followed"; at N≤5 underweight means exactly one bullet).

## Venue file changes

`rules/pga_classic/courses/tpc_twin_cities.md`: header upgraded from UNVERIFIED to first-autopsy-verified, and a 2026-07-26 per-slate observation appended — birdie fest confirmed (676.5 wins it, seven players 118+), fit model verified both directions (Blair/Chatfield/Bezuidenhout boosts hit; Finau/Coody docked-bomber busts; Knapp the exception), CH list split exactly along the skill gate (Grillo hit, Cam Davis lottery-bust), random/young-winner tendency intact (Koivun 155, a 2.68% McCarthy carries the winner), and a venue-specific ownership quirk: Scheffler's price lock funnels the field into the same $6-7K pool and the cheap comfort names steam far past vendor projection (Kohles +6.5, Blair +12, James ~+14 pts).

## Ledger hygiene

**Near promotion (3):**
- `contrarian-needs-leverage-anchor` (validated, 2/3) — **KEEP, no trigger this slate.** No entered build was a contrarian stack with/without a coffin-grade leverage anchor in the lesson's sense (L4 was chalk-anchored chaos, outside the trigger). The third slate must show: a contrarian build whose coffin-grade leverage-floor anchor absorbs 3-of-4 mid-range busts and keeps a path (or the negative — an anchor-less contrarian build collapsing to a near-zero).
- `single-vendor-overweight-self-erosion` — **third slate confirmed THIS review** (Kohles: narrative name, own drifted up 6.5 pts toward the published optimal, gap eroded at lock). Promotion proposed below.
- `vendor-independent-ceiling-scan` — **third slate confirmed THIS review** (scan ran; definer-outside-the-lens streak broken a second straight slate; the Burns-shaped criterion — a vendor-cool mid-band elite — had no victim this slate and the top-3 scores were all doc-named). Promotion proposed below.

**Merge candidates (9 pairs):**
- `leverage-spine-pairing` ↔ `leverage-spine-needs-sub20-combined-own` — **already merged 2026-07-22** (the second is retired with the scope condition folded into the first). Stale flag; no action.
- `course-history-sub5-scan` ↔ `major-pedigree-in-form-leverage` — **both retired**; cross-links are evidence trail. No action.
- `ch-scan-needs-skill-gate` ↔ `major-pedigree-in-form-leverage` — second is retired (merged into ceiling-scan). **KEEP-SEPARATE**; link is provenance only.
- `mid-owned-value-spine-over-darts` ↔ `major-pedigree-in-form-leverage` — second retired. No action.
- `mid-owned-value-spine-over-darts` ↔ `vendor-independent-ceiling-scan` — **KEEP-SEPARATE.** Distinct mechanisms: WHERE slates are won (the 10-16% band) vs HOW the board that finds them is built (vendor-independent identification). If the scan codifies, they become adjacent framework text, which is the right relationship.
- `single-vendor-overweight-self-erosion` ↔ `vendor-independent-ceiling-scan` — **KEEP-SEPARATE.** A sizing guard on the vendor's self-referential gaps vs a coverage scan for what the vendor never flags; this slate demonstrated they fail on different names (Kohles vs Blair/McCarthy).
- `dose-darts-to-course-variance` ↔ `dart-rate-exceeds-in-field-pros` — **KEEP-SEPARATE.** Per-lineup dart COUNT by course archetype vs portfolio-level sub-5% RATE vs the pro envelope; the statements already discriminate themselves explicitly.
- `design-exposures-before-lineups` ↔ `darts-come-from-the-screen` — **KEEP-SEPARATE for now.** Coverage governor (how much of the screen gets rostered) vs dart provenance (where dart slots may come from). Revisit for merge if/when the screen lesson validates; today one is codified and one is an unconfirmed hypothesis.

**Stale hypotheses:** none flagged (the two open hypotheses are one slate old and both were exercised this review). **Removed-feature check:** no live lesson references a removed feature (`act-on-redteam-portfolio-findings` was already retired on that basis 7/18).

## Proposed codifications

**1. CODIFY `pga-classic-2026-06-17-single-vendor-overweight-self-erosion`** (RBC origin + Birkdale + 3M = 3 mechanism slates; drift fired on Rai 25→30, Fitzpatrick 25.5→37.6, Kohles 19.2→25.7 — all narrative names — and correctly did NOT fire on stable value chalk Burns).

Proposed edit — `framework.md`, Section 6 (Anchor Selection Logic), append:

> **Single-vendor self-erosion guard (codified 2026-07-26).** An edge defined as one vendor's published optimal exposure minus that same vendor's ownership projection (a coffin overweight) is a sizing NOTE, never the portfolio's biggest bet, unless a second independent reason (form, skill, course fit) supports it. On narrative/rising names in vendor-subscriber contests, expect actual ownership to drift UP toward the published optimal and erode the gap by lock (Rai 25→30% RBC; Fitzpatrick 25.5→37.6% Birkdale; Kohles 19.2→25.7% 3M). The guard does NOT fire on stable, floored value chalk sitting at flat projected own (Burns, Shinnecock) — absent a concrete reason to expect own inflation, default to the trap-vs-value read and play the overweight.

On approval: set status `codified`, `codified_in: "framework.md — Section 6 Anchor Selection Logic (Single-vendor self-erosion guard)"`.

**2. CODIFY `pga-classic-2026-07-01-vendor-independent-ceiling-scan`** (Travelers origin + Birkdale + 3M = 3 mechanism slates; the definer-outside-the-lens streak — five straight slates before Birkdale — has now been broken twice in a row with the scan running).

Proposed edit — `framework.md`, Section 2 (Slate Diagnostics — Run Before Building), append:

> **Vendor-independent ceiling board (codified 2026-07-26).** Before writing Top plays, independently list the ~12-15 highest-ceiling players for the week from the projections + form (best ball-strikers, hottest approach numbers, elite anchors) REGARDLESS of whether the vendor's coffin list or a panel flagged them, and reconcile every elite/mid ceiling against that board so no stud is silently omitted (the Hovland/Morikawa/Burns failure class). The board MUST include recent tournament/major champions and proven closers gated on a current-form floor: any that survive the gate at sub-15% projected own are leverage; pedigree without form stays lottery-only (Koepka).

And `framework.md`, Section 9 (Pre-Submission Checklist), add one line to the SE and 3/5-Max checklists:

> - [ ] Ceiling board run vendor-independent? Every top-12-ceiling player has an explicit surfaced read (no silent omissions).

On approval: set status `codified`, `codified_in: "framework.md — Section 2 Slate Diagnostics (Vendor-independent ceiling board) + Section 9 checklists"`.

**3. No demotions.** `trap-vs-value-chalk` (2 prior contradictions) operated correctly in its 7/22-narrowed form this slate; no codified rule logged a new mechanism failure.

**Retirements:** none this slate.

## Applied

Approved proposals applied 2026-07-26. Codification 1: the Single-vendor self-erosion guard appended to `framework.md` Section 6 (Anchor Selection Logic) exactly as proposed; `single-vendor-overweight-self-erosion` set to `codified` with `codified_in: "framework.md — Section 6 Anchor Selection Logic (Single-vendor self-erosion guard)"`. Codification 2: the Vendor-independent ceiling board appended to `framework.md` Section 2 (Slate Diagnostics) and the checklist line added to both the Section 9 SE and 3/5-Max checklists exactly as proposed; `vendor-independent-ceiling-scan` set to `codified` with `codified_in: "framework.md — Section 2 Slate Diagnostics (Vendor-independent ceiling board) + Section 9 checklists"`. Ledger hygiene: no retire or merge actions were proposed (all flagged pairs were KEEP / KEEP-SEPARATE / already-resolved stale flags), so no other lesson was touched. `framework.md` last-updated stamp advanced to 2026-07-26. No demotions, no retirements, no philosophy.md changes.
