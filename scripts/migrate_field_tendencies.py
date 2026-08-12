"""One-time schema-v2 backfill for rules/<slug>/field_tendencies.jsonl.

A trap is a price, not a driver (user directive 8/9/26): the store used to keep
fish traps as BARE NAMES, discarding the evidence (fish/winner usage, realized
ownership) the moment it was computed. This script rebuilds every historical row
from the archived per-slate data so trap history becomes CONDITION dicts:

  - `history/<dir>/autopsy.json` — the full per-contest trap dicts
    ({name, fish_pct, winner_pct, gap, actual_fpts}) + crowded players with
    realized ownership.
  - `history/<dir>/bundle.md` — the slate's vendor projection pipe tables
    (`| name | salary | ownership | proj_points |…`), the only per-slate source
    of salary + projection + PROJECTED ownership; used to attach salary_tier,
    proj_points, proj_own, and the own-rank-vs-projection-rank `edge`.

Rows that can't be matched to an archive stay untouched (legacy bare strings —
every reader skips them; they degrade, never lie). Originals are saved to
`field_tendencies.jsonl.bak` before rewriting.

Run:  .venv/bin/python scripts/migrate_field_tendencies.py [--dry-run]
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.autopsy import _norm_name          # noqa: E402
from src.landscape import _salary_tier      # noqa: E402

SLUGS = ("nascar", "mma_se", "pga_classic", "pga_rd4_sd")


# ---------------------------------------------------------------------------
# bundle.md projection tables
# ---------------------------------------------------------------------------

def parse_bundle_tables(text: str) -> dict:
    """{normalized name -> {salary, ownership, proj_points, ceiling?}} from every
    projection pipe table in an archived bundle.md (first vendor wins a name).
    Header row is parsed dynamically so extra columns (ceiling, win_prob,
    opponent, …) don't break it."""
    out: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "name" in line.lower() and "salary" in line.lower():
            cols = [c.strip().lower() for c in line.strip("|").split("|")]
            i += 1
            if i < len(lines) and set(lines[i].strip().strip("|").replace("|", "").strip()) <= {"-", " ", ":"}:
                i += 1  # separator row
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                row = dict(zip(cols, cells))
                nm = _norm_name(str(row.get("name") or ""))
                if nm and nm not in out:
                    rec: dict = {}
                    for k in ("salary", "ownership", "proj_points", "ceiling"):
                        v = row.get(k)
                        if v not in (None, "", "None"):
                            try:
                                rec[k] = float(v)
                            except ValueError:
                                pass
                    if rec:
                        out[nm] = rec
                i += 1
            continue
        i += 1
    return out


def projection_context(table: dict) -> dict:
    """{normalized name -> {salary, salary_tier, proj_points, proj_own, edge}}
    with min-rank semantics (1 = best, ties share the top rank) matching
    landscape.mispricing_table. Upside = ceiling when any player has one, else
    proj_points. Missing values rank as 0 — same as mispricing's fillna(0)."""
    if not table:
        return {}
    use_ceiling = any("ceiling" in r for r in table.values())

    def upside(r: dict) -> float:
        if use_ceiling:
            return float(r.get("ceiling") or 0.0)
        return float(r.get("proj_points") or 0.0)

    ups = {nm: upside(r) for nm, r in table.items()}
    owns = {nm: float(r.get("ownership") or 0.0) for nm, r in table.items()}
    up_vals = list(ups.values())
    own_vals = list(owns.values())
    ctx = {}
    for nm, r in table.items():
        d: dict = {}
        if r.get("salary") is not None:
            d["salary"] = int(r["salary"])
            d["salary_tier"] = _salary_tier(float(r["salary"]))
        if r.get("proj_points") is not None:
            d["proj_points"] = round(float(r["proj_points"]), 2)
        if r.get("ownership") is not None:
            d["proj_own"] = round(float(r["ownership"]), 1)
        proj_rank = 1 + sum(1 for v in up_vals if v > ups[nm])
        own_rank = 1 + sum(1 for v in own_vals if v > owns[nm])
        d["edge"] = int(own_rank - proj_rank)
        ctx[nm] = d
    return ctx


# ---------------------------------------------------------------------------
# archive index + row rebuild
# ---------------------------------------------------------------------------

def _load_archives(root: Path, slug: str) -> tuple[dict, dict, dict]:
    """(by_contest_id, by_date_entries, ctx_by_dir) over every history dir."""
    by_cid: dict = {}
    by_de: dict = {}
    ctx_by_dir: dict = {}
    hist = root / "rules" / slug / "history"
    for d in sorted(hist.iterdir()) if hist.exists() else []:
        ap = d / "autopsy.json"
        if not ap.exists():
            continue
        try:
            records = json.loads(ap.read_text())
        except json.JSONDecodeError:
            continue
        if not isinstance(records, list):
            continue
        date_prefix = d.name[:10]
        bmd = d / "bundle.md"
        ctx_by_dir[d.name] = (projection_context(parse_bundle_tables(bmd.read_text()))
                              if bmd.exists() else {})
        for rec in records:
            if not isinstance(rec, dict):
                continue
            cid = str(rec.get("contest_id") or "")
            if cid:
                by_cid[cid] = (d.name, rec)
            by_de.setdefault((date_prefix, rec.get("entries")), []).append((d.name, rec))
    return by_cid, by_de, ctx_by_dir


