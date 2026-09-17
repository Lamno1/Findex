import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import patsy
import statsmodels.formula.api as smf


ROOT = Path(r"D:/EconomicResearch")
P = ROOT / "projects/study_05_findex_crosscountry"
DATA = P / "results/stage4_build/analytical_dataset.csv"
INST = P / "data/raw/wb_credit_information_by_country_year.csv"
STAGE5 = P / "results/stage5_estimation"
OUT = P / "results/stage5_1_reconciliation"
OUT.mkdir(parents=True, exist_ok=True)

B = 999
SEED = 20260917


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def prepare() -> pd.DataFrame:
    d = pd.read_csv(DATA)
    i = pd.read_csv(INST)
    i = i[i.year.eq(2019)].copy()
    i["coverage"] = i[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
    i = i[["iso3", "coverage", "depth_credit_info_0_8", "legal_rights_0_12"]].drop_duplicates("iso3")
    d = d.merge(i, left_on="economycode", right_on="iso3", how="left", validate="many_to_one")
    assert d.coverage.notna().all()
    d["lowcov_z"] = -(d.coverage - d.coverage.mean()) / d.coverage.std(ddof=0)
    d["lowdepth_z"] = -(d.depth_credit_info_0_8 - d.depth_credit_info_0_8.mean()) / d.depth_credit_info_0_8.std(ddof=0)
    d["age_c"] = d.age - d.age.mean()
    d["age_c2"] = d.age_c ** 2
    d["w_equal"] = d.wgt / d.groupby(["economycode", "wave"]).wgt.transform("sum")
    d["wave2024"] = (d.wave == 2024).astype(int)
    d["dig_x_lowcov"] = d.digital_payment * d.lowcov_z
    d["dig_x_wave"] = d.digital_payment * d.wave2024
    d["dig_x_lowcov_x_wave"] = d.digital_payment * d.lowcov_z * d.wave2024
    d["acc_x_lowcov"] = d.account_fin * d.lowcov_z
    return d


BASE = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
PRIMARY_RHS = "digital_payment + dig_x_lowcov + " + BASE
POOLED_RHS = "digital_payment + dig_x_lowcov + dig_x_wave + dig_x_lowcov_x_wave + " + BASE


def wild_cluster(frame: pd.DataFrame, rhs: str, label: str, term: str, seed: int) -> dict:
    formula = "formal_borrow ~ " + rhs
    y_df, x_df = patsy.dmatrices(formula, frame, return_type="dataframe")
    y = np.asarray(y_df).ravel()
    X = np.asarray(x_df)
    names = list(x_df.columns)
    idx = names.index(term)
    w = frame.loc[x_df.index, "w_equal"].to_numpy(dtype=float)
    groups = frame.loc[x_df.index, "economycode"].to_numpy()
    fit = smf.wls(formula, data=frame.loc[x_df.index], weights=w).fit(
        cov_type="cluster", cov_kwds={"groups": groups, "use_correction": True}
    )
    beta = np.asarray(fit.params)
    se = float(fit.bse.iloc[idx])
    observed_t = float(beta[idx] / se)
    # Null-imposed score bootstrap: impose H0 on the target coefficient and
    # resample economy-level score contributions with Rademacher signs.
    beta_null = beta.copy()
    beta_null[idx] = 0.0
    residual_null = y - X @ beta_null
    bread = np.linalg.pinv((X.T * w) @ X)
    clusters = np.asarray(sorted(pd.unique(groups)))
    scores = np.vstack([X[groups == g].T @ (w[groups == g] * residual_null[groups == g]) for g in clusters])
    rng = np.random.default_rng(seed)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(B, len(clusters)))
    draws = np.empty(B)
    for b in range(B):
        beta_star = bread @ (signs[b] @ scores)
        draws[b] = beta_star[idx] / se
    p = (1.0 + np.sum(np.abs(draws) >= abs(observed_t))) / (B + 1.0)
    return {
        "specification": label,
        "term": term,
        "estimate": float(beta[idx]),
        "se_cluster": se,
        "p_cluster": float(fit.pvalues.iloc[idx]),
        "ci95_lo": float(beta[idx] - 1.96 * se),
        "ci95_hi": float(beta[idx] + 1.96 * se),
        "wild_p_rademacher": float(p),
        "wild_B": B,
        "wild_seed": SEED,
        "N": int(len(frame)),
        "G": int(frame.economycode.nunique()),
        "weight": "w_equal",
        "cluster": "economy",
        "estimator": "WLS LPM; null-imposed cluster-score Rademacher bootstrap",
    }


def read_results() -> pd.DataFrame:
    return pd.read_csv(STAGE5 / "estimates.csv")


