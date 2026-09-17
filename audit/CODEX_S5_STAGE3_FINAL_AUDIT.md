# CODEX-S5-STAGE3-FINAL-001

Date: 2026-09-09  
Study: `study_05_findex_crosscountry`  
Verdict: **H-000500 NOT SUPPORTED; C1 SUPPORTED AS DESCRIPTIVE; INDEPENDENT REPRODUCTION REQUIRED**

## Gate history

Revision 2 and the WDI inputs were frozen before estimation. Stage 1 passed with 100,560
respondents in 97 economies. `CODEX-S5-EXP-20260909-001` is an incomplete, invalid run:
serialization failed before a result or receipt was issued. It was retained and never
overwritten. The valid computational set is:

- `CODEX-S5-EXP-20260909-002` — LPM specifications, registered robustness, BH family,
  Vietnam positioning, F2 and F3;
- `CODEX-S5-M6-2-20260909-001` — registered logit/probit AMEs, M2c joint wild p-value,
  and corrected covariate-adjusted F1;
- `CODEX-S5-TABLES-20260909-001` — T1 through T6 generated from those artifacts;
- `CODEX-S5-AUDIT-20260909-001` — adversarial checks.

All results remain **ESTIMATED_UNVERIFIED**. They are not manuscript-eligible until a
separate agent reproduces the frozen primary results from the raw inputs using a different
run ID and implementation.

## Main findings

M1 estimates a positive within-economy descriptive association between digital-payment use
and formal borrowing: **+0.03617** (cluster SE 0.00514; p < 0.001; 95% CI 0.02597 to
0.04638; wild-score p=0.001).

The preregistered H-000500 test has the opposite sign from predicted. M2's interaction of
digital-payment use with *lower* 2019 credit-information coverage is **-0.01975** per one
economy-level SD (cluster SE 0.00474; p=0.000068; 95% CI -0.02916 to -0.01033;
wild-score p=0.001). M2b is likewise negative (-0.03958; p=0.000093). This is evidence
against the frozen coverage-substitution hypothesis, not a reason to reverse or rewrite it.

The negative sign persists under unweighted and population weights, exclusion of six
high-income economies, M6.5 country controls, minimum-country-size filtering, internet-use
control, employment control, 999 economy-block bootstrap draws, and all 97 leave-one-country
out runs. Logit and probit interaction AMEs are also negative. Alternative moderator
constructs do not reproduce it: the depth proxy is negative but imprecise, while the legal-
rights proxy is positive and imprecise. The finding is therefore specific to the registered
coverage measure, not a generic “weak institutions” effect.

## Mechanism and placebo

The registered mechanism predictions fail. In M3a the making-payment coefficient (0.05172)
is larger than the receiving-payment coefficient (0.04080), contrary to `g1 > g2`. In M3b
the receive interaction is -0.00269 (p=0.587), not positive, while the make interaction is
-0.02021 (p=0.000062).

The placebo/contrast also rejects the intended interpretation: the informal-borrowing
interaction is positive (+0.01736; p=0.0053; BH q=0.0096), rather than approximately zero.
Thus the results cannot support a credit-information substitution mechanism even though
some secondary associations are statistically distinguishable from zero.

## Adversarial attacks

- Dropping each primary control one at a time leaves the M2 interaction negative.
- Restricting to account holders leaves it negative (-0.00803) but imprecise (p=0.218),
  showing that precision and magnitude partly depend on including non-account holders.
- Dropping zero-coverage economies or the lowest coverage quartile leaves it negative.
- Dropping each of seven regions in turn gives estimates from -0.02187 to -0.01412; all
  remain negative.
- Reversing the moderator sign yields the exact algebraic opposite (+0.019748), confirming
  that the substantive direction was not created by a naming/code-sign error.
- Leave-one-economy-out estimates range from -0.02164 to -0.01737 with no sign reversal.

## Claim-contract verdicts

| Claim | Verdict | Permitted reading |
|---|---|---|
| C1 | `SUPPORTED_DESCRIPTIVE_UNVERIFIED` | Positive conditional cross-sectional association only. |
| C2 / H-000500 | `NOT_SUPPORTED_OPPOSITE_SIGN` | The registered substitution prediction is rejected; do not relabel the reverse pattern as confirmation. |
| C3 | `NOT_SUPPORTED` | The receive-versus-make predictions fail. No mechanism claim. |
| C4 | `NOT_SUPPORTED` | The informal-borrow contrast is not null and undermines the proposed interpretation. |
| C5 | `DESCRIPTIVE_POSITIONING_AVAILABLE` | Vietnam may be located in the cross-country distributions; no Vietnam effect. |

## Remaining limitations and non-blocking technical issue

The design is a single cross-section with a non-random 2019 country moderator. Country
fixed effects do not make the cross-level interaction causal. The private-credit robustness
control has unequal country vintages (2008–2023). The GLM package warned that clustered
covariance is not fully supported with fractional frequency weights; M6.2 is therefore
sign-direction sensitivity only and should not be used as primary inference. The LPM is the
registered primary estimator.

## Final decision

The pipeline worked as intended: it preserved a clear null/contrary verdict rather than
searching for a favourable specification. Study 5 may proceed to independent reproduction
and, if reproduced, an honest paper about a positive individual-level association plus a
rejected preregistered substitution hypothesis. It may not claim causality, novelty, a
verified mechanism, or support for H-000500.
