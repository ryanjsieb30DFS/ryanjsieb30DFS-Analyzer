# Field Exploitation Plan — Large-Field Contests

**Created:** 2026-07-17 · **Reframed same day per Ryan:** construction happens in a third-party optimizer (SaberSim now, replacement later) — nothing Claude-built ever makes a lineup. This document is not about portfolio mechanics; it is about **how we exploit the field in contests**: where opponents are predictably wrong, how we get paid for each mistake, and what the Analyzer builds to make that systematic.

---

## The core idea

You do not beat a 10,000+ entry contest by projecting players better than the field — the field's ownership *is* the projection consensus. You beat it by knowing the specific, recurring mistakes the field makes and standing on the other side of them. This is already your infrastructure's strength: every autopsy logs crowded chalk, crowded pairs, fish traps (players loved by losers and faded by winners), dupe magnets, and named-shark behavior into `field_tendencies.jsonl` and the dossier files. The field's errors are **measured in your own data, per contest type** — not guessed from articles. The plan is to turn those measurements into a standing per-sport catalog of field errors and make every contest entry an explicit attack on that catalog.

---

# PART 1 — THE FIELD'S ERRORS AND HOW WE ATTACK EACH

## Error 1 — The field duplicates itself (the dupe tax)

Casual players mass-produce the same obvious lineup: consensus chalk, salary maxed, no differentiation. In a 35,000-entry field, that lineup exists dozens of times, and every copy splits the prize. Meanwhile winning lineups in your own mining data are 85–91% unique (168 PGA Classic slates, 146 RD4 SD slates).

**The attack:** never own a lineup whose expected duplicate count (ownership product × field size) is meaningfully above zero. Enough low-owned material in every entry that if it hits, the prize is yours alone. The Analyzer's dupe-magnet tracking (exact roster pairs the field piles into) tells you *which specific combos* to refuse — that's free money: skip the pair, keep the players.

## Error 2 — The field buys its ownership from the same projection sites

Ownership concentrates on consensus plays, so the price of a player (his ownership) is set by the same public numbers everyone reads. That means ownership is mispriced exactly where the public numbers are wrong. You have two detectors for this already: cross-vendor disagreement (≥15% spread between your vendors means the consensus is unstable) and ownership-vs-ceiling gaps (high ceiling, low projected own = the field is underpricing the tail).

**The attack:** every slate, the mispriced list *is* the leverage list. A player whose ownership badly lags his real win equity is uncontested; a player whose ownership exceeds his win equity is a fade even if he's "good." Leverage is earned, not forced — it only works when the field's number is structurally wrong AND the player's equity supports it (your own codified rule).

## Error 3 — The field is narrative-driven and recency-biased

The field over-owns whoever just did something visible (MMA: coming off a highlight KO; golf: last week's leaderboard; NASCAR: last race's winner) and under-owns whoever just failed publicly, without re-checking whether the underlying equity changed. Your MMA philosophy doc names this directly: recency bias, narrative chasing, cap-tier fixation are the three structural reasons field ownership is wrong.

**The attack:** buy the post-bad-result discount when the loss didn't change the player's true range (a KO loss can even *inflate* future finish equity — logged in your own philosophy). Fade the narrative premium when the story added ownership but not ceiling.

## Error 4 — The field treats substitutable anchors as one play (Anchor-Equivalence)

When two chalk-tier anchors sit at similar salary and similar equity, the field herds onto whichever one the touts named, leaving the twin at a fraction of the ownership. This is your 4-slate-validated rule, and it has cost real money every time it was ignored (Cadillac: named pick 20% own scored 43.85, ignored twin at 16% scored 64.4).

**The attack:** in a large field this stops being "one lineup runs the alternative" and becomes a sized bet: take real exposure to the underowned twin. Same win probability, fraction of the price, and if the twin hits you beat everyone who herded.

## Error 5 — The field ignores the tier where winning lineups are actually decided

Your same-slate shark head-to-head (45 slates) found the real gap between you and the sharks was not ownership discipline — it was that sharks kept mining a tier of cheap, low-owned scorers that both you and the field skipped: Noren / Pendrith / McNealy / Day in golf, Meerschaert / Volkov / Dariush in MMA, Van Gisbergen / Custer / Berry / Dillon in NASCAR, Garcia Jr. / Burger / Pivetta in MLB. The field fixates on the cap tier and the punt tier; the mid-value scorer tier goes unowned.

