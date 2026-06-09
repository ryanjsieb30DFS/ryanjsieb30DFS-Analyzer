"""Bundle for Claude.

`build_bundle` consolidates every input for the active slate into a single
markdown file at data/bundle/<slug>.md so Claude can read one file to find
everything: contest config, the projections read (chalk/leverage/anchor),
cross-vendor disagreement, sport signals, the on-disk slate-data files, the sim
summary, and absolute paths to the philosophy/framework/autopsies docs.

The bundle POINTS TO the strategy docs and slate-data files (paths) rather than
inlining them — Claude reads those with the Read tool. The output target for
the synthesis is data/slate_analysis/<slug>.md.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from src import sessions
from src.contests import load_contests, portfolio_summary
from src.landscape import leverage_table, anchor_equivalence_check
from src.projections_diff import flagged_disagreements
from src.slate_analysis import snapshot, top_chalk, sport_signals
from src.sim_data import load_sim_summary
from src.strategy import load_strategy

_REPO_ROOT = Path(__file__).parent.parent
_BUNDLE_DIR = _REPO_ROOT / "data" / "bundle"


def _path(slug: str) -> Path:
    return _BUNDLE_DIR / f"{slug}.md"


def _md_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a GitHub-flavored markdown table (no tabulate dep)."""
    if df is None or df.empty:
        return "_(none)_"
    cols = [str(c) for c in df.columns]
    head = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows = []
    for _, r in df.iterrows():
        rows.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in r.tolist()) + " |")
    return "\n".join([head, sep, *rows])


def build_bundle(slug: str, contest_label: str, sport: str) -> Path:
    """Write data/bundle/<slug>.md consolidating all inputs. Returns the path."""
    _BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    L: list[str] = [
        f"# Slate bundle — {contest_label}",
        f"_Generated {ts} · slug `{slug}` · sport `{sport}`_",
        "",
        "This file consolidates everything for the active slate. Read it, then "
        "read the files it points to, then write the slate analysis to "
        f"`data/slate_analysis/{slug}.md`.",
    ]

    # --- Contest config --- #
    L += ["", "## Contests"]
    contests = load_contests(slug)
    if contests:
        summ = portfolio_summary(slug)
        L.append(
            f"- {summ['n_contests']} contest(s), {summ['total_entries']} total entries, "
            f"**{summ['unique_lineups_needed']} unique lineups needed**"
        )
        for c in contests:
            L.append(
                f"  - **{c['name']}** ({c['type']}): field {c.get('field_size', '?'):,}, "
                f"my entries {c.get('my_entries', '?')}/{c.get('max_entries', '?')}"
            )
    else:
        L.append("_No contests declared. Default to 2 lineups if asked to build._")

    # --- Projections --- #
    L += ["", "## Projections"]
    sources = sessions.merge_same_vendor(sessions.load_sources(slug))
    if not sources:
        L.append("_No projections uploaded._")
    else:
        primary_name = list(sources.keys())[0]
        df = sources[primary_name]["df"]
        L.append(f"Primary source: **{primary_name}** ({sources[primary_name]['vendor']})")
        L.append(f"All sources: {', '.join(sources.keys())}")

        snap = snapshot(df)
        L += [
            "",
            f"- Players: {snap['n_players']} · avg salary ${snap['avg_salary']:,.0f} "
            f"(${snap['min_salary']:,}–${snap['max_salary']:,}) · avg proj {snap['avg_proj']}",
            f"- Top-5 ownership concentration: {snap['top5_own_concentration_pct']}% · "
            f"chalk (≥15%): {snap['n_chalk']} · leverage pool (<5% own): {snap['n_leverage_candidates']}",
        ]

        L += ["", "### Top chalk", _md_table(top_chalk(df))]
        L += ["", "### Top leverage", _md_table(leverage_table(df))]

        L += ["", "### Anchor-equivalence findings"]
        groups = anchor_equivalence_check(df)
        if not groups:
            L.append("_No anchor-equivalence pairs at similar ownership._")
        else:
            for g in groups:
                L.append(
                    f"- **{', '.join(g['players'])}** (own% {g['own_range'][0]:.1f}–{g['own_range'][1]:.1f}) — {g['rule']}"
                )

        # Sport signals
        signals = sport_signals(df, sport, team_data=sessions.load_team_data(slug))
        if signals:
            L += ["", f"### {sport.upper()} signals"]
            for key, table in signals.items():
                L += ["", f"**{key.replace('_', ' ').title()}**", _md_table(table)]

        # Cross-vendor disagreement
        L += ["", "### Cross-vendor disagreement (proj_points, ≥15%)"]
        if len(sources) >= 2:
            flagged = flagged_disagreements(sources, metric="proj_points", pct_threshold=15.0)
            L.append(_md_table(flagged.head(10)) if not flagged.empty else "_Vendors broadly agree._")
        else:
            L.append("_Only one source — no disagreement to compute._")

    # --- Slate data files --- #
    L += ["", "## Slate data files (read these)"]
    articles_dir = _REPO_ROOT / "articles" / slug
    files = sorted(articles_dir.glob("*")) if articles_dir.exists() else []
    if files:
        for f in files:
            L.append(f"- `{f}`")
    else:
        L.append("_No slate-data files uploaded._")

    # --- Sim data --- #
    L += ["", "## Sim data"]
    sim = load_sim_summary(slug)
    if sim:
        L.append(f"- File: `{sim['path']}` ({sim['n_rows']:,} rows × {sim['n_cols']} cols)")
        if sim.get("columns"):
            L.append(f"- Columns: {', '.join(sim['columns'])}")
        if sim.get("error"):
            L.append(f"- ⚠️ {sim['error']}")
    else:
        L.append("_No sim data uploaded._")

    # --- References for Claude --- #
    L += ["", "## References for Claude (read as needed)"]
    rules_dir = _REPO_ROOT / "rules" / slug
    for doc in ("philosophy.md", "framework.md", "autopsies.md", "autopsy_data.jsonl"):
        L.append(f"- `{rules_dir / doc}`")
    L.append(f"- `{_REPO_ROOT / 'rules' / 'shared' / 'anchor_equivalence.md'}`")
    if sport == "nascar":
        tracks_dir = _REPO_ROOT / "rules" / "nascar" / "tracks"
        tracks = sorted(tracks_dir.glob("*.md")) if tracks_dir.exists() else []
        for t in tracks:
            if t.stem.lower() != "readme":
                L.append(f"- `{t}`")

    strategy = load_strategy(slug)
    lessons = strategy.get("recent_lessons", [])[:3]
    if lessons:
        L += ["", "### Recent autopsy lessons"]
        for lesson in lessons:
            notes = (lesson.get("notes") or "").strip() or "_(no notes)_"
            us = lesson.get("user_summary") or {}
            rank_note = (
                f" (best rank {us['best_rank']:,}/{lesson['entries']:,})"
                if us.get("best_rank") and lesson.get("entries") else ""
            )
            L.append(f"- `{lesson.get('timestamp', '?')}` — {notes[:300]}{rank_note}")

    L += ["", f"**Output target:** write the synthesis to `data/slate_analysis/{slug}.md`."]

    out = _path(slug)
    out.write_text("\n".join(L) + "\n")
    return out


def clear_bundle(slug: str) -> None:
    """Delete the bundle file. Called after an autopsy log so the next slate starts fresh."""
    p = _path(slug)
    if p.exists():
        p.unlink()
