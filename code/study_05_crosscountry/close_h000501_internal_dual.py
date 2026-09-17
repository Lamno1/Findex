"""Close EXP-S5-002 after the internal cold implementation passes."""
from __future__ import annotations
import hashlib,json,platform,sys
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
P=ROOT/"projects/study_05_findex_crosscountry"
RUN=P/"results/stage2/CODEX-S5-EXP-S5-002-20260913-001"
OUT=RUN/"completion_receipt_internal_dual.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists(): raise RuntimeError("completion receipt collision")
 final=json.loads((RUN/"final_result.json").read_text())
 audit=json.loads((RUN/"completion_audit_final.json").read_text())
 cold=json.loads((RUN/"cold_reproduction_codex_b.json").read_text())
 receipt=json.loads((RUN/"final_receipt.json").read_text())
 if final["status"]!="ESTIMATED_UNVERIFIED_OUTPUT_CONTRACT_COMPLETE" or audit["verdict"]!="PASS": raise RuntimeError("run-A delivery gate not passed")
 if cold["status"]!="INTERNAL_DUAL_IMPLEMENTATION_REPRODUCED" or any(not x["match"] for x in cold["comparisons"]): raise RuntimeError("cold implementation mismatch")
 if any(sha(RUN/k)!=v for k,v in receipt["artifacts_sha256"].items()): raise RuntimeError("run-A artifact hash mismatch")
 out={"record_type":"H000501_EXP_S5_002_COMPLETION_RECEIPT","hypothesis":"H-000501","run_A":final["run_id"],"run_B":cold["run_id"],"status":"COMPLETE_INTERNAL_DUAL_IMPLEMENTATION","claim_boundary":"Two separately coded implementations executed by Codex matched all registered headline point quantities checked. This is not external-person or external-model reproduction and is not labelled independently reproduced.","classifications":cold["classifications"],"run_A_delivery_audit":"PASS","cold_quantity_count":len(cold["comparisons"]),"cold_mismatch_count":0,"independently_reproduced":False,"external_reproduction_required":False,"frozen_hashes":receipt["frozen_hashes"],"evidence_sha256":{"final_result.json":sha(RUN/"final_result.json"),"final_receipt.json":sha(RUN/"final_receipt.json"),"completion_audit_final.json":sha(RUN/"completion_audit_final.json"),"cold_reproduction_codex_b.json":sha(RUN/"cold_reproduction_codex_b.json"),"implementation_A":sha(P/"code/study_05_crosscountry/finalize_h000501.py"),"implementation_B":sha(P/"code/study_05_crosscountry/cold_reproduce_h000501_codex_b.py")},"environment":{"python":sys.version,"platform":platform.platform()},"created_utc":datetime.now(timezone.utc).isoformat()}
 OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
 print(json.dumps({"status":out["status"],"receipt":str(OUT)},indent=2))
if __name__=="__main__": main()
