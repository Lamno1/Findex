# CODEX-S5-STAGE0-001 — Verification, design and novelty gate

**Study:** H-000500 / EXP-S5-001  
**Date:** 2026-09-09  
**Reviewer:** Codex  
**Stage:** 0 only — no outcome model was estimated  
**Verdict:** **PROCEED_WITH_CHANGES**

Study 5 is feasible as a descriptive competition paper, but the frozen contracts contain
sample, estimand and inference inconsistencies that must be revised before Stage 1. This is
not authorization to estimate the current preregistration unchanged.

## 1. Artifact inventory and provenance

| Artifact | Verification |
|---|---|
| Global Findex 2025 microdata workbook | SHA-256 matches `ca307a0c…f90fce`; one labelled sheet; observed shape 144,090 × 199; 140 economies; year is uniformly 2024; VNM has 1,000 rows. The filename says `vietnam` but the contents are global. Provenance remains `VERIFIED_RECONSTRUCTED`, not original-download verified. |
| Findex DDI and codebook | Present. DDI confirms the variable labels/codes tested below. |
| Four raw World Bank API JSON responses | All four hashes match the manifest; each response records `sourceid=1`, `lastupdated=2021-08-18`, and 3,621 observations. |
| Credit-information long CSV | Hash matches `2d7c9a27…d6288`; 3,604 data rows recorded by the manifest. |
| Credit-information snapshot CSV | Hash matches `ef0c67f9…bd06c`; 190 rows; all four selected observations are dated 2019. |

The live World Bank API independently returned Vietnam bureau coverage of 20.6 for 2019,
matching the archived file. Doing Business 2020 economy profiles were spot-checked for eight
contrasting economies: Vietnam, Afghanistan, Kenya, Georgia, China/Beijing, South Africa,
Saudi Arabia and Panama. The reported depth, legal-rights and bureau/registry coverage values
match the snapshot for those cases, including zero-depth Afghanistan and 100%-coverage
Georgia and China.

**Vintage decision:** accept the 2019 Doing Business measures as preregistered historical
moderators, provided every output calls them “2019 credit-information coverage/strength” and
does not imply they measure the 2024 system contemporaneously. B-READY 2024 is not a suitable
replacement: it uses a changed framework and covers only 50 economies. It may be discussed,
but should not be introduced as a robustness moderator without a separate coverage and
construct-comparability audit.

## 2. Variable lineage and semantics

| Analysis construct | Raw lineage | Stage-0 finding |
|---|---|---|
| `formal_borrow` | Findex `fin22a` | DDI confirms 1=yes, 2=no, 3=DK, 4=refused. There are 102,644 valid 1/2 responses, not 102,954; 310 DK/refused rows must be dropped. |
| `anydigpayment` | Findex composite | DDI confirms binary 0/1 and the same 102,954-row module universe. |
| `account_fin` | Findex composite | Complete 0/1 variable. It is an essential conditioning variable but does not remove reverse causality or common formal-finance engagement. |
| `female_d` | `female` | Confirmed: 1=female, 2=male. |
| `urban_d` | `urbanicity` | Confirmed: 1=rural, 2=urban. |
| `make_dig` | `merchantpay_dig`, `pay_utilities` | DDI confirms `pay_utilities=1` means paid from an account; values 2–4 are non-digital/no payment and 5 is DK/refused. The frozen construction must treat value 5 as unknown, not automatically zero. If one component is known, define from the known component; if both are unknown/missing, set missing. Record an explicit truth table. |
| `receive_dig` | four `receive_*` variables | The same missing/unknown logic must be explicit. A response of DK/refused must not silently become zero when all observed components are DK/refused. |
| `weakCIS_z` | maximum of 2019 bureau and registry coverage | Construction is reproducible and has useful spread. It measures coverage, not the quality or actual lender use of credit reports; rename prose accordingly. |

## 3. Coverage and deterministic sample audit

The contract's anticipated “98 economies / 95k–100k adults” is only partly correct:

