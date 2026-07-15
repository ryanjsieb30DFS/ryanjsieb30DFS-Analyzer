# Post-Autopsy Review — Quaker State 400, Atlanta Motor Speedway (7/12/26)

*Logged 2026-07-14. Two SE contests: $8K Rainbow Warrior (392) and $5K Engine Block (490). Standings-only autopsy — no projections at autopsy time.*

## Process scorecard

**Pre-flight discipline — substantively HONORED (B+).**
- **Venue file:** read (`atlanta_motor_speedway.md`, UNVERIFIED-at-the-time). ✓ The "races as a drafting superspeedway, not a normal 1.5mi intermediate" framing was correct and drove the analysis.
- **Open lessons:** applied `midpack-pd` (21-30 meat → Gilliland/Nemechek/Zilisch), `roadcourse-deepback-revives` (deep-back live), `portfolio-gaps` (top-10 fade group addressed), and correctly *checked and rejected* `narrative-suppressed-elite` (Byron's HMS edge genuinely absent at a drafting track — a correct non-activation, not a demotion) and `ownership-shift` / `injury-narrative` (no trigger). Application was honest and mechanism-checked. ✓
- **Anchor-Equivalence:** surfaced as required (Decision 1, "At Most 1 of Bell/Hamlin/Reddick/Byron"). ✓ **But this is where the strategy went wrong** — see below.

**Did the strategy's edges hold vs the DK actuals? MIXED — the individual-play reads were mostly good; the central slate thesis was mechanism-wrong.**

*Held up (WINS):*
- **Tyler Reddick modal anchor** — 71.8, in most top lineups. ✓
- **Ryan Blaney elite plate floor** (listed as a 3.5★ dart) — **91.35, slate high.** ✓ Best single read on the slate.
- **Todd Gilliland mid-pack PD** (P21, 6%) — in the #2 lineup of BOTH contests. ✓
- **McDowell / Erik Jones sub-5% darts** — both surfaced in multiple top lineups (McDowell in the 490 rank-6; EJ in rank-4/8/10 spots). ✓
- **Bubba Wallace fade** — 11.4, the #1 field fish trap (≈50% of fish, 0% of winners). ✓
- **Zane Smith low-ceiling read** — busted to 17.4 (though winners tolerated him as min-salary filler). ✓ directionally.

*Failed / missed (MECHANISM ERRORS):*
1. **The "moderately contrarian, fade off the 41-45% chalk wall" thesis + the At-Most-1 anchor cap were WRONG for a pack track.** The chalk dominators HIT together — Reddick 71.8, Bell 74.6, Blaney 91.35 — and the #1 lineups in BOTH SE contests **stacked Reddick+Bell** (both in the cap group) with Blaney. The at-most-1 cap would have *blocked the winning combo.* Mechanism: at drafting tracks the lead draft stays bunched, so chalk doms finish *together* (correlated), not one-or-the-other. → new hypothesis `superspeedway-doms-correlate-not-substitute`.
2. **The "leverage dominator path" was built on multi-year avg laps-led (Cindric 40.8 / Logano 39.2), which under-delivered.** Logano scored 30.2 (a field fish trap); Cindric was moderate. The drivers who actually dominated were the day's fast cars. → new hypothesis `multiyear-lapsled-weak-perrace-signal`.
3. **Coverage gap: two of the top slate-definers were never named.** **Ty Gibbs (22% own, 70.6)** and **Carson Hocevar (18% own, 65.45)** were in 35-45% of top lineups and are absent from the entire strategy — as are the winning cheap pieces **Cole Custer** and **Noah Gragson.** The writeup over-indexed on the sub-15% leverage doms and skipped the 15-25%-owned dominator band that was the winning glue.

**Your entries vs the winners (GPP guard: losses are variance, not mechanism failures — but these are process observations):**
- **$8K Rainbow Warrior — rank 223/392, 56.9 pctile** (Blaney, Elliott, Bell, Zane Smith, Austin Hill, AJ Allmendinger). You captured the two big studs Blaney+Bell (166 of your 217 pts) but filled the other four slots with weak cars — **AJ Allmendinger (−4.2) is a field fish trap the strategy's Fades section did not name but the field flagged**, Hill 11.2, Elliott 26.6. You missed Reddick and Ty Gibbs (the winning glue). **low_own_count 0** — zero sub-5% pieces.
- **$5K Engine Block — rank 412/490, 84.1 pctile** (Reddick, Byron, Logano, Bubba, Preece, Herbst). This lineup *followed* the anchor-equivalence cap (only Reddick of the group) and paid for it — no Bell/Blaney/Gibbs, and it rostered **Bubba (11.4, the #1 fish trap the strategy explicitly UNDERWEIGHT-flagged).**
- **Recurring SE leverage leak:** shark_gap_top **−15.7** on own-per-slot; contest-1 carried zero sub-5%. This is the same NASCAR under-leverage leak flagged at Chicagoland (−16.7) — now persisting. Note: `carry-a-sub5-leverage-dart` is MME-scoped, so this is a build-execution note, not a lesson confirmation.

**Net:** Good pre-flight discipline and mostly-good individual reads, undone by a slate-thesis error — applying a non-pack-track contrarian frame (fade the chalk, cap the anchors) to a pack track where the chalk doms correlate and the winning shape is a multi-dominator stack.

## Lesson ledger changes

**Confirmations added:**
- `nascar-2026-06-20-midpack-pd-over-deep-back-chalk` (validated) — **4th confirmation** (Atlanta): Gilliland (P21, 6%) hit and was in both contests' #2 lineups; the 21-30 band (40.7% of optimal) was the meat as coded. Deep-back (16.7% here) mostly did not pay this running. Mid-pack half already codified 2026-07-12; **stays validated.**

**Scoping contradiction added (mechanism-based, NON-retirement):**
- `nascar-2026-05-24-anchor-equivalence` (codified) — added a **drafting-track scoping refinement**: at pack tracks the "substitutable coin-flip" precondition is absent (chalk doms correlate and finish together), and the at-most-1 cap would have blocked the winning Reddick+Bell stack. Substitution logic still holds at non-pack tracks (confirmed Chicagoland 3 days earlier). Codified lesson + 1 scoping contradiction → **stays codified.**

**New hypotheses born (mechanism-based):**
- `nascar-2026-07-14-superspeedway-doms-correlate-not-substitute` — at drafting tracks chalk dominators are positively correlated (bunched lead draft), so the winning shape is a 3-4 dominator STACK, not an at-most-1 substitution set; scopes the Anchor-Equivalence rule out of pack tracks.
- `nascar-2026-07-14-multiyear-lapsled-weak-perrace-signal` — multi-year avg laps-led is a weak per-race dominator predictor at superspeedways (draft/caution timing decides track position); weight current form over career avg-LL.

## Venue file changes

`rules/nascar/tracks/atlanta_motor_speedway.md` — upgraded header from **UNVERIFIED** to **PARTIALLY VERIFIED** (the 7/12/26 running is now results-verified) and appended a dated **Per-slate observations** block recording: chalk doms hit / "floor is lava" overstated; winning lineups were multi-dominator + moderately chalky (Reddick+Blaney+Bell+Gibbs); multi-year avg-LL was a weak signal (Logano 30.2); 21-30 mid-pack PD confirmed (Gilliland) but deep-back missed; mid-owned dominators (Gibbs 22%, Hocevar 18%) were the winning glue; fish traps Bubba/AJ/Briscoe.

## Proposed codifications

**None this slate.** The two new lessons are fresh single-slate hypotheses (need 3 confirming slates before promotion). The Anchor-Equivalence scoping note is a mechanism refinement on an already-codified rule, not a retirement (retirement needs 2 mechanism contradictions; this is the 1st, and it is a scope-narrowing, not a mechanism failure). No lesson currently sits at the 3-confirmation promotion threshold un-codified.
