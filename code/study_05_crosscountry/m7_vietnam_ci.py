"""M7 --- persist the Vietnam fitted-slope point estimate AND its 95% CI.

The manuscript (Section 6) reports the M2-implied digital-payment/formal-borrowing
association evaluated at Vietnam's 2019 coverage as +5.07 pp with a 95% CI of
3.87--6.27 pp. The point estimate is in results/stage2/.../result.json (vietnam.
m2_implied_association) and was reproduced to 12 decimals; the CI was never
persisted -- the last reproducibility gap before submission.

This script recomputes both by importing the Stage-4 cold estimator
(CLAUDE-S5R-20260910-001_reproduce.py), fitting M2, and applying the delta method
to  slope(z) = b_dig + b_x * z  at  z = z_VNM :
    Var = V_dd + z^2 V_xx + 2 z V_dx ,  crit = t_{0.975}(G-1) .

Run id: CLAUDE-S5R-M7-VNM-CI-20260910-001. Reuses only build()+estimator; no Codex code.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import stats

SUB = Path(__file__).resolve().parents[2]
MOD = SUB / "code/study_05_crosscountry/CLAUDE-S5R-20260910-001_reproduce.py"
OUT = SUB / "results/stage3/CLAUDE-S5R-M7-VNM-CI-20260910-001"


def sha256(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()


def load_mod():
    spec = importlib.util.spec_from_file_location("s5repro_m7", MOD)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")
    m = load_mod()
    d, ec, cc, drop = m.build()
    d = d.copy()
    d["dig_x_lowcov"] = d.anydigpayment * d.lowcov2019_z
    d["acc_x_lowcov"] = d.account_fin * d.lowcov2019_z
    base = ["anydigpayment", "dig_x_lowcov", "account_fin", "acc_x_lowcov"] + m.CTRL

    X, b, V, info = m.run_model(d, base)
    cols = list(X.columns)
    i = cols.index("anydigpayment")
    j = cols.index("dig_x_lowcov")

    z_vnm = float(d.loc[d.iso3 == "VNM", "lowcov2019_z"].iloc[0])
    slope = float(b[i] + b[j] * z_vnm)
    var = float(V[i, i] + z_vnm**2 * V[j, j] + 2.0 * z_vnm * V[i, j])
    se = float(np.sqrt(var))
    G = info["G"]
    crit = float(stats.t.ppf(0.975, G - 1))
    lo, hi = slope - crit * se, slope + crit * se

    payload = {
        "run_id": "CLAUDE-S5R-M7-VNM-CI-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Persist the M7 Vietnam fitted-slope point estimate and 95% CI (delta method).",
        "implementation": "Claude Stage-4 cold WLS+CR1 estimator; no Codex code imported",
        "method": "slope(z) = b_anydigpayment + b_dig_x_lowcov * z ; delta-method Var = V_dd + z^2 V_xx + 2 z V_dx ; crit = t_{0.975}(G-1)",
        "vietnam_lowcov2019_z": z_vnm,
        "m2_b_anydigpayment": float(b[i]),
        "m2_b_dig_x_lowcov": float(b[j]),
        "vcov_ii": float(V[i, i]),
        "vcov_jj": float(V[j, j]),
        "vcov_ij": float(V[i, j]),
        "fitted_slope_vnm": slope,
        "fitted_slope_vnm_pp": slope * 100.0,
        "se": se,
        "crit_t_Gminus1": crit,
        "ci95": [lo, hi],
        "ci95_pp": [lo * 100.0, hi * 100.0],
        "N": info["N"], "G": G,
        "cross_check_point_estimate": {
            "stage2_vietnam_m2_implied_association": 0.05072053991664186,
            "abs_diff": abs(slope - 0.05072053991664186),
        },
        "code_sha256": sha256(Path(__file__)),
        "reproduces_module_sha256": sha256(MOD),
    }
    OUT.mkdir(parents=True)
    (OUT / "result.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
