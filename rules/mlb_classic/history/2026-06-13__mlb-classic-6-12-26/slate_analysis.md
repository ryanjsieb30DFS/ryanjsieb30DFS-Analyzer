# MLB Classic — 6.12.26 slate analysis

## Pre-flight checklist
- [x] Slate confirmed: mlb_classic — 13-game main slate 6.12.26; bundle generated 2026-06-12 18:15; both SIN ranking CSVs and The Stone dated 6.12.26; first pitch 7:05 PM ET (~50 min out — tight clock, late-build lesson default applies: enter the tracked portfolio, no near-lock swaps)
- [x] Projections loaded: Ship It Nation MLB Projections (257 players, this slate) — **pool is MISSING three of the Stone's projected ATH starters**: Colby Thomas (17.2% Stone own), Jacob Wilson (14.1%), Alika Williams (10.4%). The snapshot/leverage table is structurally blind to them (sin-projection-pool-omissions mechanism recurs — autopsy note)
- [x] Venue file read: `rules/mlb_classic/parks/las_vegas_ballpark.md` (UNVERIFIED stub, one prior slate) — COL@ATH is this slate's axis game; 6/10 observation: the heat-total hype was an ownership tax, mega-stacks didn't pay, pieces did. No Coors game today (COL is the road team), so coors_field.md mechanisms do not port
- [x] Open lessons reviewed: 5 open — **applied**: se-chalk-pitcher-own-condensation (Misiorowski/Yesavage math, Decision 2), sin-projection-pool-omissions (cross-check run, found 3 omissions), blank-own-snapshot-artifact (cross-check run — no blank-Own rows, but found a duplicate-Muncy own artifact instead, see vendor section), five-man-primary-conditional-on-blowup (5-stack reserved for the one ATH-blowup lineup; 3–4 man shapes elsewhere). **Rejected**: weather-proof-dome-stack-pivot — precondition absent (no rain risk concentrating field ownership; the chalk cluster is the Vegas outdoor game on its own merits, and the Stone flags no weather)
- [x] Framework pre-lock checks: Anchor-Equivalence → Misiorowski/Yesavage at 25.2/23.6% projected own (alternative anchors Joe Ryan/McClanahan at 14.7% — Decision 2 is the call); pivot budget (codified): ~15–18% avg own, 3–5 sub-10% plays, ONE leverage axis; salary-enabler check: no cheap chalk arm exists this slate — the chalk arms are premium-priced, Imai $6.3K at 7.7% is the value route, not an enabler fade question; own-pitcher blocks mapped: Yesavage⊗NYY bats, Misiorowski⊗PHI bats, Jump⊗COL bats, Joe Ryan⊗STL, McClanahan⊗LAA
- [x] Prior results scanned: results.jsonl last 3 — best percentile of the ledger (top 4.4%) came 6/11 from the in-band, one-pivot build that kept the condensing chalk arm and pivoted in his own bats; the two slates before that were untracked-entry misses. Repeat the 6/11 process

## Slate at a glance
| Fact | Read |
|---|---|
| Games | 13, lock 7:05 PM ET; TB@LAA, COL@ATH, CHC@SF lineups still PROJECTED at write time |
| The axis game | COL@ATH (Las Vegas Ballpark): **13.85 total** (COL 6.10 / ATH 7.75), ~196% combined projected stack own per the Stone |
| Other implieds | MIL 5.35 (PHI just 2.65, Misiorowski -260), LAD 5.00 @ CWS, TB 4.95, ARI/CIN 4.85 each, HOU 4.65 |
| Chalk arms | Misiorowski $12.0K (25.2%), Yesavage $8.5K (23.6%); next tier Joe Ryan / McClanahan / McLean / Bibee 14–15% |
| Ownership shape | Top-5 concentration 128%; 13 players ≥15% — ALL of them in the COL@ATH game except the two arms |
| Contests | None declared — default 2 lineups |
| Weather | Nothing flagged; the only environment story is desert heat in Vegas |

## The 4 decisions that define this slate

