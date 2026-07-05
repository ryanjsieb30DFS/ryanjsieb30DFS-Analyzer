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
