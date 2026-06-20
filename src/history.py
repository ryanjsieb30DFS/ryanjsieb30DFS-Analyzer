"""Per-slate history archive + cross-slate results ledger.

When the user logs an autopsy, `archive_slate` copies the slate's artifacts
(slate analysis, lineups, bundle, contests) into a permanent folder at
rules/<slug>/history/<date>__<slate-label>/ BEFORE the Autopsy tab clears the
per-slate workspace, and appends one row per slate to rules/<slug>/results.jsonl
(buy-in, winnings, ROI, best rank/percentile).

Ownership contract: results.jsonl is app-written and never edited afterward.
Claude reads it for trending but never mutates it; lesson cross-references live
in rules/<slug>/lessons.yaml instead.

GPP variance note: per-lineup ROI is intentionally NOT computed — DK standings
CSVs carry no payout data, and GPP ROI is meaningless over small samples. The
ledger keeps best-percentile and process metrics alongside slate ROI.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent

# Per-slate workspace artifacts worth preserving (source path per slug).
_ARCHIVE_SOURCES = {
    "slate_analysis.md": lambda slug: _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md",
    "lineups.md": lambda slug: _REPO_ROOT / "data" / "lineups" / f"{slug}.md",
    "bundle.md": lambda slug: _REPO_ROOT / "data" / "bundle" / f"{slug}.md",
    "contests.json": lambda slug: _REPO_ROOT / "data" / "contests" / f"{slug}.json",
    "red_team.md": lambda slug: _REPO_ROOT / "data" / "red_team" / f"{slug}.md",
}


def _history_root(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "history"


def _results_path(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "results.jsonl"


def _slugify(label: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def slate_dirname(date_str: str, slate_label: str) -> str:
    """e.g. ('2026-05-31', 'Nashville Superspeedway') -> '2026-05-31__nashville-superspeedway'."""
    return f"{date_str}__{_slugify(slate_label) or 'slate'}"


def compute_roi(entry_fee, my_entries, winnings) -> dict:
    """Buy-in / winnings / ROI%. winnings=None means 'not reported' -> roi None."""
    fee = float(entry_fee or 0.0)
    n = int(my_entries or 0)
    buy_in = round(fee * n, 2)
    if winnings is None:
        return {"buy_in": buy_in, "winnings": None, "roi_pct": None}
    win = float(winnings)
    roi = round((win - buy_in) / buy_in * 100.0, 1) if buy_in > 0 else None
    return {"buy_in": buy_in, "winnings": round(win, 2), "roi_pct": roi}


def append_results(slug: str, row: dict) -> None:
    p = _results_path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(row) + "\n")


def load_results(slug: str, n: int | None = None) -> list[dict]:
    """All result rows, oldest first. n caps to the most recent n."""
    p = _results_path(slug)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-n:] if n else rows


def _calibration_path(slug: str) -> Path:
    # NOT calibrations.jsonl (plural) — those are orphaned legacy sim artifacts.
    return _REPO_ROOT / "rules" / slug / "vendor_calibration.jsonl"


def append_calibration(slug: str, rows: list[dict]) -> None:
    p = _calibration_path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def load_calibration(slug: str, n: int | None = None) -> list[dict]:
    """All vendor-calibration rows, oldest first. n caps to the most recent n."""
    p = _calibration_path(slug)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-n:] if n else rows


def vendor_accuracy(slug: str, last_n_slates: int = 10) -> list[dict]:
    """Per-vendor accuracy rollup over the most recent slates: slate count and
    mean proj/own MAE + match rate. Sorted best proj MAE first, None last."""
    rows = load_calibration(slug)
    if not rows:
        return []
    recent_slates = sorted({r.get("history_dir") or r.get("date") for r in rows})[-last_n_slates:]
    rows = [r for r in rows if (r.get("history_dir") or r.get("date")) in recent_slates]

    by_vendor: dict = {}
    for r in rows:
        by_vendor.setdefault(r.get("vendor") or "?", []).append(r)

    def _mean(vals: list, nd: int = 2):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals), nd) if vals else None

    def _tier_mean(vrows: list, field: str, tier: str):
        vals = [(r.get(field) or {}).get(tier) for r in vrows]
        return _mean([v for v in vals if v is not None])

    out = []
    for vendor, vrows in by_vendor.items():
        out.append({
            "vendor": vendor,
            "slates": len({r.get("history_dir") or r.get("date") for r in vrows}),
            "proj_mae": _mean([r.get("proj_mae") for r in vrows]),
            "own_mae": _mean([r.get("own_mae") for r in vrows]),
            "match_rate": _mean([r.get("match_rate") for r in vrows], 1),
            # By-ownership-tier (None for legacy rows lacking the field) — lets the
            # bundle say which vendor is sharpest on leverage vs chalk.
            "own_mae_leverage": _tier_mean(vrows, "own_mae_by_tier", "leverage"),
            "own_mae_chalk": _tier_mean(vrows, "own_mae_by_tier", "chalk"),
            "proj_mae_leverage": _tier_mean(vrows, "proj_mae_by_tier", "leverage"),
            "proj_mae_chalk": _tier_mean(vrows, "proj_mae_by_tier", "chalk"),
        })
    out.sort(key=lambda r: (r["proj_mae"] is None, r["proj_mae"]))
    return out


def latest_history_dir(slug: str) -> Path | None:
    """Newest archive dir (lexicographic on the dated name), or None."""
    root = _history_root(slug)
    if not root.exists():
        return None
    dirs = sorted(d for d in root.iterdir() if d.is_dir())
    return dirs[-1] if dirs else None


def archive_slate(
    slug: str,
    sport: str,
    contest_label: str,
    slate_label: str,
    autopsy_records: list[dict],
    roi_contests: list[dict],
    proj_source: str | None = None,
    shark_gap: dict | None = None,
) -> Path:
    """Archive the slate's artifacts + results. Returns the history dir.

    roi_contests rows: {name, type, source_file, field_size, my_entries,
    entry_fee, winnings (None if unreported), best_rank, best_percentile}.
    shark_gap: optional structural us-vs-sharks profile (from src.shark_gap).
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    root = _history_root(slug)
    hist_dir = root / slate_dirname(date_str, slate_label or contest_label)
    suffix = 2
    while hist_dir.exists():
        hist_dir = root / f"{slate_dirname(date_str, slate_label or contest_label)}__{suffix}"
        suffix += 1
    hist_dir.mkdir(parents=True)

    archived, missing = [], []
    for dest_name, src_fn in _ARCHIVE_SOURCES.items():
        src = src_fn(slug)
        if src.exists():
            shutil.copy2(src, hist_dir / dest_name)
            archived.append(dest_name)
        else:
            missing.append(dest_name)

    articles_dir = _REPO_ROOT / "articles" / slug
    article_files = (
        sorted(str(f.relative_to(_REPO_ROOT)) for f in articles_dir.glob("*") if f.is_file())
        if articles_dir.exists() else []
    )

    manifest = {
        "slug": slug,
        "sport": sport,
        "contest_label": contest_label,
        "date": date_str,
        "slate_label": slate_label or contest_label,
        "archived_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "archived": archived,
        "missing": missing,
        "article_files": article_files,
        "proj_source": proj_source,
    }
    (hist_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (hist_dir / "autopsy.json").write_text(json.dumps(autopsy_records, indent=2))

    # Self-grade: did our entered lineups / leverage bets actually pay off?
    # Graded deterministically against the structured actuals just archived.
    from src import accuracy
    acc = accuracy.slate_accuracy(autopsy_records)
    (hist_dir / "accuracy.json").write_text(json.dumps(acc, indent=2))

    # Structural shark-gap (did we play like the sharks, not just cash?).
    if shark_gap is not None:
        (hist_dir / "shark_gap.json").write_text(json.dumps(shark_gap, indent=2))

    contests_out = []
    for c in roi_contests:
        roi = compute_roi(c.get("entry_fee"), c.get("my_entries"), c.get("winnings"))
        contests_out.append({
            "name": c.get("name"),
            "type": c.get("type"),
            "source_file": c.get("source_file"),
            "field_size": c.get("field_size"),
            "my_entries": c.get("my_entries"),
            "entry_fee": c.get("entry_fee"),
            "buy_in": roi["buy_in"],
            "winnings": roi["winnings"],
            "roi_pct": roi["roi_pct"],
            "best_rank": c.get("best_rank"),
            "best_percentile": c.get("best_percentile"),
        })

    reported = [c for c in contests_out if c["winnings"] is not None]
    total_buy_in = round(sum(c["buy_in"] or 0.0 for c in contests_out), 2)
    reported_buy_in = round(sum(c["buy_in"] or 0.0 for c in reported), 2)
    total_winnings = round(sum(c["winnings"] for c in reported), 2) if reported else None
    slate_roi = (
        round((total_winnings - reported_buy_in) / reported_buy_in * 100.0, 1)
        if reported and reported_buy_in > 0 else None
    )
    percentiles = [c["best_percentile"] for c in contests_out if c["best_percentile"] is not None]
    ranks = [c["best_rank"] for c in contests_out if c["best_rank"] is not None]

    row = {
        "schema_version": 1,
        "date": date_str,
        "slug": slug,
        "sport": sport,
        "slate_label": slate_label or contest_label,
        "history_dir": str(hist_dir.relative_to(_REPO_ROOT)),
        "contests": contests_out,
        "total_buy_in": total_buy_in,
        "total_winnings": total_winnings,
        "roi_pct": slate_roi,
        "best_rank": min(ranks) if ranks else None,
        "best_percentile": min(percentiles) if percentiles else None,
        "entries_total": sum(int(c["my_entries"] or 0) for c in contests_out),
        # Self-grade summary (None when not gradable) — trended in the bundle.
        "edge_leverage_capture": acc["edges"].get("leverage_capture"),
        "edge_overperformer_capture": acc["edges"].get("overperformer_capture"),
        "edge_bust_exposure": acc["edges"].get("underperformer_exposure"),
        "lineup_avg_ratio": acc["lineups"].get("avg_ratio"),
        # Structural shark gap: the single biggest you-vs-shark delta this slate.
        "shark_gap_top": (
            {"dim": shark_gap["deltas"][0]["dim"], "delta": shark_gap["deltas"][0]["delta"]}
            if shark_gap and shark_gap.get("deltas") else None
        ),
    }
    (hist_dir / "results.json").write_text(json.dumps(row, indent=2))
    append_results(slug, row)
    return hist_dir
