# ETR Research Digest — NFL Classic, Week 1 weekly columns (2026-09-12, evening)

**Status: APPLIED 2026-09-12 (user: "apply everything"). C1–C5 are live in `rules/nfl_classic/framework.md` (DST pressure, ownership premium, pace/Fangio, one-game cap) and `philosophy.md` (belief 7). D1–D5 are in `lessons.yaml` as hypotheses. Section E (PDF-table parsers) stays backlog. Mirrored to the Sim the same day.**

**Site rule:** DraftKings only. Every FanDuel section, price and ownership number in these pieces was skipped.

Ten Week 1 pieces were reviewed tonight. Nine are this-Sunday slate material and go to the Slate Data tab (the user uploads them). One, *Macro vs. Micro*, is a FanDuel-only column by its own opening line and is not loaded anywhere. Four of the nine also carry **evergreen** content — a method, a number or a rule that is as true in Week 9 as in Week 1 — and those four are saved in this folder with text sidecars:

| # | Article | Author / date | Data behind it | Field type |
|---|---|---|---|---|
| 1 | GPP Leverage: Week 1 | Sam Brott, 9/12/26 | Milly Maker + The Spy ownership vs. results, Weeks 1–17, 8+ game slates; matched player pairs | LARGE (Milly ~150k) and MID (The Spy). Brott himself plays small-field DK |
| 2 | Biggest OL vs. DL Mismatches, Week 1 | Brandon Thorn, 9/11/26 | 2025 season game results; PFF-style line grades, 1–32 ranks | n/a — football data |
| 3 | Snaps and Pace: Week 1 | Pat Thorman, 9/9/26 | nflfastR pace / PROE, 10 seasons of Fangio-DC games | n/a — football data |
| 4 | Establish The Million: Week 1 | Mike Leone + Drew Dinkmeyer (livestream notes), 9/12/26 | Their own high-stakes DK builds and ownership reads | SMALL (Leone) and LARGE (Dink) — both stated |

Reminder from the user (9/12/26): **Silva and Thorman are football minds, not DFS minds.** Their pieces are the football layer — who plays, how much, how fast, which line wins — and feed the game-story and stack reads. They are never a play, fade, or ownership call. The same holds for Thorn.

Field-size note: Brott's matched-pair table is Milly Maker and The Spy data, which are far bigger fields than the user's single-entry and 3-max contests. Per the research-library rule, the user's own small-field ledger wins any conflict once it has slates. The Establish The Million notes are the only piece here where a small-field player states a small-field number.

---

## A. What these pieces CONFIRM (already in `rules/nfl_classic/framework.md` or repo doctrine)

- **Ownership carries information; a leverage twin is not free.** Brott's matched pairs (same position, salary within $500, projection within one point, one player at 2x+ the ownership of the other): the higher-owned player outscored his twin about 60% of the time in the Milly Maker and 54% in The Spy in Week 1, and reached 25 DK points more often. This is the framework's "ownership as a price" section and the Anchor-Equivalence rule, now with a number attached.
- **One disagreement per lineup, the rest fits it.** Brott: "A lineup can benefit quite a bit from getting one meaningful disagreement right, especially when the rest of its pieces fit that outcome." This is the thesis-required rule and the no-competing-lineups rule in ETR's words.
- **Every QB is paired.** Across all ten pieces no writer builds a naked QB; the framework's "QB with no teammates won 6% vs 17% of the field" stands.
- **Bring-back = a non-DST opponent.** Every bring-back named this week is a skill player (Olave, Vele, Juwan Johnson into DET stacks). Matches the tool rulebook.
- **DST punts with intent, never against your own stack.** Thorn's mismatch list backs the three DSTs ETR ranks highest (JAX #2 mismatch, NYJ #6, PHI #1) with a pass-rush reason, which is what the framework's DST line asks for.
- **Game selection before players.** Thorman's pace buckets and the GPP Game Scores table are two more inputs to "pick the game before the players." Nothing new in principle.

