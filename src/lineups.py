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

_LINEUPS_DIR = Path(__file__).parent.parent / "data" / "lineups"
_RED_TEAM_DIR = Path(__file__).parent.parent / "data" / "red_team"
_HB_ANALYSIS_DIR = Path(__file__).parent.parent / "data" / "handbuild_analysis"


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
        if p["name"] in seen:
            errors.append(f"Duplicate player: {p['name']}.")
        seen.add(p["name"])

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
        has_tee = any(p.get("tee_time") for p in players)
        head = "| Golfer |" + (" Tee time |" if has_tee else "") + " Salary | Proj | Own% |"
        rows = []
        for p in players:
            tee = f" {p.get('tee_time', '')} |" if has_tee else ""
            rows.append(f"| {p['name']} |{tee} {sal(p)} | {proj(p)} | {own(p)} |")

    sep = "|" + "---|" * (head.count("|") - 1)
    return "\n".join([head, sep, *rows])


def format_handbuilt_lineup(
    slug: str, lineup_number: int, lineup_name: str,
    thesis: str, what_if: str, players: list[dict], totals: dict,
) -> str:
    salaries = " + ".join(f"{int(p['salary']):,}" for p in players)
    cap = roster_spec(slug)["cap"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    return "\n".join([
        f'## Lineup {lineup_number} — "{lineup_name}" (handbuilt)',
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
        f"**Construction notes:** Handbuilt {ts}. Total own {totals['own_total']}% · "
        f"avg {totals['own_avg']}%/player · {totals['n_sub10']} sub-10% player(s).",
    ])


def append_handbuilt_lineup(
    slug: str, contest_label: str, lineup_name: str,
    thesis: str, what_if: str, players: list[dict],
) -> int:
    """Append a handbuilt lineup to data/lineups/<slug>.md (creating it with a
    header if missing). Returns the lineup number used. Raises ValueError on
    rule violations — the UI validates first; this is the backstop."""
    errors = validate_lineup(slug, players, thesis, what_if)
    if errors:
        raise ValueError("; ".join(errors))

    n = next_lineup_number(slug)
    totals = lineup_totals(players, roster_spec(slug)["cap"])
    block = format_handbuilt_lineup(
        slug, n, lineup_name.strip() or "Handbuilt", thesis, what_if, players, totals
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
