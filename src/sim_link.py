"""Sim → Analyzer integration (the read side of the sibling-repo bridge).

The Sim tool (~/Desktop/Repo/ryanjsieb30DFS) builds and simulates; this module
lets the Analyzer READ two of its artifacts, degrading gracefully (every helper
returns None/{} when the Sim repo or file is absent — no exceptions, no UI):

1. `data/sim_entries/<slug>.json` — the selected portfolio the Sim pushes via
   its "📨 Send entries to Analyzer Grade tab" button: player names + headline
   sim metrics (Win%/Top1%/Cash%/ROI) per entry. The ✅ Grade tab one-click
   loads it into the lineup box, replacing the hand-paste. (This file lives in
   THIS repo — the Sim writes across; cleared with the slate.)

2. The Sim's field-concentration corpus + fitted field params — used to
   correct the grader's expected-dupes estimate. The naive independence
   product (Π own × field size) over-predicts real duplication by 1-2 orders
   of magnitude (real fields are far less combinatorially spread than
   independence assumes on the DOWN side, and dupe magnets concentrate on the
   up side); the corpus carries observed top-dupe counts paired with exactly
   that naive prediction, so the correction factor is measured, not assumed.

The Analyzer still never builds lineups; both reads are grade/analysis inputs.
"""
from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
_SIM_ENTRIES_DIR = _REPO_ROOT / "data" / "sim_entries"
_SIM_ROOT = Path.home() / "Desktop" / "Repo" / "ryanjsieb30DFS"


def sim_root() -> Path | None:
    """The sibling Sim repo, or None when it isn't on this machine."""
    return _SIM_ROOT if _SIM_ROOT.exists() else None


# ---------------------------------------------------------------------------
# Entry-set hand-off (Sim Portfolio → Grade tab)
# ---------------------------------------------------------------------------

def load_sim_entries(slug: str) -> dict | None:
    """The Sim-pushed entry set for this slug, or None (absent/unreadable)."""
    path = _SIM_ENTRIES_DIR / f"{slug}.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    return payload if payload.get("entries") else None


def entries_as_grade_text(payload: dict) -> str:
    """The pushed entries in the Grade tab's paste format: one lineup per
    line, players comma-separated."""
    return "\n".join(
        ", ".join(e.get("players") or [])
        for e in (payload.get("entries") or [])
        if e.get("players")
    )


