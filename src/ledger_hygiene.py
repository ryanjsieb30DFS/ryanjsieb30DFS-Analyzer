"""Lesson-ledger hygiene — keep `rules/<slug>/lessons.yaml` sharp as it grows.

A deterministic Python pre-pass that flags, as CANDIDATES only (never mutates the
ledger here):
  - stale hypotheses: status `hypothesis`, zero confirmations, and old enough
    (>= N slates logged since `born`, OR >= N days old) — retire/merge candidates;
  - near-promotion: open lessons one mechanism confirmation away from the
    3-confirming-slate codify bar;
  - overdue promotion: lessons already at the bar but not yet codified;
  - merge candidates: lessons that cross-link each other (`[[id]]`) or share a
    high fraction of statement tokens.

The LLM review (`analysis_runner.run_ledger_review`) turns these into reasoned
proposals; the user approves via the app, and only then does
`run_apply_ledger_proposals` edit the ledger. Promotion math follows CLAUDE.md:
confirming slates = origin (1) + len(confirmations).
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent

_OPEN = ("hypothesis", "validated")
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "for", "is",
    "are", "was", "were", "be", "by", "with", "as", "at", "it", "its", "that",
    "this", "not", "no", "so", "than", "then", "from", "into", "over", "under",
    "one", "two", "each", "any", "all", "more", "less", "both", "a", "se",
    "lineup", "lineups", "slate", "slates", "play", "plays", "build", "builds",
    "gpp", "own", "owned", "ownership", "field", "rule", "test", "before",
}


def _lessons_path(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "lessons.yaml"


def load_lessons(slug: str) -> list[dict]:
    """Parsed lessons list (empty on missing/unparseable file)."""
    p = _lessons_path(slug)
    if not p.exists():
        return []
    try:
        import yaml
        data = yaml.safe_load(p.read_text()) or {}
    except Exception:  # noqa: BLE001 — never break the UI on a malformed ledger
        return []
    return data.get("lessons") or []


def confirming_slates(lesson: dict) -> int:
    """Origin slate (1) + each logged confirmation."""
    return 1 + len(lesson.get("confirmations") or [])


def _born_dt(lesson: dict):
    try:
        return datetime.strptime(str(lesson.get("born", "")).strip(), "%Y-%m-%d")
    except ValueError:
        return None


def _slates_since(born_dt, results: list[dict]) -> int:
    """How many logged slates have a date strictly after `born_dt`."""
    if born_dt is None:
        return 0
    n = 0
    for r in results:
        try:
            d = datetime.strptime(str(r.get("date", "")).strip(), "%Y-%m-%d")
        except ValueError:
            continue
        if d > born_dt:
            n += 1
    return n


def stale_hypotheses(lessons: list[dict], results: list[dict],
                     min_slates: int = 3, min_days: int = 30) -> list[dict]:
    """Hypotheses with 0 confirmations that have had a fair shot — >= min_slates
    logged since `born`, OR >= min_days old. Retire/merge candidates."""
    today = datetime.now()
    out = []
    for l in lessons:
        if l.get("status") != "hypothesis":
            continue
        if (l.get("confirmations") or []):
            continue
        born = _born_dt(l)
        slates = _slates_since(born, results)
        days = (today - born).days if born else None
        if slates >= min_slates or (days is not None and days >= min_days):
            out.append({"id": l.get("id"), "born": l.get("born"),
                        "slates_since": slates, "days_old": days,
                        "statement": (l.get("statement") or "").strip()})
    return out


def near_promotion(lessons: list[dict]) -> list[dict]:
    """Open lessons one confirmation short of the 3-slate codify bar."""
    return [{"id": l.get("id"), "status": l.get("status"),
             "confirming_slates": confirming_slates(l),
             "statement": (l.get("statement") or "").strip()}
            for l in lessons
            if l.get("status") in _OPEN and confirming_slates(l) == 2]


def overdue_promotion(lessons: list[dict]) -> list[dict]:
    """Lessons at/over the bar (>=3 confirming slates) but not yet codified."""
    return [{"id": l.get("id"), "status": l.get("status"),
             "confirming_slates": confirming_slates(l),
             "statement": (l.get("statement") or "").strip()}
            for l in lessons
            if l.get("status") in _OPEN and confirming_slates(l) >= 3]


def _tokens(s: str) -> set:
    words = re.findall(r"[a-z][a-z\-]{2,}", (s or "").lower())
    return {w for w in words if w not in _STOPWORDS}


def merge_candidates(lessons: list[dict], min_overlap: float = 0.45) -> list[dict]:
    """Pairs worth reviewing for merge: mutual/one-way `[[id]]` cross-links, or
    statement-token Jaccard >= min_overlap (open lessons only for the token pass)."""
    ids = {l.get("id") for l in lessons}
    pairs: list[dict] = []
    seen: set = set()

    # (1) cross-link signal — statements that reference another lesson's id.
    for l in lessons:
        for ref in re.findall(r"\[\[([^\]]+)\]\]", l.get("statement") or ""):
            if ref in ids and ref != l.get("id"):
                key = tuple(sorted([l.get("id"), ref]))
                if key in seen:
                    continue
                seen.add(key)
                pairs.append({"a": key[0], "b": key[1], "reason": "cross-linked [[id]]"})

    # (2) token-overlap signal among open lessons.
    open_l = [l for l in lessons if l.get("status") in _OPEN]
    for i in range(len(open_l)):
        for j in range(i + 1, len(open_l)):
            a, b = open_l[i], open_l[j]
            key = tuple(sorted([a.get("id"), b.get("id")]))
            if key in seen:
                continue
            ta, tb = _tokens(a.get("statement", "")), _tokens(b.get("statement", ""))
            if not ta or not tb:
                continue
            jac = len(ta & tb) / len(ta | tb)
            if jac >= min_overlap:
                seen.add(key)
                pairs.append({"a": key[0], "b": key[1], "reason": f"{jac:.0%} token overlap"})
    return pairs


_ALL_SLUGS = ("pga_classic", "pga_rd4_sd", "mma_se", "nascar")


def cross_sport_candidates(min_overlap: float = 0.45,
                           slugs: tuple = _ALL_SLUGS) -> list[dict]:
    """Lesson pairs from DIFFERENT sports whose statements token-overlap — the
    same pattern learned twice. Anchor-Equivalence proved universal patterns
    exist; this watches for the next one so it can be promoted to
    `rules/shared/` instead of sitting duplicated. Non-retired lessons all
    participate (a codified rule in one sport matching a hypothesis in another
    is exactly the promotion signal). Sorted by overlap, capped at 10."""
    per_sport = []
    for s in slugs:
        for l in load_lessons(s):
            if l.get("status") == "retired":
                continue
            toks = _tokens(l.get("statement", ""))
            if toks:
                per_sport.append((s, l.get("id"), toks))
    pairs = []
    for i in range(len(per_sport)):
        for j in range(i + 1, len(per_sport)):
            sa, ida, ta = per_sport[i]
            sb, idb, tb = per_sport[j]
            if sa == sb:
                continue  # within-sport dupes are merge_candidates' job
            jac = len(ta & tb) / len(ta | tb)
            if jac >= min_overlap:
                pairs.append({"a": f"{sa}:{ida}", "b": f"{sb}:{idb}",
                              "overlap": round(jac, 2)})
    pairs.sort(key=lambda p: -p["overlap"])
    return pairs[:10]


def cross_sport_md(pairs: list[dict]) -> str | None:
    if not pairs:
        return None
    out = ["#### Cross-sport lesson overlap — promotion candidates for `rules/shared/`",
           "The same pattern learned in two sports is likely UNIVERSAL (the "
           "Anchor-Equivalence path). Review each pair; if the mechanism matches, "
           "promote one statement to `rules/shared/` and cross-link both ledgers."]
    for p in pairs:
        out.append(f"- `{p['a']}` ↔ `{p['b']}` — {p['overlap']:.0%} statement overlap")
    return "\n".join(out)


def hygiene_report(slug: str) -> dict:
    """Full deterministic flag set for a slug's ledger."""
    from src import history
    lessons = load_lessons(slug)
    results = history.load_results(slug)
    statuses: dict = {}
    for l in lessons:
        statuses[l.get("status", "?")] = statuses.get(l.get("status", "?"), 0) + 1
    return {
        "slug": slug,
        "total": len(lessons),
        "by_status": statuses,
        "stale": stale_hypotheses(lessons, results),
        "near_promotion": near_promotion(lessons),
        "overdue_promotion": overdue_promotion(lessons),
        "merges": merge_candidates(lessons),
    }


