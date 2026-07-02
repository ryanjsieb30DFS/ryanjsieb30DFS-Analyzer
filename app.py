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
    run_ledger_review, run_apply_ledger_proposals, run_sim_review,
)
from src import (
    history, sessions, landscape, player_pool, contest_selection, ledger_hygiene,
    sim_data, sim_sessions, dk_ids, metrics_registry, metric_tracker,
)
from datetime import datetime as _dt
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


def _file_mtime(p: Path | None) -> float:
    return p.stat().st_mtime if p and p.exists() else 0.0


@st.cache_data(show_spinner=False)
def _cached_sources(slug: str, mtime: float) -> dict:
    # `mtime` must NOT start with an underscore — st.cache_data excludes
    # underscore-prefixed args from the key, which would defeat invalidation.
    return sessions.load_sources(slug)


def cached_sources(slug: str) -> dict:
    """sessions.load_sources, cached on the session file's mtime (self-invalidating
    when a source is saved/dropped/cleared, since those rewrite or delete the file)."""
    return _cached_sources(slug, _file_mtime(REPO_ROOT / "data" / "sessions" / f"{slug}.json"))


@st.cache_data(show_spinner=False)
def _cached_sim_analytics(slug: str, pool_mtime: float, dkmap_mtime: float, src_mtime: float) -> dict:
    """Load the persisted 5,000-lineup sim pool and compute every exposure/combo ONCE,
    cached on the underlying file mtimes. Without this the whole crunch reran on every
    interaction of every tab (Streamlit executes all tabs' bodies on each rerun).
    The mtime args must NOT be underscore-prefixed — st.cache_data drops those from
    the cache key, which would make the cache never invalidate on a new upload."""
    pool = sim_data.load_sim_pool(str(sim_sessions.pool_path(slug)))
    if pool.get("n", 0) == 0:
        return {"pool": pool}
    dkmap_path = sim_sessions.dkmap_path(slug)
    uploaded_map = dk_ids.parse_id_to_name(str(dkmap_path)) if dkmap_path else None
    id_to_name = dk_ids.resolve_id_to_name(slug, uploaded_map)
    proj = player_pool.build_pool(sessions.load_sources(slug))
    exp = sim_data.player_exposure(pool, id_to_name, proj if not proj.empty else None)
    return {
        "pool": pool,
        "id_to_name": id_to_name,
        "exp": exp,
        "gb": sim_data.good_bad_plays(exp),
        "combos": sim_data.chalky_combinations(pool, id_to_name),
    }


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
    # --- Slate readiness at a glance (no tab-hopping to see what's loaded) ---
    _arts = REPO_ROOT / "articles" / slug
    _n_articles = len([f for f in _arts.glob("*") if f.is_file()]) if _arts.exists() else 0
    _n_src = len(cached_sources(slug))
    _n_contests = len(load_contests(slug))
    _has_strategy = bool(load_persisted(slug))
    _has_pool = sim_sessions.pool_path(slug) is not None
    st.markdown("**Slate readiness**")
    st.caption(
        f"Articles: {_n_articles}  ·  Projections: {_n_src}  ·  Contests: {_n_contests}\n\n"
        f"Strategy: {'✅' if _has_strategy else '—'}  ·  Sim pool: {'✅' if _has_pool else '—'}"
    )

    st.divider()
    if st.session_state.get(f"confirm_clear_{slug}"):
        st.warning("Deletes this slate's articles, projections, strategy, pool, and contests — not recoverable.")
        cc1, cc2 = st.columns(2)
        if cc1.button("Confirm clear", type="primary", key=f"do_clear_{slug}"):
            clear_articles(slug)
            clear_persisted(slug)
            player_pool.clear_pool(slug)
            clear_contests(slug)
            clear_bundle(slug)
            sessions.clear(slug)
            sim_sessions.clear(slug)
            st.session_state[f"confirm_clear_{slug}"] = False
            st.rerun()
        if cc2.button("Cancel", key=f"cancel_clear_{slug}"):
            st.session_state[f"confirm_clear_{slug}"] = False
            st.rerun()
    elif st.button("Clear this sport's slate", type="secondary"):
        st.session_state[f"confirm_clear_{slug}"] = True
        st.rerun()


