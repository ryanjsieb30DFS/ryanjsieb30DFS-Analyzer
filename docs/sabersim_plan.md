# SaberSim Ultimate ↔ Analyzer — integration plan

**Created 2026-07-18.** We hold the SaberSim **Ultimate** tier ($297/mo — the top plan). This document maps everything Ultimate produces to a specific place in the Analyzer's loop, in phases. The standing division of labor does not change: **SaberSim builds, the Analyzer thinks.** The Analyzer never constructs a lineup, and nothing is ever scraped — every SaberSim number enters this tool as a CSV export or a screenshot the user uploads.

---

## What Ultimate actually gives us (researched 7/18, cross-checked with our own captured reference at the Sim repo's `docs/sabersim_reference.md`)

1. **Projections + sim-driven optimizer for all four of our sports** (MLB, Golf, MMA, NASCAR are all supported), with lineup groups, a diversity slider, and fast late swap.
2. **A rich projections CSV export.** The golf schema we captured on 7/4 carries: My Proj, My Own, Adj Own, Salary, Win %, Top 5/10/20 %, Make Cut %, Tee Time, per-round outcome counts (eagles/birdies/pars/bogeys), and **full percentile projections (25th / 50th / 75th / 85th / 95th / 99th)**. The MLB export additionally ships a **real stddev** (`DK Std`) and the DK player id — that signature is already live in `src/vendors.py` ("SaberSim MLB Projections").
3. **Contest Sims (Ultimate-only).** Before lock, every built lineup is run through thousands of simulated contests against **realistic opponent fields bucketed by stakes** (under \$4 / \$4–30 / \$30–100 / \$100+, across 13 contest types) with exact payout ladders. Per-lineup outputs: **expected ROI, median ROI, max/min ROI, win rate, cash rate, ROI volatility, and expected duplicate count.**
4. **Contest Flashback (Ultimate-only).** After any DK contest completes, Flashback re-simulates the REAL entered field 100,000 times. Three views: **Mine** (your lineups: Sim ROI, Sim median profit, Sim 99th-percentile profit, average dupes), **Users** (every opponent ranked by Sim ROI, filterable by entry count), and **Leaderboard** (actual results). Clicking any user opens their lineups, exposures, and salary allocation. This is "skill vs variance," quantified, per contest — including for the specific sharks we already track by handle.
5. **No export for Contest Sims or Flashback** (CSV export exists only for projections and lineups/entries). Those numbers enter the Analyzer as **screenshots into Slate Data / the autopsy** — the loader already reads images, and this respects the no-scraping rule.

---

## The five integration tracks

### Track 1 — SaberSim projections as a first-class vendor (pre-slate)
The MLB signature exists; golf, MMA, and NASCAR do not. Add one vendor signature per sport to `src/vendors.py` from a real export each (user downloads them; sample files land in ~/Downloads like the other vendors).
- Map `My Own` → ownership, `My Proj` → proj_points, the DK id, and stddev where shipped.
- **Ceiling decision:** map a high percentile to the canonical `ceiling` column — 95th percentile matches the existing MLB signature's choice (`dk_95_percentile` → ceiling). This single mapping **unlocks the entire ceiling suite (leverage candidates, ownership-vs-ceiling mispricing, boom/bust) for NASCAR and MMA** — the two sports whose current vendors ship no ceiling.
- SaberSim's ownership becomes another voice in cross-vendor disagreement (a ≥15% spread between vendors is leverage signal) and, once the calibration loop has data, a graded vendor like the others.

### Track 2 — Grade the SaberSim builds (pre-lock)
Today the Grade tab takes pasted player names, one lineup per line. SaberSim's lineup/entries export is a CSV. Add a small upload box to the Grade tab that accepts that export (and DK's own entries format) and converts rows into the same lineup list the paste path produces. Same grader, same thesis check, zero new judgment logic. This is also exactly the "portfolio CSV mode" the MME plan's Phase 1 called for — one feature serves both the 1–5-bullet slates and the future 20–150-entry MME track.

