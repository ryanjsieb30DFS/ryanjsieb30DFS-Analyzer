# Post-autopsy review — Brickyard 400, Indianapolis Motor Speedway (7/26/26)

Contests: NAS $15K Engine Block (SE, 1,470) — rank 1,387, 94.4th percentile · NAS $5K Engine Block (SE, 490) — rank 125, 25.5th percentile. Leverage capture 0/12. Tiers OUT OF ORDER (Fade 27.2 > Good 25.0). Shark-gap headline: unique_pct +25, but the real axis is chalk-side (see 1b).

## Process scorecard

**Analysis: A−. Execution: D. The strategy predicted the winning shape almost verbatim, and the entered lineups did the opposite of the doc.**

**Pre-flight checks — honored in the doc's substance.**
- **Venue file:** created for this slate and genuinely used — the 21st–30th band (45.8% of optimal), the pole-only dominator read, and the "deep-back is live here, unlike Pocono" warning all shaped the tiers and the definer screen.
- **Open lessons:** applied, and well. `se-actual-own-concentrates-on-consensus` was applied in writing ("treat Preece's 44% and Bell's 38% as floors") and lock ownership proved it (Bell 38→50%, Gilliland 15→45%). `definer-screen-must-reach-entries` was applied as doc text — the screen even named its own history ("your last slate's definer list produced twelve names and zero reached an entered lineup"). `midpack-pd-over-deep-back-chalk` drove the leverage-band framing. The field-tendencies section surfaced every required crowd cluster (Bell 4/4, Hamlin 3/4, the Byron fish-trap tension).
- **Anchor-Equivalence:** surfaced twice as required — the Bell/Elliott/Byron trio (38/36/35%) and the Preece/Cindric deep-back pair. The mechanism then played out: the trio resolved asymmetrically at lock (Bell 50%, Elliott 26%, Byron 32%) and the practice-speed side the doc pointed at (Bell) scored 66.2 while Elliott busted to −6.0.

