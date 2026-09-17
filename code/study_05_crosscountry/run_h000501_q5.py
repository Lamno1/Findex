"""Complete frozen Q5 for an existing EXP-S5-002 Q1-Q4 run."""
from __future__ import annotations
import hashlib,json,platform,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np,pandas as pd,patsy,statsmodels.api as sm
from scipy.optimize import least_squares
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
from estimate_stage2_codex import fit_lpm,bh_adjust,M2,sha256
from stage0_h000501_codex import latest_wdi
ROOT=Path(__file__).resolve().parents[4]; P=ROOT/"projects/study_05_findex_crosscountry"
RUN_ID="CODEX-S5-EXP-S5-002-20260913-001"; OUT=P/"results/stage2"/RUN_ID
PANEL=P/"results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"; MICRO=ROOT/"data/raw/data_micro_findex_2024_vietnam.xlsx"
SNAP=P/"data/raw/wb_credit_information_latest_snapshot.csv"; GDP=P/"data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json"; CREDIT=P/"data/raw/wdi_FS.AST.PRVT.GD.ZS_2000_2023.json"
FROZEN={P/"research_council/hypotheses/H-000501.json":"05387df89c5cbc4cfcbda0d2bdbdcf32ac1e54181a4f7285a277257c75c31320",P/"papers/study_05/PREREGISTRATION_H000501.md":"0ff371662e673bd087218c1433f42c20d5040e291d1c35a951079d9e94d55b8f",P/"papers/study_05/VARIABLE_CONTRACT_H000501.md":"b9ea92ee3b7437f1494d935ad5bd79b43d8592c776722f06a9891505e1d4e5ce"}
TARGET="anydigpayment:lowcov2019_z"
def fail(s): raise RuntimeError("FAIL_CLOSED: "+s)
def pick(r):
 z=r["coefficients"][TARGET]; return {"estimate":z["estimate"],"se":z["se_cluster"],"p":z["p_cluster"],"ci95":z["ci95"],"N":r["N"],"G":r["G"]}
def frame(included):
 micro=pd.read_excel(MICRO,sheet_name="findex_microdata_2025_labelled_",usecols=["economy","economycode","regionwb","pop_adult"])
 f=micro.groupby("economycode",observed=True).agg(economy=("economy","first"),region=("regionwb","first"),pop_adult=("pop_adult","first")).reset_index().rename(columns={"economycode":"iso3"}); f["included"]=f.iso3.isin(included).astype(int)
 s=pd.read_csv(SNAP); f=f.merge(s[["iso3","credit_bureau_cov_pct","credit_registry_cov_pct"]],on="iso3",how="left"); f["any_cov_2019"]=f[["credit_bureau_cov_pct","credit_registry_cov_pct"]].max(axis=1,skipna=True)
 gd,cr=latest_wdi(GDP),latest_wdi(CREDIT); f["lgdppc"]=f.iso3.map(lambda x:np.log(gd[x]["value"]) if x in gd and gd[x]["value"]>0 else np.nan); f["privcredit_gdp"]=f.iso3.map(lambda x:cr.get(x,{}).get("value"))
 all3=f[["any_cov_2019","lgdppc","privcredit_gdp"]].isna().all(axis=1); dropped=f.loc[all3,"iso3"].tolist(); f=f.loc[~all3].copy()
 for c,n in [("any_cov_2019","any_cov_2019_missing"),("lgdppc","lgdppc_missing"),("privcredit_gdp","privcredit_missing")]:
  f[n]=f[c].isna().astype(int); f[c]=f[c].fillna(0 if c=="any_cov_2019" else f[c].median())
 f["log_pop_adult"]=np.log(f.pop_adult); return f,dropped
def design(f):
 ref="Sub-Saharan Africa (excluding high income)"; rhs=f"any_cov_2019 + lgdppc + privcredit_gdp + C(region, Treatment(reference={ref!r})) + log_pop_adult"
 y,x=patsy.dmatrices("included ~ "+rhs,f,return_type="dataframe"); return y.iloc[:,0],x,rhs
