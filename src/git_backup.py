"""
Back up the learning log (autopsy history under rules/) to GitHub.

The app calls `commit_and_push(..., push=False)` after each Log Autopsy so the
user's accumulated slate knowledge is never laptop-only, then offers an EXPLICIT
button for the push. All git surface lives here behind never-raises functions: a
backup failure must never break the autopsy flow.

The commit is pathspec-limited to the paths passed in, so it can't sweep up
unrelated half-edited code that happens to be staged in the working tree.

**`git push` cannot be scoped the same way.** It takes no refspec here, so it
publishes every unpushed commit on the branch — not just the backup commit. That
is why pushing is never automatic: logging an autopsy is consent to log an
autopsy, not to publish whatever else is sitting on main. `unpushed_summary`
lets the UI say exactly what a push would send before the user asks for it.
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


def push_only(repo_root) -> dict:
    """Push the current branch, committing nothing. Never raises.

    The log flow already commits, so the backup button needs a PUSH, not another
    commit-and-push — `commit_and_push` returns "nothing" and never reaches the
    push when there's nothing new under the pathspec, which is the normal case
    right after logging.

    Returns {"status": "ok"|"nothing"|"error", "detail": str}."""
    root = Path(repo_root)
    if _run(["git", "rev-parse", "--is-inside-work-tree"], root).returncode != 0:
        return {"status": "error", "detail": "not a git repository"}
    if not _run(["git", "remote"], root).stdout.strip():
        return {"status": "error", "detail": "no git remote configured"}
    ahead = unpushed_summary(root)
    if ahead["n"] == 0:
        return {"status": "nothing", "detail": "already up to date with the remote"}
    pushed = _run(["git", "push"], root)
    if pushed.returncode != 0:
        return {"status": "error",
                "detail": "push failed: "
                          + ((pushed.stderr or pushed.stdout).strip()[:200]
                             or "unknown error")}
    n = ahead["n"]
    return {"status": "ok",
            "detail": (f"pushed {n} commit(s) to the remote" if n > 0
                       else "pushed to the remote")}


def unpushed_summary(repo_root) -> dict:
    """What a `git push` from here would actually publish. Never raises.

    Returns {"n": int, "subjects": [str], "branch": str|None, "has_remote": bool,
    "detail": str}. `n` is -1 when the ahead-count can't be determined (no
    upstream configured, not a repo). The point is that the user sees the real
    blast radius — the backup commit plus any other local commits — before
    consenting, since the push itself can't be narrowed to one commit."""
    root = Path(repo_root)
    out = {"n": -1, "subjects": [], "branch": None, "has_remote": False,
           "detail": ""}
    if _run(["git", "rev-parse", "--is-inside-work-tree"], root).returncode != 0:
        out["detail"] = "not a git repository"
        return out
    out["has_remote"] = bool(_run(["git", "remote"], root).stdout.strip())
    br = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    if br.returncode == 0:
        out["branch"] = br.stdout.strip() or None
    log = _run(["git", "log", "--oneline", "@{u}..HEAD"], root)
    if log.returncode != 0:
        out["detail"] = "no upstream branch configured for this branch"
        return out
    subjects = [ln.strip() for ln in log.stdout.splitlines() if ln.strip()]
    out["n"] = len(subjects)
    out["subjects"] = subjects
    out["detail"] = ("nothing to push" if not subjects
                     else f"{len(subjects)} unpushed commit(s)")
    return out
