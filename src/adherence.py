"""Strategy adherence — did you follow YOUR OWN strategy?

The accuracy layer grades whether the slate's edges were CORRECT. This grades
something different: whether the lineups you actually entered honored the calls
your own strategy made (`data/strategy_contract/<slug>.json` — the machine-readable
sidecar of the `## Leverage & fades` section). A strategy that said FADE X while
you rostered X in 4 of 5 bullets is a discipline leak no amount of better analysis
fixes — and until now nothing measured it.

Graded at autopsy-log time from the contract + the entered lineups already in the
autopsy records; archived to <history_dir>/adherence.json; the per-slate summary
lands in results.jsonl (`adherence_fades_violated`, `adherence_leverage_covered`)
so `history.process_trend_block` can trend it into future bundles.

Verdict semantics (matching the contract):
  fade        -> ANY exposure is a violation (the strategy said zero).
  lean_fade / underweight -> exposure above _SOFT_MAX_EXPOSURE is a violation
                 (the strategy said under-own, not zero).
  play        -> informational only: 0% exposure is flagged `ignored`, never a
                 violation (the user decides; passing on a play is legitimate).
  pass / pass_mix -> like fade but soft: exposure flagged, counted as soft.
Leverage candidates: covered if ANY entered lineup rostered them (the sharp
playbook wants ≥1 sub-5% piece somewhere, not everywhere).

Pure + deterministic; never blocks the autopsy log.
"""
from __future__ import annotations

from src.autopsy import _norm_name

# A lean_fade/underweight call is honored as long as exposure stays at or below
# this share of the user's lineups (under-owning, not zeroing).
_SOFT_MAX_EXPOSURE = 0.5

_HARD_VERDICTS = {"fade"}
_SOFT_VERDICTS = {"lean_fade", "underweight", "pass", "pass_mix"}


def _user_lineups(records) -> list[set[str]]:
    """Normalized rosters of every entered lineup across the slate's contests,
    deduped by roster (the same bullet entered in two contests is one decision)."""
    seen: set[frozenset] = set()
    out: list[set[str]] = []
    for r in (records or []):
        for ln in r.get("user_lineups") or []:
            roster = frozenset(_norm_name(p) for p in (ln.get("players") or []) if p)
            if roster and roster not in seen:
                seen.add(roster)
                out.append(set(roster))
    return out


def grade_adherence(contract: dict | None, records) -> dict:
    """Grade the entered lineups against the strategy contract's calls.

    Returns {gradable: False} when there's no contract or no entered lineups —
    a slate without a generated strategy has nothing to adhere to."""
    calls = (contract or {}).get("calls") or []
    leverage = (contract or {}).get("leverage_candidates") or []
    lineups = _user_lineups(records)
    if not lineups or (not calls and not leverage):
        return {"gradable": False, "n_lineups": len(lineups)}

    n = len(lineups)
    graded = []
    fades_violated = 0
    soft_violated = 0
    for c in calls:
        key = _norm_name(c.get("name", ""))
        if not key:
            continue
        hits = sum(1 for lu in lineups if key in lu)
        exposure = hits / n
        verdict = c.get("verdict")
        row = {"name": c.get("name"), "verdict": verdict,
               "exposure_pct": round(exposure * 100, 1), "in_lineups": hits, "of": n}
        if verdict in _HARD_VERDICTS:
            row["followed"] = hits == 0
            if hits:
                fades_violated += 1
        elif verdict in _SOFT_VERDICTS:
            row["followed"] = exposure <= _SOFT_MAX_EXPOSURE
            if not row["followed"]:
                soft_violated += 1
        else:  # play — informational, never a violation
            row["followed"] = None
            row["ignored"] = hits == 0
        graded.append(row)

    lev_rows = []
    covered = 0
    for cand in leverage:
        key = _norm_name(cand.get("name", ""))
        if not key:
            continue
        hit = any(key in lu for lu in lineups)
        covered += bool(hit)
        lev_rows.append({"name": cand.get("name"), "rostered": hit})

    return {
        "gradable": True,
        "n_lineups": n,
        "calls": graded,
        "fades_violated": fades_violated,
        "soft_violated": soft_violated,
        "leverage_candidates": lev_rows,
        "leverage_covered": covered,
        "leverage_of": len(lev_rows),
    }


def adherence_md(a: dict) -> str:
    """Compact markdown block for the Autopsy tab / autopsies.md."""
    if not a or not a.get("gradable"):
        return ("### Strategy adherence\n"
                "- *Not gradable — no strategy contract or no entered lineups this slate.*")
    out = [f"### Strategy adherence — did you follow your own strategy? "
           f"({a['n_lineups']} unique lineups)"]
    if a.get("fades_violated"):
        bad = [c for c in a["calls"] if c["verdict"] == "fade" and not c["followed"]]
        out.append(f"- ⚠️ **{a['fades_violated']} FADE call(s) violated:** " +
                   ", ".join(f"**{c['name']}** (in {c['in_lineups']} of {c['of']})"
                             for c in bad))
    else:
        out.append("- ✅ Every hard FADE honored.")
    if a.get("soft_violated"):
        soft = [c for c in a["calls"] if c["verdict"] in _SOFT_VERDICTS and not c["followed"]]
        out.append(f"- ⚠️ {a['soft_violated']} under-own call(s) over-exposed: " +
                   ", ".join(f"**{c['name']}** ({c['exposure_pct']}%)" for c in soft))
    if a.get("leverage_of"):
        out.append(f"- Leverage candidates rostered somewhere: "
                   f"**{a['leverage_covered']} of {a['leverage_of']}**.")
    ignored = [c for c in a["calls"] if c.get("ignored")]
    if ignored:
        out.append("- Plays named but never rostered (your call, just visibility): " +
                   ", ".join(c["name"] for c in ignored))
    return "\n".join(out)
