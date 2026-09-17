"""Complete structural outputs for frozen H-000501 R6; never edits frozen files."""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np,pandas as pd,patsy,statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression

HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
from estimate_stage2_codex import fit_lpm,M2,sha256
ROOT=Path(__file__).resolve().parents[4]; P=ROOT/"projects/study_05_findex_crosscountry"; RUN=P/"results/stage2/CODEX-S5-EXP-S5-002-20260913-001"
PANEL=P/"results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"; SRC=RUN/"result_r6.json"; OUT=RUN/"result_enriched.json"
FROZEN={P/"research_council/hypotheses/H-000501.json":"9eb335e85575fc06f92ab79684149483e2d1cbb0cc344b50932a89f3f4bb4e9c"}
BASE_CONTROLS="female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d"
def fail(s): raise RuntimeError("FAIL_CLOSED: "+s)
def coef(r,n):
 z=r["coefficients"][n]; return {"estimate":z["estimate"],"se":z["se_cluster"],"p":z["p_cluster"],"ci95":z["ci95"],"N":r["N"],"G":r["G"]}
def main():
 if OUT.exists(): fail("result_enriched collision")
 for p,h in FROZEN.items():
  if sha256(p)!=h: fail(f"frozen hash mismatch: {p}")
 d=pd.read_csv(PANEL); result=json.loads(SRC.read_text(encoding="utf-8"))
 # Sample comparability: S2 dropped no economies in observed fit, so registered exact sample is full panel.
 s1,_=fit_lpm(d,"formal_borrow",M2,"w_equal",("anydigpayment:lowcov2019_z",)); s1c=coef(s1,"anydigpayment:lowcov2019_z")
 result["Q1"]["sample_comparability"]={"S1_full":s1c,"S1_on_S2_sample":s1c,"S2_dropped_economies":[],"economies_lost":0}
 # S4 economy x digital cell fractional logit, weighted rates and summed survey weights.
 cells=[]
 for (iso,dig),g in d.groupby(["iso3","anydigpayment"],observed=True):
  cells.append({"iso3":iso,"digital_cell":int(dig),"L":float(g.lowcov2019_z.iloc[0]),"rate":float(np.average(g.formal_borrow,weights=g.w_equal)),"cell_weight":float(g.wgt.sum())})
 c=pd.DataFrame(cells); y,x=patsy.dmatrices("rate ~ digital_cell * L",c,return_type="dataframe"); sf=sm.GLM(y.iloc[:,0],x,family=sm.families.Binomial(),freq_weights=c.cell_weight).fit(cov_type="cluster",cov_kwds={"groups":c.iso3})
 j=list(x.columns).index("digital_cell:L"); b,se=float(sf.params.iloc[j]),float(sf.bse.iloc[j]); crit=stats.t.ppf(.975,c.iso3.nunique()-1)
 result["Q1"]["S4_fractional_logit"]={"estimate":b,"se":se,"p":float(2*stats.t.sf(abs(b/se),c.iso3.nunique()-1)),"ci95":[b-crit*se,b+crit*se],"N_cells":len(c),"G":c.iso3.nunique(),"status":"descriptive_cross_check_only"}
 # Q3 four-state sensitivity and complete gate metrics.
 acc=d.account_fin.eq(1); dig=d.anydigpayment.eq(1); d["exp_state"]=np.select([~acc&~dig,acc&~dig,acc&dig,~acc&dig],["unbanked","account_only","digitally_active","digitally_active_no_fi"],default="invalid")
 levels=["account_only","digitally_active","digitally_active_no_fi"]
 for lev in levels:d["s_"+lev]=(d.exp_state==lev).astype(int)
 rhs=" + ".join(["s_"+v+" + s_"+v+":lowcov2019_z" for v in levels])+" + "+BASE_CONTROLS+" + C(iso3)"
 q34,_=fit_lpm(d,"formal_borrow",rhs,"w_equal",tuple("s_"+v+":lowcov2019_z" for v in levels))
 w=d.loc[d.exp_state.eq("digitally_active_no_fi"),"w_equal"]; by=d[d.exp_state.eq("digitally_active_no_fi")].groupby("iso3").size()
 result["Q3"]["four_state_sensitivity"]={"model":q34,"gate":{"raw_n":len(w),"kish_n_eff":float(w.sum()**2/(w@w)),"economies_any":int(len(by)),"economies_with_at_least_5":int((by>=5).sum()),"interpretable":bool(w.sum()**2/(w@w)>=300 and (by>=5).sum()>=12)}}
 # Q2 exploratory multinomial, survey-weighted, economy FE; AME goal = descriptive AME by state.
 q=d[d.informal_borrow.notna()].copy(); q["borrow_state_4"]=np.select([(q.formal_borrow==0)&(q.informal_borrow==0),(q.formal_borrow==1)&(q.informal_borrow==0),(q.formal_borrow==0)&(q.informal_borrow==1),(q.formal_borrow==1)&(q.informal_borrow==1)],["none","formal_only","informal_only","both"],default="invalid")
 X=patsy.dmatrix("0 + anydigpayment + anydigpayment:lowcov2019_z + account_fin + account_fin:lowcov2019_z + "+BASE_CONTROLS+" + C(iso3)",q,return_type="dataframe")
 scale=X.std(ddof=0).replace(0,1); Xs=X/scale
 lm=LogisticRegression(solver="lbfgs",penalty=None,max_iter=3000,tol=1e-8,n_jobs=1).fit(Xs,q.borrow_state_4,sample_weight=q.w_equal)
 eps=1e-5; Xp=X.copy(); Xm=X.copy(); Xp["anydigpayment:lowcov2019_z"]+=eps; Xm["anydigpayment:lowcov2019_z"]-=eps
 ame=dict(zip(lm.classes_,((lm.predict_proba(Xp/scale)-lm.predict_proba(Xm/scale))/(2*eps)).mean(axis=0)))
 result["Q2"]["multinomial_exploratory"]={"estimator":"sklearn multinomial unpenalized lbfgs with w_equal; scale-normalized design (likelihood-equivalent); descriptive only","converged":bool(lm.n_iter_.max()<3000),"iterations":int(lm.n_iter_.max()),"max_iterations":3000,"N":len(q),"G":q.iso3.nunique(),"state_counts":q.borrow_state_4.value_counts().to_dict(),"interaction_regressor_ame":{k:float(v) for k,v in ame.items()}}
 result["status"]="ENRICHED_ESTIMATED_UNVERIFIED_BOOTSTRAP_TABLES_FIGURES_PENDING"; OUT.write_text(json.dumps(result,indent=2,allow_nan=False),encoding="utf-8")
 print(json.dumps({"status":result["status"],"output":str(OUT),"S4":result["Q1"]["S4_fractional_logit"],"Q3_gate":result["Q3"]["four_state_sensitivity"]["gate"],"Q2_multinomial_converged":result["Q2"]["multinomial_exploratory"]["converged"]},indent=2))
if __name__=="__main__":main()
