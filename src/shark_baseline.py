"""One-time backfill: mine the user's historical contest-standings into a real
per-sport behavioral baseline (us vs the sharks), so the shark-gap stops reading
"last 1 slate."

The user has dozens of past DK contest-standings in ~/Downloads. Each carries the
whole field (the sharks' lineups + ours), so `src.shark_gap` runs on them
directly. This aggregates the structural fingerprint per sport into
`rules/shared/shark_baseline.json` — the reference the bundle and the
envelope-enforcement read.
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

from src.autopsy import parse_dk_results
from src import shark_gap

_REPO_ROOT = Path(__file__).parent.parent
_BASELINE_PATH = _REPO_ROOT / "rules" / "shared" / "shark_baseline.json"
_DEFAULT_GLOB = str(Path.home() / "Downloads" / "contest-standings-*.csv")

# Map the classified sport to the shark watchlist key in shark_handles.yaml.
_SPORT_TO_SHARKS = {"golf": "golf", "nascar": "nascar", "mlb": "nfl", "showdown": "mma"}
# flat-6 split: NASCAR fields ~40 drivers, golf ~70+ golfers.
_NASCAR_MAX_UNIQUE = 50


def classify_sport(parsed: dict) -> str:
    """golf | nascar | mlb | showdown from the standings' roster positions."""
    pos = {str(x).strip().upper() for x in parsed["players"]["roster_position"].dropna()}
    if "CPT" in pos or "CAPTAIN" in pos:
        return "showdown"
    if {"1B", "SS", "OF", "C"} & pos:
        return "mlb"
    # flat-6: distinguish golf vs nascar by the field's unique-player count.
    return "nascar" if len(parsed["players"]) <= _NASCAR_MAX_UNIQUE else "golf"


def _dedupe_by_id(files: list[str]) -> dict[str, str]:
    by_id: dict[str, str] = {}
    for f in sorted(files):
        m = re.search(r"contest-standings-(\d+)", f)
        if m:
            by_id.setdefault(m.group(1), f)  # first (no-suffix sorts first) wins
    return by_id


def _mean(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def backfill(pattern: str = _DEFAULT_GLOB) -> dict:
    """Compute the per-sport baseline from every unique historical contest."""
    cfg = shark_gap.load_handles()
    user = cfg.get("user", [])
    sharks_by = cfg.get("sharks_by_sport", {})

    by_id = _dedupe_by_id(glob.glob(pattern))
    per_sport: dict[str, dict] = {}
    contests: list[dict] = []

    for cid, f in by_id.items():
        try:
            parsed = parse_dk_results(f)
        except Exception as e:  # noqa: BLE001 — skip unreadable, keep going
            contests.append({"id": cid, "error": str(e)})
            continue
        sport = classify_sport(parsed)
        sharks = sharks_by.get(_SPORT_TO_SHARKS.get(sport, ""), [])
        u = shark_gap.structural_profile(parsed, user)
        if not u.get("gradable"):
            continue
        g = shark_gap.shark_gap(parsed, sharks, user)
        bucket = per_sport.setdefault(sport, {"user": [], "shark": [], "n": 0, "n_sharks": 0})
        bucket["user"].append(u)
        bucket["n"] += 1
        if g.get("sharks_in_field"):
            bucket["shark"].append(g["sharks"])
            bucket["n_sharks"] += 1
        contests.append({"id": cid, "sport": sport, "n_field": len(parsed["lineups"]),
                         "n_players": len(parsed["players"]),
                         "sharks_in_field": g.get("sharks_in_field", False)})

    dims = ["own_per_slot", "leverage_pct", "anchor_exposure", "unique_pct"]
    out = {"generated_from": pattern, "n_contests": len(by_id), "sports": {}}
    for sport, b in per_sport.items():
        user_env = {d: _mean([p.get(d) for p in b["user"]]) for d in dims}
        shark_env = ({d: _mean([p.get(d) for p in b["shark"]]) for d in dims}
                     if b["shark"] else None)
        mean_gap = ({d: (round(user_env[d] - shark_env[d], 2)
                         if user_env[d] is not None and shark_env[d] is not None else None)
                     for d in dims} if shark_env else None)
        out["sports"][sport] = {
            "n_contests": b["n"], "n_with_sharks": b["n_sharks"],
            "user_envelope": user_env, "shark_envelope": shark_env, "mean_gap": mean_gap,
        }
    out["contests"] = contests
    return out


def write_baseline(baseline: dict) -> Path:
    _BASELINE_PATH.write_text(json.dumps(baseline, indent=2))
    return _BASELINE_PATH


def load_baseline() -> dict:
    if not _BASELINE_PATH.exists():
        return {}
    try:
        return json.loads(_BASELINE_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def report_md(baseline: dict) -> str:
    lines = [f"# Shark baseline — {baseline.get('n_contests', 0)} historical contests", ""]
    for sport, s in sorted(baseline.get("sports", {}).items()):
        lines.append(f"## {sport} ({s['n_contests']} contests, {s['n_with_sharks']} with tracked sharks)")
        u, sh, g = s["user_envelope"], s["shark_envelope"], s["mean_gap"]
        lines.append(f"- own%/slot — you {u['own_per_slot']} · sharks {sh['own_per_slot'] if sh else '—'}"
                     f" · Δ {g['own_per_slot'] if g else '—'}")
        lines.append(f"- % lineups w/ sub-5% piece — you {u['leverage_pct']} · "
                     f"sharks {sh['leverage_pct'] if sh else '—'} · Δ {g['leverage_pct'] if g else '—'}")
        lines.append(f"- chalk-anchor exposure — you {u['anchor_exposure']} · "
                     f"sharks {sh['anchor_exposure'] if sh else '—'} · Δ {g['anchor_exposure'] if g else '—'}")
        lines.append(f"- % unique rosters — you {u['unique_pct']} · sharks {sh['unique_pct'] if sh else '—'}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    b = backfill()
    write_baseline(b)
    print(report_md(b))
