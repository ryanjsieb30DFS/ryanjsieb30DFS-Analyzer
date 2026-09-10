# NFL Showdown Framework

**DRAFT 2026-09-09 — seeded from docs/nfl_game_theory.md (Part 2), pending user approval.**
Sources: ETR Showdown 101 + winner studies, Fantasy Team Advisors' 163-winner study (2024–26), PFF Showdown Primer, Stokastic. Numbers below are cross-vendor winner data, not this repo's own logged results — the local ledger starts at zero SD slates.

## The format

DK single-game. Six spots: 1 Captain (CPT — 1.5x points at a distinct, higher CPT salary) + 5 FLEX (any position: QB/RB/WR/TE/K/DST). $50,000 cap. Both teams must be represented. The same six players with a different captain is a DIFFERENT DK entry. This is NOT PGA RD4 SD — the captain is real here.

NFL scoring note (unique among this repo's sports): **0.0 FPTS is a real score** (a blanked WR3, a kicker with no attempts) and **a DST can go negative**. Never read a 0.0 as a scratch. (The tier-calibration scratch exclusion carries an nfl carve-out in `src/pool_calibration.py`; the counterfactual swap engine is NOT captain-aware yet, so NFL autopsies run its points-only mode — `salary_checked: False` — rather than shipping flat-priced cap math.)

## The captain decision (the whole game)

CPT costs 1.5x for 1.5x points, so the multiplier itself buys nothing — the captain call is about ceiling and about what the field over-pays for.

| Winning captain's position | FTA (163 winners) | ETR top-1% study |
|---|---|---|
| WR | 33% | 33% |
| RB | 28% | 27% (biggest edge vs field's 24%) |
| QB | 21% | 24% |
| TE | 9% | — |
| DST | 6% | field ~2.5% |
| K | 3% | field ~0.8% |

- **The field over-captains the QB.** He is optimal about 1 in 5; the field makes him the most popular captain nearly every slate. On every completed pass the catcher out-scores the thrower — the QB's own receivers systematically out-captain him. **WR + RB = 61%+ of winning captains.**
- **Winning captains are not obscure**: median winning-captain own ~11%, average price ~$13,000, ~23.6 CPT points. The edge is the right member of the chalk cluster, not a 2% punt.
- Cheap captains under $7,500 won only with genuine slate-topping ceiling (goal-line RB, deep threat) — never as a salary trick. Kicker captains cap the ceiling.

## Correlation shapes (pre-lock CHECKS — information, never gates)

These are checks to run against a built lineup, phrased as what the winner data says. None of them is a rule that costs a grade; only a call THIS slate's strategy makes can do that.

1. Pocket-QB captain → did the lineup carry 2–3 of his own pass-catchers? (A rushing QB needs only 1.)
2. WR captain → is his QB in FLEX, with at most ONE more same-team pass-catcher? (Only 8% of winners ran CPT WR + 2+ extra teammates.)
3. Passing-script build → is there a bring-back (an opposing pass-catcher)? **89% of passing-build winners had one.**
4. Kicker → paired with his own DST (the slog stack) rather than his own captain QB? (K appears in 34% of top lineups overall, only 19% next to his own CPT QB.)
5. DST → at most 3 players from the offense it faces (89% of winners).
6. Hard shape fact: **max 2 combined K+DST pieces**; 3+ won ~1% of the time. Never two kickers.
7. Double-QB (both QBs rostered, one or both at FLEX) is PFF's "closest thing to a cheat code"; ≥1 QB appears in ~96% of top lineups. Zero-QB wins ~5% — a large-field script bet only.

## Game scripts, weighted by Vegas

Every lineup is a story of how ONE game goes. Winner data by Vegas total:

- **Slog (total ≤42):** RB captains win 46% (WR 31%, QB 12%). Workhorse RBs, kickers, both DSTs.
- **Middle (42.5–48.5):** near-uniform — WR 29% / RB 27% / QB 25%. Mixed portfolio.
- **Shootout (49+):** WR captains win 47%. Double stack + bring-back. At 51+, RB captains are the leverage (the field rotates all-pass).
- **By spread:** favorite captains ~62% overall (same as the field — not leverage). At spreads of 7+, favorite captains win 80%, while underdog WRs (garbage-time script) carried ~40% fewer dupes — the dupe-cheap contrarian shape in blowout-priced games.
- **Team splits of 163 winners:** 3-3 (34%) and 4-2 (31%) dominate. 5-1/6-0 onslaught wins ~1 in 8–10 (the blowout bet — same logic as the NASCAR drafting-track chalk-dom carve-out). **2-4 tilted AWAY from the captain's team is the most under-used winning shape** (only 16% of the field builds it).

## Duplication — the format's defining problem

~30 relevant players means the chalk build is copied at scale (the 231-dupe Packers–Lions Milly winner). **Dupes are predicted by the PRODUCT of the six ownerships, not the sum.** Spending exactly $50,000 raises dupes; the captain's own ownership barely matters.

Uniqueness levers, roughly cheapest first: leave salary (**median winner left $1,400; only 7% of winners spent the full cap** — the opposite of Classic); one sub-3% FLEX piece (41% of winners); a kicker (in 40% of winners, massively under-used); the 2-4 split; two same-team RBs (~25% fewer dupes). One punt is a lever — three is a dead lineup (zero top-1% lineups carried 3+ min-priced players).

## Ownership envelope

Median winning lineup totaled **~167% ownership across 6 slots (~28% per slot)** — Showdown winners are chalkier per-slot than Classic (~13%), the same way RD4 SD and MMA run chalkier than their classic formats. Moderate chalk + one or two real leverage pieces, never an all-contrarian card. This is a RATE across winners, never a per-lineup quota (the codified sharp-envelope lesson applies here from day one).

`rules/shared/shark_baseline.json` has **no nfl_showdown block** — the user's NFL standings archive is Classic-only, so no SD envelope can be mined yet. The Grade tab degrades to "no envelope data" and the envelope accrues from logged SD autopsies (`shark_accumulate` under the `nfl_showdown` key).

## The user's contest profile

**5–20 entries in LARGE-field lotto contests** (unlike the SE/3-Max home game in other sports). That means:
- A **script portfolio**: one lineup per game story (shootout / slog / blowout-onslaught / garbage-time), weights set by the Vegas total + spread — never one "best" lineup entered repeatedly.
- Dupe awareness is load-bearing at these field sizes: product-of-ownership, salary-left, and the under-used shapes (2-4 split, kicker) are where large-field equity lives.
- Set diversity doctrine applies in full (`rules/shared/set_diversity.md`): diversity is a property of the SET, judged pairs-of-picks down.

## Pre-lock checks (information for the strategy writer, not gates)

- What are the script weights from the Vegas total + spread, and does each entered lineup name its script?
- Who is the over-captained player (CPT own vs the ~1-in-5 QB reality), and where do CPT own and FLEX own diverge on the vendor sheet?
- Does each passing build carry a bring-back?
- What is the highest-ownership-product chalk combination (the dupe magnet), and how many entries share it?
- Salary left: is any entry at exactly $50,000, and is that on purpose?
- K+DST count ≤2 per lineup; kicker not next to his own CPT QB unless the build says why.
- Anchor-Equivalence: which chalk anchors sit at similar own (including CPT-slot own) and are substitutable?
