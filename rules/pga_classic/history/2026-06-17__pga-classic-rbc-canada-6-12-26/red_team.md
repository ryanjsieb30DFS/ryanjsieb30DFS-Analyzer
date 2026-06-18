# Red team — PGA Classic · RBC Canadian Open 6.11.26 · TPC Toronto (Osprey Valley, North)

_Adversarial review of `data/lineups/pga_classic.md` (3 lineups, $12K Mulligan 5-Max, field 1,764). All salaries, projections, ownership, and make-cut numbers below were recomputed against the session ETR data — every figure in lineups.md verified exact. Calibration context: `rules/pga_classic/vendor_calibration.jsonl` **does not exist** — zero calibrated slates, so ETR's ownership projections carry no calibration weight this week. Every leverage number below is uncalibrated single-source._

## Verdict summary

| Lineup | Verdict | One-line reason |
|---|---|---|
| L1 — Model conviction | **SHIP** | Framework-mandated conviction build, math verified, rules respected — but it is the chalk-heaviest expression possible (~93–96% large-field cumulative own) riding the field's favorite pair; that risk is by design and the portfolio covers the other outcomes |
| L2 — Alt anchor + coffin spine | **SHIP** | The Fitzpatrick-over-Fleetwood pivot is the portfolio's best structural edge; the roster survives attack — but the "leverage spine" label is false advertising (Rai+Cauley ≈ 42% combined large-field own, not a sub-15% spine) |
| L3 — Contrarian / chaos | **SHIP** | Lesson-compliant chaos build with a real leverage floor; it is also the *mildest legal* chaos lineup (zero sub-4% pieces, 66% cumulative) — an accepted consequence of applying the SE leverage cap to a 3-max chaos angle |

Three SHIPs is earned, not rubber-stamped: the build's own portfolio-audit section pre-answered most attacks, and every checkable number checked. The findings below are real but none rises to a single change that improves a lineup without breaking a codified rule. The portfolio's genuine exposure is at the *portfolio* level (findings P1–P3), not in any one roster.

## Lineup attacks

### L1 — Model conviction (Fleetwood / Clark / Rai / Greyserman / Finau / James)

**Steelman.** This is the framework's mandated "trust the model" build: model #1 skill (Fleetwood, the slate's only ≥85% make-cut player at 86.9%), the two biggest coffin overweights (Rai +25.3, Finau +7.4), the group-2 alternative anchor (Clark, no docks), and genuine uniqueness at the bottom (Greyserman 5.4%, James 3.0%). The anti-Truist rule (`never-zero-value-chalk-anchor`, codified) *requires* a lineup like this to exist. Salary $49,900 verified.

**What must ALL be true to win:**
1. Fleetwood is the right anchor (not Fitzpatrick at ~half his own) — if wrong, L2 covers, which is correct portfolio design.
2. Rai's putting wart doesn't bite across 4 rounds. ETR's +25.3 is an ETR-internal artifact (their optimals vs their own ownership projection) — see P1.
3. Greyserman (58.7% make-cut) AND James (56.8%, **pro debut**, zero Tour data) both make the cut and at least one spikes. The lineup's "sub-55% make-cut players: 0" claim is literally true but both bottom pieces sit within 4 points of the threshold — the guardrail is satisfied on a technicality. Joint all-six-make-the-cut probability ≈ 10%. That's normal for golf, but the win condition leans on two near-coin-flips.
4. The best-projected core wins a 1,764-field GPP while being the most-duplicated core in it: Fleetwood+Rai is the exact default pair the slate analysis says to avoid, and ETR's published 50.2% Rai optimal exposure means every ETR-subscriber optimizer in a $12 contest is heavy on it.

**Leverage audit.** Greyserman 5.4% and James 3.0% are genuinely contrarian — verified. But the lineup's table uses snapshot (small-field) ownership. At the large-field numbers the slate analysis says to use for leverage math, the cumulative is ~93–96% (Fleetwood 32.9, Rai 24.9, Clark ~17, Finau 10.4, James 4.5), not 83.7% — far above the 60–80 band and above even the slate analysis's own 70–80% sketch for this lineup. The audit discloses the discrepancy, then concludes "in range" using the friendlier column. The Memorial autopsy's core finding was an over-chalky entry (~17.7 avg own/player); L1 is ~15.5–16/player. Better — two sub-10 pieces vs one — but the same neighborhood.

