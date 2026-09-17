# Gate 3A Closure — Raw-Data-Verified Harmonization Decision

Date: 2026-09-17  
Decision: **CONDITIONAL PASS**  
Gate 3B / regression / DiD / IV: **LOCKED**

## 1. 2021 year-field anomaly

The 2021 raw release contains 127,854 observations with `year=2021` and 16,033 with `year=2022`, across the same 139-economy release. Official World Bank catalogue metadata states that 16 economies were surveyed face-to-face in 2022 because of COVID-19 restrictions, while the observations remain part of the Global Findex 2021 release. The 16 economies in the raw file are AZE, BWA, COD, COM, ETH, GMB, GTM, LSO, MDG, MEX, MRT, NER, SWZ, TCD, VNM, and YEM.

Treatment recommendation: retain these observations as part of `wave=2021`, while preserving `year` as the interview/fieldwork timing field. The design must describe the extension as a Findex-wave comparison, not as a pure calendar-year 2021 panel. This resolves the anomaly for wave membership, but calendar-year analyses remain prohibited without a separate design.

## 2. Strict-core audit

| Component | 2017 | 2021 | 2024 | Gate verdict |
|---|---|---|---|---|
| Economy | Present; 144 economies | Present; 139 economies | Existing 97-economy analysis sample | PASS for set comparison; analysis sample not built |
| Wave | Must be assigned externally | Raw `year` includes 2021 and 2022 | Existing 2024 baseline | CONDITIONAL PASS |
| Survey weight | `wgt`, complete; mean ≈ 1 | `wgt`, complete; mean ≈ 1 | Existing baseline | PASS for within-wave use; no pooled weight |
| Formal borrowing | `fin22a`, codes 1–4, no physical missing | `fin22a`, codes 1–4, no physical missing | Existing `fin22a` baseline | PASS provisional, subject to final universe wording |
| Account ownership | `account_fin`, binary, no physical missing | `account_fin`, binary, no physical missing | Existing `account_fin` baseline | CONDITIONAL PASS; construction differs in detail |
| Sex | Complete binary field | Complete binary field | Existing baseline | PASS provisional |
| Age | 451 missing | 467 missing | Existing baseline | PASS with explicit complete-case rule |
| Education | 10 physical missing; codes 4/5 are invalid/special responses per codebook | No physical missing; codes 4/5 are invalid/special responses per codebook | Existing baseline | PASS with explicit invalid-response handling |
| Income quintile | Within-economy household income quintile, codes 1–5 | Same documented construct, codes 1–5 | Existing baseline | PASS as a cross-sectional rank, not income mobility |

## 3. Digital-payment decision

2017 has payment components but no directly observed `anydigpayment` construct; structural missingness varies by component and respondent universe. The reconstructed 2017 measure is therefore **approximately comparable**, not strict.

2021 has `anydigpayment` coded 0/1 with no physical missingness. The 2021–2024 common exposure remains **conditional** until the 2024 construction and universe are compared line-by-line against the 2021 codebook/metadata. Same-name continuity is insufficient evidence.

**Digital-payment option: OPTION 2** — 2017 reconstructed measure is approximate; 2021–2024 common measure is the candidate primary exposure.

## 4. Economy overlap

Compared with the existing 2024 analysis sample:

- 2017: 144 economies
- 2021 release: 139 economies
- 2017 ∩ 2021: 133
- 2021 ∩ 2024: 93
- 2017 ∩ 2024: 92
- three-way intersection: 90

This is an exact set audit only. No wave files were appended or merged.

## 5. Mechanism boundary

`fin20` is medical borrowing in 2017 and 2021, but mobile-loan application in 2024. It is therefore permanently classified as a 2024-only diagnostic. `fin21` is not admitted to pooled longitudinal mechanism analysis without a separate construct audit.

## 6. Closure decision

The raw files are now available and the essential file-level diagnostics are complete. A full PASS is not warranted because two named construct issues remain: full cross-wave `account_fin` construction reconciliation and strict 2021–2024 `anydigpayment` equivalence. Education and income quintile are sufficiently documented for the strict core, with explicit invalid-response and rank interpretations. The 2022 records are resolved as part of the official Findex 2021 wave, with interview timing retained separately.

**FINAL GATE 3A DECISION: CONDITIONAL PASS**

No regression, trend estimate, pooled treatment, institutional measure, DiD, or IV may be started from this artifact. The next permitted gate is Gate 3B only after these named closure items are resolved or explicitly accepted as limitations.
