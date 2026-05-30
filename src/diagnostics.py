"""
Pre-slate diagnostics.

Given a projections DataFrame and the contest's rules dict, surface:
- Player tier classification (chalk / leverage / punt / etc.)
- Chalk concentration metric (sum of top-N ownership)
- Leverage spine candidates, structural floor candidates, coffin candidates
- Warnings (e.g. "no sub-5% leverage candidate exists")

This frames the build before lineups are generated. Auto-recomputed when projections change.
"""
from __future__ import annotations

import pandas as pd


def tag_players_by_tier(projections: pd.DataFrame, rules: dict) -> pd.DataFrame:
    """Return a copy of projections with a 'tier' column based on ownership tiers in rules."""
    df = projections.copy()
    tiers = rules.get("ownership_tiers") or _default_tiers()

    def _classify(own: float) -> str:
        for name, bounds in tiers.items():
            min_own = bounds.get("min_own", 0)
            max_own = bounds.get("max_own", 100)
            if min_own <= own <= max_own:
                return name
        return "unclassified"

    df["tier"] = df["ownership"].apply(_classify)
    return df


def _default_tiers() -> dict:
    """Generic ownership tiers used when rules don't specify them."""
    return {
        "chalk":          {"min_own": 25, "max_own": 100},
        "mid_chalk":      {"min_own": 12, "max_own": 24.99},
        "leverage":       {"min_own": 5,  "max_own": 11.99},
        "deep_contrarian": {"min_own": 0, "max_own": 4.99},
    }


def slate_diagnostics(projections: pd.DataFrame, rules: dict) -> dict:
    """Return a structured pre-slate report."""
    if projections is None or projections.empty:
        return {"tier_counts": {}, "warnings": ["No projections loaded."]}

    tagged = tag_players_by_tier(projections, rules)
    tier_counts = tagged["tier"].value_counts().to_dict()

    # Chalk concentration: sum of ownership of top-6 owned players (one lineup's worth)
    top_n = min(6, len(tagged))
    top_owned = tagged.nlargest(top_n, "ownership")
    chalk_concentration = float(top_owned["ownership"].sum())

    # Leverage spine candidates: sub-15% ownership, mid-salary range ($6,500-$7,999)
    leverage_spine = tagged[
        (tagged["ownership"] < 15)
        & (tagged["salary"] >= 6500)
        & (tagged["salary"] <= 7999)
    ].sort_values("proj_points", ascending=False).head(10)

    # Structural floor candidates: high projection + high stddev = high ceiling
    tagged_with_ceiling = tagged.copy()
    tagged_with_ceiling["est_ceiling"] = (
        tagged_with_ceiling["proj_points"] + 1.28 * tagged_with_ceiling["stddev"]
    )
    structural_floor = tagged_with_ceiling[
        tagged_with_ceiling["est_ceiling"] >= 60
    ].sort_values("est_ceiling", ascending=False).head(10)

    # Coffin candidates: high ownership (>=20%) and mediocre value
    coffin_candidates = tagged[tagged["ownership"] >= 20].sort_values(
        "ownership", ascending=False
    ).head(10)

    # Deep contrarian (sub-5%)
    deep_contrarian = tagged[tagged["ownership"] < 5].sort_values(
        "proj_points", ascending=False
    ).head(10)

    warnings: list[str] = []
    if chalk_concentration > 180:
        warnings.append(
            f"Heavy chalk concentration: top {top_n} owned players sum to {chalk_concentration:.0f}% ownership."
        )
    if leverage_spine.empty:
        warnings.append("No Leverage Plays available (sub-15% own, $6.5K-$8K salary).")
    if structural_floor.empty:
        warnings.append("No Structural Plays with estimated 60+ ceiling.")
    if (tagged["ownership"] < 5).sum() == 0:
        warnings.append("No Contrarian Plays available (sub-5% own).")
    if (tagged["ownership"] >= 30).sum() >= 4:
        warnings.append(
            f"{(tagged['ownership'] >= 30).sum()} players projected at 30%+ ownership — chalk-heavy slate."
        )

    return {
        "tier_counts": tier_counts,
        "chalk_concentration_pct": round(chalk_concentration, 1),
        "leverage_spine_candidates": leverage_spine[["name", "salary", "proj_points", "ownership"]],
        "structural_floor_candidates": structural_floor[["name", "salary", "proj_points", "est_ceiling", "ownership"]],
        "coffin_candidates": coffin_candidates[["name", "salary", "proj_points", "ownership"]],
        "deep_contrarian": deep_contrarian[["name", "salary", "proj_points", "ownership"]],
        "warnings": warnings,
    }
