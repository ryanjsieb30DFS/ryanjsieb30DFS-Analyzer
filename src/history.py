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
    "player_pool.md": lambda slug: _REPO_ROOT / "data" / "player_pool" / f"{slug}.md",
    "bundle.md": lambda slug: _REPO_ROOT / "data" / "bundle" / f"{slug}.md",
    "contests.json": lambda slug: _REPO_ROOT / "data" / "contests" / f"{slug}.json",
    "strategy_contract.json": lambda slug: _REPO_ROOT / "data" / "strategy_contract" / f"{slug}.json",
    "sim_analysis.md": lambda slug: _REPO_ROOT / "data" / "sim_analysis" / f"{slug}.md",
    "sim_pool.csv": lambda slug: _REPO_ROOT / "data" / "sim_data" / f"{slug}__pool.csv",
    "lineup_grade.md": lambda slug: _REPO_ROOT / "data" / "grade" / f"{slug}.md",
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


def logged_contest_ids(slug: str) -> set[str]:
    """DK contest-instance ids already logged to rules/<slug>/autopsy_data.jsonl —
    the write-time dedup set. Logging skips a contest whose id is here, so an
    accidental second 'Log autopsy' of the same standings never double-counts the
    results ledger or the autopsy history. Legacy rows without an id contribute
    nothing (they can't be safely matched)."""
    p = _REPO_ROOT / "rules" / slug / "autopsy_data.jsonl"
    if not p.exists():
        return set()
    out: set[str] = set()
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            cid = json.loads(line).get("contest_id")
        except json.JSONDecodeError:
            continue
        if cid:
            out.add(str(cid))
    return out


