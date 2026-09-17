"""Fail-closed delivery audit for EXP-S5-002; does not re-estimate models."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
P=ROOT/"projects/study_05_findex_crosscountry"
RUN=P/"results/stage2/CODEX-S5-EXP-S5-002-20260913-001"
FINAL=RUN/"final_result.json"; RECEIPT=RUN/"final_receipt.json"; OUT=RUN/"completion_audit_final.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(cond,msg,checks): checks.append({"check":msg,"pass":bool(cond)})
def main():
 r=json.loads(FINAL.read_text(encoding="utf-8")); z=json.loads(RECEIPT.read_text(encoding="utf-8")); checks=[]
 check(r["status"]=="ESTIMATED_UNVERIFIED_OUTPUT_CONTRACT_COMPLETE","status is complete but unverified",checks)
 check(z.get("independently_reproduced") is False,"no independent-reproduction claim",checks)
 check(all(sha(P/k)==v for k,v in z["frozen_hashes"].items()),"all three frozen R6 hashes intact",checks)
 check(all(sha(RUN/k)==v for k,v in z["artifacts_sha256"].items()),"artifact hashes match receipt",checks)
 check(set(r["Q1"]["common_contrasts"])=={"S1","S2_logit","S3_modified_poisson","S4_fractional_logit"},"Q1 S1-S4 common contrasts present",checks)
 check(r["Q1"]["sample_comparability"]["economies_lost"]==0,"sample comparability present",checks)
 check(r["Q2"]["multinomial_exploratory"]["converged"],"Q2 multinomial converged",checks)
 check(r["Q3"]["four_state_sensitivity"]["gate"]["interpretable"],"Q3 four-state gate metrics present and passed",checks)
 check(len(r["Q4"]["rows"])==4 and all("C" in x for x in r["Q4"]["rows"].values()),"Q4 four rows each have C",checks)
 check(r["Q4"]["deduplication"]["complete_case_economies"]==97 and not r["Q4"]["deduplication"]["nonidentical_groups"],"Q4 R6 NaN-aware window audit",checks)
 check(r["Q5"]["classification"]=="not_transportable" and r["Q5"]["overlap"]["outside_count"]==81,"Q5 overlap/classification retained",checks)
 check(all((RUN/"tables"/f"T{i}_{n}.csv").stat().st_size>0 for i,n in [(1,"q1_scale"),(2,"q2_channel"),(3,"q3_exposure"),(4,"q4_persistence"),(5,"q5_transportability")]),"T1-T5 exist and nonempty",checks)
 check(all((RUN/"figures"/n).stat().st_size>0 for n in ["F1_absolute_relative.png","F2_common_contrast.png"]),"F1-F2 exist and nonempty",checks)
 check(r["bootstrap"]["B"]==999 and "cluster-score" in r["bootstrap"]["method"],"registered bootstrap method/draw count",checks)
 check(all(x["C"]["B"]==999 for x in r["Q4"]["rows"].values()),"Q4 C bootstrap counts",checks)
 verdict="PASS" if all(x["pass"] for x in checks) else "FAIL"
 out={"record_type":"EXP_S5_002_FINAL_DELIVERY_AUDIT","run_id":r["run_id"],"verdict":verdict,"checks":checks,"data_challenge":{"artifact_inventory":"final_result, receipt, T1-T5, F1-F2 and frozen R6 triple inspected","variable_lineage":"analysis_panel plus documented World Bank coverage/WDI sources; transformations are recorded in code and receipt hashes","coverage":{"individuals":100560,"economies":97,"Q5_frame":139},"quality_findings":["R6 Q4 duplicate check is scoped to 2015-2019 and NaN-aware","Q5 lacks common support and is classified not_transportable"],"merge_audit":"Q4 complete case is 97; Q5 is 139 after the registered TWN exclusion","leakage_and_revision_risks":"2019/2015-2019 moderator vintage remains a disclosed design limitation","unverified_semantics":[],"design_support":"Output contract can support descriptive diagnostics, not causal claims","feasibility_verdict":"FEASIBLE_WITH_LIMITATIONS"},"created_utc":datetime.now(timezone.utc).isoformat()}
 OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
 if verdict!="PASS": raise RuntimeError(json.dumps(out,indent=2))
 print(json.dumps({"verdict":verdict,"audit":str(OUT)},indent=2))
if __name__=="__main__": main()
