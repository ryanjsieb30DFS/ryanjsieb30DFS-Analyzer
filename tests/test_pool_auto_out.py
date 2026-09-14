"""NFL Classic pool auto-out (9/13/26): the ~340-player Classic board timed
out the 20-minute headless run. Players under NFL_CLASSIC_POOL_MIN_PROJ leave
the pool by rule as pre-rendered Fade table rows; Claude ranks + writes up
only the rest (write-ups for Core/Good/Okay only). Other sports unchanged."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import analysis_runner as ar, pool_calibration, pool_lock, player_pool, sessions, strategy_contract  # noqa: E402

# A section with TWO tables (ranked + pasted auto-out), including the
# no-blank-line case the parser must survive.
_TWO_TABLE_MD = """# NFL Classic — Player pool
Drafted pool, walked QB → DST.

## QB
The KC–LAC game is the shootout.

| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Patrick Mahomes | QB | KC | @LAC | $8,000 | 22.1 | 18% | shootout | Core |
| 2 | Bo Nix | QB | DEN | NYJ | $6,000 | 17.0 | 4% | sneaky | Okay · Leverage |
| 3 | Bad Quarterback | QB | NYJ | @DEN | $5,000 | 12.0 | 1% | backup-level arm, no rushing | Fade |

1. **Patrick Mahomes** — write-up — Core
2. **Bo Nix** — write-up — Okay · Leverage

### QB — out of the pool (not written up)
| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |
|---|---|---|---|---|---|---|---|---|---|
| out | Third String | QB | KC | @LAC | $4,000 | 0.4 | 0% | Under 3 projected points | Fade |

## RB
| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Isiah Pacheco | RB | KC | @LAC | $6,500 | 15.0 | 20% | volume | Good |
| Rank | Player | Pos | Team | Opp | Sal | Proj | Own | How it wins | Tier |
|---|---|---|---|---|---|---|---|---|---|
| out | Practice Squad | RB | DEN | NYJ | $4,000 | 1.1 | 0% | Under 3 projected points | Fade |

