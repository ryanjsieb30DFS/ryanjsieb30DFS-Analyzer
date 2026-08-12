# PGA Classic Framework

*Last updated: 2026-08-11*

The tactical playbook. Decision rules, construction templates, and exposure logic derived from accumulated autopsies. This is the *how* document. Updates here should be triggered by patterns in the Autopsies, not by single-week reactions.

---

## 1. Contest Selection

**Primary vehicle: Single Entry (SE).** SE is the default contest type. Every week starts with the SE build; other contest types are extensions of the SE thesis when slate conditions justify them.

**Secondary vehicles: 3-max and 5-max.** Used when slate conditions justify multi-lineup expression — e.g., when a coffin-list leverage spine creates a clear "play these together" opportunity, or when top-tier ownership concentration is high enough that 2-3 distinct anchor angles are defensible.

**Occasional vehicles: 20-max and small-portfolio large-field MME (3-20 lineups in a large-field contest).** Used selectively when the slate has clear structural edges that benefit from broader exposure. Not a default; requires explicit slate-specific rationale.

**Large-field MME (20-max / 150-max): a SEALED parallel track, not the home game (updated 2026-08-03, MME Plan Phase 1).** Single Entry, 3-Max and 5-Max remain the focus set — they drive strategy framing, the sharp-envelope target, grading calibration and the results-trend headline. Large-field MME is played deliberately and logged separately: its finishes never blend into the focus-contest headline (they carry their own best_rank_mme / best_percentile_mme), and the shark and grading accumulators ignore them. The original objection stands as the reason for the separation — 150-max demands construction precision that coarse levers cannot deliver, so it is judged on field exploitation (the 8-error catalog in `docs/mme_plan.md`), not on portfolio mechanics. First logged instance: Rocket Classic 2026, PGA TOUR $35K mini-MAX, 79,274 entries, 20 bullets, best finish 5,201st (top 6.6%).

**Cash games: deprioritized.** Cash play is incompatible with leverage-based construction; the floors required to cash consistently conflict with the ceiling-chase needed in GPPs.

**Critical workflow rule:** At the start of every slate conversation, the contest types being played must be explicitly stated. Analysis is tailored to those specific contests before any builds are constructed. Do not assume contest selection from prior weeks.

## 2. Slate Diagnostics — Run Before Building

Before constructing any lineup, answer these:

- **Cut format?** No-cut signature events boost floor for every player, compressing the value vs studs gap and amplifying the value of high-volatility ceiling plays. Cut events impose binary risk on every player.
- **Field size?** Large-field GPPs demand more contrarian construction. Top-1% scores scale with field; cash-line scores stay relatively flat.
- **Top-end ownership concentration?** If the top 3–5 anchors absorb 100%+ cumulative projected ownership, identify which anchor is "trap chalk" (overowned relative to projection) versus "value chalk" (correctly owned or underowned).
- **Are the analyst projections converging or diverging?** Convergence = the field will see the same plays. Divergence = look for the model edge.
- **Does the coffin list have ≥2 high-conviction overweight plays at sub-15% projected ownership?** If yes, this is the "leverage spine" opportunity.
- **Gated cheap-leverage scan (required):** cross the course-history/pedigree boost list against sub-5% projected ownership, then GATE on a minimum skill/current-form floor — bottom-decile ball-strikers and cold pedigree names are lottery-slot-only regardless of course stickiness. Treat the form/value engine (hot approach numbers, value-report flags) as a CO-EQUAL source of sub-5% leverage; the slate-defining cheap play has come from the form side in every logged test (Poston, Suber, Clark). Pedigree WITHOUT form = bust (Koepka, Shinnecock); pedigree WITH form = the play (Clark; Young, Birkdale).
- **Name the slate's low-owned smash (mandatory scan).** Across 168 slates (2023-2026), **96% had ≥1 golfer rostered in ≥30% of winning lineups while drawing <20% field ownership** (median ~12% own). There is essentially always a sub-radar golfer who smashes and defines the winners — the scan must surface the candidate leverage tier, and a build with zero sub-10% plays fails the structure check.
- **The 10-16% mid-owned band is where Classic slates are decided, not the sub-5% tier alone.** Guarantee explicit PLAY/PASS coverage of *every* mid-priced play projecting a 100+ ceiling in the ~7-20% own band before adding deep darts. Caveat (necessary-not-sufficient): owning the band is required but does not itself win — four straight slates we sat in the band and missed the actual hitters, so this rule must be paired with the vendor-independent ceiling scan (the primary pre-slate identification discipline) that governs *which* members of the band get rostered.

