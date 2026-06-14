"""Run slate analysis + lineup builds in-app via headless Claude Code.

The Analyze tab's buttons call `run_analysis` and `run_build_lineups`, which
shell out to the `claude` CLI in headless print mode (`claude -p`), pointed at
this repo, to read the bundle + referenced files and write an output file
(data/slate_analysis/<slug>.md or data/lineups/<slug>.md) per the CLAUDE.md
workflow.

This uses the user's existing Claude Code subscription auth — no API key, no
separate billing. The `claude` binary is already installed on the machine.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from src.bundle import build_bundle
from src.contests import portfolio_summary

_REPO_ROOT = Path(__file__).parent.parent
_TIMEOUT_S = 1200  # big slates (MLB) can blow past 10 min of reading + building


def _claude_binary() -> str | None:
    """Resolve the claude CLI path; Streamlit's PATH may not include ~/.local/bin."""
    found = shutil.which("claude")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "claude"
    return str(fallback) if fallback.exists() else None


def _run_claude(prompt: str, out_path: Path) -> dict:
    """Run `claude -p` headlessly and confirm `out_path` was freshly written.

    Returns {ok, error, duration_s, cost_usd}.
    """
    started = time.time()

    binary = _claude_binary()
    if not binary:
        return {"ok": False, "error": "Couldn't find the `claude` CLI on this machine.",
                "duration_s": 0.0, "cost_usd": None}

    # Snapshot the prior file mtime so we can confirm a fresh write below.
    prior_mtime = out_path.stat().st_mtime if out_path.exists() else None

    cmd = [
        binary, "-p", prompt,
        "--output-format", "json",
        "--permission-mode", "acceptEdits",
        "--allowedTools", "Read,Glob,Grep,Write,Edit",
    ]

    try:
        proc = subprocess.run(
            cmd, cwd=str(_REPO_ROOT),
            capture_output=True, text=True, timeout=_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Timed out after {_TIMEOUT_S // 60} minutes.",
                "duration_s": time.time() - started, "cost_usd": None}

    duration = time.time() - started

    cost = None
    cli_error = None
    if proc.stdout.strip():
        try:
            data = json.loads(proc.stdout)
            cost = data.get("total_cost_usd")
            if data.get("is_error"):
                cli_error = data.get("result") or "Claude reported an error."
        except json.JSONDecodeError:
            pass

    if proc.returncode != 0 or cli_error:
        msg = cli_error or (proc.stderr.strip()[:500]) or f"claude exited with code {proc.returncode}."
        return {"ok": False, "error": msg, "duration_s": duration, "cost_usd": cost}

    # Confirm a fresh output file actually landed.
    if not out_path.exists() or out_path.stat().st_mtime == prior_mtime:
        return {"ok": False,
                "error": "Claude ran but didn't write the output file. Check the inputs and try again.",
                "duration_s": duration, "cost_usd": cost}

    return {"ok": True, "error": None, "duration_s": duration, "cost_usd": cost}


def run_analysis(slug: str, contest_label: str, sport: str) -> dict:
    """Build the bundle and run headless Claude to write the slate analysis."""
    out_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    bundle_path = build_bundle(slug, contest_label, sport)
    prompt = (
        f"Write the {contest_label} slate analysis. "
        f"Read the bundle at `{bundle_path}` and every file it references "
        f"(projections, the article PDFs and images, strategy docs, and any sim data). "
        f"Then write a concise, scannable, GPP-framed slate analysis to `{out_path}`, "
        f"following the 'Writing the slate analysis' workflow in CLAUDE.md for sport `{sport}`. "
        f"The analysis is for a HAND-BUILDER: every call must answer who to play and, if played, "
        f"how the rest of the roster shapes around them. After the checklist it MUST contain, in "
        f"order, the sections defined in CLAUDE.md's 'Slate analysis format (handbuild-first)': "
        f"'## Slate at a glance', '## The N decisions that define this slate' (PLAY/PASS/MIX with "
        f"'If played →' salary/pairing consequences and 'If faded →' the world that bet needs, "
        f"Anchor-Equivalence as one of the decisions), the tiered '## Player board' (PLAY/MIX/PASS, "
        f"every row with an 'If played →' shaping note), '## Where I disagree with the vendors' "
        f"(never omitted — disagree whenever the mechanism supports it, weighted by "
        f"`rules/{slug}/vendor_calibration.jsonl`), and '## Edges to exploit' (each edge with its "
        f"concrete lineup expression). "
        f"MANDATORY: complete the 'Pre-flight ritual' in CLAUDE.md first — confirm the data is for "
        f"the CURRENT slate, read the venue file for this slate's venue (create a stub marked "
        f"UNVERIFIED if missing), read `rules/{slug}/lessons.yaml` (every open lesson applied or "
        f"rejected with the mechanism reason), and run the framework pre-lock checks including "
        f"Anchor-Equivalence. The output file MUST begin with the '## Pre-flight checklist' block "
        f"defined in CLAUDE.md, every line filled in with specifics. "
        f"Do not ask any questions — read the inputs and produce the file."
    )
    return _run_claude(prompt, out_path)


def run_build_lineups(slug: str, contest_label: str, sport: str, n_target: int) -> dict:
    """Build the lineup portfolio from the slate analysis via headless Claude.

    Requires the slate analysis to exist first. Builds up to n_target lineups,
    each with a distinct thesis; stops early if the slate supports fewer.
    """
    analysis_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    if not analysis_path.exists():
        return {"ok": False, "error": "Generate the slate analysis first — lineups are built from it.",
                "duration_s": 0.0, "cost_usd": None}

    out_path = _REPO_ROOT / "data" / "lineups" / f"{slug}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path = build_bundle(slug, contest_label, sport)

    prompt = (
        f"Build the {contest_label} lineup portfolio. "
        f"Read the slate analysis at `{analysis_path}`, the bundle at `{bundle_path}` and the files "
        f"it references (projections, articles), and `rules/{slug}/framework.md` + `rules/{slug}/autopsies.md` "
        f"for the sport's lineup-construction rules.\n\n"
        f"Build UP TO {n_target} lineup(s). Each lineup must have:\n"
        f"- A one-sentence thesis ('how it wins').\n"
        f"- A roster as a markdown table (player, salary, key metric, role).\n"
        f"- Total salary verified <= $50,000 — show the addition.\n"
        f"- A 'What if?' line stating which distinct scenario it answers.\n\n"
        f"Discipline (enforce strictly):\n"
        f"- Lineups MUST answer DIFFERENT questions — no near-duplicates, no shared full conviction core "
        f"(for MMA SE, differ on at least one conviction anchor, not just the leverage piece).\n"
        f"- Apply the Anchor-Equivalence pre-lock check: if 2+ chalk-tier anchors sit at similar ownership, "
        f"at least one lineup MUST run the alternative.\n"
        f"- If the slate supports FEWER than {n_target} genuinely distinct theses, build fewer and explain why — "
        f"DO NOT pad with filler lineups.\n"
        f"- Follow the sport's framework (e.g. RD4 SD is a flat 6-golfer lineup, no captain).\n"
        f"- Complete the 'Pre-flight ritual' in CLAUDE.md: re-read `rules/{slug}/lessons.yaml` and "
        f"the venue file. The output MUST begin with the '## Pre-flight checklist' block, and each "
        f"applied open lesson must be named in the lineup thesis it influenced (or explicitly "
        f"rejected with the mechanism reason).\n\n"
        f"End with a 'Portfolio audit' section: player overlap, hedges, and rule-compliance check. "
        f"Write the result to `{out_path}`. "
        f"IMPORTANT: if `{out_path}` already exists with lineups in it (e.g. handbuilt ones), "
        f"PRESERVE them exactly as written — append your new lineups after them, continue their "
        f"numbering, count them toward the {n_target}-lineup target, and make sure your new "
        f"lineups answer DIFFERENT questions than the existing ones (include them in the "
        f"Portfolio audit). Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_select_lineups(slug: str, contest_label: str, sport: str, n_target: int) -> dict:
    """Select the best lineups from the uploaded lineup pool(s) via headless Claude.

    Unlike run_build_lineups (which invents rosters), this picks up to n_target
    lineups FROM the lineup-pool CSV(s) the user uploaded in the Sim Data tab — a
    SaberSim export or any traditional optimizer's files (proj-/ceiling-/50-50-
    optimized, possibly several, with or without sim metrics) — judged against the
    slate analysis. Requires BOTH the slate analysis and at least one pool file to
    exist. Writes the chosen lineups to data/lineups/<slug>.md in the same portfolio
    format run_build_lineups uses; never edits other data files.
    """
    analysis_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    if not analysis_path.exists():
        return {"ok": False, "error": "Generate the slate analysis first — selections are judged against it.",
                "duration_s": 0.0, "cost_usd": None}

    from src.sim_data import load_sim_files
    from src.lineups import roster_spec

    sim_files = load_sim_files(slug)
    if not sim_files:
        return {"ok": False,
                "error": "Upload at least one lineup-pool CSV in the Sim Data tab first.",
                "duration_s": 0.0, "cost_usd": None}
    slots = roster_spec(slug)["slots"]
    pool_paths = "\n".join(
        f"  - `{s['path']}` ({s['n_rows']:,} rows · {'has sims' if s.get('has_sim_cols') else 'rosters only'})"
        for s in sim_files
    )

    out_path = _REPO_ROOT / "data" / "lineups" / f"{slug}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path = build_bundle(slug, contest_label, sport)

    prompt = (
        f"SELECT the {contest_label} lineup portfolio from the user's uploaded lineup pool(s) — "
        f"do NOT invent rosters. Read the slate analysis at `{analysis_path}`, the bundle at "
        f"`{bundle_path}` and the files it references (projections, articles), "
        f"`rules/{slug}/framework.md` + `rules/{slug}/autopsies.md` for the sport's "
        f"lineup-construction rules, and EVERY uploaded lineup-pool CSV below (paths also in the "
        f"bundle's '## Sim data' section):\n{pool_paths}\n\n"
        f"How to read each pool CSV: each ROW is one candidate lineup. Its first "
        f"{len(slots)} columns are DK player IDs in slot order ({', '.join(slots)}). The REMAINING "
        f"columns VARY by file and may include sim metrics (Proj Score, percentile ceilings, "
        f"Ownership, Salary, Saber Score, per-contest ROI/Win Rate/Cash Rate/Sim Dupes) OR may be "
        f"absent entirely (a traditional optimizer's rosters-only export) — use those metrics only "
        f"if present, and NEVER require them. Resolve each DK ID to a player using the projections "
        f"pool's `dk_id` column (in the bundle's Projections source) so you know the names, salaries, "
        f"ownership, teams, and slate-analysis calls behind every row.\n\n"
        f"If MULTIPLE files are present they are likely different optimizer settings "
        f"(projection-/ceiling-/50-50-weighted) — COMBINE all candidates into one pool and DEDUPE "
        f"identical rosters (same 10 player IDs = one candidate, regardless of which file it came "
        f"from). Cross-file diversity is a feature: a ceiling-optimized file is where the GPP tail "
        f"lives.\n\n"
        f"SELECT UP TO {n_target} lineup(s) from the combined pool. Selection discipline (enforce strictly):\n"
        f"- FILTER to lineups that EXPRESS the slate analysis's edges and '## Player board' calls — "
        f"NOT the rows with the highest sim ROI/Saber Score (when sims even exist). Sim rank is NOT a "
        f"quality filter: per this repo's rules a high-ROI sim row that fights the slate's edges is a "
        f"worse pick than a mid-pack row that nails them. With NO sim columns, rank purely on edge-fit, "
        f"then ceiling/projection/ownership. Judge each row on how it WINS a GPP, never on cashing.\n"
        f"- The chosen lineups MUST answer DIFFERENT questions — distinct theses, no near-duplicates "
        f"and no shared full conviction core.\n"
        f"- Apply the Anchor-Equivalence pre-lock check: if 2+ chalk-tier anchors sit at similar "
        f"ownership, at least one selected lineup MUST run the alternative.\n"
        f"- Never roster a hitter against your own pitcher (MLB) — reject any such row even if a sim "
        f"ranks it highly; honor every hard rule in the sport's framework (e.g. RD4 SD is flat 6, no "
        f"captain).\n"
        f"- If the pool offers FEWER than {n_target} genuinely distinct, edge-expressing lineups, "
        f"select fewer and explain why — DO NOT pad with near-duplicates.\n\n"
        f"For EACH selected lineup write, in the SAME format run_build_lineups uses:\n"
        f"- A one-sentence thesis ('how it wins').\n"
        f"- A roster as a markdown table (player, salary, key metric, role).\n"
        f"- Total salary verified <= $50,000 — show the addition.\n"
        f"- A 'What if?' line stating which distinct scenario it answers.\n"
        f"- Tag the lineup heading as selected from the uploaded pool and note its source FILE name "
        f"+ ROW INDEX (1-based, counting data rows after the header) for traceability.\n\n"
        f"Complete the 'Pre-flight ritual' in CLAUDE.md: re-read `rules/{slug}/lessons.yaml` and the "
        f"venue file. The output MUST begin with the '## Pre-flight checklist' block, and each applied "
        f"open lesson must be named in the lineup thesis it influenced (or explicitly rejected with the "
        f"mechanism reason).\n\n"
        f"End with a 'Portfolio audit' section: player overlap, hedges, Anchor-Equivalence "
        f"compliance, and which slate-analysis edges each selection expresses. Write the result to "
        f"`{out_path}`. "
        f"IMPORTANT: if `{out_path}` already exists with lineups in it (e.g. handbuilt ones), "
        f"PRESERVE them exactly as written — append your selected lineups after them, continue their "
        f"numbering, count them toward the {n_target}-lineup target, and make sure your selections "
        f"answer DIFFERENT questions than the existing ones (include them in the Portfolio audit).\n\n"
        f"HARD RULE: write ONLY `{out_path}` — never edit the slate analysis, the bundle, the pool "
        f"file(s), or any other data file. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_fix_lineups(slug: str, contest_label: str, sport: str) -> dict:
    """Propose pool-sourced replacements for the red-team-flagged lineups.

    Reads the red-team review (data/red_team/<slug>.md) + the current portfolio
    (data/lineups/<slug>.md), and for each lineup the red team marked FIX or KILL
    RE-SELECTS a replacement FROM the uploaded lineup pool(s) — never building
    from scratch. SHIP lineups are left untouched. Writes PROPOSALS only, to
    data/lineup_fixes/<slug>.md; the portfolio is changed later by
    run_apply_lineup_fixes. Requires the red-team review, the portfolio, and at
    least one pool file to exist.
    """
    lineups_path = _REPO_ROOT / "data" / "lineups" / f"{slug}.md"
    red_team_path = _REPO_ROOT / "data" / "red_team" / f"{slug}.md"
    analysis_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    if not lineups_path.exists():
        return {"ok": False, "error": "No lineups to fix — build/select a portfolio first.",
                "duration_s": 0.0, "cost_usd": None}
    if not red_team_path.exists():
        return {"ok": False, "error": "Run the Red Team first — there are no verdicts to act on.",
                "duration_s": 0.0, "cost_usd": None}

    from src.sim_data import load_sim_files
    from src.lineups import roster_spec, flagged_lineups

    flagged = flagged_lineups(slug)
    if not flagged:
        return {"ok": False, "error": "Every lineup is a SHIP — nothing flagged to fix.",
                "duration_s": 0.0, "cost_usd": None}
    sim_files = load_sim_files(slug)
    if not sim_files:
        return {"ok": False,
                "error": "Fixes are re-selected from your pool — upload a lineup-pool CSV in the Sim Data tab first.",
                "duration_s": 0.0, "cost_usd": None}
    slots = roster_spec(slug)["slots"]
    pool_paths = "\n".join(
        f"  - `{s['path']}` ({s['n_rows']:,} rows · {'has sims' if s.get('has_sim_cols') else 'rosters only'})"
        for s in sim_files
    )
    flagged_list = "; ".join(flagged)

    out_path = _REPO_ROOT / "data" / "lineup_fixes" / f"{slug}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path = build_bundle(slug, contest_label, sport)

    prompt = (
        f"PROPOSE fixes for the {contest_label} lineup portfolio that the Red Team flagged. "
        f"Read the red-team review at `{red_team_path}`, the current portfolio at `{lineups_path}`, "
        f"the slate analysis at `{analysis_path}`, the bundle at `{bundle_path}` and the files it "
        f"references (projections, articles), `rules/{slug}/framework.md` + `rules/{slug}/autopsies.md`, "
        f"and EVERY uploaded lineup-pool CSV below (paths also in the bundle's '## Sim data' section):\n"
        f"{pool_paths}\n\n"
        f"The red-team '## Verdict summary' marks each lineup SHIP / FIX / KILL. The lineups flagged "
        f"FIX or KILL are: {flagged_list}. **Leave every SHIP lineup alone.** For EACH flagged lineup, "
        f"propose ONE replacement RE-SELECTED FROM THE POOL — do NOT invent rosters.\n\n"
        f"How to read each pool CSV: each ROW is one candidate lineup; its first {len(slots)} columns "
        f"are DK player IDs in slot order ({', '.join(slots)}); remaining columns are optional sim "
        f"metrics (use only if present, never required). Resolve each DK ID to a player via the "
        f"projections pool's `dk_id` column (in the bundle's Projections source). COMBINE all pool "
        f"files and DEDUPE identical rosters.\n\n"
        f"Each proposed replacement (selection discipline — enforce strictly):\n"
        f"- Must be a REAL pool row — tag its source FILE name + 1-based ROW INDEX.\n"
        f"- May EITHER resolve the red team's specific objection while still answering that lineup's "
        f"original 'What if?' question, OR be a totally new, distinct lineup that answers a question "
        f"the portfolio doesn't already cover — your call per lineup; state which you chose.\n"
        f"- Must EXPRESS the slate analysis's edges / '## Player board' calls, NOT the highest sim "
        f"ROI/Saber Score row (sim rank is NOT a quality filter on this repo's rules).\n"
        f"- Total salary <= $50,000 (show the addition); <= 3 driver overlap with any KEPT (SHIP) "
        f"lineup AND with any other replacement (no near-duplicates, no shared full conviction core).\n"
        f"- Honor every framework hard rule + the Anchor-Equivalence pre-lock check across the FULL "
        f"resulting portfolio (kept SHIP lineups + replacements).\n\n"
        f"Write a proposals document to `{out_path}` with:\n"
        f"- A short intro: which lineups were flagged and why (quote each one's verdict + the "
        f"'FIX (one change)' instruction from the red team).\n"
        f"- A '## Fix proposals' section: one subsection per flagged lineup — restate the original "
        f"(label + flaw), then the PROPOSED replacement as a roster markdown table (player, salary, "
        f"key metric, role), a one-sentence thesis, a 'What if?' line, a 'Resolves:' line naming how it "
        f"answers the red team finding, and a 'Mode:' line ('same question' or 'new question').\n"
        f"- A '## Kept (SHIP)' list naming the SHIP lineups that carry over unchanged.\n"
        f"- A '## Portfolio after fixes' note: post-swap player overlap + Anchor-Equivalence compliance "
        f"across the full set.\n\n"
        f"HARD RULE: write ONLY `{out_path}` — do NOT edit the portfolio `{lineups_path}`, the red-team "
        f"file, the slate analysis, the bundle, or the pool files. Applying the fixes is a separate "
        f"step. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_apply_lineup_fixes(slug: str, contest_label: str, sport: str) -> dict:
    """Apply the proposed fixes: rewrite the portfolio keeping SHIP lineups
    verbatim and swapping in each proposed replacement. Requires both the
    proposals doc and the portfolio to exist. Writes ONLY data/lineups/<slug>.md.
    """
    lineups_path = _REPO_ROOT / "data" / "lineups" / f"{slug}.md"
    fixes_path = _REPO_ROOT / "data" / "lineup_fixes" / f"{slug}.md"
    if not fixes_path.exists():
        return {"ok": False, "error": "No fix proposals yet — run 'Fix flagged lineups' first.",
                "duration_s": 0.0, "cost_usd": None}
    if not lineups_path.exists():
        return {"ok": False, "error": "No portfolio file to apply fixes to.",
                "duration_s": 0.0, "cost_usd": None}

    prompt = (
        f"APPLY the proposed lineup fixes to the {contest_label} portfolio. Read the current portfolio "
        f"at `{lineups_path}` and the fix proposals at `{fixes_path}`. Produce the FINAL portfolio:\n"
        f"- Keep every SHIP lineup EXACTLY as written in `{lineups_path}` (verbatim — same drivers, "
        f"thesis, salary line, 'What if?').\n"
        f"- Replace each red-team-flagged (FIX/KILL) lineup with its PROPOSED replacement from "
        f"`{fixes_path}` (same roster, thesis, 'What if?', salary check, and the source FILE + ROW "
        f"INDEX tag); add a short note on the heading or below it that it was re-selected to fix the "
        f"red-team finding.\n"
        f"- Renumber the lineups L1..LN in order, keep the existing '## Pre-flight checklist' block at "
        f"the top, and REWRITE the '## Portfolio audit' to reflect the new set (exposure counts, "
        f"Anchor-Equivalence compliance, max pairwise overlap, and a line naming which lineups were "
        f"fixed and how).\n"
        f"- Verify every final lineup is <= $50,000 with the right number of players and that no two "
        f"lineups share more than 3 players.\n\n"
        f"HARD RULE: write ONLY `{lineups_path}` — do NOT edit the proposals file, the red-team file, "
        f"or any other data file. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, lineups_path)


def run_rank_lineups(slug: str, contest_label: str, sport: str,
                     lineups: list[dict]) -> dict:
    """Rank the user's candidate lineups head-to-head via headless Claude.

    Snapshots the resolved lineups to data/lineup_ranking/<slug>_input.json,
    then Claude writes a comparative ranking (best->worst with reasoning,
    per-lineup construction notes, cross-set findings, and a teaching
    paragraph) to data/lineup_ranking/<slug>.md. This is a construction coach:
    it ranks and explains, it NEVER edits the portfolio.
    """
    out_dir = _REPO_ROOT / "data" / "lineup_ranking"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"
    snap_path = out_dir / f"{slug}_input.json"
    theses_path = out_dir / f"{slug}_theses.json"
    snap_path.write_text(json.dumps({"lineups": lineups}, indent=2, default=str))
    labels = [ln.get("label") for ln in lineups]

    bundle_path = build_bundle(slug, contest_label, sport)
    analysis_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    slate_ctx = (
        f"the slate analysis at `{analysis_path}`, " if analysis_path.exists()
        else "(no slate analysis exists yet — judge from the bundle and strategy docs alone) "
    )

    prompt = (
        f"Rank the user's CANDIDATE {contest_label} lineups in `{snap_path}` (a list of "
        f"slot-assigned player rows + GPP totals per lineup). These are lineups the user built "
        f"themselves and is deciding between — your job is to rank them and TEACH the "
        f"construction reasoning, not to rewrite them. Read {slate_ctx}the bundle at "
        f"`{bundle_path}` and its referenced projections, `rules/{slug}/framework.md`, "
        f"`rules/{slug}/lessons.yaml`, and `rules/shared/anchor_equivalence.md`. If "
        f"`rules/{slug}/vendor_calibration.jsonl` exists, use it to weight vendor ownership "
        f"numbers.\n\n"
        f"GPP framing — judge every lineup on how it WINS a tournament, never on cashing. "
        f"Compare the candidates HEAD-TO-HEAD against the slate's edges. Write the result to "
        f"`{out_path}` with these sections, in order:\n\n"
        f"## Ranking\n"
        f"A table best->worst: rank, the lineup label, and a one-line reason. Ties are fine if "
        f"two genuinely answer different questions equally well — say so.\n\n"
        f"## Per-lineup construction notes\n"
        f"For each candidate: salary efficiency (where the money went and whether it bought "
        f"ceiling), correlation/shape (stacks, tee-time/wave, same-game), ownership/leverage "
        f"profile against vendor-projected own (name the numbers), and the one-sentence thesis "
        f"it is implicitly playing. Name which slate-analysis '## Player board' calls and "
        f"slate-defining decisions each lineup follows or violates — a violated PASS/MIX is a "
        f"point to argue with evidence, not an automatic demotion.\n\n"
        f"## Cross-set findings\n"
        f"Near-duplicate / redundant builds (same question answered twice), shared blind spots "
        f"across the whole set, and the Anchor-Equivalence read across the candidates.\n\n"
        f"## Construction principles\n"
        f"A short, plain teaching paragraph: the transferable lesson from this comparison the "
        f"user can apply to future builds.\n\n"
        f"THEN also write the file `{theses_path}` as JSON mapping EACH input lineup's label to "
        f"the thesis and 'what if?' it plays — so the user can save any of these to their "
        f"portfolio carrying a real thesis (never a vague label). Use exactly these labels: "
        f"{labels}. Format:\n"
        f'{{"Lineup 1": {{"thesis": "<one sentence: how it wins>", "what_if": "<the distinct '
        f'question it answers>"}}, ...}}\n'
        f"Write a thesis for every label, even the lower-ranked ones.\n\n"
        f"HARD RULE: write ONLY `{out_path}` and `{theses_path}` — never edit "
        f"`data/lineups/{slug}.md` or anything else; these are candidates, not submissions. "
        f"Do not ask any questions — produce the files."
    )
    return _run_claude(prompt, out_path)


def run_handbuild_analysis(slug: str, contest_label: str, sport: str,
                           players: list[dict], totals: dict) -> dict:
    """Analyze the user's handbuilt lineup via headless Claude.

    Snapshots the picked lineup to data/handbuild_analysis/<slug>_lineup.json,
    then Claude writes the analysis (verdict + thesis + 'What if?' + findings)
    to data/handbuild_analysis/<slug>.md. The Handbuild save flow attaches the
    parsed thesis/'What if?' to the lineup — the user never types them.
    """
    out_dir = _REPO_ROOT / "data" / "handbuild_analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"
    snap_path = out_dir / f"{slug}_lineup.json"
    snap_path.write_text(json.dumps({"players": players, "totals": totals},
                                    indent=2, default=str))

    bundle_path = build_bundle(slug, contest_label, sport)
    analysis_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    lineups_path = _REPO_ROOT / "data" / "lineups" / f"{slug}.md"
    slate_ctx = (
        f"the slate analysis at `{analysis_path}`, " if analysis_path.exists()
        else "(no slate analysis exists yet — judge from the bundle and strategy docs alone) "
    )
    portfolio_ctx = (
        f"Also read the existing portfolio at `{lineups_path}` and check whether this handbuild "
        f"competes with (answers the same question as) a lineup already in it. "
        if lineups_path.exists() else "There are no other lineups on this slate yet. "
    )

    prompt = (
        f"Analyze the user's HANDBUILT {contest_label} lineup in `{snap_path}` (canonical player "
        f"rows + GPP totals). Read {slate_ctx}the bundle at `{bundle_path}` and its referenced "
        f"projections, `rules/{slug}/philosophy.md`, `rules/{slug}/framework.md`, "
        f"`rules/{slug}/lessons.yaml`, and `rules/shared/anchor_equivalence.md`. If "
        f"`rules/{slug}/vendor_calibration.jsonl` exists, use it to weight vendor ownership "
        f"numbers. {portfolio_ctx}\n\n"
        f"GPP framing — judge the lineup on how it WINS a tournament, never on cashing:\n"
        f"1. STEELMAN: the strongest case for this build — derive the thesis the user is "
        f"implicitly playing.\n"
        f"2. ATTACK: failure modes, leverage audit against the vendor-projected ownership "
        f"(name the numbers), correlation/structure issues, framework rules or open lessons.yaml "
        f"lessons it violates, and the Anchor-Equivalence implications. If a slate analysis "
        f"exists, cross-reference its '## Player board' and slate-defining decisions: name which "
        f"calls this lineup follows and which it violates — a violated PASS/MIX call is a finding "
        f"to argue with evidence, not an automatic KILL; the board can be wrong.\n"
        f"3. VERDICT: SHIP (play as-is), FIX (the ONE specific change), or KILL (the fatal flaw).\n\n"
        f"Write the result to `{out_path}` in EXACTLY this structure — the app parses the Thesis "
        f"and 'What if?' lines verbatim, so keep their format:\n\n"
        f"## Verdict\n"
        f"SHIP|FIX|KILL — one-line reason\n\n"
        f"**Thesis:** <one sentence: how this lineup wins — write the best honest thesis even if "
        f"the verdict is FIX or KILL>\n\n"
        f"**What if?** — <the distinct question this lineup answers>\n\n"
        f"## Analysis\n"
        f"<concise and scannable: steelman, attacks, leverage math, lesson/framework checks>\n\n"
        f"HARD RULE: write ONLY `{out_path}` — never edit the lineups file or anything else; the "
        f"user decides whether to save. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_red_team(slug: str, contest_label: str, sport: str) -> dict:
    """Adversarial pre-lock review of the built lineups — findings only,
    written to data/red_team/<slug>.md. Never rewrites the lineups."""
    lineups_path = _REPO_ROOT / "data" / "lineups" / f"{slug}.md"
    if not lineups_path.exists():
        return {"ok": False, "error": "Build lineups first — the red team attacks them.",
                "duration_s": 0.0, "cost_usd": None}

    analysis_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    out_path = _REPO_ROOT / "data" / "red_team" / f"{slug}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path = build_bundle(slug, contest_label, sport)

    prompt = (
        f"Red-team the {contest_label} lineup portfolio at `{lineups_path}`. You are an ADVERSARY "
        f"whose job is to kill these lineups before lock, per the 'Red Team review' section of "
        f"CLAUDE.md. Read the slate analysis at `{analysis_path}`, the bundle at `{bundle_path}` and "
        f"its referenced projections, `rules/{slug}/philosophy.md`, `rules/{slug}/framework.md`, "
        f"`rules/{slug}/lessons.yaml`, and `rules/shared/anchor_equivalence.md`. If "
        f"`rules/{slug}/vendor_calibration.jsonl` exists, use it to judge how much to trust each "
        f"vendor's ownership numbers.\n\n"
        f"For EACH lineup:\n"
        f"1. REFUTE THE THESIS: state what must ALL be true for this lineup to win the GPP, then "
        f"attack each condition with evidence from the inputs. Steelman it first, then break it.\n"
        f"2. LEVERAGE AUDIT: recompute the math — is the 'contrarian' piece actually contrarian at "
        f"the vendor-projected ownership? Name the number. A 15%-owned 'leverage play' is chalk "
        f"wearing a costume.\n"
        f"3. SHARED FAILURE MODES: what single game-state kills this lineup AND another one in the "
        f"portfolio?\n\n"
        f"Then PORTFOLIO-LEVEL findings: competing lineups answering the same question, chalk-tier "
        f"Anchor-Equivalence violations (2+ similar-own anchors with no lineup on the alternative), "
        f"duplication risk with the field (obvious cores everyone builds), and open lessons.yaml "
        f"lessons the build ignored.\n\n"
        f"Then AUDIT THE PRE-FLIGHT CHECKLIST in `{lineups_path}` skeptically: for each checked "
        f"line, verify it was actually done (e.g. does the named venue file exist and say what's "
        f"claimed?). Flag rubber-stamps.\n\n"
        f"VERDICT per lineup: SHIP (survives attack), FIX (name the ONE specific change), or KILL "
        f"(name the fatal flaw). Be willing to say SHIP — manufactured objections are as useless as "
        f"rubber stamps.\n\n"
        f"HARD RULE: do NOT edit `{lineups_path}` or any other file — write ONLY the findings to "
        f"`{out_path}` with sections: '## Verdict summary' (table: lineup / verdict / one-line "
        f"reason), '## Lineup attacks' (one subsection each), '## Portfolio-level findings', "
        f"'## Pre-flight audit'. The user decides what to act on. "
        f"Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_autopsy_review(slug: str, contest_label: str, sport: str) -> dict:
    """Post-autopsy learning run: grade the archived slate's process, update
    the lesson ledger + venue file, and write proposed (not applied)
    framework changes to <history_dir>/autopsy_review.md."""
    from src.history import latest_history_dir

    hist_dir = latest_history_dir(slug)
    if hist_dir is None:
        return {"ok": False, "error": "No archived slate found — log an autopsy first.",
                "duration_s": 0.0, "cost_usd": None}

    out_path = hist_dir / "autopsy_review.md"
    prompt = (
        f"Run the post-autopsy review for the archived {contest_label} slate at `{hist_dir}`. "
        f"Read its manifest.json, slate_analysis.md, lineups.md, autopsy.json, and results.json "
        f"(plus red_team.md if present), the latest entries in `rules/{slug}/autopsy_data.jsonl`, "
        f"and the lesson ledger at "
        f"`rules/{slug}/lessons.yaml` (create it with the standard header from CLAUDE.md's "
        f"'Lesson ledger' section if missing). Then, following the 'Post-autopsy ritual' in CLAUDE.md:\n"
        f"1. GRADE THE PROCESS: was the pre-flight checklist present and honest in slate_analysis.md "
        f"and lineups.md? Which open lessons were applied vs ignored, and did ignored ones cost anything? "
        f"If red_team.md exists: for each FIX/KILL verdict, was it heeded before lock, and was the red "
        f"team right in hindsight? A heeded FIX that saved points or an ignored KILL that cost a lineup "
        f"is ledger-worthy evidence; an overruled verdict that was wrong is evidence against "
        f"over-trusting the red team.\n"
        f"2. UPDATE `rules/{slug}/lessons.yaml` directly (Edit tool): add confirmations/contradictions "
        f"with this slate's date and history dir; promote status to 'validated' where confirmations "
        f"exist; add new 'hypothesis' lessons born from this autopsy — mechanism-based, not "
        f"result-based.\n"
        f"3. UPDATE THE VENUE FILE for this slate's venue (sport `{sport}`; see CLAUDE.md for the "
        f"venue dir; create the file from the archived analysis if missing): append a date-stamped "
        f"'Per-slate observation' line with what this slate proved or disproved about the venue.\n"
        f"4. WRITE `{out_path}` with sections: '## Process scorecard', '## Lesson ledger changes', "
        f"'## Venue file changes', and '## Proposed codifications' — for any lesson meeting the "
        f"promotion criteria (3 confirming slates) write the exact framework.md/philosophy.md edit "
        f"you propose; for retirement candidates (2 mechanism contradictions) the same. If nothing "
        f"qualifies, write 'None this slate.' under that heading. "
        f"Do NOT edit framework.md or philosophy.md in this run — proposals only; the user approves.\n"
        f"GPP guard: a bad ROI or a lost contest is NEVER a contradiction by itself; only mechanism "
        f"failures count. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_apply_proposals(slug: str) -> dict:
    """Apply the user-approved '## Proposed codifications' from the latest
    autopsy review to framework.md/philosophy.md + the lesson ledger."""
    from src.history import latest_history_dir

    hist_dir = latest_history_dir(slug)
    review_path = hist_dir / "autopsy_review.md" if hist_dir else None
    if review_path is None or not review_path.exists():
        return {"ok": False, "error": "No autopsy review found — run the review first.",
                "duration_s": 0.0, "cost_usd": None}

    prompt = (
        f"Read `{review_path}`, section '## Proposed codifications'. The user has APPROVED these "
        f"proposals. Apply each proposed edit to `rules/{slug}/framework.md` / "
        f"`rules/{slug}/philosophy.md` exactly as written, then update `rules/{slug}/lessons.yaml`: "
        f"set the affected lessons' status to 'codified' (with codified_in naming the doc + section) "
        f"or 'retired' (with retired_reason). Finally append a line "
        f"'## Applied' with the current changes summarized to the end of `{review_path}`. "
        f"Do not ask any questions."
    )
    return _run_claude(prompt, review_path)


def lineup_target(slug: str) -> int:
    """How many unique lineups the declared contests call for (default 2)."""
    return portfolio_summary(slug).get("unique_lineups_needed") or 2
