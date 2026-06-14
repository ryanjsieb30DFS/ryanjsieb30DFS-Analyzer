# MLB Classic — Slate Analysis (6.13.26)

## Pre-flight checklist
- [x] Slate confirmed: mlb — 8-game DK MAIN slate, all 4:05/4:10 ET (MIA@PIT, SD@BAL, SEA@WSH, ARI@CIN, ATL@NYM, DET@CLE, TEX@BOS, LAD@CWS). Bundle generated 2026-06-13 14:56; Stone + screenshot dated 6.13.26 match. The Stone PDF also lists 7:10/10:05 games — those are OFF this main slate (no teams in the projection pool); ignored.
- [x] Projections loaded: SIN MLB Projections (160 players, this slate) + SaberSim cross-check. Pool ownership/salaries match the Stone's matchups.
- [x] Venue files read: citi_field.md (ATL@NYM, not a primary). Created UNVERIFIED stubs for the three stack-relevant parks lacking files — great_american_ball_park (ARI), camden_yards (SD/BAL), rate_field (LAD, the one weather game: 87°/15mph SW, "GOOD HITTING"). Stone: all other spots neutral weather.
- [x] Open lessons reviewed: 7 open/active —
  - APPLIED se-chalk-pitcher-own-condensation + condensation-target-projected-leader: Yamamoto is the projected-own #1 arm (35.3%) → expect ~55–60% close (+30 pattern: Detmers/Scott/Misiorowski). Hold him, pivot in bats (Decision 1).
  - APPLIED chalk-ace-smash-compresses-pitcher-leverage: Yamamoto vs the slate's worst offense (CWS 3.25) is a condense-AND-smash spot → lean the bat side more spread/contrarian (Decisions 1, 3, Edges).
  - APPLIED pivot-budget-small-field-se: one leverage axis (LAD stack), ~15–18% avg own, 3–5 sub-10 plays (Decisions 3–4).
  - APPLIED salary-enabler-pitcher-chalk: Chandler/Castillo are enablers that unlock the premium stack, not chalk traps — keep (Decision 2).
  - APPLIED five-man-primary-conditional-on-blowup: 5-man only on a real blowup candidate (ARI/LAD vs weak arms); default 4-man + secondary given the smash-compresses-spread read.
  - APPLIED sin-projection-pool-omissions: cross-checked Stone vs pool — no priced Stone player missing from the 160-row SIN file this slate (the omission risk did not recur).
  - REJECTED weather-proof-dome-stack-pivot: mechanism precondition absent — no rain concentrating field own on outdoor bats; the flagged park (Rate) is the OPEN-air hitting game, not a dome refuge.
  - N/A blank-own-snapshot-artifact: leverage table's 0.0% rows (Jimenez, Norby, Brujan) are real low-own bats per the Stone, not blank-Own artifacts — verified.
- [x] Framework pre-lock checks: Anchor-Equivalence → SP trio Suarez/Skubal/deGrom (25.5–29.3%) is the equivalent set; deGrom is the alternative anchor (Decision 4). Anchor-Equivalence is Decision 4 below. No-hitter-vs-own-pitcher enforced in all shaping notes.
- [x] Prior results scanned: results.jsonl last 3 slates (best pct 4.4 / 40.1 / 34.6); SIN calibration now 4 slates (proj MAE 5.88, own MAE 3.28 — past the 3-slate guard, weightable). GPP ROI noise — process notes only.

## Slate at a glance
| Game (park) | Implied (away/home) | Pitching | Read |
|---|---|---|---|
| LAD @ CWS (Rate) | 5.10 / 3.25 | Yamamoto vs Burke | LAD elite spot, 87°/wind out; CWS the slate's worst O (Yamamoto smash) |
| ARI @ CIN (GABP) | 5.25 / 4.50 | Soroka vs Lowder | ARI slate-high total in a bandbox vs a 5.11-xERA arm |
| SD @ BAL (Camden) | 4.95 / 5.25 | Vasquez vs T.Gibson | Two weak arms → BOTH offenses live; co-leader total |
| MIA @ PIT (PNC) | 4.40 / 4.80 | C.Gibson vs Chandler | Cade Gibson (1.3 IP) is soft — MIA bats live, but cheap pool |
| SEA @ WSH (Nats) | 4.50 / 4.70 | Castillo vs Cavalli | Mid totals, two midrange arms |
| ATL @ NYM (Citi) | 4.25 / 4.45 | Perez vs Manaea | Neutral; NYM thin lineup |
| DET @ CLE (Progressive) | 4.15 / 3.55 | Skubal vs Cantillo | Skubal's smash spot; CLE punt-priced bats |
| TEX @ BOS (Fenway) | 3.75 / 3.95 | deGrom vs Suarez | Lowest-total game — a PITCHER game, fade both lineups |

