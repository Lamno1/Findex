# CLAUDE-S5R-CTRLXMOD-20260910-001 — control × moderator interaction check (SELFREVIEW C5)

**Date:** 2026-09-10 · **Origin:** Claude post-registration robustness check ·
**Independent reproduction: PENDING** (single implementation; Codex has not re-run this) ·
**Verdict: the negative interaction is attenuated but not overturned.**

## Concern (SELFREVIEW C5)

The frozen M2 interacts only `anydigpayment` and `account_fin` with `lowcov2019_z`. If the
individual covariate mix of digital-payment users differs systematically between high- and
low-coverage economies, and those covariates carry a different borrowing slope, the negative
`b3` could be a compositional artifact rather than a coverage effect.

## Check

Add `X_ic × lowcov2019_z` for the full frozen control set (female, age, age², two education
dummies, four income-quintile dummies, urban — 10 terms) to M2 and re-read
`b3 = anydigpayment × lowcov2019_z`. Estimator: Claude's Stage-4 cold implementation
(`CLAUDE-S5R-20260910-001_reproduce.py`); economy FE, `w_equal`, CR1 economy-clustered SE.
N = 100,560, G = 97.

## Result

| Specification | `b3` (pp/SD) | cluster SE | p | 95% CI |
|---|---:|---:|---:|---|
| M2 baseline | −1.975 | 0.474 | 6.8 × 10⁻⁵ | [−2.92, −1.03] |
| M2 + 10 control × moderator interactions | **−1.545** | 0.451 | 9.1 × 10⁻⁴ | [−2.44, −0.65] |

The interaction keeps its sign and significance. About **22% of the baseline magnitude**
(−1.97 → −1.54 pp) is absorbed by allowing the control slopes to vary with country coverage —
i.e. composition explains part of the gradient, consistent with the account-access channel in
§7, but not the reversal itself.

## Status

SELFREVIEW C5: **addressed.** The reversal is not a compositional artifact of the control mix.
This is a post-registration check outside the frozen pre-registration and outside the
independently reproduced quantity set; it should be reported as such and is a candidate for
Codex independent reproduction.

**Artifacts:** `code/study_05_crosscountry/CLAUDE-S5R-CTRLXMOD-20260910-001.py`
(SHA-256 `c6af7813…c561`) · `results/stage4_repro/CLAUDE-S5R-CTRLXMOD-20260910-001/result.json`
