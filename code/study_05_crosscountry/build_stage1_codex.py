"""Deterministic fail-closed Stage 1 build for Study 5.

Creates a new immutable run directory and refuses collisions. No estimation is performed.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "projects" / "study_05_findex_crosscountry"
RUN_ID = "CODEX-S5-BUILD-20260909-001"
OUT = PROJECT / "results" / "stage1" / RUN_ID

EXPECTED = {
    PROJECT / "papers/study_05/CLAIM_CONTRACT.md": "d4d704be0d8fe18f97b7d96e1ab1b47eb7fcaf05d2ec6c81c1a8e8a027f9932a",
    PROJECT / "papers/study_05/CODEX_EXECUTION_BRIEF.md": "05112419c85f428f87055c438d66890b9d152182126ea48e89b1fa184d7b0a1d",
    PROJECT / "papers/study_05/PREREGISTRATION.md": "b959ae5be5d3c9fbcfb2f469a6489d3add112202c8a7db81554c333086bc75bb",
    PROJECT / "papers/study_05/REVISION_1_RESPONSE.md": "7a5e9c727dedd5431839b0fec9c8814c3cac50826b9ba679f2b412ec763d20a4",
    PROJECT / "papers/study_05/REVISION_2_RESPONSE.md": "d6206a76e00330b789373ac24cbefb52b7467c463fb5c031139886bf87daf1c5",
    PROJECT / "papers/study_05/VARIABLE_CONTRACT.md": "9a71ee5f9232d174630663373e19466159e8040203206774e879f69d711e4d6e",
    PROJECT / "research_council/hypotheses/H-000500.json": "5bcd560baf8b4c9c1dfe790009c47c8e46abc7a38a79568c6f33cb758753e653",
    PROJECT / "data/STUDY_05_RAW_MANIFEST.json": "1bce876c10ed0f72281bee846b72efb7386ed8b8e17982639a2da5b2fd2e22f6",
    ROOT / "data/raw/data_micro_findex_2024_vietnam.xlsx": "ca307a0c3dfd54dc945a18fb03c58b014143bc21c90761f71fe304e6a2f90fce",
    PROJECT / "data/raw/wb_credit_information_latest_snapshot.csv": "ef0c67f9c7d44b67939e088f0aab2e578f7ba0d7f2eeadc4093c0103cc1bd06c",
    PROJECT / "data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json": "e7921b98db185e568c7d07dd5c094eb3dbf8e56ca11ba08a15f6d9abe34dcacd",
    PROJECT / "data/raw/wdi_FS.AST.PRVT.GD.ZS_2000_2023.json": "ad301883321da15e2cfcf6a0fefb569565d8efc7c77f1ba5ee3ae540c77dc953",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> None:
    raise RuntimeError(f"FAIL_CLOSED: {message}")


def binary(series: pd.Series, yes: set, no: set) -> pd.Series:
    result = pd.Series(np.nan, index=series.index, dtype="float64")
    result.loc[series.isin(yes)] = 1.0
    result.loc[series.isin(no)] = 0.0
    return result


def latest_wdi(path: Path, value_name: str) -> pd.DataFrame:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = pd.DataFrame(payload[1])
    rows = rows.loc[rows["countryiso3code"].str.len().eq(3) & rows["value"].notna()].copy()
    rows["year"] = pd.to_numeric(rows["date"], errors="raise").astype(int)
    rows = rows.loc[rows["year"].le(2023)].sort_values(["countryiso3code", "year"])
    latest = rows.groupby("countryiso3code", as_index=False).tail(1)
    return latest[["countryiso3code", "year", "value"]].rename(
        columns={"countryiso3code": "iso3", "year": f"{value_name}_year", "value": value_name}
    )


def main() -> None:
    if OUT.exists():
        fail(f"collision: immutable output directory already exists: {OUT}")
    for path, expected in EXPECTED.items():
        if not path.is_file():
            fail(f"missing frozen input: {path}")
        actual = sha256(path)
        if actual != expected:
            fail(f"hash mismatch: {path}; expected {expected}; got {actual}")

    source = ROOT / "data/raw/data_micro_findex_2024_vietnam.xlsx"
    cols = [
        "wpid_random", "economycode", "economy", "regionwb", "wgt", "pop_adult",
        "fin22a", "anydigpayment", "account_fin", "female", "age", "educ", "inc_q",
        "urbanicity", "internet_use", "emp_in", "receive_wages", "receive_transfers",
        "receive_pensions", "receive_agriculture", "merchantpay_dig", "pay_utilities",
        "fin20", "fin24", "fin22b",
    ]
    raw = pd.read_excel(source, sheet_name="findex_microdata_2025_labelled_", usecols=cols)
    if raw.shape[0] != 144090 or raw["wpid_random"].duplicated().any():
        fail("raw row count or respondent-key uniqueness differs from contract")

    drops = []
    active = pd.Series(True, index=raw.index)

    def record(step: str, newmask: pd.Series) -> None:
        nonlocal active
        before = active.copy()
        active &= newmask.fillna(False)
        exited = sorted(set(raw.loc[before, "economycode"].dropna()) - set(raw.loc[active, "economycode"].dropna()))
        drops.append({
            "step": step,
            "rows_before": int(before.sum()),
            "rows_after": int(active.sum()),
            "rows_dropped": int(before.sum() - active.sum()),
            "economies_after": int(raw.loc[active, "economycode"].nunique()),
            "economies_exited": ";".join(exited),
        })

    record("fin22a_valid_1_or_2", raw["fin22a"].isin([1, 2]))
    for col in ["anydigpayment", "account_fin", "female", "age", "educ", "inc_q", "urbanicity"]:
        record(f"{col}_nonmissing", raw[col].notna())

    moderator = pd.read_csv(PROJECT / "data/raw/wb_credit_information_latest_snapshot.csv")
    matched = raw["economycode"].isin(set(moderator["iso3"]))
    record("moderator_iso3_match", matched)
    d = raw.loc[active].copy().rename(columns={"economycode": "iso3", "regionwb": "region"})
    if len(d) != 100560 or d["iso3"].nunique() != 97:
        fail(f"unexpected primary frame: N={len(d)}, economies={d['iso3'].nunique()}")

    d["formal_borrow"] = binary(d["fin22a"], {1}, {2})
    d["female_d"] = binary(d["female"], {1}, {2})
    d["urban_d"] = binary(d["urbanicity"], {2}, {1})
    d["inwork_d"] = binary(d["emp_in"], {1}, {0, 2})
    d["mobile_loan_app"] = binary(d["fin20"], {1}, {2})
    d["emergency_loan_source"] = binary(d["fin24"], {4}, {1, 2, 3, 5, 6, 7})
    d["informal_borrow"] = binary(d["fin22b"], {1}, {2})

    receive_cols = ["receive_wages", "receive_transfers", "receive_pensions", "receive_agriculture"]
    any_one = d[receive_cols].eq(1).any(axis=1)
    any_known_nonone = d[receive_cols].isin([2, 3, 4]).any(axis=1)
    d["receive_dig"] = np.select([any_one, (~any_one) & any_known_nonone], [1.0, 0.0], default=np.nan)
    make_one = d["merchantpay_dig"].eq(1) | d["pay_utilities"].eq(1)
    make_known_nonone = d["merchantpay_dig"].eq(0) | d["pay_utilities"].isin([2, 3, 4])
    d["make_dig"] = np.select([make_one, (~make_one) & make_known_nonone], [1.0, 0.0], default=np.nan)

    d["w_equal"] = d["wgt"] / d.groupby("iso3")["wgt"].transform("sum")
    d["w_population"] = d["w_equal"] * d["pop_adult"]
    d["w_unweighted"] = 1.0
    d["age_c"] = d["age"] - d["age"].mean()
    d["age_c2"] = d["age_c"] ** 2

    keep_mod = [
        "iso3", "depth_credit_info_0_8", "credit_bureau_cov_pct",
        "credit_registry_cov_pct", "legal_rights_0_12",
    ]
    d = d.merge(moderator[keep_mod], on="iso3", how="left", validate="many_to_one")
    if d[keep_mod[1:]].isna().any().any():
        fail("missing moderator after allegedly complete ISO3 merge")
    d = d.rename(columns={"credit_bureau_cov_pct": "bureau_cov", "credit_registry_cov_pct": "registry_cov"})
    d["any_cov"] = d[["bureau_cov", "registry_cov"]].max(axis=1)

    country = d[["iso3", "any_cov", "bureau_cov", "registry_cov", "depth_credit_info_0_8", "legal_rights_0_12"]].drop_duplicates("iso3").copy()
    if len(country) != 97:
        fail("country-level moderator is not unique on the final economy set")
    for raw_name, new_name in [
        ("any_cov", "lowcov2019_z"), ("bureau_cov", "lowbureau2019_z"),
        ("registry_cov", "lowregistry2019_z"), ("depth_credit_info_0_8", "lowdepth2019_z"),
        ("legal_rights_0_12", "lowrights2019_z"),
    ]:
        sd = country[raw_name].std(ddof=0)
        if not np.isfinite(sd) or sd <= 0:
            fail(f"cannot z-score {raw_name}")
        country[new_name] = -(country[raw_name] - country[raw_name].mean()) / sd
    median_cov = float(country["any_cov"].median())
    country["lowcov2019_bmedian"] = (country["any_cov"] < median_cov).astype(int)
    d = d.merge(country[["iso3", "lowcov2019_z", "lowcov2019_bmedian", "lowbureau2019_z", "lowregistry2019_z", "lowdepth2019_z", "lowrights2019_z"]], on="iso3", how="left", validate="many_to_one")

    acct = d.groupby("iso3").apply(lambda x: np.average(x["account_fin"], weights=x["w_equal"]), include_groups=False).rename("acct_own_rate").reset_index()
    gdp = latest_wdi(PROJECT / "data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json", "gdp_pc")
    credit = latest_wdi(PROJECT / "data/raw/wdi_FS.AST.PRVT.GD.ZS_2000_2023.json", "privcredit_gdp")
    controls = country.merge(gdp, on="iso3", how="left", validate="one_to_one").merge(credit, on="iso3", how="left", validate="one_to_one").merge(acct, on="iso3", how="left", validate="one_to_one")
    controls["lgdppc"] = np.log(controls["gdp_pc"])
    if controls[["lgdppc", "privcredit_gdp", "acct_own_rate"]].isna().any().any():
        fail("M6.5 control coverage is incomplete on the final 97 economies")
    d = d.merge(controls[["iso3", "lgdppc", "privcredit_gdp", "acct_own_rate", "gdp_pc_year", "privcredit_gdp_year"]], on="iso3", how="left", validate="many_to_one")

    if not np.allclose(d.groupby("iso3")["w_equal"].sum().to_numpy(), 1.0, atol=1e-12):
        fail("w_equal does not sum to one inside every economy")
    if d[["formal_borrow", "anydigpayment", "account_fin", "female_d", "age_c", "age_c2", "educ", "inc_q", "urban_d"]].isna().any().any():
        fail("primary analysis variable contains missing values")

    out_cols = [
        "wpid_random", "iso3", "economy", "region", "wgt", "pop_adult", "w_equal", "w_population", "w_unweighted",
        "formal_borrow", "anydigpayment", "account_fin", "female_d", "age", "age_c", "age_c2", "educ", "inc_q", "urban_d",
        "internet_use", "inwork_d", "receive_dig", "make_dig", "mobile_loan_app", "emergency_loan_source", "informal_borrow",
        "bureau_cov", "registry_cov", "any_cov", "depth_credit_info_0_8", "legal_rights_0_12", "lowcov2019_z",
        "lowcov2019_bmedian", "lowbureau2019_z", "lowregistry2019_z", "lowdepth2019_z", "lowrights2019_z",
        "lgdppc", "privcredit_gdp", "acct_own_rate", "gdp_pc_year", "privcredit_gdp_year",
    ]
    d = d[out_cols].sort_values(["iso3", "wpid_random"], kind="mergesort").reset_index(drop=True)
    drops_df = pd.DataFrame(drops)
    controls = controls.sort_values("iso3").reset_index(drop=True)

    OUT.mkdir(parents=True, exist_ok=False)
    panel_path = OUT / "analysis_panel.csv"
    drops_path = OUT / "drop_table.csv"
    controls_path = OUT / "country_controls_latest.csv"
    d.to_csv(panel_path, index=False, float_format="%.15g", lineterminator="\n")
    drops_df.to_csv(drops_path, index=False, lineterminator="\n")
    controls.to_csv(controls_path, index=False, float_format="%.15g", lineterminator="\n")

    receipt = {
        "run_id": RUN_ID,
        "study_id": "study_05_findex_crosscountry",
        "stage": 1,
        "status": "BUILT_NOT_ESTIMATED",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "collision_policy": "refuse_if_output_directory_exists",
        "input_sha256": {str(p.relative_to(ROOT)).replace('\\', '/'): h for p, h in EXPECTED.items()},
        "code_sha256": sha256(Path(__file__)),
        "outputs_sha256": {p.name: sha256(p) for p in [panel_path, drops_path, controls_path]},
        "sample": {"respondents": len(d), "economies": d["iso3"].nunique(), "economy_ids": sorted(d["iso3"].unique())},
        "drop_table": drops,
        "construction": {
            "zscore_ddof": 0,
            "age_centering": "unweighted individual mean on final primary frame",
            "any_cov_median": median_cov,
            "receive_dig_truth_table": "contract Revision 1",
            "make_dig_truth_table": "contract Revision 1",
            "fin24_revision": "Revision 2; code 4 vs 1/2/3/5/6/7; 8/9/missing excluded",
        },
        "diagnostics": {
            "w_equal_country_sum_min": float(d.groupby("iso3")["w_equal"].sum().min()),
            "w_equal_country_sum_max": float(d.groupby("iso3")["w_equal"].sum().max()),
            "m3_complete_n": int(d[["receive_dig", "make_dig"]].notna().all(axis=1).sum()),
            "secondary_nonmissing": {c: int(d[c].notna().sum()) for c in ["mobile_loan_app", "emergency_loan_source", "informal_borrow"]},
            "private_credit_latest_year_min": int(controls["privcredit_gdp_year"].min()),
            "private_credit_latest_year_max": int(controls["privcredit_gdp_year"].max()),
        },
        "environment": {"python": sys.version, "pandas": pd.__version__, "numpy": np.__version__, "os": platform.platform()},
        "evidence_status": "NOT_ADMITTED",
    }
    (OUT / "panel_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, "N": len(d), "G": d["iso3"].nunique(), "outputs": receipt["outputs_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
