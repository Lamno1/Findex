# Stage 4 — Analytical Dataset Integrity Report

Date: 2026-09-17  
Build script: `code/study_05_crosscountry/build_stage4_dataset.py`  
Contract: Stage 3D.1  
Estimation performed: **No**

## Build result

The dataset was built from the raw Findex 2021 and 2024 CSV files, restricted to the frozen 93-economy manifest, and transformed using the pre-specified missing/special-response rules. No 2017 observations entered the primary dataset. `account_fin` was preserved but not used to condition the primary Specification A sample.

| Item | Result |
|---|---:|
| Final rows | 194,558 |
| Columns | 12 |
| Economies | 93 |
| 2021 rows | 96,711 |
| 2024 rows | 97,847 |
| Dataset SHA-256 | `78938AFF518F3F3BC049A18E7B8CA5C1042996392B1ACDD6EAAB56FC555240C1` |

## Sample rule

The final row set uses complete cases for the required outcome, qualified exposure, weight, sex, age, education, and income-quintile fields. DK, refused, invalid, and structural/out-of-universe values were not recoded to zero and were not imputed. The complete-case rule was applied before any estimation and is recorded in `sample_flow.csv`.

## Artifacts

- `analytical_dataset.csv`
- `ANALYTICAL_DATASET_MANIFEST.json`
- `sample_flow.csv`
- `variable_lineage.csv`
- `missingness_summary.csv`
- `digital_payment_validation.csv`
- `reproducibility_verification.json`
- `SHA256.txt`

## Integrity checks

- Required variables were present in both raw waves.
- Primary economy membership is exactly the frozen 93-economy frame.
- Wave values are only 2021 and 2024.
- 2021 raw interview year was preserved separately; records coded 2022 remain in `wave=2021`.
- `fin22a` and `anydigpayment` were recoded only through the frozen mappings.
- `educ` retains codes 1–3; codes 4/5 and missing values are missing.
- `inc_q` retains codes 1–5.
- Original wave-specific weights were preserved; no pooled weight was created.
- `account_fin` is preserved for later Specification B but does not define the primary sample.
- Deterministic rebuild was byte-identical: `true`.

## Decision

**STAGE 4 = CONDITIONAL PASS.**

The analytical dataset follows the frozen contract and the integrity rebuild passed. The qualification is that the 2021–2024 digital-payment exposure remains a documented broadly aligned, not invariant, construct and `account_fin` remains a selection/access sensitivity variable.

## Unlock rule

Estimation may be opened only as the next explicitly authorized stage under this frozen dataset and contract. DiD, IV, causal/mechanism claims, post-result specification changes, and manuscript rewriting remain locked.
