# CODEX-S5-STAGE1-DATA-CHALLENGE-001

Date: 2026-09-09  
Build: `CODEX-S5-BUILD-20260909-001`  
Verdict: **PASS_STAGE_1_ESTIMATION_AUTHORIZED**

## DATA_CHALLENGE

### artifact_inventory

The build verified SHA-256 for the frozen Revision 2 contracts, hypothesis, raw manifest,
Global Findex workbook, 2019 Doing Business moderator snapshot, and both WDI downloads.
It wrote a new collision-protected directory containing `analysis_panel.csv`,
`drop_table.csv`, `country_controls_latest.csv`, and `panel_receipt.json`. No Study 1 file
was read as an empirical result or modified.

### variable_lineage

Every analysis variable is reconstructed from named raw fields in `VARIABLE_CONTRACT.md`.
In particular, DK/refused values are never converted to zero in `receive_dig`, `make_dig`,
or the three secondary outcomes. Revision 2 is enforced for `fin24`: code 4 is labelled
`emergency_loan_source`; codes 8, 9, and missing remain missing. Moderator z-scores use
one unweighted value per final economy with population standard deviation (`ddof=0`).

### coverage

The final primary frame contains **100,560 respondents in 97 economies**. The sequential
drop table begins with 102,644 valid `fin22a` responses in 98 module economies. Education
removes 399 rows; income quintile removes 998 and all of Lesotho; urbanicity removes 687.
The ISO3 moderator merge removes zero rows. Vietnam contributes 998 respondents.

M3 has 90,118 complete observations. Non-missing secondary outcome counts are 100,452
(`mobile_loan_app`), 97,540 (`emergency_loan_source`), and 100,428 (`informal_borrow`).

### quality_findings

`wpid_random` is unique. Primary variables are complete after the frozen filters. Each
economy's `w_equal` sums to one within floating-point tolerance (range 0.9999999999999999
to 1.0). Outcome and constructed binary variables remain within {0,1}. The moderator has
complete coverage and nonzero cross-economy variation.

### merge_audit

The Findex-to-Doing-Business merge is a validated many-to-one ISO3 join with 97/97 matches.
Both WDI controls cover 97/97 final economies under the preregistered latest-available
rule. GDP per capita is 2023 throughout. Private credit is not a common-vintage measure:
its latest years range from 2008 to 2023. That unequal vintage is retained in
`country_controls_latest.csv` and must be disclosed in M6.5.

### leakage_and_revision_risks

The 2019 moderator predates the 2024 survey but is not randomly assigned and may proxy for
development, institutions, or financial-system depth. M6.5 addresses only observed
country-level confounding. Economy fixed effects do not identify a country-level main
effect and do not make its interaction causal. Raw and Study 1-derived estimates were not
used to choose the Study 5 specification.

### unverified_semantics

No primary-variable semantic ambiguity remains. `any_cov=max(bureau,registry)` measures
coverage, not data quality, lender use, or the 2024 system. `emergency_loan_source` bundles
financial institutions, employers, and private lenders and can only be reported using that
neutral description. The WDI private-credit control has heterogeneous vintages.

### design_support

The data support the preregistered descriptive within-economy associations, cross-country
moderation tests, named robustness checks, and Vietnam positioning. They do not support
causal, policy-impact, temporal, firm-credit, or mechanism-identification claims.

### feasibility verdict

**PASS_STAGE_1_ESTIMATION_AUTHORIZED.** Stage 2 may estimate only the frozen specifications
from this immutable panel. Results remain `ESTIMATED_UNVERIFIED` until an independent run
reproduces them; a Stage 2 success is not manuscript eligibility.

## Immutable output hashes

| Artifact | SHA-256 |
|---|---|
| `analysis_panel.csv` | `ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9` |
| `drop_table.csv` | `70ba6321fee9e1c0d26ffc9f5bcc4f9fb3590c2942ccd1bccacd1bf78875e3a8` |
| `country_controls_latest.csv` | `5f17878b4e18c6c54e25bccc4dd9445e014444de178c47be79a6edf708f44d49` |
| build code | `fceceaa0b4173a3a620a8d6927de67e6d6bafaf68b477d5a3dfa73db4abf8741` |
