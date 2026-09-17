# STAGE 12 — INDEPENDENT REPLICATION REPORT (Phases B, F, I, J, K)

## Phase B — Sample reconstruction

Independently recomputed directly from `results/stage4_build/analytical_dataset.csv`
(fresh script, not reusing project code):

| Quantity | Reported | Independently recomputed | Match |
|---|---|---|---|
| 2021 rows | 96,711 | 96,711 | YES |
| 2024 rows | 97,847 | 97,847 | YES |
| Total rows | 194,558 | 194,558 | YES |
| Economies (2021) | 93 | 93 | YES |
| Economies (2024) | 93 | 93 | YES |
| Economies common to both waves | 93 | 93 | YES |
| Columns | 12 | 12 | YES |

No missing economies, no duplicate economy-wave pairs found in this check. Raw-file row
counts (143,887 for 2021, 144,090 for 2024) also independently confirmed by direct line
count of the acquired raw CSVs (see `STAGE_12_DATA_PROVENANCE_AUDIT.md`).

## Phase F — Independent re-estimation

Using a freshly written script (`indep_repro.py`, not derived from the project's own
`stage5_estimation_audit.py` line-by-line, though necessarily implementing the same
documented specification), I refit the primary WLS LPM with economy-clustered SEs for both
waves:

```
wave=2021 N=96711 G=93
  digital_payment       =  0.090725 (se 0.004662, p 2.431e-84)
  dig_x_lowcov(interac) = -0.017436 (se 0.004932, p 0.0004075) CI[-0.027104,-0.007769]
wave=2024 N=97847 G=93
  digital_payment       =  0.081290 (se 0.005680, p 1.879e-46)
  dig_x_lowcov(interac) = -0.016085 (se 0.005982, p 0.007167) CI[-0.027810,-0.004361]
```

These match `results/stage5_estimation/estimates.csv` to 6 decimal places for both
coefficients, both standard errors, and both p-values, in both waves. **Classification:
REPRODUCED.**

## Phase H — Leave-one-economy-out

Read directly from `results/stage5_estimation/leave_one_economy_out.csv` (93 rows per wave)
and independently tabulated:

| Wave | n runs | min | max | median | # positive | # negative |
|---|---|---|---|---|---|---|
| 2021 | 93 | -0.019697 | -0.015556 | -0.017403 | 0 | 93 |
| 2024 | 93 | -0.018293 | -0.012674 | -0.016025 | 0 | 93 |

All 186 leave-one-out estimates (93 × 2 waves) are negative — the manuscript's claim ("all
93 deletions preserve the NEGATIVE sign ... in both 2021 and 2024") is **confirmed**, not
merely asserted, and the reported ranges in `body_stage8.tex` ("[-1.97,-1.56] pp in 2021 and
[-1.83,-1.27] pp in 2024") match this table to two decimal places. Note this is a
robustness-of-sign claim; it says nothing about magnitude stability (the 2024 interaction
ranges from -1.27pp to -1.83pp across deletions — a non-trivial ~44% relative range), which
the manuscript does not overstate (it claims sign-robustness, not magnitude-robustness).

## Phase I — Pooled vs. separate-wave reconciliation

Reported: pooled interaction ≈ -1.98pp vs. separate-wave -1.74pp (2021) / -1.61pp (2024).
`results/stage5_1_reconciliation/cross_specification_reconciliation.csv` computes this
explicitly: the pooled "base" interaction (-1.98pp) is not required to equal either
separate-wave estimate because it is a jointly-estimated coefficient under a different
functional form (common controls/FE pooled across waves, plus wave and
wave×interaction terms) and a different effective weighting composition (both waves stacked
before the `w_equal` renormalization is applied, though renormalization is still done
per economy-wave cell — see model reconstruction). This is a legitimate mathematical
explanation, not an unexplained anomaly, and the manuscript does not silently paper over the
numeric gap — the reconciliation file exists specifically to document it, and the difference
is consistent with jointly-estimated common slopes.

## Phase J — 2017 treatment audit

`grep`-checked `body_stage8.tex` for 2017: found only in contextual/supplementary framing —
"2017 is retained only as contextual/supplementary evidence because its payment measure is
[not directly comparable]" (line 45) and "the 2017 payment reconstruction is contextual
only" (line 100). No instance was found treating 2017 as a strict panel wave, a causal
time-comparison point, or a longitudinal treatment. **No violation found.** (2017 is in fact
entirely absent from the Stage 4/5 estimation code — it plays no role in any regression in
this pipeline, consistent with "contextual/supplementary" and arguably under-using it rather
than over-using it.)

## Phase K — `account_fin` audit

Spec A (primary) excludes `account_fin`; Spec B adds `account_fin` and
`account_fin × lowcov_z` as a sensitivity check — confirmed directly in
`stage5_estimation_audit.py` (`specb_rhs` vs `primary_rhs`). Manuscript language
(body_stage8.tex line 178-179): "conditioning on account ownership slightly attenuates the
interaction in 2021 and makes it more negative in 2024. This cross-wave difference does not
identify account access as the mechanism." This correctly avoids calling account access a
mediator/mechanism/pathway. **No contradiction found** between the intended
selection/access-sensitive interpretation and the actual manuscript wording.
