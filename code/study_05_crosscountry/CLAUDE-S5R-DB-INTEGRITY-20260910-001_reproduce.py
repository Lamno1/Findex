"""Independent reproduction of CODEX-S5-DB-INTEGRITY-20260910-001 (SELFREVIEW C6 sensitivity).

Cold check: drop CHN + SAU, re-standardize the 2019 coverage moderator across the remaining
95 economies (population sd, ddof=0), re-fit the frozen M2 specification, compare the
digital-payment x lower-coverage interaction to Codex's reported value.

Reuses ONLY build() and the estimator from CLAUDE-S5R-20260910-001_reproduce.py (Claude's
Stage-4 cold implementation); no Codex estimation code is imported. Run id:
CLAUDE-S5R-DB-INTEGRITY-20260910-001.
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
REPRO = SUB / "code/study_05_crosscountry/CLAUDE-S5R-20260910-001_reproduce.py"
CODEX = SUB / "results/stage3/CODEX-S5-DB-INTEGRITY-20260910-001/result.json"
OUT = SUB / "results/stage4_repro/CLAUDE-S5R-DB-INTEGRITY-20260910-001"
DROP = {"CHN", "SAU"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def load_repro_module():
    spec = importlib.util.spec_from_file_location("s5repro", REPRO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # module guards main() behind __name__ == "__main__"
    return mod


def fit(d, m, BASE):
    d = d.copy()
    d["dig_x_lowcov"] = d.anydigpayment * d.lowcov2019_z
    d["acc_x_lowcov"] = d.account_fin * d.lowcov2019_z
    X, b, V, info = m.run_model(d, BASE)
    coef, se = m.C(X, b, V, "dig_x_lowcov")
    return coef, se, info


def main() -> None:
    if OUT.exists():
        raise RuntimeError(f"FAIL_CLOSED output collision: {OUT}")
    m = load_repro_module()
    BASE = ["anydigpayment", "dig_x_lowcov", "account_fin", "acc_x_lowcov"] + m.CTRL

    d, ec, cc, drop = m.build()

    b0, se0, info0 = fit(d, m, BASE)  # baseline, all 97, for reference

    present = set(d.iso3) & DROP
    if present != DROP:
        raise RuntimeError(f"FAIL_CLOSED expected {sorted(DROP)} in panel, found {sorted(present)}")
    dd = d[~d.iso3.isin(DROP)].copy()
    e = dd.groupby("iso3").any_cov.first().reset_index()
    mean = float(e.any_cov.mean())
    sd = float(e.any_cov.std(ddof=0))
    e["z2"] = -(e.any_cov - mean) / sd
    dd = dd.drop(columns="lowcov2019_z").merge(
        e[["iso3", "z2"]].rename(columns={"z2": "lowcov2019_z"}), on="iso3", how="left", validate="many_to_one"
    )
    b3, se3, info = fit(dd, m, BASE)
    G = info["G"]
    tstat = b3 / se3
    p_t = float(2 * stats.t.sf(abs(tstat), G - 1))
    crit = float(stats.t.ppf(0.975, G - 1))
    ci = [b3 - crit * se3, b3 + crit * se3]

    cj = json.loads(CODEX.read_text())
    cx = cj["interaction"]

    payload = {
        "run_id": "CLAUDE-S5R-DB-INTEGRITY-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "reproduces": "CODEX-S5-DB-INTEGRITY-20260910-001",
        "independent_of": "codex",
        "method": "reuse build() + hand-rolled WLS/CR1 from CLAUDE-S5R-20260910-001_reproduce.py; drop CHN+SAU; re-standardize any_cov z-score (ddof=0) over 95 economies; re-fit frozen M2",
        "baseline_all97": {"dig_x_lowcov": b0, "se_cluster": se0, "N": info0["N"], "G": info0["G"]},
        "restricted": {
            "N": info["N"], "G": G,
            "moderator_mean_95": mean, "moderator_sd_ddof0_95": sd,
            "dig_x_lowcov": b3, "se_cluster": se3, "t": tstat, "p_cluster_t": p_t, "ci95_t": ci,
        },
        "codex_targets": {
            "estimate": cx["estimate"], "se_cluster": cx["se_cluster"], "t": cx["t"],
            "p_cluster": cx["p_cluster"], "ci95": cx["ci95"],
            "moderator_mean_95": cj["moderator_mean_95_economies"],
            "moderator_sd_ddof0_95": cj["moderator_sd_ddof0_95_economies"],
        },
        "abs_diff": {
            "estimate": abs(b3 - cx["estimate"]),
            "se_cluster": abs(se3 - cx["se_cluster"]),
            "moderator_mean_95": abs(mean - cj["moderator_mean_95_economies"]),
            "moderator_sd_ddof0_95": abs(sd - cj["moderator_sd_ddof0_95_economies"]),
        },
        "verdict": "PASS" if (abs(b3 - cx["estimate"]) < 1e-8 and abs(se3 - cx["se_cluster"]) < 1e-8) else "DIFF",
        "code_sha256": sha256(Path(__file__)),
    }
    OUT.mkdir(parents=True)
    (OUT / "result.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
