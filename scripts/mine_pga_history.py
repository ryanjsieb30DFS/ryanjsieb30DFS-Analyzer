"""One-time miner for 2023-2026 PGA DK contest-standings.

Reads the user's historical contest-standings CSVs (read-only, outside the repo),
reuses src/autopsy.py to extract projection-free winning-lineup STRUCTURE per
contest, and writes tidy per-slug datasets the framework-lesson synthesis reads.

Run:  .venv/bin/python scripts/mine_pga_history.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
import traceback
from collections import Counter
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd  # noqa: E402
from src.autopsy import parse_dk_results, analyze_contest  # noqa: E402

SRC = Path.home() / "Desktop" / "DFS" / "DFS PGA Past Slate Data"
REPO = Path(__file__).resolve().parent.parent

FNAME_RE = re.compile(r"^(\d{2}-\d{2}-\d{4})\s+(.*?)\s+(R4 SD|Classic)$")


def parse_filename(stem: str):
    m = FNAME_RE.match(stem.strip())
    if not m:
        return None
    date, tourney, fmt = m.group(1), m.group(2).strip(), m.group(3)
    slug = "pga_rd4_sd" if fmt == "R4 SD" else "pga_classic"
    year = date.split("-")[2]
    # Normalize a few tournament-name quirks for grouping.
    tourney = tourney.replace("Farmer_s", "Farmers").replace("  ", " ").strip()
    tourney_key = re.sub(r"^(The|the)\s+", "", tourney)
    return {"date": date, "year": year, "tournament": tourney_key, "format": fmt, "slug": slug}


def mine_one(path: Path) -> dict | None:
    parsed = parse_dk_results(str(path))
    lineups = parsed["lineups"]
    pts = pd.to_numeric(lineups["Points"], errors="coerce").dropna()
    res = analyze_contest(parsed, None, "golf")
    ws = res["winners_summary"]
    wdf = res["winners_df"]
    # Rank-1 winning lineup detail.
    win_row = wdf.loc[wdf["rank"].idxmin()] if not wdf.empty else None
    winner_lineup = list(win_row["players"]) if win_row is not None else []
    return {
        "field_size": int(len(lineups)),
        "winning_score": round(float(pts.max()), 2) if len(pts) else None,
        "cash_line_p80": round(float(pts.quantile(0.20)), 2) if len(pts) else None,  # rank-based: top 20% cash ~ 80th pct of scores
        "median_score": round(float(pts.median()), 2) if len(pts) else None,
        "top_n": ws.get("top_n"),
        "winners_avg_own": ws.get("avg_own_mean"),
        "winners_low_own_mean": ws.get("low_own_count_mean"),
        "winners_unique_pct": ws.get("unique_pct"),
        "winners_dup_max": ws.get("dup_max"),
        "winner_avg_own": round(float(win_row["avg_own"]), 2) if win_row is not None and pd.notna(win_row["avg_own"]) else None,
        "winner_low_own_count": int(win_row["low_own_count"]) if win_row is not None and pd.notna(win_row["low_own_count"]) else None,
        "winner_lineup": winner_lineup,
        "n_slate_defining": len(res["slate_defining"]),
        "slate_defining": [
            {"name": d["name"], "own": d["actual_own"], "fpts": d["actual_fpts"], "top_pct": d["top_lineup_pct"]}
            for d in res["slate_defining"]
        ],
    }


def main():
    files = sorted(SRC.glob("*.csv"))
    by_slug: dict[str, list[dict]] = {"pga_classic": [], "pga_rd4_sd": []}
    failures: list[tuple[str, str]] = []
    unparsed_names: list[str] = []

    for i, path in enumerate(files, 1):
        meta = parse_filename(path.stem)
        if not meta:
            unparsed_names.append(path.name)
            continue
        try:
            row = mine_one(path)
        except Exception as exc:  # noqa: BLE001
            failures.append((path.name, f"{type(exc).__name__}: {exc}"))
            continue
        row.update(meta)
        row["source_file"] = path.name
        by_slug[meta["slug"]].append(row)
        if i % 50 == 0:
            print(f"  ...{i}/{len(files)}")

    for slug, rows in by_slug.items():
        outdir = REPO / "rules" / slug / "_mining"
        outdir.mkdir(parents=True, exist_ok=True)
        # JSON (full, incl. winner lineup + slate-defining)
        (outdir / "slates.json").write_text(json.dumps(rows, indent=2, default=str))
        # CSV (flat scalar columns)
        flat_cols = ["date", "year", "tournament", "slug", "field_size", "winning_score",
                     "cash_line_p80", "median_score", "top_n", "winners_avg_own",
                     "winners_low_own_mean", "winners_unique_pct", "winners_dup_max",
                     "winner_avg_own", "winner_low_own_count", "n_slate_defining", "source_file"]
        with (outdir / "slates.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=flat_cols, extrasaction="ignore")
            w.writeheader()
            for r in sorted(rows, key=lambda x: x["date"]):
                w.writerow(r)

    # ---- summary ----
    print("\n" + "=" * 60)
    print(f"Files: {len(files)} | parsed Classic: {len(by_slug['pga_classic'])} | "
          f"parsed RD4 SD: {len(by_slug['pga_rd4_sd'])} | failed: {len(failures)} | "
          f"unmatched-name: {len(unparsed_names)}")
    if failures:
        print("\nFAILURES:")
        for name, err in failures[:30]:
            print(f"  - {name}: {err}")
    if unparsed_names:
        print("\nUNMATCHED FILENAMES:")
        for n in unparsed_names[:20]:
            print(f"  - {n}")

    def agg(rows, label):
        ao = [r["winners_avg_own"] for r in rows if r["winners_avg_own"] is not None]
        lo = [r["winners_low_own_mean"] for r in rows if r["winners_low_own_mean"] is not None]
        up = [r["winners_unique_pct"] for r in rows if r["winners_unique_pct"] is not None]
        wlo = [r["winner_low_own_count"] for r in rows if r["winner_low_own_count"] is not None]
        ws = [r["winning_score"] for r in rows if r["winning_score"] is not None]
        print(f"\n--- {label} (n={len(rows)}) ---")
        if ao: print(f"  winners avg-own:   median {median(ao):.1f}%  (min {min(ao):.1f} / max {max(ao):.1f})")
        if lo: print(f"  winners <10% count: median {median(lo):.2f} of 6")
        if up: print(f"  winners unique%:   median {median(up):.0f}%")
        if wlo:
            c = Counter(wlo)
            print(f"  rank-1 #sub-10% golfers: " + ", ".join(f"{k}:{c[k]}" for k in sorted(c)))
            print(f"    -> winners w/ >=1 sub-10%: {sum(1 for x in wlo if x>=1)/len(wlo)*100:.0f}% | >=2: {sum(1 for x in wlo if x>=2)/len(wlo)*100:.0f}%")
        if ws: print(f"  winning score:     median {median(ws):.1f}  (min {min(ws):.0f} / max {max(ws):.0f})")

    agg(by_slug["pga_classic"], "PGA CLASSIC")
    agg(by_slug["pga_rd4_sd"], "PGA RD4 SD")
    print("\nWrote rules/<slug>/_mining/slates.{json,csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
