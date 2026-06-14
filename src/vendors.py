"""
Vendor auto-detection for DFS projection CSVs.

Identifies which vendor produced a CSV based on its column headers, then
normalizes the columns to our canonical schema (name, salary, proj_points,
ownership, plus optional ceiling/tee_time/matchup/etc.).

Confirmed vendor signatures live in VENDOR_SIGNATURES.
"""
from __future__ import annotations

import pandas as pd


# Vendors disagree on MLB team naming (ETR: "CHC", SIN: "Cubs"). Map every
# variant to one canonical key so cross-vendor team merges line up.
MLB_TEAM_KEYS = {
    "ARI": "ARI", "AZ": "ARI", "DIAMONDBACKS": "ARI",
    "ATL": "ATL", "BRAVES": "ATL",
    "BAL": "BAL", "ORIOLES": "BAL",
    "BOS": "BOS", "RED SOX": "BOS",
    "CHC": "CHC", "CUBS": "CHC",
    "CWS": "CWS", "CHW": "CWS", "WHITE SOX": "CWS",
    "CIN": "CIN", "REDS": "CIN",
    "CLE": "CLE", "GUARDIANS": "CLE",
    "COL": "COL", "ROCKIES": "COL",
    "DET": "DET", "TIGERS": "DET",
    "HOU": "HOU", "ASTROS": "HOU",
    "KC": "KC", "KCR": "KC", "ROYALS": "KC",
    "LAA": "LAA", "ANGELS": "LAA",
    "LAD": "LAD", "DODGERS": "LAD",
    "MIA": "MIA", "MARLINS": "MIA",
    "MIL": "MIL", "BREWERS": "MIL",
    "MIN": "MIN", "TWINS": "MIN",
    "NYM": "NYM", "METS": "NYM",
    "NYY": "NYY", "YANKEES": "NYY",
    "ATH": "ATH", "OAK": "ATH", "ATHLETICS": "ATH", "A'S": "ATH",
    "PHI": "PHI", "PHILLIES": "PHI",
    "PIT": "PIT", "PIRATES": "PIT",
    "SD": "SD", "SDP": "SD", "PADRES": "SD",
    "SEA": "SEA", "MARINERS": "SEA",
    "SF": "SF", "SFG": "SF", "GIANTS": "SF",
    "STL": "STL", "CARDINALS": "STL",
    "TB": "TB", "TBR": "TB", "RAYS": "TB",
    "TEX": "TEX", "RANGERS": "TEX",
    "TOR": "TOR", "BLUE JAYS": "TOR",
    "WSH": "WSH", "WAS": "WSH", "NATIONALS": "WSH",
}


def mlb_team_key(team) -> str:
    s = str(team).strip()
    return MLB_TEAM_KEYS.get(s.upper(), s)


# Each signature: vendor name, sport, required headers that prove identity,
# column rename map (vendor -> canonical), and optional columns to drop.
VENDOR_SIGNATURES: list[dict] = [
    {
        # Vendor unverified — the user labels projection sources going forward.
        "name": "PGA Simple (unconfirmed vendor)",
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
        # SIN's hitter + pitcher rankings files (identical headers; `pos` tells
        # the rows apart). These are RANKINGS — slate context, not the player
        # pool — so they route to articles/<slug>/, not the projections session.
        "name": "Ship It Nation MLB Rankings",
        "sport": "mlb",
        "kind": "rankings",
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
        # SIN's single-file MLB projections export (distinct from their
        # hitter/pitcher rankings pair below — different headers, team
        # abbreviations instead of nicknames). No ceiling column — stddev
        # falls back to 30% of projection.
        "name": "Ship It Nation MLB Projections",
        "sport": "mlb",
        "required_columns": {"name", "tm", "opp", "pos", "sal", "proj", "own"},
        "column_map": {
            "sal": "salary",
            "proj": "proj_points",
            "own": "ownership",
            "tm": "team",
            "opp": "opponent",
            "pos": "position",
        },
        "drop_columns": ["pt/$", "slate"],
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
        # SaberSim's DK projections export — full player pool, hitters +
        # pitchers together. Ships a real stddev (dk_std) and DK player id
        # (DFS ID), unlike the SIN pool. User's mapping: SS Proj -> proj_points,
        # My Own -> ownership (Adj Own is the user's exposure target, left as a
        # passthrough column). Coexists with the SIN pool for cross-vendor diff.
        "name": "SaberSim MLB Projections",
        "sport": "mlb",
        # Distinctive header set — none appear in the SIN signatures, so there
        # is no false-match either direction.
        "required_columns": {
            "dfs_id", "ss_proj", "saber_total", "dk_points", "dk_std", "my_own",
        },
        "column_map": {
            "ss_proj": "proj_points",
            "my_own": "ownership",
            "opp": "opponent",
            "pos": "position",
            "dfs_id": "dk_id",
            "dk_std": "stddev",
            "dk_95_percentile": "ceiling",
        },
        "drop_columns": [
            # other-site noise — keep the session lean (DK-only slate)
            "fd_points", "fd_std", "yahoo_points", "yahoo_std",
            "ob_points", "ob_std", "actual", "live_proj", "value",
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