## Sources read
All files read.
"""


def test_parser_reads_ranked_and_auto_out_tables_once_each():
    rows = pool_calibration.parse_pool_tiers(_TWO_TABLE_MD)
    names = [r["name"] for r in rows]
    assert names == ["Patrick Mahomes", "Bo Nix", "Bad Quarterback", "Third String",
                     "Isiah Pacheco", "Practice Squad"]
    assert len(names) == len(set(names))
    by = {r["name"]: r for r in rows}
    assert by["Third String"]["tier"] == "Fade" and by["Third String"]["pos"] == "QB"
    assert by["Practice Squad"]["tier"] == "Fade" and by["Practice Squad"]["pos"] == "RB"
    assert by["Bo Nix"]["tier"] == "Okay" and by["Bo Nix"]["leverage"] is True
    # the glued second header row (RB section) is NOT a player
    assert "Player" not in names


def _df():
    return pd.DataFrame([
        {"name": "Patrick Mahomes", "position": "QB", "team": "KC", "opponent": "@LAC",
         "salary": 8000, "proj_points": 22.1, "ownership": 18.0},
        {"name": "Bo Nix", "position": "QB", "team": "DEN", "opponent": "NYJ",
         "salary": 6000, "proj_points": 17.0, "ownership": 4.0},
        {"name": "Bad Quarterback", "position": "QB", "team": "NYJ", "opponent": "@DEN",
         "salary": 5000, "proj_points": 12.0, "ownership": 1.0},
        {"name": "Third String", "position": "QB", "team": "KC", "opponent": "@LAC",
         "salary": 4000, "proj_points": 0.4, "ownership": 0.0},
        {"name": "Isiah Pacheco", "position": "RB", "team": "KC", "opponent": "@LAC",
         "salary": 6500, "proj_points": 15.0, "ownership": 20.0},
        {"name": "Practice Squad", "position": "RB", "team": "DEN", "opponent": "NYJ",
         "salary": 4000, "proj_points": 1.1, "ownership": 0.0},
        {"name": "Faded Star", "position": "WR", "team": "NYJ", "opponent": "@DEN",
         "salary": 7000, "proj_points": 2.0, "ownership": 9.0},
    ])


def test_split_keeps_strategy_fades_in_ranked_set():
    ranked, out = ar.split_nfl_classic_pool(_df(), removed=["Faded Star"])
    assert set(out["name"]) == {"Third String", "Practice Squad"}
    assert "Faded Star" in set(ranked["name"])  # a fade is ranked (needs its reason)
    assert len(ranked) + len(out) == 7
    tables = ar._nfl_classic_auto_out_tables(out)
    assert set(tables) == {"QB", "RB"}
    assert ar.NFL_CLASSIC_POOL_COLUMNS in tables["QB"]
    assert "| out | Third String | QB | KC | @LAC | $4,000 | 0.4 | 0% | Under 3 projected points | Fade |" in tables["QB"]
    # the pasted tables round-trip through the parser
    parsed = pool_calibration.parse_pool_tiers("\n\n".join(tables.values()))
    assert {(r["name"], r["tier"], r["pos"]) for r in parsed} == {
        ("Third String", "Fade", "QB"), ("Practice Squad", "Fade", "RB")}


def test_nfl_classic_prompt_has_auto_out_and_drops_every_player_demand(tmp_path):
    p = ar.build_player_pool_prompt(_df(), ["Faded Star"], "note", "nfl_classic",
                                    "NFL Classic", "nfl", tmp_path / "pool.md",
                                    tmp_path / "bundle.md")
    assert "AUTO-OUT" in p and "out of the pool (not written up)" in p
    assert "2 auto-out players" in p and "5 ranked-set players" in p
    assert "Every one of the 7 players gets exactly one ranked entry" not in p
    assert "gets exactly one ranked entry" not in p
    assert "Core / Good / Okay players ONLY" in p and "35 words TOTAL" in p
    assert "at least 4 QBs, 8 RBs, 12 WRs, 5 TEs, 4 DSTs" in p
    # auto-out players are listed only in the paste block, never as ranked lines
    assert "- Third String —" not in p and "| out | Third String |" in p
    assert "- Faded Star —" in p  # the strategy fade stays a ranked line
    assert "FanDuel" not in p and "FD " not in p


def test_mma_and_showdown_prompts_unchanged(tmp_path):
    mma = pd.DataFrame([
        {"name": "Fighter A", "salary": 9000, "proj_points": 90.0, "ownership": 30.0,
         "ceiling": 110.0, "win_prob": 0.7, "opponent": "Fighter B"},
        {"name": "Fighter B", "salary": 7200, "proj_points": 2.0, "ownership": 5.0,
         "ceiling": 95.0, "win_prob": 0.3, "opponent": "Fighter A"},
    ])
    p = ar.build_player_pool_prompt(mma, [], "note", "mma_se", "UFC SE", "mma",
                                    tmp_path / "pool.md", tmp_path / "bundle.md")
    assert "Every one of the 2 players gets exactly one ranked entry" in p
    assert "AUTO-OUT" not in p and "auto-out" not in p
    assert "- Fighter B —" in p  # a 2.0-proj fighter is still ranked in MMA
    assert "| Rank | Fighter | Sal | Proj | Ceiling | Win% | Own | How it wins | Tier |" in p
    sd = _df().assign(salary_cpt=lambda d: d.salary * 1.5, own_cpt=1.0, own_flex=5.0)
    p2 = ar.build_player_pool_prompt(sd, [], "note", "nfl_sd", "NFL SD", "nfl",
                                     tmp_path / "pool.md", tmp_path / "bundle.md")
    assert "Every one of the 7 players gets exactly one ranked entry" in p2
    assert "AUTO-OUT" not in p2 and "- Third String —" in p2


def test_run_player_pool_passes_builder_prompt(tmp_path, monkeypatch):
    monkeypatch.setattr(player_pool, "_POOL_DIR", tmp_path / "pool")
    monkeypatch.setattr(sessions, "_SESSION_DIR", tmp_path / "sessions")
    sessions.save_source("nfl_classic", "etr.csv", _df(), "ETR")
    captured = {}

    def _fake(prompt, out_path):
        captured["prompt"] = prompt
        return {"ok": True, "error": None, "duration_s": 0.0, "cost_usd": None}
    monkeypatch.setattr(ar, "_run_claude", _fake)
    monkeypatch.setattr(ar, "build_bundle", lambda *a, **k: tmp_path / "bundle.md")
    from src import slate_analysis
    monkeypatch.setattr(slate_analysis, "load_persisted", lambda slug: None)
    assert ar.run_player_pool("nfl_classic", "NFL Classic", "nfl")["ok"]
    assert "AUTO-OUT" in captured["prompt"] and "| out | Practice Squad |" in captured["prompt"]


def test_lock_and_contract_board_see_auto_out_players(tmp_path, monkeypatch):
    monkeypatch.setattr(player_pool, "_POOL_DIR", tmp_path / "pool")
    monkeypatch.setattr(pool_lock, "_POOL_DIR", tmp_path / "pool")
    monkeypatch.setattr(pool_lock, "_CONTRACT_DIR", tmp_path / "contract")
    monkeypatch.setattr(strategy_contract, "_CONTRACT_DIR", tmp_path / "contract")
    monkeypatch.setattr(sessions, "_SESSION_DIR", tmp_path / "sessions")
    player_pool.save_pool("nfl_classic", _TWO_TABLE_MD)
    sessions.save_source("nfl_classic", "etr.csv", _df(), "ETR")
    rows = pool_lock.board_rows("nfl_classic")
    by = {r["name"]: r for r in rows}
    assert by["Third String"]["in_pool"] is False and by["Third String"]["pos"] == "QB"
    assert by["Practice Squad"]["in_pool"] is False and by["Practice Squad"]["proj"] == 1.1
    blk = pool_lock.lock_pool("nfl_classic")
    assert blk["n_in"] == 3 and blk["n_out"] == 3
    assert blk["by_position"]["QB"] == 2 and blk["by_position"]["RB"] == 1
    strategy_contract.update_board("nfl_classic")
    import json
    board = json.loads(strategy_contract._path("nfl_classic").read_text())["board"]
    assert {b["name"] for b in board} >= {"Third String", "Practice Squad"}
    assert next(b for b in board if b["name"] == "Third String")["tier"] == "Fade"