Contests (both SE, **1 unique lineup needed**): MLB $6K Rally Cap (882) · MLB $6K Chin Music (1,426). Small-field SE → pivot-budget band applies.

## The 4 decisions that define this slate

### 1. Yoshinobu Yamamoto ($10,800 · 35.3% proj → expect ~55–60% per condensation, 3-for-3) — PLAY
He's the projected-own #1 arm vs the slate's worst offense (CWS, 3.25 implied) — the textbook condense-AND-smash spot. Mechanism: the casual SE field converges on the crowned #1 arm (+30 pts over projection every slate: Detmers, Scott, Misiorowski), so his real ownership is ~55–60%, not 35%.
- **If played →** $39,200 for the other 9. He's the floor anchor; take ALL your leverage in the bats (chalk-ace-smash says the pitcher slot stops differentiating, EV migrates to who pairs the best cheap bats). Pair him with a cheap SP2 (Decision 2), NOT a second $10K ace, so you can afford a real stack.
- **If faded →** you're betting CWS (worst O on the board) touches him AND your alt arm out-scores him — a ~55–60% fade against the best pitching spot on the slate. Don't; this is more binary than the 35% tag implies.

### 2. The SP2 slot — salary-enabler vs second ace — MIX (default: cheap enabler)
The leverage axis lives here OR in the stack, never both (pivot-budget). With Yamamoto locked, a second ace ($10K) caps your bats at ~$3,600/hitter and double-anchors a slot the field already crowds (Suarez 29%, Skubal 28%, deGrom 25.5%).
- **If you go cheap (recommended) →** Bubba Chandler ($6,200, 12%, PIT vs soft MIA) or Luis Castillo ($7,200, 8.7%, SEA) is the enabler that unlocks an LAD or ARI premium stack — keep it, fading it cuts you off the winning salary shape (enabler lesson 3-for-3). This keeps pitchers near-chalk and makes the STACK your one pivot.
- **If you double-ace →** make the second arm deGrom (see Decision 4), and your bats must be cheap/spread to fit — your leverage then has to come from punt bats, a thinner edge.

### 3. Primary stack: LAD (leverage) vs ARI/SD (chalk) — PLAY LAD as the pivot
- **LAD — PLAY (the structural pivot).** 5.10 implied, 87°/wind-out at Rate vs weak Burke, yet only **38.9% combined own** — the slate's biggest total-vs-ownership gap. Ohtani $6,600 / Freeman $5,200 / Betts $4,300 / Muncy $4,500 / Pages $5,100 / Tucker $4,600.
  - **If played →** 4-man core (Ohtani/Freeman/Betts/Muncy ≈ $20,600) needs the cheap-SP2 route to fit alongside Yamamoto; add a cheap secondary 2-stack. Go 4-man not 5 (smash-compresses-spread + 5-man-conditional — no need to jam the 5th premium when the edge is spread).
- **ARI — MIX (the chalk you can live with).** Slate-high 5.25 in a GABP bandbox vs Lowder. But ~85% combined own. Marte $5,500 / Carroll $5,900 / Moreno $3,800 / Arenado $3,500. If you want chalk exposure, take ARI over SD — better park AND total for the same field crowding.
  - **If played →** Marte+Carroll+Moreno+Arenado ≈ $18,700 for 4; pairs cleanly with Yamamoto+Chandler. Best as the secondary behind LAD, or the primary if you fade LAD's price.