### 1. The Vegas game (COL@ATH, 13.85 total, ~196% combined own)
**MIX — buy the environment in 2–3 man pieces; the 5-stack is one lineup's bet, not a default.**
Every hitter on the slate above 12% own is in this game. The park file's only prior observation (6/10, a 14.7 total): the mega-total side paid only as *secondary pieces* in winners and the mega-stack was an ownership tax. Two extra reasons for caution today: (a) the ATH lineup is still PROJECTED, and the Stone's nine **omits Rooker (25.3% own), Cortes (20.6%), and McNeil (14.8%)** — a quarter of the field may be locked into bats who sit; (b) three Stone-projected ATH starters (Thomas/Wilson/Williams, 10–17% own) aren't in the projection pool at all, so ATH's true combined ownership is *higher* than the snapshot shows.
- **If played (ATH-5, the blowup lineup)** → confirmed-in-both-vendors core Langeliers $5.8K + Kurtz $6.0K + Soderstrom $5.0K + Bolte $3.6K + Gelof $4.8K = $25.2K; that forces value arms (Imai $6.3K + Lodolo $6.7K) and leaves $11.8K for 3 bats (~$3.9K each). Misiorowski does NOT fit over an ATH-5 ($12K + $6.3K P2 + $25.2K = $43.5K, $6.5K for three bats — dead end). This lineup is near-field chalk, not a pivot — it satisfies the band, not the leverage axis.
- **If played (pieces)** → 2–3 ATH bats (Langeliers/Kurtz/Soderstrom in any pair) slot into any build; COL mirror pieces Castro/Karros are multi-position glue at $3.0–4.1K.
- **If faded (whole game)** → you need BOTH ~100%-owned sides of the slate's best park to go quiet. The 6/10 precedent says it happens, but it's the most binary fade on the board — underweight, don't zero.

### 2. The chalk-arm pair: Misiorowski $12.0K vs Yesavage $8.5K (Anchor-Equivalence call)
**PLAY Misiorowski as the preferred chalk arm; Yesavage is the condensation magnet; ≥1 lineup must run the alternative anchor (Joe Ryan $10.0K or McClanahan $9.2K, both 14.7%).**
The vendors price the pair as equals (25.2/23.6%). The condensation lesson (validated, 2-for-2) says a small SE field converges on ONE consensus arm — and both prior condensed arms (Detmers 38→69%, Scott 44→56-63%) were the *affordable* consensus arm, because that's the one that fits under the cap next to chalk bats. Yesavage at $8.5K fits next to the ATH core; Misiorowski at $12K structurally can't be everyone's arm. Expect Yesavage to close 35–45%; Misiorowski to hold ~25% with the slate's highest projection (24.0) and a -260 line.
- **If played (Misiorowski)** → $38.0K for 9 spots ($4,222/slot). P2 must be value: Imai $6.3K (PLAY) or Lodolo $6.7K → ~$31.7K for 8 bats. He blocks only PHI bats (2.65 implied — nothing lost), and he pairs naturally with his OWN offense (Decision 3). This is the 6/11 winning pattern: keep the chalk arm, pivot in his bats.
- **If played (Yesavage)** → $41.5K for 9 ($4,611/slot) — fits Kurtz + Langeliers comfortably. But he blocks the NYY strike (Decision 4) and you're holding the condensed arm: your ONE pivot must come from the bats.
- **If faded (both)** → that's a fade of ~25% AND a real ~40% — only do it via the alternative anchor, not a punt: Joe Ryan (18.4 proj, vs STL 4.10 implied) or McClanahan (17.3, vs LAA 3.80) at 14.7% each. This lineup satisfies Anchor-Equivalence for the portfolio.

### 3. MIL bats vs Andrew Painter — the slate's structural pivot
**PLAY — this is the ONE leverage axis I'd spend the pivot budget on.**
MIL has the second-highest team total on the board (5.35), faces Painter ($6.0K, 8.11 xERA, 14.4% barrel rate, 4.8 IP leash), and carries **6.1% combined ownership** (Stone; SIN 9.1%) — a top-two run environment at one-thirtieth the ownership of the Vegas game. The field is paying Misiorowski and ignoring his offense.
- **If played** → MIL-4: Chourio $5.5K + W. Contreras $5.0K + Bauers $4.9K + Ortiz $2.6K = $18.0K (Contreras is also your C pivot off Langeliers/Goodman chalk). Double down with Misiorowski + Imai ($18.3K) = $36.3K, leaving $13.7K for 4 bats (~$3.4K each — Bolte, Castro, Karros, cheap LAD/TB fills). One stack, one game-script (MIL blowout), every piece reinforcing it.
- **If faded** → you're betting a 4.8-xERA-leash rookie holds the slate's biggest favorite under 5.35 while a quarter of the field wins with Misiorowski anyway. That's the wrong side of both bets.

