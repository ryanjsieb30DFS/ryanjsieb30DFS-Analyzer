# NFL Classic Week 2 — Sunday 9/20/26 — full process log for the master review

Written live during the slate by Claude (Sim + Analyzer session). Read this with the autopsy tonight.
Contest: NFL $20K Screen Pass [3 Entry Max], 1,568 entries, $15, top-heavy (1st $2,000, paid to 360th).

## 1. Timeline

| Time (ET) | Event |
|---|---|
| 08:57–09:06 | 10 ETR PDFs + ETR projections file (45) land in Downloads. Two PDFs cut short: Silva's Matchups ends p26/34 (MIA@SF write-up missing); The Rundown ends p14/26 (games after NO@BAL missing). |
| ~09:20 | Both Streamlit servers restarted (they predated the 9/19 commits). |
| 09:07 | Projections uploaded to Sim (365 rows). 09:09 Build 1 = full file, no pool, no stack rows (rehearsal). |
| 09:25 | Analyzer: slate strategy (3,087 words), player pool (109 in / 256 out), strategy contract, contests. Pool run finished (Week 1 timeout fix held). |
| 09:54 | Pool LOCKED (hard) in Analyzer; 09:55 Sim Include flags = 109 exactly. |
| 09:57–10:03 | ETR Discord (2hats1mike): moving off Wentz/Herbert (rain CHI-MIN, McConkey may play), Love gets steam, Purdy "safest for upside / protected from steam", now considering Maye + Bryce Young, "some Dak chalk" exposure. Saved to articles/nfl_classic/. Nothing rerun. |
| 09:58 | Build 2 (pool applied, no stack rows). 10:09 Build 3 (5 player groups, no stack rows). 10:30 Build 4 = identical to Build 3 (changes did not take; 9,542/9,618 same rows). |
| 10:40 | Build 5 = real pool: 9,590 rows, stack rows QB≥1 RB/WR/TE same team + QB exactly 0 opp DST, min salary 49,700, same 5 groups. |
| 10:49 | Picker selected 5667 / 5410 / 8021 (see §5). |
| 11:x | ETR final files (46, 47): no meaningful change; ownership identical on all rows all day. |
| ~12:00 | Final user set chosen (see §6). 12:35 Sim session file rewritten with the final selection (manual override recorded). |
| ~15:20 | Live standings pulled (contest-standings-195825300.csv); late-swap recommendations issued (§8). |

## 2. Inputs and their known quality
- ETR NFL Classic: 365 players, 13 games. Week 1 calibration on this vendor: own corr 0.96 (MAE 1.3), proj corr 0.63 (MAE 5.6), ceiling exceeded 12.8% of the time. Ownership is the trustworthy input.
- Ownership NEVER updated across files 45→46→47 (365/365 identical). Field model never saw the Love steam / McConkey news.
- Only one contest simmed (the $20K 3-Max). No second field for cross-check.

## 3. Analyzer output (09:25)
- Strategy headline: stack game is the decision; WAS@DAL 51.5 total, fastest pace, ETR game score 2.6; pivots MIA@SF (2.2), MIN@CHI (1.1), NO@BAL (1.0). Keep Bijan (sturdy chalk), move QB to Daniels/Purdy/Lamar, low-owned TE + DST, three entries = three game stories: one WAS@DAL, one MIA@SF or NO@BAL, one cheap-QB stack.
- Anchor-Equivalence: Henry/Jones/Javonte (28–30% each, hold one); Dak 15.9% vs Wentz 11.1% as the two "safer" stacks; Daniels/Purdy/Lamar within 1.5 proj of Dak at 1/3–1/2 own.
- Underweights (max 1 entry each): Wentz, Aaron Jones, Schultz, Andrews, Golden, Mayer, Bucs DST; Ravens DST lean fade.
- Build-rules block written: salary_min 49,800; ≤5 from WAS@DAL; ≤1 of Schultz/Andrews/Mayer; 4 DST-vs-own-QB pairs; portfolio: ≥1 non-Dak stack, ≥1 CMC/Saquon, ≤1 Dak, ≤1 each underweight.
- "Field vs Sharp": field = Bijan + one of Henry/Jones/Javonte + Schultz/Andrews + Dak/Lamb/Pickens + Bucs/Ravens; sharp = ~14% own/slot, one sub-5% piece most lineups, unique 99%.
- Pool: QB 16 in/10 out, RB 21/29, WR 39/44, TE 16/21, DST 17/9. Core: Dak, Purdy, Daniels (QB); Bijan, CMC, Javonte (RB); 1 Core TE.