- **SD — PASS as primary / MIX as 1–2 pieces.** 96% combined own, cheap, at a milder 4.95 vs weak Trey Gibson. This is the FIELD's stack — you're with everyone if you go SD-5.
  - **If played anyway →** keep it to a Tatis+Merrill ($9,000) mini, not the full chalk 5; the value (Sheets/Fermin) is where dupes pile up.

### 4. Anchor-Equivalence call — SP trio Suarez / Skubal / deGrom (25.5–29.3%) → deGrom is the alternative
The three midrange-to-premium arms sit within ~4 pts of each other — the field treats them as interchangeable. **deGrom is the lowest-owned (25.5%) AND has the best matchup (BOS, 3.95, lowest-total game).** With one lineup, AE resolves to: *if* you roster a second premium arm, make it deGrom, not 29%-owned Suarez — uncontested leverage if the ace tier outscores. The default build (Yamamoto + cheap enabler) satisfies leverage on the stack side and sidesteps the trio entirely; that's also AE-compliant because you're off all three crowded arms. (Note: Suarez and deGrom oppose each other in TEX@BOS — never roster TEX/BOS bats with that arm.)

## Player board
Covers the chalk tier, every named leverage bat, traps, and vendor-disagreement names. Left off: the full punt-priced CLE/CWS/TEX bottoms and the off-slate 7:10/10:05 names — irrelevant to a build.

### Pitchers
| Pitcher | Sal | Proj | Own% | Call | If played → |
|---|---|---|---|---|---|
| Yamamoto (LAD/CWS) | $10.8K | 19.8 | 35→~55-60 | PLAY | floor anchor; pair cheap SP2, leverage in bats |
| deGrom (TEX/BOS) | $10.4K | 18.3 | 25.5 | MIX | AE alternative arm; best matchup; no TEX/BOS bats |
| Skubal (DET/CLE) | $10.0K | 18.7 | 27.8 | MIX | elite, but doubling $10K aces caps bats; no DET/CLE bats |
| Suarez (BOS/TEX) | $8.8K | 17.2 | 29.3 | PASS | highest-owned of the equiv trio — AE says take deGrom instead |
| Soroka (ARI/CIN) | $9.3K | 16.3 | 21.8 | PASS | pitching INTO the GABP bandbox at 4.50 — blocks the ARI stack |
| Cavalli (WSH/SEA) | $8.2K | 14.9 | 15.0 | MIX | fine SP2 if you want mid-salary; blocks no primary stack |
| Chandler (PIT/MIA) | $6.2K | 13.1 | 12.1 | PLAY | the enabler — unlocks LAD/ARI premium; keep it |
| Castillo (SEA/WSH) | $7.2K | 12.2 | 8.7 | PLAY | cheaper enabler, lower own; same role as Chandler |

### Hitters
| Player (team) | Sal | Proj | Own% | Call | If played → |
|---|---|---|---|---|---|
| Ohtani (LAD) | $6.6K | 10.9 | 10.4 | PLAY | LAD pivot anchor; build the 4-man around him |
| Freeman (LAD) | $5.2K | 8.9 | 4.8 | PLAY | underowned LAD core; pairs in the same stack |
| Betts (LAD) | $4.3K | 8.9 | 9.6 | PLAY | value-priced LAD middle; great salary saver in the stack |
| Muncy (LAD) | $4.5K | 8.4 | 7.5 | PLAY | LAD power, sub-10 — fills the pivot density |
| Pages (LAD) | $5.1K | 9.0 | 6.7 | MIX | LAD 5th piece only if you go 5-man on a blowup read |
| Marte (ARI) | $5.5K | 10.0 | 17.2 | MIX | ARI anchor at GABP; chalk-but-best-environment |
| Carroll (ARI) | $5.9K | 11.1 | 20.8 | MIX | ARI ceiling bat; pairs with Marte, chalk |
| Moreno (ARI) | $3.8K | 8.6 | 18.1 | MIX | cheap ARI catcher — salary glue for the stack |
| Arenado (ARI) | $3.5K | 8.3 | 18.5 | MIX | cheap ARI corner; same stack only |
| Tatis (SD) | $5.1K | 10.2 | 23.8 | MIX | SD chalk leadoff; cap SD to a Tatis+Merrill mini |
| Merrill (SD) | $3.9K | 9.5 | 22.7 | MIX | cheap SD chalk; high-dupe with Tatis |
| Henderson (BAL) | $5.7K | 10.2 | 13.3 | MIX | BAL is the under-the-radar live side at Camden (5.25) |
| Alonso (BAL) | $5.3K | 9.4 | 9.6 | MIX | BAL power, sub-10 — a real leverage stack vs SD's chalk |
| Basallo (BAL) | $3.9K | 8.7 | 15.0 | MIX | cheap BAL bat; stack glue |
| Witt Jr. (KC) | $6.0K | 10.6 | — | PASS | OFF-SLATE (7:10) — not playable; ignore if pool shows him |
| Leo Jimenez (MIA) | $2.2K | 6.6 | 0.0 | MIX | true punt vs Chandler — fills min-salary, not a stack anchor |
| Connor Norby (MIA) | $3.2K | 6.2 | 0.0 | MIX | cheap MIA bat, real 0% — salary relief only |
| Phillips/Suarez bats (TEX/BOS) | — | — | — | PASS | lowest-total game; both lineups suppressed — avoid bats |