**The attack:** widen the consideration set in the value tier every slate — that is where slate-defining sub-10% plays live (players in ≥30% of winning lineups at <20% field ownership, which your autopsy already flags). This is the single most validated exploit in your data because the sharks demonstrate it against you weekly.

## Error 6 — The field builds structurally dead lineups

Chunks of the field burn their entries on constructions that cannot win regardless of outcomes: MMA opponent stacks (both sides of the same fight — one side's ceiling requires the other's floor; your own field model confirms casuals do this), NASCAR dominator stacking (laps led are zero-sum, two max-dominator bets in one lineup cap each other), golf builds that ignore wave/weather correlation on split-tee days.

**The attack:** structural correctness is free EV — a meaningful slice of any large field has effectively donated its entry fee before lock. You don't have to outplay those entries, only not be one of them. Every structurally-dead percent of the field makes the effective contest smaller than its listed size.

## Error 7 — The field overreacts to unconfirmed news

A rumor moves ownership 15%+ before anything is confirmed. Your late-news protocol already grades this: confirmed news = real reaction, reported-not-confirmed = partial, rumor = hold. The field does not grade — it stampedes.

**The attack:** when ownership swings on an unconfirmed report, the pre-news side of the swing is suddenly underowned at unchanged equity. Being deliberately slow on rumors is a leverage source, not a discipline cost.

## Error 8 — Fish traps: what losers love and winners avoid

Your `field_analysis.py` already computes the literal exploit list every autopsy: players heavily owned by the bottom of the standings and avoided by the top. These are usually "safe-looking" plays — high floor, visible narrative, no ceiling path (the MMA decision-grinder at 25% own is the archetype). Critically, your 3-slate MMA lesson cuts the other way too: a finish-capable favorite at mid ownership is NOT a trap — screen the piece, not the number.

**The attack:** the accumulated trap list is a standing fade screen, and the finish-path test is what separates real traps from legitimate mid-own cores.

---

## Where each sport's field bleeds most (attack priority per sport)

