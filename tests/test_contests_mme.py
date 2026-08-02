"""MME plan Phase 1: 20-Max/150-Max are declarable and inferable, and the
small-field machinery stays SEALED — focus gates unchanged, results headline
computed from focus contests only."""
from src.contests import (CONTEST_TYPES, FOCUS_CONTEST_TYPES,
                          MME_CONTEST_TYPES, infer_type)
from src import history


def test_vocabulary_and_seal_sets():
    assert "20-Max" in CONTEST_TYPES and "150-Max" in CONTEST_TYPES
    assert FOCUS_CONTEST_TYPES == {"SE", "3-Max", "5-Max"}
    assert MME_CONTEST_TYPES == {"20-Max", "150-Max"}
    assert not (FOCUS_CONTEST_TYPES & MME_CONTEST_TYPES)


def test_infer_type_maps_large_caps():
    assert infer_type(["a (3/20)", "b", "c (20/20)"]) == "20-Max"
    assert infer_type(["a (139/150)"]) == "150-Max"
    assert infer_type(["a (2/3)"]) == "3-Max"       # focus unchanged
    assert infer_type(["plain name"]) == "SE"


def test_results_headline_sealed_from_mme(tmp_path, monkeypatch):
    """A slate logging an SE and a 150-Max: the headline best_percentile is the
    SE's; the MME result lands in its own parallel fields."""
    monkeypatch.setattr(history, "_REPO_ROOT", tmp_path)
    (tmp_path / "rules" / "mma_se").mkdir(parents=True)
    hist = history.archive_slate(
        slug="mma_se", sport="mma", contest_label="MMA",
        slate_label="seal test",
        autopsy_records=[{"contest_id": "1", "slate_name": "seal test"}],
        roi_contests=[
            {"name": "SE", "type": "SE", "field_size": 500, "my_entries": 1,
             "entry_fee": 5, "best_rank": 100, "best_percentile": 20.0},
            {"name": "Mini Max", "type": "150-Max", "field_size": 50000,
             "my_entries": 20, "entry_fee": 0.5, "best_rank": 500,
             "best_percentile": 1.0},
        ],
        proj_source=None,
    )
    rows = history.load_results("mma_se")
    row = rows[-1]
    assert row["best_percentile"] == 20.0        # SE only — NOT the MME's 1.0
    assert row["best_percentile_mme"] == 1.0
    assert row["best_rank"] == 100 and row["best_rank_mme"] == 500
    assert hist.exists()
