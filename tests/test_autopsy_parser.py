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


def test_lineup_string_nfl_showdown():
    # DK NFL Showdown: CPT + 5 FLEX. Any position can fill FLEX (K/DST too).
    s = ("CPT Lamar Jackson FLEX Derrick Henry FLEX Zay Flowers "
         "FLEX DK Metcalf FLEX Chris Boswell FLEX Steelers")
    assert _parse_lineup_string(s) == [
        "Lamar Jackson", "Derrick Henry", "Zay Flowers",
        "DK Metcalf", "Chris Boswell", "Steelers"]


def test_lineup_string_nfl_classic_markers():
    # NFL Classic markers. DST must split as a whole token — the D inside
    # DST would otherwise match the single-char NASCAR class and mis-split
    # "DST Broncos" into "ST Broncos".
    s = ("QB Josh Allen RB Saquon Barkley RB Bijan Robinson WR Justin Jefferson "
         "WR CeeDee Lamb WR Nico Collins TE Trey McBride FLEX Ja'Marr Chase "
         "DST Broncos")
    assert _parse_lineup_string(s) == [
        "Josh Allen", "Saquon Barkley", "Bijan Robinson", "Justin Jefferson",
        "CeeDee Lamb", "Nico Collins", "Trey McBride", "Ja'Marr Chase",
        "Broncos"]


def test_lineup_captain_extraction():
    from src.autopsy import _lineup_captain
    assert _lineup_captain(
        "CPT Lamar Jackson FLEX Derrick Henry FLEX Steelers") == "Lamar Jackson"
    assert _lineup_captain("G Jon Rahm G Cameron Young") is None
    assert _lineup_captain(None) is None


def test_lineup_string_golf_captain():
    assert _parse_lineup_string("G Jon Rahm G Cameron Young") == ["Jon Rahm", "Cameron Young"]
    assert _parse_lineup_string("D Ryan Blaney D Joey Logano") == ["Ryan Blaney", "Joey Logano"]
    assert _parse_lineup_string("CPT Max Holloway UTIL Paddy Pimblett") == [
        "Max Holloway", "Paddy Pimblett"]
    assert _parse_lineup_string(None) == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


# --- NFL Classic slot rows (9/19/26) ------------------------------------
# Shape of a real DK NFL Classic standings export (anonymized/trimmed from
# ~/Downloads/contest-standings-195548784.csv): a player appears once PER
# ROSTER SLOT the field used — Gibbs at RB and again at FLEX.
def _classic_csv() -> io.StringIO:
    return _csv([
        '1,111,alpha,0,228.56,DST Bills  FLEX Michael Mayer QB Josh Allen RB Jahmyr Gibbs '
        'RB Jonathan Taylor TE Dallas Goedert WR Chris Olave WR Zay Flowers WR Josh Allen,,'
        'Jahmyr Gibbs,RB,52.78%,37.6',
        '2,222,beta,0,224.86,DST Jaguars  FLEX Jahmyr Gibbs QB Josh Allen RB Jonathan Taylor '
        'RB Travis Etienne Jr. TE Greg Dulcich WR Christian Watson WR Zay Flowers WR Josh Allen,,'
        'Jahmyr Gibbs,FLEX,2.5%,37.6',
        ',,,,,,,Josh Allen,QB,40.0%,28.3',
        ',,,,,,,Josh Allen,WR,3.0%,6.1',
        ',,,,,,,Josh Allen,FLEX,1.0%,6.1',
        ',,,,,,,Zay Flowers,WR,22.0%,19.9',
    ])


def test_classic_rb_and_flex_rows_collapse_to_one_player():
    players = parse_dk_results(_classic_csv())["players"]
    gibbs = players[players["name"] == "Jahmyr Gibbs"]
    assert len(gibbs) == 1
    assert abs(float(gibbs["actual_own"].iloc[0]) - (52.78 + 2.5)) < 1e-6
    assert float(gibbs["actual_fpts"].iloc[0]) == 37.6
    assert gibbs["roster_position"].iloc[0] == "RB"


def test_same_name_different_base_position_is_not_merged():
    """A QB and a WR who share a name are two players: never sum their
    ownership. The FLEX row attaches to the FLEX-eligible one (the WR)."""
    players = parse_dk_results(_classic_csv())["players"]
    allens = players[players["name"] == "Josh Allen"].sort_values("roster_position")
    assert len(allens) == 2
    by_pos = {r.roster_position: r for r in allens.itertuples()}
    assert set(by_pos) == {"QB", "WR"}
    assert abs(by_pos["QB"].actual_own - 40.0) < 1e-6
    assert abs(by_pos["WR"].actual_own - 4.0) < 1e-6      # WR 3.0 + FLEX 1.0
    assert by_pos["QB"].actual_fpts == 28.3
    # The untouched single-slot player passes through.
    assert len(players[players["name"] == "Zay Flowers"]) == 1
