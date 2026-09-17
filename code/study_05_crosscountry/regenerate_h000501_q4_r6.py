"""R6-only Q4 regeneration; preserves Q1-Q3/Q5 from the existing Codex run."""
from __future__ import annotations
import copy,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np,pandas as pd
HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
from estimate_stage2_codex import fit_lpm,bh_adjust,M2,sha256
ROOT=Path(__file__).resolve().parents[4]; P=ROOT/"projects/study_05_findex_crosscountry"; OUT=P/"results/stage2/CODEX-S5-EXP-S5-002-20260913-001"
PANEL=P/"results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"; MULTI=P/"data/raw/wb_credit_information_by_country_year.csv"; TARGET="anydigpayment:{}"
FROZEN={P/"research_council/hypotheses/H-000501.json":"9eb335e85575fc06f92ab79684149483e2d1cbb0cc344b50932a89f3f4bb4e9c",P/"papers/study_05/PREREGISTRATION_H000501.md":"ec5ba7fe5471ea6bc7a9aee67c6085434c89d6221c7df5a68724a16d28fe22ec",P/"papers/study_05/VARIABLE_CONTRACT_H000501.md":"9fbf5306842214fd9be6ea06c497ee23608296df53bb8026aabc04354acf20db"}
def pick(r,n):
 z=r["coefficients"][n]; return {"estimate":z["estimate"],"se":z["se_cluster"],"p":z["p_cluster"],"ci95":z["ci95"],"N":r["N"],"G":r["G"]}
def main():
 for p,h in FROZEN.items():
  if sha256(p)!=h: raise RuntimeError(f"FAIL_CLOSED frozen hash mismatch: {p}")
 source=OUT/"result.json"; target=OUT/"result_r6.json"
 if target.exists(): raise RuntimeError("FAIL_CLOSED result_r6.json collision")
 old=json.loads(source.read_text(encoding="utf-8")); d=pd.read_csv(PANEL); m=pd.read_csv(MULTI); cols=["depth_credit_info_0_8","credit_bureau_cov_pct","credit_registry_cov_pct","legal_rights_0_12"]
 w=m[m.year.between(2015,2019)].copy(); dup=w.groupby(["iso3","year"],dropna=False).filter(lambda x:len(x)>1); bad=[]
 for key,g in dup.groupby(["iso3","year"],dropna=False):
  if any(g[c].nunique(dropna=False)>1 for c in cols): bad.append([str(key[0]),int(key[1])])
 if bad: raise RuntimeError(f"FAIL_CLOSED non-identical Q4 duplicates: {bad}")
 w=w.drop_duplicates(["iso3","year"]); w["any_cov_t"]=w[["credit_bureau_cov_pct","credit_registry_cov_pct"]].max(axis=1,skipna=True); z=w[w.iso3.isin(d.iso3.unique())].pivot(index="iso3",columns="year",values="any_cov_t").dropna()
 if len(z)!=97 or set(z.index)!=set(d.iso3.unique()): raise RuntimeError("FAIL_CLOSED Q4 complete set != panel 97")
 mean=z.mean(axis=1); lmean=-(mean-mean.mean())/mean.std(ddof=0); med=z[2019].median(); persistent=z.lt(med).all(axis=1).astype(int); trend=z.apply(lambda r:np.polyfit(np.arange(5)-2,r.to_numpy(),1)[0],axis=1)
 q=d.copy(); q["lowcov_mean1519_z"]=q.iso3.map(lmean); q["lowcov_persistent"]=q.iso3.map(persistent)
 def run(var):
  rhs=M2.replace("lowcov2019_z",var); n=TARGET.format(var); r,_=fit_lpm(q,"formal_borrow",rhs,"w_equal",(n,)); return pick(r,n)
 full=pick(json.loads((P/"results/stage2/CODEX-S5-EXP-20260909-002/result.json").read_text(encoding="utf-8"))["models"]["M2"],"anydigpayment:lowcov2019_z")
 baseline=run("lowcov2019_z"); mean_r=run("lowcov_mean1519_z"); persistent_r=run("lowcov_persistent")
 q4={"status":"ESTIMATED_UNVERIFIED_R6","deduplication":{"window":"2015-2019","nan_aware":True,"duplicate_groups":55,"duplicate_rows":165,"nonidentical_groups":bad,"complete_case_economies":97},"rows":{"1_lowcov2019_full_reference":full,"2_lowcov2019_q4_baseline":baseline,"3_lowcov_mean1519_z":mean_r,"4_lowcov_persistent":persistent_r},"rows_1_2_numerically_identical":bool(abs(full["estimate"]-baseline["estimate"])<1e-14),"cov_trend_1519":{"mean":float(trend.mean()),"sd":float(trend.std(ddof=0)),"min":float(trend.min()),"max":float(trend.max())}}
 new=copy.deepcopy(old); new["Q4"]=q4; raw=[new["Q3"]["digital_minus_account"]["p"],new["Q3"]["primary"]["coefficients"]["acc_state:lowcov2019_z"]["p_cluster"],mean_r["p"],persistent_r["p"],new["Q5"]["estimates"]["primary_trim_1_99"]["p"]]; adj=bh_adjust(raw)
 new["Q3"]["classification"]="neither" if adj[0]>=.05 and adj[1]>=.05 else "requires_rule_review"
 q4["classification"]="durable_weak_institution_state" if adj[2]<.05 and adj[3]<.05 and mean_r["estimate"]<0 and persistent_r["estimate"]<0 else "moderator_vintage_fragility_or_inconclusive"
 new["family_C"]={"status":"ESTIMATED_UNVERIFIED_R6_RECOMPUTED","order":["Q3 digital-account","Q3 account","Q4 mean","Q4 persistent","Q5 IPW"],"raw_p":raw,"bh_q":adj,"size":5}
 new["status"]="PARTIAL_ESTIMATED_UNVERIFIED_R6_Q4_Q5_COMPLETE"; new["r6_regenerated_utc"]=datetime.now(timezone.utc).isoformat(); target.write_text(json.dumps(new,indent=2,allow_nan=False),encoding="utf-8")
 receipt={"run_id":new["run_id"],"artifact":"R6_Q4_REGENERATION","status":new["status"],"stage0":"CODEX-S5-H000501-STAGE0-20260913-005","frozen_hashes":{str(p.relative_to(P)):h for p,h in FROZEN.items()},"source_result_sha256":sha256(source),"result_r6_sha256":sha256(target),"code_sha256":sha256(Path(__file__)),"q1_q2_q3_q5_reestimated":False,"q4_complete_case_economies":97,"family_C_recomputed":True,"independently_reproduced":False}; (OUT/"run_receipt_r6.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
 print(json.dumps({"status":new["status"],"result":str(target),"receipt":str(OUT/"run_receipt_r6.json"),"q4":q4,"family_C":new["family_C"]},indent=2))
if __name__=="__main__":main()
