"""NFL Classic pool lock (9/12/26): Claude's board IS the pool; user flips
sit on top; lock writes a HARD pool into the strategy contract."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import pool_lock, pool_calibration, player_pool, sessions  # noqa: E402

_MD = """# NFL Classic — Player pool
Drafted pool, walked QB → DST.

## QB
The KC–LAC game is the shootout.

| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Patrick Mahomes | QB | KC | @LAC | $8,000 | 22.1 | 18% | shootout | Core |
| 2 | Bo Nix | QB | DEN | NYJ | $6,000 | 17.0 | 4% | sneaky | Okay · Leverage |
| 3 | Bad Quarterback | QB | NYJ | @DEN | $5,000 | 12.0 | 1% | no | Fade |

1. **Patrick Mahomes** — write-up — Core

## RB
| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Isiah Pacheco | RB | KC | @LAC | $6,500 | 15.0 | 20% | volume | Good |

## Sources read
All files read.
"""


def _setup(tmp_path, monkeypatch):
    monkeypatch.setattr(player_pool, "_POOL_DIR", tmp_path / "pool")
    monkeypatch.setattr(pool_lock, "_POOL_DIR", tmp_path / "pool")
    monkeypatch.setattr(pool_lock, "_CONTRACT_DIR", tmp_path / "contract")
    monkeypatch.setattr(sessions, "_SESSION_DIR", tmp_path / "sessions")
    player_pool.save_pool("nfl_classic", _MD)
    df = pd.DataFrame([
        {"name": "Patrick Mahomes", "position": "QB", "team": "KC", "opponent": "@LAC",
         "salary": 8000, "proj_points": 22.1, "ownership": 18.0},
        {"name": "Bo Nix", "position": "QB", "team": "DEN", "opponent": "NYJ",
         "salary": 6000, "proj_points": 17.0, "ownership": 4.0},
        {"name": "Bad Quarterback", "position": "QB", "team": "NYJ", "opponent": "@DEN",
         "salary": 5000, "proj_points": 12.0, "ownership": 1.0},
        {"name": "Isiah Pacheco", "position": "RB", "team": "KC", "opponent": "@LAC",
         "salary": 6500, "proj_points": 15.0, "ownership": 20.0},
    ])
    sessions.save_source("nfl_classic", "etr.csv", df, "ETR")


def test_parser_reads_every_position_table_and_leverage():
    rows = pool_calibration.parse_pool_tiers(_MD)
    assert [r["name"] for r in rows] == ["Patrick Mahomes", "Bo Nix", "Bad Quarterback",
                                         "Isiah Pacheco"]
    nix = rows[1]
    assert nix["tier"] == "Okay" and nix["leverage"] is True and nix["pos"] == "QB"
    assert rows[3]["pos"] == "RB" and rows[3]["leverage"] is False


def test_board_rows_join_projections_and_apply_overrides(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    rows = pool_lock.board_rows("nfl_classic")
    assert len(rows) == 4
    m = rows[0]
    assert m["pos"] == "QB" and m["salary"] == 8000 and m["in_pool"] is True
    bad = rows[2]
    assert bad["tier"] == "Fade" and bad["in_pool"] is False
    # The user flips the fade back in and drops Pacheco.
    pool_lock.set_override("nfl_classic", "Bad Quarterback", tier="Okay")
    pool_lock.set_override("nfl_classic", "Isiah Pacheco", tier="Fade", leverage=False)
    rows = pool_lock.board_rows("nfl_classic")
    assert rows[2]["tier"] == "Okay" and rows[2]["in_pool"] and rows[2]["overridden"]
    assert rows[2]["claude_tier"] == "Fade"
    assert rows[3]["in_pool"] is False
    groups = pool_lock.rows_by_position(rows)
    assert list(groups) == ["QB", "RB"]
    summ = pool_lock.pool_summary(rows)
    assert summ["QB"]["in"] == 3 and summ["RB"]["out"] == 1 and summ["total"]["in"] == 3


def test_lock_writes_hard_pool_and_board_into_contract(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    pool_lock.set_override("nfl_classic", "Bo Nix", leverage=False)
    block = pool_lock.lock_pool("nfl_classic")
    assert block["hard"] is True and block["n_in"] == 3 and block["n_out"] == 1
    assert block["by_position"] == {"QB": 2, "RB": 1, "WR": 0, "TE": 0, "DST": 0}
    contract = json.loads((tmp_path / "contract" / "nfl_classic.json").read_text())
    names_in = {p["name"] for p in contract["pool"]["players"] if p["in"]}
    assert names_in == {"Patrick Mahomes", "Bo Nix", "Isiah Pacheco"}
    # The board block reflects the approved tiers + the flipped leverage flag.
    nix = next(b for b in contract["board"] if b["name"] == "Bo Nix")
    assert nix["leverage"] is False and nix["tier"] == "Okay" and nix["pos"] == "QB"
    assert pool_lock.locked_pool("nfl_classic")["n_in"] == 3
    pool_lock.unlock_pool("nfl_classic")
    assert pool_lock.locked_pool("nfl_classic") is None


def test_strategy_contract_board_rows_carry_leverage_and_overrides(tmp_path, monkeypatch):
    """The old _board_rows dropped the leverage flag (parse_pool_tiers had
    already stripped `· Leverage`) — the Sim never saw `· Lev`."""
    _setup(tmp_path, monkeypatch)
    from src import strategy_contract
    rows = strategy_contract._board_rows("nfl_classic")
    nix = next(r for r in rows if r["name"] == "Bo Nix")
    assert nix["leverage"] is True and nix["tier"] == "Okay"
    pool_lock.set_override("nfl_classic", "Bo Nix", tier="Core")
    rows = strategy_contract._board_rows("nfl_classic")
    assert next(r for r in rows if r["name"] == "Bo Nix")["tier"] == "Core"


def test_classic_pool_prompt_is_position_by_position(tmp_path, monkeypatch):
    """The prompt Claude gets for nfl_classic asks for five position sections
    (QB first); other sports keep the single global table."""
    _setup(tmp_path, monkeypatch)
    from src import analysis_runner as ar
    captured = {}

    def _fake(prompt, out_path):
        captured["prompt"] = prompt
        return {"ok": True, "error": None, "duration_s": 0.0, "cost_usd": None}
    monkeypatch.setattr(ar, "_run_claude", _fake)
    monkeypatch.setattr(ar, "build_bundle", lambda *a, **k: tmp_path / "bundle.md")
    from src import slate_analysis
    monkeypatch.setattr(slate_analysis, "load_persisted", lambda slug: None)
    ar.run_player_pool("nfl_classic", "NFL Classic", "nfl")
    p = captured["prompt"]
    for h in ("`## QB`", "`## RB`", "`## WR`", "`## TE`", "`## DST`"):
        assert h in p
    assert "QUARTERBACKS FIRST" in p and "This board IS the pool" in p
    assert "NEVER CREATE LINEUPS" in p