**Why SHIP anyway.** There is no legal fix: any swap that lowers ownership adds a third sub-10% piece (breaking the codified ≤2 cap) or removes the model #1 (breaking the anti-Truist rule). The conviction lineup being chalky is its job; L2/L3 are the hedges. The risk is named, structural, and accepted.

### L2 — Alt anchor + coffin spine (Fitzpatrick / Lowry / Rai / Cauley / Fisk / Suber)

**Steelman.** The cleanest structural edge in the portfolio: Fitzpatrick is skill #3 with a better season than Fleetwood at roughly half the large-field ownership (~17% vs 32.9%) — exactly what the Anchor-Equivalence rule exists to capture. Suber is the one CH qualifier passing the skill/form gate (`ch-scan-needs-skill-gate` correctly applied), Fisk is a real form-engine piece, and $50,000 exactly. Verified.

**What must ALL be true to win:**
1. Fleetwood stumbles AND Fitzpatrick wins the week. Fair — that's the pivot, and it's priced right.
2. **The Rai+Cauley "spine" pays "multiplicative leverage."** Attack: the codified leverage-spine mechanism (lesson `leverage-spine-pairing`) is defined for coffin overweights at **sub-15% ownership** — "ceiling-equivalent exposure at materially lower duplication risk." The Truist validation pair (JT+Bradley) was **sub-19% combined**. Rai (24.9% large-field) + Cauley (17.5% large-field) is **~42% combined** — heavy chalk plus mid-chalk. The duplication-risk discount that makes the spine multiplicative does not exist at these ownerships. This is two value-chalk plays wearing a leverage costume. They are still *good plays* (value chalk is the lock per the framework), but the thesis claims an edge mechanism that isn't operating.
3. Suber (52.1% make-cut) survives. His CH boost is worth nothing at a 0.06-stickiness course — his entire case is the form line (qualifying medalist, OTT trend). Acceptable for the lottery slot, but name it for what it is.
4. Fisk's five-event putting streak holds. Putting is the least sticky skill in golf; this is the exact recency profile philosophy §2 says gets overweighted. At 4.7% own the field isn't paying for it, so the leverage is real — but the projection's reliability is the soft spot.

**Leverage audit.** Real contrarian content: Fisk 4.7%, Suber 4.6%. Fitzpatrick at 21.6% snapshot/~17% large-field is not leverage, it's the *less-popular half of a chalk coin* — which is precisely what the equivalence rule wants, so no objection. The lineup's true uniqueness is Fisk+Suber+the anchor pivot, not the "spine."

**Why SHIP.** Every condition that's attackable is a framing error, not a roster error. No swap improves it: the only same-cost upgrades to Suber are already deployed elsewhere or unaffordable at $0 remaining.

### L3 — Contrarian / chaos (Rose / Lowry / Thorbjornsen / Cole / Finau / Potgieter)

**Steelman.** The only lineup with zero exposure to the top-5 ownership concentration (114.1%). All six players sit in the 4.6–16.0% band — if the Fleetwood/Rai/Reitan core goes median, this is the coverage. It correctly applies open lesson `contrarian-needs-leverage-anchor` (Finau +7.4 coffin as the leverage floor — the exact fix for the Truist L4 collapse), honors the Potgieter lottery-slot-only call, and rejects Mitchell on mechanism (double dock), not ownership. $49,700 verified.

