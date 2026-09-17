"""Complete registered Stage 2 items omitted from CODEX-S5-EXP-20260909-002."""
from __future__ import annotations
import hashlib, json, platform, sys, time
from datetime import datetime, timezone
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[4]
PROJECT=ROOT/"projects/study_05_findex_crosscountry"
PANEL=PROJECT/"results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"
OUT=PROJECT/"results/stage2/CODEX-S5-M6-2-20260909-001"
EXPECTED="ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9"
SEED=20260909; B=999
M2="anydigpayment + anydigpayment:lowcov2019_z + account_fin + account_fin:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for z in iter(lambda:f.read(1048576),b''): h.update(z)
 return h.hexdigest()

def fail(x): raise RuntimeError("FAIL_CLOSED: "+x)

def ame(beta,cov,names,X,lowcov,link):
 j1=names.index('anydigpayment'); j3=names.index('anydigpayment:lowcov2019_z')
 eta=X@beta
 if link=='logit': mu=1/(1+np.exp(-np.clip(eta,-35,35))); deriv=mu*(1-mu)
 else:
  from scipy.stats import norm
  deriv=norm.pdf(eta)
 def calc(b):
  e=X@b
  if link=='logit': m=1/(1+np.exp(-np.clip(e,-35,35))); q=m*(1-m)
  else:
   from scipy.stats import norm
   q=norm.pdf(e)
  return np.array([np.mean(q*(b[j1]+b[j3]*lowcov)),np.mean(q*b[j3])])
 base=calc(beta); grad=np.zeros((2,len(beta))); eps=1e-6
 for j in range(len(beta)):
  step=eps*max(1,abs(beta[j])); bp=beta.copy(); bm=beta.copy(); bp[j]+=step; bm[j]-=step; grad[:,j]=(calc(bp)-calc(bm))/(2*step)
 av=grad@cov@grad.T; se=np.sqrt(np.maximum(np.diag(av),0))
 return {"anydigpayment_ame":float(base[0]),"anydigpayment_ame_se_cluster_delta":float(se[0]),"interaction_regressor_ame":float(base[1]),"interaction_regressor_ame_se_cluster_delta":float(se[1]),"definition":"sample-average derivative of inverse-link probability; digital derivative includes beta_any + beta_interaction*lowcov; interaction-regressor derivative is inverse-link derivative times beta_interaction"}

