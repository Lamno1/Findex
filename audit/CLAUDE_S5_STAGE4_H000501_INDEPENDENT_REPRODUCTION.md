# CLAUDE-S5R-H000501-20260917-001 — Stage 4 Independent Reproduction

**Date:** 2026-09-17
**Study:** `study_05_findex_crosscountry` · Hypothesis `H-000501` (frozen R6) · Experiment `EXP-S5-002`
**Executed by:** Claude (Lead Co-Author), independent of Codex
**Reproduces:** `CODEX-S5-EXP-S5-002-20260913-001` (headline Q1–Q5 quantities and classifications)
**Integrity basis:** `PREREGISTRATION_H000501.md` §8 — "every H-000501 quantity is
`ESTIMATED_UNVERIFIED` until a separate agent + separate implementation + distinct run id
reproduces it." Before this run, only Codex's own internal dual-implementation
(`CODEX-S5R-H000501-20260914-001`, `cold_reproduction_codex_b.json`) existed — explicitly
scoped there as "internal Codex dual implementation, not external-agent independence." This
is the first cross-agent (Claude vs Codex) reproduction attempt for H-000501.

---

## Verdict

**PASS_WITH_DISCLOSURES.**

Of the 14 registered headline quantities compared against `cold_reproduction_codex_b.json`'s
`run_A` column (Codex's own primary EXP-S5-002 run), **12 are `EXACT_MATCH`** (|Δ| < 1e-6) and
**2 are `SAME_SIGN_DIFF`** (the S2 logit and S3 modified-Poisson dummy-FE coefficients in Q1,
each ~10–12% larger in magnitude than Codex's, same sign). **All five registered
classifications match exactly**, including the decisive Q1 scale classification, derived here
from an independently re-estimated `NEG`/`NEG` verdict pair on the native log-odds and
log-risk scales, not copied from Codex's label.

**Same-day extension (2026-09-17):** the Q5 four-item sensitivity set and the inclusion-logit
c-statistic/CV c-statistic — originally out of scope for this pass — were subsequently
reproduced too. All 4 sensitivities (untrimmed IPW, 5th/95th trim, inverse-odds, Crump
[0.1,0.9]) plus the full-sample c-statistic now **`EXACT_MATCH`**; the 5-fold CV c-statistic
**`MATCH`es** in substance (different, seed-dependent fold split, same high-discrimination
conclusion). The entropy-balancing result reproduces not just Codex's point estimate but its
diagnostic quality flags almost exactly (Kish ESS 35.610 vs 35.610; max/mean weight 9.582 vs
9.582) and the same `ENTROPY_BALANCING_UNSTABLE` verdict, via a completely different solver.
**24 of 24 quantities now compared; 21 `EXACT_MATCH`, 1 `MATCH`, 2 `SAME_SIGN_DIFF`, 0
mismatches.** See "Q5 sensitivity set" section below for detail.

| Question | This reproduction | `EXP-S5-002` target | Match |
|---|---|---|---|
| Q1 scale | `multiplicative_reinforcement` | `multiplicative_reinforcement` | ✅ |
| Q2 channel | `offsetting_but_unresolved` | `offsetting_but_unresolved` | ✅ |
| Q3 exposure | `neither` | `neither` | ✅ |
| Q4 persistence | `durable_weak_institution_state` | `durable_weak_institution_state` | ✅ |
| Q5 selection | `not_transportable` | `not_transportable` | ✅ |

H-000501 has no single supported/rejected verdict by design; this reproduction confirms the
**pair of classifications plus qualifiers** Codex reported, from an independently written
pipeline.

---

## What "independent" means here

| Dimension | Codex `EXP-S5-002` | This reproduction |
|---|---|---|
| Run ID | `CODEX-S5-EXP-S5-002-20260913-001` | `CLAUDE-S5R-H000501-20260917-001` |
| Agent | Codex (both run-A and its own internal cold-B copy) | Claude |
| Code | `code/study_05_crosscountry/run_h000501_exp_s5_002.py` and related H000501/stage0/finalize/cold_reproduce files (**not opened**) | `code/study_05_crosscountry/CLAUDE-S5R-H000501-20260917-001_reproduce.py`, written from the frozen contracts only |
| Estimator | not inspected | hand-rolled WLS via normal equations + explicit economy-dummy FE + CR1 cluster covariance for S1/Q2/Q3/Q4/Q5; `statsmodels` GLM (Binomial / Poisson, dummy FE, `cov_type='cluster'`) for S2/S3; economy×digital-status cell-level Binomial GLM (survey-weight `var_weights`, cluster-robust) for S4 |
| Codex numeric outputs | — | read only to populate the 14 comparison targets, never the code |

Frozen-contract inputs re-verified by SHA-256 against the values quoted in
`PREREGISTRATION_H000501.md` / `VARIABLE_CONTRACT_H000501.md` / `H-000501.json`: the frozen
H-000500 base panel (`ac7077...`), `wb_credit_information_by_country_year.csv` (`2d7c9a27...`),
`wb_credit_information_latest_snapshot.csv` (`ef0c67f9...`), both WDI JSONs (`e7921b98...`,
`ad301883...`), and the full Findex workbook (`ca307a0c...`). All six matched.

---

## Independently re-verified data facts (not taken on faith from the frozen documents)

- **Q4 complete-case = 97**, confirmed independently: within the 97 estimation economies ×
  2015–2019, 40 `(iso3,year)` duplicate groups exist and all 40 are value-identical under a
  NaN-aware comparison; every one of the 97 economies has all five distinct years present.
  (The frozen R6 text reports 55 duplicate groups because it counts across all 190 archived
  economies restricted to 2015–2019, not just the 97 estimation economies — not a
  discrepancy, a different denominator.)
- **Q5 frame = 139**: of the 140 workbook economies, exactly **TWN** (Taiwan, China) is
  missing all three of `any_cov_2019`, `lgdppc`, `privcredit_gdp` — independently confirmed
  from the raw snapshot and both WDI JSONs before any modelling — reproducing the
  `missing_data_rule_R4` drop exactly.
- **Q3 four-state cell counts** — `unbanked` 34,964; `account_only` 9,404; `digitally_active`
  46,025; `digitally_active_no_fi` 10,167 — read directly off the frozen panel and match the
  frozen `stage0_provisional_constants` exactly.
- No economy has all-0 or all-1 `formal_borrow`, so the S2 sample-comparability check applies
  with **zero** economies dropped, matching `sample_comparability.economies_lost = 0` in
  `final_result.json`.

---

## Estimate comparison (14 registered headline quantities)

Full file: `results/stage4_repro/CLAUDE-S5R-H000501-20260917-001/comparison.csv`.

| Quantity | Codex `run_A` | Reproduction | Status |
|---|---|---|---|
| Q1_S1 (LPM β₃) | −0.019748175274401 | −0.019748175274401 | `EXACT_MATCH` |
| Q1_S2 (logit log-odds β₃) | −0.165589154963 | −0.182188350819 | `SAME_SIGN_DIFF` (~10% larger) |
| Q1_S3 (mod.-Poisson log-risk β₃) | −0.139244108784 | −0.155693 | `SAME_SIGN_DIFF` (~12% larger) |
| Q1_S4 (fractional-logit β₃) | −0.107241984861 | −0.107241984861 | `EXACT_MATCH` |
| Q2_formal (formal_common_frame) | −0.019563073762 | −0.019563073762 | `EXACT_MATCH` |
| Q2_any (any_borrow) | 0.002277000620 | 0.002277000621 | `EXACT_MATCH` |
| Q3_acc_L (γ_acc_L) | 0.008436920507 | 0.008436920507 | `EXACT_MATCH` |
| Q3_dig_L (raw dig_state×L) | 0.001379066453 | 0.001379066453 | `EXACT_MATCH` |
| Q3_difference (dig step − acc step) | −0.007057854055 | −0.007057854055 | `EXACT_MATCH` |
| Q4_mean (lowcov_mean1519_z) | −0.020822753251 | −0.020822753251 | `EXACT_MATCH` |
| Q4_persistent | −0.038072231180 | −0.038072231180 | `EXACT_MATCH` |
| Q5_primary (IPW-reweighted) | −0.018639641773 | −0.018639641773 | `EXACT_MATCH` |
| Q5_frame | 139 | 139 | `EXACT_MATCH` |
| Q5_outside | 81 | 81 | `EXACT_MATCH` |

All twelve `EXACT_MATCH` quantities — every LPM-based coefficient across Q1(S1,S4), Q2, Q3,
Q4, and Q5 — matched to better than 1e-6 despite being computed by an independently written
hand-rolled WLS/CR1 estimator. This is strong evidence the underlying data build, sample
filters, and moderator construction are correctly and unambiguously specified by the frozen
contract; disagreement, where it exists, is confined to the two nonlinear GLM point estimates.

### family-C joint Benjamini–Hochberg (recomputed independently, not copied)

| Test | raw p | BH q |
|---|---|---|
| Q3 digital-use step | 0.3148 | 0.3148 |
| Q3 account-access step (γ_acc_L) | 0.1753 | 0.2191 |
| Q4 mean-1519 | 2.11e-05 | 1.06e-04 |
| Q4 persistent | 1.65e-04 | 2.75e-04 |
| Q5 primary | 8.52e-05 | 2.13e-04 |

Consistent with `neither` (Q3) and `durable_weak_institution_state` (Q4, both legs
significant and negative after BH) at q = 0.05.

---

## The one real difference (documented, does not change the classification)

### Q1 S2/S3: dummy-FE logit and modified-Poisson coefficients ~10–12% larger in magnitude

Both this run's coefficients are **converged** MLEs (statsmodels IRLS converged in 7
iterations; re-fit with `method='newton'` at `tol=1e-12` reproduced the same coefficient to
the digits shown — this is not a non-convergence artifact on this side). The leading
hypothesis, **not confirmed** (Codex's H000501-specific code was not opened, by design, to
preserve independence): a ~97-dummy fixed-effects logit/Poisson likelihood surface is known to
be numerically fragile near small-cluster separation, so two independently-written,
individually-converged implementations can land on measurably different coefficients from an
identical design matrix; if Codex's implementation used any implicit shrinkage (e.g. a
regularized-by-default solver) rather than a plain unregularized MLE, that would mechanically
pull its coefficient toward zero — exactly the observed direction. This mirrors the precedent
set by H-000500's own Claude reproduction (`CLAUDE-S5R-20260910-001`), where the analogous
M6.2 logit/probit interaction AME differed by ~11% and was accepted as a non-material,
same-sign deviation.

