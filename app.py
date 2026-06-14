"""DFS Slate Analyzer — Streamlit app.

Multi-sport DFS slate analyzer for DraftKings.
Flow: Projections → Slate Data → Sim Data → Analyze → Autopsy.
"""
from __future__ import annotations

import io
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
from src.autopsy import (
    parse_dk_results, analyze_contest, load_session_projections,
    build_autopsy_record, record_md_summary, score_vendors,
)
from src.strategy import load_strategy, load_track, load_shared
from src.slate_analysis import snapshot, top_chalk, sport_signals, load_persisted, clear_persisted
from src.contests import (
    CONTEST_TYPES as CONTEST_ENTRY_TYPES,
    load_contests, add_contest, remove_contest,
    clear_contests, portfolio_summary,
)
from src.contest_templates import load_templates, save_template, remove_template
from src.sim_data import save_sim, load_sim_files, drop_sim_file, clear_sim
from src.bundle import clear_bundle
from src.analysis_runner import (
    run_analysis, run_build_lineups, run_select_lineups, lineup_target,
    run_autopsy_review, run_apply_proposals, run_red_team,
    run_handbuild_analysis, run_rank_lineups,
)
from src.lineups import (
    load_lineups, clear_lineups, load_red_team, clear_red_team,
    roster_spec, lineup_totals, validate_lineup,
    append_handbuilt_lineup, assign_slots,
    load_handbuild_analysis, clear_handbuild_analysis,
    resolve_id_lineups, load_lineup_ranking, clear_lineup_ranking,
    load_ranking_theses, load_ranking_input,
)
from src import history


# resolve() is required: under `streamlit run app.py` __file__ is relative,
# and relative_to() against an unresolved root breaks on absolute paths.
REPO_ROOT = Path(__file__).resolve().parent

CONTEST_TYPES = {
    "PGA Classic": {"slug": "pga_classic", "sport": "golf"},
    "PGA RD4 Showdown": {"slug": "pga_rd4_sd", "sport": "golf"},
    "MMA": {"slug": "mma_se", "sport": "mma"},
    "NASCAR": {"slug": "nascar", "sport": "nascar"},
    "MLB Classic": {"slug": "mlb_classic", "sport": "mlb"},
}


def clear_articles(slug: str) -> None:
    """Delete the slate's uploaded Slate Data files (articles/<slug>/)."""
    articles_dir = REPO_ROOT / "articles" / slug
    if articles_dir.exists():
        for f in articles_dir.glob("*"):
            if f.is_file():
                f.unlink()


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
        clear_articles(slug)
        clear_lineup_ranking(slug)
        st.rerun()

# Load active sport's strategy bundle (used by the Analyze tab)
strategy = load_strategy(slug)


