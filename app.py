"""DFS Slate Analyzer — Streamlit app.

Multi-sport DFS slate analyzer for DraftKings.
Tabs: Strategy, Projections, Projections Diff, Articles, Autopsy.
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
from src.projections_diff import diff_table, flagged_disagreements
from src.autopsy import parse_dk_results
from src.strategy import load_strategy, load_track, load_shared
from src.slate_analysis import (
    snapshot, top_chalk, sport_signals,
    load_persisted, clear_persisted,
)
from src.lineups import load_lineups, clear_lineups
from src.contests import (
    CONTEST_TYPES as CONTEST_ENTRY_TYPES,
    load_contests, add_contest, remove_contest,
    clear_contests, portfolio_summary,
)
from src.sabersim import (
    parse_sabersim_lineups, save_pool, load_pool, load_summary,
    load_rules, clear_sabersim,
    parse_dk_player_ids, save_dk_ids, load_dk_ids, refresh_summary_with_dkids,
    dk_ids_from_projections, resolve_dk_id_map,
)


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

# Load active sport's strategy bundle (used by every tab)
strategy = load_strategy(slug)


# ---------- Tabs ---------- #
tab_proj, tab_diff, tab_articles, tab_contests, tab_sabersim, tab_analysis, tab_lineups, tab_strategy, tab_autopsy = st.tabs(
    ["Projections", "Projections Diff", "Articles", "Contests", "SaberSim Data", "Slate Analysis", "Lineups", "Strategy", "Autopsy"]
)


# ===== Tab 0: Strategy (analysis hub + reference docs) =====
with tab_strategy:
    st.subheader(f"Strategy for {contest_label}")
    st.caption(
        "Slate read, sport-specific callouts, recent autopsy lessons, and the active sport's "
        "philosophy / framework / autopsies. Everything for this contest type lives here."
    )

    # Recent-lessons banner
    if strategy["recent_lessons"]:
        with st.container(border=True):
            st.markdown(f"**🧠 Recent lessons ({len(strategy['recent_lessons'])} last autopsies):**")
            for lesson in strategy["recent_lessons"][:3]:
                ts = lesson.get("timestamp", "?")
                notes = (lesson.get("notes") or "").strip() or "_(no notes)_"
                st.markdown(f"- `{ts}` — {notes[:240]}")
    else:
        st.info("No prior autopsies for this sport yet — lessons will appear here after you log one.")

    # NASCAR: track selector inline
    if slug == "nascar":
        track_files = strategy["track_files"]
        if track_files:
            picked = st.selectbox("Track", track_files, key="nascar_track_pick")
            with st.expander(f"🏁 Track notes — {picked}", expanded=True):
                st.markdown(load_track(picked))
        else:
            st.warning(
                "No NASCAR track notes yet. Add one at `rules/nascar/tracks/<slug>.md` "
                "(use `charlotte_motor_speedway.md` as a template)."
            )

    # PGA RD4 SD hard rule
    if slug == "pga_rd4_sd":
        st.warning(
            "⛳ **RD4 Showdown**: flat 6-golfer lineup — NO captain, NO 1.5x multiplier."
        )

    # Slate read section (requires uploaded projections)
    st.markdown("---")
    st.markdown("## Slate read")
    sources = sessions.load_sources(slug)
    if not sources:
        st.info("Upload projections in the Projections tab to see chalk tiers, leverage, and anchor-equivalence checks.")
    else:
        primary_name = list(sources.keys())[0]
        df = sources[primary_name]["df"]
        st.caption(f"Reading from: **{primary_name}** ({sources[primary_name]['vendor']})")

        st.markdown("### Chalk tiers")
        st.dataframe(chalk_summary(df), use_container_width=True)

        st.markdown("### Leverage candidates")
        st.caption("Sorted by `upside / (ownership + 1)`. Higher = better GPP leverage.")
        st.dataframe(leverage_table(df), use_container_width=True)

        st.markdown("### Anchor-Equivalence pre-lock check")
        st.caption(
            "If 2+ chalk-tier anchors sit at similar projected ownership, "
            "at least one lineup MUST run the alternative — a 4-slate-validated structural leak."
        )
        with st.expander("📖 Read the rule"):
            st.markdown(load_shared("anchor_equivalence") or "_Missing._")
        groups = anchor_equivalence_check(df)
        if not groups:
            st.success("✅ No anchor-equivalence pairs detected.")
        else:
            for g in groups:
                st.warning(
                    f"**Equivalent anchors:** {', '.join(g['players'])} "
                    f"(own% {g['own_range'][0]:.1f}–{g['own_range'][1]:.1f}). {g['rule']}"
                )

    # Strategy reference docs (always visible)
    st.markdown("---")
    st.markdown("## Reference docs")
    sub_phil, sub_frame, sub_autopsies, sub_shared = st.tabs(
        ["Philosophy", "Framework", "Autopsies", "Shared rules"]
    )
    with sub_phil:
        st.markdown(strategy["philosophy"] or "_No philosophy.md for this sport yet._")
    with sub_frame:
        st.markdown(strategy["framework"] or "_No framework.md for this sport yet._")
    with sub_autopsies:
        st.markdown(strategy["autopsies"] or "_No autopsies.md for this sport yet._")
    with sub_shared:
        st.markdown("### Anchor-Equivalence Rule (cross-sport)")
        st.markdown(load_shared("anchor_equivalence") or "_Missing._")


# ===== Tab 1: Projections =====
with tab_proj:
    st.subheader(f"Step 1: Upload {contest_label} projections")
    st.caption(
        "Drop any vendor CSV — ETR, Ship It Nation, DailyFan, DK. "
        "Vendor is auto-detected. Upload multiple to enable the Projections Diff tab."
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
        primary_name = st.selectbox("Primary source for Landscape view", list(sources.keys()))
        df = sources[primary_name]["df"]

        warnings = warn_missing_for_sport(df, sport)
        for w in warnings:
            st.warning(w)

        st.dataframe(df, use_container_width=True, height=500)
    else:
        st.info("No projections uploaded yet.")


# ===== Tab 2: Projections Diff =====
with tab_diff:
    st.subheader("Vendor projection disagreement")
    sources = sessions.load_sources(slug)
    if len(sources) < 2:
        st.info("Upload 2 or more vendor sources to see disagreements.")
    else:
        metric = st.selectbox(
            "Metric to compare",
            ["proj_points", "ownership", "ceiling"],
            key=f"diff_metric_{slug}",
        )
        threshold = st.slider("Flag delta > (%)", 5, 50, 15, key=f"diff_thresh_{slug}")

        st.markdown(f"### Players where vendors disagree by ≥ {threshold}%")
        flagged = flagged_disagreements(sources, metric=metric, pct_threshold=threshold)
        if flagged.empty:
            st.success(f"No players flagged at this threshold for `{metric}`.")
        else:
            st.dataframe(flagged, use_container_width=True)

        st.markdown("### Full diff table")
        st.dataframe(diff_table(sources, metric=metric), use_container_width=True, height=500)


# ===== Tab 4: Articles =====
with tab_articles:
    st.subheader(f"Research for {contest_label}")
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

    files = sorted(articles_dir.glob("*"))
    if not files:
        st.info("No articles uploaded yet for this contest type.")
    else:
        st.markdown(f"**{len(files)} file(s):**")
        for f in files:
            cols = st.columns([5, 1])
            cols[0].write(f"📄 {f.name}")
            if cols[1].button("Delete", key=f"del_{f.name}"):
                f.unlink()
                st.rerun()


# ===== Tab 4.3: Contests =====
with tab_contests:
    st.subheader(f"Contests — {contest_label}")
    st.caption(
        "Declare which contests you're entering this slate. Claude reads this when writing "
        "the Slate Analysis and Lineups so the recommendations respect contest field sizes, "
        "entry counts, and ceiling targets."
    )

    contests_list = load_contests(slug)

    # Portfolio summary at top
    if contests_list:
        summary = portfolio_summary(slug)
        c1, c2, c3 = st.columns(3)
        c1.metric("Contests", summary["n_contests"])
        c2.metric("Total entries", summary["total_entries"])
        c3.metric("Unique lineups needed", summary["unique_lineups_needed"])
        st.caption(
            "'Unique lineups needed' = MAX my_entries across contests "
            "(the same lineup can be entered into multiple contests on DK)."
        )
        st.markdown("---")

    # Add contest form
    with st.expander("➕ Add a contest", expanded=not contests_list):
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

    # List of contests
    if contests_list:
        st.markdown("### Active contests")
        for c in contests_list:
            with st.container(border=True):
                top_cols = st.columns([6, 1])
                top_cols[0].markdown(f"**{c['name']}** — *{c['type']}*")
                if top_cols[1].button("✕ Delete", key=f"del_contest_{c['id']}"):
                    remove_contest(slug, c["id"])
                    st.rerun()
                detail_cols = st.columns(2)
                detail_cols[0].caption(f"Field size: **{c['field_size']:,}**")
                detail_cols[1].caption(f"Entries: **{c['my_entries']} / {c['max_entries']}**")
                if c.get("entry_fee") or c.get("prize_pool"):
                    extras = []
                    if c.get("entry_fee"):
                        extras.append(f"Entry ${c['entry_fee']}")
                    if c.get("prize_pool"):
                        extras.append(f"Prize ${c['prize_pool']:,}")
                    st.caption(" · ".join(extras))
    else:
        st.info("No contests added yet. Add one above so Claude knows the contest mix when writing analysis + lineups.")


# ===== Tab 4.4: SaberSim Data =====
with tab_sabersim:
    st.subheader(f"SaberSim Data — {contest_label}")
    st.caption(
        "Upload SaberSim's simmed lineup pool for this slate. Claude reads the pool's "
        "exposures + top lineups when writing the Slate Analysis, then writes the build "
        "rules (below) for you to enter back into SaberSim."
    )

    ss_upload = st.file_uploader("SaberSim lineup export (CSV)", type="csv", key=f"ss_upload_{slug}")
    if ss_upload is not None and st.button("Load SaberSim pool", type="primary", key=f"ss_load_{slug}"):
        try:
            ss_df, ss_meta = parse_sabersim_lineups(ss_upload)
            save_pool(slug, ss_df, ss_meta)
            st.success(f"Loaded {ss_meta['n_lineups']:,} lineups.")
            det = ss_meta.get("detected", {})
            st.caption("Detected columns: " + (", ".join(f"{k}→{v}" for k, v in det.items()) or "none"))
            if ss_meta.get("player_key") == "dk_id":
                st.caption(
                    f"Roster read as DK IDs from columns {ss_meta.get('roster_columns')} — "
                    "resolved to names via your projections/DK-id map (see match status below)."
                )
            if ss_meta.get("players_source") == "none":
                st.warning(
                    "Couldn't find a players/roster column — exposure won't compute. "
                    "Check the export format and tell me the column names."
                )
            if ss_meta.get("unmatched_columns"):
                st.caption("Ignored columns: " + ", ".join(ss_meta["unmatched_columns"]))
        except Exception as exc:
            st.error(f"Failed to parse SaberSim export: {exc}")

    with st.expander("DK player IDs (maps SaberSim names → DK IDs)", expanded=False):
        st.caption(
            "Upload your DraftKings DKEntries or DKSalaries CSV so SaberSim's name-only "
            "players resolve to DK player IDs (and any name/spelling drift gets flagged)."
        )
        _proj_ids = dk_ids_from_projections(slug)
        if _proj_ids is not None and not _proj_ids.empty:
            st.info(
                f"Your projections already include DK IDs for **{len(_proj_ids)}** players — "
                "no upload needed. Upload a DK file only to override."
            )
        _dk_existing = load_dk_ids(slug)
        if _dk_existing is not None and not _dk_existing.empty:
            st.caption(f"Uploaded DK file: **{len(_dk_existing)}** player IDs (overrides projections).")
        dk_ids_upload = st.file_uploader("DK player-ID CSV", type="csv", key=f"dk_ids_upload_{slug}")
        if dk_ids_upload is not None and st.button("Load DK player IDs", key=f"dk_ids_load_{slug}"):
            try:
                dk_df = parse_dk_player_ids(dk_ids_upload)
                if dk_df.empty:
                    st.warning("No players parsed — is this a DKEntries/DKSalaries CSV with a 'Name + ID' column?")
                else:
                    save_dk_ids(slug, dk_df)
                    refresh_summary_with_dkids(slug)  # re-annotate an already-loaded pool
                    st.success(f"Loaded {len(dk_df)} DK player IDs.")
            except Exception as exc:
                st.error(f"Failed to parse DK player-ID CSV: {exc}")

    pool = load_pool(slug)
    summary = load_summary(slug)
    if pool is not None and summary is not None:
        n = summary.get("n_lineups", len(pool))
        dist = summary.get("distributions", {})
        st.markdown("### Pool summary")
        mc = st.columns(4)
        mc[0].metric("Lineups", f"{n:,}")
        mc[1].metric("Median Proj", f"{dist.get('proj', {}).get('median', '—')}")
        mc[2].metric("Median Own Sum", f"{dist.get('own_sum', {}).get('median', '—')}")
        _best_top1 = dist.get("top1_pct", {}).get("max")
        mc[3].metric("Best Top 1%", f"{_best_top1}" if _best_top1 is not None else "—")

        _match = summary.get("dk_id_match")
        if _match and _match.get("total"):
            _src = summary.get("dk_id_source", "")
            _src_label = {"uploaded": " (from uploaded file)", "projections": " (from projections)"}.get(_src, "")
            st.caption(f"DK IDs{_src_label}: matched **{_match['matched']}/{_match['total']}** SaberSim players.")
            _unmatched = summary.get("unmatched_players", [])
            if _unmatched:
                st.warning("Unmatched names (drift vs DK — fix in SaberSim or DK file): " + ", ".join(_unmatched))
        elif resolve_dk_id_map(slug)[0] is None:
            st.caption("No DK IDs available — projections don't include them; upload a DK file above to resolve players.")

        exposure = summary.get("exposure", [])
        if exposure:
            st.markdown("### Player exposure")
            st.caption("How often each player appears across the simmed pool.")
            st.dataframe(pd.DataFrame(exposure), use_container_width=True, hide_index=True)

        top_lineups = summary.get("top_lineups", {})
        if top_lineups:
            st.markdown("### Top lineups")
            _labels = {"top1_pct": "Top 1%", "win_pct": "Win %", "sim_roi": "Sim ROI", "proj": "Proj"}
            _avail = [k for k in ["top1_pct", "win_pct", "sim_roi", "proj"] if k in top_lineups]
            _choice = st.selectbox(
                "Rank by", _avail, format_func=lambda k: _labels.get(k, k), key=f"ss_rank_{slug}",
            )
            st.dataframe(pd.DataFrame(top_lineups[_choice]), use_container_width=True, hide_index=True)
    else:
        st.info("No SaberSim pool loaded for this slate yet. Upload an export above.")

    # ---- Build rules to enter into SaberSim ----
    st.markdown("---")
    st.markdown("### Build rules for SaberSim")
    ss_rules = load_rules(slug)
    if ss_rules:
        st.caption(f"Last updated: {datetime.fromtimestamp(ss_rules['mtime']).strftime('%Y-%m-%d %H:%M')}")
        st.markdown(ss_rules["markdown"])
    else:
        st.info(
            "No build rules yet. Ask Claude to **\"write the slate analysis\"** — it will generate "
            "the SaberSim build rules (exposure caps/floors, must-plays, fades, ceiling/ownership "
            "targets) here for you to enter into SaberSim."
        )


# ===== Tab 4.5: Slate Analysis =====
with tab_analysis:
    st.subheader(f"Slate Analysis — {contest_label}")
    st.caption(
        "Claude's read (top) plus an auto-generated structured breakdown from the active session below."
    )

    # ----- Claude's persisted read -----
    persisted = load_persisted(slug)
    if persisted:
        with st.container(border=True):
            st.markdown("### 📝 Claude's read")
            st.caption(f"Last updated: {persisted['mtime']}")
            st.markdown(persisted["markdown"])
    else:
        st.info(
            "**No saved analysis yet.** In Claude Code, ask: *\"review the articles and write the slate analysis\"* — "
            "Claude will read your projections, uploaded articles, philosophy/framework/autopsies, and write a synthesis here."
        )

    st.markdown("---")
    st.markdown("## Auto-generated breakdown")

    sources = sessions.load_sources(slug)
    if not sources:
        st.info("Upload projections in the Projections tab first — the analysis pulls from your active session.")
    else:
        primary_name = list(sources.keys())[0]
        df = sources[primary_name]["df"]
        st.caption(f"Reading from: **{primary_name}** ({sources[primary_name]['vendor']})")

        # 1. Snapshot
        snap = snapshot(df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Players", f"{snap['n_players']}")
        c2.metric("Top-5 own concentration", f"{snap['top5_own_concentration_pct']}%")
        c3.metric("Chalk (≥15%)", f"{snap['n_chalk']}")
        c4.metric("Leverage pool (<5% own)", f"{snap['n_leverage_candidates']}")
        st.caption(
            f"Avg salary ${snap['avg_salary']:,.0f} · range ${snap['min_salary']:,}–${snap['max_salary']:,} · avg proj {snap['avg_proj']}"
        )

        # 2. Top chalk
        st.markdown("### Top chalk")
        chalk = top_chalk(df)
        if chalk.empty:
            st.info("No players above 15% ownership.")
        else:
            st.dataframe(chalk, use_container_width=True)

        # 3. Top leverage
        st.markdown("### Top leverage candidates")
        st.dataframe(leverage_table(df), use_container_width=True)

        # 4. Anchor-Equivalence
        st.markdown("### Anchor-Equivalence findings")
        groups = anchor_equivalence_check(df)
        if not groups:
            st.success("✅ No anchor-equivalence pairs at similar ownership.")
        else:
            for g in groups:
                st.warning(
                    f"**{', '.join(g['players'])}** (own% {g['own_range'][0]:.1f}–{g['own_range'][1]:.1f}) — "
                    f"{g['rule']}"
                )

        # 5. Sport-specific signals
        signals = sport_signals(df, sport)
        if signals:
            st.markdown(f"### {sport.upper()} signals")
            for key, table in signals.items():
                label = key.replace("_", " ").title()
                st.markdown(f"**{label}**")
                st.dataframe(table, use_container_width=True)

        # 6. Vendor disagreement
        if len(sources) >= 2:
            st.markdown("### Vendor disagreement (top 5 on proj_points)")
            flagged = flagged_disagreements(sources, metric="proj_points", pct_threshold=15.0)
            if flagged.empty:
                st.success("Vendors broadly agree at the 15% threshold.")
            else:
                st.dataframe(flagged.head(5), use_container_width=True)
                st.caption("See the Projections Diff tab to change the threshold or compare other metrics.")

        # 7. Recent autopsy lessons
        st.markdown("### Recent autopsy lessons")
        lessons = strategy["recent_lessons"][:3]
        if not lessons:
            st.info("No prior autopsies for this sport yet.")
        else:
            for lesson in lessons:
                ts = lesson.get("timestamp", "?")
                notes = (lesson.get("notes") or "").strip() or "_(no notes)_"
                st.markdown(f"- `{ts}` — {notes[:300]}")

        # 8. Framework reminders
        st.markdown("### Framework reminders")
        reminders = []
        if slug == "pga_rd4_sd":
            reminders.append("⛳ **RD4 Showdown**: flat 6-golfer lineup — NO captain, NO 1.5x multiplier.")
        if slug == "nascar":
            reminders.append("🏁 **NASCAR**: read `rules/nascar/tracks/<track>.md` before locking.")
        reminders.append("🔒 **Anchor-Equivalence**: if 2+ chalk-tier anchors at similar own, ≥1 lineup MUST run the alternative.")
        reminders.append("🎯 **GPP-only framing**: optimize for ceiling and leverage, never floor.")
        for r in reminders:
            st.markdown(f"- {r}")
        st.caption("→ See the **Strategy** tab for the full philosophy/framework/autopsies for this sport.")


# ===== Tab 4.7: Lineups (hand-built by Claude) =====
with tab_lineups:
    st.subheader(f"Lineups — {contest_label}")
    st.caption(
        "Hand-built by Claude based on the Slate Analysis read. Not an optimizer — these are judgment-driven lineups, "
        "each with an articulable thesis answering a different 'what if?' question."
    )

    lineups_blob = load_lineups(slug)
    if lineups_blob:
        with st.container(border=True):
            st.caption(f"Last updated: {lineups_blob['mtime']}")
            st.markdown(lineups_blob["markdown"])
    else:
        st.info(
            "**No lineups built yet.** In Claude Code, ask: *\"build lineups for the current slate\"* — "
            "Claude will read your Slate Analysis, projections, framework, and autopsies, then write a small "
            "curated set here. Each lineup gets a thesis + roster + 'what if?' scenario."
        )

    st.markdown("---")
    st.markdown("### Reference")
    st.caption(
        "**Salary cap: $50,000** · **Roster: 6 players** (PGA Classic, PGA RD4 SD, MMA, NASCAR). "
        "Lineups in a portfolio must answer DIFFERENT \"what if?\" questions. "
        "Anchor-Equivalence pre-lock check is mandatory — see the Strategy tab for the full rule."
    )


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
                clear_lineups(slug)
                clear_contests(slug)
                clear_sabersim(slug)
                st.success(
                    f"Logged {len(parsed_contests)} contest(s) to rules/{slug}/autopsies.md "
                    "+ autopsy_data.jsonl. Cleared Slate Analysis, Lineups, Contests, and "
                    "SaberSim data for next time."
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
