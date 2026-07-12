# Post-Autopsy Review — UFC 329 (McGregor vs. Holloway) · 2026-07-12

Two 291-field SEs (UFC $10K Counter Punch, entered as SE bullets). Winning score **686.38** in both. Best finish **rank 76 / 26.1%ile**. Standings-only autopsy — no projections at autopsy time. ROI omitted by design (tracked in the user's third-party app).

**The winning lineup (both contests):** Holloway (96.3) · Pimblett (117.7) · Pinas (110.7) · **Bautista (137.43)** · Gandra (104.2) · Green (120.1) — six winners, zero busts, ~40.2% avg own, one low-owned definer (Bautista 15-16%).

## Process scorecard

**Pre-flight checklist: PRESENT and HONEST.** Every box was checked with specifics — slate freshness confirmed (bundle 2026-07-11, both articles 7/11), 2/2 files read (none skipped/unparseable), the single-vendor limitation named, all 8 open lessons individually applied-or-rejected with mechanism reasons, Anchor-Equivalence run, results.jsonl scanned, sharp envelope noted. No checklist honesty gap. This is the strongest process artifact in the ledger's history.

**Lessons applied vs. ignored — did ignored ones cost?**
- **Applied and RIGHT:**
  - `leverage-is-the-low-own-finisher` (partially) → played Green (28%) over McKinney as the -1200 leverage side. **Green 120.1, McKinney 29.8** — the single best individual call on the slate, and Green is in the winning lineup.
  - `confirmed-vs-speculative-news` / article-vs-projection edge → trusted both Matchups writers over the projection and played **Pimblett** (both writers' pick) over BSD. **Pimblett 117.7, BSD 0.5** — an elite, high-conviction call; BSD was the slate's #1 fish trap (55.9% of fish, 0.5 pts).
  - `finish-capable-favorite-is-not-secondary-chalk` → kept Pinas (26%) and treated mid-own finishers as cores. **Pinas 110.7, Gandra 104.2** — both in the winner.
  - `cap-single-favorite-exposure` / `fade-on-structure` (McKinney) → underweighted the 46% McKinney chalk. McKinney busted (29.8) and was the field's top fish trap in contest 2. Correct.
- **The costly gap — `leverage-is-the-low-own-finisher` was applied too narrowly.** The strategy hunted low-owned leverage only among **article-named favorites** (Kavanagh 17, Costa 20, Yanez 17, Riley 11) — none hit (Kavanagh 42.7 losing to Royval; Costa/Yanez not in the winner). The actual slate-definer, **Mario Bautista (137.43, 15-16% own, #1 score, in both winners)**, sat in a fight the strategy **actively faded** ("Sandhagen/Bautista — trap to fade, distance-leaning, no path to a smash"). **Brandon Royval** (114.79, ~20%, slate-defining) was the second below-spotlight definer — also on the faded side (the strategy played Kavanagh, the chalkier favorite, over him). This is the exact 6/27 Kaan-Ofli failure mode, one slate later, and worse: not just un-surfaced but affirmatively faded.

**Did the PLAY/PASS/MIX decisions and Top plays hold up?**
- **Decision 1 (Anchor-Equivalence, lean Steveson):** Sound. Steveson 116.7 > Holloway 96.3, both live; the winner used Holloway but Steveson-side lineups (spades20 rank 4, cdem06811 rank 6) also cleared. Presence on both sides was correct; no cost.
- **Decision 2 (Green over McKinney):** **Best call of the slate.** Green in the winner; McKinney the fish trap.
- **Decision 3 (low-owned favorite-finisher as differentiator — Costa/Kavanagh/Yanez):** Directionally right instinct, wrong horses. The chosen favorites did not convert; the differentiator that won (Bautista) was outside the screen because the fight was faded.
- **Decision 4 (PASS the sub-10 KO-or-bust dogs):** Correct — Ellison/Garbrandt/Garza did nothing; McGregor (the user's own contest-2 dog, 1.0) confirms the small-field binary fade.
- **Top plays overall:** The chalk/finisher reads were strong (Green, Pimblett, Pinas, Steveson, Gandra all 104-120) — the strategy correctly identified 5 of the winner's 6 fighters as plays. **The one miss (Bautista) was the differentiator, and it was faded, not merely omitted.**

**User execution vs. strategy (standings show two leaks the strategy did NOT prescribe):**
1. **McGregor in contest 2 (1.0).** A +225 main-event KO-or-bust dog the strategy explicitly said to PASS — a fish trap (0% of winners). One dead slot capped a build that otherwise held Pimblett/Steveson/Green.
2. **Cortez (a "trap to fade" fighter) in BOTH entries (35.1).** Rostering a faded piece across both SEs is a mild shared-conviction/`no-identical-core` drift and cost live ceiling.
3. **Reese (2.0)** in contest 1 — a losing cheap-slot dog. The winner's cheap end (Bautista/Gandra) were **winning** favorites, not relief dogs. Reinforces `cheap-slot-prefer-floor-or-live-dog`.

**Net:** Strong strategy process (best checklist to date; 5 of 6 winner fighters flagged as plays; two elite individual calls in Green and Pimblett), undone at the margin by (a) the recurring low-own-definer blind spot — searching only named favorites/dogs and fading a whole "distance" fight the definer came from — and (b) user-side execution deviations (McGregor, doubled Cortez, Reese) onto losing slots the strategy warned against.

## Lesson ledger changes

- **`mma-se-2026-06-27-leverage-is-the-low-own-finisher-not-the-named-dog`** → **hypothesis → validated.** Added 7/12 confirmation: Bautista (137.43, 15-16% own, in both winners) was the below-spotlight definer, and the strategy faded his whole fight; Royval a second such definer. Second confirming slate (origin 6/27 + 7/12) — one short of promotion.
- **`mma-se-2026-06-20-finish-capable-favorite-is-not-secondary-chalk`** → added 7/12 confirmation (Pinas 110.7 / Gandra 104.2 / Green 120.1, mid-own finish-capable favorites, all in the winner, none trimmable). **Origin 6/20 + 6/27 + 7/12 = 3 confirming mechanism slates → promotion candidate** (see Proposed codifications).
- **`mma-se-2026-06-20-fade-on-structure-not-narrative`** → added 7/12 confirmation (the narrative-punishment half, previously untested, confirmed: the Sandhagen/Bautista + Cong/Cortez pace-narrative fades were punished by Bautista 137.43 and Cong 90.46). Kept **validated** — this was a whole-fight/live-dog fade, an *extension* of the "live chalk piece" object rather than a clean replication, so held one short of a promotion proposal pending a clean chalk-piece test.
- **`mma-se-2026-06-27-finish-heavy-small-fields-still-won-by-differentiation`** → added a 7/12 **confirmation of the low-own-definer half** AND a 7/12 **mechanism-refining contradiction of the avg-own-target half**: the 291 finish-heavy field was won at ~40.2% avg own / 0 sub-10 (chalk-anchored + one low-owned definer), NOT the prescribed 16-20% avg-own build. Kept **hypothesis** (one contradiction, GPP-guarded — cited the winner's structure, not the loss). Reframe toward "differentiate through low-owned WINNING favorites + carry no likely-loser slot," not "cut whole-build avg-own."
- **`mma-se-2026-05-16-binary-leverage-weak-in-small-fields`** (codified) → added 7/12 confirmation via execution deviation: user's McGregor (+225 dog, 1.0, fish trap) in a 291 field; the strategy correctly PASSed all binary dogs.
- **NEW hypothesis `mma-se-2026-07-12-distance-fight-is-not-low-ceiling`** (born 7/12): "distance-leaning" ≠ "low ceiling" — a high-pace/high-volume/high-control fighter winning a dominant decision reaches 120-140+ with no finish (Bautista 137.43 from a fight faded as a distance trap; Cong 90.46). Before fading a fight for going the distance, check projected pace/volume/control. Links the low-own-definer and fade-on-structure lessons.

## Venue file changes

**None — MMA has no venue file** (per CLAUDE.md: tracks/courses/parks exist for NASCAR/PGA/MLB; "mma has none"). Nothing to create or append. The pre-flight checklist correctly recorded this as N/A.

## Proposed codifications

Proposals only — not applied. User approves in the Autopsy tab.

### 1. Codify `mma-se-2026-06-20-finish-capable-favorite-is-not-secondary-chalk` (3 confirming slates: 6/20 origin, 6/27, 7/12)

The "20%+ own = secondary chalk, trim it" rule (framework.md §"Secondary Plays Are Not Leverage") has now been over-broad in three straight slates — it would have cut slate-definers each time (6/20 Oliveira 122.51; 6/27 Abus 105.08 / Camilo 101.69; 7/12 Pinas 110.7 / Gandra 104.2 / Green 120.1). Propose adding a bounded exemption immediately after that section.

**Exact edit — `rules/mma_se/framework.md`, insert a new subsection after line 144 (the end of "### Secondary Plays Are Not Leverage"):**

```markdown
### Finish-Capable Favorites Are Not Secondary Chalk (7/12/26 — 3-slate validated)

Ownership alone does not make a mid-priced favorite a leak. EXEMPT from the "trim the
20-25% chalk" instinct any **finish-capable favorite in a clean matchup** — a real
finishing (or dominant-decision) path at mid ownership is a legitimate high-exposure
core, structurally distinct from a no-ceiling decision-grinder at the same ownership.
Screen the piece, not the number: a clean finish/dominance path → core; a capped,
decision-dependent grinder → trimmable.

Evidence (3 slates): 6/20 Oliveira (25% own, flagged "trim to 3-4") went 122.51 and
anchored the field winner + the user's best build. 6/27 Abus (17%, 105.08) and Camilo
(18-20%, 101.69) were slate-definers. 7/12 UFC 329 Pinas (26%, 110.7), Gandra (29-33%,
104.2) and Green (28-35%, 120.1) were three mid-own finish-cores, all in the 686.38
winner. Trimming any as "secondary chalk" would have cut the winning spine each slate.
```

### 2. Not yet — `fade-on-structure-not-narrative`

Reaches a 3-slate count but the 6/27 confirmation was the structural half only and the 7/12 confirmation is a whole-fight/live-dog extension rather than a clean "live chalk piece" replication. Hold for one more clean test before codifying. The specific distance-lean error is now carried by the new `distance-fight-is-not-low-ceiling` hypothesis; let that mature separately.

### 3. Retirement candidates

None this slate. No lesson has 2 mechanism contradictions. The single contradiction logged against `finish-heavy-small-fields-still-won-by-differentiation` is a mechanism *refinement* (the avg-own numeric target), not a retirement — the lesson's core (catch ≥1 low-owned definer) was confirmed, and GPP guard applies (the contest being won by chalk is structure evidence for refining the target, not grounds to retire).

## Applied

User approved the proposed codifications; changes applied 2026-07-12:

- **Proposal 1 — CODIFIED.** Inserted a new subsection **"### Finish-Capable Favorites Are Not Secondary Chalk (7/12/26 — 3-slate validated)"** into `rules/mma_se/framework.md`, immediately after the "### Secondary Plays Are Not Leverage" section, verbatim as proposed (bounded exemption + 3-slate evidence: 6/20 Oliveira, 6/27 Abus/Camilo, 7/12 Pinas/Gandra/Green). In `rules/mma_se/lessons.yaml`, set lesson `mma-se-2026-06-20-finish-capable-favorite-is-not-secondary-chalk` status `validated → codified` with `codified_in: "framework.md — Finish-Capable Favorites Are Not Secondary Chalk (7/12/26 — 3-slate validated)"`.
- **Proposal 2 — no action.** `fade-on-structure-not-narrative` held (not-yet-codify); left `validated`, unchanged.
- **Proposal 3 — no action.** No retirement candidates; no lesson retired.