## 4. Sim builds and what they showed
- Build 2 (no rules): QB slot flat 6–7% each; Bijan 24.7%, McBride 15.3, 49ers DST 12.1, JSN 12.7, Saquon 11.9; own/slot 9.8; 99% with a sub-5 piece. Double stacks 43%, naked QB 11%. Median top-1 1.14.
- Build 3/4 groups: [Bijan+Schultz ≤1], [Schultz/Henry/Jones/Lamb ≤1], [Andrews/CMC/Jefferson/G.Wilson ≤1] (UNEXPLAINED — not in strategy; capped CMC), [≥2 of 52 Core/Good] (inert), [8 underweights ≤1]. Strategy's lineup rules (49,800 floor, WAS@DAL ≤5, DST-vs-QB pairs, twins group) were NOT loaded. Median top-1 1.07.
- Build 5 (stack rows on): every lineup has a QB teammate; 0 DST-vs-own-QB; 2+ catchers 45%; naked QB (RB-only mate) 6%; median top-1 1.26, p90 2.29, median ROI −4.1 (from −13.5). Stack row was ≥1, not the strategy's 2. Min salary 49,700 not 49,800. 412 rows still had ≥5 from WAS@DAL; 137 rows two twins.
- Sim's top-1 rises monotonically with stack depth (Purdy rows: 2 SF w/ CMC+bring-back 1.70 → 5 SF 3.76 median). Love rows same (3 GB 1.33 → 6 GB 5.08). Correlation model is v1 literature-anchored, UNFITTED — this is a belief, not evidence. Week 1 evidence only validates QB+2 catchers (50% of top-10 vs 29% field).
- Week 1 calibration: sim field 16–20 pts too LOW at every percentile, 33 pts low at 1st place → top-1 rates are overstated and median-heavy lineups look better than true tail lineups.
- QB share in top-200 by top-1 (Build 5): Purdy 70, Love 34, Herbert 20, Maye 16, Dak 15, Bryce Young 14, Nix 11.

## 5. Picker (10:49) and its faults
- Picked 5667 (Love/Bijan/Javonte/Saquon/Watson/Reed/G.Wilson/Mayer/Titans), 5410 (Purdy/Javonte/CMC/Evans/Chase/Deebo/Kittle/Schultz/Titans), 8021 (Nix/Dobbins/Henry/Waddle/P.Washington/Vele/Engram/Bijan/49ers).
- Faults: Titans DST ($2,100, 5.5 proj) in 2 of 3 (salary dump — Week 1 failure mode repeated); Mayer + Schultz (underweights) as fillers; 5667 own/slot 15.7 with NO sub-5 piece; 5410 had 2 RBs (TE at FLEX); zero WAS@DAL; picker flagged the Javonte+Titans pair itself. Strategy screen removed 2,937 rows but did not prevent any of this.

## 6. User constraints added live, and the selection chain
Constraints (in order): no Titans DST (≤1, then 0) · RB at FLEX · no QB+4 team stacks · QB + at most 2 catchers · at most 2 bring-backs · no Warren at FLEX · fewer than 3 Dolphins around Purdy.

| Step | Set | P(≥1 top-1%) |
|---|---|---|
| Picker | 5667/5410/8021 | 13.2 |
| Titans out, 3 RB | 8132/2798/8021 (Purdy 5-man / Love 5-man / Nix) | 13.3 |
| QB+3 cap | 6545/7746/8021 (Purdy / Bryce Young / Nix) | 12.4 |
| QB+2, ≤2 bring-backs | 9364/7570/2973 (Purdy / Lawrence / Maye) | 9.5 |
| Warren out | 9364/7570/4489 | 9.1 |
| ≤2 Dolphins | **3095/7570/4489** (FINAL) | 9.2 |

FINAL SET (Sim Lineup numbers, Build 5):
- 3095 Purdy · Bijan · Henry · Evans · Malik Washington · Caleb Douglas · Kittle · FLEX Stevenson · Seahawks DST — $49,700, proj 133.0, top-1 3.79, own 12.0
- 7570 Lawrence · CMC · Jeanty · Waddle · Parker Washington · Quentin Johnston · Strange · FLEX Dobbins · Bears DST — $49,900, proj 126.7, top-1 3.18, own 8.6
- 4489 Maye · Hampton · Irving · Chase · Metcalf · Doubs · Hunter Henry · FLEX Hubbard · Seahawks DST — $49,900, proj 126.6, top-1 2.48, own 8.7
Overlap: only Seahawks DST (in 2). Bijan ×1, CMC ×1. All 11 portfolio rules pass. No WAS@DAL (deliberate hold by user after the Daniels 2774 option was offered).
AS ENTERED (from live standings): entry 1/3 used **Buccaneers DST** instead of Seahawks (user change at entry); 2/3 and 3/3 as above.

