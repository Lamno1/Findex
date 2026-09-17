"""Finalize H-000501 R6 inference, common contrasts, tables, figures and receipt."""
from __future__ import annotations
import hashlib,json,platform,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np,pandas as pd,patsy,statsmodels.api as sm
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
from estimate_stage2_codex import fit_lpm,M2,sha256
from run_h000501_q5 import frame as q5_frame, design as q5_design
ROOT=Path(__file__).resolve().parents[4]; P=ROOT/"projects/study_05_findex_crosscountry"; RUN=P/"results/stage2/CODEX-S5-EXP-S5-002-20260913-001"; PANEL=P/"results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"
SRC=RUN/"result_enriched.json"; FINAL=RUN/"final_result.json"; SEED=20260913; B=999
FROZEN={P/"research_council/hypotheses/H-000501.json":"9eb335e85575fc06f92ab79684149483e2d1cbb0cc344b50932a89f3f4bb4e9c",P/"papers/study_05/PREREGISTRATION_H000501.md":"ec5ba7fe5471ea6bc7a9aee67c6085434c89d6221c7df5a68724a16d28fe22ec",P/"papers/study_05/VARIABLE_CONTRACT_H000501.md":"9fbf5306842214fd9be6ea06c497ee23608296df53bb8026aabc04354acf20db"}
TARGET="anydigpayment:lowcov2019_z"
def fail(s): raise RuntimeError("FAIL_CLOSED: "+s)
def scen(d,L,D):
 q=d.copy(); q["lowcov2019_z"]=L; q["anydigpayment"]=D; return patsy.dmatrix(M2,q,return_type="dataframe")
def glm_bundle(d,family,label,lowL,highL):
 y,x=patsy.dmatrices("formal_borrow ~ "+M2,d,return_type="dataframe"); q=d.loc[x.index]; w=q.w_equal.to_numpy(); groups=q.iso3.astype("category").cat.codes.to_numpy(); model=sm.GLM(y.iloc[:,0],x,family=family,freq_weights=w); fit=model.fit(maxiter=100,tol=1e-8,cov_type="cluster",cov_kwds={"groups":q.iso3}); beta=np.asarray(fit.params); mu=np.asarray(fit.fittedvalues); X=x.to_numpy(); names=list(x.columns); j=names.index(TARGET)
 variance=mu*(1-mu) if label=="logit" else mu; bread=np.linalg.pinv(X.T@((w*variance)[:,None]*X),rcond=1e-11); scores=np.vstack([(X[groups==g]*w[groups==g,None]).T@(y.iloc[:,0].to_numpy()[groups==g]-mu[groups==g]) for g in np.unique(groups)]); infl=scores@bread.T; corr=(len(np.unique(groups))/(len(np.unique(groups))-1))*((len(q)-1)/(len(q)-X.shape[1])); infl*=np.sqrt(corr)
 mats=[scen(q,lowL,1),scen(q,lowL,0),scen(q,highL,1),scen(q,highL,0)]; signs=[1,-1,-1,1]; ww=w/w.sum(); C=0.; grad=np.zeros(len(beta))
 for sgn,xx in zip(signs,mats):
  xx=xx[names].to_numpy(); eta=xx@beta; pp=1/(1+np.exp(-eta)) if label=="logit" else np.exp(eta); der=pp*(1-pp) if label=="logit" else pp; C+=sgn*np.sum(ww*pp); grad+=sgn*np.sum((ww*der)[:,None]*xx,axis=0)
 rng=np.random.default_rng(SEED+(0 if label=="logit" else 1)); eps=rng.choice([-1.,1.],size=(B,infl.shape[0]))@infl; bdraw=beta[j]+eps[:,j]; cdraw=100*(C+eps@grad); obs=beta[j]/fit.bse.iloc[j]; tdraw=eps[:,j]/fit.bse.iloc[j]
 return {"native":{"estimate":float(beta[j]),"se":float(fit.bse.iloc[j]),"ci95":[float(beta[j]-1.984984*fit.bse.iloc[j]),float(beta[j]+1.984984*fit.bse.iloc[j])],"wild_p":float((1+np.sum(np.abs(tdraw)>=abs(obs)))/(B+1)),"B":B,"seed":SEED},"C":{"estimate_pp":float(100*C),"ci95_cluster_score_percentile":np.quantile(cdraw,[.025,.975]).tolist(),"B":B,"method":"Rademacher one-step cluster-score bootstrap by economy"},"beta_anydigpayment":float(beta[names.index("anydigpayment")]),"draws_C":cdraw}
