"""Export the portfolio to a DraftKings bulk-upload CSV.

Mirrors the simulator's dk_export. DK's entry template (the `DKEntries-*.csv`
downloaded from a contest's "My Entries" → Export) has the entries table on the
LEFT (Entry ID, Contest Name, Contest ID, Entry Fee, <ROSTER SLOTS...>, blank,
Instructions) and bolts the draftable-player list onto the RIGHT of the rows, so
later rows have more fields than the header; the slot headers are duplicates
(e.g. six `F` columns). We read only the entry columns and fill ONE lineup per
entry row as ``Name (DK_ID)`` (positionally).

Analyzer-specific: the portfolio lives as markdown roster tables in
``data/lineups/<slug>.md`` (player names, no IDs), so we parse the names out and
map them to DK IDs via the loaded pool's ``dk_id`` column.
"""
from __future__ import annotations

import csv
import io

import pandas as pd

_ROSTER_HEADERS = {"fighter", "golfer", "driver", "player", "name", "pitcher", "batter"}


# ---- DK template reading + filling (shared with the simulator) --------------

def read_dk_entries(file) -> pd.DataFrame:
    """Read just the entries table from a DK export (quote-aware; drops the
    player-pool columns bolted onto the right; stops at the first non-entry row)."""
    raw = file.read() if hasattr(file, "read") else open(file, "rb").read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig", "ignore")
    lines = raw.splitlines()
    hdr_i = next((i for i, ln in enumerate(lines) if ln.startswith("Entry ID,")), 0)
    reader = csv.reader(io.StringIO("\n".join(lines[hdr_i:])))
    header = next(reader)
    ncol = len(header)
    rows = []
    for fields in reader:
        if not fields or not fields[0].strip().isdigit():
            break
        rows.append((fields + [""] * ncol)[:ncol])
    return pd.DataFrame(rows, columns=header)


def roster_slot_positions(template: pd.DataFrame) -> list:
    """Column POSITIONS of the roster slots (between 'Entry Fee' and the trailing
    blank/'Instructions'). Positional because the slot headers are duplicates."""
    cols = list(template.columns)
    if "Entry Fee" not in cols:
        return []
    out = []
    for j in range(cols.index("Entry Fee") + 1, len(cols)):
        cs = str(cols[j])
        if cols[j] == "Instructions" or cs.startswith("Unnamed") or cs.strip() == "":
            break
        out.append(j)
    return out


def _slot_value(name, dk_id) -> str:
    if dk_id is None or pd.isna(dk_id):
        return str(name)
    try:
        return f"{name} ({int(dk_id)})"
    except (ValueError, TypeError):
        return f"{name} ({dk_id})"


def fill_dk_template(
    template: pd.DataFrame,
    lineups: list[list[tuple]],
    contest_name: str | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Fill a DK entry template — one lineup per entry row, in order. Each lineup
    is a list of (name, dk_id) tuples. Optionally restrict to one contest."""
    out = template.reset_index(drop=True).copy()
    slot_pos = roster_slot_positions(out)
    contests = (sorted(out["Contest Name"].dropna().unique().tolist())
                if "Contest Name" in out.columns else [])
    info = {"roster_slots": len(slot_pos), "n_lineups": len(lineups),
            "filled": 0, "n_entries": 0, "contests": contests, "warnings": []}
    if not slot_pos:
        info["warnings"].append("No roster slot columns found — is this a DK entries CSV?")
        return out, info

    if contest_name and "Contest Name" in out.columns:
        entry_rows = out.index[out["Contest Name"] == contest_name].tolist()
    else:
        entry_rows = out.index.tolist()
    info["n_entries"] = len(entry_rows)

    n = min(len(entry_rows), len(lineups))
    for k in range(n):
        roster = lineups[k]
        if len(roster) != len(slot_pos):
            info["warnings"].append(
                f"Lineup {k + 1} has {len(roster)} players but the template has "
                f"{len(slot_pos)} slots — filled what fit.")
        for j, col_pos in enumerate(slot_pos):
            if j < len(roster):
                name, dk_id = roster[j]
                out.iat[entry_rows[k], col_pos] = _slot_value(name, dk_id)
    info["filled"] = n
    if len(lineups) > len(entry_rows):
        info["warnings"].append(
            f"{len(lineups) - len(entry_rows)} more lineups than entries for this "
            "selection — extras not exported (reserve more DK entries, or export fewer).")
    return out, info


# ---- Analyzer portfolio (markdown) -> rosters -------------------------------

def parse_portfolio_rosters(md_text: str, roster_size: int | None = None) -> list[list[str]]:
    """Extract each lineup's player names from a data/lineups/<slug>.md portfolio.
    Each lineup is a markdown roster table whose first column is the player name;
    a header row (Fighter/Golfer/...) starts a new lineup. Non-roster tables
    (whose header isn't a known roster header) are ignored. When `roster_size` is
    given, only tables with exactly that many players are kept — drops the
    Portfolio-audit / exposure tables (which share a 'Fighter' header)."""
    rosters, current, in_table = [], [], False
    for line in md_text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if current:
                rosters.append(current)
                current = []
            in_table = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        first = cells[0]
        if set(first) <= set("-: "):                    # separator row
            continue
        if first.lower() in _ROSTER_HEADERS:            # header -> new lineup
            if current:
                rosters.append(current)
                current = []
            in_table = True
            continue
        if in_table and first:                          # data row -> player name
            current.append(first)
    if current:
        rosters.append(current)
    return [r for r in rosters if r and (roster_size is None or len(r) == roster_size)]


def rosters_to_lineups(rosters: list[list[str]], name_to_id: dict) -> tuple[list, list]:
    """Map parsed name-rosters to [(name, dk_id), ...] lineups via the pool's
    name->dk_id map. Returns (lineups, unresolved_names)."""
    lineups, unresolved = [], []
    norm = {str(k).strip().lower(): v for k, v in name_to_id.items()}
    for roster in rosters:
        lineup = []
        for name in roster:
            did = name_to_id.get(name)
            if did is None:
                did = norm.get(str(name).strip().lower())
            if did is None:
                unresolved.append(name)
            lineup.append((name, did))
        lineups.append(lineup)
    return lineups, sorted(set(unresolved))
