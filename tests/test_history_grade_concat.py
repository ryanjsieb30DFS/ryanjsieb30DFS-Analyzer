"""Per-contest grade files concatenate into ONE archived lineup_grade.md."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import history  # noqa: E402


def test_archive_concatenates_per_contest_grades(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "_REPO_ROOT", tmp_path)
    (tmp_path / "rules" / "mma_se").mkdir(parents=True)
    gdir = tmp_path / "data" / "grade"
    gdir.mkdir(parents=True)
    (gdir / "mma_se.md").write_text("legacy pooled grade")
    (gdir / "mma_se__ab12cd34.md").write_text("contest one grade")
    (gdir / "mma_se__zz99.md").write_text("contest two grade")
    hist = history.archive_slate(
        slug="mma_se", sport="mma", contest_label="MMA",
        slate_label="concat test",
        autopsy_records=[{"contest_id": "1", "slate_name": "concat test"}],
        roi_contests=[{"name": "C1", "type": "SE", "field_size": 500,
                       "my_entries": 1, "entry_fee": 5, "best_rank": 10,
                       "best_percentile": 2.0}],
        proj_source=None,
    )
    text = (hist / "lineup_grade.md").read_text()
    assert "legacy pooled grade" in text
    assert "contest one grade" in text and "contest two grade" in text
    assert "# Grade — ab12cd34" in text and "# Grade — slate" in text
    manifest = json.loads((hist / "manifest.json").read_text())
    assert "lineup_grade.md" in manifest["archived"]
