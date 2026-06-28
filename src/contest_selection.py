"""Contest-selection analytics — cross-sport "where you win".

Flattens every `rules/<slug>/results.jsonl` into one row per contest entered,
then buckets **best-percentile** by contest TYPE and FIELD-SIZE so the user can
see which contest shapes actually pay them. Best-percentile is the scoreboard:
`winnings`/`roi_pct` are usually null (the user tracks ROI in a third-party app),
so ROI is reported only as a coverage count — never required, never gated on.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src import history

_REPO_ROOT = Path(__file__).parent.parent

_BUCKET_ORDER = ["<500", "500–2k", "2k–10k", "10k+", "unknown"]


def _slugs() -> list[str]:
    """Every sport slug that has a results ledger on disk."""
    root = _REPO_ROOT / "rules"
    if not root.exists():
        return []
    return sorted(d.name for d in root.iterdir()
                  if d.is_dir() and (d / "results.jsonl").exists())


def field_size_bucket(field_size) -> str:
    """Field size -> bucket label (<500 / 500–2k / 2k–10k / 10k+ / unknown)."""
    try:
        n = int(field_size)
    except (TypeError, ValueError):
        return "unknown"
    if n < 500:
        return "<500"
    if n < 2000:
        return "500–2k"
    if n < 10000:
        return "2k–10k"
    return "10k+"


def load_contest_rows() -> pd.DataFrame:
    """One row per contest entered across ALL sports' results.jsonl ledgers."""
    rows = []
    for slug in _slugs():
        for slate in history.load_results(slug):
            for c in (slate.get("contests") or []):
                rows.append({
                    "date": slate.get("date"),
                    "slug": slug,
                    "sport": slate.get("sport"),
                    "slate_label": slate.get("slate_label"),
                    "name": c.get("name"),
                    "type": c.get("type") or "unknown",
                    "field_size": c.get("field_size"),
                    "field_bucket": field_size_bucket(c.get("field_size")),
                    "my_entries": c.get("my_entries"),
                    "entry_fee": c.get("entry_fee"),
                    "buy_in": c.get("buy_in"),
                    "winnings": c.get("winnings"),
                    "roi_pct": c.get("roi_pct"),
                    "best_rank": c.get("best_rank"),
                    "best_percentile": c.get("best_percentile"),
                })
    return pd.DataFrame(rows)


def _agg(rows: pd.DataFrame, by: str) -> pd.DataFrame:
    """Per-group rollup: contest/slate counts, median + best percentile, ROI coverage.
    Lower percentile = better (1 = top of the field)."""
    if rows.empty or by not in rows.columns:
        return pd.DataFrame()
    out = []
    for key, g in rows.groupby(by, dropna=False):
        pct = pd.to_numeric(g["best_percentile"], errors="coerce").dropna()
        roi = pd.to_numeric(g["roi_pct"], errors="coerce").dropna()
        out.append({
            by: key,
            "contests": len(g),
            "slates": int(g["slate_label"].nunique()),
            "median_pctile": round(float(pct.median()), 1) if not pct.empty else None,
            "best_pctile": round(float(pct.min()), 1) if not pct.empty else None,
            "roi_reported": int(roi.shape[0]),
            "mean_roi": round(float(roi.mean()), 1) if not roi.empty else None,
        })
    return pd.DataFrame(out)


def by_type(rows: pd.DataFrame) -> pd.DataFrame:
    """Rollup by contest type, best (lowest) median percentile first."""
    out = _agg(rows, "type")
    if out.empty:
        return out
    return out.sort_values("median_pctile", na_position="last").reset_index(drop=True)


def by_field_bucket(rows: pd.DataFrame) -> pd.DataFrame:
    """Rollup by field-size bucket, ordered small -> large."""
    out = _agg(rows, "field_bucket")
    if out.empty:
        return out
    out["field_bucket"] = pd.Categorical(out["field_bucket"], categories=_BUCKET_ORDER, ordered=True)
    return out.sort_values("field_bucket").reset_index(drop=True)


def where_you_win(rows: pd.DataFrame, min_n: int = 3) -> dict | None:
    """The (type, field_bucket) combo with the lowest median best_percentile at
    n>=min_n contests. None when no combo has enough samples yet."""
    if rows.empty:
        return None
    best = None
    for (typ, bucket), g in rows.groupby(["type", "field_bucket"], dropna=False):
        pct = pd.to_numeric(g["best_percentile"], errors="coerce").dropna()
        if len(g) < min_n or pct.empty:
            continue
        med = float(pct.median())
        if best is None or med < best["median_pctile"]:
            best = {"type": typ, "field_bucket": bucket,
                    "median_pctile": round(med, 1), "contests": len(g)}
    return best
