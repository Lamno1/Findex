# Stage 14 — Gate Decision

## Decision

**B — EMPIRICALLY SOUND, INTERPRETATION NEEDS LIMITATION.**

## Basis for the decision

### Q1 — Are the reported numbers correct?
**YES.** Independently reconstructed from raw acquisition files with a deliberately
different moderator-standardization convention (economy-level rather than
pooled-respondent-level) and reproduced the same signs, closely similar magnitudes, and
matching cluster p-values for both waves (2021: 0.0896 / -0.0171 vs. reported 0.0907 /
-0.0174; 2024: 0.0803 / -0.0157 vs. reported 0.0813 / -0.0161). The leave-one-economy-out
file was independently re-tabulated and its summary statistics (min, max, median, IQR,
sign counts) match the manuscript's stated ranges exactly. The account-sensitivity (SPECB)
and unweighted-robustness numbers were checked and are internally consistent with the
manuscript's qualitative description of them.

### Q2 — Is the statistical design implemented correctly?
**YES**, with two precision caveats that do not change the sign or qualitative conclusion:
(1) the coverage moderator is standardized over the pooled 194,558-respondent frame rather
than over the 93 equally-weighted economies, which this review confirmed changes the
interaction coefficient by only ~2-3%; (2) the "wild-cluster bootstrap" is specifically a
null-imposed cluster-score Rademacher bootstrap with a fixed standard error per replicate —
a legitimate, code-reviewed (Stage 12 P4) linearized variant, but not the classical
refit-based Cameron-Gelbach-Miller procedure the phrase most often denotes in applied
econometrics. Both should be named more precisely in the manuscript or an appendix; neither
requires re-estimation.

### Q3 — Does the interpretation exceed what the design can establish?
**Mostly no** for the causal/mechanism claims, which are already unusually tightly hedged
throughout `body_stage8.tex` (see `STAGE_14_CLAIM_LANGUAGE_REVIEW.md`: no instance found of
"effect," "mechanism," "complementarity," "stability," or "registered" being used beyond
what the design supports). **Partially yes** for the implied population scope of
"transportability" and "boundary condition": the 93-economy frame is not a neutral
intersection of "whatever Findex happened to survey twice" but a population pre-filtered by
a 2024 survey-module-administration rule that this review confirmed is correlated with the
moderator's substantive content (the excluded 40 economies are overwhelmingly high-income,
high-credit-coverage economies verified to have complete, not missing, 2019 data). This is
a disclosure gap, not a computational or design flaw, and it is fixable by adding text, not
by rerunning anything.

## Why not A

Because a specific, previously undisclosed (in the manuscript itself, though partly
inferable from `PREREGISTRATION.md`) population-scope limitation was found that affects how
far "transportability" can honestly be read, a clean "no material weakness" verdict is not
supportable.

## Why not C or D

No error was found in the arithmetic, the estimator, the clustering, the weighting logic,
the fixed-effects specification, or the leave-one-economy-out reconstruction; every number
this review attempted to independently reproduce, reproduced. The sample-composition
concern is a scope/disclosure issue that narrows the population the claims describe; it
does not reverse the sign, threaten the internal validity of the coefficient as an estimate
of "the association in the 93 sampled economies," or invalidate the wild-cluster inference.
Per the brief's own Q1/Q2/Q3 framework, this is squarely a "Q1=YES, Q2=YES, Q3 needs
narrowing" case, which the brief explicitly instructs should not be treated as an empirical
failure.

## Required actions before Stage 15 (not optional, but does not require new estimation)

1. Add one to two sentences to the Data section (or Limitations) disclosing that the
   97-economy 2024 baseline reflects module administration, not a complete or random draw
   of the 140 raw 2024 economies, and that the excluded economies (jointly present in both
   raw waves) are disproportionately high-income and near-universal-coverage.
2. Name the bootstrap procedure precisely at least once (null-imposed cluster-score
   Rademacher bootstrap with fixed per-replicate SE) rather than the generic "wild-cluster
   bootstrap."
3. State the ~3% `account_fin`/`anydigpayment` 2021 construction overlap next to the
   account-sensitivity paragraph in Results, not only in the upstream Stage 3 audit trail.
4. Add a one-line note that the leave-one-economy-out IQR is narrow in part because of the
   equal-economy-weighting scheme, so it should be read as ruling out single-country
   influence, not as evidence of cross-economy homogeneity.
5. Verify (against the actual Global Findex codebook, not this project's internal notes)
   whether `fin22a` aggregates multiple credit products; if it does, add one sentence
   acknowledging the outcome may combine loan types with different information
   requirements.
6. Optionally verify whether any of the 93 sample economies' 2019 "Getting Credit"
   sub-indices were affected by the World Bank's 2020-21 Doing Business data-integrity
   review; if any were, disclose it as a moderator-measurement caveat.

None of these require new data, new estimation, a new pre-registration, or any change to
frozen Stage 3-13 artifacts, `main.tex`, `H-000500.json`, or `H-000501.json`.
