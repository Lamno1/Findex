# Gate 3C — Empirical Design Specification Audit

Date: 2026-09-17  
Decision: **CONDITIONAL PASS**  
Estimation / pooled analytical file / DiD / IV / manuscript rewrite: **LOCKED**

## 1. Research-question verdict

The strongest defensible question is:

> Does the individual-level digital-payment/formal-borrowing association persist across Findex waves, and does its cross-economy gradient vary systematically with pre-existing credit-reporting coverage?

This is economically meaningful because it tests whether the contrary 2024 gradient is a recurring cross-economy pattern or a one-wave configuration. It is answerable as a repeated-cross-sectional association, provided that the 2021–2024 exposure is reported as broadly aligned rather than proven identical. It does not identify an effect of changing credit-information coverage.

The additional wave resolves one important uncertainty: **persistence/external validity over time**. It does not resolve information substitution, lender use, credit supply, or account-access mechanisms.

## 2. Unit-of-analysis map

| Object | Unit | Role |
|---|---|---|
| Respondent | Individual adult within an economy-wave | Variation in digital payment, borrowing, and covariates |
| Economy | Economy/ISO3 | 2019 coverage moderator and clustering unit |
| Economy-wave | Economy × Findex wave | Repeated cross-sectional context; not an individual panel |

The 2021 release remains one Findex wave even where fieldwork occurred in 2022; raw interview year must be retained separately.

## 3. Estimand table

| Estimand | Conceptual form | Unit | Main variation | Interpretation | Causal? |
|---|---|---|---|---|---|
| E1: wave-specific association | Association of (D_{ict}) with (Y_{ict}) | Individual within economy-wave | Individual exposure variation | Conditional digital-payment/formal-borrowing gradient | No |
| E2: wave-specific coverage gradient | Association of (D_{ict}\times L_{c,2019}) with (Y_{ict}) | Individual exposure × economy moderator | Within-economy exposure combined with between-economy coverage | Whether the exposure gradient differs across historical coverage states | No |
| E3: persistence contrast | (β_{3,2024}-β_{3,2021}) | Contrast of two descriptive gradients | Wave-specific estimates under qualified common exposure | Persistence or change in observed gradient | No |
| E4: institutional-layer heterogeneity | Replace (L) separately with depth or accessibility | Individual × economy | Between-economy institutional dimension | Whether the association varies with a distinct institutional layer | No |

E3 is a temporal descriptive contrast, not an institutional-change effect. Because 2019 coverage is fixed across waves, it cannot identify the effect of a change in coverage.

## 4. Temporal design

Primary comparable exposure waves: **2021 and 2024**, subject to the documented conditional comparability qualification. The 2019 coverage measure is pre-existing relative to both outcomes but time-invariant in the comparison.

2017 contributes contextual outcome/institutional evidence and, if used, a separately labelled approximate reconstructed payment measure. It must not enter the main model as an identical treatment.

The cleanest empirical sequence is:

1. separate 2021 and 2024 wave-specific models as primary;
2. a pooled repeated-cross-section model with wave effects and exposure-by-coverage-by-wave terms as a secondary synthesis, only after exposure documentation is frozen;
3. 2017 contextual/supplementary evidence.

## 5. Exposure definition

The permitted primary exposure is `anydigpayment` for 2021–2024, described as a broadly aligned measure of made-or-received digital payment with documented scope qualifications. It must not be described as an invariant treatment or as a causal treatment effect.

The 2017 reconstructed measure is supplementary only. If the final source-level comparison downgrades 2021–2024 to FAIL, the main design must revert to separate wave-specific payment measures and outcome persistence/context, with no pooled digital-payment exposure.

## 6. Account-ownership strategy

Two conceptual specifications are required; neither is universally superior.

**Specification A — total observed association:** do not condition on `account_fin`. This retains the total observed association between payment activity and formal borrowing and avoids conditioning directly on a potentially payment-derived access measure.

**Specification B — access/selection analysis:** include `account_fin` or restrict to account holders only, explicitly labelled as a conditional association. This may illuminate selection/access heterogeneity, but may also condition away part of the account-access pathway or introduce collider risk because 2021 `account_fin` includes payment/card-derived cases.

Specification B is not a “better controlled” version. Its coefficient must not be interpreted as a mechanism estimate.

## 7. Core model architecture

For each wave, the conceptual individual-level model is:

\[
Y_{ict}=\alpha_c+\beta_{1t}D_{ict}+\beta_{3t}(D_{ict}\times L_{c,2019})+X_{ict}\gamma_t+\varepsilon_{ict}.
\]

Here (Y) is formal borrowing, (D) is the qualified digital-payment measure, (L) is historical 2019 coverage, and (X) contains pre-specified respondent covariates. Economy fixed effects absorb the main effect of (L); they do not absorb (D\times L) because (D) varies within economy.

For a pooled synthesis, wave indicators and interactions are needed to allow both the payment association and coverage gradient to differ by wave. A pooled model must not be interpreted as a common treatment-effect model if the exposure scope differs across waves.