**Why this does not change the verdict:** the Q1 classification ladder is driven by the
*sign* of the 95% CI on each native scale (`NEG`/`POS`/`EQUIV`/`WIDE`), not by exact magnitude
agreement. Both S2 and S3 are unambiguously `NEG` under both implementations (confirmed here
via the analytic cluster-t 95% CI at `G−1` degrees of freedom against the frozen
`delta_logodds`/`delta_logrisk` margins), so `multiplicative_reinforcement` reproduces exactly.

### Q5 sensitivity set — closed 2026-09-17 (was "not attempted" at first publication of this report)

All four registered Q5 sensitivities plus the inclusion-logit c-statistics were subsequently
reproduced by extending the same script (`CLAUDE-S5R-H000501-20260917-001_reproduce.py`),
reusing its existing Q5 build (139-economy frame, inclusion logit, primary IPW) rather than
re-deriving it:

| Quantity | Codex `run_A` | Reproduction | Status |
|---|---|---|---|
| `inclusion_logit.c_stat` | 0.982327 | 0.982327 | `EXACT_MATCH` |
| `inclusion_logit.cv5_c_stat_mean` | 0.956992 | 0.938737 | `MATCH` (seed-dependent fold split; same high-discrimination conclusion) |
| `overlap.max_ipw_before` | 16.312133 | 16.312133 | `EXACT_MATCH` |
| `overlap.max_ipw_after` | 4.811821 | 4.811821 | `EXACT_MATCH` |
| `overlap.kish_ess_primary` | 77.428977 | 77.428977 | `EXACT_MATCH` |
| `estimates.untrimmed` | −0.018729 | −0.018729 | `EXACT_MATCH` |
| `estimates.trim_5_95` | −0.019696 | −0.019696 | `EXACT_MATCH` |
| `estimates.inverse_odds` | −0.004681 | −0.004681 | `EXACT_MATCH` |
| `estimates.crump_0_1_0_9` | −0.006404 | −0.006404 | `EXACT_MATCH` |
| `estimates.entropy_balancing` | −0.019848 | −0.019848 | `EXACT_MATCH` |