# ---------- Tabs ---------- #
tab_proj, tab_slate, tab_sim, tab_analyze, tab_hand, tab_autopsy = st.tabs(
    ["Projections", "Slate Data", "Sim Data", "Analyze", "Handbuild", "Autopsy"]
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
            if df.attrs.get("kind") is not None:
                st.info(
                    f"📊 {f.name} is {df.attrs['vendor']} data, not player "
                    "projections — upload it in the **Slate Data** tab instead."
                )
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
        pool = sessions.merge_same_vendor(sources)
        primary_name = st.selectbox("Primary source for the analysis", list(pool.keys()))
        df = pool[primary_name]["df"]

        warnings = warn_missing_for_sport(df, sport)
        for w in warnings:
            st.warning(w)

        st.dataframe(df, use_container_width=True, height=500)
    else:
        st.info("No projections uploaded yet.")


# ===== Tab 2: Slate Data =====
with tab_slate:
    st.subheader(f"Slate Data — {contest_label}")
    st.caption("Upload articles, notes, data CSVs, photos, and screenshots for the slate. Claude reads these when writing the analysis.")
    articles_dir = REPO_ROOT / "articles" / slug
    articles_dir.mkdir(parents=True, exist_ok=True)

    uploaded_pdfs = st.file_uploader(
        "Upload article PDFs / notes / data CSVs",
        type=["pdf", "txt", "md", "csv"],
        accept_multiple_files=True,
        key=f"articles_{slug}",
    )
    if uploaded_pdfs:
        for f in uploaded_pdfs:
            data = f.read()
            # CSVs get routed: team-level vendor files (e.g. SIN MLB stacks)
            # become session team data feeding the sport signals; player
            # projections are redirected; everything else is saved as context.
            if f.name.lower().endswith(".csv"):
                detected = None
                try:
                    detected = load_projections(io.BytesIO(data))
                except Exception:
                    pass
                if detected is not None and detected.attrs.get("kind") == "team_stacks":
                    sessions.save_team_data(slug, f.name, detected, detected.attrs["vendor"])
                    st.success(
                        f"📊 {f.name} — detected as **{detected.attrs['vendor']}** "
                        f"({len(detected)} teams). Feeds the {sport.upper()} stack signals."
                    )
                    continue
                if detected is not None and detected.attrs.get("kind") is not None:
                    # Recognized non-projection data (e.g. SIN rankings):
                    # falls through and is saved below as slate context.
                    pass
                elif detected is not None and detected.attrs.get("vendor") is not None:
                    st.warning(
                        f"{f.name} looks like **{detected.attrs['vendor']}** player "
                        "projections — upload it in the **Projections** tab instead."
                    )
                    continue
            ts = datetime.now().strftime("%Y-%m-%d")
            dest = articles_dir / f"{ts}__{f.name}"
            dest.write_bytes(data)
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

    team_data = sessions.load_team_data(slug)
    if team_data is not None:
        cols = st.columns([5, 1])
        cols[0].write(
            f"📊 {team_data.attrs.get('filename', 'team data')} — "
            f"`{team_data.attrs.get('vendor')}` · {len(team_data)} teams "
            f"(feeds the {sport.upper()} stack signals)"
        )
        if cols[1].button("Drop", key="drop_team_data"):
            sessions.drop_team_data(slug)
            st.rerun()

    files = sorted(articles_dir.glob("*"))
    if not files and team_data is None:
        st.info("No slate data uploaded yet for this contest type.")
    elif files:
        st.markdown(f"**{len(files)} file(s):**")
        for f in files:
            cols = st.columns([5, 1])
            suffix = f.suffix.lower()
            icon = "🖼️" if suffix in (".png", ".jpg", ".jpeg") else ("📊" if suffix == ".csv" else "📄")
            cols[0].write(f"{icon} {f.name}")
            if cols[1].button("Delete", key=f"del_{f.name}"):
                f.unlink()
                st.rerun()


# ===== Tab 3: Sim Data =====
with tab_sim:
    st.subheader(f"Sim Data — {contest_label}")
    st.caption(
        "Optional. Upload one or more lineup-pool CSVs — a SaberSim export (with sims) "
        "or a traditional optimizer's files (projection-/ceiling-/50-50-weighted, often "
        "without sims). Upload several at once; they're stored as-is and the **Select "
        "lineups** action in the Analyze tab picks from all of them. Sim columns are optional."
    )

    up = st.file_uploader(
        "Lineup-pool CSV(s)", type="csv", accept_multiple_files=True, key=f"sim_{slug}"
    )
    if up and st.button("Store file(s)", type="primary", key=f"sim_save_{slug}"):
        for f in up:
            meta = save_sim(slug, f)
            if meta.get("error"):
                st.warning(f"Stored {meta['filename']}, but {meta['error']}")
            else:
                kind = "with sims" if meta.get("has_sim_cols") else "rosters only"
                st.success(f"Stored {meta['filename']} — {meta['n_rows']:,} rows × {meta['n_cols']} cols ({kind})")
        st.rerun()

    sim_files = load_sim_files(slug)
    if sim_files:
        st.divider()
        st.markdown(f"### Stored lineup pools ({len(sim_files)})")
        for sim in sim_files:
            kind = "with sims" if sim.get("has_sim_cols") else "rosters only"
            cols = st.columns([5, 1])
            cols[0].markdown(
                f"📄 `{sim['filename']}` · {sim['n_rows']:,} rows · {sim['n_cols']} cols · **{kind}**"
            )
            if cols[1].button("Drop", key=f"sim_drop_{slug}_{sim['filename']}"):
                drop_sim_file(slug, sim["filename"])
                st.rerun()
            if sim.get("error"):
                st.warning(sim["error"])
        with st.expander("Preview columns / rows"):
            for sim in sim_files:
                st.caption(f"`{sim['filename']}` columns: " + ", ".join(sim.get("columns", [])))
                if sim.get("preview"):
                    st.dataframe(pd.DataFrame(sim["preview"]), use_container_width=True)
        if st.button("Remove all", key=f"sim_clear_{slug}"):
            clear_sim(slug)
            st.rerun()
    else:
        st.info("No lineup pools stored for this slate.")


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

        templates = load_templates(slug)
        if templates:
            st.markdown("**Add from saved**")
            tcols = st.columns([5, 2, 2, 1])
            tmpl_names = [t["name"] for t in templates]
            sel_name = tcols[0].selectbox(
                "Saved contest", tmpl_names,
                key=f"tmpl_sel_{slug}", label_visibility="collapsed",
            )
            chosen = next(t for t in templates if t["name"] == sel_name)
            t_field = tcols[1].number_input(
                "Field size", min_value=1, step=100,
                value=int(chosen.get("default_field_size", 1000)),
                key=f"tmpl_fs_{slug}_{chosen['id']}", label_visibility="collapsed",
            )
            t_mine = tcols[2].number_input(
                "My entries", min_value=1, step=1,
                value=int(chosen.get("default_my_entries", 1)),
                key=f"tmpl_me_{slug}_{chosen['id']}", label_visibility="collapsed",
            )
            if tcols[3].button("Add", key=f"tmpl_add_{slug}", type="primary"):
                add_contest(slug, {
                    "name": chosen["name"],
                    "type": chosen["type"],
                    "field_size": int(t_field),
                    "max_entries": int(chosen.get("max_entries", 1)),
                    "my_entries": int(t_mine),
                    "entry_fee": chosen.get("entry_fee"),
                    "prize_pool": chosen.get("prize_pool"),
                })
                st.rerun()
            with st.expander("Manage saved templates"):
                for t in templates:
                    mcols = st.columns([8, 1])
                    mcols[0].caption(f"{t['name']} — {t['type']}")
                    if mcols[1].button("✕", key=f"del_tmpl_{t['id']}"):
                        remove_template(slug, t["id"])
                        st.rerun()
            st.caption("— or add a new contest —")

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
            cols = st.columns([5, 3, 1, 1])
            cols[0].markdown(f"**{c['name']}** — *{c['type']}*")
            cols[1].caption(f"Field {c['field_size']:,} · entries {c['my_entries']}/{c['max_entries']}")
            if cols[2].button("★", key=f"save_tmpl_{c['id']}", help="Save as reusable template"):
                save_template(slug, {
                    "name": c["name"],
                    "type": c["type"],
                    "max_entries": c.get("max_entries", 1),
                    "entry_fee": c.get("entry_fee"),
                    "prize_pool": c.get("prize_pool"),
                    "default_field_size": c.get("field_size", 1000),
                    "default_my_entries": c.get("my_entries", 1),
                })
                st.toast(f"Saved '{c['name']}' to your template library")
                st.rerun()
            if cols[3].button("✕", key=f"del_contest_{c['id']}"):
                remove_contest(slug, c["id"])
                st.rerun()

    # ----- (b) Auto-snapshot -----
    st.markdown("---")
    sources = sessions.merge_same_vendor(sessions.load_sources(slug))
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
        signals = sport_signals(df, sport, team_data=sessions.load_team_data(slug))
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

    # ----- (f) Build lineups (one click, from the analysis) -----
    st.markdown("---")
    st.markdown("### Build lineups")
    st.caption(
        "Builds your portfolio from the analysis — each lineup with a distinct thesis. "
        "Builds fewer if the slate only supports fewer distinct angles. Handbuilt lineups "
        "already saved are kept and built around. "
        "Takes ~3–15 minutes on big slates; uses your Claude subscription."
    )
    n_target = st.number_input(
        "How many lineups?",
        min_value=1, max_value=150,
        value=lineup_target(slug),
        key=f"build_n_{slug}",
        help="Defaults to what your declared contests call for — override it freely.",
    )
    if not persisted:
        st.info("Generate the slate analysis first — lineups are built from it.")
    elif st.button("🏗️ Build lineups", type="primary", key=f"build_lineups_{slug}"):
        with st.spinner(f"Building up to {n_target} lineup(s) from the analysis… (~3–15 min — leave this tab open)"):
            lresult = run_build_lineups(slug, contest_label, sport, n_target)
        if lresult["ok"]:
            cost = lresult.get("cost_usd")
            cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
            st.success(f"Lineups built in {lresult['duration_s']:.0f}s{cost_note}.")
            st.rerun()
        else:
            st.error(f"Couldn't build lineups: {lresult['error']}")

    # ----- (f2) Select lineups (pick from the uploaded lineup pool(s)) -----
    st.markdown("---")
    st.markdown("### Select lineups (from uploaded lineup pool)")
    st.caption(
        "Already generated lineups in SaberSim or a traditional optimizer? Upload the "
        "lineup-pool CSV(s) in the Sim Data tab (multiple files OK — proj/ceiling/50-50), "
        "then click below — Claude picks the best lineups FROM your pool that express this "
        "slate's edges (NOT just the top sim rows), each with a distinct thesis, and writes "
        "them as your portfolio. Sim columns optional. Takes ~3–15 minutes; uses your Claude "
        "subscription."
    )
    n_select = st.number_input(
        "How many lineups?",
        min_value=1, max_value=150,
        value=lineup_target(slug),
        key=f"select_n_{slug}",
        help="Defaults to what your declared contests call for — override it freely.",
    )
    sim_files = load_sim_files(slug)
    pool_has_ids = any("dk_id" in s["df"].columns for s in sources.values())
    if not persisted:
        st.info("Generate the slate analysis first — selections are judged against it.")
    elif not sim_files:
        st.info(
            "Upload your lineup-pool CSV(s) in the **Sim Data** tab — these are the lineups "
            "Claude picks from (SaberSim or any optimizer export; one or many files)."
        )
    elif not pool_has_ids:
        st.info(
            "The loaded projections carry no DK IDs, so the pool's rows can't be matched to "
            "players. Load a pool with an ID column (e.g. the SaberSim **projections** export) "
            "in the Projections tab — Ship It Nation has no IDs."
        )
    elif st.button("🎯 Select lineups", type="primary", key=f"select_lineups_{slug}"):
        with st.spinner(f"Selecting up to {n_select} lineup(s) from your pool… (~3–15 min — leave this tab open)"):
            sresult = run_select_lineups(slug, contest_label, sport, n_select)
        if sresult["ok"]:
            cost = sresult.get("cost_usd")
            cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
            st.success(f"Lineups selected in {sresult['duration_s']:.0f}s{cost_note}.")
            st.rerun()
        else:
            st.error(f"Couldn't select lineups: {sresult['error']}")

    lineups_blob = load_lineups(slug)
    if lineups_blob:
        with st.container(border=True):
            st.caption(f"Last updated: {lineups_blob['mtime']}")
            st.markdown(lineups_blob["markdown"])

        # ----- (g) Red team (adversarial pre-lock review) -----
        st.markdown("---")
        st.markdown("### Red team")
        st.caption(
            "Adversarial pre-lock review: tries to refute each lineup's thesis, audits the "
            "leverage math and the pre-flight checklist, and hunts shared failure modes. "
            "Verdicts are SHIP / FIX / KILL — findings only, nothing is rewritten. "
            "Takes ~1–3 minutes; uses your Claude subscription."
        )
        if st.button("🔪 Red team the lineups", key=f"red_team_{slug}"):
            with st.spinner("Red-teaming the portfolio — attacking each thesis… (~1–3 min)"):
                rt = run_red_team(slug, contest_label, sport)
            if rt["ok"]:
                cost = rt.get("cost_usd")
                cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
                st.success(f"Red-team review written in {rt['duration_s']:.0f}s{cost_note}.")
                st.rerun()
            else:
                st.error(f"Couldn't run the red team: {rt['error']}")

        rt_blob = load_red_team(slug)
        if rt_blob:
            if rt_blob["mtime"] < lineups_blob["mtime"]:
                st.warning("Lineups changed since this red-team review — re-run it.")
            with st.container(border=True):
                st.caption(f"Last updated: {rt_blob['mtime']}")
                st.markdown(rt_blob["markdown"])


# ===== Tab 5: Handbuild =====
with tab_hand:
    st.subheader(f"Handbuild — {contest_label}")
    st.caption(
        "Build a lineup by hand from your loaded projections. Live salary / projection / "
        "ownership totals as you pick. Saved lineups join the portfolio — covered by "
        "Red Team, archived on autopsy."
    )

    hb_pool = sessions.merge_same_vendor(sessions.load_sources(slug))
    if not hb_pool:
        st.info("Upload projections first — handbuilding picks from your loaded player pool.")
    else:
        hb_src = st.selectbox("Player pool source", list(hb_pool.keys()), key=f"hb_src_{slug}")
        hb_df = hb_pool[hb_src]["df"]
        if slug == "pga_rd4_sd":
            st.caption("⛳ Flat 6-golfer lineup — no captain, no multiplier.")

        spec = roster_spec(slug)
        n_slots = len(spec["slots"])

        # Slot labels: "P 1, P 2, C, 1B…" for MLB; "Golfer 1…6" for flat sports
        slot_labels = []
        seen_slots = {}
        for s in spec["slots"]:
            seen_slots[s] = seen_slots.get(s, 0) + 1
            count_of = spec["slots"].count(s)
            if spec["positional"]:
                slot_labels.append(f"{s} {seen_slots[s]}" if count_of > 1 else s)
            else:
                slot_labels.append(f"{spec['slot_label']} {seen_slots[s]}")

        # Pool view: pinned order — selection indices map into THIS df, so its
        # row order must never change between reruns.
        view = hb_df.copy()
        view["value"] = (view["proj_points"] / view["salary"] * 1000).round(2)
        view["sub10"] = view["ownership"] < 10
        view = view.sort_values(["salary", "name"], ascending=[False, True]).reset_index(drop=True)
        extras = {
            "golf": ["current_score", "tee_time", "ceiling", "make_cut_odds"],
            "mma": ["win_prob", "ko_pct", "sub_pct", "dec_pct"],
            "nascar": ["starting_position", "dominator_points", "fast_laps"],
            "mlb": [],
        }.get(sport, [])
        wanted = ["name", "position", "team", "opponent", "salary", "proj_points",
                  "ownership", "value", "sub10"] + extras
        cols = [c for c in wanted if c in view.columns]

        nonce_key = f"hb_nonce_{slug}"
        nonce = st.session_state.setdefault(nonce_key, 0)
        left, right = st.columns([3, 2], gap="medium")

        with left:
            event = st.dataframe(
                view[cols], hide_index=True, height=500,
                use_container_width=True,
                on_select="rerun", selection_mode="multi-row",
                key=f"hb_table_{slug}_{hb_src}_{nonce}",
                column_config={
                    "sub10": st.column_config.CheckboxColumn("<10% own"),
                    "ownership": st.column_config.NumberColumn("own%", format="%.1f"),
                    "proj_points": st.column_config.NumberColumn("proj", format="%.1f"),
                },
            )
            st.caption(
                "Click rows to add players · deselect to remove. Sorting a column "
                "clears your picks — use the table's 🔍 search instead."
            )

        sel_rows = sorted(event.selection.rows)
        ignored = sel_rows[n_slots:]
        sel_rows = sel_rows[:n_slots]
        selected = [
            {k: (None if pd.isna(v) else v) for k, v in view.iloc[i].items()}
            for i in sel_rows
        ]
        picked, assign_errors = assign_slots(selected, spec)

        with right:
            totals = lineup_totals(picked, spec["cap"])
            open_slots = n_slots - totals["n_players"]
            rem_per = totals["salary_left"] // open_slots if open_slots else None
            st.markdown(f"#### Lineup ({totals['n_players']}/{n_slots})")
            a1, a2, a3 = st.columns(3)
            a1.metric("Salary", f"${totals['salary_used']:,}")
            a2.metric("Remaining", f"${totals['salary_left']:,}")
            a3.metric("Rem/Player", f"${rem_per:,}" if rem_per is not None else "—")
            b1, b2, b3 = st.columns(3)
            b1.metric("Proj", totals["proj_total"])
            b2.metric("Own%", f"{totals['own_total']}%")
            b3.metric("Sub-10%", totals["n_sub10"])

            if ignored:
                names = ", ".join(view.iloc[i]["name"] for i in ignored)
                st.warning(
                    f"{len(ignored)} too many players selected — ignoring: {names}. "
                    "Deselect rows to fix."
                )

            # Slot list — picked is in spec slot order, so a pointer-walk lines
            # each player up with its label (handles P/P and OF×3 duplicates).
            ptr = 0
            lines = []
            for i, label in enumerate(slot_labels):
                if ptr < len(picked) and picked[ptr]["slot"] == spec["slots"][i]:
                    p = picked[ptr]
                    ptr += 1
                    own = f"{float(p['ownership']):.1f}%" if p.get("ownership") is not None else "—"
                    proj = f"{float(p['proj_points']):.1f}" if p.get("proj_points") is not None else "—"
                    lines.append(f"**{label}** · {p['name']} · ${int(p['salary']):,} · {proj} · {own}")
                else:
                    lines.append(f"**{label}** · *— empty —*")
            st.markdown("\n\n".join(lines))
            st.caption("To remove a player, deselect their row in the table.")

            for e in assign_errors:
                st.error(e)

            # Live structural errors only — don't nag about incomplete slots mid-build
            if picked:
                live_errors = [
                    e for e in validate_lineup(slug, picked, thesis="x", what_if="x")
                    if e.startswith("Over the") or e.startswith("House rule")
                    or "not eligible" in e or e.startswith("Duplicate")
                ]
                for e in live_errors:
                    st.error(e)

            # Analyze & save block — Claude writes the thesis/'What if?'; the
            # user never types them. Analyze first, then save with its output.
            st.markdown("##### Claude analyze & save")
            hb_name = st.text_input(
                "Lineup name (optional)", key=f"hb_name_{slug}",
                placeholder='e.g. "Braves Freight Train"',
            )
            hb_analysis = load_handbuild_analysis(slug)
            analysis_is_current = (
                hb_analysis is not None
                and sorted(hb_analysis["players"]) == sorted(p["name"] for p in picked)
            )
            # Table picks live in the browser session — a refresh, dropped
            # connection, or server restart clears them. The analyzed lineup
            # snapshot survives on disk, so saving still works from it.
            analysis_recoverable = (
                not picked and hb_analysis is not None and bool(hb_analysis["player_rows"])
            )
            if analysis_recoverable:
                st.info(
                    "Table picks were reset (page refresh / lost connection), but your "
                    "analyzed lineup is intact: "
                    f"{', '.join(hb_analysis['players'])}. 💾 Save lineup still saves it — "
                    "or re-click the players to keep editing."
                )

            c1, c2, c3 = st.columns([1, 1, 1])
            if c1.button("🧠 Claude analyze", type="primary", key=f"hb_analyze_{slug}"):
                errors = assign_errors + validate_lineup(slug, picked, thesis="x", what_if="x")
                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    with st.spinner("Claude is analyzing your handbuild… (~1–2 min)"):
                        res = run_handbuild_analysis(slug, contest_label, sport, picked, totals)
                    if res["ok"]:
                        st.rerun()
                    else:
                        st.error(res["error"])
            if c2.button("💾 Save lineup", key=f"hb_save_{slug}"):
                if analysis_is_current:
                    save_rows = picked
                elif analysis_recoverable:
                    save_rows = hb_analysis["player_rows"]
                else:
                    save_rows = None
                if save_rows is None:
                    st.error(
                        "Run 🧠 Claude analyze first — it writes the thesis and 'What if?' "
                        "this lineup is saved with."
                    )
                elif not (hb_analysis["thesis"] and hb_analysis["what_if"]):
                    st.error(
                        "Couldn't read a Thesis / 'What if?' from the analysis — "
                        "re-run 🧠 Claude analyze."
                    )
                else:
                    errors = assign_errors + validate_lineup(
                        slug, save_rows, hb_analysis["thesis"], hb_analysis["what_if"]
                    )
                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        n = append_handbuilt_lineup(
                            slug, contest_label, hb_name,
                            hb_analysis["thesis"], hb_analysis["what_if"], save_rows,
                        )
                        clear_handbuild_analysis(slug)
                        st.session_state[nonce_key] = nonce + 1
                        st.session_state.pop(f"hb_name_{slug}", None)
                        st.success(
                            f"Saved Lineup {n} (handbuilt) to data/lineups/{slug}.md — it shows "
                            "in the Analyze tab and is covered by Red Team."
                        )
                        st.rerun()
            if c3.button("Clear lineup", key=f"hb_clear_{slug}"):
                clear_handbuild_analysis(slug)
                st.session_state[nonce_key] = nonce + 1
                st.session_state.pop(f"hb_name_{slug}", None)
                st.rerun()

        # Claude's read on the current handbuild
        if hb_analysis:
            st.markdown("#### 🧠 Claude's read on this handbuild")
            if not analysis_is_current and not analysis_recoverable:
                st.warning(
                    "Lineup changed since this analysis — re-run 🧠 Claude analyze "
                    "before saving."
                )
            with st.container(border=True):
                st.caption(f"Last updated: {hb_analysis['mtime']}")
                st.markdown(hb_analysis["markdown"])

        # Current portfolio
        hb_lineups = load_lineups(slug)
        if hb_lineups:
            with st.expander("Current lineups on this slate", expanded=False):
                st.caption(f"data/lineups/{slug}.md · last updated {hb_lineups['mtime']}")
                st.markdown(hb_lineups["markdown"])

        # ----- Rank candidate lineups (construction coach) -----
        st.markdown("---")
        st.markdown("#### 📊 Rank candidate lineups")
        st.caption(
            "Built lineups elsewhere (SaberSim, etc.) and torn between them? Paste them as DK "
            "player IDs — one lineup per line, IDs separated by spaces or commas. Claude ranks "
            "them against your slate analysis and explains which construction is best and why. "
            "Nothing here is submitted — it's a second opinion on your own builds."
        )
        if "dk_id" not in hb_df.columns:
            st.info(
                "The selected player pool doesn't carry DK IDs, so pasted IDs can't be "
                "matched to players. Pick a source with an ID column in the **Player pool "
                "source** dropdown above — for MLB, select the **SaberSim** pool (Ship It "
                "Nation has no IDs). Golf and MMA pools always carry IDs."
            )
        else:
            rank_text = st.text_area(
                "Candidate lineups (DK player IDs)", key=f"rank_ids_{slug}", height=140,
                placeholder=("43247065 43247064 43247066 43247070 43247072 43247080\n"
                             "43247065, 43247064, 43247090, 43247095, 43247100, 43247110"),
            )
            resolved, _ = (resolve_id_lineups(rank_text, hb_df, slug)
                           if rank_text.strip() else ([], []))
            n_slots = len(roster_spec(slug)["slots"])
            for ln in resolved:
                t = ln["totals"]
                st.markdown(
                    f"**{ln['label']}** · {t['n_players']}/{n_slots} · ${t['salary_used']:,} · "
                    f"proj {t['proj_total']} · own {t['own_total']}%"
                )
                st.caption(", ".join(p["name"] for p in ln["players"]) or "—")
                for e in ln["errors"]:
                    st.caption(f"⚠️ {e}")
            valid_lineups = [ln for ln in resolved if not ln["errors"]]
            if resolved:
                if st.button(
                    f"📊 Rank these lineups ({len(valid_lineups)} valid)",
                    type="primary", key=f"rank_btn_{slug}", disabled=not valid_lineups,
                ):
                    with st.spinner("Claude is ranking your lineups… (~1–2 min)"):
                        res = run_rank_lineups(slug, contest_label, sport, valid_lineups)
                    if res["ok"]:
                        st.rerun()
                    else:
                        st.error(res["error"])

        ranking = load_lineup_ranking(slug)
        if ranking:
            with st.container(border=True):
                st.caption(f"Ranking · last updated {ranking['mtime']}")
                st.markdown(ranking["markdown"])

            # Save the keepers into the portfolio WITH the ranker's thesis, so
            # they're covered by red team like every other lineup. Reads the
            # ranked snapshot (not the live text box) so edits can't desync.
            ranked_snapshot = load_ranking_input(slug)
            theses = load_ranking_theses(slug)
            if ranked_snapshot:
                st.markdown("##### Save keepers to your portfolio")
                st.caption(
                    "Each saved lineup carries the thesis the ranker argued and is reviewed "
                    "by the Analyze tab's 🔪 Red team button, same as any other lineup."
                )
                for ln in ranked_snapshot:
                    label = ln.get("label", "")
                    th = theses.get(label, {})
                    thesis, what_if = th.get("thesis", ""), th.get("what_if", "")
                    cols = st.columns([6, 2])
                    names = ", ".join(p["name"] for p in ln["players"])
                    cols[0].markdown(f"**{label}** — {names}")
                    if cols[1].button(
                        "💾 Save", key=f"rank_save_{slug}_{label}",
                        disabled=not (thesis and what_if),
                        help=None if (thesis and what_if)
                        else "No thesis yet — re-run the ranking.",
                    ):
                        try:
                            num = append_handbuilt_lineup(
                                slug, contest_label, label, thesis, what_if,
                                ln["players"], tag="from uploaded pool",
                            )
                            st.success(
                                f"Saved Lineup {num} (from uploaded pool) to data/lineups/{slug}.md. "
                                "Run 🔪 Red team in the Analyze tab to review it."
                            )
                        except ValueError as e:
                            st.error(str(e))


# ===== Tab 6: Autopsy =====
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
        proj_df, proj_source = load_session_projections(slug)
        parsed_contests = []
        for i, dk_csv in enumerate(dk_csvs):
            try:
                parsed = parse_dk_results(dk_csv)
            except ValueError as e:
                st.error(f"{dk_csv.name}: {e}")
                continue
            lineups = parsed["lineups"]
            players = parsed["players"]
            analysis = analyze_contest(parsed, proj_df, sport)

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

                pm = analysis["proj_match"]
                if pm["available"]:
                    st.caption(
                        f"Projections joined from **{proj_source}** — matched "
                        f"{pm['matched']}/{pm['total']} players."
                    )
                    if pm["matched"] < pm["total"] * 0.7:
                        st.warning(
                            "Low projection match rate — the session may hold a "
                            "different slate's projections. Salary/proj columns "
                            "may be incomplete."
                        )
                else:
                    st.warning(
                        "No projections in the active session — salary, proj-vs-actual, "
                        "and stack-shape analysis unavailable for this autopsy."
                    )
                if analysis.get("ambiguous_players"):
                    st.warning(
                        "Ambiguous in DK standings (two different players share this "
                        "name, and DK provides no team to tell them apart) — excluded "
                        "from proj-vs-actual and vendor calibration: "
                        + ", ".join(analysis["ambiguous_players"])
                    )

                st.markdown("### Your entries")
                user_df = analysis["user_lineups_df"]
                if user_df.empty:
                    st.info("No entries matching RyvlesGaming30 / ryanjsieb30 found in this contest.")
                else:
                    show_cols = [c for c in ["rank", "points", "avg_own", "low_own_count",
                                             "salary_used", "proj_total", "dup_count",
                                             "stack_shape", "players"]
                                 if sport == "mlb" or c != "stack_shape"]
                    st.dataframe(user_df[show_cols], use_container_width=True)

                st.markdown("### Winners vs You")
                ws = analysis["winners_summary"]
                us = analysis["user_summary"]
                rows = [
                    ("Avg ownership %", "avg_own_mean"),
                    ("Sub-10% players / lineup", "low_own_count_mean"),
                    ("Salary used", "salary_used_mean"),
                ]
                comp = pd.DataFrame([
                    {
                        "metric": label,
                        f"top {ws.get('top_n')} winners": ws.get(key),
                        "you": us.get(key) if us else None,
                        "delta": (analysis["vs_user"] or {}).get(key.replace("_mean", "_delta")),
                    }
                    for label, key in rows
                ])
                st.dataframe(comp, use_container_width=True)
                dup_note = (
                    f"{ws.get('unique_pct')}% of top lineups are unique "
                    f"(max duplication {ws.get('dup_max')})"
                )
                if sport == "mlb" and ws.get("stack_shapes"):
                    shapes = ", ".join(f"{k}×{v}" for k, v in list(ws["stack_shapes"].items())[:5])
                    dup_note += f" · winning stack shapes: {shapes}"
                st.caption(dup_note)

                if analysis["overperformers"] or analysis["underperformers"]:
                    st.markdown("### Proj vs actual")
                    c1, c2 = st.columns(2)
                    c1.markdown("**Overperformed**")
                    c1.dataframe(pd.DataFrame(analysis["overperformers"]), use_container_width=True)
                    c2.markdown("**Underperformed**")
                    c2.dataframe(pd.DataFrame(analysis["underperformers"]), use_container_width=True)

                if analysis["slate_defining"]:
                    st.markdown("### Slate-defining plays")
                    st.caption("In ≥30% of top lineups at <20% field ownership.")
                    st.dataframe(pd.DataFrame(analysis["slate_defining"]), use_container_width=True)

                notes = st.text_area(
                    "Lessons / patterns to log (appended to autopsies.md)",
                    key=f"autopsy_notes_{slug}_{i}",
                    height=120,
                )

                # --- ROI inputs: link to a declared contest + winnings --- #
                st.markdown("##### Results for the ROI ledger")
                declared = load_contests(slug)
                options = [c["name"] for c in declared] + ["(not declared)"]
                # Default: declared contest whose field size is within ~10%
                # of this CSV's entry count.
                default_idx = len(options) - 1
                for j, c in enumerate(declared):
                    fs = c.get("field_size") or 0
                    if fs and abs(fs - len(lineups)) / fs <= 0.10:
                        default_idx = j
                        break
                picked_name = st.selectbox(
                    "Declared contest", options, index=default_idx,
                    key=f"autopsy_contest_{slug}_{i}",
                )
                picked = next((c for c in declared if c["name"] == picked_name), None)
                if picked is None:
                    fee = st.number_input(
                        "Entry fee ($)", min_value=0.0, step=0.25, value=0.0,
                        key=f"autopsy_fee_{slug}_{i}",
                    )
                    entry_fee = float(fee) if fee else None
                    my_entries = (analysis["user_summary"] or {}).get("entry_count", 0)
                    contest_type = None
                else:
                    entry_fee = picked.get("entry_fee")
                    my_entries = picked.get("my_entries", 0)
                    contest_type = picked.get("type")
                win_raw = st.text_input(
                    "Winnings this contest ($) — optional, ROI lives in your third-party tracker",
                    key=f"autopsy_win_{slug}_{i}",
                    placeholder="blank is fine — percentile + process are tracked here either way",
                )
                try:
                    winnings = float(win_raw) if win_raw.strip() else None
                except ValueError:
                    winnings = None
                    st.warning(f"Couldn't read '{win_raw}' as a dollar amount — logging winnings as not reported.")

            us = analysis["user_summary"] or {}
            parsed_contests.append({
                "name": dk_csv.name,
                "lineups": lineups,
                "parsed": parsed,
                "analysis": analysis,
                "notes": notes,
                "roi": {
                    "name": picked_name if picked else dk_csv.name,
                    "type": contest_type,
                    "source_file": dk_csv.name,
                    "field_size": len(lineups),
                    "my_entries": my_entries,
                    "entry_fee": entry_fee,
                    "winnings": winnings,
                    "best_rank": us.get("best_rank"),
                    "best_percentile": us.get("best_percentile"),
                },
            })

        if parsed_contests:
            st.divider()
            slate_label = st.text_input(
                "Slate label (names the archive folder)",
                key=f"autopsy_slate_label_{slug}",
                placeholder="e.g. Nashville Superspeedway / Memorial Tournament / UFC 320",
            )
            if st.button("📝 Log autopsy", type="primary"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                md_path = REPO_ROOT / "rules" / slug / "autopsies.md"
                md_path.parent.mkdir(parents=True, exist_ok=True)
                jsonl_path = REPO_ROOT / "rules" / slug / "autopsy_data.jsonl"
                # One autopsies.md section + one autopsy_data.jsonl row per
                # contest; source_file disambiguates same-type contests.
                records = []
                with md_path.open("a") as fmd, jsonl_path.open("a") as fjl:
                    for pc in parsed_contests:
                        lineups = pc["lineups"]
                        notes = pc["notes"]
                        record = build_autopsy_record(
                            ts=ts,
                            contest_label=contest_label,
                            slug=slug,
                            sport=sport,
                            source_file=pc["name"],
                            parsed=pc["parsed"],
                            analysis=pc["analysis"],
                            proj_source=proj_source,
                            notes=notes,
                        )
                        fmd.write(f"\n\n## {ts} — {contest_label} ({pc['name']})\n")
                        fmd.write(f"- Entries: {len(lineups):,}\n")
                        fmd.write(f"- Winning score: {lineups['Points'].max():.1f}\n")
                        fmd.write(f"- Cash line (top 20%): {lineups['Points'].quantile(0.80):.1f}\n")
                        fmd.write(record_md_summary(record) + "\n")
                        if notes.strip():
                            fmd.write(f"\n{notes.strip()}\n")
                        fjl.write(json.dumps(record) + "\n")
                        records.append(record)
                # Archive the slate BEFORE clearing — lineups, analysis, and
                # ROI survive in rules/<slug>/history/ + results.jsonl.
                hist_dir = history.archive_slate(
                    slug=slug,
                    sport=sport,
                    contest_label=contest_label,
                    slate_label=slate_label.strip(),
                    autopsy_records=records,
                    roi_contests=[pc["roi"] for pc in parsed_contests],
                    proj_source=proj_source,
                )
                # Vendor calibration: score every uploaded vendor against the
                # actuals from the largest-field contest. Never blocks the log.
                cal_note = ""
                try:
                    biggest = max(parsed_contests, key=lambda pc: len(pc["lineups"]))
                    cal_rows = score_vendors(slug, biggest["parsed"]["players"])
                    for row in cal_rows:
                        row.update({
                            "schema_version": 1,
                            "date": ts.split(" ")[0],
                            "slug": slug,
                            "sport": sport,
                            "slate_label": slate_label.strip() or contest_label,
                            "history_dir": str(hist_dir.relative_to(REPO_ROOT)),
                            "calibrated_against": {
                                "source_file": biggest["name"],
                                "field_size": len(biggest["lineups"]),
                            },
                        })
                    if cal_rows:
                        history.append_calibration(slug, cal_rows)
                        cal_note = f" Calibrated {len(cal_rows)} vendor(s) vs actuals."
                except Exception as e:
                    cal_note = f" (Vendor calibration skipped: {e})"
                # Clear all per-slate state — next slate starts fresh
                clear_persisted(slug)
                clear_lineups(slug)
                clear_red_team(slug)
                clear_handbuild_analysis(slug)
                clear_lineup_ranking(slug)
                clear_contests(slug)
                clear_sim(slug)
                clear_bundle(slug)
                clear_articles(slug)
                st.success(
                    f"Logged {len(parsed_contests)} contest(s) to rules/{slug}/autopsies.md "
                    "+ autopsy_data.jsonl, and archived the slate to "
                    f"`{hist_dir.relative_to(REPO_ROOT)}`.{cal_note} Cleared the slate "
                    "analysis, lineups, red-team review, contests, sim data, slate data "
                    "files, and bundle for next time. Now run the post-autopsy review below."
                )

    # ----- Post-autopsy review (the learning loop) ----- #
    latest_hist = history.latest_history_dir(slug)
    if latest_hist is not None:
        st.divider()
        st.markdown("### Post-autopsy review")
        review_path = latest_hist / "autopsy_review.md"
        st.caption(
            f"Latest archived slate: `{latest_hist.relative_to(REPO_ROOT)}`. "
            "The review grades the build process, updates the lesson ledger "
            f"(rules/{slug}/lessons.yaml) and venue notes, and proposes framework "
            "changes for your approval. Takes ~1–3 minutes."
        )
        btn_label = "🔄 Re-run post-autopsy review" if review_path.exists() else "🔬 Run post-autopsy review"
        if st.button(btn_label, type="primary", key=f"autopsy_review_{slug}"):
            with st.spinner("Reviewing the archived slate — grading process, updating lessons + venue notes… (~1–3 min)"):
                rresult = run_autopsy_review(slug, contest_label, sport)
            if rresult["ok"]:
                cost = rresult.get("cost_usd")
                cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
                st.success(f"Review written in {rresult['duration_s']:.0f}s{cost_note}.")
                st.rerun()
            else:
                st.error(f"Couldn't run the review: {rresult['error']}")

        if review_path.exists():
            review_md = review_path.read_text()
            with st.container(border=True):
                st.markdown(review_md)
            proposals = re.search(
                r"(?ms)^## Proposed codifications\s*\n(.*?)(?=^## |\Z)", review_md
            )
            has_proposals = bool(
                proposals and proposals.group(1).strip()
                and "none" not in proposals.group(1).strip().lower()[:40]
            )
            if has_proposals:
                st.warning(
                    "The review proposes framework/philosophy changes (above). "
                    "Approving applies them and updates lesson statuses."
                )
                if st.button("✅ Approve & apply proposals", key=f"apply_proposals_{slug}"):
                    with st.spinner("Applying the approved proposals…"):
                        aresult = run_apply_proposals(slug)
                    if aresult["ok"]:
                        st.success("Proposals applied to the framework/philosophy + lesson ledger.")
                        st.rerun()
                    else:
                        st.error(f"Couldn't apply the proposals: {aresult['error']}")

    # ----- ROI ledger ----- #
    results_rows = history.load_results(slug)
    if results_rows:
        st.divider()
        st.markdown("### Results ledger (all archived slates)")
        st.caption(
            "Best-percentile and process metrics are the scoreboard here — "
            "ROI lives in your third-party tracker, so winnings are usually blank."
        )
        ledger = pd.DataFrame([
            {
                "date": r.get("date"),
                "slate": r.get("slate_label"),
                "entries": r.get("entries_total"),
                "buy-in $": r.get("total_buy_in"),
                "winnings $": r.get("total_winnings"),
                "ROI %": r.get("roi_pct"),
                "best %ile": r.get("best_percentile"),
                "best rank": r.get("best_rank"),
            }
            for r in reversed(results_rows)
        ])
        st.dataframe(ledger, use_container_width=True)

    # ----- Vendor accuracy ----- #
    acc = history.vendor_accuracy(slug)
    if acc:
        st.divider()
        st.markdown("### Vendor accuracy (last 10 slates)")
        st.caption(
            "Projection / ownership mean absolute error vs DK actuals from the "
            "largest-field contest per slate. Under 3 slates = small sample, note only."
        )
        st.dataframe(pd.DataFrame(acc), use_container_width=True)

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
