"""D1 regeneration: persist within-R2 for the C5 control-by-moderator check.

The manuscript (Sec 5.3) reports the M2 within-R2 rising from 0.0481 (baseline) to
0.0491 (M2 + full control x lowcov2019_z set). The baseline traces to
results/stage2/CODEX-S5-EXP-20260909-002/interaction_grid.csv; the expanded value
was never written to any result file (TABLEAUDIT-20260910T113000Z D1, MAJOR/UNTRACED).

This script recomputes both within-R2 values with the *same* estimator and the *same*
within-R2 definition used to produce interaction_grid.csv (fit_lpm in
estimate_stage2_codex.py, lines ~73-80: y demeaned by weighted economy-FE means;
within_r2 = 1 - sum(w*resid^2)/sum(w*demeaned^2)), and writes them to a result file
the manuscript can cite.

Run id: CLAUDE-S5R-CTRLXMOD-WR2-20260910-001. Read-only reuse of the frozen estimator.
"""
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
OUT = PROJECT / "results/stage3/CLAUDE-S5R-CTRLXMOD-WR2-20260910-001"
EXPECTED_PANEL_SHA256 = "ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9"
EXTRA = (
    "female_d:lowcov2019_z + age_c:lowcov2019_z + age_c2:lowcov2019_z + "
    "C(educ):lowcov2019_z + C(inc_q):lowcov2019_z + urban_d:lowcov2019_z"
)
BASELINE_WR2_INTERACTION_GRID = 0.048144861463441546


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")
    if sha256(PANEL) != EXPECTED_PANEL_SHA256:
        raise RuntimeError("FAIL_CLOSED analysis-panel hash mismatch")
    data = pd.read_csv(PANEL)

    baseline, _ = fit_lpm(data, "formal_borrow", M2, "w_equal", ())
    expanded, _ = fit_lpm(data, "formal_borrow", f"{M2} + {EXTRA}", "w_equal", ())

    wr2_base = baseline["within_r2"]
    wr2_full = expanded["within_r2"]
    grid_match = abs(wr2_base - BASELINE_WR2_INTERACTION_GRID) < 1e-12

    payload = {
        "run_id": "CLAUDE-S5R-CTRLXMOD-WR2-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "D1 regeneration: persist within-R2 for the C5 control-by-moderator check",
        "implementation": "Codex Stage-2 fit_lpm; same within-R2 definition as interaction_grid.csv",
        "within_r2_baseline_M2": wr2_base,
        "within_r2_with_control_by_moderator": wr2_full,
        "within_r2_delta": wr2_full - wr2_base,
        "baseline_matches_interaction_grid": grid_match,
        "baseline_reference": {
            "file": "results/stage2/CODEX-S5-EXP-20260909-002/interaction_grid.csv",
            "row": "M2",
            "value": BASELINE_WR2_INTERACTION_GRID,
        },
        "N_baseline": baseline["N"], "N_expanded": expanded["N"],
        "G": baseline["G"], "K_baseline": baseline["K"], "K_expanded": expanded["K"],
        "formula_added": EXTRA,
        "panel_sha256": EXPECTED_PANEL_SHA256,
        "code_sha256": sha256(Path(__file__)),
    }
    OUT.mkdir(parents=True)
    result_path = OUT / "result.json"
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "run_id": payload["run_id"],
        "input_sha256": EXPECTED_PANEL_SHA256,
        "output_sha256": sha256(result_path),
        "code_sha256": payload["code_sha256"],
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
