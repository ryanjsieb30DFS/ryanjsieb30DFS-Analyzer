"""MME plan Phase 1: 20-Max/150-Max are declarable and inferable, and the
small-field machinery stays SEALED — focus gates unchanged, results headline
computed from focus contests only."""
from src.contests import (CONTEST_TYPES, FOCUS_CONTEST_TYPES,
                          MME_CONTEST_TYPES, infer_type)
from src import history


def test_vocabulary_and_seal_sets():
    assert "20-Max" in CONTEST_TYPES and "150-Max" in CONTEST_TYPES
    assert FOCUS_CONTEST_TYPES == {"SE", "3-Max", "5-Max"}
    assert MME_CONTEST_TYPES == {"20-Max", "150-Max"}
    assert not (FOCUS_CONTEST_TYPES & MME_CONTEST_TYPES)


def test_infer_type_maps_large_caps():
    assert infer_type(["a (3/20)", "b", "c (20/20)"]) == "20-Max"
    assert infer_type(["a (139/150)"]) == "150-Max"
    assert infer_type(["a (2/3)"]) == "3-Max"       # focus unchanged
    assert infer_type(["plain name"]) == "SE"


def test_results_headline_sealed_from_mme(tmp_path, monkeypatch):
    """A slate logging an SE and a 150-Max: the headline best_percentile is the
    SE's; the MME result lands in its own parallel fields."""
    monkeypatch.setattr(history, "_REPO_ROOT", tmp_path)
    (tmp_path / "rules" / "mma_se").mkdir(parents=True)
    hist = history.archive_slate(
        slug="mma_se", sport="mma", contest_label="MMA",
        slate_label="seal test",
        autopsy_records=[{"contest_id": "1", "slate_name": "seal test"}],
        roi_contests=[
            {"name": "SE", "type": "SE", "field_size": 500, "my_entries": 1,
             "entry_fee": 5, "best_rank": 100, "best_percentile": 20.0},
            {"name": "Mini Max", "type": "150-Max", "field_size": 50000,
             "my_entries": 20, "entry_fee": 0.5, "best_rank": 500,
             "best_percentile": 1.0},
        ],
        proj_source=None,
    )
    rows = history.load_results("mma_se")
    row = rows[-1]
    assert row["best_percentile"] == 20.0        # SE only — NOT the MME's 1.0
    assert row["best_percentile_mme"] == 1.0
    assert row["best_rank"] == 100 and row["best_rank_mme"] == 500
    assert hist.exists()


# ---------------------------------------------------------------------------
# Contest-name canonicalization (9/6/26: the Sim is the naming authority)
# ---------------------------------------------------------------------------

def test_canonical_contest_name_snaps_to_sim(monkeypatch, tmp_path):
    from src import contests as c

    monkeypatch.setattr("src.sim_link.sim_contest_names",
                        lambda slug: ["UFC $4K Clinch [Single Entry]"])
    monkeypatch.setattr("src.sim_link.load_sim_pool", lambda slug: None)
    # the 9/5 failure shape: hand-typed short name, different case, no bracket
    assert (c.canonical_contest_name("mma_se", "UFC $4k Clinch")
            == "UFC $4K Clinch [Single Entry]")
    # pool labels carry a "(SE)" tag — it is stripped from the stored name
    monkeypatch.setattr("src.sim_link.sim_contest_names", lambda slug: [])
    monkeypatch.setattr(
        "src.sim_link.load_sim_pool",
        lambda slug: {"contests": [{"label": "UFC $6K Flying Knee [Single Entry] (SE)"}]})
    assert (c.canonical_contest_name("mma_se", "ufc $6K flying knee")
            == "UFC $6K Flying Knee [Single Entry]")
    # no Sim match: the typed name survives untouched
    assert c.canonical_contest_name("mma_se", "UFC $9K Uppercut") == "UFC $9K Uppercut"


def test_add_contest_canonicalizes_name(monkeypatch, tmp_path):
    from src import contests as c

    monkeypatch.setattr(c, "_CONTESTS_DIR", tmp_path)
    monkeypatch.setattr("src.sim_link.sim_contest_names",
                        lambda slug: ["NAS $5K Engine Block [Single Entry]"])
    monkeypatch.setattr("src.sim_link.load_sim_pool", lambda slug: None)
    c.add_contest("nascar", {"name": "NAS $5k engine block", "type": "SE",
                             "field_size": 490, "max_entries": 1,
                             "my_entries": 1})
    saved = c.load_contests("nascar")
    assert saved[0]["name"] == "NAS $5K Engine Block [Single Entry]"
