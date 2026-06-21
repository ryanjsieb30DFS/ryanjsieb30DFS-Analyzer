"""Tests for DraftKings bulk-upload export (Analyzer: portfolio markdown -> DK CSV)."""
import io

import pandas as pd

from src.dk_export import (read_dk_entries, roster_slot_positions, fill_dk_template,
                           parse_portfolio_rosters, rosters_to_lineups)

DK_RAW = (
    "Entry ID,Contest Name,Contest ID,Entry Fee,F,F,F,F,F,F,,Instructions\n"
    "111,UFC Test,9001,$5,,,,,,,,1. instructions\n"
    "112,UFC Test,9001,$5,,,,,,,,2. more\n"
    "113,UFC Other,9002,$3,,,,,,,,3. note,EXTRA,POOL,COLS,X,Y,Z\n"
    "F,Fighter A (701),Fighter A,701,F,9000,Game,TM\n"
)

PORTFOLIO_MD = """## Lineups
| Fighter | Salary | Own% |
|---|---|---|
| Alice | $9000 | 30 |
| Bob | $8000 | 20 |

| Fighter | Salary | Own% |
|---|---|---|
| Carl | $9000 | 25 |
| Dave | $8000 | 15 |

## Portfolio audit
| Fighter | Exposure |
|---|---|
| Alice | 50% |
| Bob | 50% |
| Carl | 50% |
| Dave | 50% |
"""


def test_read_dk_entries():
    t = read_dk_entries(io.BytesIO(DK_RAW.encode()))
    assert len(t) == 3 and roster_slot_positions(t) == [4, 5, 6, 7, 8, 9]


def test_parse_filters_audit_table_by_roster_size():
    # Without size: 3 tables (2 lineups + the 4-row audit). With size=2: only the 2 lineups.
    assert len(parse_portfolio_rosters(PORTFOLIO_MD)) == 3
    rs = parse_portfolio_rosters(PORTFOLIO_MD, roster_size=2)
    assert rs == [["Alice", "Bob"], ["Carl", "Dave"]]


def test_rosters_to_lineups_maps_and_flags_unresolved():
    rs = parse_portfolio_rosters(PORTFOLIO_MD, roster_size=2)
    lineups, unresolved = rosters_to_lineups(rs, {"Alice": 101, "Bob": 102, "Carl": 103})
    assert lineups[0] == [("Alice", 101), ("Bob", 102)]
    assert unresolved == ["Dave"]                       # not in the map


def test_fill_with_tuples_and_contest_filter():
    t = read_dk_entries(io.BytesIO(DK_RAW.encode()))
    lineups = [[("N1", 1), ("N2", 2), ("N3", 3), ("N4", 4), ("N5", 5), ("N6", 6)],
               [("M1", 7), ("M2", 8), ("M3", 9), ("M4", 10), ("M5", 11), ("M6", 12)]]
    filled, info = fill_dk_template(t, lineups, contest_name="UFC Test")
    assert info["filled"] == 2 and filled.iat[0, 4] == "N1 (1)"
    assert str(filled.iat[2, 4]).strip() == ""          # 'UFC Other' entry untouched


if __name__ == "__main__":
    for fn in [test_read_dk_entries, test_parse_filters_audit_table_by_roster_size,
               test_rosters_to_lineups_maps_and_flags_unresolved, test_fill_with_tuples_and_contest_filter]:
        fn()
        print("ok ", fn.__name__)
    print("4 passed")
