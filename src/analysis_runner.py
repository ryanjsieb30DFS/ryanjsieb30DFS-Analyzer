"""Run the slate analysis in-app via headless Claude Code.

The Analyze tab's "Generate slate analysis" button calls `run_analysis`, which:
1. Builds the consolidated bundle (data/bundle/<slug>.md) via src.bundle.
2. Shells out to the `claude` CLI in headless print mode (`claude -p`), pointed
   at this repo, telling it to read the bundle + referenced files and write the
   analysis to data/slate_analysis/<slug>.md per the CLAUDE.md workflow.
3. Confirms the output file was written and reports status + cost.

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

_REPO_ROOT = Path(__file__).parent.parent
_TIMEOUT_S = 600


def _claude_binary() -> str | None:
    """Resolve the claude CLI path; Streamlit's PATH may not include ~/.local/bin."""
    found = shutil.which("claude")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "claude"
    return str(fallback) if fallback.exists() else None


def _prompt(slug: str, contest_label: str, sport: str, bundle_path: Path, out_path: Path) -> str:
    return (
        f"Write the {contest_label} slate analysis. "
        f"Read the bundle at `{bundle_path}` and every file it references "
        f"(projections, the article PDFs and images, strategy docs, and any sim data). "
        f"Then write a concise, scannable, GPP-framed slate analysis to `{out_path}`, "
        f"following the 'Writing the slate analysis' workflow in CLAUDE.md for sport `{sport}`. "
        f"Do not ask any questions — read the inputs and produce the file."
    )


def run_analysis(slug: str, contest_label: str, sport: str) -> dict:
    """Build the bundle and run headless Claude to write the slate analysis.

    Returns {ok, error, duration_s, cost_usd}.
    """
    out_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    started = time.time()

    binary = _claude_binary()
    if not binary:
        return {"ok": False, "error": "Couldn't find the `claude` CLI on this machine.",
                "duration_s": 0.0, "cost_usd": None}

    # Snapshot the prior file mtime so we can confirm a fresh write below.
    prior_mtime = out_path.stat().st_mtime if out_path.exists() else None

    bundle_path = build_bundle(slug, contest_label, sport)

    cmd = [
        binary, "-p", _prompt(slug, contest_label, sport, bundle_path, out_path),
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

    # Confirm a fresh analysis file actually landed.
    if not out_path.exists() or out_path.stat().st_mtime == prior_mtime:
        return {"ok": False,
                "error": "Claude ran but didn't write the analysis file. Check the inputs and try again.",
                "duration_s": duration, "cost_usd": cost}

    return {"ok": True, "error": None, "duration_s": duration, "cost_usd": cost}
