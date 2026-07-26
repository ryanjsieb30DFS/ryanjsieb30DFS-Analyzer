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


def _bare_remote(tmp_path, work):
    """A real bare repo as `origin`, with an upstream set — so the push path is
    actually exercised instead of short-circuiting on 'no remote'."""
    bare = tmp_path / "remote.git"
    _git(["init", "-q", "--bare", str(bare)], tmp_path)
    _git(["remote", "add", "origin", str(bare)], work)
    _git(["push", "-q", "-u", "origin", "HEAD"], work)
    return bare


def test_push_publishes_every_unpushed_commit_not_just_the_backup(tmp_path):
    """The reason pushing is never automatic: `git push` takes no refspec, so it
    publishes UNRELATED local commits too. This test pins that behavior so the
    UI keeps warning about it — 'Log autopsy' must not be consent to publish
    whatever else is sitting on the branch."""
    from src.git_backup import push_only, unpushed_summary
    work = tmp_path / "work"
    work.mkdir()
    _init_repo(work)
    _bare_remote(tmp_path, work)

    # An unrelated local WIP commit the user has deliberately NOT pushed.
    (work / "secret_wip.py").write_text("# half-finished\n")
    _git(["add", "-A"], work)
    _git(["commit", "-q", "-m", "WIP do not publish"], work)
    # Then a learning-log backup commit.
    (work / "rules").mkdir()
    (work / "rules" / "autopsy_data.jsonl").write_text('{"slate": 1}\n')
    res = commit_and_push(work, ["rules"], "backup", push=False)
    assert res["status"] == "commit_only"

    ahead = unpushed_summary(work)
    assert ahead["n"] == 2, ahead
    assert any("WIP" in s for s in ahead["subjects"])

    pushed = push_only(work)
    assert pushed["status"] == "ok", pushed
    # Both commits are now on the remote — the WIP one rode along.
    remote_log = _git(["log", "--oneline", "HEAD"], tmp_path / "remote.git").stdout
    assert "WIP do not publish" in remote_log
    assert unpushed_summary(work)["n"] == 0


def test_push_only_reports_nothing_when_up_to_date(tmp_path):
    from src.git_backup import push_only
    work = tmp_path / "work"
    work.mkdir()
    _init_repo(work)
    _bare_remote(tmp_path, work)
    res = push_only(work)
    assert res["status"] == "nothing"


def test_push_only_errors_without_remote_or_repo(tmp_path):
    from src.git_backup import push_only
    work = tmp_path / "work"
    work.mkdir()
    _init_repo(work)
    assert push_only(work)["status"] == "error"          # no remote
    plain = tmp_path / "notarepo"
    plain.mkdir()
    assert push_only(plain)["status"] == "error"         # not a git repo


def test_unpushed_summary_handles_no_upstream(tmp_path):
    """No upstream configured must degrade to n=-1 with an explanation, not crash
    or claim zero (which would tell the user a push is a no-op)."""
    from src.git_backup import unpushed_summary
    work = tmp_path / "work"
    work.mkdir()
    _init_repo(work)
    rep = unpushed_summary(work)
    assert rep["n"] == -1 and "upstream" in rep["detail"]
    assert rep["has_remote"] is False
    assert unpushed_summary(tmp_path / "nope")["n"] == -1
