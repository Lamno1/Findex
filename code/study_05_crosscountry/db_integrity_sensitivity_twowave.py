"""Sensitivity of the Stage 5 two-wave (93-economy, 2021+2024) primary M2 estimate
to excluding China (DB2018) and Saudi Arabia (DB2020) -- the two economies the World
Bank's December 2020 'Review of Data Irregularities in Doing Business' specifically
implicates for the Getting Credit indicator that constructs the 2019 coverage moderator.

This extends CODEX-S5-DB-INTEGRITY-20260910-001 / CLAUDE-S5R-DB-INTEGRITY-20260910-001,
which ran this check only on the earlier single-wave 97-economy 2024 frame (H-000500/501).
The current manuscript's primary specification is the two-wave 93-economy design built in
Stage 4 and estimated in Stage 5 (results/stage5_estimation/estimates.csv); this script
re-runs the same exclusion-and-re-standardize check on that frame, separately by wave, using
the identical primary_rhs specification and wild-cluster (Rademacher score-bootstrap)
inference already used throughout the manuscript.

No existing Stage 4/5 output is modified. This is an additive robustness check.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import patsy
import statsmodels.formula.api as smf

ROOT = Path(r"D:/EconomicResearch")
P = ROOT / "projects/study_05_findex_crosscountry"
PANEL = P / "results/stage4_build/analytical_dataset.csv"
INST = P / "data/raw/wb_credit_information_by_country_year.csv"
STAGE5 = P / "results/stage5_estimation/estimates.csv"
OUT = P / "results/stage21_db_integrity_two_wave"
DROP_ISO3 = {"CHN", "SAU"}
B = 999
SEED = 20260918

BASE_RHS = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
PRIMARY_RHS = "digital_payment + dig_x_lowcov + " + BASE_RHS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def wild_cluster_p(frame: pd.DataFrame, rhs: str, term: str, weight_col: str, seed: int) -> dict:
    formula = "formal_borrow ~ " + rhs
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


def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")

    panel_sha = sha256(PANEL)
    inst_sha = sha256(INST)

    d = pd.read_csv(PANEL)
    assert d.economycode.nunique() == 93

    i = pd.read_csv(INST)
    i = i[i.year.eq(2019)].copy()
    i["coverage"] = i[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
    i = i[["iso3", "coverage"]].drop_duplicates("iso3")

    found = set(d.loc[d.economycode.isin(DROP_ISO3), "economycode"].unique())
    if found != DROP_ISO3:
        raise RuntimeError(f"FAIL_CLOSED expected {sorted(DROP_ISO3)}, found {sorted(found)}")

    restricted = d.loc[~d.economycode.isin(DROP_ISO3)].copy()
    assert restricted.economycode.nunique() == 91

    restricted = restricted.merge(i, left_on="economycode", right_on="iso3", how="left", validate="many_to_one")
    assert restricted.coverage.notna().all()

    cov_mean = restricted.groupby("economycode").coverage.first().mean()
    cov_sd = restricted.groupby("economycode").coverage.first().std(ddof=0)
    restricted["lowcov_z"] = -(restricted.coverage - cov_mean) / cov_sd

    restricted["age_c"] = restricted.age - restricted.age.mean()
    restricted["age_c2"] = restricted.age_c ** 2
    restricted["w_equal"] = restricted.wgt / restricted.groupby(["economycode", "wave"]).wgt.transform("sum")
    restricted["dig_x_lowcov"] = restricted.digital_payment * restricted.lowcov_z

    primary_est = pd.read_csv(STAGE5)

    def primary_value(wave: int) -> float:
        row = primary_est[(primary_est.specification == f"PRIMARY_M1_M2_{wave}") & (primary_est.term == "dig_x_lowcov")]
        return float(row.estimate.iloc[0])

    rows = []
    for wave in (2021, 2024):
        q = restricted[restricted.wave.eq(wave)].copy()
        res = wild_cluster_p(q, PRIMARY_RHS, "dig_x_lowcov", "w_equal", SEED + wave)
        base = primary_value(wave)
        rel_change = abs(res["estimate"] - base) / abs(base)
        rows.append({
            "wave": wave,
            "primary_estimate_93economies": base,
            "excl_chn_sau_estimate_91economies": res["estimate"],
            "se_cluster": res["se_cluster"],
            "ci95_lo": res["ci95_lo"], "ci95_hi": res["ci95_hi"],
            "p_cluster": res["p_cluster"], "wild_p_rademacher": res["wild_p_rademacher"],
            "N": res["N"], "G": res["G"],
            "relative_change_vs_primary": rel_change,
            "same_sign": bool(np.sign(res["estimate"]) == np.sign(base)),
            "moderator_mean_91economies": float(cov_mean),
            "moderator_sd_ddof0_91economies": float(cov_sd),
        })

    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True)
    df.to_csv(OUT / "excl_chn_sau_estimates.csv", index=False)

    receipt = {
        "run_id": "CLAUDE-S5-DB-INTEGRITY-TWOWAVE-20260918-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Extend CODEX-S5-DB-INTEGRITY-20260910-001 (single-wave 97-economy 2024 frame) "
            "to the current two-wave 93-economy primary design: exclude China (DB2018) and "
            "Saudi Arabia (DB2020), re-standardize the 2019 coverage moderator over the "
            "remaining 91 economies, and re-fit the frozen primary M2 specification "
            "separately for 2021 and 2024, with wild-cluster (Rademacher) inference."
        ),
        "excluded_economies": sorted(DROP_ISO3),
        "panel": str(PANEL), "panel_sha256": panel_sha,
        "institutional_source": str(INST), "institutional_sha256": inst_sha,
        "code": str(Path(__file__)), "code_sha256": sha256(Path(__file__)),
        "specification": PRIMARY_RHS,
        "estimator": "weighted least squares linear probability model",
        "weight": "w_equal = official wgt normalized within economy-wave",
        "cluster": "economy",
        "inference": "wild-cluster Rademacher score-bootstrap, 999 replications",
        "causal_claims": False,
        "results": rows,
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    (OUT / "result_checksum.txt").write_text(
        "excl_chn_sau_estimates.csv  " + sha256(OUT / "excl_chn_sau_estimates.csv") + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
