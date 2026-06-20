"""Slate analysis: auto-generated computations + persisted Claude synthesis.

The Slate Analysis tab has two layers:
1. Persisted markdown at data/slate_analysis/<slug>.md — Claude writes this when
   asked to "review the articles and write the slate analysis"
2. Auto-generated structured breakdown — recomputes from the active session on every load
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from src.vendors import mlb_team_key as _mlb_team_key


_ANALYSIS_DIR = Path(__file__).parent.parent / "data" / "slate_analysis"


def load_persisted(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None if no file exists."""
    p = _ANALYSIS_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def save_persisted(slug: str, markdown: str) -> None:
    """Write data/slate_analysis/<slug>.md. Called by Claude, not the UI."""
    _ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    (_ANALYSIS_DIR / f"{slug}.md").write_text(markdown)


def clear_persisted(slug: str) -> None:
    """Delete the file. Called after an autopsy log so the next slate starts fresh."""
    p = _ANALYSIS_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()


def snapshot(df: pd.DataFrame) -> dict:
    """Top-of-tab numbers: roster size, salary stats, chalk concentration, leverage count."""
    own = df["ownership"].fillna(0)
    top5_own_sum = own.nlargest(5).sum()
    return {
        "n_players": int(len(df)),
        "avg_salary": round(float(df["salary"].mean()), 0),
        "max_salary": int(df["salary"].max()),
        "min_salary": int(df["salary"].min()),
        "avg_proj": round(float(df["proj_points"].mean()), 2),
        "top5_own_concentration_pct": round(float(top5_own_sum), 1),
        "n_leverage_candidates": int((own < 5).sum()),
        "n_chalk": int((own >= 15).sum()),
    }


