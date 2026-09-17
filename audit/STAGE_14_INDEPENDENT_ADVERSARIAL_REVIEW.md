# Stage 14 — Truly Independent Adversarial Review

Reviewer role: independent adversarial reviewer, not part of the Stage 1-13 pipeline.
Method: the empirical object was reconstructed from primary sources (raw acquisition CSVs,
the frozen 93-economy manifest, the World Bank credit-information file) before any prior
audit report was opened. Prior Stage 9/10/12/13 reports were read only after this
document's independent conclusions were fixed (see
`STAGE_14_REVIEWER_INDEPENDENCE_NOTE.md`).

No Stage 3-13 artifact, Codex-authored file, `body.tex`, `main.tex`, or `H-000500.json`/
`H-000501.json` was modified in the course of this review. All new material sits under
`audit/STAGE_14_*`.

## 1. Blind reconstruction (answered before reading prior audits)

**1. Exact empirical design.** For each wave w ∈ {2021, 2024}: a survey-weighted (weights
normalized to sum to 1 within economy×wave) linear probability model of `formal_borrow`
(`fin22a`) on `digital_payment` (`anydigpayment`), an interaction `digital_payment ×
lowcov_z`, economy fixed effects, and controls (sex, age, age², education category, income
quintile). `lowcov_z` is a continuous, sign-flipped, standardized version of
max(private-bureau, public-registry coverage, 2019), fixed at the economy level and
identical across both waves. Inference clusters on economy (93 clusters); a null-imposed
cluster-score Rademacher bootstrap (999 reps) is used for the interaction term. A pooled
model adds wave and payment×wave and payment×lowcov×wave terms. A leave-one-economy-out
loop drops each of the 93 economies and re-estimates the interaction coefficient only.

**2. What variation identifies the interaction.** Two layers: (a) individual-level
covariation between `digital_payment` and `formal_borrow` within an economy-wave cell, net
of economy fixed effects and controls; (b) a single cross-sectional slope of that
individual-level association against 93 time-invariant economy values of `lowcov_z`. The
interaction is therefore identified off exactly 93 economy-level moderator values, not off
194,558 independent draws of institutional variation — the manuscript's own Limitations
section says this explicitly, and it is correct.

**3. What population the result describes.** Not "the world." It describes adults in the
93 economies for which the 2024 Global Findex borrowing/digital-payment module was
administered **and** which also appear in the 2021 release. This is a materially narrower
and non-random population than "countries observed in Findex" — see §4 below and
`STAGE_14_IDENTIFICATION_AUDIT.md`.

**4. Required assumptions for the stated interpretation.** (i) `anydigpayment` is
sufficiently comparable 2021→2024 that a level comparison of its coefficient is
meaningful; (ii) `fin22a` measures a single economically coherent "formal borrowing"
construct; (iii) the 2019 coverage variable is a meaningful proxy for "how thin the
formal credit-information environment is" in 2021 and 2024, i.e., cross-economy ranking
of coverage did not reshuffle materially in the interim; (iv) the linear-probability
functional form and equal-weighting-by-economy estimand are the right description of "the
association"; (v) the wild-cluster bootstrap correction is adequate with 93 clusters.

**5. Alternative explanations that remain observationally compatible.** See
`STAGE_14_ALTERNATIVE_EXPLANATIONS_MATRIX.md`. The most important are: account-ownership
selection into who is even eligible to show a "formal borrowing" outcome; correlation of
the coverage moderator with income/financial-system depth generally rather than
credit-information specifically; and the survey's own module-administration rule, which
already selects the estimation population on variables adjacent to the moderator.

**6. What could make the interaction mechanical.** If `lowcov_z` is highly collinear with
GDP per capita or overall financial-system depth, the "coverage" interaction could be
picking up a generic income/financial-development gradient in how digital payments relate
to borrowing, unrelated to credit-information specifically. The design cannot rule this out
because no income or financial-depth control is included in the interaction (only
individual-level income quintile, which is a within-economy, not between-economy,
control).

**7. What could make two-wave persistence misleading.** `lowcov_z` is *the same 93 numbers
in both waves* — it is a fixed 2019 snapshot, not a time-varying institutional measure.
Persistence of the interaction across 2021 and 2024 is therefore at least partly guaranteed
by construction: the between-economy ranking that generates the interaction cannot change
between waves because the moderator itself does not change. What *could* have differed, and
did not, is the within-economy digital-payment/borrowing association and its within-wave
weighting by that fixed ranking. That is a real (if narrower) empirical fact, but it is not
the same as showing that the underlying institutional relationship persisted; it shows that
a slope estimated against a frozen ranking gave a similar answer twice on adjacent,
highly-overlapping cross-sections of largely the same 93 countries.

