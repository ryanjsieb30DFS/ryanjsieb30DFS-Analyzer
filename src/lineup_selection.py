"""🎯 Per-contest entry picking over the Sim's pushed pool.

**Selection is not construction (8/9/26).** This module never authors, edits,
swaps, or fixes a roster. Every lineup it handles was BUILT AND SIMMED by the
Sim tool and arrived via `data/sim_pool/<slug>.json`.

Per-contest flow (8/9/26 evening rework — the user's contests are all small
single-entry GPPs but NOT interchangeable: different field sizes, payout
shapes, and histories, so every contest gets its own pick and its own grade):

1. `candidate_slice` deterministically cuts THAT contest's top ~50 pool rows
   (by that contest's own sim metrics — top1/win/cash/roi — plus projection,
   low-ownership and low-dupe standouts).
2. `slice_digest_md` renders the slice as one id-keyed markdown table; the
   `run_contest_selection` claude pass reads it (plus the strategy, board,
   and open lessons) and PICKS exactly `my_entries` rows BY ID.
3. `parse_pick` validates the pick hard: every id must be a slice row, the
   listed players must match that row exactly, the count must equal
   `my_entries`. Any violation → errors, nothing saved. A selection can
   choose; it can never invent.
4. `save_contest_pick` persists picks per contest (schema v2) so the Grade
   tab can one-click them into that contest's grade box.

Crowd/trap discipline still applies: a trap is a price, not a player, and
nothing here carries player-name quality signals across slates.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

_SELECTION_DIR = Path(__file__).parent.parent / "data" / "lineup_selection"

# Sim contest_type -> Analyzer declared type vocabulary.
_TYPE_MAP = {"se": "SE", "3max": "3-Max", "5max": "5-Max",
             "20max": "20-Max", "mme": "150-Max", "150max": "150-Max"}
_SMALL_FIELD_TYPES = {"se", "3max", "5max"}

# Fields under this many entries play like SE — a validated finding
# (docs/mme_plan.md: "Under ~2,500 entries plays like SE").
_PLAYS_LIKE_SE_FIELD = 2_500

_SLICE_CAP = 50


# ---------------------------------------------------------------------------
# Paths + persistence (schema v2: per-contest picks)
# ---------------------------------------------------------------------------

def _path(slug: str) -> Path:
    return _SELECTION_DIR / f"{slug}.json"


def contest_file_key(label, declared: dict | None) -> str:
    """Stable per-contest file/session key: the declared contest's 8-hex id
    when matched, else a slugified sim label (deterministic, fs-safe)."""
    if declared and declared.get("id"):
        return str(declared["id"])
    s = re.sub(r"[^a-z0-9]+", "-", str(label or "").lower()).strip("-")
    return s[:40] or "contest"


def pick_path(slug: str, key: str) -> Path:
    return _SELECTION_DIR / f"{slug}__{key}_pick.md"


def slice_path(slug: str, key: str) -> Path:
    return _SELECTION_DIR / f"{slug}__{key}_slice.md"


def load_selection(slug: str) -> dict | None:
    """The per-contest picks file, or None (absent, unreadable, pre-v2 —
    old files simply regenerate; the store is slate-scoped)."""
    p = _path(slug)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict) or data.get("schema_version") != 2:
        return None
    return data if data.get("contests") else None


def save_contest_pick(slug: str, pool: dict, label: str, declared: dict | None,
                      picks: list[dict], why: str | None) -> dict:
    """Persist one contest's validated picks into the v2 selection file.
    Returns the full payload after the write."""
    data = load_selection(slug) or {
        "schema_version": 2,
        "slug": slug,
        "pool_fp": pool.get("pool_fp"),
        "pool_len": pool.get("pool_len"),
        "contests": {},
    }
    # A pick belongs to ONE pool; a re-sent pool invalidates old picks.
    if data.get("pool_fp") != pool.get("pool_fp"):
        data = {"schema_version": 2, "slug": slug,
                "pool_fp": pool.get("pool_fp"),
                "pool_len": pool.get("pool_len"), "contests": {}}
    data["contests"][str(label)] = {
        "picked": picks,
        "why": why,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "declared_contest_id": (declared or {}).get("id"),
    }
    _SELECTION_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps(data, indent=2))
    return data


def clear_selection(slug: str) -> None:
    """Slate-scoped cleanup — the picks file plus every per-contest pick and
    slice digest."""
    if not _SELECTION_DIR.exists():
        return
    for p in [_path(slug)] + list(_SELECTION_DIR.glob(f"{slug}__*_pick.md")) \
            + list(_SELECTION_DIR.glob(f"{slug}__*_slice.md")):
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Contest matching (Sim payload contest -> declared contest)
# ---------------------------------------------------------------------------

def match_contests(pool_contests: list[dict], declared: list[dict],
                   tol: float = 0.15) -> dict:
    """{sim contest label -> declared contest dict or None}, one-to-one.

    Same idea as `contests.auto_link`: exact type match preferred, then
    field-size closeness (within `tol`). A sim contest whose type maps to a
    different declared type is never matched to it."""
    result = {str(c.get("label")): None for c in (pool_contests or [])}
    pairs = []
    for c in pool_contests or []:
        cf = c.get("field_size") or 0
        ctype = _TYPE_MAP.get(str(c.get("contest_type") or "").lower())
        for d in declared or []:
            df = d.get("field_size") or 0
            type_match = 0 if (ctype and d.get("type") == ctype) else 1
            if cf and df:
                rel = abs(cf - df) / df
                if rel > tol:
                    continue
            elif type_match:
                continue  # no field sizes AND no type match — nothing to go on
            else:
                rel = 1.0  # type matches but a field size is missing
            pairs.append((type_match, rel, str(c.get("label")), d))
    pairs.sort(key=lambda p: (p[0], p[1], p[2]))
    used_label, used_declared = set(), set()
    for _tm, _rel, label, d in pairs:
        did = d.get("id") or d.get("name")
        if label in used_label or did in used_declared:
            continue
        result[label] = d
        used_label.add(label)
        used_declared.add(did)
    return result


def as_declared(sim_contest: dict) -> dict:
    """A sim-pool contest expressed in declared-contest vocabulary, for
    contests the user never declared (grading still needs field size, type,
    and entry count)."""
    return {
        "id": None,
        "name": sim_contest.get("label"),
        "type": _TYPE_MAP.get(str(sim_contest.get("contest_type") or "").lower()),
        "field_size": sim_contest.get("field_size"),
        "my_entries": sim_contest.get("my_entries"),
        "entry_fee": sim_contest.get("entry_fee"),
        "prize_pool": sim_contest.get("prize_pool"),
        "payout_shape": None,
    }


# ---------------------------------------------------------------------------
# Candidate slice (deterministic top cut of THIS contest's pool)
# ---------------------------------------------------------------------------

def _norm(vals: list) -> list[float]:
    """Min-max normalize to [0,1]; None -> 0; constant array -> all 0.5."""
    nums = [float(v) if v is not None else None for v in vals]
    present = [v for v in nums if v is not None]
    if not present:
        return [0.0] * len(nums)
    lo, hi = min(present), max(present)
    if hi - lo < 1e-12:
        return [0.5 if v is not None else 0.0 for v in nums]
    return [((v - lo) / (hi - lo)) if v is not None else 0.0 for v in nums]


def _top_idx(vals: list, n: int, reverse: bool = True) -> list[int]:
    """Indexes of the best n values (None last; ties by index — deterministic)."""
    order = sorted(range(len(vals)),
                   key=lambda i: ((vals[i] is None),
                                  -(vals[i] or 0) if reverse else (vals[i] or 0),
                                  i))
    return order[:n]


def candidate_slice(pool: dict, contest: dict, k: int = _SLICE_CAP) -> list[dict]:
    """THIS contest's top pool rows, deterministically: the union of the best
    lineups by each of the contest's own sim metrics, plus projection and
    low-ownership / low-duplication standouts, capped at `k` by a blend score.
    Same pool + contest in, same slice out — the claude pass only ever
    chooses among these real rows."""
    rosters = pool.get("rosters") or []
    n = len(rosters)
    if n == 0:
        return []
    m = contest.get("metrics") or {}
    top1 = (m.get("top1_pct") or [None] * n)[:n]
    win = (m.get("win_pct") or [None] * n)[:n]
    cash = (m.get("cash_pct") or [None] * n)[:n]
    roi = (m.get("roi_pct") or [None] * n)[:n]
    proj = (pool.get("proj") or [None] * n)[:n]
    avg_own = (pool.get("avg_own") or [None] * n)[:n]
    dupes = contest.get("exp_dupes")

    chosen: list[int] = []
    seen: set = set()

    def _add(idxs):
        for i in idxs:
            if i not in seen:
                seen.add(i)
                chosen.append(i)

    _add(_top_idx(top1, 15))
    _add(_top_idx(win, 15))
    _add(_top_idx(cash, 10))
    _add(_top_idx(roi, 10))
    _add(_top_idx(proj, 10))
    # Standouts within the top quartile by this contest's top1: the
    # lowest-owned (leverage) and, when dupe data exists, least-duplicated.
    q_list = sorted(_top_idx(top1, max(1, n // 4)))
    _add([q_list[j] for j in _top_idx([avg_own[i] for i in q_list], 10,
                                      reverse=False)])
    if dupes:
        _add([q_list[j] for j in _top_idx([dupes[i] for i in q_list], 10,
                                          reverse=False)])

    # Cap by blend score (small fields lean on win% — plays like SE).
    t1n, wn, cn = _norm(top1), _norm(win), _norm(cash)
    field = int(contest.get("field_size") or 0)
    if field and field < _PLAYS_LIKE_SE_FIELD:
        blend = [0.4 * t1n[i] + 0.4 * wn[i] + 0.2 * cn[i] for i in range(n)]
    else:
        blend = [0.5 * t1n[i] + 0.3 * wn[i] + 0.2 * cn[i] for i in range(n)]
    chosen.sort(key=lambda i: (-blend[i], i))
    chosen = chosen[:k]

    def _val(arr, i, nd=2):
        v = arr[i] if arr and i < len(arr) else None
        return round(float(v), nd) if v is not None else None

    out = []
    for i in chosen:
        names = [str(x) for x in rosters[i]]
        out.append({
            "index": i,
            "roster": names,
            "roster_key": "|".join(sorted(names)),
            "salary": (pool.get("salary") or [None] * n)[i],
            "proj": _val(proj, i),
            "avg_own": _val(avg_own, i, 1),
            "win_pct": _val(win, i),
            "top1_pct": _val(top1, i),
            "top10_pct": _val(m.get("top10_pct") or [], i, 1),
            "cash_pct": _val(cash, i, 1),
            "roi_pct": _val(roi, i, 1),
            "exp_dupes": _val(dupes or [], i),
        })
    return out


def slice_digest_md(slug: str, label: str, contest: dict, declared: dict | None,
                    rows: list[dict], ownership: dict) -> str:
    """The candidate table the claude pass reads and picks ids from."""
    shape = (declared or {}).get("payout_shape") or "not declared"
    my = contest.get("my_entries")
    lines = [
        f"# Candidate lineups — {label}",
        f"Contest: field {int(contest.get('field_size') or 0):,} entries · "
        f"${contest.get('entry_fee')} entry · payout shape {shape} · "
        f"you are entering {my} lineup(s).",
        "Every lineup below was built and simmed by the Sim tool. "
        "Pick ONLY from this table, by id.",
        "",
        "| id | salary | proj | avg own% | win% | top1% | cash% | roi% | dupes | players |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        players = ", ".join(
            f"{nm} ({ownership.get(nm)}%)" if ownership.get(nm) is not None else nm
            for nm in r["roster"])
        lines.append(
            f"| {r['index']} | {r.get('salary')} | {r.get('proj')} | "
            f"{r.get('avg_own')} | {r.get('win_pct')} | {r.get('top1_pct')} | "
            f"{r.get('cash_pct')} | {r.get('roi_pct')} | "
            f"{r.get('exp_dupes') if r.get('exp_dupes') is not None else '—'} | "
            f"{players} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pick parsing + validation — a selection can choose, never invent
# ---------------------------------------------------------------------------

def _strip_own(cell: str) -> list[str]:
    """Player names from a table cell, ownership parentheticals removed."""
    return [re.sub(r"\s*\([^)]*\)\s*$", "", p).strip()
            for p in str(cell).split(",") if p.strip()]


def parse_pick(md: str, slice_rows: list[dict], my_entries: int) -> dict:
    """Validate the claude pick file against the slice it was given.

    Returns {"picks": [{"index", "roster_key"}], "why": str|None,
    "errors": [str]}. Non-empty errors => the picks are unusable and the
    caller must save NOTHING (selection is not construction — a pick that
    isn't a real slice row, or that lists different players than its row,
    is rejected outright)."""
    from src.autopsy import _norm_name

    by_index = {int(r["index"]): r for r in slice_rows}
    picks: list[dict] = []
    errors: list[str] = []
    seen_ids: set = set()

    lines = (md or "").splitlines()
    cols: list[str] | None = None
    table_done = False
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            if cols is not None:
                table_done = True
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        low = [c.lower() for c in cells]
        if cols is None:
            if "id" in low:
                cols = low
            continue
        if table_done:
            continue
        if set("".join(cells)) <= {"-", " ", ":"}:
            continue  # separator row
        row = dict(zip(cols, cells))
        raw_id = row.get("id", "")
        try:
            rid = int(re.sub(r"[^\d-]", "", raw_id) or "x")
        except ValueError:
            errors.append(f"'{raw_id}' is not a lineup id from the candidate table.")
            continue
        if rid not in by_index:
            errors.append(f"id {rid} is not in the candidate table — a pick "
                          "must be a real row (fabricated ids are rejected).")
            continue
        if rid in seen_ids:
            errors.append(f"id {rid} was picked twice.")
            continue
        seen_ids.add(rid)
        srow = by_index[rid]
        players_cell = row.get("players")
        if players_cell:
            listed = {_norm_name(p) for p in _strip_own(players_cell)}
            actual = {_norm_name(p) for p in srow["roster"]}
            if listed != actual:
                errors.append(
                    f"the players listed for id {rid} do not match that "
                    "lineup — a selection may never modify a roster.")
                continue
        picks.append({"index": rid, "roster_key": srow["roster_key"]})

    if len(picks) != int(my_entries):
        errors.append(f"{len(picks)} valid pick(s) but this contest takes "
                      f"exactly {my_entries} — nothing was saved.")

    why = None
    m = re.search(r"^\*\*Why[^\n]*\*\*:?\s*(.*?)(?=\n\s*\n|\Z)",
                  md or "", re.M | re.S)
    if m:
        why = " ".join(m.group(1).split()) or None

    return {"picks": picks if not errors else [], "why": why, "errors": errors}
