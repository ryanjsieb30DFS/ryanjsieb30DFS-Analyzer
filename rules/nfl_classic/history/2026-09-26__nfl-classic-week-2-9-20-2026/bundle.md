# Slate bundle — NFL Classic
_Generated 2026-09-20 09:15 · slug `nfl_classic` · sport `nfl`_
_**DraftKings only.** Ignore every FanDuel (FD) section, column, price, ownership number, or roster rule in any file below — the user never plays FD._

This file consolidates everything for the active slate: the article/slate-data files AND every loaded vendor projection. Read it, then read the article files it points to + the strategy docs + the projection tables below, then write the slate strategy to `data/slate_analysis/nfl_classic.md`.

## Contests
- 1 contest(s), 3 total entries
  - **NFL $20K Screen Pass [3 Entry Max]** (3-Max): field 1,568, my entries 3/3, payout **Top-heavy**, prize multiple 0.85x
_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, contrarian builds and the leverage-away reads matter most. **Flat** → many similar payouts; a tight high-floor-of-ceiling thesis competes fine. **Balanced** → in between. Surface it in `## Slate at a glance`; never a play/fade command._
_The home game is **small-field GPPs — Single Entry, 3-Max, and 5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still ceiling-and-leverage over median (GPP), but each of your few lineups is a distinct thesis — no 150-max MME spray. Field size within this range tunes the contrarian dial; it never flips you to a cash/floor game._

## Shark reality — how the pros play YOUR contests
FORWARD-LOOKING, accumulated from your logged autopsies. The observed sharp-envelope target for your small-field GPPs: match the STRUCTURE (own/slot, leverage rate, anchor discipline, all-unique). Surface it as the target; do NOT issue play/fade commands.
- **Your nfl shark envelope:** own/slot **13.897**, leverage **87.338%**, anchor-exposure **0.389**, unique **98.6%**.
| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |
|---|---|---|---|---|---|---|
| **moklovin** | 22 | 9/22 | 29.8 | 27.27 | 0.49 | ~29.8% own/slot |
| **youdacao** | 6 | 2/6 | 17.6 | 50.0 | 0.47 | carries a sub-5% leverage piece in most lineups, ~17.6% own/slot |
| **ShaidyAdvice** | 3 | 1/3 | 23.8 | 33.33 | 0.78 | ~23.8% own/slot |

## Slate data files (read these — they are the primary input)
Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so screenshots work). Note in the output if anything couldn't be parsed.
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__DFS Top Plays_ Week 2 _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__ETR’s Cheap WR Volume_ Week 2 _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__Establish-The-Million-Week-2.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__Establish-The-Show-Week-2.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__Evan Silva’s Matchups_ Week 2 _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__GPP Game Scores  Week 2 .pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__GPP Leverage_ Week 2 _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__The Rundown_ Week 2 _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__Thorman’s Snaps and Pace_ Week 2 _ Establish The Run.pdf`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/articles/nfl_classic/2026-09-20__Thorn_ Biggest OL vs. DL Mismatches, Week 2 _ Establish The Run.pdf`

## Projections (vendor data — read and use these too)
Every vendor projection loaded for this slate. Use these ownership/projection numbers alongside the articles. Where the two vendors disagree — or where a vendor disagrees with the articles — that gap is signal worth surfacing.

