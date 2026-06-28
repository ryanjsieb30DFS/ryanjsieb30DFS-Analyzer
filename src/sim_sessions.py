"""Persist the uploaded SaberSim pool + optional DK Name+ID map per slug.

Stored under data/sim_data/<slug>__pool.csv (+ __dkmap.csv). Per-slate: cleared
with the slate (sidebar Clear + autopsy log) alongside the Claude sim summary at
data/sim_analysis/<slug>.md.
"""
from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
_DIR = _REPO_ROOT / "data" / "sim_data"
_ANALYSIS_DIR = _REPO_ROOT / "data" / "sim_analysis"


def _pool_path(slug: str) -> Path:
    return _DIR / f"{slug}__pool.csv"


def _dkmap_path(slug: str) -> Path:
    return _DIR / f"{slug}__dkmap.csv"


def analysis_path(slug: str) -> Path:
    return _ANALYSIS_DIR / f"{slug}.md"


def save_pool(slug: str, uploaded_file) -> Path:
    _DIR.mkdir(parents=True, exist_ok=True)
    p = _pool_path(slug)
    p.write_bytes(uploaded_file.getvalue())
    return p


def save_dkmap(slug: str, uploaded_file) -> Path:
    _DIR.mkdir(parents=True, exist_ok=True)
    p = _dkmap_path(slug)
    p.write_bytes(uploaded_file.getvalue())
    return p


def pool_path(slug: str) -> Path | None:
    p = _pool_path(slug)
    return p if p.exists() else None


def dkmap_path(slug: str) -> Path | None:
    p = _dkmap_path(slug)
    return p if p.exists() else None


def clear(slug: str) -> None:
    """Remove the pool, DK map, and Claude sim summary for the slug."""
    for p in (_pool_path(slug), _dkmap_path(slug), analysis_path(slug)):
        if p.exists():
            p.unlink()
