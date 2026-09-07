#!/usr/bin/env python3
"""Blend-weight sweep on the LIVE task: does adding ROI to the picker's blend
help it capture contest winners?

    .venv/bin/python scripts/blend_sweep.py [--slug mma_se] [--slice 500]

For every archived slate (rules/<slug>/history/), for every contest with a
logged winning score AND a Sim scored pool: rebuild each pool row's blend
inputs — top1/cash/roi from the Sim's contest-matched pre-lock sim metrics,
projection and average ownership reconstructed from the Sim's slate capture
(pre-lock proj_points / proj_own per player) — then rank the pool under each
candidate weight set and measure, per the 8/29/26 rebuild's definitions:

  * SLICE capture — does the top-<slice> by blend hold a lineup whose actual
    score meets the winning score? (the live blend's 58% metric)
  * PICK percentile — where the #1-by-blend lineup's actual lands in the pool.

PRE-REGISTERED GATE (set before running, per feedback_gate_on_the_live_task):
an ROI-inclusive blend ships ONLY if its slice capture BEATS the live weights'
capture on the same contests (ties do NOT ship — live stays), its pick
percentile does not regress, and the winning ROI weight is not at the sweep's
grid edge. This script is read-only: it never writes weights anywhere.

Candidate sets: the live 0.45/0.28/0.17/0.10 (roi 0) as baseline; ROI diluting
all four proportionally at w = 0.05..0.30; and one "ROI replaces cash" set —
ROI and cash are cousins (both priced off the same sim), so the interesting
question is whether ROI adds anything cash doesn't already carry.
"""
from __future__ import annotations

import argparse
import glob
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lineup_selection import _norm, _strat_norm  # noqa: E402
from src.picker_check import default_sim_root, scored_pool_raw  # noqa: E402

_REPO = Path(__file__).parent.parent

# (label, top1, cash, proj, own, roi) — roi=0 rows are baselines.
_LIVE = ("live 0.45/0.28/0.17/0.10 (no ROI)", 0.45, 0.28, 0.17, 0.10, 0.0)


def _weight_sets() -> list[tuple]:
    out = [_LIVE]
    for w in (0.05, 0.10, 0.15, 0.20, 0.30):
        k = 1.0 - w
        out.append((f"ROI {w:.2f} (others x{k:.2f})",
                    round(0.45 * k, 3), round(0.28 * k, 3),
                    round(0.17 * k, 3), round(0.10 * k, 3), w))
    out.append(("ROI replaces cash 0.45/0/0.17/0.10/0.28",
                0.45, 0.0, 0.17, 0.10, 0.28))
    return out


def _player_table(sim_root: Path, slug: str, contest_id: str) -> dict | None:
    """name -> (proj_points, proj_own) from the Sim's slate capture for this
    contest — the PRE-LOCK numbers the picker saw, not actuals."""
    hits = glob.glob(str(sim_root / "rules" / slug / "slate_data"
                         / f"*_{contest_id}_*.json"))
    if not hits:
        return None
    try:
        cap = json.loads(Path(hits[0]).read_text())
    except (OSError, json.JSONDecodeError):
        return None
    out = {}
    for r in cap.get("players") or []:
        nm = _strat_norm(str(r.get("name") or ""))
        if nm:
            out[nm] = (r.get("proj_points"), r.get("proj_own"))
    return out or None


def _contest_rows(hist: Path, slug: str, sim_root: Path) -> list[dict]:
    """One record per contest in one archived slate: winning score + per-pool-row
    blend inputs. Contests missing any leg are skipped, never guessed."""
    try:
        autopsy = json.loads((hist / "autopsy.json").read_text())
    except (OSError, json.JSONDecodeError):
        return []
    out = []
    for rec in autopsy if isinstance(autopsy, list) else []:
        cid = str(rec.get("contest_id") or "")
        try:
            win = float(rec.get("winning_score"))
        except (TypeError, ValueError):
            continue
        pool = scored_pool_raw(sim_root, slug, cid) if cid else None
        if not pool:
            continue
        ptab = _player_table(sim_root, slug, cid)
        rows = []
        for r in pool:
            a = r.get("actual_score")
            if a is None:
                continue
            proj = own = None
            if ptab:
                names = [_strat_norm(x.strip())
                         for x in str(r.get("players") or "").split(",")]
                vals = [ptab.get(n) for n in names if n]
                if vals and all(v is not None for v in vals):
                    pjs = [v[0] for v in vals]
                    ows = [v[1] for v in vals]
                    if all(x is not None for x in pjs):
                        proj = float(sum(pjs))
                    if all(x is not None for x in ows):
                        own = float(statistics.mean(ows))
            rows.append({
                "actual": float(a),
                "top1": r.get("pre_sim_top1_pct"),
                "cash": r.get("pre_sim_cash_pct"),
                "roi": r.get("pre_sim_roi_pct"),
                "proj": proj, "own": own,
            })
        if not rows:
            continue
        out.append({"slate": hist.name, "contest_id": cid, "win": win,
                    "rows": rows})
    return out


