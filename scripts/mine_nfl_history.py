"""One-time miner for the 2024-25 NFL Classic DK contest-standings archive.

Reads the user's historical standings CSVs (read-only, outside the repo:
~/Desktop/DFS/DFS NFL Past Slate Data/"<Classic|Full> Slate Week N YYYY.csv"),
reuses src/autopsy.py + src/shark_gap.py to extract projection-free winning-
lineup STRUCTURE per contest, writes rules/nfl_classic/_mining/slates.{json,csv},
and SEEDS the `sports.nfl` block of rules/shared/shark_baseline.json.

Why the seed matters: shark_accumulate.refresh_baseline() only updates blocks
that already exist, so a sport with no seed never gets an envelope, no matter
how many autopsies are logged. The seed is built from the SMALL-FIELD files
only (< SMALL_FIELD_MAX entries) because the user's Classic profile is
SE/3-Max/5-Max; the large (Milly-size) files are summarized but never feed the
envelope. Existing user/shark blocks for other sports are left untouched, and
an existing `nfl` block is only replaced with --reseed.

Run:  .venv/bin/python scripts/mine_nfl_history.py [--reseed] [--skip-large]
"""
from __future__ import annotations

import csv
import json
import re
import sys
import traceback
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd  # noqa: E402
from src.autopsy import parse_dk_results, analyze_contest  # noqa: E402
from src.shark_gap import (structural_profile, chalk_anchors, present_handles,  # noqa: E402
                           load_handles, _handle)

SRC = Path.home() / "Desktop" / "DFS" / "DFS NFL Past Slate Data"
REPO = Path(__file__).resolve().parent.parent
BASELINE = REPO / "rules" / "shared" / "shark_baseline.json"
SLUG = "nfl_classic"
SPORT_KEY = "nfl"
SMALL_FIELD_MAX = 10_000
FEATURES = ("own_per_slot", "leverage_pct", "anchor_exposure", "unique_pct")

FNAME_RE = re.compile(r"^(Classic|Full) Slate Week (\d+) (\d{4})$")


def parse_filename(stem: str):
    m = FNAME_RE.match(stem.strip())
    if not m:
        return None
    return {"family": m.group(1), "week": int(m.group(2)), "year": m.group(3),
            "slug": SLUG, "date": f"{m.group(3)}-W{int(m.group(2)):02d}"}


def _field_size(path: Path) -> int:
    with path.open("rb") as f:
        return max(sum(1 for _ in f) - 1, 0)


def _winner_profile(parsed: dict, handles) -> dict:
    prof = structural_profile(parsed, handles, chalk_anchors(parsed))
    return {f: prof.get(f) for f in FEATURES} if prof.get("gradable") else {}


def mine_one(path: Path, cfg: dict, full: bool) -> dict:
    parsed = parse_dk_results(str(path))
    L = parsed["lineups"]
    pts = pd.to_numeric(L["Points"], errors="coerce").dropna()
    field = int(len(L))
    row = {
        "field_size": field,
        "winning_score": round(float(pts.max()), 2) if len(pts) else None,
        "cash_line_p80": round(float(pts.quantile(0.20)), 2) if len(pts) else None,
        "median_score": round(float(pts.median()), 2) if len(pts) else None,
    }
    sharks = (cfg.get("sharks_by_sport") or {}).get(SPORT_KEY, [])
    user = cfg.get("user", [])
    row["sharks_present"] = present_handles(parsed, sharks)
    row["user_present"] = present_handles(parsed, user)
    row["shark_profile"] = _winner_profile(parsed, sharks) if row["sharks_present"] else {}
    row["user_profile"] = _winner_profile(parsed, user) if row["user_present"] else {}
    # Rank-1 winner + the top-10 finishers as a "winners" cohort (fallback
    # envelope when no tracked shark is in the field).
    top = L.sort_values("Rank").head(10)
    top_handles = list({_handle(h) for h in top["EntryName"]})
    row["top10_profile"] = _winner_profile(parsed, top_handles)
    win = L.loc[L["Rank"].astype(int).idxmin()]
    row["winner_entry"] = _handle(win["EntryName"])
    row["winner_lineup"] = list(win["Lineup_parsed"])
    row["winner_profile"] = _winner_profile(parsed, [row["winner_entry"]])
    if full:
        res = analyze_contest(parsed, None, SPORT_KEY, slug=SLUG)
        ws = res["winners_summary"]
        row.update({
            "top_n": ws.get("top_n"),
            "winners_avg_own": ws.get("avg_own_mean"),
            "winners_low_own_mean": ws.get("low_own_count_mean"),
            "winners_unique_pct": ws.get("unique_pct"),
            "winners_dup_max": ws.get("dup_max"),
            "n_slate_defining": len(res["slate_defining"]),
            "slate_defining": [
                {"name": d["name"], "own": d["actual_own"], "fpts": d["actual_fpts"],
                 "top_pct": d["top_lineup_pct"]} for d in res["slate_defining"]],
        })
    return row