def main() -> None:
    d = prepare()
    wb_rows = []
    for wave in (2021, 2024):
        wb_rows.append(wild_cluster(d[d.wave.eq(wave)].copy(), PRIMARY_RHS, f"PRIMARY_{wave}", "dig_x_lowcov", SEED + wave))
    wb_rows.append(wild_cluster(d, POOLED_RHS, "SECONDARY_POOLED_2021_2024", "dig_x_lowcov", SEED + 1))
    wb_rows.append(wild_cluster(d, POOLED_RHS, "SECONDARY_POOLED_2021_2024", "dig_x_lowcov_x_wave", SEED + 2))
    wb = pd.DataFrame(wb_rows)
    wb.to_csv(OUT / "wild_cluster_bootstrap.csv", index=False)

    est = read_results()
    def val(spec, term):
        return float(est.loc[(est.specification == spec) & (est.term == term), "estimate"].iloc[0])
    s21 = val("PRIMARY_M1_M2_2021", "dig_x_lowcov")
    s24 = val("PRIMARY_M1_M2_2024", "dig_x_lowcov")
    pbase = val("SECONDARY_POOLED_2021_2024", "dig_x_lowcov")
    pinc = val("SECONDARY_POOLED_2021_2024", "dig_x_lowcov_x_wave")
    rows = [
        {"quantity": "2021 gradient", "separate_wave": s21, "pooled_implied": pbase, "difference_pooled_minus_separate": pbase - s21, "unit": "probability points", "explanation": "Pooled base interaction is the 2021 reference gradient under the pooled parameterization; it is jointly estimated with common slopes and pooled composition."},
        {"quantity": "2024 gradient", "separate_wave": s24, "pooled_implied": pbase + pinc, "difference_pooled_minus_separate": pbase + pinc - s24, "unit": "probability points", "explanation": "Pooled 2024 gradient is base interaction plus the 2024 triple interaction; separate and pooled regressions need not coincide because coefficients are jointly estimated with pooled controls, FE, weights and composition."},
        {"quantity": "2024 minus 2021 gradient", "separate_wave": s24 - s21, "pooled_implied": pinc, "difference_pooled_minus_separate": pinc - (s24 - s21), "unit": "probability points", "explanation": "Both are descriptive contrasts; no new equality test was pre-specified, so the contrast is not assigned a formal p-value here."},
    ]
    pd.DataFrame(rows).to_csv(OUT / "cross_specification_reconciliation.csv", index=False)

    loo = pd.read_csv(STAGE5 / "leave_one_economy_out.csv")
    loo_rows = []
    if not loo.empty:
        for wave in (2021, 2024):
            q = loo[loo.specification.eq(f"ROBUSTNESS_LOO_{wave}")]
            loo_rows.append({"specification": f"ROBUSTNESS_LOO_{wave}", "n_runs": int(len(q)), "min_estimate": float(q.estimate.min()), "max_estimate": float(q.estimate.max()), "all_negative": bool((q.estimate < 0).all())})
    pd.DataFrame(loo_rows).to_csv(OUT / "leave_one_out_audit.csv", index=False)

    hierarchy = pd.DataFrame([
        {"tier": "PRIMARY", "items": "2021 separate-wave; 2024 separate-wave", "interpretation": "Wave-specific associational gradients under qualified-comparable exposure"},
        {"tier": "SECONDARY", "items": "Pooled descriptive model; depth specifications", "interpretation": "Cross-wave descriptive contrast and separate institutional dimensions"},
        {"tier": "SENSITIVITY", "items": "Account-fin Specification B; unweighted estimates", "interpretation": "Selection/access sensitivity, not a superior control or mechanism test"},
        {"tier": "ROBUSTNESS", "items": "Wild-cluster bootstrap; leave-one-economy-out", "interpretation": "Inference and sample-influence checks"},
        {"tier": "EXPLORATORY", "items": "Any non-frozen analysis", "interpretation": "Not eligible for primary contribution claims"},
    ])
    hierarchy.to_csv(OUT / "result_hierarchy.csv", index=False)

    checks = {
        "dataset_sha256": sha(DATA),
        "stage5_estimates_sha256": sha(STAGE5 / "estimates.csv"),
        "wild_cluster_bootstrap_sha256": sha(OUT / "wild_cluster_bootstrap.csv"),
        "cross_specification_reconciliation_sha256": sha(OUT / "cross_specification_reconciliation.csv"),
        "leave_one_out_audit_sha256": sha(OUT / "leave_one_out_audit.csv"),
        "result_hierarchy_sha256": sha(OUT / "result_hierarchy.csv"),
        "bootstrap_B": B,
        "bootstrap_seed_base": SEED,
        "formal_beta_equality_test": False,
        "formal_beta_equality_test_reason": "E3 was frozen as a descriptive contrast; no new equality hypothesis test was pre-specified.",
    }
    (OUT / "stage5_1_receipt.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
    checks["stage5_1_receipt_sha256"] = sha(OUT / "stage5_1_receipt.json")
    (OUT / "result_checksum.txt").write_text("\n".join(f"{k}  {v}" for k, v in checks.items() if k.endswith("sha256")) + "\n", encoding="utf-8")
    print(json.dumps({"bootstrap": wb_rows, "reconciliation": rows, "loo": loo_rows, "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