# ---------- Tabs ---------- #
tab_proj, tab_slate, tab_strategy, tab_sim, tab_autopsy, tab_postsim, tab_trends = st.tabs(
    ["Projections", "Slate Data", "Slate Strategy", "Sim Data", "Autopsy", "Post-Contest Sim Data", "Trends"]
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

    sources = cached_sources(slug)
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

        # ---------- Breakdown — surface non-obvious edges (collapsed by default) ---------- #
        st.divider()
        with st.expander("🔍 Breakdown — what you'd miss", expanded=False):
            st.caption(
                f"Computed from **{primary_name}** ({pool[primary_name]['vendor']}). A reference "
                "view of this one source — the slate strategy reads all loaded vendors via the bundle."
            )

            # Edges to notice (synthesized headline flags first)
            st.markdown("#### Edges to notice")
            for bullet in landscape.breakdown_flags(df):
                st.markdown(f"- {bullet}")

            # Ceiling-based panels only when the vendor ships a REAL ceiling (golf/MLB).
            # NASCAR / names-only vendors ship none — we never fabricate one.
            real_ceil = landscape.has_real_ceiling(df)

            if real_ceil:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Underowned vs ceiling (field blind spots)")
                    mis = landscape.mispricing_table(df, top_n=10)
                    st.dataframe(mis["underowned"], use_container_width=True, hide_index=True)
                with c2:
                    st.markdown("#### Overowned vs ceiling (fade candidates)")
                    st.dataframe(mis["overowned"], use_container_width=True, hide_index=True)

            _lev_title = "Leverage board (ceiling vs ownership)" if real_ceil else "Leverage board (proj vs ownership)"
            st.markdown(f"#### {_lev_title}")
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

            if real_ceil:
                vol = landscape.volatility_table(df, top_n=10)
                c5, c6 = st.columns(2)
                with c5:
                    st.markdown("#### Boom (highest ceiling-volatility)")
                    st.dataframe(vol["boom"], use_container_width=True, hide_index=True)
                with c6:
                    st.markdown("#### Fragile chalk (owned, capped ceiling)")
                    st.dataframe(vol["fragile_chalk"], use_container_width=True, hide_index=True)
            else:
                st.caption(
                    "ℹ️ Ceiling-based views (boom/bust, mispricing-vs-ceiling) need a vendor that ships a "
                    "real ceiling — hidden here because this slate's projections are projection-only "
                    "(no fabricated ceiling)."
                )

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
                continue
            # Misfile guard: a vendor projections CSV belongs in the Projections tab.
            if f.name.lower().endswith(".csv"):
                try:
                    import io as _io
                    _probe = load_projections(_io.BytesIO(data))
                    if _probe.attrs.get("kind") is None and _probe.attrs.get("vendor"):
                        st.info(
                            f"ℹ️ {f.name} looks like **{_probe.attrs['vendor']}** projections — "
                            "if so, upload it in the **Projections** tab instead (it won't fold "
                            "into the breakdown/player-pool from here)."
                        )
                except Exception:  # noqa: BLE001 — best-effort hint only
                    pass

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
    _src_n = len(cached_sources(slug))
    _con_n = len(load_contests(slug))
    st.caption(
        f"{'✅' if article_files else '⚠️'} {len(article_files)} article file(s)  ·  "
        f"{'✅' if _src_n else '⚠️'} {_src_n} projection source(s)"
        + ("" if _src_n else " — player pool will be skipped") + "  ·  "
        f"{'✅' if _con_n else '⚠️'} {_con_n} contest(s) declared"
        + ("" if _con_n else " — no field-size framing")
    )
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
            if cached_sources(slug):
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
        _src = cached_sources(slug)
        if _src:
            _cands = landscape.leverage_candidates(player_pool.build_pool(_src))
            _missing = landscape.uncovered_candidates(persisted["markdown"], _cands)
            if _missing:
                st.warning(
                    "⚠️ **Coverage gap** — sub-10% leverage candidates the strategy never "
                    "addresses (PLAY or PASS each): " + ", ".join(_missing)
                )
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
    elif not cached_sources(slug):
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
            if not slate_label.strip():
                st.caption("Enter a slate label to enable logging — it names the archive folder.")
            if st.button("📝 Log autopsy", type="primary", disabled=not slate_label.strip()):
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
                sim_sessions.clear(slug)
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

    # ----- Lesson-ledger hygiene ----- #
    if (REPO_ROOT / "rules" / slug / "lessons.yaml").exists():
        st.divider()
        with st.expander("Lesson-ledger hygiene", expanded=False):
            st.caption(
                "Keeps the ledger sharp as it grows: stale hypotheses, lessons near the "
                "3-slate promotion bar, and likely-duplicate lessons. Flags below are computed "
                "instantly; the review turns them into proposals you approve."
            )
            with st.container(border=True):
                st.markdown(ledger_hygiene.report_md(ledger_hygiene.hygiene_report(slug)))

            ledger_review_path = REPO_ROOT / "rules" / slug / "ledger_review.md"
            lbtn = "🔄 Re-run ledger review" if ledger_review_path.exists() else "🧹 Review ledger"
            if st.button(lbtn, key=f"ledger_review_{slug}"):
                with st.spinner("Reviewing the lesson ledger — retire / merge / promote proposals…"):
                    lresult = run_ledger_review(slug)
                if lresult["ok"]:
                    cost = lresult.get("cost_usd")
                    cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
                    st.success(f"Ledger review written in {lresult['duration_s']:.0f}s{cost_note}.")
                    st.rerun()
                else:
                    st.error(f"Couldn't run the ledger review: {lresult['error']}")

            if ledger_review_path.exists():
                with st.container(border=True):
                    st.markdown(ledger_review_path.read_text())
                st.warning(
                    "Approving applies the ledger review's retire / merge / codify decisions to "
                    "lessons.yaml (and framework/philosophy for any codifications)."
                )
                if st.button("✅ Approve & apply ledger changes", key=f"apply_ledger_{slug}"):
                    with st.spinner("Applying the approved ledger changes…"):
                        lapply = run_apply_ledger_proposals(slug)
                    if lapply["ok"]:
                        st.success("Ledger changes applied.")
                        st.rerun()
                    else:
                        st.error(f"Couldn't apply the ledger changes: {lapply['error']}")

    # ----- ROI ledger ----- #
    results_rows = history.load_results(slug)
    if results_rows:
        st.divider()
        with st.expander("Results ledger (all archived slates)", expanded=False):
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
    with st.expander("Cross-slate patterns (autopsies.md)", expanded=False):
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


# ===== Tab: Trends — contest-selection analytics (cross-sport) =====
with tab_trends:
    st.subheader("Trends — where you win")
    st.caption(
        "Cross-sport, from every logged slate's results ledger. **Best-percentile is the "
        "scoreboard** (lower = better; 1 = top of the field) — ROI lives in your third-party "
        "tracker, so it shows only as a coverage count. Use this to decide which contest shapes "
        "to put bullets in."
    )
    _rows = contest_selection.load_contest_rows()
    if _rows.empty:
        st.info("No logged contests yet — log a few autopsies and this fills in.")
    else:
        _ww = contest_selection.where_you_win(_rows, min_n=3)
        if _ww:
            st.metric(
                "Best contest shape (median %ile, n≥3)",
                f"{_ww['type']} · {_ww['field_bucket']}",
                f"median {_ww['median_pctile']}%ile over {_ww['contests']} contests",
                delta_color="off",
            )
        else:
            st.caption("_Not enough contests in any one (type × field-size) bucket yet for a headline call (need ≥3)._")

        st.markdown("**By contest type**")
        st.dataframe(contest_selection.by_type(_rows), use_container_width=True, hide_index=True)

        st.markdown("**By field-size bucket**")
        st.dataframe(contest_selection.by_field_bucket(_rows), use_container_width=True, hide_index=True)

        st.caption(f"{len(_rows)} contests across {_rows['slate_label'].nunique()} slates · "
                   f"{_rows['sport'].nunique()} sports.")


# ===== Tab: Sim Data — SaberSim analytics (analytics ONLY, never lineups) =====
with tab_sim:
    st.subheader(f"Sim Data — {contest_label}")
    st.caption(
        "Upload a **SaberSim lineup-pool export** to see what the sim likes, fades, and piles "
        "into. **Analytics only — this never builds or picks lineups.** Combinations are shown "
        "as duplication/leverage signal to be aware of, not lineups to play."
    )

    up = st.file_uploader("SaberSim lineup-pool CSV", type=["csv"], key=f"simpool_{slug}")
    if up is not None:
        sim_sessions.save_pool(slug, up)
        st.success(f"Saved sim pool ({up.name}).")

    dk_up = st.file_uploader(
        "DK Name + ID file (optional — only needed if your projections lack DK IDs)",
        type=["csv"], key=f"simdkmap_{slug}",
    )
    if dk_up is not None:
        sim_sessions.save_dkmap(slug, dk_up)
        st.success(f"Saved DK Name+ID map ({dk_up.name}).")

    pool_path = sim_sessions.pool_path(slug)
    if pool_path is None:
        st.info("No sim pool loaded yet — upload a SaberSim export above.")
    else:
        _sim = _cached_sim_analytics(
            slug,
            _file_mtime(pool_path),
            _file_mtime(sim_sessions.dkmap_path(slug)),
            _file_mtime(REPO_ROOT / "data" / "sessions" / f"{slug}.json"),
        )
        pool = _sim["pool"]
        if pool.get("n", 0) == 0:
            st.error("Couldn't parse that file as a SaberSim lineup pool. Check the export format.")
        else:
            id_to_name = _sim["id_to_name"]
            exp = _sim["exp"]

            resolved = exp["player"].apply(lambda p: not str(p).isdigit()).sum() if not exp.empty else 0
            st.caption(
                f"{pool['n']:,} sim lineups · {len(pool['roster_slots'])} roster slots · "
                f"{len(exp)} players ({resolved} name-resolved). "
                + ("" if id_to_name else "No DK IDs found — upload a DK Name+ID file to show names.")
            )

            gb = _sim["gb"]
            has_field = "field_own_pct" in exp.columns and exp["field_own_pct"].notna().any()

            st.markdown("**Player exposure** — how often the sim rosters each player")
            _cols = [c for c in ["player", "sim_exposure_pct", "field_own_pct", "avg_saber", "lineups"]
                     if c in exp.columns]
            st.dataframe(exp[_cols], use_container_width=True, hide_index=True)

            _gb_cols = ["player", "field_own_pct", "proj_points", "ceiling",
                        "value", "leverage", "sim_exposure_pct"]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**✅ Good plays — underowned value**")
                st.caption("Strong projected upside the field is under-owning (leverage = upside pct − own pct).")
                st.dataframe(gb["good"][[c for c in _gb_cols if c in gb["good"].columns]],
                             use_container_width=True, hide_index=True)
            with c2:
                st.markdown("**🚫 Bad plays — overowned chalk**")
                st.caption("Owned more than the projected upside earns — chalk to fade.")
                st.dataframe(gb["bad"][[c for c in _gb_cols if c in gb["bad"].columns]],
                             use_container_width=True, hide_index=True)

            if has_field:
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown("**📈 Leverage — sim ≫ field own**")
                    st.dataframe(gb["leverage"], use_container_width=True, hide_index=True)
                with c4:
                    st.markdown("**🪤 Traps — field own ≫ sim**")
                    st.dataframe(gb["trap"], use_container_width=True, hide_index=True)
            else:
                st.caption("_Load projections in the Projections tab to unlock the leverage/trap "
                           "view (sim exposure vs field ownership)._")

            st.markdown("**Chalky combinations** — most over-represented player groups (duplication risk to fade)")
            st.dataframe(_sim["combos"], use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("### Sim summary (Claude)")
            st.caption("A written read of the sim — core, fades, leverage, chalky combos — vs the slate strategy.")
            sim_md_path = sim_sessions.analysis_path(slug)
            sbtn = "🔄 Re-run sim summary" if sim_md_path.exists() else "🧪 Write sim summary"
            if st.button(sbtn, key=f"sim_review_{slug}"):
                with st.spinner("Reading the sim pool + strategy and writing the summary…"):
                    sres = run_sim_review(slug, contest_label, sport)
                if sres["ok"]:
                    cost = sres.get("cost_usd")
                    cost_note = f" · ~${cost:.2f} of subscription usage" if cost else ""
                    st.success(f"Sim summary written in {sres['duration_s']:.0f}s{cost_note}.")
                    st.rerun()
                else:
                    st.error(f"Couldn't write the sim summary: {sres['error']}")
            if sim_md_path.exists():
                with st.container(border=True):
                    st.markdown(sim_md_path.read_text())


# ===== Tab: Post-Contest Sim Data — custom-metric definition + grading (analytics ONLY) =====
with tab_postsim:
    st.subheader(f"Post-Contest Sim Data — {contest_label}")
    st.caption(
        "Your SaberSim custom metric and how it grades out after the race. "
        "Analytics only — this never builds or picks lineups."
    )

    # ----- Custom metric — definition -----
    reg_metrics = metrics_registry.list_metrics(slug)
    if reg_metrics:
        st.markdown("### Custom metric — definition")
        for m in reg_metrics:
            st.markdown(f"**{m.get('name', m.get('id'))}**")
            st.caption(
                f"v{m.get('version')} · {m.get('status')} · export column "
                f"`{m.get('export_column')}` · {m.get('transform')}, "
                f"{m.get('aggregation')} across 6 drivers"
            )
            variables = m.get("variables", []) or []
            if variables:
                vdf = pd.DataFrame(
                    [{"Variable": v.get("stat"), "Weight": v.get("weight")} for v in variables]
                )
                st.dataframe(vdf, use_container_width=True, hide_index=True)
            if m.get("rationale"):
                st.markdown(m["rationale"])
            guardrails = m.get("guardrails", []) or []
            if guardrails:
                with st.expander("Guardrails"):
                    st.markdown("\n".join(f"- {g.strip()}" for g in guardrails))
            changelog = m.get("changelog", []) or []
            if changelog:
                with st.expander("Changelog"):
                    cdf = pd.DataFrame(
                        [{"v": c.get("version"), "date": c.get("date"),
                          "change": c.get("change"), "reason": c.get("reason")}
                         for c in changelog]
                    )
                    st.dataframe(cdf, use_container_width=True, hide_index=True)

    # ----- Grade a custom metric (post-race) -----
    st.divider()
    st.markdown("### Grade a custom metric (post-race)")
    st.caption(
        "Upload a POST-race SaberSim export (your custom-metric column + a populated `Actual` "
        "column) to measure how the metric correlated with actual scoring, and log it to the "
        "performance ledger. Analytics only — no lineups built."
    )
    if not reg_metrics:
        st.info(f"No custom metric recorded for {contest_label} yet (rules/{slug}/metrics.yaml).")
    else:
        grade_up = st.file_uploader("Post-race SaberSim export (CSV)", type=["csv"], key=f"grade_{slug}")
        if grade_up is not None:
            gpool = sim_data.load_sim_pool(grade_up)
            glu = gpool.get("lineups")
            if glu is None or gpool.get("n", 0) == 0:
                st.error("Couldn't parse that file as a SaberSim lineup export.")
            else:
                names = [m.get("name", m.get("id")) for m in reg_metrics]
                pick = st.selectbox("Which metric is this?", names, key=f"gradepick_{slug}")
                metric = reg_metrics[names.index(pick)]
                num_cols = [c for c in glu.columns if c != "__ids"]
                dcol = metric.get("export_column")
                didx = num_cols.index(dcol) if dcol in num_cols else 0
                metric_col = st.selectbox("Metric column in the export", num_cols, index=didx, key=f"gradecol_{slug}")
                if not metric_tracker.actual_is_populated(glu):
                    st.warning("⚠️ The `Actual` column is empty/all-zero — this is a PRE-race export. "
                               "Re-export after the race so Actual is filled, then grade.")
                else:
                    g = metric_tracker.grade_metric(glu, metric_col)
                    if g is None:
                        st.error("Couldn't grade — check the metric column has numeric values.")
                    else:
                        verdict = ("positive" if g["spearman"] > 0.1 else
                                   "flat/none" if g["spearman"] > -0.1 else "ANTI-informative")
                        st.metric(f"Spearman(metric → actual)  ·  n={g['n']:,}", f"{g['spearman']:+.3f}", verdict, delta_color="off")
                        st.caption(
                            f"Pearson {g['pearson']:+.3f}  ·  decile lift **+{g['decile_lift']}** "
                            f"(top decile {g['top_decile_avg']} vs bottom {g['bottom_decile_avg']}, pool {g['pool_mean']})  ·  "
                            f"best lineup {g['best_actual']} sat at the {g['best_metric_pctile']:.0f}th pct by metric "
                            f"— the metric raises the average, it doesn't crown the nuke."
                        )
                        slate_lbl = st.text_input("Slate label (for the ledger)", key=f"gradelbl_{slug}")
                        contest_id = st.text_input("Contest id (optional)", key=f"gradecid_{slug}")
                        dup = bool(contest_id) and metric_tracker.already_logged(slug, metric["id"], contest_id)
                        if dup:
                            st.info("This metric + contest is already in the ledger — it won't double-log.")
                        if st.button("📌 Log to performance ledger", key=f"gradelog_{slug}",
                                     disabled=dup or not slate_lbl):
                            row = {"metric_id": metric["id"], "version": metric.get("version"),
                                   "date": _dt.now().strftime("%Y-%m-%d"), "slate": slate_lbl,
                                   "contest": contest_id or None, "metric_col": metric_col,
                                   "status": metric.get("status"), **g}
                            metric_tracker.log_performance(slug, row)
                            st.success(f"Logged {pick} performance for {slate_lbl}.")
                            st.rerun()

        # ----- Metric performance trend -----
        rows = metric_tracker.load_performance(slug)
        if rows:
            st.markdown("#### Metric performance over time")
            trend = pd.DataFrame([{
                "date": r.get("date"), "slate": r.get("slate"), "metric": r.get("metric_id"),
                "n": r.get("n"), "spearman": r.get("spearman"),
                "decile_lift": r.get("decile_lift"), "status": r.get("status"),
            } for r in rows])
            st.dataframe(trend, use_container_width=True, hide_index=True)
            st.caption("Promotion out of `testing` is a human call once several slates trend positive.")
