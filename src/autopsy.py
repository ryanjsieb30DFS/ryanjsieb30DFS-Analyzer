"""
Post-slate autopsy: parse DraftKings contest results CSVs, compare actuals vs
projections, log structured autopsy entries, detect patterns over N slates,
suggest rule changes for user approval, and apply approved changes.

DK contest-standings CSV format (confirmed from real file):
  Rank, EntryId, EntryName, TimeRemaining, Points, Lineup, <blank>, Player, Roster Position, %Drafted, FPTS
  - Left columns: one row per contest entry
  - Right columns: one row per player (count differs from entries)
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


_RULES_DIR = Path(__file__).parent.parent / "rules"


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


_ENTRY_SUFFIX_RE = re.compile(r"\s*\(\d+/\d+\)\s*$")


def _strip_entry_suffix(name: str) -> str:
    """Strip the DK MME '(N/N)' suffix from an EntryName for matching."""
    if not isinstance(name, str):
        return ""
    return _ENTRY_SUFFIX_RE.sub("", name).strip()


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


def log_autopsy(
    contest_type: str,
    slate_name: str,
    projections: pd.DataFrame,
    dk_results: dict,
    user_entry_names: list[str],
    slug: str | None = None,
    pools: dict | None = None,
) -> dict:
    """
    Compare projections vs actuals; write structured + narrative entries to disk.
    Returns metrics dict for UI display.
    """
    from src.rules import get_slug  # local import to avoid circular

    slug = slug or get_slug(contest_type)
    if not slug:
        raise ValueError(f"Unknown contest type: {contest_type}")

    players_actual = dk_results["players"]
    lineups = dk_results["lineups"]

    # Merge projections with actuals on name
    merged = projections.merge(
        players_actual[["name", "actual_own", "actual_fpts"]],
        on="name",
        how="outer",
    )
    merged["own_delta"] = merged["actual_own"] - merged["ownership"]
    merged["fpts_delta"] = merged["actual_fpts"] - merged["proj_points"]

    # Identify user's lineups. DK appends a "(N/N)" suffix to every entry on
    # multi-entry contests (e.g. "RyvlesGaming30 (4/4)"); strip it on both
    # sides so the user can type just their base username and match all entries.
    if user_entry_names:
        wanted = {_strip_entry_suffix(n) for n in user_entry_names}
        normalized = lineups["EntryName"].astype(str).apply(_strip_entry_suffix)
        user_lineups_df = lineups[normalized.isin(wanted)]
    else:
        user_lineups_df = pd.DataFrame()

    # Slate-defining plays: high actual FPTS at low actual ownership
    slate_defining = merged[
        (merged["actual_fpts"].notna()) & (merged["actual_own"] < 15)
    ].nlargest(10, "actual_fpts")

    # Performance breakdowns by tier
    chalk_actual = merged[merged["actual_own"] >= 30]
    leverage_actual = merged[(merged["actual_own"] >= 5) & (merged["actual_own"] < 15)]
    deep_actual = merged[merged["actual_own"] < 5]

    metrics = {
        "slate_name": slate_name,
        "contest_type": contest_type,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "num_players": int(merged["actual_fpts"].notna().sum()),
        "chalk_avg_fpts": float(chalk_actual["actual_fpts"].mean()) if not chalk_actual.empty else None,
        "chalk_count": int(len(chalk_actual)),
        "leverage_avg_fpts": float(leverage_actual["actual_fpts"].mean()) if not leverage_actual.empty else None,
        "leverage_count": int(len(leverage_actual)),
        "deep_avg_fpts": float(deep_actual["actual_fpts"].mean()) if not deep_actual.empty else None,
        "deep_count": int(len(deep_actual)),
        "user_lineups": user_lineups_df.to_dict(orient="records") if not user_lineups_df.empty else [],
        "best_user_rank": int(user_lineups_df["Rank"].min()) if not user_lineups_df.empty else None,
        "field_size": int(len(lineups)),
        "top_overperformers": merged.dropna(subset=["fpts_delta"]).nlargest(5, "fpts_delta")[
            ["name", "proj_points", "actual_fpts", "fpts_delta", "ownership", "actual_own"]
        ].to_dict(orient="records"),
        "top_underperformers": merged.dropna(subset=["fpts_delta"]).nsmallest(5, "fpts_delta")[
            ["name", "proj_points", "actual_fpts", "fpts_delta", "ownership", "actual_own"]
        ].to_dict(orient="records"),
        "slate_defining_plays": slate_defining[
            ["name", "salary", "actual_fpts", "actual_own"]
        ].to_dict(orient="records") if not slate_defining.empty else [],
    }

    # Score every built lineup in every pool against per-player actuals so the
    # user can see what unentered lineups would have scored. Persisted into the
    # autopsy_data.jsonl so it survives clear_session() after log.
    if pools:
        from src.lineup_scoring import score_built_lineups
        scored = score_built_lineups(pools, players_actual)
        # Phase A: join pre-slate sim metrics (roi/top1/win/cash) onto each
        # lineup row when the build was simmed against a contest. Uses the
        # most-recently-added contest per build (last key in the dict).
        if not scored.empty:
            sim_rows: list[dict] = []
            for build_name, pool in pools.items():
                sim_map = (pool or {}).get("contest_results_by_name") or {}
                if not sim_map:
                    continue
                contest_label = list(sim_map.keys())[-1]
                sim_df = sim_map[contest_label]
                if sim_df is None or len(sim_df) == 0:
                    continue
                for i, row in enumerate(sim_df.itertuples(index=False), start=1):
                    sim_rows.append({
                        "build_name": build_name,
                        "lineup_idx": i,
                        "sim_contest": contest_label,
                        "pre_sim_roi_pct": float(getattr(row, "roi_percent", 0) or 0),
                        "pre_sim_top1_pct": float(getattr(row, "top_1_percent", 0) or 0),
                        "pre_sim_win_pct": float(getattr(row, "win_percent", 0) or 0),
                        "pre_sim_cash_pct": float(getattr(row, "cash_percent", 0) or 0),
                    })
            if sim_rows:
                scored = scored.merge(
                    pd.DataFrame(sim_rows),
                    on=["build_name", "lineup_idx"],
                    how="left",
                )
        metrics["all_builds_scored"] = scored.to_dict(orient="records")
    else:
        metrics["all_builds_scored"] = []

    _append_autopsies_md(slug, metrics)
    _append_autopsy_data(slug, metrics)

    # Pre-serialize the per-player display slice so the full merged DataFrame
    # never enters st.session_state and isn't re-shipped to the browser on
    # every rerun (crashes Chrome on MME-sized fields).
    metrics["merged_display"] = (
        merged[["name", "salary", "ownership", "actual_own",
                "proj_points", "actual_fpts", "fpts_delta"]]
        .sort_values("fpts_delta", ascending=False)
        .to_dict(orient="records")
    )
    return metrics


def _append_autopsies_md(slug: str, metrics: dict) -> None:
    """Append a structured entry to rules/<slug>/autopsies.md."""
    path = _RULES_DIR / slug / "autopsies.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "",
        "---",
        "",
        f"## Autopsy: {metrics['slate_name']}",
        f"*Logged: {metrics['date']} | Field: {metrics['field_size']} entries*",
        "",
        "### Performance by tier",
        "",
        f"- **Chalk (30%+ own):** {metrics['chalk_count']} players, avg {_fmt(metrics['chalk_avg_fpts'])} FPTS",
        f"- **Leverage (5-15% own):** {metrics['leverage_count']} players, avg {_fmt(metrics['leverage_avg_fpts'])} FPTS",
        f"- **Deep contrarian (<5% own):** {metrics['deep_count']} players, avg {_fmt(metrics['deep_avg_fpts'])} FPTS",
        "",
        "### User result",
    ]
    if metrics["user_lineups"]:
        lines.append(f"- Best rank: **{metrics['best_user_rank']}** of {metrics['field_size']}")
        for lu in metrics["user_lineups"]:
            lines.append(f"  - `{lu.get('EntryName', '?')}`: {lu.get('Points', '?')} pts, rank {lu.get('Rank', '?')}")
    else:
        lines.append("- _No user lineups identified by EntryName._")

    lines.extend([
        "",
        "### Top over-performers (FPTS vs projection)",
        "",
        "| Player | Proj | Actual | Δ | Proj Own | Actual Own |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for p in metrics["top_overperformers"]:
        lines.append(
            f"| {p['name']} | {_fmt(p['proj_points'])} | {_fmt(p['actual_fpts'])} | "
            f"{_fmt(p['fpts_delta'], sign=True)} | {_fmt(p['ownership'])}% | {_fmt(p['actual_own'])}% |"
        )

    lines.extend(["", "### Top under-performers", "",
                  "| Player | Proj | Actual | Δ | Proj Own | Actual Own |",
                  "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for p in metrics["top_underperformers"]:
        lines.append(
            f"| {p['name']} | {_fmt(p['proj_points'])} | {_fmt(p['actual_fpts'])} | "
            f"{_fmt(p['fpts_delta'], sign=True)} | {_fmt(p['ownership'])}% | {_fmt(p['actual_own'])}% |"
        )

    if metrics["slate_defining_plays"]:
        lines.extend(["", "### Slate-defining plays (low-own, high FPTS)", "",
                      "| Player | Salary | Actual FPTS | Actual Own |",
                      "| --- | ---: | ---: | ---: |"])
        for p in metrics["slate_defining_plays"]:
            salary = p.get("salary")
            salary_str = f"${int(salary):,}" if salary and not pd.isna(salary) else "—"
            lines.append(
                f"| {p['name']} | {salary_str} | {_fmt(p['actual_fpts'])} | {_fmt(p['actual_own'])}% |"
            )

    with open(path, "a") as f:
        f.write("\n".join(lines) + "\n")


def _append_autopsy_data(slug: str, metrics: dict) -> None:
    """Append a single line of structured JSON to autopsy_data.jsonl."""
    path = _RULES_DIR / slug / "autopsy_data.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)

    # Strip non-JSON-serializable fields
    record = {k: v for k, v in metrics.items() if k != "merged"}
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def _fmt(x: Any, sign: bool = False) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    fmt = "+.1f" if sign else ".1f"
    try:
        return format(float(x), fmt)
    except (ValueError, TypeError):
        return str(x)


def load_autopsy_history(slug: str) -> list[dict]:
    """Read all past autopsy records for this contest type."""
    path = _RULES_DIR / slug / "autopsy_data.jsonl"
    if not path.exists():
        return []
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def detect_patterns(slug: str, window: int = 5) -> list[dict]:
    """
    Detect recurring patterns over the last `window` slates.
    Returns a list of pattern dicts with evidence count.
    """
    history = load_autopsy_history(slug)
    if len(history) < 3:
        return []

    recent = history[-window:]
    patterns: list[dict] = []

    # Pattern 1: chalk consistently outperforming
    chalk_strong = sum(
        1 for s in recent
        if s.get("chalk_avg_fpts") and s.get("leverage_avg_fpts")
        and s["chalk_avg_fpts"] > s["leverage_avg_fpts"] * 1.1
    )
    if chalk_strong >= 3:
        patterns.append({
            "id": "chalk_outperforming",
            "summary": f"Chalk has outperformed leverage in {chalk_strong} of last {len(recent)} slates",
            "evidence_count": chalk_strong,
            "window": len(recent),
            "implication": "Consider loosening leverage-mandatory rules or raising chalk exposure caps.",
        })

    # Pattern 2: leverage consistently rewarded
    leverage_strong = sum(
        1 for s in recent
        if s.get("leverage_avg_fpts") and s.get("chalk_avg_fpts")
        and s["leverage_avg_fpts"] > s["chalk_avg_fpts"] * 0.95
    )
    if leverage_strong >= 3:
        patterns.append({
            "id": "leverage_rewarded",
            "summary": f"Leverage matched or beat chalk in {leverage_strong} of last {len(recent)} slates",
            "evidence_count": leverage_strong,
            "window": len(recent),
            "implication": "Current min_sub16_ownership rule is paying off — consider tightening (require 2 sub-16% per lineup).",
        })

    # Pattern 3: deep contrarian (<5% own) consistently top-tier
    deep_strong = sum(
        1 for s in recent
        if s.get("deep_avg_fpts") and s.get("chalk_avg_fpts")
        and s["deep_avg_fpts"] > s["chalk_avg_fpts"] * 0.8
    )
    if deep_strong >= 3:
        patterns.append({
            "id": "deep_contrarian_alive",
            "summary": f"Sub-5% plays delivered competitive FPTS in {deep_strong} of last {len(recent)} slates",
            "evidence_count": deep_strong,
            "window": len(recent),
            "implication": "Consider adding a min_deep_contrarian_per_lineup constraint.",
        })

    return patterns


def suggest_rule_changes(slug: str, patterns: list[dict]) -> list[dict]:
    """Convert patterns into proposed YAML edits with before/after diffs."""
    rules_path = _RULES_DIR / slug / "rules.yaml"
    if not rules_path.exists():
        return []
    with open(rules_path) as f:
        current_rules = yaml.safe_load(f) or {}

    suggestions: list[dict] = []
    for p in patterns:
        if p["id"] == "leverage_rewarded":
            current_val = current_rules.get("constraints", {}).get("min_sub16_ownership_per_lineup")
            if current_val is not None and current_val < 2:
                suggestions.append({
                    "pattern_id": p["id"],
                    "summary": p["summary"],
                    "rule_path": "constraints.min_sub16_ownership_per_lineup",
                    "current_value": current_val,
                    "proposed_value": current_val + 1,
                    "evidence_count": p["evidence_count"],
                    "window": p["window"],
                })
        elif p["id"] == "chalk_outperforming":
            current_val = current_rules.get("constraints", {}).get("max_player_exposure_pct")
            if current_val is not None and current_val < 75:
                suggestions.append({
                    "pattern_id": p["id"],
                    "summary": p["summary"],
                    "rule_path": "constraints.max_player_exposure_pct",
                    "current_value": current_val,
                    "proposed_value": min(75, current_val + 10),
                    "evidence_count": p["evidence_count"],
                    "window": p["window"],
                })
        elif p["id"] == "deep_contrarian_alive":
            constraints = current_rules.get("constraints", {})
            if "min_deep_contrarian_per_lineup" not in constraints:
                suggestions.append({
                    "pattern_id": p["id"],
                    "summary": p["summary"],
                    "rule_path": "constraints.min_deep_contrarian_per_lineup",
                    "current_value": None,
                    "proposed_value": 1,
                    "evidence_count": p["evidence_count"],
                    "window": p["window"],
                })

    return suggestions


def apply_rule_change(slug: str, suggestion: dict) -> None:
    """Apply an approved rule change to rules.yaml and log to changelog."""
    rules_path = _RULES_DIR / slug / "rules.yaml"
    with open(rules_path) as f:
        current = yaml.safe_load(f) or {}

    # Set nested path, e.g. 'constraints.min_sub16_ownership_per_lineup'
    parts = suggestion["rule_path"].split(".")
    node = current
    for key in parts[:-1]:
        if key not in node or not isinstance(node[key], dict):
            node[key] = {}
        node = node[key]
    node[parts[-1]] = suggestion["proposed_value"]

    with open(rules_path, "w") as f:
        yaml.safe_dump(current, f, sort_keys=False)

    _append_changelog(slug, suggestion)


def _append_changelog(slug: str, suggestion: dict) -> None:
    """Append the accepted change to rule_changelog.md."""
    path = _RULES_DIR / slug / "rule_changelog.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = (
        f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"- **Rule:** `{suggestion['rule_path']}`\n"
        f"- **Before:** `{suggestion['current_value']}`\n"
        f"- **After:** `{suggestion['proposed_value']}`\n"
        f"- **Pattern:** {suggestion['summary']}\n"
        f"- **Evidence:** {suggestion['evidence_count']} of last {suggestion['window']} slates\n"
    )
    with open(path, "a") as f:
        f.write(entry)
