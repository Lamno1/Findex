"""Read-only Stage-0 checks for H-000501; estimates no EXP-S5-002 model."""

from __future__ import annotations

import hashlib
import json
import os
import platform
from pathlib import Path
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "projects" / "study_05_findex_crosscountry"
PANEL = PROJECT / "results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"
MICRO = ROOT / "data/raw/data_micro_findex_2024_vietnam.xlsx"
MULTI = PROJECT / "data/raw/wb_credit_information_by_country_year.csv"
SNAPSHOT = PROJECT / "data/raw/wb_credit_information_latest_snapshot.csv"
GDP = PROJECT / "data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json"
CREDIT = PROJECT / "data/raw/wdi_FS.AST.PRVT.GD.ZS_2000_2023.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def latest_wdi(path: Path) -> dict[str, dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload[1]
    result: dict[str, dict[str, object]] = {}
    for row in rows:
        iso3 = row.get("countryiso3code")
        value = row.get("value")
        year = int(row["date"])
        if not iso3 or value is None or year > 2023:
            continue
        if iso3 not in result or year > int(result[iso3]["year"]):
            result[iso3] = {"value": float(value), "year": year}
    return result


def scan_q1_artifacts() -> list[dict[str, object]]:
    terms = ("logit", "probit", "poisson", "log-odds", "log_odds", "log-risk", "log_risk", "m6.2")
    matches: list[dict[str, object]] = []
    results = PROJECT / "results"
    for path in results.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".csv"}:
            continue
        if path.stat().st_size > 5_000_000:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        hits = [term for term in terms if term in lower]
        if hits:
            lines = [line.strip() for line in text.splitlines() if any(t in line.lower() for t in hits)]
            matches.append({
                "path": path.relative_to(PROJECT).as_posix(),
                "terms": hits,
                "lines": lines[:12],
            })
    return matches


