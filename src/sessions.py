"""Per-sport session persistence.

One JSON file per contest type at data/sessions/<slug>.json.
Stores the uploaded projection sources for the active slate.
"""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd


_SESSION_DIR = Path(__file__).parent.parent / "data" / "sessions"


def _path(slug: str) -> Path:
    return _SESSION_DIR / f"{slug}.json"


def load(slug: str) -> dict:
    """Return saved session for slug, or empty default."""
    p = _path(slug)
    if not p.exists():
        return {"sources": {}}
    return json.loads(p.read_text())


def save(slug: str, session: dict) -> None:
    _SESSION_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps(session, default=str, indent=2))


def save_source(slug: str, source_name: str, df: pd.DataFrame, vendor: str) -> None:
    """Persist a single projection source under the slug."""
    session = load(slug)
    session.setdefault("sources", {})[source_name] = {
        "vendor": vendor,
        "rows": df.to_dict(orient="records"),
    }
    save(slug, session)


def load_sources(slug: str) -> dict[str, dict]:
    """Return {source_name: {vendor, df}} for the slug."""
    session = load(slug)
    out = {}
    for name, blob in session.get("sources", {}).items():
        out[name] = {
            "vendor": blob.get("vendor"),
            "df": pd.DataFrame(blob.get("rows", [])),
        }
    return out


def drop_source(slug: str, source_name: str) -> None:
    session = load(slug)
    session.get("sources", {}).pop(source_name, None)
    save(slug, session)


def merge_same_vendor(sources: dict[str, dict]) -> dict[str, dict]:
    """Concat sources sharing a vendor into one virtual source.

    SIN ships MLB hitters + pitchers as two files with the same vendor; the
    analysis needs them as a single pool. Single-file vendors pass through
    unchanged, preserving upload order.
    """
    by_vendor: dict[str, list[tuple[str, pd.DataFrame]]] = {}
    for name, blob in sources.items():
        by_vendor.setdefault(blob.get("vendor"), []).append((name, blob["df"]))

    out: dict[str, dict] = {}
    for vendor, group in by_vendor.items():
        if len(group) == 1:
            name, df = group[0]
            out[name] = {"vendor": vendor, "df": df}
            continue
        combined = pd.concat([df for _, df in group], ignore_index=True)
        # Two-way-player guard: keep the higher-projected row per name
        combined = (
            combined.sort_values("proj_points", ascending=False)
            .drop_duplicates(subset="name", keep="first")
            .reset_index(drop=True)
        )
        out[f"{vendor} — combined ({len(group)} files)"] = {
            "vendor": vendor,
            "df": combined,
        }
    return out


def save_team_data(slug: str, filename: str, df: pd.DataFrame, vendor: str) -> None:
    """Persist team-level data (e.g. SIN MLB stack rankings) as a side-channel."""
    session = load(slug)
    session["team_data"] = {
        "filename": filename,
        "vendor": vendor,
        "rows": df.to_dict(orient="records"),
    }
    save(slug, session)


def load_team_data(slug: str) -> pd.DataFrame | None:
    """Return the stored team-level DataFrame, or None if absent."""
    blob = load(slug).get("team_data")
    if not blob:
        return None
    df = pd.DataFrame(blob.get("rows", []))
    df.attrs["filename"] = blob.get("filename")
    df.attrs["vendor"] = blob.get("vendor")
    return df


def drop_team_data(slug: str) -> None:
    session = load(slug)
    session.pop("team_data", None)
    save(slug, session)


def clear(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()