def _evaluate(contest: dict, wt: tuple, slice_n: int) -> dict:
    _lbl, w_t1, w_ca, w_pj, w_ow, w_roi = wt
    rows = contest["rows"]
    t1 = _norm([r["top1"] for r in rows])
    ca = _norm([r["cash"] for r in rows])
    pj = _norm([r["proj"] for r in rows])
    ow = _norm([r["own"] for r in rows])
    roi = _norm([r["roi"] for r in rows])
    score = [w_t1 * t1[i] + w_ca * ca[i] + w_pj * pj[i]
             + w_ow * ow[i] + w_roi * roi[i] for i in range(len(rows))]
    order = sorted(range(len(rows)), key=lambda i: -score[i])
    top = order[:slice_n]
    win = contest["win"]
    pick_actual = rows[order[0]]["actual"]
    actuals = [r["actual"] for r in rows]
    return {
        "slice_capture": any(rows[i]["actual"] >= win for i in top),
        "pick_pctile": 100.0 * sum(1 for a in actuals if a < pick_actual)
                       / len(actuals),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", default="mma_se")
    ap.add_argument("--slice", type=int, default=500,
                    help="candidate-slice size (live picker uses 500)")
    ap.add_argument("--sim-root", type=Path, default=default_sim_root())
    args = ap.parse_args()

    contests = []
    for hist in sorted((_REPO / "rules" / args.slug / "history").glob("*")):
        if hist.is_dir():
            contests.extend(_contest_rows(hist, args.slug, args.sim_root))
    if not contests:
        print(f"{args.slug}: no contests with winning score + scored pool "
              f"+ slate capture — nothing to sweep")
        return 1
    n_missing_proj = sum(1 for c in contests
                         if all(r["proj"] is None for r in c["rows"]))
    print(f"{args.slug}: {len(contests)} contests across "
          f"{len({c['slate'] for c in contests})} slates, slice={args.slice}"
          + (f"  (⚠ {n_missing_proj} contests have NO reconstructable "
             f"projection column — proj term normalizes to 0 there)"
             if n_missing_proj else ""))

    results = []
    for wt in _weight_sets():
        evs = [_evaluate(c, wt, args.slice) for c in contests]
        cap = 100.0 * sum(e["slice_capture"] for e in evs) / len(evs)
        med_pct = statistics.median(e["pick_pctile"] for e in evs)
        results.append((wt[0], cap, med_pct, wt[5]))
    base_cap, base_pct = results[0][1], results[0][2]

    print(f"\n{'weights':44} {'slice capture':>14} {'median pick pctile':>19}")
    for lbl, cap, med_pct, _w in results:
        mark = " <- live" if lbl == _LIVE[0] else ""
        print(f"{lbl:44} {cap:13.1f}% {med_pct:18.1f}%{mark}")

    roi_rows = [r for r in results[1:] if r[3] > 0]
    best = max(roi_rows, key=lambda r: (r[1], r[2]))
    edge = best[3] == 0.30
    print("\nGATE (pre-registered): ship an ROI blend only if it BEATS "
          f"{base_cap:.1f}% capture (ties stay live), pick pctile holds "
          f"(live {base_pct:.1f}%), and the ROI weight is interior.")
    if best[1] > base_cap and best[2] >= base_pct - 1.0 and not edge:
        print(f"VERDICT: '{best[0]}' PASSES — capture {best[1]:.1f}% vs live "
              f"{base_cap:.1f}%. Present to the user before shipping; this "
              f"script never writes weights.")
    else:
        why = []
        if best[1] <= base_cap:
            why.append(f"best ROI capture {best[1]:.1f}% does not beat live "
                       f"{base_cap:.1f}%")
        if best[2] < base_pct - 1.0:
            why.append("pick percentile regresses")
        if edge:
            why.append("winner sits on the ROI grid edge (0.30)")
        print(f"VERDICT: DO NOT SHIP — {'; '.join(why)}. Live weights stay.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
