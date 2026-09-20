"""Trimmed, generated views of the learning ledgers for the headless runs.

The strategy and player-pool prompts used to point Claude at the FULL
`rules/<slug>/lessons.yaml` (40-50 lessons, most already codified into
framework.md or retired) and the FULL `rules/<slug>/autopsies.md` (dozens of
entries). Both files keep growing; the runs kept getting slower and the open
lessons kept getting buried. These two writers render what the runs actually
need (9/19/26):

  - `rules/<slug>/lessons_open.md`   — hypothesis + validated lessons only
    (id, born, statement, evidence counts, latest note) plus a bare list of
    codified ids so the strategy contract's `from: <lesson id>` still resolves.
  - `rules/<slug>/autopsies_recent.md` — the last N `## ` entries of
    autopsies.md, newest last, verbatim.

Both are regenerated before every strategy / pool / review run
(`analysis_runner.refresh_trimmed_views`) and are gitignored: derived files,
never edited by hand. The review run still edits lessons.yaml directly.
"""
from __future__ import annotations

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
OPEN_STATUSES = ("hypothesis", "validated")


def _rules_dir(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug


def _one_line(text, n: int = 400) -> str:
    t = " ".join(str(text or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def _latest_note(lesson: dict) -> str | None:
    """The newest confirmation/contradiction note, tagged with its kind."""
    best = None
    for kind in ("confirmations", "contradictions"):
        for e in lesson.get(kind) or []:
            if not isinstance(e, dict):
                continue
            d = str(e.get("date") or "")
            if best is None or d > best[0]:
                best = (d, kind[:-1], _one_line(e.get("note"), 300))
    if best is None:
        return None
    return f"{best[1]} {best[0]}: {best[2]}" if best[2] else f"{best[1]} {best[0]}"


def render_open_lessons(lessons: list[dict], slug: str) -> str:
    """Markdown for the open-lessons view (pure function; see write_open_lessons)."""
    open_l = [l for l in lessons if l.get("status") in OPEN_STATUSES]
    codified = [l for l in lessons if l.get("status") == "codified"]
    out = [f"# Open lessons — {slug} (generated from lessons.yaml, do not edit)",
           "",
           f"{len(open_l)} open lesson(s): ideas still being tested (hypothesis) or "
           f"proven but not yet written into framework.md (validated). Apply each one "
           f"whose mechanism fits THIS slate; silently drop the rest. Codified lessons "
           f"already live in framework.md / philosophy.md; retired ones are gone.",
           ""]
    for l in open_l:
        conf = len(l.get("confirmations") or [])
        contra = len(l.get("contradictions") or [])
        out.append(f"## {l.get('id')}")
        out.append(f"- status: {l.get('status')} · born: {l.get('born')} · "
                   f"confirmations: {conf} · contradictions: {contra}")
        out.append(f"- statement: {_one_line(l.get('statement'), 900)}")
        note = _latest_note(l)
        if note:
            out.append(f"- latest note: {note}")
        out.append("")
    out.append("## Codified lesson ids (for the strategy contract's `from:` field)")
    out.append("The rule text for each lives where `codified_in` points.")
    if not codified:
        out.append("- none")
    for l in codified:
        out.append(f"- `{l.get('id')}` — {_one_line(l.get('codified_in'), 160) or 'framework.md'}")
    out.append("")
    return "\n".join(out)


def write_open_lessons(slug: str) -> Path | None:
    """Regenerate rules/<slug>/lessons_open.md. Returns the path, or None when
    the sport has no ledger (nothing is written)."""
    from src.ledger_hygiene import load_lessons
    if not (_rules_dir(slug) / "lessons.yaml").exists():
        return None
    lessons = load_lessons(slug)
    path = _rules_dir(slug) / "lessons_open.md"
    path.write_text(render_open_lessons(lessons, slug))
    return path


def recent_autopsy_entries(text: str, n: int = 6) -> str:
    """The preamble (everything before the first `## ` entry) plus the LAST n
    `## ` entries of an autopsies.md, verbatim and in file order."""
    parts = re.split(r"(?m)^(?=## )", text or "")
    if not parts:
        return ""
    preamble, entries = parts[0], parts[1:]
    kept = entries[-n:] if n > 0 else []
    head = preamble.rstrip() + "\n\n" if preamble.strip() else ""
    note = (f"_Showing the last {len(kept)} of {len(entries)} logged entries "
            f"(generated from autopsies.md, do not edit)._\n\n")
    return head + note + "".join(kept)


def write_recent_autopsies(slug: str, n: int = 6) -> Path | None:
    """Regenerate rules/<slug>/autopsies_recent.md from autopsies.md."""
    src = _rules_dir(slug) / "autopsies.md"
    if not src.exists():
        return None
    path = _rules_dir(slug) / "autopsies_recent.md"
    path.write_text(recent_autopsy_entries(src.read_text(), n=n))
    return path