## Where I disagree with the vendors
(SIN own MAE 3.28 over 4 slates — past the small-sample guard, so ownership is weightable; the disagreements below are mechanism-driven, not calibration.)
- **Vendor: Yamamoto 35.3% own. Me: ~55–60% actual.** The projected-own #1 SE arm condenses +30 every slate (Detmers 38→69, Scott 44→56-63, Misiorowski 25→55). This isn't a calibration miss (SIN's overall own MAE is 3.3) — it's concentrated on the chalk #1. Consequence: holding him is higher-floor than the field thinks, and fading him is a ~55–60% binary.
- **Vendor: LAD 38.9% combined own. Me: too low for the spot.** Highest implied total in the open-air hitting game (87°, wind out) vs a weak arm, yet the field anchors on cheaper SD/ARI. The price tag suppresses ownership, not the projection — that gap IS the edge.
- **Vendor: SD 96% combined own at 4.95. Me: overowned vs environment.** SD is cheap, so the field stacks it, but Camden vs a weak Trey Gibson also lights up BAL's OWN bats (5.25, the co-leader) at a third of the ownership. Be underweight SD, look at BAL as the same-game leverage side.
- **Cross-vendor: SaberSim has Skubal 13.89 vs SIN 18.7 (−29.5%).** SIN is the calibrated vendor (proj MAE 5.88) and Skubal's matchup (CLE 3.55, weak) supports the higher number — I side with SIN; the SaberSim figure looks like a workload/IP haircut, a risk note not a fade. SaberSim's Zach McKinstry 0.0 (vs SIN 6.33) is just a not-confirmed-lineup artifact — noise.

## Edges to exploit
1. **LAD as the one pivot, funded by the cheap-SP2 route.** Expression: Yamamoto + Chandler ($6.2K) or Castillo ($7.2K), then LAD-4 (Ohtani/Freeman/Betts/Muncy ≈ $20.6K) + a cheap 2-stack. ~38.9% combined LAD own vs 5.10 implied is the slate's biggest total-vs-own gap; the enabler arm is what makes the premium stack fit.
2. **Hold the condensing ace, spend the leverage in the bats.** Expression: lock Yamamoto, do NOT fade; take a non-SD primary so you're off the field's stack while still on the slate's best arm. Chalk-ace-smash says wider bat-spread (3–5 sub-10) wins when the ace condenses-and-smashes — lean LAD value + a punt (Jimenez/Norby) over a 5th premium.
3. **BAL > SD as the Camden side.** Expression: if you want the SD@BAL game, stack BAL (Henderson/Alonso/Basallo, ~13/10/15% own) instead of 96%-owned SD — same weak-pitching game environment, a third of the ownership.
4. **ARI over SD when you take chalk.** Expression: Marte+Carroll+Moreno+Arenado at GABP (5.25, bandbox) is the chalk with the best park AND total; if a slot must be chalky, make it this one, not the SD value pile where dupes concentrate.
5. **deGrom is the free AE leverage among the aces.** Expression: if a second premium arm fits, deGrom (25.5%, BOS 3.95 matchup) over Suarez (29.3%) — lowest-owned of the interchangeable trio with the best spot.