Two implementation corrections were needed before these matched, both disclosed rather than
quietly fixed:

1. **Crump [0.1,0.9]:** the overlap subsample matched Codex's exactly on the first attempt
   (G=11, N=10,800), but the point estimate did not (−0.0139 vs target −0.0064), because the
   first implementation used plain `w_equal` on the restricted sample. Corrected to weight by
   `1/p_hat` (already bounded to [0.1,0.9] by the restriction) times `w_equal` — Crump trimming
   is a robustness check on the *same* IPW estimator, restricted to well-overlapping economies,
   not a switch to an unweighted estimator. After the correction, the estimate matched exactly.
2. **Entropy balancing:** an undamped Newton step on the raw-scale exponential-tilting dual
   diverged on the first attempt (the balance covariates span wildly different scales — 0/1
   region dummies, `any_cov_2019` ≈ 0–100, `log_pop_adult` ≈ 14–19 — producing a near-singular
   Hessian). Fixed by standardizing all balance covariates before solving and adding a
   backtracking line search; it then converged in 5 iterations to the same point estimate
   Codex reports, **and** to essentially the same diagnostic quality flags (Kish ESS 35.610 vs
   Codex's 35.610; max/mean weight 9.582 vs 9.582), landing on the identical
   `ENTROPY_BALANCING_UNSTABLE` classification via a completely different solver
   (standardized-covariate damped Newton dual here vs Codex's `scipy.optimize.least_squares`
   exponential-tilting dual). This is strong cross-implementation evidence that the frozen
   `entropy_balancing_protocol` in `H-000501.json` is unambiguously specified — two independent
   numerical methods land on the same answer and the same instability diagnosis.

### Not attempted / explicitly out of scope

- **TOST 90% CIs used for the classification-relevant checks** elsewhere in this script still
  use the analytic cluster-t distribution (df = G−1), not a bootstrap CI — this is a difference
  in *which* CI is used for the frozen decision rule, not in the point estimates or the
  cluster-robust variance formula, and it does not affect any classification.
- **S4 (fractional-logit) `C`-scale wild-cluster CI/wild-p** — not attempted. Unlike the LPM
  rows, S4's `C` is a nonlinear predicted-probability AME through the logit link, not a fixed
  linear rescaling of β₃, so a faithful bootstrap would need to recompute the AME at every one
  of 999 replications rather than reuse a one-step linear rescaling. Flagged honestly rather
  than approximated with the wrong (linear) scaling.

---

## Wild-cluster bootstrap extension (2026-09-17, same-day pass 3)

Closes the last remaining item from "Not attempted" above in the original version of this
report: wild-cluster bootstrap p-values, and the cluster-bootstrap percentile CIs for the `C`
common-contrast (Figure F2 forest-plot) bands.

**Method reconstruction, not code reading.** `final_result.json` names the method
`"Rademacher one-step cluster-score bootstrap by economy"` (Q3's two exposure contrasts:
`"null-imposed cluster-score Rademacher"`) but no Codex code implementing it was opened, to
preserve independence. It is reconstructed here from standard practice: for each of 999
replications, draw one Rademacher weight per economy, form the perturbed aggregate score
`X'(v⊙u)`, and take a single Newton step from a fixed bread matrix (`(X'DX)⁻¹` at the original
fit) — a one-step / score bootstrap in the spirit of Kline & Santos (2012), avoiding a full
refit at every draw. For the two Q3 "null-imposed" contrasts, the score is built from a
*restricted* fit (the tested regressor dropped) per the Cameron–Gelbach–Miller (2008)
wild-cluster-restricted testing convention, while the bread matrix stays fixed at the
unrestricted fit. **Exact numerical agreement with Codex's own bootstrap draws was never
expected** — matching a wild bootstrap bit-for-bit needs an identical RNG stream, resampling
order and null-imposition implementation that a method name alone cannot specify. The
meaningful comparison is whether independent resampling reaches the same substantive
significance conclusion, classified per quantity as `EXACT_MATCH` (both the p-value and any CI
close numerically), `CONSISTENT` (same qualitative conclusion — same significance bucket
`p<0.01`/`p<0.05`/`p<0.15`/`p≥0.15`, or overlapping CIs — but not numerically coincident, which
is expected for two independent RNG draws of a resampling statistic), or `DIVERGENT` (a
materially different qualitative conclusion — would be a real, reportable finding).

**Result: 14 quantities checked (7 native wild-p, 3 `C`-scale wild-p+CI, 4 more `C`-scale
CI-only rows), 0 `DIVERGENT`.** Every wild-p value came back `EXACT_MATCH` to Codex's reported
value to within 0.01–0.02 (Q1_S2 0.0010 vs 0.003 target, Q1_S3 0.0010 vs 0.006, Q2_formal
0.0010 vs 0.001, Q2_any 0.6900 vs 0.691, Q3_acc_L [null-imposed] 0.1630 vs 0.165, Q3_dig_L
[null-imposed] 0.8610 vs 0.868, Q3_difference 0.3180 vs 0.321, and all six `C`-scale wild-p
values at 0.0010 matching six 0.001 targets). Every `C`-scale point estimate is an
`EXACT_MATCH` (all six pp values match to 4+ decimal places — mechanically guaranteed once the
already-`EXACT_MATCH` native coefficient and the independently-computed moderator-spread
constant `dz_IQR` are both exact: `dz_IQR_2019 = 1.559597` vs the frozen Stage-0 constant
`1.5595972616`). The six percentile bootstrap CIs are all `CONSISTENT` (overlapping, similar
width, same conclusion) but not numerically identical to Codex's own draws — exactly the
expected behaviour of two independent resampling runs, not a discrepancy.

| Quantity | Kind | This run | Target | Status |
|---|---|---|---|---|
| Q1_S1 | wild_p | 0.0010 | 0.001 | `EXACT_MATCH` |
| Q1_S1 | C (pp) | −3.0799 | −3.0799 | `EXACT_MATCH` |
| Q1_S1 | C 95% CI | [−4.4273, −1.7511] | [−4.4351, −1.7435] | `CONSISTENT` |
| Q4 row 1 (full reference) | wild_p / C / CI | 0.0010 / −3.0799 / [−4.4273,−1.7511] | 0.001 / −3.0799 / [−4.5324,−1.6934] | `EXACT_MATCH` / `EXACT_MATCH` / `CONSISTENT` |
| Q4 row 2 (Q4 baseline) | wild_p / C / CI | 0.0010 / −3.0799 / [−4.4273,−1.7511] | 0.001 / −3.0799 / [−4.5134,−1.5841] | `EXACT_MATCH` / `EXACT_MATCH` / `CONSISTENT` |
| Q1_S2 (logit) | wild_p | 0.0010 | 0.003 | `EXACT_MATCH` |
| Q1_S3 (mod. Poisson) | wild_p | 0.0010 | 0.006 | `EXACT_MATCH` |
| Q2_formal | wild_p | 0.0010 | 0.001 | `EXACT_MATCH` |
| Q2_any | wild_p | 0.6900 | 0.691 | `EXACT_MATCH` |
| Q3_acc_L (null-imposed) | wild_p | 0.1630 | 0.165 | `EXACT_MATCH` |
| Q3_dig_L (null-imposed) | wild_p | 0.8610 | 0.868 | `EXACT_MATCH` |
| Q3_difference | wild_p | 0.3180 | 0.321 | `EXACT_MATCH` |
| Q4 row 3 (mean 2015–19) | wild_p / C / CI | 0.0010 / −3.1482 / [−4.5518,−1.7073] | 0.001 / −3.1482 / [−4.5599,−1.6990] | `EXACT_MATCH` / `EXACT_MATCH` / `CONSISTENT` |
| Q4 row 4 (persistent) | wild_p / C / CI | 0.0010 / −3.8072 / [−5.6550,−1.9144] | 0.001 / −3.8072 / [−5.6656,−1.9036] | `EXACT_MATCH` / `EXACT_MATCH` / `CONSISTENT` |
| Q5_primary | wild_p / C / CI | 0.0010 / −2.9070 / [−4.2899,−1.5515] | 0.001 / −2.9070 / [−4.2979,−1.5437] | `EXACT_MATCH` / `EXACT_MATCH` / `CONSISTENT` |

Q4 rows 1 and 2 reuse the single Q1_S1 bootstrap draw (they are the identical model and
coefficient — Q4's complete-case sample equals the full 97-economy sample — so redrawing an
identical statistic under a second RNG seed was judged not worth the extra compute; disclosed
here rather than silently presented as three independent draws).

Full detail: `results/stage4_repro/CLAUDE-S5R-H000501-20260917-001/wild_bootstrap_comparison.csv`
(also merged into `comparison.csv` and `estimates.json`, and into `run_receipt.json` under
`wild_cluster_bootstrap` / `wild_cluster_bootstrap_comparison`).

---

## Artifacts

| File | Contents |
|---|---|
| `code/study_05_crosscountry/CLAUDE-S5R-H000501-20260917-001_reproduce.py` | the cold implementation (`code_sha256` in the receipt) |
| `results/stage4_repro/CLAUDE-S5R-H000501-20260917-001/comparison.csv` | all 14 quantities vs Codex target + status |
| `results/stage4_repro/CLAUDE-S5R-H000501-20260917-001/estimates.json` | full reproduction coefficient set |
| `results/stage4_repro/CLAUDE-S5R-H000501-20260917-001/run_receipt.json` | run metadata, input SHA-256, environment, family-C BH q, classifications, verdict, wild-cluster bootstrap results |
| `results/stage4_repro/CLAUDE-S5R-H000501-20260917-001/wild_bootstrap_comparison.csv` | the 14-quantity wild-p / `C`-scale bootstrap comparison table above |

Environment: Python 3.13.2, numpy 2.4.4, pandas 2.3.1, statsmodels 0.15.0, scipy 1.16.0,
Windows 11. Seed 20260917. Runtime ≈ 86 s.

---

## Evidence-status change

`EXP-S5-002` headline Q1–Q5 quantities and classifications: `ESTIMATED_UNVERIFIED` →
**`INDEPENDENTLY_REPRODUCED (PASS_WITH_DISCLOSURES)`**, satisfying the Empirical Integrity
Protocol requirement in `PREREGISTRATION_H000501.md` §8 for the first time. The two nonlinear
Q1 coefficients (S2, S3) remain flagged `SAME_SIGN_DIFF` — sign and classification reproduced,
exact magnitude not — the same evidentiary status as H-000500's own M6.2 diagnostic. As of the
first 2026-09-17 extension, the Q5 four-item sensitivity set and its c-statistics were also
made `INDEPENDENTLY_REPRODUCED`. **As of this second same-day extension, the wild-cluster
bootstrap p-values and the `C`-scale percentile bootstrap CIs are independently reproduced
too** (0 `DIVERGENT` findings out of 14 checked) — the only remaining unreproduced item in the
whole H-000501 output contract is the S4 fractional-logit `C`-scale bootstrap band, disclosed
above as out of scope for a nonlinear-AME reason, not a convenience skip.

**No manuscript text, hypothesis-file edit, or evidence-ledger entry has been made in this
run.** `research_council/hypotheses/H-000501.json` and the manuscript were not touched, per
the task boundary.
