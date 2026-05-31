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

import csv
import io
import json
import unicodedata
from pathlib import Path

import pandas as pd

_SABERSIM_DIR = Path(__file__).parent.parent / "data" / "sabersim"

_PLAYERS_SEP = " | "

# Canonical metric -> candidate header names (matched case/space-insensitively,
# both as exact normalized keys and as substrings). Order = match priority.
_METRIC_SYNONYMS: dict[str, list[str]] = {
    "salary":      ["salary", "sal"],
    "proj":        ["proj score", "proj", "projection", "projected", "fpts", "points"],
    "own_sum":     ["own sum", "ownership sum", "sum own", "total own", "ownsum", "ownership", "own"],
    "cash_pct":    ["cash %", "cash rate", "cash percent", "cash"],
    "win_pct":     ["win %", "win rate", "win percent", "win"],
    "top1_pct":    ["top 1%", "top 1 %", "top 1", "top1", "top 1 percent"],
    "optimal_pct": ["sim optimals", "optimals", "optimal %", "optimal"],
    "saber_score": ["saber score", "saberscore"],
    "ceiling":     ["95th", "ceiling", "ceil"],
    "avg_payout":  ["avg payout", "average payout", "payout"],
    # sim_roi is matched specially (must contain "roi" but NOT "stdev"/"dupes").
}
# Meta (non-metric) columns we also surface.
_META_SYNONYMS: dict[str, list[str]] = {
    "build":     ["build", "build name"],
    "lineup_id": ["lineup id", "lineup", "id"],
}
_PLAYERS_SYNONYMS = ["players", "roster", "lineup players"]
# Short position codes that mark a leading roster-block column (DK roster slots).
_POSITION_CODES = {"g", "f", "d", "cpt", "util", "flex", "mvp", "star", "pro"}

# Metrics that are numeric and get distribution + exposure stats.
_NUMERIC = ["salary", "proj", "own_sum", "sim_roi", "cash_pct", "win_pct",
            "top1_pct", "optimal_pct", "saber_score", "ceiling", "avg_payout"]
# Preferred ranking metrics for the "top lineups" view (in priority order).
_RANK_METRICS = ["top1_pct", "win_pct", "sim_roi", "saber_score", "proj"]


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


def _read_grid(csv_path_or_buffer) -> list[list[str]]:
    """Read any CSV into a ragged list-of-rows via the csv module (tolerant of
    SaberSim's duplicate headers + blank separator column that break pandas)."""
    if hasattr(csv_path_or_buffer, "read"):
        data = csv_path_or_buffer.read()
        if isinstance(data, bytes):
            data = data.decode("utf-8-sig", errors="replace")
        return list(csv.reader(io.StringIO(data)))
    with open(csv_path_or_buffer, "r", encoding="utf-8-sig", errors="replace", newline="") as fh:
        return list(csv.reader(fh))


_ID_SUFFIX = None  # compiled lazily


def _strip_id_suffix(s: str) -> str:
    import re
    global _ID_SUFFIX
    if _ID_SUFFIX is None:
        _ID_SUFFIX = re.compile(r"\s*\(\d+\)\s*$")
    return _ID_SUFFIX.sub("", s).strip()


def _detect_metrics(header: list[str], col_indices: list[int]) -> dict[str, int]:
    """Map canonical metric/meta names → column index over the given columns."""
    norm = {j: _norm(header[j]) for j in col_indices}
    detected: dict[str, int] = {}

    def _find(cands: list[str]):
        for cand in cands:  # exact normalized first
            for j in col_indices:
                if norm[j] == cand and j not in detected.values():
                    return j
        for cand in cands:  # then substring
            for j in col_indices:
                if cand in norm[j] and j not in detected.values():
                    return j
        return None

    for canon, cands in {**_META_SYNONYMS, **_METRIC_SYNONYMS}.items():
        j = _find(cands)
        if j is not None:
            detected[canon] = j
    # sim_roi: a column containing "roi" but not stdev/std/dupes.
    if "sim_roi" not in detected:
        for j in col_indices:
            n = norm[j]
            if "roi" in n and not any(bad in n for bad in ("stdev", "std", "dupe")) and j not in detected.values():
                detected["sim_roi"] = j
                break
    return detected


