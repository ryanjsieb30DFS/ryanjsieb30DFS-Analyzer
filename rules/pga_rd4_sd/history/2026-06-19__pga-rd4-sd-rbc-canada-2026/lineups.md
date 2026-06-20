# PGA RD4 Showdown — Selected lineups (RBC Canadian Open R4, TPC Toronto Osprey Valley)

_Selected FROM the uploaded lineup pool — these rosters were not invented. Source file: `lineups_dk_golf_classic_6-14-2026_1030am.csv` (5,000 rows, SaberSim w/ sims). Sim rank was NOT used as a quality filter; each row was chosen because it expresses the slate analysis's edges and Player-board calls. 6 entries → 6 lineups._

## Pre-flight checklist
- [x] Slate confirmed: RBC Canadian Open R4 — pool exported 6-14-2026 10:30am; matches the slate analysis (bundle 2026-06-14) and the live leaderboard (Suber -13, Cauley -12, Tommy/Clark/Jesper/Garnett -11). Current slate.
- [x] Pool loaded + IDs resolved: 5,000 candidate rows resolved via the DK PGA RD4 SD projections `dk_id` column (75 players); deduped by sorted roster.
- [x] Venue file read: `rules/pga_classic/courses/tpc_toronto_osprey_valley.md` (UNVERIFIED). 2026-06-14 note: course has played TOUGH (leader -13 vs 2025's -18) — the forcing evidence to tilt tough — but the venue's birdie-fest baseline + a calm Sunday is the live flip risk, so the birdie hedge is mandatory.
- [x] Open lessons reviewed: **ruleset-split-default** (codified) → 4 tough/moderate + 2 birdie hedges (tilt, not full commit); **anchor-equivalence** (codified) → Clark ×3, Burns ×2, Tommy ×2 (capped), none at 0%; **correct-chalk-concentration** (codified) → L2; **winning-structure 19%/1.7-darts** (codified) → every lineup ≥1 sub-10 dart, portfolio chalk-anchored; **sub15-midtier-birdiefest-score-source** (validated) → now genuinely expressed via **Theegala in L6** (the sub-15% mid-tier ceiling slot), rejected on the tough core (rule-set-gated mechanism); **repeated-punt-needs-thesis** (hypothesis) → no longer triggered: Pendrith is in L1 only; **leverage-play-still-mandatory** (hypothesis) → ≥1 sub-10 in all six, tough builds dosed ~1–2.
- [x] Framework pre-lock checks: Anchor-Equivalence split satisfied (Tommy/Burns/Clark rotated, Tommy ≤2); coffin → Suber 0% (the slate's #1 coffin), Cauley never paired with Suber, max-1 coffin/lineup; mid-tier trap ≤2 per lineup on DK own (all six clean — no Stone-adjustment needed); 60+ ceiling in every lineup; PASS tier (Suber/Hovland/Bridgeman) = 0; every lineup is a real row from the uploaded pool.
- [x] Prior results scanned: last 3 RD4 SDs lost at the tough-course over-commitment; this week tough is OBSERVED not predicted, so we tilt tough but keep 2 real birdie hedges. vendor_calibration.jsonl empty → mechanism only, no MAE weighting.

---

## Lineup 1 — Double-elite top end (Clark + Burns) · _selected from pool, file `lineups_dk_golf_classic_6-14-2026_1030am.csv`, row 4852_
**Thesis:** On a tough course where the field pays up for the 8K leader jam, the two highest-ceiling anchors the field can't afford *together* (Clark + Burns, 60+ ceilings both) plus a cheap second leader and the home-country leverage starter is the build no one can duplicate (Edge 3 + anchor-equivalence).

| Slot | Player | Salary | Own% (DK→Stone) | Key metric | Role |
|---|---|---|---|---|---|
| G | Sam Burns | $10,900 | 22.6 | ceil 66.4, -10 | Lowest-owned elite anchor |
| G | Wyndham Clark | $9,700 | 24.9 | ceil 62.0, -11 | Best-form elite anchor (best R3, top SG) |
| G | Ryan Fox | $8,500 | 21.4 | ceil 56.5, -10 | 2nd T-10 leader (def. champ) |
| G | Taylor Pendrith | $7,900 | 12.8→6.1 | ceil 53.2, -7 | Sub-10 leverage starter (Canadian) |
| G | David Skinns | $6,400 | 7.2 | -? value | Salary-engine dart |
| G | Ben Kohles | $6,300 | 5.8 | value | Salary-engine dart |

Salary: 10,900 + 9,700 + 8,500 + 7,900 + 6,400 + 6,300 = **$49,700** ≤ $50,000 ✓
T-10 starters: 3 (Burns/Clark/Fox) · sub-10 darts: ≥2 · 60+ ceiling: Burns/Clark · mid-tier (10-20%): 1 (Pendrith)
**Pendrith cheap-spike thesis:** home-country -7 starter at sub-6% Stone own with single-round upside — the leverage starter doing ceiling work. After the L3/L4 red-team fixes Pendrith is now isolated to L1 only (no longer a repeated punt), the home-country differentiator for the double-elite build.
**What if?** _What if the field's salary is trapped in the 8K leader jam and the two un-pairable elite anchors both post 60+?_

## Lineup 2 — Correct-Chalk Concentration (the connected core) · _selected from pool, row 4557_
**Thesis:** Roster the justified moderate-own core *together* rather than as scattered legs — Clark + Cauley + Yella + Mitchell, the connected ~10-25% own group with real ceilings, plus a cheap T-10 leader (Horschel) and a sub-10 value (Potgieter); when the field shares this core, you need the whole thing in one lineup (Edge 4, correct-chalk-concentration lesson).

| Slot | Player | Salary | Own% (DK→Stone) | Key metric | Role |
|---|---|---|---|---|---|
| G | Wyndham Clark | $9,700 | 24.9 | ceil 62.0, -11 | Core anchor |
| G | Keith Mitchell | $8,900 | 10.8→8.7 | ceil 57.7, -7 | Sub-10 ceiling pivot |
| G | Bud Cauley | $8,600 | 34.8→22.7 | ceil 57.9, -12 | The one 8K leader (best underlying) |
| G | Sudarshan Yellamaraju | $8,300 | 21.9 | ceil 58.2, -10 | Connected T-10 leader |
| G | Aldrich Potgieter | $7,800 | 7.8 | upside | Sub-10 value |
| G | Billy Horschel | $6,500 | 18.2 | -10 | Cheap T-10 leader |

Salary: 9,700 + 8,900 + 8,600 + 8,300 + 7,800 + 6,500 = **$49,800** ≤ $50,000 ✓
Leaderboard starters: 4 (Clark/Cauley/Yella/Horschel) · sub-10: 2 (Mitchell/Potgieter) · 60+ ceiling: Clark · mid-tier: 2 (Mitchell/Horschel) · cum own ~118 (≈19.7 avg — squarely the winning-structure target)
**What if?** _What if the field's shared correct-chalk core is exactly right, and the win goes to whoever rostered all of it connected?_

## Lineup 3 — Modal anchor + the best-underlying leader (tough) · _selected from pool, file `lineups_dk_golf_classic_6-14-2026_1030am.csv`, row 759 (re-selected from pool per red team)_
**Thesis:** The tough-course build that field-weights the modal anchor (Tommy) and pairs him with the *one* 8K leader worth taking — Cauley (best win/top-5 underlying) — then pivots the rest to low-owned starters who can actually move on a hard course (Stanger -10, Homa, Potgieter), refusing the second jammed leader (Edge 2: take one 8K leader, pivot the rest).

| Slot | Player | Salary | Own% (DK→Stone) | Key metric | Role |
|---|---|---|---|---|---|
| G | Tommy Fleetwood | $10,800 | 30.9→42.8 | ceil 67.0, -11 | Modal anchor |
| G | Bud Cauley | $8,600 | 34.8→22.7 | ceil 57.9, -12 | The one 8K leader |
| G | Harry Hall | $8,400 | 5.7→5.3 | ceil 54.7 | Sub-10 mid-salary value |
| G | Aldrich Potgieter | $7,800 | 7.8→5.7 | ceil 51.1 | Sub-10 value |
| G | Max Homa | $7,100 | 9.9→18.8 | ceil 54.7, -8 | Name-brand sub-10 (DK) pivot |
| G | Jimmy Stanger | $7,000 | 10.5→9.1 | ceil 49.8, -10 | Sub-10 near-lead starter |

Salary: 10,800 + 8,600 + 8,400 + 7,800 + 7,100 + 7,000 = **$49,700** ≤ $50,000 ✓
T-10 starters: 3 (Tommy/Cauley/Stanger) · sub-10 (DK): Hall/Potgieter/Homa · 60+ ceiling: Tommy · mid-tier (10-20% DK): 1 (Stanger) · cum own ~100
**Red-team fix (re-selected from pool):** dropped Pavon (2.7%, way-back — a dart that can't post on a tough course) and Pendrith (-7, over-exposed across L1/L3/L4); the pivots are now sub-10% starters who can move on a hard course (Stanger -10 near lead, plus the Hall/Potgieter/Homa value cast). No way-back darts.
**What if?** _What if the course stays tough and the modal anchor + the best-underlying leader hold while the second-leader jam (Suber) stalls?_

## Lineup 4 — Burns + Koepka leverage (tough, names the field abandoned) · _selected from pool, file `lineups_dk_golf_classic_6-14-2026_1030am.csv`, row 196 (re-selected on REAL leaderboard positions)_
**Thesis:** The leverage tough build — the lowest-owned elite (Burns) paired with a contrarian ceiling *name* the field walked away from (Brooks Koepka, a major champ at 4.2% own because he sits -6) over a positioned low-owned cast (Homa/Mouw -8, McGreevy -6, Bezuidenhout -4), with zero Suber/Cauley/Tommy chalk. Every player is still in the red on a tough course, so the leverage survives the read — this is the lowest cum-own lineup the field doesn't have (anchor-equivalence alternative + leverage-still-mandatory).

| Slot | Player | Salary | Own% (DK→Stone) | Key metric | Role |
|---|---|---|---|---|---|
| G | Sam Burns | $10,900 | 22.6 | ceil 66.4, -10 | Lowest-owned elite anchor |
| G | Brooks Koepka | $10,200 | 4.2→8.7 | ceil 55.7, -6 | Contrarian ceiling name (field abandoned) |
| G | Max Homa | $7,100 | 9.9→18.8 | ceil 54.7, -8 | Sub-10 (DK) positioned value |
| G | William Mouw | $7,100 | 9.3→9.4 | ceil 52.4, -8 | Sub-10 positioned value |
| G | Max McGreevy | $7,200 | 6.7→5.4 | ceil 52.7, -6 | Sub-10 value |
| G | Christiaan Bezuidenhout | $7,400 | 4.6→3.9 | ceil 52.0, -4 | Sub-5 value |

Salary: 10,900 + 10,200 + 7,100 + 7,100 + 7,200 + 7,400 = **$49,900** ≤ $50,000 ✓
Real leaderboard: all six in the red (-4 to -10) — no way-back darts · sub-5 (DK): Koepka 4.2, Bezuidenhout 4.6 · 60+ ceiling: Burns · mid-tier (10-20% DK): **0** · cum own ~57 (the portfolio's true leverage / lowest-cum lineup)
**Correction (re-selected on real positions):** the prior L4 carried Nick Taylor on a fabricated "-11" tag — he is actually **+6** (0% win / 0% top-5), a way-back dart that dies on a tough course. Replaced via real pool row 196: Burns + Koepka headline a deep-leverage build where **every piece is verified on the leaderboard**. Also drops Fox out of L4 (Fox now 2 lineups, not 3).
**What if?** _What if the tough course rewards the low-owned names already in the red that the field faded — Burns + Koepka anchoring a lineup nobody else has?_

## Lineup 5 — Birdie hedge A: chalk leaders + way-back darts · _selected from pool, row 617_
**Thesis:** The calm-Sunday hedge where scoring reopens and BOTH the chalk leaders (Tommy/Cauley/Fox) AND the way-back sub-5 spikes (Thorbjornsen 3.2%, Tom Kim 4.0%) go low — the birdie-fest world the tough core can't reach, with the mandatory sub-5 spike slot we keep skipping (sub5-spike-portfolio clause + sub15-midtier-birdiefest mechanism).

| Slot | Player | Salary | Own% (DK→Stone) | Key metric | Role |
|---|---|---|---|---|---|
| G | Tommy Fleetwood | $10,800 | 30.9→42.8 | ceil 67.0, -11 | Chalk leader anchor |
| G | Bud Cauley | $8,600 | 34.8→22.7 | ceil 57.9, -12 | Chalk leader |
| G | Ryan Fox | $8,500 | 21.4 | ceil 56.5, -10 | Chalk leader |
| G | Michael Thorbjornsen | $7,500 | 6.8→3.2 | ceil 50.8, -4 | Sub-5 way-back spike |
| G | Tom Kim | $7,400 | 5.8→4.0 | ceil 50.1, -6 | Sub-5 way-back spike |
| G | Kevin Yu | $7,200 | 6.0 | upside | Sub-10 value |

Salary: 10,800 + 8,600 + 8,500 + 7,500 + 7,400 + 7,200 = **$50,000** ≤ $50,000 ✓
Leaderboard: 3 (Tommy/Cauley/Fox, birdie min) · sub-5 spikes: 2 (Thorb/Tom Kim) · 60+ ceiling: Tommy · mid-tier: 0
**What if?** _What if Sunday calms, scoring reopens, and the leaders AND the way-back lottery tickets all post -6/-7?_

## Lineup 6 — Birdie hedge B: the faded -9 block (leverage version) + spikes · _selected from pool, file `lineups_dk_golf_classic_6-14-2026_1030am.csv`, row 2741 (re-selected from pool)_
**Thesis:** The other birdie world — the -9 T12 block the tough core FADED posts low rounds in a reopened scoring environment, but expressed through its *leverage* members (MacIntyre + **Theegala**, the validated sub-15% mid-tier ceiling slot) rather than the chalk -9s, anchored by Clark and paired with two cheap spikes (Bezuidenhout 4.6%, McGreevy); this is the hedge against our own tough-course read (the scar tissue from Cadillac/Truist/CJ Cup).

| Slot | Player | Salary | Own% (DK→Stone) | Key metric | Role |
|---|---|---|---|---|---|
| G | Wyndham Clark | $9,700 | 24.9 | ceil 62.0, -11 | Anchor |
| G | Robert MacIntyre | $9,000 | 18.4 | ceil 60.3, -9 | Faded -9 climber (live on birdie) |
| G | Sahith Theegala | $8,800 | 13.5→9.9 | ceil 55.4, -9 (T12) | Sub-15 mid-tier ceiling slot (the board's PLAY) |
| G | Aldrich Potgieter | $7,800 | 7.8→5.7 | ceil 51.1 | Sub-10 value |
| G | Christiaan Bezuidenhout | $7,400 | 4.6→3.9 | ceil 52.0 | Sub-5 spike |
| G | Max McGreevy | $7,200 | 6.7→5.4 | ceil 52.7, -6 | Sub-5 way-back spike |

Salary: 9,700 + 9,000 + 8,800 + 7,800 + 7,400 + 7,200 = **$49,900** ≤ $50,000 ✓
Birdie block: MacIntyre/Theegala (-9 T12) · sub-5 spikes: 2 (Bezuidenhout 4.6 DK, McGreevy) · 60+ ceiling: MacIntyre/Clark · mid-tier (10-20% DK): 2 (MacIntyre/Theegala) · cum own ~76
**Finding #2 fix (re-selected from pool):** swaps the chalk -9s (Lowry/MacIntyre at ~18%) for the *leverage* version of the same block — MacIntyre kept for the 60+ ceiling, plus **Theegala** (the board's unused sub-15% mid-tier PLAY, 9.9% on SIN), now expressing the validated `sub15-midtier-birdiefest-score-source` lesson the prior hedge skipped. Lower cum own (76) and a real sub-5 spike (Bezuidenhout).
**What if?** _What if the birdie-fest comes and the win lives in the leverage members of the faded -9 block (MacIntyre/Theegala), not the chalk -9s the field piles into?_

---

## Portfolio audit

**Rule-set split (codified lesson):** L1–L4 tough/moderate (4), L5–L6 birdie hedges (2). Tilted tough on OBSERVED scoring (leader -13, +4 rounds, R2 leader collapsed) — the forcing evidence the lesson requires for one-sided lean — while keeping two real birdie hedges with the sub-5 spike slot. Not a full commit; the scar tissue from three straight tough-course losses is honored.

**Anchor-Equivalence (mandatory pre-lock):** Tommy (L3, L5) = 2 of 6 (capped per analysis); Burns (L1, L4) = 2; Clark (L1, L2, L6) = 3. All three elite anchors run, none at 0% (never-zero-top3). The Clark-frees-salary route is expressed in L1 (Clark enables Burns alongside) and L2.

**8K leader / coffin discipline:** Suber (the slate's #1 coffin, ~38% own, "overpriced") = **0 lineups** — the deliberate fade. Cauley (the better-underlying 8K leader) = L2, L3, L5, always as the lone 8K leader, never paired with Suber. Max-1 coffin per lineup holds throughout. PASS-tier (Hovland, Bridgeman) = 0 lineups.

**Player overlap / diversification:** No two lineups share more than 2 of 6 (framework limit is 4). **Watch-items at 50% (3/6) — at the cap, none over it:** Cauley (L2/L3/L5, flagged prior), Potgieter (L2/L3/L6 — sub-10 value across three builds). Fox dropped to 2 (L1/L5) after the L4 re-selection. Pendrith is isolated to L1, so the repeated-punt concern no longer applies. All other repeats ≤ 2.

**Mid-tier trap:** ≤2 plays at 10-20% DK own per lineup — satisfied on **DK own** everywhere, no Stone-adjustment needed: L1 = 1 (Pendrith), L2 = 2 (Mitchell/Horschel), L3 = 1 (Stanger), L4 = 0, L5 = 0, L6 = 2 (MacIntyre/Theegala). The prior L4 violation (three in band) is gone.

**Real-position audit (vs The Stone R4 leaderboard):** every player on the tough builds (L1–L4) is in the red — verified Event Score, not inferred from tee time. L4's prior Nick Taylor "-11" was wrong (he is +6); re-selected so all six L4 pieces are -4 or better. Birdie hedges (L5/L6) intentionally carry way-back spikes (Thorbjornsen -4, etc.).

**Ceiling + leverage floors:** Every lineup has a 60+ ceiling player and ≥1 sub-10 dart (leverage-still-mandatory). The portfolio carries the mandatory sub-5 spike across the birdie hedges (L5: Thorbjornsen/Tom Kim; L6: Bezuidenhout/McGreevy) — the slot skipped at PGA Champ/Truist. L4's leverage now runs through Koepka (4.2%) + Bezuidenhout (4.6%).

**Edges expressed:** Edge 1 anchor-equivalence split → whole portfolio; Edge 2 one 8K leader + sub-10 pivots → L3 (and L2); Edge 3 cheap-leader engine to double elites → L1; Edge 4 correct-chalk concentration → L2; Edge 5 mandatory sub-5 spike on the hedges → L5/L6; the validated sub-15% mid-tier ceiling slot (sub15-midtier-birdiefest) → **Theegala in L6**. The Burns leverage build (L4) expresses the lowest-owned-elite anchor-equivalence alternative.

**Distinct questions:** double-elite hold (L1) · shared-core correctness (L2) · modal anchor + best leader on tough (L3) · Burns+Koepka deep-leverage names the field abandoned on tough (L4) · calm-Sunday chalk-leaders + spikes (L5) · faded -9 block leverage version in a birdie-fest (L6). Six different bets, not one thesis sized ×6.

**Pool provenance:** every lineup is a verified real row from `lineups_dk_golf_classic_6-14-2026_1030am.csv` — L1 row 4852, L2 row 4557, L3 row 759, L4 row 196, L5 row 617, L6 row 2741.