def _row_trap_names(row: dict) -> list[str]:
    out = []
    for t in row.get("fish_traps") or []:
        out.append(str(t.get("name")) if isinstance(t, dict) else str(t))
    return out


def _match_record(row: dict, by_cid: dict, by_de: dict):
    cid = str(row.get("contest_id") or "")
    if cid and cid in by_cid:
        return by_cid[cid]
    key = (str(row.get("date") or "")[:10], row.get("field_size"))
    cands = by_de.get(key) or []
    if len(cands) == 1:
        return cands[0]
    if len(cands) > 1:
        row_traps = _row_trap_names(row)
        for dir_name, rec in cands:
            rec_traps = [str(t.get("name")) for t in
                         ((rec.get("field_profile") or {}).get("fish_traps") or [])]
            if rec_traps[:len(row_traps)] == row_traps or row_traps[:len(rec_traps)] == rec_traps:
                return (dir_name, rec)
        return cands[0]  # identical-record twins — any match is correct
    return None


def rebuild_row(row: dict, rec: dict, ctx: dict) -> dict:
    """The row with condition-dict traps + upgraded crowds, from one archive
    record + that slate's projection context. Additive; schema_version 2."""
    fp = rec.get("field_profile") or {}
    crowded = fp.get("crowded_players") or []
    own_rank_by_name = {_norm_name(str(c.get("name"))): i + 1
                        for i, c in enumerate(crowded)}
    own_by_name = {_norm_name(str(c.get("name"))): c.get("field_own")
                   for c in crowded}
    fpts_by_name = {_norm_name(str(c.get("name"))): c.get("actual_fpts")
                    for c in crowded}

    def _ctx(d: dict, name) -> dict:
        d.update(ctx.get(_norm_name(str(name)), {}))
        return d

    traps = []
    for t in (fp.get("fish_traps") or [])[:8]:
        nm = _norm_name(str(t.get("name")))
        d = {k: t.get(k) for k in ("name", "fish_pct", "winner_pct", "gap",
                                   "actual_fpts") if t.get(k) is not None}
        if own_by_name.get(nm) is not None:
            d["field_own"] = own_by_name[nm]
            d["own_rank"] = own_rank_by_name[nm]
        traps.append(_ctx(d, t.get("name")))

    crowds = []
    for c in crowded[:8]:
        d = {"name": c.get("name"), "own": c.get("field_own"),
             "fpts": c.get("actual_fpts")}
        crowds.append(_ctx(d, c.get("name")))

    out = dict(row)
    out["schema_version"] = 2
    if traps:
        out["fish_traps"] = traps
    # Upgrade crowds; keep the row's own dicts' shape when it already had own.
    if crowds:
        out["crowded_players"] = crowds
    # fpts backfill for rows that already stored {name, own} dicts
    elif all(isinstance(c, dict) for c in out.get("crowded_players") or []):
        for c in out["crowded_players"]:
            nm = _norm_name(str(c.get("name")))
            if c.get("fpts") is None and fpts_by_name.get(nm) is not None:
                c["fpts"] = fpts_by_name[nm]
            c.update(ctx.get(nm, {}))
    return out


def migrate_slug(root: Path, slug: str, dry_run: bool = False) -> dict:
    """Backfill one slug. Returns a summary dict; writes only when not dry_run
    and something changed. Original file saved to .bak before rewriting."""
    path = root / "rules" / slug / "field_tendencies.jsonl"
    summary = {"slug": slug, "rows": 0, "matched": 0, "enriched_traps": 0,
               "with_projection": 0, "legacy": 0}
    if not path.exists():
        return summary
    by_cid, by_de, ctx_by_dir = _load_archives(root, slug)
    out_lines = []
    changed = False
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            out_lines.append(line)
            continue
        summary["rows"] += 1
        m = _match_record(row, by_cid, by_de)
        if m is None:
            summary["legacy"] += 1
            out_lines.append(line)
            continue
        dir_name, rec = m
        new_row = rebuild_row(row, rec, ctx_by_dir.get(dir_name) or {})
        summary["matched"] += 1
        traps = [t for t in new_row.get("fish_traps") or [] if isinstance(t, dict)]
        if traps:
            summary["enriched_traps"] += 1
        if any(isinstance(t.get("edge"), (int, float)) for t in traps):
            summary["with_projection"] += 1
        if new_row != row:
            changed = True
        out_lines.append(json.dumps(new_row))
    if changed and not dry_run:
        shutil.copy2(path, path.with_suffix(".jsonl.bak"))
        path.write_text("\n".join(out_lines) + "\n")
    summary["written"] = changed and not dry_run
    return summary


def main() -> None:
    dry = "--dry-run" in sys.argv
    root = Path(__file__).resolve().parent.parent
    print(f"{'DRY RUN — ' if dry else ''}backfilling field_tendencies to schema v2 "
          f"(a trap is a price, not a driver)\n")
    for slug in SLUGS:
        s = migrate_slug(root, slug, dry_run=dry)
        print(f"{slug:12s} rows {s['rows']:3d} · matched {s['matched']:3d} · "
              f"traps enriched {s['enriched_traps']:3d} · with projection ctx "
              f"{s['with_projection']:3d} · left legacy {s['legacy']:3d}"
              + ("  [written]" if s.get("written") else ""))


if __name__ == "__main__":
    main()