**Vendor-independent ceiling board (codified 2026-07-26).** Before writing Top plays, independently list the ~12-15 highest-ceiling players for the week from the projections + form (best ball-strikers, hottest approach numbers, elite anchors) REGARDLESS of whether the vendor's coffin list or a panel flagged them, and reconcile every elite/mid ceiling against that board so no stud is silently omitted (the Hovland/Morikawa/Burns failure class). The board MUST include recent tournament/major champions and proven closers gated on a current-form floor: any that survive the gate at sub-15% projected own are leverage; pedigree without form stays lottery-only (Koepka).

## 3. Ownership Tier Framework

| Tier | Projected Own | Strategic Role |
|---|---|---|
| Heavy chalk | 20%+ | Consider one per lineup if value chalk; fade if trap chalk |
| Mid-chalk | 12–20% | Most builds will hold 1–2 of these; rotate which ones |
| Soft chalk | 8–12% | Best risk/reward bracket; often where coffin-list overweights live |
| Sub-projected | 4–8% | Targeted leverage plays; the difference between cashing and winning |
| Deep contrarian | <4% | High-volatility ceiling chase; required in tournament-winning builds |

**Avoid playing more than one player from the "trap chalk" tier per lineup.** Trap chalk = a player ETR or your projection source flags as overowned (coffin list negative side).

**Empirical winning-structure baseline (168 slates, 2023-2026 — `mining_2023_2026.md`):** winning lineups average **~13% per-player ownership** (~78% cumulative across the 6 golfers — this is a per-player mean, NOT a lineup total), carry **2-3 sub-10%-owned golfers** (median 2.5; 78% of winners ≥2, 91% ≥1), and are **91% unique**. Target this shape; an all-chalk lineup is a structural non-starter. Stable every year 2023-2026.

**Dart-count calibration:** hold ~13% average per-player ownership, and set the per-lineup sub-10% dart count by course archetype: birdie-fest ~2; no-cut birdie-fest ~2.5; tough non-cut ~3; tough or birdie-fest WITH a 36-hole cut, cap at ~2–2.5 (each added cut-coinflip multiplies binary cut-out risk). Verified: mining n=168 plus RBC (~2), Shinnecock (2.1–2.7), Travelers (2.5), Birkdale (2.25).

**Portfolio-level low-owned RATE (codified 2026-08-03).** The per-lineup dart count above governs a single lineup; this governs the SET. In small-field 5-Max, hold the share of your lineups carrying a sub-5%-owned piece near the observed in-field pro rate — roughly "one sub-5% piece in most lineups," not one in nearly every lineup plus extras. Mechanism: at 5 bullets in a ~2-3K field your lineups are already 100% unique, so a marginal sub-5% piece buys no uniqueness and only adds bust risk, while the slate-definers keep landing in the 10-20% own band (5 of 6 at the Rocket Classic; 4 of 5 at the 3M; 4 of 4 at Birkdale). Verified across four slates as the top structural shark gap, always in the same direction: +53.3 (Shinnecock), +60.0 (Birkdale), +20.0 (3M), +16.4 (Rocket). Push freed slots UP into the 10-20% definer band, not down. **Corollary (Rocket Classic):** once the rate is near the pro envelope, the residual gap moves to average ownership per slot — target the winners' ~12-13%, and trim it from the crowded anchor, not from the cheap pieces.

## 4. Roster Construction Templates

These are starting structures, not rigid rules. Modify based on slate diagnostics.

### A. Single Entry — Default Template

For the standard SE GPP build, target six players that express the slate's structural reads in one coherent thesis:

