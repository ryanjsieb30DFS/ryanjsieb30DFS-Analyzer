# MLB Classic — 6/10/26 slate analysis

_7-game main slate (PHI@TOR, STL@NYM, ATL@CWS, TEX@KC, CHC@COL, MIL@ATH, HOU@LAA) · 2 SE contests ($4K field 392, $6K field 1,000) · 1 unique lineup needed_

## Pre-flight checklist
- [x] Slate confirmed: mlb_classic — 6/10/26 main slate — bundle generated 2026-06-10 17:40; The Stone 6/10/26 + SIN rankings/screenshots all dated 2026-06-10 and match the projection player pool. The bundle also lists 6/9-dated files — those belong to the already-archived 6.9.26 slate and were ignored.
- [x] Projections loaded: Ship It Nation MLB Projections `mlb-projections-dk-20260610.csv` (140 players, $2,000–$11,000); session data is for THIS slate. Calibration note: SIN own corr 0.819 / MAE 2.76 vs proj corr only 0.261 / MAE 5.64 — trust its ownership far more than its points (1 slate, note not weight).
- [x] Venue file read: `rules/mlb_classic/parks/coors_field.md` (CHC@COL is on this slate); created `rules/mlb_classic/parks/las_vegas_ballpark.md` stub for MIL@ATH — **UNVERIFIED, built from this slate's articles only**.
- [x] Open lessons reviewed: 4 open hypotheses — applied: pivot-budget-small-field-se (both contests are small-field SE → chalk frame + ONE pivot, see Construction), salary-enabler-pitcher-chalk (Detmers is enabler chalk, Scherzer is the leash trap, see Pitching), blank-own-snapshot-artifact (Nicky Lopez's 0.0%-own leverage row is a blank-Own artifact — The Stone has him 10.0%; row discarded), untracked-entry-bypasses-loop (process: both SE entries must exist in `data/lineups/mlb_classic.md` before lock).
- [x] Framework pre-lock checks: 5-man primary stack is the codified core lever; no-hitter-vs-own-pitcher honored in all calls below; Anchor-Equivalence → Detmers/Luzardo pitcher pair (35.3–38.0%) and ATH/TEX/MIL/CHC stack cluster (77–92% combined own) — call in its own section below.
- [x] Prior results scanned: results.jsonl (1 slate, 6.9.26: -100% ROI, best top 39.9% — noise at n=1). Process notes that DO carry: winners ran near-field own with ~4–5 sub-10% plays; my $10K entry over-pivoted (8 sub-10%); chalk-plus-one-pivot is the read for this field size.

## Slate shape — three clean run environments, three rain games

| Game | Implied (away/home) | Weather |
|---|---|---|
| MIL @ ATH (Las Vegas, 9:05) | **7.35 / 7.35** | Clear, 106° — slate's biggest total (14.7) |
| CHC @ COL (Coors, 8:40) | **6.70 / 5.55** | Mostly clear |
| TEX @ KC (7:40) | 5.20 / 5.00 | ⚠️ **41% rain, scattered T-storms** |
| PHI @ TOR (7:07) | 4.80 / 3.95 | Dome |
| STL @ NYM (7:10) | 4.10 / 4.60 | ⚠️ 34% rain |
| ATL @ CWS (7:40) | 4.30 / 3.45 | ⚠️ **52% rain** |
| HOU @ LAA (9:38) | 4.25 / 4.45 | Clear |

**Weather is the slate's hidden axis and the field isn't pricing it.** TEX is a top-tier chalk stack (82% combined vendor own, Seager 20.7%/Langford 16.5%/Duran 15.1%) sitting in the slate's worst rain game. Chris Sale (28% own, $11,000) and his leverage mirror Davis Martin both pitch in the 52%-rain game. The three clean games — Vegas, Coors, HOU@LAA — plus the dome hold all the weather-proof equity. A delay or PPD in TEX@KC or ATL@CWS is free leverage for anyone who simply isn't there.

Caveat: CHC, MIL, ATH, and both HOU@LAA lineups were still **PROJECTED** (not confirmed) at analysis time — confirm batting orders near lock for the two late games.

## Pitching

**Chalk class (the field's 73%):**
- **Reid Detmers $7,500, 17.5 proj, 38.0% own** (vs HOU, 4.25 implied) — this is *salary-enabler* chalk, not trap chalk: 5.7 avg IP, 28% K, and the $7,500 tag is what unlocks the expensive Vegas/Coors bats. Per the salary-enabler lesson, do NOT fade him on ownership alone — last slate's Dustin May equivalent anchored 13 of 20 top-10 lineups.
- **Jesus Luzardo $8,500, 17.3 proj, 35.3% own** (vs TOR, 3.95 implied, dome) — the safest environment on the slate: zero weather risk, weak opponent, 9.86 K/9. Also enables a correlated PHI-bats build (PHI hitters face Scherzer, not Luzardo).
- **Chris Sale $11,000, 21.1 proj, 28.1% own** — best arm on the slate (6.0 IP, 10.65 K/9, 32% K vs a 3.45-implied CWS), but **52% rain** and a price that forces bat compromises. The rain makes 28% ownership a worse bet than it looks.

**Leverage arms (clean-weather first):**
- **Peter Lambert $8,200, 9.2% own** (vs LAA, clear) — 5.6 IP leash, ultra-low 1.5% barrel rate against a 4.45 implied; the quiet within-class alternative.
- **Shota Imanaga $8,000, 14.1% own** — at Coors. The Coors tax is real; only as a "Cubs blow out COL" correlation piece.
- **Davis Martin $9,500, 2.8% own** (vs ATL) — 6.0 IP, 9.08 K/9, 3.65 xERA, SIN's GPP-2 core arm — but he shares Sale's 52%-rain game, which caps the appeal.
- **Seth Lugo $7,600, 8.2%** / **MacKenzie Gore $7,800, 12.4%** — both in the 41%-rain TEX@KC game; the article's "contrarian SP2 vs the Rangers" call carries the same weather risk it dodges in ownership.

**Trap:** **Max Scherzer $6,500, 11.9% own — 3.6 avg IP, 6.82 xERA, 14.5% K.** This is exactly the Kai-Wei Teng short-leash profile that busted at 27–29% last slate. The leash discrimination worked then; apply it again — avoid.

## Stacks

**Chalk cluster (anchor-equivalent, 77–92% combined own):**
- **ATH 91.8%** — Kurtz 20.9 / Cortes 18.3 / Langeliers 18.3 / Rooker 18.8 / Soderstrom 15.6, with Bolte $3,500 (13.3%) and McNeil $3,000 (15.1%) as cheap finishers. 7.35 implied, clear. The field's #1 build.
- **TEX 82.5%** — only $17,800 for the top stack pieces (Seager $4,300, Langford $3,300, Nimmo $3,500), which is WHY it's owned — but it's in the 41%-rain game. **This is the chalk to be underweight.**
- **MIL 81.8%** — Chourio 16.7 / Turang 19.5 / Contreras 16.4 / Bauers 17.8. Note: Turang burned the field at ~31% actual own last slate (0.0 pts) and is back at 19.5%.
- **CHC 76.9%** — PCA 19.6 / Busch 18.6 / Hoerner 16.0 / Happ 15.3 at Coors, 6.70 implied (highest single-team number until the Vegas game).

**Leverage stacks:**
- **PHI 27.3% combined, 4.80 implied, dome** — Schwarber 5.3%, Harper 5.9% (.453 xwOBA, .336 xISO), Turner 4.9%, Marsh 6.6%, Stott 4.7%. SIN's own breakdown says PHI comes in "far less popular than the slate environment probably warrants." Pairs naturally with Luzardo for a fully correlated, weather-proof build. **Best risk-adjusted pivot on the slate.**
- **COL 53.2% vs CHC 76.9%** — the Coors park file's confirmed mechanism (leverage lives on the unowned side). The field half-learned from 6/9 — Goodman 10.1%, Karros 11.5%, Tovar 10.4%, Castro 13.5% — so the edge is thinner, but McCarthy 6.4% / Rumfield 7.7% still ride the same 5.55 implied for a fraction of the Cubs' ownership.
- **KC 40.1%, 5.00 implied** — Witt 8.0%, Caglianone 3.3% (last slate's 40-point hero), Salvy 8.6% — real ceiling, but the 41% rain applies to both sides of that game.
- **HOU 7.7% combined, 4.25 implied, clear** — Yordan Alvarez $6,400 at **0.65%**, Pena 2.3%, Altuve 1.8%, Paredes 1.2%. This is the direct strike against Detmers chalk: an HOU 4–5 stack wins precisely the worlds where 38% of the field's P1 busts. Binary, but it's the slate's purest leverage.

## Where the snapshot and the articles diverge

- **Nicky Lopez (#1 snapshot leverage, "0.0% own")** — blank-Own artifact (open lesson, confirmed again here): The Stone has him 10.0% own, batting 9th for TEX. Still fine at $2,200/7.6 proj as a salary saver, but he's a known value-bat, not a 0%-own secret — and he's in the rain game.
- **Yordan Alvarez 0.65% own** — NOT an artifact; The Stone confirms it (.489 xwOBA, .409 xISO over his last 40 AB). The single best one-off leverage play on the slate; verify he's in the (projected) lineup near lock.
- **Juan Soto 1.09%** — real (.475 xwOBA); but NYM sits in the 34%-rain game.
- **Miguel Vargas 0.36%** — real, hot (.484 xwOBA), but he faces Sale; only usable in a build that's already off Sale.
- **Snapshot stack_proj loves MIL (94.9) over ATH (90.7); SIN's vendor ranks flip it (ATH own 91.8 way above MIL 81.8)** — with proj MAE 5.64/corr 0.26, lean on the ownership signal: ATH is the more contested side of the same game; MIL is the marginally cheaper-owned door into the 14.7-total environment.
- **The articles' "tournament pivot" arms (Gore, Lugo, Martin)** all sit in rain games — the snapshot has no weather column, and the articles under-discount it too. The genuinely clean pivot arm is Lambert.

## Anchor-Equivalence call

- **Pitcher pair: Detmers 38.0% / Luzardo 35.3%** — equivalent to the field. With one unique lineup, do not default to the higher-owned half. Luzardo is the better risk-adjusted member (dome vs a projected late-game lineup), and the true alternative-anchor move — per the 6/9 caveat that the alternative can come from inside the class — is **Lambert at 9.2%** as SP2 next to whichever chalk anchor you keep.
- **Stack cluster: ATH 91.8 / TEX 82.5 / MIL 81.8 / CHC 76.9** — four equivalents; the rule demands the build not simply take the most-owned. TEX self-eliminates on weather. The compliant structure: primary from ATH/MIL/CHC (clean-weather chalk is fine in small SE), with the **alternative anchor expressed via the pivot** — PHI mini-stack, COL Coors side, or the HOU strike.

## Construction guidance (small-field SE — chalk + ONE pivot)

Both contests are ≤1,000-entry SE: per the pivot-budget lesson, winners run **near-field ownership with one structural pivot** (~13–16% avg own, 4–5 sub-10% players — not 8). Pick ONE leverage axis and keep everything else field-standard:

1. **PHI 3–5 + Luzardo (recommended axis)** — fully correlated, dome, 27% combined own in a 4.80-implied spot the article itself calls underowned. Leaves room for an ATH/MIL/CHC mini as the chalk anchor. Weather-proof by construction.
2. **HOU 4–5 vs Detmers** — maximum leverage (sub-8% combined own vs 38% pitcher chalk), but binary and dependent on a projected late lineup. The sharper play in the 1,000-field $6K than the 392-field $4K.
3. **COL side of Coors** — confirmed park mechanism, thinner edge this time (field at 53%, not 6/9's vacuum). Best as 2–3 one-offs (McCarthy/Rumfield tier) rather than the full pivot.
4. **Passive weather fade** — whatever the axis, keep chalk exposure out of TEX@KC and ATL@CWS. Not owning the 82%-owned rain-game stack is itself leverage that costs nothing.

Avoid: Scherzer at any ownership (leash trap); paying the Sale + rain double-risk at 28%; a CWS bat next to Sale or an HOU bat next to Detmers (own-pitcher rule).

**Process note (open lesson):** both DK entries are the same single unique lineup — whatever is actually entered must exist in `data/lineups/mlb_classic.md` (built or handbuilt) before lock, so the red team and autopsy grade the real portfolio.
