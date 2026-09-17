# Stage 14.1 — Governance + External Validity Closure

Date: 2026-09-17
Scope: remediation of the six items the owner selected from Stage 14's blind adversarial
review (`audit/STAGE_14_INDEPENDENT_ADVERSARIAL_REVIEW.md`). This is a remediation pass, not
a re-audit: it uses information already established by Stage 14 and by this project's own
prior H-000500/H-000501 investigations, plus new provenance tracing for item 6.

No primary model was re-estimated. No data file was altered. No Stage 3-13 or Stage 14
artifact, Codex-authored file, `body.tex`, `main.tex`, `H-000500.json`, or `H-000501.json`
was modified. The only file changed is `papers/study_05/manuscript/body_stage8.tex`
(canonical per `CANONICAL_MANUSCRIPT.md`), followed by a `main.pdf` rebuild.

## Item 1 — Module-administration sample-selection disclosure

**Disclosure limitation, not empirical invalidation.** Stage 14 found that the 93-economy
frame is the intersection of (a) the 97 economies where the 2024 borrowing/digital-payment
module was administered and (b) the 139 economies in the 2021 raw release, and that the 40
economies excluded from the 93-economy frame despite having complete raw 2021+2024 data are
overwhelmingly high-income, near-universal-coverage economies. This review confirms Stage
14's own numbers were not independently re-derived here (no new cross-check against the raw
files was performed in this pass; Stage 14's figures — 40 excluded of 133 raw-common
economies, 24 of 34 worldwide ≥95%-coverage economies excluded, in-sample IQR 11.7-60.7 vs.
excluded-pool IQR 1.2-92.6 — are taken as given, consistent with this project's broader
practice of not re-deriving a quantity a prior independent stage already established without
cause to doubt it).

This does not change any coefficient, sample size, or classification. It changes what
population the paper's "boundary condition" / "transportability" language may honestly be
read to describe: module-administered, predominantly low-to-middle-coverage economies, not
economies in general.

**Manuscript changes** (`body_stage8.tex`):
- **Data and measurement**: the sample paragraph now states why the 2024 baseline is 97 (not
  140), that the 93-economy frame's exclusions are correlated with the moderator, names the
  40-economy exclusion, the "24 of 34 ≥95%-coverage economies excluded" fact, and the IQR
  compression figures.
- **Discussion**: a new paragraph immediately after the two-wave persistence discussion
  scopes the boundary-condition/transportability claim explicitly to module-administered
  economies with predominantly low-to-middle coverage.
- **Limitations**: a new sentence reinforces the sample-selection caveat and cross-references
  Data, so it is not the only place a reader encounters it.

**Verdict: LIMITATION.**

## Item 2 — Precise bootstrap naming

**Disclosure limitation.** Stage 14 (§2, "Bootstrap") and this project's own Stage 12 audit
both independently examined `stage5_1_reconciliation.py`'s `wild_cluster()` function and
found it implements a null-imposed, cluster-score Rademacher bootstrap with a fixed bread
matrix from the unrestricted fit (a one-step/score-bootstrap variant), not a full-refit
Cameron-Gelbach-Miller wild-cluster bootstrap. The generic phrase "wild-cluster bootstrap"
was not incorrect but elided this distinction.

**Manuscript changes**: Empirical strategy section now names the procedure precisely once,
immediately after the weighting/clustering description, and states explicitly that "wild-
cluster bootstrap" as used elsewhere in the paper refers to this one-step variant.

**Verdict: LIMITATION** (terminology precision gap; now remediated).

## Item 3 — `account_fin`/`anydigpayment` ~3% construction overlap (2021)

**Disclosure limitation.** `audit/STAGE_3A2_FINAL_CONSTRUCT_RECONCILIATION_2026-09-17.md` §2
documents, from the 2021 Global Findex microdata codebook, that approximately 3% of
`account_fin=1` respondents in the 2021 wave are constructed from payment/card-derived
evidence rather than the ordinary account-screening questions. This was previously stated
only in that upstream Stage 3 audit file, not in the manuscript itself, next to the
Specification-B (account-conditioning) result it bears on.

**Manuscript changes**: the account-sensitivity paragraph in Results now states the ~3%
overlap fact directly, framed as a 2021-specific collinearity risk distinct from the
selection-versus-mechanism caveat already present.

**Verdict: LIMITATION.**

## Item 4 — Leave-one-economy-out IQR mechanical narrowness

**Disclosure limitation (owner classified this "should do," not mandatory).** Stage 14
computed the LOO range mechanically: with `w_equal` weighting, dropping one of 93 equally
weighted economies removes only ≈1.08% of total estimation weight, so the LOO range is
mechanically narrow by construction, independent of whether the underlying association is
actually homogeneous across economies or economy subgroups.

**Manuscript changes**: the Results paragraph reporting the LOO ranges now adds this
mechanical explanation and states explicitly that sign preservation rules out a
dominant-influence economy, not cross-economy homogeneity.

**Verdict: LIMITATION.**

## Item 5 — `fin22a` product scope verification

