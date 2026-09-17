"""Extend CLAUDE-S5-DB-INTEGRITY-TWOWAVE-20260918-001 to the macro-control
interaction check (Stage 17, Item 2). Same exclusion (China DB2018, Saudi
Arabia DB2020), applied to the digital_payment x lgdppc_z / x acc_rate_z
specification, with lgdppc_z and acc_rate_z re-standardized over the
remaining 91 economies.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(r"D:/EconomicResearch")
P = ROOT / "projects/study_05_findex_crosscountry"
PANEL = P / "results/stage4_build/analytical_dataset.csv"
INST = P / "data/raw/wb_credit_information_by_country_year.csv"
GDP = P / "data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json"
STAGE17 = P / "results/stage17_external_validity/macro_control_estimates.csv"
STAGE5 = P / "results/stage5_estimation/estimates.csv"
OUT = P / "results/stage21_db_integrity_two_wave"
DROP_ISO3 = {"CHN", "SAU"}


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


d = pd.read_csv(PANEL)
assert d.economycode.nunique() == 93
d = d.loc[~d.economycode.isin(DROP_ISO3)].copy()
assert d.economycode.nunique() == 91

i = pd.read_csv(INST)
i = i[i.year.eq(2019)].copy()
i["coverage"] = i[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1, skipna=True)
i = i[["iso3", "coverage"]].drop_duplicates("iso3")
d = d.merge(i, left_on="economycode", right_on="iso3", how="left", validate="many_to_one")
assert d.coverage.notna().all()

cov_mean = d.groupby("economycode").coverage.first().mean()
cov_sd = d.groupby("economycode").coverage.first().std(ddof=0)
d["lowcov_z"] = -(d.coverage - cov_mean) / cov_sd
d["age_c"] = d.age - d.age.mean()
d["age_c2"] = d.age_c ** 2
d["w_equal"] = d.wgt / d.groupby(["economycode", "wave"]).wgt.transform("sum")
d["dig_x_lowcov"] = d.digital_payment * d.lowcov_z

gd = latest_wdi(GDP)
economies_91 = sorted(d.economycode.unique())
lgdppc = pd.DataFrame({
    "iso3": economies_91,
    "lgdppc": [np.log(gd[e]["value"]) if e in gd and gd[e]["value"] > 0 else np.nan for e in economies_91],
})
assert lgdppc.lgdppc.notna().all(), lgdppc[lgdppc.lgdppc.isna()]
lgdppc["lgdppc_z"] = (lgdppc.lgdppc - lgdppc.lgdppc.mean()) / lgdppc.lgdppc.std(ddof=0)

acc_rate = (
    d.groupby(["economycode", "wave"])
    .apply(lambda g: np.average(g.account_fin, weights=g.wgt), include_groups=False)
    .rename("acc_rate")
    .reset_index()
)

BASE_RHS = "female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
primary_est = pd.read_csv(STAGE5)


def primary_value(wave: int) -> float:
    row = primary_est[(primary_est.specification == f"PRIMARY_M1_M2_{wave}") & (primary_est.term == "dig_x_lowcov")]
    return float(row.estimate.iloc[0])


baseline = pd.read_csv(STAGE17)

rows = []
for wave in (2021, 2024):
    q = d[d.wave.eq(wave)].copy()
    q = q.merge(lgdppc[["iso3", "lgdppc_z"]], left_on="economycode", right_on="iso3", how="inner")
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
    base_93 = primary_value(wave)
    for term in ["dig_x_lowcov", "dig_x_lgdppc", "dig_x_accrate"]:
        b, se, p = float(fit.params[term]), float(fit.bse[term]), float(fit.pvalues[term])
        base_row = baseline[(baseline.wave == wave) & (baseline.term == term)]
        base_93_term = float(base_row.estimate.iloc[0])
        rows.append({
            "wave": wave, "term": term, "estimate_91economies": b, "se_cluster": se, "p_cluster": p,
            "ci95_lo": b - 1.96 * se, "ci95_hi": b + 1.96 * se,
            "N": int(fit.nobs), "G": int(q.economycode.nunique()),
            "estimate_93economies": base_93_term,
            "relative_change_vs_93economies": abs(b - base_93_term) / abs(base_93_term),
            "same_sign_vs_93economies": bool(np.sign(b) == np.sign(base_93_term)),
        })
    new_lowcov = float(fit.params["dig_x_lowcov"])
    rows.append({
        "wave": wave, "term": "dig_x_lowcov_vs_PRIMARY_93econ", "estimate_91economies": new_lowcov,
        "se_cluster": None, "p_cluster": None, "ci95_lo": None, "ci95_hi": None, "N": None, "G": None,
        "estimate_93economies": base_93,
        "relative_change_vs_93economies": abs(new_lowcov - base_93) / abs(base_93),
        "same_sign_vs_93economies": bool(np.sign(new_lowcov) == np.sign(base_93)),
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "macro_excl_chn_sau.csv", index=False)
print(df.to_string(index=False))
