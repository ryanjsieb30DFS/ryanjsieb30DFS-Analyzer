"""Targeted regression tests for the Tier 1/2 audit fixes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402

from src.vendors import mlb_team_key  # noqa: E402
from src.projections_diff import diff_table  # noqa: E402
from src.slate_analysis import _mlb_signals  # noqa: E402


def test_mlb_team_key_none_and_nan():
    assert mlb_team_key(None) is None
    assert mlb_team_key(float("nan")) is None
    assert mlb_team_key("") is None
    assert mlb_team_key("   ") is None
    # real teams still resolve
    assert mlb_team_key("Cubs") == "CHC" or mlb_team_key("CHC") == "CHC"


def test_projections_diff_zero_mean_is_finite():
    # Two vendors whose values cancel to a ~0 mean must not yield inf delta_pct.
    a = pd.DataFrame({"name": ["X"], "proj_points": [5.0]})
    b = pd.DataFrame({"name": ["X"], "proj_points": [-5.0]})
    out = diff_table({"A": {"df": a, "vendor": "A"}, "B": {"df": b, "vendor": "B"}},
                     metric="proj_points")
    assert not out.empty
    import math
    for v in out["delta_pct"]:
        assert math.isfinite(v), f"delta_pct should be finite, got {v}"


def test_mlb_pitcher_excluded_and_nan_position_does_not_crash():
    # A pitcher WITH a position is excluded from the hitter stack; a row with a
    # NaN position must not crash the signal build (fillna hygiene). Note: a
    # pitcher with NO position is genuinely unclassifiable and counts as a hitter.
    df = pd.DataFrame({
        "name": ["Ace", "Bat1", "Bat2", "Unknown"],
        "position": ["P", "1B", "OF", None],  # explicit P + one NaN position
        "team": ["NYM", "NYM", "NYM", "NYM"],
        "proj_points": [18.0, 9.0, 8.0, 7.0],
        "ownership": [20.0, 12.0, 10.0, 5.0],
    })
    sig = _mlb_signals(df)  # must not raise on the NaN position
    stacks = sig.get("team_stacks")
    assert stacks is not None and len(stacks)
    nym = [r for r in stacks.to_dict("records") if r.get("team") == "NYM"][0]
    # 2 real hitters + the unclassifiable row = 3; the explicit pitcher is excluded.
    assert nym["n"] == 3, f"explicit pitcher should be excluded; got {nym}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