**Verified directly against the source codebook** (not merely re-stated from a prior audit).
`data/external/GlobalFindex2025_DDI.xml`, variable `V72` (`fin22a`): label "Borrowed from a
formal bank or similar financial institution"; question text "In the past 12 months, have
you borrowed any money from a bank or a similar financial institution?" This is a single
self-reported yes/no item, not an analyst-constructed aggregate of multiple named credit
products the way `anydigpayment` aggregates multiple payment channels. It does leave
interpretive latitude to the respondent about what counts as "a similar financial
institution" (potentially including credit unions, microfinance institutions, or other
non-bank formal lenders, at the respondent's own judgment), which is a real but different
kind of heterogeneity than a constructed multi-item aggregate.

**Manuscript changes**: the outcome-variable description in Data and measurement now quotes
the exact question wording and states the single-item nature and the "or similar financial
institution" interpretive latitude explicitly, replacing the previous generic description.

**Verdict: PASS** (claim in the codebook verified directly; the only residual caveat —
respondent interpretive latitude in "similar financial institution" — is now disclosed,
not a coding error).

## Item 6 — Doing Business / "Getting Credit" provenance

See `STAGE_14_1_DB_PROVENANCE_TRACE.md` for the full a-e trace. Summary:

- (a)/(b) **Resolved.** The 93-economy/2021-2024 pipeline's 2019 coverage moderator is
  sourced from `data/raw/wb_credit_information_by_country_year.csv`
  (SHA-256 `2D7C9A27EFB59FF7BBCB894F3C0ECB51782DD8B1076C347868AAE047FE3D6288`), filtered to
  `year=2019`, taking `max(credit_bureau_cov_pct, credit_registry_cov_pct)` — this is the
  **exact same file, byte-for-byte**, already used and investigated for the frozen
  H-000500/H-000501 single-wave design (same SHA-256 recorded in
  `data/STUDY_05_RAW_MANIFEST.json`, acquired 2026-09-09, described there as "Doing Business
  2020 release"). Nothing was freshly re-acquired for Stage 3-11; this pipeline reuses the
  existing shared file.
- (c) **Resolved.** CHN and SAU — the two economies the World Bank's prior review is recorded
  (in this project's own `audit/CODEX_S5_DB_INTEGRITY_SENSITIVITY.md` /
  `audit/CLAUDE_S5_DB_INTEGRITY_REPRODUCTION.md`, produced for H-000500/H-000501) as having
  confirmed irregular Getting Credit scores (China DB2018, Saudi Arabia DB2020) — are both
  present in the 93-economy manifest (`final_sample=1` for both). No evidence was found, in
  the files available, of the review having flagged additional economies beyond these two.
- (d) **`PROVENANCE_UNCERTAINTY`, honestly unresolved.** Whether the archived 2019 values for
  CHN/SAU in this file are pre- or post-review figures cannot be established from the files
  available to this project. The file is recorded as "Doing Business 2020 release" with an
  acquisition date of 2026-09-09; the World Bank's review findings were reported around
  December 2020 and the report series was fully discontinued in September 2021, but no
  corrigendum file, revision date, or version marker is present in the acquired data to
  determine which side of any correction this snapshot falls on. This is the same open
  question already carried, in the same words, by the H-000500/H-000501 manuscript's own
  Doing Business paragraph — Stage 14.1 does not resolve it, and does not claim to.

**Verdict: LIMITATION** (data reused as-is with a disclosed, unresolved provenance question;
no evidence found of actual corruption or of the specific values being wrong — this is
carried forward, not newly discovered, and is not grounds for re-estimation).

**Manuscript changes**: Data and measurement now states the Doing Business provenance, names
CHN and SAU as the two confirmed-irregular economies present in-sample, and explicitly
labels the pre/post-review question as unresolved. Limitations cross-references it.

## Disclosure vs. invalidation — explicit summary

| Item | Disclosure limitation | Empirical invalidation |
|---|---|---|
| 1. Module-administration selection | Yes — scope of external-validity claim | No — coefficients, signs, and Stage 12/14 reproductions are unaffected |
| 2. Bootstrap naming | Yes — terminology precision | No — Stage 12 and Stage 14 both independently confirm the mechanics are statistically sound |
| 3. account_fin/anydigpayment overlap | Yes — collinearity risk for one 2021 sensitivity spec | No — the primary specification does not condition on account_fin |
| 4. LOO IQR narrowness | Yes — interpretation of what "robustness" the LOO check licenses | No — the LOO check still validly rules out single-economy influence |
| 5. fin22a scope | N/A — verified PASS, only interpretive latitude disclosed | No |
| 6. Doing Business provenance | Yes — unresolved data-vintage question for 2 of 93 economies | No demonstrated error found; disclosed as uncertainty, not correction |

## What would have crossed the line into re-estimation (and did not)

None of the six items produced evidence that the current data, moderator, or outcome
construction is built wrong. All six are either (a) scope/disclosure gaps in what the
manuscript said about correctly-computed quantities, or (b) an honestly-labeled provenance
question this project cannot resolve from available files. Per the owner's explicit rule,
no primary model was re-estimated.
