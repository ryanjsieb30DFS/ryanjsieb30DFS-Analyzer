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


# ---------------------------------------------------------------------------
# Contest screener (8/30/26) — your record in contests shaped like these
# ---------------------------------------------------------------------------
#
# REVIVED from the removed Trends tab, as a pre-lock screen: when the slate's
# contests are declared, show how you have ACTUALLY finished in contests of
# the same shape (type + field size). Contest selection is edge that costs
# nothing at lock — a 390-entry field and a 25,000-entry field are different
# games, and the ledger knows which shapes have paid you.
#
# Information only, never a command (the gate-only-strategy-calls rule): the
# table names the shape, the sample size, and the record; the user decides
# what to enter. Small samples say so out loud instead of pretending.

_THIN_N = 5   # below this many comparable contests, the record is a hint


def _rate(pct_series, threshold: float):
    """Share of finishes at or under `threshold` percentile (lower = better)."""
    vals = [v for v in pct_series if v is not None]
    if not vals:
        return None
    return round(100.0 * sum(1 for v in vals if v <= threshold) / len(vals), 0)


def screen_declared(declared: list[dict],
                    rows: pd.DataFrame | None = None) -> list[dict]:
    """One record per declared contest: the ledger's history for contests of
    the same SHAPE, with the comparison basis named and thin samples flagged.

    Comparison basis, most specific first:
      * "same type + field size"  — type matches AND same field-size bucket
      * "same type"               — type matches, any field size
      * "same field size"         — same bucket, any type
      * none                      — no comparable history at all
    """
    if rows is None:
        rows = load_contest_rows()
    out = []
    for c in declared or []:
        typ = c.get("type") or "unknown"
        bucket = field_size_bucket(c.get("field_size"))
        rec = {"name": c.get("name"), "type": typ,
               "field_size": c.get("field_size"), "field_bucket": bucket,
               "entry_fee": c.get("entry_fee"), "my_entries": c.get("my_entries")}
        if rows.empty:
            rec.update({"basis": None, "n": 0})
            out.append(rec)
            continue
        candidates = (
            ("same type + field size",
             rows[(rows["type"] == typ) & (rows["field_bucket"] == bucket)]),
            ("same type", rows[rows["type"] == typ]),
            ("same field size", rows[rows["field_bucket"] == bucket]),
        )
        basis, hist = None, None
        for label, sub in candidates:
            if len(sub) >= 1:
                basis, hist = label, sub
                break
        if hist is None:
            rec.update({"basis": None, "n": 0})
            out.append(rec)
            continue
        pct = pd.to_numeric(hist["best_percentile"], errors="coerce").dropna()
        rec.update({
            "basis": basis,
            "n": len(hist),
            "slates": int(hist["slate_label"].nunique()),
            "median_pctile": round(float(pct.median()), 1) if not pct.empty else None,
            "best_pctile": round(float(pct.min()), 1) if not pct.empty else None,
            "top10_rate": _rate(pct.tolist(), 10.0),
            "top1_rate": _rate(pct.tolist(), 1.0),
            "thin": len(hist) < _THIN_N,
        })
        out.append(rec)
    return out


def screen_md(records: list[dict]) -> str:
    """The screener, in plain words. Percentile: LOWER is better — 5 means
    the entry beat 95% of the field."""
    if not records:
        return ""
    lines = [
        "This table shows how you have finished in past contests SHAPED like "
        "each one you declared — same contest type and a similar field size. "
        "Finish is a percentile of the field: **lower is better** (5 means "
        "the entry beat 95% of the field). It is your record, not a command "
        "— you decide what to enter.",
        "",
        "| declared contest | shape | your history | median finish | "
        "top-10% rate | best ever |",
        "|---|---|---|---:|---:|---:|",
    ]
    for r in records:
        shape = f"{r['type']} · {r['field_bucket']} field"
        if not r.get("n"):
            lines.append(f"| {r['name']} | {shape} | no comparable history "
                         "yet | — | — | — |")
            continue
        hist = f"{r['n']} contest(s) ({r['basis']})"
        if r.get("thin"):
            hist += " ⚠️ thin"
        lines.append(
            f"| {r['name']} | {shape} | {hist} | "
            f"{r.get('median_pctile') if r.get('median_pctile') is not None else '—'} | "
            f"{str(int(r['top10_rate'])) + '%' if r.get('top10_rate') is not None else '—'} | "
            f"{r.get('best_pctile') if r.get('best_pctile') is not None else '—'} |")
    lines.append("")
    lines.append("⚠️ thin = under 5 comparable contests, so the record is a "
                 "hint, not a pattern. \"same type\" means no history at this "
                 "exact field size — the comparison widened to the contest "
                 "type alone.")
    lines.append("")
    lines.append("One honest caveat: the finish is your BEST entry in that "
                 "contest. A 150-Max played with 10 entries gets 10 tries at "
                 "a good finish, a single entry gets one — so a multi-entry "
                 "shape's record always looks better than a single-entry "
                 "shape's, even at equal skill. Compare a shape against "
                 "ITSELF over time, not single-entry against multi-entry.")
    # Best-shaped combo per TRACK, as orientation. Focus (SE/3-Max/5-Max) and
    # MME are graded separately — the entry-count caveat above is exactly why
    # a single cross-track "best shape" would always crown the multi-entry one.
    all_rows = load_contest_rows()
    if not all_rows.empty:
        focus = all_rows[all_rows["type"].isin(["SE", "3-Max", "5-Max"])]
        mme = all_rows[all_rows["type"].isin(["20-Max", "150-Max"])]
        for label, sub in (("small-field (SE/3-Max/5-Max)", focus),
                           ("large-field (20-Max/150-Max)", mme)):
            best = where_you_win(sub)
            if best:
                lines.append("")
                lines.append(
                    f"Your best {label} record: **{best['type']} contests "
                    f"with a {best['field_bucket']} field** — median finish "
                    f"at the {best['median_pctile']} percentile over "
                    f"{best['contests']} contest(s).")
    return "\n".join(lines)
