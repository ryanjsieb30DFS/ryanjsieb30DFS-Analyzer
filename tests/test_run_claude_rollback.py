"""_run_claude's rollback must cover the COLLATERAL files the prompt tells
claude to edit (lessons.yaml, framework.md, ...), not just out_path — a
timed-out review otherwise leaves half-edited ledgers behind. A collateral
YAML that no longer parses after a "successful" run must also restore
everything and fail the run."""

from src import analysis_runner as ar


class _FakeProc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _fake_run(mutations, returncode=0):
    """A subprocess.run stand-in that applies file mutations then exits."""
    def run(cmd, **kwargs):
        for path, content in mutations:
            path.write_text(content)
        return _FakeProc(returncode=returncode)
    return run


def _setup(monkeypatch, tmp_path):
    monkeypatch.setattr(ar, "_claude_binary", lambda: "/fake/claude")
    out = tmp_path / "review.md"
    lessons = tmp_path / "lessons.yaml"
    lessons.write_text("lessons: []\n")
    return out, lessons


def test_failed_run_restores_collateral_edits(monkeypatch, tmp_path):
    out, lessons = _setup(monkeypatch, tmp_path)
    monkeypatch.setattr(
        ar.subprocess, "run",
        _fake_run([(lessons, "lessons:\n  - id: partial-edit\n"),
                   (out, "half-written review")], returncode=1))
    res = ar._run_claude("prompt", out, collateral=[lessons])
    assert res["ok"] is False
    assert lessons.read_text() == "lessons: []\n"       # collateral restored
    assert not out.exists()                              # out_path rolled back


def test_broken_yaml_after_success_restores_everything_and_fails(monkeypatch, tmp_path):
    out, lessons = _setup(monkeypatch, tmp_path)
    monkeypatch.setattr(
        ar.subprocess, "run",
        _fake_run([(lessons, "lessons: [unclosed\n"),    # invalid YAML
                   (out, "review text")], returncode=0))
    res = ar._run_claude("prompt", out, collateral=[lessons])
    assert res["ok"] is False
    assert "lessons.yaml" in res["error"]
    assert lessons.read_text() == "lessons: []\n"
    assert not out.exists()


def test_successful_run_with_valid_yaml_keeps_edits(monkeypatch, tmp_path):
    out, lessons = _setup(monkeypatch, tmp_path)
    edited = "lessons:\n  - id: new-lesson\n    status: hypothesis\n"
    monkeypatch.setattr(
        ar.subprocess, "run",
        _fake_run([(lessons, edited), (out, "review text")], returncode=0))
    res = ar._run_claude("prompt", out, collateral=[lessons])
    assert res["ok"] is True
    assert lessons.read_text() == edited
    assert out.read_text() == "review text"


def test_collateral_created_by_failed_run_is_deleted(monkeypatch, tmp_path):
    monkeypatch.setattr(ar, "_claude_binary", lambda: "/fake/claude")
    out = tmp_path / "review.md"
    lessons = tmp_path / "lessons.yaml"   # does NOT exist pre-run
    monkeypatch.setattr(
        ar.subprocess, "run",
        _fake_run([(lessons, "lessons: []\n"), (out, "x")], returncode=1))
    res = ar._run_claude("prompt", out, collateral=[lessons])
    assert res["ok"] is False
    assert not lessons.exists()


# --- 9/19/26: model / turn / budget flags + one retry on timeout -----------

def test_cli_flags_pin_model_turns_and_budget(monkeypatch, tmp_path):
    out, lessons = _setup(monkeypatch, tmp_path)
    seen = {}

    def run(cmd, **kwargs):
        seen["cmd"] = cmd
        out.write_text("x")
        return _FakeProc(returncode=0)
    monkeypatch.setattr(ar.subprocess, "run", run)
    assert ar._run_claude("prompt", out)["ok"] is True
    cmd = seen["cmd"]
    assert cmd[cmd.index("--model") + 1] == ar.CLAUDE_MODEL
    assert cmd[cmd.index("--max-turns") + 1] == str(ar.CLAUDE_MAX_TURNS)
    assert cmd[cmd.index("--max-budget-usd") + 1] == "15"
    assert ar.CLAUDE_MODEL  # never empty


def test_timeout_retries_exactly_once_when_asked(monkeypatch, tmp_path):
    out, _ = _setup(monkeypatch, tmp_path)
    calls = {"n": 0}

    def run(cmd, **kwargs):
        calls["n"] += 1
        out.write_text("partial")
        raise ar.subprocess.TimeoutExpired(cmd="claude", timeout=1)
    monkeypatch.setattr(ar.subprocess, "run", run)
    res = ar._run_claude("prompt", out, retry_on_timeout=True)
    assert res["ok"] is False and "retried once" in res["error"]
    assert calls["n"] == 2
    assert not out.exists()          # partial write rolled back both times


def test_timeout_does_not_retry_by_default(monkeypatch, tmp_path):
    out, _ = _setup(monkeypatch, tmp_path)
    calls = {"n": 0}

    def run(cmd, **kwargs):
        calls["n"] += 1
        raise ar.subprocess.TimeoutExpired(cmd="claude", timeout=1)
    monkeypatch.setattr(ar.subprocess, "run", run)
    res = ar._run_claude("prompt", out)
    assert res["ok"] is False and calls["n"] == 1


def test_retry_succeeds_on_second_attempt(monkeypatch, tmp_path):
    out, _ = _setup(monkeypatch, tmp_path)
    calls = {"n": 0}

    def run(cmd, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise ar.subprocess.TimeoutExpired(cmd="claude", timeout=1)
        out.write_text("done")
        return _FakeProc(returncode=0)
    monkeypatch.setattr(ar.subprocess, "run", run)
    res = ar._run_claude("prompt", out, retry_on_timeout=True)
    assert res["ok"] is True and calls["n"] == 2 and out.read_text() == "done"


def test_post_check_errors_roll_everything_back(monkeypatch, tmp_path):
    out, lessons = _setup(monkeypatch, tmp_path)
    monkeypatch.setattr(
        ar.subprocess, "run",
        _fake_run([(lessons, "lessons:\n  - id: dup\n  - id: dup\n"), (out, "review")]))
    res = ar._run_claude("prompt", out, collateral=[lessons],
                         post_check=lambda: ["dup: duplicate id"])
    assert res["ok"] is False and "duplicate id" in res["error"]
    assert lessons.read_text() == "lessons: []\n" and not out.exists()
