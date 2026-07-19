"""Saved contest templates — reusable per-sport contest presets.

The user enters the same recurring DK contests every slate (e.g. "NASCAR $5K
Chin Music"). A template stores a contest's stable identity (name, type,
entry caps/fees) plus typical defaults for the two fields that vary slate to
slate (field size, my entries), so the contest can be re-added from a
dropdown instead of retyped. Templates persist in their own file and survive
slate clears and autopsy logs (which only clear data/contests/<slug>.json).
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path


_TEMPLATES_DIR = Path(__file__).parent.parent / "data" / "contest_templates"


def _path(slug: str) -> Path:
    return _TEMPLATES_DIR / f"{slug}.json"


def _norm(name) -> str:
    return str(name).strip().casefold()


def load_templates(slug: str) -> list[dict]:
    p = _path(slug)
    if not p.exists():
        return []
    return json.loads(p.read_text()).get("templates", [])


def _save(slug: str, templates: list[dict]) -> None:
    _TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps({"templates": templates}, indent=2))


def save_template(slug: str, template: dict) -> None:
    """Save (or update) a template. Dedup by case-insensitive name: an existing
    template with the same name is overwritten in place (keeping its id)."""
    templates = load_templates(slug)
    template = dict(template)
    for existing in templates:
        if _norm(existing.get("name")) == _norm(template.get("name")):
            template["id"] = existing.get("id", uuid.uuid4().hex[:8])
            existing.clear()
            existing.update(template)
            _save(slug, templates)
            return
    template["id"] = uuid.uuid4().hex[:8]
    templates.append(template)
    _save(slug, templates)


def remove_template(slug: str, template_id: str) -> None:
    templates = [t for t in load_templates(slug) if t.get("id") != template_id]
    _save(slug, templates)