### ETR NFL Classic — `DraftKings NFL DFS Projections -- Main Slate (45).csv` (365 players)
| name | salary | ownership | proj_points | ceiling | opponent | team | position |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bijan Robinson | 8200 | 37.5 | 24.0 | 38.6 | CAR | ATL | RB |
| Jaxon Smith-Njigba | 8100 | 9.0 | 18.2 | 31.8 | @ARI | SEA | WR |
| Christian McCaffrey | 8000 | 19.7 | 21.4 | 35.8 | MIA | SF | RB |
| Justin Jefferson | 7800 | 18.7 | 18.0 | 31.8 | @CHI | MIN | WR |
| Ja'Marr Chase | 7600 | 17.1 | 18.6 | 32.5 | @HOU | CIN | WR |
| Lamar Jackson | 7300 | 3.2 | 20.8 | 30.6 | NO | BAL | QB |
| CeeDee Lamb | 7300 | 28.6 | 18.8 | 33.1 | WAS | DAL | WR |
| Derrick Henry | 7200 | 30.4 | 20.4 | 34.8 | NO | BAL | RB |
| Chris Olave | 7200 | 5.8 | 15.0 | 27.2 | @BAL | NO | WR |
| Saquon Barkley | 7000 | 8.7 | 17.3 | 30.6 | @TEN | PHI | RB |
| Trey McBride | 6900 | 7.3 | 16.7 | 28.9 | SEA | ARI | TE |
| Chase Brown | 6900 | 6.1 | 15.5 | 27.1 | @HOU | CIN | RB |
| Caleb Williams | 6800 | 2.0 | 19.6 | 29.4 | MIN | CHI | QB |
| Ashton Jeanty | 6800 | 13.2 | 18.0 | 30.2 | @LAC | LV | RB |
| DeVonta Smith | 6800 | 4.8 | 14.1 | 26.3 | @TEN | PHI | WR |
| De'Von Achane | 6700 | 5.5 | 16.8 | 29.0 | @SF | MIA | RB |
| Jalen Hurts | 6700 | 1.0 | 19.7 | 29.6 | @TEN | PHI | QB |
| Joe Burrow | 6600 | 2.1 | 18.3 | 27.9 | @HOU | CIN | QB |
| Omarion Hampton | 6600 | 8.4 | 15.7 | 28.3 | LV | LAC | RB |
| Mike Evans | 6600 | 6.1 | 13.8 | 26.2 | MIA | SF | WR |
| Jaylen Waddle | 6500 | 6.7 | 14.0 | 26.1 | JAX | DEN | WR |
| David Montgomery | 6500 | 5.6 | 14.8 | 26.9 | CIN | HOU | RB |
| Dak Prescott | 6400 | 15.9 | 21.7 | 32.2 | WAS | DAL | QB |
| Javonte Williams | 6400 | 28.0 | 18.7 | 32.3 | WAS | DAL | RB |
| Emeka Egbuka | 6400 | 2.6 | 13.2 | 25.0 | CLE | TB | WR |
| D'Andre Swift | 6300 | 4.7 | 14.8 | 26.9 | MIN | CHI | RB |
| George Pickens | 6300 | 25.9 | 16.2 | 30.0 | WAS | DAL | WR |
| Jayden Daniels | 6300 | 7.8 | 20.3 | 30.0 | @DAL | WAS | QB |
| Christian Watson | 6200 | 9.7 | 14.1 | 27.4 | @NYJ | GB | WR |
| Ladd McConkey | 6200 | 3.7 | 13.1 | 24.8 | LV | LAC | WR |
| Breece Hall | 6200 | 14.0 | 15.6 | 27.7 | GB | NYJ | RB |
| Brock Purdy | 6200 | 7.0 | 21.1 | 31.4 | MIA | SF | QB |
| Tetairoa McMillan | 6100 | 7.2 | 14.0 | 26.4 | @ATL | CAR | WR |
| Tee Higgins | 6100 | 5.4 | 13.2 | 25.4 | @HOU | CIN | WR |
| Drake Maye | 6100 | 5.0 | 19.1 | 29.3 | PIT | NE | QB |
| Bucky Irving | 6100 | 13.6 | 16.2 | 28.1 | CLE | TB | RB |
| Drake London | 6000 | 1.5 | 13.1 | 24.7 | CAR | ATL | WR |
| Justin Herbert | 6000 | 3.5 | 18.9 | 28.8 | LV | LAC | QB |
| Travis Etienne Jr. | 6000 | 0.4 | 10.6 | 19.6 | @BAL | NO | RB |
| Garrett Wilson | 6000 | 17.4 | 15.7 | 28.4 | GB | NYJ | WR |
| Jeremiyah Love | 5900 | 0.3 | 11.4 | 20.5 | SEA | ARI | RB |
| Jordan Love | 5900 | 10.2 | 19.1 | 29.3 | @NYJ | GB | QB |
| Parker Washington | 5900 | 12.9 | 14.6 | 27.0 | @DEN | JAX | WR |
| Chuba Hubbard | 5800 | 8.0 | 14.5 | 25.9 | @ATL | CAR | RB |
| Courtland Sutton | 5800 | 1.4 | 10.9 | 21.6 | JAX | DEN | WR |
| Trevor Lawrence | 5800 | 5.4 | 18.7 | 28.2 | @DEN | JAX | QB |
| Luther Burden III | 5700 | 6.4 | 11.5 | 21.9 | MIN | CHI | WR |
| Bo Nix | 5700 | 6.3 | 19.4 | 29.3 | JAX | DEN | QB |
| Rhamondre Stevenson | 5700 | 7.4 | 14.7 | 26.6 | PIT | NE | RB |
| Bhayshul Tuten | 5600 | 0.2 | 10.8 | 20.1 | @DEN | JAX | RB |
| Baker Mayfield | 5600 | 3.3 | 18.2 | 27.1 | CLE | TB | QB |
| Chris Godwin Jr. | 5600 | 1.5 | 11.0 | 20.9 | CLE | TB | WR |
| Rome Odunze | 5500 | 0.5 | 10.0 | 21.0 | MIN | CHI | WR |
| C.J. Stroud | 5500 | 2.6 | 16.7 | 26.0 | CIN | HOU | QB |
| Jadarian Price | 5500 | 4.5 | 13.2 | 24.6 | @ARI | SEA | RB |
| Jacory Croskey-Merritt | 5500 | 2.4 | 12.3 | 22.8 | @DAL | WAS | RB |
| Michael Wilson | 5400 | 0.7 | 10.1 | 19.8 | SEA | ARI | WR |
| Bryce Young | 5400 | 3.2 | 17.0 | 26.5 | @ATL | CAR | QB |
| Quinshon Judkins | 5400 | 0.5 | 11.8 | 21.4 | @TB | CLE | RB |
| Jaylen Warren | 5400 | 0.5 | 11.7 | 20.9 | @NE | PIT | RB |
| Kyle Monangai | 5300 | 0.2 | 8.9 | 17.4 | MIN | CHI | RB |
| MarShawn Lloyd | 5300 | 2.3 | 12.5 | 23.5 | @NYJ | GB | RB |
| Tyler Shough | 5300 | 5.5 | 17.5 | 26.4 | @BAL | NO | QB |
| Deebo Samuel Sr. | 5300 | 3.3 | 10.8 | 21.0 | MIA | SF | WR |
| Tony Pollard | 5300 | 0.2 | 9.3 | 17.9 | PHI | TEN | RB |
| Stefon Diggs | 5300 | 7.0 | 12.2 | 22.7 | @DAL | WAS | WR |
| Malik Willis | 5200 | 2.7 | 15.6 | 24.5 | @SF | MIA | QB |
| TreVeyon Henderson | 5200 | 0.2 | 8.4 | 16.6 | PIT | NE | RB |
| DK Metcalf | 5200 | 15.4 | 13.9 | 25.9 | @NE | PIT | WR |
| Terry McLaurin | 5200 | 14.2 | 12.4 | 24.1 | @DAL | WAS | WR |
| Jalen Coker | 5100 | 12.0 | 12.7 | 24.2 | @ATL | CAR | WR |
| Chris Rodriguez Jr. | 5100 | 0.1 | 5.4 | 11.9 | @DEN | JAX | RB |
| Aaron Jones Sr. | 5100 | 28.7 | 16.3 | 28.5 | @CHI | MIN | RB |
| Jordan Addison | 5100 | 2.6 | 10.1 | 20.7 | @CHI | MIN | WR |
| Aaron Rodgers | 5100 | 0.0 | 14.3 | 22.4 | @NE | PIT | QB |
| Kenny Gainwell | 5100 | 0.3 | 9.8 | 18.6 | CLE | TB | RB |
| Carnell Tate | 5100 | 0.4 | 9.2 | 18.1 | PHI | TEN | WR |
| Jacoby Brissett | 5000 | 0.5 | 15.6 | 24.4 | SEA | ARI | QB |
| Colston Loveland | 5000 | 6.2 | 12.2 | 23.0 | MIN | CHI | TE |
| J.K. Dobbins | 5000 | 5.5 | 12.6 | 24.0 | JAX | DEN | RB |
| Kirk Cousins | 5000 | 0.0 | 12.6 | 20.3 | @LAC | LV | QB |
| Quentin Johnston | 5000 | 7.2 | 11.4 | 22.6 | LV | LAC | WR |
| Romeo Doubs | 5000 | 1.9 | 10.2 | 20.6 | PIT | NE | WR |
| Rachaad White | 5000 | 0.2 | 8.4 | 16.5 | @DAL | WAS | RB |
| Tyler Allgeier | 4900 | 0.2 | 7.8 | 15.3 | SEA | ARI | RB |
| Marvin Harrison Jr. | 4900 | 0.8 | 9.4 | 19.0 | SEA | ARI | WR |
| Tucker Kraft | 4900 | 4.0 | 11.0 | 21.5 | @NYJ | GB | TE |
| Jakobi Meyers | 4900 | 1.6 | 10.4 | 19.9 | @DEN | JAX | WR |
| Rico Dowdle | 4900 | 0.2 | 11.0 | 19.9 | @NE | PIT | RB |
| Drew Lock | 4900 | 0.5 | 15.4 | 24.2 | @ARI | SEA | QB |
| Cam Ward | 4900 | 0.0 | 12.6 | 20.0 | PHI | TEN | QB |
| Jonathon Brooks | 4800 | 0.1 | 6.2 | 13.1 | @ATL | CAR | RB |
| Chris Brooks | 4800 | 0.1 | 6.9 | 14.2 | @NYJ | GB | RB |
| Brian Thomas Jr. | 4800 | 0.4 | 9.2 | 19.0 | @DEN | JAX | WR |
| Geno Smith | 4800 | 1.3 | 13.8 | 22.5 | GB | NYJ | QB |
| Dallas Goedert | 4800 | 1.5 | 10.7 | 20.2 | @TEN | PHI | TE |
| Tyjae Spears | 4800 | 0.0 | 8.4 | 16.2 | PHI | TEN | RB |
| Brian Robinson Jr. | 4700 | 0.1 | 5.5 | 12.2 | CAR | ATL | RB |
| Matthew Golden | 4700 | 17.3 | 12.4 | 23.9 | @NYJ | GB | WR |
| Tank Bigsby | 4700 | 0.0 | 1.6 | 5.4 | @TEN | PHI | RB |
| Keaton Mitchell | 4600 | 0.1 | 6.2 | 13.4 | LV | LAC | RB |
| Carson Wentz | 4600 | 11.1 | 15.6 | 24.6 | @CHI | MIN | QB |
| Alvin Kamara | 4600 | 0.1 | 5.4 | 11.6 | @BAL | NO | RB |
| Makai Lemon | 4600 | 0.3 | 7.7 | 16.0 | @TEN | PHI | WR |
| George Kittle | 4600 | 6.3 | 11.3 | 21.9 | MIA | SF | TE |
| Wan'Dale Robinson | 4600 | 1.8 | 10.0 | 18.7 | PHI | TEN | WR |
| Kyle Pitts Sr. | 4500 | 0.2 | 8.2 | 16.4 | CAR | ATL | TE |
| Deshaun Watson | 4500 | 0.0 | 13.7 | 21.0 | @TB | CLE | QB |
| Emari Demercado | 4500 | 0.0 | 2.7 | 7.9 | WAS | DAL | RB |
| Jayden Reed | 4500 | 6.6 | 11.3 | 22.2 | @NYJ | GB | WR |
| Woody Marks | 4500 | 0.2 | 7.4 | 14.8 | CIN | HOU | RB |
| Tre Tucker | 4500 | 0.8 | 10.0 | 19.7 | @LAC | LV | WR |
| Kendre Miller | 4500 | 0.0 | 2.9 | 7.7 | @BAL | NO | RB |
| Kaelon Black | 4500 | 0.2 | 7.6 | 15.7 | MIA | SF | RB |
| George Holani | 4500 | 0.2 | 7.7 | 15.4 | @ARI | SEA | RB |
| Kaytron Allen | 4500 | 0.0 | 1.7 | 5.9 | @DAL | WAS | RB |
| Rashod Bateman | 4400 | 0.6 | 9.1 | 18.8 | NO | BAL | WR |
| Mark Andrews | 4400 | 20.0 | 13.4 | 24.5 | NO | BAL | TE |
| Samaje Perine | 4400 | 0.1 | 5.3 | 11.5 | @HOU | CIN | RB |
| Sean Tucker | 4400 | 0.0 | 1.8 | 6.2 | CLE | TB | RB |
| Jalen McMillan | 4400 | 0.1 | 6.0 | 13.6 | CLE | TB | WR |
| Antonio Williams | 4400 | 0.1 | 6.0 | 13.6 | @DAL | WAS | WR |
| Kaleb Johnson | 4300 | 0.0 | 0.6 | 2.4 | @NYJ | GB | RB |
| Mike Washington Jr. | 4300 | 0.0 | 3.3 | 8.3 | @LAC | LV | RB |
| Kimani Vidal | 4300 | 0.0 | 0.9 | 3.4 | LV | LAC | RB |
| Mack Hollins | 4300 | 1.2 | 8.5 | 17.9 | PIT | NE | WR |
| Dontayvion Wicks | 4300 | 0.3 | 8.2 | 17.2 | @TEN | PHI | WR |
| Rashid Shaheed | 4300 | 0.1 | 6.9 | 15.0 | @ARI | SEA | WR |
| Cooper Rush | 4200 | 0.0 | 12.0 | 19.6 | CAR | ATL | QB |
| Justice Hill | 4200 | 0.2 | 7.9 | 16.4 | NO | BAL | RB |
| Denzel Boston | 4200 | 0.3 | 7.6 | 15.8 | @TB | CLE | WR |
| Jonah Coleman | 4200 | 0.0 | 3.8 | 9.9 | JAX | DEN | RB |
| Pat Bryant | 4200 | 1.5 | 8.7 | 17.7 | JAX | DEN | WR |
| Jaylen Wright | 4200 | 0.0 | 0.9 | 3.4 | @SF | MIA | RB |
| Corey Kiner | 4200 | 0.0 | 0.4 | 1.5 | PIT | NE | RB |
| Devaughn Vele | 4200 | 3.4 | 9.9 | 19.0 | @BAL | NO | WR |
| Braelon Allen | 4200 | 0.1 | 6.0 | 12.9 | GB | NYJ | RB |
| Will Shipley | 4200 | 0.0 | 2.6 | 7.4 | @TEN | PHI | RB |
| KC Concepcion | 4100 | 1.8 | 9.8 | 18.6 | @TB | CLE | WR |
| Harold Fannin Jr. | 4100 | 1.7 | 9.5 | 17.7 | @TB | CLE | TE |
| Ameer Abdullah | 4100 | 0.0 | 0.4 | 1.5 | @DEN | JAX | RB |
| Cooper Kupp | 4100 | 0.1 | 6.3 | 13.9 | @ARI | SEA | WR |
| Calvin Ridley | 4100 | 0.0 | 4.4 | 10.8 | PHI | TEN | WR |
| Bam Knight | 4000 | 0.0 | 0.3 | 1.2 | SEA | ARI | RB |
| Rasheen Ali | 4000 | 0.0 | 0.4 | 1.4 | NO | BAL | RB |
| AJ Dillon | 4000 | 0.0 | 0.4 | 1.5 | @ATL | CAR | RB |
| Roschon Johnson | 4000 | 0.0 | 0.3 | 1.0 | MIN | CHI | RB |
| Tahj Brooks | 4000 | 0.0 | 0.3 | 1.4 | @HOU | CIN | RB |
| Jaleel McLaughlin | 4000 | 0.0 | 1.2 | 3.9 | @TB | CLE | RB |
| Michael Burton | 4000 | 0.0 | 0.1 | 0.4 | @TB | CLE | RB |
| Raheim Sanders | 4000 | 0.0 | 3.3 | 8.2 | @TB | CLE | RB |
| Hunter Luepke | 4000 | 0.0 | 2.2 | 6.5 | WAS | DAL | RB |
| Tyler Badie | 4000 | 0.0 | 3.5 | 8.7 | JAX | DEN | RB |
| Adam Prentice | 4000 | 0.0 | 0.5 | 1.9 | JAX | DEN | RB |
| British Brooks | 4000 | 0.0 | 0.1 | 0.6 | CIN | HOU | RB |
| Kayshon Boutte | 4000 | 2.2 | 9.0 | 18.8 | CIN | HOU | WR |
| LeQuint Allen Jr. | 4000 | 0.0 | 1.2 | 4.0 | @DEN | JAX | RB |
| Dylan Laube | 4000 | 0.0 | 1.2 | 3.8 | @LAC | LV | RB |
| Connor Heyward | 4000 | 0.0 | 1.1 | 3.7 | @LAC | LV | RB |
| Alec Ingold | 4000 | 0.0 | 0.3 | 1.2 | LV | LAC | RB |
| Tre' Harris | 4000 | 1.4 | 7.9 | 16.4 | LV | LAC | WR |
| Ollie Gordon II | 4000 | 0.0 | 1.0 | 3.6 | @SF | MIA | RB |
| Malik Washington | 4000 | 3.0 | 9.7 | 18.9 | @SF | MIA | WR |
| DJ Herman | 4000 | 0.0 | 0.6 | 2.2 | @SF | MIA | RB |
| Demond Claiborne | 4000 | 0.0 | 1.7 | 5.6 | @CHI | MIN | RB |
| DeeJay Dallas | 4000 | 0.0 | 3.6 | 9.2 | @CHI | MIN | RB |
| Max Bredeson | 4000 | 0.0 | 0.1 | 0.5 | @CHI | MIN | RB |
| Hunter Henry | 4000 | 4.6 | 10.0 | 19.6 | PIT | NE | TE |
| Reggie Gilliam | 4000 | 0.0 | 0.1 | 0.6 | PIT | NE | RB |
| CJ Donaldson | 4000 | 0.0 | 0.7 | 2.8 | @BAL | NO | RB |
| Isaiah Davis | 4000 | 0.0 | 0.5 | 2.0 | GB | NYJ | RB |
| Adonai Mitchell | 4000 | 0.6 | 7.7 | 16.8 | GB | NYJ | WR |
| Andrew Beck | 4000 | 0.0 | 0.3 | 1.1 | GB | NYJ | RB |
| Mason Rudolph | 4000 | 0.0 | 0.0 | 1.4 | @NE | PIT | QB |
| Travis Homer | 4000 | 0.0 | 0.0 | 0.2 | @NE | PIT | RB |
| Riley Nowakowski | 4000 | 0.0 | 0.2 | 0.7 | @NE | PIT | RB |
| Kyle Juszczyk | 4000 | 0.0 | 2.1 | 6.7 | MIA | SF | RB |
| Brady Russell | 4000 | 0.0 | 0.8 | 3.0 | @ARI | SEA | RB |
| Emanuel Wilson | 4000 | 0.0 | 1.8 | 6.2 | @ARI | SEA | RB |
| Julius Chestnut | 4000 | 0.0 | 0.2 | 0.8 | PHI | TEN | RB |
| Kendrick Bourne | 3900 | 0.2 | 7.1 | 14.4 | SEA | ARI | WR |
| Jerry Jeudy | 3900 | 0.1 | 7.1 | 15.0 | @TB | CLE | WR |
| Brenton Strange | 3900 | 1.8 | 8.8 | 17.2 | @DEN | JAX | TE |
| Jalen Nailor | 3900 | 0.2 | 8.3 | 17.3 | @LAC | LV | WR |
| Juwan Johnson | 3900 | 7.1 | 10.6 | 19.8 | @BAL | NO | TE |
| Demarcus Robinson | 3900 | 0.6 | 6.9 | 15.5 | MIA | SF | WR |
| Ryan Flournoy | 3800 | 1.0 | 8.0 | 16.7 | WAS | DAL | WR |
| Jake Ferguson | 3800 | 3.5 | 8.7 | 17.5 | WAS | DAL | TE |
| Troy Franklin | 3800 | 0.0 | 3.3 | 9.1 | JAX | DEN | WR |
| DeMario Douglas | 3800 | 1.4 | 8.3 | 17.1 | PIT | NE | WR |
| Kenyon Sadiq | 3800 | 0.1 | 6.0 | 12.9 | GB | NYJ | TE |
| 49ers | 3800 | 4.4 | 9.1 | 17.0 | MIA | SF | DST |
| Elijah Sarratt | 3700 | 0.0 | 0.5 | 1.9 | NO | BAL | WR |
| Jaylin Noel | 3700 | 0.4 | 7.0 | 14.9 | CIN | HOU | WR |
| Caleb Douglas | 3700 | 6.0 | 9.6 | 19.1 | @SF | MIA | WR |
| Pat Freiermuth | 3700 | 1.5 | 9.2 | 17.6 | @NE | PIT | TE |
| Eagles | 3700 | 4.8 | 9.1 | 16.9 | @TEN | PHI | DST |
| Kalif Raymond | 3600 | 0.2 | 6.1 | 13.5 | MIN | CHI | WR |
| Mike Gesicki | 3600 | 0.1 | 6.2 | 13.2 | @HOU | CIN | TE |
| Jack Bech | 3600 | 0.1 | 5.7 | 12.4 | @LAC | LV | WR |
| Michael Mayer | 3600 | 16.8 | 11.9 | 21.3 | @LAC | LV | TE |
| Kyle Williams | 3600 | 0.0 | 3.0 | 8.7 | PIT | NE | WR |
| Hollywood Brown | 3600 | 0.0 | 0.3 | 1.0 | @TEN | PHI | WR |
| Buccaneers | 3600 | 12.7 | 9.3 | 17.2 | CLE | TB | DST |
| Zachariah Branch | 3500 | 0.0 | 1.7 | 5.2 | CAR | ATL | WR |
| Xavier Hutchinson | 3500 | 1.9 | 9.0 | 18.4 | CIN | HOU | WR |
| Brenen Thompson | 3500 | 0.0 | 0.9 | 3.6 | LV | LAC | WR |
| Oronde Gadsden II | 3500 | 0.0 | 3.2 | 8.6 | LV | LAC | TE |
| Chris Bell | 3500 | 0.1 | 5.0 | 11.6 | @SF | MIA | WR |
| T.J. Hockenson | 3500 | 4.2 | 8.8 | 17.3 | @CHI | MIN | TE |
| Elic Ayomanor | 3500 | 0.2 | 3.7 | 9.5 | PHI | TEN | WR |
| Seahawks | 3500 | 4.2 | 8.4 | 16.2 | @ARI | SEA | DST |
| Jahan Dotson | 3400 | 0.1 | 5.3 | 12.2 | CAR | ATL | WR |
| Devontez Walker | 3400 | 0.1 | 5.9 | 13.8 | NO | BAL | WR |
| Xavier Legette | 3400 | 0.0 | 4.7 | 11.5 | @ATL | CAR | WR |
| Jahdae Walker | 3400 | 0.0 | 1.4 | 4.9 | MIN | CHI | WR |
| Noah Fant | 3400 | 0.0 | 4.1 | 9.4 | @BAL | NO | TE |
| Germie Bernard | 3400 | 0.0 | 4.5 | 10.7 | @NE | PIT | WR |
| Cade Otton | 3400 | 1.3 | 7.8 | 16.1 | CLE | TB | TE |
| Packers | 3400 | 1.3 | 7.6 | 15.1 | @NYJ | GB | DST |
| Chris Moore | 3300 | 0.0 | 2.7 | 7.9 | NO | BAL | WR |
| Lil'Jordan Humphrey | 3300 | 0.0 | 1.4 | 5.0 | JAX | DEN | WR |
| Evan Engram | 3300 | 1.6 | 7.2 | 14.7 | JAX | DEN | TE |
| Travis Hunter | 3300 | 0.0 | 1.9 | 5.8 | @DEN | JAX | WR |
| Isaiah Williams | 3300 | 0.0 | 4.3 | 10.1 | GB | NYJ | WR |
| AJ Barner | 3300 | 0.1 | 6.9 | 14.5 | @ARI | SEA | TE |
| Ravens | 3300 | 10.9 | 8.5 | 16.5 | NO | BAL | DST |
| Olamide Zaccheaus | 3200 | 0.0 | 3.0 | 7.9 | CAR | ATL | WR |
| Dalton Schultz | 3200 | 31.7 | 11.6 | 21.4 | CIN | HOU | TE |
| Greg Dulcich | 3200 | 0.6 | 6.5 | 13.4 | @SF | MIA | TE |
| Bryce Lance | 3200 | 0.1 | 5.8 | 12.9 | @BAL | NO | WR |
| Roman Wilson | 3200 | 1.3 | 7.7 | 16.1 | @NE | PIT | WR |
| Tory Horton | 3200 | 0.0 | 1.5 | 5.3 | @ARI | SEA | WR |
| Ted Hurst III | 3200 | 0.0 | 4.7 | 11.7 | CLE | TB | WR |
| Chargers | 3200 | 3.6 | 7.4 | 14.7 | LV | LAC | DST |
| LaJohntay Wester | 3100 | 0.2 | 5.3 | 12.3 | NO | BAL | WR |
| Darren Waller | 3100 | 0.2 | 5.4 | 12.3 | @ATL | CAR | TE |
| Zavion Thomas | 3100 | 0.0 | 0.4 | 1.5 | MIN | CHI | WR |
| Andrei Iosivas | 3100 | 0.0 | 4.6 | 11.4 | @HOU | CIN | WR |
| KaVontae Turpin | 3100 | 0.0 | 2.6 | 7.6 | WAS | DAL | WR |
| Efton Chism III | 3100 | 0.0 | 0.5 | 2.1 | PIT | NE | WR |
| Gunnar Helm | 3100 | 0.6 | 6.9 | 13.8 | PHI | TEN | TE |
| Patriots | 3100 | 4.3 | 7.3 | 14.5 | PIT | NE | DST |
| Simi Fehoko | 3000 | 0.0 | 0.1 | 0.5 | SEA | ARI | WR |
| Devin Duvernay | 3000 | 0.0 | 0.1 | 0.5 | SEA | ARI | WR |
| Chris Blair | 3000 | 0.0 | 0.2 | 0.9 | CAR | ATL | WR |
| Brycen Tremayne | 3000 | 0.0 | 0.8 | 3.2 | @ATL | CAR | WR |
| John Metchie III | 3000 | 0.0 | 0.7 | 2.7 | @ATL | CAR | WR |
| Cole Kmet | 3000 | 0.0 | 4.4 | 10.8 | MIN | CHI | TE |
| Colbie Young | 3000 | 0.0 | 0.6 | 2.4 | @HOU | CIN | WR |
| Dohnte Meyers | 3000 | 0.0 | 1.5 | 4.9 | @HOU | CIN | WR |
| Isaiah Bond | 3000 | 0.0 | 0.9 | 3.5 | @TB | CLE | WR |
| Tylan Wallace | 3000 | 0.0 | 0.3 | 1.4 | @TB | CLE | WR |
| Jonathan Mingo | 3000 | 0.0 | 1.2 | 4.4 | WAS | DAL | WR |
| Skyy Moore | 3000 | 0.0 | 0.7 | 2.7 | @NYJ | GB | WR |
| Bo Melton | 3000 | 0.0 | 1.3 | 4.8 | @NYJ | GB | WR |
| Lewis Bond | 3000 | 0.0 | 0.8 | 3.1 | CIN | HOU | WR |
| Jared Wayne | 3000 | 0.0 | 2.8 | 8.1 | CIN | HOU | WR |
| Josh Cameron | 3000 | 0.0 | 1.7 | 5.4 | @DEN | JAX | WR |
| CJ Williams | 3000 | 0.0 | 0.1 | 0.6 | @DEN | JAX | WR |
| Malik Benson | 3000 | 0.0 | 1.4 | 4.8 | @LAC | LV | WR |
| Cody White | 3000 | 0.0 | 0.6 | 2.5 | @LAC | LV | WR |
| Dareke Young | 3000 | 0.0 | 0.4 | 1.6 | @LAC | LV | WR |
| Gary Jennings Jr. | 3000 | 0.0 | 0.1 | 0.5 | LV | LAC | WR |
| Derius Davis | 3000 | 0.0 | 0.8 | 3.0 | LV | LAC | WR |
| David Njoku | 3000 | 0.2 | 6.2 | 13.7 | LV | LAC | TE |
| Kevin Coleman Jr. | 3000 | 0.0 | 2.6 | 7.2 | @SF | MIA | WR |
| Ryan Miller | 3000 | 0.0 | 0.1 | 0.4 | @SF | MIA | WR |
| Tai Felton | 3000 | 0.0 | 3.0 | 8.1 | @CHI | MIN | WR |
| Myles Price | 3000 | 0.0 | 0.5 | 2.0 | @CHI | MIN | WR |
| Dillon Bell | 3000 | 0.0 | 0.1 | 0.5 | @CHI | MIN | WR |
| Eli Raridon | 3000 | 0.0 | 2.1 | 6.5 | PIT | NE | TE |
| Barion Brown | 3000 | 0.0 | 0.4 | 1.4 | @BAL | NO | WR |
| Kevin Austin Jr. | 3000 | 0.0 | 0.6 | 2.2 | @BAL | NO | WR |
| Arian Smith | 3000 | 0.0 | 0.2 | 1.0 | GB | NYJ | WR |
| Darius Cooper | 3000 | 0.0 | 0.5 | 2.0 | @TEN | PHI | WR |
| Britain Covey | 3000 | 0.0 | 0.1 | 0.5 | @TEN | PHI | WR |
| Kaden Wetjen | 3000 | 0.0 | 0.3 | 1.1 | @NE | PIT | WR |
| Ben Skowronek | 3000 | 0.0 | 1.4 | 4.7 | @NE | PIT | WR |
| KhaDarel Hodge | 3000 | 0.0 | 0.2 | 0.6 | MIA | SF | WR |
| Jordan Watkins | 3000 | 0.0 | 0.1 | 0.6 | MIA | SF | WR |
| Jacob Cowing | 3000 | 0.0 | 0.3 | 1.2 | MIA | SF | WR |
| Montorie Foster Jr. | 3000 | 0.0 | 0.1 | 0.5 | @ARI | SEA | WR |
| Tez Johnson | 3000 | 0.0 | 0.6 | 2.6 | CLE | TB | WR |
| Kameron Johnson | 3000 | 0.0 | 0.1 | 0.6 | CLE | TB | WR |
| Chimere Dike | 3000 | 0.0 | 0.8 | 3.2 | PHI | TEN | WR |
| Dyami Brown | 3000 | 0.0 | 3.2 | 8.6 | @DAL | WAS | WR |
| Jaylin Lane | 3000 | 0.0 | 1.4 | 5.1 | @DAL | WAS | WR |
| Bears | 3000 | 5.1 | 7.2 | 14.8 | MIN | CHI | DST |
| Texans | 3000 | 4.0 | 7.0 | 14.5 | CIN | HOU | DST |
| Jonnu Smith | 2900 | 0.0 | 4.1 | 10.0 | @NYJ | GB | TE |
| Darnell Washington | 2900 | 0.0 | 4.5 | 10.5 | @NE | PIT | TE |
| Ben Sinnott | 2900 | 0.0 | 3.6 | 9.1 | @DAL | WAS | TE |
| Falcons | 2900 | 1.7 | 6.3 | 13.4 | CAR | ATL | DST |
| Cowboys | 2900 | 1.7 | 6.2 | 13.5 | WAS | DAL | DST |
| Brevyn Spann-Ford | 2800 | 0.0 | 2.6 | 7.5 | WAS | DAL | TE |
| Adam Trautman | 2800 | 0.0 | 2.8 | 7.7 | JAX | DEN | TE |
| Mason Taylor | 2800 | 0.1 | 5.6 | 12.1 | GB | NYJ | TE |
| Broncos | 2800 | 8.0 | 7.2 | 14.7 | JAX | DEN | DST |
| Steelers | 2800 | 2.2 | 6.4 | 13.6 | @NE | PIT | DST |
| Foster Moreau | 2700 | 0.0 | 3.0 | 8.3 | CIN | HOU | TE |
| Charlie Kolar | 2700 | 0.1 | 2.8 | 7.9 | LV | LAC | TE |
| John Bates | 2700 | 0.1 | 4.2 | 10.1 | @DAL | WAS | TE |
| Panthers | 2700 | 5.4 | 6.9 | 14.5 | @ATL | CAR | DST |
| Bengals | 2700 | 1.5 | 6.0 | 13.2 | @HOU | CIN | DST |
| Tommy Tremble | 2600 | 0.0 | 3.8 | 9.4 | @ATL | CAR | TE |
| Drew Sample | 2600 | 0.0 | 2.7 | 7.0 | @HOU | CIN | TE |
| Daniel Bellinger | 2600 | 0.0 | 1.6 | 4.9 | PHI | TEN | TE |
| Raiders | 2600 | 1.3 | 5.5 | 12.5 | @LAC | LV | DST |
| Vikings | 2600 | 1.8 | 4.8 | 11.6 | @CHI | MIN | DST |
| Elijah Higgins | 2500 | 0.0 | 0.9 | 3.2 | SEA | ARI | TE |
| Hunter Long | 2500 | 0.0 | 0.9 | 3.3 | SEA | ARI | TE |
| Austin Hooper | 2500 | 0.0 | 1.3 | 4.6 | CAR | ATL | TE |
| Charlie Woerner | 2500 | 0.0 | 1.4 | 4.4 | CAR | ATL | TE |
| Nick Muse | 2500 | 0.0 | 0.1 | 0.6 | CAR | ATL | TE |
| Matt Hibner | 2500 | 0.0 | 2.1 | 6.2 | NO | BAL | TE |
| Durham Smythe | 2500 | 0.0 | 3.0 | 8.0 | NO | BAL | TE |
| Josh Cuevas | 2500 | 0.0 | 0.4 | 1.6 | NO | BAL | TE |
| Feleipe Franks | 2500 | 0.0 | 0.1 | 0.6 | @ATL | CAR | TE |
| Mitchell Evans | 2500 | 0.0 | 2.1 | 6.4 | @ATL | CAR | TE |
| Sam Roush | 2500 | 0.0 | 0.6 | 2.5 | MIN | CHI | TE |
| Erick All Jr. | 2500 | 0.0 | 1.3 | 4.4 | @HOU | CIN | TE |
| Tanner Hudson | 2500 | 0.0 | 1.2 | 4.1 | @HOU | CIN | TE |
| Carsen Ryan | 2500 | 0.0 | 0.1 | 0.5 | @TB | CLE | TE |
| Blake Whiteheart | 2500 | 0.0 | 1.9 | 5.5 | @TB | CLE | TE |
| Luke Schoonmaker | 2500 | 0.0 | 1.1 | 4.1 | WAS | DAL | TE |
| Nate Adkins | 2500 | 0.0 | 0.8 | 3.0 | JAX | DEN | TE |
| Mark Redman | 2500 | 0.0 | 0.2 | 0.6 | @NYJ | GB | TE |
| Josh Whyle | 2500 | 0.0 | 0.6 | 2.3 | @NYJ | GB | TE |
| Cade Stover | 2500 | 0.0 | 2.0 | 6.0 | CIN | HOU | TE |
| Marlin Klein | 2500 | 0.0 | 0.6 | 2.5 | CIN | HOU | TE |
| Nate Boerkircher | 2500 | 0.0 | 2.0 | 6.0 | @DEN | JAX | TE |
| Quintin Morris | 2500 | 0.0 | 0.9 | 3.3 | @DEN | JAX | TE |
| Ian Thomas | 2500 | 0.0 | 0.3 | 1.0 | @LAC | LV | TE |
| Chris Myarick | 2500 | 0.0 | 0.3 | 1.1 | @LAC | LV | TE |
| Will Kacmarek | 2500 | 0.0 | 0.7 | 2.7 | @SF | MIA | TE |
| Seydou Traore | 2500 | 0.0 | 0.1 | 0.5 | @SF | MIA | TE |
| Josh Oliver | 2500 | 0.0 | 3.9 | 9.7 | @CHI | MIN | TE |
| Gavin Bartholomew | 2500 | 0.0 | 0.1 | 0.6 | @CHI | MIN | TE |
| Tanner Arkin | 2500 | 0.0 | 0.1 | 0.2 | PIT | NE | TE |
| Cameron Latu | 2500 | 0.0 | 0.1 | 0.2 | PIT | NE | TE |
| Oscar Delp | 2500 | 0.0 | 0.2 | 0.6 | @BAL | NO | TE |
| Treyton Welch | 2500 | 0.0 | 0.2 | 0.6 | @BAL | NO | TE |
| Jeremy Ruckert | 2500 | 0.0 | 1.2 | 4.2 | GB | NYJ | TE |
| Jelani Woods | 2500 | 0.0 | 0.3 | 1.1 | GB | NYJ | TE |
| Johnny Mundt | 2500 | 0.0 | 0.9 | 3.5 | @TEN | PHI | TE |
| E.J. Jenkins | 2500 | 0.0 | 0.1 | 0.5 | @TEN | PHI | TE |
| Robert Tonyan | 2500 | 0.0 | 0.1 | 0.6 | @NE | PIT | TE |
| Luke Farrell | 2500 | 0.0 | 2.5 | 7.2 | MIA | SF | TE |
| Brayden Willis | 2500 | 0.0 | 0.3 | 1.1 | MIA | SF | TE |
| Elijah Arroyo | 2500 | 0.0 | 2.7 | 7.6 | @ARI | SEA | TE |
| Eric Saubert | 2500 | 0.0 | 0.6 | 2.4 | @ARI | SEA | TE |
| Bauer Sharp | 2500 | 0.0 | 0.2 | 0.6 | CLE | TB | TE |
| Payne Durham | 2500 | 0.0 | 0.1 | 0.6 | CLE | TB | TE |
| Ko Kieft | 2500 | 0.0 | 0.2 | 0.6 | CLE | TB | TE |
| Kylen Granson | 2500 | 0.0 | 0.1 | 0.5 | PHI | TEN | TE |
| Colson Yankoff | 2500 | 0.0 | 1.2 | 4.0 | @DAL | WAS | TE |
| Cardinals | 2500 | 3.8 | 5.9 | 12.9 | SEA | ARI | DST |
| Commanders | 2500 | 0.9 | 4.6 | 11.6 | @DAL | WAS | DST |
| Jaguars | 2400 | 1.7 | 5.4 | 12.3 | @DEN | JAX | DST |
| Jets | 2400 | 1.9 | 5.1 | 11.8 | GB | NYJ | DST |
| Saints | 2300 | 0.6 | 4.5 | 11.4 | @BAL | NO | DST |
| Browns | 2200 | 4.1 | 5.3 | 12.2 | @TB | CLE | DST |
| Titans | 2100 | 6.7 | 5.5 | 12.3 | PHI | TEN | DST |
| Dolphins | 2000 | 1.4 | 3.7 | 10.4 | @SF | MIA | DST |

