"""Unit tests for the sport-calibrated lineup grader (✅ Grade tab).

Includes the calibration requirement from the retro-audit: a no-sub-10%
lineup must NEVER hard-flag in ANY sport (8/28/26, user directive) — the
grade measures whether a lineup follows THIS slate's strategy, and "carry a
low-owned player" is a cross-sport shark average, not a strategy call. The
UFC 250 winning builds carried none; so do contest winners regularly.
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


def test_no_leverage_is_never_a_warning_in_any_sport():
    """8/28/26, user directive: the grade measures THIS slate's strategy, and
    "carry a sub-10% player" is not a strategy call — it is a cross-sport
    shark average. It can never cost a letter, in any sport, at any rate."""
    # Golf-style, where the sharks DO carry leverage often (49%): still info.
    golf = _grade_text("Alpha Guy, Beta Guy, Gamma Guy", _cal())[0]
    assert not any("sub-10%" in w for w in _warns(golf))
    lev = [f for f in golf["flags"] if f["code"] == "no_leverage"]
    assert lev and lev[0]["level"] == "info"
    assert "does not lower the grade" in lev[0]["msg"]
    # Showdown-style, where they carry one in ~89% of lineups: STILL info.
    sd = _grade_text("Alpha Guy, Beta Guy, Gamma Guy",
                     _cal(sport="showdown", shark_leverage_pct=88.7))[0]
    assert not any("sub-10%" in w for w in _warns(sd))
    # MMA-style (no envelope at all): info, and it says the pros run chalk.
    mma = _grade_text("Alpha Guy, Beta Guy, Gamma Guy",
                      _cal(sport="mma", shark_leverage_pct=None,
                           own_flag_above=None))[0]
    assert not any("sub-10%" in w for w in _warns(mma))
    assert any("chalk-heavy" in f["msg"] for f in mma["flags"]
               if f["code"] == "no_leverage")


def test_a_no_leverage_lineup_can_still_grade_A():
    """The letter is what the user actually reads — an otherwise clean lineup
    carrying zero low-owned players must not lose a step for it."""
    # Gamma 20% + Delta 12%: nothing under 10, and avg own 16 is under the
    # 21.6 chalk line, so no_leverage is the only thing the grader can see.
    g = _grade_text("Gamma Guy, Delta Guy", _cal())[0]
    assert g["n_sub10"] == 0
    assert _warns(g) == []
    assert grader.letter_grade(g, _cal())["letter"] == "A"


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


def test_salary_over_cap_warns():
    import pandas as pd
    big = pd.DataFrame({
        "name": ["Rich One", "Rich Two"],
        "ownership": [20.0, 20.0],
        "salary": [30000, 30000],
        "proj_points": [50, 50],
    })
    lus = grader.parse_lineups("Rich One, Rich Two", big)
    g = grader.grade_lineup(lus[0], _cal())
    assert any("exceeds" in w for w in _warns(g))


def test_retro_grade_flags_vs_clean():
    from src.autopsy import _norm_name
    cal = _cal(fades={_norm_name("Bad Fade")}, own_flag_above=25.0,
               shark_leverage_pct=49.0)
    records = [{"user_lineups": [
        # flagged: chalk-heavy AND fade violation
        {"players": ["Bad Fade", "B"], "avg_own": 40.0, "low_own_count": 1,
         "percentile": 60.0},
        # clean: modest own, has a low-own piece
        {"players": ["C", "D"], "avg_own": 15.0, "low_own_count": 1,
         "percentile": 5.0},
        # CLEAN as of 8/28/26: no low-owned piece is not a flag at any shark
        # rate — the self-validation must measure what the grader charges for.
        {"players": ["E", "F"], "avg_own": 20.0, "low_own_count": 0,
         "percentile": 45.0},
    ]}]
    rg = grader.retro_grade(records, cal)
    assert rg["gradable"] and rg["n_lineups"] == 3
    assert rg["flagged_pctiles"] == [60.0]
    assert sorted(rg["clean_pctiles"]) == [5.0, 45.0]
    flags = {tuple(l["players"]): l["flags"] for l in rg["lineups"]}
    assert "fade_violation" in flags[("B", "Bad Fade")]
    assert flags[("E", "F")] == []


def test_retro_grade_never_flags_no_leverage():
    # 8/28/26: no_leverage is not a retro flag in ANY sport, at any rate.
    cal = _cal(shark_leverage_pct=None, own_flag_above=None)
    records = [{"user_lineups": [
        {"players": ["A", "B"], "avg_own": 45.0, "low_own_count": 0, "percentile": 1.0},
    ]}]
    rg = grader.retro_grade(records, cal)
    assert rg["lineups"][0]["flags"] == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


def test_leverage_md_reads_exposure_vs_field():
    """The leverage read: my entry-set exposure vs projected field ownership."""
    from src.grader import leverage_md
    lus = [{"players": [{"name": "A", "own": 30.0}, {"name": "B", "own": 8.0}]},
           {"players": [{"name": "A", "own": 30.0}, {"name": "C", "own": None}]}]
    md = leverage_md(lus)
    assert "| A | 100% | 30.0% | +70.0% |" in md
    assert "| B | 50% | 8.0% | +42.0% |" in md
    assert "| C | 50% | — | — |" in md      # missing ownership never fabricated
    assert leverage_md([]) is None


# ---- Per-contest letter grading (8/9/26) -----------------------------------


def _flag(level, code):
    return {"level": level, "code": code, "msg": f"[{code}]"}


def test_flag_codes_present():
    from src.autopsy import _norm_name
    cal = _cal(fades={_norm_name("Alpha Guy")}, own_flag_above=10.0)
    g = _grade_text("Alpha Guy, Beta Guy, Gamma Guy", cal)[0]
    codes = {f.get("code") for f in g["flags"]}
    assert "fade" in codes and "chalk_heavy" in codes


def test_letter_grade_boundaries():
    cal = _cal()
    for n, expect in ((0, "A"), (1, "B"), (2, "C"), (3, "D"), (4, "F")):
        g = {"flags": [_flag("warn", "chalk_heavy")] * n}
        assert grader.letter_grade(g, cal)["letter"] == expect
    # Hard F: a fade violation is final even with one warn.
    g = {"flags": [_flag("warn", "fade")]}
    lt = grader.letter_grade(g, cal)
    assert lt["letter"] == "F" and "final" in lt["why"][0]
    assert grader.letter_grade({"flags": [_flag("warn", "salary_cap")]},
                               cal)["letter"] == "F"


def test_letter_grade_sim_bumps():
    cal = _cal(payout_shape="Top-heavy")
    # 92nd percentile in this contest -> one step up.
    g1 = {"flags": [_flag("warn", "chalk_heavy")] * 3}       # base D
    lt = grader.letter_grade(g1, cal, {"pct_top1": 92.0, "pct_cash": 10.0})
    assert lt["letter"] == "C" and lt["base"] == "D"
    # A stays A.
    lt2 = grader.letter_grade({"flags": []}, cal, {"pct_top1": 99.0, "pct_cash": 0})
    assert lt2["letter"] == "A"
    # 20th percentile -> one step down; D drops to F.
    lt3 = grader.letter_grade(g1, cal, {"pct_top1": 20.0, "pct_cash": 95.0})
    assert lt3["letter"] == "F"
    lt4 = grader.letter_grade({"flags": []}, cal, {"pct_top1": 20.0, "pct_cash": 95.0})
    assert lt4["letter"] == "B"
    # Mid percentile -> unchanged.
    assert grader.letter_grade({"flags": []}, cal,
                               {"pct_top1": 50.0, "pct_cash": 50.0})["letter"] == "A"
    # Hard F never bumps up.
    hard = {"flags": [_flag("warn", "fade")]}
    assert grader.letter_grade(hard, cal, {"pct_top1": 99.0,
                                           "pct_cash": 99.0})["letter"] == "F"
    # Flat contests read the cash percentile instead.
    flat = _cal(payout_shape="Flat")
    assert grader.letter_grade(g1, flat, {"pct_top1": 5.0,
                                          "pct_cash": 95.0})["letter"] == "C"
    # No sim row -> no adjustment + the plain-language note.
    lt5 = grader.letter_grade({"flags": []}, cal, None)
    assert lt5["letter"] == "A" and any("not in the Sim's pool" in w
                                        for w in lt5["why"])


def test_worst_letter():
    assert grader.worst_letter(["A", "C", "B"]) == "C"
    assert grader.worst_letter(["A", "F"]) == "F"
    assert grader.worst_letter([]) is None


def test_sim_standing_percentile_exact():
    pool = {"rosters": [["A", "B"], ["C", "D"], ["E", "F"]]}
    contest = {"metrics": {"top1_pct": [1.0, 5.0, 9.0],
                           "cash_pct": [30.0, 20.0, 10.0]}}
    std = grader.sim_standing(pool, contest, "C|D")
    assert std["index"] == 1
    assert std["pct_top1"] == 50.0      # 1 of 2 others strictly below
    assert std["pct_cash"] == 50.0
    assert grader.sim_standing(pool, contest, "X|Y") is None
    top = grader.sim_standing(pool, contest, "E|F")
    assert top["pct_top1"] == 100.0 and top["pct_cash"] == 0.0


def test_contest_calibration_carries_contest_context(monkeypatch):
    import src.grader as gmod
    monkeypatch.setattr(gmod, "_baseline", lambda: {}, raising=False)
    contest = {"id": "ab12cd34", "name": "Little SE", "type": "SE",
               "field_size": 588, "my_entries": 1, "entry_fee": 12.0,
               "payout_shape": "Top-heavy"}
    cal = grader.contest_calibration("nascar", "nascar", contest)
    assert cal["field_size"] == 588            # THIS contest, not a slate max
    assert cal["payout_shape"] == "Top-heavy"
    assert cal["contest_name"] == "Little SE" and cal["my_entries"] == 1


def test_contest_grade_md_shows_letters():
    cal = _cal(contest_name="Little SE", payout_shape="Top-heavy")
    g = _grade_text("Alpha Guy, Beta Guy, Gamma Guy, Delta Guy, Echo Guy, Foxtrot Guy",
                    cal)[0]
    lt = grader.letter_grade(g, cal)
    md = grader.contest_grade_md([g], [lt], [], cal)
    assert f"Grade {lt['letter']} — Lineup 1" in md
    assert "Little SE" in md


def test_clear_drafts_globs_suffixed(tmp_path, monkeypatch):
    import src.grader as gmod
    monkeypatch.setattr(gmod, "_DRAFT_DIR", tmp_path)
    (tmp_path / "nascar.txt").write_text("x")
    (tmp_path / "nascar__ab12cd34.txt").write_text("y")
    grader.clear_drafts("nascar")
    assert not list(tmp_path.glob("nascar*"))