**Did the synthesized edges hold up against the DK actuals? Mostly yes — unusually well.**
- **The core thesis was the contest result.** The doc's "gap" paragraph said: same top four chalk, completely different sixth slot — "chalk anchors plus one piece almost nobody has." The $15K winner (Krighton, 333.4) was exactly that: Bell + Cindric + Preece (the three chalk anchors, 47–50% owned) + Gibbs + Hocevar + **Corey Heim at 7.5% own, 70.45 — the slate high**.
- **The definer screen produced both contest-winners' leverage.** Heim (named, front-of-grid section) was in the winning lineup of BOTH contests and 65% of the $15K top-20. Keselowski (named, mid-pack section) scored 49.8 at 5.7% and sat in the $5K winner, which carried three sub-10% pieces.
- **The fades held.** Wallace LEAN FADE → 16.4 at 44–45% own (Dustin's "17th for 38 points" fear, but worse). Elliott UNDERWEIGHT → −6.0. Custer FADE → irrelevant. The one reversed call: McDowell FADE was right (low score), while the doc's counter-case for him didn't materialize.
- **The misses.** Larson, tiered Good with a win-in-play note, crashed to −25.2 and was the slate's #1 fish trap (55–58% of fish, 0% of winners) — a crash is variance, not a mechanism miss (GPP guard), but the doc's "cheaper side of the elite-anchor bet" framing put no counterweight on him the way it did on Wallace. Logano, tiered Okay in the text ("random contrarian play") and Fade on the board, anchored the $5K winner with 61.5 at 6.5% own. And the board (not the text) buried Heim in the Fade tier — see the tier calibration below.
- **Tier calibration:** OUT OF ORDER for the second straight slate — Core 35.7 > Good 25.0 > Okay 21.1 but **Fade 27.2**, with leakage Heim (Fade, 70.5) and Logano (Fade, 61.5). Core itself was well-picked (Bell 66.2, Preece 62.2, Cindric 50.5). The failure is specifically the Fade tier swallowing ceiling-tagged sub-10% plays — birthed as a new hypothesis.
- **Grader check:** the retro-grader flagged neither entry; both "clean" lineups finished 94.4 and 25.5. The no-leverage condition is info-only for NASCAR (sharks here run chalk), which this slate shows is a blind spot when the sharks run chalk *plus* a definer — worth watching, not yet a recalibration signal.

**Your entries vs the winners.** The $15K entry (92.4, 94.4th pctile) shared ONE player with the winner (Preece), needed 5 swaps, and carried two fish traps (Larson −25.2, Nemechek −5.8) plus zero sub-10% pieces. The $5K entry (223.0, 25.5th) was the honest chalk build — Bell/Preece/Cindric/Hamlin all hit — and still needed the definer: best single swap was Nemechek → Heim for +76.2. In both contests the distance to the winner was the sixth slot the strategy told you about.

## 1b. Shark gap — the recurring structural axis

The headline delta is unique_pct (+25: you 100%, sharks 75%), but that's 4 shark entries with one duplicated pair — thin. The load-bearing axis is **chalk-side underweight**: own_per_slot −11.4 (you 31.8 vs sharks 43.2) and **anchor_exposure −0.667** (sharks carried Bell, Preece AND Cindric in 100% of their entries; you carried only Preece). Leverage_pct was 0–0: at Indy the sharks ran pure chalk and still put their best entry at the 8.8th percentile.

**This axis is recurring.** Last four slates' top gap: leverage_pct −16.7 (Chicagoland 7/12), own_per_slot −15.7 (Atlanta 7/14), own_per_slot −0.1 (NW 7/21), and now own_per_slot −11.4 with anchor exposure at a third of the sharks'. The mechanism, stated as a mechanism: **I under-own the consensus chalk anchors the pros ride at full exposure, and I spend the freed salary on mid-owned pivots (Larson 37.5%, Chastain 20%, Nemechek 20%) instead of one sub-10% definer.** Mid-owned mush is the fish shape — the fish profile ran 26.6%/slot with 39.5% dart rate; the winners ran 31.1%/slot, 0% darts, one definer. Birthed as `nascar-2026-07-26-anchors-held-differentiate-in-sixth-slot`.

## 1c. Adherence — discipline graded separately from analysis

**Formal adherence: clean.** 0 fade violations, all four contract calls followed (Wallace lean_fade at exactly 50% exposure, Elliott/Reddick/Custer at zero). Results did not need to launder anything — the discipline on fades was real and it helped (Wallace 16.4, Elliott −6.0).

**Leverage adherence: 0 of 12, second straight slate.** No entered lineup carried any of the twelve named leverage candidates; Heim and Keselowski from that list were in the contest winners. The results.jsonl trend is now a four-slate pattern — 0%, 50%, 0/12, 0/12 — which is exactly the mechanism of `definer-screen-must-reach-entries`; this slate is its first formal confirmation (promoted to validated).

**Beyond the contract, both entries violated the strategy's own structural refusals** — a process finding regardless of score:
- The $15K entry carried **Preece + Wallace**, the doc's #1 named refusal ("a sharp will not carry both"). Actual field: 362 lineups (24.7%) shared it.
- The $5K entry carried **Preece + Cindric** (150 lineups, 30.7% — the field's top pair) *and* Bell + Preece *and* Bell + Cindric.
- Both entries failed the doc's own pre-lock check #1 ("Does it carry at least one driver owned under 10%?").

The $5K entry scoring the 25.5th percentile anyway is the GPP guard in action: it does not make carrying the field's most-shared pair in a 490-field SE a good decision.

## 1d. Codified-rule check

| Codified lesson | This slate | Mechanism vs actuals |
|---|---|---|
| `50-pct-chalk-rule` | Triggered at lock (Bell 50.2%) | **Held** — the extreme chalk (Bell 66.2, Preece 62.2, Cindric 50.5) was justified; fading it without definitive evidence would have been (and was, structurally) the losing side. |
| `anchor-equivalence` (+ `not-parity`) | Applied — trio + pair surfaced | **Held** — trio resolved asymmetrically; the doc's practice-speed discrimination (Bell/Byron over Elliott) was directionally right. |
| `midpack-pd-over-deep-back-chalk` | Applied — screen sourced from the 21–30 band | **Held with a caveat** — band anchors paid (Bell P23), Keselowski P16 paid at 5.7%, but the slate-definer came from P7 (Heim). Not a contradiction (the lesson claims where *reliable PD* lives, not where every definer comes from), logged in the venue file. |
| `mme-or-fade-means-fade-in-se` | Triggered — Heim tagged "large-field-only," Logano "random contrarian" | **FAILED — second mechanism contradiction.** Both tagged drivers defined/won the SE contests at 6–8% own, on a track-position flat track (so the NW "chaos short track" scope caveat no longer contains it). 2 contradictions → demotion proposal below. |
| `sleeper-spike-floor` | Not honored in entries | Entries carried zero sub-15%/sub-$6K PD pieces; folds into the definer-screen finding rather than a separate contradiction. |
| `hms-intermediate-double-up` | Not triggered (Indy is not an intermediate) | HMS went 25.1 / −25.2 / −6.0 here — consistent with the lesson's intermediate-only scope and DDD's "equipment matters less at Indy." |
| `backup-car-not-auto-fade`, `bet-sizing`, format/iteration lessons | Not triggered | No injury narrative, no multi-build portfolio this slate. |
| `sim-roi-not-a-selector`, `chalky-combos-scrub` | Cannot fire as written | Both reference SaberSim-era artifacts ("Sim ROI rank," "Exposure-tab lift," "Chalky-Combos-to-Avoid list"). The chalky-combos mechanism now fires through the Analyzer's own Duplication watch (kept, see hygiene); the Sim-ROI mechanism has no surface left (retire proposal below). |

## Lesson ledger changes

Applied directly to `rules/nascar/lessons.yaml` this run:

1. **`nascar-2026-07-21-definer-screen-must-reach-entries`** — first confirmation added (0/12 again; screen named both winners' leverage) → **promoted hypothesis → validated**.
2. **`nascar-2026-07-21-se-actual-own-concentrates-on-consensus`** — first confirmation added (Bell 38→50, Gilliland 15→45–47, co-anchors Elliott/Byron/Hamlin deflated) → **promoted hypothesis → validated**.
3. **`nascar-2026-05-01-portfolio-gaps-addressed-pre-lock`** — second confirmation added (gap diagnosed in the doc's own text and pre-lock check, again unaddressed) → now **3 confirming slates → codification proposal below**.
4. **`nascar-2026-05-17-mme-or-fade-means-fade-in-se`** — **second mechanism contradiction** added (Heim/Logano) → demotion proposal below.
5. **Born:** `nascar-2026-07-26-anchors-held-differentiate-in-sixth-slot` (hypothesis) — the recurring chalk-side shark-gap axis from 1b.
6. **Born:** `nascar-2026-07-26-fade-tier-buries-ceiling-tagged-definers` (hypothesis) — two-slate tier-calibration pattern (NW + Indy) of the board's Fade tier swallowing the ceiling-tagged sub-10% plays that decide SE contests.

## Venue file changes

`rules/nascar/tracks/indianapolis_motor_speedway.md`:
- Header updated from **UNVERIFIED** to **verified in part** by this autopsy.
- Appended a date-stamped post-race observation: third straight running won by heavy chalk + one cheap unknown; deep-back chalk (Preece P34 / Cindric P35) justified again; 21–30 band held for anchors but the definer came from P7 (Heim — front-of-grid is not auto-dead); pole dominator real but capped (Hocevar 40.6); fish traps Larson/Elliott/Nemechek; Gilliland's 15→47% lock jam as the field's dupe glue.

## Ledger hygiene

**Stale hypotheses (3):**
- `nascar-2026-05-01-ownership-shift-full-reevaluation` — **RETIRE via merge** into `nascar-2026-07-21-se-actual-own-concentrates-on-consensus` (now validated). Same underlying mechanism — ownership numbers move against the plan and the plan must re-price — but the newer lesson has evidence, a measurable trigger (projected vs lock), and an app surface (`drift.py`); the 86-day-old version never accumulated a confirmation of its own. Merge text in Proposed codifications. retired_reason: "merged into nascar-2026-07-21-se-actual-own-concentrates-on-consensus."
- `nascar-2026-06-28-roadcourse-deepback-revives-on-strategy` — **KEEP.** Scoped to road courses; no road-course slate has run since Sonoma. Untested for lack of a relevant slate is KEEP, not retire (GPP guard).
- `nascar-2026-07-12-narrative-suppressed-elite-is-leverage` — **KEEP.** Its trigger (articles + field converge on an org-hierarchy narrative demoting an elite with a codified track-type edge) has not set up since Chicagoland. Hamlin's practice walk-back this slate was single-driver form, not an org narrative, and his ownership was not suppressed — no test occurred.

**Near promotion (1):**
- `nascar-2026-05-01-portfolio-gaps-addressed-pre-lock` — the third confirming slate **happened this slate** (gap diagnosed in writing, 0/12 again, Heim/Keselowski in the winners). Promotion proposal below. The exact mechanism a third slate needed to confirm — a pre-lock-diagnosed gap left unaddressed that then cost captured equity — is precisely what occurred.

**Merge candidates (16 pairs):** one MERGE, one already-satisfied, fourteen KEEP-SEPARATE.
- `ownership-shift-full-reevaluation` ↔ `se-actual-own-concentrates-on-consensus` — **MERGE** (survivor: `se-actual-own-concentrates-on-consensus`; see above and Proposed codifications).
- `backup-car-not-auto-fade` ↔ `injury-narrative-not-a-fade-thesis` — **already merged** 2026-07-21 (the latter is retired); flag is satisfied, no action.
- All fourteen remaining pairs — **KEEP-SEPARATE.** Each is a genuine `[[id]]` cross-link between complementary scopes, not duplication: coverage vs sizing (`anchor-equivalence` ↔ `not-parity`), general principle vs operational gate (`portfolio-gaps` ↔ `definer-screen`), base rule vs track-type scoping (`anchor-equivalence` ↔ `superspeedway-doms`), band mechanics vs revival caveat (`midpack-pd` ↔ `roadcourse-deepback`), and the documented tension pair (`mme-or-fade` ↔ `definer-screen`), which the demotion proposal below resolves rather than a merge.

**Removed-feature check:**
- `nascar-2026-05-24-sim-roi-not-a-selector` — **retire candidate** (proposal below). Its mechanism is a warning about SaberSim's pre-slate Sim-ROI ranker and prescribes the Exposure-tab lift score — all removed with the 7/24/26 SaberSim retirement; nothing remains that could fire it.
- `nascar-2026-05-24-chalky-combos-scrub` — **KEEP.** Written against the SaberSim combos list, but the mechanism (don't repeat a flagged crowded pair across entries) now fires through the Analyzer's own `## Chalk combos` / Duplication-watch section — and this slate violated it, so it is very much alive.

## Proposed codifications

*Proposals only — nothing below has been applied to framework.md or philosophy.md. Approve via the app.*

**1. CODIFY `nascar-2026-05-01-portfolio-gaps-addressed-pre-lock`** (3 confirming slates: Texas origin, North Wilkesboro 7/21, Indy 7/26).

- `framework.md` → **Quick-Reference Decision Heuristics**, add:
  > **A diagnosed gap must reach a roster before lock (3-slate rule).** An identified portfolio gap is already-diagnosed edge the field may not have priced; a diagnosis that lives only in the strategy doc transfers zero equity (Texas: Suarez flagged, unfixed, 35.35; NW: 12 definers named, 0 entered, three defined the slate; Indy: 12 named, 0 entered, Heim 70.45 in both contest winners). Before lock, every gap the doc names gets addressed in at least one entry — the operational gate is the SE definer-slot check ([[nascar-2026-07-21-definer-screen-must-reach-entries]]): each SE bullet carries one piece from the sub-10% definer list, verified in the Grade tab.
- `philosophy.md` → **On Process Discipline**, add:
  > Diagnosis is not execution. Three slates proved the strategy layer reliably *finds* the slate-defining gap and the entry layer reliably drops it. The doc and the entered roster are separate artifacts; only the roster is a bet. If the doc names a gap and no lineup addresses it, we chose to forfeit a known edge — write that sentence at lock, or fix the lineup.
- `lessons.yaml`: set status → codified; codified_in → "framework.md — Quick-Reference Decision Heuristics (diagnosed gap must reach a roster); philosophy.md — On Process Discipline (Diagnosis is not execution)".

**2. DEMOTE (narrow) `nascar-2026-05-17-mme-or-fade-means-fade-in-se`** — 2 mechanism contradictions (NW 7/21: Suarez/Hocevar/SVG; Indy 7/26: Heim/Logano, on a non-chaos track type, so the scope caveat is exhausted).

- `framework.md` → Step 6 check #6 and the Quick-Reference line, replace "'MME or fade' means fade in single entry, full stop" with:
  > **"MME or fade" (and cousins: "large-field-only," "random contrarian") marks a low-floor/live-ceiling EV shape — not SE-unplayable.** In a top-heavy SE payout, ONE such driver from a paying start band is a legitimate candidate for the entry's single sub-10% definer slot (NW: Suarez/Hocevar in the $15K winner; Indy: Heim in both winners, Logano in the $5K winner). Carrying two or more of them in one SE bullet remains an MME-only shape, and in flat/cash-adjacent payouts the original fade holds.
- `philosophy.md` → **On Reading the Source Material**: append the same narrowing to the Dover paragraph, citing both contradiction slates.
- `lessons.yaml`: keep id, rewrite the statement to the narrowed scope, note the demotion date; status stays codified with the narrowed text (alternative if you prefer clean history: retire with retired_reason "narrowed after 2 SE mechanism contradictions" and birth the replacement — my recommendation is the in-place narrow, since the tag-reading half is still true).

**3. MERGE `nascar-2026-05-01-ownership-shift-full-reevaluation` → `nascar-2026-07-21-se-actual-own-concentrates-on-consensus`.**

- Surviving statement gains one sentence at the end:
  > A major vendor-ownership shift BEFORE lock (e.g. Blaney 54→39 at Texas) is the same mechanism upstream — it re-prices every fade and overweight justified against the old number and triggers a full re-evaluation of the chalk structure (the drift panel is the surface), never confirmation of the existing plan.
- `lessons.yaml`: retire the old id with retired_reason "merged into nascar-2026-07-21-se-actual-own-concentrates-on-consensus".

**4. RETIRE `nascar-2026-05-24-sim-roi-not-a-selector`** — mechanism references the removed SaberSim pipeline (pre-slate Sim ROI rank, Exposure-tab lift score) and can no longer fire.

- `framework.md`: remove Step 6 mandatory check #11.
- `philosophy.md`: remove the "Sim ROI is informational, not a selection ranker" line from On Process Discipline.
- `lessons.yaml`: status → retired; retired_reason: "references the removed SaberSim Sim-ROI/Exposure pipeline (retired 2026-07-24); mechanism can no longer fire"; codified_in updated to note the removals, mirroring the post-roi retirement format.

## Applied

Applied 2026-07-26 (user-approved). **1. CODIFIED `portfolio-gaps-addressed-pre-lock`** — added the "diagnosed gap must reach a roster before lock (3-slate rule)" heuristic to framework.md Quick-Reference Decision Heuristics and the "Diagnosis is not execution" paragraph to philosophy.md On Process Discipline; lessons.yaml status → codified with codified_in naming both sections. **2. NARROWED (in-place) `mme-or-fade-means-fade-in-se`** — framework.md Step 6 check #6 and the Quick-Reference line replaced with the low-floor/live-ceiling narrowing (one such driver is a legitimate SE definer-slot candidate; two-plus stays MME-only); philosophy.md On Reading the Source Material Dover paragraph appended with the same narrowing citing NW 7/21 + Indy 7/26; lessons.yaml statement rewritten to the narrowed scope with the 2026-07-26 demotion date, status stays codified. **3. MERGED `ownership-shift-full-reevaluation` → `se-actual-own-concentrates-on-consensus`** — survivor's statement gained the pre-lock vendor-ownership-shift sentence (drift panel as the surface); old id retired with retired_reason "merged into nascar-2026-07-21-se-actual-own-concentrates-on-consensus". **4. RETIRED `sim-roi-not-a-selector`** — framework.md Step 6 check #11 removed (gate line now reads "checks 8-10"); philosophy.md Sim-ROI paragraph removed; lessons.yaml status → retired with the SaberSim-pipeline retired_reason and codified_in noting the removals. Ledger-hygiene KEEP / KEEP-SEPARATE lessons untouched.
