# MLB Classic — 6.11.26 slate analysis

## Pre-flight checklist
- [x] Slate confirmed: mlb_classic — 5-game MAIN (ARI@MIA, MIN@DET, STL@NYM, TEX@KC, CHC@COL), first pitch 1:10 PM ET; bundle generated 2026-06-11 11:49; all article files dated 2026-06-11 and The Stone is the 6.11.26 edition — current slate
- [x] Projections loaded: Ship It Nation MLB Projections `mlb-projections-dk-20260611.csv` (99 players, exactly this slate's 10 teams); SIN hitter+pitcher rankings in Slate Data match the same pool
- [x] Venue file read: `rules/mlb_classic/parks/coors_field.md` (CHC@COL is the slate's run environment — third straight CHC@COL slate). Other 4 parks had no files — created UNVERIFIED stubs from this slate's articles: `loandepot_park.md`, `comerica_park.md`, `citi_field.md`, `kauffman_stadium.md`
- [x] Open lessons reviewed: 7 open — applied: pivot-budget-small-field-se (construction band below), salary-enabler-pitcher-chalk (Phillips fade / Scott keep), se-chalk-pitcher-own-condensation (Scott fade sizing), blank-own-snapshot-artifact (cross-checked — no artifact this slate, Feltner's 1.04% is real), untracked-entry-bypasses-loop + late-build-bailout (process notes below; analysis lands ~80 min pre-lock); rejected: weather-proof-dome-stack-pivot as primary pivot (mechanism needs field ownership concentrated on the rain-exposed offense — here the #1 ownership cluster is CHC at sunny Coors; applied only as a tiebreak against KC/TEX)
- [x] Framework pre-lock checks: Anchor-Equivalence run on all 3 flagged tiers (call below); team-stack-driven roster confirmed (5-man primary shapes won all 4 logged contests); no-hitter-vs-own-pitcher noted (Feltner blocks COL bats, Dobbins blocks STL bats — and stacking NYM pairs *with* Scott, it doesn't block him)
- [x] Prior results scanned: results.jsonl last 2 slates — best finishes top 40.1% / 39.9%, both played untracked SaberSim imports while the tracked build held the winning skeleton (6/10). Process target this slate: enter the audited lineup
- Vendor calibration: SIN at 2 slates (proj MAE 5.82, own MAE 3.02) — **<3 slates, note only, not weighted**. Known pattern: ownership miss concentrates on the consensus chalk pitcher (Detmers +30.8).

---

## Slate at a glance

2 SE contests (490 + 1,189 fields), **1 unique lineup** covers both.

| Game (away@home) | Implied | Weather | Lineups |
|---|---|---|---|
| ARI @ MIA, 1:10 | 4.30 / 4.40 | **Dome** | both confirmed |
| MIN @ DET, 1:10 | 4.70 / 5.00 | Sunny 89° | both confirmed |
| STL @ NYM, 1:10 | 4.30 / **4.90** (-140) | Partly sunny 91° | both confirmed |
| TEX @ KC, 2:10 | 5.00 / 5.20 | **KC WATCH: T-storm, 31% rain, 18mph** | TEX still projected |
| CHC @ COL, 3:10 | **6.05** / 5.20 | Coors, sunny 75° | both projected |

The field's money is on Coors (CHC 146% combined own) and Christian Scott (43.9%). The slate's structural gift is the Mets: highest non-Coors home implied total (4.90, biggest favorite on the board) at just **34.7% combined ownership**, facing the worst non-punt arm (Dobbins, 5.33 xERA).

## Pitcher read

| Arm | Sal | Proj | Own% | Avg IP | K% | xERA | Call |
|---|---|---|---|---|---|---|---|
| Christian Scott (NYM) | 8300 | 14.71 | 43.9 | 4.5 | 26.4 | 4.13 | **Right chalk.** Best K profile vs a 20.8%-owned STL. Condensation lesson: 43.9% can close 55–70% (Detmers went 38→69) — a Scott fade is more binary than it looks |
| Zebby Matthews (MIN) | 8500 | 12.27 | 24.2 | 6.0 | 27.7 | 3.56 | **Best SP2 mechanism on the slate** — longest leash + K combo in the 22–25% class |
| Michael Wacha (KC) | 9000 | 11.50 | 17.9 | 6.2 | 21.5 | 5.06 | Longest leash, below-class own — but his game carries the 31% rain risk; a shortened start kills a $9K arm |
| Keider Montero (DET) | 7700 | 11.95 | 23.2 | 5.5 | 16.1 | 5.56 | Fine, low K% — middle of the class |
| Merrill Kelly (ARI) | 7000 | 11.85 | 23.6 | 5.8 | 11.5 | 7.65 | **Worst xERA + K% of the chalk class** — the weakest 23% on the board |
| Edward Cabrera (CHC) | 7500 | 12.05 | 25.2 | 5.2 | 21.8 | 4.64 | Coors tax on the arm; the Stone notes his salary supports the fit, but park risk is real |
| Tyler Phillips (MIA) | 6200 | 11.34 | 21.9 | **2.4** | 22.9 | 3.88 | **The chalk trap.** 2.4 avg IP is the Kai-Wei Teng profile (2.5 IP, busted at 1.8 pts on 27% own). Stone ranks him P #1 and G_RIZEN cores him — the leash mechanism says fade anyway. Salary-enabler lesson does NOT protect him: it protects cheap chalk with a workable leash, and his fails the leash test |
| Kumar Rocker (TEX) | 6800 | 9.57 | 10.1 | 5.1 | 23.8 | 4.61 | The legit leverage P2 — decent leash/K at 10% — but same rain game |
| Hunter Dobbins (STL) | 6500 | 8.95 | 9.2 | 4.3 | 21.1 | 5.33 | Only if NOT stacking NYM; thin |
| Ryan Feltner (COL) | 6000 | 7.76 | 1.0 | 4.6 | 15.3 | 5.69 | **Reject.** Tops the auto-snapshot leverage table but Stone ranks him last (xERA 5.69 at Coors). Leverage score artifact of a tiny denominator, not a play. Also blocks COL bats |

## Stack read

| Team | Implied | Comb. own | Call |
|---|---|---|---|
| CHC | 6.05 | **146%** | Ownership tax, third straight Coors slate — park file: the owned Coors side hasn't paid a primary-stack premium either prior slate. Fine as a 2–3 man mini, not the 5-man |
| NYM | 4.90 | **34.7%** | **The slate's pivot.** Biggest favorite, hot park (91°), worst opposing arm, and every bat but Soto (11.3%) is sub-7% — Young 6.1, Benge 7.0, Ewing 5.2, Semien 4.8, Bichette 5.2, Alvarez 3.4. Pairs naturally WITH Scott (same team) |
| KC | 5.20 | ~75% | Chalk (Witt 22.5, Pasquantino 16.6, Jensen 13.6, Caglianone 12.6) carrying **unpriced 31% rain/PPD risk** — underweight |
| TEX | 5.00 | ~60% | Cheap correlation (Pederson/Seager/Jung/Nimmo/Langford, $3.1–4.6K) but same storm window; lineup unconfirmed at writing |
| DET | 5.00 | ~61% | Clean mid-owned secondary: McGonigle 16.3, Greene 11.6, Carpenter 13.0, Dingler 11.1 in 89° sun |
| MIN | 4.70 | ~41% | Quiet leverage mini: Clemens 11.1 + Bell 3.5 + Larnach 6.3; Buxton 13.3 the ceiling bat |
| COL | 5.20 | ~66% | NOT the free square it was — COL own roughly quadrupled vs 6/9. The repeatable park edge is the cheap one-off: **Cole Carrigg $2,500 (10.6% per Stone) — note he's missing from the SIN projections CSV**, so the snapshot can't see him |
| STL | 4.30 | ~21% | The anti-Scott binary: Burleson (Stone hitter RK 6) 4.5%, Herrera 3.9, Walker 3.3, Wetherholt 5.5. Real leverage but it only wins the world where 50–70%-actual-own Scott busts — that's a second pivot, not a first |
| MIA | 4.40 | ~50% | Dome safety at a weak total; tiebreak vs KC/TEX, not a primary |
| ARI | 4.30 | ~35% | Carroll/Marte fine one-offs; lowest team total side, pass on the stack |

## Where the auto-snapshot and the articles diverge

- **Feltner** — snapshot's #1 leverage vs Stone RK 15 of 16 arms. Articles win: no ceiling, blocks Coors bats. Reject.
- **Phillips** — articles' P #1 (Stone, G_RIZEN GPP1, DK Cash Core) vs the validated leash lesson. The lesson wins: 2.4 avg IP caps DK pitcher scoring structurally. This is the one place I'm overriding the articles on mechanism.
- **STL leverage cluster** (Crooks/Gorman/Church/Winn high on snapshot leverage) — real ownership numbers, but they're the Scott-bust world. Use only as the deliberate anti-Scott binary, not as "free" leverage.
- **Jared Young** — Stone's #1 ranked hitter on the whole slate at $2,600 / 6.1% own (xwOBA +0.056 over wOBA, hot Citi). Snapshot barely notices him. Best value bat on the board and he's inside the pivot stack.
- **KC chalk** — vendor ownership doesn't price the 31% rain. Witt at 22.5% in a possibly-shortened game is worse than his number.
- **G_RIZEN value bats** (Clemens, Bell, Loftin, McKinstry, Semien, Young) — all sub-$3,600 fills the snapshot agrees are cheap; Bell (3.5%) and Semien (4.8%) double as leverage.

## Anchor-Equivalence call

1. **Busch / Happ / Hoerner / Bregman (28.0–30.7%)** — all four are the same CHC stack, so the field treats them as one decision. Alternative anchor = the lower-owned CHC pieces (Suzuki 22.3 / Swanson 17.3 / Ballesteros 15.7) if running Cubs, or the NYM stack fade entirely. With a 1-lineup portfolio: don't roster 3+ of the quartet.
2. **Pitcher class 21.9–25.2% (Cabrera/Matthews/Kelly/Montero/Phillips + Witt/Suzuki)** — per the 6/9 caveat the alternative can come from inside the class: **Matthews is the lower-owned-enough, best-mechanism member** (vs Cabrera's park tax, Kelly's 7.65 xERA, Phillips's leash). Below-class alternative is Rocker 10.1%.
3. **Wacha / Castro / Swanson / Pasquantino / McGonigle / Ballesteros (15.7–17.9%)** — satisfied automatically if the build uses any one of these rather than the obvious tier-1 piece at the slot.

**The call:** the single lineup satisfies the rule by running the alternative on the pitcher tier (Matthews over Cabrera/Kelly/Phillips as SP2) and by not maxing the CHC quartet.

## Construction guidance (1 unique lineup, both SE contests)

Winning band from 4 logged SE contests: **~15–16% avg own, 4–5 sub-10% plays, 5-man primary stack (5-3 / 5-2-1 / 5-1-1-1), ~$49.5K+ spent, ONE structural pivot.** The 1,189-field Chin Music is marginally above the lesson's ~1,000 band — same regime, don't add a second pivot for it.

- **Primary build: Scott + Matthews, NYM-5 primary, CHC or DET mini.** The pivot is the stack, not the pitcher: keep the 44% arm (he's the right chalk and fading him is a 60–70%-actual fade), and take his own team's bats at 3–11% own. NYM-5 (Soto + four of Young/Benge/Ewing/Semien/Alvarez/Bichette) supplies the 4–5 sub-10% plays by itself; a CHC 3-man mini (e.g. PCA/Suzuki + one of the quartet) or DET-3 keeps near-field Coors/secondary exposure. That's chalk-plus-one-pivot exactly.
- **Acceptable alternative:** Stone's "swap to Royals-4 + Twins-3" path — but it eats the rain risk; only if the storm window clears before lock.
- **Avoid:** Phillips at any exposure; CHC-5 as primary (146% tax, two slates of evidence); double-pivot builds (STL bats *and* a Scott fade *and* a stack fade — the 6/9 mistake).
- **Process:** this analysis lands ~80 minutes pre-lock. Build now, red-team it, and **enter the audited lineup** — two straight slates the tracked build beat the SaberSim swap-in.
