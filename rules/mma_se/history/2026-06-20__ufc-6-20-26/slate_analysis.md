# MMA Slate Analysis — UFC Fight Night 6/20/2026 (Classic)

## Pre-flight checklist
- [x] Slate confirmed: bundle generated 2026-06-20 15:53; all three article PDFs dated 6.20.26; UFC Fight Night, 12 fights / 24 fighters. **This is a CLASSIC 6-fighter / $50K slate** (24-fighter pool, no captain) — NOT a showdown like the last archived slate (6/14 Freedom). Data is for THIS slate.
- [x] Projections loaded: SIN **The Stone** (primary, full card w/ odds + ITD% + Core/O/U/F tags) + **DailyFan MMA** (Brett/Gordo tiered ranks). 24 fighters; session data is this slate.
- [x] Venue file: **N/A — MMA has no venue files** (per CLAUDE.md); nothing to read or stub.
- [x] Open lessons reviewed (lessons.yaml): `confirmed-vs-speculative-news` → **N/A**, no injury/weigh-in news (all weights made per The Stone). The five `2026-06-14` hypotheses are **showdown/captain-specific → rejected as not-applicable here**, but their generalizable mechanisms are applied: `cap-single-favorite-exposure` → cap Horiguchi/Mesquita across the 10; `cheap-slot-prefer-floor-or-live-dog` → SE cheap slot uses a value-favorite floor, not a pure punt; `flex-spine-diversity` → classic analog = all-unique cores. Codified rules applied throughout (field-size calibration, one-leverage-swing, ceiling threshold, binary-leverage-weak-in-small-fields, ceiling-gate-reserve-field-fade, asymmetric anchor-equiv weighting, SE-bullet = differentiated build).
- [x] Framework pre-lock checks: **Anchor-Equivalence** → three substitutable $9K debut-finishers (Chokheli 39 / Magomedov 37 / Stirling 35) must be ROTATED as the premium anchor, not defaulted to Chokheli; plus Mesquita 33 / Lima 29 and the Horiguchi/Kape main-event sides (see Decision 2). Ceiling threshold ≥~600 win-case enforced; binary KO-punts steered to the mini-MAX only; ≥1 field-fade lineup reserved.
- [x] Prior results scanned (results.jsonl): 1 slate (6/14 Freedom showdown, best 0.2%, ROI n/a). Sample far too small to read as ROI — process note only.
- [x] Sharp envelope: **no sub-5%-owned play exists on this slate** (leverage floor is ~13–21%); target = ≥1 sub-20% (ideally sub-15%) leverage piece in MOST builds. MMA own/slot ~28–30% is format-appropriate (don't force 12–16%). All-unique; cap any single favorite ≤~60% of the 10 lineups; judge on ceiling.

## Slate at a glance
| Fact | Detail |
|---|---|
| Card | UFC Fight Night, 12 fights, classic 6-fighter DK ($50K) |
| Format | Stacked top — 6 favorites $8.9K–$9.7K all with finish equity; "play whoever you want, all have merit" (DailyFan) |
| Main event | Kape (-155, $8.6K) vs **Horiguchi (+135, $7.6K)** — flyweight; the dog is the chalk (47% own) |
| Pick'em fights | Rosa (-108) / Santos (-112); Nascimento (-162) / Raposo (+142) |
| Top studs | Mesquita ($9.6K, -600, win-ITD lock) · Lima ($9.7K, -650) · Chokheli/Magomedov/Stirling (debut finishers) |
| Leverage floor | **Zero sub-5% plays.** Lowest owned: Mullins 10 · Borjas 11 · Bolanos 13 · Cutelaba/Fili 17 · Baghdasaryan 18 · Shahbazyan/Rosa/Raposo 20 |
| Contests | **$8K Flying Knee** SE (field **784**) · **$5K Clinch** SE (field **1,189**) · **$20K mini-MAX** 150-Max (field **47,562**, 10 of 150 entries) → **10 unique lineups**, two of them serve as the SE bullets |
| Scoring reminder | R1 finish = +90 bonus; ceiling lives in early-finisher favorites; floor lives in grappling/value favorites in decisions |

## The 4 decisions that define this slate

### 1. The main event: Horiguchi ($7,600 · 47% own · +135) — PLAY, but it's the chalkiest play on the slate
**PLAY (as a value-favorite-priced live dog), cap exposure.** Horiguchi is a +135 dog who **already beat Kape**, at $7.6K with a grappling floor (1.61 TD, 3.77 SLpM) — the rare chalk you can roster because the underdog has real win equity AND a decision floor, not KO-or-bust. The Stone cores him; both DailyFan analysts rank him #1 in his tier. SIN projects him 67.54 vs DailyFan's 55.97 (+18.7%) — I lean the higher SIN number on the grappling-floor mechanism.
- **If played →** $42,400 left for 5 spots ($8,480/spot) — he's a salary saver that funds a $9K+ stud. He pairs cleanly with the debut finishers (different fights). His 47% own means he is **not** your differentiator — he's the floor; your edge must come from the other five slots.
- **If faded →** you need the world where the 89%-combined-owned main event (Horiguchi 47 + Kape 42) busts or extends to a flat decision. That world exists (flyweights, +135 dog) and is **the single best leverage angle on the slate** — reserve ≥1 mini-MAX lineup that rosters NEITHER (see Edge 3).
- **Exposure rule:** per `cap-single-favorite-exposure`, hold Horiguchi to ≤~6 of 10 lineups. **Never roster Kape with him** (opponent stack).

### 2. Anchor-Equivalence: the three $9K debut finishers — ROTATE, don't default to Chokheli
**MANDATORY pre-lock call.** Chokheli (39% · $9.1K · best PT/$ 9.52), Magomedov (37% · $9.0K), and Stirling (35% · $9.2K) are three substitutable chalk anchors within ~4% ownership — all -325 to -375 favorites projected as R1-finish ceiling engines, all in different fights (rosterable together or apart). The field treats them as interchangeable, so defaulting every build to Chokheli concentrates portfolio risk on one debut whose tape we don't have.
- **If played →** each is a ~$9K anchor; pairing two of the three pushes you into Horiguchi/value territory for the cheap slots. Chokheli + Magomedov is the highest-ceiling double-finisher core; both are debuts, so that's also the highest-variance core.
- **Rotation rule:** across the 10, anchor roughly equal thirds on Chokheli / Magomedov / Stirling as the premium piece. **Stirling is the weakest of the three** — debut with the "toughest matchup," shown willing to go the distance (boom/bust) — so weight him slightly *under* the projection-implied ordering (Decision in Player board).
- **If you collapse to one →** make it Magomedov or Chokheli (both profile as early finishers historically per DailyFan); Stirling-only builds carry the distance risk without the finish edge.

### 3. Rodriguez ($8,400 · 21% own · -200) — PLAY / overweight: the best leverage on a slate with no sub-5% plays
**PLAY, lean overweight.** A -200 winning favorite at only 21% own with wrestling/grappling ceiling (3.85 SLpM, 1.75 TD) against high-pace Amil — The Stone's explicit "target and potentially come in overweight." On a slate where the leverage floor is ~13–21%, a *winning favorite* at sub-tier ownership is worth more than a KO-punt dog: you get win equity AND differentiation in the same slot.
- **If played →** $8.4K mid-anchor leaves room for one $9K finisher + Horiguchi value; it's the connective tissue that lets a lineup carry two studs. He is the **non-binary leverage swing** the SE framework wants (blended EV well above the ~50 floor) — correct for the small SE fields where pure KO-punts are structurally weak.
- **If faded →** you're betting Amil's high pace produces the upset-with-volume (his fights "crush on DK win or lose"); fine as a one-off mini-MAX dart, but fading a 21%-owned winning favorite is conceding free leverage.

### 4. The cheap slot: KO-punt vs value-favorite floor — split by contest
**MIX, and the split is by field size.** The punts — Bolanos ($6.8K, 13%, striking spot vs Aswell who "gets hit a ton"), Mullins ($6.6K, 10%), Borjas ($6.5K, 11%) — are pure KO-or-bust dogs.
- **If played → mini-MAX only.** In the 47,562-field a sub-15% punt that lands a finish is tournament-winning leverage and frees a second stud; carry one in 1–2 of the 10 (Bolanos is the best of them — live striking path). Per `ceiling-gate-underrates-low-own-finishers`, reserve ≥1 field-fade build around this tier.
- **If faded (the SE bullets) →** per `binary-leverage-weak-in-small-fields`, the 784- and 1,189-field SEs should fill the cheap slot with a **value-favorite floor** — Horiguchi, Santos, Rosa, or Raposo — not a binary punt. A 25%-chance-of-115 / 75%-chance-of-0 punt blends to ~29 EV and is a structural leak in small fields.

## Player board
Ownership = projected classic own%. "If played →" is the roster-shaping consequence. Covers the full chalk tier + every named leverage piece + traps + vendor disagreements. (Left off: deep-punt Borjas — see PASS note — and the redundant favorite-side reads already implied by their opponents.)

| Fighter | Sal | Proj | Own% | Odds / ITD | Finish lean | Call | If played → |
|---|---|---|---|---|---|---|---|
| **Mesquita** | $9.6K | 88.83 | 33 | -600 / -260 | High (100–115 in most wins) | **PLAY** | Safest ceiling on the card; pairs with ONE other $9K max — eats salary, forces value cheap slots. Anchor-equiv pivot: Lima. |
| **Chokheli** | $9.1K | 86.60 | 39 | -375 / -500 | R1 finish | **PLAY** | Premium debut anchor (best PT/$). Rotate vs Magomedov/Stirling — don't put in all 10. |
| **Magomedov** | $9.0K | 82.69 | 37 | -350 / -210 | R1 finish | **PLAY** | Co-best debut finisher; the Chokheli pair is the top-ceiling (and top-variance) core. |
| **Stirling** | $9.2K | 80.96 | 35 | -325 / -210 | Boom/bust (will go distance) | **MIX** | Third of the debut trio — weight UNDER his projection; use when you want size without doubling the finish bet. |
| **Aswell** | $9.4K | 81.37 | 27 | -400 / +100 | Volume (7.79 SLpM), moderate ceiling | **MIX** | High-action pivot off the debuts; ceiling needs the finish. Good in builds that fade a debut. |
| **Lima** | $9.7K | 84.20 | 29 | -650 / -135 | Domination/grind | **MIX** | The lower-owned Mesquita pivot (anchor-equiv) — most expensive, less smash, but domination floor. ≥1 lineup Lima-not-Mesquita. |
| **Rodriguez** | $8.4K | 73.60 | 21 | -200 / +110 | Wrestling | **PLAY** | Best leverage anchor (Decision 3). Mid-salary glue; overweight. Never with Amil. |
| **Oliveira** | $8.9K | 78.46 | 25 | -285 / -135 | Finish-capable | **MIX** | Clean mid-range finisher; fine in finisher-stacked builds, but 25% own is secondary not leverage. |
| **Collins** | $8.5K | 75.02 | 25 | -230 / -110 | Finish-dependent (7-0, thin data) | **MIX** | Boom/bust favorite; ceiling fine, win-security questionable. Pair with floor pieces, not other binaries. |
| **Horiguchi** | $7.6K | 67.54 | 47 | +135 / dog | Decision floor (grappling) | **PLAY** | The value-favorite floor / cheap-slot fix for SE (Decision 1, 4). Cap ≤~6/10. Never with Kape. |
| **Santos** | $7.9K | 61.63 | 26 | -112 / pick'em | 80–90 in a win | **MIX/PASS** | The chalkier pick'em side; **fade-leaning** — "best opponent she's faced," The Stone underweight. If played, it's a floor-favorite slot, not ceiling. |
| **Rosa** | $8.3K | 61.75 | 20 | -108 / pick'em | "Crushes in wins historically" | **PLAY (leverage)** | The lower-owned side of a true pick'em (Edge 2). Use as the sub-tier leverage favorite. Never with Santos. |
| **Shahbazyan** | $7.1K | 35.78 | 20 | +310 | Low-own upside / leverage | **MIX (mini-MAX)** | Field-fade leverage dog; "significant leverage, better sim target." Cheap-slot ceiling swing in big-field builds. |
| **Baghdasaryan** | $7.2K | 42.24 | 18 | +285 | Upside dog | **MIX (mini-MAX)** | SIN 42.24 vs DailyFan 31.94 — the higher read makes him a live cheap dog; mini-MAX leverage only. |
| **Raposo** | $7.4K | 48.02 | 20 | +142 | Win-equity dog, capped ceiling | **MIX** | Best win-equity dog (+142); a floor-ish pick'em-side value for SE cheap slots over the pure punts. |
| **Fili** | $7.3K | 42.03 | 17 | +245 | Veteran, competitive dog | **MIX (mini-MAX)** | Viable secondary leverage dog; volume path, not a finisher. |
| **Bolanos** | $6.8K | 37.37 | 13 | +330 | Live striking KO path | **MIX (mini-MAX punt)** | Best of the punts — striking fight vs a hittable Aswell. 1–2 mini-MAX bullets only. |
| **Cutelaba** | $7.0K | 44.67 | 17 | +250 | KO-or-bust, tough matchup | **PASS** | Rising-own trap — "known commodity, like him least." If played anyway: mini-MAX dart only, never an SE slot. |
| **Kape** | $8.6K | 78.26 | 42 | -155 | Ceiling-capped in extended fight | **PASS** | Both vendors cool on his ceiling; overpriced favorite. If played anyway: it's a main-event-side bet vs Horiguchi — never both. |
| **Mullins / Borjas** | $6.6K/$6.5K | 32/34 | 10/11 | +450/+475 | Pure punt | **PASS** | Narrative/chaos only. Mini-MAX max-leverage darts at most; never an SE slot. |
| **Nascimento / Tanzilovi** | $8.8K/$7.7K | 68/46 | 22/21 | -162/+195 | Low-volume / capped-win | **PASS** | The Stone underweight / "struggle to see crushing in a win." Salary-inefficient; better mid-tier options exist. |

## Where I disagree with the vendors
_Calibration note: only DailyFan MMA has a logged calibration row (1 slate, match_rate 0, MAE n/a) — **<3 slates, a note not a weight**. SIN The Stone has no logged history. So these are mechanism-based, not calibration-weighted._
- **Santos (26% own).** SIN/DailyFan price her the pick'em favorite (-112) and she'll draw 26%; The Stone is underweight and **I go further — fade-lean.** Mechanism: "best opponent Santos has faced by far," likely a flat striking decision without a ceiling. I'd rather own **Rosa (20%)**, the lower-owned side who "crushes in wins historically." This is a real ownership-leverage disagreement with the field.
- **Stirling (proj 80.96, ranks as a top anchor).** I disagree with the raw projection ordering: he's a debut with the "toughest matchup" who has gone the distance — a boom/bust profile that the point projection over-rates relative to Chokheli/Magomedov. Weight him **third** of the debut trio, not co-equal.
- **Cutelaba (17%, projected to rise).** The Stone expects ownership to pile in and likes him "the least" in a tough matchup; **I PASS** — a KO-or-bust dog whose ownership is rising is the worst kind of trap (you take the variance AND the duplication).
- **Kape (42%, $8.6K).** The field has him as the second-most-owned play; **I PASS.** Both vendors flag a capped ceiling in an extended fight, and $8.6K for a ceiling-limited -155 favorite is a poor use of salary when Horiguchi (the live side) is $1K cheaper. The disagreement is with the *field's exposure*, not the projection.
- **Where I agree with the field:** Horiguchi as a live, floor-y dog is correct (I just won't over-own him), and the top-stud reads (Mesquita/Chokheli/Magomedov) are right — this is a genuinely deep, "play-who-you-want" top tier, so the edge is in selection + rotation, not in contrarian stud fades.

## Edges to exploit
1. **Rodriguez as the leverage anchor (21% winning favorite).** Expression: build mid-salary cores on Rodriguez ($8.4K) + one $9K debut finisher (Chokheli/Magomedov) + Horiguchi ($7.6K) value, leaving ~$24.1K for three mid pieces. Gets you win equity AND sub-tier ownership in one slot. Never with Amil.
2. **Rosa over Santos in the pick'em (20% vs 26%).** Expression: when a build needs the value-favorite floor slot, take Rosa ($8.3K) as the lower-owned side of a coin-flip whose win-case "crushes." Never roster both (same fight). Pure free leverage vs the field's Santos lean.
3. **The main-event fade lineup (the slate's #1 leverage).** Expression: ≥1 mini-MAX bullet that rosters **neither Horiguchi nor Kape** — e.g. Mesquita + Chokheli + Magomedov + Rodriguez + Rosa + Bolanos. With 89% of the field's exposure tied up in that one fight, this build wins outright if the main event busts or goes to a flat decision.
4. **Debut-finisher rotation = anchor-equivalence in action.** Expression: across the 10, anchor ~3 builds each on Chokheli / Magomedov / Stirling (Stirling slightly fewer). This captures uncontested leverage if the less-popular debut is the one who lands the R1 finish — the recurring structural-leak fix.
5. **KO-punt only where the field rewards it.** Expression: 1–2 mini-MAX bullets carry **Bolanos** ($6.8K, 13%, live striking path) to free a second $9K stud; keep all punts OUT of the two SE bullets, which instead use a value-favorite floor (Horiguchi/Rosa/Raposo). Right variance in the right field size.

---
**Build targets recap:** SE bullets ($8K Flying Knee 784 / $5K Clinch 1,189) = highest-conviction *differentiated* builds, ≥~600 win-case ceiling, ONE non-binary swing (Rodriguez/Rosa), no pure punts, and the two SEs must differ on ≥1 conviction anchor (don't twin the core). The 10 mini-MAX lineups = all-unique, Horiguchi ≤~6/10, ≥1 main-event-fade build, ≥1 punt-leverage build, debut anchors rotated, ≥1 sub-20% leverage piece in most.
