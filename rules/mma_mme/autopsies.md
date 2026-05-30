# MMA DFS Autopsies — MME (150-Max GPP)

**Contest Type:** Multi-Entry / 150-Max GPP
**Document Type:** Slate-by-Slate Post-Mortems
**Last Updated:** May 17, 2026
**Companion Files:** MME_mma_philosophy_2026-05-17.md, MME_mma_framework_2026-05-17.md

---

Slate-by-slate post-mortem record for MME (150-Max) contests. Each entry documents what was believed, what happened, and what the lessons are. Update within 48 hours of every slate.

---

## 2026-05-09 — UFC Chimaev vs. Strickland

### Contests Played

| Contest | Buy-in | Field | Top Prize | Result |
|---|---|---|---|---|
| $0.50 MME (150) | $75 | 59,453 entrants | $2,500 | 18/150 cashed (12%) — net loss |

### Pre-Slate Beliefs

- **Chimaev was a 100% lock.** Correct. Scored 105.08 in lopsided wrestling decision over Strickland.
- **Taira/Van co-main was the duplication trap.** Correct framing — 86% combined field ownership.
- **Brady was a chalk fade target before injury news.** Defensible at 33% field ownership.
- **King Green was over-priced relative to projection.** Per DailyFan, Green's mean projection of 73 ranked poorly per dollar at $9,200. We ended at 2.7% exposure across 150 MME lineups.
- **The leverage punt slot should be Stephens (8% owned, 28% win odds).** Forced into 30% of MME lineups via Player Group Min.

### What Actually Happened

Top scorers of the slate:
- Sean Brady — 136.27 (24.6% drafted) — **TOP scorer**
- Joshua Van — 131.63 (45.1%)
- King Green — 122.02 (18.2%)
- Yaroslav Amosov — 114.56 (27.9%)
- Jose Ochoa — 108.67 (13.6%)
- Khamzat Chimaev — 105.08 (60.6%)

Total blanks (our portfolio touched these heavily):
- Joaquin Buckley — 5.20 (we had 24% in MME)
- Jeremy Stephens — 2.61 (we had 30% in MME)
- Joel Alvarez — 3.40 (we had 20% in MME)
- Jared Gordon — 14.32 (we had 12% in MME)
- Mateusz Rebecki — 40.66 (we had 22% in MME)

Winning lineup: **Chimaev / Brady / Green / Van / Amosov / Miller** = 703.36 pts.

Notable: the winning lineup was NOT a leverage stack. It was the higher-EV chalk plays plus two correct contrarian wins (Brady through injury news, Green at 18% field ownership).

### Decision-Level Errors

**1. Brady injury overreaction.** The slate's biggest unforced error. Pre-news exposure was 25% Brady; post-news swap moved 12 lineups to Buckley, ending at 17% Brady / 24% Buckley. Brady scored the most points on the slate (136.27) and KO'd Buckley (5.20). Combined cost: roughly 12 lineups went from a top-tier score to near-zero from that fight alone.

The decision was defensible at the time given a 17% field shift on the news. **The lesson is not "ignore news." The lesson is news-magnitude calibration:**
- A "may be hurt" rumor doesn't justify a 12-lineup swap when the field shift is 17%
- The pre-news Brady exposure (25%) was already a moderate fade of 33% chalk — additional fading on speculative news compounded the position

**2. King Green fade too aggressive.** Green at 2.7% exposure on a -445 favorite (78% win odds) who scored 122 was the largest single under-allocation in the portfolio. The optimizer's projection of 73 mean was materially wrong; Brett's qualitative analysis ("Green has scored 64, 121, 105, 97, and 110 in his last five decision wins") flagged this and was ignored in favor of the model.

The 4 Green lineups Ryan had became his only path to a strong finish. The best lineup (rank 482, 651 pts) was a Green build. **The optimizer was wrong about Green; Brett was right.** This is the canonical case of qualitative read overriding model output — and we did not act on it.

