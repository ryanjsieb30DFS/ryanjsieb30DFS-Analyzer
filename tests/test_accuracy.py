"""Unit tests for the self-grading accuracy layer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import accuracy  # noqa: E402


def _record(user_players, defining, over, under, proj=300.0, pts=330.0, pct=8.0):
    """One synthetic autopsy contest record (subset of the real schema)."""
    return {
        "user_lineups": [{
            "entry_name": "Me (1/1)", "players": user_players,
            "proj_total": proj, "points": pts, "percentile": pct, "avg_own": 14.0,
        }],
        "slate_defining_plays": [{"name": n} for n in defining],
        "top_overperformers": [{"name": n} for n in over],
        "top_underperformers": [{"name": n} for n in under],
    }


def test_leverage_capture_counts_owned_defining_plays():
    rec = _record(
        user_players=["Bud Cauley", "Scottie Scheffler", "X", "Y", "Z", "W"],
        defining=["Bud Cauley", "Some Sleeper"],  # we own 1 of 2
        over=[], under=[],
    )
    e = accuracy.grade_edges([rec])
    assert e["gradable"] is True
    assert e["leverage_capture"] == 0.5
    assert e["leverage_hit"] == ["Bud Cauley"]
    assert e["leverage_missed"] == ["Some Sleeper"]


def test_overperformer_and_bust_capture():
    rec = _record(
        user_players=["Hot Guy", "Bust Guy", "a", "b", "c", "d"],
        defining=[],
        over=["Hot Guy", "Other Hot"],   # owned 1/2
        under=["Bust Guy"],              # owned 1/1 -> bad
    )
    e = accuracy.grade_edges([rec])
    assert e["overperformer_capture"] == 0.5
    assert e["underperformer_exposure"] == 1.0
    assert e["underperformer_hit"] == ["Bust Guy"]


def test_edges_not_gradable_without_lineups():
    rec = {"user_lineups": [], "slate_defining_plays": [{"name": "x"}]}
    assert accuracy.grade_edges([rec])["gradable"] is False


def test_name_normalization_matches_accents_and_periods():
    rec = _record(
        user_players=["Daniel Suárez", "J.T. Poston", "a", "b", "c", "d"],
        defining=["Daniel Suarez", "J T Poston"],  # accent/period variants
        over=[], under=[],
    )
    e = accuracy.grade_edges([rec])
    # "Daniel Suarez" matches "Daniel Suárez"; "J T Poston" has a space the norm
    # doesn't strip, so it won't match "J.T. Poston" -> exactly one capture.
    assert e["leverage_hit"] == ["Daniel Suarez"]


def test_grade_lineups_ratio_and_percentile():
    rec = _record(["a", "b", "c", "d", "e", "f"], [], [], [], proj=300.0, pts=330.0, pct=4.0)
    ln = accuracy.grade_lineups([rec])
    assert ln["n_lineups"] == 1
    assert ln["avg_ratio"] == 1.1
    assert ln["best_percentile"] == 4.0
    assert ln["n_top_10pct"] == 1


def test_grade_lineups_dedupes_same_entry_across_contests():
    players = ["a", "b", "c", "d", "e", "f"]
    rec1 = _record(players, [], [], [], pct=8.0)
    rec2 = _record(players, [], [], [], pct=8.0)  # same entry in a 2nd contest
    ln = accuracy.grade_lineups([rec1, rec2])
    assert ln["n_lineups"] == 1, "same roster+entry should dedupe across records"


def test_slate_accuracy_md_renders():
    rec = _record(["Bud Cauley", "b", "c", "d", "e", "f"], ["Bud Cauley"], ["Bud Cauley"], [])
    md = accuracy.slate_accuracy_md([rec])
    assert "Self-grade" in md and "Leverage capture" in md


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
