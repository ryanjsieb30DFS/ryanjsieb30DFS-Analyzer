"""NFL Showdown (nfl_sd) support — vendor detection, projections pipeline,
grader captain math, autopsy CPT pricing, registry wiring. Added 2026-09-09."""
import io
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.projections import load_projections, warn_missing_for_sport  # noqa: E402
from src.vendors import VENDOR_SIGNATURES, detect_vendor  # noqa: E402


# The real ETR NFL Showdown export headers (user-confirmed 9/9/26,
# "DK BAL-PIT Showdown Fantasy and Ownership Projections.csv").
_SD_CSV = (
    '"Name","Team","Position","Salary","Projection","Ceiling","Total Own",'
    '"CPT Salary","CPT Projection","CPT Own"\n'
    '"Lamar Jackson","BAL","QB","11600","17.0","26.6","65.3","17400","25.4","16.2"\n'
    '"Derrick Henry","BAL","RB","11400","16.5","29.7","61.7","17100","24.8","21.2"\n'
    '"Zay Flowers","BAL","WR","9200","15.3","27.6","63.9","13800","22.9","18.7"\n'
    '"Aaron Rodgers","PIT","QB","10000","13.7","22.4","43.1","15000","20.6","5.7"\n'
    '"Chris Boswell","PIT","K","4600","8.1","13.9","28.0","6900","12.2","2.1"\n'
    '"Steelers","PIT","DST","4200","6.5","12.0","30.5","6300","9.8","3.3"\n'
)


def _norm_cols(headers):
    return {h.replace("﻿", "").strip().lower().replace(" ", "_") for h in headers}


def test_sd_vendor_detected():
    df = pd.read_csv(io.StringIO(_SD_CSV))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    sig = detect_vendor(df)
    assert sig is not None and sig["name"] == "ETR NFL Showdown"
    assert sig["sport"] == "nfl"


def test_main_slate_etr_nfl_gets_no_signature():
    # The ETR NFL Main Slate export lacks the CPT columns — Showdown is the
    # ONLY NFL signature tonight, so this header set must match NOTHING.
    cols = _norm_cols([
        "Name", "Team", "Opponent", "Position", "Salary", "Projection",
        "Value", "Ownership", "DKSlateID", "Floor", "Ceiling", "Small",
    ])
    df = pd.DataFrame(columns=sorted(cols))
    assert detect_vendor(df) is None


def test_sd_signature_does_not_shadow_others():
    # The SD required set must not be a subset of any other sheet's headers:
    # no existing signature's required columns may be a subset of the SD
    # headers either (which would create a detection tie).
    sd = next(s for s in VENDOR_SIGNATURES if s["name"] == "ETR NFL Showdown")
    sd_headers = _norm_cols([
        "Name", "Team", "Position", "Salary", "Projection", "Ceiling",
        "Total Own", "CPT Salary", "CPT Projection", "CPT Own"])
    for sig in VENDOR_SIGNATURES:
        if sig["name"] == "ETR NFL Showdown":
            continue
        assert not sig["required_columns"].issubset(sd_headers), (
            f"{sig['name']} would also match the NFL SD sheet")


def test_sd_pipeline_canonical_columns():
    df = load_projections(io.StringIO(_SD_CSV))
    assert df.attrs["vendor"] == "ETR NFL Showdown"
    for col in ("name", "salary", "proj_points", "ownership", "position",
                "team", "salary_cpt", "proj_cpt", "own_cpt", "own_flex",
                "ceiling"):
        assert col in df.columns, f"missing {col}"
    lamar = df[df["name"] == "Lamar Jackson"].iloc[0]
    assert lamar["salary"] == 11600            # FLEX price
    assert lamar["salary_cpt"] == 17400        # captain price (1.5x)
    assert lamar["ownership"] == 65.3          # TOTAL own (CPT+FLEX)
    assert lamar["own_cpt"] == 16.2
    assert abs(lamar["own_flex"] - 49.1) < 1e-6   # total - cpt, floored at 0
    assert (df["own_flex"] >= 0).all()


def test_warn_missing_nfl():
    ok = pd.DataFrame({"name": ["a"], "salary": [1], "proj_points": [1.0],
                       "ownership": [1.0], "position": ["QB"], "team": ["BAL"],
                       "salary_cpt": [1.5], "own_cpt": [0.5]})
    assert warn_missing_for_sport(ok, "nfl") == []
    bare = ok.drop(columns=["position", "team", "salary_cpt", "own_cpt"])
    warns = warn_missing_for_sport(bare, "nfl")
    assert len(warns) == 4
    joined = " ".join(warns)
    for col in ("position", "team", "salary_cpt", "own_cpt"):
        assert col in joined


def test_registry_wiring():
    from app import CONTEST_TYPES
    assert CONTEST_TYPES["NFL Showdown"] == {"slug": "nfl_sd", "sport": "nfl"}
    from src.sim_link import _SLUG_SPORT, _CORRECTABLE_SPORTS
    assert _SLUG_SPORT["nfl_sd"] == "nfl_showdown"
    # No NFL dupe-correction corpus exists — nfl must never be correctable.
    assert "nfl_showdown" not in _CORRECTABLE_SPORTS
    assert "nfl" not in _CORRECTABLE_SPORTS


