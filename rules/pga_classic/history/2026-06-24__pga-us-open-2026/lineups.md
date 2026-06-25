# PGA Classic — Lineups: U.S. Open at Shinnecock Hills (R1 Thu 6/18/2026)

_**Selected FROM the uploaded lineup pool** (`lineups_dk_golf_classic_6-18-2026_635am.csv`, 5,000 candidate rows). Rosters were NOT invented — each lineup is a real pool row, resolved by `dk_id` and chosen for **edge-fit to the slate analysis** (sim ROI / Saber Score / sim-dupes columns were read but **deliberately NOT used as the quality filter**, per repo rules). 6 lineups for the **PGA $20K Mulligan** + **PGA $10K Eagle** (both 5-Max, 3/5 entries). This file supersedes the prior auto-selection for this slate (no handbuilt lineups were present to preserve). **Red-team fixes applied:** L1 was re-selected from the pool to resolve the FIX verdict; L2–L6 carried SHIP and are kept verbatim._

## Pre-flight checklist
- [x] **Slate confirmed:** golf — **U.S. Open, Shinnecock Hills** (par 70, penal major, 36-hole cut to top 60+ties). Pool file dated 6-18-2026 6:35am; projections + slate analysis are THIS slate. Selecting from this slate's pool, not analyzing stale data.
- [x] **Projections loaded:** ETR PGA (156 players) carry `dk_id`; **every selected pool row was resolved to names/salary/own/ceiling** off the session projections. Pool = 5,000 rows, has sims (sims read, NOT used to rank).
- [x] **Venue file read:** `rules/pga_classic/courses/shinnecock_hills.md` (**UNVERIFIED** stub). Penal "limit-the-damage" prior → elite anchors strengthened (drives the Scottie/Bryson+Brooks/Rahm+Xander anchor cores) and **cut risk is real for the cheap tier → zero way-back qualifiers selected** (Stout/Roy/Hammer/Sato/Coussaud all rejected).
- [x] **Open lessons applied** (each named in the thesis it shaped):
  - `single-vendor-overweight-self-erosion` (hyp) → **Aaron Rai 0/6** (last week's exact bust; no single-vendor ETR coffin gap is a backbone). No coffin "+gap" used as conviction without a 2nd reason.
  - `leverage-spine-needs-sub20-combined-own` (hyp) → **Si Woo (29.6) + Fitz (25.1) never paired**; treated as two standalone chalk bets, split across separate lineups (SiWoo→L6, Fitz→L2/L3).
  - `mid-owned-value-spine-over-darts` + `leverage-play-mandatory` (codified) → the **10–16% ceiling band guaranteed across the set** (Hovland 2/6, plus Gotterup/Spaun/Morikawa/McNealy/Adam Scott/W.Clark); the autopsy-gap fix.
  - `ch-scan-needs-skill-gate` (validated) → **every sub-5% piece is skill/form-floored** (Conners, Noren, Straka, Hojgaard, Mitchell, Hall, Woodland, Cauley, Bridgeman, J.T. Poston) — all ≥55% make-cut, none sub-40%-MC amateurs. _(Red-team FIX: the two off-board sub-50%-MC darts — Suber, Herbert — were removed from L1/L2.)_
  - `dose-darts-to-course-variance` (hyp) → 1–2 skill-floored sub-5 darts per build (penal-cut course caps dart count vs a birdie-fest; not a forced hard 3).
  - `contrarian-needs-leverage-anchor` (validated) → the deep chaos build (L3, own ~8.8/slot) is **floored by Fitz** alongside the two champ anchors — never all coin-flips.
  - `never-zero-value-chalk-anchor` (codified) → model #1 / lone "Lock" make-cut **Scottie carried in 2/6**; value-chalk star **Rory carried in 2/6** — neither zeroed.
  - `design-exposures-before-lineups` (hyp) → exposures set BEFORE picking rows (Scottie 2/6, Rory 2/6, Fitz 2/6, Hovland mid-band 2/6, SiWoo capped 1/6, **Rai 0/6**, 4/6 no-Scottie to honor the fade).
- [x] **Framework pre-lock checks:** **Anchor-Equivalence** satisfied on both clusters (value: L2 & L3 run **Fitz without Si Woo**; $10K: L3 Bryson+Brooks, L4 Rahm+Xander, L2/L6 Rory — **4/6 lineups are no-Scottie**). Bryson is the explicit 6.1% contrarian alternative (L3). "Never two of Fleetwood/Aberg/Fitzpatrick together" honored (no Aberg anywhere; Fleetwood and Fitz never share a lineup). All 6 unique, **max pairwise overlap 2/6** (no shared full core). All ≤ $50,000.
- [x] **Prior results scanned:** `results.jsonl` — RBC best 5.0%, Memorial 3.5% (ROI n/a, sample <10 → process only). Carry-in cure applied: **full exposure to the mid-owned ceiling band** the last two autopsies say we kept missing (Fox/Yellamaraju-equivalents here = Hovland/Morikawa/Kitayama/McNealy/Spaun).
- [x] **Sharp envelope:** every lineup all-unique ✅; **≥1 sub-5% skill-floored piece in 6/6** (L3/L4 carry 2) ✅; avg own/slot **8.8–14.2** (portfolio ~12.0, in/near the ~12–14 target; the chaos build runs contrarian-side by design) ✅; elite anchor + downstream differentiation ✅; ceiling-judged ✅.

---

## Lineup 1 — Model conviction (Scottie + proven value spine): Kitayama + English engines _(re-selected to fix red-team FIX)_
**Re-selected from pool to resolve the red team's L1 FIX:** the original L1 banked Scottie + Fleetwood behind **four** $6.2–6.6K sub-5% cut-coinflips — the exact structure Decision #1 forbids — and left **Kitayama AND English 0/6** (the review's strongest finding, P1). This pool row (`lineups_dk_golf_classic_6-18-2026_635am.csv`, **data row 1074**) installs **both** named $6–7K value engines in one lineup and collapses the cut-coinflip count from four to **one**, exceeding the "four→three" the FIX asked for and closing all of P1.