### Track 3 — Contest Sim numbers as DATA, never the decider (pre-lock)
The per-lineup contest-sim panel (ROI, win rate, expected dupes) gets screenshotted into Slate Data when the user wants the strategy or the Grade thesis check to see it. Two standing cautions stay codified: **sim rank is not gospel** (build for the tail, not the expected case) and our own MMA benchmark showed SaberSim's cash-optimized scores overlap real GPP winners poorly. The one number worth systematically capturing is **expected dupes** — it directly feeds the dupe-tax thinking the Grade tab and the MME error catalog already do.

### Track 4 — Contest Flashback into the autopsy loop (post-slate) — the biggest new edge
- **(a) Skill-vs-variance, quantified.** After logging a contest, the user screenshots the **Mine** tab (Sim ROI / median / 99th per entered lineup) into the autopsy. The post-autopsy review gets ground truth for its GPP guard: a lineup that lost money but sims +ROI over 100k replays is GOOD process (and the reverse — a cash that sims deeply negative — is a warning wearing a win). This turns "a lost contest is never evidence by itself" from a principle into a measurement.
- **(b) Shark validation.** The **Users** tab ranks every opponent by Sim ROI. Cross-reference our tracked handles: are the pros in `shark_handles.yaml` actually +EV in the re-sims, or just running hot? Screenshot the top of the Users tab + any tracked pro's drill-down (their exposures and construction) into the autopsy; the per-pro dossier's "pattern" line gets real substance.
- **(c) Field errors for the MME track.** Flashback's dupes data and the gap between the Leaderboard (actual) and Users-by-Sim-ROI (deserved) views is a direct read on which field mistakes paid and which got lucky — feeding the 8-error catalog in `docs/mme_plan.md`.

### Track 5 — Strategy decisions this resolves
- The **MME plan's Phase 3** ("evaluate/choose a replacement optimizer") is answered while Ultimate is active: **SaberSim stays the construction engine for both the SE/3/5-max slates and the MME track.** The Sim repo's `rules/mma_mme/` playbook (cumulative-ownership band, sub-16% leverage rule, etc.) is solver configuration for SaberSim's builder, as planned.
- The **SaberSim sunset is on hold** — the archive checklist and calibration baseline in the Sim repo remain valuable but are no longer urgent.
- **Sim Savant is out of scope** (user decision 7/18/26): SaberSim Ultimate is the single sim/optimizer stack. No Sim Savant vendor signature, no integration work.

---

## Phased rollout

**Phase 0 — capture, no code (next slate).** Export one projections CSV per sport from SaberSim; screenshot the Contest Sim panel after a build and all three Flashback tabs after the contest. This confirms the real column headers and what the screenshots legibly carry before anything is built.

**Phase 1 — vendor signatures (small, immediate after Phase 0).** Add golf/MMA/NASCAR SaberSim signatures + tests (mirroring the MLB one), with the percentile→ceiling mapping. Ships the NASCAR/MMA ceiling unlock.

**Phase 2 — Grade tab CSV upload.** Accept the SaberSim/DK entries CSV alongside the paste box; parse to the existing lineup structure. (Also satisfies MME plan Phase 1's portfolio-CSV requirement.)

**Phase 3 — Flashback in the autopsy ritual.** Add an optional "Flashback" step to the autopsy flow: screenshots (Mine / Users tabs) uploaded with the standings; the post-autopsy review prompt gains a step — when Flashback data is present, grade process-vs-variance with it and cross-check tracked sharks' Sim ROI. Optionally record the per-lineup Sim ROI numbers in the autopsy notes so they land in `autopsy_data.jsonl`.

**Phase 4 — SaberSim calibration ledger (data-gated, later).** Once several slates carry both contest-sim expectations and actual results, grade SaberSim itself the way we grade vendors: does its pre-lock ROI ranking predict our actual finishes? Does its dupes estimate match the dupes the autopsy counts? Only build this once ~5+ slates have the paired data.

---

## Open decisions (user)

1. Ceiling mapping: 95th percentile (matches MLB signature) or 85th (more conservative)? Default = 95th unless told otherwise.
2. Green-light order: Phase 0 is free and immediate; Phases 1–2 are small code; Phase 3 touches the autopsy ritual.