1. `fin22a in {1,2}` leaves **102,644 adults in 98 economies**.
2. Applying the frozen complete-case controls sequentially leaves **96,925 adults in 96
   economies**.
3. Lesotho exits because `inc_q` is entirely missing; China exits because `emp_in` is
   entirely missing.
4. Six retained module economies are labelled `High income` by `regionwb`: Croatia, Poland,
   Romania, Oman, Saudi Arabia and Panama. Therefore the current primary sample is not
   literally “developing and emerging economies.”
5. After complete-case filtering, moderator spread remains adequate: `any_cov` 0–100,
   median 40.3; 24 economies below 10%; 37 below 25%; 14 economies have depth zero and 60
   have depth 7–8.

### Required population revision

Choose and freeze one of these before Stage 1:

- **Recommended:** define the primary population as “economies administered the Findex
  borrowing/digital-payment module,” retain the six high-income economies, and change all
  developing/emerging claims accordingly. Report the 96-economy complete-case primary
  sample and make exclusion of the six high-income economies a robustness check.
- Alternatively, exclude the six high-income economies in the primary build and redefine
  the target as non-high-income module economies. This will reduce the complete-case sample
  to roughly 90 economies and requires all z-scores to be recomputed on that set.

The current combination—retaining the six economies while claiming a developing/emerging
population—is rejected.

## 4. Merge audit

- The 98 outcome-module economies match the moderator snapshot by ISO3 with 0 unmatched
  rows before complete-case filtering.
- `economycode` is a valid three-character join key in the observed workbook; the moderator
  snapshot has one row per ISO3.
- The final analysis panel must record both structural country exits and respondent-level
  missingness. A single aggregate “complete cases” row is insufficient.
- Snapshot country labels such as Beijing, Delhi and Rio de Janeiro reflect Doing Business's
  reference-city convention; join by ISO3, never by these labels.

## 5. Leakage and revision risks

- The moderator precedes the 2024 outcome, so there is no look-ahead leakage. The five-year
  mismatch instead creates measurement drift and possible moderator misclassification.
- `internet_use` is plausibly a precursor, co-determined digital-capability measure, or part
  of the pathway represented by payment use. In a non-causal association model there is no
  uniquely “correct” adjustment set, but treating it as mandatory changes the estimand.
  **Revision required:** omit `internet_use` from the primary adjustment set and add it in a
  named robustness specification, or explicitly define the primary estimand as conditional
  on current internet use. The first option is recommended.
- `account_fin` adjustment is necessary to distinguish payment use from basic bank-account
  access, but it may also condition on a common consequence or mediator. The account-holder
  restriction is therefore an essential sensitivity analysis, not a cure for endogeneity.
- No temporal ordering exists between payment use and borrowing. Formal borrowing can itself
  induce account opening and digital activity. No mechanism or causal language is permitted.

## 6. Weighting and estimand audit — blocking correction

The registered formulas do not implement their stated estimands:

- `w1 = wgt / mean_c(wgt)` gives each economy total weight approximately `n_c`, not equal
  economy weight. With sample sizes ranging from roughly 500 to several thousand, economies
  do not contribute equally.
- The proposed `w2 = w1 * pop_adult_c / sum_c(n_c)` gives economy total weight proportional
  to `n_c × pop_adult_c`, not population alone.

**Required revision:**

```text
w_equal_i = wgt_i / sum_{j in c}(wgt_j)
w_population_i = w_equal_i * pop_adult_c
w_unweighted_i = 1
```

Scaling by a global constant is allowed. Name `w_equal` as the primary weight only if the
estimand remains the average economy-specific association. If the intended estimand is the
average sampled adult, register a different weighting rule and wording explicitly.

## 7. Design support and inference

- Economy fixed effects appropriately absorb country-level moderator main effects. The
  interaction estimates whether the within-economy payment–borrowing slope varies with the
  2019 moderator; it does not identify the effect of either variable.
- `account_fin × weakCIS_z` is a sensible safeguard against attributing heterogeneous account
  ownership slopes to digital payment use. It does not solve omitted heterogeneity.
- Clustered inference with approximately 90–96 economies is reasonable; the preregistered
  wild-cluster bootstrap is a useful check.