def wls_boot(d,outcome,rhs,target,dz,weight,seed):
 y,x=patsy.dmatrices(outcome+" ~ "+rhs,d,return_type="dataframe"); q=d.loc[x.index]; X=x.to_numpy(); Y=y.iloc[:,0].to_numpy(); w=q[weight].to_numpy(); g=q.iso3.astype("category").cat.codes.to_numpy(); sw=np.sqrt(w); bread=np.linalg.pinv((X*sw[:,None]).T@(X*sw[:,None]),rcond=1e-11); beta=bread@(X.T@(w*Y)); u=Y-X@beta; ids=np.unique(g); score=np.vstack([(X[g==k]*w[g==k,None]).T@u[g==k] for k in ids]); corr=(len(ids)/(len(ids)-1))*((len(Y)-1)/(len(Y)-X.shape[1])); infl=score@bread.T*np.sqrt(corr); j=list(x.columns).index(target); rng=np.random.default_rng(seed); delta=rng.choice([-1.,1.],size=(B,len(ids)))@infl[:,j]; draws=100*dz*(beta[j]+delta); se=np.sqrt(np.sum(infl[:,j]**2)); obs=beta[j]/se; wild=float((1+np.sum(np.abs(delta/se)>=abs(obs)))/(B+1)); return {"estimate_pp":float(100*dz*beta[j]),"ci95_cluster_score_percentile":np.quantile(draws,[.025,.975]).tolist(),"wild_p":wild,"B":B,"seed":seed,"method":"Rademacher one-step cluster-score bootstrap by economy","native_estimate":float(beta[j]),"native_se_cluster_score":float(se)}
def s4_bundle(c,lowL,highL):
 y,x=patsy.dmatrices("rate ~ digital_cell * L",c,return_type="dataframe"); X=x.to_numpy(); Y=y.iloc[:,0].to_numpy(); w=c.cell_weight.to_numpy(); g=c.iso3.astype("category").cat.codes.to_numpy(); fit=sm.GLM(Y,X,family=sm.families.Binomial(),freq_weights=w).fit(); beta=np.asarray(fit.params); mu=np.asarray(fit.fittedvalues); bread=np.linalg.pinv(X.T@((w*mu*(1-mu))[:,None]*X)); score=np.vstack([(X[g==k]*w[g==k,None]).T@(Y[g==k]-mu[g==k]) for k in np.unique(g)]); infl=score@bread.T
 def xx(L,D): return np.column_stack([np.ones(len(c)),np.full(len(c),D),np.full(len(c),L),np.full(len(c),D*L)])
 ww=w/w.sum(); C=0.; grad=np.zeros(4)
 for sgn,Z in zip([1,-1,-1,1],[xx(lowL,1),xx(lowL,0),xx(highL,1),xx(highL,0)]):
  p=1/(1+np.exp(-(Z@beta))); C+=sgn*np.sum(ww*p); grad+=sgn*np.sum((ww*p*(1-p))[:,None]*Z,axis=0)
 eps=np.random.default_rng(SEED+4).choice([-1.,1.],size=(B,len(np.unique(g))))@infl; draws=100*(C+eps@grad); j=list(x.columns).index("digital_cell:L"); nse=float(np.sqrt(np.sum(infl[:,j]**2))); wp=float((1+np.sum(np.abs(eps[:,j]/nse)>=abs(beta[j]/nse)))/(B+1)); return {"estimate_pp":float(100*C),"ci95_cluster_score_percentile":np.quantile(draws,[.025,.975]).tolist(),"B":B,"seed":SEED+4,"method":"Rademacher one-step cluster-score bootstrap by economy","native_wild_p":wp,"native_score_se":nse}