- 1 elite top anchor ($10K+) — the model's #1 or #2 baseline, value chalk preferred over trap chalk
- 1 mid-tier $8K-$9K play — pivoting off field-default chalk in this range
- 1 leverage spine play ($7K range) — coffin-list overweight at sub-10% projected ownership
- 1 value engine ($6K-$7K range) — slate's best value chalk (coffin-list overweight, often projected 20%+)
- 1 sub-5% lottery ticket — course-history-boost + low-ownership candidate, or analyst-specific value report play
- 1 cheap unique ($5K-$6K) — if floor allows, otherwise replace with second mid-range piece

**Critical SE rule:** Never run a single-entry lineup with three or more high-conviction sub-10% leverage plays. Correlated bust risk on multi-leverage-spine SE lineups is real (PGA Championship 2026: Keegan + Hatton + Hovland all busted in unison). Cap leverage spine at 2 plays per SE; use the third slot for value chalk or anchor stability.

### B. 3-Max Template

Three lineups, three distinct slate-outcome theses. Each lineup expresses one structural angle:

- **Lineup 1: Model conviction.** Top of the board includes the model's #1 anchor. The "trust the projections" build. Lower variance, higher floor.
- **Lineup 2: Coffin chalk leverage.** Top of the board pivots to the coffin-list overweight at the top tier. The "field underowning the right player" build. Higher leverage.
- **Lineup 3: Contrarian / chaos.** Top of the board features a sub-10% own top-tier play (e.g., the model's #5-#7 with strong skill baseline). The "chaos slate" build.

Shared spine across all three: the value engine (coffin chalk at $6K) and 1-2 mid-range leverage plays.

### C. 5-Max Template

Five lineups, five distinct slate-outcome theses. Add two angles to the 3-max template:

- **Lineup 4: Double-tap top.** Two $10K+ plays at the top, leaning into the field's expected stars-and-scrubs structure but with internal differentiation in the value tier.
- **Lineup 5: Pure leverage spine.** Built around 2-3 coffin-list overweights, paired with a mid-tier value play and one sub-5% lottery ticket. The Truist L1/L3 template.

### D. 20-Max / Small-Portfolio Large-Field MME Template

When playing 3-20 lineups in a large-field contest, treat the build as a *scaled portfolio* rather than a thesis-per-lineup approach:

- 25-35% of lineups: Lineup 1 conviction template (model #1 anchor)
- 25-35% of lineups: Lineup 2 coffin chalk leverage template
- 15-25% of lineups: Lineup 3 contrarian / chaos template
- 10-20% of lineups: Lineup 5 leverage spine template
- 5-10% of lineups: deep contrarian (sub-65% cumulative ownership)

Maximum single-player exposure: 35%. No player in more than 70% of lineups in any portfolio size.

## 5. The Leverage Spine

When 2 or more players appear on the coffin list as significant overweights (≥+10% gap between recommended and projected ownership), treat them as a near-permanent feature across multiple lineups in the portfolio.

**Why this works:** A coffin-list overweight at sub-15% ownership offers ceiling-equivalent exposure to a chalk play at materially lower duplication risk. When two such plays exist on the same slate, deploying both in the same lineup compounds the leverage advantage.

**Truist validation (May 2026):** JT (+16.6% coffin) + Bradley (+12.1% coffin) deployed together in L1 and L3 produced 164 combined points at sub-19% combined ownership. L1 missed cash by 2 points only because the cheap pieces (Berger, Straka) busted; L3 cashed.

**Multi-leverage-spine cautionary note (PGA Championship 2026):** The leverage spine concept validates when 2 coffin-list overweights are deployed together. It does NOT validate when 3+ independent high-conviction leverage plays are stacked in a single SE lineup. The Keegan + Hatton + Hovland triple-stack collapsed in unison (15 + 20 + 22.5 = 57.5 combined FPTS) despite each play being individually defensible. **Correlated bust risk increases non-linearly past 2 leverage plays per lineup.** In SE format, cap at 2 leverage plays per build; in 3-max or 5-max, distribute leverage plays across separate lineup angles rather than concentrating them.

## 6. Anchor Selection Logic

**Three-question filter for top-end:**

1. Who does the model rank #1 in current skill baseline + course fit?
2. Who does the field appear to be most crowded on (steam vs projection)?
3. Which anchor's price tag leaves room for the leverage spine and value engine?

**Default policy:** Do not zero-out the model's projection #1 across the entire portfolio. If the model says Player X is the best player on the slate and the field crowds on X at expected levels (not 5%+ above projection), at least one lineup carries X. The Truist Aberg miss validates this rule.

**Trap chalk vs value chalk (narrowed 2026-08-03 after a third mechanism failure).** The coffin list PROPOSES the trap/value split; ownership disposes it — and the split is only usable BELOW the field's top crowding tier. **A player projected inside the slate's top-3 field ownership may not be labeled "value chalk" on a coffin gap at all**, however his ownership behaves: at ~25%+ own he is the crowd's anchor, and sizing him is a chalk-exposure decision on his own merit (skill, form, fit, price), not a leverage decision. Evidence for the ceiling: Rai at the RBC (own steamed to ~30%, busted), Fitzpatrick at Birkdale (25.5%→37.6%, 22.0 FPTS, 54.1% of fish vs 2.8% of winners), and Gotterup at the Rocket Classic (coffin +7.1, 27.3% projected → 26.7-29.7% actual — dead flat, no drift prong available — yet the #1 fish trap in BOTH contests: 47.1% of fish vs 0.0% of winners, and 40.4% vs 0.4%). Below that tier the original split still holds: a coffin fade is void when projected ownership never materializes (sub-12% actual = mispriced leverage, not trap — Memorial), and a stable floored name at flat projected own keeps its coffin label (Burns, Shinnecock).

**A fade is conditional on the ownership materializing.** Before locking any coffin/writer fade, sanity-check the player's actual/late ownership read: if it is sub-~12%, the fade premise is void and the player is mispriced leverage, not trap chalk. A sub-10% "fade" is not a fade — it just zeroes cheap upside. (Repeatedly cost slate-definers: Reitan/Clark at the Memorial, Reitan at the RBC, Fitzpatrick at the Travelers.)

**Single-vendor self-erosion guard (codified 2026-07-26).** An edge defined as one vendor's published optimal exposure minus that same vendor's ownership projection (a coffin overweight) is a sizing NOTE, never the portfolio's biggest bet, unless a second independent reason (form, skill, course fit) supports it. On narrative/rising names in vendor-subscriber contests, expect actual ownership to drift UP toward the published optimal and erode the gap by lock (Rai 25→30% RBC; Fitzpatrick 25.5→37.6% Birkdale; Kohles 19.2→25.7% 3M). The guard does NOT fire on stable, floored value chalk sitting at flat projected own (Burns, Shinnecock) — absent a concrete reason to expect own inflation, default to the trap-vs-value read and play the overweight.

## 7. Exposure Caps (Multi-Lineup Portfolios)

For multi-lineup portfolios, the exposure ceiling scales with portfolio size:

| Portfolio Size | Hard Cap (single player) | Soft Guideline (key anchor) |
|---|---|---|
| 3-max | 2 of 3 (67%) | Use sparingly; prefer 1 of 3 |
| 5-max | 3 of 5 (60%) | Top 2-3 anchors only |
| 20-max | 35% | Top conviction overweight |
| Small-portfolio MME (3-20 lineups) | 35% | Top conviction overweight |

The portfolio cap protects against the reverse failure mode — when a high-conviction play bombs in all lineups simultaneously.

**Soft guideline: every lineup should have at least 1 player at sub-8% projected ownership.** If a lineup has zero sub-8% pieces, it is structurally identical to thousands of field lineups; no path to the top 0.1%.

**Per-contest UNDERWEIGHT floor (codified 2026-08-11).** An UNDERWEIGHT call on top-skill contested chalk means at least one bullet IN EACH entered contest (in a 1–5 entry contest: exactly one). Check the floor per contest, never on the pooled entry set — 0-of-N in the focus contest is a full fade the analysis never argued.

**Exposures before lineups:** before building any multi-lineup set (and even a single bullet), write target exposures first — the value spine's carry rate, the mid-owned multipliers, the dart pool drawn FROM the strategy's definer screen, and a hard cap per expensive chalk anchor — then fill lineups to those targets. Independent lineup-by-lineup assembly has no governor: the screen's best value loses slot competition (Young 0/5 at Birkdale as the winner's carrier; Fox/Yellamaraju at RBC) and incoherent chalk-stack builds slip through.

## 8. Pricing & Salary Allocation

**Typical signature event allocation:**
- Top 1–2 anchors: 38–45% of cap
- Mid-tier ($8K–$9.5K): 20–25% of cap
- Leverage spine: 25–30% of cap
- Cheap unique: 10–13% of cap

Leaving more than $300 in unused salary is a sign of either over-conservative pricing or a missing player in the build.

## 9. Pre-Submission Checklist

**Every entered lineup must trace to the written plan, or the deviation is logged pre-lock with a one-line rationale.** A checklist line at submission: for each entered lineup, name the plan lineup/Decision it maps to; any player not in the plan requires a recorded reason. Undocumented deviations forfeit the process grade and any red-team/portfolio safety net (Memorial, RBC, and Travelers all off-plan with no `lineups.md`; Shinnecock on-plan and fully gradeable — the discipline is the difference).

### A. Single Entry Checklist

- [ ] At least one player from the coffin-list overweight side
- [ ] No more than one player from the coffin-list underweight side
- [ ] At least one sub-8% ownership piece
- [ ] No more than $300 unused salary
- [ ] No more than 2 high-conviction sub-10% leverage plays in the same lineup (correlated bust risk)
- [ ] Gated cheap-leverage scan run: at least one candidate considered that passes the skill/current-form gate (CH/pedigree boost × sub-5% own × form floor, or a form/value-engine flag)
- [ ] Ceiling board run vendor-independent? Every top-12-ceiling player has an explicit surfaced read (no silent omissions).
- [ ] Cumulative projected ownership in target range (signature events: 70–90%; large field: 60–80%)
- [ ] No combination flagged as "avoid" in the slate preview (e.g., chalk-on-chalk traps)

### B. 3-Max and 5-Max Checklist

- [ ] Each lineup expresses a distinct slate-outcome thesis (no near-duplicates)
- [ ] Portfolio exposure cap respected (3-max: 2/3 max per player; 5-max: 3/5 max)
- [ ] At least one lineup carries the model's #1 anchor (anti-Truist blind spot rule)
- [ ] At least one lineup is positioned for the "chaos slate" outcome (sub-65% cumulative ownership)
- [ ] The leverage spine (when present) appears in 60-80% of lineups, not 100%
- [ ] No player appears in every lineup (forces internal differentiation)
- [ ] Gated cheap-leverage scan (CH/pedigree × sub-5% own × skill/form floor; form/value engine co-equal) completed
- [ ] Ceiling board run vendor-independent? Every top-12-ceiling player has an explicit surfaced read (no silent omissions).

### C. Small-Portfolio MME Checklist (3-20 Lineups)

- [ ] Portfolio distribution matches Section 4D template percentages
- [ ] Maximum single-player exposure ≤35%
- [ ] At least one lineup with cumulative ownership <65% (deep contrarian coverage)
- [ ] All four major slate-outcome categories represented (chalk wins / leverage spine wins / chaos / model-default)
- [ ] Gated cheap-leverage scan candidates (skill/form-gated) considered for at least 2-3 lineups

## 10. Tracking Stats (Build Weekly)

Maintain a rolling log of these metrics. Patterns over 8+ weeks should trigger framework updates.

- Cash rate by contest type
- Average finish percentile by contest type
- Coffin-list hit rate (when overweight plays exceeded projection)
- Reverse coffin-list hit rate (when fades validated)
- "Slate lock" identification rate (did I have the player who appeared in N/N winning lineups)
- Course-history-boost + sub-5% own play identification rate (did the slate-defining play meet this criterion, and did I have exposure)
- ROI by contest type

## 11. Quality of Rules Discipline (Cross-Sport Operating Principle)

Per Philosophy Section 11: use the fewest, sharpest constraints that produce the desired structural outcome. Every rule must earn its place by addressing a specific failure mode. If a build needs more than 3-5 core constraints, the strategy is wrong, not the rules. Two-build maximum per slate.

This applies whether building 1 SE lineup, 3-max, 5-max, or small-portfolio MME. The rule-construction discipline does not change with portfolio size.

---

*This document evolves through Autopsy patterns. Do not modify based on single-week outcomes; require 3+ weeks of consistent signal.*
