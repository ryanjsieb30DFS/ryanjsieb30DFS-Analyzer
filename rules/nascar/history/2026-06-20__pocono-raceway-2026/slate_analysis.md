# NASCAR Slate Analysis — Pocono Raceway (Cup)

## Pre-flight checklist
- [x] Slate confirmed: nascar — **Pocono Raceway** — bundle generated 2026-06-14 11:35; all four article PDFs dated 6.14.26; race is TODAY (moved to 1:00pm ET on rain threat). Data is for this slate.
- [x] Projections loaded: DailyFan NASCAR (38 drivers); session/bundle ownership is for THIS slate. Single source — cross-vendor disagreement table is empty by construction.
- [x] Venue file: **created `rules/nascar/tracks/pocono_raceway.md` — marked UNVERIFIED** (no prior in-repo Pocono slate; built from this slate's DDD + DailyFan tables). Confirm against a 2nd source post-autopsy.
- [x] Open lessons reviewed (lessons.yaml): **applied** — anchor-equivalence (Decision 4: Hamlin↔Larson, Bubba↔Keselowski); sleeper-spike-floor (scoped DOWN — see Decision 2, Pocono's worse-than-30th bucket is only 9.5% of optimal, NOT a chaotic-1.5-mile carnage track); sub-10-punts-over-15-20 (Erik Jones 7% / Nemechek 5% over Preece 36%, floors+endorsement match per DFR3); mme-or-fade-means-fade-in-SE (Logano/McDowell/AJ flagged — but this is 20-Max MME, so they're 1-2-lineup darts not auto-outs); sim-roi-not-a-selector (the SaberSim top-Proj-Score rows are 115–182% cumulative own — informational only). **Rejected** — backup-car-not-auto-fade is invoked *for* Bubba (P38 backup car, still core), not against; HMS-intermediate-double-up does NOT transfer (Pocono is not an intermediate — mechanism absent).
- [x] Framework pre-lock checks: Anchor-Equivalence run (Decision 4). Two-dominator-path minimum confirmed by venue history. Sleeper-spike floor re-scoped for Pocono. Sim-ROI-as-selector explicitly rejected.
- [x] Prior results scanned: `results.jsonl` does not exist yet (no logged NASCAR slate in ledger); last archived process notes are Charlotte 600 (anchor-equivalence + sleeper-spike births). No vendor_calibration.jsonl inlined — DailyFan own is the only source, treated as a note, not a weighted edge.

---

## Slate at a glance
| Fact | Detail |
|---|---|
| Track | Pocono Raceway — 2.5-mi triangle, ~160 laps, track-position + horsepower track |
| Field set by | Qualifying (real grid; pit strategy can flip it) |
| Weather | **Rain threat — race moved to 1pm.** Halfway/shortened finish live → compresses dominator pts, amplifies strategy/track-position variance |
| Dom structure | **Two-dominator builds historically optimal** (≥2 top-10 starters in 9 of last 11 perfect lineups); single-dom only if an elite PD play out-scores a $11k dom |
| Optimal start band | 11th–30th = **57%** of optimal spots; worse-than-30th = only **9.5%** |
| Contest | NAS $100K Chrome Horn ($20K to 1st) — **20-Max**, field 29,726, **10 entries** |
| Chalk pileup | Top-5 own = 228% → Keselowski 52, Bubba 50, Hamlin 48, Elliott 42, Preece 36 |

This is a **20-Max MME** build (10 distinct lineups), not single entry — the portfolio can absorb 1-2-lineup variance darts the SE rules forbid. The whole field is funneling into one core: **Hamlin (dom) + Bubba/Keselowski (deep-back PD) + Elliott + Preece**. Edge lives in pivoting the dominator (Larson), upgrading the PD-elite slot (Hocevar over Preece), and mining the low-owned value-PD tier the field is mispricing on practice speed.

---

## The 4 decisions that define this slate

### 1. The dominator slot: Hamlin is core — but how many laps does a 160-lap race give him?
**PLAY (Hamlin) — every lineup needs ≥1 dom, and he's the best car at his best track.** Mechanism: two-dom track, Hamlin P1 with elite speed; "eat the chalk." But it's only a 160-lap race with live pit-cycle/rain strategy — his laps-led ceiling is capped, and Larson can grab the initial lead.
- **If played →** Hamlin $11,000 leaves **$39,000 for 5 ($7,800/slot)**. Pair with ONE PD-elite (Hocevar/Elliott) + one deep-PD chalk (Bubba or Kes) + value. Do **not** pair two $9.9k+ doms with him — 2025 showed two doms at this price is hard to make optimal (Hamlin+Briscoe both dominated last year and Hamlin still wasn't optimal). Single strong dom + PD is the shape.
- **If faded →** you're betting the rain/strategy world where the lead rotates and a pure dom never materializes — real, but you're fading 48% off his best track. Price it: a Hamlin-out lineup needs a contrarian dom (Briscoe/Byron) to actually dominate, which Dustin calls "rather random."

### 2. The deep-back PD chalk: Bubba P38 (50%) + Keselowski P37 (52%) — ride or trim?
**PLAY both, but know you're buying the 9.5% bucket at 50%+ own.** Mechanism: backup-car-not-auto-fade (Bubba) + 50%-Chalk Rule — these are good cars that qualified deep; Bubba needs P18 for 45 pts, top-15 clears 50; Keselowski had the fastest car here last year. The PD math is real.
- **If played →** Bubba $8,000 + Keselowski $7,900 = **$15,900 for two slots**; stacked with Hamlin that's $26,900 for 3, leaving $23,100 for 3 (the field's Elliott+Preece+Herbst finish). **Cap it at ~33% portfolio on running BOTH together** — Pocono's worse-than-30th bucket is only 9.5% of optimal, so a lineup leaning on two P37+ starters is doubling into the thinnest historical path. At least a few of 10 lineups should run **one** deep-PD chalk, not both.
- **If faded (one of them) →** the alternative is a mid-pack PD elite who needs less to pay off: Hocevar P26 or Elliott P23 finishing top-10 beats a P37 car finishing 16th. **This is the sleeper-spike-floor lesson, re-scoped:** at Charlotte the rule demanded sub-15%/sub-$6K deep darts; Pocono's history says deep raw-PD ceilings are *thin* (best worse-than-30th NextGen finish = Haley 22nd/32). So the "floor" play here is the **11th–30th PD band**, not the back row.

### 3. Christopher Bell P22 (17%) — the binary the field is underpricing
**PASS / heavy underweight.** Mechanism: Bell has a **fractured wrist, driving one-handed**, AND Brandon Jones is on relief-driver standby — if Jones takes the car it finishes ~28th. Dustin explicitly "wants to be light." A JGR car starting 22nd is a tempting top-10/PD play, but 17% field own treats it as a normal mid-PD piece, not the coin-flip it is.
- **If played anyway (1-2 MME darts max) →** treat it as pure variance, never a core; pair with a high-floor dom + value, and accept the ~28th-place relief-driver outcome as a live KILL on that lineup. It is not a lineup you build the portfolio around.
- **If faded →** reallocate the 17%/$9,700 into a **contrarian dominator** with an independent positive case — **Byron $9,500 (15%, race-winning practice speed, "huge differentiator")** or **Briscoe $9,900 (13%, won + dominated here last year)**. That's the same salary slot expressing a real win path instead of a health binary.

### 4. Anchor-Equivalence (MANDATORY): the field's dominator and PD-chalk are both coin flips it's already mispriced
**MIX — at least one lineup must run each alternative.** Two equivalence pairs matter:
- **Dominator: Hamlin (48%) ↔ Larson (27%).** Dustin frames Larson as "the direct pivot from Hamlin" — best 10-lap practice avg, HMS close to JGR this week, can grab the initial lead. Same dom profile at **21 fewer points of ownership.** **≥1 lineup MUST anchor Larson over Hamlin.**
  - If played → Larson $10,500 leaves $39,500/5; build the *same* PD shape around him so the only swing variable is which HMS/JGR car dominates — uncontested leverage if Larson leads.
- **Deep-PD chalk: Bubba (50%) ↔ Keselowski (52%).** Field plays both; the leverage alternative is **Hocevar P26 (32%)** — a mid-PD elite (legit top-5 speed, 5th at Michigan last week, 2nd in 5-lap practice) needing less than a P37 car to hit. **≥1 lineup should run Hocevar in place of one deep-PD chalk.**

---

## Player board
Covers the full chalk tier + every named leverage/value-PD play + the traps. Sport columns: Start / Dom-or-PD role. Ownership is DailyFan (single source — a note, not a weighted edge).

| Driver | Sal | Start | Proj | Own% | Role | Call | If played → |
|---|---|---|---|---|---|---|---|
| Denny Hamlin | $11.0K | 1 | 64.3 | 48 | Primary dom | **PLAY** | Core dom; $39K/5 after. ONE dom per lineup, not two $9.9k+ |
| Kyle Larson | $10.5K | 2 | 55.2 | 27 | Primary dom (alt) | **PLAY** | Anchor-Equivalence pivot off Hamlin in ≥1; same PD shape around him |
| Tyler Reddick | $10.3K | 16 | 48.25 | 29 | Secondary | **MIX** | High floor, no dom equity, "not a great track for him" — under field; only as a 2nd top-5 piece |
| Ryan Blaney | $10.1K | 10 | 40.9 | 11 | Contrarian dom | **MIX** | Must-dominate, team lost speed — 1-lineup dart only, never a floor piece |
| Chase Briscoe | $9.9K | 5 | 47.4 | 13 | Contrarian dom | **PLAY** | Won+dominated here last yr, JGR class of field; the differentiated 2nd-dom path. Pure dom — needs to lead |
| Christopher Bell | $9.7K | 22 | 35.0 | 17 | PD (injured) | **PASS** | One-handed + relief-driver risk; 1-2 MME darts max, never core |
| William Byron | $9.5K | 9 | 45.05 | 15 | Contrarian dom | **PLAY** | Race-winning practice speed, "huge differentiator" pivot off Elliott chalk |
| Chase Elliott | $9.2K | 23 | 52.35 | 42 | PD-elite core | **PLAY** | Top-10 upside from 23rd at $9.2k — the easy PD-elite; pairs with any dom |
| Ty Gibbs | $8.9K | 4 | 37.8 | 12 | Contrarian dom | **PASS** | Starts too high, must lead to score; "bet against" — skip on DK |
| Carson Hocevar | $8.7K | 26 | 48.35 | 32 | PD-elite (lev) | **PLAY** | The Hocevar>Preece edge: top-5 speed, 5th Michigan, 2nd practice; starts rear after repairs, ELITE PD upside |
| Chris Buescher | $8.5K | 6 | 45.4 | 22 | Secondary dom | **MIX** | Electric here (4th last yr, 19 fast laps, 1st 5-lap); ~46pts at P4 — fine 2nd dom in Hamlin-salary builds |
| Joey Logano | $8.3K | 11 | 35.0 | 10 | — | **PASS** | "MME or fade," starts too high; if anyway: 1-lineup dart only |
| Ross Chastain | $8.1K | 24 | 35.0 | 17 | PD (lev) | **MIX** | Hasn't finished better than 16th on a standard oval all yr; restart/strategy dart, not a core |
| Bubba Wallace | $8.0K | 38 | 49.0 | 50 | Deep-PD chalk | **PLAY** | Core PD; backup-car-not-fade. Cap running w/ Keselowski both to ~33% of lineups |
| Brad Keselowski | $7.9K | 37 | 48.0 | 52 | Deep-PD chalk | **PLAY** | Core PD; fastest car here last yr. Equivalence-pair w/ Bubba — don't double blindly |
| Daniel Suarez | $7.7K | 3 | 31.0 | 5 | — | **PASS** | Needs top-5 from P3 to pay off; "low% play" — Erik Jones is the better value |
| Erik Jones | $7.5K | 7 | 35.0 | 7 | Value PD (lev) | **PLAY** | The DFR3 "Erik Jones 2024" repeat (8%/38pts then); top-6 car, 2nd at Michigan, 3rd 10-lap practice. P6=39 |
| Alex Bowman | $7.3K | 12 | 21.0 | 6 | — | **PASS** | "Checked out," no speed — MME dart at best |
| Austin Cindric | $7.2K | 17 | 32.0 | 16 | Value PD (lev) | **PLAY** | "Perfect pivot off Preece," 8th–12th range, P10=41 — lower-owned value PD |
| Shane Van Gisbergen | $7.0K | 31 | 21.0 | 13 | Strategy dart | **MIX** | Strategy-only 40pt path; deep-PD bucket is thin here — 1-2 lineups |
| Ryan Preece | $6.9K | 35 | 40.0 | 36 | Deep-PD chalk | **MIX** | **Over-owned value PD** (practice-speed concerns, could run 24th). The fade target — pivot to Hocevar/Cindric/Erik Jones |
| Zane Smith | $6.8K | 18 | 29.0 | 7 | — | **PASS** | "Bad floor and ceiling," MME dart only |
| Josh Berry | $6.6K | 20 | 20.0 | 5 | — | **PASS** | "25th-place guy starting 20th" — no |
| Connor Zilisch | $6.5K | 28 | 28.0 | 9 | PD dart | **MIX** | Start-and-park concern (dead last in 3 races); pivot off Herbst/Preece, 1-lineup dart |
| Michael McDowell | $6.3K | 13 | 24.0 | 4 | — | **PASS** | Starts too high, needs top-10 — "MME or fade" |
| Riley Herbst | $6.0K | 25 | 34.0 | 27 | Value PD chalk | **PLAY** | Clear best value: ultra-fast Toyota, P15=38, floor ~20th/28. The chalk value-PD anchor |
| John H. Nemechek | $5.9K | 8 | 25.0 | 5 | Value PD (lev) | **PLAY** | "1000% a legit top-10 threat," 5th 10-lap practice, P10=32 — field scared off. Leverage to Herbst |
| Austin Dillon | $5.8K | 32 | 32.0 | 23 | Value PD chalk | **PLAY** | "Clearest PD play"; ~20th standard race, P18=39/P22=30. Split own with Herbst |
| Ricky Stenhouse Jr | $5.7K | 21 | 21.0 | 5 | PD dart | **MIX** | Random top-15 on a speed oval, P17=30 — small MME exposure |
| Noah Gragson | $5.4K | 30 | 20.0 | 9 | Strategy dart | **MIX** | Strategy/caution-flip dart; "get randomly lucky" |
| Todd Gilliland | $5.3K | 29 | 19.0 | 7 | Strategy dart | **MIX** | Same as Gragson — 1-lineup dart |
| Ty Dillon / Dye / Ware / Mears | $5.0–4.5K | 27–36 | 11–15 | 1–4 | Punts | **PASS** | "Slowest of the slow on a pure-speed track" — only if salary forces it |

_Left off: the remaining sub-$5.5K back-markers (Custer, Hill) — both "fade," start too high or no floor, and Pocono's 9.5% worse-than-30th optimal rate doesn't reward bottom-of-board darts the way a carnage track would._

---

## Where I disagree with the vendors
Single source (DailyFan/Dustin), so these are field-ownership and sim disagreements, not cross-vendor. No vendor_calibration.jsonl yet → DailyFan own is a note, not a weight (small-sample guard fully applies).

- **Preece at 36% own → I trim him toward field-low and pivot the slot.** The field is buying a deep-PD value play on perceived PD equity, but Dustin's own write-up flags "fundamental issues with this car in practice… could finish 24th," and DFR3 documents the exact failure mode: 2024's highest-owned value plays (Gilliland 27%, Stenhouse 21%, McDowell 20%) all busted while the low-owned value tier (Erik Jones 8%, Lajoie 11%) scored. Preece is this slate's Gilliland. **Expression: Hocevar (32%, better-supported PD) or Cindric/Erik Jones (lower-owned) in the slot Preece occupies in field cores.**
- **The 17% on Bell is too high for a one-handed driver with a relief-driver standby.** I agree with Dustin ("want to be light") but disagree with the *field* — 17% prices Bell as a normal PD piece, not the health binary he is. Underweight hard; reallocate to Byron/Briscoe contrarian doms.
- **The SaberSim top-Proj-Score rows are not a selection signal.** The pool's highest Proj-Score / Saber-Score lineups carry **115–182% cumulative ownership** (chalk-on-chalk stacks of Hamlin+Bubba+Keselowski+Elliott). Per the Charlotte 600 lesson (sim ROI Spearman −0.054 vs actual), I am NOT selecting by sim rank — these rows confirm where the field is concentrated, which is the thing to leverage AGAINST, not copy.
- **Reddick at 29%/$10.3k is rich for a no-dom-equity car.** Dustin: "not a great track for Reddick… high floor type of play" without Hamlin/Larson's ceiling. At $10.3k with no laps-led path, he's a worse use of salary than Briscoe/Byron as a 2nd dom. Under field.

---

## Edges to exploit
Ranked, each with its concrete hand-build expression.

1. **Larson over Hamlin (Anchor-Equivalence, uncontested dom leverage).** Same dominator profile at 27% vs 48%. _Expression:_ Build a Larson-anchored lineup with the identical PD shape (Larson $10.5K + Elliott $9.2K + Bubba $8.0K + Cindric $7.2K + Herbst $6.0K + Nemechek $5.9K = ~$46.8K, room to upgrade a value slot) — the only swing is which HMS/JGR car leads.
2. **Hocevar in place of Preece in the PD slot.** Better-supported PD elite (top-5 speed, 5th Michigan, 2nd practice) at 32% beats an over-owned 36% value play with practice-speed red flags. _Expression:_ Hamlin $11.0K + Hocevar $8.7K + Bubba $8.0K + Herbst $6.0K + Erik Jones $7.5K + Nemechek $5.9K = $47.1K — a top-heavy dom/PD build that fades the Preece chalk entirely.
3. **The low-owned value-PD tier (the DFR3 repeat).** Erik Jones 7%, Nemechek 5%, Cindric 16% are this slate's "Erik Jones 2024" (8%/38). _Expression:_ Use one as the value engine in 4–5 lineups instead of Preece/Herbst chalk; Erik Jones P7 + a few fast laps clears 40 and is barely owned.
4. **Contrarian 2nd dominator instead of doubling deep-PD chalk.** Byron (15%, race-winning practice speed) or Briscoe (13%, won here last year) give an independent dom path. _Expression:_ Larson $10.5K + Briscoe $9.9K (two-dom build, venue-supported) + Elliott $9.2K + Herbst $6.0K + Nemechek $5.9K + a $4.5–5.0K punt to fit — a differentiated two-dom shape the chalk cores miss.
5. **Don't double Bubba + Keselowski in more than ~3 of 10.** Two P37+ starters in one lineup leans into Pocono's 9.5% worse-than-30th bucket. _Expression:_ In most lineups run ONE deep-PD chalk + one mid-PD elite (Hocevar/Elliott/Chastain) rather than both back-row cars — captures PD upside without betting the thinnest historical path twice.
