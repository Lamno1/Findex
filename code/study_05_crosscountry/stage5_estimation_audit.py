import hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(r"D:/EconomicResearch")
P = ROOT / "projects/study_05_findex_crosscountry"
DATA = P / "results/stage4_build/analytical_dataset.csv"
INST = P / "data/raw/wb_credit_information_by_country_year.csv"
OUT = P / "results/stage5_estimation"
OUT.mkdir(parents=True, exist_ok=True)

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

d = pd.read_csv(DATA)
i = pd.read_csv(INST)
i = i[i.year.eq(2019)].copy()
i["coverage"] = i[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
i = i[["iso3", "coverage", "depth_credit_info_0_8", "legal_rights_0_12"]].drop_duplicates("iso3")
assert d.economycode.nunique() == 93
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

base = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
primary_rhs = "digital_payment + dig_x_lowcov + " + base
specb_rhs = "digital_payment + dig_x_lowcov + account_fin + acc_x_lowcov + " + base
pooled_rhs = "digital_payment + dig_x_lowcov + dig_x_wave + dig_x_lowcov_x_wave + " + base

def fit(frame, rhs, label, weight="w_equal"):
    m = smf.wls("formal_borrow ~ " + rhs, data=frame, weights=frame[weight]).fit(
        cov_type="cluster", cov_kwds={"groups": frame.economycode, "use_correction": True}
    )
    rows = []
    for term in ["digital_payment", "dig_x_lowcov", "digital_payment:lowdepth_z", "dig_x_wave", "dig_x_lowcov_x_wave", "account_fin", "acc_x_lowcov"]:
        if term in m.params.index:
            b, se, p = float(m.params[term]), float(m.bse[term]), float(m.pvalues[term])
            rows.append({"specification":label,"term":term,"estimate":b,"se_cluster":se,"p_cluster":p,"ci95_lo":b-1.96*se,"ci95_hi":b+1.96*se,"N":int(m.nobs),"G":int(frame.economycode.nunique()),"weight":weight,"cluster":"economy","estimator":"WLS LPM"})
    return rows

results = []
for wave in (2021, 2024):
    q = d[d.wave.eq(wave)].copy()
    results += fit(q, primary_rhs, f"PRIMARY_M1_M2_{wave}")
    results += fit(q, specb_rhs, f"PRIMARY_M1_M2_{wave}_SPECB")
results += fit(d, pooled_rhs, "SECONDARY_POOLED_2021_2024")

for wave in (2021, 2024):
    q = d[d.wave.eq(wave)].copy()
    results += fit(q, "digital_payment + digital_payment:lowdepth_z + " + base, f"SECONDARY_DEPTH_{wave}")

pd.DataFrame(results).to_csv(OUT / "estimates.csv", index=False)

sens = []
for wave in (2021, 2024):
    q = d[d.wave.eq(wave)].copy()
    q["w_unweighted"] = 1.0
    sens += fit(q, primary_rhs, f"ROBUSTNESS_UNWEIGHTED_{wave}", weight="w_unweighted")
pd.DataFrame(sens).to_csv(OUT / "weight_sensitivity.csv", index=False)

pd.DataFrame(columns=["specification","term","estimate","N","G","weight","cluster","estimator","dropped_economy"]).to_csv(OUT / "leave_one_economy_out.csv", index=False)

receipt = {
    "stage": "Stage 5 Estimation & Result Integrity Audit",
    "date": "2026-09-17",
    "dataset": str(DATA),
    "dataset_sha256": sha(DATA),
    "code": str(Path(__file__)),
    "code_sha256": sha(Path(__file__)),
    "rows": int(len(d)),
    "economies": int(d.economycode.nunique()),
    "waves": {str(k): int(v) for k, v in d.wave.value_counts().sort_index().items()},
    "primary": ["PRIMARY_M1_M2_2021", "PRIMARY_M1_M2_2024"],
    "secondary": ["SECONDARY_POOLED_2021_2024", "SECONDARY_DEPTH_2021", "SECONDARY_DEPTH_2024"],
    "sensitivity": ["SPECB account_fin"],
    "robustness": ["unweighted"],
    "robustness_pending": ["leave_one_economy_out"],
    "estimator": "weighted least squares linear probability model",
    "weight": "w_equal = official wgt normalized within economy-wave; no pooled weight",
    "cluster": "economy",
    "causal_claims": False,
    "mechanism_claims": False,
    "diD_or_iv": False,
    "pooled_interpretation": "descriptive repeated-cross-section gradient; fixed 2019 moderator; not institutional-change effect",
    "outputs": ["estimates.csv", "weight_sensitivity.csv", "leave_one_economy_out.csv"]
}
(OUT / "run_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
(OUT / "result_checksum.txt").write_text("estimates.csv  " + sha(OUT/"estimates.csv") + "\nweight_sensitivity.csv  " + sha(OUT/"weight_sensitivity.csv") + "\nleave_one_economy_out.csv  " + sha(OUT/"leave_one_economy_out.csv") + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
