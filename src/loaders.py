"""Slate-folder loaders.

Given a slate folder, walk inputs/ and return normalized dataframes per vendor
using vendors.detect_vendor + vendors.normalize_to_canonical.
"""
from pathlib import Path
import pandas as pd
from . import vendors


def load_projections(slate_dir: Path) -> dict[str, pd.DataFrame]:
    """Return {source_filename: canonical_df} for every CSV in inputs/projections/."""
    out = {}
    proj_dir = Path(slate_dir) / "inputs" / "projections"
    if not proj_dir.exists():
        return out
    for csv in sorted(proj_dir.glob("*.csv")):
        df = pd.read_csv(csv)
        sig = vendors.detect_vendor(df)
        if sig is None:
            continue
        out[csv.name] = vendors.normalize_to_canonical(df, sig)
    return out


def list_research(slate_dir: Path) -> dict[str, list[Path]]:
    base = Path(slate_dir) / "inputs" / "research"
    return {
        "articles": sorted((base / "articles").glob("*")) if (base / "articles").exists() else [],
        "podcasts": sorted((base / "podcasts").glob("*")) if (base / "podcasts").exists() else [],
        "notes": sorted((base / "notes").glob("*")) if (base / "notes").exists() else [],
    }
