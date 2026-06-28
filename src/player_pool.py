"""Player pool: the rosterable universe from the loaded vendor projections, with
the fades named in the slate strategy removed.

Lives in the Slate Strategy tab. The fighter/player universe + salary/own/proj
come from the uploaded vendor projections; the fades are read straight out of the
generated slate strategy's "## Leverage & fades" -> Fades subsection (the strategy
being the app's distillation of the uploaded documents + projections). This is a
display helper for the pool membership; the ranking/write-ups are Claude-generated.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.sessions import merge_same_vendor

_POOL_DIR = Path(__file__).parent.parent / "data" / "player_pool"


def load_pool(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} for the generated pool, or None."""
    p = _POOL_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def save_pool(slug: str, markdown: str) -> None:
    """Write data/player_pool/<slug>.md. Called by Claude, not the UI."""
    _POOL_DIR.mkdir(parents=True, exist_ok=True)
    (_POOL_DIR / f"{slug}.md").write_text(markdown)


def clear_pool(slug: str) -> None:
    """Delete the generated pool. Called when the slate is cleared/logged."""
    p = _POOL_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()


def build_pool(sources: dict[str, dict]) -> pd.DataFrame:
    """Union every player across the loaded vendor sources into one row each.

    Same-vendor multi-file uploads are collapsed first (merge_same_vendor); then
    we union across vendors, deduping by normalized name. Ownership/projection are
    averaged across the vendors that report them; salary is the consensus (max).
    """
    merged = merge_same_vendor(sources)
    frames = []
    for _name, blob in merged.items():
        df = blob.get("df")
        if df is None or df.empty:
            continue
        df = df.copy()
        df["__vendor"] = blob.get("vendor")
        frames.append(df)
    if not frames:
        return pd.DataFrame()

    allp = pd.concat(frames, ignore_index=True)
    allp["__key"] = allp["name"].astype(str).str.strip().str.lower()

    rows = []
    for _key, g in allp.groupby("__key", sort=False):
        sal = pd.to_numeric(g.get("salary"), errors="coerce").dropna()
        own = pd.to_numeric(g.get("ownership"), errors="coerce").dropna()
        proj = pd.to_numeric(g.get("proj_points"), errors="coerce").dropna()
        ceil = (pd.to_numeric(g.get("ceiling"), errors="coerce").dropna()
                if "ceiling" in g.columns else pd.Series(dtype=float))
        opp = ""
        if "opponent" in g.columns:
            opp = next((str(v) for v in g["opponent"] if isinstance(v, str) and v.strip()), "")
        rows.append({
            "name": g["name"].iloc[0],
            "salary": int(sal.max()) if not sal.empty else None,
            "ownership": round(float(own.mean()), 1) if not own.empty else None,
            "proj_points": round(float(proj.mean()), 1) if not proj.empty else None,
            "ceiling": round(float(ceil.mean()), 1) if not ceil.empty else None,
            "opponent": opp,
            "vendors": int(g["__vendor"].nunique()),
        })

    pool = pd.DataFrame(rows)
    if "opponent" in pool.columns and not pool["opponent"].str.strip().any():
        pool = pool.drop(columns=["opponent"])
    return pool.sort_values("salary", ascending=False, na_position="last").reset_index(drop=True)


def _leading_name(raw: str) -> str:
    """Pull the subject player name from a bolded fade bullet, dropping price/own
    parentheticals and relative-fade tails ('Donchenko at $9,400 vs Yakhyaev' ->
    'Donchenko', so the alternative isn't swept in)."""
    s = raw.strip()
    s = re.split(r"\s+(?:at|vs|over|on)\s+|\s*[\(\$]|,|\d", s)[0]
    return s.strip(" :—-").strip()


def extract_fades(strategy_md: str) -> list[str]:
    """Names from the strategy's '## Leverage & fades' -> Fades subsection.

    Returns the leading subject name of each bolded fade bullet (e.g.
    'Shara Magomedov', 'Donchenko', 'Ruziboev'). Non-name directives like 'PASS'
    fall through harmlessly — they won't match any player in apply_fades.
    """
    if not strategy_md:
        return []
    sec = re.search(r"##\s*Leverage\s*&\s*fades(.*?)(?:\n##\s|\Z)", strategy_md, re.S | re.I)
    if not sec:
        return []
    section = sec.group(1)
    head = re.search(r"\*\*Fades[^*]*\*\*", section, re.I)
    block = section[head.end():] if head else section
    names = []
    for raw in re.findall(r"\*\*(.+?)\*\*", block):
        cand = _leading_name(raw)
        if cand:
            names.append(cand)
    return names


def apply_fades(pool_df: pd.DataFrame, fade_names: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """Split the pool into (kept, removed) by matching each fade name against
    player names (case-insensitive substring, so last-name-only fades resolve).
    Returns (kept_df, sorted removed player names)."""
    if pool_df.empty or not fade_names:
        return pool_df.reset_index(drop=True), []
    names_lower = pool_df["name"].astype(str).str.lower()
    drop_idx, removed = set(), []
    for fade in fade_names:
        f = fade.strip().lower()
        if len(f) < 4:
            continue
        hits = pool_df[names_lower.str.contains(re.escape(f), na=False)]
        for idx, r in hits.iterrows():
            drop_idx.add(idx)
            removed.append(r["name"])
    kept = pool_df.drop(index=list(drop_idx)).reset_index(drop=True)
    return kept, sorted(set(removed))