Nothing in Section A needs editing.

---

## B. NEW findings, by article

### B1. Brott — GPP Leverage (Week 1 ownership efficiency, matched pairs)

1. **Week 1 projections are not worse.** ETR's fantasy-point projections "have historically been roughly as accurate in Week 1 as in all other weeks of the season." So the case for extra guessing against the projections in Week 1 (the "I know better" edit) is no stronger than any other week.
2. **The higher-owned twin usually wins.** Same position, same price band, same projection band, 2x the ownership: the popular one outscored the other ~60% (Milly) / 54% (Spy) in Week 1 and hit 25 DK points more often.
3. **The trade-off has a size.** In Week 1 Spy contests the lower-owned twin carried about one-quarter of the ownership while reaching 25 points about 60% as often. In the Milly Maker the lower-owned twin carried about one-third of the ownership and reached 25 points only about one-third as often. Later in the season the ceiling gap narrowed a lot in both contests while the ownership gap stayed.
4. **So the rule of thumb:** in Week 1 the ownership premium is better earned than later in the year. Respect it more in Week 1; lean on the low-owned twin more as the season goes on.
5. **The column's weekly method** is a per-game "what the market assumes vs. the counter-thesis" read. That is a structured way to state the one disagreement per lineup.

### B2. Thorn — OL vs. DL (D/ST is a pressure bet)

1. **"Just 2.5% of games last season ended in a shutout, and only 9.7% ended with one team being held to six points or fewer."** So chasing the points-allowed bonus is "a fool's errand"; DK D/ST points come from sacks, fumbles, interceptions and touchdowns, and those come from QB pressure.
2. **The objective is to project QB pressure**, which is the OL vs. DL mismatch. The column ships 1–32 ranks for every OL and DL weekly plus a ranked mismatch list.
3. **Second-order use:** a QB stack whose OL faces a top pressure mismatch is a weaker stack and a weaker bring-back source that week.

### B3. Thorman — Snaps and Pace (volume drags that persist)

1. **Definitions:** "situation neutral" = within seven points, first three quarters, minus the final two minutes of the first half. Neutral pace = seconds of play clock used. PROE = pass rate over expectation from ETR's model.
2. **A Fangio-tree defensive coordinator is a volume drag for years.** In Fangio's eight DC seasons the games he coached ranked 32nd, 31st, 30th, 30th, 25th, 18th, 16th and 14th in average combined offensive plays. New DCs from his tree (Parker in DAL this year) inherit the effect.
3. **Cowboys games have finished top five in combined snaps six of the last seven years.** The opposite persistence.
4. **Weekly pace buckets** (Up in pace / Slow-paced slog) are a game-selection input beside total and spread.

### B4. Establish The Million — small-field reads from a small-field player

1. **How many players from one game is too many depends on field size.** Dinkmeyer: "In a small field contest, you could get into 6 players but you can run into very similar lineups. Would limit it to 5 players in large field."
2. **Three-RB builds.** Leone: "Interested in playing 3 RBs on DK this week. Top lineups are using more 3 RB than the field and it won't be super owned this week." A slot-mix read, not a rule.
3. **Chalk verdicts by position** ("good chalk / bad chalk") and a per-position ownership order are stated every week. That is the sturdy-vs-fragile chalk read the framework already asks for.
4. **Late-swap trap:** a punt priced with no same-salary alternative (Mayer at $2,900 this week) needs two-for-two swap room if the late games matter.

---

## C. PROPOSED edits to repo docs (each needs a yes)