def top_chalk(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Players at >=15% own, ranked by ownership, with proj/$ and proj/own ratio."""
    chalk = df[df["ownership"].fillna(0) >= 15].copy()
    if chalk.empty:
        return chalk
    chalk["pt_per_$"] = (chalk["proj_points"] / chalk["salary"] * 1000).round(2)
    chalk["proj_per_own"] = (chalk["proj_points"] / chalk["ownership"]).round(3)
    cols = ["name", "salary", "proj_points", "ownership"]
    if "current_score" in chalk.columns:  # golf RD4 SD live leaderboard position
        cols.append("current_score")
    cols += ["pt_per_$", "proj_per_own"]
    return chalk.sort_values("ownership", ascending=False).head(n)[cols].reset_index(drop=True)


def sport_signals(df: pd.DataFrame, sport: str, team_data: pd.DataFrame | None = None) -> dict:
    """Sport-specific tables. Each value is either a DataFrame or None when data absent.

    team_data: optional team-level table (e.g. SIN MLB stack rankings) — only
    used by MLB.
    """
    if sport == "golf":
        return _golf_signals(df)
    if sport == "mma":
        return _mma_signals(df)
    if sport == "nascar":
        return _nascar_signals(df)
    if sport == "mlb":
        return _mlb_signals(df, team_data)
    return {}


def _golf_signals(df: pd.DataFrame) -> dict:
    out: dict = {}
    if "tee_time" in df.columns and df["tee_time"].notna().any():
        wave = df.groupby("tee_time").agg(
            n=("name", "count"),
            avg_proj=("proj_points", "mean"),
            avg_own=("ownership", "mean"),
        ).round(2).reset_index().sort_values("tee_time")
        out["tee_time_waves"] = wave
    if "make_cut_odds" in df.columns and df["make_cut_odds"].notna().any():
        bins = pd.cut(
            df["make_cut_odds"].fillna(0),
            bins=[-0.01, 0.40, 0.55, 0.70, 0.85, 1.01],
            labels=["Coffin (<40%)", "Risky (40–55%)", "Coin-flip (55–70%)", "Solid (70–85%)", "Lock (≥85%)"],
        )
        tier = df.assign(cut_tier=bins).groupby("cut_tier", observed=True).agg(
            n=("name", "count"),
            avg_proj=("proj_points", "mean"),
            avg_own=("ownership", "mean"),
        ).round(2).reset_index()
        out["make_cut_tiers"] = tier
    # RD4 Showdown live leaderboard position: who among the low-owned plays is
    # actually in contention vs. way back. A way-back dart can't post the round it
    # needs on a tough course — this table surfaces the trap (mirrors NASCAR pd).
    if "current_score" in df.columns and df["current_score"].notna().any():
        low = df[(df["ownership"].fillna(100) < 10) & df["current_score"].notna()].copy()
        if not low.empty:
            leader = df["current_score"].min()
            low["back"] = (low["current_score"] - leader).round(0)
            cols = ["name", "salary", "ownership", "current_score", "back"]
            if "ceiling" in low.columns:
                cols.append("ceiling")
            out["low_own_by_position"] = (
                low.sort_values("current_score").head(15)[cols].reset_index(drop=True)
            )
    return out


def _mma_signals(df: pd.DataFrame) -> dict:
    out: dict = {}
    if "win_prob" in df.columns and df["win_prob"].notna().any():
        card = df[["name", "salary", "win_prob", "proj_points", "ownership"]].copy()
        if "opponent" in df.columns:
            card.insert(1, "opponent", df["opponent"])
        if "proj_win" in df.columns and "proj_loss" in df.columns:
            card["win_loss_spread"] = (df["proj_win"] - df["proj_loss"]).round(1)
        card["role"] = card["win_prob"].apply(
            lambda p: "Big fav (≥65%)" if p >= 0.65 else ("Fav" if p >= 0.5 else ("Dog" if p >= 0.35 else "Big dog (<35%)"))
        )
        out["matchup_card"] = card.sort_values("win_prob", ascending=False).reset_index(drop=True)

        # Underdog leverage: low own + meaningful win equity
        dogs = df[(df["win_prob"] < 0.5) & (df["ownership"].fillna(0) < 10)].copy()
        if not dogs.empty:
            dogs = dogs[["name", "salary", "win_prob", "proj_points", "ownership"]].sort_values("win_prob", ascending=False)
            out["underdog_leverage"] = dogs.head(8).reset_index(drop=True)
    return out


def _nascar_signals(df: pd.DataFrame) -> dict:
    out: dict = {}
    if "dominator_points" in df.columns and df["dominator_points"].notna().any():
        dom = df[df["dominator_points"].fillna(0) > 0][
            ["name", "salary", "proj_points", "dominator_points", "ownership"]
        ].sort_values("dominator_points", ascending=False)
        out["dominator_pool"] = dom.head(12).reset_index(drop=True)
    if "starting_position" in df.columns and df["starting_position"].notna().any():
        # Position differential leverage: starting deep, projected well
        pd_df = df[df["starting_position"] >= 20].copy()
        if not pd_df.empty:
            pd_df["pd_score"] = (pd_df["proj_points"] / (pd_df["ownership"].fillna(0) + 1)).round(2)
            cols = ["name", "salary", "starting_position", "proj_points", "ownership", "pd_score"]
            out["pd_candidates"] = pd_df.sort_values("pd_score", ascending=False).head(10)[cols].reset_index(drop=True)
    return out


_PITCHER_POS = {"p", "sp", "rp"}

def _mlb_signals(df: pd.DataFrame, team_data: pd.DataFrame | None = None) -> dict:
    """Team stacks (the core MLB lever) + the pitcher pool."""
    out: dict = {}
    has_pos = "position" in df.columns and df["position"].notna().any()
    # fillna("") so a missing position cleans to "" rather than the literal
    # "nan"/"None" token before matching the pitcher set. (A row with no position
    # is genuinely unclassifiable and still falls to the hitter side either way.)
    pos_lower = df["position"].fillna("").astype(str).str.strip().str.lower() if has_pos else None

    # Team-stack table: hitters grouped by team (MLB analog to NASCAR's dom pool).
    if "team" in df.columns and df["team"].notna().any():
        hitters = df[~pos_lower.isin(_PITCHER_POS)] if pos_lower is not None else df
        stacks = hitters.groupby("team").agg(
            n=("name", "count"),
            stack_proj=("proj_points", "sum"),
            avg_own=("ownership", "mean"),
        ).round(2).reset_index()
        if "team_total" in df.columns and df["team_total"].notna().any():
            tt = df.groupby("team")["team_total"].max().reset_index()
            stacks = stacks.merge(tt, on="team", how="left").sort_values(
                ["team_total", "stack_proj"], ascending=False
            )
        else:
            stacks = stacks.sort_values("stack_proj", ascending=False)
        # Vendor stack rankings (e.g. SIN MLB stack file) beat our summed proxy.
        # Merge on normalized team keys — vendors mix abbreviations and nicknames.
        if team_data is not None and not team_data.empty and "team" in team_data.columns:
            vendor_cols = {
                "stack_proj": "vendor_stack_proj",
                "stack_own": "vendor_stack_own",
                "stack_salary": "vendor_stack_salary",
            }
            keep = ["team"] + [c for c in vendor_cols if c in team_data.columns]
            td = team_data[keep].rename(columns=vendor_cols).copy()
            td["_team_key"] = td["team"].apply(_mlb_team_key)
            td = td.drop(columns="team")
            stacks["_team_key"] = stacks["team"].apply(_mlb_team_key)
            stacks = stacks.merge(td, on="_team_key", how="left").drop(columns="_team_key")
            if "vendor_stack_proj" in stacks.columns:
                stacks = stacks.sort_values("vendor_stack_proj", ascending=False)
        out["team_stacks"] = stacks.reset_index(drop=True)

    # Pitcher pool.
    if pos_lower is not None:
        pitchers = df[pos_lower.isin(_PITCHER_POS)]
        if not pitchers.empty:
            cols = [c for c in ["name", "team", "opponent", "salary", "proj_points", "ownership"]
                    if c in pitchers.columns]
            out["pitchers"] = pitchers.sort_values("proj_points", ascending=False)[cols].reset_index(drop=True)
    return out