def parse_sabersim_lineups(csv_path_or_buffer) -> tuple[pd.DataFrame, dict]:
    """Read a SaberSim lineup export. Returns (normalized_df, meta).

    Handles two shapes:
      (a) a single comma-separated players/roster column (names), or
      (b) the real SaberSim layout: a leading roster block of position columns
          (holding DK player IDs or names), a blank separator column, then
          sim-metric columns. Roster tokens may be DK IDs — `save_pool` resolves
          them to names via the slate's DK-id map.
    """
    grid = _read_grid(csv_path_or_buffer)
    if not grid:
        return pd.DataFrame({"players": []}), {"n_lineups": 0, "detected": {}, "players_source": "none"}
    header = [c.strip() for c in grid[0]]
    data = grid[1:]
    ncol = len(header)

    def _cell(row: list, j: int) -> str:
        return row[j].strip() if 0 <= j < len(row) else ""

    # --- locate the roster ---
    players_source = "none"
    roster_cols: list[int] = []
    players_col = None

    # (a) single comma-separated players column
    for j in range(ncol):
        if _norm(header[j]) in _PLAYERS_SYNONYMS:
            players_col = j
            break
    if players_col is not None:
        players_source = "players_column"
    else:
        # (b) leading roster block: stop at the first blank-header (separator)
        sep = next((j for j in range(ncol) if header[j] == ""), None)
        if sep is not None and sep > 0:
            roster_cols = list(range(sep))
        else:
            # fallback: maximal leading run of position-code / numeric-id columns
            run = []
            for j in range(ncol):
                h = _norm(header[j])
                col_vals = [_cell(r, j) for r in data[:20] if _cell(r, j)]
                numeric = col_vals and all(v.replace(".", "").isdigit() for v in col_vals)
                if h in _POSITION_CODES or numeric:
                    run.append(j)
                else:
                    break
            roster_cols = run
        if roster_cols:
            players_source = "roster_block"

    # metric region = everything not in the roster / players column
    used = set(roster_cols) | ({players_col} if players_col is not None else set())
    sep_idx = next((j for j in range(ncol) if header[j] == ""), None)
    if sep_idx is not None:
        used.add(sep_idx)
    metric_cols = [j for j in range(ncol) if j not in used]
    detected = _detect_metrics(header, metric_cols)

    # --- build roster token lists ---
    players_lists: list[list[str]] = []
    for row in data:
        if players_col is not None:
            toks = [t.strip() for t in _cell(row, players_col).split(",") if t.strip()]
        else:
            toks = [_strip_id_suffix(_cell(row, j)) for j in roster_cols if _cell(row, j)]
        players_lists.append(toks)

    flat = [t for lst in players_lists for t in lst]
    player_key = "dk_id" if (flat and all(t.replace(".", "").isdigit() for t in flat)) else "name"

    out = pd.DataFrame()
    out["players"] = players_lists
    for canon, j in detected.items():
        if canon in _NUMERIC:
            out[canon] = [_to_num(_cell(r, j)) for r in data]
        else:
            out[canon] = [_cell(r, j) for r in data]

    meta = {
        "n_lineups": int(len(out)),
        "detected": {k: header[j] for k, j in detected.items()},
        "players_source": players_source,
        "player_key": player_key,
        "roster_columns": [header[j] for j in roster_cols],
        "separator_index": sep_idx,
        "unmatched_columns": [header[j] for j in metric_cols if j not in detected.values()],
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


# --------------------------------------------------------------------------- #
# DK player-ID map (resolves SaberSim's name-only players to DK IDs)
# --------------------------------------------------------------------------- #
_NAME_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def _norm_name(s) -> str:
    """Normalize a player name for fuzzy matching: strip accents/punctuation,
    lowercase, drop generational suffixes."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = "".join(ch if (ch.isalnum() or ch == " ") else " " for ch in s.lower())
    toks = [t for t in s.split() if t and t not in _NAME_SUFFIXES]
    return " ".join(toks)


def parse_dk_player_ids(csv_path_or_buffer) -> pd.DataFrame:
    """Parse a DraftKings DKEntries/DKSalaries CSV into name↔DK-ID rows.

    Locates the player-pool sub-table by finding the `Name + ID` header cell
    (the DKEntries layout offsets it to the right and partway down; a plain
    DKSalaries puts it on row 0). Returns columns: name, dk_id, salary,
    roster_position, team.
    """
    # DK's DKEntries CSV is ragged (the entry-template rows are narrower than
    # the player-pool sub-table), which breaks pandas — read with csv instead.
    if hasattr(csv_path_or_buffer, "read"):
        data = csv_path_or_buffer.read()
        if isinstance(data, bytes):
            data = data.decode("utf-8-sig", errors="replace")
        grid = list(csv.reader(io.StringIO(data)))
    else:
        with open(csv_path_or_buffer, "r", encoding="utf-8-sig", errors="replace", newline="") as fh:
            grid = list(csv.reader(fh))

    hr = None
    for r, row in enumerate(grid):
        if any(cell.strip() == "Name + ID" for cell in row):
            hr = r
            break
    if hr is None:
        raise ValueError("Could not find a 'Name + ID' player-pool header in this CSV.")

    header: dict[str, int] = {}
    for j, cell in enumerate(grid[hr]):
        lab = cell.strip()
        if lab and lab not in header:
            header[lab] = j
    name_col, id_col = header.get("Name"), header.get("ID")
    if name_col is None or id_col is None:
        raise ValueError("DK player-pool header is missing a 'Name' or 'ID' column.")
    sal_col, rost_col, team_col = header.get("Salary"), header.get("Roster Position"), header.get("TeamAbbrev")

    def _cell(row: list, j) -> str:
        return row[j].strip() if (j is not None and j < len(row)) else ""

    rows = []
    for row in grid[hr + 1:]:
        nm, idv = _cell(row, name_col), _cell(row, id_col)
        if not nm or not idv:
            continue
        rows.append({
            "name": nm,
            "dk_id": idv,
            "salary": _to_num(_cell(row, sal_col)),
            "roster_position": _cell(row, rost_col),
            "team": _cell(row, team_col),
        })
    return pd.DataFrame(rows)


def _build_name_index(dkid_df: pd.DataFrame) -> tuple[dict, dict]:
    """Return (exact_map, norm_map) from a DK-ID DataFrame: name→dk_id."""
    exact, norm = {}, {}
    for _, row in dkid_df.iterrows():
        exact[str(row["name"]).strip()] = row["dk_id"]
        norm.setdefault(_norm_name(row["name"]), row["dk_id"])
    return exact, norm


def _match_name(name: str, exact_map: dict, norm_map: dict):
    """Resolve a SaberSim player name to a DK id (exact, then normalized)."""
    s = str(name).strip()
    if s in exact_map:
        return exact_map[s]
    return norm_map.get(_norm_name(s))


def annotate_summary_with_dkids(summary: dict, dkid_df: pd.DataFrame) -> dict:
    """Add dk_id to each exposure row and attach dk_id_map / unmatched_players /
    dk_id_match to the summary, so the tab + Claude reference exact DK players."""
    exact_map, norm_map = _build_name_index(dkid_df)
    id_map, unmatched = {}, []
    for row in summary.get("exposure", []):
        player = row.get("player")
        dk_id = _match_name(player, exact_map, norm_map)
        row["dk_id"] = dk_id
        if dk_id is not None:
            id_map[player] = dk_id
        else:
            unmatched.append(player)
    total = len(summary.get("exposure", []))
    summary["dk_id_map"] = id_map
    summary["unmatched_players"] = unmatched
    summary["dk_id_match"] = {"matched": len(id_map), "total": total}
    return summary


def save_dk_ids(slug: str, df: pd.DataFrame) -> None:
    _SABERSIM_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(_path(slug, "dkids.csv"), index=False)


def load_dk_ids(slug: str) -> pd.DataFrame | None:
    p = _path(slug, "dkids.csv")
    if not p.exists():
        return None
    return pd.read_csv(p, dtype={"dk_id": str})


def dk_ids_from_projections(slug: str) -> pd.DataFrame | None:
    """Derive a name↔DK-ID map from the active projections session, if those
    projections already carry `dk_id` (e.g. ETR / DK RD4 SD exports)."""
    from src import sessions  # local import to avoid any import-order coupling
    rows = []
    for src in sessions.load_sources(slug).values():
        df = src.get("df")
        if df is None or "name" not in df.columns or "dk_id" not in df.columns:
            continue
        for _, r in df[["name", "dk_id"]].iterrows():
            if pd.isna(r["dk_id"]) or not str(r["name"]).strip():
                continue
            idv = str(r["dk_id"]).strip()
            if idv.endswith(".0"):  # int stored as float in JSON round-trip
                idv = idv[:-2]
            rows.append({"name": str(r["name"]).strip(), "dk_id": idv})
    if not rows:
        return None
    return pd.DataFrame(rows).drop_duplicates(subset=["name"])


def resolve_dk_id_map(slug: str) -> tuple[pd.DataFrame | None, str]:
    """Best available name↔DK-ID map for the join. Uploaded file overrides
    projection-derived IDs. Returns (df_or_None, source)."""
    uploaded = load_dk_ids(slug)
    if uploaded is not None and not uploaded.empty:
        return uploaded, "uploaded"
    proj = dk_ids_from_projections(slug)
    if proj is not None and not proj.empty:
        return proj, "projections"
    return None, "none"


def refresh_summary_with_dkids(slug: str) -> None:
    """Re-annotate an existing pool summary with the best available DK-id map
    (uploaded file, else projection-derived). Used when the DK-id file or
    projections change after the SaberSim pool was loaded."""
    summary = load_summary(slug)
    if summary is None:
        return
    dkids, source = resolve_dk_id_map(slug)
    if dkids is None or dkids.empty:
        return
    summary = annotate_summary_with_dkids(summary, dkids)
    summary["dk_id_source"] = source
    _path(slug, "summary.json").write_text(json.dumps(summary, indent=2))


def _path(slug: str, suffix: str) -> Path:
    return _SABERSIM_DIR / f"{slug}_{suffix}"


def save_pool(slug: str, df: pd.DataFrame, meta: dict) -> None:
    _SABERSIM_DIR.mkdir(parents=True, exist_ok=True)
    df = df.copy()

    # Real SaberSim exports carry the roster as DK player IDs. Resolve them to
    # names via the slate's DK-id map so exposure/top-lineups read as players.
    if meta.get("player_key") == "dk_id":
        dkids, _src = resolve_dk_id_map(slug)
        id2name = {}
        if dkids is not None and not dkids.empty:
            id2name = {str(r["dk_id"]).strip(): str(r["name"]).strip() for _, r in dkids.iterrows()}
        unresolved = set()

        def _resolve(lst):
            out = []
            for tok in (lst if isinstance(lst, list) else []):
                name = id2name.get(str(tok).strip())
                if name:
                    out.append(name)
                else:
                    out.append(tok)
                    unresolved.add(tok)
            return out

        df["players"] = df["players"].map(_resolve)
        meta = {**meta, "unresolved_ids": sorted(unresolved)}

    disk = df.copy()
    disk["players"] = disk["players"].map(
        lambda lst: _PLAYERS_SEP.join(lst) if isinstance(lst, list) else (lst or "")
    )
    disk.to_csv(_path(slug, "lineups.csv"), index=False)
    summary = summarize_pool(df)
    summary["meta"] = meta
    # Annotate with the best available DK-id map (uploaded file, else the
    # projections' own dk_id) so Claude's summary.json carries exact DK IDs.
    dkids, source = resolve_dk_id_map(slug)
    if dkids is not None and not dkids.empty:
        summary = annotate_summary_with_dkids(summary, dkids)
        summary["dk_id_source"] = source
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
    for suffix in ("lineups.csv", "summary.json", "rules.md", "dkids.csv"):
        p = _path(slug, suffix)
        if p.exists():
            p.unlink()
