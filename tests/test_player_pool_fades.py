"""extract_fades: verdict-aware fade extraction (both strategy formats).

The player pool's membership = projections minus these fades — so a PLAY call
or a 'Do NOT zero' underweight leaking into the fade list silently drops the
strategy's own leverage plays from the board."""
from src.player_pool import extract_fades, parse_calls

# Modern format: no literal "**Fades**" subheading — verdicts on every line.
_MODERN = """
## Leverage & fades
**Leverage candidates to address (bundle list — every one gets a call):**
- **Doug Ghim $8,600 (10%) — PLAY.** Top-of-band multiplier.
- **Christiaan Bezuidenhout $7,800 (8%) — PASS/MIX.** Narrative, BUT dock. Fade the history.
- **Aldrich Potgieter $7,500 (7–8%) — PLAY (form dart).** Explicitly a **form-over-fit bet**.

**Additional fades / underweights:**
- **Keith Mitchell $10,000 — FADE.** Trap-priced volatile anchor.
- **Jackson Koivun $9,400 — UNDERWEIGHT the field.** Do NOT zero.
- **Eric Cole $9,100 — LEAN FADE.** Docked profile.

## Decisions
"""

# Legacy format: a literal "**Fades**" subheading with plain bolded names.
_LEGACY = """
## Leverage & fades
Leverage: take **Ruziboev** over the chalk.

**Fades:**
- **Shara Magomedov** — priced like a lock, isn't one.
- **Donchenko at $9,400 vs Yakhyaev** — wrong side of the number.
- **PASS** on anyone under $7K here.

## Decisions
"""


def test_modern_format_hard_fades_only():
    fades = extract_fades(_MODERN)
    assert fades == ["Keith Mitchell"], fades  # NOT Ghim/Potgieter (PLAY), NOT Koivun/Cole


def test_legacy_fades_subheading_still_works():
    fades = extract_fades(_LEGACY)
    # Plain bolded names under the Fades heading count; the leverage bold above
    # the heading does NOT; the PASS directive is excluded by its verdict.
    assert "Shara Magomedov" in fades and "Donchenko" in fades
    assert "Ruziboev" not in fades
    assert "PASS" not in fades


def test_parse_calls_shared_semantics():
    verdicts = {c["name"]: c["verdict"] for c in parse_calls(_MODERN)}
    assert verdicts["Doug Ghim"] == "play"
    assert verdicts["Jackson Koivun"] == "underweight"
    assert verdicts["Keith Mitchell"] == "fade"


def test_empty_and_sectionless():
    assert extract_fades("") == []
    assert extract_fades("## Top plays\n- **X** PLAY") == []


def test_build_pool_carries_mma_ceiling_and_winprob():
    """MMA fighters must surface ceiling (proj_win) + win_prob for the ranking."""
    import pandas as pd
    from src.player_pool import build_pool
    df = pd.DataFrame({
        "name": ["Max Holloway", "Cory Sandhagen"],
        "salary": [9000, 8300], "ownership": [45.0, 18.0],
        "proj_points": [80.8, 66.5], "proj_win": [108.8, 91.1],
        "win_prob": [0.66, 0.54], "matchup": ["vs X", "vs Y"],
    })
    pool = build_pool({"mma.csv": {"vendor": "DailyFan MMA", "df": df}})
    assert "win_prob" in pool.columns
    holl = pool[pool["name"] == "Max Holloway"].iloc[0]
    assert holl["ceiling"] == 108.8          # proj_win used as the MMA ceiling
    assert round(holl["win_prob"], 2) == 0.66
    assert holl["opponent"] == "vs X"        # matchup → opponent


def test_build_pool_drops_winprob_for_non_mma():
    import pandas as pd
    from src.player_pool import build_pool
    df = pd.DataFrame({"name": ["A"], "salary": [10000], "ownership": [20.0],
                       "proj_points": [70.0], "ceiling": [95.0]})
    pool = build_pool({"g.csv": {"vendor": "ETR PGA", "df": df}})
    assert "win_prob" not in pool.columns     # golf: no win prob column
    assert pool.iloc[0]["ceiling"] == 95.0


# ---- Split format (7/27/26): '## Leverage' and '## Fades' are separate ----

_SPLIT_MD = """# Strategy
## Leverage
This section names the low-owned players who could decide the slate.
- **Corey Heim** (7% owned) — his best realistic day is about 70 points.

## Fades
This section names the popular players whose price looks too high.
- **Valter Walker** ($8,800, 34%) — **FADE.** Needs a finish to score at all.
- **Sam Patterson** ($9,400, 32%) — **LEAN FADE.** Ceiling capped past round one.
- **Muhammad Saidov** — plain bolded name, no verdict token here.

## Key themes
- **Bogus Bold** should not be swept — different section.
"""


def test_split_format_extract_fades_zeroes_only_the_fades_section():
    fades = extract_fades(_SPLIT_MD)
    # Hard FADE zeroed; the dedicated section makes a verdict-less bolded
    # name unambiguous fade-context; LEAN FADE is under-own, never a zero.
    assert "Valter Walker" in fades
    assert "Muhammad Saidov" in fades
    assert "Sam Patterson" not in fades
    # Names outside '## Fades' are never swept.
    assert "Corey Heim" not in fades and "Bogus Bold" not in fades


def test_split_format_parse_calls_reads_both_sections():
    calls = {c["name"]: c["verdict"] for c in parse_calls(_SPLIT_MD)}
    assert calls.get("Valter Walker") == "fade"
    assert calls.get("Sam Patterson") == "lean_fade"
    # No verdict token -> no call (Saidov, Heim).
    assert "Muhammad Saidov" not in calls and "Corey Heim" not in calls
