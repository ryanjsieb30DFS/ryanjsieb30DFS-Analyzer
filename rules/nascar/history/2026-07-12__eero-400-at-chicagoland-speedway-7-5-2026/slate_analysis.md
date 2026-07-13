# NASCAR Slate Strategy — Chicagoland Speedway (2026-07-05)

## Pre-flight checklist
- [x] Slate confirmed: nascar — **Chicagoland Speedway** (Joliet, IL), first Cup race here since 2019, NextGen car has never raced here. Bundle generated 2026-07-05 13:12; all 3 `articles/nascar/` files dated 2026-07-05 → current slate, not stale.
- [x] **Files read: 3 of 3** — `DDD 7.5.26.pdf` (24pp, Dustin's Deep Dive: track profile + full driver-by-driver, read all 24 pages), `DFR Image 1 7.5.26.pdf` (2026 intermediate optimal-lineup reference table), `DFR Image 2 7.5.26.pdf` (starting-position → top-10 DK / optimal distribution table). **No file was unreadable or skipped.** Plus the DailyFan projection table (38 players) in the bundle.
- [x] Venue file: none existed → **created `rules/nascar/tracks/chicagoland_speedway.md` as a stub, marked UNVERIFIED** (built from this slate's article + DFR intermediate tables; NextGen has never raced here, so all track reads are extrapolation from comparable intermediates — Kansas/Vegas banking, Darlington/Homestead tire wear).
- [x] Open lessons reviewed (7 open; codified ones live in framework):
  - APPLIED `midpack-pd-over-deep-back-chalk` (hyp) → Leverage & Fades + Decision 3: the P11–30 band is the "bread is butter" tier here (~55% of intermediate optimal spots).
  - APPLIED `anchor-equivalence-not-parity` (validated) → Decision 1: run Bell as the alt, size for leverage, NOT a 50/50 Reddick hedge.
  - APPLIED `carry-a-sub5-leverage-dart-mme` (hyp) → Leverage: Herbst 4% / Zane 5% / Nemechek 5% as the MME sub-5% darts (single-entry caution noted).
  - APPLIED `portfolio-gaps-addressed-pre-lock` (hyp) → named the mid-pack-PD gap + sub-5% gap and addressed both.
  - APPLIED (spirit, w/ caveat) `roadcourse-deepback-revives-on-strategy` (hyp) → mechanism is road-course-born (caution/fuel compression); the intermediate analog here is high-tire-wear **off-cycle pitting** → treat deep-back band (Heim P28, McDowell P38, Logano P31) as live, don't fade deep-back chalk purely on base rate.
  - REJECTED `ownership-shift-full-reevaluation` (hyp) → mechanism absent: only one vendor ownership snapshot loaded, no shift to react to.
  - REJECTED `injury-narrative-not-a-fade-thesis` (hyp) → mechanism absent: no injury narrative on this slate (Bell healthy; his Texas wrist is old news).
- [x] Framework pre-lock checks: Anchor-Equivalence → Reddick 39% vs Bell 24% (also Larson 30%), equivalent Toyota dominators — run Bell (Decision 1). Two-dominator-paths rule → Hamlin + a Bell/Larson/Briscoe second path. HMS-intermediate double-up → available (Byron+Elliott) but demoted, article says Toyota > HMS on this track type in 2026. "MME or fade" → Bowman, Zilisch = fade in single entry.
- [x] Prior autopsy notes scanned: `results.jsonl` last 2 slates — Pocono (25,260 field, best 4.0%), Sonoma (best rank 9, 0.3%, SVG+Gibbs+Zilisch). Mid-pack-PD + carry-a-leverage-dart themes recur; leverage_capture 1.0 both slates.
- [x] Sharp envelope noted: NASCAR is the user's **weakest sport** (sub-5% leverage in only 19% of lineups vs 59% in PGA). Target ≥1 sub-5% leverage piece in most lineups, elite anchor (Hamlin) + downstream differentiation, all-unique, judged on ceiling. Sharp-playbook names SVG / Custer / Berry / Stenhouse / Zilisch as the NASCAR value-tier scorers this account habitually skips — all live here.

## Slate at a glance
| Item | Detail |
|---|---|
| Track | Chicagoland Speedway — 1.52mi tri-oval intermediate, 18° banking, D-shaped |
| Defining trait | High tire wear / degradation → off-cycle pitting, "comers and goers," fast laps spread through field |
| NextGen history | **None** — never raced here in this car; extrapolate from Kansas/Vegas + Darlington/Homestead |
| Pole / front row | Hamlin P1, Larson P2, Buescher P3, Keselowski P4, Gibbs P5, Bell P6 |
| Top org | JGR / 23XI Toyota — all 6 intermediate optimals in 2026 rostered multiple Toyotas |
| PD sweet spot | P11–30 band = ~55% of intermediate optimal spots; worse-than-30th ~8% (thin) |
| Highest owned | Hamlin 55%, Heim 45%, Reddick 39% (DailyFan) |
| Weather | Not provided in articles — N/A |
| Contests | **None declared** → default to large-field GPP, maximum-differentiation posture |

## Top plays
**Core dominators**
- **Denny Hamlin** — $11,000, P1, **55% own (DailyFan; DDD expects ~50%, could balloon high-50s)**. #1 dominator on the slate per both sources; unstoppable on high-speed ovals this year, tested here in April. The one chalk you ride, not fade.
- **Christopher Bell** — $10,000, P6, **24% own, 58.0 proj (DailyFan — highest projection on the board after Hamlin)**. DDD's #2 dominator and "one of my top plays" (FD GPP Fav); 2nd at Nashville & Charlotte with 61/44 fast laps. The projection AND the article both say he outranks Reddick, yet the field owns Reddick 15pts more — the leverage dominator.

**Secondary dominators / pivots**
- **Kyle Larson** — $10,500, P2, **30% own, 54.5 proj (DailyFan)**. Tested here in April, top-5 all intermediates; DDD calls him a "really good dominator play" but questions whether he can beat Toyota long-run speed. Secondary path.
- **Chase Briscoe** — $9,900, P7, **14% own, 46.85 proj (DailyFan)**. JGR race-winning upside; DDD says the $9.9k tag forces him to be a top dominator (pure pivot off Bell/Hamlin) but he's under-owned for that ceiling.

**Mid-pack PD core (the "bread is butter" tier — P11–30)**
- **Corey Heim** — $7,500, P28, **45% own, 45.25 proj (DailyFan)**. DDD "No brainer" CORE; qualified early, moves forward, strong floor+ceiling. Massive chalk — the deep-back PD everyone has.
- **Erik Jones** — $7,200, P22, **24% own, 36.8 proj (DailyFan)**. DDD raves — "so good" on this track type, 13th/11th/2nd/6th run at Charlotte/Nashville/Michigan/Pocono. Only needs ~13th for 40 pts.
- **Austin Cindric** — $7,000, P23, **27% own, 36.0 proj (DailyFan)**. 2nd in 10-lap practice average; 5th Darlington, 12th Kansas, 11th Michigan — enough results to hit ~40 from P23.

**Darts / salary savers**
- **Josh Berry** — $5,500, P34, **16% own, 28.0 proj (DailyFan)**. DDD's favorite value play — price + upside, top-25 gets ~30 pts. Deep PD.
- **Ryan Preece** — $6,700, P20, **17% own, 37.0 proj (DailyFan)**. Better racer than qualifier; RFK speed (BK/Buescher top-5 quali) implies Preece has pace; 13th = ~37 pts.

## How to approach the slate
Two-dominator structure, always: **Hamlin is the near-mandatory anchor** (elite car, P1, 55% chalk you don't fight), then a **second dominator path** that differentiates — Bell is the sharp one (under-owned relative to his projection), with Larson/Briscoe as alternates. The winning shape at a high-tire-wear intermediate is **1–2 front-running dominators + a stack of P11–30 place-differential cars** that gain spots as the field cycles pits and tires fall off. The intermediate optimal profile says every winning build here except one rostered ≥3 top-15 starters, so don't overload the very back — worse-than-30th is only ~8% of optimals; the **P11–30 mid-pack is where ~55% of optimal value lives.**

Field-size posture: **no contests declared, so build for a large-field GPP** — maximum differentiation. The top of this slate (Hamlin/Heim/Reddick) is chalky and obvious; your edge is **selection in the mid-pack PD tier** where 8–10 drivers all have the same ~40-point ceiling at a fraction of Heim's 45% ownership. Sharp target: **≥1 sub-5%-owned leverage driver in most lineups** (this account carries one only 19% of the time in NASCAR vs 59% in PGA — that gap is the single biggest fixable leak), an elite anchor with downstream differentiation, every lineup unique, judged on ceiling not floor.

## Key themes
- **Reddick (vendor loves) vs Bell (article loves) — the central disagreement, and the edge.** DailyFan has Reddick at **39% own / 57.1 proj** (2nd-most-owned driver) but has Bell at **24% own / 58.0 proj** — a *higher* projection at 15 fewer points of ownership. DDD independently backs Bell: Reddick is "secondary… not sure he's an elite play," his lead is often "handed to him" without the fastest car, and his upside is capped if Hamlin dominates the available laps-led; Bell is "the 2nd best guy this year" hidden by bad luck. **Both the article's qualitative read and the vendor's own number say Bell > Reddick — yet the field is on Reddick.** Trust Bell; that's uncontested leverage.
- **Mid-pack PD is the meat, and it's a deep pool.** DDD: "the top end of this slate is probably chalky and obvious but this mid tier is where the bread will be butter" — he counts 20–23 drivers with legit top-15 equity from P11–30. That's the exact mid-pack-PD mechanism from Pocono/Sonoma, and the DFR intermediate table confirms it structurally (~55% of optimal spots from P11–30). The leverage isn't *whether* to play the band — it's *which* of the interchangeable ~40-point ceilings you pick, at 1/3 of Heim's ownership.
- **Heim is deep-back PD chalk (45%) — great player, contested ownership.** DDD CORE and hard to bet against, but at 45% from P28 he's the play everyone has. Per `correlation-not-substitution`, the other deep/mid PD guys (Jones 24%, Cindric 27%, Zane 5%, Herbst 4%, Nemechek 5%) are **independent shots at the same point distribution, not substitutes** — roster the band, not just the chalk representative.
- **McDowell 24% own undercuts his own thesis.** DDD likes attacking pass-through-penalty plays "because ownership is typically limited" (McDowell failed inspection, starts P38, pass-through). But DailyFan has him at **24%** — that's not limited, that's chalk. The vendor number contradicts the article's leverage premise; his deep-PD appeal is already priced in.
- **Toyota > HMS on this track type in 2026 (article) mutes the HMS-intermediate double-up lesson.** The framework says HMS teammates double-up at intermediates, but DDD is explicit that JGR/23XI has been "borderline unfuckwithable" after 15 laps all year and HMS/Penske/RFK are "a clear step off." Byron (18%) + Elliott (15%) are live *contrarian* doms (they need top-3 + 20 fast laps) — a leverage double-up for MME, not the primary path. I trust the article's org read here.

## Leverage & fades
**Leverage — play (each a mid-pack/value PD shot at a ~40-pt ceiling the field is under-owning):**
- **Zane Smith** — $6,600, P16, 5% own, proj 27 (DailyFan). PLAY. Sub-5% with *proven* intermediate top-10 speed this year (9th Nashville, 10th Charlotte, both on merit) from a P16 mid-pack start — floor matches the 15%+ crowd at a third the ownership.
- **Riley Herbst** — $6,500, P18, 4% own, proj 29 (DailyFan). PLAY (leverage dart). 23XI equipment (the best org on the track type) + P18 PD; 11th Texas, 14th Kansas. The cleanest sub-5% dart per `carry-a-sub5-leverage-dart-mme`.
- **John H. Nemechek** — $5,700, P17, 5% own, proj 24 (DailyFan). PLAY (dart). Deep P17 PD, smashed Pocono (4th), teammate Jones stellar on the track type — legit top-15 equity at sub-5%.
- **Ricky Stenhouse Jr** — $6,200, P24, 7% own, proj 16 (DailyFan). PLAY (leverage). P24 sits dead-center in the P11–30 PD band that paid at Pocono (34.45) and Sonoma (33.0); sub-10%, and named in the sharp-playbook as a value scorer this account skips. DDD calls him "super contrarian" — that's the point.
- **Todd Gilliland** — $5,300, P29, 6% own, proj 19 (DailyFan). PLAY (salary saver). P29 is the exact mid-pack-band start where Gilliland scored 35.5 at Pocono; sub-10% cheap PD that frees salary for two dominators.
- **Chase Briscoe** — $9,900, P7, 14% own, proj 46.85 (DailyFan). PLAY. Under-owned JGR dominator upside — a pivot off the Hamlin/Bell chalk that captures the same Toyota edge at 14%.

**Fades / passes (a fade is a bet — price the world it needs):**
- **Tyler Reddick** — $10,700, P13, 39% own, proj 57.1 (DailyFan). FADE relative to field (not zero). Needs to out-dominate Hamlin AND Bell for the laps-led points to justify 39% — the article and the vendor's own Bell projection both say that's the less-likely of the equivalent Toyota doms. Underweight, play Bell instead.
- **Alex Bowman** — $7,300, P12, 4% own, proj 21 (DailyFan). FADE. Starts too high for PD, no intermediate top-10 this year, bad floor; DDD "MME or fade" = **fade in single entry** (Dover lesson). Sub-5% own is the field correctly pricing a low floor, not leverage.
- **Ross Chastain** — $7,800, P19, 8% own, proj 30 (DailyFan). PASS (light MME dart only). Needs a top-10 he hasn't managed all year with Trackhouse struggling; the 8% own makes a single MME bullet defensible, but no positive floor case for single entry.
- **AJ Allmendinger** — $6,000, P11, 3% own, proj 18 (DailyFan). FADE. DDD explicit "Fade" — starts too high for PD, bad floor, top-10 unlikely; sub-5% is correct pricing.
- **Connor Zilisch** — $6,300, P21, 3% own, proj 15 (DailyFan). PASS/fade single-entry. DDD "MME or fade," over-priced ($6.3k for a $5.3k profile), wrecks too much. P21 is in the band, but the floor is structurally low — one MME variance bullet at most.
- **Cody Ware** — $4,800, P37, 3% own, proj 14 (DailyFan). FADE. Needs carnage to matter (thin ~8% worse-than-30th optimal bucket); a sub-5% Ware busted and sank lineups at Sonoma. Only rosterable if you're betting on a wreck-fest.
- **Noah Gragson** — $5,400, P32, 8% own, proj 20 (DailyFan). PASS (SE) / MME punt. Deep P32 PD has a ceiling, but worse-than-30th is the ~8% thin bucket — a salary-relief punt only if Tier 5 forces it, not a target.
- **Cole Custer** — $5,100, P33, 8% own, proj 19 (DailyFan). PASS (SE) / viable MME PD punt. DDD says he "carries the most PD" of the bottom group and is a sharp-playbook value name, but P33 is deep-back — MME salary-saver, not a single-entry floor play.

## Decisions
1. **PLAY Bell over Reddick — Anchor-Equivalence call (MANDATORY).** Reddick (39% own, $10.7k) and Bell (24% own, $10.0k) — with Larson (30%, $10.5k) — are equivalent-profile Toyota dominators; the field over-owns Reddick while the vendor's own projection (Bell 58.0 > Reddick 57.1) and the article both rank Bell higher. Run Bell as the alternative in at least one lineup, **sized for leverage, not a 50/50 Reddick/Larson hedge** (`anchor-equivalence-not-parity`).
2. **PLAY Hamlin as the near-mandatory anchor, build a second dominator path around him.** He's the #1 dom from P1 at 55% you don't fight; the differentiation comes from *which* second dominator (Bell > Larson > Briscoe) and the mid-pack cars beneath, not from fading Hamlin.
3. **PLAY the P11–30 mid-pack PD band deep, don't lean on Heim alone.** Source place-differential from the 55%-of-optimal mid-pack tier — pair the chalk (Heim 45% / Jones 24% / Cindric 27%) with the under-owned interchangeable ceilings (Zane 5%, Herbst 4%, Nemechek 5%, Stenhouse 7%, Gilliland 6%); they're independent shots, not substitutes (`midpack-pd-over-deep-back-chalk` + `correlation-not-substitution`).
4. **PLAY ≥1 sub-5% leverage driver in most lineups — fix the NASCAR leak.** Herbst (4%), Zane (5%), or Nemechek (5%) — this account carries a sub-5% piece in only 19% of NASCAR lineups vs 59% in PGA, the biggest fixable weakness; the ceiling comes from the tail, not the median (`carry-a-sub5-leverage-dart-mme`, sharp playbook).
5. **PASS Bowman, AJ, and Ware in single entry.** All three are "starts too high, no floor" or "needs carnage" — Bowman/Zilisch carry DDD "MME or fade" tags (= fade in SE, Dover lesson), and their sub-5% ownership is the field pricing a low floor correctly, not leverage.

_Note: NextGen has never raced Chicagoland — every track read here is extrapolation from comparable intermediates and this account's first look at the venue. Confirm the mid-pack-PD and Toyota-dominance reads at the autopsy and de-UNVERIFY the venue file._