def test_grader_baseline_key():
    from src.grader import _baseline_key
    assert _baseline_key("nfl_sd", "nfl") == "nfl_showdown"
    assert _baseline_key("pga_rd4_sd", "golf") == "showdown"
    assert _baseline_key("mma_se", "mma") == "mma"


def test_grader_calibration_degrades_without_sd_baseline():
    # shark_baseline.json has no nfl_showdown block — targets must be None,
    # never a crash (guide-not-gate: absence of data is not a warning).
    from src.grader import calibration
    cal = calibration("nfl_sd", "nfl", [])
    assert cal["shark_own"] is None
    assert cal["shark_leverage_pct"] is None


def test_grader_cpt_marker_prices_captain():
    from src.grader import parse_lineups, grade_lineup
    pool = load_projections(io.StringIO(_SD_CSV))
    text = ("CPT Lamar Jackson, FLEX Derrick Henry, FLEX Zay Flowers, "
            "FLEX Aaron Rodgers, FLEX Chris Boswell, FLEX Steelers")
    lus = parse_lineups(text, pool)
    assert len(lus) == 1
    lu = lus[0]
    assert lu["unmatched"] == []
    cpt = lu["players"][0]
    assert cpt["name"] == "Lamar Jackson" and cpt.get("cpt") is True
    assert cpt["salary"] == 17400          # CPT price, not the 11600 FLEX price
    assert cpt["own"] == 16.2              # CPT own, not the 65.3 total own
    g = grade_lineup(lu, {"slug": "nfl_sd", "sport": "nfl"})
    # 17400 + 11400 + 9200 + 10000 + 4600 + 4200 = 56800 — flex-priced it
    # would be 51000... either way over cap here, but the point is the CPT
    # price is in the sum.
    assert g["salary_used"] == 17400 + 11400 + 9200 + 10000 + 4600 + 4200


def test_grader_no_cpt_marker_info_flag():
    from src.grader import parse_lineups, grade_lineup
    pool = load_projections(io.StringIO(_SD_CSV))
    lus = parse_lineups("Lamar Jackson, Derrick Henry", pool)
    g = grade_lineup(lus[0], {"slug": "nfl_sd", "sport": "nfl"})
    codes = [f["code"] for f in g["flags"]]
    assert "no_cpt_marker" in codes
    assert all(f["level"] == "info" for f in g["flags"]
               if f["code"] == "no_cpt_marker")


def test_autopsy_lineup_profile_uses_cpt_price():
    from src.autopsy import lineup_profile, _norm_name
    proj_lookup = {
        _norm_name("Lamar Jackson"): {
            "salary": 11600, "proj_points": 17.0,
            "salary_cpt": 17400, "proj_cpt": 25.4},
        _norm_name("Derrick Henry"): {
            "salary": 11400, "proj_points": 16.5,
            "salary_cpt": 17100, "proj_cpt": 24.8},
    }
    own_map = {_norm_name("Lamar Jackson"): 40.0,
               _norm_name("Derrick Henry"): 30.0}
    prof = lineup_profile(["Lamar Jackson", "Derrick Henry"], own_map,
                          proj_lookup, {}, "nfl", cpt="Lamar Jackson")
    assert prof["salary_used"] == 17400 + 11400
    assert prof["proj_total"] == round(25.4 + 16.5, 2)
    # Without a captain, everything stays FLEX-priced (all other sports).
    flat = lineup_profile(["Lamar Jackson", "Derrick Henry"], own_map,
                          proj_lookup, {}, "nfl")
    assert flat["salary_used"] == 11600 + 11400


def test_pool_calibration_nfl_keeps_zero_scores():
    from src.pool_calibration import grade_tiers
    md = ("| Rank | Player | Tier |\n|---|---|---|\n"
          "| 1 | Zay Flowers | Core |\n| 2 | Chris Boswell | Okay |\n")
    players = pd.DataFrame({"name": ["Zay Flowers", "Chris Boswell"],
                            "actual_fpts": [21.5, 0.0]})
    # Default (non-NFL): the 0.0 is excluded as a scratch.
    cal = grade_tiers(md, players)
    assert cal["excluded_scratches"] == [{"name": "Chris Boswell", "tier": "Okay"}]
    # NFL: 0.0 is a real score — nothing excluded.
    cal_nfl = grade_tiers(md, players, sport="nfl")
    assert cal_nfl["excluded_scratches"] == []
    okay = next(t for t in cal_nfl["tiers"] if t["tier"] == "Okay")
    assert okay["avg_fpts"] == 0.0


def test_shark_handles_map_nfl_sd():
    import yaml
    cfg = yaml.safe_load(
        (Path(__file__).parent.parent / "rules" / "shared"
         / "shark_handles.yaml").read_text())
    assert cfg["slug_sport"]["nfl_sd"] == "nfl_showdown"
    assert cfg["sharks_by_sport"]["nfl_showdown"] == cfg["sharks_by_sport"]["nfl"]


def test_rules_dir_exists():
    root = Path(__file__).parent.parent / "rules" / "nfl_sd"
    for f in ("philosophy.md", "framework.md", "autopsies.md", "lessons.yaml"):
        assert (root / f).exists(), f"rules/nfl_sd/{f} missing"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
