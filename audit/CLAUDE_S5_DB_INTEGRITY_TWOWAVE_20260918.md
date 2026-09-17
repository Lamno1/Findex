# CLAUDE-S5-DB-INTEGRITY-TWOWAVE-20260918-001

Date: 2026-09-18
Concern: Q1 peer-review point — the China (DB2018) / Saudi Arabia (DB2020) Doing
Business "Getting Credit" data-irregularity disclosure (Data section, body_stage8.tex)
was carried as prose only; the existing quantitative exclusion check
(`CODEX-S5-DB-INTEGRITY-20260910-001` / `CLAUDE-S5R-DB-INTEGRITY-20260910-001`) was run
only on the earlier single-wave 97-economy 2024 frame (H-000500/H-000501), not on the
two-wave 93-economy 2021+2024 primary design the current manuscript actually reports.
Verdict: **PASS_SENSITIVITY; MEASUREMENT_LIMITATION_REMAINS** (same qualitative verdict
as the 2026-09-10 single-wave check, now confirmed on the design actually in the paper).

## What was checked

Excludes `CHN` and `SAU` from the Stage 4 analytical dataset
(`results/stage4_build/analytical_dataset.csv`, 194,558 rows / 93 economies), re-standardizes
the 2019 `lowcov_z` moderator (population SD, ddof=0) across the remaining 91 economies, and
re-fits the frozen primary M2 specification
(`digital_payment + dig_x_lowcov + female_binary + age_c + age_c2 + C(education) +
C(income_quintile) + C(economycode)`) separately for 2021 and 2024, with wild-cluster
(Rademacher score-bootstrap, 999 replications) inference — identical estimator, weighting
and inference procedure used throughout the manuscript.

## Result

| Wave | Primary (93 econ.) | Excl. CHN+SAU (91 econ.) | Relative change | Wild-cluster $p$ | N | G |
|---|---|---|---|---|---|---|
| 2021 | -1.7436 pp | -1.6443 pp | 5.7% | 0.001 | 92,263 | 91 |
| 2024 | -1.6085 pp | -1.5386 pp | 4.3% | 0.007 | 92,822 | 91 |

Both estimates retain the same sign, remain statistically significant at conventional
levels, and change by well under the +/-50% stability band used elsewhere in the manuscript
(Stage 17 external-validity / macro-control checks). The result is not driven by the two
in-sample economies with documented *Getting Credit* irregularities.

## What this does and does not establish

This shows the registered coverage reversal survives dropping the two economies with
disclosed data-integrity problems in the specific indicator used as the moderator. It does
not validate the Doing Business production process for the remaining 91 economies, nor does
it rule out general moderator measurement error -- the same limitation already disclosed for
the single-wave check.

Artifacts:
- Code: `code/study_05_crosscountry/db_integrity_sensitivity_twowave.py` (SHA-256
  `E15F6C97A59D3144AC8F55AC1B6818A8A4003D659F57C3BD19F50A04E4B10BA3`)
- Result: `results/stage21_db_integrity_two_wave/excl_chn_sau_estimates.csv`
- Receipt: `results/stage21_db_integrity_two_wave/receipt.json`
- Input panel SHA-256 (Stage 4 analytical dataset, unmodified):
  `78938AFF518F3F3BC049A18E7B8CA5C1042996392B1ACDD6EAAB56FC555240C1`

## Extension (same date): consistency across every table using `lowcov_z`

A reviewer note (2026-09-18) pointed out that `lowcov_z` is also the moderator in the
informal-borrowing placebo (Stage 18) and the macro-control interaction check (Stage 17,
Item 2), and that checking only the primary table while leaving those two on the full
93-economy frame would be an inconsistent application of the same data-integrity concern.
Both were re-run excluding `CHN`/`SAU`, re-standardizing `lowcov_z` (and, for the macro
check, `lgdppc_z`/`acc_rate_z`) over the same 91 economies, with the identical estimator
and wild-cluster inference.

**Placebo (informal borrowing), `dig_x_lowcov`:**

| Wave | Primary (93 econ.) | Excl. CHN+SAU (91 econ.) | Relative change | Wild-cluster $p$ | Same sign |
|---|---|---|---|---|---|
| 2021 | +1.9511 pp | +1.8133 pp | 7.1% | 0.026 | yes |
| 2024 | +1.7547 pp | +1.6861 pp | 3.9% | 0.012 | yes |

The placebo's positive, significant interaction on informal borrowing is unchanged in
sign and significance; it is not an artifact of the two irregularity-implicated economies
either.

**Macro-control interaction, `dig_x_lowcov`:**

| Wave | 93 econ. (with macro controls) | 91 econ. (with macro controls) | Relative change | $p$ (91 econ.) |
|---|---|---|---|---|
| 2021 | -1.206 pp ($p=0.087$) | -1.384 pp | 14.8% | 0.039 |
| 2024 | -0.981 pp ($p=0.311$) | -0.946 pp | 3.6% | 0.331 |

Excluding China and Saudi Arabia does not change the paper's qualitative reading: the
coverage interaction remains attenuated relative to the no-macro-controls primary estimate
in both waves (20.6% and 41.2% relative change against the true 93-economy primary,
respectively) and is not significant at 5% in 2024; in 2021 it is, if anything, slightly
more precisely estimated on the 91-economy frame ($p=0.039$ vs.\ $p=0.087$ on 93 economies)
rather than less. `dig_x_lgdppc` and `dig_x_accrate` themselves remain non-significant in
both waves on 91 economies, consistent with the 93-economy result.

**Conclusion:** the data-integrity sensitivity check is now applied consistently to every
table that uses `lowcov_z` (primary, placebo, and macro-control), not only the headline
result. All three tell the same story on 91 economies as on 93.

Artifacts (extension):
- Code: `code/study_05_crosscountry/db_integrity_sensitivity_placebo_twowave.py`,
  `code/study_05_crosscountry/db_integrity_sensitivity_macro_twowave.py`
- Results: `results/stage21_db_integrity_two_wave/placebo_excl_chn_sau.csv`,
  `results/stage21_db_integrity_two_wave/macro_excl_chn_sau.csv`

Source: World Bank (2020), *Review of Data Irregularities in Doing Business*, 16 December.
