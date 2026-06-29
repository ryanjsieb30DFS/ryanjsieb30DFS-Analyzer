"""Read the per-sport custom-metric registry (`rules/<slug>/metrics.yaml`).

Metrics are authored in SaberSim and recorded here (definition + changelog); this
module just reads them so the Sim Data tab can list them and map a metric to its
export column. The Analyzer never scores/builds lineups.
"""
from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent


def _path(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "metrics.yaml"


def list_metrics(slug: str) -> list[dict]:
    """All recorded metrics for the sport (empty list if none / unparseable)."""
    p = _path(slug)
    if not p.exists():
        return []
    try:
        import yaml
        data = yaml.safe_load(p.read_text()) or {}
    except Exception:  # noqa: BLE001 — never break the UI on a bad file
        return []
    return data.get("metrics") or []


def get_metric(slug: str, metric_id: str) -> dict | None:
    return next((m for m in list_metrics(slug) if m.get("id") == metric_id), None)
