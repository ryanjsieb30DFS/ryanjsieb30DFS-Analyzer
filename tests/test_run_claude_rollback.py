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
