"""Unit tests for the DK contest-standings parser — the one input everything
downstream (autopsy, field profile, shark gap, accuracy) depends on."""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.autopsy import parse_dk_results, _parse_lineup_string  # noqa: E402


_HEADER = "Rank,EntryId,EntryName,TimeRemaining,Points,Lineup,,Player,Roster Position,%Drafted,FPTS\n"


def _csv(rows: list[str]) -> io.StringIO:
    return io.StringIO(_HEADER + "\n".join(rows))


def _happy_csv() -> io.StringIO:
    return _csv([
        '1,111,shark1 (1/1),0,150.5,G Jon Rahm G Cameron Young G Max Homa '
        'G Sam Burns G Tom Kim G Corey Conners,,Jon Rahm,G,45.5%,90.1',
        '2,222,RyvlesGaming30,0,120.0,G Jon Rahm G Cameron Young G Max Homa '
        'G Sam Burns G Tom Kim G Denny McCarthy,,Cameron Young,G,30.2%,80.5',
        ',,,,,,,Max Homa,G,12.0%,70.0',
        ',,,,,,,Denny McCarthy,G,4.1%,88.8',
    ])


def test_happy_path_parses_both_halves():
    parsed = parse_dk_results(_happy_csv())
    assert len(parsed["lineups"]) == 2
    assert len(parsed["players"]) == 4
    assert parsed["players"]["actual_own"].tolist()[0] == 45.5
    assert parsed["lineups"]["Lineup_parsed"].iloc[0][0] == "Jon Rahm"


def test_malformed_drafted_pct_coerces_to_nan_not_crash():
    # DK renders missing ownership as an em-dash; that must not kill the parse.
    parsed = parse_dk_results(_csv([
        '1,111,someone,0,150.5,G Jon Rahm G Cameron Young G Max Homa '
        'G Sam Burns G Tom Kim G Corey Conners,,Jon Rahm,G,—,90.1',
        ',,,,,,,Cameron Young,G,30.2%,80.5',
    ]))
    own = parsed["players"]["actual_own"]
    assert own.isna().iloc[0], "em-dash ownership should coerce to NaN"
    assert own.iloc[1] == 30.2


def test_missing_player_half_raises():
    # Right half stripped (hand-edited CSV) → fail fast, never a zero-player "analysis".
    try:
        parse_dk_results(_csv([
            '1,111,someone,0,150.5,G Jon Rahm G Cameron Young G Max Homa '
            'G Sam Burns G Tom Kim G Corey Conners,,,,,',
        ]))
        raise AssertionError("expected ValueError for zero player rows")
    except ValueError as e:
        assert "player" in str(e).lower()


def test_header_only_csv_raises():
    try:
        parse_dk_results(io.StringIO(_HEADER))
        raise AssertionError("expected ValueError for zero lineup rows")
    except ValueError as e:
        assert "lineup" in str(e).lower()


def test_missing_columns_raises():
    try:
        parse_dk_results(io.StringIO("Rank,EntryName,Points\n1,x,100\n"))
        raise AssertionError("expected ValueError for missing columns")
    except ValueError as e:
        assert "missing" in str(e).lower()


def test_lineup_string_golf_mlb_captain():
    assert _parse_lineup_string("G Jon Rahm G Cameron Young") == ["Jon Rahm", "Cameron Young"]
    assert _parse_lineup_string(
        "1B Vinnie Pasquantino 2B Romy Gonzalez SS Bobby Witt Jr."
    ) == ["Vinnie Pasquantino", "Romy Gonzalez", "Bobby Witt Jr."]
    assert _parse_lineup_string("CPT Max Holloway UTIL Paddy Pimblett") == [
        "Max Holloway", "Paddy Pimblett"]
    assert _parse_lineup_string(None) == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