## Leverage candidates to address (sub-10% own, high ceiling)
COVERAGE RULE: the slate strategy's `## Leverage` or `## Edges & tensions` AND the player pool must ADDRESS **each** player below with a one-line synthesis of their leverage/ceiling case (surface it — no play/fade command required). Never silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak (the play that decides the slate from nowhere). Individual plays only; build no lineups.
- Jaxon Smith-Njigba — $8,100, 9% own, proj 18.2, ceiling 31.8
- Brock Purdy — $6,200, 7% own, proj 21.1, ceiling 31.4
- Lamar Jackson — $7,300, 3% own, proj 20.8, ceiling 30.6
- Saquon Barkley — $7,000, 9% own, proj 17.3, ceiling 30.6
- Jayden Daniels — $6,300, 8% own, proj 20.3, ceiling 30.0
- Jalen Hurts — $6,700, 1% own, proj 19.7, ceiling 29.6
- Caleb Williams — $6,800, 2% own, proj 19.6, ceiling 29.4
- Drake Maye — $6,100, 5% own, proj 19.1, ceiling 29.3
- Bo Nix — $5,700, 6% own, proj 19.4, ceiling 29.3
- De'Von Achane — $6,700, 6% own, proj 16.8, ceiling 29.0
- Trey McBride — $6,900, 7% own, proj 16.7, ceiling 28.9
- Justin Herbert — $6,000, 4% own, proj 18.9, ceiling 28.8