def _mean_env(profiles: list[dict]) -> dict:
    out = {}
    for f in FEATURES:
        vals = [p[f] for p in profiles if p.get(f) is not None]
        out[f] = round(mean(vals), 3) if vals else None
    return out


def seed_baseline(rows: list[dict], reseed: bool) -> dict | None:
    base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {"sports": {}, "contests": []}
    sports = base.setdefault("sports", {})
    if SPORT_KEY in sports and not reseed:
        print(f"\nshark_baseline.json already has an `{SPORT_KEY}` block — pass --reseed to replace it.")
        return None
    small = [r for r in rows if r["field_size"] < SMALL_FIELD_MAX]
    shark_profiles = [r["shark_profile"] for r in small if r["shark_profile"]]
    user_profiles = [r["user_profile"] for r in small if r["user_profile"]]
    top_profiles = [r["top10_profile"] for r in small if r["top10_profile"]]
    if shark_profiles:
        shark_env, source, weight = _mean_env(shark_profiles), "tracked sharks", len(shark_profiles)
    else:
        shark_env, source, weight = _mean_env(top_profiles), "top-10 finishers (no tracked shark in field)", len(top_profiles)
    # An EMPTY dict when the user never appears: the bundle's shark-reality
    # block tests `if user_env:` and would otherwise print "own/slot None".
    user_env = _mean_env(user_profiles) if user_profiles else {}
    gap = ({f: round(user_env[f] - shark_env[f], 2) for f in FEATURES
            if user_env.get(f) is not None and shark_env.get(f) is not None}
           if user_env else {})
    block = {
        "n_contests": len(small),
        "n_with_sharks": len(shark_profiles),
        "user_envelope": user_env,
        "shark_envelope": shark_env,
        "mean_gap": gap,
        "seed_envelope": dict(shark_env),
        "seed_weight": max(int(weight), 1),
        "accumulated_contests": 0,
        "seed_source": (f"scripts/mine_nfl_history.py 2026-09-12 — {source}; "
                        f"{len(small)} small-field (<{SMALL_FIELD_MAX:,}) NFL Classic "
                        f"contests from the 2024-25 archive"),
    }
    sports[SPORT_KEY] = block
    contests = [c for c in base.get("contests", []) if c.get("sport") != SPORT_KEY]
    for r in small:
        contests.append({"id": r["source_file"], "sport": SPORT_KEY, "n_field": r["field_size"],
                         "n_players": None, "sharks_in_field": bool(r["sharks_present"])})
    base["contests"] = contests
    base["n_contests"] = len(contests)
    BASELINE.write_text(json.dumps(base, indent=2))
    return block


