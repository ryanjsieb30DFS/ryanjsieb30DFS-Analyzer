"""
Load and validate the player projections CSV.

Required columns (all sports):
  name, salary, proj_points, ownership

Optional sport-specific columns (preserved if present):
  ceiling, make_cut_odds, tee_time                          (PGA)
  matchup, opponent, win_prob, proj_win, proj_loss,
    ko_pct, sub_pct, dec_pct                                (MMA)
  starting_position, dominator_points, fast_laps            (NASCAR)
  dk_id                                                     (all)

Stddev is auto-derived (vendors typically don't provide it):
  - If 'ceiling' is present: stddev = (ceiling - proj_points) / 1.28
  - Otherwise: stddev = 30% of proj_points

Accepts vendor-friendly inputs:
  - Salary as "$14,800" / "14,800" / 14800
  - Ownership as "32%" / 0.32 / 32
"""
from __future__ import annotations

import pandas as pd

from src.vendors import detect_vendor, mlb_team_key, normalize_to_canonical


REQUIRED_COLUMNS = ["name", "salary", "proj_points", "ownership"]

OPTIONAL_FLOAT_COLUMNS = [
    "stddev", "ceiling", "make_cut_odds",
    "win_prob", "proj_win", "proj_loss",
    "ko_pct", "sub_pct", "dec_pct",
    "dominator_points", "fast_laps",
    "team_total",
    # live to-par leaderboard score (e.g. DK PGA RD4 SD "Current Score").
    # Float, NOT int: the int path uses -1 as its NA sentinel, which would
    # wipe every real -1 (one-under) score.
    "current_score",
]
OPTIONAL_INT_COLUMNS = ["starting_position", "dk_id", "matchup", "batting_order"]
OPTIONAL_STR_COLUMNS = ["opponent", "tee_time", "position", "team", "hand"]


def drop_junk_rows(projections: pd.DataFrame) -> pd.DataFrame:
    """Drop vendor junk rows (blank / trailing rows in the CSV): a row with no
    usable name or no projection can't be analyzed and pollutes chalk/leverage
    tiers. DailyFan's MMA export ships exactly such a trailing row (name "nan",
    NaN proj)."""
    if "proj_points" not in projections.columns or "name" not in projections.columns:
        return projections
    name_lower = projections["name"].astype(str).str.strip().str.lower()
    keep = pd.to_numeric(projections["proj_points"], errors="coerce").notna() & ~name_lower.isin(
        ["", "nan", "none"]
    )
    return projections[keep].reset_index(drop=True)


