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
_TIMEOUT_S = 600


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
        f"- Follow the sport's framework (e.g. RD4 SD is a flat 6-golfer lineup, no captain).\n\n"
        f"End with a 'Portfolio audit' section: player overlap, hedges, and rule-compliance check. "
        f"Write the result to `{out_path}`. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def lineup_target(slug: str) -> int:
    """How many unique lineups the declared contests call for (default 2)."""
    return portfolio_summary(slug).get("unique_lineups_needed") or 2
