"""
Vendor auto-detection for DFS projection CSVs.

Identifies which vendor produced a CSV based on its column headers, then
normalizes the columns to our canonical schema (name, salary, proj_points,
ownership, plus optional ceiling/tee_time/matchup/etc.).

Confirmed vendor signatures live in VENDOR_SIGNATURES.
"""
from __future__ import annotations

import pandas as pd


# Each signature: vendor name, sport, required headers that prove identity, an
# optional `aliases` map (canonical -> [candidate headers], first present wins —
# for vendors that ship several headers for the same field), a column rename map
# (vendor -> canonical), and optional columns to drop.
#
# Keep `required_columns` to the headers a vendor has NEVER renamed, and put the
# volatile ones in `aliases`. A required column that the vendor later renames
# turns into a hard upload failure mid-slate.
VENDOR_SIGNATURES: list[dict] = [
    {
        # Simple PGA export (NAME/SAL/PROJ/CEIL/OWN), attributed to ETR
        # (user-confirmed 7/5/26). Filenames never affect detection.
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
        # ETR's RICH golf export. ETR renamed its projection AND ownership
        # headers twice in July 2026 (DK Points + Small/Large Field Own →
        # Projection + Large Field Own → Proj + Own). This used to be THREE
        # signatures, one per generation, each hard-coupling one projection
        # header to one ownership header — so only the 3 diagonal combos
        # loaded. A sheet that mixed generations (Proj + Small Field Own) hit
        # the worst failure mode available: it DETECTED as ETR PGA and then
        # died on `missing required columns: ['proj_points']`, taking the whole
        # PGA pipeline (strategy, board, contract, grade) with it.
        #
        # Identity now rests only on the headers ETR has never renamed; the
        # volatile ones are resolved by `aliases` below, so any combination
        # loads and the next single rename can't break detection.
        "name": "ETR PGA",
        "sport": "golf",
        "required_columns": {"golfer", "dk_salary", "dk_ceiling", "make_cut_odds"},
        "aliases": {
            # First candidate PRESENT wins. Small field own before large:
            # this tool is scoped to SE/3-Max/5-Max, and mapping Large Field
            # Own was the process bug the Sim repo fixed 7/18/26.
            "proj_points": ["dk_points", "projection", "proj"],
            "ownership": ["small_field_own", "large_field_own", "own"],
        },
        "column_map": {
            "golfer": "name",
            "dk_salary": "salary",
            "dk_ceiling": "ceiling",
            "round_1_tee_time": "tee_time",
            "id": "dk_id",
        },
        "drop_columns": ["round_2_tee_time", "dk_value", "volatility", "site"],
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
        # DailyFan's ~7/2026 MMA rename: Fighter→name, Projection DK (Mean)→
        # projection, DK ID→dfs_id, Projection DK (Win) DROPPED. (Ported from
        # the Sim repo, which absorbed the rename 7/25/26.)
        "name": "DailyFan MMA",
        "sport": "mma",
        "required_columns": {
            "name", "matchup", "win_%", "finish_odds",
            "projection", "projection_dk_(loss)",
        },
        "column_map": {
            "salary": "salary",
            "ownership": "ownership",
            "projection": "proj_points",
            "projection_dk_(loss)": "proj_loss",
            "win_%": "win_prob",
            "dfs_id": "dk_id",
        },
        "drop_columns": ["win_odds", "finish_odds", "mean_ppd", "win_ppd"],
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
    # Ship It Nation signatures removed 7/26/26 — the user dropped the vendor
    # 7/18/26 (mirrors the Sim repo). The SIN filename relabel is gone too:
    # it only created false-positive risk on ETR files.
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
        # driving input for RD4 Showdown selection.
        # KEEP `finish_points` too, and ADD it into proj_points (8/3/26, mirrors
        # the Sim repo — reverses the 8/2 "noise" call): DK's RD4 SD actuals
        # INCLUDE finish-position points, so a projection without them runs
        # structurally low on contenders (top-15 bias +5.27/golfer without FP
        # vs +0.32 with, 8/3 slate). Only `value` is noise.
        "drop_columns": ["value"],
        "add_to_proj": ["finish_points"],
    },
]


def detect_vendor(df: pd.DataFrame, source_name: str | None = None) -> dict | None:
    """Return the matching vendor signature (or None if no match).

    Assumes df.columns has already been normalized to lowercase snake_case.
    Picks the signature with the most matched columns (best fit).
    **Filenames never affect detection** — `source_name` is accepted for
    call-site compatibility only and is ignored. (It once relabeled Ship It
    Nation's identical-schema PGA export; SIN support was removed 7/18/26 when
    the user dropped the vendor, and it must not be re-added.)
    """
    columns = set(df.columns)
    best: dict | None = None
    best_score = (0, 0)
    for sig in VENDOR_SIGNATURES:
        required = sig["required_columns"]
        if not required.issubset(columns):
            continue
        # Tie-break on how many column_map/alias candidates the sheet actually
        # carries, so the MOST SPECIFIC signature wins. Without this, DailyFan
        # MMA (6 required cols, listed first) beat DailyFan MMA (CPT/Flex)
        # (also 6) on every CPT/Flex sheet — whose salary lives in salary_flex,
        # so the old map produced no salary/ownership and the upload failed.
        mapped_present = sum(1 for c in sig.get("column_map", {}) if c in columns)
        mapped_present += sum(
            1 for cands in (sig.get("aliases") or {}).values()
            for c in cands if c in columns
        )
        score = (len(required), mapped_present)
        if score > best_score:
            best = sig
            best_score = score
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
    """Apply alias resolution + rename + drop based on a vendor signature."""
    df = df.copy()
    # Drop unwanted columns first (silently ignore missing)
    for col in signature.get("drop_columns", []):
        if col in df.columns:
            df = df.drop(columns=col)
    # Resolve ALIASES before the plain rename. A vendor that ships several
    # headers for the SAME canonical field — ETR golf has shipped Small AND
    # Large Field Own together, and three different projection headers across
    # July 2026 — would otherwise need one signature per header combination
    # (and a plain rename would collide two columns onto one name). First
    # candidate present wins; the losing candidates are dropped.
    for canonical, candidates in (signature.get("aliases") or {}).items():
        present = [c for c in candidates if c in df.columns]
        if not present:
            continue
        keep, losers = present[0], present[1:]
        if losers:
            df = df.drop(columns=losers)
        if keep != canonical:
            df = df.rename(columns={keep: canonical})
    # Rename to canonical column names
    rename = {k: v for k, v in signature.get("column_map", {}).items() if k in df.columns}
    df = df.rename(columns=rename)
    # Fold declared add-on columns into proj_points (e.g. DK RD4 SD finish
    # points — DK's actuals include them, so a projection without them runs
    # structurally low). Blank cells count as 0; the column is retained.
    for col in signature.get("add_to_proj", []):
        if col in df.columns and "proj_points" in df.columns:
            df["proj_points"] = (
                pd.to_numeric(df["proj_points"], errors="coerce")
                + pd.to_numeric(df[col], errors="coerce").fillna(0)
            )
    return df
