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
import unicodedata
from collections import Counter

import pandas as pd


# DK entry names use the account's display name, not the login email prefix.
USER_ALIASES = ("ryvlesgaming30", "ryanjsieb30")

_PITCHER_POSITIONS = {"p", "sp", "rp"}


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
    if lineups.empty:
        # Header-only / truncated export: fail fast instead of rendering a
        # zero-entry "analysis" that looks like it worked.
        raise ValueError("DK CSV parsed but contains no lineup rows.")
    lineups["Lineup_parsed"] = lineups["Lineup"].apply(_parse_lineup_string)
    lineups["Points"] = pd.to_numeric(lineups["Points"], errors="coerce")

    players = raw[right_cols].dropna(subset=["Player"]).copy()
    if players.empty:
        # Right half stripped (e.g. hand-edited CSV): everything downstream
        # (ownership, field profile, shark gap) would silently run on nothing.
        raise ValueError("DK CSV parsed but contains no player-ownership rows.")
    players = players.rename(columns={
        "Player": "name",
        "Roster Position": "roster_position",
        "%Drafted": "actual_own",
        "FPTS": "actual_fpts",
    })
    # Strip % sign from actual_own; coerce DK's missing-data placeholders
    # ("—", "-", blank) to NaN instead of crashing the whole parse.
    players["actual_own"] = pd.to_numeric(
        players["actual_own"].astype(str).str.rstrip("%"), errors="coerce"
    )
    players["actual_fpts"] = pd.to_numeric(players["actual_fpts"], errors="coerce")
    players["name"] = players["name"].astype(str).str.strip()

    return {"lineups": lineups, "players": players}


def _parse_lineup_string(lineup_str: str) -> list[str]:
    """Convert 'G Jon Rahm G Cameron Young G ...' into ['Jon Rahm', 'Cameron Young', ...]."""
    if not isinstance(lineup_str, str):
        return []
    # Explicit position-marker alternation: multi-char tokens (1B/2B/3B/SS/OF
    # for MLB, CPT/UTIL/FLEX for showdowns) must come before the single-char
    # class or they'd never match.
    tokens = re.split(
        r"(?:^|\s)(CPT|UTIL|FLEX|1B|2B|3B|SS|OF|SP|RP|[PCGDF])\s+", lineup_str
    )
    # tokens alternate: ['', position, name_segment, position, name_segment, ...]
    players: list[str] = []
    for i in range(2, len(tokens), 2):
        name = tokens[i].strip()
        if name:
            players.append(name)
    return players


_NAME_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def _norm_name(name) -> str:
    """Join key for matching standings names to projection names. Accent- and
    period-insensitive ('Daniel Suárez' == 'daniel suarez'); also drops a trailing
    Jr/Sr/III, quoted nicknames, and apostrophes/hyphens — the differences that
    silently zeroed MMA vendor matching (e.g. 'Michael Aswell Jr.' vs 'Michael
    Aswell')."""
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r'"[^"]*"|\'[^\']*\'', " ", s)           # drop "Nickname" / 'Nickname'
    s = s.casefold().replace(".", "").replace("'", "").replace("-", " ")
    toks = [t for t in s.split() if t]
    while toks and toks[-1] in _NAME_SUFFIXES:
        toks.pop()
    return " ".join(toks).strip()


def ambiguous_actual_norms(players: pd.DataFrame) -> set[str]:
    """Norm-keys that are two DIFFERENT players sharing a name in DK standings.

    DK standings carry no team column, so namesakes (6/12: Max Muncy LAD +
    Max Muncy ATH) can't be told apart — exclude them from joins rather than
    mis-attribute. Multi-position listings of ONE player repeat with identical
    FPTS, so only >1 distinct FPTS per norm flags as ambiguous.
    """
    df = players[["name", "actual_fpts"]].copy()
    df["_norm"] = df["name"].apply(_norm_name)
    counts = df.groupby("_norm")["actual_fpts"].nunique()
    return set(counts[counts > 1].index)


def is_user_entry(entry_name) -> bool:
    """True if a DK EntryName ('RyvlesGaming30 (4/10)' or bare) is the user's."""
    if not isinstance(entry_name, str):
        return False
    base = entry_name.split(" (")[0].strip().casefold()
    return base in USER_ALIASES


def _opt_round(values: list, ndigits: int = 2):
    """Mean of the non-None values, rounded; None if nothing to average.
    Pandas stores None as NaN in numeric columns, so filter both."""
    vals = [v for v in values if v is not None and pd.notna(v)]
    if not vals:
        return None
    return round(sum(vals) / len(vals), ndigits)


