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
        # Vendor unverified — the user labels projection sources going forward.
        # Simple PGA export (NAME/SAL/PROJ/CEIL/OWN). Default attribution is ETR
        # (user-confirmed 7/5/26); SIN ships the same shape for Showdowns — the
        # filename hint below relabels those.
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
        # ETR renamed "DK Points" -> "Proj" in June 2026; both map to
        # proj_points and neither is required so old and new exports match.
        "name": "ETR PGA",
        "sport": "golf",
        "required_columns": {
            "golfer", "dk_salary", "dk_ceiling",
            "large_field_own", "make_cut_odds", "round_1_tee_time",
        },
        "column_map": {
            "golfer": "name",
            "dk_salary": "salary",
            "dk_points": "proj_points",
            "proj": "proj_points",
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
        # Identify on the STABLE distinctive columns. DailyFan renamed
        # "Salary DK"/"Ownership DK" -> "Salary"/"Ownership" (6/2026), so those are
        # mapped-if-present (below) not required — keeps both old + new formats working.
        "required_columns": {
            "fighter", "matchup", "win_%", "projection_dk_(mean)",
            "projection_dk_(win)", "projection_dk_(loss)",
        },
        "column_map": {
            "fighter": "name",
            "salary_dk": "salary",          # old format (mapped if present)
            "ownership_dk": "ownership",     # old format (mapped if present)
            "projection_dk_(mean)": "proj_points",
            "projection_dk_(win)": "proj_win",
            "projection_dk_(loss)": "proj_loss",
            "win_%": "win_prob",
            "dk_id": "dk_id",
        },
        "drop_columns": ["win_odds", "finish_odds", "mean_ppd", "win_ppd"],
    },
    {
        # Ship It Nation MMA simple export: NAME, SAL, PROJ, OWN, PT/$ (no ceiling,
        # so it won't collide with the simple PGA format which requires `ceil`).
        "name": "Ship It Nation MMA",
        "sport": "mma",
        "required_columns": {"name", "sal", "proj", "own"},
        "column_map": {
            "sal": "salary",
            "proj": "proj_points",
            "own": "ownership",
        },
        "drop_columns": ["pt/$"],
    },
    {
        # DailyFan's newer MMA sheet adds Captain/Flex pricing (Salary CPT/Flex,
        # Ownership CPT/Flex/Total, DK ID CPT/Flex) — distinct from the older flat
        # "salary_dk" sheet above. Map the FLEX columns (the flat-contest pricing;
        # CPT is the 1.5x captain price). CPT columns pass through untouched so
        # captain-mode ("special event") data survives if a build needs it.
        "name": "DailyFan MMA (CPT/Flex)",
        "sport": "mma",
        "required_columns": {
            "fighter", "matchup", "win_%", "salary_flex",
            "ownership_total", "projection_dk_(mean)",
        },
        "column_map": {
            "fighter": "name",
            "salary_flex": "salary",
            "ownership_total": "ownership",
            "projection_dk_(mean)": "proj_points",
            "projection_dk_(win)": "proj_win",
            "projection_dk_(loss)": "proj_loss",
            "win_%": "win_prob",
            "dk_id_flex": "dk_id",
        },
        "drop_columns": [
            "win_odds", "finish_odds", "mean_ppd_(flex)", "win_ppd_(flex)",
        ],
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
        # Keep `current_score` — it's the live to-par leaderboard position, THE
        # driving input for RD4 Showdown selection. `value`/`finish_points` are noise.
        "drop_columns": ["value", "finish_points"],
    },
]


def _filename_hints_sin(source_name: str | None) -> bool:
    """True when a filename clearly indicates Ship It Nation ('SIN' as a word
    token, or 'ship'). Word-boundary match so e.g. 'wisconsin' never triggers."""
    if not source_name:
        return False
    import re as _re
    low = source_name.lower()
    return bool(_re.search(r"\bsin\b", low)) or "ship" in low


def detect_vendor(df: pd.DataFrame, source_name: str | None = None) -> dict | None:
    """Return the matching vendor signature (or None if no match).

    Assumes df.columns has already been normalized to lowercase snake_case.
    Picks the signature with the most matched columns (best fit).

    `source_name` (the uploaded filename) disambiguates schema COLLISIONS:
    Ship It Nation's simple PGA export (e.g. their Showdown file) ships the
    exact same headers as ETR PGA (NAME, SAL, PROJ, CEIL, OWN, PT/$) — when
    that signature matches and the filename says SIN, relabel to
    'Ship It Nation PGA (simple)' so blend-source and vendor-accuracy
    attribution stay honest.
    """
    columns = set(df.columns)
    best: dict | None = None
    best_score = (0, 0)
    for sig in VENDOR_SIGNATURES:
        required = sig["required_columns"]
        if not required.issubset(columns):
            continue
        # Tie-break on how many column_map keys the sheet actually carries, so
        # the MOST SPECIFIC signature wins. Without this, DailyFan MMA (6
        # required cols, listed first) beat DailyFan MMA (CPT/Flex) (also 6)
        # on every CPT/Flex sheet — whose salary lives in salary_flex, so the
        # old map produced no salary/ownership and the upload always failed.
        mapped_present = sum(1 for c in sig.get("column_map", {}) if c in columns)
        score = (len(required), mapped_present)
        if score > best_score:
            best = sig
            best_score = score
    if (best is not None
            and best["name"] == "ETR PGA"
            and _filename_hints_sin(source_name)):
        best = dict(best, name="Ship It Nation PGA (simple)")
    return best


def detect_vendor_confidence(df: pd.DataFrame) -> dict:
    """Diagnostic companion to detect_vendor — surfaces WHY a match is shaky so a
    changed vendor header isn't a silent misdetect. Returns:
      matched      — vendor names whose required columns are fully present
      ambiguous    — True if 2+ signatures tie at the top required-column count
      near_misses  — [(vendor, [missing_col]), ...] for signatures missing exactly
                     one required column (a likely renamed header)
    """
    columns = set(df.columns)
    full = [(sig["name"], len(sig["required_columns"]))
            for sig in VENDOR_SIGNATURES if sig["required_columns"].issubset(columns)]
    near = [(sig["name"], sorted(sig["required_columns"] - columns))
            for sig in VENDOR_SIGNATURES
            if len(sig["required_columns"] - columns) == 1]
    ambiguous = False
    if full:
        top = max(c for _, c in full)
        ambiguous = sum(1 for _, c in full if c == top) > 1
    return {
        "matched": [v for v, _ in sorted(full, key=lambda x: -x[1])],
        "ambiguous": ambiguous,
        "near_misses": near[:5],
    }


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