**3. Punt-tier saturation.** Multiple lineups carried Stephens + Gordon + Buckley + Alvarez combinations. When all four blanked, those lineups died regardless of stud performance. The MME's punt-tier discipline rule (max 1 fighter under $7,200 per lineup) was not enforced, and roughly 30 lineups crashed because of compound punt failure.

### What Worked

- **Chimaev lock was correct.** 105.08 from a 60% chalk play that the contest was structurally weighted toward.
- **Heavy Van exposure (43%)** captured a 131.63 ceiling outcome. The co-main sweep call was right.
- **Amosov exposure (23%)** captured a 114.56 win. Strong floor play paid.
- **Best MME lineup at rank 482 / 59,453** demonstrates the portfolio had ceiling; the bigger problem was median lineup quality (445 pts), not absence of upside builds.

### Process-Level Lessons (added to framework)

1. **Late-breaking news protocol updated.** Partial reaction on speculative news; full reaction on confirmed news only.

2. **Qualitative analysis trumps optimizer projection when they conflict and the qualitative source is reliable.** Brett's read on Green's volume-driven scoring history was concrete evidence that the projection model was miscalibrated for him. Watch list for any future fighter where Brett's qualitative analysis materially diverges from optimizer projections.

3. **Punt-tier saturation as a hard rule.** Add to MME pre-submission checklist: no lineup contains more than 1 fighter priced below $7,200.

### What This Slate Was Not

A failure of the overall framework. The Chimaev lock was correct. Heavy Van exposure was correct. The MME structure was sound. **The slate was lost on three specific decisions: the Brady overreaction, the Green fade, and the punt-tier saturation.** The framework is intact; the execution had specific mistakes that have been added to the framework's update log.

---

## 2026-05-16 — UFC Vegas 117 (Allen vs. Costa)

### Contests Played

| Contest | Buy-in | Field | Top Prize | Result |
|---|---|---|---|---|
| $0.50 MME (150) | $75 | 35,672 entrants | $1,500 | Best rank 141, 34/150 cashed — net loss |

Estimated total return: ~$44. Net loss: ~$31.

### Pre-Slate Beliefs

- **No 100% lock exists on this slate.** Correct — confirmed by post-slate review. The flat ownership distribution and absence of mega-chalk plays meant no single fighter justified a lock.
- **Bukauskas fade was the conviction call.** We held him at 26% MME (vs. 45% field). He scored 51.65 (decision win). The fade was correct.
- **Santos + Gantt was the chalk-with-ceiling conviction pair.** Forced via Min 40% cap on Santos and IF/THEN Santos→Gantt rule. Result: Santos lost to Choi (30.82), Gantt won big (129.45). **The pair was 50/50 right.**
- **Veretennikov was a leverage striking dog with KO equity.** We had him at 33% MME. He got KO'd by Williams (6.60 pts).
- **Costa was a defensible value play in main event.** We had him at 45%. He lost to Allen (46.75 pts). Field-matched, no edge given/taken.
- **The seven-build optimization process was sound.** Correct in retrospect on Bukauskas (faded right) and Gantt (over-exposure right). Incorrect on Santos cap (forced overexposure) and Veretennikov boost legacy (over-exposed loser).

### What Actually Happened

Top scorers of the slate:
- Arnold Allen — 142.84 (25.5% drafted)
- Tommy Gantt — 129.45 (36.7%)
- Khaos Williams — 113.02 (25.6%)
- Dooho Choi — 110.53 (22.1%)
- Luis Gurule — 109.78 (24.3%)
- Benardo Sopaj — 109.02 (27.5%)
- Juan Diaz — 108.04 (10.0%)
- Alice Ardelean — 107.55 (28.8%)

**Winning MME lineup (712.90 pts):** Allen + Sopaj + Choi + Diaz + Gantt + Williams. A punt-heavy ceiling stack — Diaz at 7%, Williams at 19%, Sopaj at 24%. **Zero of our 150 lineups had 5 of these 6 fighters. Only 2 had 4 of 6.**

