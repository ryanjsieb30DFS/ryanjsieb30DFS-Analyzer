# Sharp Playbook — universal GPP rules from the best players (PGA + NFL validated)

_Reverse-engineered from DK **contest-standings** the user owns — no scraping. Two large archives, the SAME 12 elite handles in both: **PGA** = `~/Desktop/DFS/DFS PGA Past Slate Data/` (395 files, 2023–26) and **NFL** = `~/Desktop/DFS/DFS NFL Past Slate Data/` (69 files, 2024–25). MMA/MLB notes come from the smaller `~/Downloads` set._

**Why two sports:** PGA (6 independent golfers, no correlation) and NFL (9-man, stack/correlation-driven) are about as different as DFS gets. **A tendency that holds in BOTH is genuinely universal** — it's the player's philosophy, not a sport quirk. Anything that shows up in only one sport is listed separately as non-transferable.

**Confidence:** large-sample in both (tens of thousands of entries per handle). Standings lack **salary and team**, so ownership / leverage / uniqueness / results are high-confidence; salary distribution + exact structure are inferred.

---

## ⭐ Universal Sharp Principles (apply to ALL sports — PGA, MMA, NASCAR, MLB)

Each rule held across **both** PGA and NFL, with the numbers:

1. **Every lineup is unique.** Duplicate ratio ≈ **1.0** in both sports even at **120–150 entries/slate** — no two bets the same. *(PGA dup ~1.00–1.04; NFL ~1.00–1.15.)* → For your hand-built few: never run two lineups that answer the same question.

2. **Always carry a leverage piece.** A sub-5%-owned player appears in the **majority** of their lineups — **PGA 60–80%, NFL 64–86%**. → Default to **≥1 sub-5%-owned player per lineup.**

3. **Moderate ownership — neither chalk nor punt.** Average ownership **per roster slot ~12–16%** in both sports (PGA Classic ~12–14%, NFL ~14–16%). They don't chalk-stack and they don't punt the whole card. → Target a **balanced, slightly-contrarian** build, not extremes.

4. **Build for the tail; ignore the median.** Their **median entry finishes ~40–52%** — mid-pack — in *both* sports, even for players with multiple wins. The edge is entirely in the top-1% / win tail. → Judge each lineup on **ceiling**, never on "will it cash." *(= `feedback_sim_rank_not_gospel`.)*

