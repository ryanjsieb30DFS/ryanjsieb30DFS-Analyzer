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
    run_ledger_review, run_apply_ledger_proposals,
)
from src import (
    history, sessions, landscape, player_pool, ledger_hygiene,
    sim_sessions, field_tendencies,
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
def _cached_breakdown(slug: str, src_mtime: float, primary_name: str, sport_: str | None) -> dict:
    """The entire Projections-tab Breakdown suite, computed once per (sources,
    selected view). Streamlit expanders are NOT lazy — a collapsed expander's
    body still executes every rerun — so without this the ~10 landscape tables
    recomputed on every interaction of every tab."""
    sources = sessions.load_sources(slug)
    pool = sessions.merge_same_vendor(sources)
    if primary_name not in pool:
        return {}
    df = pool[primary_name]["df"]
    real_ceil = landscape.has_real_ceiling(df)
    out = {
        "vendor": pool[primary_name].get("vendor"),
        "warnings": warn_missing_for_sport(df, sport_),
        "df": df,
        "flags": landscape.breakdown_flags(df),
        "real_ceil": real_ceil,
        "leverage": landscape.leverage_table(df, top_n=15),
        "chalk": landscape.chalk_summary(df),
        "value": landscape.value_by_tier(df),
        "waves": landscape.tee_wave_split(df),
        "mis": landscape.mispricing_table(df, top_n=10) if real_ceil else None,
        "vol": landscape.volatility_table(df, top_n=10) if real_ceil else None,
        "disagree": (flagged_disagreements(sources, metric="proj_points", pct_threshold=15.0)
                     if len(sources) >= 2 else None),
    }
    return out


@st.cache_data(show_spinner=False)
def _cached_dk_analysis(csv_bytes: bytes, sport_: str | None, slug_: str):
    """Autopsy per-CSV heavy lifting (parse + structural analysis + shark gap),
    cached on the uploaded file's bytes. Without this, every keystroke in the
    notes/ROI widgets re-parsed and re-analyzed EVERY uploaded standings CSV
    (~270ms each). Raises ValueError for unparseable CSVs (handled at call site)."""
    import io
    parsed = parse_dk_results(io.BytesIO(csv_bytes))
    analysis = analyze_contest(parsed, None, sport_)
    try:
        from src import shark_gap as _sg
        gap = _sg.gap_for_slug(slug_, parsed)
    except Exception:  # noqa: BLE001 — the gap panel is best-effort
        gap = None
    try:
        from src import field_analysis as _fa
        field = _fa.field_profile(parsed, sport_)
    except Exception:  # noqa: BLE001 — the field panel is best-effort
        field = None
    return parsed, analysis, gap, field


def _split_leading_table(md: str):
    """Split a player-pool markdown doc into (leading table as DataFrame, remainder
    markdown). Returns (None, md) when no pipe-table is found near the top."""
    lines = md.splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if ln.strip().startswith("|") and ln.strip().endswith("|")), None)
    if start is None:
        return None, md
    end = start
    while end < len(lines) and lines[end].strip().startswith("|"):
        end += 1
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")]
            for ln in lines[start:end]]
    # rows[0] = header, rows[1] = the |---| separator, rest = data
    if len(rows) < 3:
        return None, md
    header = rows[0]
    data = [r for r in rows[2:] if any(c for c in r) and not set("".join(r)) <= set("-: ")]
    data = [r for r in data if len(r) == len(header)]
    if not data:
        return None, md
    df = pd.DataFrame(data, columns=header)
    remainder = "\n".join(lines[:start] + lines[end:]).strip()
    return df, remainder


