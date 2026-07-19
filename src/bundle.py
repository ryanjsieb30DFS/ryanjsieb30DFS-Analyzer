"""Bundle for Claude.

`build_bundle` consolidates the inputs for the active slate into a single
markdown file at data/bundle/<slug>.md so Claude can read one file to find
everything: the declared contests, the on-disk article/slate-data files (the
primary input), and absolute paths to the strategy docs.

The bundle POINTS TO the strategy docs and slate-data files (paths) rather than
inlining them — Claude reads those with the Read tool. The output target for
the synthesis is data/slate_analysis/<slug>.md (the written slate strategy).
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from src import sessions
from src.contests import load_contests, portfolio_summary

_REPO_ROOT = Path(__file__).parent.parent
_BUNDLE_DIR = _REPO_ROOT / "data" / "bundle"

# Venue-knowledge dir per slug (relative to rules/). Both PGA slugs share the
# same physical courses; MMA has no strategy-relevant venue.
_VENUE_DIRS = {
    "nascar": "nascar/tracks",
    "pga_classic": "pga_classic/courses",
    "pga_rd4_sd": "pga_classic/courses",
}


def _path(slug: str) -> Path:
    return _BUNDLE_DIR / f"{slug}.md"


def build_bundle(slug: str, contest_label: str, sport: str) -> Path:
    """Write data/bundle/<slug>.md consolidating all inputs. Returns the path."""
    _BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    L: list[str] = [
        f"# Slate bundle — {contest_label}",
        f"_Generated {ts} · slug `{slug}` · sport `{sport}`_",
        "",
        "This file consolidates everything for the active slate: the article/slate-data "
        "files AND every loaded vendor projection. Read it, then read the article files it "
        "points to + the strategy docs + the projection tables below, then write the slate "
        f"strategy to `data/slate_analysis/{slug}.md`.",
    ]

    # --- Contest config --- #
    L += ["", "## Contests"]
    contests = load_contests(slug)
    if contests:
        summ = portfolio_summary(slug)
        L.append(
            f"- {summ['n_contests']} contest(s), {summ['total_entries']} total entries"
        )
        for c in contests:
            line = (
                f"  - **{c['name']}** ({c['type']}): field {c.get('field_size', '?'):,}, "
                f"my entries {c.get('my_entries', '?')}/{c.get('max_entries', '?')}"
            )
            # Payout shape frames the contrarian dial: top-heavy pays the ceiling
            # chase; flat pays tighter theses. Prize multiple = pool / total fees
            # (higher = softer rake / overlay).
            shape = c.get("payout_shape")
            if shape:
                line += f", payout **{shape}**"
            fee, pool_, fs = c.get("entry_fee"), c.get("prize_pool"), c.get("field_size")
            if fee and pool_ and fs:
                line += f", prize multiple {pool_ / (fee * fs):.2f}x"
            L.append(line)
        if any(c.get("payout_shape") for c in contests):
            L.append(
                "_Payout shape read: **Top-heavy** → the win is everything; maximum-ceiling, "
                "contrarian builds and the leverage-away reads matter most. **Flat** → many "
                "similar payouts; a tight high-floor-of-ceiling thesis competes fine. "
                "**Balanced** → in between. Surface it in `## How to approach the slate`; "
                "never a play/fade command._"
            )
        L.append(
            "_This tool is focused on **small-field GPPs — Single Entry, 3-Max, and "
            "5-Max**. Build for a tight all-unique set of 1/3/5 bullets: still "
            "ceiling-and-leverage over median (GPP), but each of your few lineups is a "
            "distinct thesis — no 150-max MME spray. Field size within this range tunes "
            "the contrarian dial; it never flips you to a cash/floor game._"
        )
    else:
        L.append("_No contests declared._")

    # --- Field tendencies (forward-feed: how the field plays THIS contest type) --- #
    if contests:
        try:
            from src import field_tendencies
            block = field_tendencies.bundle_block(slug, contests)
            if block:
                L += ["", block]
        except Exception:  # noqa: BLE001 — never block the bundle
            pass

    # --- Shark reality (forward-feed: how the PROS in your contests actually play) --- #
    try:
        from src import shark_dossier
        shark_block = shark_dossier.shark_reality_block(slug)
        if shark_block:
            L += ["", shark_block]
    except Exception:  # noqa: BLE001 — never block the bundle
        pass

    # --- Process trend (forward-feed: the self-grade sequences from results.jsonl,
    # so a recurring weakness — leverage capture at 0%, climbing bust exposure,
    # violated fades — shapes THIS strategy instead of dying in the archive) --- #
    try:
        from src import history as _hist
        trend_block = _hist.process_trend_block(slug)
        if trend_block:
            L += ["", trend_block]
    except Exception:  # noqa: BLE001 — never block the bundle
        pass

    # --- Slate data files (the primary input) --- #
    L += ["", "## Slate data files (read these — they are the primary input)"]
    articles_dir = _REPO_ROOT / "articles" / slug
    files = sorted(articles_dir.glob("*")) if articles_dir.exists() else []
    if files:
        L.append(
            "Read every file: `*.pdf`, `*.txt`/`*.md`, `*.csv` (read as text tables), "
            "and `*.png`/`*.jpg`/`*.jpeg` (the Read tool reads images visually, so "
            "screenshots work). Note in the output if anything couldn't be parsed."
        )
        for f in files:
            L.append(f"- `{f}`")
    else:
        L.append("_No slate-data files uploaded — there is nothing to synthesize from._")

    # --- Projections (vendor data — a primary input too) --- #
    proj_sources = sessions.load_sources(slug)
    if proj_sources:
        L += ["", "## Projections (vendor data — read and use these too)"]
        L.append(
            "Every vendor projection loaded for this slate. Use these ownership/projection "
            "numbers alongside the articles. Where the two vendors disagree — or where a vendor "
            "disagrees with the articles — that gap is signal worth surfacing."
        )
        _pref = ["name", "salary", "ownership", "proj_points", "ceiling",
                 "win_prob", "opponent", "team", "position", "batting_order"]
        for name, blob in proj_sources.items():
            df = blob.get("df")
            if df is None or df.empty:
                continue
            cols = [c for c in _pref if c in df.columns]
            if not cols:
                cols = list(df.columns)
            L += ["", f"### {blob.get('vendor', 'Unknown vendor')} — `{name}` ({len(df)} players)"]
            L.append("| " + " | ".join(cols) + " |")
            L.append("| " + " | ".join("---" for _ in cols) + " |")
            for _, r in df.iterrows():
                cells = ["" if (v := r[c]) is None or (isinstance(v, float) and pd.isna(v))
                         else str(v) for c in cols]
                L.append("| " + " | ".join(cells) + " |")

    # --- Leverage candidates to address (coverage guard) --- #
    if proj_sources:
        from src import landscape
        from src.player_pool import build_pool
        pool = build_pool(proj_sources)
        cands = landscape.leverage_candidates(pool) if not pool.empty else pd.DataFrame()
        if not cands.empty:
            L += ["", "## Leverage candidates to address (sub-10% own, high ceiling)"]
            L.append(
                "COVERAGE RULE: the slate strategy's `## Leverage & fades` or `## Edges & tensions` "
                "AND the player pool must ADDRESS **each** player below with a one-line synthesis "
                "of their leverage/ceiling case (surface it — no play/fade command required). Never "
                "silently omit one — a sub-10% high-ceiling play left unaddressed is a coverage leak "
                "(the play that decides the slate from nowhere). Individual plays only; build no lineups."
            )
            for _, r in cands.iterrows():
                own = f"{r['ownership']:.0f}%" if pd.notna(r.get("ownership")) else "n/a"
                proj = (f"{r['proj_points']:.1f}" if "proj_points" in cands.columns
                        and pd.notna(r.get("proj_points")) else "n/a")
                ceil = f"{r['upside']:.1f}" if pd.notna(r.get("upside")) else "n/a"
                sal = (f"${int(r['salary']):,}" if "salary" in cands.columns
                       and pd.notna(r.get("salary")) else "n/a")
                L.append(f"- {r['name']} — {sal}, {own} own, proj {proj}, ceiling {ceil}")

        # --- Chalk combos: THIS slate's likely-duplicated pairs (duplication watch) --- #
        combos = landscape.chalky_combos(pool) if not pool.empty else []
        if combos:
            # Expected copies scale with the biggest declared field.
            field = max((c.get("field_size") or 0) for c in contests) if contests else 0
            L += ["", "## Chalk combos — the pairs the field will stack together (duplication watch)"]
            L.append(
                "Estimated from this slate's projected ownership (co-occurrence ≈ ownA × ownB — "
                "a FLOOR, real fields correlate their chalk). Rostering one of these pairs means "
                "sharing that slice of the field's lineups — it is where uniqueness quietly dies "
                "in a small-field GPP. The strategy MUST surface the top combos as a duplication "
                "tension in `## Edges & tensions` (descriptive — never a fade command; breaking a "
                "pair is the user's call)."
            )
            for c in combos:
                line = (f"- **{c['players'][0]} + {c['players'][1]}** — "
                        f"{c['own_a']}% × {c['own_b']}% ≈ {c['joint_pct']}% of the field")
                if field:
                    line += f" (~{int(round(c['joint_pct'] / 100 * field)):,} lineups of {field:,})"
                L.append(line)

    # --- References for Claude --- #
    L += ["", "## References for Claude (read as needed)"]
    rules_dir = _REPO_ROOT / "rules" / slug
    for doc in ("philosophy.md", "framework.md", "autopsies.md", "autopsy_data.jsonl"):
        L.append(f"- `{rules_dir / doc}`")
    L.append(f"- `{_REPO_ROOT / 'rules' / 'shared' / 'anchor_equivalence.md'}`")
    sharp_path = _REPO_ROOT / "rules" / "shared" / "sharp_playbook.md"
    if sharp_path.exists():
        L.append(f"- `{sharp_path}` — sharp-player tendencies reverse-engineered from contest standings")
    lessons_path = rules_dir / "lessons.yaml"
    if lessons_path.exists():
        L.append(f"- `{lessons_path}` — **mandatory pre-flight read: open lessons (hypothesis/validated)**")
    results_path = rules_dir / "results.jsonl"
    if results_path.exists():
        L.append(f"- `{results_path}` — cross-slate results ledger (process notes only)")
    venue_rel = _VENUE_DIRS.get(slug)
    if venue_rel:
        venue_dir = _REPO_ROOT / "rules" / venue_rel
        venues = sorted(venue_dir.glob("*.md")) if venue_dir.exists() else []
        for v in venues:
            if v.stem.lower() != "readme":
                L.append(f"- `{v}`")

    L += ["", f"**Output target:** write the slate strategy to `data/slate_analysis/{slug}.md`."]

    out = _path(slug)
    out.write_text("\n".join(L) + "\n")
    return out


def clear_bundle(slug: str) -> None:
    """Delete the bundle file. Called after an autopsy log so the next slate starts fresh."""
    p = _path(slug)
    if p.exists():
        p.unlink()
