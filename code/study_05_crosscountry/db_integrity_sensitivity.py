"""Sensitivity of Study 5 M2 to Doing Business integrity-implicated economies."""
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
OUT = PROJECT / "results/stage3/CODEX-S5-DB-INTEGRITY-20260910-001"
EXPECTED_PANEL_SHA256 = "ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9"
DROP_ISO3 = {"CHN", "SAU"}

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")
    if sha256(PANEL) != EXPECTED_PANEL_SHA256:
        raise RuntimeError("FAIL_CLOSED analysis-panel hash mismatch")
    data = pd.read_csv(PANEL)
    found = set(data.loc[data["iso3"].isin(DROP_ISO3), "iso3"].unique())
    if found != DROP_ISO3:
        raise RuntimeError(f"FAIL_CLOSED expected {sorted(DROP_ISO3)}, found {sorted(found)}")
    restricted = data.loc[~data["iso3"].isin(DROP_ISO3)].copy()
    economy = restricted[["iso3", "any_cov"]].drop_duplicates()
    if economy["iso3"].duplicated().any():
        raise RuntimeError("FAIL_CLOSED moderator is not unique by economy")
    mean = economy["any_cov"].mean()
    sd = economy["any_cov"].std(ddof=0)
    z = economy.assign(lowcov2019_z=-(economy["any_cov"] - mean) / sd)
    restricted = restricted.drop(columns="lowcov2019_z").merge(
        z[["iso3", "lowcov2019_z"]], on="iso3", how="left", validate="many_to_one"
    )
    result, _ = fit_lpm(restricted, "formal_borrow", M2, "w_equal", ())
    term = result["coefficients"]["anydigpayment:lowcov2019_z"]
    payload = {
        "run_id": "CODEX-S5-DB-INTEGRITY-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "C6 sensitivity excluding China and Saudi Arabia and re-standardizing coverage",
        "excluded_economies": sorted(DROP_ISO3),
        "N": result["N"], "G": result["G"],
        "moderator_mean_95_economies": mean,
        "moderator_sd_ddof0_95_economies": sd,
        "interaction": term,
        "panel_sha256": EXPECTED_PANEL_SHA256,
        "code_sha256": sha256(Path(__file__)),
    }
    OUT.mkdir(parents=True)
    output = OUT / "result.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = {"run_id": payload["run_id"], "input_sha256": EXPECTED_PANEL_SHA256,
               "output_sha256": sha256(output), "code_sha256": payload["code_sha256"]}
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