def main(argv: list[str]) -> None:
    reseed = "--reseed" in argv
    skip_large = "--skip-large" in argv
    cfg = load_handles()
    files = sorted(SRC.glob("*.csv"))
    rows: list[dict] = []
    failures: list[tuple[str, str]] = []
    unparsed: list[str] = []
    for i, path in enumerate(files, 1):
        meta = parse_filename(path.stem)
        if not meta:
            unparsed.append(path.name)
            continue
        size = _field_size(path)
        small = size < SMALL_FIELD_MAX
        if skip_large and not small:
            continue
        print(f"  [{i}/{len(files)}] {path.name} ({size:,} entries){'' if small else ' — large, summary only'}")
        try:
            row = mine_one(path, cfg, full=small)
        except Exception as exc:  # noqa: BLE001
            failures.append((path.name, f"{type(exc).__name__}: {exc}"))
            continue
        row.update(meta)
        row["source_file"] = path.name
        rows.append(row)

    outdir = REPO / "rules" / SLUG / "_mining"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "slates.json").write_text(json.dumps(rows, indent=2, default=str))
    flat_cols = ["date", "year", "week", "family", "slug", "field_size", "winning_score",
                 "cash_line_p80", "median_score", "top_n", "winners_avg_own",
                 "winners_low_own_mean", "winners_unique_pct", "winners_dup_max",
                 "winner_entry", "n_slate_defining", "source_file"]
    with (outdir / "slates.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flat_cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x["year"], x["week"])):
            w.writerow(r)

    print("\n" + "=" * 60)
    small = [r for r in rows if r["field_size"] < SMALL_FIELD_MAX]
    large = [r for r in rows if r["field_size"] >= SMALL_FIELD_MAX]
    print(f"Files: {len(files)} | mined: {len(rows)} (small {len(small)} / large {len(large)}) | "
          f"failed: {len(failures)} | unmatched-name: {len(unparsed)}")
    for name, err in failures:
        print(f"  FAIL {name}: {err}")
    for n in unparsed:
        print(f"  UNMATCHED {n}")

    def agg(rs, label):
        print(f"\n--- {label} (n={len(rs)}) ---")
        if not rs:
            return
        ws = [r["winning_score"] for r in rs if r["winning_score"] is not None]
        print(f"  field size: median {median([r['field_size'] for r in rs]):,.0f}")
        print(f"  winning score: median {median(ws):.1f} (min {min(ws):.0f} / max {max(ws):.0f})")
        wp = [r["winner_profile"] for r in rs if r["winner_profile"]]
        if wp:
            e = _mean_env(wp)
            print(f"  rank-1 winner: own/slot {e['own_per_slot']}, sub-5% piece {e['leverage_pct']}%, "
                  f"anchor exposure {e['anchor_exposure']}, unique {e['unique_pct']}%")
        tp = [r["top10_profile"] for r in rs if r["top10_profile"]]
        if tp:
            e = _mean_env(tp)
            print(f"  top-10 cohort: own/slot {e['own_per_slot']}, sub-5% {e['leverage_pct']}%, "
                  f"anchor {e['anchor_exposure']}, unique {e['unique_pct']}%")
        sp = [r["shark_profile"] for r in rs if r["shark_profile"]]
        print(f"  contests with a tracked shark: {len(sp)}"
              + (f" — shark envelope {_mean_env(sp)}" if sp else ""))
        up = [r["user_profile"] for r in rs if r["user_profile"]]
        print(f"  contests with the user: {len(up)}"
              + (f" — user envelope {_mean_env(up)}" if up else ""))
        ao = [r["winners_avg_own"] for r in rs if r.get("winners_avg_own") is not None]
        if ao:
            print(f"  top-N winners avg-own: median {median(ao):.1f}% | <10% count median "
                  f"{median([r['winners_low_own_mean'] for r in rs if r.get('winners_low_own_mean') is not None]):.2f}")

    agg(small, "SMALL FIELD (<10k)")
    agg(large, "LARGE FIELD")
    block = seed_baseline(rows, reseed)
    if block:
        print(f"\nSeeded shark_baseline.json sports.{SPORT_KEY}: {json.dumps(block, indent=1)}")
    print("\nWrote rules/nfl_classic/_mining/slates.{json,csv}")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception:
        traceback.print_exc()
        sys.exit(1)
