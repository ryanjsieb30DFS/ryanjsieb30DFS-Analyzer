"""Static check that app.py has no undefined module-level names.

This exists because of a real mid-slate crash: `board_tier_map` was called at
app.py module scope but never added to the `from src.analyzer_link import (...)`
block. It shipped in commit 0108be3 and stayed invisible for a day — the running
Streamlit process had been started before that commit, and Streamlit caches `src`
modules, so the module body never re-executed. The first restart crashed the app
on load with `NameError: name 'board_tier_map' is not defined`.

The 374-test suite could not have caught it: nothing else in tests/ touches
app.py at all, so the entire Streamlit layer had zero import-time coverage.

We deliberately do NOT import app.py — a Streamlit module body needs a script
runner and would fail for unrelated reasons. A static AST parse is enough for
this bug class, and it is fast and dependency-free.
"""
from __future__ import annotations

import ast
import builtins
from pathlib import Path

APP = Path(__file__).parent.parent / "app.py"


def _module_level_bindings(tree: ast.Module) -> set[str]:
    """Every name bound at module scope, plus builtins.

    Walks the full subtree of each top-level statement so that names bound
    inside `if`/`try`/`with`/`for` blocks still count — those execute at module
    level too.
    """
    bound = set(dir(builtins)) | {"__file__", "__name__", "__doc__"}
    for node in tree.body:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Import):
                for a in sub.names:
                    bound.add((a.asname or a.name).split(".")[0])
            elif isinstance(sub, ast.ImportFrom):
                for a in sub.names:
                    bound.add(a.asname or a.name)
            elif isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                bound.add(sub.name)
            elif isinstance(sub, ast.Name) and isinstance(sub.ctx, (ast.Store, ast.Del)):
                bound.add(sub.id)
            elif isinstance(sub, ast.ExceptHandler) and sub.name:
                bound.add(sub.name)
    return bound


def _module_level_loads(node: ast.AST):
    """Name loads that actually execute at MODULE level.

    Skipping function/class/lambda bodies is what makes this precise: their
    parameters and locals are bound in their own scope, and treating them as
    module names produced 18 false positives on the first attempt at this check
    (`tab_purpose`, `sport_slug`, `done`/`total`, …). Only module-scope loads can
    raise the NameError this test guards against.
    """
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                         ast.ClassDef, ast.Lambda)):
        return
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        yield node
    for child in ast.iter_child_nodes(node):
        yield from _module_level_loads(child)


def undefined_module_names(path: Path) -> dict[str, int]:
    """{name: first line} for module-level loads that are never bound."""
    tree = ast.parse(path.read_text())
    bound = _module_level_bindings(tree)
    missing: dict[str, int] = {}
    for node in tree.body:
        for name in _module_level_loads(node):
            if name.id not in bound:
                missing.setdefault(name.id, name.lineno)
    return missing


def test_app_has_no_undefined_module_level_names():
    missing = undefined_module_names(APP)
    assert not missing, (
        "app.py references names at module scope that are never imported or "
        "assigned — the app will crash with NameError on load:\n  "
        + "\n  ".join(f"line {ln}: {nm}" for nm, ln in sorted(missing.items(),
                                                              key=lambda kv: kv[1]))
    )


def test_checker_catches_a_missing_import():
    """Guard the guard: if the detection logic silently broke, the test above
    would pass on a genuinely broken app.py and we'd learn about it mid-slate
    again."""
    import tempfile
    broken = "import os\n\nx = os.getcwd()\ny = never_imported_helper(x)\n"
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(broken)
        tmp = Path(fh.name)
    try:
        missing = undefined_module_names(tmp)
        assert missing == {"never_imported_helper": 4}, missing
    finally:
        tmp.unlink()


def test_function_scoped_names_are_not_flagged():
    """The false-positive class: parameters and locals of nested functions are
    bound in their own scope and must never be reported."""
    import tempfile
    fine = (
        "import os\n\n"
        "def outer(tab_purpose, done, total):\n"
        "    label = f'{tab_purpose} {done}/{total}'\n"
        "    def inner(kind, text):\n"
        "        return f'{kind}:{text}:{label}'\n"
        "    return inner\n\n"
        "for item in os.listdir('.'):\n"
        "    last = item\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(fine)
        tmp = Path(fh.name)
    try:
        assert undefined_module_names(tmp) == {}
    finally:
        tmp.unlink()