Total blanks our portfolio held heavily:
- Malcolm Wellmaker — 6.00 (we had 42% via Max cap, KO'd by Diaz)
- Nikolay Veretennikov — 6.60 (we had 33% via earlier boost, KO'd by Williams)
- Daniel Santos — 30.82 (we had 45% via Min cap, lost to Choi)
- Andre Petroski — 14.28 (we had 20%, lost to Brundage by TKO)

Best of our 150 MME lineups: **662.81 (rank ~141)**. Cash threshold: 477.48 (top 23%). We cashed 34/150 but most cashes were min-cash $1 returns.

### Decision-Level Errors

**1. Santos Min 40% cap was process drift, not strategy.** Build 5 had Santos at 43% naturally without a cap. The Build 5 → Build 6 transition added a Min 40% cap because we wanted to "force the conviction lean." This was the wrong call. Build 4's natural 33% Santos was probably closer to right — the optimizer's projection was hedging against the exact pace-fight loss scenario that occurred. **Forcing minimum exposures on conviction plays is different from removing maximums on them.** The Min cap removed Santos-light builds where Choi paid off, which is exactly what happened. ~67 lineups had Santos at 30.82 pts.

**2. The IF/THEN Santos→Gantt rule compounded Santos's loss.** When Santos lost, every Santos lineup also had Gantt (mechanically). Gantt's 129 pts couldn't carry the 30-point Santos slot. The pair was designed as conviction-with-correlated-EV; in practice, they were uncorrelated outcomes (different fights) but the rule forced their coupling. **The rule should be a soft preference, not a hard pair.** When one of two paired fighters loses, the other can't compensate for the dead weight at half the salary.

**3. Veretennikov over-exposure was legacy contamination from Build 2.** In Build 2 we boosted him +2 when removing Bukauskas exposure. In subsequent builds, we never explicitly checked whether the boost still made sense at his new natural exposure level. Result: 49 of 150 lineups had Vere, who scored 6.6 pts. **Old adjustments need to be re-evaluated as the build evolves, not just stacked into the next build.**

**4. Wellmaker Max 42% cap was correct in design, wrong in choice of fighter.** The cap held him at exactly 42% — meaning we still had 63 lineups dead on a 6-point KO loss. The cap protected against worse over-concentration but didn't protect against the underlying play being bad. **Wellmaker was the wrong fighter to be 42% on; the cap masked the deeper issue.**

**5. Williams under-exposure (15% MME, 19% field) missed the winning lineup piece.** Williams scored 113 in a high-pace striking win. He was the natural pivot from Veretennikov in the Williams/Vere fight, but we kept Vere as the leverage side because of finish-equity narrative. **In binary striking fights with both fighters having KO equity, the higher-pace fighter is often the better fantasy play regardless of who actually wins.** Williams was the higher-volume striker; we under-indexed on volume.

**6. Sub-16% leverage rule produced Cavalcanti (23% exposure, 25 pts) and Vieira (27%, 63 pts) instead of Minev (9%, 9 pts) or Diaz (7%, 108 pts).** Diaz was a winning lineup piece at 7% actual ownership. The leverage rule preferred Cavalcanti/Vieira because they fit salary more easily, but Diaz was the right leverage anchor. **The leverage rule's salary-fit preference is biased toward mid-tier sub-16% fighters when the real leverage sometimes lives at the punt tier.**

### What Worked

- **Bukauskas fade (26% MME vs. 45% field):** Correct call, executed cleanly. He scored 51.65. ~110 lineups benefited from the fade.
- **Heavy Gantt exposure (62%):** Captured 129.45 ceiling. The Santos→Gantt IF/THEN actually inflated Gantt usefully, even if the Santos side failed.
- **Costa correct fade-match (45%):** No edge, but no error.
- **Punt-tier discipline:** No lineup had multiple punts. The 5/9 autopsy rule held.
- **Bukauskas+Wellmaker concentration reduction:** Dropped from 38 lineups (Build 1) to 14 final. Prevented compound disaster.
- **Best lineup at rank 141 of 35,672:** Top 0.4%. The ceiling existed; the median was the problem.

### Process-Level Lessons

1. **Min caps on conviction plays remove optionality.** When the optimizer wants a fighter at 33% and qualitative analysis says 40%+, the gap between 33% and 40% represents real uncertainty. Forcing the 40% via Min cap eliminates the optimizer's hedge against the projection being right. **Boost beats Min cap for conviction expression.** A Boost +1 or +2 nudges toward the conviction without eliminating the hedge; a Min cap forces the bet.

2. **IF/THEN rules between fighters in different fights create artificial portfolio correlation.** The Santos→Gantt rule made our portfolio behave as if Santos+Gantt were one play. They weren't — they were independent outcomes in different fights. **IF/THEN should be reserved for true correlation (same fight stacking decisions) or anti-correlation (opponent locking), not for "I like both these fighters."** For preferred pairings, use individual exposure floors instead.

3. **Boost/Dock adjustments persist across builds; audit them every iteration.** The Veretennikov +2 boost from Build 2 was never explicitly removed in Builds 3-7 when re-evaluation would have shown it wasn't needed. **Pre-build checklist: review every boost/dock from the prior build before running the next.** Default to removing all adjustments and re-adding only the ones still justified.

4. **The Wellmaker Max 42% cap was right; the underlying conviction was wrong.** Caps prevent disasters but don't fix bad underlying calls. **When a cap on a fighter feels necessary, the deeper question is whether that fighter belongs in the portfolio at all.** Lower-conviction plays should have lower default exposure, not capped high exposure.

5. **The sub-16% leverage rule needs a salary-tier qualifier.** Adding "At Least 1 F where Own % is Less Than 16 AND Salary Less Than $8000" (or similar) would force the leverage anchor into the punt/salary-saver tier where real GPP leverage lives.

6. **Punt-tier saturation rule from 5/9 still held and saved us.** Despite multiple concerns flagged during the build process, no lineup had 2+ punts. This rule is permanent.

7. **The optimizer process can produce diminishing returns.** Seven builds was excessive. Builds 1-3 fixed real problems; Builds 4-7 traded one slight overexposure for another. **A defensible heuristic: stop when the pre-submission checklist passes for the first time.** Build 4 was the first build that passed all 11 checks.

### Process-Level Changes To Framework

Added to MME framework:
- Pre-build checklist item: "Review every Boost/Dock adjustment from the prior build. Default removal; only re-add if still strategically justified."
- Conviction-play exposure rule: "Use Boost over Min cap to express conviction. Min caps are reserved for fighters whose natural exposure trends dangerously low (15%+ under target) AND whose conviction case is iron-clad."
- IF/THEN rule restriction: "Reserve IF/THEN for same-fight stack/anti-stack decisions. For preferred pairings of fighters in different fights, use individual exposure boosts, not conditional rules."
- Build-stopping heuristic: "Stop building at the first build where the pre-submission checklist fully passes."
- Leverage rule refinement: "Consider adding a salary qualifier to the sub-16% leverage rule on slates where mid-tier fighters dominate the sub-16% pool."

### What This Slate Was Not

A failure of the overall framework. The Bukauskas fade was the right call and executed correctly. The Gantt conviction was correct. The portfolio's ceiling reached rank 141 of 35,672 (top 0.4%) — the framework can produce winning ceilings.

**The slate was lost on specific tactical decisions inside a sound framework:**
- Santos Min cap (process drift)
- Veretennikov boost legacy (failure to audit prior-build adjustments)
- Wellmaker cap protecting a play that shouldn't have been at 42% anyway
- Leverage rule producing Cavalcanti/Vieira instead of Diaz/Minev

**The slate was also lost on slate-specific variance** — three sub-25%-owned fighters (Diaz, Williams, Sopaj) all scored 100+ in the same evening, producing a winning lineup composition no projection model would have built and no balanced 150-lineup portfolio would have captured at high exposure. **In a 35K-entrant field with 23% cash rate and top-heavy prize structure, missing the dog-stack scenario is a structural cost of any non-degen portfolio.**

The framework remains intact. The tactical lessons have been added to the framework's update log.

---

## Template for Future MME Entries

### Pre-Slate Beliefs
### What Actually Happened
### Decision-Level Errors
### What Worked
### Process-Level Lessons
### What This Slate Was Not
