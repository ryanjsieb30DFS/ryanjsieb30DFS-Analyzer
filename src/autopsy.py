"""
Post-slate autopsy: parse DraftKings contest-standings CSVs into lineup and
player DataFrames for the Autopsy tab.

DK contest-standings CSV format (confirmed from real file):
  Rank, EntryId, EntryName, TimeRemaining, Points, Lineup, <blank>, Player, Roster Position, %Drafted, FPTS
  - Left columns: one row per contest entry
  - Right columns: one row per player (count differs from entries)

The Autopsy tab logs lessons (autopsies.md + autopsy_data.jsonl) inline; the
strategic learning is done by Claude reading those files, not by this module.
"""
from __future__ import annotations

import re

import pandas as pd


def parse_dk_results(csv_path_or_buffer) -> dict:
    """Parse a DK contest-standings CSV into lineup and player DataFrames."""
    raw = pd.read_csv(csv_path_or_buffer)

    # The CSV has a blank column between the two datasets.
    # Left half is lineup-level, right half is player-level.
    left_cols = ["Rank", "EntryId", "EntryName", "TimeRemaining", "Points", "Lineup"]
    right_cols = ["Player", "Roster Position", "%Drafted", "FPTS"]

    missing_left = [c for c in left_cols if c not in raw.columns]
    if missing_left:
        raise ValueError(f"DK CSV missing lineup columns: {missing_left}")

    missing_right = [c for c in right_cols if c not in raw.columns]
    if missing_right:
        raise ValueError(f"DK CSV missing player columns: {missing_right}")

    lineups = raw[left_cols].dropna(subset=["EntryId"]).copy()
    lineups["Lineup_parsed"] = lineups["Lineup"].apply(_parse_lineup_string)
    lineups["Points"] = lineups["Points"].astype(float)

    players = raw[right_cols].dropna(subset=["Player"]).copy()
    players = players.rename(columns={
        "Player": "name",
        "Roster Position": "roster_position",
        "%Drafted": "actual_own",
        "FPTS": "actual_fpts",
    })
    # Strip % sign from actual_own
    players["actual_own"] = (
        players["actual_own"].astype(str).str.rstrip("%").astype(float)
    )
    players["actual_fpts"] = players["actual_fpts"].astype(float)
    players["name"] = players["name"].astype(str).str.strip()

    return {"lineups": lineups, "players": players}


def _parse_lineup_string(lineup_str: str) -> list[str]:
    """Convert 'G Jon Rahm G Cameron Young G ...' into ['Jon Rahm', 'Cameron Young', ...]."""
    if not isinstance(lineup_str, str):
        return []
    # Split on single-letter position markers (G, F, D, CPT, etc.) preceded by space or start
    tokens = re.split(r"(?:^|\s)([A-Z]{1,4})\s+", lineup_str)
    # tokens alternate: ['', position, name_segment, position, name_segment, ...]
    players: list[str] = []
    for i in range(2, len(tokens), 2):
        name = tokens[i].strip()
        if name:
            players.append(name)
    return players
