# MLB Classic — Lineup Portfolio (2026-06-09)

**Contests:** MLB $5k Base Hit (SE, field 490) + MLB $10K Base Hit (SE, field 980) — 2 entries, **1 unique lineup** (same lineup in both SE contests).

Portfolio size note: the contest config asks for exactly 1 unique lineup, and the slate supports exactly one fully-distinct thesis at this entry count — no padding needed or allowed.

---

## Lineup 1 — "Braves Freight Train" (ATL 5 + cheap ATH 2 + Coors hedge, Wheeler pivot)

**Thesis:** The field piles 86–101% combined ownership onto MIL/CHC/ATH while the Braves — second-best offense spot on the slate (5.10 implied, −160 vs Erick Fedde, with Acuna .435 / Harris .507 / Olson .438 xwOBA) — go ~37% combined; this lineup wins when ATL out-scores at least two of the three mega-chalk stacks while Zack Wheeler (9.5% own, best IP/xERA combo on the slate) beats the Burns/Cease/Peralta/May chalk cluster at a third of its ownership.

| Player | Pos | Team | Salary | Key metric | Role |
|---|---|---|---|---|---|
| Zack Wheeler | P | PHI (vs TOR) | $10,700 | 17.38 proj · 9.5% own · 6.3 avg IP, 3.21 xERA | SP1 — the tournament pivot (AE alternative anchor) |
| Andrew Alvarez | P | WSH (vs SF) | $7,200 | 11.84 proj · 8.1% own | SP2 — mid-priced leverage relief (NADES GPP core), avoids the May/Teng/Giolito salary-chalk train |
| Austin Wynns | C | ATL | $2,100 | 6.72 proj · 5.8% own | Punt C inside the primary stack — SIN value-bat call, unlocks the build |
| Matt Olson | 1B | ATL | $5,000 | 9.42 proj · 6.7% own · .438 xwOBA | ATL primary stack |
| Willi Castro | 2B | COL | $4,200 | 8.70 proj · 13.5% own · Coors | One-off Coors hedge — keeps exposure to the 6.8/5.95 CHC@COL game while fading the 90%-owned CHC side |
| Max Muncy | 3B | ATH | $3,500 | 8.71 proj · 15.0% own | Cheap ATH secondary piece (13.2-total game) |
| Mauricio Dubon | SS | ATL | $3,300 | 7.65 proj · 9.1% own | ATL primary stack — cheap SS keeps salary for the bats that matter |
| Ronald Acuna Jr. | OF | ATL | $5,800 | 10.93 proj · 8.0% own · .435 xwOBA | ATL primary stack — premium leverage bat |
| Michael Harris II | OF | ATL | $4,500 | 9.81 proj · 6.1% own · **.507 xwOBA** | ATL primary stack — hottest bat on the slate |
| Colby Thomas | OF | ATH | $3,500 | 9.50 proj · 16.7% own | Cheap ATH secondary piece — SIN value bat |

**Salary check:** 10,700 + 7,200 = 17,900 (P) · 2,100 + 5,000 + 4,200 + 3,500 + 3,300 + 5,800 + 4,500 + 3,500 = 31,900 (hitters) · **17,900 + 31,900 = $49,800 ≤ $50,000** ✓ ($200 unspent)

**Projected points:** ~100.7

**What if?** — *What if the field's three mega-stacks (MIL 101% / CHC 90% / ATH 86%) are anchor-equivalent and the slate's separator is the second-best offense spot nobody is on — ATL at one-third the ownership — paired with the ace the field skipped (Wheeler 9.5%) instead of the chalk-cluster arms?*

**Construction notes:**
- Shape follows SIN's named leverage variant: **ATL 5 primary** (Acuna/Harris/Olson/Dubon/Wynns) **+ cheap ATH secondary** (Thomas/Muncy — the value pieces of the cheapest mega-stack, $7,000 combined) + a Coors one-off (Castro) so a CHC@COL shootout doesn't zero the lineup.
- Own-pitcher rule: Wheeler (PHI) faces TOR — zero TOR bats ✓. Alvarez (WSH) faces SF — zero SF bats ✓. ATL bats face Fedde (CWS), not either of my pitchers ✓.
- Yordan Alvarez ($6,200, 3.9%) was the preferred premium one-off but is salary-infeasible alongside Wheeler + the full ATL 5; Castro at $4,200 in Coors is the best-fitting non-punt one-off.
- **Pre-lock:** ATH and COL lineups were PROJECTED at Stone print time — confirm Colby Thomas, Muncy, Bolte-tier ATH bats and Willi Castro are in confirmed batting orders before lock. If Castro sits, pivot to Ezequiel Duran (TEX 2B/SS, $3,500, 7.2%) or Nasim Nunez (WSH 2B, $3,200) — do not pivot up into CHC chalk.

---

## Portfolio audit

- **Lineup count:** 1 built of 1 requested — matches `unique_lineups_needed`; the same lineup enters both SE contests, which is the contest config's intent (2 entries, 1 unique).
- **Player overlap:** N/A (single lineup).
- **Hedges within the lineup:** fades MIL and CHC entirely but keeps a foot in the MIL@ATH 13.2-total game via the two cheap ATH bats, and in the Coors game via Castro — the lineup doesn't need all three chalk games to fail, only ATL to hit.
- **Anchor-Equivalence pre-lock check (mandatory):**
  - *Pitcher class* (Burns/Cease/Peralta/May/Teng, 19.4–28.8%): **PASS** — runs the named alternative anchor, Wheeler at 9.5%, and avoids the May/Teng salary-relief chalk at P2 (Alvarez 8.1%).
  - *Stack class* (MIL/CHC/ATH, 86–101% combined): **PASS** — anchors on the alternative (ATL, ~37%), touching the equivalence class only through its cheapest members as a secondary.
  - *Hitter-tier flags* (Langeliers/Bauers/Turang; PCA/Hoerner/Chourio/Rooker; etc.): resolved downstream of the stack decision per the slate analysis — none rostered standalone.
- **Rule compliance:** roster is P,P,C,1B,2B,3B,SS,OF×3 ✓ · salary $49,800 ≤ $50,000 (addition shown) ✓ · no hitter faces my own pitcher ✓ · GPP-framed leverage build ✓ · no NFL/NBA, no scraping, no cash-game framing ✓.
- **Framework caveat:** `rules/mlb_classic/framework.md` is still a stub — built from roster facts + general MLB GPP principles + the slate analysis, as the framework directs. No autopsy lessons exist yet for MLB Classic.
