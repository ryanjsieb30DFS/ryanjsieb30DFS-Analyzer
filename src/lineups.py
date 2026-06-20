"""Persisted Claude-written per-slate artifacts: lineups + red-team review.

Claude writes data/lineups/<slug>.md (Analyze tab "Build lineups" button) and
data/red_team/<slug>.md ("Red team the lineups" button) via headless claude -p.
This module just reads + clears them, mirroring src/slate_analysis.py.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd

_LINEUPS_DIR = Path(__file__).parent.parent / "data" / "lineups"
_RED_TEAM_DIR = Path(__file__).parent.parent / "data" / "red_team"
_FIXES_DIR = Path(__file__).parent.parent / "data" / "lineup_fixes"
_HB_ANALYSIS_DIR = Path(__file__).parent.parent / "data" / "handbuild_analysis"
_RANKING_DIR = Path(__file__).parent.parent / "data" / "lineup_ranking"


def load_lineups(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None if no file exists."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def clear_lineups(slug: str) -> None:
    """Delete the file. Called after an autopsy log so the next slate starts fresh."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()


def load_red_team(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None if no file exists."""
    p = _RED_TEAM_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def clear_red_team(slug: str) -> None:
    """Delete the file. Called after an autopsy log so the next slate starts fresh."""
    p = _RED_TEAM_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()


def red_team_verdicts(slug: str) -> dict[str, str]:
    """Parse the red-team review's '## Verdict summary' table into
    {lineup_label: 'SHIP'|'FIX'|'KILL'}. Returns {} if no review exists.

    Reads only the rows of the FIRST markdown table whose verdict cell is a
    bold SHIP/FIX/KILL — the verdict summary — so per-lineup attack headers
    (which repeat the verdict) don't double-count.
    """
    p = _RED_TEAM_DIR / f"{slug}.md"
    if not p.exists():
        return {}
    out: dict[str, str] = {}
    for label, verdict in re.findall(
        r"(?m)^\|\s*(L\d+\b[^|]*?)\s*\|\s*\*\*(SHIP|FIX|KILL)\*\*\s*\|", p.read_text()
    ):
        out[label.strip()] = verdict
    return out


def flagged_lineups(slug: str) -> list[str]:
    """Labels of lineups the red team marked FIX or KILL (in table order)."""
    return [lab for lab, v in red_team_verdicts(slug).items() if v in ("FIX", "KILL")]


def load_lineup_fixes(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} for the fix-proposals doc, or None."""
    p = _FIXES_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def clear_lineup_fixes(slug: str) -> None:
    """Delete the fix-proposals doc (per-slate working state)."""
    p = _FIXES_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()


def load_handbuild_analysis(slug: str) -> dict | None:
    """Claude's analysis of the current handbuild, or None if none exists.

    Returns {'markdown', 'mtime', 'thesis', 'what_if', 'players'} — thesis and
    what_if are parsed from the fixed-format lines Claude writes; players come
    from the lineup snapshot saved when the analysis ran, so the UI can detect
    a lineup that changed after its analysis.
    """
    p = _HB_ANALYSIS_DIR / f"{slug}.md"
    if not p.exists():
        return None
    md = p.read_text()
    thesis = re.search(r"(?m)^\*\*Thesis:\*\*\s*(.+?)\s*$", md)
    what_if = re.search(r"(?m)^\*\*What if\?\*\*\s*[—:–-]?\s*\*?(.+?)\*?\s*$", md)
    players: list[str] = []
    player_rows: list[dict] = []
    snap = _HB_ANALYSIS_DIR / f"{slug}_lineup.json"
    if snap.exists():
        try:
            player_rows = json.loads(snap.read_text())["players"]
            players = [pl["name"] for pl in player_rows]
        except (json.JSONDecodeError, KeyError, TypeError):
            players, player_rows = [], []
    return {
        "markdown": md,
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
        "thesis": thesis.group(1).strip() if thesis else "",
        "what_if": what_if.group(1).strip() if what_if else "",
        "players": players,
        # Full slotted row dicts — lets the save flow work even after the
        # table's browser-session selections are lost (refresh / restart).
        "player_rows": player_rows,
    }


def clear_handbuild_analysis(slug: str) -> None:
    """Delete the analysis + lineup snapshot. Called on save, clear, and autopsy log."""
    for p in (_HB_ANALYSIS_DIR / f"{slug}.md", _HB_ANALYSIS_DIR / f"{slug}_lineup.json"):
        if p.exists():
            p.unlink()


def load_lineup_ranking(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} for the candidate-lineup ranking, or None."""
    p = _RANKING_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def clear_lineup_ranking(slug: str) -> None:
    """Delete the ranking doc + its input/thesis sidecars. Slate-specific — cleared with the slate."""
    for p in (_RANKING_DIR / f"{slug}.md",
              _RANKING_DIR / f"{slug}_input.json",
              _RANKING_DIR / f"{slug}_theses.json"):
        if p.exists():
            p.unlink()


# ---------- Handbuild: roster specs, math, validation, append ---------- #

SALARY_CAP = 50_000

# DK roster shapes per contest slug. positional=False means interchangeable
# slots with no position filtering. RD4 SD is flat 6 — NO captain, NO 1.5x.
ROSTER_SPECS: dict[str, dict] = {
    "pga_classic": {"slots": ["G"] * 6, "slot_label": "Golfer", "positional": False, "cap": SALARY_CAP},
    "pga_rd4_sd":  {"slots": ["G"] * 6, "slot_label": "Golfer", "positional": False, "cap": SALARY_CAP},
    "mma_se":      {"slots": ["F"] * 6, "slot_label": "Fighter", "positional": False, "cap": SALARY_CAP},
    "nascar":      {"slots": ["D"] * 6, "slot_label": "Driver", "positional": False, "cap": SALARY_CAP},
    "mlb_classic": {
        "slots": ["P", "P", "C", "1B", "2B", "3B", "SS", "OF", "OF", "OF"],
        "slot_label": "Player", "positional": True, "cap": SALARY_CAP,
    },
}


def roster_spec(slug: str) -> dict:
    """Roster shape for the slug; KeyError on unknown slug is intentional."""
    return ROSTER_SPECS[slug]


def slot_eligible(position, slot: str) -> bool:
    """True if a player's position string qualifies for the slot.
    Handles multi-eligibility: '1B/3B' fills the 1B or the 3B slot.
    Non-positional sports pass position=None -> always eligible."""
    if position is None:
        return True
    return slot in [p.strip().upper() for p in str(position).split("/")]


def assign_slots(players: list[dict], spec: dict) -> tuple[list[dict], list[str]]:
    """Auto-assign selected players to roster slots.

    Returns (assigned, errors). assigned = copies of placeable players with
    'slot' set, ordered by slot index (spec order). errors = one message per
    unplaceable player. Positional sports use Kuhn's augmenting-path bipartite
    matching (exact — picking '1B/3B' then '1B' relocates the flex player to
    3B instead of erroring); flat sports fill slots in order. Partial
    selections are fine — open slots stay open.
    """
    slots = spec["slots"]
    if not spec["positional"]:
        assigned = [dict(p, slot=slots[i]) for i, p in enumerate(players[: len(slots)])]
        errors = [
            f"No open slot for {p['name']} — all {len(slots)} slots are filled."
            for p in players[len(slots):]
        ]
        return assigned, errors

    elig = [
        [j for j, s in enumerate(slots) if slot_eligible(p.get("position"), s)]
        for p in players
    ]
    owner: dict[int, int] = {}  # slot index -> player index

    def _place(i: int, visited: set) -> bool:
        for j in elig[i]:
            if j in visited:
                continue
            visited.add(j)
            if j not in owner or _place(owner[j], visited):
                owner[j] = i
                return True
        return False

    errors = []
    # Scarcity order: rigid players claim slots first, so errors land on the
    # most flexible (and most fixable) picks.
    for i in sorted(range(len(players)), key=lambda i: (len(elig[i]), i)):
        p = players[i]
        if not elig[i]:
            errors.append(f"{p['name']} ({p.get('position')}) doesn't fit any slot in this contest.")
        elif not _place(i, set()):
            taken = " and ".join(dict.fromkeys(slots[j] for j in elig[i]))
            errors.append(f"No open slot for {p['name']} ({p.get('position')}) — {taken} already filled.")

    assigned = [dict(players[i], slot=slots[j]) for j, i in sorted(owner.items())]
    return assigned, errors


def lineup_totals(players: list[dict], cap: int = SALARY_CAP) -> dict:
    """GPP summary math for a (possibly partial) lineup of canonical row dicts."""
    salaries = [int(p["salary"]) for p in players if p.get("salary") is not None]
    projs = [float(p["proj_points"]) for p in players if p.get("proj_points") is not None]
    owns = [float(p["ownership"]) for p in players if p.get("ownership") is not None]
    used = sum(salaries)
    return {
        "n_players": len(players),
        "salary_used": used,
        "salary_left": cap - used,
        "proj_total": round(sum(projs), 2),
        "own_total": round(sum(owns), 1),
        "own_avg": round(sum(owns) / len(owns), 1) if owns else None,
        "n_sub10": sum(1 for o in owns if o < 10),
    }


def validate_lineup(slug: str, players: list[dict], thesis: str, what_if: str) -> list[str]:
    """House rules — always on, no toggles. Each player dict carries the
    canonical row fields plus 'slot'. Returns [] when saveable, else one
    plain-English error per violation."""
    spec = roster_spec(slug)
    errors = []

    if len(players) != len(spec["slots"]):
        errors.append(f"Lineup incomplete: {len(players)}/{len(spec['slots'])} slots filled.")

    totals = lineup_totals(players, spec["cap"])
    if totals["salary_used"] > spec["cap"]:
        errors.append(f"Over the ${spec['cap']:,} cap by ${totals['salary_used'] - spec['cap']:,}.")

    seen = set()
    for p in players:
        nm = p.get("name")  # backstop must not itself KeyError on a malformed row
        if nm in seen:
            errors.append(f"Duplicate player: {nm}.")
        seen.add(nm)

    if spec["positional"]:
        for p in players:
            if not slot_eligible(p.get("position"), p["slot"]):
                errors.append(
                    f"{p['name']} is not eligible at {p['slot']} (listed {p.get('position')})."
                )
        # Never roster a hitter against your own pitcher. Keyed off the P SLOT
        # (not the position string) — more robust than parsing positions.
        pitchers = [p for p in players if p["slot"] == "P"]
        hitters = [p for p in players if p["slot"] != "P"]
        for pit in pitchers:
            for hit in hitters:
                same_game_opposed = (
                    (hit.get("team") and hit.get("team") == pit.get("opponent"))
                    or (hit.get("opponent") and hit.get("opponent") == pit.get("team"))
                )
                if same_game_opposed:
                    errors.append(
                        f"House rule: never roster a hitter against your own pitcher — "
                        f"{hit['name']} ({hit.get('team')}) bats against your pitcher "
                        f"{pit['name']} ({pit.get('team')} vs {pit.get('opponent')})."
                    )

    if not thesis.strip():
        errors.append("Every lineup needs a one-sentence thesis — how does this lineup win?")
    if not what_if.strip():
        errors.append("Add the 'What if?' question this lineup answers.")
    return errors


def resolve_id_lineups(text: str, pool_df: pd.DataFrame, slug: str) -> tuple[list[dict], list[str]]:
    """Parse pasted candidate lineups (one per non-empty line, DK player IDs
    separated by space/comma/tab) and resolve each ID to a pool row via dk_id.

    Returns (lineups, errors). Each lineup: {'label', 'players' (slot-assigned
    rows), 'totals', 'errors' (per-lineup messages)}. `errors` is the flat list
    across all lineups for a quick summary. If the pool has no dk_id column,
    returns ([], [<one explanatory error>]) so the UI can explain the gap."""
    spec = roster_spec(slug)
    if "dk_id" not in pool_df.columns:
        return [], [
            "The selected player pool has no DK IDs, so pasted IDs can't be matched "
            "to players. Select a pool with an ID column (e.g. SaberSim) — the SIN "
            "MLB file doesn't carry IDs."
        ]

    # Build dk_id (as a digits-only string) -> clean player-row dict.
    id_map: dict[str, dict] = {}
    for rec in pool_df.to_dict("records"):
        did = rec.get("dk_id")
        if did is None or (isinstance(did, float) and pd.isna(did)):
            continue
        clean = {k: (None if (isinstance(v, float) and pd.isna(v)) else v) for k, v in rec.items()}
        id_map[str(int(did))] = clean

    lineups: list[dict] = []
    flat_errors: list[str] = []
    for idx, line in enumerate([ln for ln in text.splitlines() if ln.strip()], start=1):
        label = f"Lineup {idx}"
        tokens = [t for t in re.split(r"[\s,;]+", line.strip()) if t]
        players_raw, errs = [], []
        for tok in tokens:
            key = re.sub(r"\D", "", tok)
            if not key:
                continue
            row = id_map.get(key)
            if row is None:
                errs.append(f"{label}: unknown DK ID {tok} — not in the loaded pool.")
            else:
                players_raw.append(row)
        picked, assign_errs = assign_slots(players_raw, spec)
        # thesis/what_if are placeholders so only structural rules fire here.
        val_errs = validate_lineup(slug, picked, thesis="x", what_if="x")
        errs += assign_errs + val_errs
        lineups.append({
            "label": label,
            "players": picked,
            "totals": lineup_totals(picked, spec["cap"]),
            "errors": errs,
        })
        flat_errors += errs
    return lineups, flat_errors


def resolve_pool_candidates(slug: str) -> tuple[list[dict], list[str]]:
    """Resolve EVERY uploaded lineup-pool row to players via the merged
    projections' dk_id, so callers can FILTER/RANK in Python instead of making a
    headless LLM crunch a multi-MB CSV (the old Select/Fix hang). Returns
    (candidates, notes).

    Each candidate dict: {row (1-based), source (filename), ids, names, players,
    salary, avg_own, sub5, sub5_skill, min_sub5_mc, ceil_sum, exp_made_cuts,
    contest_metrics}. Deduped by roster (same set of dk_ids = one candidate).
    `contest_metrics` maps a DECLARED-contest name -> {roi, dupes, win_rate}
    when the pool carries that contest's columns (prefix match)."""
    from src import sessions
    from src.sim_data import load_sim_files
    from src.contests import load_contests

    spec = roster_spec(slug)
    n_slots = len(spec["slots"])

    sources = sessions.merge_same_vendor(sessions.load_sources(slug))
    if not sources:
        return [], ["No projections loaded — upload vendor projections first."]
    pname = max(sources, key=lambda k: len(sources[k]["df"]))
    pdf = sources[pname]["df"]
    if "dk_id" not in pdf.columns:
        return [], ["Projections carry no dk_id column — can't resolve the pool to players."]

    id_map: dict[str, dict] = {}
    for rec in pdf.to_dict("records"):
        did = rec.get("dk_id")
        if did is None or (isinstance(did, float) and pd.isna(did)):
            continue
        id_map[str(int(did))] = rec

    pool_files = load_sim_files(slug)
    if not pool_files:
        return [], ["No lineup-pool CSV uploaded (Sim Data tab)."]

    contests = load_contests(slug)

    def _mc(v):
        try:
            v = float(v)
        except (TypeError, ValueError):
            return 0.0
        return v / 100 if v > 1.5 else v

    seen: set = set()
    cands: list[dict] = []
    notes: list[str] = []
    for pf in pool_files:
        try:
            df = pd.read_csv(pf["path"])
        except Exception as e:  # noqa: BLE001 — surface, don't crash the run
            notes.append(f"Couldn't read {Path(pf['path']).name}: {e}")
            continue
        cols = list(df.columns)
        id_cols = cols[:n_slots]
        # Match each declared contest to its pool columns (prefix match).
        cmatch: dict[str, tuple] = {}
        for c in contests:
            cn = str(c.get("name", "")).strip()
            if not cn:
                continue
            roi = next((col for col in cols if col.startswith(cn) and col.endswith("ROI")), None)
            dup = next((col for col in cols if col.startswith(cn) and col.endswith("Sim Dupes")), None)
            win = next((col for col in cols if col.startswith(cn) and col.endswith("Win Rate")), None)
            if roi or dup or win:
                cmatch[cn] = (roi, dup, win)
        for i, rec in enumerate(df.to_dict("records"), start=1):
            ids = [re.sub(r"\D", "", str(rec.get(c, ""))) for c in id_cols]
            ids = [x for x in ids if x]
            if len(ids) != n_slots:
                continue
            players = [id_map.get(x) for x in ids]
            if any(p is None for p in players):
                continue
            key = frozenset(ids)
            if key in seen:
                continue
            seen.add(key)
            owns = [float(p.get("ownership") or 0) for p in players]
            mcs = [_mc(p.get("make_cut_odds")) for p in players]
            ceils = [float(p.get("ceiling") or 0) for p in players]
            sal = sum(int(p.get("salary") or 0) for p in players)
            sub5 = [j for j, o in enumerate(owns) if o < 5]
            cm = {
                cn: {
                    "roi": rec.get(roi) if roi else None,
                    "dupes": rec.get(dup) if dup else None,
                    "win_rate": rec.get(win) if win else None,
                }
                for cn, (roi, dup, win) in cmatch.items()
            }
            cands.append({
                "row": i,
                "source": Path(pf["path"]).name,
                "ids": ids,
                "names": [p["name"] for p in players],
                "players": players,
                "salary": sal,
                "avg_own": round(sum(owns) / n_slots, 1),
                "sub5": len(sub5),
                "sub5_skill": sum(1 for j in sub5 if mcs[j] >= 0.5),
                "min_sub5_mc": round(min((mcs[j] for j in sub5), default=1.0), 2),
                "ceil_sum": round(sum(ceils), 1),
                "exp_made_cuts": round(sum(mcs), 2),
                "contest_metrics": cm,
            })
    return cands, notes


def next_lineup_number(slug: str) -> int:
    """1 + the highest '## Lineup N' heading in data/lineups/<slug>.md; 1 if none."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if not p.exists():
        return 1
    nums = [int(m) for m in re.findall(r"(?m)^## Lineup\s+(\d+)", p.read_text())]
    return max(nums) + 1 if nums else 1


def _roster_table(slug: str, players: list[dict]) -> str:
    """Markdown roster table with columns adapted to the sport's data."""
    def own(p):
        return f"{float(p['ownership']):.1f}%" if p.get("ownership") is not None else ""

    def proj(p):
        return f"{float(p['proj_points']):.1f}" if p.get("proj_points") is not None else ""

    def sal(p):
        return f"${int(p['salary']):,}"

    if slug == "mlb_classic":
        head = "| Player | Pos | Team | Salary | Proj | Own% |"
        rows = [
            f"| {p['name']} | {p['slot']} | "
            f"{p.get('team', '')}{' (vs ' + str(p['opponent']) + ')' if p.get('opponent') else ''} | "
            f"{sal(p)} | {proj(p)} | {own(p)} |"
            for p in players
        ]
    elif slug == "mma_se":
        has_win = any(p.get("win_prob") is not None for p in players)
        head = "| Fighter | Opponent | Salary | Proj | Own% |" + (" Win% |" if has_win else "")
        rows = []
        for p in players:
            row = f"| {p['name']} | {p.get('opponent', '')} | {sal(p)} | {proj(p)} | {own(p)} |"
            if has_win:
                w = p.get("win_prob")
                row += f" {float(w):.0f}% |" if w is not None else " |"
            rows.append(row)
    elif slug == "nascar":
        head = "| Driver | Start | Salary | Proj | Own% |"
        rows = [
            f"| {p['name']} | {p.get('starting_position', '')} | {sal(p)} | {proj(p)} | {own(p)} |"
            for p in players
        ]
    else:  # golf — never any CPT wording
        def _score(p):  # current_score: float to-par, may be None/NaN
            v = p.get("current_score")
            return v if (v is not None and v == v) else None
        has_tee = any(p.get("tee_time") for p in players)
        has_score = any(_score(p) is not None for p in players)
        head = (
            "| Golfer |"
            + (" Tee time |" if has_tee else "")
            + (" Score |" if has_score else "")
            + " Salary | Proj | Own% |"
        )
        rows = []
        for p in players:
            tee = f" {p.get('tee_time', '')} |" if has_tee else ""
            sc = _score(p)
            score = (f" {sc:+.0f} |" if sc is not None else " |") if has_score else ""
            rows.append(f"| {p['name']} |{tee}{score} {sal(p)} | {proj(p)} | {own(p)} |")

    sep = "|" + "---|" * (head.count("|") - 1)
    return "\n".join([head, sep, *rows])


def load_ranking_theses(slug: str) -> dict:
    """Label -> {'thesis', 'what_if'} from the ranker's sidecar, or {} if none."""
    p = _RANKING_DIR / f"{slug}_theses.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return {}


def load_ranking_input(slug: str) -> list[dict]:
    """The ranked candidate lineups snapshot (players + totals + label), or []."""
    p = _RANKING_DIR / f"{slug}_input.json"
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text()).get("lineups", [])
    except json.JSONDecodeError:
        return []