def q4_data(d):
 m=pd.read_csv(P/"data/raw/wb_credit_information_by_country_year.csv"); cols=["depth_credit_info_0_8","credit_bureau_cov_pct","credit_registry_cov_pct","legal_rights_0_12"]
 w=m[m.year.between(2015,2019)].copy(); dup=w.groupby(["iso3","year"],dropna=False).filter(lambda x:len(x)>1)
 bad=[key for key,g in dup.groupby(["iso3","year"],dropna=False) if any(g[c].nunique(dropna=False)>1 for c in cols)]
 if bad: fail(f"non-identical Q4 duplicates: {bad}")
 w=w.drop_duplicates(["iso3","year"]); w["any_cov_t"]=w[["credit_bureau_cov_pct","credit_registry_cov_pct"]].max(axis=1,skipna=True); z=w[w.iso3.isin(d.iso3.unique())].pivot(index="iso3",columns="year",values="any_cov_t").dropna()
 if len(z)!=97: fail("Q4 complete-case set is not 97")
 av=z.mean(axis=1); lmean=-(av-av.mean())/av.std(ddof=0); persistent=z.lt(z[2019].median()).all(axis=1).astype(int); q=d.copy(); q["lowcov_mean1519_z"]=q.iso3.map(lmean); q["lowcov_persistent"]=q.iso3.map(persistent)
 return q,float(lmean.quantile(.75)-lmean.quantile(.25))
def q5_weighted_data(d):
 f,dropped=q5_frame(set(d.iso3.unique())); y,x,_=q5_design(f); fit=sm.GLM(y,x,family=sm.families.Binomial()).fit(maxiter=100,tol=1e-8); ph=np.asarray(fit.predict(x)); inc=f.included.eq(1); raw=1/ph[inc]; lo,hi=np.quantile(raw,[.01,.99]); eco=dict(zip(f.loc[inc,"iso3"],np.clip(raw,lo,hi))); q=d.copy(); q["w_q5_boot"]=q.w_equal*q.iso3.map(eco); return q[q.w_q5_boot.notna()].copy()
def q3_contrast_boot(d,seed):
 rhs="acc_state + dig_state + acc_state:lowcov2019_z + dig_state:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"; y,x=patsy.dmatrices("formal_borrow ~ "+rhs,d,return_type="dataframe"); q=d.loc[x.index]; X=x.to_numpy(); Y=y.iloc[:,0].to_numpy(); w=q.w_equal.to_numpy(); g=q.iso3.astype("category").cat.codes.to_numpy(); bread=np.linalg.pinv(X.T@(w[:,None]*X)); beta=bread@(X.T@(w*Y)); u=Y-X@beta; ids=np.unique(g); score=np.vstack([(X[g==k]*w[g==k,None]).T@u[g==k] for k in ids]); infl=score@bread.T*np.sqrt((len(ids)/(len(ids)-1))*((len(Y)-1)/(len(Y)-X.shape[1]))); names=list(x.columns); signs=np.random.default_rng(seed).choice([-1.,1.],size=(B,len(ids))); out={}
 for label,weights in {"account":{"acc_state:lowcov2019_z":1},"digital":{"dig_state:lowcov2019_z":1},"digital_minus_account":{"dig_state:lowcov2019_z":1,"acc_state:lowcov2019_z":-1}}.items():
  a=np.zeros(len(names))
  for n,v in weights.items(): a[names.index(n)]=v
  delta=signs@(infl@a); est=float(a@beta); se=float(np.sqrt(np.sum((infl@a)**2))); out[label]={"estimate":est,"se":se,"wild_p":float((1+np.sum(np.abs(delta/se)>=abs(est/se)))/(B+1)),"B":B,"seed":seed}
 return out
