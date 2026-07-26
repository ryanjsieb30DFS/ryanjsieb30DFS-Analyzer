"""Render an ARCHIVED slate's numbers from disk.

Why this exists: every numeric read the autopsy produces was either bound to the
uploader (so it vanished the moment the slate was cleared), or rendered once from
session state at log time (so it vanished on restart), or written to JSON and never
displayed at all. A user who asked "where is the breakdown?" after logging had no
way to find it — the answer was sitting in
`rules/<slug>/history/<dir>/{results,accuracy,adherence,pool_calibration,shark_gap,grader_validation}.json`
with nothing in the UI reading those files.

So this module takes a history directory and renders it, using the renderers that
already existed but were only ever pointed at live data:
  - src/adherence.py::adherence_md
  - src/pool_calibration.py::calibration_md
  - src/shark_gap.py::gap_md
plus a retro-grade renderer built here, because none existed.

Everything is read from disk, so a breakdown survives Clear, a Streamlit restart,
and moving on to the next slate — and any past slate stays browsable.

Pure functions, no Streamlit, so this is unit-testable.
"""
from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent


def _load(hist_dir: Path, name: str) -> dict | None:
    """One archived JSON file, or None when absent/unreadable. Archives from
    older app versions are missing files that newer ones write, so every section
    degrades independently rather than failing the whole breakdown."""
    try:
        p = Path(hist_dir) / name
        if not p.exists():
            return None
        loaded = json.loads(p.read_text())
        return loaded if isinstance(loaded, dict) else None
    except (json.JSONDecodeError, OSError):
        return None


def list_archives(slug: str) -> list[Path]:
    """Archived slate dirs for a slug, NEWEST FIRST.

    Names are `YYYY-MM-DD__slate-slug`, so a reverse lexicographic sort is
    chronological (matching history.latest_history_dir's assumption)."""
    root = _REPO_ROOT / "rules" / slug / "history"
    if not root.exists():
        return []
    return sorted((d for d in root.iterdir() if d.is_dir()),
                  key=lambda d: d.name, reverse=True)


def archive_label(hist_dir: Path) -> str:
    """Human label for a picker: the slate label plus when it was archived."""
    man = _load(hist_dir, "manifest.json") or {}
    label = man.get("slate_label") or Path(hist_dir).name
    when = man.get("archived_at") or man.get("date") or Path(hist_dir).name[:10]
    return f"{label}  ({when})"


def retro_grade_md(gv: dict | None) -> str | None:
    """Render grader_validation.json — the retro grade.

    This had NO renderer anywhere: `grader.retro_grade` ran at log time and its
    output went only to the archive and to a prompt block, so the user could
    never see whether the pre-lock checks actually predicted anything.

    The point of the retro grade is self-validation: it re-applies the same
    pre-lock gates to the ENTERED lineups against actual ownership, so flagged
    lineups should finish WORSE than clean ones. When they don't, the gates are
    miscalibrated — which is worth knowing and is what this surfaces."""
    if not gv or not gv.get("gradable"):
        return None
    lineups = gv.get("lineups") or []
    if not lineups:
        return None
    flagged = [l for l in lineups if l.get("flags")]
    clean = [l for l in lineups if not l.get("flags")]

    def _avg(rows):
        vals = [r["percentile"] for r in rows if r.get("percentile") is not None]
        return sum(vals) / len(vals) if vals else None

    out = [f"### Retro grade — did the pre-lock checks predict anything? "
           f"({len(lineups)} lineups)"]
    if not flagged:
        out.append(f"- **No lineup was flagged.** All {len(clean)} passed every "
                   f"pre-lock check.")
    else:
        fa, ca = _avg(flagged), _avg(clean)
        out.append(f"- **{len(flagged)} flagged**, {len(clean)} clean "
                   f"(lower percentile = better finish).")
        if fa is not None and ca is not None:
            verdict = ("the checks worked — flagged lineups finished worse"
                       if fa > ca else
                       "the checks did NOT work here — flagged lineups finished "
                       "BETTER, so the gates want recalibrating")
            out.append(f"- Flagged averaged **{fa:.1f}%ile**, clean averaged "
                       f"**{ca:.1f}%ile** — {verdict}.")
        seen: dict = {}
        for l in flagged:
            for f in l.get("flags") or []:
                msg = f.get("msg") if isinstance(f, dict) else str(f)
                seen[msg] = seen.get(msg, 0) + 1
        for msg, n in sorted(seen.items(), key=lambda kv: -kv[1])[:5]:
            out.append(f"  - {msg} *(×{n})*")
    return "\n".join(out)


