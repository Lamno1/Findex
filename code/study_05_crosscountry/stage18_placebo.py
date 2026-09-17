"""Stage 18 -- Placebo test (informal borrowing) for the 93-economy/2021-2024 line.

ADDITIVE analysis, not remediation. Third item on the owner's journal-hardening
list, after Stage 17's items #1 (external-validity reweighting) and #2
(macro-control interactions). Does not alter, delete, or re-estimate anything
in results/stage5_estimation/, results/stage17_external_validity/, or the
manuscript's existing Results numbers; this is a new subsection layered on top.

Construction. informal_borrow is built exactly analogous to the frozen
H-000500 construction (code/study_05_crosscountry/build_stage1_codex.py,
line ~127: binary(fin22b, {1}, {2})): 1 if fin22b==1, 0 if fin22b==2, missing
(dropped) for DK/refused codes 3/4 or physical missing. This is its own
complete-case sample -- informal_borrow's own missingness is NOT part of the
primary formal_borrow analysis sample's complete-case criteria, so the
placebo N/G legitimately differs from the primary sample's N/G, exactly as
it did for the frozen H-000500 line's own informal-borrowing placebo.

The row-level sample is reconstructed by replicating
code/study_05_crosscountry/build_stage4_dataset.py's load() filter (raw
Findex row -> restrict to the 93-economy manifest) rather than joining onto
results/stage4_build/analytical_dataset.csv, because that file does not
retain a respondent-level ID and cannot be safely joined back to fin22b.
The primary covariate-completeness criteria (digital_payment, wgt,
female_binary, age, education, income_quintile all non-missing) are applied
identically, so this script's own re-derived formal_borrow-based N/G is
checked against results/stage5_estimation/estimates.csv as a validation that
the row-level reconstruction is faithful before informal_borrow's own
missingness is additionally applied.

Model: identical M2 specification already used for formal_borrow (same RHS,
same w_equal-style economy-wave weighting, same economy-clustered SE, same
null-imposed cluster-score Rademacher wild-cluster bootstrap already
implemented in stage17_external_validity.py's wild_cluster_p, generalised
here to accept an arbitrary outcome column), with informal_borrow as the
outcome instead of formal_borrow, estimated separately for 2021 and 2024.

Sources:
  data/acquisition/FINDEX_2021/raw_microdata.csv, FINDEX_2024/raw_microdata.csv
  data/manifests/findex_2021_2024_primary_93.csv
  data/raw/wb_credit_information_by_country_year.csv (2019 coverage)
  results/stage5_estimation/estimates.csv (validation cross-check only)

Outputs (this run only, does not touch any existing file):
  results/stage18_placebo/informal_borrow_estimates.csv
  results/stage18_placebo/validation_check.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import patsy
import statsmodels.formula.api as smf

ROOT = Path(r"D:/EconomicResearch")
P = ROOT / "projects/study_05_findex_crosscountry"
ACQ = P / "data/acquisition"
MANIFEST = P / "data/manifests/findex_2021_2024_primary_93.csv"
INST = P / "data/raw/wb_credit_information_by_country_year.csv"
STAGE5 = P / "results/stage5_estimation/estimates.csv"
OUT = P / "results/stage18_placebo"
OUT.mkdir(parents=True, exist_ok=True)

B = 999
SEED = 20261801

sample = pd.read_csv(MANIFEST, dtype={"economy_code": str})
primary93 = set(sample.loc[sample.final_sample.eq(1), "economy_code"])
assert len(primary93) == 93


def load_raw(wave: int) -> pd.DataFrame:
    d = pd.read_csv(ACQ / f"FINDEX_{wave}/raw_microdata.csv", encoding="cp1252", low_memory=False)
    d = d[d.economycode.isin(primary93)].copy()
    d["wave"] = wave
    return d


def build_wave(wave: int) -> pd.DataFrame:
    d = load_raw(wave)
    d["formal_borrow"] = d.fin22a.map({1: 1, 2: 0})
    d["digital_payment"] = d.anydigpayment.map({1: 1, 0: 0})
    d["female_binary"] = d.female.map({1: 1, 2: 0})
    d["education"] = d.educ.where(d.educ.isin([1, 2, 3]))
    d["income_quintile"] = d.inc_q.where(d.inc_q.isin([1, 2, 3, 4, 5]))
    d["age"] = pd.to_numeric(d.age, errors="coerce")
    d["informal_borrow"] = d.fin22b.map({1: 1, 2: 0})
    cols = ["economycode", "wave", "wgt", "formal_borrow", "digital_payment",
            "female_binary", "age", "education", "income_quintile", "informal_borrow"]
    return d[cols]


frames = {wave: build_wave(wave) for wave in (2021, 2024)}

# --- Validation: replicate the primary formal_borrow complete-case N/G and
# check against results/stage5_estimation/estimates.csv before trusting the
# reconstructed row-level sample for the placebo. ---
primary_est = pd.read_csv(STAGE5)
validation = {}
for wave in (2021, 2024):
    d = frames[wave]
    core = ["formal_borrow", "digital_payment", "wgt", "female_binary", "age", "education", "income_quintile"]
    complete = d[core].notna().all(axis=1)
    d_complete = d.loc[complete]
    n_repro, g_repro = len(d_complete), d_complete.economycode.nunique()
    row = primary_est[(primary_est.specification == f"PRIMARY_M1_M2_{wave}") & (primary_est.term == "dig_x_lowcov")]
    n_expected, g_expected = int(row.N.iloc[0]), int(row.G.iloc[0])
    validation[str(wave)] = {
        "reconstructed_N": int(n_repro), "reconstructed_G": int(g_repro),
        "expected_N": n_expected, "expected_G": g_expected,
        "N_match": n_repro == n_expected, "G_match": g_repro == g_expected,
    }
    if n_repro != n_expected or g_repro != g_expected:
        raise SystemExit(f"Row-level reconstruction for {wave} does not match primary sample: {validation[str(wave)]}")

(OUT / "validation_check.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

# --- Attach 2019 coverage moderator (same construction as stage17/stage5) ---
inst = pd.read_csv(INST)
inst = inst[inst.year.eq(2019)].copy()
inst["coverage"] = inst[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
inst = inst[["iso3", "coverage"]].drop_duplicates("iso3")


def prepare_wave(wave: int) -> pd.DataFrame:
    d = frames[wave].merge(inst, left_on="economycode", right_on="iso3", how="left", validate="many_to_one")
    assert d.coverage.notna().all()
    core = ["formal_borrow", "digital_payment", "wgt", "female_binary", "age", "education", "income_quintile"]
    d = d.loc[d[core].notna().all(axis=1)].copy()
    d["lowcov_z"] = -(d.coverage - d.coverage.mean()) / d.coverage.std(ddof=0)
    d["age_c"] = d.age - d.age.mean()
    d["age_c2"] = d.age_c ** 2
    d["w_equal"] = d.wgt / d.groupby("economycode").wgt.transform("sum")
    d["dig_x_lowcov"] = d.digital_payment * d.lowcov_z
    return d


BASE_RHS = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
M2_RHS = "digital_payment + dig_x_lowcov + " + BASE_RHS


def wild_cluster_p(frame: pd.DataFrame, outcome: str, rhs: str, term: str, weight_col: str, seed: int) -> dict:
    formula = f"{outcome} ~ " + rhs
    y_df, x_df = patsy.dmatrices(formula, frame, return_type="dataframe")
    yv = np.asarray(y_df).ravel()
    X = np.asarray(x_df)
    names = list(x_df.columns)
    idx = names.index(term)
    w = frame.loc[x_df.index, weight_col].to_numpy(dtype=float)
    groups = frame.loc[x_df.index, "economycode"].to_numpy()
    fit = smf.wls(formula, data=frame.loc[x_df.index], weights=w).fit(
        cov_type="cluster", cov_kwds={"groups": groups, "use_correction": True}
    )
    beta = np.asarray(fit.params)
    se = float(fit.bse.iloc[idx])
    observed_t = float(beta[idx] / se)
    beta_null = beta.copy()
    beta_null[idx] = 0.0
    residual_null = yv - X @ beta_null
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
        "estimate": float(beta[idx]), "se_cluster": se, "p_cluster": float(fit.pvalues.iloc[idx]),
        "ci95_lo": float(beta[idx] - 1.96 * se), "ci95_hi": float(beta[idx] + 1.96 * se),
        "wild_p_rademacher": float(p), "N": int(len(frame)), "G": int(frame.economycode.nunique()),
    }


rows = []
for wave in (2021, 2024):
    p = prepare_wave(wave)
    core_placebo = p.dropna(subset=["informal_borrow"]).copy()
    dp_res = wild_cluster_p(core_placebo, "informal_borrow", M2_RHS, "digital_payment", "w_equal", SEED + wave)
    ix_res = wild_cluster_p(core_placebo, "informal_borrow", M2_RHS, "dig_x_lowcov", "w_equal", SEED + wave + 1)
    rows.append({"wave": wave, "term": "digital_payment", **dp_res})
    rows.append({"wave": wave, "term": "dig_x_lowcov", **ix_res})

out_df = pd.DataFrame(rows)
out_df.to_csv(OUT / "informal_borrow_estimates.csv", index=False)
print(out_df.to_string(index=False))
print()
print(json.dumps(validation, indent=2))
