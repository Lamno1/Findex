"""SELFREVIEW C5 — post-registration robustness: add control x moderator interactions to M2.

If the covariate mix of digital-payment users differs across countries by 2019 coverage, and
those covariates carry a different borrowing slope, the negative b3 could be compositional.
This check adds X_ic x lowcov2019_z for the full frozen control set to M2 and re-reads b3
(anydigpayment x lowcov2019_z). Single implementation (Claude), pending independent reproduction.

Run id: CLAUDE-S5R-CTRLXMOD-20260910-001. Reuses only build()+estimator from the Stage-4 module.
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
OUT = SUB / "results/stage4_repro/CLAUDE-S5R-CTRLXMOD-20260910-001"


def sha256(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()


def load_mod():
    spec = importlib.util.spec_from_file_location("s5repro", REPRO)
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

    Xb, bb, Vb, ib = m.run_model(d, base)
    b3_base, se_base = m.C(Xb, bb, Vb, "dig_x_lowcov")

    xterms = []
    for c in m.CTRL:
        col = f"{c}_x_lz"
        d[col] = d[c].astype(float) * d.lowcov2019_z
        xterms.append(col)
    Xf, bf, Vf, iff = m.run_model(d, base + xterms)
    b3_full, se_full = m.C(Xf, bf, Vf, "dig_x_lowcov")

    G = iff["G"]
    t = b3_full / se_full
    p = float(2 * stats.t.sf(abs(t), G - 1))
    crit = float(stats.t.ppf(0.975, G - 1))
    ci = [b3_full - crit * se_full, b3_full + crit * se_full]

    payload = {
        "run_id": "CLAUDE-S5R-CTRLXMOD-20260910-001",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "SELFREVIEW C5: M2 + full control x lowcov2019_z interaction set",
        "origin": "claude_post_registration_check",
        "independent_reproduction_status": "PENDING",
        "spec": "M2 (anydigpayment, dig_x_lowcov, account_fin, acc_x_lowcov, + 10 frozen controls) + {control x lowcov2019_z for each of the 10 controls}",
        "N": iff["N"], "G": G,
        "b3_dig_x_lowcov_baseline_M2": {"est": b3_base, "se_cluster": se_base},
        "b3_dig_x_lowcov_with_controlXmod": {
            "est": b3_full, "se_cluster": se_full, "t": t, "p_cluster_t": p, "ci95_t": ci,
        },
        "added_terms": xterms,
        "conclusion": (
            "b3 stays negative and significant" if (b3_full < 0 and p < 0.05)
            else "b3 changes sign or loses significance"
        ),
        "code_sha256": sha256(Path(__file__)),
    }
    OUT.mkdir(parents=True)
    (OUT / "result.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
