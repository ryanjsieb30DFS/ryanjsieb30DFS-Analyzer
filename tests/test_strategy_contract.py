"""Strategy contract: verdict parsing + hard-fade-only semantics.

The contract must NEVER mark a PLAY/underweight/lean-fade call as an
auto-appliable fade — that's the footgun that would zero the strategy's own
leverage plays in the Sim tool."""
import pandas as pd

from src.strategy_contract import parse_calls, write_contract

_MD = """
## Leverage & fades
**Leverage candidates to address (bundle list — every one gets a call):**
- **Doug Ghim $8,600 (10%) — PLAY.** Ceiling 107.5, top-of-band multiplier.
- **Christiaan Bezuidenhout $7,800 (8%) — PASS/MIX.** Narrative, BUT dock. Fade the history.
- **Aldrich Potgieter $7,500 (7–8%) — PLAY (form dart).** Explicitly a **form-over-fit bet**.

**Additional fades / underweights:**
- **Keith Mitchell $10,000 — FADE.** Trap-priced volatile anchor.
- **Jackson Koivun $9,400 — UNDERWEIGHT the field.** Do NOT zero.
- **Eric Cole $9,100 — LEAN FADE.** Docked profile.

## Decisions
"""


def _sources():
    df = pd.DataFrame([
        {"name": n, "salary": 8000, "proj_points": 70.0, "ownership": 9.0}
        for n in ["Doug Ghim", "Christiaan Bezuidenhout", "Aldrich Potgieter",
                  "Keith Mitchell", "Jackson Koivun", "Eric Cole"]
    ])
    return {"src.csv": {"vendor": "ETR PGA", "df": df}}


def test_parse_calls_reads_verdicts_not_section_sweep():
    calls = {c["name"]: c["verdict"] for c in parse_calls(_MD)}
    assert calls["Doug Ghim"] == "play"
    assert calls["Christiaan Bezuidenhout"] == "pass_mix"   # 'Fade the history' must NOT win
    assert calls["Aldrich Potgieter"] == "play"
    assert calls["Keith Mitchell"] == "fade"
    assert calls["Jackson Koivun"] == "underweight"
    assert calls["Eric Cole"] == "lean_fade"


def test_parse_calls_ignores_prose_verdict_words():
    """Verdict words buried in PROSE (not the bolded lead / first sentence after
    it) must never be read as calls — a phantom fade here becomes a false
    discipline violation in the Grade tab and the adherence trend. Also:
    substring hits inside words ('faded', 'plays', 'playable') don't count."""
    md = """
## Leverage & fades
**(a) Low-owned definers:**
- **Adrian Bautista $7,800 (6% own)** — last card the winning definer was one the field faded; his ceiling path is a first-round finish.
- **Sam Hughes $6,900 (4% own)** — the field plays him at 4% but every winner carried him; playable ceiling.

**Fades:**
- **Keith Mitchell $10,000 — FADE.** Trap-priced volatile anchor.
- **Rory Sabbatini** ($9.8K) — LEAN FADE. Needs wind to matter.
"""
    calls = {c["name"]: c["verdict"] for c in parse_calls(md)}
    assert "Adrian Bautista" not in calls   # 'faded' in prose is NOT a call
    assert "Sam Hughes" not in calls        # 'plays'/'playable' are NOT calls
    assert calls["Keith Mitchell"] == "fade"
    assert calls["Rory Sabbatini"] == "lean_fade"  # decimal in $9.8K must not clip the clause


def test_write_contract_hard_fades_only(tmp_path, monkeypatch):
    monkeypatch.setattr("src.strategy_contract._CONTRACT_DIR", tmp_path)
    import json
    p = write_contract("pga_classic", _MD, _sources())
    c = json.loads(p.read_text())
    # ONLY the hard FADE is auto-appliable; junk headings filtered by the universe.
    assert c["fades"] == ["Keith Mitchell"]
    names = {x["name"] for x in c["calls"]}
    assert "Additional fades / underweights" not in names
    assert "form-over-fit bet" not in names
    assert {x["verdict"] for x in c["calls"]} == {"play", "pass_mix", "fade",
                                                  "underweight", "lean_fade"}


