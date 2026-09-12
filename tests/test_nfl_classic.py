"""NFL Classic (nfl_classic) support — vendor detection (both ETR header
generations), projections pipeline, warn split, registry wiring, grader slot
markers, autopsy salary map, rules dir, strategy block. Added 2026-09-12."""
import io
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.projections import load_projections, warn_missing_for_sport  # noqa: E402
from src.vendors import VENDOR_SIGNATURES, detect_vendor  # noqa: E402

# The real 2026 ETR NFL Main Slate headers (user sample 9/12/26).
_CLASSIC_CSV = (
    '"Player","DK Pos","Team","Opp","DK Salary","DK Proj","DK Value","Small Field",'
    '"Large Field","DK Floor","DK Ceiling","id"\n'
    '"Jahmyr Gibbs","RB","DET","NO","$8,000","24.8","5.9","56.0%","42.4%","11.0","40.6","43727325"\n'
    '"Ja\'Marr Chase","WR","CIN","TB","$7,800","22.1","3.7","33.7%","28.3%","9.4","37.5","43727631"\n'
    '"Josh Allen","QB","BUF","@MIA","$7,400","22.0","3.0","12.0%","10.1%","13.0","33.0","43727001"\n'
    '"Sam LaPorta","TE","DET","NO","$5,000","11.0","1.0","9.0%","8.0%","4.0","21.0","43727002"\n'
    '"Chargers ","DST","LAC","ARI","$3,500","8.1","0.1","4.7%","5.6%","2.0","15.7","43728525"\n'
    '"Corey Kiner","RB","NE","@SEA","$4,000","0.0","-8.5","0.0%","0.0%","0.0","0.0","43727585"\n'
)
_LEGACY_CSV = (
    '"Name","Team","Opponent","Position","Salary","Projection","Value","Ownership",'
    '"DKSlateID","Floor","Ceiling","Small"\n'
    '"Josh Allen","BUF","MIA","QB","7400","22.0","3.0","10.1","43727001","13.0","33.0","12.0"\n'
    '"Steelers","PIT","ATL","DST","3300","8.5","1.0","20.0","43728527","2.0","15.0","18.2"\n'
)
_REAL = Path.home() / "Downloads" / "DraftKings NFL DFS Projections -- Main Slate (42).csv"


def _norm_cols(headers):
    return {h.replace("﻿", "").strip().lower().replace(" ", "_") for h in headers}


def test_classic_vendor_detected():
    df = pd.read_csv(io.StringIO(_CLASSIC_CSV))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    sig = detect_vendor(df)
    assert sig is not None and sig["name"] == "ETR NFL Classic"
    assert sig["sport"] == "nfl"


def test_legacy_classic_vendor_detected():
    df = pd.read_csv(io.StringIO(_LEGACY_CSV))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    sig = detect_vendor(df)
    assert sig is not None and sig["name"] == "ETR NFL Classic (legacy)"
    # the 3-game-slate header variant
    cols = _norm_cols(["DK Name", "Team", "Opponent", "DK Position", "DK Salary",
                       "DK Projection", "DK Value", "DK Ownership", "DK Floor",
                       "DK Ceiling", "DKSlateID"])
    assert detect_vendor(pd.DataFrame(columns=sorted(cols)))["name"] == "ETR NFL Classic (legacy)"


def test_classic_signature_does_not_shadow_showdown():
    sd_headers = _norm_cols(["Name", "Team", "Position", "Salary", "Projection", "Ceiling",
                             "Total Own", "CPT Salary", "CPT Projection", "CPT Own"])
    assert detect_vendor(pd.DataFrame(columns=sorted(sd_headers)))["name"] == "ETR NFL Showdown"
    for sig in VENDOR_SIGNATURES:
        if sig["name"].startswith("ETR NFL Classic"):
            assert not sig["required_columns"].issubset(sd_headers)


