# Post-autopsy review — UFC Fight Night, Baku (6/27/26)

Contests: 490-entry SE (free), **$5K Clinch SE — 1,189** (the live $5 bullet), 594-entry SE (3 entries, free). Best finish: **rank 8 / 1.3%ile** (594 field). Autopsy is standings-only — no projections existed at lock for the autopsy panels.

## Process scorecard

**Pre-flight checklist — present and honest. ✅**
All six ritual items checked with specifics: slate confirmed (bundle 2026-06-27 10:46, article dates 6/26, current not stale); 4 of 4 slate-data files read with nothing unparsed; venue correctly noted as N/A for MMA by design; open lessons reviewed with applied/rejected calls each carrying a mechanism reason; framework pre-lock incl. Anchor-Equivalence run; results.jsonl scanned; sharp envelope noted. The lesson triage was genuinely honest — it **rejected all four `showdown-*` lessons** with the correct mechanism reason (this is classic 6-fighter, not captain-mode) rather than pretending to apply them. No checklist inflation.

**Lessons applied vs ignored.**
- `anchor-equivalence-fifth-validation` → Decision 1 (Yakhyaev vs Donchenko/Aliskerov). **Applied, and it won** — see ledger.
- `asymmetric-anchor-equivalence-weighting` → checked, correctly did NOT fire (Yakhyaev has a G&P/sub/decision floor, not KO-or-bust). Correct boundary call.
- `binary-leverage-weak-in-small-fields` → Decision 5 field-split (Camilo floor in the 490, Walker dog in the 1,189). Small-field half hit; large-field half misfired (see new lesson). **Applied.**
- `finish-capable-favorite-is-not-secondary-chalk` → Decisions 2 & 3 (Abus/Olek banger + Reyes/Camilo cores exempt from chalk-trim). **Applied, confirmed.**
- `fade-on-structure-not-narrative` → Shara structural fade (Decision 4), Torres/Ferreira explicitly NOT narrative-faded. **Applied, confirmed.**
- `field-size-calibration` / `one-leverage-swing-conviction-core` / `no-identical-conviction-cores` / `ceiling-threshold-discipline` / `confirmed-vs-speculative-news` → all applied. No open lesson was silently ignored.

**Did the Top plays / PLAY-PASS-MIX decisions hold up?**
- **Main event read — the standout win.** The strategy preferred the **lower-owned Fiziev over chalk Torres** and faded the combined main-event pile. Fiziev WON and anchored nearly every top lineup in all three contests. The user's single best build (594 L3, rank 8) carried Fiziev; **every Torres entry he ran underperformed** (490 rank 442 / 90.2%ile, 1,189 rank 141 / 11.9%ile, 594 L1 rank 583 / 98.1%ile). The strategy was right on the slate's pivotal fight; partial adherence (running Torres in 3 builds) is what capped the result.
- **Decision 1 Anchor-Equivalence — won.** Donchenko (the cheaper alternative) anchored the **1,189-field winner** (Leeleebee 671.42) and recurred through every top board; Yakhyaev also cleared. Running the alternative captured the uncontested win.
- **Decision 2 banger — hit (one side).** Abus Magomedov hit 105.08 and was a slate-definer; the strategy correctly flagged the fight as a must-play and called both sides live. Variance landed on Abus, not the user's chosen Olek — within the "either side" framing.
- **Decision 3 finish-capable cores — hit.** Camilo (101.69) and the finish-capable framing held.
- **Decision 4 Shara structural fade — neutral-to-correct.** Not a slate-definer.
- **The miss — coverage.** The single slate-defining play, **Kaan Ofli (112.76 at 5.7–9.4% own, in 45–70% of all top lineups)**, was never mentioned anywhere in the strategy, alongside Abdullayev (~9% own) and Ruziboev (16.6%). The strategy's chosen sub-10% leverage horse was a KO-or-bust dog (Walker, busted), not the low-owned finisher who actually decided the slate. This is the headline lesson below.

**Net.** Strong process slate: honest checklist, every lesson applied or rejected with a reason, and the two highest-leverage calls (Fiziev-over-Torres, Donchenko anchor-equivalence) were vindicated by the field winners. The user's best contest (1.3%ile) came from the differentiated Fiziev/Camilo/Hasanov build the strategy pointed at. The recurring structural gap is leverage **screening** — the build hunts the sub-10% slot among article-named dogs and misses low-owned finishers below the spotlight.

## Lesson ledger changes

- `mma-se-2026-05-30-anchor-equivalence-fifth-validation` (codified) — **+1 confirmation (2026-06-27), now 7th cross-format validation.** Donchenko-not-Yakhyaev anchored the 1,189-field winner; running the cheaper equivalent captured the win without sacrificing the chalk side.
- `mma-se-2026-06-20-finish-capable-favorite-is-not-secondary-chalk` (hypothesis → **validated**) — +1 confirmation. Abus (17%, 105.08) and Camilo (18–20%, 101.69) were mid-owned finish-capable favorites in clean spots, both slate-definers; trimming either as "secondary chalk" would have cut two of the slate's cheap definers.
- `mma-se-2026-06-20-fade-on-structure-not-narrative` (hypothesis → **validated**) — +1 directional confirmation. Every fade this slate was structural (Shara ceiling-cap, main-event over-concentration), all held; the structural Fiziev-over-Torres read won. The narrative-punishment half of the mechanism still awaits a test (no narrative fade was made).
- `mma-se-2026-05-16-binary-leverage-weak-in-small-fields` (codified) — **+1 confirmation (small-field-floor half).** Camilo floor hit in the 490; the large-field binary-dog half (Walker) misfired and feeds the new lesson below — a refinement, not a contradiction.
- **NEW hypothesis** `mma-se-2026-06-27-leverage-is-the-low-own-finisher-not-the-named-dog` — in finish-heavy MMA the slate-defining sub-10% piece is a low-owned converting finisher (Ofli/Abdullayev/Ruziboev), not the article-named KO-or-bust dog. Rule to test: screen the FULL rosterable pool under ~10% own for a real finish path before locking the leverage slot.
- **NEW hypothesis** `mma-se-2026-06-27-finish-heavy-small-fields-still-won-by-differentiation` — on >=70%-finish boards even ~500-entry fields are won by ~16–18% avg-own differentiated builds (all three Baku winners), while the user's 43%-own chalk build finished 90.2%ile. Caveat the "small field → lean chalk" calibration for finish-heavy slates.

No retirements. No contradictions logged — the Walker misfire is a refinement of where to find large-field leverage, not a mechanism failure, and the GPP guard holds (a lost contest is never a contradiction by itself).

## Venue file changes

**None — MMA carries no venue file by design** (CLAUDE.md: venue files exist only for NASCAR tracks / PGA courses / MLB parks; matchup-specific reads come from the articles). The slate strategy's pre-flight correctly recorded this. No stub created.

## Proposed codifications

**None this slate.** The two lessons that gained confirmations both moved hypothesis → validated but neither has reached the 3-confirming-slate promotion bar:
- `finish-capable-favorite-is-not-secondary-chalk`: origin 6/20 + 1 confirmation (6/27) = 2 of 3.
- `fade-on-structure-not-narrative`: origin 6/20 + 1 confirmation (6/27) = 2 of 3.

`anchor-equivalence-fifth-validation` and `binary-leverage-weak-in-small-fields` are already codified. No lesson has 2 mechanism contradictions, so no retirement proposals. Re-evaluate codification next MMA slate if either validated lesson confirms a third time.
