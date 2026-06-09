"""DFS Slate Analyzer — Streamlit app.

Multi-sport DFS slate analyzer for DraftKings.
Flow: Projections → Slate Data → Sim Data → Analyze → Autopsy.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from src import sessions
from src.projections import load_projections, warn_missing_for_sport
from src.landscape import chalk_summary, leverage_table, anchor_equivalence_check
from src.projections_diff import flagged_disagreements
from src.autopsy import parse_dk_results
from src.strategy import load_strategy, load_track, load_shared
from src.slate_analysis import snapshot, top_chalk, sport_signals, load_persisted, clear_persisted
from src.contests import (
    CONTEST_TYPES as CONTEST_ENTRY_TYPES,
    load_contests, add_contest, remove_contest,
    clear_contests, portfolio_summary,
)
from src.sim_data import save_sim, load_sim_summary, clear_sim
from src.bundle import clear_bundle
from src.analysis_runner import run_analysis


REPO_ROOT = Path(__file__).parent

CONTEST_TYPES = {
    "PGA Classic": {"slug": "pga_classic", "sport": "golf"},
    "PGA RD4 Showdown": {"slug": "pga_rd4_sd", "sport": "golf"},
    "MMA": {"slug": "mma_se", "sport": "mma"},
    "NASCAR": {"slug": "nascar", "sport": "nascar"},
}


st.set_page_config(page_title="DFS Slate Analyzer", layout="wide")
st.title("DFS Slate Analyzer")
st.caption("Multi-sport DFS slate analyzer for DraftKings.")

# ---------- Sidebar ---------- #
with st.sidebar:
    contest_label = st.selectbox("Contest type", list(CONTEST_TYPES.keys()))
    cfg = CONTEST_TYPES[contest_label]
    slug = cfg["slug"]
    sport = cfg["sport"]

    st.divider()
    if st.button("Clear this sport's slate", type="secondary"):
        sessions.clear(slug)
        st.rerun()

# Load active sport's strategy bundle (used by the Analyze tab)
strategy = load_strategy(slug)


# ---------- Tabs ---------- #
tab_proj, tab_slate, tab_sim, tab_analyze, tab_autopsy = st.tabs(
    ["Projections", "Slate Data", "Sim Data", "Analyze", "Autopsy"]
)


# ===== Tab 1: Projections =====
with tab_proj:
    st.subheader(f"Step 1: Upload {contest_label} projections")
    st.caption(
        "Drop any vendor CSV — ETR, Ship It Nation, DailyFan, DK. "
        "Vendor is auto-detected. Upload multiple to surface cross-vendor "
        "disagreement in the Analyze tab."
    )

    uploaded = st.file_uploader(
        "Vendor CSV",
        type="csv",
        accept_multiple_files=True,
        key=f"upload_{slug}",
    )

    if uploaded:
        for f in uploaded:
            try:
                df = load_projections(f)
            except Exception as e:
                st.error(f"❌ Failed to load {f.name}: {e}")
                continue
            vendor_name = df.attrs.get("vendor")
            if vendor_name is None:
                st.error(
                    f"❌ Couldn't detect vendor for {f.name}. "
                    f"Headers seen: {list(df.columns)}"
                )
                continue
            sessions.save_source(slug, f.name, df, vendor_name)
            st.success(f"✅ {f.name} — detected as **{vendor_name}** ({len(df)} players)")

    sources = sessions.load_sources(slug)
    if sources:
        st.divider()
        st.markdown(f"**Loaded sources ({len(sources)}):**")
        for name, blob in sources.items():
            cols = st.columns([4, 2, 1])
            cols[0].write(f"📄 {name}")
            cols[1].write(f"`{blob['vendor']}` · {len(blob['df'])} players")
            if cols[2].button("Drop", key=f"drop_{name}"):
                sessions.drop_source(slug, name)
                st.rerun()

        st.divider()
        primary_name = st.selectbox("Primary source for the analysis", list(sources.keys()))
        df = sources[primary_name]["df"]

        warnings = warn_missing_for_sport(df, sport)
        for w in warnings:
            st.warning(w)

        st.dataframe(df, use_container_width=True, height=500)
    else:
        st.info("No projections uploaded yet.")


# ===== Tab 2: Slate Data =====
with tab_slate:
    st.subheader(f"Slate Data — {contest_label}")
    st.caption("Upload articles, notes, photos, and screenshots for the slate. Claude reads these when writing the analysis.")
    articles_dir = REPO_ROOT / "articles" / slug
    articles_dir.mkdir(parents=True, exist_ok=True)

    uploaded_pdfs = st.file_uploader(
        "Upload article PDFs / notes",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        key=f"articles_{slug}",
    )
    if uploaded_pdfs:
        for f in uploaded_pdfs:
            ts = datetime.now().strftime("%Y-%m-%d")
            dest = articles_dir / f"{ts}__{f.name}"
            dest.write_bytes(f.read())
            st.success(f"Saved {dest.name}")

    uploaded_photos = st.file_uploader(
        "Upload photos / screenshots",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key=f"photos_{slug}",
    )
    if uploaded_photos:
        for f in uploaded_photos:
            ts = datetime.now().strftime("%Y-%m-%d")
            dest = articles_dir / f"{ts}__{f.name}"
            dest.write_bytes(f.read())
            st.success(f"Saved {dest.name}")

    files = sorted(articles_dir.glob("*"))
    if not files:
        st.info("No slate data uploaded yet for this contest type.")
    else:
        st.markdown(f"**{len(files)} file(s):**")
        for f in files:
            cols = st.columns([5, 1])
            icon = "🖼️" if f.suffix.lower() in (".png", ".jpg", ".jpeg") else "📄"
            cols[0].write(f"{icon} {f.name}")
            if cols[1].button("Delete", key=f"del_{f.name}"):
                f.unlink()
                st.rerun()


# ===== Tab 3: Sim Data =====
with tab_sim:
    st.subheader(f"Sim Data — {contest_label}")
    st.caption(
        "Optional. Upload a sim export CSV (e.g. SaberSim). It's stored as-is for "
        "Claude to read; a light summary shows below."
    )

    up = st.file_uploader("Sim export (CSV)", type="csv", key=f"sim_{slug}")
    if up is not None and st.button("Store sim file", type="primary", key=f"sim_save_{slug}"):
        meta = save_sim(slug, up)
        if meta.get("error"):
            st.warning(f"Stored {meta['filename']}, but {meta['error']}")
        else:
            st.success(f"Stored {meta['filename']} — {meta['n_rows']:,} rows × {meta['n_cols']} cols")

    summary = load_sim_summary(slug)
    if summary:
        st.divider()
        st.markdown("### Stored sim file")
        st.caption(f"`{summary['filename']}` · {summary['n_rows']:,} rows · {summary['n_cols']} cols")
        if summary.get("columns"):
            st.write("**Columns:** " + ", ".join(summary["columns"]))
        if summary.get("preview"):
            st.dataframe(pd.DataFrame(summary["preview"]), use_container_width=True)
        if summary.get("error"):
            st.warning(summary["error"])
        if st.button("Remove sim file", key=f"sim_clear_{slug}"):
            clear_sim(slug)
            st.rerun()
    else:
        st.info("No sim data stored for this slate.")


# ===== Tab 4: Analyze =====
with tab_analyze:
    st.subheader(f"Analyze — {contest_label}")
    st.caption(
        "Set your contests, review the auto-snapshot, then bundle everything for Claude. "
        "Claude's written analysis appears at the bottom."
    )

    # ----- (a) Contest config (folded in) -----
    contests_list = load_contests(slug)
    with st.expander("Contests", expanded=not contests_list):
        st.caption(
            "Declare which contests you're entering. Field size + your entry count drive how "
            "contrarian the read is and how many unique lineups Claude builds."
        )
        if contests_list:
            csum = portfolio_summary(slug)
            c1, c2, c3 = st.columns(3)
            c1.metric("Contests", csum["n_contests"])
            c2.metric("Total entries", csum["total_entries"])
            c3.metric("Unique lineups needed", csum["unique_lineups_needed"])

        with st.form(key=f"add_contest_{slug}", clear_on_submit=True):
            name = st.text_input("Contest name", placeholder="e.g., UFC $100K MEGA mini-MAX")
            type_label = st.selectbox("Contest type", list(CONTEST_ENTRY_TYPES.keys()))
            type_meta = CONTEST_ENTRY_TYPES.get(type_label, {})
            col_a, col_b = st.columns(2)
            with col_a:
                field_size = st.number_input("Field size (entries)", min_value=1, value=1000, step=100)
                my_entries = st.number_input("My entries", min_value=1, value=1, step=1)
            with col_b:
                max_entries = st.number_input(
                    "Max entries allowed", min_value=1,
                    value=type_meta.get("default_max_entries", 1), step=1,
                )
            col_c, col_d = st.columns(2)
            with col_c:
                entry_fee = st.number_input("Entry fee ($, optional)", min_value=0.0, value=0.0, step=0.25)
            with col_d:
                prize_pool = st.number_input("Prize pool ($, optional)", min_value=0, value=0, step=100)
            submitted = st.form_submit_button("Add contest", type="primary")
            if submitted and name.strip():
                add_contest(slug, {
                    "name": name.strip(),
                    "type": type_label,
                    "field_size": int(field_size),
                    "max_entries": int(max_entries),
                    "my_entries": int(my_entries),
                    "entry_fee": float(entry_fee) if entry_fee else None,
                    "prize_pool": int(prize_pool) if prize_pool else None,
                })
                st.rerun()

        for c in contests_list:
            cols = st.columns([6, 3, 1])
            cols[0].markdown(f"**{c['name']}** — *{c['type']}*")
            cols[1].caption(f"Field {c['field_size']:,} · entries {c['my_entries']}/{c['max_entries']}")
            if cols[2].button("✕", key=f"del_contest_{c['id']}"):
                remove_contest(slug, c["id"])
                st.rerun()

    # ----- (b) Auto-snapshot -----
    st.markdown("---")
    sources = sessions.load_sources(slug)
    if not sources:
        st.info("Upload projections in the Projections tab — the snapshot pulls from your active session.")
    else:
        primary_name = list(sources.keys())[0]
        df = sources[primary_name]["df"]
        st.caption(f"Reading from: **{primary_name}** ({sources[primary_name]['vendor']})")

        snap = snapshot(df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Players", f"{snap['n_players']}")
        c2.metric("Top-5 own concentration", f"{snap['top5_own_concentration_pct']}%")
        c3.metric("Chalk (≥15%)", f"{snap['n_chalk']}")
        c4.metric("Leverage pool (<5% own)", f"{snap['n_leverage_candidates']}")
        st.caption(
            f"Avg salary ${snap['avg_salary']:,.0f} · range ${snap['min_salary']:,}–${snap['max_salary']:,} · avg proj {snap['avg_proj']}"
        )

        st.markdown("### Chalk tiers")
        st.dataframe(chalk_summary(df), use_container_width=True)

        st.markdown("### Top chalk")
        chalk = top_chalk(df)
        if chalk.empty:
            st.info("No players above 15% ownership.")
        else:
            st.dataframe(chalk, use_container_width=True)

        st.markdown("### Top leverage candidates")
        st.caption("Sorted by `upside / (ownership + 1)`. Higher = better GPP leverage.")
        st.dataframe(leverage_table(df), use_container_width=True)

        st.markdown("### Anchor-Equivalence pre-lock check")
        with st.expander("📖 Read the rule"):
            st.markdown(load_shared("anchor_equivalence") or "_Missing._")
        groups = anchor_equivalence_check(df)
        if not groups:
            st.success("✅ No anchor-equivalence pairs at similar ownership.")
        else:
            for g in groups:
                st.warning(
                    f"**{', '.join(g['players'])}** (own% {g['own_range'][0]:.1f}–{g['own_range'][1]:.1f}) — {g['rule']}"
                )

        # Sport-specific signals
        signals = sport_signals(df, sport)
        if signals:
            st.markdown(f"### {sport.upper()} signals")
            for key, table in signals.items():
                st.markdown(f"**{key.replace('_', ' ').title()}**")
                st.dataframe(table, use_container_width=True)

        # NASCAR track reminder
        if slug == "nascar":
            track_files = strategy["track_files"]
            if track_files:
                picked = st.selectbox("Track notes", track_files, key="nascar_track_pick")
                with st.expander(f"🏁 Track notes — {picked}", expanded=False):
                    st.markdown(load_track(picked))
            else:
                st.warning("No NASCAR track notes yet. Add `rules/nascar/tracks/<slug>.md`.")
        if slug == "pga_rd4_sd":
            st.warning("⛳ **RD4 Showdown**: flat 6-golfer lineup — NO captain, NO 1.5x multiplier.")

        # Cross-vendor disagreement (auto)
        if len(sources) >= 2:
            st.markdown("### Vendor disagreement (top 5 on proj_points)")
            flagged = flagged_disagreements(sources, metric="proj_points", pct_threshold=15.0)
            if flagged.empty:
                st.success("Vendors broadly agree at the 15% threshold.")
            else:
                st.dataframe(flagged.head(5), use_container_width=True)

    # ----- (d) Generate the slate analysis (one click) -----
    st.markdown("---")
    st.markdown("### Generate slate analysis")
    st.caption(
        "Runs Claude on your uploaded projections, articles, and strategy docs and writes "
        "the analysis below — no need to leave the app. Takes ~1–3 minutes. "
        "Uses your Claude subscription."
    )
    if not sources:
        st.info("Upload projections first — the analysis reads from your active session.")
    elif st.button("✨ Generate slate analysis", type="primary", key=f"analyze_{slug}"):
        with st.spinner("Analyzing the slate — reading your projections, articles, and strategy docs… (~1–3 min)"):
            result = run_analysis(slug, contest_label, sport)
        if result["ok"]:
            cost = result.get("cost_usd")
            cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
            st.success(f"Analysis written in {result['duration_s']:.0f}s{cost_note}.")
            st.rerun()
        else:
            st.error(f"Couldn't generate the analysis: {result['error']}")

    # ----- (e) The written analysis -----
    st.markdown("---")
    st.markdown("## Slate analysis")
    persisted = load_persisted(slug)
    if persisted:
        with st.container(border=True):
            st.caption(f"Last updated: {persisted['mtime']}")
            st.markdown(persisted["markdown"])
    else:
        st.info("**No saved analysis yet.** Click **Generate slate analysis** above and it appears here.")


# ===== Tab 5: Autopsy =====
with tab_autopsy:
    st.subheader(f"Post-slate autopsy — {contest_label}")

    dk_csvs = st.file_uploader(
        "DraftKings contest-standings CSV(s)",
        type="csv",
        accept_multiple_files=True,
        key=f"dk_upload_{slug}",
        help="Upload one CSV per DK contest you entered on this slate. Each is "
             "summarized and logged as its own autopsy entry. Player scores are "
             "identical across contests; field size, winning score, and cash line differ.",
    )

    if dk_csvs:
        # Parse + display each contest in its own section, collecting a per-CSV
        # payload (with its own notes) for the single Log button below. A bad
        # CSV is reported but doesn't block the others.
        parsed_contests = []
        for i, dk_csv in enumerate(dk_csvs):
            try:
                parsed = parse_dk_results(dk_csv)
            except ValueError as e:
                st.error(f"{dk_csv.name}: {e}")
                continue
            lineups = parsed["lineups"]
            players = parsed["players"]

            with st.expander(
                f"{dk_csv.name} — {len(lineups):,} entries, winning "
                f"{lineups['Points'].max():.1f}",
                expanded=(i == 0),
            ):
                st.markdown("### Field summary")
                c1, c2, c3 = st.columns(3)
                c1.metric("Entries", f"{len(lineups):,}")
                c2.metric("Winning score", f"{lineups['Points'].max():.1f}")
                c3.metric("Cash line (top 20%)", f"{lineups['Points'].quantile(0.80):.1f}")

                st.markdown("### Top 10 lineups")
                top = lineups.nlargest(10, "Points")[["Rank", "EntryName", "Points", "Lineup_parsed"]]
                st.dataframe(top, use_container_width=True)

                st.markdown("### Highest-scoring players")
                top_players = players.nlargest(15, "actual_fpts")[
                    ["name", "roster_position", "actual_own", "actual_fpts"]
                ]
                st.dataframe(top_players, use_container_width=True)

                notes = st.text_area(
                    "Lessons / patterns to log (appended to autopsies.md)",
                    key=f"autopsy_notes_{slug}_{i}",
                    height=120,
                )
            parsed_contests.append({
                "name": dk_csv.name,
                "lineups": lineups,
                "notes": notes,
            })

        if parsed_contests:
            st.divider()
            if st.button("📝 Log autopsy", type="primary"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                md_path = REPO_ROOT / "rules" / slug / "autopsies.md"
                md_path.parent.mkdir(parents=True, exist_ok=True)
                jsonl_path = REPO_ROOT / "rules" / slug / "autopsy_data.jsonl"
                # One autopsies.md section + one autopsy_data.jsonl row per
                # contest; source_file disambiguates same-type contests.
                with md_path.open("a") as fmd, jsonl_path.open("a") as fjl:
                    for pc in parsed_contests:
                        lineups = pc["lineups"]
                        notes = pc["notes"]
                        fmd.write(f"\n\n## {ts} — {contest_label} ({pc['name']})\n")
                        fmd.write(f"- Entries: {len(lineups):,}\n")
                        fmd.write(f"- Winning score: {lineups['Points'].max():.1f}\n")
                        fmd.write(f"- Cash line (top 20%): {lineups['Points'].quantile(0.80):.1f}\n")
                        if notes.strip():
                            fmd.write(f"\n{notes.strip()}\n")
                        row = {
                            "timestamp": ts,
                            "contest_type": contest_label,
                            "source_file": pc["name"],
                            "entries": int(len(lineups)),
                            "winning_score": float(lineups["Points"].max()),
                            "cash_line_p80": float(lineups["Points"].quantile(0.80)),
                            "notes": notes.strip(),
                        }
                        fjl.write(json.dumps(row) + "\n")
                # Clear all per-slate state — next slate starts fresh
                clear_persisted(slug)
                clear_contests(slug)
                clear_sim(slug)
                clear_bundle(slug)
                st.success(
                    f"Logged {len(parsed_contests)} contest(s) to rules/{slug}/autopsies.md "
                    "+ autopsy_data.jsonl. Cleared the slate analysis, contests, sim data, "
                    "and bundle for next time."
                )

    st.divider()
    st.markdown("### Cross-slate patterns (autopsies.md)")
    st.caption("Most recent slate first; older slates below.")
    autopsies_md = REPO_ROOT / "rules" / slug / "autopsies.md"
    if autopsies_md.exists():
        _text = autopsies_md.read_text()
        # Render dated slate sections newest-first. Keep the file preamble
        # (title/intro) pinned on top and any non-dated section (e.g. the
        # "Template for Future SE Entries") at the bottom.
        _chunks = re.split(r"(?m)^(?=## )", _text)
        _preamble = _chunks[0] if _chunks and not _chunks[0].startswith("## ") else ""
        _sections = _chunks[1:] if _preamble else _chunks
        _dated = [c for c in _sections if re.match(r"## \d{4}-", c)]
        _other = [c for c in _sections if not re.match(r"## \d{4}-", c)]
        _ordered = ([_preamble] if _preamble else []) + list(reversed(_dated)) + _other
        st.markdown("".join(_ordered))
    else:
        st.info("No autopsies logged yet for this contest type.")
