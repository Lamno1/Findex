# STAGE 12 — MODEL RECONSTRUCTION (Phase D + E)

## Weighting (Phase D)

Code (`stage5_estimation_audit.py` line 33 / `stage5_1_reconciliation.py` line 43):

```
w_equal = wgt / groupby(["economycode","wave"])["wgt"].transform("sum")
```

This is the **official Findex wave-specific weight, renormalized to sum to 1 within each
economy-wave cell**, not the raw official weight and not a pooled cross-wave weight. This
choice mechanically gives every economy-wave cell equal total aggregate weight regardless of
its underlying sample size or population, which is a deliberate and disclosed design choice
(the manuscript states this explicitly: "Weights are the official wave-specific weights
normalised within economy-wave; no pooled survey weight is created," body_stage8.tex line
123-124). This is **not** the same as ordinary population-weighted survey regression, and a
reader could reasonably want raw-weight results as a robustness check; a raw-weight
(un-normalized within cell) specification was not found as a reported robustness check
anywhere in `weight_sensitivity.csv` (which only varies weighted-vs-unweighted, not
normalized-vs-raw). This is flagged as a **specification choice that is disclosed but not
stress-tested against the most natural alternative** — not an error, but a gap.

No pooled weight is used in the pooled model in place of wave-specific weights: confirmed
directly in code (the `w_equal` variable is computed once for the full pooled frame, using
`groupby(["economycode","wave"])`, i.e. it still normalizes within economy-*and*-wave even
in the pooled regression, not within economy only). This matches the "no pooled weight" claim.

## Model equation (Phase E)

As estimated in code, for each wave `w`:

```
formal_borrow_icw = β1·digital_payment_icw + β2·(digital_payment_icw × lowcov_z_c)
                     + γ1·female_binary_icw + γ2·age_c_icw + γ3·age_c_icw²
                     + Σ δ_e·1[education_icw=e] + Σ θ_q·1[income_quintile_icw=q]
                     + Σ α_c·1[economy=c]  (economy fixed effects)
                     + ε_icw
```
estimated by WLS with weight `w_equal`, standard errors clustered by economy
(`cov_type="cluster"`, `use_correction=True`). Spec B adds `account_fin` and
`account_fin × lowcov_z`. The pooled secondary model adds `digital_payment × wave2024` and
`digital_payment × lowcov_z × wave2024`, with `lowcov_z` itself time-invariant (2019-fixed),
consistent with the stated design ("the moderator is fixed historically").

**Code vs. manuscript vs. table agreement:** the manuscript's methods section
(body_stage8.tex lines 115-128) states this same equation in prose and LaTeX math, including
the explicit note that "since L_c^2019 does not change between 2021 and 2024, the triple
interaction is a cross-wave conditional contrast" — this matches the code's construction of
`dig_x_lowcov_x_wave` as `digital_payment × lowcov_z × wave2024` (the moderator itself carries
no wave subscript). **No mismatch found** between the code's model and the manuscript's
stated model for the primary/pooled specifications.

Economy fixed effects (`C(economycode)`) are included in every specification. This means the
`digital_payment` main-effect and interaction coefficients are identified from **within-economy**
variation in individual digital-payment status, not from cross-economy variation in overall
adoption levels — an important and correctly implied restriction (the manuscript's own
conclusion states "The interaction is identified by 93 economy-level historical moderator
values, not by 194,558 independent observations of institutional variation," body_stage8.tex
line 226, which correctly describes the effective degrees of freedom problem for the
*moderator-level* variation, though the individual-level main effect and interaction with
individual-level `digital_payment` do use within-economy, respondent-level variation).
