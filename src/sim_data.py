"""Generic lineup-pool / sim-data store.

The user uploads one or more lineup-pool CSVs — a SaberSim export (with sim
metrics), or a traditional optimizer's lineup files (proj-/ceiling-/50-50-
optimized, often WITHOUT sims), possibly several at once. We store each raw file
as-is and keep a light per-file summary (row/col counts, column names, a small
preview, and whether it carries sim metrics) so Claude can read the raw files
later when selecting lineups. No fuzzy column detection, no DK-ID matching here —
just store + summarize.

Multiple files coexist per slug. The manifest at `<slug>_summary.json` holds
`{"files": [entry, ...]}`. An older single-dict manifest is read transparently.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

_SIM_DIR = Path(__file__).parent.parent / "data" / "sim_data"

# Column-name fragments that mark a file as carrying sim metrics (vs rosters only).
_SIM_COL_MARKERS = ("roi", "saber", "percentile", "win rate", "sim dupes", "sim optimals")


def _summary_path(slug: str) -> Path:
    return _SIM_DIR / f"{slug}_summary.json"


def _has_sim_cols(columns: list[str]) -> bool:
    lowered = [str(c).lower() for c in columns]
    return any(any(m in c for m in _SIM_COL_MARKERS) for c in lowered) or \
        any(c in {"95th", "99th", "85th"} for c in lowered)


def _summarize(filename: str, dest: Path) -> dict:
    entry: dict = {
        "filename": filename,
        "path": str(dest),
        "n_rows": 0,
        "n_cols": 0,
        "columns": [],
        "has_sim_cols": False,
        "preview": [],
    }
    try:
        df = pd.read_csv(dest)
        entry["n_rows"] = int(len(df))
        entry["n_cols"] = int(df.shape[1])
        entry["columns"] = [str(c) for c in df.columns]
        entry["has_sim_cols"] = _has_sim_cols(entry["columns"])
        entry["preview"] = df.head(5).to_dict(orient="records")
    except Exception as exc:  # noqa: BLE001 — store what we can; a bad CSV shouldn't crash the UI
        entry["error"] = f"Could not parse as CSV: {exc}"
    return entry


def _read_manifest(slug: str) -> dict:
    """Return {"files": [...]}, transparently wrapping the old single-dict shape."""
    p = _summary_path(slug)
    if not p.exists():
        return {"files": []}
    data = json.loads(p.read_text())
    if isinstance(data, dict) and "files" in data:
        return data
    # Legacy single-file manifest (top-level filename/path) — wrap it.
    if isinstance(data, dict) and data.get("filename"):
        data.setdefault("has_sim_cols", _has_sim_cols(data.get("columns", [])))
        return {"files": [data]}
    return {"files": []}


def _write_manifest(slug: str, files: list[dict]) -> None:
    _SIM_DIR.mkdir(parents=True, exist_ok=True)
    _summary_path(slug).write_text(json.dumps({"files": files}, default=str, indent=2))


def save_sim(slug: str, uploaded_file) -> dict:
    """Store one uploaded lineup-pool file (APPENDING — multiple coexist per slug).

    Re-uploading the same filename replaces that entry. Returns the file's summary.
    """
    _SIM_DIR.mkdir(parents=True, exist_ok=True)
    raw = uploaded_file.read()
    dest = _SIM_DIR / f"{slug}__{uploaded_file.name}"
    dest.write_bytes(raw)

    entry = _summarize(uploaded_file.name, dest)
    files = [f for f in _read_manifest(slug)["files"] if f.get("filename") != uploaded_file.name]
    files.append(entry)
    _write_manifest(slug, files)
    return entry


def load_sim_files(slug: str) -> list[dict]:
    """Return all stored lineup-pool file summaries for the slug (oldest first).

    Drops manifest entries whose raw file no longer exists on disk. Empty list if
    none. Reads transparently across the new multi-file and legacy single-file
    manifest shapes (pure read — never rewrites)."""
    files = _read_manifest(slug)["files"]
    return [f for f in files if f.get("path") and Path(f["path"]).exists()]


def load_sim_summary(slug: str) -> dict | None:
    """Back-compat shim: the first stored file, or None. Prefer load_sim_files."""
    files = load_sim_files(slug)
    return files[0] if files else None


def drop_sim_file(slug: str, filename: str) -> None:
    """Delete one stored lineup-pool file + its manifest entry. Safe if absent."""
    dest = _SIM_DIR / f"{slug}__{filename}"
    if dest.exists():
        dest.unlink()
    remaining = [f for f in _read_manifest(slug)["files"] if f.get("filename") != filename]
    if remaining:
        _write_manifest(slug, remaining)
    else:
        clear_sim(slug)


def clear_sim(slug: str) -> None:
    """Delete ALL of the slug's stored lineup-pool files + manifest. Safe if none."""
    if not _SIM_DIR.exists():
        return
    for f in _SIM_DIR.glob(f"{slug}__*"):
        f.unlink()
    p = _summary_path(slug)
    if p.exists():
        p.unlink()
