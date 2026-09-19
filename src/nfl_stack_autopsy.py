"""NFL Classic stack-centric autopsy ("Phase 4", 9/14/26).

Reads every lineup in a DK NFL Classic contest-standings file as a STACK
SHAPE — did the lineup pair its quarterback with teammates, did it carry a
player from the other side of that game (a "bring-back"), how many running
backs did it play, and how many players came from one game — then compares
the whole field, the top 1%, the top 20 and the user's own entries, and
says the winning lineup's shape in words.

The stack vocabulary comes from `src/nfl_classic_defs.py` (shared verbatim
with the Sim): a stack mate is ANY non-DST teammate of the QB, a bring-back
is ANY non-DST player on the QB's opponent.

What is needed: DK standings carry each player's roster slot (the Lineup
string: "QB Lamar Jackson RB Jahmyr Gibbs FLEX ..."), so positions are
mostly known from the standings alone. TEAMS are not in the standings — they
come from the slate's still-loaded projections (team + opponent columns). No
projections ⇒ the report degrades to "not gradable" and says why; it never
crashes the autopsy. Descriptive only: nothing here is a rule.
"""
from __future__ import annotations

import re
from collections import Counter

from src.nfl_classic_defs import (
    STACK_MATE_POSITIONS, game_key, normalize_opponent, normalize_position,
    normalize_team, stack_shape,
)

# Slot markers DK uses in a Classic lineup string. FLEX is a slot, not a
# position — the player's real position comes from the standings' own
# per-player table or the projections.
_SLOT_RE = re.compile(r"(?:^|\s)(CPT|UTIL|FLEX|DST|QB|RB|WR|TE)\s+")
_SLOT_ONLY = ("FLEX", "CPT", "UTIL")

SHAPE_WORDS = {
    "naked": "no stack (QB alone)",
    "stack1": "single stack (QB + 1 teammate)",
    "stack2": "double stack (QB + 2 teammates)",
    "stack3plus": "triple-plus stack (QB + 3 or more teammates)",
}
_SHAPE_ORDER = ("naked", "stack1", "stack2", "stack3plus")


def lineup_slots(lineup_str) -> list[tuple[str, str]]:
    """[(slot, name), ...] from a DK Classic lineup string, in DK's order."""
    if not isinstance(lineup_str, str):
        return []
    tokens = _SLOT_RE.split(lineup_str)
    out = []
    for i in range(1, len(tokens) - 1, 2):
        name = tokens[i + 1].strip()
        if name:
            out.append((tokens[i].upper(), name))
    return out


def build_lookup(players, proj_df) -> dict:
    """norm-name → {position, team, opponent} for every player the standings
    or the projections know. Positions come from the standings' per-player
    table first (a non-FLEX roster slot IS the position), then projections;
    team + opponent come from projections only (DK standings carry none).
    Returns {} when nothing resolves."""
    from src.autopsy import _norm_name

    lookup: dict = {}
    if players is not None and not getattr(players, "empty", True) \
            and "roster_position" in players.columns:
        for name, slot in zip(players["name"], players["roster_position"]):
            pos = normalize_position(slot)
            if pos and pos not in _SLOT_ONLY:
                lookup.setdefault(_norm_name(name), {})["position"] = pos
    if proj_df is not None and not getattr(proj_df, "empty", True):
        cols = set(proj_df.columns)
        if "team" in cols:
            norm_col = (proj_df["_norm"] if "_norm" in cols
                        else proj_df["name"].apply(_norm_name))
            for norm, (_, r) in zip(norm_col, proj_df.iterrows()):
                entry = lookup.setdefault(norm, {})
                team = normalize_team(r.get("team"))
                if team:
                    entry.setdefault("team", team)
                opp = normalize_opponent(r.get("opponent")) if "opponent" in cols else ""
                if opp:
                    entry.setdefault("opponent", opp)
                pos = normalize_position(r.get("position")) if "position" in cols else ""
                if pos and "position" not in entry:
                    entry["position"] = pos
    return lookup


def _fill_opponents(lookup: dict) -> None:
    """A team's opponent is the same for every player on it — copy it across
    so a player whose projections row lacked an opponent still gets one."""
    by_team: dict = {}
    for e in lookup.values():
        t, o = e.get("team"), e.get("opponent")
        if t and o:
            by_team.setdefault(t, o)
    for e in lookup.values():
        t = e.get("team")
        if t and not e.get("opponent") and t in by_team:
            e["opponent"] = by_team[t]


