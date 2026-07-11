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
        # MMA carries a real ceiling (proj_win = points if they win) + win prob,
        # and its opponent lives in `matchup` (not `opponent`). Surface them so the
        # fighter ranking can show ceiling / win% and use proj_win as the ceiling.
        pwin = (pd.to_numeric(g.get("proj_win"), errors="coerce").dropna()
                if "proj_win" in g.columns else pd.Series(dtype=float))
        wprob = (pd.to_numeric(g.get("win_prob"), errors="coerce").dropna()
                 if "win_prob" in g.columns else pd.Series(dtype=float))
        opp = ""
        for _oc in ("opponent", "matchup"):
            if _oc in g.columns:
                opp = next((str(v) for v in g[_oc] if isinstance(v, str) and v.strip()), "")
                if opp:
                    break
        ceil_val = round(float(ceil.mean()), 1) if not ceil.empty else (
            round(float(pwin.mean()), 1) if not pwin.empty else None)
        rows.append({
            "name": g["name"].iloc[0],
            "salary": int(sal.max()) if not sal.empty else None,
            "ownership": round(float(own.mean()), 1) if not own.empty else None,
            "proj_points": round(float(proj.mean()), 1) if not proj.empty else None,
            "ceiling": ceil_val,
            "win_prob": round(float(wprob.mean()), 3) if not wprob.empty else None,
            "opponent": opp,
            "vendors": int(g["__vendor"].nunique()),
        })

    pool = pd.DataFrame(rows)
    if "opponent" in pool.columns and not pool["opponent"].str.strip().any():
        pool = pool.drop(columns=["opponent"])
    if "win_prob" in pool.columns and pool["win_prob"].isna().all():
        pool = pool.drop(columns=["win_prob"])   # non-MMA: no win prob
    return pool.sort_values("salary", ascending=False, na_position="last").reset_index(drop=True)


def _leading_name(raw: str) -> str:
    """Pull the subject player name from a bolded fade bullet, dropping price/own
    parentheticals and relative-fade tails ('Donchenko at $9,400 vs Yakhyaev' ->
    'Donchenko', so the alternative isn't swept in)."""
    s = raw.strip()
    s = re.split(r"\s+(?:at|vs|over|on)\s+|\s*[\(\$]|,|\d", s)[0]
    return s.strip(" :—-").strip()


# Verdict tokens for per-player calls in the Leverage & fades section. Order
# matters: longer/more-specific first so "LEAN FADE" isn't read as "FADE" and
# "PASS/MIX" isn't read as "PASS".
_VERDICT_TOKENS = [
    ("LEAN FADE", "lean_fade"),
    ("UNDERWEIGHT", "underweight"),
    ("PASS/MIX", "pass_mix"),
    ("FADE", "fade"),
    ("PASS", "pass"),
    ("PLAY", "play"),
]


def _verdict_for(bold_text: str, after_bold: str, line: str) -> str | None:
    """The call's verdict, read where the convention puts it: inside the bolded
    lead ('**Keith Mitchell $10,000 — FADE.**'), else the first clause after the
    bold ('— PASS/MIX.'), else anywhere in the line (last resort)."""
    for scope in (bold_text, after_bold.split(".")[0], line):
        u = scope.upper()
        for token, verdict in _VERDICT_TOKENS:
            if token in u:
                return verdict
    return None


def parse_calls(strategy_md: str) -> list[dict]:
    """Per-player calls from the '## Leverage & fades' section: one
    {name, verdict} per bolded bullet line with a recognizable verdict."""
    if not strategy_md:
        return []
    sec = re.search(r"##\s*Leverage\s*&\s*fades(.*?)(?:\n##\s|\Z)", strategy_md, re.S | re.I)
    if not sec:
        return []
    calls = []
    for line in sec.group(1).splitlines():
        m = re.search(r"\*\*(.+?)\*\*", line)
        if not m:
            continue
        name = _leading_name(m.group(1))
        if not name:
            continue
        verdict = _verdict_for(m.group(1), line[m.end():], line)
        if verdict:
            calls.append({"name": name, "verdict": verdict})
    return calls


def extract_fades(strategy_md: str) -> list[str]:
    """Names the strategy actually ZEROES, from '## Leverage & fades'.

    Verdict-aware: a bolded bullet is a fade only when its line carries a hard
    FADE verdict — PLAY / PASS / PASS-MIX / UNDERWEIGHT / LEAN FADE calls are
    NOT fades (under-own ≠ zero). Legacy format is still honored: under a
    literal '**Fades**' subheading, plain bolded names WITHOUT any verdict
    token count as fades (that subsection is unambiguous).

    Previously this swept EVERY bolded name in the section when the strategy
    used a heading like 'Additional fades / underweights' instead of a literal
    '**Fades**' — which marked the strategy's own PLAY calls as fades and
    silently dropped them from the player pool (caught on the 7/2/26 John
    Deere strategy: 6 PLAY calls + a 'Do NOT zero' underweight were swept).
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
    for line in block.splitlines():
        m = re.search(r"\*\*(.+?)\*\*", line)
        if not m:
            continue
        cand = _leading_name(m.group(1))
        if not cand:
            continue
        verdict = _verdict_for(m.group(1), line[m.end():], line)
        if verdict == "fade" or (verdict is None and head is not None):
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
