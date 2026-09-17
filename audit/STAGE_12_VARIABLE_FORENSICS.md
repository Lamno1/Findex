# STAGE 12 — VARIABLE FORENSICS (Phase C)

Source: `code/study_05_crosscountry/build_stage4_dataset.py` (lines 33-44) and
`stage5_estimation_audit.py` / `stage5_1_reconciliation.py` (moderator merge).

## C1-C5 — Coding as implemented

| Analytical var | Raw source | Coding | Missing handling |
|---|---|---|---|
| `formal_borrow` | `fin22a` | `{1:1, 2:0}` map; anything else (3/4, DK/refused) → `NaN` | dropped in complete-case build |
| `digital_payment` | `anydigpayment` | `{1:1, 0:0}` map | dropped if missing |
| `account_fin` | `account_fin` (already binary in raw extract) | passthrough | **not** used for primary complete-case filter (preserved even if missing on other vars) |
| `female_binary` | `female` | `{1:1, 2:0}` | dropped if missing |
| `education` | `educ` | retained only if in `{1,2,3}`; 4/5 → `NaN` | dropped if missing |
| `income_quintile` | `inc_q` | retained only if in `{1..5}` | dropped if missing |
| `age` | `age` | `pd.to_numeric`, coerce errors to `NaN` | dropped if missing |
| moderator `coverage` | `wb_credit_information_by_country_year.csv`, year==2019, `max(credit_bureau_cov_pct, credit_registry_cov_pct)` | economy-level, one row per `iso3` after `drop_duplicates` | asserted non-missing for all 93 economies (`assert d.coverage.notna().all()`) — **independently confirmed**: the merge is `validate="many_to_one"` and the assertion holds in the delivered `estimates.csv` runs (all N match the analytical dataset N, no silent row loss) |

## C6 — Cross-wave comparability of `digital_payment`

The manuscript and `variable_lineage.csv` both explicitly label `anydigpayment` as
"qualified-comparable 2021-2024," not a strict invariant treatment — this matches the task
brief's design description and is stated consistently, not silently upgraded to a strict
treatment anywhere found in `body_stage8.tex` (checked with a full-text grep for
"invariant," "identical construct," "same treatment," none of which appear applied to
`anydigpayment`).

## C7/C8 — "Low coverage" coding and sign convention

```
lowcov_z = -(coverage - mean(coverage)) / std(coverage, ddof=0)
```

This is a population-standardized (ddof=0) z-score of coverage, **sign-reversed** so that
higher `lowcov_z` = *lower* actual credit-bureau/registry coverage. This is coded
correctly for the stated interpretation ("low coverage" should load positively on
`lowcov_z`): an economy with coverage below the 93-economy mean gets `lowcov_z > 0`.
Independently re-derived from `wb_credit_information_by_country_year.csv` in the Stage 12
reproduction script and found consistent — confirmed no sign error.

## C9 — Interaction coefficient interpretation matches the coding

`dig_x_lowcov = digital_payment * lowcov_z`. A **negative** coefficient on this term means:
holding digital-payment status fixed, the association between digital payment and formal
borrowing is *weaker* in economies with *lower* 2019 credit-information coverage (since
`lowcov_z` is higher there). This is exactly how the manuscript describes it ("the
interaction ... is negative," "weaker in economies with thinner historical 2019
credit-reporting coverage"). **No sign-convention mismatch found.**

## Not independently re-verified (scope limitation, disclosed per rule 14)

- The exact raw-value dictionaries for `educ` and `inc_q` were not cross-checked against
  the official Global Findex 2021/2024 codebooks in this session (would require opening the
  codebook PDFs at the World Bank microdata catalogue links in `source_url.txt`); coding
  logic in the build script is internally sensible (1-3 / 1-5 category retention) but is
  marked **UNVERIFIED against the official codebook**.
- `fin20`/`fin21` wave-specific-meaning caveats (medical borrowing 2017/2021 vs. mobile-loan
  application 2024) are not used anywhere in the Stage 4/5 build or estimation code — they
  do not appear among the 12 analytical columns or in the regression formulas — so the
  caveat about not treating them as cross-wave mechanism variables is **moot for this
  pipeline** (they are simply not used), not a violation.
- `account_fin` interpretation check: see `STAGE_12_CLAIM_AUDIT.md` (Phase K).
