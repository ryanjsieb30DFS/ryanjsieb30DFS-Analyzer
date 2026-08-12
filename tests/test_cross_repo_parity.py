"""Cross-repo parity guard (8/10/26).

The Sim repo and this repo deliberately keep NO shared package (user
decision) — a handful of constants and one function are duplicated instead.
This suite locks the duplicates together so a one-sided edit fails loudly
with a message naming the file to port the change to.

The Sim's modules are NOT imported (both repos use the `src` package name —
importing would silently mix the two repos). Values are extracted from the
Sim's SOURCE via ast; `_norm_name` is compared BEHAVIORALLY over a fixture
list, so comment/docstring drift never false-alarms.

Skips cleanly when the Sim repo is absent (CI or another machine).
"""
from __future__ import annotations

import ast
import re
import unicodedata

import pytest

from src.sim_link import sim_root

SIM = sim_root()

pytestmark = pytest.mark.skipif(SIM is None, reason="Sim repo not present")


# ---------------------------------------------------------------------------
# ast extraction helpers
# ---------------------------------------------------------------------------

def _module_tree(rel_path: str):
    text = (SIM / rel_path).read_text()
    return text, ast.parse(text)


def _extract_literal(rel_path: str, name: str):
    """The literal value of a top-level `name = <literal>` assign in a Sim file."""
    _, tree = _module_tree(rel_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if name in targets:
                return ast.literal_eval(node.value)
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.target.id == name and node.value is not None:
            return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found as a literal in Sim {rel_path}")


def _extract_function(rel_path: str, fn_name: str, const_names: set):
    """Exec a Sim top-level function + the named module constants it uses,
    in a namespace with re/unicodedata provided. Returns the function."""
    text, tree = _module_tree(rel_path)
    pieces = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in const_names
                for t in node.targets):
            pieces.append(ast.get_source_segment(text, node))
        if isinstance(node, ast.FunctionDef) and node.name == fn_name:
            pieces.append(ast.get_source_segment(text, node))
    assert pieces, f"{fn_name} not found in Sim {rel_path}"
    ns = {"re": re, "unicodedata": unicodedata}
    exec("\n\n".join(pieces), ns)  # noqa: S102 — our own source, test-only
    return ns[fn_name]


# ---------------------------------------------------------------------------
# _norm_name — the join key for EVERY cross-repo player match
# ---------------------------------------------------------------------------

# Names that exercise every branch: accents, stroked letters, nicknames,
# suffixes, hyphens, apostrophes, periods, casefold.
_TRICKY_NAMES = [
    "Nicolai Højgaard",
    "Nicolai Hojgaard",
    "Bryson DeChambeau",
    "Matt Fitzpatrick Jr.",
    "Frankie Corrales III",
    'Dustin "The Diamond" Poirier',
    "Jean-Charles Valladon",
    "Ludvig Åberg",
    "Joaquin Niemann",
    "O'Hair, Sean",
    "sean o'hair",
    "St. John Smythe",
    "Erik van Rooyen",
    "Đorđe Petrović",
    "Kyle Larson",
]


def test_norm_name_behavior_matches():
    sim_fn = _extract_function(
        "src/vendor_calibration.py", "_norm_name",
        {"_SUFFIXES", "_LETTER_FOLD"})
    from src.autopsy import _norm_name as ana_fn
    for name in _TRICKY_NAMES:
        assert sim_fn(name) == ana_fn(name), (
            f"_norm_name diverged on {name!r}: Sim -> {sim_fn(name)!r}, "
            f"Analyzer -> {ana_fn(name)!r}. Port the change to the other repo "
            "(Sim src/vendor_calibration.py <-> Analyzer src/autopsy.py) — "
            "this function is the join key for every cross-repo player match."
        )


# ---------------------------------------------------------------------------
# Salary cap
# ---------------------------------------------------------------------------

def test_salary_cap_matches():
    sim_cap = _extract_literal("src/optimize.py", "SALARY_CAP")
    from src.grader import _SALARY_CAP as ana_cap
    assert sim_cap == ana_cap, (
        f"Salary cap drifted: Sim optimize.py SALARY_CAP={sim_cap} vs "
        f"Analyzer grader.py _SALARY_CAP={ana_cap}. Fix whichever is wrong."
    )


# ---------------------------------------------------------------------------
# Field-size bands (2,500 / 10,000)
# ---------------------------------------------------------------------------

def test_size_bands_match():
    sim_bands = _extract_literal("src/rules.py", "SIZE_BANDS")
    cuts = sorted(hi for hi, _label in sim_bands)

    from src.lineup_selection import _PLAYS_LIKE_SE_FIELD
    assert _PLAYS_LIKE_SE_FIELD == cuts[0], (
        f"lineup_selection._PLAYS_LIKE_SE_FIELD={_PLAYS_LIKE_SE_FIELD} no "
        f"longer matches the Sim's small-band cut {cuts[0]} "
        "(Sim src/rules.py SIZE_BANDS). Port the change."
    )

    # sim_link.dupe_correction hardcodes the same cut points inline; they must
    # track the Sim's SIZE_BANDS or a fitted band gets applied to a size it
    # was never fitted on.
    import inspect
    from src import sim_link
    src_text = inspect.getsource(sim_link.dupe_correction)
    numbers = {int(n.replace("_", "")) for n in re.findall(r"\b\d[\d_]{2,}\b", src_text)}
    for cut in cuts:
        assert cut in numbers, (
            f"Analyzer sim_link.dupe_correction no longer references the Sim "
            f"band cut {cut} (Sim src/rules.py SIZE_BANDS={sim_bands}). "
            "Update its inline band literals."
        )


# ---------------------------------------------------------------------------
# Contest-type vocabulary (the 150max class of drift)
# ---------------------------------------------------------------------------

def test_sim_mode_map_covers_analyzer_type_map():
    sim_modes = _extract_literal("src/analyzer_link.py", "_MODE_BY_CONTEST_TYPE")
    from src.lineup_selection import _TYPE_MAP
    missing = set(_TYPE_MAP) - set(sim_modes)
    assert not missing, (
        f"Sim analyzer_link._MODE_BY_CONTEST_TYPE is missing contest types "
        f"the Analyzer knows: {sorted(missing)}. A missing key silently falls "
        "back to the small_field rule pack (the 150max bug, fixed 8/10/26) — "
        "add the key to the Sim's map."
    )


# ---------------------------------------------------------------------------
# Slug -> sport maps (key sets only — pga_rd4_sd VALUES differ on purpose:
# the Analyzer maps it to 'golf_showdown' so RD4 SD can never inherit PGA
# Classic's dupe-correction factor; the Sim maps it to 'golf' for its own
# fit scripts. Documented in Analyzer src/sim_link.py.)
# ---------------------------------------------------------------------------

def test_slug_maps_cover_same_slugs():
    contest_types = _extract_literal("src/rules.py", "CONTEST_TYPES")
    sim_slugs = set()
    for entry in contest_types.values():
        sim_slugs.add(entry["slug"])
        sim_slugs.update((entry.get("variants") or {}).values())

    from src.sim_link import _SLUG_SPORT
    # Every Analyzer slug must exist in the Sim (mma_mme is Sim-only, so the
    # Sim may know MORE slugs than the Analyzer — that direction is fine).
    missing = set(_SLUG_SPORT) - sim_slugs
    assert not missing, (
        f"Analyzer sim_link._SLUG_SPORT names slugs the Sim doesn't have: "
        f"{sorted(missing)} (Sim src/rules.py CONTEST_TYPES). Align the maps."
    )