def format_handbuilt_lineup(
    slug: str, lineup_number: int, lineup_name: str,
    thesis: str, what_if: str, players: list[dict], totals: dict,
    tag: str = "handbuilt",
) -> str:
    salaries = " + ".join(f"{int(p['salary']):,}" for p in players)
    cap = roster_spec(slug)["cap"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    source = "Selected from uploaded pool" if tag == "from uploaded pool" else "Handbuilt"
    return "\n".join([
        f'## Lineup {lineup_number} — "{lineup_name}" ({tag})',
        "",
        f"**Thesis:** {thesis.strip()}",
        "",
        _roster_table(slug, players),
        "",
        f"**Salary check:** {salaries} = **${totals['salary_used']:,} ≤ ${cap:,}** ✓ "
        f"(${totals['salary_left']:,} unspent)",
        "",
        f"**Projected points:** ~{totals['proj_total']}",
        "",
        f"**What if?** — *{what_if.strip()}*",
        "",
        f"**Construction notes:** {source} {ts}. Total own {totals['own_total']}% · "
        f"avg {totals['own_avg']}%/player · {totals['n_sub10']} sub-10% player(s).",
    ])


def append_handbuilt_lineup(
    slug: str, contest_label: str, lineup_name: str,
    thesis: str, what_if: str, players: list[dict], tag: str = "handbuilt",
) -> int:
    """Append a handbuilt lineup to data/lineups/<slug>.md (creating it with a
    header if missing). Returns the lineup number used. Raises ValueError on
    rule violations — the UI validates first; this is the backstop."""
    errors = validate_lineup(slug, players, thesis, what_if)
    if errors:
        raise ValueError("; ".join(errors))

    n = next_lineup_number(slug)
    totals = lineup_totals(players, roster_spec(slug)["cap"])
    default_name = "From pool" if tag == "from uploaded pool" else "Handbuilt"
    block = format_handbuilt_lineup(
        slug, n, lineup_name.strip() or default_name, thesis, what_if, players, totals, tag=tag
    )

    p = _LINEUPS_DIR / f"{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        header = (
            f"# {contest_label} — Lineup Portfolio ({datetime.now().strftime('%Y-%m-%d')})\n\n"
            "*(Started from the Handbuild tab — no Claude-built lineups on this slate yet.)*\n"
        )
        p.write_text(header + "\n---\n\n" + block + "\n")
    else:
        with p.open("a") as f:
            f.write("\n\n---\n\n" + block + "\n")
    return n
