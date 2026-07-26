"""The log flow appends autopsy_data.jsonl (the dedup authority) per contest,
then archives the slate. If the archive raises, the appends must be reversible —
otherwise logged_contest_ids treats every re-log as a duplicate and the contest
can never reach results.jsonl. truncate_to is that reversal."""

import json

from src import history


def _write_rows(path, rows):
    with path.open("a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_truncate_to_restores_pre_log_state(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "_REPO_ROOT", tmp_path)
    slug = "mma_se"
    jl = tmp_path / "rules" / slug / "autopsy_data.jsonl"
    jl.parent.mkdir(parents=True)

    _write_rows(jl, [{"contest_id": "111", "slug": slug}])
    pre_size = jl.stat().st_size
    assert history.logged_contest_ids(slug) == {"111"}

    # A failed log appended two more contests before the archive blew up.
    _write_rows(jl, [{"contest_id": "222", "slug": slug},
                     {"contest_id": "333", "slug": slug}])
    assert history.logged_contest_ids(slug) == {"111", "222", "333"}

    history.truncate_to(jl, pre_size)
    assert history.logged_contest_ids(slug) == {"111"}
    # The surviving line is still valid JSON (no partial-line damage).
    assert json.loads(jl.read_text().strip()) == {"contest_id": "111", "slug": slug}


def test_truncate_to_zero_removes_a_file_created_by_the_failed_log(tmp_path):
    p = tmp_path / "autopsies.md"
    p.write_text("## section written by the failed log\n")
    history.truncate_to(p, 0)
    assert not p.exists()


def test_truncate_to_missing_file_is_a_noop(tmp_path):
    history.truncate_to(tmp_path / "never_existed.jsonl", 42)
