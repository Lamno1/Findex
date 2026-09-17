"""Persist the Study 5 sample-composition statistics used in manuscript section 3.4."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "projects" / "study_05_findex_crosscountry"
PANEL = PROJECT / "results/stage1/CODEX-S5-BUILD-20260909-001/analysis_panel.csv"
OUT = PROJECT / "results/stage3/CODEX-S5-SAMPLE-COMPOSITION-20260910-001"
EXPECTED_SHA = "ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")
    if sha256(PANEL) != EXPECTED_SHA:
        raise RuntimeError("FAIL_CLOSED analysis-panel hash mismatch")
    data = pd.read_csv(PANEL, usecols=["iso3", "region", "any_cov"])
    economies = data.drop_duplicates("iso3")
    payload = {
        "run_id": "CODEX-S5-SAMPLE-COMPOSITION-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "N": int(len(data)), "G": int(len(economies)),
        "economies_by_world_bank_region": economies["region"].value_counts().sort_index().to_dict(),
        "respondents_by_world_bank_region": data["region"].value_counts().sort_index().to_dict(),
        "high_income_economies": int((economies["region"] == "High income").sum()),
        "high_income_respondents": int((data["region"] == "High income").sum()),
        "coverage_below_10_economies": int((economies["any_cov"] < 10).sum()),
        "coverage_below_10_respondents": int((data["any_cov"] < 10).sum()),
        "coverage_below_10_respondent_share": float((data["any_cov"] < 10).mean()),
        "panel_sha256": EXPECTED_SHA,
        "code_sha256": sha256(Path(__file__)),
    }
    OUT.mkdir(parents=True)
    result = OUT / "result.json"
    result.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (OUT / "receipt.json").write_text(json.dumps({"input_sha256": EXPECTED_SHA,
        "output_sha256": sha256(result), "code_sha256": payload["code_sha256"]}, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps(payload, indent=2))
if __name__ == "__main__":
    main()
