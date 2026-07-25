"""
Back up the learning log (autopsy history under rules/) to GitHub.

The app calls `commit_and_push` after each Log Autopsy so the user's accumulated
slate knowledge is never laptop-only. All git surface lives here behind one
never-raises function: a backup failure must never break the autopsy flow.

The commit is pathspec-limited to the paths passed in, so it can't sweep up
unrelated half-edited code that happens to be staged in the working tree.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


class _Result:
    """Stand-in for a failed CompletedProcess when subprocess itself errors."""
    def __init__(self, detail: str):
        self.returncode = 1
        self.stdout = ""
        self.stderr = detail


def _run(args: list[str], cwd, timeout: int = 120):
    try:
        return subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True, timeout=timeout,
        )
    except Exception as exc:  # noqa: BLE001 — surface as a failed result, never raise
        return _Result(str(exc))


def commit_and_push(repo_root, paths: list[str], message: str, push: bool = True) -> dict:
    """Commit (and optionally push) only `paths` under `repo_root`.

    Returns {"status": ..., "detail": ...} where status is one of:
      - "ok"          committed and pushed
      - "commit_only" committed locally but not pushed (no remote / push failed / push=False)
      - "nothing"     no changes under `paths` to back up
      - "error"       not a git repo, or the commit itself failed
    Never raises."""
    root = Path(repo_root)

    if _run(["git", "rev-parse", "--is-inside-work-tree"], root).returncode != 0:
        return {"status": "error", "detail": "not a git repository"}

    added = _run(["git", "add", "--", *paths], root)
    if added.returncode != 0:
        # A failed add (stale index.lock, permissions) used to fall through to
        # the diff check and get misreported as "nothing to back up" — while new
        # autopsy data sat uncommitted. Report it as the error it is.
        return {"status": "error",
                "detail": "git add failed: "
                          + ((added.stderr or added.stdout).strip()[:300] or "unknown error")}

    # Nothing staged under these paths → nothing to back up.
    if _run(["git", "diff", "--cached", "--quiet", "--", *paths], root).returncode == 0:
        return {"status": "nothing", "detail": "no learning-log changes to back up"}

    # Pathspec-limited commit: only `paths` are committed even if other files
    # are staged elsewhere in the working tree.
    commit = _run(["git", "commit", "-m", message, "--", *paths], root)
    if commit.returncode != 0:
        return {"status": "error",
                "detail": (commit.stderr or commit.stdout).strip()[:300] or "git commit failed"}

    if not push:
        return {"status": "commit_only", "detail": "committed locally (push disabled)"}

    if not _run(["git", "remote"], root).stdout.strip():
        return {"status": "commit_only", "detail": "committed locally; no git remote configured"}

    pushed = _run(["git", "push"], root)
    if pushed.returncode != 0:
        return {"status": "commit_only",
                "detail": "committed locally; push failed: "
                          + ((pushed.stderr or pushed.stdout).strip()[:200] or "unknown error")}

    return {"status": "ok", "detail": "backed up to GitHub"}
