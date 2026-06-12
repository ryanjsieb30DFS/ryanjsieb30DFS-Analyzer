# MLB Classic — 6.11.26 lineup portfolio

## Pre-flight checklist
- [x] Slate confirmed: mlb_classic — 5-game MAIN (ARI@MIA, MIN@DET, STL@NYM, TEX@KC, CHC@COL), first pitch 1:10 PM ET; bundle generated 2026-06-11 11:57, slate analysis written 2026-06-11, all article files dated 2026-06-11 — current slate
- [x] Projections loaded: Ship It Nation MLB Projections `mlb-projections-dk-20260611.csv` (99 players, exactly this slate's 10 teams); SIN calibration at 2 slates (<3 → note only, not weighted)
- [x] Venue file read: `rules/mlb_classic/parks/coors_field.md` (two-slate pattern: owned Coors side is an ownership tax — CHC capped at a mini, not the 5-man) + `citi_field.md` stub (91°, pivot stack's park); comerica/kauffman/loandepot stubs noted, not load-bearing for this build
- [x] Open lessons reviewed: 7 open — **applied:** pivot-budget-small-field-se (ONE pivot: the NYM stack; pitchers stay chalk; 4 sub-10% plays, 16.8% avg own ≈ winners' band), salary-enabler-pitcher-chalk (chalk arms discriminated by leash: Scott/Matthews kept, Phillips faded on his 2.4 avg IP — the leash mechanism, not his 21.9% ownership), se-chalk-pitcher-own-condensation (Scott KEPT because his 43.9% can condense to 55–70% — fading him is more binary than projected; the pivot is his own bats instead), blank-own-snapshot-artifact (verified — no blank-Own rows this slate; Feltner's 1.04% is real, and he's rejected on xERA/ceiling, blocking COL bats), untracked-entry-bypasses-loop + late-build-bailout (process: this audited lineup is the entry — no near-lock SaberSim swap; build lands with red-team time); **rejected:** weather-proof-dome-stack-pivot as a primary pivot (mechanism requires field ownership concentrated on the rain-exposed offense; here the #1 ownership cluster is CHC at sunny Coors and the dome team MIA has a weak 4.40 total — applied only as a tiebreak to underweight KC/TEX in the 31%-rain window)
- [x] Framework pre-lock checks: team-stack-driven 10-man roster (5-3 shape — the dominant winning shape in all 4 logged SE contests); no-hitter-vs-own-pitcher verified (Scott blocks STL — zero STL bats; Matthews blocks DET — zero DET bats, which also rules out the DET-3 mini alternative; NYM bats pair WITH Scott, not against him); Anchor-Equivalence run on all 3 flagged tiers (call below)
- [x] Prior results scanned: results.jsonl last 2 slates — best finishes top 40.1% / 39.9%, both played untracked SaberSim imports while the tracked build held the winning skeleton. Process target this slate: enter this lineup as audited

## Anchor-Equivalence call

1. **CHC quartet Busch/Happ/Hoerner/Bregman (28.0–30.7%)** — lineup rosters only ONE of the four (Bregman) and runs the lower-owned CHC alternatives (Suzuki 22.3%, Ballesteros 15.7%) for the rest of the mini. Satisfied.
2. **Pitcher class 21.9–25.2% (Cabrera/Matthews/Kelly/Montero/Phillips)** — lineup runs the in-class alternative: Matthews, the lowest-owned-enough member with the best mechanism (6.0 avg IP, 27.7 K%, 3.56 xERA) over Cabrera (Coors park tax), Kelly (7.65 xERA), and Phillips (2.4 avg IP leash). Satisfied per the 6/9 caveat that the alternative may come from inside the class.
3. **15.7–17.9% tier (Wacha/Castro/Swanson/Pasquantino/McGonigle/Ballesteros)** — Ballesteros used at C over the obvious tier-1 piece. Satisfied automatically.

---

## Lineup 1 — NYM-5 leverage stack + right-chalk arms (5-3)

**Thesis:** The Mets — the slate's biggest favorite (4.90 implied, -140) in a 91° park against the worst non-punt arm (Dobbins, 5.33 xERA) — out-hit their 34.7% combined ownership while their own ace Scott caps STL, with a near-field CHC-3 mini keeping Coors exposure without paying the 146% tax.

| Slot | Player | Team | Salary | Proj | Own% | Role |
|---|---|---|---|---|---|---|
| P | Christian Scott | NYM | $8,300 | 14.71 | 43.9% | Right chalk — best K profile (26.4%) vs 20.8%-owned STL; pairs with the stack |
| P | Zebby Matthews | MIN | $8,500 | 12.27 | 24.2% | Anchor-Equivalence alternative — best leash+K mechanism in the 22–25% class |
| C | Moises Ballesteros | CHC | $4,000 | 7.70 | 15.7% | CHC mini, lower-owned alternative to the 28–31% quartet |
| 1B | Jared Young | NYM | $2,600 | 7.98 | 6.1% | Stone's #1 ranked hitter on the slate (xwOBA +0.056); the stack's value engine |
| 2B | Marcus Semien | NYM | $3,000 | 7.66 | 4.8% | Stack leverage piece — sub-5% own in the slate's best favorite spot |
| 3B | Alex Bregman | CHC | $4,800 | 9.79 | 28.0% | The ONE quartet member — near-field Coors anchor per pivot-budget lesson |
| SS | Bo Bichette | NYM | $3,900 | 7.81 | 5.2% | Stack leverage piece at SS, sub-6% own |
| OF | Juan Soto | NYM | $6,000 | 10.26 | 11.3% | The stack's ceiling bat — highest-owned Met still only 11.3% |
| OF | Carson Benge | NYM | $3,700 | 8.32 | 7.0% | Fifth Met, completes the 5-man primary at 7% own |
| OF | Seiya Suzuki | CHC | $5,200 | 9.80 | 22.3% | CHC mini, lower-owned alternative to PCA (35.9%) and the quartet |

**Salary:** $8,300 + $8,500 + $4,000 + $2,600 + $3,000 + $4,800 + $3,900 + $5,200 + $6,000 + $3,700 = **$50,000** ✓ (≤ $50,000, fully spent per the winning-band target of ~$49.5K+)

**Shape:** NYM 5 (Soto/Young/Semien/Bichette/Benge) – CHC 3 (Bregman/Suzuki/Ballesteros) — the 5-3 that produced the most top-20 winners across all four logged SE contests. Avg ownership 16.8%, four sub-10% plays (Young 6.1, Semien 4.8, Bichette 5.2, Benge 7.0) — inside the validated ~15–16% / 4–5 sub-10% winning band with ONE structural pivot (the stack).

**What if?** What if the slate's best game environment isn't Coors — where 146% of the field is paying full price — but the 91° Citi Field game where the biggest favorite on the board sits at one-quarter the ownership?

---

## Lineup 2 — SIN preferred: Cubs 5 + Rangers 3 (chat-built, user-entered)

*(Built in chat 12:30 PM from SIN's stated build plan at the user's direction;
entered in the $5K Base Hit. Logged pre-lock per untracked-entry-bypasses-loop.)*

**Thesis:** SIN's preferred structure — the 6.05-implied Coors Cubs deliver as
the slate's engine while the cheap correlated TEX trio out-scores the field's
KC-side exposure in the 31%-T-storm game; wins on the chalk being right plus
better-chosen secondaries, not on a pivot.

| Slot | Player | Team | Salary | Proj | Own% | Role |
|---|---|---|---|---|---|---|
| P | Christian Scott | NYM | $8,300 | 14.71 | 43.9% | Right chalk, both lineups |
| P | Merrill Kelly | ARI | $7,000 | 11.85 | 23.6% | SIN's named SP2 path (dome game) |
| C | Carson Kelly | CHC | $3,800 | 7.87 | 14.3% | Within-stack discount over the 28–31% quartet |
| 1B | Michael Busch | CHC | $5,300 | 10.63 | 30.7% | Stack engine piece |
| 2B | Ezequiel Duran | TEX | $3,500 | 7.95 | 10.4% | TEX trio — cheap correlation per SIN |
| 3B | Josh Jung | TEX | $3,800 | 8.88 | 14.0% | TEX trio |
| SS | Dansby Swanson | CHC | $4,200 | 8.03 | 17.3% | Within-stack discount over Hoerner |
| OF | Pete Crow-Armstrong | CHC | $5,800 | 11.74 | 35.9% | Stack engine piece |
| OF | Ian Happ | CHC | $5,000 | 10.00 | 29.4% | Funded the Langford swap (Suzuki −$200) |
| OF | Wyatt Langford | TEX | $3,300 | 9.00 | 11.1% | Replaced Joc Pederson (late scratch) |

**Salary:** **$50,000** ✓ · avg own 23.1% · 5-3 shape (CHC 5 + TEX 3)

**What if?** What if the obvious slate simply happens — Cubs at Coors — and the
edge is refusing the storm-game KC side plus taking the within-stack discounts
(C.Kelly/Swanson over Hoerner/Bregman) the first-click field doesn't take?

Notes: SIN's named Cubs core (PCA/Hoerner/Busch/Bregman/Happ) cannot fit with
Scott+Kelly under the cap in any combination — this is the affordable five. The
TEX trio (2:10 start) stays late-swappable if Kauffman weather breaks. Own-pitcher
rule clean: TEX faces Wacha, CHC faces Feltner, no STL bats with Scott.

---

## Portfolio audit

- **Count:** 1 unique lineup for 2 SE entries (MLB $5K Base Hit, 490 fields; MLB $5K Chin Music, 1,189 fields) — matches the bundle's `unique_lineups_needed: 1`. The Chin Music field is marginally above the lesson's ~1,000-entry band; per the slate analysis, same regime, no second pivot added.
- **Player overlap / hedges:** N/A with one lineup — no competing-lineup risk, no shared-core duplication possible. The single structural bet is NYM over the field's Coors/Scott-fade money; the hedge against a NYM dud is that the lineup keeps the field's two best arms (Scott at 43.9%, Matthews as the class alternative) and near-field CHC exposure, so a chalk slate doesn't bury it.
- **Distinct-question check:** The one thesis (underowned biggest favorite beats the owned run environment) is distinct from the field's default build (CHC-5 Coors + Scott). No filler lineups added — the slate analysis supports exactly this one build for an SE pair.
- **Rule compliance:**
  - Roster: P, P, C, 1B, 2B, 3B, SS, OF×3 ✓ (Young at 1B, Semien at 2B, Bichette at SS, Ballesteros at C — all listed positions)
  - Salary $50,000 ≤ $50,000 ✓ (addition shown above)
  - No hitter vs own pitcher ✓ — Scott (NYM) faces STL: zero STL bats; Matthews (MIN) faces DET: zero DET bats. Note: this is why the DET-3 mini from the slate analysis's guidance is unavailable — Matthews blocks it — making CHC-3 the only compliant near-field mini from the recommended build.
  - Anchor-Equivalence ✓ — all three flagged tiers resolved with an alternative (see call above)
  - Team-stack-driven ✓ — 5-man primary, the codified core lever
  - Avoid-list honored ✓ — zero Phillips exposure (leash mechanism), no CHC-5 primary (two slates of ownership-tax evidence), no double-pivot (STL bats and the Scott fade both passed on; one pivot only)
- **Process:** per untracked-entry-bypasses-loop and late-build-bailout — this audited lineup is the entry for BOTH contests. Red-team it next, then enter it as-is. Two straight slates the tracked build beat the near-lock SaberSim swap.

### Audit addendum (12:40 PM, pre-lock — actual entries)

The user entered TWO different lineups (screenshot-confirmed, both tracked above):
- **$5K Chin Music (1,189 SE):** Lineup 1 (NYM-5 leverage stack) — the app-built lineup, entered as audited.
- **$5K Base Hit (490 SE):** Lineup 2 (Cubs 5 + Rangers 3) — chat-built at the user's direction to follow SIN's preferred structure.

**Distinct-question check (now 2 lineups):** L1 bets the under-owned biggest
favorite beats the owned run environment; L2 bets the obvious slate happens and
wins on secondary discrimination. Opposite sides of the same structural question
— acceptable for SE entries in different contests, not competing.

**Shared exposure:** Scott 2-for-2 (deliberate — the right-chalk read; a Scott
bust likely hurts both). Zero shared bats (L1 CHC mini: Ballesteros/Bregman/
Suzuki; L2 CHC stack: C.Kelly/Busch/Swanson/PCA/Happ). SP2 class covered by two
different members (Matthews L1, Kelly L2) per Anchor-Equivalence.

**Process note for the autopsy:** both entries exist in this file pre-lock —
untracked-entry-bypasses-loop honored for the first time in three slates. L2
departs from the app build's single-lineup recommendation (it adds the chalk-frame
build the analysis argued against); grade that call on its mechanism at autopsy.