### 4. The zero-own binaries: NYY vs Yesavage, PHI vs Misiorowski
**NYY MIX (only as THE pivot in a no-Yesavage build) · PHI PASS.**
NYY's nine carries **3.1% combined own** because Yesavage is 24%-going-on-40% — Rice $6.1K (0.3%), Bellinger $5.1K (0.4%), Grisham $4.1K (1.7%) top the leverage table. PHI at 0.0x% is *correctly* unowned: a 2.65 implied against the slate's best arm is dead equity, not leverage.
- **If played (NYY mini-stack)** → Rice + Bellinger + Grisham = $15.3K. Hard rule: cannot roster Yesavage in this lineup, and per the pivot budget this IS the lineup's one axis — pitchers and the rest of the roster stay near-field (e.g. Joe Ryan + Imai $16.3K, then chalk Vegas pieces).
- **If faded** → nothing needed; that's the default. Just don't "fade Yesavage" by punting P2 — fade him THROUGH the NYY bats or through the alternative arm, never both in one lineup.

## Player board
Tiers cover the chalk tier, every named leverage candidate, traps, and vendor disagreements — not the full pool.

| Player | Team/Role | Sal | Proj | Own% (adj) | Call | If played → |
|---|---|---|---|---|---|---|
| Jacob Misiorowski | MIL P1 | $12.0K | 24.0 | 25 (holds ~25) | PLAY | value P2 (Imai/Lodolo) + his own MIL bats; blocks PHI (nothing lost) |
| Trey Yesavage | TOR P | $8.5K | 18.2 | 24→**35–45** | MIX | you're holding the condensed arm — take your one pivot in bats; blocks the NYY strike |
| Joe Ryan | MIN P | $10.0K | 18.4 | 14.7 | PLAY | the Anchor-Equivalence alternative; pairs with Imai for $16.3K total P |
| Shane McClanahan | TB P | $9.2K | 17.3 | 14.7 | MIX | second alternative anchor; blocks LAA only |
| Tatsuya Imai | HOU P | $6.3K | 13.1 | 7.7 | PLAY | the slate's value P2 — unlocks every premium-bat structure |
| Tanner Bibee | CLE P | $7.3K | 15.6 | 14.4 | MIX | mid-chalk P2 when Imai's savings aren't needed |
| Spencer Strider | ATL P | $9.5K | 15.6 | 4.6 | MIX | K-upside leverage arm (10.75 K/9) — counts as a lineup's one pivot; blocks NYM |
| Gage Jump | ATH P | $7.0K | 11.4 | 2.5 | PASS | (if anyway: only WITH an ATH stack — correlated blowout — never with COL bats) |
| Shea Langeliers | ATH C | $5.8K | 13.0 | 27.9 | PLAY | the C slot in any Vegas-exposed build; don't auto-pair with Kurtz in every lineup |
| Nick Kurtz | ATH 1B | $6.0K | 13.5 | 26.0 | PLAY | premium 1B; over a MIL-4 he's the salary squeeze — pick him OR Rice/Bauers route |
| Tyler Soderstrom | ATH OF | $5.0K | 10.5 | 21.4 | PLAY | in both vendors' nine; mid-salary OF anchor for ATH pieces |
| Henry Bolte | ATH OF | $3.6K | 9.1 | 21.5 | MIX | cheap chalk in both vendors' nine; fine glue, no leverage |
| Brent Rooker | ATH OF | $4.5K | 11.4 | 25.3 | MIX | **NOT in the Stone's projected nine** — confirm before lock; unconfirmed, his 25% own is the field's risk, not yours |
| Carlos Cortes | ATH OF | $4.3K | 10.2 | 20.6 | MIX | same lineup risk as Rooker; if confirmed he's a normal chalk piece |
| Zack Gelof | ATH 2B | $4.8K | 9.4 | 14.6 | MIX | 2B filler in ATH-heavy builds; Castro is the cheaper 2B route |
| Colby Thomas | ATH OF | $3.8K | 8.5* | 17.2* | MIX | *Stone only — invisible to the pool/snapshot; real chalk if he starts; cheap ATH correlation the optimizer crowd can't see either |
| Jacob Wilson | ATH SS | $3.3K | 9.6* | 14.1* | MIX | *Stone only; $3.3K SS relief inside ATH builds (vs Tovar $4.0K) |
| Willi Castro | COL 2B/3B | $4.1K | 10.1 | 18.7 | MIX | best COL piece (multi-pos, vendor agreement); 1–2 COL bats max per lineup |
| Kyle Karros | COL 3B | $3.0K | 9.3 | 16.1 | MIX | cheap 3B glue; the COL piece to keep when salary is tight |
| Ezequiel Tovar | COL SS | $4.0K | 9.0 | 18.8 | MIX | SS chalk; Wilson at $3.3K is the same exposure $700 cheaper if he confirms |
| Hunter Goodman | COL C | $5.4K | 11.0 | 14.7 (Stone 17.9) | PASS | 45.5% K rate, the *owned* COL name, and Langeliers owns the C slot (if anyway: never alongside Langeliers) |
| Cole Carrigg | COL OF | $2.7K | 8.6* | 16–19 | PASS | the field found him — two slates of free equity now fully priced (if anyway: treat as chalk glue, not a pivot) |
| Jackson Chourio | MIL OF | $5.5K | 9.5 | 2.7 | PLAY | core of the MIL-4 pivot |
| William Contreras | MIL C | $5.0K | 8.4 | 1.4 | PLAY | the C pivot off 30–45% combined C chalk — MIL stack's spine |
| Jake Bauers | MIL 1B/OF | $4.9K | 8.4 | 1.8 | PLAY | 1B/OF flexibility inside the MIL-4; the 1B pivot off Kurtz |
| Joey Ortiz | MIL SS | $2.6K | 6.4 | 1.5 | PLAY | $2.6K stack glue that funds Misiorowski |
| Brice Turang | MIL 2B | $5.7K | 8.7 | 1.5 | MIX | priciest MIL bat and 0-pointers on two recent ledger slates — 5th man, not core |
| Christian Yelich | MIL OF | $5.3K | 8.9 | 1.8 | MIX | swap for Chourio/Bauers when salary allows; same thesis |
| Ben Rice | NYY 1B | $6.1K | 8.9 | 0.3 | MIX | NYY-strike lineup only (no Yesavage); top of the leverage table |
| Cody Bellinger | NYY OF | $5.1K | 7.9 | 0.4 | MIX | second piece of the NYY mini-stack |
| Trent Grisham | NYY OF | $4.1K | 8.4 | 1.7 | MIX | leadoff, cheapest NYY piece with a real projection |
| Andy Pages | LAD OF | $5.4K | 9.1 | 3.0 | PLAY | best bat of the quiet LAD 5.00 implied vs Kay (6.76 xERA) |
| Freddie Freeman | LAD 1B | $5.0K | 8.9 | 3.2 | MIX | LAD 3-man piece; 1B pivot off Kurtz at -$1.0K |
| Kyle Tucker | LAD OF | $4.8K | 8.4 | 3.6 | MIX | third LAD piece (Pages/Freeman/Tucker = $15.2K) |
| Junior Caminero | TB 3B | $5.6K | 10.4 | 5.6 | MIX | the 3B ceiling pivot off Karros/Castro chalk; TB 4.95 implied |
| Yandy Diaz | TB 1B/3B | $5.2K | 10.5 | 9.0 | MIX | highest-projected TB bat; corner flexibility |
| Kyle Schwarber | PHI OF | $6.3K | 7.6 | 0.1 | PASS | 2.65 implied vs Misiorowski — correctly unowned, not leverage |
| Bryce Harper | PHI 1B | $5.3K | 7.6 | 0.0 | PASS | same — the leverage table's top rows are this dead PHI equity; ignore them |

