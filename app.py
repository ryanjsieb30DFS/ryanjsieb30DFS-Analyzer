"""DFS Slate Analyzer — Streamlit app.

Sister to ~/Desktop/Repo/ryanjsieb30DFS sim. This tool analyzes; the sim builds.

Tabs: Projections, Landscape, Projections Diff, Articles, Autopsy.
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


REPO_ROOT = Path(__file__).parent

CONTEST_TYPES = {
    "PGA Classic": {"slug": "pga_classic", "sport": "golf"},
    "PGA RD4 Showdown": {"slug": "pga_rd4_sd", "sport": "golf"},
    "MMA": {"slug": "mma_se", "sport": "mma"},
    "NASCAR": {"slug": "nascar", "sport": "nascar"},
}


st.set_page_config(page_title="DFS Slate Analyzer", layout="wide")
st.title("DFS Slate Analyzer")
st.caption("Sister tool to the sim — this one reads the slate, doesn't build lineups.")

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

# ---------- Tabs ---------- #
tab_proj, tab_landscape, tab_diff, tab_articles, tab_autopsy = st.tabs(
    ["Projections", "Landscape", "Projections Diff", "Articles", "Autopsy"]
)


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


# ===== Tab 2: Landscape =====
with tab_landscape:
    st.subheader("Slate landscape")
    sources = sessions.load_sources(slug)
    if not sources:
        st.info("Upload projections in the Projections tab first.")
    else:
        primary_name = list(sources.keys())[0]
        df = sources[primary_name]["df"]
        st.caption(f"Reading from: **{primary_name}** ({sources[primary_name]['vendor']})")

        if slug == "nascar":
            st.warning(
                "🏁 **NASCAR**: read the track-specific notes at `rules/nascar/tracks/<track>.md` "
                "before locking. If the track isn't documented yet, add it."
            )
        if slug == "pga_rd4_sd":
            st.warning(
                "⛳ **RD4 Showdown**: flat 6-golfer lineup — NO captain, NO 1.5x multiplier."
            )

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
        groups = anchor_equivalence_check(df)
        if not groups:
            st.success("✅ No anchor-equivalence pairs detected.")
        else:
            for g in groups:
                st.warning(
                    f"**Equivalent anchors:** {', '.join(g['players'])} "
                    f"(own% {g['own_range'][0]:.1f}–{g['own_range'][1]:.1f}). {g['rule']}"
                )


# ===== Tab 3: Projections Diff =====
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
            cols = st.columns([5, 1, 1])
            cols[0].write(f"📄 {f.name}")
            if f.suffix.lower() in (".txt", ".md"):
                with cols[1].expander("View"):
                    pass  # placeholder
            if cols[2].button("Delete", key=f"del_{f.name}"):
                f.unlink()
                st.rerun()


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
    st.markdown("### Cross-slate patterns")
    autopsies_md = REPO_ROOT / "rules" / slug / "autopsies.md"
    if autopsies_md.exists():
        st.markdown(autopsies_md.read_text())
    else:
        st.info("No autopsies logged yet for this contest type.")