def test_empty_strategy_yields_empty_contract(tmp_path, monkeypatch):
    monkeypatch.setattr("src.strategy_contract._CONTRACT_DIR", tmp_path)
    import json
    p = write_contract("nascar", "", {})
    c = json.loads(p.read_text())
    assert c["fades"] == [] and c["calls"] == [] and c["leverage_candidates"] == []


def test_no_price_dash_verdict_bullets_parse():
    """REGRESSION (live pga_rd4_sd 7/5): bullets without a $price ('**Mac
    Meissner — FADE**') failed name extraction and the whole contract shipped
    empty while the app reported success."""
    from src.player_pool import parse_calls
    md = (
        "## Leverage & fades\n"
        "- **Blades Brown — PLAY.** Elite ball striking this week.\n"
        "- **Mac Meissner — FADE** Cold putter, bad course fit.\n"
        "- **Keith Mitchell $10,000 — FADE.** Price still too high.\n"
    )
    calls = {c["name"]: c["verdict"] for c in parse_calls(md)}
    assert calls == {"Blades Brown": "play", "Mac Meissner": "fade",
                     "Keith Mitchell": "fade"}


def test_matchup_headers_and_lowercase_prose_no_phantom_calls():
    """REGRESSION (live mma_se 7/25): '**Walker vs Petersen:**' headers plus
    lowercase 'play' in prose produced a phantom PLAY on Valter Walker beside
    his real LEAN FADE."""
    from src.player_pool import parse_calls
    md = (
        "## Leverage & fades\n"
        "- **Walker vs Petersen:** the leverage side against the chalkiest "
        "play on the slate.\n"
        "- **Valter Walker — LEAN FADE.** 36% own on a coin-flip heavyweight.\n"
    )
    calls = parse_calls(md)
    assert calls == [{"name": "Valter Walker", "verdict": "lean_fade"}]


def test_contract_dedups_conflicting_verdicts_harsher_wins(tmp_path, monkeypatch):
    import src.strategy_contract as sc
    monkeypatch.setattr(sc, "_CONTRACT_DIR", tmp_path)
    import pandas as pd
    sources = {"v.csv": {"vendor": "T", "df": pd.DataFrame({
        "name": ["Valter Walker", "Thomas Petersen"],
        "salary": [8800, 7400], "proj_points": [67.8, 40.3],
        "ownership": [36.0, 28.0]})}}
    md = (
        "## Leverage & fades\n"
        "- **Valter Walker — PLAY.** x.\n"
        "- **Valter Walker — LEAN FADE.** y.\n"
    )
    sc.write_contract("mma_se", md, sources)
    import json
    payload = json.loads((tmp_path / "mma_se.json").read_text())
    walker = [c for c in payload["calls"] if c["name"] == "Valter Walker"]
    assert walker == [{"name": "Valter Walker", "verdict": "lean_fade"}]


def test_short_fragment_never_substring_resolves(tmp_path, monkeypatch):
    import src.strategy_contract as sc
    monkeypatch.setattr(sc, "_CONTRACT_DIR", tmp_path)
    import pandas as pd
    sources = {"v.csv": {"vendor": "T", "df": pd.DataFrame({
        "name": ["Bo Nickal"], "salary": [9000], "proj_points": [90.0],
        "ownership": [30.0]})}}
    md = "## Leverage & fades\n- **Bo — FADE.** short fragment.\n"
    sc.write_contract("mma_se", md, sources)
    import json
    payload = json.loads((tmp_path / "mma_se.json").read_text())
    # "bo" (2 chars) must NOT resolve to Bo Nickal via substring...
    # (exact _norm_name match doesn't hit either: "bo" != "bo nickal")
    assert payload["fades"] == []
