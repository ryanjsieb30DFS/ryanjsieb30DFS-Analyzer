"""Sim Data analytics — read a SaberSim lineup-pool export and surface, for any
sport, what the sim LIKES and FADES and which player COMBINATIONS it piles into.

ANALYTICS ONLY. This module never assembles, ranks, or returns a playable lineup —
it reports individual-player exposures and co-occurring combinations as
fade/leverage signal, consistent with the Analyzer's hard "never build lineups"
rule. The combinations are surfaced to be *aware of / fade for duplication*, not
to play together.

A SaberSim pool CSV = one row per simulated lineup. The leading columns are the
roster slots (6 for golf/MMA/NASCAR, 10 for MLB) holding DK player IDs, then a
blank separator, then per-lineup metrics (Proj Score, percentiles, Ownership,
Salary, Saber Score, per-contest ROI/Dupes/Win Rate/Cash Rate).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations

import pandas as pd

from src.autopsy import _norm_name
from src.dk_ids import fmt_id


def load_sim_pool(file_or_buffer) -> dict:
    """Parse a SaberSim lineup-pool CSV into a structured dict.

    Returns {lineups, roster_slots, metric_cols, contest_cols, n}. `lineups` is a
    DataFrame with a `__ids` column (list of DK ids per lineup) plus the metric
    columns. Empty dict-shape on an unrecognizable file."""
    try:
        df = pd.read_csv(file_or_buffer)
    except Exception:  # noqa: BLE001
        return {"lineups": pd.DataFrame(), "roster_slots": [], "metric_cols": [], "contest_cols": [], "n": 0}

    cols = list(df.columns)
    # Roster slots = the leading columns before the blank separator / 'Proj Score'.
    cut = len(cols)
    for i, c in enumerate(cols):
        cl = str(c).strip().lower()
        if cl.startswith("unnamed") or cl == "proj score":
            cut = i
            break
    roster_slots = cols[:cut]
    if not roster_slots:
        return {"lineups": pd.DataFrame(), "roster_slots": [], "metric_cols": [], "contest_cols": [], "n": 0}

    metric_cols = [c for c in cols[cut:] if not str(c).strip().lower().startswith("unnamed")]

    def _ids(row) -> list[str]:
        out = []
        for s in roster_slots:
            v = row[s]
            if pd.isna(v):
                continue
            out.append(fmt_id(v))
        return out

    work = df.copy()
    work["__ids"] = work.apply(_ids, axis=1)
    lineups = work[["__ids"] + [c for c in metric_cols if c in work.columns]].reset_index(drop=True)
    contest_cols = [c for c in metric_cols
                    if str(c).endswith("ROI") or "Win Rate" in str(c) or "Cash Rate" in str(c)]
    return {"lineups": lineups, "roster_slots": roster_slots,
            "metric_cols": metric_cols, "contest_cols": contest_cols, "n": int(len(lineups))}


def _quality_col(lineups: pd.DataFrame) -> str | None:
    for c in ("Saber Score", "Proj Score"):
        if c in lineups.columns:
            return c
    return None


def player_exposure(pool: dict, id_to_name: dict[str, str],
                    projections: pd.DataFrame | None = None) -> pd.DataFrame:
    """Per-player sim exposure across the pool, joined to field ownership.

    Columns: player, dk_id, sim_exposure_pct, lineups, avg_saber, field_own_pct
    (when projections carry ownership). Sorted by sim exposure desc. When
    projections are supplied, the FULL projection universe is included so
    sim-faded-but-rostered players appear at 0% (that's the 'bad plays' signal)."""
    lineups, n = pool.get("lineups", pd.DataFrame()), pool.get("n", 0)
    if lineups.empty or n == 0:
        return pd.DataFrame()

    qcol = _quality_col(lineups)
    count: dict[str, int] = defaultdict(int)
    qsum: dict[str, float] = defaultdict(float)
    for _, row in lineups.iterrows():
        q = row[qcol] if qcol else None
        for pid in set(row["__ids"]):
            count[pid] += 1
            if q is not None and pd.notna(q):
                qsum[pid] += float(q)

    rows = []
    for pid, c in count.items():
        rows.append({
            "dk_id": pid,
            "player": id_to_name.get(pid, pid),
            "sim_exposure_pct": round(100.0 * c / n, 1),
            "lineups": c,
            "avg_saber": round(qsum[pid] / c, 1) if c and pid in qsum else None,
        })
    exp = pd.DataFrame(rows)

    if projections is not None and not projections.empty \
            and {"name", "ownership"}.issubset(projections.columns):
        own = {_norm_name(nm): o for nm, o in zip(projections["name"], projections["ownership"])
               if pd.notna(o)}
        # Include projection players the sim never used (exposure 0) — the fades.
        seen = {_norm_name(p) for p in exp["player"]}
        extra = []
        for nm, o in zip(projections["name"], projections["ownership"]):
            if _norm_name(nm) in seen:
                continue
            extra.append({"dk_id": None, "player": str(nm), "sim_exposure_pct": 0.0,
                          "lineups": 0, "avg_saber": None})
        if extra:
            exp = pd.concat([exp, pd.DataFrame(extra)], ignore_index=True)
        exp["field_own_pct"] = exp["player"].apply(lambda nm: own.get(_norm_name(nm)))

    return exp.sort_values("sim_exposure_pct", ascending=False).reset_index(drop=True)


def good_bad_plays(exposure: pd.DataFrame, top_n: int = 12) -> dict:
    """Split exposure into the actionable buckets.

    good = sim core (top exposure); bad = sim fades (lowest exposure / 0). When
    field ownership is present: leverage = sim>>field (sim sees value the field
    sleeps on); trap = field>>sim (field chalk the sim won't touch)."""
    out: dict[str, pd.DataFrame] = {"good": pd.DataFrame(), "bad": pd.DataFrame(),
                                    "leverage": pd.DataFrame(), "trap": pd.DataFrame()}
    if exposure.empty:
        return out
    out["good"] = exposure.head(top_n)
    out["bad"] = exposure.sort_values("sim_exposure_pct").head(top_n).reset_index(drop=True)

    if "field_own_pct" in exposure.columns and exposure["field_own_pct"].notna().any():
        e = exposure.dropna(subset=["field_own_pct"]).copy()
        e["edge"] = (e["sim_exposure_pct"] - e["field_own_pct"]).round(1)
        cols = ["player", "sim_exposure_pct", "field_own_pct", "edge", "avg_saber"]
        cols = [c for c in cols if c in e.columns]
        out["leverage"] = e.sort_values("edge", ascending=False).head(top_n)[cols].reset_index(drop=True)
        out["trap"] = e.sort_values("edge").head(top_n)[cols].reset_index(drop=True)
    return out


def chalky_combinations(pool: dict, id_to_name: dict[str, str],
                        sizes: tuple[int, ...] = (2, 3), top_n: int = 15) -> pd.DataFrame:
    """Top co-occurring player groups across the pool — duplication/chalk signal.

    Columns: size, combo (names joined by ' + '), joint_exposure_pct, lineups.
    These are combos to be AWARE of / fade for duplication, NOT lineups to play."""
    lineups, n = pool.get("lineups", pd.DataFrame()), pool.get("n", 0)
    if lineups.empty or n == 0:
        return pd.DataFrame()

    counters = {k: Counter() for k in sizes}
    for ids in lineups["__ids"]:
        uniq = sorted(set(ids))
        for k in sizes:
            if len(uniq) >= k:
                counters[k].update(combinations(uniq, k))

    rows = []
    for k in sizes:
        for combo, c in counters[k].most_common(top_n):
            rows.append({
                "size": k,
                "combo": " + ".join(id_to_name.get(pid, pid) for pid in combo),
                "joint_exposure_pct": round(100.0 * c / n, 1),
                "lineups": c,
            })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(
        ["size", "joint_exposure_pct"], ascending=[True, False]).reset_index(drop=True)
