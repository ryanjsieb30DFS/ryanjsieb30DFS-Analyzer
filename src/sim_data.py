"""Generic sim-data store.

Replaces the old SaberSim-specific ingestion. The user uploads any sim export
(e.g. a SaberSim lineup CSV); we store the raw file as-is and compute a light
summary (row/col counts, column names, a small preview) so Claude can read the
raw file later when writing the slate analysis. No fuzzy column detection, no
DK-ID matching, no build-rules generation — just store + summarize.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

_SIM_DIR = Path(__file__).parent.parent / "data" / "sim_data"


def _summary_path(slug: str) -> Path:
    return _SIM_DIR / f"{slug}_summary.json"


def save_sim(slug: str, uploaded_file) -> dict:
    """Write the raw upload to disk and persist a light summary. Returns the summary."""
    _SIM_DIR.mkdir(parents=True, exist_ok=True)

    # Clear any previously stored sim file for this slug so only the latest remains.
    clear_sim(slug)

    raw = uploaded_file.read()
    dest = _SIM_DIR / f"{slug}__{uploaded_file.name}"
    dest.write_bytes(raw)

    summary: dict = {
        "filename": uploaded_file.name,
        "path": str(dest),
        "n_rows": 0,
        "n_cols": 0,
        "columns": [],
        "preview": [],
    }
    try:
        df = pd.read_csv(dest)
        summary["n_rows"] = int(len(df))
        summary["n_cols"] = int(df.shape[1])
        summary["columns"] = [str(c) for c in df.columns]
        summary["preview"] = df.head(5).to_dict(orient="records")
    except Exception as exc:  # noqa: BLE001 — store what we can; a bad CSV shouldn't crash the UI
        summary["error"] = f"Could not parse as CSV: {exc}"

    _summary_path(slug).write_text(json.dumps(summary, default=str, indent=2))
    return summary


def load_sim_summary(slug: str) -> dict | None:
    """Return the stored summary dict, or None if no sim data exists for this slug."""
    p = _summary_path(slug)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def clear_sim(slug: str) -> None:
    """Delete the slug's stored sim file(s) + summary. Safe if nothing exists."""
    if not _SIM_DIR.exists():
        return
    for f in _SIM_DIR.glob(f"{slug}__*"):
        f.unlink()
    p = _summary_path(slug)
    if p.exists():
        p.unlink()
