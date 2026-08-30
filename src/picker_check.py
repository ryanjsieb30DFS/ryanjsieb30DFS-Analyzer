"""POOL / SLICE / PICK — where each contest was won or lost, per slate.

Part of the POST-SLATE ANALYSIS since 8/30/26 (user directive): the Log
Autopsy flow runs `check_history_dir` on the slate it just archived, writes
`picker_check.json` beside the other archive files, and the post-autopsy
review reads it. `scripts/picker_report.py` runs the same measurement over
EVERY archived slate for the cross-slate trend.

The three chain links, separated per contest:

    POOL   did the Sim build a lineup scoring >= the winning score at all?
    SLICE  did that lineup reach the table Claude was shown? (needs the
           archived slice digest — archived with every slate from 8/30/26)
    PICK   what did the pick score, and where does that sit in the pool?

A slice miss means re-weight the table; a pick miss means the prompt is the
bottleneck. On 8/29 the row that beat the winning score by 47 points sat IN
the slice and was never mentioned — this file makes that a counted number
instead of an anecdote.

Data joins, all read-only:
    <hist>/lineup_selection.json   the picks
    <hist>/results.json            contest -> source_file (the join to DK)
    <hist>/autopsy.json            contest -> winning score
    <hist>/<slug>__*_slice.md      the shown table (8/30/26+)
    Sim rules/<slug>/scored_pools/*_<contest_id>_*.json.gz
                                   every pool lineup's ACTUAL score

The Sim repo is found as a sibling directory (`../ryanjsieb30DFS`, the
standard two-repo layout); pass `sim_root` to point elsewhere. Missing data
never crashes an autopsy — a contest without all three legs is skipped, and
`check_md` says what was missing.
"""
from __future__ import annotations

import glob
import gzip
import json
import re
from datetime import datetime
from pathlib import Path

from src.lineup_selection import (_contest_join_key, _strat_norm,
                                  contest_file_key)

_REPO_ROOT = Path(__file__).parent.parent


def default_sim_root() -> Path:
    """The Sim repo's expected location: a sibling of this repo."""
    return _REPO_ROOT.parent / "ryanjsieb30DFS"


def _roster_key(names) -> frozenset:
    return frozenset(_strat_norm(n) for n in names if str(n).strip())


def scored_pool(sim_root: Path, slug: str, contest_id: str) -> list | None:
    """[(roster_key, actual_score), ...] from the Sim's scored pool for one
    contest, or None when the Sim never scored it (or the repo is absent)."""
    hits = glob.glob(str(sim_root / "rules" / slug / "scored_pools"
                         / f"*_{contest_id}_*.json.gz"))
    if not hits:
        return None
    try:
        raw = json.loads(gzip.open(hits[0]).read())
    except (OSError, json.JSONDecodeError):
        return None
    out = []
    for r in raw:
        a = r.get("actual_score")
        if a is None:
            continue
        names = [x.strip() for x in str(r.get("players") or "").split(",")]
        if names:
            out.append((_roster_key(names), float(a)))
    return out or None


