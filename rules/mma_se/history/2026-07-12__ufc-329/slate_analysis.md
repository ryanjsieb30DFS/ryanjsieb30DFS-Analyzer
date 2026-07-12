# MMA Slate Strategy — UFC 329 (McGregor vs. Holloway) · 2026-07-11

## Pre-flight checklist
- [x] Slate confirmed: mma_se — UFC 329 (14 fights, McGregor/Holloway main event) — bundle generated 2026-07-11 11:55; both article files dated 2026-07-11; matches today. Fresh slate, not stale.
- [x] Files read: **2 of 2** `articles/mma_se/` files — `DF Top Plays 7.11.26.pdf` (6pp, full) and `DF Matchups 7.11.26.pdf` (88pp, full, every fight). Plus the DailyFan projection CSV (28 fighters) in the bundle. **No file skipped, none unparseable.** Only one vendor loaded (DailyFan) → no cross-vendor board; disagreement below is article-vs-article and article-vs-projection.
- [x] Venue file: N/A — MMA has no venue file (per CLAUDE.md); nothing to read/stub.
- [x] Open lessons reviewed (lessons.yaml):
  - APPLIED `leverage-is-the-low-own-finisher-not-the-named-dog` (6/27) → leverage = the low-owned FINISHER who wins (Green/Costa/Kavanagh/Riley), NOT the article-named punt dogs (Garza/Garbrandt/Ellison) — see Leverage & fades.
  - APPLIED `finish-heavy-small-fields-still-won-by-differentiation` (6/27) → 10+ fights carry strong ITD lines; 291 is a small field but held to ~16–20% avg own / ≥1 low-owned finisher, NOT relaxed to chalk — see How to approach.
  - APPLIED `fade-on-structure-not-narrative` (6/20) → McKinney/Holloway underweights are STRUCTURAL (RD1-or-lose fragility; 45% own + duplication + price-ceiling), not scouting guesses.
  - APPLIED `finish-capable-favorite-is-not-secondary-chalk` (6/20) → McKinney, Pinas, Costa, Kavanagh, Yanez are finish-capable favorites, exempt from the "trim mid-own chalk" instinct.
  - APPLIED `cap-single-favorite-exposure` (6/14, format-agnostic) → cap the chalkiest favorite (McKinney/Holloway), carry a fade of each, but do NOT zero a live favorite.
  - APPLIED `cheap-slot-prefer-floor-or-live-dog` (6/14) → cheap slot = live finisher/floor (Reese/Krylov/Almeida), not pure relief.
  - APPLIED `confirmed-vs-speculative-news` (5/9) → Basharat's opponent swap to Garza is CONFIRMED (late replacement); reacted fully.
  - REJECTED all four showdown lessons (`flex-spine-diversity`, `trust-cpt-own`, `captain-the-ceiling`, `cap-single-favorite`'s captain framing) — mechanism-N/A: this is CLASSIC 6-fighter + 5-Max, no captain slot.
- [x] Framework pre-lock checks: **Anchor-Equivalence** → Holloway (45%) / Steveson (34%) premium-anchor pair; run Steveson-not-Holloway in ≥1 build, never both together (article-confirmed duplication). Asymmetric-weighting trigger does NOT fire (Holloway is chalkiest but has a decision FLOOR, not KO-or-bust) → default to presence on both sides, mild lean to lower-owned/higher-ceiling Steveson. **Ceiling threshold** OK — Steveson (102)/Holloway (80)/McKinney (115 avg-win) clear a ~500+ target easily; don't let the gate zero out low-own finishers. **Binary-leverage-weak-in-small-fields** → 291 is small, so prefer finish-capable FAVORITES (Costa/Kavanagh/Riley) over pure KO-or-bust dogs (Ellison/Garbrandt/Garza).
- [x] Prior results scanned: results.jsonl last 3 (6/14, 6/20, 6/27). 6/27 Baku best 1.3%ile came from the DIFFERENTIATED build (Fiziev/Camilo); chalkiest build finished 90.2%ile — the direct evidence behind the finish-heavy differentiation lean here.
- [x] Sharp envelope noted: target ~16–20% avg own/slot, ceiling over median, all-unique, elite anchor + downstream differentiation, ≥1 genuinely low-owned finisher. NOTE: literal sub-5% is only Ellison (2%, a near-dead punt), so satisfy the spirit with a sub-15% favorite-finisher (Kavanagh 17 / Riley 11 / Green 28).

## Slate at a glance
| Fight (wt) | Favorite | ITD line | DK notable | DailyFan own |
|---|---|---|---|---|
| McGregor / **Holloway** (170, 5rd, ME) | Holloway -225 | -450 | Holloway $9k | Holl 45 / McG 28 |
| BSD / Pimblett (155) | **BSD** -152 | -215 | BSD 123/win | BSD 36 / Pimb 29 |
| **Sandhagen** / Bautista (135) | Sand -136 | +162 (dist -230) | pace, no dominator | Sand 18 / Baut 17 |
| Royval / **Kavanagh** (125) | Kav -220 | +110 | Kav boom/bust | Kav 17 / Roy 15 |
| Green / **McKinney** (155) | McK -130 | **-1200** | McK 115.7/win | McK 46 / Green 28 |
| **Whittaker** / Krylov (205) | Whit -125 | -160 | both hittable | Kry 29 / Whit 16 |
| **Steveson** / Ellison (HW) | Stev -3000 | -2000 | Stev proj 102 | Stev 34 / Elli 2 |
| Garbrandt / **Yanez** (135) | Yan -450 | -180 | Yan boom/bust | Yan 17 / Garb 9 |
| Kamaka / **Riley** (145) | Riley -260 | +140 | Riley low-own fav | Riley 11 / Kam 14 |
| **Cortez** / Cong (125) | Cortez -114 | +195 (dist -250) | binary, low ceiling | Cong 16 / Cort 21 |
| **Pinas** / Almeida (185) | Pinas -205 | -400 | Pinas 100% finish | Pinas 26 / Alm 15 |
| **Basharat** / Garza (135) | Bash -650 | -132 | Bash grappling floor | Bash 15 / Garza 7 |
| **Gandra** / Reese (185) | Gandra -126 | **-600** | both KO threats | Gandra 29 / Reese 27 |
| Durden / **Costa** (125) | Costa -235 | -180 | Costa KO finisher | Costa 20 / Durd 13 |

Contests (both **291-field**): **UFC $10K Counter Punch** (SE, 1/1) + **UFC $10K Counter Jab** (5-Max, 1/5). Small fields — but finish-heavy (below), so differentiate anyway.

## Top plays

**Core anchors (high conviction)**
- **Gable Steveson** — $9.9k, 34% own, proj 102.25, -3000 (DailyFan/articles). Near-lock to win, highest ceiling & projection on the board; the premium build-around. Caveat: 9.9k has been optimal only 1 of last 6 times, so he wins but may not be *optimal* — that's the leverage door (below).
- **Max Holloway** — $9k, 45% own, proj 80.76 (DailyFan); ITD -140, slate-breaking ceiling (past wins 209/164/153 per Top Plays). Safest premium floor; but chalkiest play and duplication magnet.
- **Terrance McKinney** — $8.4k, 46% own, proj 67.31; fight **-1200 ITD** (Matchups). Highest early-finish equity on the slate — every win RD1, 115.7 avg in wins. Chalk, but a finish-capable favorite (exempt from trim).
- **Benoit Saint Denis** — $8.5k, 36% own, proj 72.58, -152 (DailyFan); 123 DK/win historic scorer (Matchups). Grappling-pace ceiling in a win.

**Pivots (mid, leverage-leaning)**
- **King Green** — $7.8k, **28% own**, +110 (DailyFan). The cheaper, lower-owned side of the -1200 McKinney fight; multiple analysts call him the value side ("survives and finishes," Matchups). Same near-certain-finish fight at 18 pts less own.
- **Lone'er Kavanagh** — $8.8k, **17% own**, -220, proj 70.12 (DailyFan). Low-owned favorite with real KO equity — the article's named "8k contrarian target."
- **Alessandro Costa** — $9.1k, **20% own**, -235, proj 73.51 (DailyFan). Low-owned KO finisher; Brett's preferred sneaky finisher, "mid-round finish at low public ownership."
- **Paddy Pimblett** — $7.7k, 29% own, +132 (DailyFan). BOTH matchup writers lean Pimblett to WIN while the projection favors BSD — article-vs-projection edge at a $800 discount to BSD.
- **Damian Pinas** — $8.9k, 26% own, -205, fight -400 ITD (Matchups). 100% finish rate, RD1 KO threat.

**Darts / value**
- **Adrian Yanez** — $9.4k, 17% own, -450, proj 76.63 (DailyFan). Low-owned favorite finisher; boom/bust, needs the early KO.
- **Luke Riley** — $9.3k, **11% own**, -260, proj 72.74 (DailyFan). Lowest-owned favorite on the board; caveat +185 ITD → likely a decision, so ceiling is capped.
- **Farid Basharat** — $9.6k, 15% own, -650, proj 82.99 (DailyFan). Highest floor of the low-owned tier (grappling decision, 80–90 median); contrarian at 9.6k.
- **Zach Reese** — $7.6k, 27% own, +106 — cheap live finisher (fight -600 ITD). **Nikita Krylov** — $7.5k, 29% own, +105, 94% career finish rate — cheap value. **Cesar Almeida** — $7.3k, 15% own, +175 — sneaky KO dog.

## How to approach the slate
Winning shape: an **elite anchor (Steveson OR Holloway, not both) + a finish-capable favorite core + one genuinely low-owned finisher**, judged on ceiling. This is a **finish-heavy board** — McKinney/Green -1200, Steveson -2000, Gandra/Reese -600, Pinas/Almeida -400, plus BSD/Pimblett -215, Costa/Durden -180, Yanez/Garbrandt -180. That much finish equity produces wide score dispersion, which lets low-owned finishers separate **even in a 291 field** (direct 6/27 Baku evidence: chalkiest build 90.2%ile, differentiated build 1.3%ile). So despite the small fields, do **not** collapse to chalk — hold ~16–20% avg own and carry ≥1 sub-15% finisher.

Chalk-vs-contrarian: the field will pile Holloway (45) + McKinney (46) + Steveson (34); Top Plays explicitly flags Holloway+Steveson and Steveson+McKinney+Holloway as the **most-duplicated** constructions — avoid stacking all the top chalk together. Own an anchor, then differentiate downstream through the low-owned favorite-finishers (Kavanagh 17, Costa 20, Yanez 17, Riley 11) and the leverage sides of near-certain finishes (Green 28). SE bullet = your single highest-conviction *differentiated* build (Steveson-not-Holloway or a heavy low-owned-finisher core); the 5-Max spreads across both anchor sides and both McKinney/Green sides. Never run two entries that answer the same question, and don't lean the cheap slot on pure salary relief — use a live finisher/floor (Reese/Krylov/Almeida).

## Key themes
- **Where the sources disagree (the edge):**
  - **Article vs projection — BSD/Pimblett:** both Matchups writers (Tim + Brett) pick **Pimblett to win**; the DailyFan projection has **BSD** at 58.5% win / 36% own vs Pimblett 41.5% / 29%. Trust the article lean here — Pimblett at 29% and $800 cheaper is the leverage side of a fight the numbers over-weight to BSD.
  - **Article vs projection — Whittaker/Krylov:** article trusts **Whittaker** (better technical kickboxer at 205) but expects **Krylov** to be chalkier (7.5k value, +105). Projection: Krylov 29% own vs Whittaker 16%. If you believe the article's Whittaker read, 16% own is uncontested leverage on the side more likely to win.
  - **Article vs projection — McKinney/Green:** Technical Tim picks **Green**; projection has McKinney at 46% own / 53% win. The -1200 ITD means someone scores big early — Green (28%) captures that same finish cheaper.
- **The Steveson paradox:** -3000 to win but 9.9k is historically almost never optimal (1/6). He's the highest-floor *anchor* yet a leverage *fade* relative to his ceiling — the article's contrarian construction is "build the stacked 7.5k–8.9k mid-range WITHOUT Steveson." Both truths coexist; that's the anchor-equivalence lever.
- **McKinney is a coin flip dressed as chalk:** -130 (fallen from -170), all wins RD1, documented cardio/durability collapse if extended. His ceiling is real (finish-capable favorite, keep him) but his 46% own prices in a win he only lands ~half the time — Green is the structural hedge inside the same fight.
- **Cong/Cortez and Sandhagen/Bautista are the traps to fade:** distance-leaning (-230 / -250), low-dominance, "no clear path to a smash" per both writers — mid-priced fighters that eat salary without a ceiling.

## Leverage & fades

**Leverage (underowned, real finish/floor path — the mechanism each needs):**
- **King Green — PLAY (28%).** Needs the -1200 fight to end early on his side (+110, live finisher, "survives and finishes"); same near-certain-finish equity as 46%-owned McKinney at 18 pts less ownership.
- **Lone'er Kavanagh — PLAY (17%).** Needs an early KO of Royval (Kape blueprint, -220 favorite, proj 70); low-owned favorite = ceiling without the crowd.
- **Alessandro Costa — PLAY (20%).** Needs a mid-round KO of the durability-fading Durden (-235, article's preferred low-own finisher); prices in a finish the field isn't paying for.
- **Adrian Yanez — PLAY (17%).** Needs to survive early and finish the regressed Garbrandt (-450); low-owned favorite finisher, boom/bust.
- **Luke Riley — PLAY, thin (11%).** Lowest-owned favorite; needs to beat Kamaka but +185 ITD caps him to a ~decision ceiling — a differentiator, not a smash.
- **Farid Basharat — PLAY as floor-leverage (15%).** Needs takedowns/control to grind Garza (-650, grappling); highest median floor of the low-owned tier at a 9.6k ownership discount.
- **Paddy Pimblett — PLAY (29%).** Needs to weather BSD's early grappling and win an extended fight (both writers' pick); the article-preferred side the projection under-weights.

**Fades / underweights (a fade is a bet — the world it needs):**
- **Max Holloway — UNDERWEIGHT (45%).** STRUCTURAL: chalkiest play + duplication magnet at $9k; needs an early finish (not just a decision win) to beat his price ceiling on a slate stacked with 100+ scores. Pivot to Steveson. Not a zero — he has a real floor.
- **Terrance McKinney — MIX/underweight-vs-field (46%).** STRUCTURAL: his entire case is RD1; if it extends "he very likely loses." Keep him (finish-capable favorite) but pair the same fight's Green side rather than over-concentrating on the 46% chalk.
- **Cong Wang / Tracy Cortez, Sandhagen / Bautista — FADE.** Distance-leaning, low-dominance fights (-230/-250 to go the distance); no ceiling to justify mid-range salary.

**Mandatory sub-10% coverage (leverage candidates):**
- **John Garza — PASS ($6.6k, 7%).** +475 boxer on one week's notice vs a -650 grappler who takes him down 3–5x; coin-flip win equity too thin for a 291 SE that rewards a differentiated finisher over a random dog. Deep-field dart only.
- **Cody Garbrandt — PASS ($6.8k, 9%).** Only path is a fluke RD1 KO (+550 ITD); a "win" decision scores ~42–50 — not enough ceiling to define the field. Punt only.
- **Elisha Ellison — PASS, hard ($6.3k, 2%).** +1500 vs Steveson -3000; "historic upset," 8% win. A 2% dart for a massive-field portfolio, not a 291 SE.

## Decisions
1. **PLAY the Anchor-Equivalence split — Steveson-not-Holloway in ≥1 build, and never both together.** Holloway (45%) and Steveson (34%) are substitutable premium anchors; Top Plays confirms pairing them is the most-duplicated construction. Asymmetric-weighting does NOT fire (Holloway has a decision floor, isn't KO-or-bust) → keep both sides present, mild lean to lower-owned/higher-ceiling Steveson.
2. **PLAY Green as the leverage side of the -1200 McKinney fight; MIX McKinney rather than jamming the 46% chalk.** One of them scores big early; owning the 28% side captures the same near-certain finish with real leverage.
3. **PLAY a low-owned favorite-finisher as the required differentiator — Costa (20%), Kavanagh (17%), or Yanez (17%) — not a KO-or-bust punt dog.** Finish-heavy board + small field means the separator is a sub-20% finisher who WINS (6/27 lesson), so screen favorites, not just the article's named long-shots.
4. **PASS the pure KO-or-bust punts (Ellison 2%, Garbrandt 9%, Garza 7%) as core plays.** In a 291 field their blended EV is too low; binary variance without a floor is punished at this field size — reserve them for deep-field darts only.
5. **PLAY the SE bullet as the single highest-conviction DIFFERENTIATED build; spread the 5-Max across both anchor sides.** Differentiate the 5 entries on ≥1 conviction anchor (Steveson vs Holloway, McKinney vs Green) — identical cores make five entries one bet, and the lone SE is where differentiation matters most.
