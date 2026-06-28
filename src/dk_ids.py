"""Resolve DraftKings player IDs -> player names for the Sim Data tab.

A SaberSim lineup-pool export keys each roster slot by DK player ID, not name. To
show readable analytics we map id -> name from two sources, in priority order:
  1. the loaded vendor projections, when they carry a `dk_id` column; then
  2. a DK "Name + ID" file the user uploads (the standard DKSalaries player-pool
     export, or the DK entries template — both carry `Name`/`ID` or a combined
     "Name + ID" column).
Unmatched ids fall back to the raw id string so nothing silently disappears.
"""
from __future__ import annotations

import re

import pandas as pd

from src.autopsy import _norm_name
from src.sessions import load_sources

# "Player Name (12345678)" — DK's combined "Name + ID" column.
_NAME_ID_RE = re.compile(r"^\s*(.*?)\s*\((\d{3,})\)\s*$")


def fmt_id(did) -> str:
    """DK ids are integers; render without a trailing '.0' from float parsing."""
    if isinstance(did, float) and did.is_integer():
        return str(int(did))
    s = str(did).strip()
    return s[:-2] if s.endswith(".0") and s[:-2].isdigit() else s


def parse_id_to_name(file_or_buffer) -> dict[str, str]:
    """{dk_id -> display name} from a DK salaries/entries CSV. {} if unparseable.

    Prefers explicit `Name` + `ID` columns; falls back to a combined "Name + ID"
    column ("Player (12345678)")."""
    try:
        df = pd.read_csv(file_or_buffer)
    except Exception:  # noqa: BLE001 — a bad upload should not crash the tab
        return {}
    cols = {str(c).strip().lower(): c for c in df.columns}
    out: dict[str, str] = {}

    name_col, id_col = cols.get("name"), cols.get("id")
    if name_col is not None and id_col is not None:
        for nm, did in zip(df[name_col], df[id_col]):
            if pd.isna(nm) or pd.isna(did):
                continue
            out[fmt_id(did)] = str(nm).strip()
        if out:
            return out

    combo_col = cols.get("name + id") or cols.get("name+id")
    if combo_col is not None:
        for val in df[combo_col]:
            m = _NAME_ID_RE.match(str(val))
            if m:
                out[m.group(2)] = m.group(1).strip()
    return out


def id_to_name_from_projections(slug: str) -> dict[str, str]:
    """{dk_id -> name} from loaded projections that carry a `dk_id` column."""
    out: dict[str, str] = {}
    for blob in load_sources(slug).values():
        df = blob.get("df")
        if df is None or df.empty or "dk_id" not in df.columns or "name" not in df.columns:
            continue
        for nm, did in zip(df["name"], df["dk_id"]):
            if pd.isna(did) or pd.isna(nm):
                continue
            out[fmt_id(did)] = str(nm).strip()
    return out


def resolve_id_to_name(slug: str, uploaded_map: dict[str, str] | None = None) -> dict[str, str]:
    """Projections' dk_id first; the uploaded DK Name+ID map fills any gaps."""
    out = id_to_name_from_projections(slug)
    if uploaded_map:
        for k, v in uploaded_map.items():
            out.setdefault(k, v)
    return out