@st.cache_data(show_spinner=False)
def _cached_hygiene_md(slug: str, lessons_mtime: float) -> str:
    """Lesson-ledger hygiene report, cached on lessons.yaml's mtime (the ledger
    only changes via review-apply, which rewrites the file)."""
    return ledger_hygiene.report_md(ledger_hygiene.hygiene_report(slug))


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
    st.markdown("**Slate readiness**")
    st.caption(
        f"Articles: {_n_articles}  ·  Projections: {_n_src}  ·  Contests: {_n_contests}\n\n"
        f"Strategy: {'✅' if _has_strategy else '—'}"
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
            from src.strategy_contract import clear_contract
            clear_contract(slug)
            st.session_state[f"confirm_clear_{slug}"] = False
            st.rerun()
        if cc2.button("Cancel", key=f"cancel_clear_{slug}"):
            st.session_state[f"confirm_clear_{slug}"] = False
            st.rerun()
    elif st.button("Clear this sport's slate", type="secondary"):
        st.session_state[f"confirm_clear_{slug}"] = True
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
                df = load_projections(f, source_name=getattr(f, "name", None))
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
        # Every table below comes from the cached suite — recomputes only when the
        # sources file or the selected view changes, not on every rerun.
        bd = _cached_breakdown(
            slug, _file_mtime(REPO_ROOT / "data" / "sessions" / f"{slug}.json"),
            primary_name, sport,
        )
        for w in bd.get("warnings") or []:
            st.warning(w)
        st.dataframe(bd["df"], use_container_width=True, height=500)

        # ---------- Breakdown — surface non-obvious edges (collapsed by default) ---------- #
        st.divider()
        with st.expander("🔍 Breakdown — what you'd miss", expanded=False):
            st.caption(
                f"Computed from **{primary_name}** ({bd.get('vendor')}). A reference "
                "view of this one source — the slate strategy reads all loaded vendors via the bundle."
            )

            # Edges to notice (synthesized headline flags first)
            st.markdown("#### Edges to notice")
            for bullet in bd["flags"]:
                st.markdown(f"- {bullet}")

            # Ceiling-based panels only when the vendor ships a REAL ceiling (golf/MLB).
            # NASCAR / names-only vendors ship none — we never fabricate one.
            real_ceil = bd["real_ceil"]

            if real_ceil:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Underowned vs ceiling (field blind spots)")
                    st.dataframe(bd["mis"]["underowned"], use_container_width=True, hide_index=True)
                with c2:
                    st.markdown("#### Overowned vs ceiling (fade candidates)")
                    st.dataframe(bd["mis"]["overowned"], use_container_width=True, hide_index=True)

            _lev_title = "Leverage board (ceiling vs ownership)" if real_ceil else "Leverage board (proj vs ownership)"
            st.markdown(f"#### {_lev_title}")
            st.dataframe(bd["leverage"], use_container_width=True, hide_index=True)

            c3, c4 = st.columns(2)
            with c3:
                st.markdown("#### Slate shape — chalk tiers")
                st.dataframe(bd["chalk"], use_container_width=True, hide_index=True)
            with c4:
                st.markdown("#### Value leaders by salary tier")
                st.dataframe(bd["value"], use_container_width=True, hide_index=True)

            st.markdown("#### Tee-wave split (AM / PM)")
            if bd["waves"].empty:
                st.caption("No `tee_time` column — wave split unavailable for this vendor file.")
            else:
                st.dataframe(bd["waves"], use_container_width=True, hide_index=True)

            if real_ceil:
                c5, c6 = st.columns(2)
                with c5:
                    st.markdown("#### Boom (highest ceiling-volatility)")
                    st.dataframe(bd["vol"]["boom"], use_container_width=True, hide_index=True)
                with c6:
                    st.markdown("#### Fragile chalk (owned, capped ceiling)")
                    st.dataframe(bd["vol"]["fragile_chalk"], use_container_width=True, hide_index=True)
            else:
                st.caption(
                    "ℹ️ Ceiling-based views (boom/bust, mispricing-vs-ceiling) need a vendor that ships a "
                    "real ceiling — hidden here because this slate's projections are projection-only "
                    "(no fabricated ceiling)."
                )

            # Cross-vendor disagreement — only when 2+ sources loaded
            if bd.get("disagree") is not None:
                st.markdown("#### Cross-vendor disagreement (≥15% spread)")
                if bd["disagree"].empty:
                    st.caption("No players with ≥15% projection spread across loaded vendors.")
                else:
                    st.dataframe(bd["disagree"], use_container_width=True, hide_index=True)
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
                    _probe = load_projections(_io.BytesIO(data), source_name=f.name)
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
            "Declare the contests you're entering — the autopsy tracks how each one's "
            "field plays over time, and that history feeds back into the strategy."
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
            # Strategy contract → the Sim tool (fades + leverage candidates).
            # Best-effort: a contract failure never blocks the strategy itself.
            try:
                from src.strategy_contract import write_contract
                _persisted_md = (load_persisted(slug) or {}).get("markdown", "")
                write_contract(slug, _persisted_md, cached_sources(slug))
                msg += " Strategy contract written for the Sim tool."
            except Exception as _ce:  # noqa: BLE001
                msg += f" (Strategy contract skipped: {_ce})"
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
        # Field-tendency coverage: the bundle surfaced recurring crowds, but the
        # strategy names NONE of them — the leverage-away read got dropped.
        _crowds = field_tendencies.crowded_names(slug, load_contests(slug))
        if _crowds:
            _crowd_missing = landscape.uncovered_candidates(
                persisted["markdown"], pd.DataFrame({"name": _crowds})
            )
            if len(_crowd_missing) == len(_crowds):
                st.warning(
                    "⚠️ **Field-tendency coverage gap** — the strategy surfaces none of the "
                    "plays your field reliably crowds (leverage lives AWAY from these): "
                    + ", ".join(_crowds)
                )
        with st.container(border=True):
            st.caption(f"Last updated: {persisted['mtime']}")
            st.markdown(persisted["markdown"])
    else:
        st.info("**No saved strategy yet.** Click **Generate slate strategy** above and it appears here.")

    # ----- (d) Player pool — ranked board (with the strategy, or standalone) -----
    st.markdown("---")
    _pnoun = "fighters" if sport == "mma" else "players"
    st.markdown(f"## {_pnoun.capitalize()} ranked — all data")
    st.caption(
        f"Every {_pnoun[:-1]} you could roster, ranked for GPP from **all your data** "
        "(projections + ownership + articles) — an easy-to-read table first, a short write-up "
        "each below. Built with the slate strategy above, or rank standalone anytime with the "
        "button." + (" MMA shows ceiling (points if they win) + win%." if sport == "mma" else "")
    )
    if cached_sources(slug):
        if st.button(f"🏆 Rank {_pnoun} (all data)", key=f"rank_pool_{slug}",
                     help="Runs the ranked board now — works even without a generated slate "
                          "strategy (ranks the full pool). Reads your articles if any are loaded."):
            with st.spinner(f"Ranking {_pnoun} from projections + ownership + articles… (~1–2 min)"):
                _pr = run_player_pool(slug, contest_label, sport)
            if _pr["ok"]:
                st.success(f"Ranked in {_pr['duration_s']:.0f}s."
                           + (f" · ~${_pr['cost_usd']:.2f}" if _pr.get("cost_usd") else ""))
                st.rerun()
            else:
                st.error(_pr["error"])
    saved_pool = player_pool.load_pool(slug)
    if saved_pool:
        with st.container(border=True):
            st.caption(f"Last updated: {saved_pool['mtime']}")
            # Render the leading ranked table as a dataframe (easy-to-read, sortable);
            # the detailed write-ups follow below it.
            _tbl, _rest = _split_leading_table(saved_pool["markdown"])
            if _tbl is not None:
                st.dataframe(_tbl, use_container_width=True, hide_index=True)
                with st.expander("Detailed write-ups (how each wins)", expanded=False):
                    st.markdown(_rest)
            else:
                st.markdown(saved_pool["markdown"])
    elif not cached_sources(slug):
        st.info(f"Upload projections in the **Projections** tab, then rank the {_pnoun}.")
    else:
        st.info(f"Click **🏆 Rank {_pnoun}** above (or generate the slate strategy) to build the board.")


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

        # Auto-link each CSV to a declared contest — ZERO manual selection. Infer
        # the entry-cap type from the standings' (n/m) suffix, then match to the
        # declared contest by field size. Computed once here; the per-CSV loop and
        # the log step just read `_auto_links`. (_cached_dk_analysis is byte-cached,
        # so this pre-pass is free.)
        from src import contests as _C
        _declared_all = load_contests(slug)
        _csv_infos = []
        for _dc in dk_csvs:
            try:
                _p, _a, _g, _f = _cached_dk_analysis(_dc.getvalue(), sport, slug)
            except ValueError:
                continue
            _csv_infos.append({
                "name": _dc.name,
                "field_size": len(_p["lineups"]),
                "inferred_type": _C.infer_type(_p["lineups"]["EntryName"]),
            })
        _auto_links = _C.auto_link(_csv_infos, _declared_all)
        if _csv_infos:
            _lines = []
            for _ci in _csv_infos:
                _d = _auto_links.get(_ci["name"])
                _t = (_d.get("type") if _d else None) or _ci.get("inferred_type") or "?"
                if _d:
                    _lines.append(f"- **{_ci['name']}** → **{_d['name']}** ({_t})")
                else:
                    _lines.append(
                        f"- **{_ci['name']}** → type **{_t}** from the standings "
                        "(no declared match — declare it in Slate Strategy for "
                        "specific-contest tracking)")
            st.success("🔗 **Auto-linked** (no manual step):\n" + "\n".join(_lines))

        for i, dk_csv in enumerate(dk_csvs):
            try:
                # Cached on the file's bytes — typing in the notes/ROI widgets no
                # longer re-parses and re-analyzes every uploaded CSV per keystroke.
                parsed, analysis, _gap_cached, _field_cached = _cached_dk_analysis(
                    dk_csv.getvalue(), sport, slug)
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

                # Shark gap — structural us-vs-sharks fingerprint for THIS field
                # (computed once in _cached_dk_analysis; None = best-effort failure).
                if _gap_cached is not None:
                    from src import shark_gap as _sg
                    _gap = _gap_cached
                    with st.container(border=True):
                        st.markdown(_sg.gap_md(_gap))
                        if not _gap.get("sport"):
                            st.caption("No sport→shark mapping for this slug yet — add it in "
                                       "rules/shared/shark_handles.yaml.")
                        elif not _gap.get("sharks_in_field"):
                            st.caption(f"No tracked {_gap.get('sport')} sharks entered this contest. "
                                       "Add the heavy-MME top finishers to shark_handles.yaml to "
                                       "build the watchlist.")

                    # Per-pro dossier + auto-discovery: the named humans in your
                    # contests, how they play vs you, and recurring top-finishers
                    # not yet on the watchlist (one-click promote). Sport-level, so
                    # only render on the first CSV to avoid repeating the table.
                    if i == 0 and _gap.get("sport"):
                        from src import shark_dossier as _sd
                        _dmd = _sd.dossier_md(_gap["sport"])
                        _cands = _sd.promotion_candidates(slug)
                        if _dmd or _cands:
                            with st.container(border=True):
                                if _dmd:
                                    st.markdown(_dmd)
                                    st.caption("Accumulated from your logged autopsies — the specific "
                                               "pros, how they play, and their record vs you.")
                                if _cands:
                                    st.markdown("**Recurring opponents not yet tracked** — pros who keep "
                                                "finishing top of your contests but aren't on the watchlist:")
                                    for _c in _cands:
                                        _pc1, _pc2 = st.columns([4, 1])
                                        with _pc1:
                                            st.markdown(f"- **{_c['handle']}** — in {_c['in_n']} of your "
                                                        f"{_c['sport']} contests, best finish "
                                                        f"{_c['best_pctile']}%ile")
                                        with _pc2:
                                            if st.button("➕ Track", key=f"promote_{slug}_{_c['handle']}"):
                                                if _sd.promote(_c["sport"], _c["handle"]):
                                                    st.success(f"Added {_c['handle']} to the "
                                                               f"{_c['sport']} watchlist.")
                                                    st.rerun()

                # --- Field / Fish: how opponents played → leverage away from it --- #
                if _field_cached and _field_cached.get("gradable"):
                    _fp = _field_cached
                    with st.container(border=True):
                        st.markdown("#### 🐟 Field / Fish — leverage away from this next time")
                        for _b in _fp.get("read", []):
                            st.markdown(f"- {_b}")
                        fc1, fc2 = st.columns(2)
                        with fc1:
                            st.caption("**Crowd chalk** (field own — fade the traps)")
                            st.dataframe(pd.DataFrame(_fp["crowded_players"]).rename(
                                columns={"name": "Player", "field_own": "Field %", "actual_fpts": "FPTS"}),
                                use_container_width=True, hide_index=True, height=240)
                        with fc2:
                            st.caption("**Fish traps** (loved by losers, faded by winners)")
                            if _fp["fish_traps"]:
                                st.dataframe(pd.DataFrame(_fp["fish_traps"])[["name", "fish_pct", "winner_pct", "gap"]].rename(
                                    columns={"name": "Player", "fish_pct": "Fish %", "winner_pct": "Win %", "gap": "Gap"}),
                                    use_container_width=True, hide_index=True, height=240)
                            else:
                                st.caption("None — fish and winners played similarly.")
                        st.caption("**Dupe magnets** — pairs the field crowded (break these to get unique):")
                        st.markdown("  ·  ".join(
                            f"{c['players'][0]} + {c['players'][1]} ({c['field_pct']}%)"
                            for c in _fp["crowded_combos"][:5]) or "_none_")
                        _wp, _fpz = _fp.get("winners_profile"), _fp.get("fish_profile")
                        if _wp and _fpz:
                            st.caption(
                                f"Structure — winners {_wp.get('avg_own_per_slot')}% own/slot, "
                                f"{_wp.get('dart_pct')}% carried a dart · "
                                f"fish {_fpz.get('avg_own_per_slot')}% own/slot, {_fpz.get('dart_pct')}% darts."
                            )
                        # Forward-looking: how the field has historically played
                        # THIS contest — prefer the specific recurring contest
                        # (by name), fall back to its entry-cap type.
                        _c_match = None
                        for _c in load_contests(slug):
                            _fs = _c.get("field_size") or 0
                            if _fs and abs(_fs - len(lineups)) / _fs <= 0.10:
                                _c_match = _c; break
                        from src import field_tendencies as _ft
                        _hist = _ft.summarize_contest(slug, _c_match["name"]) if _c_match else None
                        _scope = f"**{_c_match['name']}**" if (_hist and _c_match) else None
                        if not _hist and _c_match:
                            _hist = _ft.summarize(slug, _c_match.get("type"))
                            _scope = f"**{_c_match.get('type')}** contests"
                        if _hist:
                            _rc = ", ".join(f"{d['name']} ({d['in_n']}/{d['of']})"
                                            for d in _hist["reliably_crowded"][:6])
                            _msg = (f"📁 Across {_hist['n_contests']} past logs of {_scope}, "
                                    f"the field reliably crowds: {_rc or '—'}")
                            _opp = _hist.get("recurring_opponents") or []
                            if _opp:
                                _msg += ("  ·  recurring opponents: "
                                         + ", ".join(f"{o['handle']} ({o['in_n']}/{o['of']})"
                                                     for o in _opp[:6]))
                            _tr = _hist.get("winners_own_trend")
                            if _tr is not None and abs(_tr) >= 1.0:
                                _msg += (f"  ·  winners trending "
                                         f"{'chalkier' if _tr > 0 else 'sharper'} ({_tr:+} own/slot)")
                            st.info(_msg)

                notes = st.text_area(
                    "Lessons / patterns to log (appended to autopsies.md)",
                    key=f"autopsy_notes_{slug}_{i}",
                    height=120,
                )

                # --- Contest link: AUTO by default (see top-level summary),
                # override only if the auto-match is wrong. --- #
                st.markdown("##### Results for the ROI ledger")
                declared = _declared_all
                _linked = _auto_links.get(dk_csv.name)
                _inferred = _C.infer_type(lineups["EntryName"])
                _cid = _C.contest_id_from_filename(dk_csv.name)
                ov = st.selectbox(
                    "Contest link — auto-detected; override only if wrong",
                    ["(auto)"] + [c["name"] for c in declared] + ["(not declared)"],
                    index=0, key=f"autopsy_contest_{slug}_{i}",
                )
                if ov == "(auto)":
                    picked = _linked
                elif ov == "(not declared)":
                    picked = None
                else:
                    picked = next((c for c in declared if c["name"] == ov), None)
                # contest_type ALWAYS resolves — matched contest's type, else inferred
                # from the standings' (n/m) suffix. Never None / "unknown".
                contest_type = (picked.get("type") if picked else None) or _inferred
                contest_name = picked.get("name") if picked else None
                picked_name = picked["name"] if picked else dk_csv.name
                if picked:
                    entry_fee = picked.get("entry_fee")
                    my_entries = picked.get("my_entries", 0)
                    st.caption(f"🔗 Linked to **{picked['name']}** · type **{contest_type}** "
                               f"· contest {_cid or '—'}")
                else:
                    entry_fee = None
                    my_entries = (analysis["user_summary"] or {}).get("entry_count", 0)
                    st.caption(f"🔗 No declared match · type **{contest_type or '?'}** inferred "
                               f"from the standings · contest {_cid or '—'}")
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
                "field_profile": _field_cached,
                "contest_type": contest_type,
                "contest_name": contest_name,
                "contest_id": _cid,
                "notes": notes,
                "roi": {
                    "name": picked_name if picked else dk_csv.name,
                    "type": contest_type,
                    "contest_id": _cid,
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
                            field_profile=pc.get("field_profile"),
                        )
                        # Accumulate the field tendencies for this contest — keyed
                        # by the specific contest name (sharpest) with contest-type
                        # fallback. Append-only "moving forward" substrate.
                        try:
                            from src import field_tendencies as _ft
                            _ft.record(slug, pc.get("contest_type"), len(lineups),
                                       pc.get("field_profile") or {}, ts,
                                       contest_name=pc.get("contest_name"),
                                       contest_id=pc.get("contest_id"))
                        except Exception:  # noqa: BLE001 — never blocks the log
                            pass
                        fmd.write(f"\n\n## {ts} — {contest_label} ({pc['name']})\n")
                        fmd.write(f"- Entries: {len(lineups):,}\n")
                        fmd.write(f"- Winning score: {lineups['Points'].max():.1f}\n")
                        fmd.write(f"- Cash line (top 20%): {lineups['Points'].quantile(0.80):.1f}\n")
                        fmd.write(record_md_summary(record) + "\n")
                        if notes.strip():
                            fmd.write(f"\n{notes.strip()}\n")
                        fjl.write(json.dumps(record) + "\n")
                        records.append(record)
                # Structural shark-gap on the largest SE/3-Max/5-Max contest — we
                # benchmark against sharks' SMALL-FIELD play, never their 150-max
                # MME dumps. Falls back to the biggest contest only for display
                # (record_observation still refuses to accumulate a non-focus
                # contest). Never blocks the log.
                sgap = None
                try:
                    from src import shark_gap as _shark_gap
                    from src.contests import FOCUS_CONTEST_TYPES
                    _focus = [pc for pc in parsed_contests
                              if pc.get("contest_type") in FOCUS_CONTEST_TYPES]
                    _pick = max(_focus or parsed_contests, key=lambda pc: len(pc["lineups"]))
                    sgap = _shark_gap.gap_for_slug(slug, _pick["parsed"])
                    # Accumulate the observed shark structure into the living
                    # envelope, then refresh the baseline the Sim tool reads.
                    if sgap and sgap.get("sharks_in_field"):
                        from src import shark_accumulate as _acc
                        if _acc.record_observation(
                            sgap.get("sport"), sgap.get("sharks"), slug,
                            _dt.now().strftime("%Y-%m-%d"),
                            contest_type=_pick.get("contest_type"),
                        ):
                            _acc.refresh_baseline()
                        # Per-pro dossier: one row per NAMED shark in-field (their
                        # fingerprint + our side), so we track the specific humans
                        # over time — not just the aggregate envelope.
                        from src import shark_dossier as _dossier
                        _dossier.record_pros(
                            slug, sgap.get("sport"), _pick["parsed"], sgap,
                            _dt.now().strftime("%Y-%m-%d"),
                            contest_type=_pick.get("contest_type"),
                            field_size=len(_pick["lineups"]),
                            contest_id=_pick.get("contest_id"),
                        )
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
                # Logging + archive are done. Do NOT auto-clear — set a PERSISTENT
                # completion flag and let the user clear the slate deliberately
                # (so they get a lasting confirmation and can run the review first).
                st.session_state[f"autopsy_done_{slug}"] = {
                    "n": len(parsed_contests),
                    "hist_dir": str(hist_dir.relative_to(REPO_ROOT)),
                }
                st.rerun()

    # ----- Completion signal + user-controlled clear ----- #
    _done = st.session_state.get(f"autopsy_done_{slug}")
    if _done:
        st.divider()
        st.success(
            f"✅ **Autopsy logged & archived** — {_done['n']} contest(s) saved to "
            f"`rules/{slug}/autopsies.md` + `autopsy_data.jsonl`, archived to "
            f"`{_done['hist_dir']}`. **Your data is safe.** Run the post-autopsy review below if "
            "you want, then clear the slate when you're ready to start fresh."
        )
        if st.button("🧹 Clear slate data (start the next slate fresh)", key=f"clear_after_log_{slug}"):
            clear_persisted(slug)
            player_pool.clear_pool(slug)
            clear_contests(slug)
            clear_bundle(slug)
            clear_articles(slug)
            sessions.clear(slug)
            sim_sessions.clear(slug)
            from src.strategy_contract import clear_contract
            clear_contract(slug)
            del st.session_state[f"autopsy_done_{slug}"]
            st.success("Slate data cleared — ready for the next slate.")
            st.rerun()

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
                st.markdown(_cached_hygiene_md(
                    slug, _file_mtime(REPO_ROOT / "rules" / slug / "lessons.yaml")))

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