- **Delete two-way clustering by economy and region from confirmatory robustness.** Economies
  are nested within only seven regions, making the second clustering dimension too small and
  the two-way construction uninformative/unreliable. Region leave-out analysis is more
  transparent and should remain adversarial sensitivity analysis.
- “Within-R2” must be precisely defined for weighted LPM with absorbed effects and generated
  consistently across estimators.
- Logit/probit with economy fixed effects and average marginal effects require a declared
  implementation and convergence/separation policy before execution.
- M2c needs a preregistered joint-test definition and a rule for countries where bureau and
  registry coverage are both zero.
- Multiple-testing correction must specify one method now; “Romano-Wolf or BH” is not frozen.
  Recommended: Romano–Wolf if the implementation is independently tested, otherwise BH with
  the exact family enumerated.

## 8. Novelty check

The exact individual-level specification—Global Findex microdata, formal borrowing outcome,
digital-payment exposure, and moderation by national credit-information coverage—was not
located in the Stage-0 search. However, novelty is **limited/moderate**, not established:

- Galilea, Farazi and Mare (2026) already test the closely analogous firm-level moderation
  across 101 economies.
- The Global Findex reports already document overlap among account use, digital payments and
  borrowing.
- Bazarbash and Beaton (2020) relate cross-country fintech credit to financial development
  and information infrastructure, though with provider-level marketplace-lending data.
- Adjacent 2024–2026 studies already use Global Findex for digital-payment adoption and broad
  formal-borrowing/financial-inclusion outcomes.

Permitted positioning: **an individual-level descriptive analogue and external-population
check of an established firm-level pattern.** Prohibited: “first,” “novel,” “fills a gap,” or
claims that the interaction identifies a digital-footprint mechanism.

## 9. Contract revisions required before Stage 1

1. Correct the sample claim and expected final count (98 module economies before controls;
   96 under the current complete-case rule).
2. Resolve the six high-income economies and align the target-population language.
3. Correct `w1` and `w2` so they implement the stated estimands.
4. Freeze an explicit `make_dig`/`receive_dig` unknown-value truth table.
5. Resolve `internet_use` placement before seeing estimates.
6. Remove confirmatory two-way economy+region clustering.
7. Choose one multiplicity procedure and define its exact hypothesis family.
8. Specify fixed-effect logit/probit implementation, failure policy, and AME calculation.
9. Define the M2c joint test and weighted/absorbed `within-R2` calculation.
10. Change all prose from current “credit-information systems” to the measured construct:
    **2019 bureau/registry coverage**, with depth/legal rights as distinct robustness proxies.

After Claude records these as a dated pre-estimation contract revision—or the owner assigns
that revision to Codex—the revised documents should be hash-frozen. Only then may Stage 1
begin.

## 10. Stage-0 decision

**PROCEED_WITH_CHANGES.** The raw data and moderator are real, internally coherent and
linkable. The descriptive study is feasible and potentially competitive for the UEH student
competition. The current frozen preregistration is not executable as written because its
population count, target-population label, weighting formulas and several inference choices
conflict with the observed data or their stated estimands. No empirical claim is supported
and no outcome regression has been run.

## Public sources used in verification

- Global Findex 2025 catalog: https://microdata.worldbank.org/catalog/7860
- World Bank Doing Business indicator glossary: https://databank.worldbank.org/metadataglossary/doing-business/series/IC.CRED.ACC.DPTH.CISI.XD.08.DB1519
- Doing Business 2020 reports and economy profiles: https://archive.doingbusiness.org/en/reports/global-reports/doing-business-reports
- B-READY reports and coverage: https://www.worldbank.org/en/businessready/reports
- Galilea, Farazi and Mare context: https://blogs.worldbank.org/en/allaboutfinance/when-digital-payments-unlock-access-to-credit--new-evidence-from
- Bazarbash and Beaton (2020): https://www.imf.org/en/Publications/WP/Issues/2020/08/07/Filling-the-Gap-Digital-Credit-and-Financial-Inclusion-49638