def load_projections(csv_path_or_buffer) -> pd.DataFrame:
    """Read the projections CSV and return a cleaned DataFrame.

    The returned DataFrame has a `.attrs["vendor"]` key set to the detected
    vendor name (or None) so the UI can show what was detected.
    """
    projections = pd.read_csv(csv_path_or_buffer)
    projections = _clean_columns(projections)

    vendor_name: str | None = None
    from src.vendors import detect_vendor_confidence
    _vendor_conf = detect_vendor_confidence(projections)
    signature = detect_vendor(projections)
    if signature is not None:
        # Non-projection files (team stacks, rankings) skip the player
        # schema entirely — normalized and returned with their kind tagged
        # so the UI can route them.
        kind = signature.get("kind")
        if kind is not None:
            out = normalize_to_canonical(projections, signature)
            if kind == "team_stacks":
                for col in ("stack_proj", "stack_own", "stack_salary"):
                    if col in out.columns:
                        out[col] = out[col].apply(_clean_number)
                out["team"] = out["team"].astype(str).str.strip()
            out = out.reset_index(drop=True)
            out.attrs["vendor"] = signature["name"]
            out.attrs["kind"] = kind
            return out
        projections = normalize_to_canonical(projections, signature)
        vendor_name = signature["name"]

    # Vendors occasionally export the same row twice (SIN 6/11: Cole Carrigg).
    # Identical rows are harmless — drop them; validate_projections still
    # rejects same-name rows whose data actually differs.
    projections = projections.drop_duplicates().reset_index(drop=True)

    # Two DIFFERENT players can share a name (6/12: Max Muncy LAD + Max Muncy
    # ATH). Name is the join key app-wide, so suffix the team to keep it unique.
    projections = _disambiguate_duplicate_names(projections)

    validate_projections(projections)
    projections = projections.copy()
    projections["name"] = projections["name"].astype(str).str.strip()

    projections["salary"] = projections["salary"].apply(_clean_salary).astype(int)
    projections["proj_points"] = projections["proj_points"].astype(float)
    projections = drop_junk_rows(projections)
    projections["ownership"] = _normalize_ownership_column(projections["ownership"])

    for col in OPTIONAL_FLOAT_COLUMNS:
        if col in projections.columns:
            projections[col] = projections[col].apply(_clean_number)
    for col in OPTIONAL_INT_COLUMNS:
        if col in projections.columns:
            projections[col] = projections[col].apply(_clean_number)
            projections[col] = projections[col].fillna(-1).astype(int).replace(-1, pd.NA)
    for col in OPTIONAL_STR_COLUMNS:
        if col in projections.columns:
            projections[col] = projections[col].astype(str).str.strip()

    # stddev is derived in one place below (after opponent derivation).

    # Normalize win_prob: accept 0–1 or 0–100, store as 0–1
    if "win_prob" in projections.columns:
        wp = projections["win_prob"]
        if wp.max(skipna=True) is not None and wp.max(skipna=True) > 1.5:
            projections["win_prob"] = wp / 100.0

    # Normalize make_cut_odds same way
    if "make_cut_odds" in projections.columns:
        mco = projections["make_cut_odds"]
        if mco.max(skipna=True) is not None and mco.max(skipna=True) > 1.5:
            projections["make_cut_odds"] = mco / 100.0

    # Derive opponent from matchup if matchup present and opponent missing
    if "matchup" in projections.columns and "opponent" not in projections.columns:
        projections["opponent"] = _derive_opponent_from_matchup(projections)

    # Single source of truth for stddev (ceiling-derived, else 30% of proj).
    projections["stddev"] = _derive_stddev(projections)

    if projections["stddev"].min() < 0:
        raise ValueError("Standard deviation cannot be negative.")

    result = projections.reset_index(drop=True)
    result.attrs["vendor"] = vendor_name
    result.attrs["vendor_confidence"] = _vendor_conf
    return result


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and strip column names; preserve order. Strips the UTF-8 BOM
    some vendor exports prepend to the first header (str.strip won't)."""
    df = df.copy()
    df.columns = [
        c.replace("\ufeff", "").strip().lower().replace(" ", "_") for c in df.columns
    ]
    return df


def _clean_salary(val) -> float:
    if pd.isna(val):
        return 0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace("$", "").replace(",", "").strip()
    return float(s) if s else 0


def _clean_ownership(val) -> float:
    """Strip $/% formatting and parse one ownership value to float. Does NOT
    rescale — column-level rescaling (fraction vs. percent) happens in
    `_normalize_ownership_column` so a lone 1.0 isn't misread as 100%."""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace("%", "").strip()
    if not s:
        return 0.0
    return float(s)


def _derive_stddev(df: pd.DataFrame) -> pd.Series:
    """One place for stddev: use the given column where present, fill gaps from
    ceiling ((ceiling - proj)/1.28), then any remainder with 30% of projection.
    Floored at 0.01. Vendors that ship a real stddev (e.g. SaberSim) keep theirs."""
    if "stddev" in df.columns:
        sd = pd.to_numeric(df["stddev"], errors="coerce")
    else:
        sd = pd.Series(float("nan"), index=df.index, dtype="float64")
    if "ceiling" in df.columns:
        from_ceiling = (df["ceiling"] - df["proj_points"]) / 1.28
        sd = sd.where(sd.notna(), from_ceiling)
    sd = sd.where(sd.notna(), df["proj_points"] * 0.30)
    return sd.clip(lower=0.01)


def _normalize_ownership_column(series: pd.Series) -> pd.Series:
    """Parse + rescale an ownership column to 0–100. Decides fraction vs.
    percent at column scope: if any value > 1.0, treat the whole column as
    percent integers (so a row with 1.0 stays 1%, not 100%)."""
    cleaned = series.apply(_clean_ownership).astype(float)
    if (cleaned > 1.0).any():
        return cleaned
    return cleaned * 100


def _clean_number(val):
    """Strip $/% and commas, parse to float. Returns NaN if blank."""
    if pd.isna(val):
        return float("nan")
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace("$", "").replace("%", "").replace(",", "").strip()
    if not s:
        return float("nan")
    try:
        return float(s)
    except ValueError:
        return float("nan")


def _derive_opponent_from_matchup(projections: pd.DataFrame) -> pd.Series:
    """For each fighter, find the other fighter in their matchup number."""
    opponents = []
    for i, row in projections.iterrows():
        m = row.get("matchup")
        if pd.isna(m):
            opponents.append("")
            continue
        same = projections[(projections["matchup"] == m) & (projections.index != i)]
        opponents.append(same.iloc[0]["name"] if not same.empty else "")
    return pd.Series(opponents, index=projections.index)


def _disambiguate_duplicate_names(projections: pd.DataFrame) -> pd.DataFrame:
    """Suffix the team onto duplicate names that belong to DIFFERENT teams.

    "Max Muncy" (LAD) and "Max Muncy" (ATH) are two real players. Rewrite them
    to "Max Muncy (LAD)" / "Max Muncy (ATH)" using the canonical team key so
    the suffix matches across vendors regardless of team spelling. Groups with
    a missing team or repeated team keys are left alone — validate_projections
    raises on those, since same name + same team really is a vendor error.
    """
    if "name" not in projections.columns or "team" not in projections.columns:
        return projections
    names = projections["name"].astype(str).str.strip()
    dup_mask = names.duplicated(keep=False)
    if not dup_mask.any():
        return projections

    projections = projections.copy()
    for _, idx in names[dup_mask].groupby(names[dup_mask]).groups.items():
        teams = projections.loc[idx, "team"]
        keys = [
            "" if pd.isna(t) or not str(t).strip() else mlb_team_key(t)
            for t in teams
        ]
        if "" in keys or len(set(keys)) != len(keys):
            continue
        projections.loc[idx, "name"] = [
            f"{names[i]} ({k})" for i, k in zip(idx, keys)
        ]
    return projections


def validate_projections(projections: pd.DataFrame) -> None:
    """Raise a helpful error if the CSV is missing columns or has bad values."""
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in projections.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {missing_columns}")

    if projections["name"].duplicated().any():
        duplicates = projections.loc[projections["name"].duplicated(), "name"].tolist()
        raise ValueError(
            f"Duplicate player names with conflicting data: {duplicates} — the same "
            "name appears twice with different values on the same team (or with no "
            "team column to tell them apart); fix the vendor file. Different-team "
            "namesakes are disambiguated automatically."
        )


def warn_missing_for_sport(projections: pd.DataFrame, sport: str | None) -> list[str]:
    """Return warnings about optional columns missing for the given sport."""
    warnings = []
    if sport == "mma":
        if "opponent" not in projections.columns and "matchup" not in projections.columns:
            warnings.append(
                "MMA: 'opponent' / 'matchup' column missing — opponent-stacking constraint cannot be enforced."
            )
        if not all(c in projections.columns for c in ("proj_win", "proj_loss", "win_prob")):
            warnings.append(
                "MMA: bimodal sim disabled — add 'proj_win', 'proj_loss', 'win_prob' for accurate sim."
            )
    if sport == "golf":
        if "tee_time" not in projections.columns:
            warnings.append("PGA: 'tee_time' column missing — wave correlation disabled.")
    if sport == "nascar" and "starting_position" not in projections.columns:
        warnings.append(
            "NASCAR: 'starting_position' column missing — PD floor constraint cannot be enforced."
        )
    if sport == "mlb":
        if "team" not in projections.columns:
            warnings.append("MLB: 'team' column missing — team-stack analysis disabled.")
        if "position" not in projections.columns:
            warnings.append("MLB: 'position' column missing — pitcher/hitter split disabled.")
    return warnings
