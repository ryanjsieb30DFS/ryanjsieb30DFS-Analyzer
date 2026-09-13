# ETR Research Digest — NFL Classic (2026-09-12)

**Status: APPLIED 2026-09-12 (user approved "apply everything"). C1–C5 and D1–D4 are live in `rules/nfl_classic/framework.md`, `philosophy.md` (belief 6), `lessons.yaml` (5 hypotheses), and `docs/dfs_research_library.md` Ch.7 item 8 + Ch.9 items 11–13. D5 is guidance for the user. Section E (tools) stays backlog. The Classic framework/philosophy were signed off by the user the same day (DRAFT label removed).**

Four Establish The Run pieces, saved as PDFs in this folder (text sidecars `.txt` beside each):

| # | Article | Author / date | Data behind it | Field type |
|---|---|---|---|---|
| 1 | Pass Rate Over Expectation (PROE) | ETR staff, 1/17/26 (2025 final data) | nflfastR play-by-play, xpass model | n/a — a reference table |
| 2 | NFL DFS: Putting the Sims to the Test (Parts 1–3) | Mike Leone, 9/6/26 | **DK Game Changer: single-entry, $1,500, ~275 entrants, 35 contests (2024 Wk2–21 + 2025 Wk4–21), 9,570 lineups**, post-lock Solver sims | **SMALL, SINGLE-ENTRY — the user's format** |
| 3 | Top NFL Narratives: True or False? | Sam Brott, 8/5/24 | 2021–23 play-by-play / Next Gen Stats | n/a — projection-level facts |
| 4 | When Is a Chalk Bring-Back Worth It? | Mike Leone, 9/3/26 | Two small-field contests (Game Changer ~275, Luxury Box 100), post-lock sims | **SMALL** |

Field-size note: article 2 is the first ETR study ever run on a **single-entry small field** — the same size class as the user's 28-contest archive (median ~2,300). It is the most on-point research in either digest so far. Article 4 is two contests and says so. Per the research-library rule, the user's own small-field data still wins any conflict once the local Classic ledger has slates.

---

## A. What these articles CONFIRM (already in `rules/nfl_classic/framework.md` or repo doctrine)

- **Sims are a threshold, not a ranking** (memory: sim-rank-not-gospel; Sim docs/sim_tools_playbook.md). ETR now says it in their own words: the sim "does a good job distinguishing bad from good, an okay job good from very good, and loses signal between very good and the absolute best." The top three sim-ROI buckets posted the same actual ROI. Rank-order bias on a sorted list is named as a trap.
- **Top 1% leads the picker, ROI is noisiest** (memory: 7/28 benchmark — Top 1% our most consistent winner-finder, ROI our noisiest). ETR: cash rate is well calibrated but over-confident at the very top; top-10 rate is the best-calibrated metric; sim ROI is directional only (every negative bucket was actually negative, every positive bucket positive, but the three best were flat). Leone is moving his own process from Sim ROI toward Top 10 and Top 1%.
- **Ownership convergence is the thing that breaks a lineup post-lock** (memory: 8/30 ownership report, stampede chalk +15–30 pts; Sim ⚡ ownership stress test). ETR's worst pre→post-lock crater: a stack whose two pieces went from 26%/31% projected to 43%/47% actual, total lineup ownership 264% → 311%, and the RB chalk combo from 48 lineups (15%) to 80 (25%).
- **Combo ownership matters more than single-player ownership** (set-diversity doctrine, Sim chalk-combos report). ETR counts the same thing: the RAW NUMBER of lineups sharing a chalk pair, not the percentages.
- **Diversify across entries; one bet per story** (no-competing-lineups, set-diversity). Leone: "multiple strong paths to a bink, even if that makes my sweat muddier."
- **Bring-back is real but conditional** (framework item 5 + 7). Article 4 sharpens the condition (Section B4) rather than contradicting it.
- **RB chalk is sturdy** (framework "Ownership as a price"). Article 4's Week 10 case: the fade that worked was the one that freed salary for THREE Tier-1 RB values — the RB tier was where the edge lived.

Nothing in Section A needs editing.

---

## B. NEW findings, by article

### B1. Article 2 — what a positive-sim lineup is actually worth in a ~275-entry single-entry contest

The only ETR study on the user's exact contest shape. 35 contests, 9,570 lineups, DK Game Changer (SE, $1,500, ~275 entries, ~22% paid, top-heavy).

