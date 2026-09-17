"""Execute frozen H-000501 / EXP-S5-002. Descriptive, non-causal."""
from __future__ import annotations

import hashlib, json, platform, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from estimate_stage2_codex import fit_lpm, bh_adjust, M2, sha256  # noqa: E402
from stage0_h000501_codex import latest_wdi  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
P = ROOT / "projects/study_05_findex_crosscountry"
RUN_ID = "CODEX-S5-EXP-S5-002-20260913-001"
OUT = P / "results/stage2" / RUN_ID
PANEL = P / "results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"
MULTI = P / "data/raw/wb_credit_information_by_country_year.csv"
MICRO = ROOT / "data/raw/data_micro_findex_2024_vietnam.xlsx"
SNAP = P / "data/raw/wb_credit_information_latest_snapshot.csv"
GDP = P / "data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json"
CREDIT = P / "data/raw/wdi_FS.AST.PRVT.GD.ZS_2000_2023.json"
FROZEN = {
 P/"research_council/hypotheses/H-000501.json":"05387df89c5cbc4cfcbda0d2bdbdcf32ac1e54181a4f7285a277257c75c31320",
 P/"papers/study_05/PREREGISTRATION_H000501.md":"0ff371662e673bd087218c1433f42c20d5040e291d1c35a951079d9e94d55b8f",
 P/"papers/study_05/VARIABLE_CONTRACT_H000501.md":"b9ea92ee3b7437f1494d935ad5bd79b43d8592c776722f06a9891505e1d4e5ce"}
SEED, B = 20260913, 999

def fail(s): raise RuntimeError("FAIL_CLOSED: "+s)
def term(r,n):
 z=r["coefficients"][n]; return {"estimate":z["estimate"],"se":z["se_cluster"],"p":z["p_cluster"],"ci95":z["ci95"],"N":r["N"],"G":r["G"]}
def tost(est,se,margin,df):
 c=stats.t.ppf(.95,df); ci=[est-c*se,est+c*se]
 return {"margin":margin,"ci90":ci,"equivalent":bool(ci[0]>-margin and ci[1]<margin),
         "p_lower":float(stats.t.sf((est+margin)/se,df)),"p_upper":float(stats.t.cdf((est-margin)/se,df))}
def fit_glm(d,family):
 y,x=patsy.dmatrices("formal_borrow ~ "+M2,d,return_type="dataframe")
 q=d.loc[x.index]; model=sm.GLM(y.iloc[:,0],x,family=family,freq_weights=q.w_equal)
 f=model.fit(maxiter=100,tol=1e-8,cov_type="cluster",cov_kwds={"groups":q.iso3})
 n="anydigpayment:lowcov2019_z"; j=list(x.columns).index(n); b=float(f.params.iloc[j]); se=float(f.bse.iloc[j])
 return {"estimate":b,"se":se,"p":float(2*stats.t.sf(abs(b/se),q.iso3.nunique()-1)),
  "ci95":[float(b-stats.t.ppf(.975,q.iso3.nunique()-1)*se),float(b+stats.t.ppf(.975,q.iso3.nunique()-1)*se)],
  "N":len(q),"G":q.iso3.nunique(),"converged":bool(f.converged),"names":list(x.columns)}

