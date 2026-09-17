"""Independent Codex reproduction of the post-registration C5 check."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from estimate_stage2_codex import M2, fit_lpm

ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "projects" / "study_05_findex_crosscountry"
PANEL = PROJECT / "results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"
OUT = PROJECT / "results/stage3/CODEX-S5-CTRLXMOD-REPRO-20260910-001"
EXPECTED_PANEL_SHA256 = "ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9"
EXTRA = (
    "female_d:lowcov2019_z + age_c:lowcov2019_z + age_c2:lowcov2019_z + "
    "C(educ):lowcov2019_z + C(inc_q):lowcov2019_z + urban_d:lowcov2019_z"
)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            h.update(chunk)
    return h.hexdigest()

def extract(result: dict) -> dict:
    return result["coefficients"]["anydigpayment:lowcov2019_z"]

def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")
    if sha256(PANEL) != EXPECTED_PANEL_SHA256:
        raise RuntimeError("FAIL_CLOSED analysis-panel hash mismatch")
    data = pd.read_csv(PANEL)
    baseline, _ = fit_lpm(data, "formal_borrow", M2, "w_equal", ())
    expanded, _ = fit_lpm(data, "formal_borrow", f"{M2} + {EXTRA}", "w_equal", ())
    payload = {
        "run_id": "CODEX-S5-CTRLXMOD-REPRO-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Independent reproduction of SELFREVIEW C5 control-by-moderator check",
        "implementation": "Codex Stage-2 patsy/WLS estimator; Claude check code not imported",
        "status": "INDEPENDENT_REPRODUCTION_COMPLETE",
        "N": expanded["N"], "G": expanded["G"],
        "baseline": extract(baseline),
        "with_control_by_moderator": extract(expanded),
        "formula_added": EXTRA,
        "panel_sha256": EXPECTED_PANEL_SHA256,
        "code_sha256": sha256(Path(__file__)),
    }
    OUT.mkdir(parents=True)
    result_path = OUT / "result.json"
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = {"run_id": payload["run_id"], "input_sha256": EXPECTED_PANEL_SHA256,
               "output_sha256": sha256(result_path), "code_sha256": payload["code_sha256"]}
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
