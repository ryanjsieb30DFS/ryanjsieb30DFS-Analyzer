"""Unit tests for the sport-calibrated lineup grader (✅ Grade tab).

Includes the calibration requirement from the retro-audit: in a sport whose
observed sharks DON'T carry leverage (MMA-style), a no-sub-10% lineup must NOT
hard-flag (the UFC 250 winning builds); where sharks DO carry it (golf-style),
it must flag.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import grader  # noqa: E402


def _pool():
    return pd.DataFrame({
        "name": ["Alpha Guy", "Beta Guy", "Gamma Guy", "Delta Guy", "Echo Guy", "Foxtrot Guy"],
        "ownership": [45.0, 30.0, 20.0, 12.0, 8.0, 4.0],
        "salary": [10000, 9000, 8000, 7000, 6000, 5000],
        "proj_points": [50, 45, 40, 35, 30, 25],
    })


def _cal(**over):
    base = {
        "slug": "test", "sport": "golf",
        "shark_own": 16.0, "winners_own": 18.0, "own_flag_above": 21.6,
        "shark_leverage_pct": 49.0,
        "fades": set(), "soft_fades": set(),
        "tiers": {}, "bottom_tier": None,
        "crowded": set(), "pairs": [], "field_size": 500,
    }
    base.update(over)
    return base


def _grade_text(text, cal):
    lus = grader.parse_lineups(text, _pool())
    return [grader.grade_lineup(l, cal) for l in lus]


def _warns(g):
    return [f["msg"] for f in g["flags"] if f["level"] == "warn"]


def test_parse_matches_and_reports_unmatched():
    lus = grader.parse_lineups("Alpha Guy, beta guy, Nobody Real", _pool())
    assert len(lus) == 1
    assert [p["name"] for p in lus[0]["players"]] == ["Alpha Guy", "Beta Guy"]
    assert lus[0]["unmatched"] == ["Nobody Real"]


def test_fade_violation_flags():
    from src.autopsy import _norm_name
    cal = _cal(fades={_norm_name("Alpha Guy")})
    g = _grade_text("Alpha Guy, Echo Guy", cal)[0]
    assert any("FADE" in w for w in _warns(g))


def test_chalk_heavy_flags_above_calibrated_target():
    # Alpha+Beta avg own 37.5 > 21.6 flag line (golf calibration) → flag.
    g = _grade_text("Alpha Guy, Beta Guy", _cal())[0]
    assert any("Chalk-heavy" in w for w in _warns(g))
    # Echo+Foxtrot avg 6 → no chalk flag.
    g2 = _grade_text("Echo Guy, Foxtrot Guy", _cal())[0]
    assert not any("Chalk-heavy" in w for w in _warns(g2))


def test_no_leverage_flag_is_sport_gated():
    # Golf-style (sharks carry leverage): no sub-10 piece → WARN.
    golf = _grade_text("Alpha Guy, Beta Guy, Gamma Guy", _cal())[0]
    assert any("No sub-10%" in w for w in _warns(golf))
    # MMA-style (no envelope / chalk sharks): same lineup → info only, no warn.
    mma = _grade_text("Alpha Guy, Beta Guy, Gamma Guy",
                      _cal(sport="mma", shark_leverage_pct=None,
                           own_flag_above=None))[0]
    assert not any("No sub-10%" in w for w in _warns(mma))
    assert any("not auto-flagged" in f["msg"] for f in mma["flags"] if f["level"] == "info")


def test_recurring_pair_warns():
    cal = _cal(pairs=[{"players": ["Alpha Guy", "Beta Guy"],
                       "norm": ["alpha guy", "beta guy"], "in_n": 2, "of": 3}])
    g = _grade_text("Alpha Guy, Beta Guy, Foxtrot Guy", cal)[0]
    assert any("recurring pair" in w for w in _warns(g))
    g2 = _grade_text("Alpha Guy, Gamma Guy, Foxtrot Guy", cal)[0]
    assert not any("recurring pair" in w for w in _warns(g2))


def test_bottom_tier_flags():
    from src.autopsy import _norm_name
    cal = _cal(tiers={_norm_name("Delta Guy"): "Fade"}, bottom_tier="Fade")
    g = _grade_text("Delta Guy, Echo Guy", cal)[0]
    assert any("bottom tier" in w for w in _warns(g))


def test_portfolio_identical_and_competing():
    grades = _grade_text(
        "Alpha Guy, Beta Guy, Gamma Guy\n"
        "Alpha Guy, Beta Guy, Gamma Guy\n"       # identical
        "Alpha Guy, Beta Guy, Delta Guy\n",       # one-off pivot of #1
        _cal())
    flags = grader.grade_portfolio(grades)
    msgs = " | ".join(f["msg"] for f in flags)
    assert "IDENTICAL" in msgs and "ONE player" in msgs


def test_expected_dupes_computed():
    g = _grade_text("Alpha Guy, Beta Guy", _cal(field_size=1000))[0]
    # 0.45 * 0.30 * 1000 = 135
    assert abs(g["expected_dupes"] - 135.0) < 0.5


def test_grade_md_renders():
    grades = _grade_text("Alpha Guy, Echo Guy, Foxtrot Guy", _cal())
    md = grader.grade_md(grades, [], _cal())
    assert "Lineup 1" in md and "Calibration" in md


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