def test_classic_pipeline_load():
    df = load_projections(io.StringIO(_CLASSIC_CSV))
    assert df.attrs.get("vendor") == "ETR NFL Classic"
    assert len(df) == 6                                 # the 0.0-proj row SURVIVES (NFL: 0.0 is real)
    for c in ("name", "position", "team", "opponent", "salary", "proj_points",
              "ownership", "own_large", "floor", "ceiling", "dk_id", "stddev"):
        assert c in df.columns, c
    gibbs = df[df["name"] == "Jahmyr Gibbs"].iloc[0]
    assert gibbs["salary"] == 8000
    assert gibbs["ownership"] == 56.0                   # Small Field wins `ownership`
    assert gibbs["own_large"] == 42.4                   # Large Field survives alongside
    assert gibbs["floor"] == 11.0 and gibbs["ceiling"] == 40.6
    assert gibbs["dk_id"] == 43727325
    assert "Chargers" in set(df["name"])                # trailing space stripped
    assert "dk_value" not in df.columns


def test_legacy_pipeline_load():
    df = load_projections(io.StringIO(_LEGACY_CSV))
    assert df.attrs.get("vendor") == "ETR NFL Classic (legacy)"
    allen = df[df["name"] == "Josh Allen"].iloc[0]
    assert allen["ownership"] == 12.0                   # `Small` beats `Ownership`
    assert allen["dk_id"] == 43727001 and allen["position"] == "QB"


@pytest.mark.skipif(not _REAL.exists(), reason="real ETR Main Slate file not on disk")
def test_real_main_slate_file_loads():
    df = load_projections(str(_REAL))
    assert df.attrs.get("vendor") == "ETR NFL Classic"
    assert len(df) >= 300
    assert (df["position"] == "DST").sum() >= 20
    assert set(df["position"]) == {"QB", "RB", "WR", "TE", "DST"}
    assert df["name"].str.strip().eq(df["name"]).all()


def test_warn_missing_split_by_slug():
    ok = pd.DataFrame({"name": ["a"], "salary": [1], "proj_points": [1.0],
                       "ownership": [1.0], "position": ["QB"], "team": ["BAL"],
                       "opponent": ["PIT"]})
    assert warn_missing_for_sport(ok, "nfl", slug="nfl_classic") == []
    # Classic never asks for captain columns...
    assert not any("cpt" in w for w in
                   warn_missing_for_sport(ok, "nfl", slug="nfl_classic"))
    bare = ok.drop(columns=["position", "team", "opponent"])
    warns = warn_missing_for_sport(bare, "nfl", slug="nfl_classic")
    assert len(warns) == 3 and all(w.startswith("NFL Classic:") for w in warns)
    # ...while Showdown still does (and the slug-less call keeps SD behavior).
    sd = warn_missing_for_sport(ok, "nfl", slug="nfl_sd")
    assert any("salary_cpt" in w for w in sd) and any("own_cpt" in w for w in sd)
    assert warn_missing_for_sport(ok, "nfl") == sd


def test_registry_wiring():
    from app import CONTEST_TYPES
    assert CONTEST_TYPES["NFL Classic"] == {"slug": "nfl_classic", "sport": "nfl"}
    from src.sim_link import _SLUG_SPORT, _CORRECTABLE_SPORTS
    assert _SLUG_SPORT["nfl_classic"] == "nfl"
    assert "nfl" not in _CORRECTABLE_SPORTS          # no NFL dupe corpus


def test_grader_baseline_key_and_seeded_envelope():
    import json
    from src.grader import _baseline_key, calibration
    assert _baseline_key("nfl_classic", "nfl") == "nfl"
    base = json.loads((Path(__file__).parent.parent / "rules" / "shared"
                       / "shark_baseline.json").read_text())
    blk = base["sports"]["nfl"]
    assert blk["n_contests"] >= 20 and blk["seed_weight"] >= 1
    for f in ("own_per_slot", "leverage_pct", "anchor_exposure", "unique_pct"):
        assert blk["shark_envelope"][f] is not None
    cal = calibration("nfl_classic", "nfl", [])
    assert cal["shark_own"] == blk["shark_envelope"]["own_per_slot"]