def read_lineup(lineup_str, lookup: dict) -> dict | None:
    """The stack read of ONE lineup, or None when a player's team or a FLEX
    player's position cannot be resolved (never guess a stack)."""
    from src.autopsy import _norm_name

    slots = lineup_slots(lineup_str)
    if not slots:
        return None
    positions, teams, opps, names = [], [], [], []
    for slot, name in slots:
        norm = _norm_name(name)
        e = lookup.get(norm) or {}
        pos = slot if slot not in _SLOT_ONLY else (e.get("position") or "")
        team, opp = e.get("team") or "", e.get("opponent") or ""
        if not pos or not team or not opp:
            return None
        positions.append(pos)
        teams.append(team)
        opps.append(opp)
        names.append(name)
    shape = stack_shape(positions, teams, opps)
    qb_i = next((i for i, p in enumerate(positions) if p == "QB"), None)
    qb_team = shape["qb_team"]
    qb_opp = opps[qb_i] if qb_i is not None else ""
    mates = [names[i] for i, p in enumerate(positions)
             if i != qb_i and p in STACK_MATE_POSITIONS and teams[i] == qb_team]
    bring = [names[i] for i, p in enumerate(positions)
             if p in STACK_MATE_POSITIONS and qb_opp and teams[i] == qb_opp]
    game_counts = Counter(game_key(t, o) for t, o in zip(teams, opps))
    top_game, top_n = game_counts.most_common(1)[0]
    return {
        **shape,
        "qb": names[qb_i] if qb_i is not None else "",
        "qb_opp": qb_opp,
        "mates_names": mates,
        "bringback_names": bring,
        "rb_count": int(sum(1 for p in positions if p == "RB")),
        "one_game_max": int(top_n),
        "one_game_key": "-".join(top_game),
    }


_SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv", "v"}


def _short(name: str) -> str:
    """Last name without a Jr./III suffix ('Travis Etienne Jr.' → 'Etienne')."""
    toks = [t for t in str(name).split() if t]
    while len(toks) > 1 and toks[-1].lower() in _SUFFIXES:
        toks.pop()
    return toks[-1] if toks else str(name)


def shape_words(read: dict | None) -> str:
    """'Goff double stack + Olave bring-back, 5 from DET-NO'."""
    if not read:
        return "not gradable"
    qb = _short(read["qb"]) if read.get("qb") else "no QB"
    shape = read.get("shape", "naked")
    if shape == "naked":
        head = f"{qb} with no teammate (no stack)"
    else:
        label = {"stack1": "single stack", "stack2": "double stack",
                 "stack3plus": "triple-plus stack"}[shape]
        mates = ", ".join(_short(n) for n in read.get("mates_names") or [])
        head = f"{qb} {label} ({mates})" if mates else f"{qb} {label}"
    bb = read.get("bringback_names") or []
    if bb:
        head += " + " + ", ".join(_short(n) for n in bb) + \
            (" bring-back" if len(bb) == 1 else " bring-backs")
    else:
        head += ", no bring-back"
    extras = []
    if read.get("rb_count", 0) >= 3:
        extras.append(f"{read['rb_count']} RBs")
    if read.get("dst_vs_qb"):
        extras.append("DST against its own QB")
    tail = f"{read.get('one_game_max')} from {read.get('one_game_key')}"
    if extras:
        tail = ", ".join(extras) + ", " + tail
    return f"{head}, {tail}"


def _group_stats(reads: list[dict]) -> dict:
    n = len(reads)
    if not n:
        return {"n": 0}
    pct = lambda k: round(k / n * 100, 1)  # noqa: E731
    shapes = Counter(r["shape"] for r in reads)
    return {
        "n": n,
        "naked_pct": pct(shapes.get("naked", 0)),
        "single_pct": pct(shapes.get("stack1", 0)),
        "double_pct": pct(shapes.get("stack2", 0)),
        "triple_plus_pct": pct(shapes.get("stack3plus", 0)),
        "bringback_pct": pct(sum(1 for r in reads if r["bringback"] > 0)),
        "three_rb_pct": pct(sum(1 for r in reads if r["rb_count"] >= 3)),
        "dst_vs_qb_pct": pct(sum(1 for r in reads if r["dst_vs_qb"])),
        "one_game_max_mean": round(sum(r["one_game_max"] for r in reads) / n, 2),
        "one_game_5plus_pct": pct(sum(1 for r in reads if r["one_game_max"] >= 5)),
    }


