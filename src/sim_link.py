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
   correct the grader's expected-dupes estimate. The naive independence product
   (Π own × field size) UNDER-predicts real duplication, because entrants
   converge on the same chalk rosters rather than drawing players independently;
   measured over the Sim's corpus every factor is > 1 (MMA 1.7-4.2x, NASCAR
   3.1-6.6x, golf far too dispersed to use). The corpus carries observed
   top-dupe counts paired with exactly that naive prediction, so the correction
   factor is measured, not assumed.

3. The Sim's full-slate captures — roster-level field structure for the autopsy.

The Analyzer still never builds lineups; every read is a grade/analysis input.

The Sim repo's location can be overridden with the DFS_SIM_ROOT environment
variable; it otherwise defaults to the sibling checkout path.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
_SIM_ENTRIES_DIR = _REPO_ROOT / "data" / "sim_entries"
_SIM_ROOT = Path.home() / "Desktop" / "Repo" / "ryanjsieb30DFS"


def sim_root() -> Path | None:
    """The sibling Sim repo, or None when it isn't on this machine.

    Honors $DFS_SIM_ROOT so a moved/renamed checkout doesn't silently take every
    bridge read down with it — without the override the only symptom was panels
    quietly going missing."""
    env = os.environ.get("DFS_SIM_ROOT")
    if env:
        p = Path(env).expanduser()
        return p if p.exists() else None
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

_SLUG_SPORT = {"pga_classic": "golf", "pga_rd4_sd": "golf_showdown",
               "mma_se": "mma", "nascar": "nascar"}

# Sports whose corpus evidence is tight enough to correct a user-facing number.
# Measured over the Sim's 577-contest corpus (7/25/26), median observed/naive by
# band, with the p10-p90 spread:
#   mma     1.7 - 4.2   (p10 0.95, p90 ~13)     → usable
#   nascar  3.1 - 6.6   (p10 1.24, p90 ~90)     → usable
#   golf   13.9 - 69.8  (p10 3.7,  p90 5,760)   → NOT usable
# Golf's ratio spans three-plus orders of magnitude because it is strongly
# scale-dependent (~3,099x in the lowest own-product quartile vs ~5x in the
# chalkiest), so a single median is not a defensible multiplier for a pre-lock
# decision input — it over-corrected chalk ~13x. Golf keeps the naive number
# until the factor is bucketed by own_product. `golf_showdown` is listed above
# only so RD4 SD (6 golfers, tiny field) can never silently inherit a full-field
# PGA Classic multiplier, which it did until 7/25/26.
_CORRECTABLE_SPORTS = {"mma", "nascar"}
_dupe_cache: dict = {}


def dupe_correction(slug: str, field_size: int | None) -> float | None:
    """Measured correction factor for the naive independence dupe estimate:
    median(observed top-dupe count / naive prediction) over the Sim corpus's
    contests of this sport in the same field-size band. None when the corpus is
    absent, thin (<3 evidence rows), or the sport's evidence is too dispersed to
    trust (see `_CORRECTABLE_SPORTS`) — caller keeps the naive number.

    Direction: every measured factor is **> 1**. Real fields duplicate consensus
    rosters MORE than per-player independence predicts, because entrants
    converge on the same chalk rosters. (Comments here and in grader.py used to
    claim the opposite — "naive over-predicts, observed ~0.01-0.09x" — which was
    backwards and would have argued for shrinking an already-low estimate.)

    Honest caveat: the evidence rows are the MOST-duplicated rosters per
    contest, so the factor is calibrated for chalky lineups — exactly the
    ones whose dupe risk the Grade tab needs to price."""
    sport = _SLUG_SPORT.get(slug)
    root = sim_root()
    if sport is None or sport not in _CORRECTABLE_SPORTS or root is None \
            or not field_size:
        return None
    band = ("small" if field_size <= 2_500 else
            "mid" if field_size <= 10_000 else "large")
    corpus = root / "data" / "field_corpus" / "field_concentration.jsonl"
    if not corpus.exists():
        return None
    # Key the cache on the corpus mtime too: a long-running Streamlit process
    # otherwise kept serving a stale factor after the Sim backfilled new
    # contests, and the whole point is that the number is measured.
    try:
        stamp = corpus.stat().st_mtime_ns
    except OSError:
        return None
    key = (sport, band, stamp)
    if key in _dupe_cache:
        return _dupe_cache[key]
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

