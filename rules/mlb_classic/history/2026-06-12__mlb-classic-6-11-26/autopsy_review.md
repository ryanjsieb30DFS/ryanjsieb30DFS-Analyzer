# Post-autopsy review — MLB Classic 6.11.26 (logged 2026-06-12 14:09)

Contests: **$5K Chin Music** (SE, 1,189 entries) — L1 NYM-5 build, rank 52, **top 4.4%** (ledger best; prior best 39.9%) · **$5K Base Hit** (SE, 490) — L2 CHC-5+TEX-3 build, rank 141, top 28.8%.

## Process scorecard

| Check | Grade | Evidence |
|---|---|---|
| Pre-flight checklists honest | ✅ | Verified line by line: venue files exist as claimed (coors read + 4 stubs created pre-lock), all 7 open lessons genuinely applied-or-rejected with named mechanisms, anchor-equivalence run on all 3 flagged tiers, calibration small-sample guard observed (SIN at 2 slates, note-only) |
| Lessons applied vs ignored | ✅ | Best application yet: Scott kept per the condensation hypothesis (he condensed 43.9→56-63% exactly as predicted), pivot budget held (L1: one pivot, 14.0% avg own), Phillips faded per the leash clause (which backfired — but applying a validated lesson that then takes a contradiction is correct process, not a miss) |
| Entries tracked pre-lock | ✅ | **First time in three slates.** Both entries existed in lineups.md before lock — L1 app-built, L2 chat-built with thesis + audit addendum. The untracked-swap pattern is broken |
| Red team run | ❌ | **The one process miss.** No red_team.md — the build's own process line said "red-team it next, then enter as-is" and the step was skipped (build landed ~35 min pre-lock; the time pressure the late-build-bailout lesson describes). The swap didn't happen this time, but the portfolio went in unrefuted |
| Late-build window | ⚠️ | Analysis 11:54, build 12:35/12:40, lock 13:10 — tight again. Target remains 60-90 min so the red team fits |
| GPP guard observed | ✅ | No conclusions drawn from L2's mid-pack finish per se; only mechanism events ledgered |

**Percentile trend (best per slate):** 39.9% → 40.1% → **4.4%** — first top-5% finish, achieved by the audited, in-band build.

**Same-slate contrast worth naming:** L1 (in the winners' band: 13.99% avg own, 6 sub-10%, one structural pivot) beat L2 (above the band: 23.1% avg own, no structural pivot) by 29.6 points and 24 percentile points on identical slate information. That is the pivot-budget lesson run as a controlled experiment.

## Lesson ledger changes

- **pivot-budget-small-field-se** — 3rd mechanism confirmation (winners 15.4%/3.3 sub-10 and 18.5%/3.6 across the two contests; plus the L1-vs-L2 contrast). Band refined to "one pivot, ~3-5 sub-10% plays." → **proposed for codification** below.
- **salary-enabler-pitcher-chalk** — split evidence this slate: 3rd confirmation of the **enabler-keep** mechanism (fading $6,200 Phillips cut builds off from the winning salary structure; the Base Hit winner ran Phillips+Kelly to fund bats) AND 1st **contradiction of the leash clause** (Phillips's 2.4 avg IP was the exact fade-trigger profile; he threw past it for 22.85, the slate-defining arm — leash-as-fade-trigger now 1-1). → **proposed for codification with the leash clause narrowed**; a 2nd leash contradiction retires that clause.
- **untracked-entry-bypasses-loop** — 3rd confirmation, the positive case: loop honored, audited build delivered the ledger-best percentile. → **proposed for codification as a hard rule**.
- **se-chalk-pitcher-own-condensation** — `hypothesis` → **`validated`** (Scott 43.9→56.0-62.7%; second straight consensus-P1 condensation). Refinement logged: condensation concentrates ONLY on the consensus #1 — Phillips (cheap #2 chalk) closed *below* projection (21.9→14.6-17.6%).
- **weather-proof-dome-stack-pivot / blank-own-snapshot-artifact / late-build-bailout** — no status change; notes added (precondition correctly judged absent / no artifact recurred / default honored, no swap, but window tight and red team skipped).
- **Born:** `sin-projection-pool-omissions` (Carrigg $2,500 missing from the SIN projections CSV; scored 17.0 @ 3-4.5%, in the Chin Music winner — the snapshot is structurally blind to omitted players; cross-check the Stone's value list against the pool pre-lock) and `five-man-primary-conditional-on-blowup` (winners were 3-2-1-1-1 and 4-3-1; 5-man primaries in under half of top-20s when no offense blew up — the 5-man premium is conditional, stacking itself is not in question).

## Venue file changes

- **coors_field.md** — 3rd CHC@COL observation: cheap unowned-side one-off now **3-for-3** (Castro 6/9, Carrigg 6/10 and 6/11); the owned COL piece (Goodman, ~25% actual) busted at 0.0 — ownership, not park side, is the discriminator.
- **citi_field.md** — NYM heat paid top-of-order only (Soto 21/Young 19/Bichette 16 vs Semien 3/Benge 5); early lean: premium NYM bats over stack depth.
- **comerica_park.md** — game split by side: DET paid (Keith 28 @ 1-2%, Montero 23.25 = slate arm), MIN imploded (Matthews 1.5, Buxton 0.0).
- **kauffman_stadium.md** — rain game played; KC chalk busted on performance (Witt 3.0 @ ~31%), visiting TEX bats paid (Seager 19 in both winners).
- **loandepot_park.md** — Phillips 22.85 in the pitcher-leaning dome; bat sides quiet as priced.

## Proposed codifications

**APPROVED by the user in chat 2026-06-12 ("Just apply everything") — all four applied to framework.md the same day.**

1. **Pivot budget (small-field SE)** → framework.md, Lineup discipline: *"In SE fields up to ~1,200 entries, build chalk-plus-ONE-structural-pivot: ~15-18% average ownership, roughly 3-5 sub-10% plays, one leverage axis (stack OR pitcher — never both). Layered contrarianism out-leverages the field."* (3 mechanism confirmations: 6/9 origin, 6/10, 6/11.)
2. **Salary-enabler pitcher chalk** → framework.md, Pitcher selection: *"Cheap chalk arms whose salary unlocks the winning bat structure are enablers — keep them; fading them is a structural, not a leverage, decision. A short leash (low avg IP) is a risk note, not a fade trigger."* (Enabler-keep 3-for-3; leash clause demoted after the Phillips contradiction — it stays in the ledger and dies on a second contradiction.)
3. **Tracked-entry hard rule** → framework.md, Hard rules: *"Every lineup entered on DK must exist in data/lineups/<slug>.md before lock — Claude-built, handbuilt, or chat-built with a logged thesis. No untracked entries."* (3 slates of evidence, both directions.)

Also flagged (user's call): the Coors cheap-unowned-one-off mechanism is 3-for-3 but venue-specific — it can stay in parks/coors_field.md (pre-flight already forces the read) or be added to framework.md as a one-line pointer.