def stack_report(parsed: dict, proj_df, is_user=None) -> dict:
    """The per-contest stack report. `parsed` is parse_dk_results' output;
    `proj_df` the still-loaded projections frame (team/opponent/position) or
    None; `is_user` an EntryName predicate (defaults to autopsy.is_user_entry).
    Always returns a dict; `gradable` False carries a plain-language `reason`."""
    from src.autopsy import is_user_entry

    is_user = is_user or is_user_entry
    lineups = parsed["lineups"]
    field = int(len(lineups))
    lookup = build_lookup(parsed.get("players"), proj_df)
    _fill_opponents(lookup)
    if not any(e.get("team") for e in lookup.values()):
        return {"gradable": False, "n_field": field, "n_graded": 0,
                "reason": ("Teams are not in the DK standings and no projections with a "
                           "team column were loaded, so the stacks could not be read.")}

    reads: dict = {}   # row index → read
    for idx, r in lineups.iterrows():
        rd = read_lineup(r.get("Lineup"), lookup)
        if rd is not None:
            reads[idx] = rd
    if not reads:
        return {"gradable": False, "n_field": field, "n_graded": 0,
                "reason": ("No lineup could be matched to the projections' teams "
                           "(names did not join), so the stacks could not be read.")}

    ranks = {idx: int(r) for idx, r in zip(lineups.index, lineups["Rank"])}
    top1_n = max(1, round(0.01 * field))
    field_reads = list(reads.values())
    top1 = [rd for idx, rd in reads.items() if ranks[idx] <= top1_n]
    top20 = [rd for idx, rd in reads.items() if ranks[idx] <= 20]
    user_rows = [(ranks[idx], idx) for idx in reads
                 if is_user(lineups.loc[idx, "EntryName"])]
    user_rows.sort()
    user_reads = [reads[idx] for _, idx in user_rows]

    win_idx = min(reads, key=lambda i: ranks[i])
    winner = reads[win_idx]
    winner_out = {
        "rank": ranks[win_idx],
        "entry_name": str(lineups.loc[win_idx, "EntryName"]),
        "words": shape_words(winner),
        **{k: winner[k] for k in ("shape", "mates", "bringback", "rb_count",
                                  "one_game_max", "one_game_key", "dst_vs_qb", "qb")},
    }
    return {
        "gradable": True,
        "n_field": field,
        "n_graded": len(reads),
        "top1_n": top1_n,
        "groups": {
            "field": _group_stats(field_reads),
            "top1pct": _group_stats(top1),
            "top20": _group_stats(top20),
            "user": _group_stats(user_reads),
        },
        "winner": winner_out,
        "user_lineups": [
            {"rank": rk, "words": shape_words(reads[idx]),
             "shape": reads[idx]["shape"], "bringback": reads[idx]["bringback"],
             "rb_count": reads[idx]["rb_count"],
             "one_game_max": reads[idx]["one_game_max"]}
            for rk, idx in user_rows
        ],
    }


def lineup_reads_for(parsed: dict, proj_df, lineup_strings) -> list[dict | None]:
    """Stack reads for arbitrary lineup strings (used by the shark gap)."""
    lookup = build_lookup(parsed.get("players"), proj_df)
    _fill_opponents(lookup)
    return [read_lineup(s, lookup) for s in lineup_strings]


def stack_summary(report: dict | None) -> str | None:
    """One line for results.jsonl: the numbers the process trend reads."""
    if not report or not report.get("gradable"):
        return None
    g = report["groups"]
    w = report.get("winner") or {}
    parts = []
    for key, label in (("top1pct", "top 1%"), ("field", "field"), ("user", "you")):
        s = g.get(key) or {}
        if s.get("n"):
            parts.append(f"{label}: double stack {s['double_pct']}% · bring-back "
                         f"{s['bringback_pct']}% (n={s['n']})")
    if w.get("words"):
        parts.append(f"winner: {w['words']}")
    return " | ".join(parts)


def stack_md(report: dict | None, source_file: str | None = None) -> str:
    """The '### Stack shapes' block, plain language. Defines the terms the
    first time they appear."""
    title = "### Stack shapes" + (f" — {source_file}" if source_file else "")
    if not report:
        return ""
    if not report.get("gradable"):
        return (f"{title}\n- *Not gradable: {report.get('reason', 'no data')}* "
                f"(load the slate's projections before logging to get this block).")
    g = report["groups"]
    w = report["winner"]
    lines = [
        title,
        "A stack is a quarterback plus his own teammates (any running back, receiver "
        "or tight end). A bring-back is a player from the team the quarterback is "
        "playing against, so the lineup wins when that game turns into a shootout. "
        f"Read from {report['n_graded']:,} of {report['n_field']:,} lineups "
        "(the rest had a player the projections did not know).",
        "",
        f"- **Winning lineup ({w['entry_name']}):** {w['words']}.",
        "",
        "| Group | Lineups | No stack | Single stack | Double stack | 3+ stack | "
        "Bring-back | 3 RBs | DST vs own QB | Most from one game (avg) | 5+ from one game |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for key, label in (("field", "Whole field"),
                       (
                           "top1pct", f"Top 1% (top {report.get('top1_n')})"),
                       ("top20", "Top 20"), ("user", "Your entries")):
        s = g.get(key) or {}
        if not s.get("n"):
            lines.append(f"| {label} | 0 | — | — | — | — | — | — | — | — | — |")
            continue
        lines.append(
            f"| {label} | {s['n']:,} | {s['naked_pct']}% | {s['single_pct']}% | "
            f"{s['double_pct']}% | {s['triple_plus_pct']}% | {s['bringback_pct']}% | "
            f"{s['three_rb_pct']}% | {s['dst_vs_qb_pct']}% | {s['one_game_max_mean']} | "
            f"{s['one_game_5plus_pct']}% |")
    if report.get("user_lineups"):
        lines.append("")
        lines.append("Your lineups, one line each:")
        for u in report["user_lineups"]:
            lines.append(f"- rank {u['rank']:,}: {u['words']}")
    else:
        lines.append("")
        lines.append("- None of your entries were found in this contest.")
    lines.append("")
    lines.append("_Descriptive only — how the field, the winners and you built. "
                 "A rate is information, never a rule._")
    return "\n".join(lines)
