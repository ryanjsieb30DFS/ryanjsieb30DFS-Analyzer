"""MMA vendor detection: DailyFan new format (Salary/Ownership), Ship It Nation
MMA signature, and junk-row sanitization. Mirrors the Simulator fixes."""
import numpy as np
import pandas as pd

from src.projections import drop_junk_rows
from src.vendors import detect_vendor


def _norm(df):
    df = df.copy()
    df.columns = [c.replace("﻿", "").strip().lower().replace(" ", "_") for c in df.columns]
    return df


def test_dailyfan_mma_new_format_detected():
    raw = pd.DataFrame(columns=[
        "Fighter", "Matchup", "Win Odds", "Win %", "Finish Odds", "Salary",
        "Ownership", "Projection DK (Mean)", "Projection DK (Win)",
        "Projection DK (Loss)", "Mean PPD", "Win PPD", "DK ID",
    ])
    sig = detect_vendor(_norm(raw))
    assert sig is not None and sig["name"] == "DailyFan MMA"


def test_ship_it_nation_removed():
    """SIN signatures were removed 7/26/26 (vendor dropped 7/18); a bare
    NAME/SAL/PROJ/OWN sheet no longer detects, and the simple PGA signature
    (has CEIL) still wins for a golf file."""
    sin = pd.DataFrame(columns=["NAME", "SAL", "PROJ", "OWN", "PT/$"])
    assert detect_vendor(_norm(sin)) is None
    pga = pd.DataFrame(columns=["NAME", "SAL", "PROJ", "CEIL", "OWN", "PT/$"])
    assert detect_vendor(_norm(pga))["name"] == "ETR PGA"


def test_dailyfan_mma_cpt_flex_detected():
    """The CPT/Flex sheet contains ALL of the old flat signature's required
    columns too, so it used to LOSE the tie to the earlier-listed old signature
    — whose map produced no salary/ownership, failing every upload. The
    mapped-columns tie-break must pick the CPT/Flex signature."""
    raw = pd.DataFrame(columns=[
        "Fighter", "Matchup", "Win Odds", "Win %", "Finish Odds",
        "Salary CPT", "Salary Flex", "Ownership CPT", "Ownership Flex",
        "Ownership Total", "Projection DK (Mean)", "Projection DK (Win)",
        "Projection DK (Loss)", "Mean PPD (Flex)", "Win PPD (Flex)",
        "DK ID CPT", "DK ID Flex",
    ])
    sig = detect_vendor(_norm(raw))
    assert sig is not None and sig["name"] == "DailyFan MMA (CPT/Flex)"
    # And the old flat sheet must STILL detect as the old signature.
    old = pd.DataFrame(columns=[
        "Fighter", "Matchup", "Win Odds", "Win %", "Finish Odds", "Salary DK",
        "Ownership DK", "Projection DK (Mean)", "Projection DK (Win)",
        "Projection DK (Loss)", "Mean PPD", "Win PPD", "DK ID",
    ])
    assert detect_vendor(_norm(old))["name"] == "DailyFan MMA"


def test_drop_junk_rows():
    df = pd.DataFrame({
        "name": ["A", "nan", "B"], "salary": [9000, 0, 8000],
        "proj_points": [50.0, np.nan, 40.0], "ownership": [20.0, 0.0, 10.0],
    })
    out = drop_junk_rows(df)
    assert list(out["name"]) == ["A", "B"] and not out["proj_points"].isna().any()


def test_etr_and_dailyfan_july_2026_generations():
    """ETR changed golf schema twice in July 2026 and DailyFan renamed its MMA
    export; the Analyzer must load all of them (it silently rejected every one,
    killing the whole strategy pipeline for PGA + MMA)."""
    import io
    from src.projections import load_projections
    gen13 = io.StringIO(
        "Golfer,Round 1 Tee Time,Round 2 Tee Time,DK Salary,Projection,DK Value,"
        "Large Field Own,DK Ceiling,Make Cut Odds,Volatility,Site,id\n"
        "Scottie Scheffler,7:33,12:43,11500,95.2,1.1,28.0,132,0.92,7.5,dk,111\n")
    gen14 = io.StringIO(
        "Golfer,Round 1 Tee Time,Round 2 Tee Time,DK Salary,Proj,DK Value,"
        "Own,DK Ceiling,Make Cut Odds,Volatility,Site,id\n"
        "Scottie Scheffler,7:33,12:43,11500,95.2,1.1,28.0,132,0.92,7.5,dk,111\n")
    classic = io.StringIO(
        "Golfer,Round 1 Tee Time,DK Salary,DK Points,DK Ceiling,Make Cut Odds,"
        "Small Field Own,Large Field Own,id\n"
        "Scottie Scheffler,7:33,11500,95.2,132,0.92,26.3,31.0,111\n")
    for gen in (gen13, gen14, classic):
        df = load_projections(gen)
        assert df.attrs["vendor"] == "ETR PGA"
        assert df["proj_points"].iloc[0] == 95.2
    # Classic export prefers SMALL field own (the SE/3-max tool's number).
    classic.seek(0)
    df = load_projections(classic)
    assert df["ownership"].iloc[0] == 26.3

    mma_v2 = io.StringIO(
        "name,Matchup,Win Odds,Win %,Finish Odds,Salary,Ownership,"
        "projection,Projection DK (Loss),Mean PPD,Win PPD,dfs_id\n"
        "Fav Fighter,1,-600,80.00%,-235,9500,30%,84.0,20.0,8.8,10.0,111\n")
    df = load_projections(mma_v2)
    assert df.attrs["vendor"] == "DailyFan MMA"
    assert df["proj_points"].iloc[0] == 84.0


def test_etr_rich_loads_every_projection_x_ownership_combo():
    """Regression (7/25/26): the rich ETR export had ONE signature per header
    generation, each hard-coupling a projection header to an ownership header,
    so only the 3 diagonal combos loaded. A mixed sheet (Proj + Small Field
    Own) DETECTED as ETR PGA and then died on missing proj_points — the worst
    mode, because a confident vendor label preceded a hard failure that killed
    the whole PGA pipeline. ETR renamed headers twice in one month, so every
    combination has to load."""
    import io
    import itertools
    from src.projections import load_projections

    def sheet(proj_hdr, own_hdr, second_own=None):
        cols = ["Golfer", "Round 1 Tee Time", "DK Salary", "DK Ceiling",
                "Make Cut Odds", proj_hdr, own_hdr]
        vals = ["Scottie Scheffler", "7:33", "11500", "132", "0.92",
                "95.2", "26.3"]
        if second_own:
            cols.append(second_own)
            vals.append("31.0")
        return io.StringIO(",".join(cols) + "\n" + ",".join(vals) + "\n")

    for p, o in itertools.product(["DK Points", "Projection", "Proj"],
                                  ["Small Field Own", "Large Field Own", "Own"]):
        df = load_projections(sheet(p, o))
        assert df.attrs["vendor"] == "ETR PGA", f"{p} + {o} failed detection"
        assert df["proj_points"].iloc[0] == 95.2, f"{p} + {o} lost proj_points"
        assert df["ownership"].iloc[0] == 26.3, f"{p} + {o} lost ownership"

    # When ETR ships BOTH ownership columns, small-field own wins — this tool
    # is scoped to SE/3-Max/5-Max, and mapping Large Field Own was the process
    # bug the Sim repo fixed 7/18/26.
    df = load_projections(sheet("DK Points", "Small Field Own", "Large Field Own"))
    assert df["ownership"].iloc[0] == 26.3
    assert "large_field_own" not in df.columns   # loser alias dropped, no collision