def main() -> None:
    pre_failures: list[str] = []
    expected_hashes = {
        "panel": "ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9",
        "micro": "ca307a0c3dfd54dc945a18fb03c58b014143bc21c90761f71fe304e6a2f90fce",
        "multi": "2d7c9a27efb59ff7bbcb894f3c0ecb51782dd8b1076c347868aae047fe3d6288",
        "snapshot": "ef0c67f9c7d44b67939e088f0aab2e578f7ba0d7f2eeadc4093c0103cc1bd06c",
    }
    paths = {"panel": PANEL, "micro": MICRO, "multi": MULTI, "snapshot": SNAPSHOT}
    hashes = {name: sha256(path) for name, path in paths.items()}

    panel = pd.read_csv(PANEL)
    micro = pd.read_excel(
        MICRO,
        sheet_name="findex_microdata_2025_labelled_",
        usecols=["economy", "economycode", "regionwb", "pop_adult", "wgt", "fin22a", "fin22b"],
    )
    economy_counts = micro.groupby("economycode", observed=True).size().sort_index()
    included = set(panel["iso3"].unique())
    released = set(micro["economycode"].dropna().unique())

    weighted_p = float(np.average(panel["formal_borrow"], weights=panel["w_equal"]))
    delta_pp = 1.0
    delta_prob = 0.01
    delta_logodds = delta_prob / (weighted_p * (1.0 - weighted_p))
    delta_logrisk = delta_prob / weighted_p

    economy_cov = panel[["iso3", "any_cov", "lowcov2019_z"]].drop_duplicates("iso3")
    q25, q75 = economy_cov["any_cov"].quantile([0.25, 0.75]).tolist()
    cov_mean = float(economy_cov["any_cov"].mean())
    cov_sd = float(economy_cov["any_cov"].std(ddof=0))
    low_at_q25 = -(q25 - cov_mean) / cov_sd
    low_at_q75 = -(q75 - cov_mean) / cov_sd
    dz_iqr = float(low_at_q25 - low_at_q75)
    delta_c = delta_pp * dz_iqr

    account = panel["account_fin"].eq(1)
    digital = panel["anydigpayment"].eq(1)
    state = np.select(
        [~account & ~digital, account & ~digital, account & digital, ~account & digital],
        ["unbanked", "account_only", "digitally_active", "digitally_active_no_fi"],
        default="invalid",
    )
    q3 = panel[["iso3", "w_equal"]].copy()
    q3["state"] = state
    q3_cells: dict[str, dict[str, object]] = {}
    for label, group in q3.groupby("state", observed=True):
        weights = group["w_equal"].to_numpy(float)
        by_economy = group.groupby("iso3", observed=True).size()
        q3_cells[str(label)] = {
            "raw_n": int(len(group)),
            "share": float(len(group) / len(q3)),
            "kish_n_eff_w_equal": float(weights.sum() ** 2 / np.square(weights).sum()),
            "economies_any": int(group["iso3"].nunique()),
            "economies_with_at_least_5_raw": int((by_economy >= 5).sum()),
        }

    multi = pd.read_csv(MULTI)
    multi["any_cov"] = multi[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
    value_columns = ["depth_credit_info_0_8", "credit_bureau_cov_pct",
                     "credit_registry_cov_pct", "legal_rights_0_12"]
    q4_window = multi[multi["year"].between(2015, 2019)].copy()
    duplicate_groups = q4_window.groupby(["iso3", "year"], dropna=False).filter(lambda x: len(x) > 1)
    nonidentical_duplicate_groups = []
    for key, group in duplicate_groups.groupby(["iso3", "year"], dropna=False):
        if any(group[column].nunique(dropna=False) > 1 for column in value_columns):
            nonidentical_duplicate_groups.append({"iso3": str(key[0]), "year": int(key[1])})
    if nonidentical_duplicate_groups:
        pre_failures.append(
            f"R6 Q4-window value-identity claim fails: {len(nonidentical_duplicate_groups)} "
            "duplicate 2015-2019 (iso3, year) groups have non-identical indicator vectors."
        )
    dedup = multi.drop_duplicates(["iso3", "year"], keep="first")
    q4 = dedup[dedup["iso3"].isin(included) & dedup["year"].between(2015, 2019)]
    q4_counts = q4[q4["any_cov"].notna()].groupby("iso3")["year"].nunique()
    q4_complete = sorted(q4_counts[q4_counts.eq(5)].index.tolist())
    family_c_size = 5 if len(q4_complete) >= 60 else 3

    informal_valid = panel["informal_borrow"].isin([0, 1])
    formal_valid = panel["formal_borrow"].isin([0, 1])
    common = formal_valid & informal_valid

    snapshot = pd.read_csv(SNAPSHOT)
    gdp = latest_wdi(GDP)
    credit = latest_wdi(CREDIT)
    basic_frame = micro.groupby("economycode", observed=True).agg(
        economy=("economy", "first"),
        region=("regionwb", "first"),
        pop_adult=("pop_adult", "first"),
    ).reset_index().rename(columns={"economycode": "iso3"})
    basic_frame["included"] = basic_frame["iso3"].isin(included).astype(int)
    basic_frame = basic_frame.merge(
        snapshot[["iso3", "credit_bureau_cov_pct", "credit_registry_cov_pct"]], how="left", on="iso3"
    )
    basic_frame["any_cov_2019"] = basic_frame[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
    basic_frame["lgdppc"] = basic_frame["iso3"].map(lambda x: np.log(gdp[x]["value"]) if x in gdp and gdp[x]["value"] > 0 else np.nan)
    basic_frame["gdp_year"] = basic_frame["iso3"].map(lambda x: gdp.get(x, {}).get("year"))
    basic_frame["privcredit_gdp"] = basic_frame["iso3"].map(lambda x: credit.get(x, {}).get("value"))
    basic_frame["privcredit_gdp_year"] = basic_frame["iso3"].map(lambda x: credit.get(x, {}).get("year"))

    q1_matches = scan_q1_artifacts()
    poisson_matches = [
        match for match in q1_matches
        if any(term in match["terms"] for term in ("poisson", "log-risk", "log_risk"))
        and "CODEX-S5-EXP-S5-002-20260913-001" not in str(match["path"])
    ]
    prereg_text = (PROJECT / "papers/study_05/PREREGISTRATION_H000501.md").read_text(encoding="utf-8")
    contract_text = (PROJECT / "papers/study_05/VARIABLE_CONTRACT_H000501.md").read_text(encoding="utf-8")
    hypothesis_text = (PROJECT / "research_council/hypotheses/H-000501.json").read_text(encoding="utf-8")
    q1_known_disclosed = all(
        token in prereg_text
        for token in ("pre-specified post-result diagnostic", "−0.16558915", "−0.08842991")
    )
    income_group_removed = all(
        "income_group" not in line
        for line in contract_text.splitlines()
        if line.strip().startswith("- Regressors, **fixed list")
    ) and "`income_group` REMOVED" in contract_text

    missing_q5_before_rule = basic_frame.loc[
        basic_frame[["any_cov_2019", "lgdppc", "privcredit_gdp", "region", "pop_adult"]].isna().any(axis=1),
        ["iso3", "economy", "included", "any_cov_2019", "lgdppc", "privcredit_gdp", "region", "pop_adult"],
    ]
    all_three_missing = basic_frame[["any_cov_2019", "lgdppc", "privcredit_gdp"]].isna().all(axis=1)
    q5_frame = basic_frame.loc[~all_three_missing].copy()
    for column, indicator in (
        ("any_cov_2019", "any_cov_2019_missing"),
        ("lgdppc", "lgdppc_missing"),
        ("privcredit_gdp", "privcredit_missing"),
    ):
        q5_frame[indicator] = q5_frame[column].isna().astype(int)
        fill_value = 0.0 if column == "any_cov_2019" else float(q5_frame[column].median())
        q5_frame[column] = q5_frame[column].fillna(fill_value)
    missing_q5_after_rule = q5_frame.loc[
        q5_frame[["any_cov_2019", "lgdppc", "privcredit_gdp", "region", "pop_adult"]].isna().any(axis=1)
    ]
    actual_regions = sorted(basic_frame["region"].dropna().astype(str).unique().tolist())
    registered_reference = "Sub-Saharan Africa (excluding high income)"
    reference_exact_match = registered_reference in actual_regions
    region_counts_139 = q5_frame.groupby("region", observed=True).size().sort_values(ascending=False)
    reference_is_modal = int(region_counts_139[registered_reference]) == int(region_counts_139.max())
    exact_macro_map_tokens = (
        "Asia-Pacific = {'East Asia & Pacific (excluding high income)', 'South Asia'}",
        "Africa & Middle East = {'Sub-Saharan Africa (excluding high income)', 'Middle East & North Africa (excluding high income)'}",
        "Europe, Americas & High income = {'Europe & Central Asia (excluding high income)', 'Latin America & Caribbean (excluding high income)', 'High income'}",
    )
    macro_map_frozen = all(token in hypothesis_text for token in exact_macro_map_tokens)
    entropy_max_iter_numeric = "max_iterations = 5000" in contract_text
    entropy_quality_thresholds_frozen = all(
        token in contract_text for token in ("max_c(w_c) / mean_c(w_c) > 10", "Kish ESS = (Σ w_c)² / Σ(w_c²) < 48")
    )

    failures = list(pre_failures)
    if hashes != {name: expected_hashes[name] for name in hashes}:
        failures.append("One or more frozen input hashes do not match.")
    if len(micro) != 144090 or len(released) != 140:
        failures.append("Findex workbook semantic shape differs from the registered 144090-row/140-economy release.")
    if len(included) != 97 or len(released - included) != 43:
        failures.append("The registered 97 included / 43 excluded split does not reproduce.")
    if not q1_known_disclosed:
        failures.append("R3 does not fully disclose the known logit/probit Q1 inputs in the preregistration.")
    if poisson_matches:
        failures.append("A results artifact contains a Poisson/log-link/log-risk marker; S3 may not be prospective.")
    if not income_group_removed:
        failures.append("income_group was not removed consistently from the registered Q5 model.")
    if set(basic_frame.loc[all_three_missing, "iso3"]) != {"TWN"} or len(q5_frame) != 139 or not missing_q5_after_rule.empty:
        failures.append(
            "R4 missing_data_rule does not resolve exactly to TWN dropped and a complete 139-economy Q5 frame."
        )
    if not reference_exact_match or not macro_map_frozen:
        failures.append(
            "R4 region reference or explicit seven-to-three macro-region mapping does not match the frozen data/JSON."
        )
    if not entropy_max_iter_numeric or not entropy_quality_thresholds_frozen:
        failures.append(
            "The entropy-balancing protocol is not fully frozen: it gives no numeric maximum-iteration cap and leaves extreme-weight/low-ESS thresholds to the future receipt."
        )

    disclosures = []
    if not reference_is_modal:
        disclosures.append(
            "The selected region reference is valid but not modal on the 139-economy frame: High income has 46 economies and Sub-Saharan Africa (excluding high income) has 35. The false modal rationale was corrected before freeze; the selected reference was retained."
        )

    receipt = {
        "run_id": "CODEX-S5-H000501-STAGE0-20260913-005",
        "stage": "H-000501_STAGE0_NO_OUTCOME_MODELS",
        "created_by": "codex",
        "date": "2026-09-13",
        "exp_s5_002_estimation_run": False,
        "verdict": "FAIL" if failures else ("PASS_WITH_DISCLOSURES" if disclosures else "PASS"),
        "failures": failures,
        "disclosures": disclosures,
        "input_paths_resolved": {name: str(path) for name, path in paths.items()},
        "input_hashes": {
            name: {"actual": hashes[name], "expected": expected_hashes[name], "match": hashes[name] == expected_hashes[name]}
            for name in hashes
        },
        "findex_semantics": {
            "rows": int(len(micro)),
            "columns_registered": 199,
            "distinct_economies": int(len(released)),
            "per_economy_n_min": int(economy_counts.min()),
            "per_economy_n_median": float(economy_counts.median()),
            "per_economy_n_max": int(economy_counts.max()),
            "vnm_n": int(economy_counts.get("VNM", 0)),
            "included_economies": int(len(included)),
            "excluded_economies": int(len(released - included)),
        },
        "q1_status_check": {
            "known_logit_probit_disclosed": q1_known_disclosed,
            "all_nonlinear_matches": q1_matches,
            "poisson_or_loglink_matches": poisson_matches,
            "s3_modified_poisson_still_prospective": not poisson_matches,
        },
        "q2_common_frame": {
            "n": int(common.sum()),
            "economies": int(panel.loc[common, "iso3"].nunique()),
            "rows_dropped_from_frozen_panel": int((~common).sum()),
        },
        "q3_exposure_cells": q3_cells,
        "q3_four_state_interpretation_gate": {
            "kish_n_eff_min": 300,
            "economies_with_at_least_5_raw_min": 12,
            "resolved_for_digitally_active_no_fi": bool(
                q3_cells["digitally_active_no_fi"]["kish_n_eff_w_equal"] >= 300
                and q3_cells["digitally_active_no_fi"]["economies_with_at_least_5_raw"] >= 12
            ),
        },
        "q4": {
            "rule": "five distinct years after value-identity-verified (iso3, year) deduplication",
            "duplicate_rows_in_duplicate_groups": int(len(duplicate_groups)),
            "duplicate_groups_n": int(duplicate_groups.groupby(["iso3", "year"]).ngroups),
            "duplicate_economies": sorted(duplicate_groups["iso3"].unique().tolist()),
            "nonidentical_duplicate_groups": nonidentical_duplicate_groups,
            "complete_case_economies_n": int(len(q4_complete)),
            "complete_case_economies": q4_complete,
            "family_c_size_frozen_candidate": family_c_size,
        },
        "stage0_constants": {
            "p_bar_w_equal": weighted_p,
            "delta_pp": delta_pp,
            "delta_prob": delta_prob,
            "delta_logodds_first_order_local": delta_logodds,
            "delta_logrisk_first_order_local": delta_logrisk,
            "any_cov_p25": float(q25),
            "any_cov_p75": float(q75),
            "dz_IQR_lowcov_z": dz_iqr,
            "delta_C_pp": delta_c,
        },
        "q5_basic_frame": {
            "released_rows_before_R4_rule": int(len(basic_frame)),
            "rows_after_R4_rule": int(len(q5_frame)),
            "included_after_R4_rule": int(q5_frame["included"].sum()),
            "excluded_after_R4_rule": int((1 - q5_frame["included"]).sum()),
            "missing_before_R4_rule": {
                col: int(basic_frame[col].isna().sum())
                for col in ["any_cov_2019", "lgdppc", "privcredit_gdp", "region", "pop_adult"]
            },
            "all_three_missing_economies_dropped": basic_frame.loc[all_three_missing, "iso3"].tolist(),
            "rows_with_any_registered_covariate_missing_before_rule": missing_q5_before_rule.to_dict(orient="records"),
            "rows_with_any_registered_covariate_missing_after_rule": int(len(missing_q5_after_rule)),
            "imputation_indicator_sums_after_drop": {
                col: int(q5_frame[col].sum())
                for col in ["any_cov_2019_missing", "lgdppc_missing", "privcredit_missing"]
            },
            "gdp_vintage_min": int(basic_frame["gdp_year"].dropna().min()),
            "gdp_vintage_max": int(basic_frame["gdp_year"].dropna().max()),
            "privcredit_vintage_min": int(basic_frame["privcredit_gdp_year"].dropna().min()),
            "privcredit_vintage_max": int(basic_frame["privcredit_gdp_year"].dropna().max()),
            "income_group_removed_from_registered_model": income_group_removed,
            "actual_region_levels": actual_regions,
            "region_counts_139": {str(k): int(v) for k, v in region_counts_139.items()},
            "registered_region_reference": registered_reference,
            "registered_region_reference_exact_match": reference_exact_match,
            "registered_region_reference_is_modal": reference_is_modal,
            "explicit_macro_region_map_frozen": macro_map_frozen,
            "entropy_numeric_max_iter_frozen": entropy_max_iter_numeric,
            "entropy_quality_thresholds_frozen": entropy_quality_thresholds_frozen,
        },
        "prohibited_action_confirmation": "No Q1-Q5 interaction, inclusion-logit, IPW outcome, or other EXP-S5-002 model was estimated.",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
        },
    }
    # Force standards-compliant JSON: missing numeric values are null, never NaN.
    receipt = json.loads(pd.Series([receipt]).to_json(orient="records"))[0]
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    output = PROJECT / "research_council/reports/CODEX-S5-H000501-STAGE0-20260913-005.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