def process_trend_block(slug: str, n: int = 5) -> str | None:
    """Forward-feed block for the slate bundle: the last n slates' PROCESS trend
    from results.jsonl — best percentile, leverage capture, bust exposure, and the
    recurring shark-gap axis. This is the read-back that makes the self-grade a
    learning loop instead of a per-slate display: 'leverage capture 0% two slates
    running' should shape the next strategy. None until ≥2 slates exist.
    Descriptive only — mirrors field_tendencies.bundle_block."""
    rows = load_results(slug, n)
    if len(rows) < 2:
        return None

    def _seq(field, fmt="{:.0f}"):
        vals = [(r.get(field)) for r in rows]
        return " → ".join("—" if v is None else fmt.format(v) for v in vals)

    def _pct_seq(field):
        vals = [r.get(field) for r in rows]
        return " → ".join("—" if v is None else f"{v * 100:.0f}%" for v in vals)

    lines = [
        "## Process trend — your last %d slates (oldest → newest)" % len(rows),
        "FORWARD-LOOKING self-grade from results.jsonl. Read the SEQUENCES, not one "
        "slate: a recurring weakness (leverage capture repeatedly 0%, bust exposure "
        "climbing, the same shark-gap axis) is a process leak the strategy below "
        "should account for. GPP guard: one bad percentile is variance, not signal.",
        f"- **Best percentile:** {_seq('best_percentile', '{:.1f}')}",
        f"- **Leverage capture** (slate-defining low-owned plays we rostered): "
        f"{_pct_seq('edge_leverage_capture')}",
        f"- **Bust exposure** (top underperformers we rostered): "
        f"{_pct_seq('edge_bust_exposure')}",
    ]
    gaps = [r.get("shark_gap_top", {}).get("dim") for r in rows
            if isinstance(r.get("shark_gap_top"), dict)]
    if gaps:
        from collections import Counter
        dim, cnt = Counter(gaps).most_common(1)[0]
        if cnt >= 2:
            lines.append(f"- **Recurring shark-gap axis:** `{dim}` was your biggest "
                         f"structural gap vs the pros in {cnt} of the last {len(rows)} "
                         f"slates.")
    adh = [r.get("adherence_fades_violated") for r in rows
           if r.get("adherence_fades_violated") is not None]
    if adh:
        lines.append(f"- **Own-strategy adherence:** fade calls violated per slate: "
                     f"{' → '.join(str(a) for a in adh)} (0 = you followed your own fades).")
    ordered = [r.get("tiers_ordered") for r in rows if r.get("tiers_ordered") is not None]
    if ordered:
        held = sum(1 for o in ordered if o)
        lines.append(f"- **Player-pool tier calibration:** tier ordering held in "
                     f"{held} of {len(ordered)} graded slates"
                     + (" — the board's boundaries are suspect." if held < len(ordered) else "."))
    # Grader self-validation: pool the per-lineup outcomes across slates. Only
    # meaningful once BOTH buckets have a few lineups.
    fl, cl = [], []
    for r in rows:
        gc = r.get("grader_check") or {}
        fl += gc.get("flagged_pctiles") or []
        cl += gc.get("clean_pctiles") or []
    if len(fl) >= 3 and len(cl) >= 3:
        med = lambda v: sorted(v)[len(v) // 2]  # noqa: E731
        lines.append(f"- **Grader validation:** lineups the pre-lock checks would flag "
                     f"finished median {med(fl):.1f}%ile (n={len(fl)}) vs clean "
                     f"{med(cl):.1f}%ile (n={len(cl)}) — "
                     + ("the checks are earning their keep." if med(fl) > med(cl)
                        else "flags are NOT predicting worse finishes; recalibrate."))
    return "\n".join(lines)


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
    adherence: dict | None = None,
    pool_calibration: dict | None = None,
    grader_validation: dict | None = None,
) -> Path:
    """Archive the slate's artifacts + results. Returns the history dir.

    roi_contests rows: {name, type, source_file, field_size, my_entries,
    entry_fee, winnings (None if unreported), best_rank, best_percentile}.
    shark_gap: optional structural us-vs-sharks profile (from src.shark_gap).
    adherence: optional own-strategy adherence grade (from src.adherence).
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

    # Own-strategy adherence (did we follow our own fades / leverage calls?).
    if adherence is not None:
        (hist_dir / "adherence.json").write_text(json.dumps(adherence, indent=2))

    # Player-pool tier calibration (did the board's tiers hold up?).
    if pool_calibration is not None:
        (hist_dir / "pool_calibration.json").write_text(
            json.dumps(pool_calibration, indent=2))

    # Grader self-validation (do flagged lineups actually finish worse?).
    if grader_validation is not None:
        (hist_dir / "grader_validation.json").write_text(
            json.dumps(grader_validation, indent=2))

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
        # Own-strategy adherence summary (None when not gradable) — trended in
        # process_trend_block so a recurring discipline leak surfaces pre-slate.
        "adherence_fades_violated": (
            adherence.get("fades_violated") if adherence and adherence.get("gradable") else None
        ),
        "adherence_leverage_covered": (
            f"{adherence['leverage_covered']}/{adherence['leverage_of']}"
            if adherence and adherence.get("gradable") and adherence.get("leverage_of")
            else None
        ),
        # Pool tier calibration summary (None when not gradable) — trended.
        "tier_summary": (pool_calibration.get("summary")
                         if pool_calibration and pool_calibration.get("gradable") else None),
        "tiers_ordered": (pool_calibration.get("tiers_ordered")
                          if pool_calibration and pool_calibration.get("gradable") else None),
        # Grader self-validation: per-lineup finish pctiles split by whether the
        # calibrated pre-lock checks would have flagged them. Accumulates the
        # evidence that validates (or corrects) the grader's thresholds.
        "grader_check": (
            {"flagged_pctiles": grader_validation["flagged_pctiles"],
             "clean_pctiles": grader_validation["clean_pctiles"]}
            if grader_validation and grader_validation.get("gradable") else None
        ),
    }
    (hist_dir / "results.json").write_text(json.dumps(row, indent=2))
    append_results(slug, row)
    return hist_dir
