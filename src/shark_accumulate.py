"""Living shark envelope — accumulate observed shark structure over time.

`shark_baseline.json` started as a one-time 63-contest backfill. This turns it
into a LIVING dataset: every autopsy where tracked sharks are in-field appends
their observed `structural_profile` (from `shark_gap.structural_profile`) to
`rules/shared/shark_observations.jsonl`, and `refresh_baseline()` recomputes each
sport's `shark_envelope` as a count-weighted blend of the frozen backfill SEED +
all accumulated observations.

The seed is frozen on first refresh (`seed_envelope` / `seed_weight`) so the blend
is idempotent and always re-derivable from (seed + observations) — a re-run never
double-counts. The Sim tool reads the refreshed envelope via
`analyzer_link.load_shark_envelope`, so accumulated shark reality flows straight
into the builder/diversifier.

Feeds the "play like a shark" goal: match STRUCTURE (own/slot, leverage rate,
anchor concentration, uniqueness), not clone player exposures.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.contests import FOCUS_CONTEST_TYPES

_SHARED = Path(__file__).parent.parent / "rules" / "shared"
_OBS_PATH = _SHARED / "shark_observations.jsonl"
_BASELINE_PATH = _SHARED / "shark_baseline.json"

FEATURES = ("own_per_slot", "leverage_pct", "anchor_exposure", "unique_pct")


def _in_focus(contest_type: str | None) -> bool:
    """Only SE/3-Max/5-Max feed the envelope — the Analyzer benchmarks against
    sharks' SMALL-FIELD play, never their 150-max MME dumps (a different game)."""
    return contest_type in FOCUS_CONTEST_TYPES


def record_observation(sport: str | None, shark_profile: dict, slug: str, date: str,
                       contest_type: str | None = None,
                       contest_id: str | None = None) -> bool:
    """Append one contest's in-field SHARK structural profile. Returns True if
    recorded. Skips when sport is unknown, sharks weren't gradable, any of the 4
    envelope features is missing (an incomplete row would bias the blend), or the
    contest is NOT an in-focus SE/3-Max/5-Max small-field GPP.

    Rows carry `contest_id` so a re-logged contest can never double-weight the
    envelope: `refresh_baseline` keeps only the LATEST row per id. The envelope
    calibrates the grader's chalk threshold and the bundle's `## Shark reality`
    target, so a silent double-count here corrupts money-adjacent numbers."""
    if not sport or not shark_profile or not shark_profile.get("gradable"):
        return False
    if not _in_focus(contest_type):
        return False
    row = {f: shark_profile.get(f) for f in FEATURES}
    if any(row[f] is None for f in FEATURES):
        return False
    row.update({"date": date, "slug": slug, "sport": sport,
                "contest_type": contest_type,
                "contest_id": str(contest_id) if contest_id else None,
                "n_entries": shark_profile.get("n_entries")})
    _OBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _OBS_PATH.open("a") as f:
        f.write(json.dumps(row) + "\n")
    return True


def _load_observations() -> list[dict]:
    """All observation rows, deduped by contest_id (latest row wins) — the
    read-time guard matching field_tendencies/shark_dossier, so an append that
    slipped past write-time dedup can't permanently double-weight the blend.
    Legacy rows without a contest_id pass through untouched."""
    if not _OBS_PATH.exists():
        return []
    out: list[dict] = []
    by_id: dict[str, int] = {}  # contest_id -> index in out (latest replaces)
    for line in _OBS_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        cid = row.get("contest_id")
        if cid and cid in by_id:
            out[by_id[cid]] = row
        else:
            if cid:
                by_id[cid] = len(out)
            out.append(row)
    return out


def refresh_baseline() -> dict:
    """Recompute each sport's `shark_envelope` = count-weighted blend of the frozen
    backfill seed + accumulated observations. Idempotent. Returns the new baseline."""
    if not _BASELINE_PATH.exists():
        return {}
    base = json.loads(_BASELINE_PATH.read_text())
    sports = base.get("sports", {})
    # Only SE/3-Max/5-Max observations feed the blend. Legacy rows written before
    # contest_type was tagged are excluded (contest_type absent → not in focus),
    # so an old 20-max MME row can never pollute the small-field envelope.
    obs = [o for o in _load_observations() if _in_focus(o.get("contest_type"))]
    by_sport: dict[str, list[dict]] = {}
    for o in obs:
        by_sport.setdefault(o.get("sport"), []).append(o)

    for sport, block in sports.items():
        # Freeze the original backfill as the immutable seed on first pass.
        if "seed_envelope" not in block:
            block["seed_envelope"] = dict(block.get("shark_envelope", {}))
            block["seed_weight"] = int(block.get("n_with_sharks")
                                       or block.get("n_contests") or 10)
        seed = block["seed_envelope"]
        sw = float(block["seed_weight"])
        rows = by_sport.get(sport, [])
        blended = {}
        for f in FEATURES:
            if seed.get(f) is None:
                continue
            num = seed[f] * sw + sum(r[f] for r in rows)
            blended[f] = round(num / (sw + len(rows)), 3)
        block["shark_envelope"] = {**block.get("shark_envelope", {}), **blended}
        block["accumulated_contests"] = len(rows)

    _BASELINE_PATH.write_text(json.dumps(base, indent=2))
    return base