def slice_rosters(hist_dir: Path, slug: str) -> dict:
    """{slice file stem: [roster_key, ...]} for every archived slice digest."""
    out = {}
    for f in sorted(Path(hist_dir).glob(f"{slug}__*_slice.md")):
        rows = []
        cols = None
        for line in f.read_text().splitlines():
            s = line.strip()
            if not s.startswith("|"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            low = [c.lower() for c in cells]
            if cols is None:
                if "id" in low and "players" in low:
                    cols = low
                continue
            if set("".join(cells)) <= {"-", " ", ":"}:
                continue
            row = dict(zip(cols, cells))
            players = [re.sub(r"\s*\([^)]*\)\s*$", "", p).strip()
                       for p in str(row.get("players") or "").split(",")]
            players = [p for p in players if p]
            if players:
                rows.append(_roster_key(players))
        if rows:
            out[f.stem] = rows
    return out


def slice_for_contest(slices: dict, declared_id, label: str) -> list | None:
    """The archived slice for one contest — matched on the same key
    `lineup_selection.contest_file_key` used to write it."""
    key = contest_file_key(label, {"id": declared_id} if declared_id else None)
    for stem, rows in slices.items():
        if stem.endswith(f"__{key}_slice"):
            return rows
    return None


def slate_rows(hist: Path, slug: str, sim_root: Path) -> list[dict]:
    """Per-contest POOL/SLICE/PICK measurements for one archived slate.
    Contests missing any join leg (no pick, no logged result, no winning
    score, no scored pool) are skipped — never guessed at."""
    hist = Path(hist)
    try:
        sel = json.loads((hist / "lineup_selection.json").read_text())
        res = json.loads((hist / "results.json").read_text())
        autopsy = json.loads((hist / "autopsy.json").read_text())
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(sel, dict) or sel.get("schema_version") != 2:
        return []
    win_by_id = {}
    for r in autopsy if isinstance(autopsy, list) else []:
        try:
            win_by_id[str(r.get("contest_id"))] = float(r.get("winning_score"))
        except (TypeError, ValueError):
            continue
    src_by_name = {_contest_join_key(c.get("name")): str(c.get("source_file") or "")
                   for c in res.get("contests") or [] if c.get("name")}
    slices = slice_rosters(hist, slug)

    out = []
    for label, rec in (sel.get("contests") or {}).items():
        source = src_by_name.get(_contest_join_key(label))
        if not source:
            continue
        m = re.search(r"(\d{6,})", source)
        cid = m.group(1) if m else None
        win = win_by_id.get(cid)
        pool = scored_pool(sim_root, slug, cid) if cid else None
        if win is None or not pool:
            continue
        actual_by_roster = {}
        for rk, a in pool:
            actual_by_roster[rk] = max(a, actual_by_roster.get(rk, a))
        picks = (rec or {}).get("picked") or []
        pick_scores = [actual_by_roster.get(_roster_key(p["roster_key"].split("|")))
                       for p in picks if p.get("roster_key")]
        pick_scores = [s for s in pick_scores if s is not None]
        if not pick_scores:
            continue
        pick_best = max(pick_scores)
        pool_scores = [a for _rk, a in pool]
        row = {
            "date": str(res.get("date") or ""),
            "contest": str(label),
            "winning_score": round(win, 1),
            "pool_n": len(pool_scores),
            "pool_max": round(max(pool_scores), 1),
            "pool_held_winner": max(pool_scores) >= win,
            "n_pool_ge_win": sum(1 for a in pool_scores if a >= win),
            "pick_actual": round(pick_best, 1),
            "pick_won": pick_best >= win,
            # % of pool lineups the pick BEAT — higher is better.
            "pick_pool_pctile": round(
                100.0 * sum(1 for a in pool_scores if a < pick_best)
                / len(pool_scores), 1),
        }
        srows = slice_for_contest(slices, (rec or {}).get("declared_contest_id"),
                                  label)
        if srows:
            svals = [actual_by_roster.get(rk) for rk in srows]
            svals = [v for v in svals if v is not None]
            if svals:
                row.update({
                    "slice_n": len(svals),
                    "slice_max": round(max(svals), 1),
                    "slice_held_winner": max(svals) >= win,
                    # Rows on the shown table that outscored the pick — the
                    # 8/29 failure, counted: "look DOWN the table" misses.
                    "n_slice_above_pick": sum(1 for v in svals if v > pick_best),
                })
        out.append(row)
    return out


def check_history_dir(hist_dir: Path, slug: str,
                      sim_root: Path | None = None) -> dict:
    """The picker check for ONE archived slate, ready to persist as
    picker_check.json. `contests` is empty (with `note` saying why) when the
    Sim repo or its scored pools are missing — an autopsy never fails on it."""
    root = Path(sim_root) if sim_root else default_sim_root()
    if not (root / "rules").exists():
        return {"schema_version": 1, "slug": slug, "contests": [],
                "note": f"Sim repo not found at {root} — scored pools are "
                        "needed to score the pool and the pick.",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")}
    rows = slate_rows(Path(hist_dir), slug, root)
    note = None
    if not rows:
        note = ("No contest had all three legs: a saved pick, a logged "
                "winning score, and a Sim scored pool. Score the slate in "
                "the Sim before logging the autopsy to fill this in.")
    return {"schema_version": 1, "slug": slug, "contests": rows, "note": note,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")}


def check_md(data: dict) -> str:
    """The picker check in plain words — rendered in the Autopsy tab and read
    back by the slate breakdown."""
    rows = (data or {}).get("contests") or []
    if not rows:
        return ("**🎯 Picker check — not measurable this slate.** "
                + str((data or {}).get("note") or ""))
    L = ["**🎯 Picker check — was the miss in the table or in the pick?**",
         ""]
    for r in rows:
        bits = [
            f"**{r['contest']}** — winning score {r['winning_score']:g}.",
            (f"The pool's best lineup scored {r['pool_max']:g} — the Sim "
             + ("DID build a contest winner"
                if r["pool_held_winner"] else "did NOT build a winner")
             + f" ({r['n_pool_ge_win']} lineup(s) at or above the winning "
               "score)."),
        ]
        if "slice_held_winner" in r:
            bits.append(
                f"The table Claude was shown held {r['slice_n']} rows, best "
                f"{r['slice_max']:g} — "
                + ("a winning row WAS on the table."
                   if r["slice_held_winner"] else
                   "no winning row reached the table (a slice miss, not a "
                   "pick miss)."))
        else:
            bits.append("No archived table for this contest — the slice leg "
                        "is unmeasurable here (tables archive with every "
                        "slate from 8/30/26 on).")
        bits.append(
            f"The pick scored {r['pick_actual']:g}"
            + (" — it WON the contest." if r["pick_won"] else
               f", beating {r['pick_pool_pctile']:g}% of the pool it was "
               "chosen from."))
        if r.get("n_slice_above_pick"):
            bits.append(
                f"⚠️ {r['n_slice_above_pick']} row(s) ON THE SHOWN TABLE "
                "outscored the pick — the 8/29 failure shape: the answer was "
                "in front of the picker and it chose lower.")
        L.append("- " + " ".join(bits))
    L.append("")
    L.append("A pool miss is a BUILD problem; a slice miss is a TABLE "
             "problem; a table row above the pick is a PICK problem. They "
             "need different fixes — never blame the picker for a lineup it "
             "was never shown.")
    return "\n".join(L)
