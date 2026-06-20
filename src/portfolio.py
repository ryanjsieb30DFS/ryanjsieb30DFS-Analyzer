"""Deterministic portfolio selection — the part the LLM cannot reliably do.

`run_select_lineups` used to hand Claude a flat 160-row shortlist and ask IT to
guarantee, by reading the table, that the chosen lineups were diverse (no shared
core) and exposure-balanced, then write a prose "Portfolio audit." Counting
shared players across 160 rows and tracking per-player exposure across the picks
is arithmetic over a large grid — exactly where an LLM approximates and asserts a
diversity that isn't actually there (the PGA Classic miss). This module does that
math in Python so it is reproducible:

  * `select_portfolio` pre-prunes the ranked pool into a genuinely DIVERSE menu
    (no two menu rows share more than `max_overlap` players) before the LLM sees
    it, so the LLM picks edge-fit + thesis from already-distinct options.
  * `validate_portfolio` recomputes overlap + exposure on the LLM's FINAL picks
    as a hard gate, and `exposure_report_md` renders the authoritative audit —
    the LLM no longer computes these numbers.

Candidates are the dicts produced by `lineups.resolve_pool_candidates` (each has
`ids` [dk-id strings, one per roster slot], `players`, `salary`, `avg_own`,
`ceil_sum`, `sub5_skill`, `row`, `source`).
"""
from __future__ import annotations

import math