**What must ALL be true to win:**
1. Five chalk-tier anchors (Fleetwood, Fitzpatrick, Burns, Rai, Reitan) ALL go median-or-worse. Low joint probability — but that's what a chaos hedge is for, and it costs one lineup of three. Legitimate.
2. Thorbjornsen spikes. Attack the pivot math: he gives up ~10 projected points (60.2 vs Reitan's 70.2) and ~11 ceiling points (98.3 vs 109.4) to buy ~14 ownership points (7.0% vs 21.3%). At a 1,764 field that trade can be right, but it's a real price, and his 62.2% make-cut makes him the second cut risk in the build.
3. Potgieter (53.4% make-cut, ETR course-fit **dock**) survives and bombs his way up the board. Note the venue file actually *supports* his thesis (ARG explained ~6% of variance — short game barely mattered; soft + wide + top-15 driving distance), so this is a defensible disagreement with ETR, correctly confined to a lottery slot.
4. It out-scores other chaos-positioned field lineups — and here's the soft spot: L3 has the **lowest aggregate ceiling in the portfolio** (591.5 vs 613.1/597.5) and its highest-owned pieces (Cole 15.9%, Rose 16.0%) are at the very top of the band the thesis says the winner comes from. Lowry is explicitly a cap-compliance pick ("keeps the build inside the ≤2 sub-10% cap"). A chaos lineup with a stability piece and zero sub-4% exposure is betting on *mild* chaos.

**Leverage audit.** Thorbjornsen 7.0% and Potgieter 4.6% are genuine. Cole at 15.9% and Rose at 16.0% are mid-chalk — fine for the thesis as framed, but nobody should call this a deep-contrarian build: cumulative 66.0% misses the sub-65% chaos target (admitted), and the framework's "deep contrarian <4%: required in tournament-winning builds" tier is represented nowhere in this lineup.

**Why SHIP.** The mildness is lesson-driven, not lazy — `contrarian-needs-leverage-anchor` was born from exactly the wild four-coin-flip build this avoids, and the ≤2 sub-10 cap was honored deliberately. The fix I wanted to name (swap Cole or Lowry for a sub-4% piece like Fishburn) breaks either the ≤$300-unused rule ($1,600 left) or the sub-10 cap. Within the codified rule lattice this is the chaos build. See P6 for the rule-scoping question this raises.

## Portfolio-level findings

**P1 — The entire edge rests on one uncalibrated vendor's internal disagreement with itself.** Single-source week, and `vendor_calibration.jsonl` doesn't exist (Memorial matched 0 projections). The slate's headline edge — Rai +25.3 — is ETR's optimal exposure (50.2%) minus ETR's own ownership projection (24.9%). Both halves are ETR artifacts. Worse, the gap is self-eroding: in a $12 contest drawing ETR subscribers, actual ownership drifts toward the published recommendation, so Rai could come in at 30%+ and the "largest overweight ever logged" compresses toward zero. This is the mirror image of open lesson `fade-needs-ownership-to-materialize` — *overweights* need ownership to stay low to pay, and there is no calibration evidence ETR projects ownership well. Nothing in the build violates a rule here, but 2/3 Rai exposure is the portfolio's biggest single bet and it's a bet on an unverifiable number.

**P2 — Shared failure mode: a bomber leaderboard beats all three lineups at once.** The portfolio is an accuracy-thesis monoculture: Rai (2/3, #1 driving accuracy), Fitzpatrick, Rose, Lowry, Fleetwood, Cole. The venue file itself says wide fairways (top-15 on Tour), soft conditions, top-15 adjusted driving distance, "green light for driver" — ETR's accuracy tilt is a *light* tilt they applied after clipping outliers, and the Value Report argued the opposite. If distance wins the week (Burns, Hojgaard, Pendrith, the docked bombers), the only coverage in 18 roster slots is Potgieter's single lottery slot in L3. The zero-exposure trap-tier decision (Burns ~20%, Hojgaard 15.4%) is simultaneously a full fade of the distance scenario. No rule violated — but this is the one game-state that kills L1 AND L2 AND L3 together.

**P3 — Reitan 0/3 partially repeats the pattern the open lesson warns about.** The Mitchell rejection is clean (mechanism: double dock). Reitan is not: lineups.md says his exclusion is structural, but one of the two stated reasons — "his 21.3% own breaks L3's sub-65% chaos target" — is ownership-premised, and the precedent case for `fade-needs-ownership-to-materialize` is *Reitan himself* (projected ~26.5%, came in at ~11% actual at the Memorial, landed in half the winning SE top-5). If his ownership undershoots again, the portfolio holds zero of the tier-1 anchor most likely to be mispriced leverage. Within the slate analysis's stated 0–1 range, and documented for process-grading — but the red team's read is that 0/3 is the aggressive end of a call the ledger has already burned us on once.

**P4 — Cumulative-ownership accounting uses the friendlier column.** All three lineup tables and the portfolio average (75.4%) use snapshot ownership, which the slate analysis itself flagged as the small-field column. At large-field numbers: L1 ≈ 93–96%, L2 ≈ 81%, L3 ≈ 68%, portfolio average ≈ 81–84%. The disclosure exists in the audit ("ETR large-field reads higher") but the in-range conclusions don't survive the correct numbers for L1/L2. Not dishonest — but the next autopsy should grade against large-field ownership, not snapshot.

**P5 — Three players at the 2/3 hard cap couples every lineup pair.** Rai (L1+L2), Finau (L1+L3), Lowry (L2+L3). The framework's soft guideline for 3-max is "prefer 1 of 3"; this portfolio puts three different players at the hard cap, so any one of three busts damages two-thirds of the portfolio. Rai at 2/3 has explicit slate-analysis backing; Finau and Lowry at 2/3 are convenience overlaps that were never argued for anywhere.

**P6 — Chaos coverage is structurally thin, and a rule-scoping question caused it.** Across 18 slots, exactly one player is under 4% owned (James, 3.0%, in the *conviction* lineup of all places). The designated chaos lineup has none. Cause: the ≤2 sub-10% leverage cap — which framework §4A scopes to **SE** builds ("in 3-max or 5-max, distribute leverage plays across separate lineup angles," §5) — was applied as a hard cap to all three lineups. That reading may be right, but it guarantees the chaos lineup can never actually reach the deep-contrarian tier the framework calls "required in tournament-winning builds." Worth a lessons.yaml hypothesis after this slate, whichever way it resolves.

**No Anchor-Equivalence violations.** Group 1 (Burns/Fitzpatrick/Reitan/Rai, 19.4–22.9%): portfolio leans Rai, Fitzpatrick anchors L2 — alternative satisfied. Group 2 (Bridgeman/Clark/Rose/Cole/Hojgaard/Morikawa, 15.1–17.5%): Clark (L1), Rose and Cole (L3) — satisfied, docked names excluded. Verified against rosters.

**Open lessons scorecard:** `contrarian-needs-leverage-anchor` applied (L3/Finau — though +7.4 is below the +10 spine-grade bar, the slate analysis itself blessed Finau-or-James as the anchor); `ch-scan-needs-skill-gate` applied (Suber-only gate, correct); `fade-needs-ownership-to-materialize` partially applied (Mitchell clean, Reitan half-ownership-premised — P3); `entered-lineups-must-trace-to-plan` carried as a process note — unverifiable pre-lock, lives or dies on what gets entered.

## Pre-flight audit

Each checklist line in lineups.md verified against the underlying files, not trusted:

| Line | Verdict | Evidence |
|---|---|---|
| Slate confirmed | **VERIFIED** (minor nit) | Bundle is this slate (RBC Canadian Open, Ben James debut, Fox defending). Nit: checklist cites "bundle generated 00:25"; the bundle file header reads 00:31 — likely regenerated between; immaterial, same slate |
| Projections loaded | **VERIFIED** | Bundle confirms ETR PGA, 147 players, $6,000–$10,500, single source. All 18 rostered players' salary/proj/own/make-cut figures recomputed from session data — exact matches, all three salary sums correct ($49,900 / $50,000 / $49,700) |
| Venue file read | **VERIFIED** | `rules/pga_classic/courses/tpc_toronto_osprey_valley.md` exists, is marked UNVERIFIED stub as claimed, and contains every cited read: 0.06 stickiness, 3.75" rough as only defense, accuracy tilt, ±0.3 pt wave impact |
| Open lessons reviewed | **VERIFIED, one soft spot** | Exactly 4 open lessons in lessons.yaml, all four genuinely addressed in the build (not name-dropped). Soft spot: the Reitan disposition is half-ownership-premised (P3) while claiming to be structural |
| Framework pre-lock checks | **VERIFIED, one accounting flag** | A-E groups covered (verified above); sub-10 counts 2/2/2 ✓; ≥1 sub-8% piece per lineup ✓ (James 3.0 / Suber 4.6 + Fisk 4.7 / Potgieter 4.6); unused salary $100/$0/$300 ✓. Flags: ownership-band compliance computed on the small-field column (P4), and L1's "sub-55% make-cut: 0" is technically true with both bottom pieces at 56.8%/58.7% — threshold-gaming, not falsehood |
| Prior results scanned | **VERIFIED** | results.jsonl confirms Memorial best 3.5% of 23,781; the ~12.5% winner own / ~2 sub-10 pieces figures match the lessons.yaml entry (12.25 / 2.24). Calibration claim confirmed the hard way: vendor_calibration.jsonl does not exist at all — "no usable rows" is accurate |

**No rubber-stamps found.** Every checked line was actually done. The two honesty flags (snapshot-vs-large-field ownership accounting, make-cut threshold-gaming) are disclosed-but-minimized framings, not fabrications — both should be graded against the harder numbers in the autopsy.

---

_Findings only — no lineup files were modified. The user decides what to act on._
