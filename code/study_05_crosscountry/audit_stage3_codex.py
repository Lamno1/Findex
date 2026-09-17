"""Pre-specified/adversarial falsification checks for Study 5 Stage 3."""
from __future__ import annotations
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np,pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parent))
from estimate_stage2_codex import fit_lpm, M2

ROOT=Path(__file__).resolve().parents[4]; P=ROOT/'projects/study_05_findex_crosscountry'
PANEL=P/'results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv'; OUT=P/'results/stage3/CODEX-S5-AUDIT-20260909-001'
EXPECTED='ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9'
def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for z in iter(lambda:f.read(1048576),b''): h.update(z)
 return h.hexdigest()
def one(df,rhs=M2,target='anydigpayment:lowcov2019_z'):
 r,_=fit_lpm(df,'formal_borrow',rhs,'w_equal',()); z=r['coefficients'][target]; return {'estimate':z['estimate'],'se':z['se_cluster'],'p':z['p_cluster'],'N':r['N'],'G':r['G']}
def main():
 if OUT.exists(): raise RuntimeError('FAIL_CLOSED collision')
 if sha(PANEL)!=EXPECTED: raise RuntimeError('FAIL_CLOSED panel hash')
 d=pd.read_csv(PANEL); out={}; base=one(d); out['base']=base
 controls=['account_fin','female_d','age_c','age_c2','C(educ)','C(inc_q)','urban_d']
 out['drop_one_control']={}
 for c in controls:
  terms=[z.strip() for z in M2.split('+')]
  terms=[z for z in terms if z!=c and not (c=='account_fin' and z=='account_fin:lowcov2019_z')]
  rhs=' + '.join(terms)
  out['drop_one_control'][c]=one(d,rhs)
 out['account_holders_only']=one(d[d.account_fin.eq(1)])
 out['drop_zero_coverage']=one(d[d.any_cov.gt(0)])
 out['drop_lowest_coverage_quartile']=one(d[d.any_cov.gt(d[['iso3','any_cov']].drop_duplicates().any_cov.quantile(.25))])
 out['leave_one_region_out']={}
 for reg in sorted(d.region.unique()): out['leave_one_region_out'][reg]=one(d[d.region.ne(reg)])
 rev=d.copy(); rev['highcov2019_z']=-rev.lowcov2019_z; rr=M2.replace('lowcov2019_z','highcov2019_z'); out['sign_reversal_algebra_check']=one(rev,rr,'anydigpayment:highcov2019_z')
 stage2=json.loads((P/'results/stage2/CODEX-S5-EXP-20260909-002/result.json').read_text())
 out['placebo_comparison']={'formal_b3':base['estimate'],'informal_b3':stage2['models']['M4_informal_borrow']['coefficients']['anydigpayment:lowcov2019_z']['estimate'],'informal_p':stage2['models']['M4_informal_borrow']['coefficients']['anydigpayment:lowcov2019_z']['p_cluster']}
 estimates=[x['estimate'] for x in out['leave_one_region_out'].values()]; out['summary']={'all_drop_control_negative':all(x['estimate']<0 for x in out['drop_one_control'].values()),'all_leave_region_negative':all(x<0 for x in estimates),'leave_region_min':min(estimates),'leave_region_max':max(estimates),'account_holder_sign_negative':out['account_holders_only']['estimate']<0,'hypothesis_direction_supported':False,'placebo_undermines_coverage_substitution':out['placebo_comparison']['informal_b3']>0 and out['placebo_comparison']['informal_p']<.05}
 payload={'run_id':'CODEX-S5-AUDIT-20260909-001','status':'ADVERSARIAL_AUDIT_COMPLETE_UNVERIFIED','created_utc':datetime.now(timezone.utc).isoformat(),'checks':out}
 OUT.mkdir(parents=True); (OUT/'adversarial_checks.json').write_text(json.dumps(payload,indent=2)+'\n'); (OUT/'receipt.json').write_text(json.dumps({'panel_sha256':EXPECTED,'code_sha256':sha(Path(__file__)),'output_sha256':sha(OUT/'adversarial_checks.json')},indent=2)+'\n'); print(json.dumps(out['summary'],indent=2))
if __name__=='__main__': main()