def main():
 if OUT.exists(): fail('collision')
 if sha(PANEL)!=EXPECTED: fail('panel hash mismatch')
 d=pd.read_csv(PANEL); OUT.mkdir(parents=True)
 y,x=patsy.dmatrices('formal_borrow ~ '+M2,d,return_type='dataframe'); names=list(x.columns); groups=d.loc[x.index,'iso3']
 fits={}
 for link_name,link in [('logit',sm.families.links.Logit()),('probit',sm.families.links.Probit())]:
  print(link_name,flush=True); model=sm.GLM(y,x,family=sm.families.Binomial(link=link),freq_weights=d.loc[x.index,'w_equal'])
  method='newton'
  try: fit=model.fit(method='newton',maxiter=100,cov_type='cluster',cov_kwds={'groups':groups})
  except Exception:
   method='lbfgs'; fit=model.fit(method='lbfgs',maxiter=100,cov_type='cluster',cov_kwds={'groups':groups})
  beta=np.asarray(fit.params); cov=np.asarray(fit.cov_params());
  fits[link_name]={"converged":bool(getattr(fit,'converged',True)),"method":method,"N":int(fit.nobs),"G":int(groups.nunique()),"coefficients":{"anydigpayment":float(beta[names.index('anydigpayment')]),"interaction":float(beta[names.index('anydigpayment:lowcov2019_z')])},"ame":ame(beta,cov,names,np.asarray(x),d.loc[x.index,'lowcov2019_z'].to_numpy(),link_name)}

 # Exact joint cluster-score wild bootstrap for M2c's two registered interactions.
 rhs="anydigpayment + anydigpayment:lowbureau2019_z + anydigpayment:lowregistry2019_z + account_fin + account_fin:lowcov2019_z + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)"
 yy,xx=patsy.dmatrices('formal_borrow ~ '+rhs,d,return_type='dataframe'); nms=list(xx.columns); X=np.asarray(xx); Y=np.asarray(yy).ravel(); w=d.loc[xx.index,'w_equal'].to_numpy(); g=d.loc[xx.index,'iso3'].astype('category').cat.codes.to_numpy(); bread=np.linalg.pinv((X*np.sqrt(w)[:,None]).T@(X*np.sqrt(w)[:,None]),rcond=1e-11); beta=bread@(X.T@(w*Y)); u=Y-X@beta; ids=np.unique(g); score=np.vstack([(X[g==k]*w[g==k,None]).T@u[g==k] for k in ids]); infl=score@bread.T
 jj=[nms.index('anydigpayment:lowbureau2019_z'),nms.index('anydigpayment:lowregistry2019_z')]; V=(len(ids)/(len(ids)-1))*((len(Y)-1)/(len(Y)-X.shape[1]))*bread@(score.T@score)@bread; b=beta[jj]; vv=V[np.ix_(jj,jj)]; obs=float(b@np.linalg.pinv(vv)@b)
 rng=np.random.default_rng(SEED); draws=[]
 for _ in range(B):
  delta=rng.choice([-1.,1.],len(ids))@infl[:,jj]; draws.append(float(delta@np.linalg.pinv(vv)@delta))
 joint={"wald_chi2":obs,"df":2,"wild_cluster_score_p":float((1+np.sum(np.asarray(draws)>=obs))/(B+1)),"B":B,"seed":SEED}

 # Covariate-adjusted country gap: residualise outcome on registered controls + economy FE, excluding digital-payment terms.
 ry,rx=patsy.dmatrices('formal_borrow ~ account_fin + female_d + age_c + age_c2 + C(educ) + C(inc_q) + urban_d + C(iso3)',d,return_type='dataframe'); Xr=np.asarray(rx); wr=d.loc[rx.index,'w_equal'].to_numpy(); br=np.linalg.pinv((Xr*np.sqrt(wr)[:,None]).T@(Xr*np.sqrt(wr)[:,None]),rcond=1e-11)@(Xr.T@(wr*np.asarray(ry).ravel())); resid=np.asarray(ry).ravel()-Xr@br; z=d.loc[rx.index,['iso3','anydigpayment','any_cov']].copy(); z['resid']=resid; z['w']=wr; gaps=[]
 for c,q in z.groupby('iso3'):
  rates={k:np.average(a.resid,weights=a.w) for k,a in q.groupby('anydigpayment')}
  if 0 in rates and 1 in rates: gaps.append({'iso3':c,'any_cov':q.any_cov.iloc[0],'adjusted_gap':rates[1]-rates[0]})
 gaps=pd.DataFrame(gaps); gaps.to_csv(OUT/'F1_adjusted_country_gaps.csv',index=False); co=np.polyfit(gaps.any_cov,gaps.adjusted_gap,1); grid=np.linspace(gaps.any_cov.min(),gaps.any_cov.max(),100); vv=gaps[gaps.iso3.eq('VNM')]
 plt.figure(figsize=(7,5)); plt.scatter(gaps.any_cov,gaps.adjusted_gap,s=18,alpha=.7); plt.plot(grid,np.polyval(co,grid),color='black'); plt.scatter(vv.any_cov,vv.adjusted_gap,color='red'); plt.annotate('Vietnam',(vv.any_cov.iloc[0],vv.adjusted_gap.iloc[0])); plt.xlabel('2019 credit-information coverage (%)'); plt.ylabel('Covariate-adjusted borrowing residual gap'); plt.tight_layout(); plt.savefig(OUT/'F1_adjusted_country_gap.png',dpi=180); plt.close()
 out={"run_id":"CODEX-S5-M6-2-20260909-001","status":"ESTIMATED_UNVERIFIED_STAGE2_COMPLETION","M6_2":fits,"M2c_joint_wild":joint,"F1":{"method":"outcome residualised on frozen individual controls and economy FE, excluding digital-payment terms; weighted residual gap by digital status within economy","countries":len(gaps)},"created_utc":datetime.now(timezone.utc).isoformat()}
 (OUT/'result.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); receipt={"input_panel_sha256":EXPECTED,"code_sha256":sha(Path(__file__)),"outputs_sha256":{p.name:sha(p) for p in OUT.iterdir() if p.is_file() and p.name!='receipt.json'},"environment":{"python":sys.version,"statsmodels":sm.__version__,"platform":platform.platform()}}; (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2))

if __name__=='__main__': main()
