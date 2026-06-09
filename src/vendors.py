"""
Vendor auto-detection for DFS projection CSVs.

Identifies which vendor produced a CSV based on its column headers, then
normalizes the columns to our canonical schema (name, salary, proj_points,
ownership, plus optional ceiling/tee_time/matchup/etc.).

Confirmed vendor signatures live in VENDOR_SIGNATURES.
"""
from __future__ import annotations

import pandas as pd


# Each signature: vendor name, sport, required headers that prove identity,
# column rename map (vendor -> canonical), and optional columns to drop.
VENDOR_SIGNATURES: list[dict] = [
    {
        "name": "ETR PGA",
        "sport": "golf",
        "required_columns": {"name", "sal", "proj", "ceil", "own"},
        "column_map": {
            "sal": "salary",
            "proj": "proj_points",
            "ceil": "ceiling",
            "own": "ownership",
        },
        "drop_columns": ["pt/$"],
    },
    {
        "name": "Ship It Nation PGA",
        "sport": "golf",
        "required_columns": {
            "golfer", "dk_salary", "dk_points", "dk_ceiling",
            "large_field_own", "make_cut_odds", "round_1_tee_time",
        },
        "column_map": {
            "golfer": "name",
            "dk_salary": "salary",
            "dk_points": "proj_points",
            "dk_ceiling": "ceiling",
            "large_field_own": "ownership",
            "round_1_tee_time": "tee_time",
            "id": "dk_id",
        },
        "drop_columns": [
            "round_2_tee_time", "small_field_own", "dk_value",
            "volatility", "site",
        ],
    },
    {
        "name": "DailyFan NASCAR",
        "sport": "nascar",
        "required_columns": {
            "driver", "salary", "starting_position",
            "dk_proj._points_(mean)", "dk_proj._ownership",
        },
        "column_map": {
            "driver": "name",
            "dk_proj._points_(mean)": "proj_points",
            "dk_proj._ownership": "ownership",
        },
        "drop_columns": [
            "dk_proj._points_per_dollar", "fd_proj._points_(mean)",
        ],
    },
    {
        "name": "DailyFan MMA",
        "sport": "mma",
        "required_columns": {
            "fighter", "matchup", "win_%", "salary_dk",
            "ownership_dk", "projection_dk_(mean)",
            "projection_dk_(win)", "projection_dk_(loss)",
        },
        "column_map": {
            "fighter": "name",
            "salary_dk": "salary",
            "ownership_dk": "ownership",
            "projection_dk_(mean)": "proj_points",
            "projection_dk_(win)": "proj_win",
            "projection_dk_(loss)": "proj_loss",
            "win_%": "win_prob",
            "dk_id": "dk_id",
        },
        "drop_columns": ["win_odds", "finish_odds", "mean_ppd", "win_ppd"],
    },
    {
        # SIN ships MLB as separate hitter + pitcher files with identical
        # headers — this one signature matches both; `pos` tells the rows apart.
        "name": "Ship It Nation MLB",
        "sport": "mlb",
        "required_columns": {"name", "team", "opp", "pos", "h", "salary", "proj", "own"},
        "column_map": {
            "proj": "proj_points",
            "own": "ownership",
            "pos": "position",
            "opp": "opponent",
            "h": "hand",
        },
        "drop_columns": ["#", "slate"],
    },
    {
        # SIN's third MLB file: team-level stack rankings, not player rows.
        "name": "Ship It Nation MLB Stacks",
        "sport": "mlb",
        "kind": "team_stacks",
        "required_columns": {"team", "proj", "own_%", "stack_salary"},
        "column_map": {
            "proj": "stack_proj",
            "own_%": "stack_own",
        },
        "drop_columns": ["#", "slate"],
    },
    {
        "name": "DK PGA RD4 SD",
        "sport": "golf",
        "required_columns": {
            "golfer", "tee_time", "salary", "points",
            "ownership", "current_score", "finish_points",
        },
        "column_map": {
            "golfer": "name",
            "points": "proj_points",
            "id": "dk_id",
        },
        "drop_columns": ["value", "current_score", "finish_points"],
    },
]


def detect_vendor(df: pd.DataFrame) -> dict | None:
    """Return the matching vendor signature (or None if no match).

    Assumes df.columns has already been normalized to lowercase snake_case.
    Picks the signature with the most matched columns (best fit).
    """
    columns = set(df.columns)
    best: dict | None = None
    best_match_count = 0
    for sig in VENDOR_SIGNATURES:
        required = sig["required_columns"]
        if required.issubset(columns) and len(required) > best_match_count:
            best = sig
            best_match_count = len(required)
    return best


def normalize_to_canonical(df: pd.DataFrame, signature: dict) -> pd.DataFrame:
    """Apply rename + drop based on a vendor signature."""
    df = df.copy()
    # Drop unwanted columns first (silently ignore missing)
    for col in signature.get("drop_columns", []):
        if col in df.columns:
            df = df.drop(columns=col)
    # Rename to canonical column names
    rename = {k: v for k, v in signature.get("column_map", {}).items() if k in df.columns}
    df = df.rename(columns=rename)
    return df
