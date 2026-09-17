"""Frozen Stage 2 estimation for Study 5 (descriptive, non-causal).

The script refuses output collisions and verifies the immutable Stage 1 panel before use.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import patsy
from scipy import stats


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "projects/study_05_findex_crosscountry"
BUILD = PROJECT / "results/stage1/CODEX-S5-BUILD-20260909-001"
RUN_ID = "CODEX-S5-EXP-20260909-002"
OUT = PROJECT / "results/stage2" / RUN_ID
SEED = 20260909
B = 999
PANEL_HASH = "ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str) -> None:
    raise RuntimeError("FAIL_CLOSED: " + msg)


def design(df: pd.DataFrame, outcome: str, rhs: str):
    y, x = patsy.dmatrices(f"{outcome} ~ {rhs}", df, return_type="dataframe", NA_action="drop")
    return y.iloc[:, 0].to_numpy(float), x.to_numpy(float), list(x.columns), x.index


def fit_lpm(df: pd.DataFrame, outcome: str, rhs: str, weight: str = "w_equal", targets=()):
    y, x, names, idx = design(df, outcome, rhs)
    sub = df.loc[idx]
    w = sub[weight].to_numpy(float)
    groups = sub["iso3"].astype("category").cat.codes.to_numpy()
    sw = np.sqrt(w)
    xw, yw = x * sw[:, None], y * sw
    xtx = xw.T @ xw
    bread = np.linalg.pinv(xtx, rcond=1e-11)
    beta = bread @ (xw.T @ yw)
    resid = y - x @ beta
    unique = np.unique(groups)
    score = np.vstack([(x[groups == g] * w[groups == g, None]).T @ resid[groups == g] for g in unique])
    correction = (len(unique) / (len(unique) - 1)) * ((len(y) - 1) / max(1, len(y) - x.shape[1]))
    vcov = correction * bread @ (score.T @ score) @ bread
    se = np.sqrt(np.maximum(np.diag(vcov), 0))
    tval = beta / se
    p = 2 * stats.t.sf(np.abs(tval), df=len(unique) - 1)
    crit = stats.t.ppf(0.975, df=len(unique) - 1)
    ci_lo, ci_hi = beta - crit * se, beta + crit * se
    # Weighted within R2: residualise y only on economy FE; full SSR uses the fitted model.
    wybar = sub.assign(_y=y, _w=w).groupby("iso3", observed=True).apply(
        lambda z: np.average(z["_y"], weights=z["_w"]), include_groups=False
    )
    demeaned = y - sub["iso3"].map(wybar).to_numpy(float)
    tss = float(np.sum(w * demeaned**2))
    ssr = float(np.sum(w * resid**2))
    within_r2 = 1.0 - ssr / tss
    result = {
        "outcome": outcome, "rhs": rhs, "weight": weight, "N": len(y), "G": len(unique),
        "K": x.shape[1], "within_r2": within_r2, "cluster_df": len(unique) - 1,
        "coefficients": {n: {"estimate": float(beta[i]), "se_cluster": float(se[i]), "t": float(tval[i]),
                              "p_cluster": float(p[i]), "ci95": [float(ci_lo[i]), float(ci_hi[i])]}
                         for i, n in enumerate(names)},
    }
    # Fast score wild-cluster bootstrap, null-imposed at the cluster influence level.
    rng = np.random.default_rng(SEED)
    for target in targets:
        if target not in names:
            fail(f"target {target} not found in {names}")
        j = names.index(target)
        influence = score @ bread[j, :]
        denom = math.sqrt(float(np.sum(influence**2)))
        draws = rng.choice([-1.0, 1.0], size=(B, len(unique))) @ influence / denom
        obs = beta[j] / max(se[j], 1e-30)
        result["coefficients"][target]["p_wild_score_rademacher_999"] = float((1 + np.sum(np.abs(draws) >= abs(obs))) / (B + 1))
        result["coefficients"][target]["wild_method"] = "null-imposed cluster-score Rademacher; seed 20260909"
    return result, {"beta": beta, "vcov": vcov, "names": names, "idx": idx, "resid": resid}


BASE = "anydigpayment + account_fin + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"
M2 = "anydigpayment + anydigpayment:lowcov2019_z + account_fin + account_fin:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"


def pick(res, name):
    z = res["coefficients"][name]
    return {"estimate": z["estimate"], "se": z["se_cluster"], "p_cluster": z["p_cluster"],
            "p_wild": z.get("p_wild_score_rademacher_999"), "ci95": z["ci95"],
            "N": res["N"], "G": res["G"], "within_r2": res["within_r2"]}


def bh_adjust(pvals):
    p = np.asarray(pvals, float); n = len(p); order = np.argsort(p); q = np.empty(n); prev = 1.0
    for rank_index in range(n - 1, -1, -1):
        i = order[rank_index]; rank = rank_index + 1; prev = min(prev, p[i] * n / rank); q[i] = prev
    return q.tolist()


def m2_within_crossproducts(df: pd.DataFrame):
    """Economy-level cross-products after weighted within transformation (M2 slopes)."""
    rhs = "0 + anydigpayment + anydigpayment:lowcov2019_z + account_fin + account_fin:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d"
    xdf = patsy.dmatrix(rhs, df, return_type="dataframe")
    names = list(xdf.columns); target = names.index("anydigpayment:lowcov2019_z")
    x = xdf.to_numpy(float); y = df.formal_borrow.to_numpy(float); w = df.w_equal.to_numpy(float)
    cps = []
    for c in sorted(df.iso3.unique()):
        mask = df.iso3.eq(c).to_numpy(); wc=w[mask]; xc=x[mask]; yc=y[mask]
        xc=xc-np.average(xc,axis=0,weights=wc); yc=yc-np.average(yc,weights=wc)
        cps.append((c,(xc*wc[:,None]).T@xc,(xc*wc[:,None]).T@yc))
    return names,target,cps


def main():
    if OUT.exists(): fail(f"collision: {OUT}")
    panel = BUILD / "analysis_panel.csv"
    if sha256(panel) != PANEL_HASH: fail("Stage 1 panel hash mismatch")
    freeze = json.loads((PROJECT / "audit/CODEX_S5_REVISION2_FREEZE.json").read_text(encoding="utf-8"))
    for rel, expected in freeze["frozen_sha256"].items():
        if sha256(PROJECT / rel) != expected: fail(f"frozen contract changed: {rel}")
    d = pd.read_csv(panel)
    if len(d) != 100560 or d.iso3.nunique() != 97: fail("panel dimensions changed")
    OUT.mkdir(parents=True, exist_ok=False); (OUT / "figures").mkdir()
    started = time.time(); models = {}; summaries = {}

    def run(label, data, outcome, rhs, weight="w_equal", targets=()):
        print(label, flush=True); res, aux = fit_lpm(data, outcome, rhs, weight, targets)
        models[label] = res
        return res, aux

    m1, a1 = run("M1", d, "formal_borrow", BASE, targets=["anydigpayment"])
    m2, a2 = run("M2", d, "formal_borrow", M2, targets=["anydigpayment:lowcov2019_z"])
    m2b_rhs = M2.replace("lowcov2019_z", "lowcov2019_bmedian")
    m2b, _ = run("M2b", d, "formal_borrow", m2b_rhs, targets=["anydigpayment:lowcov2019_bmedian"])
    m2c_rhs = "anydigpayment + anydigpayment:lowbureau2019_z + anydigpayment:lowregistry2019_z + account_fin + account_fin:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"
    m2c, a2c = run("M2c", d, "formal_borrow", m2c_rhs, targets=["anydigpayment:lowbureau2019_z", "anydigpayment:lowregistry2019_z"])
    joint_names = ["anydigpayment:lowbureau2019_z", "anydigpayment:lowregistry2019_z"]
    jj = [a2c["names"].index(x) for x in joint_names]; b = a2c["beta"][jj]; v = a2c["vcov"][np.ix_(jj, jj)]
    wald = float(b @ np.linalg.pinv(v) @ b); m2c["joint_interactions"] = {"F": wald / 2, "df_num": 2, "df_den": m2c["G"]-1, "p_cluster": float(stats.f.sf(wald/2, 2, m2c["G"]-1)), "wild_note": "individual wild p-values reported; joint score bootstrap not separately implemented"}

    m3 = d.dropna(subset=["receive_dig", "make_dig"])
    m3a_rhs = "receive_dig + make_dig + account_fin + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"
    m3b_rhs = "receive_dig + make_dig + receive_dig:lowcov2019_z + make_dig:lowcov2019_z + account_fin + account_fin:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"
    m3a, _ = run("M3a", m3, "formal_borrow", m3a_rhs, targets=["receive_dig", "make_dig"])
    m3b, _ = run("M3b", m3, "formal_borrow", m3b_rhs, targets=["receive_dig:lowcov2019_z", "make_dig:lowcov2019_z"])

    secondary = []
    for outcome in ["mobile_loan_app", "emergency_loan_source", "informal_borrow"]:
        z = d.dropna(subset=[outcome])
        r, _ = run("M4_" + outcome, z, outcome, M2, targets=["anydigpayment", "anydigpayment:lowcov2019_z"])
        secondary.extend([pick(r, "anydigpayment"), pick(r, "anydigpayment:lowcov2019_z")])

    m5_specs = {
        "inc_q": M2 + " + anydigpayment:lowcov2019_z:inc_q",
        "female_d": M2 + " + anydigpayment:lowcov2019_z:female_d",
        "educ": M2 + " + anydigpayment:lowcov2019_z:educ",
        "region": M2 + " + anydigpayment:lowcov2019_z:C(region)",
    }
    m5_p = []
    for key, rhs in m5_specs.items():
        target = f"anydigpayment:lowcov2019_z:{key}" if key != "region" else None
        r, aux = run("M5_" + key, d, "formal_borrow", rhs, targets=[target] if target else [])
        if target:
            m5_p.append(r["coefficients"][target]["p_cluster"])
        else:
            names = [n for n in aux["names"] if "anydigpayment:lowcov2019_z:C(region)" in n]
            jj = [aux["names"].index(n) for n in names]; bv=aux["beta"][jj]; vv=aux["vcov"][np.ix_(jj,jj)]
            stat=float(bv@np.linalg.pinv(vv)@bv); p=float(stats.f.sf(stat/len(jj),len(jj),r["G"]-1)); r["joint_region"]={"F":stat/len(jj),"df_num":len(jj),"df_den":r["G"]-1,"p_cluster":p}; m5_p.append(p)

    robustness = {}
    for label, weight in [("M6_1_unweighted", "w_unweighted"), ("M6_1_population", "w_population")]:
        r,_=run(label,d,"formal_borrow",M2,weight,targets=["anydigpayment:lowcov2019_z"]); robustness[label]=pick(r,"anydigpayment:lowcov2019_z")
    high = set(d.loc[d.region.eq("High income"),"iso3"]); lowinc=d.loc[~d.iso3.isin(high)].copy()
    for c in ["any_cov","bureau_cov","registry_cov","depth_credit_info_0_8","legal_rights_0_12"]:
        vals=lowinc[["iso3",c]].drop_duplicates()[c]; lowinc[c.replace("any_cov","lowcov2019_z").replace("bureau_cov","lowbureau2019_z").replace("registry_cov","lowregistry2019_z").replace("depth_credit_info_0_8","lowdepth2019_z").replace("legal_rights_0_12","lowrights2019_z")]=-(lowinc[c]-vals.mean())/vals.std(ddof=0)
    r,_=run("M6_3_drop_high_income",lowinc,"formal_borrow",M2,targets=["anydigpayment:lowcov2019_z"]); robustness["M6_3_drop_high_income"]=pick(r,"anydigpayment:lowcov2019_z")
    for proxy in ["lowdepth2019_z","lowrights2019_z"]:
        rhs=M2.replace("lowcov2019_z",proxy); r,_=run("M6_4_"+proxy,d,"formal_borrow",rhs,targets=[f"anydigpayment:{proxy}"]); robustness["M6_4_"+proxy]=pick(r,f"anydigpayment:{proxy}")
    macro_rhs=M2+" + lgdppc + privcredit_gdp + acct_own_rate + anydigpayment:lgdppc + anydigpayment:privcredit_gdp + anydigpayment:acct_own_rate"
    r,_=run("M6_5_country_controls",d,"formal_borrow",macro_rhs,targets=["anydigpayment:lowcov2019_z"]); robustness["M6_5_country_controls"]=pick(r,"anydigpayment:lowcov2019_z")
    counts=d.groupby("iso3").size(); d500=d[d.iso3.isin(counts[counts>=500].index)]
    r,_=run("M6_6_n_ge_500",d500,"formal_borrow",M2,targets=["anydigpayment:lowcov2019_z"]); robustness["M6_6_n_ge_500"]=pick(r,"anydigpayment:lowcov2019_z")
    for extra,label in [("internet_use","M6_8_internet"),("inwork_d","M6_10_inwork")]:
        z=d.dropna(subset=[extra]); rhs=M2.replace(" + C(iso3)",f" + {extra} + C(iso3)"); r,_=run(label,z,"formal_borrow",rhs,targets=["anydigpayment:lowcov2019_z"]); robustness[label]=pick(r,"anydigpayment:lowcov2019_z")

    # Economy-block bootstrap of M2 b3 using exact within-FE cluster cross-products.
    rng=np.random.default_rng(SEED); iso=sorted(d.iso3.unique()); block=[]
    _,target,cps=m2_within_crossproducts(d); xx=np.stack([z[1] for z in cps]); xy=np.stack([z[2] for z in cps])
    for rep in range(B):
        chosen=rng.integers(0,len(cps),size=len(cps)); beta=np.linalg.pinv(xx[chosen].sum(axis=0),rcond=1e-11)@xy[chosen].sum(axis=0); block.append(float(beta[target]))
    robustness["M6_7_economy_block_bootstrap"]={"B":B,"seed":SEED,"estimate":pick(m2,"anydigpayment:lowcov2019_z")["estimate"],"ci95_percentile":np.quantile(block,[.025,.975]).tolist(),"p_sign":float(2*min(np.mean(np.array(block)<=0),np.mean(np.array(block)>=0)))}

    # Leave-one-economy-out.
    loo=[]; xx_all=xx.sum(axis=0); xy_all=xy.sum(axis=0)
    for i,c in enumerate(iso):
        beta=np.linalg.pinv(xx_all-xx[i],rcond=1e-11)@(xy_all-xy[i]); loo.append({"dropped_iso3":c,"b3":float(beta[target])})
    pd.DataFrame(loo).to_csv(OUT/"leave_one_economy_out.csv",index=False)
    robustness["M6_9_leave_one_out"]={"min":float(min(x["b3"] for x in loo)),"max":float(max(x["b3"] for x in loo)),"sign_reversals":sum(np.sign(x["b3"])!=np.sign(pick(m2,"anydigpayment:lowcov2019_z")["estimate"]) for x in loo)}

    # BH family: M4 b1/b3 (6 values, placebo family uses b3 only per frozen list) + M5 four.
    bh_p=[models["M4_mobile_loan_app"]["coefficients"]["anydigpayment"]["p_cluster"],models["M4_mobile_loan_app"]["coefficients"]["anydigpayment:lowcov2019_z"]["p_cluster"],models["M4_emergency_loan_source"]["coefficients"]["anydigpayment"]["p_cluster"],models["M4_emergency_loan_source"]["coefficients"]["anydigpayment:lowcov2019_z"]["p_cluster"],models["M4_informal_borrow"]["coefficients"]["anydigpayment:lowcov2019_z"]["p_cluster"]]+m5_p
    if len(bh_p)!=9: fail("BH family no longer has nine members")
    bh_names=["mobile_b1","mobile_b3","emergency_loan_source_b1","emergency_loan_source_b3","informal_b3","M5_inc_q","M5_female","M5_educ","M5_region_joint"]
    bh=[{"test":n,"p":float(p),"q_bh":float(q),"reject_q05":q<=.05} for n,p,q in zip(bh_names,bh_p,bh_adjust(bh_p))]

    # Descriptives and Vietnam positioning.
    desc={"N":len(d),"G":d.iso3.nunique(),"weighted_means":{c:float(np.average(d[c],weights=d.w_equal)) for c in ["formal_borrow","anydigpayment","account_fin","female_d","urban_d"]}}
    country=d[["iso3","economy","region","any_cov","depth_credit_info_0_8","lowcov2019_z"]].drop_duplicates("iso3")
    v=country[country.iso3.eq("VNM")].iloc[0]
    def pct(series,value): return float(100*np.mean(series<=value))
    vnm={"any_cov":float(v.any_cov),"any_cov_percentile":pct(country.any_cov,v.any_cov),"depth":float(v.depth_credit_info_0_8),"depth_percentile":pct(country.depth_credit_info_0_8,v.depth_credit_info_0_8)}
    for dig in [0,1]:
        q=d[(d.iso3.eq("VNM"))&(d.anydigpayment.eq(dig))]; vnm[f"formal_borrow_rate_dig_{dig}"]=float(np.average(q.formal_borrow,weights=q.w_equal))
    b1=m2["coefficients"]["anydigpayment"]["estimate"]; b3=m2["coefficients"]["anydigpayment:lowcov2019_z"]["estimate"]; vnm["m2_implied_association"]=float(b1+b3*v.lowcov2019_z)

    # Figures.
    loo_df=pd.DataFrame(loo).sort_values("b3"); plt.figure(figsize=(9,4)); plt.plot(range(len(loo_df)),loo_df.b3); plt.axhline(pick(m2,"anydigpayment:lowcov2019_z")["estimate"],color="black",ls="--"); plt.axhline(0,color="grey",lw=.8); plt.ylabel("M2 interaction estimate"); plt.xlabel("Leave-one-economy-out runs (sorted)"); plt.tight_layout(); plt.savefig(OUT/"figures/F2_leave_one_out.png",dpi=180); plt.close()
    gaps=[]
    for c,q in d.groupby("iso3"):
        rates={k:np.average(z.formal_borrow,weights=z.w_equal) for k,z in q.groupby("anydigpayment")}
        if 0 in rates and 1 in rates: gaps.append({"iso3":c,"any_cov":q.any_cov.iloc[0],"gap":rates[1]-rates[0]})
    gaps=pd.DataFrame(gaps); co=np.polyfit(gaps.any_cov,gaps.gap,1); xx=np.linspace(gaps.any_cov.min(),gaps.any_cov.max(),100)
    plt.figure(figsize=(7,5)); plt.scatter(gaps.any_cov,gaps.gap,s=18,alpha=.7); plt.plot(xx,np.polyval(co,xx),color="black"); vv=gaps[gaps.iso3.eq("VNM")]; plt.scatter(vv.any_cov,vv.gap,color="red"); plt.annotate("Vietnam",(vv.any_cov.iloc[0],vv.gap.iloc[0])); plt.xlabel("2019 credit-information coverage (%)"); plt.ylabel("Raw weighted borrowing-rate gap"); plt.tight_layout(); plt.savefig(OUT/"figures/F1_country_gap.png",dpi=180); plt.close()
    grid=np.linspace(country.lowcov2019_z.min(),country.lowcov2019_z.max(),100); assoc=b1+b3*grid; j1=a2["names"].index("anydigpayment"); j3=a2["names"].index("anydigpayment:lowcov2019_z"); vv=a2["vcov"][[j1,j3]][:,[j1,j3]]; se=np.sqrt(vv[0,0]+2*grid*vv[0,1]+grid**2*vv[1,1]);
    plt.figure(figsize=(7,5)); plt.plot(grid,assoc); plt.fill_between(grid,assoc-1.985*se,assoc+1.985*se,alpha=.2); plt.axhline(0,color="grey",lw=.8); plt.axvline(v.lowcov2019_z,color="red",ls="--",label="Vietnam"); plt.xlabel("Lower 2019 coverage (z)"); plt.ylabel("M2 implied digital-payment association"); plt.legend(); plt.tight_layout(); plt.savefig(OUT/"figures/F3_implied_association.png",dpi=180); plt.close()

    primary={"M1_b1":pick(m1,"anydigpayment"),"M2_b3":pick(m2,"anydigpayment:lowcov2019_z"),"M2_b1":pick(m2,"anydigpayment"),"M2b_b3":pick(m2b,"anydigpayment:lowcov2019_bmedian"),"M2c_joint":m2c["joint_interactions"]}
    output={"run_id":RUN_ID,"study_id":"study_05_findex_crosscountry","status":"ESTIMATED_UNVERIFIED","noncausal":True,"primary":primary,"models":models,"robustness":robustness,"bh_family":bh,"descriptives":desc,"vietnam":vnm,"limitations":["single 2024 cross-section","2019 moderator is non-random and slow-moving","private-credit control vintages range 2008-2023","97 economy clusters","results require independent reproduction"],"unimplemented_registered_items":["M6.2 FE logit/probit AMEs","separate joint wild-bootstrap p for M2c","F1 covariate-adjusted rather than raw gap"],"created_utc":datetime.now(timezone.utc).isoformat()}
    (OUT/"result.json").write_text(json.dumps(output,indent=2,ensure_ascii=False,default=lambda x: x.item() if isinstance(x,np.generic) else str(x))+"\n",encoding="utf-8")
    pd.DataFrame([{**{"model":k},**pick(v,"anydigpayment:lowcov2019_z")} for k,v in models.items() if "anydigpayment:lowcov2019_z" in v["coefficients"]]).to_csv(OUT/"interaction_grid.csv",index=False)
    receipt={"run_id":RUN_ID,"status":"ESTIMATED_UNVERIFIED","created_utc":datetime.now(timezone.utc).isoformat(),"seed":SEED,"wild_repetitions":B,"input_panel_sha256":PANEL_HASH,"code_sha256":sha256(Path(__file__)),"runtime_seconds":time.time()-started,"environment":{"python":sys.version,"numpy":np.__version__,"pandas":pd.__version__,"platform":platform.platform()},"outputs_sha256":{}}
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name!="run_receipt.json": receipt["outputs_sha256"][str(p.relative_to(OUT)).replace('\\','/')]=sha256(p)
    (OUT/"run_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(primary,indent=2))


if __name__ == "__main__": main()
