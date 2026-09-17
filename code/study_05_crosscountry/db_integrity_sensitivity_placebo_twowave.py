"""Extend CLAUDE-S5-DB-INTEGRITY-TWOWAVE-20260918-001 to the informal-borrowing
placebo check (Stage 18). Same exclusion (China DB2018, Saudi Arabia DB2020),
same re-standardization of lowcov_z over 91 economies, applied to the placebo
outcome instead of formal_borrow. Row-level reconstruction and validation logic
copied from stage18_placebo.py (that file does not import cleanly as a module
because it executes on import; the reconstruction is short enough to duplicate
here rather than refactor a frozen, already-manuscript-cited script).
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
STAGE18 = P / "results/stage18_placebo/informal_borrow_estimates.csv"
OUT = P / "results/stage21_db_integrity_two_wave"
DROP_ISO3 = {"CHN", "SAU"}
B = 999
SEED = 20260918

sample = pd.read_csv(MANIFEST, dtype={"economy_code": str})
primary93 = set(sample.loc[sample.final_sample.eq(1), "economy_code"])
assert len(primary93) == 93
primary91 = primary93 - DROP_ISO3
assert len(primary91) == 91


def load_raw(wave: int) -> pd.DataFrame:
    d = pd.read_csv(ACQ / f"FINDEX_{wave}/raw_microdata.csv", encoding="cp1252", low_memory=False)
    d = d[d.economycode.isin(primary91)].copy()
    d["wave"] = wave
    return d


def build_wave(wave: int) -> pd.DataFrame:
    d = load_raw(wave)
    d["digital_payment"] = d.anydigpayment.map({1: 1, 0: 0})
    d["female_binary"] = d.female.map({1: 1, 2: 0})
    d["education"] = d.educ.where(d.educ.isin([1, 2, 3]))
    d["income_quintile"] = d.inc_q.where(d.inc_q.isin([1, 2, 3, 4, 5]))
    d["age"] = pd.to_numeric(d.age, errors="coerce")
    d["informal_borrow"] = d.fin22b.map({1: 1, 2: 0})
    cols = ["economycode", "wave", "wgt", "digital_payment",
            "female_binary", "age", "education", "income_quintile", "informal_borrow"]
    return d[cols]


inst = pd.read_csv(INST)
inst = inst[inst.year.eq(2019)].copy()
inst["coverage"] = inst[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
inst = inst[["iso3", "coverage"]].drop_duplicates("iso3")

BASE_RHS = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
M2_RHS = "digital_payment + dig_x_lowcov + " + BASE_RHS


def prepare_wave(wave: int) -> pd.DataFrame:
    d = build_wave(wave).merge(inst, left_on="economycode", right_on="iso3", how="left", validate="many_to_one")
    assert d.coverage.notna().all()
    core = ["digital_payment", "wgt", "female_binary", "age", "education", "income_quintile"]
    d = d.loc[d[core].notna().all(axis=1)].copy()
    cov_mean = d.groupby("economycode").coverage.first().mean()
    cov_sd = d.groupby("economycode").coverage.first().std(ddof=0)
    d["lowcov_z"] = -(d.coverage - cov_mean) / cov_sd
    d["age_c"] = d.age - d.age.mean()
    d["age_c2"] = d.age_c ** 2
    d["w_equal"] = d.wgt / d.groupby("economycode").wgt.transform("sum")
    d["dig_x_lowcov"] = d.digital_payment * d.lowcov_z
    return d


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


baseline = pd.read_csv(STAGE18)

rows = []
for wave in (2021, 2024):
    p = prepare_wave(wave)
    core_placebo = p.dropna(subset=["informal_borrow"]).copy()
    assert core_placebo.economycode.nunique() == 91
    res = wild_cluster_p(core_placebo, "informal_borrow", M2_RHS, "dig_x_lowcov", "w_equal", SEED + wave)
    base_row = baseline[(baseline.wave == wave) & (baseline.term == "dig_x_lowcov")]
    base = float(base_row.estimate.iloc[0])
    rel_change = abs(res["estimate"] - base) / abs(base)
    rows.append({
        "wave": wave, "outcome": "informal_borrow",
        "primary_estimate_93economies": base,
        "excl_chn_sau_estimate_91economies": res["estimate"],
        "se_cluster": res["se_cluster"], "ci95_lo": res["ci95_lo"], "ci95_hi": res["ci95_hi"],
        "p_cluster": res["p_cluster"], "wild_p_rademacher": res["wild_p_rademacher"],
        "N": res["N"], "G": res["G"], "relative_change_vs_primary": rel_change,
        "same_sign": bool(np.sign(res["estimate"]) == np.sign(base)),
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "placebo_excl_chn_sau.csv", index=False)
print(df.to_string(index=False))