- **MMA:** the softest field. Opponent stacks (dead entries), KO-narrative chasing, favorites owned without finish paths. Attack: structural correctness + which-favorite selection + occasional live dog. The one warning from your data: the field being chalky is *correct* in MMA — don't fade chalk wholesale, pick the wrong-chalk.
- **PGA Classic:** field crowds the cap tier and tout-named plays; winners consistently carry 2–3 sub-10% golfers from the ignored value tier. Attack: Error 5 above, plus anchor-equivalence splits at the top.
- **PGA RD4 Showdown:** the field is closest to right here — winning structure is genuinely chalky (~19%/slot). The exploit is small and precise: 1–2 low-owned spots plus dupe avoidance. Over-contrarian play is donating; your mining data says don't import Classic dosage.
- **NASCAR:** the field (and historically you — 0% leverage rate vs sharks' 10–15%) ignores sub-5% sleepers entirely, and crowds dominator candidates whose points are zero-sum. Attack: sleeper coverage + dominator anchor-equivalence. Treat early NASCAR contests as paid calibration.

## Contest selection is itself field exploitation

The same lineup is worth more in a softer room:

- **Fish density scales down with stakes.** Micro-stakes ($0.25–$3) large-field GPPs carry the highest share of duplicated-chalk and structurally-dead entries. Start there — the errors in this catalog are most abundant there.
- **Effective field size < listed field size.** Every dupe cluster and dead structure shrinks the real competition. A 35K field where 20% of entries are duplicated chalk or opponent stacks is a much smaller contest than it looks — top-heavy payouts against a partially-dead field is the whole MME appeal.
- **Know which sharks are in the room.** Your per-pro dossier already profiles the named handles; large-field contests dilute them with fish, but they're firing 150 uniques each. The dossier tells you what they'll do (their envelope) — the catalog tells you what the fish will do. You're threading between the two: unowned by the fish, differentiated from the sharks.
- **Under ~2,500 entries plays like SE** (your validated finding) — that's the existing game, not this plan.

## The measurement loop — the actual moat

Every error above is only exploitable while it's *current*. Fields adapt slowly, but they adapt. Your edge is not any single item in the catalog — it's that your autopsy loop re-measures the catalog every contest: which chalk was crowded, which pairs duplicated, which traps caught the fish, whether the winners' structure moved. Nobody else in a $1 contest is running that loop. The tooling below exists to keep the catalog measured and to force every strategy to attack it explicitly.

---

# PART 2 — TOOLING (Analyzer only; optimizer is third-party)

**Division of labor, unchanged from the 7/17 decision:** a third-party optimizer builds (SaberSim now, replacement before the sub lapses ~Aug–Oct 2026); the Analyzer thinks, checks, and measures; nothing Claude-built creates lineups; the Sim repo stays shelved.

## Phase 0 — Play now, zero code

Next MMA card: micro-stakes large-field GPP, 20–50 entries, built in SaberSim with the existing `mma_mme` framework doc (Sim repo, `rules/mma_mme/` — it's a written solver guide). Run the normal Analyzer slate flow. Manually check the entries against the eight errors above — especially expected dupes ≈ 0 and no crowded-pair copies. Upload standings to autopsy as always; the field data is what Phase 2 feeds on.

## Phase 1 — Analyzer learns large fields (first code wave)

1. **Contest types:** add `20-Max` / `150-Max` as `MME_CONTEST_TYPES` in `src/contests.py`, fully separate from `FOCUS_CONTEST_TYPES`. SE/3/5-max baselines, grading calibration, and shark envelope stay sealed — your small-field game is working; large-field data never bleeds into it.
2. **Strategy prompt gains a `## Field attack plan` section** (only when a large-field contest is declared): for each catalog error with evidence on THIS slate, one line naming the field's mistake and one line naming the attack — mispriced-ownership list, anchor-equivalence twins with split sizing, the ignored value-tier scorers, trap-list players present, crowded pairs to refuse, news-swing reads. Still zero lineups; it's a target list, not a build.
3. **Grade tab portfolio mode** (upload the optimizer's export CSV, up to 150 rows) — exploitation checks, deterministic: expected dupes per lineup, trap-list exposure, crowded-pair copies, anchor-equivalence split actually taken, value-tier coverage, structural-dead checks (opponent stacks, dominator double-ups). Grades only, no fixes.

## Phase 2 — Make the catalog self-updating

1. **Field-error catalog file per sport** (`rules/<slug>/field_errors.md` or generated from `field_tendencies.jsonl`): each error with its current evidence counts (in-N-of-M contests), auto-fed into the slate bundle the same way field tendencies flow today. Errors that stop recurring age out — exploits decay when measured dead.
2. **Large-field shark + fish baselines:** `infer_type` currently discards standings rows above 5-max — stop discarding. Accumulate a separate large-field baseline (shark envelope AND fish profile: dupe rates, dead-structure share, trap ownership) from the CSVs you already upload. Within a few slates the fish-density and effective-field-size numbers stop being estimates.
3. **Autopsy panels for large fields:** how duplicated was the chalk actually, did the trap list catch losers again, which catalog errors paid this slate, effective-field-size estimate.

## Phase 3 — Replacement optimizer (before SaberSim lapses)

Evaluation, not code. Requirements: covers MMA/PGA/NASCAR on DK; accepts your vendor projections; per-player exposure caps across 150 lineups; can express "≥1 player under X% owned per lineup" (disqualifying if not); boost/dock soft weighting; MMA opponent exclusion; min-unique + 150-entry DK export. Migrate the `mma_mme` framework into the new solver's vocabulary, run one slate in both while the sub lives, confirm the export parses in the Grade portfolio mode.

## Guardrails

- Analyzer never builds a lineup; construction is third-party only.
- SE/3/5-max benchmarks stay sealed from large-field data — parallel files, never merged.
- No scraping — all field data comes from standings CSVs you upload.
- Winnings/ROI stay in the third-party tracker; percentile + process are the in-repo metrics.
- No commits without explicit instruction; this document is the only artifact.

## Open decisions (none block Phase 0)

1. First slate — MMA recommended, next card, micro-stakes, 20–50 entries.
2. Phase 1 green light — say the word.
3. Replacement-optimizer shortlist for Phase 3, while SaberSim still runs for a parallel test.
