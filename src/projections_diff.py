"""Cross-vendor projection disagreement detector."""
from __future__ import annotations

import pandas as pd


def diff_table(sources: dict[str, dict], metric: str = "proj_points") -> pd.DataFrame:
    """Wide table: one row per player, one column per source's metric.

    sources: {source_name: {"vendor": str, "df": pd.DataFrame}}
    """
    if not sources:
        return pd.DataFrame()

    wide = None
    for name, blob in sources.items():
        df = blob["df"]
        if metric not in df.columns:
            continue
        sub = df[["name", metric]].rename(columns={metric: name})
        sub["name"] = sub["name"].astype(str).str.strip()
        wide = sub if wide is None else wide.merge(sub, on="name", how="outer")

    if wide is None or len(wide.columns) <= 2:
        return pd.DataFrame()

    value_cols = [c for c in wide.columns if c != "name"]
    wide["max"] = wide[value_cols].max(axis=1)
    wide["min"] = wide[value_cols].min(axis=1)
    wide["delta"] = wide["max"] - wide["min"]
    wide["delta_pct"] = (wide["delta"] / wide[value_cols].mean(axis=1) * 100).round(1)

    return wide.sort_values("delta", ascending=False).reset_index(drop=True)


def flagged_disagreements(sources: dict[str, dict], metric: str = "proj_points", pct_threshold: float = 15.0) -> pd.DataFrame:
    """Subset of diff_table where delta_pct > threshold."""
    df = diff_table(sources, metric)
    if df.empty:
        return df
    return df[df["delta_pct"] >= pct_threshold].reset_index(drop=True)
