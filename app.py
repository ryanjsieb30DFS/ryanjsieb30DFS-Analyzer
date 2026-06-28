"""DFS Slate Analyzer — Streamlit app.

Article-driven, multi-sport DFS slate-strategy tool for DraftKings.
Flow: Slate Data → Slate Strategy → Autopsy.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from src.autopsy import (
    parse_dk_results, analyze_contest,
    build_autopsy_record, record_md_summary,
)
from src.slate_analysis import load_persisted, clear_persisted
from src.contests import (
    CONTEST_TYPES as CONTEST_ENTRY_TYPES,
    load_contests, add_contest, remove_contest,
    clear_contests, portfolio_summary,
)
from src.contest_templates import load_templates, save_template, remove_template
from src.bundle import clear_bundle
from src.analysis_runner import (
    run_analysis, run_autopsy_review, run_apply_proposals, run_player_pool,
)
from src import history, sessions, landscape, player_pool
from src.projections import load_projections, warn_missing_for_sport
from src.projections_diff import flagged_disagreements


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


def clear_articles(slug: str) -> list[str]:
    """Delete the slate's uploaded Slate Data files (articles/<slug>/).

    Best-effort: a locked/undeletable file is skipped (its name returned) rather
    than crashing the clear mid-way and leaving the slate in an inconsistent state.
    """
    articles_dir = REPO_ROOT / "articles" / slug
    failed: list[str] = []
    if articles_dir.exists():
        for f in articles_dir.glob("*"):
            if f.is_file():
                try:
                    f.unlink()
                except OSError:
                    failed.append(f.name)
    return failed


st.set_page_config(page_title="DFS Slate Analyzer", layout="wide")
st.title("DFS Slate Analyzer")
st.caption("Article-driven DFS slate-strategy tool for DraftKings.")

# ---------- Sidebar ---------- #
with st.sidebar:
    contest_label = st.selectbox("Contest type", list(CONTEST_TYPES.keys()))
    cfg = CONTEST_TYPES[contest_label]
    slug = cfg["slug"]
    sport = cfg["sport"]

    st.divider()
    if st.button("Clear this sport's slate", type="secondary"):
        clear_articles(slug)
        clear_persisted(slug)
        player_pool.clear_pool(slug)
        clear_contests(slug)
        clear_bundle(slug)
        sessions.clear(slug)
        st.rerun()


# ---------- Tabs ---------- #
tab_proj, tab_slate, tab_strategy, tab_autopsy = st.tabs(
    ["Projections", "Slate Data", "Slate Strategy", "Autopsy"]
)


# ===== Tab: Projections =====
with tab_proj:
    st.subheader(f"Projections — {contest_label}")
    st.caption(
        "Drop any vendor projection CSV — ETR, Ship It Nation, DailyFan, DK. "
        "Vendor is auto-detected. Stored per slate, viewable here, AND folded into the "
        "bundle so the slate strategy reads them alongside your articles. (The autopsy "
        "still works from DK standings alone.)"
    )

    uploaded = st.file_uploader(
        "Vendor projection CSV",
        type="csv",
        accept_multiple_files=True,
        key=f"proj_upload_{slug}",
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
                    f"📊 {f.name} is {df.attrs.get('vendor')} data, not player "
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
            _conf = df.attrs.get("vendor_confidence") or {}
            if _conf.get("ambiguous"):
                st.warning(
                    f"⚠️ Ambiguous match — {f.name} also fits "
                    f"{', '.join(_conf['matched'][1:])}. Verify the detected vendor is right."
                )
            for _vn, _missing in _conf.get("near_misses", []):
                if _vn != vendor_name:
                    st.caption(
                        f"↳ Near-miss: looks almost like **{_vn}** but missing "
                        f"`{', '.join(_missing)}` — a renamed header? Update src/vendors.py if so."
                    )

    sources = sessions.load_sources(slug)
    if sources:
        st.divider()
        st.markdown(f"**Loaded sources ({len(sources)}):**")
        for name, blob in sources.items():
            cols = st.columns([4, 2, 1])
            cols[0].write(f"📄 {name}")
            cols[1].write(f"`{blob['vendor']}` · {len(blob['df'])} players")
            if cols[2].button("Drop", key=f"proj_drop_{name}"):
                sessions.drop_source(slug, name)
                st.rerun()

        st.divider()
        pool = sessions.merge_same_vendor(sources)
        primary_name = st.selectbox("View source", list(pool.keys()))
        df = pool[primary_name]["df"]
        for w in warn_missing_for_sport(df, sport):
            st.warning(w)
        st.dataframe(df, use_container_width=True, height=500)

        # ---------- Breakdown — surface non-obvious edges ---------- #
        st.divider()
        st.markdown("### 🔍 Breakdown — what you'd miss")
        st.caption(
            f"Computed from **{primary_name}** ({pool[primary_name]['vendor']}). A reference "
            "view of this one source — the slate strategy reads all loaded vendors via the bundle."
        )

        # Edges to notice (synthesized headline flags first)
        st.markdown("#### Edges to notice")
        for bullet in landscape.breakdown_flags(df):
            st.markdown(f"- {bullet}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Underowned vs ceiling (field blind spots)")
            mis = landscape.mispricing_table(df, top_n=10)
            st.dataframe(mis["underowned"], use_container_width=True, hide_index=True)
        with c2:
            st.markdown("#### Overowned vs ceiling (fade candidates)")
            st.dataframe(mis["overowned"], use_container_width=True, hide_index=True)

        st.markdown("#### Leverage board (ceiling vs ownership)")
        st.dataframe(landscape.leverage_table(df, top_n=15), use_container_width=True, hide_index=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("#### Slate shape — chalk tiers")
            st.dataframe(landscape.chalk_summary(df), use_container_width=True, hide_index=True)
        with c4:
            st.markdown("#### Value leaders by salary tier")
            st.dataframe(landscape.value_by_tier(df), use_container_width=True, hide_index=True)

        waves = landscape.tee_wave_split(df)
        st.markdown("#### Tee-wave split (AM / PM)")
        if waves.empty:
            st.caption("No `tee_time` column — wave split unavailable for this vendor file.")
        else:
            st.dataframe(waves, use_container_width=True, hide_index=True)

        vol = landscape.volatility_table(df, top_n=10)
        c5, c6 = st.columns(2)
        with c5:
            st.markdown("#### Boom (highest ceiling-volatility)")
            st.dataframe(vol["boom"], use_container_width=True, hide_index=True)
        with c6:
            st.markdown("#### Fragile chalk (owned, capped ceiling)")
            st.dataframe(vol["fragile_chalk"], use_container_width=True, hide_index=True)

        # Cross-vendor disagreement — only when 2+ sources loaded
        if len(sources) >= 2:
            st.markdown("#### Cross-vendor disagreement (≥15% spread)")
            disagree = flagged_disagreements(sources, metric="proj_points", pct_threshold=15.0)
            if disagree.empty:
                st.caption("No players with ≥15% projection spread across loaded vendors.")
            else:
                st.dataframe(disagree, use_container_width=True, hide_index=True)
    else:
        st.info("No projections uploaded yet.")


# ===== Tab 1: Slate Data =====
with tab_slate:
    st.subheader(f"Slate Data — {contest_label}")
    st.caption(
        "Upload the slate's articles, notes, data files, photos, and screenshots. "
        "Claude reads these when writing the slate strategy."
    )
    articles_dir = REPO_ROOT / "articles" / slug
    articles_dir.mkdir(parents=True, exist_ok=True)

    uploaded_pdfs = st.file_uploader(
        "Upload article PDFs / notes / data files",
        type=["pdf", "txt", "md", "csv"],
        accept_multiple_files=True,
        key=f"articles_{slug}",
    )
    if uploaded_pdfs:
        for f in uploaded_pdfs:
            data = f.read()
            ts = datetime.now().strftime("%Y-%m-%d")
            dest = articles_dir / f"{ts}__{f.name}"
            try:
                dest.write_bytes(data)
                st.success(f"Saved {dest.name}")
            except OSError as e:
                st.error(f"Couldn't save {f.name}: {e}")

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
            try:
                dest.write_bytes(f.read())
                st.success(f"Saved {dest.name}")
            except OSError as e:
                st.error(f"Couldn't save {f.name}: {e}")

    files = sorted(articles_dir.glob("*"))
    if not files:
        st.info("No slate data uploaded yet for this contest type.")
    else:
        st.markdown(f"**{len(files)} file(s):**")
        for f in files:
            cols = st.columns([5, 1])
            suffix = f.suffix.lower()
            icon = "🖼️" if suffix in (".png", ".jpg", ".jpeg") else ("📊" if suffix == ".csv" else "📄")
            cols[0].write(f"{icon} {f.name}")
            if cols[1].button("Delete", key=f"del_{slug}_{f.name}"):
                try:
                    f.unlink()
                except OSError as e:
                    st.error(f"Couldn't delete {f.name}: {e}")
                st.rerun()


# ===== Tab 2: Slate Strategy =====
with tab_strategy:
    st.subheader(f"Slate Strategy — {contest_label}")
    st.caption(
        "Declare your contests, then generate the slate strategy. Claude reads everything "
        "you uploaded — your articles + every loaded vendor projection + strategy docs — and "
        "writes the strategy below."
    )

    # ----- (a) Contest config (folded in) -----
    contests_list = load_contests(slug)
    with st.expander("Contests", expanded=not contests_list):
        st.caption(
            "Declare which contests you're entering. Field size frames how contrarian "
            "the read should be."
        )
        if contests_list:
            csum = portfolio_summary(slug)
            c1, c2 = st.columns(2)
            c1.metric("Contests", csum["n_contests"])
            c2.metric("Total entries", csum["total_entries"])

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

    # ----- (b) Generate the slate strategy + player pool (one click) -----
    st.markdown("---")
    st.markdown("### Generate slate strategy + player pool")
    st.caption(
        "Runs Claude on everything you uploaded — articles + every loaded vendor projection + "
        "strategy docs — and writes both the slate strategy and the ranked player pool below. "
        "No need to leave the app. Takes ~2–6 minutes. Uses your Claude subscription."
    )
    article_files = sorted((REPO_ROOT / "articles" / slug).glob("*"))
    if not article_files:
        st.info("Upload articles in the **Slate Data** tab first — the strategy reads from them.")
    elif st.button("✨ Generate slate strategy + player pool", type="primary", key=f"strategy_{slug}"):
        with st.spinner("Building the slate strategy — reading your articles, projections, and strategy docs… (~1–3 min)"):
            result = run_analysis(slug, contest_label, sport)
        if not result["ok"]:
            st.error(f"Couldn't generate the slate strategy: {result['error']}")
        else:
            cost = result.get("cost_usd") or 0.0
            msg = f"Slate strategy written in {result['duration_s']:.0f}s."
            # Chain the player pool — it reads the strategy just written for fades.
            if sessions.load_sources(slug):
                with st.spinner("Building the player pool — ranking your players from the documents… (~1–3 min)"):
                    pool_result = run_player_pool(slug, contest_label, sport)
                if pool_result["ok"]:
                    cost += pool_result.get("cost_usd") or 0.0
                    msg += f" Player pool written in {pool_result['duration_s']:.0f}s."
                else:
                    msg += f" (Player pool step failed: {pool_result['error']})"
            else:
                msg += " (No projections loaded — skipped the player pool.)"
            cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
            st.success(msg + cost_note)
            st.rerun()

    # ----- (c) The written slate strategy -----
    st.markdown("---")
    st.markdown("## Slate strategy")
    persisted = load_persisted(slug)
    if persisted:
        with st.container(border=True):
            st.caption(f"Last updated: {persisted['mtime']}")
            st.markdown(persisted["markdown"])
    else:
        st.info("**No saved strategy yet.** Click **Generate slate strategy** above and it appears here.")

    # ----- (d) Player pool — ranked board, built with the strategy -----
    st.markdown("---")
    st.markdown("## Player pool")
    st.caption(
        "Every player you could roster, ranked for GPP with a short write-up each — built "
        "automatically with the slate strategy above. Membership = the projections you loaded "
        "(Projections tab) minus the fades your strategy names; ranking + write-ups from your documents."
    )
    saved_pool = player_pool.load_pool(slug)
    if saved_pool:
        with st.container(border=True):
            st.caption(f"Last updated: {saved_pool['mtime']}")
            st.markdown(saved_pool["markdown"])
    elif not sessions.load_sources(slug):
        st.info("Upload projections in the **Projections** tab, then generate the slate strategy — the pool is built with it.")
    else:
        st.info("Generate the **slate strategy** above — the player pool is built along with it.")


# ===== Tab 3: Autopsy =====
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
        # CSV is reported but doesn't block the others. No projections in this
        # tool — the autopsy works from DK standings alone.
        proj_df, proj_source = None, None
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

                if analysis.get("ambiguous_players"):
                    st.warning(
                        "Ambiguous in DK standings (two different players share this "
                        "name, and DK provides no team to tell them apart) — excluded "
                        "from the structural analysis: "
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

                if analysis["slate_defining"]:
                    st.markdown("### Slate-defining plays")
                    st.caption("In ≥30% of top lineups at <20% field ownership.")
                    st.dataframe(pd.DataFrame(analysis["slate_defining"]), use_container_width=True)

                # Self-grade: did OUR entered lineups capture the leverage/edges?
                if analysis.get("user_lineups_df") is not None and not analysis["user_lineups_df"].empty:
                    from src import accuracy
                    from src.autopsy import _lineup_records
                    _field = len(parsed["lineups"])
                    _grade_rec = {
                        "user_lineups": _lineup_records(analysis["user_lineups_df"], _field),
                        "slate_defining_plays": analysis["slate_defining"],
                        "top_overperformers": analysis["overperformers"],
                        "top_underperformers": analysis["underperformers"],
                    }
                    with st.container(border=True):
                        st.markdown(accuracy.slate_accuracy_md([_grade_rec]))
                        st.caption("Computed in Python from this contest's actuals — trended into "
                                   "the next slate's bundle when you log the autopsy.")

                # Shark gap — structural us-vs-sharks fingerprint for THIS field.
                try:
                    from src import shark_gap as _sg
                    _gap = _sg.gap_for_slug(slug, parsed)
                    with st.container(border=True):
                        st.markdown(_sg.gap_md(_gap))
                        if not _gap.get("sport"):
                            st.caption("No sport→shark mapping for this slug yet — add it in "
                                       "rules/shared/shark_handles.yaml.")
                        elif not _gap.get("sharks_in_field"):
                            st.caption(f"No tracked {_gap.get('sport')} sharks entered this contest. "
                                       "Add the heavy-MME top finishers to shark_handles.yaml to "
                                       "build the watchlist.")
                except Exception:  # noqa: BLE001 — panel is best-effort
                    pass

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
                # Structural shark-gap on the largest-field contest (where the
                # sharks are most likely to be entered). Never blocks the log.
                sgap = None
                try:
                    from src import shark_gap as _shark_gap
                    _biggest = max(parsed_contests, key=lambda pc: len(pc["lineups"]))
                    sgap = _shark_gap.gap_for_slug(slug, _biggest["parsed"])
                except Exception:  # noqa: BLE001
                    sgap = None
                # Archive the slate BEFORE clearing — analysis and ROI survive
                # in rules/<slug>/history/ + results.jsonl.
                hist_dir = history.archive_slate(
                    slug=slug,
                    sport=sport,
                    contest_label=contest_label,
                    slate_label=slate_label.strip(),
                    autopsy_records=records,
                    roi_contests=[pc["roi"] for pc in parsed_contests],
                    proj_source=proj_source,
                    shark_gap=sgap,
                )
                # Clear all per-slate state — next slate starts fresh
                clear_persisted(slug)
                player_pool.clear_pool(slug)
                clear_contests(slug)
                clear_bundle(slug)
                clear_articles(slug)
                sessions.clear(slug)
                st.success(
                    f"Logged {len(parsed_contests)} contest(s) to rules/{slug}/autopsies.md "
                    "+ autopsy_data.jsonl, and archived the slate to "
                    f"`{hist_dir.relative_to(REPO_ROOT)}`. Cleared the slate strategy, "
                    "contests, slate data files, projections, and bundle for next time. Now run the "
                    "post-autopsy review below."
                )

    # ----- Post-autopsy review (the learning loop) ----- #
    latest_hist = history.latest_history_dir(slug)
    if latest_hist is not None:
        st.divider()
        st.markdown("### Post-autopsy review")
        review_path = latest_hist / "autopsy_review.md"
        st.caption(
            f"Latest archived slate: `{latest_hist.relative_to(REPO_ROOT)}`. "
            "The review grades the process, updates the lesson ledger "
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
