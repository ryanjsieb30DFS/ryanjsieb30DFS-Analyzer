"""DK player-ID mapping: attach DraftKings player IDs to the slate's projections.

Some vendor projection exports ship DK IDs (ETR PGA, DK RD4 SD, DailyFan MMA,
SaberSim MLB); others don't (DailyFan NASCAR, Ship It Nation MLB). When they
don't, the user uploads a DraftKings DKEntries/DKSalaries CSV here and we match
its Name↔ID rows onto the projection session by player name, so the pool's
rows can be resolved to players and the Analyze tab's **Select lineups**
feature un-gates (it requires the projections to carry `dk_id`).

The parser + name-matching helpers are ported from the retired src/sabersim.py
(removed in 88b47f4). Persistence is a single per-slug map at
data/dk_ids/<slug>.csv so the mapping survives reruns and re-attaches when
projections are (re-)uploaded.
"""
from __future__ import annotations

import csv
import io
import unicodedata
from pathlib import Path

import pandas as pd

from src import sessions

_DK_IDS_DIR = Path(__file__).parent.parent / "data" / "dk_ids"

_NAME_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


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


def _norm_name(s) -> str:
    """Normalize a player name for fuzzy matching: strip accents/punctuation,
    lowercase, drop generational suffixes."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = "".join(ch if (ch.isalnum() or ch == " ") else " " for ch in s.lower())
    toks = [t for t in s.split() if t and t not in _NAME_SUFFIXES]
    return " ".join(toks)


def _clean_id(val) -> str:
    """DK IDs as a digits-only string (JSON round-trips ints as floats)."""
    s = str(val).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s


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
            "dk_id": _clean_id(idv),
            "salary": _to_num(_cell(row, sal_col)),
            "roster_position": _cell(row, rost_col),
            "team": _cell(row, team_col),
        })
    return pd.DataFrame(rows)


def _build_name_index(dkid_df: pd.DataFrame) -> tuple[dict, dict]:
    """Return (exact_map, norm_map) from a DK-ID DataFrame: name→dk_id."""
    exact, norm = {}, {}
    for _, row in dkid_df.iterrows():
        exact[str(row["name"]).strip()] = _clean_id(row["dk_id"])
        norm.setdefault(_norm_name(row["name"]), _clean_id(row["dk_id"]))
    return exact, norm


def _match_name(name: str, exact_map: dict, norm_map: dict):
    """Resolve a projection player name to a DK id (exact, then normalized)."""
    s = str(name).strip()
    if s in exact_map:
        return exact_map[s]
    return norm_map.get(_norm_name(s))


# --------------------------------------------------------------------------- #
# Persistence
# --------------------------------------------------------------------------- #
def _path(slug: str) -> Path:
    return _DK_IDS_DIR / f"{slug}.csv"


def save_map(slug: str, df: pd.DataFrame) -> None:
    _DK_IDS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(_path(slug), index=False)


def load_map(slug: str) -> pd.DataFrame | None:
    p = _path(slug)
    if not p.exists():
        return None
    return pd.read_csv(p, dtype={"dk_id": str})


def clear_map(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()


# --------------------------------------------------------------------------- #
# Apply the map to the projection session
# --------------------------------------------------------------------------- #
def apply_to_sessions(slug: str, dkid_df: pd.DataFrame) -> dict:
    """Attach a `dk_id` column to every projection source by name match and
    re-save it. Returns match stats: {matched, total, unmatched, per_source}.

    `matched`/`total`/`unmatched` are computed over the union of distinct
    projection player names across all sources (so a name matched in any
    source counts once).
    """
    exact_map, norm_map = _build_name_index(dkid_df)
    per_source: dict[str, dict] = {}
    matched_names: set[str] = set()
    all_names: set[str] = set()

    for name, blob in sessions.load_sources(slug).items():
        df = blob["df"]
        vendor = blob["vendor"]
        if df.empty or "name" not in df.columns:
            continue
        ids = []
        s_matched = 0
        for nm in df["name"]:
            all_names.add(str(nm).strip())
            dk_id = _match_name(nm, exact_map, norm_map)
            if dk_id is not None:
                ids.append(dk_id)
                s_matched += 1
                matched_names.add(str(nm).strip())
            else:
                ids.append(None)
        df = df.copy()
        df["dk_id"] = ids
        sessions.save_source(slug, name, df, vendor)
        per_source[name] = {"matched": s_matched, "total": int(len(df))}

    unmatched = sorted(n for n in all_names if n not in matched_names)
    return {
        "matched": len(matched_names),
        "total": len(all_names),
        "unmatched": unmatched,
        "per_source": per_source,
    }


def projections_id_count(slug: str) -> int:
    """How many distinct projection player names currently carry a dk_id."""
    names: set[str] = set()
    for blob in sessions.load_sources(slug).values():
        df = blob["df"]
        if df.empty or "name" not in df.columns or "dk_id" not in df.columns:
            continue
        for _, r in df[["name", "dk_id"]].iterrows():
            if pd.isna(r["dk_id"]) or str(r["dk_id"]).strip() in ("", "nan"):
                continue
            names.add(str(r["name"]).strip())
    return len(names)