**8. Claims stronger than the data justify.** On direct reading of `body_stage8.tex`
before consulting prior audits, the text is unusually disciplined; see
`STAGE_14_CLAIM_LANGUAGE_REVIEW.md`. The residual points of concern are (a) the Data
section's account of *why* the sample is 93/97 economies, which does not disclose that the
97-economy 2024 baseline is itself a module-administered subset correlated with financial
inclusion, and (b) the description of the bootstrap simply as "wild-cluster bootstrap"
without noting it is a null-imposed cluster-score/Rademacher variant that does not
re-estimate the standard error on each replicate.

## 2. P1 — Internal validity of the estimated pattern

An independent, from-scratch reconstruction was built (not a re-run of the project's
scripts) directly from `data/acquisition/FINDEX_2021/raw_microdata.csv`,
`data/acquisition/FINDEX_2024/raw_microdata.csv`, `data/manifests/findex_2021_2024_primary_93.csv`,
and `data/raw/wb_credit_information_by_country_year.csv`, coding all variables independently
from the manuscript's stated rules rather than importing `build_stage4_dataset.py`. One
deliberate design change was introduced: the coverage moderator was standardized at the
**economy level** (93 equally weighted values) rather than at the pooled-respondent level
used in the project's own scripts (`stage5_estimation_audit.py`, `stage5_1_reconciliation.py`,
`stage5_leave_one_out.py`, all of which compute `mean()`/`std()` over the row-level, i.e.
respondent-weighted, pooled 194,558-row frame before splitting by wave).

Independent result:

| Wave | digital_payment | dig_x_lowcov (economy-level z) | p (cluster) |
|---|---:|---:|---:|
| 2021 | 0.0896 | -0.0171 | 0.0004 |
| 2024 | 0.0803 | -0.0157 | 0.0072 |

Project-reported result (respondent-level standardization):

| Wave | digital_payment | dig_x_lowcov | p (cluster) |
|---|---:|---:|---:|
| 2021 | 0.0907 | -0.0174 | 0.0004 |
| 2024 | 0.0813 | -0.0161 | 0.0072 |

**Finding:** the sign, approximate magnitude, and cluster p-values are robust to this
construction choice; the two standardizations differ by roughly 2–3% in the interaction
coefficient (economy-level SD of coverage = 31.79 vs. the pooled-respondent SD used in the
frozen pipeline). **Q1 (are the reported numbers correct) = YES**, confirmed independently,
not merely by re-running the existing code. **However**, this also means the manuscript's
implicit "per one SD of institutional coverage" language is not exactly a per-economy-SD
statement — it is a per-SD-of-the-survey-weighted-pooled-distribution statement, which
over-weights the moderator distribution toward economies with larger raw Findex sample
sizes (e.g., India, Nigeria, China have larger raw N than small economies). The effect on
the substantive results is small (as shown above) but the manuscript should say so.

**LOO reconstruction.** `results/stage5_estimation/leave_one_economy_out.csv` and its
generating script `stage5_leave_one_out.py` were inspected line-by-line rather than merely
re-run. Independently recomputed summary statistics from the existing CSV (`STAGE_14_LOO_DIAGNOSTIC.csv`):

- 2021: 93/93 negative, min -0.01970, max -0.01556, median -0.01740, IQR [-0.01762, -0.01723].
- 2024: 93/93 negative, min -0.01829, max -0.01267, median -0.01602, IQR [-0.01627, -0.01577].

These match the manuscript's stated ranges exactly. **Important qualification** (see §5
of the required Final Report and `STAGE_14_IDENTIFICATION_AUDIT.md`): because `w_equal`
gives each of the 93 economies equal aggregate weight, dropping any single economy removes
almost exactly 1/93 (≈1.08%) of total estimation weight. The IQR is therefore mechanically
narrow (≈0.0004 pp wide in 2021) by the design of the weighting scheme, not because the
underlying relationship is homogeneous across economies. Sign preservation across 93
single-economy drops is a real and useful check against one dominant-influence country; it
is not evidence of homogeneity across subsets of economies (e.g., by region or income), a
distinction the manuscript's own text (correctly) avoids over-claiming, but that the
"robustness" framing invites a reader to over-read.

