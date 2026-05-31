"""SaberSim lineup-pool ingestion + build-rules store (per-sport/slate).

SaberSim builds and simulates ~5,000 lineups for the slate's contests and
exports them with sim metrics (Proj, Own Sum, Sim ROI %, Cash %, Top 1%,
Win %, Avg Payout). We ingest that pool to review exposures + top lineups,
and we persist a compact summary that Claude reads when writing the slate
analysis. The other half of the loop is the build-rules markdown: Claude
writes the constraints (exposure caps/floors, must-plays, fades, ceiling /
ownership targets) that the user types back into SaberSim.

Persistence (dir data/sabersim/):
  <slug>_lineups.csv   — normalized lineup pool (players joined by " | ")
  <slug>_summary.json  — compact summary for display + Claude
  <slug>_rules.md      — build rules to enter into SaberSim
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

_SABERSIM_DIR = Path(__file__).parent.parent / "data" / "sabersim"

_PLAYERS_SEP = " | "

# Canonical metric -> candidate header names (matched case/space-insensitively,
# both as exact normalized keys and as substrings). Order = match priority.
_METRIC_SYNONYMS: dict[str, list[str]] = {
    "salary":     ["salary", "sal"],
    "proj":       ["proj", "projection", "projected", "fpts", "points"],
    "own_sum":    ["own sum", "ownership sum", "sum own", "total own", "ownsum"],
    "own":        ["own", "ownership", "proj own", "pown"],
    "sim_roi":    ["sim roi %", "sim roi", "roi %", "roi percent", "roi"],
    "cash_pct":   ["cash %", "cash percent", "cash"],
    "top1_pct":   ["top 1%", "top 1 %", "top 1", "top1", "top 1 percent"],
    "win_pct":    ["win %", "win percent", "win"],
    "avg_payout": ["avg payout", "average payout", "payout"],
}
# Meta (non-metric) columns we also surface.
_META_SYNONYMS: dict[str, list[str]] = {
    "build":     ["build", "build name"],
    "lineup_id": ["lineup id", "lineup", "id"],
}
_PLAYERS_SYNONYMS = ["players", "roster", "lineup players"]

# Metrics that are numeric and get distribution + exposure stats.
_NUMERIC = ["salary", "proj", "own_sum", "own", "sim_roi", "cash_pct", "win_pct", "top1_pct", "avg_payout"]
# Preferred ranking metrics for the "top lineups" view (in priority order).
_RANK_METRICS = ["top1_pct", "win_pct", "sim_roi", "proj"]


def _norm(s: str) -> str:
    return " ".join(str(s).strip().lower().replace("%", " %").split())


def _to_num(val):
    if val is None:
        return None
    s = str(val).strip().replace("$", "").replace(",", "").replace("%", "")
    if s == "" or s.lower() == "nan":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _match_column(columns: list[str], candidates: list[str]) -> str | None:
    """Return the first original column matching any candidate (exact normalized,
    then substring)."""
    norm_map = {_norm(c): c for c in columns}
    for cand in candidates:
        if cand in norm_map:
            return norm_map[cand]
    for cand in candidates:
        for ncol, orig in norm_map.items():
            if cand in ncol:
                return orig
    return None


def parse_sabersim_lineups(csv_path_or_buffer) -> tuple[pd.DataFrame, dict]:
    """Read a SaberSim lineup export. Returns (normalized_df, meta).

    Column-flexible: detects a comma-separated players column (preferred) or
    per-position player columns, plus sim-metric columns by fuzzy header match.
    The normalized df has a `players` column of list[str] plus whichever
    canonical metric/meta columns were detected.
    """
    raw = pd.read_csv(csv_path_or_buffer)
    raw.columns = [str(c).strip() for c in raw.columns]
    cols = list(raw.columns)

    detected: dict[str, str] = {}
    for canon, cands in {**_META_SYNONYMS, **_METRIC_SYNONYMS}.items():
        hit = _match_column(cols, cands)
        if hit is not None and hit not in detected.values():
            detected[canon] = hit

    # --- players: prefer a single comma-separated column ---
    players_source = "none"
    players_col = _match_column(cols, _PLAYERS_SYNONYMS)
    # Guard: don't mistake the "lineup id" column for the players column.
    if players_col is not None and players_col == detected.get("lineup_id"):
        players_col = None
    players_lists: list[list[str]] = []
    if players_col is not None:
        players_source = "players_column"
        for v in raw[players_col].fillna(""):
            names = [p.strip() for p in str(v).split(",") if p.strip()]
            players_lists.append(names)
    else:
        # Fallback: per-position columns (values like "Name" or "Name (12345)").
        # Roster columns = those not claimed as meta/metric and that look like names.
        claimed = set(detected.values())
        slot_cols = [c for c in cols if c not in claimed]
        import re as _re
        def _looks_like_name(x: str) -> bool:
            x = str(x).strip()
            return bool(x) and any(ch.isalpha() for ch in x)
        slot_cols = [c for c in slot_cols if raw[c].map(_looks_like_name).mean() > 0.8]
        if slot_cols:
            players_source = "position_columns"
            _id = _re.compile(r"\s*\(\d+\)\s*$")
            for _, row in raw[slot_cols].iterrows():
                names = [_id.sub("", str(row[c]).strip()) for c in slot_cols if str(row[c]).strip()]
                players_lists.append([n for n in names if n])
        else:
            players_lists = [[] for _ in range(len(raw))]

    out = pd.DataFrame()
    out["players"] = players_lists
    for canon, orig in detected.items():
        if canon in _NUMERIC:
            out[canon] = raw[orig].map(_to_num)
        else:
            out[canon] = raw[orig].astype(str).str.strip()

    claimed_all = set(detected.values()) | ({players_col} if players_col else set())
    meta = {
        "n_lineups": int(len(out)),
        "detected": detected,
        "players_source": players_source,
        "players_column": players_col,
        "unmatched_columns": [c for c in cols if c not in claimed_all],
    }
    return out, meta


def summarize_pool(df: pd.DataFrame) -> dict:
    """Compact, JSON-serializable summary: distributions, player exposure, and
    top lineups by each available ranking metric. This is what Claude reads."""
    n = int(len(df))
    summary: dict = {"n_lineups": n, "distributions": {}, "exposure": [], "top_lineups": {}}
    if n == 0:
        return summary

    for m in _NUMERIC:
        if m in df.columns and df[m].notna().any():
            s = df[m].dropna()
            summary["distributions"][m] = {
                "min": round(float(s.min()), 2),
                "median": round(float(s.median()), 2),
                "max": round(float(s.max()), 2),
                "mean": round(float(s.mean()), 2),
            }

    # Player exposure across the pool.
    exploded = df.explode("players")
    exploded = exploded[exploded["players"].astype(bool)]
    if not exploded.empty:
        rows = []
        for player, grp in exploded.groupby("players"):
            row = {
                "player": player,
                "count": int(len(grp)),
                "exposure_pct": round(100 * len(grp) / n, 1),
            }
            if "top1_pct" in grp.columns and grp["top1_pct"].notna().any():
                row["avg_top1_pct"] = round(float(grp["top1_pct"].mean()), 2)
            if "sim_roi" in grp.columns and grp["sim_roi"].notna().any():
                row["avg_sim_roi"] = round(float(grp["sim_roi"].mean()), 1)
            rows.append(row)
        summary["exposure"] = sorted(rows, key=lambda r: r["count"], reverse=True)

    # Top lineups by each available ranking metric.
    keep = [c for c in ["players", "salary", "proj", "own_sum", "sim_roi", "cash_pct", "top1_pct", "win_pct", "avg_payout"] if c in df.columns]
    for m in _RANK_METRICS:
        if m in df.columns and df[m].notna().any():
            top = df.nlargest(25, m)[keep].copy()
            top["players"] = top["players"].map(lambda lst: ", ".join(lst) if isinstance(lst, list) else lst)
            summary["top_lineups"][m] = top.to_dict(orient="records")
    return summary


def _path(slug: str, suffix: str) -> Path:
    return _SABERSIM_DIR / f"{slug}_{suffix}"


def save_pool(slug: str, df: pd.DataFrame, meta: dict) -> None:
    _SABERSIM_DIR.mkdir(parents=True, exist_ok=True)
    disk = df.copy()
    disk["players"] = disk["players"].map(
        lambda lst: _PLAYERS_SEP.join(lst) if isinstance(lst, list) else (lst or "")
    )
    disk.to_csv(_path(slug, "lineups.csv"), index=False)
    summary = summarize_pool(df)
    summary["meta"] = meta
    _path(slug, "summary.json").write_text(json.dumps(summary, indent=2))


def load_pool(slug: str) -> pd.DataFrame | None:
    p = _path(slug, "lineups.csv")
    if not p.exists():
        return None
    df = pd.read_csv(p)
    if "players" in df.columns:
        df["players"] = df["players"].fillna("").map(
            lambda s: [x for x in str(s).split(_PLAYERS_SEP) if x]
        )
    return df


def load_summary(slug: str) -> dict | None:
    p = _path(slug, "summary.json")
    if not p.exists():
        return None
    return json.loads(p.read_text())


def save_rules(slug: str, markdown: str) -> None:
    _SABERSIM_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug, "rules.md").write_text(markdown)


def load_rules(slug: str) -> dict | None:
    """Return {markdown, mtime} or None."""
    p = _path(slug, "rules.md")
    if not p.exists():
        return None
    return {"markdown": p.read_text(), "mtime": p.stat().st_mtime}


def clear_sabersim(slug: str) -> None:
    for suffix in ("lineups.csv", "summary.json", "rules.md"):
        p = _path(slug, suffix)
        if p.exists():
            p.unlink()