CAPTURE_SCHEMA_VERSION = 1

# Set when a capture was found but couldn't be trusted, so the UI can say
# "the bridge is degraded" instead of looking identical to "no Sim repo".
capture_warnings: dict = {}


def find_sim_capture(slug: str, n_entries: int | None,
                     contest_id: str | None = None) -> dict | None:
    """The Sim's full-slate capture for the contest being autopsied.

    Matched on `contest_id` FIRST, falling back to exact entry count. The count
    fallback assumes both tools parsed the same standings CSV and agree — true
    for a clean file, but two contests on one slate can have equal entry counts
    (then the alphabetically-first file silently won), and any row the Analyzer
    drops that the Sim kept breaks the match entirely.

    Captures are validated against CAPTURE_SCHEMA_VERSION: a newer capture whose
    block semantics changed would otherwise be read as v1 and quietly produce
    wrong numbers. Rejections land in `capture_warnings[slug]`."""
    root = sim_root()
    if root is None:
        return None
    if not n_entries and not contest_id:
        return None
    capture_warnings.pop(slug, None)
    d = root / "rules" / slug / "slate_data"
    if not d.exists():
        return None
    by_count = None
    drifted: list = []
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(rec, dict):
            continue
        ver = rec.get("schema_version", CAPTURE_SCHEMA_VERSION)
        if not isinstance(ver, int) or ver > CAPTURE_SCHEMA_VERSION:
            drifted.append(f"{p.name} (schema v{ver})")
            continue
        if contest_id and str(rec.get("contest_id") or "") == str(contest_id):
            return rec
        if by_count is None and n_entries and (
                ((rec.get("field") or {}).get("summary") or {}
                 ).get("n_entries") == n_entries):
            by_count = rec
    if drifted:
        capture_warnings[slug] = (
            "Sim capture(s) were written by a newer build than this Analyzer "
            "understands and were skipped rather than misread: "
            + ", ".join(drifted[:3]))
    return by_count


def capture_field_stats(slug: str, n_entries: int | None,
                        contest_id: str | None = None) -> dict | None:
    """Roster-level field structure for an autopsied contest, from the Sim's
    capture: real dupe stats + entries-per-user + (MMA, when the capture
    carries opponents) the DEAD-STRUCTURE share — entries rostering both
    fighters of a bout, whose combined ceiling is capped by the bout being
    zero-sum. This is the evidence the standings-only autopsy can't see:
    it knows scores and ownership, not the joint roster structure."""
    cap = find_sim_capture(slug, n_entries, contest_id=contest_id)
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
    # Dead-structure share (MMA): entries rostering both fighters of a bout.
    # Needs a per-player `opponent` in the capture, which older captures don't
    # carry. Say so rather than silently omitting the panel — a bare
    # `except: pass` here meant the feature staying dark was indistinguishable
    # from it having nothing to report.
    rosters = field.get("rosters") or []
    counts = field.get("counts") or []
    if len(rosters) != len(counts):
        stats["dead_structure_note"] = (
            f"capture has {len(rosters)} rosters but {len(counts)} counts — "
            f"skipping roster-level math rather than truncating it")
        return stats
    try:
        from src.autopsy import _norm_name
        opp = {}
        for pl in cap.get("players") or []:
            o = pl.get("opponent")
            if o and pl.get("name"):
                opp[_norm_name(str(pl["name"]))] = _norm_name(str(o))
        if not opp:
            stats["dead_structure_note"] = (
                "this capture carries no per-fighter opponent, so the "
                "dead-structure share can't be computed for it")
        else:
            index = [_norm_name(str(n)) for n in field.get("player_index") or []]
            dead = total = 0
            for roster, count in zip(rosters, counts):
                names = {index[i] for i in roster if i < len(index)}
                total += count
                if any(opp.get(n) in names for n in names):
                    dead += count
            if total:
                stats["dead_structure_pct"] = round(100.0 * dead / total, 1)
    except Exception as exc:  # noqa: BLE001 — enhancement only, but never silent
        stats["dead_structure_note"] = (
            f"dead-structure share unavailable ({type(exc).__name__})")
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
    out = " · ".join(bits)
    # Say WHY a metric is missing. Otherwise a capture too old to carry
    # opponents looks exactly like a slate with nothing to report.
    if stats.get("dead_structure_note"):
        out += (("  \n" if out else "")
                + f"_Dead-structure share: {stats['dead_structure_note']}._")
    return out
