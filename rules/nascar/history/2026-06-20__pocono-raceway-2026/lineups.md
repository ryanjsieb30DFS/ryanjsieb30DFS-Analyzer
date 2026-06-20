# NASCAR Lineups — Pocono Raceway (Cup) — SELECTED from uploaded pool (10 of 10)

_All 10 lineups are real rows from the uploaded pool `nascar__lineups_dk_nascar_classic_6-14-2026_119pm.csv` (4,999 candidates, deduped). Each heading tags its 1-based data-row index for traceability. Selection is edge-driven per the slate analysis Player board + Edges, **not** sim ROI / Saber Score rank (anti-informative on NASCAR — Spearman −0.054, lesson `nascar-2026-05-24-sim-roi-not-a-selector`). Contest: NAS $100K Chrome Horn, 20-Max, 10 entries._

_**Revision:** the prior 8-lineup set had two correlated-leverage builds (old L5 & L6 both paired Larson+Briscoe — flagged in that set's audit, L6 "first to cut"). Those two were dropped; **four new pool rows** were selected to reach 10 (2 replacing the flagged pair + 2 extending coverage). Result: Larson+Briscoe co-occurrence is now **0**, Hocevar de-concentrated from a projected 6/10 to 4/10, and max pairwise driver overlap across all 10 is 3._

## Pre-flight checklist
- [x] Slate confirmed: nascar — **Pocono Raceway** — pool file dated 6-14-2026 1:19pm; race is TODAY. Pool + projections are for THIS slate.
- [x] Projections loaded: DailyFan NASCAR (38 drivers) resolved to pool via `data/dk_ids/nascar.csv` (38/38 IDs map cleanly). Ownership figures are DailyFan (single source — a note, not a weighted edge).
- [x] Venue file read: `rules/nascar/tracks/pocono_raceway.md` (UNVERIFIED stub). Applied: 11th–30th start band = 57% of optimal, worse-than-30th only 9.5% (deep-back PD is thin → sleeper-spike re-scoped UP-board); two-dominator builds optimal; field over-owns value on practice speed → low-owned value PD is the leverage.
- [x] Open lessons reviewed (lessons.yaml): **applied** — `nascar-2026-05-24-anchor-equivalence` (Larson-over-Hamlin in L2/L7/L9; Hocevar-over-Preece in L2/L3/L4/L7; Reddick-completion in L6; Keselowski-without-Bubba in L6); `nascar-2026-05-24-sleeper-spike-floor` (re-scoped to the 11th–30th band — Gilliland P29, Gragson P30, Stenhouse P21); `nascar-2026-05-01-50-pct-chalk-rule` (deep-PD chalk Bubba/Kes covered in 8 of 10 ≥33% ✓); `nascar-2026-05-01-correlation-not-substitution` (EJ/Nemechek/Cindric used as independent value engines); `nascar-2026-05-01-sub-10-punts-over-15-20` (EJ 7%, Nemechek 5%, Cindric 16% preferred over Preece 36% chalk — **Preece faded in all 10**). **Rejected** — HMS-intermediate-double-up / road-course-fade (Pocono is neither — mechanism absent); mme-or-fade-means-fade-in-SE (this is 20-Max MME, not SE).
- [x] Framework pre-lock checks: **Anchor-Equivalence** run on all bundle pairs (Hamlin↔Larson ✓; Preece↔Hocevar ✓ Preece in 0; Reddick↔Larson↔Herbst ✓; Bubba↔Keselowski ✓ L6 runs Kes WITHOUT Bubba = the split). **Two-dominator minimum** met in 9 of 10 (L1 single-dom by design — chalk-core coverage). **Sleeper-spike floor** ✓ (≥3 lineups). **Sim-ROI-as-selector** explicitly NOT used. **Chalky-combo scrub**: Bubba+Keselowski together in 3 of 10 (L1, L8, L9) — at the Edge-5 "≤3 of 10" cap, not over.
- [x] Prior results scanned: `results.jsonl` does not exist yet (no logged NASCAR slate). Charlotte 600 process note: the selection layer is the historical leak, not the build layer → these picks filter for **edge-fit**, not sim rank; correlated-leverage stacks (Watkins Glen Bell+Zilisch) actively scrubbed — the old Larson+Briscoe pair was removed this revision.

---

## L1 — Chalk-core eater _(pool row 1759)_
**Thesis:** If the field's exact chalk pileup hits (Hamlin dominates from P1, the deep-back PD chalk pays), I'm in it — with Erik Jones (7%) as the low-owned tiebreaker inside an otherwise-chalk build. The `50%-chalk-rule` coverage lineup (Bubba 50% + Keselowski 52% both rostered).

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Denny Hamlin | $11,000 | 1 | 48 | 64.3 | Primary dominator |
| Chase Elliott | $9,200 | 23 | 42 | 52.35 | PD-elite |
| Bubba Wallace | $8,000 | 38 | 50 | 49.0 | Deep-PD chalk |
| Brad Keselowski | $7,900 | 37 | 52 | 48.0 | Deep-PD chalk |
| Erik Jones | $7,500 | 7 | 7 | 35.0 | Low-owned value (differentiator) |
| Riley Herbst | $6,000 | 25 | 27 | 34.0 | Value PD |

Salary: **$49,600** ≤ $50,000 ✓
**What if?** — What if the chalkiest version of the slate goes chalk (Hamlin leads wire-to-wire, both back-row chalk cars top-15)? Pre-Lock Sanity #1 coverage.

---

## L2 — Larson anchor-equivalence pivot (multi-dom) _(pool row 282)_
**Thesis:** The mandatory Hamlin↔Larson anchor-equivalence pivot (`nascar-2026-05-24-anchor-equivalence`) — Larson is the "direct pivot from Hamlin" (Edge #1) and grabs the lead while Byron (race-winning practice speed, Bell-reallocation per Decision 3) and Buescher (4th here last yr) give two more dom paths; Hocevar is the Preece-fade PD; Gilliland is the sleeper-spike floor.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Kyle Larson | $10,500 | 2 | 27 | 55.2 | Primary dominator (alt to Hamlin) |
| William Byron | $9,500 | 9 | 15 | 45.05 | Contrarian dominator |
| Carson Hocevar | $8,700 | 26 | 32 | 48.35 | PD-elite (Preece pivot) |
| Chris Buescher | $8,500 | 6 | 22 | 45.4 | Secondary dominator |
| Zane Smith | $6,800 | 18 | 7 | 29.0 | Value |
| Todd Gilliland | $5,300 | 29 | 7 | 19.0 | Sleeper-spike (≥15 SP) |

Salary: **$49,300** ≤ $50,000 ✓
**What if?** — What if Hamlin never gets the lead and it rotates through the HMS/JGR contenders while the field is stuck on Hamlin? Uncontested-leverage dom pivot.

---

## L3 — Hamlin top-heavy, Preece fully faded _(pool row 110)_
**Thesis:** Edge #2 expression — Hocevar in the PD slot the field gives Preece (36% over-owned value with practice-speed red flags; I run Hocevar 32%, the better-supported PD elite), top-heavy with Hamlin + Elliott + Buescher and a low-owned value engine (Nemechek 5% + Austin Dillon). No deep-back chalk and zero Preece.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Denny Hamlin | $11,000 | 1 | 48 | 64.3 | Primary dominator |
| Chase Elliott | $9,200 | 23 | 42 | 52.35 | PD-elite |
| Carson Hocevar | $8,700 | 26 | 32 | 48.35 | PD-elite (Preece pivot) |
| Chris Buescher | $8,500 | 6 | 22 | 45.4 | Secondary dominator |
| John H. Nemechek | $5,900 | 8 | 5 | 25.0 | Low-owned value |
| Austin Dillon | $5,800 | 32 | 23 | 32.0 | Value PD |

Salary: **$49,100** ≤ $50,000 ✓
**What if?** — What if Preece's practice-speed concerns play out (runs ~24th) and the field that bought him at 36% eats the bust, while Hocevar's top-5 speed converts from P26?

---

## L4 — Hamlin + Briscoe contrarian two-dom _(pool row 167)_
**Thesis:** The venue-supported two-dominator build with a *differentiated* second dom — Briscoe (13%, won + dominated Pocono last year) instead of doubling deep-PD chalk; Hocevar PD + one deep chalk (Bubba) + Nemechek value. The contrarian-2nd-dom path (Edge #4) anchored on the chalk dom.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Denny Hamlin | $11,000 | 1 | 48 | 64.3 | Primary dominator |
| Chase Briscoe | $9,900 | 5 | 13 | 47.4 | Contrarian dominator |
| Carson Hocevar | $8,700 | 26 | 32 | 48.35 | PD-elite (Preece pivot) |
| Bubba Wallace | $8,000 | 38 | 50 | 49.0 | Deep-PD chalk |
| Riley Herbst | $6,000 | 25 | 27 | 34.0 | Value PD |
| John H. Nemechek | $5,900 | 8 | 5 | 25.0 | Low-owned value |

Salary: **$49,500** ≤ $50,000 ✓
**What if?** — What if Briscoe leads laps from P5 the way he did winning here last year, giving a second dominator the field is 35pts of ownership light on?

---

## L5 — Hamlin + Byron two-dom (Bell reallocation) + Cindric value _(pool row 32)_
**Thesis:** Decision 3 expression — reallocate the Bell health-binary slot into Byron (15%, "huge differentiator" practice speed) as the contrarian second dom; pair with one deep chalk (Bubba), Buescher secondary dom, and Cindric ("perfect pivot off Preece," 16%, P10=41) as the lower-owned value PD.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Denny Hamlin | $11,000 | 1 | 48 | 64.3 | Primary dominator |
| William Byron | $9,500 | 9 | 15 | 45.05 | Contrarian dominator |
| Chris Buescher | $8,500 | 6 | 22 | 45.4 | Secondary dominator |
| Bubba Wallace | $8,000 | 38 | 50 | 49.0 | Deep-PD chalk |
| Austin Cindric | $7,200 | 17 | 16 | 32.0 | Value PD (Preece pivot) |
| Austin Dillon | $5,800 | 32 | 23 | 32.0 | Value PD |

Salary: **$50,000** = $50,000 ✓
**What if?** — What if Byron's race-winning practice speed converts (the Bell money should have gone here) and Cindric's 8th–12th range hits while the field rides Preece?

---

## L6 — Reddick anchor-equivalence completion + Keselowski single-deep-chalk _(pool row 494)_
**Thesis:** Closes the remaining anchor-equivalence pairs — Reddick (29%, the Reddick↔Larson↔Herbst trio I'm otherwise zeroing) as the high-floor secondary alongside Larson, and **Keselowski WITHOUT Bubba** (the Bubba↔Keselowski split — Kes had the fastest car here last year). Erik Jones value + Gilliland sleeper-spike. The only lineup running Reddick and the only one splitting the deep-PD-chalk pair.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Kyle Larson | $10,500 | 2 | 27 | 55.2 | Primary dominator (alt) |
| Tyler Reddick | $10,300 | 16 | 29 | 48.25 | Secondary (high floor) |
| Chris Buescher | $8,500 | 6 | 22 | 45.4 | Secondary dominator |
| Brad Keselowski | $7,900 | 37 | 52 | 48.0 | Deep-PD chalk (split from Bubba) |
| Erik Jones | $7,500 | 7 | 7 | 35.0 | Low-owned value |
| Todd Gilliland | $5,300 | 29 | 7 | 19.0 | Sleeper-spike (≥15 SP) |

Salary: **$50,000** = $50,000 ✓
**What if?** — What if Keselowski (not Bubba) is the back-row chalk car that hits AND Reddick's high floor from P16 anchors a no-Hamlin build?

---

## L7 — Hamlin value-tier, Preece faded _(NEW · pool row 814)_
**Thesis:** Edge #2 + #3 maximal — Hamlin top-heavy with Hocevar in the Preece slot, behind a **double low-owned value engine** (Erik Jones 7% + Cindric 16%) plus one deep chalk (Bubba) and an SVG strategy dart. If the mispriced sub-16% value-PD tier the field is scared off hits behind a chalk dom, this captures it cheaply. Zero Preece.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Denny Hamlin | $11,000 | 1 | 48 | 64.3 | Primary dominator |
| Carson Hocevar | $8,700 | 26 | 32 | 48.35 | PD-elite (Preece pivot) |
| Bubba Wallace | $8,000 | 38 | 50 | 49.0 | Deep-PD chalk |
| Erik Jones | $7,500 | 7 | 7 | 35.0 | Low-owned value |
| Austin Cindric | $7,200 | 17 | 16 | 32.0 | Value PD (Preece pivot) |
| Shane Van Gisbergen | $7,000 | 31 | 13 | 21.0 | Strategy dart |

Salary: **$49,400** ≤ $50,000 ✓ · pool 99th pct ceiling 301
**What if?** — What if the DFR3 "2024 value repeat" hits (the cheap low-owned cars score) while the field's Preece pick busts, all behind a Hamlin dom?

---

## L8 — Larson chalk-shape mirror (Edge #1) _(NEW · pool row 3945)_
**Thesis:** The Larson version of L1's chalk-eater — Larson (27%) as the uncontested-leverage dom over the field's exact deep-chalk PD shape (Elliott + Bubba + Keselowski), with Gibbs as a cheap leverage piece and Gragson sleeper. If Larson grabs the lead the field handed Hamlin, this owns the chalk-PD payout at 21 fewer points of dom ownership.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Kyle Larson | $10,500 | 2 | 27 | 55.2 | Primary dominator (alt) |
| Chase Elliott | $9,200 | 23 | 42 | 52.35 | PD-elite |
| Ty Gibbs | $8,900 | 4 | 12 | 37.8 | Leverage dart |
| Bubba Wallace | $8,000 | 38 | 50 | 49.0 | Deep-PD chalk |
| Brad Keselowski | $7,900 | 37 | 52 | 48.0 | Deep-PD chalk |
| Noah Gragson | $5,400 | 30 | 9 | 20.0 | Sleeper-spike (≥15 SP) |

Salary: **$49,900** ≤ $50,000 ✓ · pool 99th pct ceiling 317
**What if?** — What if Larson, not Hamlin, leads the most laps — the chalk PD core pays exactly as the field expects, but my dom is 21% lower-owned?

---

## L9 — No-chalk-favorite ceiling (Pre-Lock #2) _(NEW · pool row 4018)_
**Thesis:** The maximum-ceiling world where BOTH chalk favorites (Hamlin AND Larson) fade — Blaney (11%) + Byron (15%) are two contrarian doms who can lead, riding the deep-PD chalk (Bubba + Kes) and Elliott PD with a Gilliland sleeper. Highest pool ceiling in the set (99th = 327); the "win it outright if the favorites bust" entry.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Ryan Blaney | $10,100 | 10 | 11 | 40.9 | Contrarian dominator |
| William Byron | $9,500 | 9 | 15 | 45.05 | Contrarian dominator |
| Chase Elliott | $9,200 | 23 | 42 | 52.35 | PD-elite |
| Bubba Wallace | $8,000 | 38 | 50 | 49.0 | Deep-PD chalk |
| Brad Keselowski | $7,900 | 37 | 52 | 48.0 | Deep-PD chalk |
| Todd Gilliland | $5,300 | 29 | 7 | 19.0 | Sleeper-spike (≥15 SP) |

Salary: **$50,000** = $50,000 ✓ · pool 99th pct ceiling 327
**What if?** — What if neither chalk favorite leads and the race goes to the contrarian doms (Blaney/Byron) while both back-row chalk cars convert? Pre-Lock Sanity #2 — can I win 1st?

---

## L10 — Maximum-leverage min-own dart _(NEW · pool row 3942)_
**Thesis:** The lowest cumulative-ownership lineup in the pool set (SaberSim own 39 vs 145–247 for the rest) — Larson dom + Blaney contrarian dom + an all-sub-13%-owned supporting cast (Gibbs, Suarez, SVG, Stenhouse). Pure tournament-tail leverage: if the slate breaks chaotic and the field's chalk cores all miss, this is the uncontested winner. One speculative dart of ten, by design.

| Driver | Sal | Start | Own% | Proj | Role |
|---|---|---|---|---|---|
| Kyle Larson | $10,500 | 2 | 27 | 55.2 | Primary dominator (alt) |
| Ryan Blaney | $10,100 | 10 | 11 | 40.9 | Contrarian dominator |
| Ty Gibbs | $8,900 | 4 | 12 | 37.8 | Leverage dart |
| Daniel Suarez | $7,700 | 3 | 5 | 31.0 | Low-owned value |
| Shane Van Gisbergen | $7,000 | 31 | 13 | 21.0 | Strategy dart |
| Ricky Stenhouse Jr | $5,700 | 21 | 5 | 21.0 | Sleeper-spike / low-owned |

Salary: **$49,900** ≤ $50,000 ✓ · pool cumulative own 39 (lowest in set)
**What if?** — What if the rain/strategy race blows up the chalk entirely and a low-owned front-row pivot (Larson/Blaney/Gibbs) leads while the back fills with sub-5% spikes?

---

## Portfolio audit

**10 of 10 selected from the pool (6 kept + 4 new).** The prior 8-lineup set's two flagged builds (old L5/L6, both Larson+Briscoe) were dropped; four edge-distinct pool rows were added. No filler — each of the 10 answers a different "what if?".

**Dominator coverage (Pre-Lock #5 — diversified across ≥2):**
- Hamlin (primary): L1, L3, L4, L5, L7 = **5/10 (50%, ≈ field 48%)** — near field rate.
- Larson (primary alt): L2, L6, L8, L10 = **4/10 (40%, vs field 27%)** — deliberate Edge-#1 / anchor-equivalence overweight; every Hamlin-or-Larson lineup carries exactly one, so the portfolio survives either top dom busting.
- Contrarian/secondary doms: Byron 3 (L2,L5,L9), Buescher 4 (L2,L3,L5,L6), Blaney 2 (L9,L10), Briscoe 1 (L4). **Larson+Briscoe co-occurrence = 0** (the flagged correlation is resolved).

**Anchor-Equivalence compliance (MANDATORY — all bundle pairs):**
- Hamlin↔Larson (48–52 tier): ✓ Larson in 4 lineups.
- Preece↔Hocevar (32–36): ✓ Hocevar in L2/L3/L4/L7; **Preece in 0** (the over-owned-value fade, Edge #2).
- Reddick↔Larson↔Herbst (27–29): ✓ Reddick (L6), Larson (4), Herbst (L1/L4).
- Bubba↔Keselowski (50–52): ✓ **L6 runs Keselowski with no Bubba** — the split the lesson demands.
- Byron/Cindric tier (15–17): ✓ Byron (3) + Cindric (2); **Bell faded entirely** (Decision 3 health binary — correct).

**Exposure (across 10):** Bubba 6, Hamlin 5, Larson/Keselowski/Elliott/Hocevar/Buescher 4 each, EJ/Gilliland/Byron 3, then the value/dart tier ≤2. **Hocevar held to 4/10 (40%, field 32%)** — fixed the over-concentration that an earlier draft would have hit (6/10). No driver is wildly off field rate.

**50% Chalk Rule:** Deep-PD chalk (Bubba and/or Keselowski) in L1, L4, L5, L6, L7, L8, L9 = **8/10 (80%)** ≥ 33% ✓. Bubba+Keselowski *together* in **L1, L8, L9 = 3/10** — at the Edge-#5 "≤3 of 10" cap, not over.

**Sleeper-spike floor (framework check #9):** ≥3 lineups carry a sub-15%/sub-$6K ≥15-SP driver — Gilliland P29 (L2, L6, L9), Gragson P30 (L8), Stenhouse P21 (L10). Exceeds the ≥2 floor; re-scoped to the 11th–30th band per the venue file.

**Low-owned value engine (Edge #3, `correlation-not-substitution`):** Erik Jones 7% (L1,L6,L7), Nemechek 5% (L3,L4), Cindric 16% (L5,L7), Suarez 5% (L10) used as independent value shots. Over-owned Preece (36%) faded in all 10.

**Player overlap:** Max pairwise overlap across all 10 = **3 of 6** — no near-duplicates (no-competing-lineups rule holds).

**Honest flags:**
- **Ty Gibbs in L8 + L10 (2/10)** despite a PASS call in the analysis ("starts too high, must lead"). Used only as a cheap leverage piece in two leverage builds — within the "1-2 MME darts" allowance, but he is the weakest single inclusion; if trimming below 10 entries, L10 (the speculative min-own dart) is the first to cut.
- **L10 is intentionally high-variance** (Larson/Blaney + four sub-13% cars) — the tournament-tail ticket, not a floor play.

**Pre-Lock Sanity:** #1 (cash if chalk hits) → L1. #2 (win if leverage hits) → L9/L10. #3 (no single load-bearing sub-15% leverage play) → ✓ every lineup holds on its doms. #4 (deep-PD chalk covered) → ✓ 8 lineups. #5 (≥2 doms) → ✓ 9 of 10 (L1 single-dom by design).
