"""Strategy contract: verdict parsing + hard-fade-only semantics.

The contract must NEVER mark a PLAY/underweight/lean-fade call as an
auto-appliable fade — that's the footgun that would zero the strategy's own
leverage plays in the Sim tool."""
import json

import pandas as pd

import src.strategy_contract as sc
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
    import json
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


def test_contract_carries_slate_rule_material(tmp_path, monkeypatch):
    """7/29/26: the contract ships chalk_pairs + anchor_pairs — the Sim renders
    one-click builder rules from them. Data-derived from the pool's ownership,
    so the names always resolve."""
    import json
    import src.strategy_contract as sc
    monkeypatch.setattr(sc, "_CONTRACT_DIR", tmp_path)
    df = pd.DataFrame([
        {"name": "Chalk One", "salary": 10000, "proj_points": 90.0, "ownership": 35.0},
        {"name": "Chalk Two", "salary": 9800, "proj_points": 88.0, "ownership": 33.0},
        {"name": "Chalk Three", "salary": 9000, "proj_points": 80.0, "ownership": 20.0},
        {"name": "Value Guy", "salary": 7000, "proj_points": 65.0, "ownership": 6.0},
    ])
    p = sc.write_contract("pga_classic", _MD, {"src.csv": {"vendor": "ETR PGA", "df": df}})
    payload = json.loads(p.read_text())
    pairs = payload["chalk_pairs"]
    assert pairs and pairs[0]["players"] == ["Chalk One", "Chalk Two"]
    assert pairs[0]["joint_pct"] > 10
    # 35% and 33% sit within the 5-pt anchor-equivalence window -> a twin set.
    anchors = payload["anchor_pairs"]
    assert anchors and set(anchors[0]["players"]) >= {"Chalk One", "Chalk Two"}


# ---- Structural quotas stated in prose ------------------------------------

def test_parse_structure_rules_reads_the_real_8_2_26_sentence():
    """The sentence that cost a slate.

    The 8/2/26 RD4 Showdown strategy said "using a minimum of 2 and maximum of
    3 leaderboard golfers per team". The contract had no field for it, so the
    Sim never received it and 17 of 34 entered lineups broke the rule."""
    md = ("- **The course changed.** ETR expected the rebuilt par-70 course to "
          "play \"2-3 strokes harder overall\". That contradiction is why the "
          "article is splitting the difference on structure — using a minimum "
          "of 2 and maximum of 3 leaderboard golfers per team, and deliberately "
          "not forcing a way-back golfer into every lineup.")
    got = sc.parse_structure_rules(md)
    assert len(got) == 1
    assert (got[0]["min"], got[0]["max"]) == (2, 3)
    assert got[0]["kind"] == "leaderboard"
    # The quote must contain the rule, not just the head of a long bullet —
    # it is the user's only check on a parser that shapes thousands of lineups.
    assert "minimum of 2 and maximum of 3" in got[0]["quote"]
    # "2-3 strokes harder" must NOT be mistaken for the quota.
    assert got[0]["max"] != 0


def test_parse_structure_rules_accepts_the_shorthand_forms():
    for text, exp in [
        ("I will be using a min 2, max 3 LB (T-10 and ties) MME set.", (2, 3)),
        ("I am using 2-3 leaderboard golfers per lineup.", (2, 3)),
        ("a min of 1 and a max of 4 leaderboard golfers (T-15 and ties)", (1, 4)),
    ]:
        got = sc.parse_structure_rules(text)
        assert got, f"no match for: {text}"
        assert (got[0]["min"], got[0]["max"]) == exp


def test_parse_structure_rules_reads_top_n_and_defaults_to_ten():
    assert sc.parse_structure_rules(
        "min 2, max 3 LB (T-15 and ties)")[0]["top_n"] == 15
    # No T-N stated -> the RD4 SD convention.
    assert sc.parse_structure_rules(
        "a minimum of 2 and maximum of 3 leaderboard golfers")[0]["top_n"] == 10


def test_parse_structure_rules_stays_quiet_when_unsure():
    """A wrong quota silently shapes thousands of lineups, so ambiguity must
    return nothing and leave the numbers to the user."""
    for text in [
        "The leaderboard is crowded at the top.",       # no numbers
        "min 2 and max 3 of the value tier",            # not the leaderboard
        "a minimum of 2 and maximum of 8 leaderboard golfers",  # >6-man roster
        "",
    ]:
        assert sc.parse_structure_rules(text) == [], text


def test_contract_payload_carries_structure_rules(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "_CONTRACT_DIR", tmp_path)
    md = ("## Fades\n- **Someone** — FADE\n\n"
          "## Key themes\n- using a minimum of 2 and maximum of 3 leaderboard "
          "golfers per team.\n")
    sc.write_contract("pga_rd4_sd", md, {})
    payload = json.loads((tmp_path / "pga_rd4_sd.json").read_text())
    assert "structure_rules" in payload
    assert payload["structure_rules"][0]["min"] == 2
    assert payload["structure_rules"][0]["max"] == 3