**Thesis (how it wins):** Scottie's lone-"Lock" conviction, now banked behind the **proven mid-owned value spine Decision #1 demands** — Kitayama + English, the two highest-coffin $6–7K engines (the literal headliners of the autopsy-proven win condition, `mid-owned-value-spine-over-darts`) — instead of a four-deep $5–6K cut-coinflip swamp, finished with one skill-floored sub-5 (Hojgaard, 59% MC).

| Golfer | Salary | Own% | Ceiling | Role |
|---|---|---|---|---|
| Scottie Scheffler | $14,900 | 24.3 | 101.0 | Primary anchor (model #1, lone "Lock" MC) — conviction kept |
| Sam Burns | $7,700 | 19.2 | 83.0 | Value-chalk co-anchor, standalone (NOT w/ Si Woo/Cantlay per Player board) |
| Jordan Spieth | $7,100 | 6.0 | 77.7 | Sub-10 ceiling value (major champ) |
| Harris English | $6,700 | 11.1 | 74.0 | 2nd mid-owned value engine (+6.4 coffin, 63% MC) — closes the other half of P1 |
| Nicolai Hojgaard | $6,700 | 4.0 | 73.6 | Sub-5 skill-floored dart (59% MC) — the single required leverage piece |
| Kurt Kitayama | $6,500 | 12.4 | 80.0 | Proven $6–7K floor (+16.2 coffin, 61% MC) — the named Decision-#1 / P1 fix |

**Salary:** 14,900 + 7,700 + 7,100 + 6,700 + 6,700 + 6,500 = **$49,600** ✅ (≤ $50,000)
**Avg own/slot:** 12.8 (sits on the codified ~13% winning envelope) · **Sub-5 pieces:** 1 (Hojgaard, 59% MC)
**What if?** — _What if the slate is won exactly where the last two autopsies say it is: Scottie floors it while the proven 11–12%-owned value multipliers (Kitayama, English) carry the lineup — the win condition the original L1 named but zeroed?_

## Lineup 2 — Anchor-Equivalence (value tier): Fitz over Si Woo, NO Scottie, mid-band ceiling
**Thesis (how it wins):** runs the **Fitzpatrick (2022 USO champ) value anchor instead of the higher-owned Si Woo** (`leverage-spine-needs-sub20-combined-own` — the two never paired) alongside value-chalk star **Rory**, then loads the **mid-owned ceiling band** (Gotterup, Spaun) the autopsies say wins these, finished by **Cauley** — last week's slate-definer profile (`mid-owned-value-spine-over-darts`) — as the vetted skill dart. The no-Scottie, balanced-build expression of Edge #4. _**Red-team FIX applied:** the off-board sub-50%-MC dart (Herbert, 49.6% MC) is replaced — re-selected from pool: file `lineups_dk_golf_classic_6-18-2026_635am.csv`, **data row 4037** (supersedes prior row 268)._

| Golfer | Salary | Own% | Ceiling | Role |
|---|---|---|---|---|
| Rory McIlroy | $12,200 | 21.5 | 93.4 | Value-chalk star anchor (model #2) |
| Matt Fitzpatrick | $8,900 | 25.1 | 83.1 | Value anchor (the Si-Woo alternative) |
| Chris Gotterup | $8,200 | 16.0 | 78.9 | Mid-owned ceiling (length + form) |
| J.J. Spaun | $7,500 | 11.2 | 77.8 | Mid-owned multiplier (defending champ) |
| Bud Cauley | $6,700 | 3.4 | 71.8 | Sub-5 vetted skill dart (60% MC, RBC slate-definer) |
| Jacob Bridgeman | $6,500 | 5.4 | 73.4 | Skill-floored value (56% MC) |

**Salary:** 12,200 + 8,900 + 8,200 + 7,500 + 6,700 + 6,500 = **$50,000** ✅ (≤ $50,000)
**Avg own/slot:** 13.8 · **Sub-5 pieces:** 1 (Cauley; Bridgeman 5.4% just above)
**What if?** — _What if Fitz is the slate-definer the field splits with Si Woo, and the Fitz-not-Si-Woo coin lands your way (the RBC pattern repeating) while the mid-owned band carries it?_

## Lineup 3 — Chaos / $10K Anchor-Equivalence: Bryson + Brooks (two USO champs), Fitz floor, NO Scottie
**Thesis (how it wins):** the two U.S. Open champions the field has at **~13% combined own** — **Bryson** (6.1%, course-fit #2: length + the widest USO fairways) + **Brooks** (7.2%, **won at this exact course in 2018**) — detonate at a venue built for their profiles, while the build never goes all-coin-flips: **Fitz is the leverage-grade floor** (`contrarian-needs-leverage-anchor`) with **Straka + Hojgaard** as two skill-floored sub-5 darts. The deepest-leverage no-Scottie build (own ~8.8/slot). _Selected from pool: file `lineups_dk_golf_classic_6-18-2026_635am.csv`, **data row 3185**._

| Golfer | Salary | Own% | Ceiling | Role |
|---|---|---|---|---|
| Bryson DeChambeau | $11,000 | 6.1 | 81.8 | Leverage anchor (2× USO champ, course-fit #2) |
| Brooks Koepka | $9,400 | 7.2 | 78.3 | 2nd champ anchor (won Shinnecock '18) |
| Matt Fitzpatrick | $8,900 | 25.1 | 83.1 | Leverage-grade floor (2022 USO champ) |
| Kristoffer Reitan | $6,900 | 7.1 | 76.7 | Sub-10 value |
| Sepp Straka | $7,000 | 3.5 | 69.8 | Sub-5 skill-floored dart (multi-time winner) |
| Nicolai Hojgaard | $6,700 | 4.0 | 73.6 | Sub-5 skill-floored dart |

**Salary:** 11,000 + 9,400 + 8,900 + 6,900 + 7,000 + 6,700 = **$49,900** ✅ (≤ $50,000)
**Avg own/slot:** 8.8 · **Sub-5 pieces:** 2 (Straka, Hojgaard)
**What if?** — _What if the major-pedigree horses the field is sleeping on win the course-fit slate while Scottie merely makes the cut — the chaos outcome no chalk build covers?_

## Lineup 4 — $10K Anchor-Equivalence alt: Rahm + Xander, cheap skill-leverage spine, NO Scottie
**Thesis (how it wins):** the second no-Scottie hedge — the LIV-suppressed penal monster **Rahm** (16.7%, course-fit #6) + the alternative $10K chalk **Xander** — funding the slate's cleanest cheap edge: **Conners (1.3%) + Noren (4.9%)**, two accuracy/penal-fit ball-strikers at a fraction of equivalent-skill ownership (`ch-scan-needs-skill-gate`). Henley/Spieth fill the accuracy mid-tier. _Selected from pool: file `lineups_dk_golf_classic_6-18-2026_635am.csv`, **data row 3613**._

| Golfer | Salary | Own% | Ceiling | Role |
|---|---|---|---|---|
| Jon Rahm | $11,500 | 16.7 | 89.1 | Leverage anchor ($10K alt, own suppressed) |
| Xander Schauffele | $10,100 | 19.8 | 86.6 | 2nd elite anchor (Scottie alternative) |
| Russell Henley | $8,000 | 16.9 | 80.0 | Accuracy / short-game penal fit |
| Jordan Spieth | $7,100 | 6.0 | 77.7 | Sub-10 ceiling value (major champ) |
| Corey Conners | $6,500 | 1.3 | 63.9 | Sub-5 standout skill-floored leverage |
| Alex Noren | $6,400 | 4.9 | 69.5 | Sub-5 accuracy/penal-fit dart |

**Salary:** 11,500 + 10,100 + 8,000 + 7,100 + 6,500 + 6,400 = **$49,600** ✅ (≤ $50,000)
**Avg own/slot:** 10.9 · **Sub-5 pieces:** 2 (Conners, Noren)
**What if?** — _What if the two elite anchors the field under-owns relative to skill (Rahm's LIV discount, Xander's Scottie shadow) carry it, and Conners is the cheap skill-floored smash the mining says shows up 96% of slates?_

## Lineup 5 — Mid-owned ceiling band carries it (autopsy-gap fix), Scottie floor _(re-selected to trim Spieth exposure)_
**Re-selected from pool to trim undesigned Spieth concentration:** Spieth had crept to 3/6 (50%) as a byproduct of the L1 swap — an emergent, not designed, exposure to a 6%-owned piece (`design-exposures-before-lineups`). This pool row (`lineups_dk_golf_classic_6-18-2026_635am.csv`, **data row 667**) keeps L5's thesis intact while swapping **Spieth → Shane Lowry** (same sub-10% ceiling archetype, links pedigree), dropping Spieth to a designed 2/6 and removing the half-portfolio shared-failure risk.

**Thesis (how it wins):** directly closes the last-two-slates gap (zero exposure to the Fox/Yellamaraju mid-owned multipliers) — the **mid-owned ceiling band (Hovland, McNealy, Kitayama)** is the backbone behind a **Scottie** floor, with **Lowry** the links-pedigree sub-10% ceiling value and **Hall** the skill dart (`mid-owned-value-spine-over-darts`). The leverage-leaning Scottie build with downstream differentiation from L1.

| Golfer | Salary | Own% | Ceiling | Role |
|---|---|---|---|---|
| Scottie Scheffler | $14,900 | 24.3 | 101.0 | Anchor floor (model #1) |
| Viktor Hovland | $8,100 | 9.4 | 82.8 | Mid-owned ceiling band |
| Shane Lowry | $7,100 | 6.8 | 74.1 | Sub-10 ceiling value (links pedigree) — the Spieth-trim swap |
| Maverick McNealy | $6,800 | 11.2 | 75.3 | Mid-owned multiplier |
| Kurt Kitayama | $6,500 | 12.4 | 80.0 | Mid-owned ceiling engine |
| Harry Hall | $6,200 | 1.4 | 64.2 | Sub-5 skill-floored dart (55% MC) |

**Salary:** 14,900 + 8,100 + 7,100 + 6,800 + 6,500 + 6,200 = **$49,600** ✅ (≤ $50,000)
**Avg own/slot:** 10.9 · **Sub-5 pieces:** 1 (Hall, 55% MC)
**What if?** — _What if the slate is won below the anchors — the mid-owned ceiling multipliers smash while the expensive non-Scottie chalk underperforms?_

## Lineup 6 — Value-chalk-correct + elite irons: Si Woo engine + Morikawa/Rory, deep dart, NO Scottie
**Thesis (how it wins):** the one **Si Woo** lineup, deployed as the **value engine** (genuinely ~$1.5K underpriced) funding **Rory** + the elite-iron mid band that fits this approach test — **Morikawa** (coffin fade I take the leverage on) + **Hovland** + **defending champ Spaun** — with **J.T. Poston** (the form/value cheap-definer profile that beat us at Memorial) as the deep dart. Si Woo is standalone here, never paired with Burns/Cantlay. _Selected from pool: file `lineups_dk_golf_classic_6-18-2026_635am.csv`, **data row 157**._

| Golfer | Salary | Own% | Ceiling | Role |
|---|---|---|---|---|
| Rory McIlroy | $12,200 | 21.5 | 93.4 | Value-chalk star anchor |
| Collin Morikawa | $8,500 | 11.6 | 79.9 | Elite-irons leverage (coffin fade I take) |
| Viktor Hovland | $8,100 | 9.4 | 82.8 | Mid-owned ceiling band |
| J.J. Spaun | $7,500 | 11.2 | 77.8 | Mid-owned multiplier (defending champ) |
| Si Woo Kim | $7,200 | 29.6 | 81.6 | Value engine (capped to this lineup) |
| J.T. Poston | $6,300 | 2.1 | 72.6 | Sub-5 form/value deep dart |

**Salary:** 12,200 + 8,500 + 8,100 + 7,500 + 7,200 + 6,300 = **$49,800** ✅ (≤ $50,000)
**Avg own/slot:** 14.2 · **Sub-5 pieces:** 1 (J.T. Poston)
**What if?** — _What if the value-chalk consensus AND the elite-iron mid band both pay — Si Woo's price is right, Morikawa's irons fit the approach test, and the slate rewards accuracy over the expensive anchors?_

---

## Portfolio audit

**Count:** 6 lineups delivered (hard requirement met). All selected from the uploaded pool, all resolved by `dk_id`, all ≤ $50,000, each traceable to a real pool row index. **Fixes applied this pass:** **L1 re-selected post-red-team (row 1074)** to resolve the FIX verdict — cut-coinflip swamp out, Kitayama + English proven value spine in (Scottie conviction kept); **L5 re-selected (row 667)** to trim undesigned Spieth concentration (3/6 → 2/6), Spieth → Lowry with the thesis intact; **L2/L3/L4/L6 carried SHIP and are kept verbatim** (L2 retains its earlier off-board-dart fix at row 4037).

**Distinct questions (no near-duplicates, no shared full core):**
- L1 chalk-conviction-correct (Scottie floor + proven mid-owned value spine Kitayama/English) · L2 Fitz-over-Si-Woo value-anchor + mid-band (no Scottie) · L3 two-USO-champ chaos with Fitz floor (no Scottie, deep) · L4 Rahm/Xander LIV-discount + cheap-skill spine (no Scottie) · L5 mid-owned-band-wins with Scottie floor · L6 value-chalk-correct + elite-irons (Si Woo engine, no Scottie).
- **Max pairwise roster overlap = 2/6** (L1∩L5 = Scottie+Kitayama; others ≤1) — well inside the no-shared-core rule. All 6 unique.

**Replacement overlap re-check (new L1 + new L5 vs every kept lineup, by name):** L1∩L2 = 0 · L1∩L3 = 1 (Hojgaard) · L1∩L4 = 1 (Spieth) · L1∩L5 = 2 (Scottie, Kitayama) · L1∩L6 = 0 · L5∩L6 = 1 (Hovland) · L5∩others ≤1. Max = **2/6** — no near-duplicate, no shared full core.

**Exposures (re-balanced by the L1 + L5 swaps):**
- **Scottie 2/6** (33%) — model #1 / lone "Lock," strengthened at a penal major; held to 2 to honor the Edge-#5 fade (4/6 lineups are no-Scottie).
- **Rory 2/6**, **Fitz 2/6** — value-chalk stars not zeroed (`never-zero-value-chalk-anchor`).
- **Spieth 2/6 (was 3/6)** — trimmed by the L5 swap; a 6%-owned piece now sized on purpose (L1 + L4), not an emergent 50% (`design-exposures-before-lineups`).
- **Mid-owned ceiling band (autopsy-gap fix, now fully closed):** Hovland 2/6, **Kitayama 2/6** (L1 + L5), **English 1/6** (P1 gaps closed), **Lowry 1/6 (new)**, plus Gotterup / Spaun (2/6) / Morikawa / McNealy 1/6 each; every lineup except the deep-chaos L3 carries ≥1 mid-owned 10–16% multiplier.
- **Si Woo 1/6** (capped, standalone — never with Burns/Cantlay) · Bryson/Brooks/Rahm/Xander 1/6 each · **Burns 1/6** (PASS play, but standalone — within the Player board's "if anyway: standalone, not w/ Si Woo" escape hatch).
- **Removed by the fixes:** **Fleetwood 1→0/6** (L1 swap — logged trade-off; he is value chalk, not the model-#1 / Anchor-Equiv alternative, so the cluster stays covered by Scottie 2/6, Rory 2/6, Bryson, Rahm+Xander; zeroing him does NOT trip `never-zero-value-chalk-anchor`); **Adam Scott 1→0/6** and **Mitchell 1→0/6** (L5 swap — both replaced by Lowry + Kitayama + Hall, same mid-owned/skill-dart roles). Noren (L4) retains its home.
- **Aaron Rai 0/6** — `single-vendor-overweight-self-erosion` honored. **Cameron Young / Knapp / Niemann 0/6** (slate-analysis PASS plays). **Zero way-back sub-1% amateurs** (Stout/Roy/Hammer/Sato/Coussaud) — penal-cut survival gate.

**Hedges / Anchor-Equivalence compliance (re-checked across the fixed set):**
- **Value tier (Si Woo 29.6 / Fitz 25.1):** L2 + L3 run **Fitz WITHOUT Si Woo** ✅ (Si Woo isolated to L6).
- **$10K cluster (Scottie 24.3 / Fleetwood 22.9 / Rory 21.5 / Aberg 21.5 / Xander 19.8 / Young 19.5):** L3 (Bryson+Brooks), L4 (Rahm+Xander), L2/L6 (Rory) all run alternatives — **4/6 no-Scottie** ✅. Bryson is the explicit 6.1% contrarian alternative (L3) ✅.
- "Never two of Fleetwood/Aberg/Fitzpatrick together" ✅ (Fleetwood now 0/6; no Aberg; Fleetwood and Fitz never share a lineup).

**Sharp envelope (after fix):** all-unique ✅; **≥1 sub-5% skill-floored piece in 6/6** (L3/L4 carry 2 — all ≥55% MC) ✅; per-lineup avg own 8.8–14.2 (new L1 = 12.8, on the ~13% codified winning envelope; portfolio ~12.0 — conviction/value builds in the 11–14 band, the chaos build contrarian-side by design) ✅; elite anchor + downstream differentiation ✅; ceiling-judged ✅. Cumulative own per lineup spans ~53–83% (L3 deep contrarian → L6 chalk-leaning) — a healthy spread across slate outcomes.

**Edge-to-lineup map (from the slate analysis):**
- Edge 1 (Bryson contrarian top anchor, 6.1%, course-fit #2) → **L3**
- Edge 2 (own the entire 10–16% value-multiplier band) → **L1** (Kitayama/English), **L2** (Gotterup/Spaun), **L5** (Hovland/McNealy/Kitayama/Lowry), **L6** (Morikawa/Hovland/Spaun)
- Edge 3 (skill-gated tough-course dart, not the amateur dart) → **L4** (Conners/Noren), **L3** (Straka/Hojgaard), **L1** (Hojgaard), **L2** (Cauley/Bridgeman), **L5** (Hall), **L6** (Poston)
- Edge 4 (Fitz over Si Woo as the major-pedigree value anchor) → **L2** (and Fitz floor in **L3**)
- Edge 5 (fade Scottie + coffin-fade chalk to free salary) → **4/6 no-Scottie builds** (L2/L3/L4/L6); Young/Knapp/Niemann/Rai all 0/6

**Fixes summary (what changed and why):**
- **L1 — FIX → replaced (row 1074).** Original banked Scottie + Fleetwood behind four sub-5% cut-coinflips (the structure Decision #1 forbids). Swap installs the proven $6–7K value spine (Kitayama +16.2 coffin / English +6.4 coffin), drops cut-coinflips from four to one (Hojgaard, 59% MC), and closes the review's strongest finding P1 (Kitayama 0→1/6 AND English 0→1/6) in a single lineup. Same question preserved (Scottie conviction + the value tier beneath him carries it). Logged trade-off: Fleetwood 1→0/6.
- **L5 — discretionary trim (row 667).** Not a red-team verdict — Spieth had emerged at 3/6 (50%) as a byproduct of the L1 swap. Re-selected to swap Spieth → Lowry (same sub-10% ceiling archetype), dropping Spieth to a designed 2/6 and removing the half-portfolio shared-failure risk (`design-exposures-before-lineups`). Thesis unchanged (mid-owned band + Scottie floor).
- **L2/L3/L4/L6 — SHIP, kept verbatim.** "No single legal roster change improves this lineup."

**Caveats:**
- The venue file is **UNVERIFIED** (no Slate Data uploaded) — the penal-major shape is a strong prior, not calibrated fact.
- `dose-darts-to-course-variance` leans ~3 darts on a tough course, but the **36-hole cut** caps how many sub-5 cut-risk pieces are safe; this set runs 1–2 skill-floored darts per lineup by design — a deliberate cut-survival trade, logged here.
- Sim ROI / Saber Score / sim-dupes columns exist in the pool but were **not** used to rank — selection is edge-fit per repo rules. Pool ownership figures differ slightly from the ETR session projections; per-player own% above are the ETR session values (consistent with the slate analysis).