## Chalk combos — the pairs the field will stack together (duplication watch)
Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — a FLOOR, real fields correlate their chalk). Rostering one of these pairs means sharing that slice of the field's lineups — it is where uniqueness quietly dies in a small-field GPP. The strategy MUST surface the top combos as a duplication tension in `## Edges & tensions` (descriptive — never a fade command; breaking a pair is the user's call).
- **Bijan Robinson + Dalton Schultz** — 37.5% × 31.7% ≈ 11.9% of the field (~187 lineups of 1,568)
- **Bijan Robinson + Derrick Henry** — 37.5% × 30.4% ≈ 11.4% of the field (~179 lineups of 1,568)
- **Bijan Robinson + Aaron Jones Sr.** — 37.5% × 28.7% ≈ 10.8% of the field (~169 lineups of 1,568)
- **Bijan Robinson + CeeDee Lamb** — 37.5% × 28.6% ≈ 10.7% of the field (~168 lineups of 1,568)
- **Bijan Robinson + Javonte Williams** — 37.5% × 28.0% ≈ 10.5% of the field (~165 lineups of 1,568)
- **Bijan Robinson + George Pickens** — 37.5% × 25.9% ≈ 9.7% of the field (~152 lineups of 1,568)

## Trap-shaped prices on THIS slate (ownership ahead of projection)
A trap is a price, not a player. This list is where TODAY'S numbers have the trap shape: the field's pick rate (ownership) ranks higher than the player's projection ranks. Naming a player here is fine — these are this slate's prices, not a history of the player. State each as a tension in `## Edges & tensions` or `## Fades`; the user decides.
- **Ravens** — $3,300, 10.9% own: the crowd pays 102 ranks more ownership than his projection earns (owned ahead of projection).
- **Buccaneers** — $3,600, 12.7% own: the crowd pays 96 ranks more ownership than his projection earns (owned ahead of projection).
- **Dalton Schultz** — $3,200, 31.7% own: the crowd pays 72 ranks more ownership than his projection earns (owned ahead of projection).
- **Michael Mayer** — $3,600, 16.8% own: the crowd pays 62 ranks more ownership than his projection earns (owned ahead of projection).
- **Matthew Golden** — $4,700, 17.3% own: the crowd pays 49 ranks more ownership than his projection earns (owned ahead of projection).
- **Mark Andrews** — $4,400, 20.0% own: the crowd pays 46 ranks more ownership than his projection earns (owned ahead of projection).

## References for Claude (read as needed)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_classic/philosophy.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_classic/framework.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_classic/autopsies.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_classic/autopsy_data.jsonl`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/anchor_equivalence.md`
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/sharp_playbook.md` — sharp-player tendencies reverse-engineered from contest standings
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/shared/set_diversity.md` — set-level diversity + dupe-avoidance doctrine (build loose, pick strict)
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_classic/lessons.yaml` — **mandatory pre-flight read: open lessons (hypothesis/validated)**
- `/Users/ryansieb/Desktop/Repo/ryanjsieb30DFS-Analyzer/rules/nfl_classic/results.jsonl` — cross-slate results ledger (process notes only)

**Output target:** write the slate strategy to `data/slate_analysis/nfl_classic.md`.