def _json_safe(val):
    """None for NaN/None; plain Python scalar otherwise (json.dumps-safe)."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


def lineup_profile(players: list[str], own_map: dict, proj_lookup: dict | None,
                   dup_counts: dict, sport: str) -> dict:
    """Structural profile of one lineup. salary_used/proj_total are None unless
    EVERY player matched projections — partial sums mislead."""
    norms = [_norm_name(p) for p in players]
    owns = [own_map[n] for n in norms if n in own_map]
    profile = {
        "avg_own": round(sum(owns) / len(owns), 2) if owns else None,
        "low_own_count": int(sum(1 for o in owns if o < 10)),
        "salary_used": None,
        "proj_total": None,
        "dup_count": int(dup_counts.get(tuple(sorted(norms)), 1)),
        "stack_shape": None,
    }
    if proj_lookup is not None:
        rows = [proj_lookup.get(n) for n in norms]
        if all(r is not None for r in rows):
            profile["salary_used"] = int(sum(r["salary"] for r in rows))
            profile["proj_total"] = round(sum(r["proj_points"] for r in rows), 2)
            if sport == "mlb":
                hitter_teams = [
                    r.get("team") for r in rows
                    if str(r.get("position", "")).strip().lower() not in _PITCHER_POSITIONS
                ]
                counts = sorted(Counter(t for t in hitter_teams if t).values(), reverse=True)
                profile["stack_shape"] = "-".join(str(c) for c in counts) if counts else None
    return profile


def analyze_contest(parsed: dict, proj_df: pd.DataFrame | None, sport: str) -> dict:
    """Structural analysis of one contest: the user's entries, the top finishers'
    lineup profiles, proj-vs-actual outliers, and slate-defining plays."""
    lineups = parsed["lineups"]
    players = parsed["players"]

    own_map = dict(zip(players["name"].apply(_norm_name), players["actual_own"]))
    fpts_map = dict(zip(players["name"].apply(_norm_name), players["actual_fpts"]))

    # Namesakes (>1 distinct FPTS per norm) are ambiguous in standings — drop
    # them from the maps so dict last-write can't credit the wrong player.
    # Lineups containing one degrade safely: lineup_profile's all-matched
    # guard nulls salary/proj rather than half-summing. Known noise: dup_counts
    # treats lineups differing only in WHICH namesake they used as duplicates.
    ambiguous = ambiguous_actual_norms(players)
    for norm in ambiguous:
        own_map.pop(norm, None)
        fpts_map.pop(norm, None)
    ambiguous_players = sorted(
        {str(p["name"]) for _, p in players.iterrows() if _norm_name(p["name"]) in ambiguous}
    )

    proj_lookup = None
    matched = 0
    if proj_df is not None and not proj_df.empty:
        proj_lookup = {}
        for _, r in proj_df.iterrows():
            entry = {"salary": r["salary"], "proj_points": r["proj_points"],
                     "ownership": r.get("ownership")}
            for opt in ("team", "position"):
                if opt in proj_df.columns:
                    entry[opt] = r[opt]
            proj_lookup[r["_norm"]] = entry
        matched = int(sum(1 for n in own_map if n in proj_lookup))

    # Rows with empty lineups (late scratches / withdrawn entries) are noise.
    valid = lineups[lineups["Lineup_parsed"].apply(len) > 0].copy()
    dup_counts = Counter(
        tuple(sorted(_norm_name(p) for p in lp)) for lp in valid["Lineup_parsed"]
    )

    field = len(lineups)
    top_n = min(100, max(20, round(0.01 * field)))

    def _profiled(rows: pd.DataFrame) -> pd.DataFrame:
        out = []
        for _, r in rows.iterrows():
            prof = lineup_profile(r["Lineup_parsed"], own_map, proj_lookup, dup_counts, sport)
            out.append({
                "rank": int(r["Rank"]),
                "entry_name": r["EntryName"],
                "points": float(r["Points"]),
                "players": list(r["Lineup_parsed"]),
                **prof,
            })
        return pd.DataFrame(out)

    winners_df = _profiled(valid.nsmallest(top_n, "Rank"))
    user_df = _profiled(valid[valid["EntryName"].apply(is_user_entry)])

    def _summary(df: pd.DataFrame) -> dict | None:
        if df.empty:
            return None
        return {
            "avg_own_mean": _opt_round(list(df["avg_own"])),
            "low_own_count_mean": _opt_round(list(df["low_own_count"])),
            "salary_used_mean": _opt_round(list(df["salary_used"]), 0),
        }

    winners_summary = _summary(winners_df) or {}
    winners_summary.update({
        "top_n": int(len(winners_df)),
        "dup_max": int(winners_df["dup_count"].max()) if not winners_df.empty else 0,
        "unique_pct": round(float((winners_df["dup_count"] == 1).mean() * 100), 1)
        if not winners_df.empty else None,
    })
    if sport == "mlb" and not winners_df.empty:
        shapes = Counter(s for s in winners_df["stack_shape"] if s)
        winners_summary["stack_shapes"] = dict(shapes.most_common())

    user_summary = _summary(user_df)
    if user_summary is not None:
        best = user_df.loc[user_df["rank"].idxmin()]
        user_summary.update({
            "entry_count": int(len(user_df)),
            "best_rank": int(best["rank"]),
            "best_percentile": round(float(best["rank"]) / field * 100, 1),
        })

    vs_user = None
    if user_summary is not None:
        vs_user = {}
        for key in ("avg_own_mean", "low_own_count_mean", "salary_used_mean"):
            w, u = winners_summary.get(key), user_summary.get(key)
            vs_user[key.replace("_mean", "_delta")] = (
                round(w - u, 2) if w is not None and u is not None else None
            )

    # Proj vs actual outliers (needs projections).
    overperformers: list[dict] = []
    underperformers: list[dict] = []
    if proj_lookup is not None:
        deltas = []
        for _, p in players.iterrows():
            norm = _norm_name(p["name"])
            proj = proj_lookup.get(norm)
            if proj is None:
                continue
            deltas.append({
                "name": p["name"],
                "proj_points": round(float(proj["proj_points"]), 2),
                "actual_fpts": float(p["actual_fpts"]),
                "fpts_delta": round(float(p["actual_fpts"]) - float(proj["proj_points"]), 2),
                "ownership": round(float(proj["ownership"]), 2)
                if proj.get("ownership") is not None and pd.notna(proj.get("ownership")) else None,
                "actual_own": float(p["actual_own"]),
            })
        deltas.sort(key=lambda d: d["fpts_delta"], reverse=True)
        overperformers = deltas[:5]
        underperformers = sorted(deltas[-5:], key=lambda d: d["fpts_delta"])

    # Slate-defining plays: heavily rostered by winners, low actual ownership.
    slate_defining: list[dict] = []
    if not winners_df.empty:
        appearance = Counter(
            _norm_name(p) for lp in winners_df["players"] for p in set(lp)
        )
        display = {_norm_name(p["name"]): p["name"] for _, p in players.iterrows()}
        for norm, count in appearance.items():
            pct = count / len(winners_df) * 100
            own = own_map.get(norm)
            if pct >= 30 and own is not None and own < 20:
                proj = proj_lookup.get(norm) if proj_lookup else None
                slate_defining.append({
                    "name": display.get(norm, norm),
                    "salary": int(proj["salary"]) if proj else None,
                    "actual_fpts": float(fpts_map.get(norm, 0)),
                    "actual_own": float(own),
                    "top_lineup_pct": round(pct, 1),
                })
        slate_defining.sort(key=lambda d: d["actual_fpts"], reverse=True)
        slate_defining = slate_defining[:8]

    return {
        "user_lineups_df": user_df,
        "winners_df": winners_df,
        "winners_summary": winners_summary,
        "user_summary": user_summary,
        "vs_user": vs_user,
        "overperformers": overperformers,
        "underperformers": underperformers,
        "slate_defining": slate_defining,
        "proj_match": {"matched": matched, "total": int(len(players)),
                       "available": proj_lookup is not None},
        "ambiguous_players": ambiguous_players,
    }


def _lineup_records(df: pd.DataFrame, field: int, cap: int = 10) -> list[dict]:
    """JSON-safe per-lineup rows, capped."""
    out = []
    for _, r in df.head(cap).iterrows():
        out.append({
            "rank": int(r["rank"]),
            "entry_name": str(r["entry_name"]),
            "points": float(r["points"]),
            "percentile": round(int(r["rank"]) / field * 100, 1),
            "players": list(r["players"]),
            "avg_own": _json_safe(r["avg_own"]),
            "low_own_count": int(r["low_own_count"]),
            "salary_used": _json_safe(r["salary_used"]),
            "proj_total": _json_safe(r["proj_total"]),
            "dup_count": int(r["dup_count"]),
            "stack_shape": _json_safe(r["stack_shape"]),
        })
    return out


def build_autopsy_record(*, ts: str, contest_label: str, slug: str, sport: str,
                         source_file: str, parsed: dict, analysis: dict,
                         proj_source: str | None, notes: str,
                         field_profile: dict | None = None,
                         contest_id: str | None = None) -> dict:
    """Assemble the schema-v2 jsonl record. Top-level fields are a strict
    superset of the legacy 7-field rows so bundle.py keeps working.
    `contest_id` (the DK contest instance) is the write-time dedup key —
    the log step skips a contest whose id is already in the ledger."""
    lineups = parsed["lineups"]
    field = len(lineups)
    winners = analysis["winners_summary"]
    return {
        "timestamp": ts,
        "contest_type": contest_label,
        "source_file": source_file,
        "contest_id": contest_id,
        "entries": int(field),
        "winning_score": float(lineups["Points"].max()),
        "cash_line_p80": float(lineups["Points"].quantile(0.80)),
        "notes": notes.strip(),
        "schema_version": 2,
        "slug": slug,
        "sport": sport,
        "projections": {
            "available": analysis["proj_match"]["available"],
            "source": proj_source,
            "matched": analysis["proj_match"]["matched"],
            "total": analysis["proj_match"]["total"],
        },
        "user_summary": analysis["user_summary"],
        # cap=150 (DK max-entry) so OUR entries are never silently truncated —
        # the accuracy layer + autopsy grade off this full set. Winners stay at 10.
        "user_lineups": _lineup_records(analysis["user_lineups_df"], field, cap=150),
        "top_overperformers": analysis["overperformers"],
        "top_underperformers": analysis["underperformers"],
        "slate_defining_plays": analysis["slate_defining"],
        "winners_structure": {
            **{k: winners.get(k) for k in
               ("top_n", "avg_own_mean", "low_own_count_mean", "salary_used_mean",
                "dup_max", "unique_pct")},
            **({"stack_shapes": winners["stack_shapes"]} if "stack_shapes" in winners else {}),
            "top_lineups": _lineup_records(analysis["winners_df"], field),
            "vs_user": analysis["vs_user"],
        },
        # Field / Fish profile — how the crowd + the fish played (standings-only);
        # the "leverage away from this" read, archived per contest.
        "field_profile": field_profile or None,
        # Near-miss counterfactual + winner build story (standings-only): was the
        # loss one swap away or structural, and what leverage carried the winner?
        "winner_story": _counterfactual("winner_story", parsed, analysis),
        "near_miss": _counterfactual("near_miss", parsed, analysis),
    }


def _counterfactual(kind: str, parsed: dict, analysis: dict):
    """Best-effort counterfactual fields for the record — never blocks it."""
    try:
        from src import counterfactual as _cf
        return (_cf.winner_story(parsed) if kind == "winner_story"
                else _cf.near_miss(parsed, analysis))
    except Exception:  # noqa: BLE001
        return None


def record_md_summary(record: dict) -> str:
    """Brief human-readable block for autopsies.md (the jsonl holds the detail)."""
    lines: list[str] = []
    us = record.get("user_summary")
    ws = record.get("winners_structure", {})
    if us:
        lines.append(
            f"- My entries: {us['entry_count']} · best rank {us['best_rank']:,}"
            f"/{record['entries']:,} (top {us['best_percentile']}%)"
        )
        deltas = ws.get("vs_user") or {}
        own_d = deltas.get("avg_own_delta")
        low_d = deltas.get("low_own_count_delta")
        if own_d is not None and ws.get("avg_own_mean") is not None:
            lines.append(
                f"- Winners (top {ws.get('top_n')}): avg own {ws['avg_own_mean']}% "
                f"vs mine {us['avg_own_mean']}% · sub-10% plays/lineup "
                f"{ws['low_own_count_mean']} vs mine {us['low_own_count_mean']}"
                + (f" · salary Δ {deltas.get('salary_used_delta'):+,.0f}"
                   if deltas.get("salary_used_delta") is not None else "")
            )
    else:
        lines.append("- My entries: none found in this contest")
    if ws.get("stack_shapes"):
        top_shapes = ", ".join(f"{k}×{v}" for k, v in list(ws["stack_shapes"].items())[:4])
        lines.append(f"- Winning stack shapes: {top_shapes}")
    over = record.get("top_overperformers") or []
    under = record.get("top_underperformers") or []
    if over:
        lines.append("- Overperformed proj: " + ", ".join(d["name"] for d in over[:3]))
    if under:
        lines.append("- Underperformed proj: " + ", ".join(d["name"] for d in under[:3]))
    sd = record.get("slate_defining_plays") or []
    if sd:
        lines.append(
            "- Slate-defining plays: "
            + ", ".join(f"{d['name']} ({d['actual_fpts']:.1f} pts @ {d['actual_own']:.1f}%)"
                        for d in sd[:4])
        )
    return "\n".join(lines)