Left off: the 4.10–4.85-implied middle (BAL/SD, DET/CLE, TEX/BOS, ARI/CIN, HOU one-offs like Yordan $6.2K) — all playable as fills, none changes a build's shape; and sub-$3K punts not attached to any thesis.

## Where I disagree with the vendors
Calibration context: SIN is 3 slates calibrated (own MAE 3.62, proj MAE 5.79) — at the small-sample bar, lean on their ownership, question individual point calls. The Stone has no calibration history (article, not a ledger vendor) — its edge here is lineup status and per-game detail, not its RK column.

1. **SIN puts Rooker (25.3%), Cortes (20.6%), McNeil (14.8%) in the chalk tier → I say their ownership is conditional, not real.** The Stone's projected ATH nine omits all three. Mechanism: ownership projected onto a bat that may not start is the field's trap, not a signal — if they confirm, play them as normal chalk; until then build ATH exposure through Langeliers/Kurtz/Soderstrom/Bolte, who are in both vendors' nine.
2. **Both vendors price Misiorowski and Yesavage as equal chalk (~24–25%) → I say the real gap is 20 points.** SE condensation (validated lesson, 2-for-2) lands on the *affordable* consensus arm — Yesavage fits next to chalk bats at $8.5K, Misiorowski at $12K can't be everyone's arm. Yesavage ~35–45% real, Misiorowski ~25%: at near-equal projected own, Misiorowski is the better side of the same coin with a 5.8-point projection edge.
3. **The Stone ranks Gage Jump P#1 → pass.** That RK is value-math; the mechanism says a 6.10-implied opponent in the slate's hottest park caps a $7.0K arm's ceiling. Both vendors' raw projections (11.4–11.6) agree with me; the rank doesn't.
4. **SIN's own table has a duplicate-Muncy artifact**: LAD Max Muncy and ATH Max Muncy carry byte-identical proj/own (8.53/10.04). The Stone has LAD Muncy at 0.65% own, ATH Muncy at 11.5% — the LAD number is a copy error. Don't read LAD Muncy as a 10%-owned bat (blank-own-artifact lesson's cross-check, applied — different artifact, same fix).
5. **The snapshot's leverage table top (Harper/Schwarber/Goldschmidt at ~0%) → not leverage.** Verified real against the Stone, but the mechanism (PHI 2.65 implied vs the slate's best arm; Goldschmidt in a 4.05 offense) means these are correctly priced at zero, and the table is also blind to the real cheap chalk it never saw (Thomas/Wilson). Use the leverage table for the MIL/NYY/LAD rows, not its top.

