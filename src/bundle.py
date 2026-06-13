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
from src.sim_data import load_sim_files
from src.strategy import load_strategy

_REPO_ROOT = Path(__file__).parent.parent
_BUNDLE_DIR = _REPO_ROOT / "data" / "bundle"

# Venue-knowledge dir per slug (relative to rules/). Both PGA slugs share the
# same physical courses; MMA has no strategy-relevant venue.
_VENUE_DIRS = {
    "nascar": "nascar/tracks",
    "pga_classic": "pga_classic/courses",
    "pga_rd4_sd": "pga_classic/courses",
    "mlb_classic": "mlb_classic/parks",
}


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

    # --- Sim data / lineup pools --- #
    L += ["", "## Sim data"]
    sim_files = load_sim_files(slug)
    if sim_files:
        L.append(
            f"{len(sim_files)} uploaded lineup-pool file(s). Each row is a candidate "
            "lineup (the first columns are DK player IDs in roster-slot order); sim "
            "metric columns may or may not be present. Read every file below:"
        )
        for sim in sim_files:
            kind = "has sims" if sim.get("has_sim_cols") else "rosters only"
            L.append(f"- `{sim['path']}` ({sim['n_rows']:,} rows × {sim['n_cols']} cols · {kind})")
            if sim.get("columns"):
                L.append(f"    - Columns: {', '.join(sim['columns'])}")
            if sim.get("error"):
                L.append(f"    - ⚠️ {sim['error']}")
    else:
        L.append("_No sim data / lineup pools uploaded._")

    # --- References for Claude --- #
    L += ["", "## References for Claude (read as needed)"]
    rules_dir = _REPO_ROOT / "rules" / slug
    for doc in ("philosophy.md", "framework.md", "autopsies.md", "autopsy_data.jsonl"):
        L.append(f"- `{rules_dir / doc}`")
    L.append(f"- `{_REPO_ROOT / 'rules' / 'shared' / 'anchor_equivalence.md'}`")
    lessons_path = rules_dir / "lessons.yaml"
    if lessons_path.exists():
        L.append(f"- `{lessons_path}` — **mandatory pre-build read: open lessons (hypothesis/validated)**")
    results_path = rules_dir / "results.jsonl"
    if results_path.exists():
        L.append(f"- `{results_path}` — cross-slate results ledger")
    calibration_path = rules_dir / "vendor_calibration.jsonl"
    if calibration_path.exists():
        L.append(f"- `{calibration_path}` — per-vendor accuracy history vs DK actuals")
    venue_rel = _VENUE_DIRS.get(slug)
    if venue_rel:
        venue_dir = _REPO_ROOT / "rules" / venue_rel
        venues = sorted(venue_dir.glob("*.md")) if venue_dir.exists() else []
        for v in venues:
            if v.stem.lower() != "readme":
                L.append(f"- `{v}`")

    # Vendor calibration inline so the headless run can't skip it.
    from src.history import load_results, vendor_accuracy
    acc = vendor_accuracy(slug)
    if acc:
        L += ["", "### Vendor calibration (vs DK actuals)"]
        for a in acc:
            flag = " ⚠️ <3 slates — note only, do not weight" if a["slates"] < 3 else ""
            proj = a["proj_mae"] if a["proj_mae"] is not None else "n/a"
            own = a["own_mae"] if a["own_mae"] is not None else "n/a"
            L.append(
                f"- **{a['vendor']}** — {a['slates']} slate(s): proj MAE {proj}, own MAE {own}{flag}"
            )
        L.append(
            "_When vendors disagree, weight the vendor with the lower demonstrated MAE for that "
            "metric; ownership MAE drives leverage calls._"
        )

    # Last 3 slate results inline so the headless run can't skip them.
    recent_results = load_results(slug, n=3)
    if recent_results:
        L += ["", "### Recent slate results (from results.jsonl)"]
        for r in reversed(recent_results):
            roi = f"{r['roi_pct']}%" if r.get("roi_pct") is not None else "n/a"
            pct = f"top {r['best_percentile']}%" if r.get("best_percentile") is not None else "no entries found"
            L.append(
                f"- `{r.get('date')}` — {r.get('slate_label')}: {r.get('entries_total')} entries, "
                f"ROI {roi}, best finish {pct} (archive: `{r.get('history_dir')}`)"
            )
        L.append("_GPP ROI is noise under ~10 slates — read these for process notes, not conclusions._")

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
