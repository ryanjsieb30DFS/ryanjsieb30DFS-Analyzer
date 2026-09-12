"""`## Build rules` — the strategy's machine-readable rule block (9/12/26).

The Sim's Filter gate enforces ONLY what this block carries, so the parser
must (1) read exactly what the strategy wrote, (2) drop a rule it cannot
check (unknown player) and SAY so, and (3) ride the contract."""
import json

import pandas as pd

from src.autopsy import _norm_name
from src.strategy_contract import parse_build_rules, write_contract

_NAMES = ["Tommy Gantt", "Jean Silva", "Ignacio Bahamondes", "Yousri Belgaroui",
          "Tommy McMillen", "JJ Aldrich"]
_UNI = {_norm_name(n): n for n in _NAMES}

_MD = """# MMA slate strategy — test card
## Build it like a sharp
1. one twin at most.
## Build rules
```yaml
lineup_rules:
  - rule: at_most
    count: 1
    players: [Tommy Gantt, Jean Silva]
    why: one twin per lineup
    from: strategy
  - rule: salary_min
    value: 49500
    why: the sharp leaves no more than $500
  - rule: at_least
    count: 1
    players: [Nobody Real]
portfolio_rules:
  - rule: min_entries_with
    count: 1
    players: [Ignacio Bahamondes, Yousri Belgaroui]
    why: anchor-equivalence — the alternative anchor runs somewhere
    from: mma-se-2026-05-30-anchor-equiv
  - rule: max_entries_with
    count: 1
    players: [JJ Aldrich]
    why: darts are a rate
  - rule: max_exposure_pct
    player: Jean Silva
    value: 60
```
"""


def test_parse_reads_lineup_and_portfolio_rules_and_drops_unknown_players():
    out = parse_build_rules(_MD, _UNI)
    assert out["present"] is True
    rules = {(r["rule"], tuple(r.get("players") or ())) for r in out["lineup_rules"]}
    assert ("at_most", ("Tommy Gantt", "Jean Silva")) in rules
    assert any(r["rule"] == "salary_min" and r["value"] == 49500 for r in out["lineup_rules"])
    # The unknown-player rule is DROPPED and reported, never half-enforced.
    assert not any("Nobody Real" in (r.get("players") or []) for r in out["lineup_rules"])
    assert any("Nobody Real" in e for e in out["errors"])
    prules = {r["rule"]: r for r in out["portfolio_rules"]}
    assert prules["min_entries_with"]["players"] == ["Ignacio Bahamondes", "Yousri Belgaroui"]
    assert prules["min_entries_with"]["from"] == "mma-se-2026-05-30-anchor-equiv"
    assert prules["max_entries_with"]["count"] == 1
    assert prules["max_exposure_pct"]["player"] == "Jean Silva"
    assert prules["max_exposure_pct"]["value"] == 60


def test_no_block_is_absent_not_empty():
    out = parse_build_rules("# T\n## Build it like a sharp\nwords\n", _UNI)
    assert out["present"] is False and out["lineup_rules"] == [] and out["errors"] == []


def test_empty_block_is_present_and_honest():
    md = "# T\n## Build rules\n```yaml\nlineup_rules: []\nportfolio_rules: []\n```\n"
    out = parse_build_rules(md, _UNI)
    assert out["present"] is True and out["lineup_rules"] == [] and out["portfolio_rules"] == []


def test_contract_carries_the_block(tmp_path, monkeypatch):
    import src.strategy_contract as sc
    monkeypatch.setattr(sc, "_CONTRACT_DIR", tmp_path)
    df = pd.DataFrame([{"name": n, "salary": 8000, "proj_points": 70.0, "ownership": 20.0}
                       for n in _NAMES])
    p = write_contract("mma_se", _MD, {"src.csv": {"vendor": "DailyFan MMA", "df": df}})
    d = json.loads(p.read_text())
    assert d["build_rules"]["present"] is True
    assert any(r["rule"] == "at_most" for r in d["lineup_rules"])
    assert len(d["portfolio_rules"]) == 3
    assert any("Nobody Real" in e for e in d["build_rules"]["errors"])