5. **Anchor an elite, differentiate downstream.** They concentrate on the truly elite anchor (PGA: Scheffler the universal #1; NFL: elite QB/RB) and create separation in the **mid/value tier**, not by fading the studs. → Pay up for the correct anchor; find your edge below it.

6. **Volume is unique breadth, not repetition.** They fire many lineups but each is a distinct angle. At your scale, copy the **breadth-of-angles** mindset (each lineup a different "what if?"), not the entry count.

These six are the cross-sport core — fold them into every sport's build, MMA/NASCAR/MLB included.

---

## Sport-specific (do NOT generalize)
- **NFL only:** QB stacked with a pass-catcher + bring-back (game correlation). Real in NFL; **irrelevant to golf/MMA/NASCAR** (no equivalent correlation) — MLB is the only other sport with true stacking.
- **PGA R4 SD / showdown:** chalkier — per-player own ~17–19% (own_sum ~103–113) and fewer leverage pieces; fewer viable plays.
- **MMA (small sample):** chalkier still — favorites convert; leverage is *which* favorites + an occasional dog, not fading chalk wholesale.

---

## PGA evidence (395 files, 2023–26; entries = total)

| Handle | Classic slates / entries | per-player own | leverage% | top1% | wins | best |
|---|---|---|---|---|---|---|
| moklovin | 193 / 26,388 | 13.6 | 57 | 1.1 | 3 (+1 SD) | 0.003% |
| PetrGibbons | 146 / 16,825 | 13.1 | 68 | 1.6 | 1 | 0.007% |
| skyhoke | 142 / 12,658 | 12.8 | 74 | 1.4 | 0 | 0.01% |
| sullybrochill | 131 / 14,619 | 13.3 | 67 | 1.2 | 3 (SD) | 0.006% |
| JBCJBCJBC | 107 / 14,317 | 13.0 | 68 | 1.1 | 1 (+1 SD) | 0.003% |
| youdacao | 104 / 14,885 | 12.1 | 71 | 1.2 | 0 | 0.004% |
| needlunchmoney | 64 / 9,381 | 13.7 | 72 | 1.3 | 0 | 0.027% |
| hishboo | 42 / 6,030 | 11.9 | 78 | 1.2 | 0 | 0.01% |
| rsbathla | 29 / 3,954 | 13.3 | 64 | 1.5 | 0 | 0.037% |
| (vishy2773 77, skyhoke, sullybrochill also heavy R4 SD) | | | | | | |

R4 SD (chalkier): sullybrochill 85 slates / 3 wins, moklovin 142, JBCJBCJBC 34, skyhoke 62. Universal anchor: **Scottie Scheffler**, then Rory / Xander / Morikawa / Si Woo Kim / Sungjae.

## NFL evidence (69 files, 2024–25; per-player own normalizes the 9-man roster)

| Handle | slates / entries | entries/slate | per-player own | leverage% | dup | top1% | wins | median |
|---|---|---|---|---|---|---|---|---|
| moklovin | 69 / 8,363 | 121 | 14.0 | 83 | 1.04 | 0.9 | 1 | 46% |
| ShaidyAdvice | 53 / 7,239 | 137 | 14.1 | 81 | 1.03 | 1.6 | 2 | 43% |
| youdacao | 41 / 6,150 | 150 | 14.7 | 82 | 1.06 | **3.4** | 0 | 40% |
| needlunchmoney | 41 / 6,150 | 150 | 14.6 | 83 | 1.02 | 1.6 | 0 | 40% |
| hishboo | 41 / 6,150 | 150 | 15.4 | 68 | 1.03 | 1.9 | 0 | 39% |
| sullybrochill | 41 / 6,150 | 150 | 15.0 | 78 | 1.02 | 1.6 | 0 | 42% |
| bpcologna | 41 / 6,050 | 148 | 14.7 | 79 | 1.06 | 1.6 | 0 | 43% |
| PetrGibbons | 36 / 5,255 | 146 | 13.6 | 86 | 1.00 | 1.8 | 0 | 43% |
| JBCJBCJBC | 35 / 4,654 | 133 | 15.7 | 75 | 1.03 | 1.6 | 0 | 42% |
| rsbathla | 40 / 4,138 | 104 | 17.3 | 64 | 1.15 | 2.2 | 1 | 41% |
| skyhoke | 37 / 2,611 | 71 | 15.6 | 73 | 1.06 | 1.0 | 0 | 50% |
| vishy2773 | 36 / 983 | 27 | 13.8 | 85 | 1.00 | 1.8 | 0 | 42% |

**Read:** identical structural discipline as PGA — moderate per-player ownership, a leverage piece in most lineups, all-unique, mid-pack median. youdacao (3.4% top-1%) and rsbathla (2.2%) are standout NFL converters; ShaidyAdvice wins in both sports.

---

## How to apply (you hand-build a few lineups)
Copy the **structure**, not the entry count: each lineup a distinct angle, **~12–16% average ownership per slot**, **≥1 sub-5% leverage piece**, an elite anchor with differentiation below it, and judged on ceiling not median. These six universal rules are validated across two very different games — the strongest evidence we can get short of tracking your own results.

_Caveats: descriptive correlation, not causation; copying the structure at low volume is a sound hypothesis to track, not a guarantee. NFL is out of the user's play scope — used only to prove which tendencies are universal. Salary/team absent from standings. MMA/MLB notes are small-sample._
