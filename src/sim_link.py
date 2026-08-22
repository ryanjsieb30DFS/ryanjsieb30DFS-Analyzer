"""Sim → Analyzer integration (the read side of the sibling-repo bridge).

The Sim tool (~/Desktop/Repo/ryanjsieb30DFS) builds and simulates; this module
lets the Analyzer READ two of its artifacts, degrading gracefully (every helper
returns None/{} when the Sim repo or file is absent — no exceptions, no UI):

1. `data/sim_entries/<slug>.json` — the DIVERSIFIED portfolio the Sim pushes
   via its "📨 Send pool + these entries" button: player names + headline sim
   metrics (Win%/Top1%/Top10%/Cash%/ROI) per entry. Schema v2 (8/22/26) also
   carries `pool_fp` and a per-entry `index`/`roster_key`, so these entries can
   be matched by identity against THIS repo's own per-contest picks — the Grade
   tab shows the two side by side with an agreement count (`sim_entries_by_contest`
   groups them; `sim_entries_stale` catches a payload from another pool). The
   Analyzer's pick is deliberately BLIND to this file: agreement only means
   something if the two processes chose independently. (This file lives in THIS
   repo — the Sim writes across; cleared with the slate.)

2. The Sim's field-concentration corpus (data/field_corpus/
   field_concentration.jsonl — the only fitted-data file this module reads) —
   used to correct the grader's expected-dupes estimate. The naive independence product
   (Π own × field size) UNDER-predicts real duplication, because entrants
   converge on the same chalk rosters rather than drawing players independently;
   measured over the Sim's corpus every factor is > 1 (MMA 1.7-4.2x, NASCAR
   3.1-6.6x, golf far too dispersed to use). The corpus carries observed
   top-dupe counts paired with exactly that naive prediction, so the correction
   factor is measured, not assumed.

3. The Sim's full-slate captures — roster-level field structure for the autopsy.

4. The Sim's saved settings (data/user_config.json) — `dk_username()` makes the
   Sim the single source of truth for the user's DK handle (8/10/26).

The Analyzer still never builds lineups; every read is a grade/analysis input.

The Sim repo's location can be overridden with the DFS_SIM_ROOT environment
variable; it otherwise defaults to the sibling checkout path.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
_SIM_ENTRIES_DIR = _REPO_ROOT / "data" / "sim_entries"
_SIM_ROOT = Path.home() / "Desktop" / "Repo" / "ryanjsieb30DFS"


def sim_root() -> Path | None:
    """The sibling Sim repo, or None when it isn't on this machine.

    Honors $DFS_SIM_ROOT so a moved/renamed checkout doesn't silently take every
    bridge read down with it — without the override the only symptom was panels
    quietly going missing."""
    env = os.environ.get("DFS_SIM_ROOT")
    if env:
        p = Path(env).expanduser()
        return p if p.exists() else None
    return _SIM_ROOT if _SIM_ROOT.exists() else None


def sim_raw_projection_files(slug: str) -> list[Path]:
    """The Sim's saved RAW projection uploads for this slate (one upload per
    slate, not one per tool — 8/22/26).

    The Sim keeps each uploaded vendor CSV's original bytes at
    data/uploads/<slug>/; the Projections tab's "📥 Pull from the Sim" button
    re-parses them through THIS repo's vendor detection, exactly as if the
    user had dropped them here. Raw bytes on purpose: the two repos keep
    deliberately different canonical column maps, so only the original file
    round-trips loss-free. [] when the bridge or dir is absent."""
    root = sim_root()
    if root is None:
        return []
    d = root / "data" / "uploads" / slug
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.csv") if p.is_file())


def dk_username() -> str | None:
    """The DK handle the user saved in the SIM's settings, or None.

    The Sim persists it at data/user_config.json (its Autopsy tab pre-fills
    from it). Reading it here makes the Sim the single source of truth — the
    Analyzer's autopsy previously hardcoded the handle, so changing it in the
    Sim silently broke the Analyzer's your-entries matching (fixed 8/10/26).
    Degrades to None when the bridge or key is absent."""
    root = sim_root()
    if root is None:
        return None
    path = root / "data" / "user_config.json"
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text()).get("dk_username")
    except (json.JSONDecodeError, OSError):
        return None
    value = str(value or "").strip()
    return value or None


# ---------------------------------------------------------------------------
# Entry-set hand-off (Sim Portfolio → Grade tab)
# ---------------------------------------------------------------------------

def load_sim_entries(slug: str) -> dict | None:
    """The Sim-pushed entry set for this slug, or None (absent/unreadable)."""
    path = _SIM_ENTRIES_DIR / f"{slug}.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    return payload if payload.get("entries") else None


def sim_entries_by_contest(payload: dict | None) -> dict:
    """`{contest label: [entry, …]}` for the Sim's pushed entry set.

    The Sim sends the SAME label string the pool payload uses, so these route
    straight against the Grade tab's per-contest sections. Entries with no
    contest land under `""` (a pre-v2 file, or a hand-edited one) rather than
    being dropped — the caller decides what to do with them."""
    out: dict = {}
    for e in (payload or {}).get("entries") or []:
        out.setdefault(str(e.get("contest") or ""), []).append(e)
    return out


def sim_entries_stale(payload: dict | None, pool: dict | None) -> bool:
    """True when the pushed entries were selected from a DIFFERENT pool than
    the one this repo holds — their pool indexes then point at other lineups.

    A payload with no `pool_fp` (schema v1, before 8/22/26) is *unknown*, not
    stale: it carries player names, which still grade fine."""
    fp = (payload or {}).get("pool_fp")
    if not fp or not pool:
        return False
    return str(fp) != str(pool.get("pool_fp"))


def clear_sim_entries(slug: str) -> None:
    """Slate-scoped cleanup — called wherever the slate clears."""
    path = _SIM_ENTRIES_DIR / f"{slug}.json"
    if path.exists():
        path.unlink()


# ---------------------------------------------------------------------------
# Sim autopsy hand-off (Sim Score-slate → this repo's Autopsy tab, 8/3/26)
# ---------------------------------------------------------------------------
# At Score-slate time the Sim writes two things into THIS repo:
#   data/sim_standings/<slug>/ — a copy of each scored standings CSV + manifest,
#     so the Autopsy tab can load the identical file without a second upload.
#   data/sim_autopsy/<slug>__<contest_id>.json — the measurements only the Sim
#     can make: pool-vs-picking (was the winning lineup IN the built pool?) and
#     whether each pre-lock sim ranking metric actually predicted finishes.
# Both are slate-scoped: cleared wherever sim_entries clears.

_SIM_STANDINGS_DIR = _REPO_ROOT / "data" / "sim_standings"
_SIM_AUTOPSY_DIR = _REPO_ROOT / "data" / "sim_autopsy"
_SIM_POOL_DIR = _REPO_ROOT / "data" / "sim_pool"


def load_sim_pool(slug: str) -> dict | None:
    """The Sim's FULL simmed pool + entered contests for the Entry picker
    (pushed by the Sim Portfolio tab's "📤 Send pool" button, 8/9/26) — or
    None (absent, unreadable, wrong schema, or carrying no contests).

    Columnar payload: rosters/salary/proj/avg_own arrays aligned by pool
    index, plus per-contest metric arrays (win/top1/top10/cash/roi + expected
    dupes). Selection over this pool is the ONE sanctioned exception to the
    no-selecting rule — see CLAUDE.md "Selection is not construction"."""
    path = _SIM_POOL_DIR / f"{slug}.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        return None
    if not payload.get("rosters") or not payload.get("contests"):
        return None
    return payload


def sim_pool_mtime(slug: str) -> float | None:
    """Modification time of the pushed pool file — session-state cache key so
    the multi-MB payload isn't re-parsed on every Streamlit rerun."""
    path = _SIM_POOL_DIR / f"{slug}.json"
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def list_sim_standings(slug: str) -> list[dict]:
    """Standings CSVs the Sim already scored for this slug, newest manifest
    order. Rows: {filename, path, contest_id, slate_name, scored_at}. Empty
    list when the Sim never pushed (or the files were cleared)."""
    d = _SIM_STANDINGS_DIR / slug
    manifest_path = d / "manifest.json"
    if not manifest_path.exists():
        return []
    try:
        rows = json.loads(manifest_path.read_text()).get("files") or []
    except Exception:  # noqa: BLE001
        return []
    out = []
    for r in rows:
        p = d / str(r.get("filename") or "")
        if p.exists():
            out.append({**r, "path": str(p)})
    return out


def load_sim_autopsy(slug: str) -> dict[str, dict]:
    """All Sim autopsy payloads for this slug, keyed by contest_id (falls back
    to the payload's slate_name key when the Sim had no contest id)."""
    if not _SIM_AUTOPSY_DIR.exists():
        return {}
    out: dict[str, dict] = {}
    for p in sorted(_SIM_AUTOPSY_DIR.glob(f"{slug}__*.json")):
        try:
            payload = json.loads(p.read_text())
        except Exception:  # noqa: BLE001
            continue
        key = str(payload.get("contest_id") or payload.get("slate_name") or p.stem)
        out[key] = payload
    return out


def sim_autopsy_md(payload: dict) -> str:
    """Plain-language markdown for one contest's Sim autopsy payload."""
    if not payload:
        return ""
    lines = ["#### 🎰 Sim autopsy — was it the pool or the picking?",
             "This block comes from the Sim tool. It looks at every lineup the "
             "builder created (the pool), not just the ones entered."]
    pool = payload.get("pool") or {}
    user = payload.get("user") or {}
    if pool:
        lines.append(
            f"- The pool held **{pool.get('n', 0):,} lineups**. Its best would have "
            f"scored **{pool.get('max_actual')}**; the middle one scored "
            f"{pool.get('median_actual')}.")
        if pool.get("n_beating_best_entry") is not None:
            lines.append(
                f"- **{pool['n_beating_best_entry']} pool lineups "
                f"({pool.get('pct_beating_best_entry')}%)** would have beaten your "
                f"best entered lineup ({user.get('best_points')} points).")
        edge = pool.get("picking_edge_points")
        if edge is not None:
            direction = ("added" if edge >= 0 else "cost")
            lines.append(
                f"- Your picks averaged {abs(edge)} points "
                f"{'above' if edge >= 0 else 'below'} the pool average — "
                f"picking {direction} points on average.")
    signals = payload.get("rank_signal") or []
    if signals:
        lines.append("")
        lines.append("**Did the sim's pre-lock ranking predict real finishes?** "
                     "(1.0 = perfect, 0 = coin flip, negative = backwards)")
        lines.append("| Ranking metric | Link to actual score | Top-100 avg | Pool avg |")
        lines.append("|---|---|---|---|")
        for s in signals:
            rho = s.get("spearman_vs_actual")
            lines.append(
                f"| {s.get('label')} | {'n/a' if rho is None else rho} "
                f"| {s.get('top100_avg_actual')} | {s.get('pool_avg_actual')} |")
    return "\n".join(lines)


def clear_sim_handoff(slug: str) -> None:
    """Remove the Sim's pushed standings copies + autopsy payloads for this
    slug — slate-scoped, called wherever sim_entries clears."""
    d = _SIM_STANDINGS_DIR / slug
    if d.exists():
        for p in d.glob("*"):
            try:
                p.unlink()
            except OSError:
                pass
        try:
            d.rmdir()
        except OSError:
            pass
    if _SIM_AUTOPSY_DIR.exists():
        for p in _SIM_AUTOPSY_DIR.glob(f"{slug}__*.json"):
            try:
                p.unlink()
            except OSError:
                pass
    pool_path = _SIM_POOL_DIR / f"{slug}.json"
    if pool_path.exists():
        try:
            pool_path.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Corpus-corrected dupe estimate (grader)
# ---------------------------------------------------------------------------

_SLUG_SPORT = {"pga_classic": "golf", "pga_rd4_sd": "golf_showdown",
               "mma_se": "mma", "nascar": "nascar"}

# Sports whose corpus evidence is tight enough to correct a user-facing number.
# Measured over the Sim's 577-contest corpus (7/25/26), median observed/naive by
# band, with the p10-p90 spread:
#   mma     1.7 - 4.2   (p10 0.95, p90 ~13)     → usable
#   nascar  3.1 - 6.6   (p10 1.24, p90 ~90)     → usable
#   golf   13.9 - 69.8  (p10 3.7,  p90 5,760)   → NOT usable
# Golf's ratio spans three-plus orders of magnitude because it is strongly
# scale-dependent (~3,099x in the lowest own-product quartile vs ~5x in the
# chalkiest), so a single median is not a defensible multiplier for a pre-lock
# decision input — it over-corrected chalk ~13x. Golf keeps the naive number
# until the factor is bucketed by own_product. `golf_showdown` is listed above
# only so RD4 SD (6 golfers, tiny field) can never silently inherit a full-field
# PGA Classic multiplier, which it did until 7/25/26.
_CORRECTABLE_SPORTS = {"mma", "nascar"}
_dupe_cache: dict = {}


def dupe_correction(slug: str, field_size: int | None) -> float | None:
    """Measured correction factor for the naive independence dupe estimate:
    median(observed top-dupe count / naive prediction) over the Sim corpus's
    contests of this sport in the same field-size band. None when the corpus is
    absent, thin (<3 evidence rows), or the sport's evidence is too dispersed to
    trust (see `_CORRECTABLE_SPORTS`) — caller keeps the naive number.

    Direction: every measured factor is **> 1**. Real fields duplicate consensus
    rosters MORE than per-player independence predicts, because entrants
    converge on the same chalk rosters. (Comments here and in grader.py used to
    claim the opposite — "naive over-predicts, observed ~0.01-0.09x" — which was
    backwards and would have argued for shrinking an already-low estimate.)

    Honest caveat: the evidence rows are the MOST-duplicated rosters per
    contest, so the factor is calibrated for chalky lineups — exactly the
    ones whose dupe risk the Grade tab needs to price."""
    sport = _SLUG_SPORT.get(slug)
    root = sim_root()
    if sport is None or sport not in _CORRECTABLE_SPORTS or root is None \
            or not field_size:
        return None
    band = ("small" if field_size <= 2_500 else
            "mid" if field_size <= 10_000 else "large")
    corpus = root / "data" / "field_corpus" / "field_concentration.jsonl"
    if not corpus.exists():
        return None
    # Key the cache on the corpus mtime too: a long-running Streamlit process
    # otherwise kept serving a stale factor after the Sim backfilled new
    # contests, and the whole point is that the number is measured.
    try:
        stamp = corpus.stat().st_mtime_ns
    except OSError:
        return None
    key = (sport, band, stamp)
    if key in _dupe_cache:
        return _dupe_cache[key]
    lo, hi = {"small": (0, 2_500), "mid": (2_500, 10_000),
              "large": (10_000, float("inf"))}[band]
    ratios: list[float] = []
    try:
        corpus_text = corpus.read_text()
    except OSError:
        return None
    # Per-line tolerance: the corpus is append-mode from the Sim, so ONE
    # truncated/garbled line must skip that line — a whole-loop except here
    # silently disabled the correction for every contest.
    for line in corpus_text.splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(r, dict) or "skipped" in r or r.get("sport") != sport:
            continue
        n = r.get("n_entries") or 0
        if not isinstance(n, (int, float)) or not (lo < n <= hi):
            continue
        for ev in r.get("top_dupe_evidence") or []:
            prod = ev.get("own_product")
            count = ev.get("count")
            if (isinstance(prod, (int, float)) and prod > 0
                    and isinstance(count, (int, float)) and count > 0):
                naive = prod * n
                if naive > 0:
                    ratios.append(count / naive)
    if len(ratios) < 3:
        result = None
    else:
        ratios.sort()
        result = round(ratios[len(ratios) // 2], 4)
    _dupe_cache[key] = result
    return result


# ---------------------------------------------------------------------------
# Slate captures (the Sim's full-field records) → autopsy field learning
# ---------------------------------------------------------------------------

CAPTURE_SCHEMA_VERSION = 1

# Set when a capture was found but couldn't be trusted, so the UI can say
# "the bridge is degraded" instead of looking identical to "no Sim repo".
capture_warnings: dict = {}


def find_sim_capture(slug: str, n_entries: int | None,
                     contest_id: str | None = None) -> dict | None:
    """The Sim's full-slate capture for the contest being autopsied.

    Matched on `contest_id` FIRST, falling back to exact entry count. The count
    fallback only fires when it is UNAMBIGUOUS: a candidate carrying a
    DIFFERENT contest id than the requested one is never a fallback (it is
    known to be another contest), and two candidates with the same entry count
    return None + a warning instead of letting the alphabetically-first file
    silently win — a mis-join would append wrong capture_* fields to
    field_tendencies.jsonl permanently. The returned record carries
    `_match_method` ("contest_id" / "entry_count") so downstream rows record
    how trustworthy the join was.

    Captures are validated against CAPTURE_SCHEMA_VERSION: a newer capture whose
    block semantics changed would otherwise be read as v1 and quietly produce
    wrong numbers. Rejections land in `capture_warnings[slug]`."""
    root = sim_root()
    if root is None:
        return None
    if not n_entries and not contest_id:
        return None
    capture_warnings.pop(slug, None)
    d = root / "rules" / slug / "slate_data"
    if not d.exists():
        return None
    by_count: list = []
    drifted: list = []
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(rec, dict):
            continue
        ver = rec.get("schema_version", CAPTURE_SCHEMA_VERSION)
        if not isinstance(ver, int) or ver > CAPTURE_SCHEMA_VERSION:
            drifted.append(f"{p.name} (schema v{ver})")
            continue
        cap_id = str(rec.get("contest_id") or "")
        if contest_id and cap_id == str(contest_id):
            rec["_match_method"] = "contest_id"
            return rec
        if contest_id and cap_id:
            continue  # a different contest — never a count fallback
        if n_entries and (
                ((rec.get("field") or {}).get("summary") or {}
                 ).get("n_entries") == n_entries):
            by_count.append((p.name, rec))
    if drifted:
        capture_warnings[slug] = (
            "Sim capture(s) were written by a newer build than this Analyzer "
            "understands and were skipped rather than misread: "
            + ", ".join(drifted[:3]))
    if len(by_count) == 1:
        by_count[0][1]["_match_method"] = "entry_count"
        return by_count[0][1]
    if len(by_count) > 1:
        capture_warnings[slug] = (
            f"{len(by_count)} Sim captures share this contest's entry count "
            f"({', '.join(n for n, _ in by_count[:3])}) with no contest id to "
            f"disambiguate — none was used rather than guessing.")
    return None


def capture_field_stats(slug: str, n_entries: int | None,
                        contest_id: str | None = None) -> dict | None:
    """Roster-level field structure for an autopsied contest, from the Sim's
    capture: real dupe stats + entries-per-user + (MMA, when the capture
    carries opponents) the DEAD-STRUCTURE share — entries rostering both
    fighters of a bout, whose combined ceiling is capped by the bout being
    zero-sum. This is the evidence the standings-only autopsy can't see:
    it knows scores and ownership, not the joint roster structure."""
    cap = find_sim_capture(slug, n_entries, contest_id=contest_id)
    if cap is None:
        return None
    field = cap.get("field") or {}
    s = field.get("summary") or {}
    stats = {
        "capture": cap.get("slate_name"),
        "match_method": cap.get("_match_method"),
        "unique_pct": s.get("unique_pct"),
        "max_dupe": s.get("max_dupe"),
        "top_dupes": (s.get("top_dupes") or [])[:5],
        "pct_single_entry_users": (s.get("entries_per_user") or {}).get("pct_single"),
        "mean_entries_per_user": (s.get("entries_per_user") or {}).get("mean"),
        "top3_chalk_lineup_pct": (s.get("chalk_share") or {}).get("top3_lineup_pct"),
    }
    # Dead-structure share (MMA): entries rostering both fighters of a bout.
    # Needs a per-player `opponent` in the capture, which older captures don't
    # carry. Say so rather than silently omitting the panel — a bare
    # `except: pass` here meant the feature staying dark was indistinguishable
    # from it having nothing to report.
    rosters = field.get("rosters") or []
    counts = field.get("counts") or []
    if len(rosters) != len(counts):
        stats["dead_structure_note"] = (
            f"capture has {len(rosters)} rosters but {len(counts)} counts — "
            f"skipping roster-level math rather than truncating it")
        return stats
    try:
        from src.autopsy import _norm_name
        opp = {}
        for pl in cap.get("players") or []:
            o = pl.get("opponent")
            if o and pl.get("name"):
                opp[_norm_name(str(pl["name"]))] = _norm_name(str(o))
        if not opp:
            stats["dead_structure_note"] = (
                "this capture carries no per-fighter opponent, so the "
                "dead-structure share can't be computed for it")
        else:
            index = [_norm_name(str(n)) for n in field.get("player_index") or []]
            dead = total = 0
            for roster, count in zip(rosters, counts):
                names = {index[i] for i in roster if i < len(index)}
                total += count
                if any(opp.get(n) in names for n in names):
                    dead += count
            if total:
                stats["dead_structure_pct"] = round(100.0 * dead / total, 1)
    except Exception as exc:  # noqa: BLE001 — enhancement only, but never silent
        stats["dead_structure_note"] = (
            f"dead-structure share unavailable ({type(exc).__name__})")
    return stats


def capture_stats_md(stats: dict) -> str:
    """One-glance markdown for the autopsy panel."""
    bits = []
    if stats.get("unique_pct") is not None:
        bits.append(f"**{stats['unique_pct']:.0f}%** unique rosters")
    if stats.get("max_dupe") is not None:
        bits.append(f"top roster duped **{stats['max_dupe']}×**")
    if stats.get("pct_single_entry_users") is not None:
        bits.append(f"**{stats['pct_single_entry_users']:.0f}%** single-entry users")
    if stats.get("mean_entries_per_user") is not None:
        bits.append(f"~{stats['mean_entries_per_user']:.1f} entries/user")
    if stats.get("top3_chalk_lineup_pct") is not None:
        bits.append(f"**{stats['top3_chalk_lineup_pct']:.0f}%** of entries carry all top-3 chalk")
    if stats.get("dead_structure_pct") is not None:
        bits.append(f"**{stats['dead_structure_pct']:.0f}%** dead structure "
                    "(opponent-stacked entries — capped ceiling by construction)")
    out = " · ".join(bits)
    # Say WHY a metric is missing. Otherwise a capture too old to carry
    # opponents looks exactly like a slate with nothing to report.
    if stats.get("dead_structure_note"):
        out += (("  \n" if out else "")
                + f"_Dead-structure share: {stats['dead_structure_note']}._")
    return out
