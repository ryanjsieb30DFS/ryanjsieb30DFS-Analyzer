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
    "mlb_classic": "mlb_classic/parks",
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
            L.append(
                f"  - **{c['name']}** ({c['type']}): field {c.get('field_size', '?'):,}, "
                f"my entries {c.get('my_entries', '?')}/{c.get('max_entries', '?')}"
            )
        L.append(
            "_Field size frames how contrarian the read should be — bigger field → "
            "more ceiling/leverage; smaller field → tighter, higher-floor calls._"
        )
    else:
        L.append("_No contests declared._")

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
