# MLB Classic — Lineup Portfolio (2026-06-10)

*(Lineup 1 handbuilt; Lineups 2–3 Claude-built from the 6/10 slate analysis.)*

## Pre-flight checklist
- [x] Slate confirmed: mlb_classic — 6/10/26 main slate (7 games) — bundle generated 2026-06-10 18:44; projections file `mlb-projections-dk-20260610.csv` and The Stone 6.10.26 both dated today. The 6/9-dated article files belong to the archived prior slate and were ignored.
- [x] Projections loaded: Ship It Nation MLB Projections (140 players, $2,000–$11,000); session data is for THIS slate. Calibration (1 slate — note, not weight): SIN ownership MAE 2.76 is trustworthy, proj MAE 5.64 is not — ownership drives the leverage calls below.
- [x] Venue file read: `rules/mlb_classic/parks/coors_field.md` (CHC@COL — leverage lives on the unowned COL side) and `rules/mlb_classic/parks/las_vegas_ballpark.md` (MIL@ATH — **UNVERIFIED stub**, 14.7 total, no unowned side this time).
- [x] Open lessons reviewed: 4 open hypotheses, all applied — **pivot-budget-small-field-se** (L2 is chalk + ONE pivot at 14.3% avg own / 5 sub-10%; L3 concentrates all leverage into a single correlated game-axis, see its thesis); **salary-enabler-pitcher-chalk** (Detmers kept in L2 as enabler chalk, his $7,500 is what funds Schwarber/Harper/Turner; Scherzer leash-trap avoided in all lineups); **blank-own-snapshot-artifact** (Nicky Lopez "0.0% own" row discarded — The Stone has him 10%, and he's in the rain game); **untracked-entry-bypasses-loop** (whichever lineups are entered must come from this file — all three candidates live here before lock).
- [x] Framework pre-lock checks: 5-man primary stack core lever applied (L2 PHI 5-stack, L3 HOU 5-stack); no-hitter-vs-own-pitcher verified per lineup; Anchor-Equivalence → pitcher pair Detmers 38.0%/Luzardo 35.3% (L1 runs both; **L3 runs Lambert 9.2% as the within-class alternative arm**) and stack cluster ATH 91.8/TEX 82.5/MIL 81.8/CHC 76.9 (L1 runs CHC; **L2 and L3 run the alternative anchors PHI and HOU**; TEX avoided entirely on weather).
- [x] Prior results scanned: results.jsonl (1 slate, 6.9.26: -100% ROI, best top 39.9% — noise at n=1). Process note that carries: winners ran near-field own with ~4–5 sub-10% plays; chalk-plus-one-pivot is the read for these field sizes (392 and 588).

---

## Lineup 1 — "Handbuilt" (handbuilt)

**Thesis:** The Cubs blow out Colorado at Coors (6.70 implied, clear) behind the slate's two safest chalk arms, and four sub-10% salary fills out-kick the field's punts in a small SE field where chalk-plus-better-punts is the winning shape.

| Player | Pos | Team | Salary | Proj | Own% |
|---|---|---|---|---|---|
| Reid Detmers | P | LAA (vs HOU) | $7,500 | 17.5 | 38.0% |
| Jesus Luzardo | P | PHI (vs TOR) | $8,500 | 17.3 | 35.3% |
| Kyle Higashioka | C | TEX (vs KC) | $2,700 | 7.0 | 9.4% |
| Michael Busch | 1B | CHC (vs COL) | $5,200 | 11.5 | 18.6% |
| Nick Madrigal | 2B | LAA (vs HOU) | $2,300 | 6.8 | 7.5% |
| Alex Bregman | 3B | CHC (vs COL) | $4,900 | 10.0 | 14.2% |
| Jorge Mateo | SS | ATL (vs CWS) | $2,900 | 6.4 | 2.2% |
| Ian Happ | OF | CHC (vs COL) | $5,000 | 11.0 | 15.3% |
| Seiya Suzuki | OF | CHC (vs COL) | $5,200 | 10.6 | 9.2% |
| Pete Crow-Armstrong | OF | CHC (vs COL) | $5,600 | 13.1 | 19.6% |

**Salary check:** 7,500 + 8,500 + 2,700 + 5,200 + 2,300 + 4,900 + 2,900 + 5,000 + 5,200 + 5,600 = **$49,800 ≤ $50,000** ✓ ($200 unspent)

**Projected points:** ~111.26

**What if?** — *What if the small-field winner isn't a leverage play at all, but the cleanest weather-proof chalk build with sharper punt fills than the field's?*

**Construction notes:** Handbuilt 2026-06-10 18:23. Total own 169.4% · avg 16.9%/player · 4 sub-10% player(s).

---

## Lineup 2 — PHI dome pivot (chalk frame + the underowned 4.80)

**Thesis:** The chalk pitcher pair holds while the slate's best risk-adjusted hitting pivot — a fully correlated PHI 5-stack with Luzardo in the dome (4.80 implied, just 27% combined own that SIN itself calls underowned) — out-scores the rain-exposed TEX/MIL/ATH chalk cluster; per **pivot-budget-small-field-se** everything outside the one PHI pivot stays near-field, and per **salary-enabler-pitcher-chalk** Detmers is kept, not faded — his $7,500 is exactly what pays for Schwarber/Harper/Turner.

| Player | Pos | Team | Salary | Proj | Own% |
|---|---|---|---|---|---|
| Jesus Luzardo | P | PHI (vs TOR) | $8,500 | 17.3 | 35.3% |
| Reid Detmers | P | LAA (vs HOU) | $7,500 | 17.5 | 38.0% |
| J.T. Realmuto | C | PHI (vs TOR) | $3,200 | 6.6 | 4.1% |
| Bryce Harper | 1B | PHI (vs TOR) | $5,300 | 9.6 | 5.9% |
| Jeff McNeil | 2B | ATH (vs MIL) | $3,000 | 8.0 | 15.1% |
| Willi Castro | 3B | COL (vs CHC) | $4,400 | 9.3 | 13.5% |
| Trea Turner | SS | PHI (vs TOR) | $5,000 | 8.7 | 4.9% |
| Kyle Schwarber | OF | PHI (vs TOR) | $6,300 | 11.0 | 5.3% |
| Brandon Marsh | OF | PHI (vs TOR) | $4,000 | 8.7 | 6.6% |
| Cole Carrigg | OF | COL (vs CHC) | $2,500 | 7.9 | 14.2% |

**Salary check:** 8,500 + 7,500 + 3,200 + 5,300 + 3,000 + 4,400 + 5,000 + 6,300 + 4,000 + 2,500 = **$49,700 ≤ $50,000** ✓ ($300 unspent)

**Projected points:** ~104.6 · total own 142.9% · avg 14.3%/player · 5 sub-10% players (all five are the PHI stack — one pivot, not layered pivots)

**Construction:** PHI 5-stack (Schwarber–Turner–Harper–Marsh–Realmuto, $24,400) correlated with Luzardo (PHI's own arm — a PHI win feeds both). Fills are near-field, clean-weather chalk: McNeil (ATH, 15.1%, Vegas heat game) plus a Castro+Carrigg COL mini — the Coors park file's confirmed mechanism (leverage lives on the unowned side; Castro was a winning-lineup staple on 6/9), used here as the analysis directs: 2 one-offs, not the full pivot. Entire lineup is weather-proof: dome, Vegas, Coors — zero exposure to the three rain games.

**What if?** — *What if the rain games fizzle and the night's real scoring environment is the underowned Phillies dome offense, while the field's 77–92%-owned stack cluster splits its equity across TEX rain risk and the contested Vegas game?*

---

## Lineup 3 — HOU strike vs Detmers (the field's P1 busts)

**Thesis:** The 38%-owned Detmers busts because Houston's bats show up — an HOU 5-stack (7.7% combined own, Yordan at 0.65%) paired with HOU's own arm Peter Lambert wins exactly the worlds where the field's pitcher slot dies, with Lambert (9.2%) doubling as the **Anchor-Equivalence** within-class alternative to the Detmers/Luzardo pair; **pivot-budget-small-field-se** is honored in mechanism — all seven sub-10% pieces are ONE correlated axis (the HOU side of HOU@LAA plus its pitcher), not layered independent pivots, and the analysis sizes this binary strike for the larger $6K field.

| Player | Pos | Team | Salary | Proj | Own% |
|---|---|---|---|---|---|
| Jesus Luzardo | P | PHI (vs TOR) | $8,500 | 17.3 | 35.3% |
| Peter Lambert | P | HOU (vs LAA) | $8,200 | 12.9 | 9.2% |
| Moises Ballesteros | C | CHC (vs COL) | $4,000 | 8.8 | 9.8% |
| Christian Walker | 1B | HOU (vs LAA) | $4,200 | 7.6 | 1.7% |
| Jose Altuve | 2B | HOU (vs LAA) | $4,000 | 7.8 | 1.8% |
| Isaac Paredes | 3B | HOU (vs LAA) | $3,900 | 7.6 | 1.2% |
| Jeremy Pena | SS | HOU (vs LAA) | $4,400 | 8.4 | 2.3% |
| Yordan Alvarez | OF | HOU (vs LAA) | $6,400 | 9.1 | 0.65% |
| Henry Bolte | OF | ATH (vs MIL) | $3,500 | 9.1 | 13.3% |
| Cole Carrigg | OF | COL (vs CHC) | $2,500 | 7.9 | 14.2% |

**Salary check:** 8,500 + 8,200 + 4,000 + 4,200 + 4,000 + 3,900 + 4,400 + 6,400 + 3,500 + 2,500 = **$49,600 ≤ $50,000** ✓ ($400 unspent)

**Projected points:** ~96.5 · total own 89.6% · avg 9.0%/player

**Construction:** HOU 5-stack (Alvarez–Pena–Altuve–Paredes–Walker, $22,900) plus Lambert is a single double-sided bet on one game: HOU scoring kills Detmers AND hands Lambert the win — The Stone confirms Yordan's 0.65% is real (.489 xwOBA last 40 AB), not a data artifact. Luzardo stays as the chalk spine (safest environment on the slate: dome, 3.95-implied TOR). Remaining slots are the chalkiest clean-weather fills the salary allows: Ballesteros (CHC Coors), Bolte (ATH Vegas), Carrigg (COL Coors). **Pre-lock caution:** HOU@LAA lineups were still PROJECTED at analysis time — confirm Alvarez/Altuve are in near lock.

**What if?** — *What if the play 38% of the field anchors on is the one that fails — who scoops the prize pool when Detmers gets tagged and every chalk build loses its P1?*

---

## Portfolio audit

**Distinct questions (no near-duplicates):**
- L1: cleanest weather-proof chalk everywhere, wins on punt quality (CHC Coors core).
- L2: keeps the chalk pitcher frame, swaps the chalk stack cluster for the underowned PHI dome game.
- L3: directly attacks the field's #1 pitcher — wins the worlds L1 and L2 (and 38% of the field) lose.

No shared full conviction core: stacks are CHC (L1) / PHI (L2) / HOU (L3) — three different games.

**Player overlap matrix:**
| Pair | Shared players |
|---|---|
| L1 ∩ L2 | Detmers, Luzardo (2) |
| L1 ∩ L3 | Luzardo (1) |
| L2 ∩ L3 | Luzardo, Carrigg (2) |

**Honest flag — Luzardo is 3-for-3.** A Luzardo bust hurts the whole portfolio. Accepted deliberately: he is the slate's safest environment (dome, weakest opponent, zero weather risk), the pivot-budget lesson says to keep the non-pivot slots near-field, and the Anchor-Equivalence obligation on the pitcher pair is discharged via Lambert in L3 (the within-class alternative the 6/9 caveat allows), not by forcing a bad arm. Detmers is the hedged anchor instead: held in L1+L2, attacked in L3.

**Hedge map:**
- **Weather:** all three lineups have ZERO hitters in the three rain games (TEX@KC 41%, ATL@CWS 52%, STL@NYM 34%) except L1's two minor punts (Higashioka TEX, Mateo ATL — handbuilt, preserved). Not owning the 82%-owned TEX rain stack anywhere is costless portfolio-wide leverage.
- **Stack cluster (ATH/TEX/MIL/CHC, 77–92% own):** CHC primary in L1 only; ATH only as 1–2 fills (McNeil, Bolte); MIL and TEX zero exposure. L2/L3 run the alternative anchors (PHI, HOU) per Anchor-Equivalence.
- **Detmers axis:** L1+L2 with him, L3 wins when he busts.
- **Traps avoided everywhere:** Scherzer (leash trap, per salary-enabler lesson's discrimination), Sale (rain + $11,000 double-risk at 28%).

**Rule compliance:**
- Salary: $49,800 / $49,700 / $49,600 — all ≤ $50,000, addition shown per lineup ✓
- Roster shape P,P,C,1B,2B,3B,SS,OF×3 filled in all three ✓ (Castro at 3B, Carrigg at OF, McNeil at 2B via listed eligibility)
- No hitter vs own pitcher: L1 (no HOU bats vs Detmers, no TOR vs Luzardo — Madrigal is LAA *with* Detmers ✓); L2 (no TOR, no HOU ✓); L3 (no TOR vs Luzardo, no LAA vs Lambert — the 5 HOU bats are Lambert's OWN team, positively correlated ✓)
- Max 5 hitters per team: PHI ×5 (L2), HOU ×5 (L3), CHC ×4 (L1) ✓
- Anchor-Equivalence: satisfied at both pitcher and stack level (see checklist) ✓
- Blank-own artifact rows (Nicky Lopez) excluded ✓

**Entry mapping (2 SE entries, user's call):** the analysis sizes the binary HOU strike for the larger field — natural fit is L1 or L2 in the $4K (392 entries) and L3 in the $6K (588 entries). Whichever two are entered, they're both in this file, so the red team and autopsy grade the real portfolio (untracked-entry lesson).
