"""Landscape computations: chalk tiers, leverage, anchor-equivalence."""
from __future__ import annotations

import pandas as pd


def chalk_tiers(projections: pd.DataFrame) -> pd.DataFrame:
    """Bin players by ownership tier."""
    df = projections.copy()
    own = df["ownership"].fillna(0)

    def tier(o):
        if o >= 25: return "Mega-chalk (25%+)"
        if o >= 15: return "Chalk (15-25%)"
        if o >= 8:  return "Mid-own (8-15%)"
        if o >= 3:  return "Low-own (3-8%)"
        return "Punt (<3%)"

    df["tier"] = own.apply(tier)
    return df


def chalk_summary(projections: pd.DataFrame) -> pd.DataFrame:
    """Counts and avg proj/salary per tier."""
    df = chalk_tiers(projections)
    grp = df.groupby("tier").agg(
        n=("name", "count"),
        avg_proj=("proj_points", "mean"),
        avg_salary=("salary", "mean"),
        avg_own=("ownership", "mean"),
    ).round(2).reset_index()
    order = ["Mega-chalk (25%+)", "Chalk (15-25%)", "Mid-own (8-15%)", "Low-own (3-8%)", "Punt (<3%)"]
    grp["tier"] = pd.Categorical(grp["tier"], categories=order, ordered=True)
    return grp.sort_values("tier").reset_index(drop=True)


def leverage_table(projections: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Low ownership + high upside. Uses ceiling if available, else proj."""
    df = projections.copy()
    upside = df["ceiling"] if "ceiling" in df.columns and df["ceiling"].notna().any() else df["proj_points"]
    df["upside"] = upside
    df["leverage_score"] = df["upside"] / (df["ownership"].fillna(0) + 1)
    cols = ["name", "salary", "proj_points", "upside", "ownership", "leverage_score"]
    return df.sort_values("leverage_score", ascending=False).head(top_n)[cols].reset_index(drop=True)


def anchor_equivalence_check(projections: pd.DataFrame, own_window: float = 5.0) -> list[dict]:
    """Find chalk-tier anchor pairs at similar own%. Returns groups of equivalent anchors.

    The leak: if 2+ chalk-tier anchors at similar own, >=1 lineup must run the alternative.
    """
    df = projections.copy()
    chalk = df[df["ownership"].fillna(0) >= 15].sort_values("ownership", ascending=False)
    if len(chalk) < 2:
        return []

    groups = []
    used = set()
    for i, a in chalk.iterrows():
        if i in used:
            continue
        peers = chalk[
            (chalk.index != i)
            & (~chalk.index.isin(used))
            & ((chalk["ownership"] - a["ownership"]).abs() <= own_window)
        ]
        if len(peers) >= 1:
            members = [a.to_dict()] + peers.to_dict("records")
            used.add(i)
            used.update(peers.index.tolist())
            groups.append({
                "players": [m["name"] for m in members],
                "own_range": (
                    min(m["ownership"] for m in members),
                    max(m["ownership"] for m in members),
                ),
                "rule": "At least one lineup must run the alternative anchor.",
            })
    return groups