## Edges to exploit
1. **MIL bats vs Painter — the slate's mispriced run environment.** Second-best team total (5.35) at 6% combined own against an 8.11-xERA arm. Expression: MIL-4 Chourio/W.Contreras/Bauers/Ortiz ($18.0K) + Misiorowski + Imai ($18.3K) = $36.3K, four ~$3.4K fills (Bolte, Castro or Karros, a cheap LAD/TB bat). One game-script, doubled through the pitcher.
2. **Misiorowski-over-Yesavage selection.** Same projected own, but the field's salary structure condenses on Yesavage — taking the $12K arm is unconciously contrarian at P while staying chalk on paper. Expression: any Misiorowski + Imai build; the $31.7K bat budget still fits two ATH pieces + the MIL core.
3. **The invisible ATH starters.** Thomas ($3.8K) and Wilson ($3.3K) are Stone-projected starters the SIN pool — and therefore every snapshot-driven builder — literally cannot see. Expression: in ATH-piece builds, take Wilson over Tovar (-$700, same game) and Thomas as the third ATH bat; confirm the lineup at lock.
4. **LAD's quiet 5.00 implied vs Anthony Kay.** A top-three run environment at ~19% combined (Stone) with no single bat over 7%. Expression: Pages/Freeman/Tucker 3-man ($15.2K) as the secondary stack behind a MIL or ATH core — fits any premium-arm route.
5. **The NYY strike (one lineup, conditional).** If the portfolio carries a no-Yesavage lineup, Rice/Bellinger/Grisham ($15.3K) at 3% combined is the highest-leverage expression of his 35–45% real ownership busting — with Joe Ryan + Imai as the near-field arms and Vegas chalk pieces filling, so the strike stays the lineup's only pivot.