def main():
 started=time.time()
 if OUT.exists(): fail("output path exists")
 for p,h in FROZEN.items():
  if sha256(p)!=h: fail(f"frozen hash mismatch: {p}")
 d=pd.read_csv(PANEL)
 pre={"N":len(d),"G":d.iso3.nunique(),"frozen_hashes":{str(p.relative_to(P)):h for p,h in FROZEN.items()}}
 # Q1
 logit=fit_glm(d,sm.families.Binomial())
 pois=fit_glm(d,sm.families.Poisson())
 pbar=float(np.average(d.formal_borrow,weights=d.w_equal)); dlo=.01/(pbar*(1-pbar)); dlr=.01/pbar
 def verdict(z,m):
  if not z["converged"]: return "FAIL"
  if z["ci95"][1]<0:return "NEG"
  if z["ci95"][0]>0:return "POS"
  return "EQUIV" if tost(z["estimate"],z["se"],m,z["G"]-1)["equivalent"] else "WIDE"
 v2,v3=verdict(logit,dlo),verdict(pois,dlr)
 if "FAIL" in (v2,v3): q1class="multiplicative_scale_inconclusive_estimator"
 elif v2==v3=="NEG": q1class="multiplicative_reinforcement"
 elif v2 in ("POS","EQUIV") and v3 in ("POS","EQUIV"): q1class="additive_scale_artifact"
 elif (v2=="NEG" and v3 in ("POS","EQUIV")) or (v3=="NEG" and v2 in ("POS","EQUIV")) or (v2=="POS" and v3=="WIDE") or (v3=="POS" and v2=="WIDE"): q1class="scale_discordance"
 else:q1class="multiplicative_scale_underpowered"
 # Q2
 common=d[d.informal_borrow.notna()].copy(); common["any_borrow"]=((common.formal_borrow==1)|(common.informal_borrow==1)).astype(int)
 fc,_=fit_lpm(common,"formal_borrow",M2,"w_equal",("anydigpayment:lowcov2019_z",)); ab,_=fit_lpm(common,"any_borrow",M2,"w_equal",("anydigpayment:lowcov2019_z",))
 fct,abt=term(fc,"anydigpayment:lowcov2019_z"),term(ab,"anydigpayment:lowcov2019_z"); atost=tost(abt["estimate"]*100,abt["se"]*100,1.0,96)
 if abt["ci95"][1]<0:q2="total_borrowing_suppression"
 elif abt["ci95"][0]>0:q2="total_borrowing_amplification"
 elif fct["estimate"]<0 and fct["p"]<.05 and atost["equivalent"]:q2="reallocation_consistent"
 elif fct["estimate"]<0 and fct["p"]<.05 and abt["p"]>=.05:q2="offsetting_but_unresolved"
 else:q2="mixed_inconclusive"
 # Q3
 acc=d.account_fin.eq(1); dig=d.anydigpayment.eq(1)
 d["exp_state"]=np.select([~acc&~dig,acc&~dig,acc&dig,~acc&dig],["unbanked","account_only","digitally_active","digitally_active_no_fi"],default="invalid")
 cells=d.groupby("exp_state").agg(raw_n=("iso3","size"),economies=("iso3","nunique")).to_dict("index")
 q3=d[d.exp_state.ne("digitally_active_no_fi")].copy(); q3["acc_state"]=(q3.exp_state=="account_only").astype(int); q3["dig_state"]=(q3.exp_state=="digitally_active").astype(int)
 rhs3="acc_state + dig_state + acc_state:lowcov2019_z + dig_state:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"
 r3,raw3=fit_lpm(q3,"formal_borrow",rhs3,"w_equal",("acc_state:lowcov2019_z","dig_state:lowcov2019_z"))
 names=raw3["names"]; ia=names.index("acc_state:lowcov2019_z"); idg=names.index("dig_state:lowcov2019_z"); c=float(raw3["beta"][idg]-raw3["beta"][ia]); cs=float(np.sqrt(raw3["vcov"][idg,idg]+raw3["vcov"][ia,ia]-2*raw3["vcov"][idg,ia])); cp=float(2*stats.t.sf(abs(c/cs),r3["G"]-1))
 # Q4
 m=pd.read_csv(MULTI); m["any_cov_t"]=m[["credit_bureau_cov_pct","credit_registry_cov_pct"]].max(axis=1,skipna=True); z=m[m.year.between(2015,2019)].pivot_table(index="iso3",columns="year",values="any_cov_t",aggfunc="max").dropna(); z=z.loc[z.index.intersection(d.iso3.unique())]; mean=z.mean(axis=1); lmean=-(mean-mean.mean())/mean.std(ddof=0); med=z[2019].median(); pers=(z.lt(med).all(axis=1)).astype(int)
 q4=d[d.iso3.isin(z.index)].copy(); q4["lowcov_mean1519_z"]=q4.iso3.map(lmean); q4["lowcov_persistent"]=q4.iso3.map(pers)
 def modfit(var):
  rhs=M2.replace("lowcov2019_z",var); rr,_=fit_lpm(q4,"formal_borrow",rhs,"w_equal",(f"anydigpayment:{var}",)); return term(rr,f"anydigpayment:{var}")
 q4mean,q4pers=modfit("lowcov_mean1519_z"),modfit("lowcov_persistent")
 # Family C and readings (Q5 appended by the dedicated second phase below).
 provisional={"q3_digital_minus_account":{"estimate":c,"se":cs,"p":cp},"q3_account":term(r3,"acc_state:lowcov2019_z"),"q4_mean":q4mean,"q4_persistent":q4pers}
 out={"run_id":RUN_ID,"status":"RUNNING_Q5_NOT_YET_FINAL","noncausal":True,"pre_outcome":pre,
  "Q1":{"S2_logit":logit,"S3_modified_poisson":pois,"verdicts":[v2,v3],"classification":q1class,"margins":{"delta_logodds":dlo,"delta_logrisk":dlr}},
  "Q2":{"formal_common_frame":fct,"any_borrow":abt,"any_borrow_tost":atost,"classification":q2,"N":len(common)},
  "Q3":{"cells":cells,"primary":r3,"digital_minus_account":provisional["q3_digital_minus_account"]},"Q4":{"G":len(z),"mean":q4mean,"persistent":q4pers},"family_C_provisional":provisional,
  "created_utc":datetime.now(timezone.utc).isoformat(),"runtime_seconds":time.time()-started}
 OUT.mkdir(parents=True); (OUT/"partial_q1_q4.json").write_text(json.dumps(out,indent=2,allow_nan=False),encoding="utf-8")
 print(json.dumps({"run_id":RUN_ID,"phase":"Q1_Q4_COMPLETE_Q5_PENDING","path":str(OUT)},indent=2))
if __name__=="__main__": main()
