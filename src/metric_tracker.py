"""Grade a custom lineup metric against actual results and log the trend.

A POST-race SaberSim export self-contains both the custom-metric column AND the
`Actual` (post-race) score per lineup, so the robust full-pool grade needs only that
export — no standings matching. We compute the rank correlation of metric vs actual
across the whole pool plus a decile lift, and append the result to
`rules/<slug>/metric_performance.jsonl` so the metric earns (or loses) trust over
slates. This is analytics on the user's own lineups — no lineup building.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

_REPO_ROOT = Path(__file__).parent.parent


def _perf_path(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "metric_performance.jsonl"


def actual_is_populated(lineups: pd.DataFrame, actual_col: str = "Actual") -> bool:
    """True if the export's actual-score column exists and isn't all-zero/blank
    (a PRE-race export has Actual all zeros)."""
    if actual_col not in lineups.columns:
        return False
    a = pd.to_numeric(lineups[actual_col], errors="coerce").dropna()
    return (not a.empty) and bool((a != 0).any())


def grade_metric(lineups: pd.DataFrame, metric_col: str,
                 actual_col: str = "Actual") -> dict | None:
    """Full-pool grade of `metric_col` vs `actual_col`. None if columns missing/empty.

    Returns spearman (rank corr — no scipy), pearson, n, pool_mean, top/bottom decile
    avg, top50/100/500 avg, best_actual + the metric percentile that best lineup sat at.
    """
    if metric_col not in lineups.columns or actual_col not in lineups.columns:
        return None
    d = lineups[[metric_col, actual_col]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(d) < 10:
        return None
    m, a = d[metric_col], d[actual_col]
    spearman = round(float(m.rank().corr(a.rank())), 3)      # Spearman = Pearson of ranks
    pearson = round(float(m.corr(a)), 3)
    pool_mean = round(float(a.mean()), 1)

    order = d.sort_values(metric_col)
    n = len(d)
    bottom_decile = round(float(order.head(max(1, n // 10))[actual_col].mean()), 1)
    top_decile = round(float(order.tail(max(1, n // 10))[actual_col].mean()), 1)

    def top_n_avg(k: int):
        return round(float(d.nlargest(k, metric_col)[actual_col].mean()), 1) if k <= n else None

    best_idx = a.idxmax()
    best_actual = round(float(a.loc[best_idx]), 1)
    best_metric_pctile = round(float((m < m.loc[best_idx]).mean() * 100), 0)

    return {
        "n": n, "spearman": spearman, "pearson": pearson, "pool_mean": pool_mean,
        "top_decile_avg": top_decile, "bottom_decile_avg": bottom_decile,
        "decile_lift": round(top_decile - bottom_decile, 1),
        "top50_avg": top_n_avg(50), "top100_avg": top_n_avg(100), "top500_avg": top_n_avg(500),
        "best_actual": best_actual, "best_metric_pctile": best_metric_pctile,
    }


def log_performance(slug: str, row: dict) -> None:
    """Append one performance record to rules/<slug>/metric_performance.jsonl."""
    p = _perf_path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(row) + "\n")


def load_performance(slug: str, metric_id: str | None = None) -> list[dict]:
    """All performance rows (optionally filtered to one metric), oldest first."""
    p = _perf_path(slug)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if metric_id is None or r.get("metric_id") == metric_id:
            out.append(r)
    return out


def already_logged(slug: str, metric_id: str, contest: str) -> bool:
    """True if a row for this metric+contest is already in the ledger (dedupe guard)."""
    return any(r.get("metric_id") == metric_id and str(r.get("contest")) == str(contest)
               for r in load_performance(slug, metric_id))