1. **Positive-sim lineups win 1.65x as often as chance; negative-sim lineups 0.57x.** 23 of 35 winners (65.7%) simmed positive at lock, against a field where 60% of lineups sim negative. Average winner sim ROI +9.0% vs the field's −5.3%. Bad lineups still win: the Week 15 winner simmed −20% ROI with a 0.30% win rate (chance was 0.35%).
2. **Cash rate is calibrated, except at the very top.** Actual cash rate landed inside the simmed bucket in 4 of 5 buckets and rose monotonically. The top 0.9% of lineups by simmed cash rate under-delivered — the sim is over-confident about its favorite lineups.
3. **Top-10 rate is the best-calibrated metric.** Actual top-10 rate landed inside the simmed bucket in 5 of 5 buckets; the 377 lineups simmed above 7% top-10 hit 6.4% actual. Less top-end deterioration than cash rate. In Leone's bankroll model, simulated top-10 rate had "meaningfully more sway" on real results than cash rate.
4. **Sim ROI is directional, not precise.** All negative buckets actually negative, all positive buckets actually positive; worst two by sim were worst two by result; best three by sim were best three by result — but those best three were flat against each other (~+38% actual in the top bucket).
5. **Pre-lock ROI regresses ~20 points to post-lock.** 14 best pre-lock lineups from Week 5 dropped ~20 points mean/median ROI once the real field was in, yet 13 of 14 still simmed ≥ +40% post-lock. The real field is always a bit tougher than the projected field.
6. **The three ownership checks that predict a pre→post-lock crater** (Leone's checklist): (a) ownership of the CORRELATED pieces (did the stack come in above projection?), (b) COMBO ownership of the chalk pieces (how many lineups share the chalk pair — 48 vs 80 in the example), (c) ownership of the DIFFERENTIATION piece (the lowest-owned player: 8.2% projected → 14.8% actual killed one lineup; 8.2% → 3.5% actual made another). A lineup that goes 0-for-3 craters; 3-for-3 improves.
7. **Contest-to-contest ownership differs even at equal size.** A 3-max 300-entry field and a single-entry 300-entry field draw different ownership. Play similar contests consistently so the ownership read is learnable.
8. **Metrics that matter, in ETR's own list:** Sim ROI, Cash Rate, Top 1%, 1st, Top 10. **AVG and CEILING points are irrelevant** — "all we care about is beating our competition; sometimes that comes from winning low-scoring slates."
9. **"IKB" (I Know Better) as a freeroll.** Find lineups that sim well on BASE projections, then use projection disagreements only to choose among them. Edit ≤10 players, 1–2 points each. IKB a CORRELATED set when possible: one correct assumption ("this team throws and scores more") lifts 3–4 players at once, so a neutral-sim lineup becomes positive on one call instead of several.
10. **Bankroll reality for a single-entry small field (Leone's model, overfit but useful):** even the best lineups are under 50% to profit in a season; a "Solid" lineup runs ~+16% ROI long-term yet profits only ~1 season in 3; 39% of profitable seasons come from a bink; at a 20x-buy-in bankroll the outcome is binary (profit or bust), at 40x a good lineup is under 10% to bust. Leone's own 22 Game Changer entries: −57.6% realized ROI while routinely simming positive. Not a doc change — a reality check the user already lives by (ROI stays in the third-party app; percentile + process are the scoreboard).
11. **Leone's four-step process:** (1) lineups above a minimum pre-lock threshold (Top 10 / Top 1% / ROI — pick one), (2) filter to the ones robust to an ownership miss for THIS contest, (3) choose among the survivors by feel or small projection edits — never by the exact ROI rank, (4) when playing several, diversify.

### B2. Article 4 — when the chalk bring-back is worth it (two small-field contests)

1. **A chalk bring-back is +EV inside its stack when it is (a) the best value at its position, (b) a natural fit for the roster, and (c) the QB it rides with is NOT over-owned.** Week 9: Chase was 66% owned on Caleb Williams stacks vs Nacua 13%, yet the sims rated the two versions equal (slightly favoring Chase) — because Chase was the top raw AND value WR, the Nacua swap changed nothing else in the lineup, and Caleb was only 11% owned (4th-highest QB), so the leverage was already in the QB.
2. **The same chalk WR OUTSIDE his stack simmed negative.** Chase had negative mean sim ROI on non-Caleb teams (positive on only 4 of 15 QBs, two of those +1%). Rule of thumb: **a chalk pass-catcher from the chalk game belongs inside the stack he correlates with, or not at all.**
3. **Fading the obvious bring-back is −EV unless the fade UNLOCKS something.** Week 10, Luxury Box (100 entries): Mac Jones stacks with the Nacua bring-back were mostly negative-sim; the one lineup without Nacua worked because fading him freed salary for three Tier-1 RB values (the other nine Mac stacks were forced into double-TE builds on a slate with no TE value) AND opened a WR slot for a mini-correlation (Deebo + Jameson Williams). "The strongest bring-back fades are those that unlock a meaningful roster-construction advantage."
4. **Small fields magnify the fade.** One lineup without the bring-back among 10 Mac stacks is a real edge; the raw count of competing lineups is what matters. "Smaller-field tournaments may offer clearer opportunities to omit the chalk bring-back — more opponents hand-build or follow traditional correlation rules."
5. **Pivot-for-variance without losing EV:** Nacua-for-Chase on Bears stacks did not sim worse; it created a higher-variance lineup at the same EV. Direct 1-on-1 leverage is fine when it costs nothing else.

### B3. Article 3 — narratives, the parts that touch DFS

Projection-level; ETR's projections already price most of it, so these are TIEBREAKERS, never double-counted:

1. **Domes (TRUE):** +13% TDs; QBs +12% DK points; RB/WR/TE +6%; WR/TE receiving TDs +22%/+33%; QBs scramble 12% less; **DSTs −15% DK points**. Use: when two game environments are otherwise equal, the dome game is the stack; a dome is a strike against the DST in that game. (Consistent with the SD digest's dome-kicker finding.)
2. **Mobile QB → his RB gets more right-tail carries (TRUE, small):** +0.1–0.2 yards per carry, but the gain is in home-run frequency — "a ceiling tiebreaker."
3. **Backup QBs target backup WRs +2–3% (TRUE);** backup QBs do NOT target TEs more (FALSE). Use: in the forced-value read after a QB injury, the WR2/WR3 inherits slightly more than the TE.
4. **Freak athletes (TRUE-ish):** the No. 1 athletic score at each position met or beat projection on average every season (Allen, Henry, Metcalf, Kittle); the edge is ceiling size, not hit rate. A tiebreaker for the leverage piece.
5. **Multiple high-value players from one offense CAN all hit (FALSE narrative):** the "not enough mouths" fear is already priced. Supports double-stacking.
6. Mobile QBs vs man coverage (TRUE, scramble tail) and the college-teammate "shower narrative" (case by case) are noted for completeness; no DFS action.

### B4. Article 1 — PROE

A reference table (2025 final; **2026 data starts after Week 2**): each team's pass rate, PROE (called pass rate minus expected pass rate from game context), neutral-situation PROE, red-zone PROE, last-4-games PROE. ETR's point: PROE is the stable half of future pass rate (game script is the volatile half), so it is a better read of team INTENT than raw pass rate. Use: a game-selection input for "pick the game before the players" — two high-PROE teams in one game is the shootout shape; a high red-zone PROE team leans its TDs to WR/TE over RB. The PDF's text extraction separated the numbers from the team names, so the table is not machine-readable here; read it on the site when 2026 data lands.

---

## C. CORRECTIONS to existing repo docs

1. **`rules/nfl_classic/framework.md` — "The winning stack" item 5 (bring-back real but modest) and item 7 (skip when blowout).** Add the small-field conditions from B2: inside the stack the chalk bring-back is fine even at high ownership when he is the best value and the QB is not the chalk QB; outside his stack the same chalk WR is a negative; fade the obvious bring-back only when the fade buys a construction edge (a third Tier-1 RB, a mini-correlation), and small fields are where that fade counts most.
2. **`rules/nfl_classic/framework.md` — "Pre-lock checks."** Add Leone's three ownership checks (correlated pieces, chalk-combo count, differentiation piece) and the "pre-lock ROI regresses ~20 points" expectation. These replace nothing; the current list has no ownership-miss check.
3. **`rules/nfl_classic/framework.md` — "Pick the game before the players."** Add PROE as an intent input and the dome tiebreaker (+12% QB, −15% DST). Mark both as already-priced-in-projections: tiebreakers, never double counts.
4. **`rules/nfl_classic/philosophy.md` — belief about sims.** The draft says the sim ranks on Win% / Top 1%. Add the ETR-confirmed framing: the sim separates bad from good reliably and very good from best poorly; the pick is made INSIDE the good set by ownership robustness and thesis, never by ROI rank. (Already repo doctrine; now sourced.)
5. **`docs/dfs_research_library.md` Ch.7 (sim industry).** Note that ETR published a calibration of its own post-lock sims on a ~275-entry SE field: positive-sim 1.65x win rate, top-10 rate best calibrated, ROI directional. Our 7/28 benchmark reached the same ordering on our own archive (Top 1% most consistent, ROI noisiest).

---

## D. PROPOSED additions (draft text, for approval)

### D1. `rules/nfl_classic/framework.md`

Replace items 5 and 7 of "The winning stack" with:

> 5. **Bring-back (stack + 1 opposing pass-catcher): 36% of winners vs 31% of the field.** Real but modest; two or more opposing pieces shows no edge. **The chalk bring-back is fine INSIDE the stack** even at very high conditional ownership (Chase was 66% on Caleb Williams stacks, Week 9 2025, and simmed as well as the 13%-owned pivot) when three things hold: he is the best raw-and-value play at his position, he fits the roster without forcing anything else, and the QB he rides with is not the chalk QB (Caleb was 11%, the 4th-highest-owned QB). **The same chalk WR outside his stack is a negative** (Chase simmed negative on 11 of 15 non-Caleb QBs). A chalk pass-catcher from the chalk game belongs in the stack he correlates with, or not at all.
> 7. **Skip or fade the bring-back only when the fade buys something.** A blowout-shaped ceiling story (huge favorite steamrolling) is one reason. The other is roster construction: in a 100-entry contest (Week 10 2025) the one Mac Jones stack WITHOUT the obvious Nacua bring-back worked because the freed salary bought three Tier-1 RB values and a WR slot for a mini-correlation, while the nine stacks WITH Nacua were forced into double-TE builds on a slate with no TE value. **Small fields are where this fade counts most** — more opponents hand-build by the correlation rulebook, and one lineup without the bring-back among ten stacks is a measurable edge. A direct 1-for-1 pivot (Nacua for Chase) that changes nothing else raises variance at the same EV; that is allowed, not required.

Add to "Pick the game before the players":

> - **Team intent:** ETR's Pass Rate Over Expectation (PROE — how much more a team throws than the game situation predicts) is the stable half of future pass rate; game script is the volatile half. Two high-PROE teams in one game is the shootout shape; a high red-zone PROE leans that team's touchdowns to WR/TE. 2026 numbers start after Week 2 (`docs/etr_research/…pass_rate_over_expectation.pdf`).
> - **Dome tiebreaker:** in domes QBs score ~12% more, WR/TE ~6% more (receiving TDs +22%/+33%), and DSTs ~15% LESS. ETR's projections already carry most of this — it breaks ties between two otherwise-equal game environments and counts against the dome DST; it is never added on top.

Add to "Pre-lock checks":

> - **The three ownership checks** (ETR's post-lock autopsy of a ~275-entry SE field): did the CORRELATED pieces come in above projection? how many lineups share the chalk COMBO (count them — 48 vs 80 lineups is a different contest)? did the DIFFERENTIATION piece stay low? Expect the best pre-lock lineups to give back ~20 points of sim ROI once the real field is in; a lineup that fails all three checks craters, one that passes all three improves.
> - **Metrics:** Win% / Top 1% / Top 10% decide; cash rate is calibrated but over-confident at the very top; the sim separates bad from good well and very good from best poorly — pick inside the good set, never by ROI rank.

### D2. `rules/nfl_classic/philosophy.md`

Append to the beliefs list:

> 6. **The sim is a threshold, and the pick is made inside it.** ETR's own calibration on a ~275-entry single-entry field (35 contests): positive-sim lineups win 1.65x as often as chance, negative-sim 0.57x, and the three best sim buckets post the same real ROI. So: build to the threshold, then choose by ownership robustness (the three checks) and the one-sentence thesis — never by the exact ROI order. "AVG" and "CEILING" points do not matter; beating the field does, and some weeks that is a low-scoring slate.

### D3. `rules/nfl_classic/lessons.yaml` — candidate hypotheses (status: hypothesis, 0 confirmations, external data)

- `nfl_classic_chalk_bringback_inside_stack` — A chalk pass-catcher from the chalk game scores as a positive inside the stack he correlates with and as a negative outside it. Why: the stack pays his ceiling twice; naked, his ownership is a pure tax. Counts as confirmed when: on a logged slate, the chalk bring-back's top-10 lineups are stack-mates of his QB more often than not, and his naked lineups finish below the field median.
- `nfl_classic_bringback_fade_needs_a_reason` — Fading the obvious bring-back beats keeping him only when the fade buys a construction edge (a third Tier-1 RB, a mini-correlation). Why: the fade's leverage alone is small in a stack that is not over-owned; the salary it frees is where the edge lives. Counts as confirmed when: a logged no-bring-back winner or top-10 lineup carries a visibly different construction from the with-bring-back stacks.
- `nfl_classic_positive_sim_wins_more` — The user's entered lineup sims positive on Top 1% / Win% at lock more often when it finishes top 10 than when it does not. Why: ETR measured 1.65x / 0.57x on a same-size SE field. Counts as confirmed when: the picker check in the autopsy shows the top-10 finisher was positive-sim in ≥ 6 of the first 10 logged slates.
- `nfl_classic_ownership_miss_three_checks` — A lineup that misses on all three ownership checks (correlated pieces up, chalk combo count up, differentiation piece up) finishes below a lineup that passes all three, at equal pre-lock sim. Why: the real field is tougher than the projected one by ~20 points of ROI and the miss concentrates in exactly these three places. Counts as confirmed when: the Sim's vendor_calibration ownership deltas for the entered lineup's stack + combo + low-own piece predict its percentile direction on ≥ 4 of 6 logged slates.
- `nfl_classic_dome_stack_tiebreaker` — Between two equal game environments, the dome game's stack outscores the outdoor one and the dome DST underscores. Why: +12% QB / −15% DST in domes historically. Counts as confirmed when: logged slates show the dome-game stack's actual points above projection more often than the outdoor comparison's.

### D4. `docs/dfs_research_library.md` — Chapter 7 addendum and Chapter 9 candidates

- Ch.7: one paragraph on ETR's post-lock calibration (B1 items 1–4) next to our 7/28 benchmark.
- Ch.9 candidates: "chalk bring-back inside the stack or not at all"; "fade the bring-back only for a construction edge"; "pick inside the threshold by the three ownership checks".

### D5. For the user, not a doc change

- **Contest consistency:** ETR found ownership differs between a 3-max and a single-entry contest of the same size. Playing the same few contests each week makes the ownership read learnable; the contest screener rows accrue per contest for that reason.
- **Bankroll framing:** in a single-entry small field, even a genuinely good lineup profits in well under half of seasons and most profitable seasons come from one bink. Judge the process by percentile and by the three checks, not by a season's ROI (this is already the repo's rule).

---

## E. Tool implications (backlog, no commitments)

1. **Sim, Lineups tab — already aligned.** Default rank is Top 1%; Win% / Top 1% / Top 10% / Cash% are the contract; ETR's "AVG / CEILING are irrelevant" matches sim-rank-not-gospel. Possible addition: a raw **"Top 10 (count)"** column beside Top 10% — ETR found the raw top-10 rate the best-calibrated metric and it is the one that maps to a 275-entry field (Top 10% there is 27 places, not 10).
2. **Sim, ⚡ ownership stress test — extend to the three checks.** Today it boosts the top-3 chalk ×1.4. Leone's version boosts the STACK pieces and the DIFFERENTIATION piece and re-sims; a per-lineup "ownership robustness" flag (does its Top 1% survive stack +15 pts / low-own piece ×2 / chalk combo +10 lineups?) is the same machinery pointed at three places. Fits the diversifier-first workstream.
3. **Sim, chalk-combos report — count in lineups, not only %.** The set-diversity combo flags report percentages; add the raw lineup count at the declared field size (48 vs 80 is how ETR reads it).
4. **Analyzer, Grade tab — post-lock three-checks line.** After a slate logs, compare projected vs actual ownership for the entered lineup's stack pieces, its chalk pair, and its lowest-owned player, and print pass/fail per check next to the percentile. Pure data-join; the vendor_calibration rows already carry the deltas.
5. **Sim, projections editor — IKB freeroll guard.** Show, for an edited slate, how many players were edited and by how much (ETR's own limit: ≤10 players, 1–2 points), and keep the base-projection sim result beside the edited one so an edit is a freeroll, not a rebuild.
6. **Not building:** a bankroll simulator (ROI lives in the third-party app); PROE table ingestion (it is a read, and 2026 data is weeks away).