- **C1. `rules/nfl_classic/framework.md` → "Roster construction" DST line.** Add: grade a DST by the pass-rush mismatch (opponent OL rank vs. own DL rank), not by opponent points allowed — only 2.5% of games are shutouts and 9.7% hold a team to six or fewer. Source: Thorn.
- **C2. `rules/nfl_classic/framework.md` → "Ownership as a price."** Add the matched-pair number: at equal price and projection, the higher-owned twin outscores the lower-owned one about 60% of the time in Week 1 and reaches 25 DK points more often; the lower-owned twin buys about one-quarter to one-third of the ownership at a real ceiling cost that shrinks later in the season. Frame it as the price of leverage, not a fade of leverage. Source: Brott (large/mid fields; local ledger wins on conflict).
- **C3. `rules/nfl_classic/framework.md` → "Pick the game before the players."** Add two persistence inputs: a Fangio-tree DC drags combined plays for years (rank list above); Cowboys games run top-five in snaps. Add Thorman's pace bucket beside total and spread. Source: Thorman.
- **C4. `rules/nfl_classic/philosophy.md` → Week 1 belief.** Add one sentence: ETR's projections are about as accurate in Week 1 as any other week, so Week 1 earns no extra guessing against them. Source: Brott.
- **C5. `rules/nfl_classic/framework.md` → "Duplication."** Add the field-size cap on one game's player count as a stated small-field observation: 6 from one game is possible in a small field but breeds near-duplicate lineups; 5 is the large-field limit. Source: Dinkmeyer.

## D. PROPOSED hypotheses for `rules/nfl_classic/lessons.yaml` (status: hypothesis until the ledger confirms)

- **D1. `nfl_classic_dst_pressure_not_points_allowed`.** A DST attached to a top-6 pass-rush mismatch outscores a DST picked for opponent points allowed. Confirmed when: over 6 logged slates, the mismatch-backed DSTs beat their projection more often than the points-allowed picks.
- **D2. `nfl_classic_week1_ownership_premium`.** In Week 1 the higher-owned of two matched twins hits his ceiling more often than later in the season. Confirmed when: the user's own Week 1 autopsies (this season and next) show the chalk twin outscoring the leverage twin at a higher rate than mid-season autopsies do.
- **D3. `nfl_classic_one_game_cap_by_field`.** Six players from one game in a small field produces measurable duplication. Confirmed when: the Sim's dupe report or the standings show a 6-from-one-game lineup duplicated in a small field.
- **D4. `nfl_classic_three_rb_underowned`.** Three-RB builds appear in top lineups more than in the field. Confirmed when: the stack-centric autopsy (Phase 4) shows 3-RB slot mix over-represented among winners on 4 of 6 slates.
- **D5. `nfl_classic_fangio_tree_volume_drag`.** Games with a Fangio-tree DC finish bottom-half in combined plays. Confirmed when: logged slates with such a game show its total plays below the slate median 4 of 6 times.

## E. Tool backlog (information panels, never rules — build after the first Classic autopsy)

- **E1.** Parse the **GPP Game Scores** table out of the uploaded PDF in `articles/nfl_classic/` into `game, game_total, dk_game_score` and show it beside the Sim's stack rows. The user uploads the PDF weekly; no paste, no ETR connector (their site is subscription-only, and pulling it with the user's login is vendor scraping, which is banned).
- **E2.** Parse **The Rundown** header (kickoff, total, spread, forecast, wind) the same way.
- **E3.** Parse **Thorn's 1–32 OL and DL ranks** and derive a per-game pressure gap for the DST section of the player pool.
- **E4.** Parse the **DFS Top Plays** rank list as a DK value-tier feed joined to salary.
- **E5.** A **cheap-WR volume filter** on the ETR projection CSV: salary ≤ $5,000 and projected targets ≥ 5 (Jack Miller's screen). The CSV already has the columns.
- **E6.** Weather from a free public service for outdoor stadiums (already in the saved MCP backlog).

## F. Not applied / skipped

- *Macro vs. Micro* (Stringfield): FanDuel-only by design. Skipped entirely.
- Any FD price, ownership or roster note in the other nine pieces.
- Silva's Matchups and Thorman's pace notes for games not on the DK main slate (SF–LAR, DAL–NYG, DEN–KC, NE–SEA): per the user, only Classic-slate teams are researched this week.
