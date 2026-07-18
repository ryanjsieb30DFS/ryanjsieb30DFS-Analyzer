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


def test_ship_it_mma_detected_and_no_pga_collision():
    sin = pd.DataFrame(columns=["NAME", "SAL", "PROJ", "OWN", "PT/$"])
    sig = detect_vendor(_norm(sin))
    assert sig is not None and sig["name"] == "Ship It Nation MMA"
    # The simple PGA signature (has CEIL) must still win for a golf file, not Ship It MMA.
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


if __name__ == "__main__":
    test_dailyfan_mma_new_format_detected()
    test_ship_it_mma_detected_and_no_pga_collision()
    test_dailyfan_mma_cpt_flex_detected()
    test_drop_junk_rows()
    print("4 passed")
