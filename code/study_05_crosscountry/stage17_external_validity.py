"""Stage 17 -- Additional robustness for the 93-economy/2021-2024 line.

ADDITIVE analysis, not remediation. Owner-directed after Stage 16's READY
verdict, targeting journal submission (JFSR / World Development / Financial
Innovation per audit/STAGE_11_JOURNAL_FIT_MATRIX.md). Does not alter, delete,
or re-estimate anything in results/stage5_estimation/ or the manuscript's
existing Results numbers; this is a new subsection layered on top.

Item 1 -- External-validity reweighting.
  Quantifies (not just narrates) the Stage-14 finding that the 93-economy
  common frame excludes ~40 mostly-high-coverage economies. Adapts the
  IPW/entropy-style technique already built for H-000501's Q5 module-
  selection transportability check (see code/study_05_crosscountry/
  run_h000501_q5.py and research_council/hypotheses/H-000501.json
  decision_rules.Q5_selection_transportability) to a DIFFERENT target
  population: the 133 economies present in BOTH raw Findex 2021 and 2024
  releases (not H-000501's 139-economy "released Findex 2024" frame).

Item 2 -- Macro-control interactions.
  The directive as written asked for lowcov_z x lgdppc and lowcov_z x
  acc_rate as new M2 regressors. That is NOT ESTIMABLE: M2 includes
  C(economycode) fixed effects, and lowcov_z, lgdppc and acc_rate are all
  constant within an economy (acc_rate is aggregated within economy-wave,
  and each wave is estimated separately) -- any economy-level-only
  covariate or interaction of two economy-level covariates is perfectly
  collinear with the economy dummies and cannot be estimated alongside
  them. ADAPTED (disclosed here, not silently substituted): interact
  digital_payment (an individual-level variable, so NOT absorbed by FE)
  with lgdppc_z and acc_rate_z instead -- the same construction pattern
  already used for dig_x_lowcov = digital_payment x lowcov_z. This tests
  whether dig_x_lowcov survives once the digital-payment effect is also
  allowed to vary with economy-level development/inclusion, which is the
  substantive question the directive asked ("does the interaction survive
  once the moderator's association with general economic/financial
  development is netted out") in an estimable form.

Sources (all immutable / already-acquired with recorded provenance):
  data/acquisition/FINDEX_2021/raw_microdata.csv, FINDEX_2024/raw_microdata.csv
  data/manifests/findex_2021_2024_primary_93.csv
  data/raw/wb_credit_information_by_country_year.csv   (2019 coverage; same
      file results/stage5_estimation/estimates.csv already uses)
  data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json            (GDP per capita;
      already acquired with provenance for H-000501, WDI indicator
      NY.GDP.PCAP.CD, vintage through 2023 -- reused here unmodified,
      no new acquisition needed)
  results/stage4_build/analytical_dataset.csv           (primary 93-economy
      analysis-ready panel, Stage 4)

Outputs (this run only, does not touch any existing file):
  results/stage17_external_validity/inclusion_logit.json
  results/stage17_external_validity/reweighted_estimates.csv
  results/stage17_external_validity/macro_control_estimates.csv
  results/stage17_external_validity/common_support.png
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

ROOT = Path(r"D:/EconomicResearch")
P = ROOT / "projects/study_05_findex_crosscountry"
ACQ = P / "data/acquisition"
MANIFEST = P / "data/manifests/findex_2021_2024_primary_93.csv"
INST = P / "data/raw/wb_credit_information_by_country_year.csv"
GDP = P / "data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json"
PANEL = P / "results/stage4_build/analytical_dataset.csv"
STAGE5 = P / "results/stage5_estimation/estimates.csv"
OUT = P / "results/stage17_external_validity"
OUT.mkdir(parents=True, exist_ok=True)

B = 999
SEED = 20261701


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def latest_wdi(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload[1]
    result: dict = {}
    for row in rows:
        iso3 = row.get("countryiso3code")
        value = row.get("value")
        year = int(row["date"])
        if not iso3 or value is None or year > 2023:
            continue
        if iso3 not in result or year > int(result[iso3]["year"]):
            result[iso3] = {"value": float(value), "year": year}
    return result


# ---------------------------------------------------------------------------
# Step 1-2: build the 133-economy frame and its economy-level covariates
# ---------------------------------------------------------------------------

def load_raw_economy_cols(wave: int) -> pd.DataFrame:
    return pd.read_csv(
        ACQ / f"FINDEX_{wave}/raw_microdata.csv",
        encoding="cp1252", low_memory=False,
        usecols=["economycode", "economy", "regionwb", "pop_adult"],
    )


d21_raw = load_raw_economy_cols(2021)
d24_raw = load_raw_economy_cols(2024)
e21 = set(d21_raw.economycode.unique())
e24 = set(d24_raw.economycode.unique())
frame_iso = sorted(e21 & e24)

manifest = pd.read_csv(MANIFEST, dtype={"economy_code": str})
primary93 = set(manifest.loc[manifest.final_sample.eq(1), "economy_code"])
assert len(primary93) == 93

econ = (
    d24_raw[d24_raw.economycode.isin(frame_iso)]
    .groupby("economycode", observed=True)
    .agg(economy=("economy", "first"), region=("regionwb", "first"), pop_adult=("pop_adult", "first"))
    .reset_index()
    .rename(columns={"economycode": "iso3"})
)
econ["included"] = econ.iso3.isin(primary93).astype(int)

inst = pd.read_csv(INST)
inst = inst[inst.year.eq(2019)].copy()
inst["coverage"] = inst[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
inst = inst[["iso3", "coverage"]].drop_duplicates("iso3")
econ = econ.merge(inst, on="iso3", how="left")

gd = latest_wdi(GDP)
econ["lgdppc"] = econ.iso3.map(lambda x: np.log(gd[x]["value"]) if x in gd and gd[x]["value"] > 0 else np.nan)

both_missing = econ.coverage.isna() & econ.lgdppc.isna()
dropped_economies = econ.loc[both_missing, "iso3"].tolist()
econ = econ.loc[~both_missing].copy()
partial_missing = econ[econ.coverage.isna() | econ.lgdppc.isna()][["iso3", "coverage", "lgdppc"]].to_dict("records")
assert econ.coverage.notna().all() and econ.lgdppc.notna().all(), (
    f"unexpected partial covariate missingness after full-missing drop: {partial_missing}"
)
econ["log_pop_adult"] = np.log(econ.pop_adult)

FRAME_N = len(econ)
INCLUDED_N = int(econ.included.sum())
EXCLUDED_N = FRAME_N - INCLUDED_N

# ---------------------------------------------------------------------------
# Step 3-5: inclusion logit, propensity, overlap diagnostics
# ---------------------------------------------------------------------------

REF_REGION = "Sub-Saharan Africa (excluding high income)"
RHS = f"coverage + lgdppc + C(region, Treatment(reference={REF_REGION!r})) + log_pop_adult"
y, x = patsy.dmatrices("included ~ " + RHS, econ, return_type="dataframe")
logit = sm.GLM(y, x, family=sm.families.Binomial()).fit(maxiter=100, tol=1e-8)
ph = np.asarray(logit.predict(x))
econ["p_hat"] = ph

auc = float(roc_auc_score(y, ph))
cv_scores = []
skf = StratifiedKFold(5, shuffle=True, random_state=SEED)
for tr, te in skf.split(x, y):
    m = sm.GLM(y.iloc[tr], x.iloc[tr], family=sm.families.Binomial()).fit(maxiter=100, tol=1e-8)
    cv_scores.append(roc_auc_score(y.iloc[te], m.predict(x.iloc[te])))

inc = econ.included.eq(1)
inc_ph, exc_ph = ph[inc.to_numpy()], ph[(~inc).to_numpy()]
lo, hi = max(inc_ph.min(), exc_ph.min()), min(inc_ph.max(), exc_ph.max())
outside_count = int(((ph < lo) | (ph > hi)).sum())

raw_ipw = 1.0 / inc_ph
q01, q99 = np.quantile(raw_ipw, [0.01, 0.99])
ipw_trim = np.clip(raw_ipw, q01, q99)
kish_ess = float(ipw_trim.sum() ** 2 / (ipw_trim @ ipw_trim))
iso_included = econ.loc[inc, "iso3"].to_numpy()
ipw_map = dict(zip(iso_included, ipw_trim))

fig, ax = plt.subplots()
ax.hist(inc_ph, bins=15, alpha=0.55, label=f"included (n={INCLUDED_N})")
ax.hist(exc_ph, bins=15, alpha=0.55, label=f"excluded (n={EXCLUDED_N})")
ax.axvspan(lo, hi, alpha=0.08, color="green")
ax.legend()
ax.set(xlabel="Estimated inclusion probability", ylabel="Economies",
       title="Stage 17: 93-of-133 inclusion propensity")
fig.tight_layout()
fig.savefig(OUT / "common_support.png", dpi=180)
plt.close(fig)

inclusion_logit_report = {
    "frame_133_n": FRAME_N,
    "included_n": INCLUDED_N,
    "excluded_n": EXCLUDED_N,
    "dropped_missing_all_covariates": dropped_economies,
    "rhs": RHS,
    "coefficients": {k: float(v) for k, v in zip(x.columns, logit.params)},
    "c_stat": auc,
    "cv5_c_stat_mean": float(np.mean(cv_scores)),
    "cv5_folds": [float(v) for v in cv_scores],
    "overlap": {
        "included_minmax": [float(inc_ph.min()), float(inc_ph.max())],
        "excluded_minmax": [float(exc_ph.min()), float(exc_ph.max())],
        "common_support": [float(lo), float(hi)],
        "outside_count": outside_count,
        "max_ipw_before_trim": float(raw_ipw.max()),
        "max_ipw_after_trim": float(ipw_trim.max()),
        "kish_ess": kish_ess,
    },
}

# ---------------------------------------------------------------------------
# Item 1: reweighted M2 interaction, 2021 and 2024
# ---------------------------------------------------------------------------

BASE_RHS = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
M2_RHS = "digital_payment + dig_x_lowcov + " + BASE_RHS


def prepare_panel() -> pd.DataFrame:
    d = pd.read_csv(PANEL)
    i = pd.read_csv(INST)
    i = i[i.year.eq(2019)].copy()
    i["coverage"] = i[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
    i = i[["iso3", "coverage"]].drop_duplicates("iso3")
    d = d.merge(i, left_on="economycode", right_on="iso3", how="left", validate="many_to_one")
    assert d.coverage.notna().all()
    d["lowcov_z"] = -(d.coverage - d.coverage.mean()) / d.coverage.std(ddof=0)
    d["age_c"] = d.age - d.age.mean()
    d["age_c2"] = d.age_c ** 2
    d["w_equal"] = d.wgt / d.groupby(["economycode", "wave"]).wgt.transform("sum")
    d["dig_x_lowcov"] = d.digital_payment * d.lowcov_z
    return d


panel = prepare_panel()


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


primary_est = pd.read_csv(STAGE5)


def primary_value(wave: int) -> float:
    row = primary_est[(primary_est.specification == f"PRIMARY_M1_M2_{wave}") & (primary_est.term == "dig_x_lowcov")]
    return float(row.estimate.iloc[0])


reweighted_rows = []
for wave in (2021, 2024):
    q = panel[panel.wave.eq(wave)].copy()
    q["ipw"] = q.economycode.map(ipw_map)
    q = q[q.ipw.notna()].copy()
    q["w_ipw"] = q.w_equal * q.ipw
    res = wild_cluster_p(q, M2_RHS, "dig_x_lowcov", "w_ipw", SEED + wave)
    base = primary_value(wave)
    rel_change = abs(res["estimate"] - base) / abs(base)
    reweighted_rows.append({
        "wave": wave, "primary_estimate": base, "reweighted_estimate": res["estimate"],
        "se_cluster": res["se_cluster"], "ci95_lo": res["ci95_lo"], "ci95_hi": res["ci95_hi"],
        "p_cluster": res["p_cluster"], "wild_p_rademacher": res["wild_p_rademacher"],
        "N": res["N"], "G": res["G"], "relative_change_vs_primary": rel_change,
        "same_sign": (np.sign(res["estimate"]) == np.sign(base)),
    })

reweighted_df = pd.DataFrame(reweighted_rows)
reweighted_df.to_csv(OUT / "reweighted_estimates.csv", index=False)

overlap_ok = outside_count <= 10 and ipw_trim.max() <= 10.0
if not overlap_ok:
    q5_classification = "not_transportable"
else:
    sign_ok = reweighted_df.same_sign.all()
    magnitude_ok = (reweighted_df.relative_change_vs_primary <= 0.5).all()
    q5_classification = "stable" if (sign_ok and magnitude_ok) else "not_generalisable"

inclusion_logit_report["item1_classification"] = q5_classification
inclusion_logit_report["item1_classification_basis"] = {
    "overlap_ok": bool(overlap_ok),
    "outside_count_le_10": outside_count <= 10,
    "max_ipw_after_trim_le_10": bool(ipw_trim.max() <= 10.0),
    "all_same_sign": bool(reweighted_df.same_sign.all()),
    "all_relative_change_le_50pct": bool((reweighted_df.relative_change_vs_primary <= 0.5).all()),
}
(OUT / "inclusion_logit.json").write_text(json.dumps(inclusion_logit_report, indent=2), encoding="utf-8")

# ---------------------------------------------------------------------------
# Item 2: macro-control interactions (adapted to digital_payment x macro,
# not lowcov_z x macro -- see module docstring for why)
# ---------------------------------------------------------------------------

econ_included = econ.loc[inc, ["iso3", "lgdppc"]].copy()
econ_included["lgdppc_z"] = (econ_included.lgdppc - econ_included.lgdppc.mean()) / econ_included.lgdppc.std(ddof=0)

acc_rate = (
    panel.groupby(["economycode", "wave"])
    .apply(lambda g: np.average(g.account_fin, weights=g.wgt), include_groups=False)
    .rename("acc_rate")
    .reset_index()
)

macro_rows = []
for wave in (2021, 2024):
    q = panel[panel.wave.eq(wave)].copy()
    q = q.merge(econ_included[["iso3", "lgdppc_z"]], left_on="economycode", right_on="iso3", how="inner")
    wave_acc = acc_rate[acc_rate.wave.eq(wave)][["economycode", "acc_rate"]]
    wave_acc = wave_acc.assign(
        acc_rate_z=(wave_acc.acc_rate - wave_acc.acc_rate.mean()) / wave_acc.acc_rate.std(ddof=0)
    )
    q = q.merge(wave_acc[["economycode", "acc_rate_z"]], on="economycode", how="inner")
    q["dig_x_lgdppc"] = q.digital_payment * q.lgdppc_z
    q["dig_x_accrate"] = q.digital_payment * q.acc_rate_z

    rhs = "digital_payment + dig_x_lowcov + dig_x_lgdppc + dig_x_accrate + " + BASE_RHS
    fit = smf.wls("formal_borrow ~ " + rhs, data=q, weights=q.w_equal).fit(
        cov_type="cluster", cov_kwds={"groups": q.economycode, "use_correction": True}
    )
    for term in ["dig_x_lowcov", "dig_x_lgdppc", "dig_x_accrate"]:
        b, se, p = float(fit.params[term]), float(fit.bse[term]), float(fit.pvalues[term])
        macro_rows.append({
            "wave": wave, "term": term, "estimate": b, "se_cluster": se, "p_cluster": p,
            "ci95_lo": b - 1.96 * se, "ci95_hi": b + 1.96 * se,
            "N": int(fit.nobs), "G": int(q.economycode.nunique()),
        })
    base = primary_value(wave)
    new_est = float(fit.params["dig_x_lowcov"])
    macro_rows.append({
        "wave": wave, "term": "dig_x_lowcov_PRIMARY_FOR_COMPARISON", "estimate": base,
        "se_cluster": None, "p_cluster": None, "ci95_lo": None, "ci95_hi": None,
        "N": None, "G": None,
    })
    macro_rows.append({
        "wave": wave, "term": "dig_x_lowcov_RELATIVE_CHANGE", "estimate": abs(new_est - base) / abs(base),
        "se_cluster": None, "p_cluster": None, "ci95_lo": None, "ci95_hi": None,
        "N": None, "G": None,
    })

macro_df = pd.DataFrame(macro_rows)
macro_df.to_csv(OUT / "macro_control_estimates.csv", index=False)

print(json.dumps({
    "frame_133_n": FRAME_N, "included_n": INCLUDED_N, "excluded_n": EXCLUDED_N,
    "dropped": dropped_economies, "c_stat": auc, "item1_classification": q5_classification,
    "reweighted": reweighted_rows,
}, indent=2, default=str))
