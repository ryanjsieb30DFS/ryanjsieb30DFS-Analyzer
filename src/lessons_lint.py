"""Lesson-ledger integrity lint (9/19/26).

`lint_lessons(slug)` returns ERROR strings (empty = clean). It runs as the
post-check of the post-autopsy review (`analysis_runner._run_claude(...,
post_check=...)`): any error rolls the review back, exactly like a YAML parse
failure. `lint_warnings(slug)` returns soft findings (legacy ids) that never
fail a run. `rot_report` lists hypotheses nobody has checked.

Schema (as the six ledgers actually use it): each lesson has id / born /
origin / statement / status / confirmations[] / contradictions[] /
codified_in / retired_reason. An evidence entry carries `date` plus a
history pointer under ONE of `history_dir` (nfl_classic, nascar),
`origin_dir` (mma_se), `history` (nfl_sd) — or, in the older PGA / MMA
entries, just a `slate` label. All four spellings are accepted; a
dateless entry, or one with none of them, is an error.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent

LIFECYCLE = ("hypothesis", "validated", "codified", "retired")
_HISTORY_KEYS = ("history_dir", "origin_dir", "history", "slate")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# New-lesson id convention: <slug-with-dashes>-YYYY-MM-DD-<short-kebab>.
_DATED_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")


def _date(v) -> datetime | None:
    s = str(v or "").strip()
    if not _DATE_RE.match(s):
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return None


def lint_lessons_list(lessons: list[dict]) -> list[str]:
    """Errors for an already-loaded lessons list."""
    errs: list[str] = []
    seen: dict[str, int] = {}
    for i, l in enumerate(lessons):
        if not isinstance(l, dict):
            errs.append(f"lesson #{i + 1} is not a mapping")
            continue
        lid = str(l.get("id") or "").strip()
        tag = lid or f"lesson #{i + 1}"
        if not lid:
            errs.append(f"{tag}: missing id")
        elif lid in seen:
            errs.append(f"{tag}: duplicate id (also lesson #{seen[lid] + 1})")
        else:
            seen[lid] = i
        status = l.get("status")
        if status not in LIFECYCLE:
            errs.append(f"{tag}: status {status!r} not in {list(LIFECYCLE)}")
        born = _date(l.get("born"))
        if born is None:
            errs.append(f"{tag}: born {l.get('born')!r} is not YYYY-MM-DD")
        if status == "codified" and not str(l.get("codified_in") or "").strip():
            errs.append(f"{tag}: codified but codified_in is empty")
        for kind in ("confirmations", "contradictions"):
            entries = l.get(kind)
            if entries is None:
                continue
            if not isinstance(entries, list):
                errs.append(f"{tag}: {kind} is not a list")
                continue
            for k, e in enumerate(entries):
                if not isinstance(e, dict):
                    errs.append(f"{tag}: {kind}[{k}] is not a mapping")
                    continue
                d = _date(e.get("date"))
                if d is None:
                    errs.append(f"{tag}: {kind}[{k}] has no YYYY-MM-DD date")
                elif born is not None and d < born:
                    errs.append(f"{tag}: {kind}[{k}] dated {e.get('date')} before born {l.get('born')}")
                if not any(str(e.get(h) or "").strip() for h in _HISTORY_KEYS):
                    errs.append(f"{tag}: {kind}[{k}] has no history_dir "
                                f"(or origin_dir / history / slate)")
    return errs


def lint_lessons(slug: str) -> list[str]:
    """Errors for rules/<slug>/lessons.yaml (empty list = clean; a missing
    ledger is clean; an unparseable one is a single error)."""
    p = _REPO_ROOT / "rules" / slug / "lessons.yaml"
    if not p.exists():
        return []
    try:
        import yaml
        data = yaml.safe_load(p.read_text()) or {}
    except Exception as e:  # noqa: BLE001
        return [f"lessons.yaml does not parse: {e}"]
    lessons = data.get("lessons")
    if lessons is None:
        return []
    if not isinstance(lessons, list):
        return ["`lessons:` is not a list"]
    return lint_lessons_list(lessons)


def is_dated_slug_id(lid: str) -> bool:
    return bool(_DATED_ID_RE.match(str(lid or "")))


def lint_warnings(slug: str) -> list[str]:
    """Soft findings — never fail a run. Today: legacy ids that don't follow
    the dated-slug convention (nfl_classic_te_bring_back style). Existing ids
    are NEVER renamed (codified_in and cross-links point at them)."""
    from src.ledger_hygiene import load_lessons
    out = []
    for l in load_lessons(slug):
        lid = str(l.get("id") or "")
        if lid and not is_dated_slug_id(lid):
            out.append(f"{lid}: legacy id (new lessons use "
                       f"{slug.replace('_', '-')}-YYYY-MM-DD-<short-kebab>)")
    return out


def rot_report(slug: str, results_jsonl=None, min_slates: int = 3) -> list[dict]:
    """Hypothesis lessons with ZERO confirmations and ZERO contradictions that
    have sat through >= min_slates logged slates since they were born — ideas
    nobody has checked. `results_jsonl` is a path to a results.jsonl (default:
    the sport's own) or an already-loaded list of rows."""
    import json
    from src.ledger_hygiene import load_lessons, _born_dt, _slates_since
    if isinstance(results_jsonl, list):
        rows = results_jsonl
    else:
        p = Path(results_jsonl) if results_jsonl else _REPO_ROOT / "rules" / slug / "results.jsonl"
        rows = []
        if p.exists():
            for line in p.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    out = []
    for l in load_lessons(slug):
        if l.get("status") != "hypothesis":
            continue
        if (l.get("confirmations") or []) or (l.get("contradictions") or []):
            continue
        n = _slates_since(_born_dt(l), rows)
        if n >= min_slates:
            out.append({"id": l.get("id"), "born": l.get("born"), "slates_since": n,
                        "statement": " ".join(str(l.get("statement") or "").split())})
    out.sort(key=lambda r: -r["slates_since"])
    return out


def rot_report_md(rows: list[dict]) -> str:
    if not rows:
        return "_Every open idea has been checked at least once — nothing is rotting._"
    out = ["Ideas still being tested (hypothesis lessons) that no review has confirmed "
           "OR contradicted, even though 3+ slates have been logged since they were "
           "written. The next review must give each one a verdict or retire it."]
    for r in rows:
        stmt = r["statement"] if len(r["statement"]) <= 160 else r["statement"][:159] + "…"
        out.append(f"- `{r['id']}` — born {r['born']}, {r['slates_since']} slates since — {stmt}")
    return "\n".join(out)