def results_md(res: dict | None) -> str | None:
    """The headline: how each contest actually finished."""
    if not res:
        return None
    contests = res.get("contests") or []
    if not contests:
        return None
    out = [f"### How it finished — {res.get('slate_label') or 'this slate'}",
           "", "| Contest | Type | Field | Entries | Best rank | Finish |",
           "|---|---|---:|---:|---:|---:|"]
    for c in contests:
        pct = c.get("best_percentile")
        out.append(
            f"| {c.get('name') or c.get('source_file') or '—'} "
            f"| {c.get('type') or '—'} "
            f"| {(c.get('field_size') or 0):,} "
            f"| {c.get('my_entries') or 0} "
            f"| {c.get('best_rank') or '—'} "
            f"| {f'top {pct}%' if pct is not None else '—'} |")
    best = res.get("best_percentile")
    total = res.get("total_buy_in")
    tail = []
    if best is not None:
        tail.append(f"best finish across the slate: **top {best}%**")
    if total:
        tail.append(f"${total:,.0f} in")
    if res.get("entries_total"):
        tail.append(f"{res['entries_total']} entries")
    if tail:
        out += ["", "_" + " · ".join(tail) + "._"]
    return "\n".join(out)


def lineups_md(acc: dict | None) -> str | None:
    """Per-lineup finishes and how chalky each was."""
    if not acc:
        return None
    block = (acc.get("lineups") or {})
    rows = block.get("lineups") or []
    if not rows:
        return None
    out = ["### Your lineups", "", "| Entry | Points | Finish | Avg own |",
           "|---|---:|---:|---:|"]
    for r in sorted(rows, key=lambda r: (r.get("percentile") is None,
                                         r.get("percentile"))):
        pct = r.get("percentile")
        own = r.get("avg_own")
        out.append(
            f"| {r.get('entry_name') or '—'} "
            f"| {(r.get('points') or 0):.1f} "
            f"| {f'top {pct}%' if pct is not None else '—'} "
            f"| {f'{own:.1f}%' if own is not None else '—'} |")
    n_top = block.get("n_top_10pct")
    if n_top is not None:
        out += ["", f"_{n_top} of {len(rows)} finished in the top 10%._"]
    return "\n".join(out)


def breakdown_md(hist_dir) -> str:
    """The full numeric breakdown of one archived slate, as markdown.

    Sections degrade independently — an older archive missing a file simply
    omits that section rather than failing."""
    hist_dir = Path(hist_dir)
    if not hist_dir.exists():
        return "_That archived slate is missing from disk._"

    sections: list[str] = []
    sections.append(results_md(_load(hist_dir, "results.json")))
    sections.append(lineups_md(_load(hist_dir, "accuracy.json")))

    adh = _load(hist_dir, "adherence.json")
    if adh:
        try:
            from src.adherence import adherence_md
            sections.append(adherence_md(adh))
        except Exception:  # noqa: BLE001 — one bad section must not kill the view
            pass

    cal = _load(hist_dir, "pool_calibration.json")
    if cal:
        try:
            from src.pool_calibration import calibration_md
            sections.append(calibration_md(cal))
        except Exception:  # noqa: BLE001
            pass

    gap = _load(hist_dir, "shark_gap.json")
    if gap:
        try:
            from src.shark_gap import gap_md
            sections.append(gap_md(gap))
        except Exception:  # noqa: BLE001
            pass

    sections.append(retro_grade_md(_load(hist_dir, "grader_validation.json")))

    body = [s for s in sections if s]
    if not body:
        return ("_No archived numbers for this slate — it predates the breakdown, "
                "or the log did not complete._")
    return "\n\n".join(body)


def has_review(hist_dir) -> bool:
    return (Path(hist_dir) / "autopsy_review.md").exists()


def review_md(hist_dir) -> str | None:
    p = Path(hist_dir) / "autopsy_review.md"
    try:
        return p.read_text() if p.exists() else None
    except OSError:
        return None