def smds(f,w=None):
 z=pd.get_dummies(f[["any_cov_2019","lgdppc","privcredit_gdp","region","pop_adult"]],columns=["region"],dtype=float); out={}
 for c in z:
  a=f.included.eq(1).to_numpy(); x=z[c].to_numpy(float); wa=np.ones(a.sum()) if w is None else np.asarray(w)[a]; wb=np.ones((~a).sum())
  ma=np.average(x[a],weights=wa); mb=np.average(x[~a],weights=wb); va=np.average((x[a]-ma)**2,weights=wa); vb=np.average((x[~a]-mb)**2,weights=wb); out[c]=float((ma-mb)/np.sqrt((va+vb)/2)) if va+vb else 0.0
 return out
def interaction(d,eco_w,label):
 q=d.copy(); q[label]=q.iso3.map(eco_w); q=q[q[label].notna()].copy(); q[label]=q.w_equal*q[label]; r,_=fit_lpm(q,"formal_borrow",M2,label,(TARGET,)); return pick(r)
def main():
 t=time.time(); partial=OUT/"partial_q1_q4.json"; final=OUT/"result.json"
 if not partial.exists() or final.exists(): fail("partial missing or final collision")
 for p,h in FROZEN.items():
  if sha256(p)!=h: fail(f"frozen hash mismatch {p}")
 prior=json.loads(partial.read_text(encoding="utf-8")); d=pd.read_csv(PANEL); f,dropped=frame(set(d.iso3.unique()))
 if len(f)!=139 or f.included.sum()!=97 or dropped!=["TWN"]: fail(f"R4 frame mismatch: {len(f)}, {f.included.sum()}, {dropped}")
 y,x,rhs=design(f); model=sm.GLM(y,x,family=sm.families.Binomial()); fit=model.fit(maxiter=100,tol=1e-8); ph=np.asarray(fit.predict(x)); f["p_hat"]=ph
 auc=float(roc_auc_score(y,ph)); cv=[]; sk=StratifiedKFold(5,shuffle=True,random_state=20260913)
 for tr,te in sk.split(x,y): cv.append(roc_auc_score(y.iloc[te],sm.GLM(y.iloc[tr],x.iloc[tr],family=sm.families.Binomial()).fit(maxiter=100,tol=1e-8).predict(x.iloc[te])))
 inc=f.included.eq(1); lo=max(ph[inc].min(),ph[~inc].min()); hi=min(ph[inc].max(),ph[~inc].max()); outside=int(((ph<lo)|(ph>hi)).sum())
 raw=1/ph[inc]; q01,q99=np.quantile(raw,[.01,.99]); wpri=np.clip(raw,q01,q99); q05,q95=np.quantile(raw,[.05,.95]); w595=np.clip(raw,q05,q95)
 iso=f.loc[inc,"iso3"].to_numpy(); maps=lambda w:dict(zip(iso,np.asarray(w,float)))
 estimates={"primary_trim_1_99":interaction(d,maps(wpri),"w_q5"),"untrimmed":interaction(d,maps(raw),"w_q5"),"trim_5_95":interaction(d,maps(w595),"w_q5"),"inverse_odds":interaction(d,maps((1-ph[inc])/ph[inc]),"w_q5")}
 crmask=inc&(f.p_hat.between(.1,.9)); estimates["crump_0_1_0_9"]=interaction(d,dict(zip(f.loc[crmask,"iso3"],(1/f.loc[crmask,"p_hat"]).to_numpy())),"w_q5") if crmask.sum() else {"status":"FAILED_EMPTY"}
 # Entropy balancing by exponential tilting on standardized numeric + region-share covariates.
 eb=pd.concat([f[["any_cov_2019","lgdppc","privcredit_gdp","log_pop_adult"]],pd.get_dummies(f.region,dtype=float)],axis=1); sd=eb.std(ddof=0).replace(0,1); zs=(eb-eb.mean())/sd; A=zs.loc[inc].to_numpy(); target=zs.mean().to_numpy()
 def fun(lam):
  v=np.clip(A@lam,-50,50); w=np.exp(v); return (w[:,None]*A).sum(0)/w.sum()-target
 sol=least_squares(fun,np.zeros(A.shape[1]),max_nfev=5000,xtol=1e-13,ftol=1e-13,gtol=1e-13); web=np.exp(np.clip(A@sol.x,-50,50)); imb=float(np.max(np.abs(fun(sol.x)))); ess=float(web.sum()**2/(web@web)); ratio=float(web.max()/web.mean())
 ebstatus="ENTROPY_BALANCING_FAILED" if (not sol.success or imb>1e-8) else ("ENTROPY_BALANCING_UNSTABLE" if ratio>10 or ess<48 else "ENTROPY_BALANCING_OK")
 estimates["entropy_balancing"]=interaction(d,maps(web),"w_q5") if ebstatus!="ENTROPY_BALANCING_FAILED" else {"status":ebstatus}
 primary=estimates["primary_trim_1_99"]; base=-0.01975; overlap_ok=outside<=10 and float(wpri.max())<=10
 q5class="not_transportable" if not overlap_ok else ("not_generalisable" if np.sign(primary["estimate"])!=np.sign(base) or abs(primary["estimate"]-base)/abs(base)>.5 else "stable")
 pvals=[prior["family_C_provisional"]["q3_digital_minus_account"]["p"],prior["family_C_provisional"]["q3_account"]["p"],prior["family_C_provisional"]["q4_mean"]["p"],prior["family_C_provisional"]["q4_persistent"]["p"],primary["p"]]; qs=bh_adjust(pvals)
 wall=np.ones(len(f)); wall[inc.to_numpy()]=wpri
 q5={"frame":{"N":len(f),"included":int(inc.sum()),"excluded":int((~inc).sum()),"dropped":dropped},"inclusion_logit":{"rhs":rhs,"coefficients":dict(zip(x.columns,map(float,fit.params))),"c_stat":auc,"cv5_c_stat_mean":float(np.mean(cv)),"cv5_folds":cv},"overlap":{"included_minmax":[float(ph[inc].min()),float(ph[inc].max())],"excluded_minmax":[float(ph[~inc].min()),float(ph[~inc].max())],"common_support":[float(lo),float(hi)],"outside_count":outside,"max_ipw_before":float(raw.max()),"max_ipw_after":float(wpri.max()),"kish_ess_primary":float(wpri.sum()**2/(wpri@wpri))},"smd_before":smds(f),"smd_after_primary":smds(f,wall),"estimates":estimates,"entropy":{"status":ebstatus,"solver":"scipy.optimize.least_squares exponential-tilting dual","scipy":__import__("scipy").__version__,"iterations":int(sol.nfev),"max_standardized_imbalance":imb,"max_over_mean":ratio,"kish_ess":ess},"classification":q5class}
 prior["Q5"]=q5; prior["family_C"]={"order":["Q3 digital-account","Q3 account","Q4 mean","Q4 persistent","Q5 IPW"],"raw_p":pvals,"bh_q":qs,"size":5}; prior["status"]="PARTIAL_ESTIMATED_UNVERIFIED_Q5_COMPLETE"; prior.pop("family_C_provisional",None); prior["completed_utc"]=datetime.now(timezone.utc).isoformat()
 OUT.mkdir(exist_ok=True); final.write_text(json.dumps(prior,indent=2,allow_nan=False),encoding="utf-8")
 fig,ax=plt.subplots(); ax.hist(ph[inc],bins=15,alpha=.55,label="included"); ax.hist(ph[~inc],bins=15,alpha=.55,label="excluded"); ax.axvspan(lo,hi,alpha=.08,color="green"); ax.legend(); ax.set(xlabel="Estimated inclusion probability",ylabel="Economies"); fig.tight_layout(); fig.savefig(OUT/"Q5_common_support.png",dpi=180); plt.close(fig)
 receipt={"run_id":RUN_ID,"status":"PARTIAL_ESTIMATED_UNVERIFIED_Q5_COMPLETE","hypothesis":"H-000501","scope_note":"Q5 is complete. The overall EXP-S5-002 output contract is not yet complete; no full-run completion claim is made.","frozen_hashes":{str(p.relative_to(P)):h for p,h in FROZEN.items()},"result_sha256":sha256(final),"code_sha256":{"q1_q4":sha256(HERE/"run_h000501_exp_s5_002.py"),"q5":sha256(Path(__file__))},"runtime_seconds_q5":time.time()-t,"no_independent_reproduction_claim":True,"environment":{"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"pandas":pd.__version__,"statsmodels":sm.__version__},"created_utc":datetime.now(timezone.utc).isoformat()}; (OUT/"run_receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
 print(json.dumps({"run_id":RUN_ID,"status":receipt["status"],"result":str(final),"receipt":str(OUT/"run_receipt.json"),"q5_classification":q5class},indent=2))
if __name__=="__main__": main()