def sim_metrics_md(payload: dict) -> str:
    """Markdown table of the pushed entries' sim metrics — shown beside the
    grade so the deterministic checks and the sim's own numbers sit together.
    Empty string when no entry carries metrics."""
    entries = [e for e in (payload.get("entries") or []) if e.get("win_pct") is not None]
    if not entries:
        return ""
    lines = [
        "| # | Contest | Win % | Top 1% | Cash % | Sim ROI |",
        "| ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for i, e in enumerate(entries, start=1):
        lines.append(
            f"| {i} | {e.get('contest', '?')} | {e.get('win_pct', 0):.2f}% "
            f"| {e.get('top1_pct', 0):.1f}% | {e.get('cash_pct', 0):.1f}% "
            f"| {e.get('roi_pct', 0):.0f}% |"
        )
    return "\n".join(lines)


def clear_sim_entries(slug: str) -> None:
    """Slate-scoped cleanup — called wherever the slate clears."""
    path = _SIM_ENTRIES_DIR / f"{slug}.json"
    if path.exists():
        path.unlink()


# ---------------------------------------------------------------------------
# Corpus-corrected dupe estimate (grader)
# ---------------------------------------------------------------------------

_SLUG_SPORT = {"pga_classic": "golf", "pga_rd4_sd": "golf",
               "mma_se": "mma", "nascar": "nascar"}
_dupe_cache: dict = {}


def dupe_correction(slug: str, field_size: int | None) -> float | None:
    """Measured correction factor for the naive independence dupe estimate:
    median(observed top-dupe count / naive prediction) over the Sim corpus's
    contests of this sport in the same field-size band. None when the corpus
    is absent or thin (<3 evidence rows) — caller keeps the naive number.

    Honest caveat: the evidence rows are the MOST-duplicated rosters per
    contest, so the factor is calibrated for chalky lineups — exactly the
    ones whose dupe risk the Grade tab needs to price."""
    sport = _SLUG_SPORT.get(slug)
    root = sim_root()
    if sport is None or root is None or not field_size:
        return None
    band = ("small" if field_size <= 2_500 else
            "mid" if field_size <= 10_000 else "large")
    key = (sport, band)
    if key in _dupe_cache:
        return _dupe_cache[key]
    corpus = root / "data" / "field_corpus" / "field_concentration.jsonl"
    if not corpus.exists():
        return None
    lo, hi = {"small": (0, 2_500), "mid": (2_500, 10_000),
              "large": (10_000, float("inf"))}[band]
    ratios: list[float] = []
    try:
        for line in corpus.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if "skipped" in r or r.get("sport") != sport:
                continue
            n = r.get("n_entries") or 0
            if not (lo < n <= hi):
                continue
            for ev in r.get("top_dupe_evidence") or []:
                prod = ev.get("own_product")
                if prod and prod > 0 and ev.get("count"):
                    naive = prod * n
                    if naive > 0:
                        ratios.append(ev["count"] / naive)
    except (json.JSONDecodeError, OSError):
        return None
    if len(ratios) < 3:
        result = None
    else:
        ratios.sort()
        result = round(ratios[len(ratios) // 2], 4)
    _dupe_cache[key] = result
    return result


# ---------------------------------------------------------------------------
# Slate captures (the Sim's full-field records) → autopsy field learning
# ---------------------------------------------------------------------------

def find_sim_capture(slug: str, n_entries: int | None) -> dict | None:
    """The Sim's full-slate capture for the contest being autopsied, matched
    by exact entry count (both tools parsed the same standings CSV, so the
    counts agree). None when the Sim repo/captures are absent."""
    root = sim_root()
    if root is None or not n_entries:
        return None
    d = root / "rules" / slug / "slate_data"
    if not d.exists():
        return None
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if ((rec.get("field") or {}).get("summary") or {}).get("n_entries") == n_entries:
            return rec
    return None


def capture_field_stats(slug: str, n_entries: int | None) -> dict | None:
    """Roster-level field structure for an autopsied contest, from the Sim's
    capture: real dupe stats + entries-per-user + (MMA, when the capture
    carries opponents) the DEAD-STRUCTURE share — entries rostering both
    fighters of a bout, whose combined ceiling is capped by the bout being
    zero-sum. This is the evidence the standings-only autopsy can't see:
    it knows scores and ownership, not the joint roster structure."""
    cap = find_sim_capture(slug, n_entries)
    if cap is None:
        return None
    field = cap.get("field") or {}
    s = field.get("summary") or {}
    stats = {
        "capture": cap.get("slate_name"),
        "unique_pct": s.get("unique_pct"),
        "max_dupe": s.get("max_dupe"),
        "top_dupes": (s.get("top_dupes") or [])[:5],
        "pct_single_entry_users": (s.get("entries_per_user") or {}).get("pct_single"),
        "mean_entries_per_user": (s.get("entries_per_user") or {}).get("mean"),
        "top3_chalk_lineup_pct": (s.get("chalk_share") or {}).get("top3_lineup_pct"),
    }
    # Dead-structure share (MMA): opponent info arrived in captures 7/26+.
    try:
        from src.autopsy import _norm_name
        opp = {}
        for pl in cap.get("players") or []:
            o = pl.get("opponent")
            if o and pl.get("name"):
                opp[_norm_name(str(pl["name"]))] = _norm_name(str(o))
        if opp:
            index = [_norm_name(str(n)) for n in field.get("player_index") or []]
            dead = total = 0
            for roster, count in zip(field.get("rosters") or [],
                                     field.get("counts") or []):
                names = {index[i] for i in roster if i < len(index)}
                total += count
                if any(opp.get(n) in names for n in names):
                    dead += count
            if total:
                stats["dead_structure_pct"] = round(100.0 * dead / total, 1)
    except Exception:  # noqa: BLE001 — enhancement only
        pass
    return stats


def capture_stats_md(stats: dict) -> str:
    """One-glance markdown for the autopsy panel."""
    bits = []
    if stats.get("unique_pct") is not None:
        bits.append(f"**{stats['unique_pct']:.0f}%** unique rosters")
    if stats.get("max_dupe") is not None:
        bits.append(f"top roster duped **{stats['max_dupe']}×**")
    if stats.get("pct_single_entry_users") is not None:
        bits.append(f"**{stats['pct_single_entry_users']:.0f}%** single-entry users")
    if stats.get("mean_entries_per_user") is not None:
        bits.append(f"~{stats['mean_entries_per_user']:.1f} entries/user")
    if stats.get("top3_chalk_lineup_pct") is not None:
        bits.append(f"**{stats['top3_chalk_lineup_pct']:.0f}%** of entries carry all top-3 chalk")
    if stats.get("dead_structure_pct") is not None:
        bits.append(f"**{stats['dead_structure_pct']:.0f}%** dead structure "
                    "(opponent-stacked entries — capped ceiling by construction)")
    return " · ".join(bits)
