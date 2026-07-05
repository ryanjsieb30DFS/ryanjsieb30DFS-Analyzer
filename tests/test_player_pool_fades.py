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
