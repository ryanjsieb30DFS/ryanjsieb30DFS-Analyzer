# MLB Classic — 6.12.26 lineup portfolio

## Pre-flight checklist
- [x] Slate confirmed: mlb_classic — 13-game main slate 6.12.26; bundle generated 2026-06-12 18:32, slate analysis written same day; lock 7:05 PM ET — tight clock, so the late-build-bailout default applies: enter THIS tracked portfolio as-is, no near-lock swaps to untracked lineups
- [x] Projections loaded: Ship It Nation MLB Projections (257 players, this slate); pool-omission cross-check run — Colby Thomas / Jacob Wilson / Alika Williams are Stone-projected ATH starters missing from the SIN pool; Wilson is rostered in Lineup 2 from Stone data ($3.3K, 14.1% own) — **confirm the ATH lineup at lock**
- [x] Venue file read: `rules/mlb_classic/parks/las_vegas_ballpark.md` (UNVERIFIED stub) — 6/10 observation: the mega-total paid as secondary PIECES, never as the primary 5-stack → Vegas exposure capped at 2–3 bats per side per lineup, no ATH-5 in this portfolio
- [x] Open lessons reviewed: 5 open — **applied**: se-chalk-pitcher-own-condensation (L1 keeps the chalk arm and pivots in his own bats — the 6/11 winning pattern; L2 sizes the Yesavage fade as a real ~40% fade and expresses it through the NYY bats), sin-projection-pool-omissions (Wilson rostered in L2 despite pool omission), five-man-primary-conditional-on-blowup (no 5-stack anywhere — 4-man and 3-man primaries; the ATH-5 blowup build was the analysis's "near-field chalk, not a pivot" and loses the slot in a 2-lineup portfolio), late-build-bailout (process default named in line 1), blank-own-snapshot-artifact (cross-check run in the analysis — duplicate-Muncy artifact caught; LAD Muncy not read as 10% own and not rostered). **Rejected**: weather-proof-dome-stack-pivot — precondition absent (no rain risk concentrating field ownership; nothing flagged by the Stone)
- [x] Framework pre-lock checks: Anchor-Equivalence → Misiorowski/Yesavage at 25.2/23.6% are the equivalent chalk-arm pair; L2 runs the alternative anchor Joe Ryan (14.7%) ✓. Pivot budget (codified): ONE leverage axis per lineup ✓ (L1 = MIL stack, pitchers chalk; L2 = NYY strike, pitchers near-field). Own-pitcher blocks verified: L1 Misiorowski⊗PHI ✓, Imai⊗KC ✓; L2 Joe Ryan⊗STL ✓, Bibee⊗DET ✓. Salary verified ≤ $50,000 with addition shown per lineup
- [x] Prior results scanned: results.jsonl last 3 — the ledger-best top 4.4% (6/11) came from the in-band, one-pivot build that KEPT the condensing chalk arm and pivoted into his own bats; L1 repeats that exact process. The two slates before were untracked-entry misses — this portfolio is the tracked entry

---

## Lineup 1 — MIL doubled through Misiorowski (4-2-1-1)

**Thesis:** MIL — the slate's second-best team total (5.35) at 6% combined ownership against Painter's 8.11 xERA and 4.8-IP leash — blows up while its own chalk arm Misiorowski (the $12K side of the chalk pair the field CAN'T condense on) holds serve, doubling one game script through pitcher and bats per the 6/11 ledger-best pattern (se-chalk-pitcher-own-condensation: keep the chalk arm, take the pivot in his bats).

| Player | Pos | Team | Salary | Proj / Own% | Role |
|---|---|---|---|---|---|
| Jacob Misiorowski | P | MIL | $12,000 | 24.0 / 25.2 | Chalk arm — holds ~25% while Yesavage condenses; correlates with the MIL stack |
| Tatsuya Imai | P | HOU | $6,300 | 13.1 / 7.7 | The slate's value P2 — funds the build (PLAY per board) |
| William Contreras | C | MIL | $5,000 | 8.4 / 1.4 | MIL-4 spine; the C pivot off 30–45% combined Langeliers/Goodman chalk |
| Jake Bauers | 1B | MIL | $4,900 | 8.4 / 1.8 | MIL-4; the 1B pivot off 26%-owned Kurtz |
| Willi Castro | 2B | COL | $4,100 | 10.1 / 18.7 | Best COL piece (vendor agreement) — Vegas exposure as a piece, not a stack |
| Kyle Karros | 3B | COL | $3,000 | 9.3 / 16.1 | Cheap 3B chalk glue; 2nd-and-last COL bat |
| Joey Ortiz | SS | MIL | $2,600 | 6.4 / 1.5 | MIL-4 glue — the $2.6K that funds Misiorowski |
| Jackson Chourio | OF | MIL | $5,500 | 9.5 / 2.7 | MIL-4 core bat |
| Henry Bolte | OF | ATH | $3,600 | 9.1 / 21.5 | ATH chalk piece (in both vendors' nine — no Rooker/Cortes lineup risk) |
| Austin Slater | OF | TB | $2,600 | 8.1 / 6.9 | Cheap TB one-off (4.95 implied) — best proj-per-$ fill under $3K |

**Salary:** 12,000 + 6,300 + 5,000 + 4,900 + 4,100 + 3,000 + 2,600 + 5,500 + 3,600 + 2,600 = **$49,600** ≤ $50,000 ✓

**Shape & band:** MIL-4 + COL-2 + ATH-1 + TB-1 (4-2-1-1, a recurring winning shape in all five logged contests). One leverage axis (the MIL stack); both arms and all four fills are chalk/near-field. 6 sub-10% plays — above the codified 3–5 note but identical to the 6/11 top-4.4% build's density; avg own 10.3%.

**What if?** What if the field's ~196%-owned Vegas game stays merely loud while the quiet 5.35-implied offense facing the slate's worst xERA arm is the one that actually blows up?

## Lineup 2 — The Yesavage bust / NYY strike with the alternative anchor (3-2-2-1)

**Thesis:** Yesavage's projected 23.6% condenses to a real 35–45% (se-chalk-pitcher-own-condensation, sized pre-lock) and busts against a NYY offense the field owns at 3.1% combined — Rice/Bellinger/Grisham cash the uncontested equity while alternative anchor Joe Ryan (14.7%, Anchor-Equivalence satisfied) outscores the chalk arms, and the rest of the roster stays near-field Vegas chalk so the strike is the lineup's ONLY pivot.

> **Pre-lock repair (6/12):** Chad Stevens (COL 2B $2,600) scratched. No 2B ≤$2,700 carries chalk ownership (best: Rojas 3.5%), so the chalk-glue role moved to the OF slot: Carrigg (COL, 15.9%) in for Slater (TB, 6.9%), and Kiner-Falefa fills 2B at $2,600. Thesis, NYY axis, arms, and 3-2-2-1 shape unchanged; COL-2 Vegas-piece chalk exposure preserved.

| Player | Pos | Team | Salary | Proj / Own% | Role |
|---|---|---|---|---|---|
| Joe Ryan | P | MIN | $10,000 | 18.4 / 14.7 | The Anchor-Equivalence alternative anchor (vs STL, 4.10 implied) |
| Tanner Bibee | P | CLE | $7,300 | 15.6 / 14.4 | Mid-chalk P2 — keeps the arms near-field so the NYY bats are the only pivot |
| Shea Langeliers | C | ATH | $5,800 | 13.0 / 27.9 | The C slot in any Vegas-exposed build; chalk ballast |
| Ben Rice | 1B | NYY | $6,100 | 8.9 / 0.3 | NYY strike — top of the leverage table |
| Isiah Kiner-Falefa | 2B | BOS | $2,600 | 6.3 / 2.6 | Best-proj 2B at the slot price post-scratch (no chalk 2B exists ≤$2,700); BOS one-off |
| Kyle Karros | 3B | COL | $3,000 | 9.3 / 16.1 | 3B chalk glue; 2nd-and-last COL bat |
| Jacob Wilson | SS | ATH | $3,300 | 9.6* / 14.1* | *Stone-only (SIN pool omission — sin-projection-pool-omissions applied): same Vegas exposure as Tovar, $700 cheaper, invisible to snapshot-driven builders — **confirm at lock** |
| Cody Bellinger | OF | NYY | $5,100 | 7.9 / 0.4 | NYY strike |
| Trent Grisham | OF | NYY | $4,100 | 8.4 / 1.4 | NYY strike — leadoff, cheapest real-projection NYY bat |
| Cole Carrigg | OF | COL | $2,700 | 8.7 / 15.9 | Chalk COL Vegas piece — inherits the scratched Stevens role (salary release that keeps Rice affordable) |

**Salary:** 10,000 + 7,300 + 5,800 + 6,100 + 2,600 + 3,000 + 3,300 + 5,100 + 4,100 + 2,700 = **$50,000** ≤ $50,000 ✓

**Shape & band:** NYY-3 + ATH-2 + COL-2 + BOS-1 (3-2-2-1 — the diversified shape that won the 6/11 Chin Music). One leverage axis (the NYY strike); arms at 14.7/14.4% and four Vegas-chalk fills keep everything else near-field. 4 sub-10% plays ✓ in band; avg own 10.8%.

**What if?** What if the arm the small SE field condenses on busts — who is holding the 3%-owned offense that beat him?

## Portfolio audit

**Distinct questions ✓** — L1 bets a game-environment (MIL blows up WITH the chalk arm); L2 bets a pitcher-bust world (Yesavage condenses and fails AGAINST the alternative arm). L1 wins in worlds where chalk-arm scoring holds; L2 wins in worlds where it doesn't — opposite sides of the slate's highest-variance decision.

**Player overlap:** 1 of 10 — Kyle Karros ($3.0K 3B chalk glue) only (the Stevens scratch repair removed the Slater overlap). No shared conviction core: zero shared pitchers, zero shared stack pieces. Both axes (MIL-4, NYY-3) are 100% exclusive to their lineup.

**Hedges:**
- Pitcher: Misiorowski (chalk pair, preferred side) vs Joe Ryan (alternative anchor) — the portfolio holds both sides of the chalk-arm question while rostering Yesavage in neither (his condensed ~40% is the bet being attacked, per Decision 2).
- Vegas game: pieces in both lineups (L1: Castro/Karros/Bolte; L2: Langeliers/Wilson/Karros/Carrigg), mega-stack in neither — per the park file's 6/10 observation (pieces paid, the 5-stack was an ownership tax). Both lineups within the 2–3-bats-per-side cap ✓.
- C: Contreras (1.4%) vs Langeliers (27.9%) — the pivot and the chalk at the slate's most condensed bat position.

**Rule compliance:**
- Anchor-Equivalence (mandatory): Misiorowski/Yesavage flagged at 25.2/23.6% → L2 runs alternative anchor Joe Ryan ✓. The bundle's bat-cluster flags (Langeliers/Kurtz/Rooker tier; Bolte/Soderstrom/Cortes/Tovar tier) are all Vegas-game names — L1's MIL-4 is the portfolio's alternative to that entire cluster, and the unconfirmed members (Rooker, Cortes, McNeil) are rostered nowhere ✓.
- Own-pitcher blocks: L1 — no PHI or KC hitters ✓; L2 — no STL or DET hitters ✓.
- Pivot budget (codified): one axis per lineup ✓; sub-10% density 6 (L1 — above the 3–5 note, matching the 6/11 ledger-best build exactly) and 4 (L2, in band). Avg own 10.3%/10.7% sits below the 15–18% band — disclosed honestly: the axes (4 MIL bats ≤2.7%, 3 NYY bats ≤1.4%) mathematically drag the mean; everything outside each axis is chalk/near-field.
- Salary: $49,600 and $50,000, addition shown ✓.
- 5-stack premium: withheld per five-man-primary-conditional-on-blowup (no team rostered 5-deep) ✓.
- Tracked-entry HARD RULE: this file is the portfolio to enter — per late-build-bailout, do NOT swap to untracked lineups near lock.
- Lock-time confirms: ATH starting nine (Wilson in L2; Bolte/Langeliers assumed safe — both in the Stone's projected nine); MIL/TB/CHC/SF lineups were still projected at analysis time — verify Bauers/Ortiz and Slater (L1) are in. Post-scratch adds: verify Carrigg is in the COL lineup (his role likely grows with Stevens out) and Kiner-Falefa is in the BOS nine.
