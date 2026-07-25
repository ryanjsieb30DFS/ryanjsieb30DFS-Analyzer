"""Tests for the learning-log git backup helper (src/git_backup.py)."""
import subprocess

from src.git_backup import commit_and_push


def _git(args, cwd):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def _init_repo(path):
    _git(["init", "-q"], path)
    _git(["config", "user.name", "Test"], path)
    _git(["config", "user.email", "test@example.com"], path)
    # An initial commit so HEAD exists.
    (path / "README.md").write_text("init\n")
    _git(["add", "-A"], path)
    _git(["commit", "-q", "-m", "init"], path)


def _commit_count(path):
    out = _git(["rev-list", "--count", "HEAD"], path)
    return int(out.stdout.strip())


def test_commit_only_when_no_remote(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "autopsy_data.jsonl").write_text('{"slate": 1}\n')

    before = _commit_count(tmp_path)
    res = commit_and_push(tmp_path, ["rules"], "backup", push=True)
    # No remote configured → committed locally, not pushed.
    assert res["status"] == "commit_only"
    assert _commit_count(tmp_path) == before + 1


def test_nothing_to_back_up(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "a.jsonl").write_text("x\n")
    commit_and_push(tmp_path, ["rules"], "first", push=False)

    # Second call with no further changes → nothing.
    res = commit_and_push(tmp_path, ["rules"], "second", push=False)
    assert res["status"] == "nothing"


def test_error_when_not_a_repo(tmp_path):
    res = commit_and_push(tmp_path, ["rules"], "backup", push=False)
    assert res["status"] == "error"


def test_push_disabled_returns_commit_only(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "a.jsonl").write_text("x\n")
    res = commit_and_push(tmp_path, ["rules"], "backup", push=False)
    assert res["status"] == "commit_only"


def test_commit_is_pathspec_limited(tmp_path):
    """A staged unrelated file must NOT ride along in the rules-scoped commit."""
    _init_repo(tmp_path)
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "a.jsonl").write_text("lesson\n")
    # Stage an unrelated code change.
    (tmp_path / "code.py").write_text("print('wip')\n")
    _git(["add", "code.py"], tmp_path)

    res = commit_and_push(tmp_path, ["rules"], "backup rules only", push=False)
    assert res["status"] == "commit_only"

    # The new commit should touch only rules/, not code.py.
    files = _git(["show", "--name-only", "--pretty=format:", "HEAD"], tmp_path).stdout.split()
    assert "rules/a.jsonl" in files
    assert "code.py" not in files
    # code.py remains staged but uncommitted.
    assert _git(["diff", "--cached", "--name-only"], tmp_path).stdout.strip() == "code.py"


def test_failed_git_add_reports_error_not_nothing(monkeypatch, tmp_path):
    """A failed `git add` (stale index.lock, permissions) must surface as an
    error — it used to fall through the diff check and get misreported as
    'no learning-log changes to back up' while data sat uncommitted."""
    import src.git_backup as gb

    real_run = gb._run

    def fake_run(args, cwd, timeout=120):
        if args[:2] == ["git", "add"]:
            return gb._Result("fatal: Unable to create index.lock: File exists")
        return real_run(args, cwd, timeout)

    # A real repo so the rev-parse pre-check passes.
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    monkeypatch.setattr(gb, "_run", fake_run)
    out = gb.commit_and_push(tmp_path, ["rules"], "msg", push=False)
    assert out["status"] == "error"
    assert "index.lock" in out["detail"]