def test_grader_strips_classic_slot_markers():
    from src.grader import parse_lineups, grade_lineup
    pool = load_projections(io.StringIO(_CLASSIC_CSV))
    text = ("QB Josh Allen, RB Jahmyr Gibbs, WR Ja'Marr Chase, TE Sam LaPorta, "
            "FLEX Corey Kiner, DST Chargers")
    lus = parse_lineups(text, pool)
    assert len(lus) == 1 and lus[0]["unmatched"] == []
    names = [p["name"] for p in lus[0]["players"]]
    assert names == ["Josh Allen", "Jahmyr Gibbs", "Ja'Marr Chase", "Sam LaPorta",
                     "Corey Kiner", "Chargers"]
    assert not any(p.get("cpt") for p in lus[0]["players"])
    g = grade_lineup(lus[0], {"slug": "nfl_classic", "sport": "nfl"})
    assert g["salary_used"] == 7400 + 8000 + 7800 + 5000 + 4000 + 3500
    # The Showdown "no captain marked" note must never fire on Classic.
    assert "no_cpt_marker" not in [f["code"] for f in g["flags"]]


def test_autopsy_classic_keeps_salary_map():
    from src.autopsy import analyze_contest, parse_dk_results, proj_frame_for_autopsy
    csv = (
        "Rank,EntryId,EntryName,TimeRemaining,Points,Lineup,,Player,Roster Position,%Drafted,FPTS\n"
        "1,1,alpha,0,150.0,DST Chargers  FLEX Corey Kiner QB Josh Allen RB Jahmyr Gibbs RB Jahmyr Gibbs "
        "TE Sam LaPorta WR Ja'Marr Chase WR Ja'Marr Chase WR Ja'Marr Chase,,Josh Allen,QB,12.0%,25.0\n"
        "2,2,beta,0,140.0,DST Chargers  FLEX Corey Kiner QB Josh Allen RB Jahmyr Gibbs RB Jahmyr Gibbs "
        "TE Sam LaPorta WR Ja'Marr Chase WR Ja'Marr Chase WR Ja'Marr Chase,,Jahmyr Gibbs,RB,56.0%,30.0\n"
        ",,,,,,,Chargers,DST,4.7%,-2.0\n"
    )
    parsed = parse_dk_results(io.StringIO(csv))
    pool = load_projections(io.StringIO(_CLASSIC_CSV))
    pf = proj_frame_for_autopsy([pool])
    classic = analyze_contest(parsed, pf, "nfl", slug="nfl_classic")
    assert classic["salary_map"]                      # salary-aware counterfactual kept
    sd = analyze_contest(parsed, pf, "nfl", slug="nfl_sd")
    assert sd["salary_map"] is None                   # Showdown still points-only


def test_shark_handles_map_nfl_classic():
    import yaml
    cfg = yaml.safe_load((Path(__file__).parent.parent / "rules" / "shared"
                          / "shark_handles.yaml").read_text())
    assert cfg["slug_sport"]["nfl_classic"] == "nfl"
    assert cfg["sharks_by_sport"]["nfl"]


def test_rules_dir_exists():
    root = Path(__file__).parent.parent / "rules" / "nfl_classic"
    for f in ("philosophy.md", "framework.md", "autopsies.md", "lessons.yaml"):
        assert (root / f).exists(), f"rules/nfl_classic/{f} missing"
    import yaml
    lessons = yaml.safe_load((root / "lessons.yaml").read_text())["lessons"]
    assert len(lessons) >= 4 and all(l["status"] == "hypothesis" for l in lessons)


def test_strategy_block_injection():
    import inspect
    from src import analysis_runner as ar
    assert "nfl_classic" in ar._NFL_CLASSIC_STRATEGY_BLOCK or "NFL CLASSIC" in ar._NFL_CLASSIC_STRATEGY_BLOCK
    src = inspect.getsource(ar.run_analysis)
    assert '_NFL_CLASSIC_STRATEGY_BLOCK if slug == "nfl_classic"' in src
    assert '_NFL_SD_STRATEGY_BLOCK if slug == "nfl_sd"' in src
    pool_src = inspect.getsource(ar.run_player_pool)
    assert "| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |" in pool_src
