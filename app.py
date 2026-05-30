"""DFS Slate Analyzer — Streamlit app.

Multi-sport DFS slate analyzer for DraftKings.
Tabs: Strategy, Projections, Projections Diff, Articles, Autopsy.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from src import sessions
from src.projections import load_projections, warn_missing_for_sport
from src.vendors import detect_vendor, normalize_to_canonical
from src.landscape import chalk_summary, leverage_table, anchor_equivalence_check
from src.projections_diff import diff_table, flagged_disagreements
from src.autopsy import parse_dk_results
from src.strategy import load_strategy, load_track, load_shared
from src.slate_analysis import snapshot, top_chalk, sport_signals


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
tab_proj, tab_diff, tab_articles, tab_analysis, tab_strategy, tab_autopsy = st.tabs(
    ["Projections", "Projections Diff", "Articles", "Slate Analysis", "Strategy", "Autopsy"]
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
            raw = pd.read_csv(f)
            sig = detect_vendor(raw)
            if sig is None:
                st.error(f"❌ Couldn't detect vendor for {f.name}.")
                continue
            df = normalize_to_canonical(raw, sig)
            sessions.save_source(slug, f.name, df, sig.get("name", "unknown"))
            st.success(f"✅ {f.name} — detected as **{sig.get('name')}** ({len(df)} players)")

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


# ===== Tab 4.5: Slate Analysis =====
with tab_analysis:
    st.subheader(f"Slate Analysis — {contest_label}")
    st.caption(
        "Auto-generated breakdown of the active slate. Recomputes from the latest uploaded data every time you load this tab."
    )

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


# ===== Tab 5: Autopsy =====
with tab_autopsy:
    st.subheader(f"Post-slate autopsy — {contest_label}")

    dk_csv = st.file_uploader(
        "DraftKings contest-standings CSV",
        type="csv",
        key=f"dk_upload_{slug}",
    )

    if dk_csv is not None:
        try:
            parsed = parse_dk_results(dk_csv)
        except ValueError as e:
            st.error(str(e))
        else:
            lineups = parsed["lineups"]
            players = parsed["players"]

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

            st.divider()
            notes = st.text_area(
                "Lessons / patterns to log (appended to autopsies.md)",
                key=f"autopsy_notes_{slug}",
                height=120,
            )
            if st.button("📝 Log autopsy", type="primary"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                # Append to autopsies.md
                md_path = REPO_ROOT / "rules" / slug / "autopsies.md"
                md_path.parent.mkdir(parents=True, exist_ok=True)
                with md_path.open("a") as f:
                    f.write(f"\n\n## {ts} — {contest_label}\n")
                    f.write(f"- Entries: {len(lineups):,}\n")
                    f.write(f"- Winning score: {lineups['Points'].max():.1f}\n")
                    f.write(f"- Cash line (top 20%): {lineups['Points'].quantile(0.80):.1f}\n")
                    if notes.strip():
                        f.write(f"\n{notes.strip()}\n")
                # Append structured row to autopsy_data.jsonl
                jsonl_path = REPO_ROOT / "rules" / slug / "autopsy_data.jsonl"
                row = {
                    "timestamp": ts,
                    "contest_type": contest_label,
                    "entries": int(len(lineups)),
                    "winning_score": float(lineups["Points"].max()),
                    "cash_line_p80": float(lineups["Points"].quantile(0.80)),
                    "notes": notes.strip(),
                }
                with jsonl_path.open("a") as f:
                    f.write(json.dumps(row) + "\n")
                st.success(f"Logged to rules/{slug}/autopsies.md + autopsy_data.jsonl")

    st.divider()
    st.markdown("### Cross-slate patterns (autopsies.md)")
    autopsies_md = REPO_ROOT / "rules" / slug / "autopsies.md"
    if autopsies_md.exists():
        st.markdown(autopsies_md.read_text())
    else:
        st.info("No autopsies logged yet for this contest type.")
