"""Per-sport session persistence.

One JSON file per contest type at data/sessions/<slug>.json. Stores the
uploaded projection sources for the active slate. Simpler than the sim's
session_store because the Analyzer has no lineup pools.
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


def clear(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()