Survey weights define the target as a weighted within-economy adult association. Economy-clustered inference is required because the moderator is economy-level and observations are repeated within economies across waves.

## 8. Identification map

| Quantity | Identifying variation | Removed by economy FE | Remaining limitation |
|---|---|---|---|
| β1t | Individual differences in digital-payment activity within economy-wave | Economy-level payment prevalence | Selection, reverse causality, demand/supply confounding |
| γ3t | Individual payment variation interacted with between-economy 2019 coverage | Main effect of coverage | Only 90–93 relevant common economies depending on sample; moderator is not individual-level |
| E3 | Difference between wave-specific descriptive gradients | Time-invariant economy differences in levels | Not an effect of institutional change; questionnaire and composition differences remain |
| E4 | Individual payment variation interacted with separate institutional layer | Main effect of layer | Layer measures are historical/proxy variables and may have limited coverage |

The effective moderator variation is economy-level. More than 100,000 respondent observations do not create more than one independent coverage value per economy.

## 9. Inference design

The preferred conceptual inference is economy-clustered standard errors, with wild-cluster bootstrap as a robustness procedure where appropriate. Repeated waves make economy the natural dependence unit; economy-wave clustering alone could fail to account for serial dependence within economy across waves. The number of clusters is the number of economies actually used, not the number of respondents.

Weights should remain wave-specific and preserve nationally representative within-economy interpretation. No pooled weight should be invented.

## 10. Institutional-measure hierarchy

| Measure | Role in Gate 3C |
|---|---|
| 2019 coverage | PRIMARY moderator, with explicit “historical formal credit-reporting coverage” label |
| Depth | SECONDARY separate institutional dimension |
| Accessibility/B-READY | VALIDATION or limited subsample/context |
| Legal rights | SEPARATE institutional construct, not a substitute for coverage |
| Positive reporting | VALUABLE secondary layer if consistent coding exists |
| Open banking/alternative-data legality | CONTEXT or exploratory institutional layer |
| Actual lender use | Not available for the main global design; required only for a high-end mechanism claim |

No composite index is permitted.

## 11. Mechanism boundary

The design can document persistence and institutional heterogeneity. It cannot distinguish, by itself, among:

- information substitution;
- institutional complementarity;
- account-access selection;
- lender processing capacity;
- supply-side rationing;
- payment-record measurement error;
- differences between realised borrowing and unmet credit demand.

For all of these: **Not established by the current evidence.**

## 12. Contribution-gain assessment

The gain from adding 2021 is **HIGH relative to the current paper’s principal uncertainty**, because it tests whether the 2024 reverse gradient persists beyond one survey wave. The gain is not mechanism identification and not causal identification.

The strongest plausible contribution is therefore an **individual-level cross-wave institutional-boundary/external-validity paper**: firm-level and retail-level evidence appear to exhibit different observed boundary conditions for the association between digital payments and formal borrowing. The repeated-cross-section extension can strengthen that puzzle without claiming that coverage causes the difference.

## 13. Alternative identification options

| Option | Scientific gain | Requirements | Current feasibility | Decision |
|---|---|---|---|---|
| Repeated cross-section | Persistence and external validity | Qualified common exposure; harmonized outcome; wave-aware inference | Feasible with limitations | Proceed after measurement freeze |
| Institutional panel | Historical institutional heterogeneity | Aligned economy-year measures | Feasible descriptively | Secondary, no causal change claim |
| Natural experiment/DiD | Institutional change effect | Real shock, timing, comparison group, pre-period outcomes | No concrete shock | Locked |
| IV | Exogenous variation in digital payments or coverage | Credible instrument and first stage | None identified | Do not pursue |
| Mechanism data | Distinguishes information value, access, supply, and lender use | Applications, approvals, lender type, terms, records/use | Difficult and country-specific | High-end extension only |

## 14. Exact conditions before estimation

1. Freeze the 2021–2024 `anydigpayment` documentation as either qualified common exposure or wave-specific measures.
2. Decide whether `account_fin` is a conditional covariate only, and pre-specify Specification A versus B conceptually.
3. Define the primary economy sample and retain the raw 2021 interview-year field while coding the release as `wave=2021`.
4. Freeze the separate roles of coverage, depth, and accessibility; no composite index.
5. Write the analysis plan and estimand contract before constructing the analytical dataset.

## 15. Final Gate 3C decision

**CONDITIONAL PASS.**

The strongest testable version is:

\[
\boxed{\text{2021–2024 qualified repeated cross-section}
 + \text{2019 coverage}
 + \text{separate institutional layers}
 + \text{2017 contextual evidence}}
\]

The condition is explicit: the design remains associational, `anydigpayment` must carry its documented scope qualification, and `account_fin` cannot be treated as an invariant neutral control.

## 16. Locked status

Still locked: all regression execution, analytical-file merge/append, pooled coefficient estimation, persistence estimates, treatment-index construction, DiD, IV, causal/mechanism claims, and manuscript rewriting.
