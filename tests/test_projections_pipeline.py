"""Data-pipeline tests (Tier-3): ownership scaling, stddev derivation, and vendor
detection confidence for the restored Projections upload tab."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402

from src.projections import _normalize_ownership_column, _derive_stddev  # noqa: E402
from src.vendors import detect_vendor_confidence  # noqa: E402


def test_ownership_scaling_percent_vs_fraction():
    # any value > 1 -> already percent (kept as-is)
    pct = _normalize_ownership_column(pd.Series([5.0, 22.0, 0.4]))
    assert list(pct) == [5.0, 22.0, 0.4]
    # all <= 1 -> fractions, scaled to percent
    frac = _normalize_ownership_column(pd.Series([0.05, 0.22, 0.4]))
    assert [round(x, 1) for x in frac] == [5.0, 22.0, 40.0]


def test_derive_stddev_from_ceiling_then_fallback():
    df = pd.DataFrame({"proj_points": [10.0, 20.0], "ceiling": [22.8, float("nan")]})
    sd = _derive_stddev(df)
    assert round(sd.iloc[0], 2) == 10.0          # (22.8-10)/1.28
    assert round(sd.iloc[1], 2) == 6.0           # 30% of 20 (no ceiling)


def test_derive_stddev_keeps_real_vendor_value():
    df = pd.DataFrame({"proj_points": [10.0], "ceiling": [22.8], "stddev": [3.5]})
    assert round(_derive_stddev(df).iloc[0], 2) == 3.5   # real stddev preserved


def test_vendor_confidence_near_miss_flags_renamed_header():
    # Build a frame that matches a signature except for one renamed column.
    from src.vendors import VENDOR_SIGNATURES
    sig = max(VENDOR_SIGNATURES, key=lambda s: len(s["required_columns"]))
    req = sorted(sig["required_columns"])
    cols = set(req[:-1]) | {req[-1] + "_RENAMED"}     # drop one required col, add a decoy
    conf = detect_vendor_confidence(pd.DataFrame(columns=list(cols)))
    assert any(name == sig["name"] for name, _ in conf["near_misses"])


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


def test_sin_filename_relabels_identical_etr_schema():
    """SIN's simple PGA export shares ETR's exact headers — the filename is the
    only disambiguator. Without a SIN hint the label stays ETR PGA."""
    import pandas as pd
    from src.vendors import detect_vendor
    df = pd.DataFrame({
        "name": ["A"], "sal": [10000], "proj": [50.0],
        "ceil": [70.0], "own": [20.0], "pt/$": [5.0],
    })
    # Simple shape defaults to ETR PGA (user-confirmed 7/5/26); SIN filename overrides.
    assert detect_vendor(df, source_name="SIN pga-sd-projections-dk.csv")["name"] == "Ship It Nation PGA (simple)"
    assert detect_vendor(df, source_name="PGA Projections DK.csv")["name"] == "ETR PGA"
    assert detect_vendor(df, source_name="wisconsin.csv")["name"] == "ETR PGA"
    assert detect_vendor(df)["name"] == "ETR PGA"