def _short(stmt: str, n: int = 120) -> str:
    stmt = " ".join((stmt or "").split())
    return stmt if len(stmt) <= n else stmt[: n - 1] + "…"


def report_md(report: dict) -> str:
    """Human-readable summary for instant display in the app (no Claude needed)."""
    L = [f"**{report['total']} lessons** — "
         + ", ".join(f"{k}: {v}" for k, v in sorted(report["by_status"].items()))]

    def block(title: str, items: list, render) -> None:
        if not items:
            return
        L.append(f"\n**{title} ({len(items)})**")
        for it in items:
            L.append(render(it))

    block("🗑 Stale hypotheses (0 confirmations, had their shot)", report["stale"],
          lambda it: f"- `{it['id']}` — {it['slates_since']} slates / {it['days_old']}d old — {_short(it['statement'])}")
    block("⏳ Near promotion (2 of 3 confirming slates)", report["near_promotion"],
          lambda it: f"- `{it['id']}` ({it['status']}) — {_short(it['statement'])}")
    block("⬆ Overdue promotion (≥3 confirming slates, not codified)", report["overdue_promotion"],
          lambda it: f"- `{it['id']}` ({it['status']}, {it['confirming_slates']} slates) — {_short(it['statement'])}")
    block("🔗 Merge candidates", report["merges"],
          lambda it: f"- `{it['a']}` ↔ `{it['b']}` — {it['reason']}")

    if len(L) == 1:
        L.append("\n_Ledger is clean — nothing flagged._")
    return "\n".join(L)