def main():
 started=time.time()
 if FINAL.exists():fail("final output collision")
 for p,h in FROZEN.items():
  if sha256(p)!=h:fail(f"frozen hash mismatch {p}")
 d=pd.read_csv(PANEL); r=json.loads(SRC.read_text(encoding="utf-8")); ec=d[["iso3","any_cov","lowcov2019_z"]].drop_duplicates(); q25,q75=ec.any_cov.quantile([.25,.75]); mean,sd=ec.any_cov.mean(),ec.any_cov.std(ddof=0); lowL,highL=-(q25-mean)/sd,-(q75-mean)/sd; dz=lowL-highL
 logit=glm_bundle(d,sm.families.Binomial(),"logit",lowL,highL); pois=glm_bundle(d,sm.families.Poisson(),"poisson",lowL,highL)
 s1=r["Q1"]["sample_comparability"]["S1_full"]; s1b=wls_boot(d,"formal_borrow",M2,TARGET,dz,"w_equal",SEED+10)
 c=d.groupby(["iso3","lowcov2019_z","anydigpayment"],as_index=False).apply(lambda z:pd.Series({"rate":np.average(z.formal_borrow,weights=z.w_equal),"cell_weight":z.w_equal.sum()}),include_groups=False).rename(columns={"anydigpayment":"digital_cell","lowcov2019_z":"L"}); s4c=s4_bundle(c,lowL,highL)
 r["Q1"]["common_contrasts"]={"S1":s1b,"S2_logit":logit["C"],"S3_modified_poisson":pois["C"],"S4_fractional_logit":s4c}; r["Q1"]["S2_logit"].update(logit["native"]); r["Q1"]["S3_modified_poisson"].update(pois["native"]); r["Q1"]["S4_fractional_logit"]["C"]=s4c; r["Q1"]["S4_fractional_logit"]["wild_p"]=s4c["native_wild_p"]
 q4,mean_dz=q4_data(d); q4_specs={"1_lowcov2019_full_reference":("lowcov2019_z",dz),"2_lowcov2019_q4_baseline":("lowcov2019_z",dz),"3_lowcov_mean1519_z":("lowcov_mean1519_z",mean_dz),"4_lowcov_persistent":("lowcov_persistent",1.)}
 for i,(key,(var,dd)) in enumerate(q4_specs.items()): r["Q4"]["rows"][key]["C"]=wls_boot(q4,"formal_borrow",M2.replace("lowcov2019_z",var),f"anydigpayment:{var}",dd,"w_equal",SEED+20+i)
 q5d=q5_weighted_data(d); q5=r["Q5"]["estimates"]["primary_trim_1_99"]; q5["C"]=wls_boot(q5d,"formal_borrow",M2,TARGET,dz,"w_q5_boot",SEED+30)
 r["Q2"]["formal_common_frame"]["bootstrap"]=wls_boot(d[d.informal_borrow.notna()],"formal_borrow",M2,TARGET,1.,"w_equal",SEED+40); r["Q2"]["any_borrow"]["bootstrap"]=wls_boot(d[d.informal_borrow.notna()].assign(any_borrow=lambda z:((z.formal_borrow==1)|(z.informal_borrow==1)).astype(int)),"any_borrow",M2,TARGET,1.,"w_equal",SEED+41)
 acc=d.account_fin.eq(1); dig=d.anydigpayment.eq(1); d["exp_state"]=np.select([~acc&~dig,acc&~dig,acc&dig,~acc&dig],["unbanked","account_only","digitally_active","digitally_active_no_fi"],default="invalid"); q3=d[d.exp_state.ne("digitally_active_no_fi")].copy(); q3["acc_state"]=(q3.exp_state=="account_only").astype(int); q3["dig_state"]=(q3.exp_state=="digitally_active").astype(int)
 q3b=q3_contrast_boot(q3,SEED+50); r["Q3"]["digital_minus_account"]["bootstrap"]=q3b["digital_minus_account"]; r["Q3"]["primary"]["coefficients"]["acc_state:lowcov2019_z"]["wild_p"]=q3b["account"]["wild_p"]; r["Q3"]["primary"]["coefficients"]["dig_state:lowcov2019_z"]["wild_p"]=q3b["digital"]["wild_p"]
 # Tables: transparent flat CSV exports from final quantities.
 tabs=RUN/"tables"; figs=RUN/"figures"; tabs.mkdir(exist_ok=True); figs.mkdir(exist_ok=True)
 pd.DataFrame([{"model":"S1 LPM",**s1,"C_pp":s1b["estimate_pp"],"C_ci":s1b["ci95_cluster_score_percentile"],"wild_p":s1b["wild_p"]},{"model":"S2 logit",**r["Q1"]["S2_logit"],"C_pp":logit["C"]["estimate_pp"],"C_ci":logit["C"]["ci95_cluster_score_percentile"]},{"model":"S3 modified Poisson",**r["Q1"]["S3_modified_poisson"],"C_pp":pois["C"]["estimate_pp"],"C_ci":pois["C"]["ci95_cluster_score_percentile"]},{"model":"S4 fractional logit",**r["Q1"]["S4_fractional_logit"],"C_pp":s4c["estimate_pp"],"C_ci":s4c["ci95_cluster_score_percentile"]}]).to_csv(tabs/"T1_q1_scale.csv",index=False)
 known=json.loads((P/"results/stage2/CODEX-S5-EXP-20260909-002/result.json").read_text()); q2rows=[{"outcome":"formal_full","details":json.dumps(known["models"]["M2"])},{"outcome":"formal_common_frame",**r["Q2"]["formal_common_frame"]},{"outcome":"informal_borrow_KNOWN","details":json.dumps(known["models"]["M4_informal_borrow"])},{"outcome":"any_borrow",**r["Q2"]["any_borrow"]},{"outcome":"any_borrow_TOST","details":json.dumps(r["Q2"]["any_borrow_tost"])}]+[{"outcome":"multinomial_"+k,"AME":v} for k,v in r["Q2"]["multinomial_exploratory"]["interaction_regressor_ame"].items()]; pd.DataFrame(q2rows).to_csv(tabs/"T2_q2_channel.csv",index=False)
 q3rows=[{"term":k,**v} for k,v in r["Q3"]["primary"]["coefficients"].items() if "state" in k]+[{"term":"cell_"+k,"details":json.dumps(v)} for k,v in r["Q3"]["cells"].items()]+[{"term":"four_state_gate","details":json.dumps(r["Q3"]["four_state_sensitivity"]["gate"])},{"term":"four_state_model","details":json.dumps(r["Q3"]["four_state_sensitivity"]["model"])}]; pd.DataFrame(q3rows).to_csv(tabs/"T3_q3_exposure.csv",index=False)
 pd.DataFrame([{"row":k,**{z:v[z] for z in ("estimate","se","p","N","G")},"C_pp":v["C"]["estimate_pp"]} for k,v in r["Q4"]["rows"].items()]).to_csv(tabs/"T4_q4_persistence.csv",index=False)
 q5rows=[{"section":"estimate","item":k,"details":json.dumps(v)} for k,v in r["Q5"]["estimates"].items()]+[{"section":k,"item":"all","details":json.dumps(r["Q5"][k])} for k in ("frame","inclusion_logit","overlap","smd_before","smd_after_primary","entropy")]; pd.DataFrame(q5rows).to_csv(tabs/"T5_q5_transportability.csv",index=False)
 # F1 absolute association and multiplicative risk ratio.
 grid=np.linspace(d.lowcov2019_z.min(),d.lowcov2019_z.max(),200); base=json.load(open(P/"results/stage2/CODEX-S5-EXP-20260909-002/result.json")); b1=base["models"]["M2"]["coefficients"]["anydigpayment"]["estimate"]; b3=s1["estimate"]; rr=np.exp(pois["beta_anydigpayment"]+pois["native"]["estimate"]*grid); pp=100*(b1+b3*grid); fig,ax=plt.subplots(1,2,figsize=(10,4)); ax[0].plot(grid,pp); ax[0].axhline(0,color="black",lw=.7); ax[0].set(xlabel="Low-coverage z",ylabel="LPM association (pp)"); ax[1].plot(grid,rr); ax[1].axhline(1,color="black",lw=.7); ax[1].set(xlabel="Low-coverage z",ylabel="Modified-Poisson risk ratio"); dec=np.quantile(ec.lowcov2019_z,np.arange(.1,1,.1)); vnm=float(ec.loc[ec.iso3.eq("VNM"),"lowcov2019_z"].iloc[0]);
 for a in ax:
  for x0 in dec:a.axvline(x0,color="grey",lw=.35,alpha=.35)
  a.axvline(vnm,color="red",lw=1,ls="--",label="Vietnam"); a.legend()
 fig.tight_layout(); fig.savefig(figs/"F1_absolute_relative.png",dpi=180); plt.close(fig)
 forest=[("S1 LPM",s1b),("S2 logit",logit["C"]),("S3 mod. Poisson",pois["C"]),("S4 fractional",s4c)]+[("Q4 "+k,v["C"]) for k,v in r["Q4"]["rows"].items()]+[("Q5 IPW",q5["C"])]; fig,ax=plt.subplots(figsize=(8,6)); ys=np.arange(len(forest)); vals=[v["estimate_pp"] for _,v in forest]; cis=[v["ci95_cluster_score_percentile"] for _,v in forest]; ax.errorbar(vals,ys,xerr=[[v-c[0] for v,c in zip(vals,cis)],[c[1]-v for v,c in zip(vals,cis)]],fmt="o"); ax.set_yticks(ys,[k for k,_ in forest]); ax.axvline(0,color="black",lw=.7); ax.set_xlabel("Common moderation contrast C (pp)"); fig.tight_layout(); fig.savefig(figs/"F2_common_contrast.png",dpi=180); plt.close(fig)
 r["status"]="ESTIMATED_UNVERIFIED_OUTPUT_CONTRACT_COMPLETE"; r["bootstrap"]={"method":"Rademacher one-step cluster-score bootstrap by economy","B":B,"seed":SEED}; r["completed_utc"]=datetime.now(timezone.utc).isoformat(); FINAL.write_text(json.dumps(r,indent=2,allow_nan=False),encoding="utf-8")
 artifacts=[FINAL,*sorted(tabs.glob("*.csv")),*sorted(figs.glob("*.png"))]; inputs=[PANEL,SRC,P/"data/raw/wb_credit_information_by_country_year.csv",P/"data/raw/wb_credit_information_latest_snapshot.csv",ROOT/"data/raw/data_micro_findex_2024_vietnam.xlsx",P/"data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json",P/"data/raw/wdi_FS.AST.PRVT.GD.ZS_2000_2023.json"]; codes=[Path(__file__),HERE/"complete_h000501_outputs.py",HERE/"regenerate_h000501_q4_r6.py",HERE/"run_h000501_exp_s5_002.py",HERE/"run_h000501_q5.py",HERE/"estimate_stage2_codex.py"]; receipt={"run_id":r["run_id"],"status":r["status"],"independently_reproduced":False,"frozen_hashes":{str(p.relative_to(P)):h for p,h in FROZEN.items()},"code_sha256":{str(p.relative_to(P)):sha256(p) for p in codes},"input_sha256":{str(p.relative_to(ROOT)):sha256(p) for p in inputs},"artifacts_sha256":{str(p.relative_to(RUN)):sha256(p) for p in artifacts},"bootstrap":{"method":"Rademacher one-step cluster-score bootstrap by economy","draws":B,"seed":SEED},"wall_clock_seconds_finalizer":time.time()-started,"environment":{"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"pandas":pd.__version__,"statsmodels":sm.__version__}}; (RUN/"final_receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8"); print(json.dumps({"status":r["status"],"final":str(FINAL),"receipt":str(RUN/"final_receipt.json")},indent=2))
if __name__=="__main__":main()