Known soft spots stated before lock: cheap fillers are salary artifacts (Malik Washington $4,000, Douglas $3,700, Q. Johnston $5,000); Seahawks DST twice; 3095 is $100 under the 49,800 floor; the top game absent; all three DSTs $3,000–3,500 while every DST prices at 2.1–2.6 pts/$1k (the DST money is exactly the WR-filler money).

## 7. Questions the autopsy must answer
1. Stack depth: did top-10 lineups run QB+2 or QB+4/5? (sim says deeper; evidence stops at 2)
2. Did any cheap Miami receiver (Douglas / M. Washington) matter? Did the Achane-less Purdy build cost us?
3. Dak/Lamb/Pickens: did the field's shared stack win, or did sharing cost them? Was holding zero WAS@DAL right?
4. DST: did winners punt DST ($2,100–2,700) and spend at WR, or pay $3,500+? (fix capture code: field rosters are de-duped and not aligned to scores, so this could not be measured for Week 1)
5. Did Love steam materialize? Golden actual own vs 17.3 projected.
6. Did the sim's top-1 ordering (3095 > 7570 > 4489) predict our finish order?
7. Titans DST actual vs the two Seahawks/Bears picks.
8. Warren's line vs the Hubbard swap.

## 8. Late swap (≈15:20 ET, standings file contest-standings-195825300.csv)
Early games final/late: ATL-CAR, CIN-HOU, BAL-NO, CHI-MIN, GB-NYJ, CLE-TB, NE-PIT, PHI-TEN. Late: MIA@SF, WAS@DAL, JAX@DEN, LV@LAC, SEA@ARI.
Standing at pull: 3/3 78.4 banked (rank 194, 2 left); 1/3 36.1 (rank 1,177, 5 left; Bijan 11.1, Henry 17.7, Stevenson 4.3, Bucs 3.0); 2/3 10.0 (rank 1,553, 8 left). Field median banked 49.6; leader 128.3 with 1 player left.
Recommendations issued (enumerated over late-game pool players, blend proj/ceiling, QB+2 exactly, ≤2 bring-backs, ≤3 per team):
- 1/3: NO change (Dak fill gains only +4.7 proj / +6.5 ceiling; keeps the two trailing entries on different late games).
- 2/3: Lawrence→Dak, Jeanty→Achane, P. Washington→Lamb, Waddle→Pickens, Q. Johnston→Caleb Douglas, Strange→Mayer; keep CMC, Dobbins, Bears. Proj 119.5→129.0, ceiling 211→224.5, $50,000. With a WAS bring-back (McLaurin/Diggs) best was 126.4 / 219 — declined for ceiling. Any-FLEX search gave the same answer.
- 3/3: Hampton→Javonte Williams, Seahawks→49ers DST ($10,200 exact). Ceiling for the two spots 44.5→49.3.
Whether the user executed these swaps: NOT confirmed at time of writing — check the final standings.

## 9. Tool fixes for Week 3 (process, not rules)
- Stack row default = QB + 2 same-team WR/TE (strategy asked for 2; Build 5 ran ≥1).
- Load the strategy's lineup rules block exactly (49,800 floor, WAS@DAL ≤5, twins group, DST-vs-QB pairs); drop the unexplained Andrews/CMC/Jefferson/Wilson group and the inert "≥2 of 52" group.
- Picker: DST salary/projection floor (no $2,100 dumps), flag any sub-$4,000 non-DST filler, require ≥1 sub-5% piece per lineup, honor RB-at-FLEX if the user wants it as a builder knob.
- Sim: fit or at least sanity-check the NFL correlation loadings against Week 1+2 top-10 stack shapes; recalibrate field strength (16–20 pts low in Week 1).
- Capture: store field rosters aligned to entry scores (needed for DST-spend and stack-depth questions).
- Sim: a second contest simmed each week for cross-check; a late-swap tab that enumerates fills for open slots from the pool (today this was done ad hoc in Python).
- Builds 3→4 "settings did not take" needs a repro: stack rows/min salary edited in UI were not in the build snapshot.