**Weight-sensitivity robustness.** `results/stage5_estimation/weight_sensitivity.csv`
(unweighted LPM) gives dig_x_lowcov = -0.0161 (2021) and -0.0143 (2024), both p<0.01 —
consistent in sign and similar in magnitude to the weighted primary estimates. This
robustness check exists in the results tree but is not reported in `body_stage8.tex`; it
strengthens the internal-validity case and could be cited.

**Bootstrap.** `stage5_1_reconciliation.py`'s `wild_cluster()` function implements a
**null-imposed cluster-score Rademacher bootstrap**: it imposes the null on the target
coefficient, computes economy-level score contributions of the null residual, flips their
sign with independent Rademacher draws 999 times, reconstructs the implied coefficient via
the fixed "bread" matrix (X'WX)⁻¹ from the *original, unrestricted* design, and forms a
bootstrap t-statistic using the **original** (non-bootstrapped) standard error as the
denominator in every replicate. This is a legitimate, well-known linearized wild-bootstrap
variant (in the spirit of Kline & Santos's cluster-robust score bootstrap), appropriate
when refitting a model with ~100 fixed-effect dummies 999 times per specification is
costly. It is **not** the classical Cameron–Gelbach–Miller wild-cluster-restricted
bootstrap, which re-estimates the coefficient *and* its standard error from a full refit on
each synthetic draw. The manuscript's plain phrase "wild-cluster bootstrap" is not wrong,
but it elides a design choice (fixed SE across replicates) that a specialist referee would
want named. Stage 12's P4 audit already code-reviewed this and found it "statistically
sound... correct null-imposed score/Rademacher construction" — this review agrees with that
assessment on the mechanics, and adds the more precise characterization above.

## 3. P2 — Identification of the interaction

The interaction is identified by combining (a) genuine individual-level, within-economy
variation in `digital_payment` and `formal_borrow` with (b) exactly 93 cross-sectional
values of a fixed 2019 institutional index. This is a classic "micro variable × macro
moderator" design, and its Achilles heel is always the same: nothing in the estimating
equation can separate "coverage" from any other economy-level characteristic that is
correlated with coverage across the same 93 economies. The design does not, and cannot on
its own, distinguish the coverage channel from:

- income/financial-system-depth generally (no GDP per capita or financial-depth control is
  interacted; income quintile is an *individual*, within-economy control and cannot proxy
  for *between*-economy development level);
- the survey's own module-administration selection rule (see next section), which already
  restricts the estimation population on a variable plausibly correlated with financial
  inclusion.

This review's own quantitative check (below) shows this is not a hypothetical concern.

### Sample-composition finding (new; not surfaced in Stage 9/12/13's headline text)

The 2024 Findex borrowing/digital-payment module was administered in 97 of the 140 raw 2024
economies (`papers/study_05/PREREGISTRATION.md` §0: "the economies where the 2024 Global
Findex borrowing/digital-payment module was administered **and** complete primary
covariates are available"). The 93-economy primary frame is the intersection of that
97-economy set with the 139 economies in the 2021 raw release. This review cross-checked
the raw acquisition files directly:

- 133 economies are common to the 2021 and 2024 **raw** releases (140 and 139 economies
  respectively).
- Of those 133, **40 are excluded from the 93-economy frame**, and this excluded set is
  overwhelmingly high-income/OECD: Australia, Austria, Belgium, Canada, Switzerland, Chile,
  Cyprus, Czechia, Germany, Denmark, Spain, Estonia, Finland, France, UK, Greece, Hong Kong,
  Hungary, Ireland, Iceland, Israel, Italy, Japan, Korea, Lithuania, Latvia, Malta,
  Netherlands, Norway, New Zealand, Portugal, Russia, Singapore, Slovakia, Slovenia,
  Sweden, Taiwan, Uruguay, USA (plus Lesotho, which is excluded for a documented, unrelated
  reason — `inc_q` is entirely missing there per `VARIABLE_CONTRACT.md`).
- These excluded high-income economies are **not** missing 2019 coverage data: this review
  directly verified 2019 values for AUS, USA, DEU, JPN, GBR, ITA, KOR, CAN in
  `data/raw/wb_credit_information_by_country_year.csv` and found credit-bureau coverage of
  100% for most of them. They are excluded because the 2024 survey module was not
  administered there (plausibly because near-universal formal inclusion made the module
  less informative to field), not because the moderator is unavailable.
- Comparing the moderator's distribution inside vs. outside the 93-economy frame (economies
  with valid 2019 coverage data, n=93 in-sample vs. n=97 with-data-but-excluded): means are
  similar (42.5 vs. 43.0), but the **interquartile range is compressed** in-sample (11.7 to
  60.7) relative to the excluded pool (1.2 to 92.6), and 24 of the 34 economies worldwide
  with near-universal coverage (≥95%) are excluded from the 93-economy frame, vs. only 10
  retained.

**Interpretation.** The primary sample is not simply "whichever economies happened to be
surveyed in both waves." It is a population pre-filtered by a Findex fieldwork decision
that is plausibly endogenous to the very construct the moderator is meant to capture
(formal financial-system completeness). The 93-economy frame under-represents the
near-universal-coverage tail of the global distribution and, to a lesser extent,
under-represents the very-low-coverage tail as well (25th percentile 11.7 in-sample vs. 1.2
in the excluded pool) — i.e., both extremes are compressed. This does not appear to bias
the *within-sample* sign or magnitude of the interaction (the LOO and unweighted robustness
checks show no single economy or weighting scheme drives the sign), but it materially
narrows what population the "boundary condition" and "transportability" language can
honestly be read to describe: the finding characterizes a population that already excludes
the richest, most credit-information-complete economies in the world, for a reason (module
administration) that is not disclosed in `body_stage8.tex`'s Data section. The manuscript's
current sentence — "The original 2024 baseline contains 97 economies; the difference
reflects the requirement of a common two-wave frame and does not imply that the two samples
are the same population" — is true as far as it goes (93 vs. 97) but does not explain why
the 2024 baseline itself is 97 rather than the raw 140, nor that this restriction is
correlated with the moderator's substantive content.

## 4. Persistence-across-waves challenge (Section 6 of the brief)

Because `lowcov_z` is fixed at 2019 and identical in both waves, two-wave "persistence" of
the interaction cannot, by construction, be driven by any change in the moderator. What it
tests is narrower: whether the within-economy digital-payment/borrowing gradient, weighted
by the *same* fixed cross-economy ranking, gives a similar answer on two different calendar
cross-sections drawn from largely the same 93 countries roughly three years apart. Given
that country-level financial-system composition, survey methodology, and the payment/
borrowing constructs themselves are all highly autocorrelated over a 3-year gap, a
persistent selection or measurement structure recurring in both waves is at least as
parsimonious an explanation as a persistent economic mechanism, and the design has no way
to adjudicate between them. The manuscript's own Discussion section states this directly
("the same persistent selection or measurement structure could recur") — this review
independently reaches the same conclusion and regards the manuscript's hedge as accurate,
not performative.

## 5. 2019 moderator challenge

`coverage = max(credit_bureau_cov_pct, credit_registry_cov_pct)` for 2019, drawn from
`data/raw/wb_credit_information_by_country_year.csv`, which — based on its column set
(`depth_credit_info_0_8`, `credit_bureau_cov_pct`, `credit_registry_cov_pct`,
`legal_rights_0_12`) — corresponds to the World Bank Doing Business "Getting Credit" topic
indicators. Two points follow from this identification, offered with appropriate caution
since this review did not have live access to re-verify current World Bank documentation:

1. The Doing Business report series was discontinued by the World Bank in 2021 following an
   internal review that found data irregularities in a subset of country scores (publicly
   reported at the time). If any of the 93 sample economies' credit-information sub-indices
   were affected by that episode, the 2019 moderator value for those economies would carry
   unquantified measurement error beyond ordinary sampling/definitional noise. This review
   flags it as a provenance question worth a one-line disclosure or a targeted check against
   the World Bank's own corrigenda, not as a demonstrated flaw in this project's data.
2. Independent of the discontinuation episode, "coverage" as coded here is a **breadth**
   measure (share of adults covered by a bureau or registry), not depth, accessibility,
   legal usability, or actual lender use — a distinction the manuscript's Data section
   already states explicitly and correctly. This review's own check confirms the four
   available World Bank sub-indicators (depth, bureau coverage, registry coverage, legal
   rights) are conceptually and empirically distinct, and that only the coverage pair is
   used in the primary moderator (depth is relegated to a secondary specification, exactly
   as the manuscript states).

Because "coverage" and general financial/economic development are plausibly correlated
across countries, and no country-level income or financial-depth interaction term is
included, this review cannot rule out that the moderator is partly proxying broader
financial-system development rather than credit-information thinness specifically. The
manuscript already acknowledges a version of this ("Coverage, depth, accessibility... remain
separate constructs") but does not explicitly flag the income/financial-development
confound at the country level, which this review considers the more policy-relevant
omission.

## 6. Digital-payment and formal-borrowing measure challenges

`anydigpayment` and `fin22a` were not re-derived from the World Bank codebook text in this
review (no internet access was used); this review relies on the project's own construct
audit, `audit/STAGE_3A2_FINAL_CONSTRUCT_RECONCILIATION_2026-09-17.md`, which independently
documents (before this Stage 14 review existed) that: `anydigpayment` aggregates several
distinct payment channels (mobile money, cards, mobile-phone payments, bill/purchase
payments, remittances, and digital receipt of wages/transfers/pensions/agricultural
payments) under one 0/1 flag, and is "broadly aligned" but not proven component-identical
between 2021 and 2024. This supports the manuscript's own "qualified-comparable" language
and this review finds no basis to weaken that hedge further, but also no basis to consider
it resolved: a single aggregate flag conflating "received a government transfer digitally"
with "made a merchant payment via card" mixes payment-as-access with payment-as-behavior in
a way that could contribute non-trivial measurement heterogeneity to the coefficient,
independent of the 2021-2024 comparability question. `fin22a` is treated in this project's
own audit trail purely as "formal borrowing from a bank or other formal financial
institution," coded 1/2 (yes/no) with 3/4 (DK/refused) set to missing; this review did not
find, in the files available, an explicit statement of whether `fin22a` in the Global
Findex instrument aggregates multiple credit products (bank loan, credit union, MFI, credit
card) under one item or is a single clean question. This is flagged as an open,
unresolved verification item rather than a finding either way.

## 7. Account-access challenge

`audit/STAGE_3A2_FINAL_CONSTRUCT_RECONCILIATION_2026-09-17.md` documents that roughly 3% of
`account_fin`=1 respondents in the **2021** wave are constructed from payment/card-derived
evidence rather than the ordinary account-screening questions — i.e., `account_fin` and
`digital_payment` share a small amount of construction overlap specifically in 2021. This
creates a first-order collinearity/contamination risk for the Specification-B
(account-conditioning) sensitivity model in exactly the wave where the account coefficient
is *not* significant on the interaction (2021: acc_x_lowcov p=0.32) and the digital-payment
main effect roughly halves (0.0907→0.0419). `body_stage8.tex` treats `account_fin`
correctly as "selection/access sensitivity" and does not claim it identifies a mechanism —
this review finds the manuscript's restraint on this point appropriate, but recommends the
~3% construction-overlap fact be stated explicitly next to the account-sensitivity
paragraph rather than left implicit in an upstream Stage 3 document a reader of the paper
will not see.

## 8. Economic interpretation challenge

The manuscript separates "what the data show" (an observed association and interaction
sign), "what the theory predicted" (a substitution effect that did not materialize), and
"what the data do not identify" (lender information use, processing capacity, information
quality, causal substitution/complementarity, supply rationing, borrower selection) in its
Discussion and Limitations sections. This review read the manuscript end to end looking
specifically for slippage between these categories and found the text disciplined; see
`STAGE_14_CLAIM_LANGUAGE_REVIEW.md` for the line-by-line audit and the residual points that
should still be tightened.

## 9. Multiple-testing / specification-search challenge

This review did not find, in the files available, a documented history of alternative
93-economy definitions, alternative moderator definitions, or alternative payment variables
having been tried and discarded before the current specification was chosen — nor evidence
that they were not. The manuscript and Stage 12/13 record are explicit that the
specification was "developed during exploratory analysis" and is not confirmatory; this
review agrees that "exploratory, subsequently computationally reproduced" is the most
precise description available given the documented evidence, and that nothing in the
record supports upgrading the status to confirmatory or downgrading it to a demonstrated
p-hacking exercise. The correct answer is the one the manuscript already gives: exploratory,
not confirmatory, not p-hacked-and-proven, not registered.

## 10. Governance/provenance cross-check

Independent of the empirical review above, this reviewer confirms — by direct inspection of
`papers/study_05/PREREGISTRATION.md`, `research_council/hypotheses/active/H-000004.json`/
`H-000005.json` context, and `audit/STAGE_12_GOVERNANCE_AUDIT.md`/`STAGE_13...md` — that the
manuscript's current framing (exploratory, not pre-registered, H-000501 scope excludes this
design, retroactive registration explicitly rejected by the owner) is consistent with the
governance record as it stands. This review's own reading of `body_stage8.tex` did not find
any residual "pre-registered" or "registered prediction" language; that specific defect,
identified by Stage 12, appears to have been fixed by the time of this review (see
`STAGE_14_REVIEWER_INDEPENDENCE_NOTE.md`).
