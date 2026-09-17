"""Build frozen T1-T6 presentation tables from immutable Stage 1/2 artifacts."""
import hashlib,json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[4]; P=ROOT/'projects/study_05_findex_crosscountry'; OUT=P/'results/stage2/CODEX-S5-TABLES-20260909-001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists(): raise RuntimeError('FAIL_CLOSED collision')
 base=P/'results/stage2/CODEX-S5-EXP-20260909-002/result.json'; add=P/'results/stage2/CODEX-S5-M6-2-20260909-001/result.json'; panel=P/'results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv'
 d=json.loads(base.read_text()); a=json.loads(add.read_text()); x=pd.read_csv(panel); OUT.mkdir(parents=True)
 (P/'results/stage1/CODEX-S5-BUILD-20260909-001/drop_table.csv').replace if False else None
 pd.read_csv(P/'results/stage1/CODEX-S5-BUILD-20260909-001/drop_table.csv').to_csv(OUT/'T1_drop_table.csv',index=False)
 rows=[]
 for group,q in [('overall',x),('anydigpayment_0',x[x.anydigpayment.eq(0)]),('anydigpayment_1',x[x.anydigpayment.eq(1)])]:
  for v in ['formal_borrow','account_fin','female_d','age','urban_d']:
   rows.append({'panel':group,'variable':v,'weighted_mean':np.average(q[v],weights=q.w_equal),'N':q[v].notna().sum()})
 country=x[['iso3','any_cov','bureau_cov','registry_cov','depth_credit_info_0_8','legal_rights_0_12']].drop_duplicates('iso3')
 for v in ['any_cov','bureau_cov','registry_cov','depth_credit_info_0_8','legal_rights_0_12']:
  rows.append({'panel':'economy_moderator','variable':v,'weighted_mean':country[v].mean(),'N':len(country),'p25':country[v].quantile(.25),'median':country[v].median(),'p75':country[v].quantile(.75),'vietnam':country.loc[country.iso3.eq('VNM'),v].iloc[0]})
 pd.DataFrame(rows).to_csv(OUT/'T2_descriptives.csv',index=False)
 def coef(model,term):
  z=d['models'][model]['coefficients'][term]; return {'model':model,'term':term,'estimate':z['estimate'],'se_cluster':z['se_cluster'],'p_cluster':z['p_cluster'],'p_wild':z.get('p_wild_score_rademacher_999'),'ci_low':z['ci95'][0],'ci_high':z['ci95'][1],'N':d['models'][model]['N'],'G':d['models'][model]['G']}
 pd.DataFrame([coef('M1','anydigpayment'),coef('M2','anydigpayment'),coef('M2','anydigpayment:lowcov2019_z'),coef('M2b','anydigpayment:lowcov2019_bmedian')]).to_csv(OUT/'T3_primary_moderation.csv',index=False)
 pd.DataFrame([coef(m,t) for m,t in [('M3a','receive_dig'),('M3a','make_dig'),('M3b','receive_dig:lowcov2019_z'),('M3b','make_dig:lowcov2019_z')]]).to_csv(OUT/'T4_mechanism.csv',index=False)
 pd.DataFrame([coef('M4_'+m,t) for m in ['mobile_loan_app','emergency_loan_source','informal_borrow'] for t in ['anydigpayment','anydigpayment:lowcov2019_z']]).to_csv(OUT/'T5_secondary_placebo.csv',index=False)
 rr=[]
 for k,z in d['robustness'].items():
  if isinstance(z,dict) and 'estimate' in z: rr.append({'variant':k,**{q:z.get(q) for q in ['estimate','se','p_cluster','p_wild','N','G']}})
 for link,z in a['M6_2'].items(): rr.append({'variant':'M6_2_'+link+'_interaction_AME','estimate':z['ame']['interaction_regressor_ame'],'se':z['ame']['interaction_regressor_ame_se_cluster_delta'],'N':z['N'],'G':z['G']})
 pd.DataFrame(rr).to_csv(OUT/'T6_robustness.csv',index=False)
 receipt={'source_sha256':{str(p.relative_to(P)):sha(p) for p in [base,add,panel]},'output_sha256':{}}
 for p in sorted(OUT.glob('T*.csv')): receipt['output_sha256'][p.name]=sha(p)
 (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt['output_sha256'],indent=2))
if __name__=='__main__': main()
