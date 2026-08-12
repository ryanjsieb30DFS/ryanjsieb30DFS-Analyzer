"""DFS Slate Analyzer — Streamlit app.

Article-driven, multi-sport DFS slate-strategy tool for DraftKings.
Flow: Slate Data → Slate Strategy → Autopsy.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from src.autopsy import (
    parse_dk_results, analyze_contest,
    build_autopsy_record, record_md_summary,
    USER_ALIASES,
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
    run_grade, run_contest_selection,
)
from src import (
    history, sessions, landscape, player_pool, ledger_hygiene,
    sim_sessions, field_tendencies, grader, sim_link,
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


def _md_safe(text: str) -> str:
    """Escape $ so Streamlit's markdown doesn't treat '$13.3K … $11.9K' as a
    LaTeX math span (the 'weird font' bug — everything between two $ renders in
    math italics). Applied at RENDER time only; the files on disk stay clean."""
    return (text or "").replace("\\$", "$").replace("$", "\\$")


# ---- Autopsy-notes drafts: persisted to disk as the user types, so a Streamlit
# crash/restart mid-autopsy never eats the lessons text. Keyed per CSV name;
# deleted on log + on slate clear. ----
def _notes_draft_path(slug: str) -> Path:
    return REPO_ROOT / "data" / "autopsy_drafts" / f"{slug}.json"


def _load_notes_drafts(slug: str) -> dict:
    p = _notes_draft_path(slug)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text()) or {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_notes_draft(slug: str, csv_name: str, text: str) -> None:
    drafts = _load_notes_drafts(slug)
    if drafts.get(csv_name, "") == text:
        return  # unchanged — skip the write
    drafts[csv_name] = text
    p = _notes_draft_path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(drafts))


def _clear_notes_drafts(slug: str) -> None:
    try:
        _notes_draft_path(slug).unlink(missing_ok=True)
    except OSError:
        pass


def _purge_slate_session_keys(slug: str) -> None:
    """Deleting the draft FILES is not enough on a clear: the widget text lives
    on in st.session_state, and the very next render re-saves it to disk — so
    last slate's Grade-tab lineups and autopsy notes resurrected after every
    clear. Purge the keys so the widgets reload from the now-empty drafts."""
    for k in [k for k in st.session_state
              if k.startswith(f"grade_text_{slug}")
              or k == f"autopsy_slate_label_{slug}"
              or k == f"autopsy_done_{slug}"
              or k.startswith(f"autopsy_notes_{slug}_")
              # Winnings + contest-link overrides are slate-scoped too — left
              # behind, last slate's values re-attached to the next slate's CSVs.
              or k.startswith(f"autopsy_win_{slug}_")
              or k.startswith(f"autopsy_contest_{slug}_")]:
        del st.session_state[k]


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
def _cached_dk_analysis(csv_bytes: bytes, sport_: str | None, slug_: str, src_mtime: float = 0.0):
    """Autopsy per-CSV heavy lifting (parse + structural analysis + shark gap),
    cached on the uploaded file's bytes. Without this, every keystroke in the
    notes/ROI widgets re-parsed and re-analyzed EVERY uploaded standings CSV
    (~270ms each). Raises ValueError for unparseable CSVs (handled at call site).
    `src_mtime` is the projections session file's mtime — it keys the cache so
    the salary enrichment refreshes when sources change (see _cached_breakdown)."""
    import io
    parsed = parse_dk_results(io.BytesIO(csv_bytes))
    # Best-effort salary/proj enrichment from still-loaded projections. The
    # autopsy never REQUIRES projections — no sources ⇒ proj_frame is None and
    # every salary field stays None, exactly the old standings-only behavior.
    proj_frame = None
    try:
        from src.autopsy import proj_frame_for_autopsy
        pool = sessions.merge_same_vendor(sessions.load_sources(slug_))
        proj_frame = proj_frame_for_autopsy([s.get("df") for s in pool.values()])
    except Exception:  # noqa: BLE001 — enrichment is best-effort
        proj_frame = None
    analysis = analyze_contest(parsed, proj_frame, sport_)
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
    # Sorting fix: these columns arrive as TEXT ("$9.8K", "13.8%"), so a sort was
    # alphabetical — "$9.8K" > "$13.3K" — and the top-salary players vanished to
    # the far end. Coerce to real numbers so st.dataframe sorts correctly.
    def _num(col, series):
        s = series.astype(str).str.strip().str.strip("*")
        s = s.str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        s = s.str.replace("%", "", regex=False)
        k = s.str.upper().str.endswith("K")
        vals = pd.to_numeric(s.str.rstrip("Kk"), errors="coerce")
        return vals.where(~k, vals * 1000)
    for col in df.columns:
        cl = col.strip().lower()
        if cl in ("rank", "sal", "salary", "proj", "own", "ceiling", "win%", "win"):
            coerced = _num(col, df[col])
            if coerced.notna().mean() > 0.8:  # only if the column really is numeric
                df[col] = coerced
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
            _clear_notes_drafts(slug)
            grader.clear_drafts(slug)
            _purge_slate_session_keys(slug)
            (REPO_ROOT / "data" / "grade" / f"{slug}.md").unlink(missing_ok=True)
            for _gp in (REPO_ROOT / "data" / "grade").glob(f"{slug}__*.md"):
                _gp.unlink(missing_ok=True)
            from src.strategy_contract import clear_contract
            clear_contract(slug)
            from src.sim_link import clear_sim_entries, clear_sim_handoff
            clear_sim_entries(slug)
            clear_sim_handoff(slug)
            from src.lineup_selection import clear_selection
            clear_selection(slug)
            st.session_state[f"confirm_clear_{slug}"] = False
            st.rerun()
        if cc2.button("Cancel", key=f"cancel_clear_{slug}"):
            st.session_state[f"confirm_clear_{slug}"] = False
            st.rerun()
    elif st.button("Clear this sport's slate", type="secondary"):
        st.session_state[f"confirm_clear_{slug}"] = True
        st.rerun()


# ---------- Tabs ---------- #
tab_proj, tab_slate, tab_strategy, tab_grade, tab_autopsy = st.tabs(
    ["Projections", "Slate Data", "Slate Strategy", "✅ Grade", "Autopsy"]
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
            # Loud at UPLOAD time (not buried in the Breakdown): rows silently
            # filtered + sport-critical columns this vendor stopped shipping.
            _junk = df.attrs.get("junk_dropped") or []
            if _junk:
                st.caption(f"↳ Dropped {len(_junk)} unparseable row(s) from the export: "
                           + ", ".join(_junk[:5])
                           + ("…" if len(_junk) > 5 else ""))
            for _w in warn_missing_for_sport(df, sport):
                st.warning(f"⚠️ {f.name}: {_w}")
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
        # Name-hygiene: the same player under two spellings would sit on the
        # board TWICE at different owns/salaries — flag it before it misleads.
        _susp = player_pool.suspect_duplicates(player_pool.build_pool(sources))
        if _susp:
            st.warning(
                "⚠️ **Possible duplicate players across sources** (spelling mismatch — "
                "the pool counts them twice): "
                + " · ".join(f"{a} ↔ {b}" for a, b in _susp)
            )
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
                st.markdown(_md_safe(f"- {bullet}"))

            # Ceiling-based panels only when the vendor ships a REAL ceiling (golf).
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
                    "payout_shape": chosen.get("payout_shape"),
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
            payout_shape = st.selectbox(
                "Payout shape (optional — frames how contrarian to be)",
                ["(unknown)", "Top-heavy", "Balanced", "Flat"],
                help="Top-heavy (1st takes a big share) demands max-ceiling contrarian "
                     "builds; Flat (min-cashes pay similar) rewards tighter theses. "
                     "Check the contest's payout table on DK.",
            )
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
                    "payout_shape": None if payout_shape == "(unknown)" else payout_shape,
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
        # ON-SLATE only (7/31/26): never demand the strategy discuss a player
        # who isn't on this card (MMA rosters turn over ~100% per slate — the
        # transferable read is the ownership SHAPE, which the bundle carries).
        _slate_names_now = None
        if _src:
            try:
                _slate_names_now = player_pool.build_pool(_src)["name"].astype(str).tolist()
            except Exception:  # noqa: BLE001
                _slate_names_now = None
        _crowds = field_tendencies.crowded_names(slug, load_contests(slug),
                                                 current_names=_slate_names_now)
        if _crowds:
            _crowd_missing = landscape.uncovered_candidates(
                persisted["markdown"], pd.DataFrame({"name": _crowds})
            )
            if len(_crowd_missing) == len(_crowds):
                st.warning(
                    "⚠️ **Field-tendency coverage gap** — the strategy surfaces none of the "
                    "plays your opponents reliably crowd (a map of THEM, not a read on the "
                    "players — leverage lives AWAY from these): "
                    + ", ".join(_crowds)
                )
        # Ownership drift: if the loaded projections moved since the strategy was
        # written (newer vendor upload), flag the leverage candidates whose
        # thesis changed — no regen needed to SEE the move.
        if _src:
            try:
                from src import drift as _drift
                _d = _drift.ownership_drift(slug, player_pool.build_pool(_src))
                _dmd = _drift.drift_md(_d) if _d else None
                if _dmd:
                    (st.warning if _d["drifted"] else st.caption)(_dmd)
            except Exception:  # noqa: BLE001 — display-only
                pass
        with st.container(border=True):
            st.caption(f"Last updated: {persisted['mtime']}")
            st.markdown(_md_safe(persisted["markdown"]))
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
                # Refresh the contract's machine-readable board so the Sim
                # sees the new tiers even on a standalone re-rank.
                try:
                    from src.strategy_contract import update_board
                    update_board(slug)
                except Exception:  # noqa: BLE001
                    pass
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
                _colcfg = {}
                for _c in _tbl.columns:
                    _cl = _c.strip().lower()
                    if _cl in ("sal", "salary"):
                        _colcfg[_c] = st.column_config.NumberColumn(_c, format="$%d")
                    elif _cl in ("own", "win%", "win"):
                        _colcfg[_c] = st.column_config.NumberColumn(_c, format="%.1f%%")
                st.dataframe(_tbl, use_container_width=True, hide_index=True,
                             column_config=_colcfg)
                with st.expander("Detailed write-ups (how each wins)", expanded=False):
                    st.markdown(_md_safe(_rest))
            else:
                st.markdown(_md_safe(saved_pool["markdown"]))
    elif not cached_sources(slug):
        st.info(f"Upload projections in the **Projections** tab, then rank the {_pnoun}.")
    else:
        st.info(f"Click **🏆 Rank {_pnoun}** above (or generate the slate strategy) to build the board.")


# ===== Tab: Grade (per contest — Claude picks + A-F letter grades) =====
with tab_grade:
    st.markdown("### ✅ Grade — pick and grade your entries, contest by contest")
    st.caption(
        "Not every contest is the same. Each contest below is picked and graded "
        "against ITS OWN field size, payout shape, and comparable history. Claude "
        "can pick a contest's entries from the Sim's pool (real lineups only — it "
        "never builds or edits one), and every lineup gets a letter grade (A to F) "
        "with the reasons spelled out."
    )
    from src import lineup_selection as _ls
    from src.autopsy import _norm_name as _nn_g

    # Sim pool, cached on the file's mtime (multi-MB parse).
    _pk_mtime = sim_link.sim_pool_mtime(slug)
    _pk_pool = None
    if _pk_mtime is not None:
        _pk_cache = st.session_state.get(f"_sim_pool_cache_{slug}")
        if not _pk_cache or _pk_cache.get("mtime") != _pk_mtime:
            _pk_cache = {"mtime": _pk_mtime, "pool": sim_link.load_sim_pool(slug)}
            st.session_state[f"_sim_pool_cache_{slug}"] = _pk_cache
        _pk_pool = _pk_cache.get("pool")

    _src_g = cached_sources(slug)
    _gpool = player_pool.build_pool(_src_g) if _src_g else pd.DataFrame()
    _declared_g = load_contests(slug)

    # One section per contest: every Sim-pool contest (matched to a declared
    # one when possible) plus any declared contest the Sim didn't sim.
    _sections = []
    if _pk_pool:
        _match_g = _ls.match_contests(_pk_pool.get("contests") or [], _declared_g)
        _used_ids = set()
        for _c in _pk_pool.get("contests") or []:
            _lbl = str(_c.get("label"))
            _d = _match_g.get(_lbl)
            if _d and _d.get("id"):
                _used_ids.add(_d["id"])
            _sections.append({"label": _lbl, "sim": _c, "declared": _d,
                              "key": _ls.contest_file_key(_lbl, _d)})
        for _d in _declared_g:
            if _d.get("id") not in _used_ids:
                _sections.append({"label": _d.get("name"), "sim": None,
                                  "declared": _d,
                                  "key": _ls.contest_file_key(_d.get("name"), _d)})
    else:
        for _d in _declared_g:
            _sections.append({"label": _d.get("name"), "sim": None, "declared": _d,
                              "key": _ls.contest_file_key(_d.get("name"), _d)})

    # Normalized name -> the Sim pool's exact spelling (for sim-standing lookups).
    _pool_name_map = {}
    if _pk_pool:
        for _r_nm in _pk_pool.get("rosters") or []:
            for _n_nm in _r_nm:
                _pool_name_map.setdefault(_nn_g(str(_n_nm)), str(_n_nm))

    if not _src_g:
        st.info("Load projections first (Projections tab) — grading needs ownership + salary.")
    elif not _sections:
        # Fallback: nothing declared and no pool — one generic box, pooled calibration.
        _gk = f"grade_text_{slug}"
        if _gk not in st.session_state:
            st.session_state[_gk] = grader.load_draft(slug)
        _gtext = st.text_area("Lineups (one per line — declare contests in Slate "
                              "Strategy for per-contest grading)", key=_gk, height=160)
        grader.save_draft(slug, _gtext)
        _glus = grader.parse_lineups(_gtext, _gpool) if _gtext.strip() else []
        if _glus:
            _gcal = grader.calibration(slug, sport, [])
            _ggrades = [grader.grade_lineup(l, _gcal) for l in _glus]
            _gletters = [grader.letter_grade(g, _gcal) for g in _ggrades]
            _ghead = grader.worst_letter([l["letter"] for l in _gletters])
            st.markdown(f"## Grade: {_ghead}")
            with st.container(border=True):
                st.markdown(_md_safe(grader.contest_grade_md(
                    _ggrades, _gletters, grader.grade_portfolio(_ggrades), _gcal)))
        else:
            st.caption("Paste lineups above to grade them.")
    else:
        # One-click distribution of the Sim's pushed entry set into the boxes.
        _sim_entries = sim_link.load_sim_entries(slug)
        if _sim_entries:
            _se_n = len(_sim_entries.get("entries") or [])
            if st.button(f"📥 Distribute {_se_n} Sim entr"
                         f"{'y' if _se_n == 1 else 'ies'} into the contest boxes",
                         key=f"load_sim_entries_{slug}",
                         help="Routes each pushed entry to its contest's box by the "
                              "contest name the Sim sent with it."):
                _routed, _unrouted = 0, []
                _by_label = {s["label"]: s["key"] for s in _sections}
                _box_lines: dict = {}
                for _e in _sim_entries.get("entries") or []:
                    _ck = _by_label.get(str(_e.get("contest")))
                    if _ck and _e.get("players"):
                        _box_lines.setdefault(_ck, []).append(", ".join(_e["players"]))
                        _routed += 1
                    else:
                        _unrouted.append(str(_e.get("contest")))
                for _ck, _lines in _box_lines.items():
                    st.session_state[f"grade_text_{slug}_{_ck}"] = "\n".join(_lines)
                    grader.save_draft(f"{slug}__{_ck}", "\n".join(_lines))
                if _unrouted:
                    st.caption("Couldn't route entries for: "
                               + ", ".join(sorted(set(_unrouted))))
                if _routed:
                    st.rerun()

        _selection_g = _ls.load_selection(slug)
        _sel_stale = bool(_selection_g and _pk_pool
                          and _selection_g.get("pool_fp") != _pk_pool.get("pool_fp"))
        if _sel_stale:
            st.info("The Sim re-sent a different pool since Claude's picks were made "
                    "— the old picks are stale; re-run them below.")

        _all_parsed = []   # (label, parsed lineups) for the cross-contest view
        for _sec in _sections:
            _key = _sec["key"]
            _sim_c = _sec["sim"]
            _decl = _sec["declared"] or (_ls.as_declared(_sim_c) if _sim_c else {})
            _fs_c = int(_decl.get("field_size") or (_sim_c or {}).get("field_size") or 0)
            _my_c = int(_decl.get("my_entries") or (_sim_c or {}).get("my_entries") or 1)
            _shape_c = (_sec["declared"] or {}).get("payout_shape")
            with st.container(border=True):
                st.markdown(
                    f"#### {str(_sec['label']).replace('$', chr(92) + '$')}")
                st.caption(f"field {_fs_c:,} · {_my_c} entr"
                           f"{'y' if _my_c == 1 else 'ies'}"
                           + (f" · payout {_shape_c}" if _shape_c
                              else " · payout shape not declared"))
                if _sec["declared"] is None and _sim_c is not None:
                    st.caption("⚠️ Not declared in Slate Strategy → Contests — "
                               "declare it for payout shape + history bookkeeping. "
                               "Picking and grading still work off the Sim's numbers.")
                if _sim_c is None and _pk_pool:
                    st.caption("No matching Sim contest in the pushed pool — grade "
                               "box only (no Claude pick, no sim adjustment).")

                _gk = f"grade_text_{slug}_{_key}"
                if _gk not in st.session_state:
                    st.session_state[_gk] = grader.load_draft(f"{slug}__{_key}")

                # ---- Claude pick (selection is not construction) ----------
                if _sim_c is not None and _pk_pool:
                    if st.button(
                        f"🎯 Have Claude pick this contest's {_my_c} entr"
                        f"{'y' if _my_c == 1 else 'ies'}",
                        key=f"pick_{slug}_{_key}",
                        help="Claude reads this contest's top ~50 Sim lineups (with "
                             "THIS contest's sim numbers), the slate strategy, and "
                             "the open lessons, then picks by lineup id. Every pick "
                             "is validated against the Sim's table — a made-up or "
                             "modified lineup is rejected and nothing saves.",
                    ):
                        with st.spinner("Reading the slate docs and picking… (~1-2 min)"):
                            _pres = run_contest_selection(slug, contest_label, sport,
                                                          _sec["label"])
                        if not _pres.get("ok"):
                            st.error(f"Pick failed — {_pres.get('error')}")
                        else:
                            _rows_v = _ls.candidate_slice(_pk_pool, _sim_c)
                            _pick_p = _ls.pick_path(slug, _key)
                            _pick_md = _pick_p.read_text() if _pick_p.exists() else ""
                            _pp = _ls.parse_pick(_pick_md, _rows_v, _my_c)
                            if _pp["errors"]:
                                for _e in _pp["errors"]:
                                    st.error(f"Pick rejected — {_e}")
                            else:
                                _ls.save_contest_pick(slug, _pk_pool, _sec["label"],
                                                      _sec["declared"], _pp["picks"],
                                                      _pp["why"])
                                st.rerun()
                    _stored = (((_selection_g or {}).get("contests") or {})
                               .get(_sec["label"]) if not _sel_stale else None)
                    if _stored:
                        _own_g = _pk_pool.get("ownership") or {}
                        _m_g = _sim_c.get("metrics") or {}
                        st.markdown("**Claude's pick for this contest:**")
                        for _p in _stored.get("picked") or []:
                            _i = _p.get("index")
                            if _i is None or _i >= len(_pk_pool["rosters"]):
                                continue
                            _names_g = [str(x) for x in _pk_pool["rosters"][_i]]
                            _bits_g = []
                            for _mk, _ml in (("top1_pct", "chance of 1st (top1)"),
                                             ("win_pct", "win"),
                                             ("cash_pct", "any payout (cash)")):
                                _arr = _m_g.get(_mk) or []
                                if _i < len(_arr) and _arr[_i] is not None:
                                    _bits_g.append(f"{_ml} {_arr[_i]}%")
                            st.markdown(
                                "- " + ", ".join(f"{n} ({_own_g.get(n, '?')}%)"
                                                 for n in _names_g)
                                + ("  \n  _" + " · ".join(_bits_g) + "_" if _bits_g else ""))
                        if _stored.get("why"):
                            st.caption(f"💡 {_stored['why']}")
                        if st.button("📋 Load pick into the grade box",
                                     key=f"loadpick_{slug}_{_key}"):
                            _lines_g = [
                                ", ".join(map(str, _pk_pool["rosters"][_p["index"]]))
                                for _p in _stored.get("picked") or []
                                if _p.get("index") is not None
                                and _p["index"] < len(_pk_pool["rosters"])]
                            if _lines_g:
                                st.session_state[_gk] = "\n".join(_lines_g)
                                grader.save_draft(f"{slug}__{_key}", "\n".join(_lines_g))
                                st.rerun()

                # ---- Grade box (A-F, calibrated to THIS contest) ----------
                _gtext = st.text_area("Lineups for this contest (one per line)",
                                      key=_gk, height=100)
                grader.save_draft(f"{slug}__{_key}", _gtext)
                _glus = (grader.parse_lineups(_gtext, _gpool)
                         if _gtext.strip() and not _gpool.empty else [])
                if _glus:
                    _cal_c = grader.contest_calibration(slug, sport, _decl)
                    _grades_c = [grader.grade_lineup(l, _cal_c) for l in _glus]
                    _letters_c = []
                    for _g_i, _lu_i in zip(_grades_c, _glus):
                        _std = None
                        if (_pk_pool and _sim_c is not None
                                and _lu_i.get("players") and not _lu_i.get("unmatched")):
                            _mapped = [_pool_name_map.get(_nn_g(p["name"]))
                                       for p in _lu_i["players"]]
                            if all(_mapped):
                                _std = grader.sim_standing(
                                    _pk_pool, _sim_c, "|".join(sorted(_mapped)))
                        _letters_c.append(grader.letter_grade(_g_i, _cal_c, _std))
                    _head_l = grader.worst_letter([l["letter"] for l in _letters_c])
                    st.markdown(f"## Grade: {_head_l}")
                    with st.container(border=True):
                        st.markdown(_md_safe(grader.contest_grade_md(
                            _grades_c, _letters_c,
                            grader.grade_portfolio(_grades_c), _cal_c)))
                    _all_parsed.append((_sec["label"], _glus))
                    if st.button("🧠 Thesis check for this contest (claude)",
                                 key=f"grade_thesis_{slug}_{_key}"):
                        with st.spinner("Reading the strategy + pool and checking "
                                        "each thesis…"):
                            _gres = run_grade(slug, contest_label, sport, _gtext,
                                              contest=_decl, file_key=_key)
                        if _gres.get("ok"):
                            st.rerun()
                        else:
                            st.error(_gres["error"])
                    _gpath_c = REPO_ROOT / "data" / "grade" / f"{slug}__{_key}.md"
                    if _gpath_c.exists():
                        with st.container(border=True):
                            st.markdown(_md_safe(_gpath_c.read_text()))
                else:
                    st.caption("Paste lineups (or load Claude's pick) to grade "
                               "this contest.")

        # ---- Cross-contest view (info only — reuse across contests is legal) --
        _every_lu = [lu for _, lus in _all_parsed for lu in lus]
        if _every_lu:
            with st.expander("🎚 Portfolio view across ALL contests"):
                st.caption("Cross-contest reads only. Reusing one lineup in two "
                           "different contests is allowed on DK — noted as info, "
                           "never a warning.")
                _lmd = grader.leverage_md(_every_lu)
                if _lmd:
                    st.markdown(_lmd)
                _seen_ros: dict = {}
                for _lblx, _lusx in _all_parsed:
                    for _lux in _lusx:
                        _rk = frozenset(_nn_g(p["name"])
                                        for p in _lux.get("players") or [])
                        if _rk:
                            _seen_ros.setdefault(_rk, set()).add(str(_lblx))
                for _rk, _lbls in _seen_ros.items():
                    if len(_lbls) > 1:
                        st.caption("ℹ️ The same lineup appears in: "
                                   + ", ".join(sorted(_lbls)) + " — allowed on DK.")


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
    # One upload, not two: when the Sim's "Score slate" already pushed the same
    # standings CSVs here (data/sim_standings/<slug>/), offer them one-click —
    # this guarantees both tools autopsy the IDENTICAL file. An explicit upload
    # above always wins; the shim mimics the two UploadedFile members the rest
    # of the tab reads (.name / .getvalue()).
    if not dk_csvs:
        try:
            from src.sim_link import list_sim_standings as _lss
            _sim_pushed = _lss(slug)
        except Exception:  # noqa: BLE001
            _sim_pushed = []
        if _sim_pushed:
            _pushed_names = ", ".join(r["filename"] for r in _sim_pushed)
            if st.checkbox(
                f"📥 Use the {len(_sim_pushed)} standings file(s) the Sim already "
                f"scored — {_pushed_names}",
                value=True,
                key=f"use_sim_standings_{slug}",
                help="The Sim tool copied these here when you clicked Score slate. "
                     "Same files, no second upload.",
            ):
                class _SimPushedCSV:
                    def __init__(self, row):
                        self.name = row["filename"]
                        self._bytes = Path(row["path"]).read_bytes()

                    def getvalue(self):
                        return self._bytes

                dk_csvs = [_SimPushedCSV(r) for r in _sim_pushed]
    # Three steps, in order. Nothing in the app communicated that Log must precede
    # Review, so the review got clicked first and silently re-reviewed a week-old
    # slate. Follows the readiness-caption pattern from the Slate Strategy tab.
    _step_logged = bool(st.session_state.get(f"autopsy_done_{slug}"))
    _step_has_arch = history.latest_history_dir(slug) is not None
    st.caption(
        f"**1.** Upload standings {'✅' if dk_csvs else '—'}  ·  "
        f"**2.** Log autopsy {'✅' if _step_logged else '⚠️ not yet'}  ·  "
        f"**3.** Post-autopsy review {'available' if _step_has_arch else '—'}"
        "   —   the review reads the ARCHIVE, so step 2 must happen first."
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
                _p, _a, _g, _f = _cached_dk_analysis(
                    _dc.getvalue(), sport, slug,
                    _file_mtime(REPO_ROOT / "data" / "sessions" / f"{slug}.json"))
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
                    dk_csv.getvalue(), sport, slug,
                    _file_mtime(REPO_ROOT / "data" / "sessions" / f"{slug}.json"))
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
                    st.info(
                        "No entries matching "
                        + " / ".join(USER_ALIASES)
                        + " found in this contest."
                    )
                else:
                    show_cols = ["rank", "points", "avg_own", "low_own_count",
                                 "salary_used", "proj_total", "dup_count", "players"]
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
                        st.markdown(_md_safe(accuracy.slate_accuracy_md([_grade_rec])))
                        st.caption("Computed in Python from this contest's actuals — trended into "
                                   "the next slate's bundle when you log the autopsy.")

                # Near-miss counterfactual + winner build story: one swap away,
                # or a structural rebuild? And what leverage carried the winner?
                try:
                    from src import counterfactual as _cf
                    _cf_md = _cf.counterfactual_md(
                        _cf.winner_story(parsed), _cf.near_miss(parsed, analysis))
                    if _cf_md:
                        with st.container(border=True):
                            st.markdown(_md_safe(_cf_md))
                except Exception:  # noqa: BLE001 — display-only, never blocks
                    pass

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
                        # Roster-level structure from the Sim's full-field
                        # capture (same standings CSV, captured at its Score
                        # slate) — evidence the standings-only profile can't
                        # see: real dupe counts + dead-structure share.
                        try:
                            from src.sim_link import (capture_field_stats,
                                                      capture_stats_md,
                                                      capture_warnings)
                            # Join on the DK contest instance id (from the
                            # download's filename) so two contests on the same
                            # slate with equal entry counts can't cross-match.
                            from src.contests import contest_id_from_filename
                            _cs = capture_field_stats(
                                slug, len(parsed["lineups"]),
                                contest_id=contest_id_from_filename(dk_csv.name))
                            if _cs:
                                _cs_md = capture_stats_md(_cs)
                                if _cs_md:
                                    st.markdown("📦 **Sim capture — roster structure:** " + _cs_md)
                            # A degraded bridge must not look like a clean one.
                            if capture_warnings.get(slug):
                                st.caption(f"⚠️ {capture_warnings[slug]}")
                        except Exception:  # noqa: BLE001
                            pass
                        for _b in _fp.get("read", []):
                            st.markdown(f"- {_b}")
                        fc1, fc2 = st.columns(2)
                        with fc1:
                            st.caption("**Crowd chalk** (field own — fade the traps)")
                            st.dataframe(pd.DataFrame(_fp["crowded_players"]).rename(
                                columns={"name": "Player", "field_own": "Field %", "actual_fpts": "FPTS"}),
                                use_container_width=True, hide_index=True, height=240)
                        with fc2:
                            st.caption("**Fish traps** (price shapes the losing half "
                                       "bought and winners didn't — a trap is a "
                                       "price, not a player)")
                            if _fp["fish_traps"]:
                                _ft_df = pd.DataFrame(_fp["fish_traps"])
                                _ft_cols = [c for c in ("name", "field_own", "fish_pct",
                                                        "winner_pct", "gap")
                                            if c in _ft_df.columns]
                                st.dataframe(_ft_df[_ft_cols].rename(
                                    columns={"name": "Player", "field_own": "Field %",
                                             "fish_pct": "Fish %",
                                             "winner_pct": "Win %", "gap": "Gap"}),
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
                        _hist = (_ft.summarize_contest(slug, _c_match["name"],
                                                       target_field_size=len(lineups))
                                 if _c_match else None)
                        _scope = f"**{_c_match['name']}**" if (_hist and _c_match) else None
                        if not _hist and _c_match:
                            _hist = _ft.summarize(slug, _c_match.get("type"),
                                                  target_field_size=len(lineups))
                            _scope = f"**{_c_match.get('type')}** contests"
                        if _hist:
                            _rc = ", ".join(f"{d['name']} ({d['in_n']}/{d['of']})"
                                            for d in _hist["reliably_crowded"][:6])
                            _msg = (f"📁 Across {_hist['n_contests']} comparable past logs of "
                                    f"{_scope}, your opponents reliably pile onto: {_rc or '—'}")
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

                # --- Sim autopsy: pool-vs-picking + did the sim ranking work --- #
                # Pushed by the Sim's Score slate; joined on the DK contest id
                # from the filename. Measurements only the Sim can make (it
                # holds the built pool + the simulation; this tool never does).
                try:
                    from src.sim_link import load_sim_autopsy, sim_autopsy_md
                    from src.contests import contest_id_from_filename as _cidff
                    _sa_all = load_sim_autopsy(slug)
                    _sa = _sa_all.get(str(_cidff(dk_csv.name) or ""))
                    if _sa:
                        _sa_md = sim_autopsy_md(_sa)
                        if _sa_md:
                            with st.container(border=True):
                                st.markdown(_sa_md)
                except Exception:  # noqa: BLE001 — a broken bridge never blocks the tab
                    pass

                # Draft-persisted: survives a Streamlit crash/restart mid-autopsy.
                # Keyed by FILE identity (not loop index): index keys stick to
                # the slot, so removing/reordering uploads cross-wired notes,
                # contest links, and winnings between contests — and the notes
                # draft then overwrote the wrong contest's on-disk draft.
                _wkey = "".join(c if c.isalnum() else "_" for c in dk_csv.name)
                _nk = f"autopsy_notes_{slug}_{_wkey}"
                if _nk not in st.session_state:
                    st.session_state[_nk] = _load_notes_drafts(slug).get(dk_csv.name, "")
                notes = st.text_area(
                    "Lessons / patterns to log (appended to autopsies.md)",
                    key=_nk,
                    height=120,
                )
                _save_notes_draft(slug, dk_csv.name, notes)

                # --- Contest link: AUTO by default (see top-level summary),
                # override only if the auto-match is wrong. --- #
                st.markdown("##### Results for the ROI ledger")
                declared = _declared_all
                _linked = _auto_links.get(dk_csv.name)
                _inferred = _C.infer_type(lineups["EntryName"])
                _cid = _C.contest_id_from_filename(dk_csv.name)
                if _cid is None:
                    # Renamed/exported standings carry no DK id in the filename,
                    # which used to bypass EVERY dedup layer (a second Log click
                    # double-counted results.jsonl, the archive, and the shark
                    # envelope). Fall back to a content hash: the same file
                    # re-uploaded under any name still dedups.
                    _cid = "file-" + hashlib.sha1(dk_csv.getvalue()).hexdigest()[:12]
                ov = st.selectbox(
                    "Contest link — auto-detected; override only if wrong",
                    ["(auto)"] + [c["name"] for c in declared] + ["(not declared)"],
                    index=0, key=f"autopsy_contest_{slug}_{_wkey}",
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
                    key=f"autopsy_win_{slug}_{_wkey}",
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
                # Write-time dedup: a contest whose DK id is already in the
                # ledger is SKIPPED — an accidental second log of the same
                # standings must never double-count results.jsonl / the
                # autopsy history (the trend everything else reads).
                _already_ids = history.logged_contest_ids(slug)
                _to_log, _dupe_names = [], []
                _batch_ids: set[str] = set()  # same contest twice in ONE upload batch
                for pc in parsed_contests:
                    _cid = pc.get("contest_id")
                    if _cid and (str(_cid) in _already_ids or str(_cid) in _batch_ids):
                        _dupe_names.append(pc["name"])
                    else:
                        if _cid:
                            _batch_ids.add(str(_cid))
                        _to_log.append(pc)
                if not _to_log:
                    st.warning(
                        f"⚠️ **Nothing logged** — all {len(parsed_contests)} uploaded contest(s) "
                        "are already in the ledger (same DK contest id). Duplicate logs are "
                        "skipped to keep results.jsonl and the trend honest."
                    )
                    st.stop()
                # Best-effort steps must never block the log, but a silent
                # failure loses learning data — collect and SHOW what failed.
                _log_warnings: list[str] = []
                if _dupe_names:
                    _log_warnings.append(
                        f"Skipped {len(_dupe_names)} already-logged contest(s): "
                        + ", ".join(_dupe_names))
                # One autopsies.md section + one autopsy_data.jsonl row per
                # contest; source_file disambiguates same-type contests.
                # Pre-log sizes: autopsy_data.jsonl is the dedup authority, so
                # if the archive below fails, these appends must be rolled back
                # or the contest is skipped as a "duplicate" on every re-log
                # and can never reach results.jsonl.
                _md_size = md_path.stat().st_size if md_path.exists() else 0
                _jl_size = jsonl_path.stat().st_size if jsonl_path.exists() else 0
                records = []
                with md_path.open("a") as fmd, jsonl_path.open("a") as fjl:
                    for pc in _to_log:
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
                            contest_id=pc.get("contest_id"),
                        )
                        # Accumulate the field tendencies for this contest — keyed
                        # by the specific contest name (sharpest) with contest-type
                        # fallback. Append-only "moving forward" substrate.
                        try:
                            from src import field_tendencies as _ft
                            from src.sim_link import capture_field_stats as _cfs
                            try:
                                _cap_stats = _cfs(slug, len(lineups),
                                                  contest_id=pc.get("contest_id"))
                            except Exception:  # noqa: BLE001
                                _cap_stats = None
                            # This slate's projections (still loaded at Log
                            # time) attach salary/projection/projected-own to
                            # each trap and crowd row — a trap is a price, not
                            # a player, so the price must be stored with it.
                            try:
                                _ft_pool = player_pool.build_pool(cached_sources(slug))
                            except Exception:  # noqa: BLE001
                                _ft_pool = None
                            _ft.record(slug, pc.get("contest_type"), len(lineups),
                                       pc.get("field_profile") or {}, ts,
                                       contest_name=pc.get("contest_name"),
                                       contest_id=pc.get("contest_id"),
                                       sim_capture=_cap_stats,
                                       pool=_ft_pool)
                        except Exception as _fte:  # noqa: BLE001 — never blocks the log
                            _log_warnings.append(
                                f"Field-tendency row NOT written for {pc['name']}: {_fte}")
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
                    _focus = [pc for pc in _to_log
                              if pc.get("contest_type") in FOCUS_CONTEST_TYPES]
                    # Focus contests ONLY — no fallback to a large-field pick.
                    # The envelope/dossier writers already refused non-focus
                    # rows, but the archived shark_gap.json + results.jsonl
                    # shark_gap_top leaked MME structure into the sealed
                    # small-field trend via process_trend_block.
                    _pick = (max(_focus, key=lambda pc: len(pc["lineups"]))
                             if _focus else None)
                    sgap = (_shark_gap.gap_for_slug(slug, _pick["parsed"])
                            if _pick else None)
                    # Accumulate the observed shark structure into the living
                    # envelope, then refresh the baseline the Grade tab and
                    # bundle read (Analyzer-internal since the Sim dropped
                    # shark machinery 7/24/26).
                    if sgap and sgap.get("sharks_in_field"):
                        from src import shark_accumulate as _acc
                        if _acc.record_observation(
                            sgap.get("sport"), sgap.get("sharks"), slug,
                            _dt.now().strftime("%Y-%m-%d"),
                            contest_type=_pick.get("contest_type"),
                            contest_id=_pick.get("contest_id"),
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
                except Exception as _se:  # noqa: BLE001
                    sgap = None
                    _log_warnings.append(f"Shark tracking NOT recorded this slate: {_se}")
                # Own-strategy adherence: did the entered lineups honor the
                # strategy contract's fade/under-own calls + leverage candidates?
                # Graded before the contract is cleared with the slate.
                _adh = None
                try:
                    from src import adherence as _adh_mod
                    _contract_path = REPO_ROOT / "data" / "strategy_contract" / f"{slug}.json"
                    if _contract_path.exists():
                        _adh = _adh_mod.grade_adherence(
                            json.loads(_contract_path.read_text()), records)
                        if _adh.get("gradable"):
                            with md_path.open("a") as _fmd2:
                                _fmd2.write("\n" + _adh_mod.adherence_md(_adh) + "\n")
                except Exception as _ae:  # noqa: BLE001
                    _adh = None
                    _log_warnings.append(f"Adherence grade NOT computed: {_ae}")
                # Pool tier calibration: grade the board's tiers against actuals
                # (scores are identical across the slate's contests — any works).
                _cal = None
                try:
                    from src import pool_calibration as _pcal
                    _pool_saved = player_pool.load_pool(slug)
                    if _pool_saved:
                        _cal = _pcal.grade_tiers(
                            _pool_saved["markdown"], _to_log[0]["parsed"]["players"])
                        _cal_md = _pcal.calibration_md(_cal)
                        if _cal_md:
                            with md_path.open("a") as _fmd3:
                                _fmd3.write("\n" + _cal_md + "\n")
                except Exception as _ce:  # noqa: BLE001
                    _cal = None
                    _log_warnings.append(f"Tier calibration NOT computed: {_ce}")
                # Grader self-validation: auto-grade the ENTERED lineups with the
                # same calibrated checks and log flags-vs-finish — the evidence
                # that validates (or corrects) the Grade tab's thresholds.
                _gv = None
                try:
                    _gv = grader.retro_grade(
                        records, grader.calibration(slug, sport, load_contests(slug)))
                except Exception as _ge:  # noqa: BLE001
                    _gv = None
                    _log_warnings.append(f"Grader self-validation NOT computed: {_ge}")
                # Sim autopsy payloads (pool-vs-picking + sim-ranking report),
                # matched to this log's contests by contest_id — archived so the
                # post-autopsy review can read them after the hand-off clears.
                _sim_aut = None
                try:
                    from src.sim_link import load_sim_autopsy as _lsa
                    _sa_all = _lsa(slug)
                    _sim_aut = [
                        _sa_all[str(r.get("contest_id"))]
                        for r in records
                        if str(r.get("contest_id")) in _sa_all
                    ] or None
                except Exception as _sae:  # noqa: BLE001
                    _sim_aut = None
                    _log_warnings.append(f"Sim autopsy NOT archived: {_sae}")
                # Archive the slate BEFORE clearing — analysis and ROI survive
                # in rules/<slug>/history/ + results.jsonl. If archiving fails,
                # roll autopsies.md + autopsy_data.jsonl back to their pre-log
                # sizes so a re-log isn't vetoed by the dedup set. The side
                # ledgers (field_tendencies / shark stores) keep their rows —
                # they all dedup by contest_id on read, so a clean re-log
                # collapses them.
                try:
                    hist_dir = history.archive_slate(
                        slug=slug,
                        sport=sport,
                        contest_label=contest_label,
                        slate_label=slate_label.strip(),
                        autopsy_records=records,
                        roi_contests=[pc["roi"] for pc in _to_log],
                        proj_source=proj_source,
                        shark_gap=sgap,
                        adherence=_adh,
                        pool_calibration=_cal,
                        grader_validation=_gv,
                        sim_autopsy=_sim_aut,
                    )
                except Exception as _arch_err:  # noqa: BLE001
                    history.truncate_to(md_path, _md_size)
                    history.truncate_to(jsonl_path, _jl_size)
                    st.error(
                        f"❌ **Archive failed — nothing was logged.** The autopsy "
                        f"ledger was rolled back so you can fix the problem and "
                        f"log again cleanly. Error: {_arch_err}"
                    )
                    st.stop()
                # Logging + archive are done. Do NOT auto-clear — set a PERSISTENT
                # completion flag and let the user clear the slate deliberately
                # (so they get a lasting confirmation and can run the review first).
                _clear_notes_drafts(slug)  # logged — the draft did its job
                # Commit the learning log (rules/: ledgers, history archives,
                # venue files, shared shark stores) LOCALLY. Two full slates of
                # lessons once lived only on this laptop, so the commit is
                # automatic — but the PUSH is not.
                #
                # `git push` takes no refspec, so it publishes every unpushed
                # commit on the branch, not just this one. "Log autopsy" is
                # consent to log an autopsy, not to publish whatever else is
                # sitting on main. The explicit backup button below the
                # completion banner does the push.
                from src.git_backup import commit_and_push
                _bk = commit_and_push(
                    REPO_ROOT, ["rules"],
                    f"Auto-backup learning log: {slate_label.strip() or slug} "
                    f"({_dt.now().strftime('%Y-%m-%d %H:%M')})",
                    push=False,
                )
                if _bk["status"] == "error":
                    _log_warnings.append(f"Learning-log backup skipped — {_bk['detail']}")
                from src.adherence import adherence_md as _adh_md_fn
                from src.pool_calibration import calibration_md as _cal_md_fn
                st.session_state[f"autopsy_done_{slug}"] = {
                    "n": len(_to_log),
                    "hist_dir": str(hist_dir.relative_to(REPO_ROOT)),
                    "warnings": _log_warnings,
                    "adherence_md": (_adh_md_fn(_adh)
                                     if _adh and _adh.get("gradable") else None),
                    "calibration_md": (_cal_md_fn(_cal)
                                       if _cal and _cal.get("gradable") else None),
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
        for _w in _done.get("warnings") or []:
            st.warning(f"⚠️ {_w}")

        # ----- Explicit GitHub backup (never automatic) ----- #
        # The learning log is already committed LOCALLY by the log flow. Pushing
        # is a separate, deliberate action because `git push` takes no refspec —
        # it publishes every unpushed commit on the branch, not just the backup.
        from src.git_backup import push_only, unpushed_summary
        _un = unpushed_summary(REPO_ROOT)
        with st.container(border=True):
            if not _un["has_remote"]:
                st.caption("💾 Learning log committed locally. No git remote is "
                           "configured, so there's nothing to back up to.")
            elif _un["n"] == 0:
                st.caption("💾 Learning log committed locally and already backed "
                           "up to GitHub — nothing left to push.")
            else:
                _n = _un["n"]
                if _n > 0:
                    st.caption(
                        f"💾 Learning log committed locally. Pushing sends "
                        f"**{_n} commit(s)** on `{_un['branch']}` to GitHub — "
                        f"git can't push just one, so this is everything "
                        f"unpushed:")
                    st.code("\n".join(_un["subjects"][:10]), language=None)
                else:
                    st.caption(f"💾 Learning log committed locally. {_un['detail']} — "
                               "a push may still work; check the result below.")
                if st.button("⬆️ Back up learning log to GitHub",
                             key=f"push_backup_{slug}"):
                    with st.spinner("Pushing to GitHub…"):
                        _res = push_only(REPO_ROOT)
                    if _res["status"] == "ok":
                        st.success(f"✅ Backed up to GitHub — {_res['detail']}.")
                    elif _res["status"] == "nothing":
                        st.info(f"Nothing to push — {_res['detail']}.")
                    else:
                        st.warning(f"⚠️ {_res['detail']}")
                    st.rerun()

        if _done.get("adherence_md"):
            with st.container(border=True):
                st.markdown(_md_safe(_done["adherence_md"]))
                st.caption("Graded against your own strategy contract — discipline, "
                           "separate from whether the reads were right. Archived to "
                           "adherence.json + trended in results.jsonl.")
        if _done.get("calibration_md"):
            with st.container(border=True):
                st.markdown(_md_safe(_done["calibration_md"]))
                st.caption("The board's tiers graded against actuals — archived to "
                           "pool_calibration.json + trended in results.jsonl.")
        if st.button("🧹 Clear slate data (start the next slate fresh)", key=f"clear_after_log_{slug}"):
            clear_persisted(slug)
            player_pool.clear_pool(slug)
            clear_contests(slug)
            clear_bundle(slug)
            clear_articles(slug)
            sessions.clear(slug)
            sim_sessions.clear(slug)
            _clear_notes_drafts(slug)
            grader.clear_drafts(slug)
            _purge_slate_session_keys(slug)
            (REPO_ROOT / "data" / "grade" / f"{slug}.md").unlink(missing_ok=True)
            for _gp in (REPO_ROOT / "data" / "grade").glob(f"{slug}__*.md"):
                _gp.unlink(missing_ok=True)
            from src.strategy_contract import clear_contract
            clear_contract(slug)
            from src.sim_link import clear_sim_entries, clear_sim_handoff
            clear_sim_entries(slug)
            clear_sim_handoff(slug)
            from src.lineup_selection import clear_selection
            clear_selection(slug)
            del st.session_state[f"autopsy_done_{slug}"]
            st.success("Slate data cleared — ready for the next slate.")
            st.rerun()

    # ----- Slate breakdown: the archived NUMBERS, read from disk ----- #
    # Every numeric read used to be bound to the uploader (gone on Clear) or
    # rendered once from session state at log time (gone on restart), and several
    # archived JSON files were never displayed at all. A user who logged an
    # autopsy and asked "where is the breakdown?" had nowhere to look.
    from src import slate_breakdown as _sb
    _archives = _sb.list_archives(slug)
    if _archives:
        st.divider()
        st.markdown("### 📊 Slate breakdown")
        st.caption("Read from the archive on disk, so it survives clearing the "
                   "slate and restarting the app. Past slates stay browsable.")
        _pick = _archives[0]
        if len(_archives) > 1:
            _labels = [_sb.archive_label(d) for d in _archives]
            _sel = st.selectbox("Which slate", _labels, index=0,
                                key=f"breakdown_pick_{slug}")
            _pick = _archives[_labels.index(_sel)]
        with st.container(border=True):
            st.markdown(_md_safe(_sb.breakdown_md(_pick)))

    # ----- Post-autopsy review (the learning loop) ----- #
    latest_hist = history.latest_history_dir(slug)
    if latest_hist is not None:
        st.divider()
        st.markdown("### Post-autopsy review")
        review_path = latest_hist / "autopsy_review.md"
        # STALENESS GATE. This section used to be gated only on "an archive
        # exists", so with unlogged CSVs sitting in the uploader it happily
        # re-reviewed whatever was newest — a week-old card, twice, with no
        # signal. The uploaded contest ids are already computed above, so
        # comparing them to the ledger answers "is what I'm looking at logged?"
        _pending = []
        try:
            _logged_ids = history.logged_contest_ids(slug)
            for _pc in (parsed_contests if dk_csvs else []):
                if _pc.get("contest_id") and _pc["contest_id"] not in _logged_ids:
                    _pending.append(_pc.get("contest_name") or _pc.get("name") or "?")
        except Exception:  # noqa: BLE001 — never block the section on this check
            _pending = []
        _arch_when = ""
        try:
            _man = json.loads((latest_hist / "manifest.json").read_text())
            _arch_when = _man.get("archived_at") or _man.get("date") or ""
        except Exception:  # noqa: BLE001
            pass
        _arch_name = latest_hist.name
        if _pending:
            # Exactly tonight's failure — made impossible.
            st.warning(
                f"⚠️ **Log the autopsy first.** {len(_pending)} uploaded contest(s) "
                f"are not in the ledger yet: {', '.join(_pending[:3])}"
                f"{'…' if len(_pending) > 3 else ''}.\n\n"
                f"Running the review now would re-review **{_arch_name}**"
                f"{f' (archived {_arch_when})' if _arch_when else ''}, not this slate."
            )
            st.caption("Scroll up, add a slate label, and click **📝 Log autopsy**. "
                       "The review reads the ARCHIVE, not the uploader.")
        else:
            st.caption(
                f"Reviews **{_arch_name}**"
                f"{f', archived {_arch_when}' if _arch_when else ''}. "
                "It grades the process, updates the lesson ledger "
                f"(rules/{slug}/lessons.yaml) and venue notes, and proposes framework "
                "changes for your approval. Takes ~1–3 minutes."
            )
        _inflight_key = f"_review_running_{slug}"
        btn_label = "🔄 Re-run post-autopsy review" if review_path.exists() else "🔬 Run post-autopsy review"
        # A ~1-3 min, ~$3 claude run should not be double-firable.
        if (not _pending) and st.button(btn_label, type="primary",
                                       key=f"autopsy_review_{slug}",
                                       disabled=bool(st.session_state.get(_inflight_key))):
            st.session_state[_inflight_key] = True
            try:
                with st.spinner("Reviewing the archived slate — grading process, updating lessons + venue notes… (~1–3 min)"):
                    rresult = run_autopsy_review(slug, contest_label, sport,
                                                 hist_dir=latest_hist)
            finally:
                st.session_state.pop(_inflight_key, None)
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
                st.markdown(_md_safe(review_md))
            proposals = re.search(
                r"(?ms)^## Proposed codifications\s*\n(.*?)(?=^## |\Z)", review_md
            )
            has_proposals = bool(
                proposals and proposals.group(1).strip()
                and "none" not in proposals.group(1).strip().lower()[:40]
            )
            # A successful apply appends '## Applied' to the review. The
            # proposals section still exists after that, so without this gate
            # the button stays armed forever and a second click re-applies the
            # same edits (duplicating framework text).
            already_applied = "## Applied" in review_md
            if has_proposals and already_applied:
                st.caption("✅ These proposals were already applied (see the "
                           "**## Applied** section above).")
            elif has_proposals:
                st.warning(
                    "The review proposes framework/philosophy changes (above). "
                    "Approving applies them and updates lesson statuses."
                )
                if st.button("✅ Approve & apply proposals", key=f"apply_proposals_{slug}"):
                    with st.spinner("Applying the approved proposals…"):
                        aresult = run_apply_proposals(slug, hist_dir=latest_hist)
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

            # Cross-sport overlap: the same lesson learned in two sports is a
            # promotion candidate for rules/shared/ (the Anchor-Equivalence path).
            try:
                _xs = ledger_hygiene.cross_sport_md(ledger_hygiene.cross_sport_candidates())
                if _xs:
                    with st.container(border=True):
                        st.markdown(_xs)
            except Exception:  # noqa: BLE001 — display-only
                pass

            # The standalone "Review ledger" button + its Approve path were
            # removed 7/18/26: hygiene flags now ride the post-autopsy review
            # (its '## Ledger hygiene' section), which recomputes them fresh
            # every run — no stale ledger_review.md behind an armed button.
            st.caption(
                "Retire / merge / promote decisions on these flags are made by the "
                "post-autopsy review above (its **Ledger hygiene** section) and applied "
                "with the same Approve button."
            )

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