def default_params(n_slots: int) -> dict:
    """Diversity/exposure caps, roster-size scaled. `max_overlap` mirrors the
    existing Fix convention (<=3 shared players on a 6-man roster); `exposure_cap`
    is the max fraction of the FINAL portfolio any one player may appear in."""
    return {
        "max_overlap": max(1, n_slots // 2),  # 6 -> 3, 10 -> 5
        "exposure_cap": 0.6,
    }


def overlap(a: dict, b: dict) -> int:
    """Number of players two candidate lineups share, by dk_id."""
    return len(set(a["ids"]) & set(b["ids"]))


def max_pairwise_overlap(selected: list[dict]) -> int:
    """Largest shared-player count between any two lineups in the set (0 if <2)."""
    worst = 0
    for i in range(len(selected)):
        for j in range(i + 1, len(selected)):
            worst = max(worst, overlap(selected[i], selected[j]))
    return worst


def player_exposure(selected: list[dict]) -> dict[str, dict]:
    """Per-player exposure across a chosen set: dk_id -> {name, count, pct}."""
    n = len(selected)
    counts: dict[str, int] = {}
    names: dict[str, str] = {}
    for c in selected:
        for pid, p in zip(c["ids"], c["players"]):
            counts[pid] = counts.get(pid, 0) + 1
            names.setdefault(pid, (p or {}).get("name", pid))
    return {
        pid: {"name": names[pid], "count": k,
              "pct": round(100 * k / n, 1) if n else 0.0}
        for pid, k in counts.items()
    }


def _runs(c: dict, name: str) -> bool:
    """True if the lineup rosters a player with this name."""
    return any((p or {}).get("name") == name for p in c["players"])


def select_portfolio(
    candidates: list[dict],
    n_target: int,
    params: dict,
    anchor_groups: list[dict] | None = None,
    oversample: int = 4,
    floor: int = 30,
) -> tuple[list[dict], list[tuple[dict, str]], dict]:
    """Prune a PRIORITY-ORDERED candidate list into a diverse menu for the LLM.

    Walks `candidates` best-first (the caller pre-ranks ceiling-up / chalk-down)
    and admits a lineup only if it shares <= `max_overlap` players with every
    lineup already admitted — so the menu is free of near-duplicates. The menu is
    grown to ~`max(n_target*oversample, floor)` rows (capped by what's available).
    If `anchor_groups` is given (from `landscape.anchor_equivalence_check`), the
    menu is guaranteed to contain >=1 lineup that AVOIDS each group's top-owned
    anchor, so the final pick can satisfy the Anchor-Equivalence rule.

    Returns (menu, rejected, report). `rejected` is [(candidate, reason)] for
    traceability; `report` summarizes the prune.
    """
    max_overlap = params["max_overlap"]
    target_menu = min(len(candidates), max(n_target * oversample, floor))

    menu: list[dict] = []
    rejected: list[tuple[dict, str]] = []
    for c in candidates:
        if len(menu) >= target_menu:
            break
        clash = next((m for m in menu if overlap(c, m) > max_overlap), None)
        if clash is not None:
            rejected.append(
                (c, f"shares {overlap(c, clash)} players (> {max_overlap}) with "
                    f"{clash['source']} row {clash['row']}")
            )
            continue
        menu.append(c)

    # Never starve the LLM below the requested count: if strict diversity left
    # fewer than n_target options, relax overlap and top up with the best
    # remaining rows (flagged so the audit knows they're overlap-relaxed).
    relaxed = 0
    if len(menu) < min(n_target, len(candidates)):
        picked_ids = {(c["source"], c["row"]) for c in menu}
        for c in candidates:
            if len(menu) >= min(n_target, len(candidates)):
                break
            if (c["source"], c["row"]) in picked_ids:
                continue
            menu.append(c)
            relaxed += 1

    # Anchor-Equivalence coverage: make sure the menu offers a way to run the
    # alternative anchor for each chalk-equivalent group.
    anchor_added = 0
    for grp in (anchor_groups or []):
        primary = grp["players"][0]  # highest-owned anchor in the group
        if any(not _runs(m, primary) for m in menu):
            continue  # already coverable
        alt = next((c for c in candidates
                    if not _runs(c, primary)
                    and (c["source"], c["row"]) not in
                    {(m["source"], m["row"]) for m in menu}), None)
        if alt is not None:
            menu.append(alt)
            anchor_added += 1

    report = {
        "n_in": len(candidates),
        "n_menu": len(menu),
        "n_rejected_dupe": len(rejected),
        "n_overlap_relaxed": relaxed,
        "n_anchor_coverage_added": anchor_added,
        "max_overlap": max_overlap,
    }
    return menu, rejected, report


def validate_portfolio(
    selected: list[dict],
    params: dict,
    anchor_groups: list[dict] | None = None,
) -> list[str]:
    """Hard gate on the FINAL picks: recompute overlap, exposure, and Anchor-
    Equivalence and return one plain-English string per violation ([] = clean)."""
    violations: list[str] = []
    max_overlap = params["max_overlap"]
    n = len(selected)

    for i in range(n):
        for j in range(i + 1, n):
            ov = overlap(selected[i], selected[j])
            if ov > max_overlap:
                shared = ", ".join(
                    sorted((p or {}).get("name", pid)
                           for pid, p in zip(selected[i]["ids"], selected[i]["players"])
                           if pid in set(selected[j]["ids"]))
                )
                violations.append(
                    f"Lineups {i + 1} & {j + 1} share {ov} players (> {max_overlap}): {shared}"
                )

    exposure_limit = math.ceil(params["exposure_cap"] * n) if n else 0
    for pid, info in player_exposure(selected).items():
        if n and info["count"] > exposure_limit:
            violations.append(
                f"{info['name']} appears in {info['count']}/{n} lineups "
                f"({info['pct']}%) — over the {int(params['exposure_cap'] * 100)}% cap"
            )

    for grp in (anchor_groups or []):
        primary = grp["players"][0]
        if selected and all(_runs(c, primary) for c in selected):
            alts = " / ".join(grp["players"][1:]) or "an alternative"
            violations.append(
                f"Anchor-Equivalence: every lineup runs {primary} "
                f"({grp['players']}); at least one must run {alts}"
            )
    return violations


def exposure_report_md(
    selected: list[dict],
    params: dict,
    anchor_groups: list[dict] | None = None,
) -> str:
    """The authoritative, Python-computed '## Portfolio audit (computed)' block —
    per-player exposure, max pairwise overlap, and pass/flag lines."""
    n = len(selected)
    if not n:
        return "## Portfolio audit (computed)\n\n*No selected lineups to audit.*"

    exp = player_exposure(selected)
    rows = sorted(exp.values(), key=lambda r: (-r["count"], r["name"]))
    table = ["| Player | Lineups | Exposure |", "|---|---|---|"]
    table += [f"| {r['name']} | {r['count']}/{n} | {r['pct']}% |" for r in rows]

    worst = max_pairwise_overlap(selected)
    violations = validate_portfolio(selected, params, anchor_groups)
    status = "✅ no cap violations" if not violations else "⚠️ " + "; ".join(violations)

    return "\n".join([
        "## Portfolio audit (computed)",
        "",
        f"*Computed in Python over {n} pool-selected lineup(s) — not an LLM estimate.*",
        "",
        f"- **Max pairwise overlap:** {worst} shared player(s) "
        f"(cap {params['max_overlap']})",
        f"- **Exposure cap:** {int(params['exposure_cap'] * 100)}% "
        f"(max {math.ceil(params['exposure_cap'] * n)}/{n} lineups per player)",
        f"- **Check:** {status}",
        "",
        "### Player exposure",
        *table,
    ])
