# PROPOSED framework/philosophy edits from 2023-2026 mining — PGA Classic + RD4 SD

**APPLIED 2026-06-13: P1, P2, R1, R2 codified into framework.md (lessons flipped to
`codified`). HELD as open hypotheses: P3, R3** (confirm on future slates before codifying).

Per repo rule, codifying into framework.md / philosophy.md requires user approval. Each
item cites the seeded `lessons.yaml` entry and the mining report it rests on.

---

## PGA CLASSIC

### P1 — Quantify the winning-structure target (Section 3 Ownership Tier Framework / Section 5 The Leverage Spine)
Add a one-line empirical anchor: *"168-slate baseline (2023-2026): winning lineups
average ~13% PER-PLAYER ownership (~78% cumulative across 6) with 2-3 sub-10%-owned
golfers and are 91% unique. Target this shape; an all-chalk lineup is a structural
non-starter."*
Basis: `pga-classic-...-winning-structure-13own-2to3-darts` (validated). Note this only
makes an *existing* codified number (the 12.25/2.24 SE reference) explicit and large-sample.

### P2 — "The leverage play is mandatory" (Section 2 Slate Diagnostics, as a required output)
Add to the pre-build scan: *"Every slate has a sub-radar smash — 96% of 2023-2026 slates
had >=1 <20%-own golfer in >=30% of winners (median ~12% own). The scan must name the
candidate leverage tier; a build with zero sub-10% plays fails the structure check."*
Basis: `pga-classic-...-leverage-play-mandatory` (validated). Reinforces existing leverage-spine.

### P3 — Dart-count by course archetype (Section 5 / Section 9 checklists) — *hypothesis, lighter*
Add: *"Dose darts to course variance: tough courses ~3 sub-10% plays, birdie-fests ~2
(avg per-player ownership stays ~13% either way)."* Mark as a hypothesis to confirm on the next few
slates before hard-coding.
Basis: `pga-classic-...-dose-darts-to-course-variance` (hypothesis).

---

## PGA RD4 SD

### R1 — Replace the "Historical Winning Structure (ETR Database)" numbers with actual DK winners
The framework's `## Historical Winning Structure (ETR Database)` section currently uses
ETR-estimated averages. Replace/annotate with the 146-slate actual-DK baseline:
*"Winning lineups average ~19% PER-PLAYER ownership (~115% cumulative) with ~1.7 sub-10%
golfers (median), 85% unique; 93% of winners carry >=1 sub-10% play. Stable 2023-2026."*
Basis: `pga-rd4-sd-...-winning-structure-19own-1to2-darts` (validated).

### R2 — Add the cross-format leverage-gap rule (new short subsection)
*"RD4 SD is structurally chalkier than Classic: ~19% vs ~13% winning per-player own, ~1.7 vs ~2.5
darts. Do not import Classic's contrarian dosage. The single round + smaller field +
lower variance shrink the contrarian payoff — leverage is still required, in a smaller
dose."*
Basis: `pga-rd4-sd-...-format-leverage-gap-vs-classic` (validated). This is the single most
actionable new finding — it prevents over-fading on RD4 SD.

### R3 — ">=1 sub-10% still mandatory" + tough-course bump — *hypothesis, lighter*
Add to the pre-lock check: *"Even chalky RD4 SD winners carry >=1 sub-10% play (97% of
slates have a <20%-own slate-definer); tough courses reward ~1.9 vs ~1.6 on birdie-fests."*
Basis: `pga-rd4-sd-...-leverage-play-still-mandatory` (hypothesis).

---

## Courses (`rules/pga_classic/courses/`, shared by both slugs)
The mining dataset has per-tournament winning scores and structure; I can generate
date-stamped per-course observation stubs (winning-score band, birdie-fest vs tough
classification) for the recurring venues on request — not auto-created here.

## How to proceed
Tell me which of P1-P3 / R1-R3 to apply (e.g. "apply P1, P2, R1, R2; hold the hypotheses").
I'll edit the named framework.md/philosophy.md sections and flip the corresponding
lessons.yaml entries to `codified` with the `codified_in` pointer.
