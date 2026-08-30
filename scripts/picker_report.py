#!/usr/bin/env python
"""Was the miss in the TABLE or in the PICK? — the cross-slate trend.

    .venv/bin/python scripts/picker_report.py
    .venv/bin/python scripts/picker_report.py --slug mma_se
    .venv/bin/python scripts/picker_report.py --sim-root /path/to/ryanjsieb30DFS

Read-only. Writes nothing, ships nothing, changes no parameter.

The per-slate measurement lives in `src/picker_check.py` and runs
automatically at Log Autopsy (archived as picker_check.json, read by the
post-autopsy review). This script runs the SAME measurement over every
archived slate at once, for the trend a single autopsy can't show: is the
pick step improving, and is the slice capturing winners at the rate the
8/29 rework was tuned for?
"""
from __future__ import annotations

import argparse
import statistics as st
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from src.picker_check import default_sim_root, slate_rows  # noqa: E402

SLUGS = ["mma_se", "nascar", "pga_classic", "pga_rd4_sd"]


def _median(vals):
    return round(st.median(vals), 1) if vals else None


def report(slug: str, sim_root: Path) -> str:
    hist_root = _ROOT / "rules" / slug / "history"
    rows = []
    for hist in sorted(hist_root.iterdir()) if hist_root.exists() else []:
        rows.extend(slate_rows(hist, slug, sim_root))
    L = [f"### {slug} — {len(rows)} measurable contest(s)"]
    if not rows:
        L.append("  nothing measurable yet: needs an archived pick, a logged "
                 "autopsy (winning score), and the Sim's scored pool for the "
                 "same contest.")
        return "\n".join(L)
    held = [r for r in rows if r["pool_held_winner"]]
    sliced = [r for r in rows if "slice_held_winner" in r]
    L.append(f"  POOL   held a contest-winning lineup in {len(held)} of "
             f"{len(rows)} — the Sim's build ceiling.")
    if sliced:
        s_held = sum(1 for r in sliced if r["slice_held_winner"])
        L.append(f"  SLICE  (the {len(sliced)} contest(s) with an archived "
                 f"table) held one in {s_held} of {len(sliced)}.")
    else:
        L.append("  SLICE  no archived tables yet — they archive with every "
                 "autopsy from 8/30/26 on; this line fills in next slate.")
    won = sum(1 for r in rows if r["pick_won"])
    L.append(f"  PICK   scored >= the winning score in {won} of {len(rows)}; "
             f"median pick beat {_median([r['pick_pool_pctile'] for r in rows])}% "
             "of the pool it was chosen from.")
    for r in rows:
        extra = ""
        if "slice_held_winner" in r:
            extra = (f" · slice held winner: {'YES' if r['slice_held_winner'] else 'no'}"
                     f" · rows on the table above the pick: {r['n_slice_above_pick']}")
        L.append(f"    {r['date']} {r['contest'][:44]:44s} win {r['winning_score']:7.1f}"
                 f" · pool max {r['pool_max']:7.1f}"
                 f" ({'held winner' if r['pool_held_winner'] else 'no winner':>11s})"
                 f" · pick {r['pick_actual']:7.1f}"
                 f" (beat {r['pick_pool_pctile']}% of pool){extra}")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", choices=SLUGS)
    ap.add_argument("--sim-root", type=Path, default=default_sim_root(),
                    help="Path to the Sim repo (scored pools live there).")
    args = ap.parse_args()
    if not (args.sim_root / "rules").exists():
        print(f"Sim repo not found at {args.sim_root} — pass --sim-root.")
        return 1
    print("Was the miss in the TABLE or in the PICK?  (per contest: the pool's")
    print("ceiling, whether it reached the shown table, and where the pick landed)")
    print()
    for slug in ([args.slug] if args.slug else SLUGS):
        print(report(slug, args.sim_root))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
