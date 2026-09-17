# Gate 3B — Institutional Construct & Measurement Audit

Date: 2026-09-17  
Scope: credit-information environment and its role in the digital-payment/formal-borrowing puzzle  
Decision: **CONDITIONAL PASS**  
Regression / pooled analysis / DiD / IV / manuscript rewrite: **LOCKED**

## 1. Construct definition

For this project, **credit-information environment** should not be treated as a single latent index by default. The economically relevant construct is a layered institutional environment affecting whether borrower information exists, what it contains, whether lenders can access it, and whether it can be used in underwriting:

1. **Coverage:** who appears in a public registry or private bureau.
2. **Depth/content:** what types and history of information are available.
3. **Accessibility:** whether borrowers and lenders can obtain reports or scores.
4. **Legal/technical usability:** whether data can legally and technically be shared and processed.
5. **Actual lender use:** whether information is incorporated into credit decisions.

The current paper directly observes only the first layer robustly, observes part of the second and legal layer through Doing Business indicators, and does not observe global actual lender use.

## 2. Institutional measurement map

| Theoretical dimension | Economic meaning | Available measure | What it does not establish | Status |
|---|---|---|---|---|
| Coverage | Breadth of recorded borrower information | Private-bureau and public-registry coverage | File quality, lender access, or use | Primary observable |
| Depth/content | Scope, history, positive/negative information, and accessibility rules | Doing Business depth index, 0–8 | Actual data quality or current lender behavior | Valuable secondary measure |
| Legal rights | Borrower/lender collateral and bankruptcy rights | Strength of legal-rights index, 0–12 | Credit-reporting usability or payment-data use | Separate institutional construct |
| Accessibility | Ability to obtain reports/scores and operational functioning | B-READY credit-reporting questionnaire | Broad 97-economy coverage or historical continuity | Validation/subsample layer |
| Positive reporting | Availability of repayment performance, not only defaults | Partly embedded in depth/B-READY questions | Complete global series in current workspace | Targeted additional coding |
| Alternative-data legality | Permission to use nontraditional/payment information | Policy/legal sources; no global merged microdata | Actual technical access or lender use | Exploratory/contextual |
| Open banking/data portability | Ability to share transaction data with consent | Policy/regulatory sources | Whether lenders actually use the data | Exploratory/contextual |
| Actual lender use | Information enters underwriting decisions | No adequate global public measure found | — | Unobserved |

The World Bank defines the depth index as rules affecting the scope, accessibility, and quality of credit information, with higher scores indicating more information available to facilitate lending decisions. This definition makes depth conceptually broader than coverage, but not equivalent to actual lender use. [World Bank DataBank glossary](https://databank.worldbank.org/metadataglossary/jobs/series/IC.CRD.INFO.XQ)

## 3. 2019 coverage validity

The current moderator is the maximum of private-bureau and public-registry coverage. The underlying coverage concepts are narrower than a general “quality of credit information” construct:

- private-bureau coverage counts individuals/firms listed with borrowing-history information, including certain lender-requested reports for people without recent borrowing history;
- public-registry coverage counts individuals/firms with current repayment history, unpaid debt, or credit outstanding.

[Private-bureau definition](https://databank.worldbank.org/metadataglossary/doing-business/series/IC.CRED.ACC.PRVT.CRD.ZS) and [public-registry definition](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/IC.CRED.PUBL.ZS)

The local institutional panel contains 3,604 country-year rows for 190 ISO3 codes from 2003–2019. Coverage variables have 3,078 non-missing observations; depth and legal-rights variables have 1,477 non-missing observations. In 2019 the panel has 212 coverage/depth/legal-rights records, but this is broader than the manuscript’s 97-economy analysis sample and must not be treated as a completed merge.

The maximum operator is defensible only as a measure of **whether either formal credit-reporting channel has broad reach**. It does not measure combined coverage, depth, accessibility, or lender use. It may also conceal institutional substitution between public and private systems.

**2019 moderator decision: KEEP WITH QUALIFICATION.** It should be called historical formal credit-reporting coverage, not credit-information quality, accessibility, or lender use.

## 4. Alternative measures

| Measure | Role | Decision |
|---|---|---|
| Depth index | Alternative/complementary operationalization of information content and reporting rules | Keep separate; do not combine with coverage |
| Legal-rights index | Different institutional construct concerning collateral/bankruptcy protections | Keep separate; not a credit-information substitute |
| Positive reporting | More direct quality/content dimension | Valuable if consistently coded; not currently a complete global series |
| Accessibility | Directly relevant to lender/borrower obtainability | Validation layer where B-READY coverage permits |
| Alternative-data legality/open banking | Legal/technical usability of payment data | Exploratory contextual layer; not actual lender use |

Statistical performance must not determine whether any measure is theoretically valid. An imprecise alternative proxy would indicate limited measurement or power, not disprove the coverage construct.

## 5. B-READY role

B-READY is scientifically promising because its questionnaire includes credit-reporting operation, accessibility, credit scores, and whether financial institutions review credit information in practice when deciding on loan applications. [B-READY questionnaire description](https://thedocs.worldbank.org/en/doc/783622a927811f39dc2d6af019910087-0540012024/original/B-READY-Description-of-Questionnaires.pdf)

Its appropriate roles are:

- validation of the institutional construct;
- descriptive institutional context;
- limited subsample comparison.

It should not replace 2019 coverage as the primary moderator for all 97 economies because the 2024 B-READY round has limited economy coverage and a changed methodology. It is not a full historical panel and does not automatically identify actual lender use.

## 6. Payment-data usability

The available evidence must distinguish three levels:

`legal permission` → `technical accessibility/data portability` → `actual lender use`

Legal or regulatory evidence can establish that alternative data or open banking is permitted. It cannot establish that consumers can technically authorize access, that lenders can retrieve usable records, or that payment records enter underwriting. Therefore, no current global source supports an actual payment-record-use measure for the planned design.

## 7. Link to the current puzzle

| Institutional dimension | Substitution prediction | Complementarity/access/processing prediction |
|---|---|---|
| Coverage | Thin conventional files increase marginal value of payment information | Thin formal systems may reduce the ability to connect, verify, or use payment signals |
| Depth/positive reporting | Greater conventional information may reduce incremental value of payment data | Richer information systems may make payment signals more useful through integration |
| Accessibility | Payment data can substitute when conventional reports are unavailable | Low access prevents either signal from reaching lenders |
| Legal/technical usability | Permitted alternative data can substitute for missing conventional records | Usability is a prerequisite for any complementarity or substitution |
| Actual lender use | Direct evidence would be needed to distinguish information value from non-use | Direct evidence would also distinguish lender processing from borrower selection |

None of these mechanisms is established by the current Findex interaction. The negative interaction is evidence of a robust conditional association, not proof of complementarity, access selection, processing incapacity, or a negative structural effect.

## 8. Account ownership implication

`account_fin` should be treated as an access/selection variable with possible mediator and collider implications, not as an automatically neutral control. This is especially important because the 2021 construction adds some payment/card-derived cases. Future specifications should treat “with account ownership” and “without account ownership” as distinct conceptual conditioning choices, disclose the risk of conditioning on part of the payment structure, and avoid mechanism interpretation from its coefficient.

## 9. Minimum measurement upgrade

| Layer | Classification | Reason |
|---|---|---|
| Coverage | ESSENTIAL | Core historical institutional-state measure already supporting the puzzle |
| Depth | VALUABLE | Tests whether breadth differs from information content |
| Accessibility | VALUABLE | Directly relevant to whether information can be obtained and used |
| Positive reporting | VALUABLE | Closer to usable repayment-history information |
| Legal usability | OPTIONAL/VALUABLE | Needed only for a legal/alternative-data extension |
| Open banking | OPTIONAL | Contextual unless tied to a documented institutional change |
| Actual lender use | ESSENTIAL only for a high-end mechanism claim; otherwise unavailable and not mandatory for specialist path | Distinguishes information value from non-use and supply constraints |

No composite index is justified at this stage. The primary measure should remain coverage; depth, accessibility, positive reporting, and legal usability should be reported as separate layers.

## 10. Defensible design options

| Design | Scientific question | Institutional requirement | Remaining limitation |
|---|---|---|---|
| 2024 cross-section | Does the conditional gradient appear in the current baseline? | 2019 historical coverage, qualified | Single cross-section; no mechanism identification |
| 2021–2024 repeated cross-section | Does the gradient recur across Findex waves? | Coverage plus qualified digital-payment measure | Not an individual panel; exposure scope differences |
| 2017 contextual + 2021–2024 primary | Is the pattern contextualized without forcing a common 2017 treatment? | Coverage panel; 2017 reconstructed payment only | 2017 exposure is approximate |
| Institutional panel | Does the association vary with historical institutional states? | Coverage panel; depth as separate secondary measure | No causal institutional shock; historical measures are imperfect |
| Mechanism extension | Is the gradient due to information value, access, processing, or supply? | Application/approval/lender-use data | No adequate global public dataset currently available |

The most defensible near-term path is **2017 contextual + 2021–2024 primary**, with coverage as the primary institutional measure and depth/accessibility as separate validation or heterogeneity layers.

## 11. Final Gate 3B decision

**CONDITIONAL PASS**

The construct is now sufficiently defined to support a controlled next-stage design: “credit-information environment” is a layered concept, while the current moderator measures only historical formal credit-reporting coverage. The remaining condition is that future empirical design must preserve the separation of coverage, depth, accessibility, legal usability, and actual lender use.

## 12. Unlocked and locked work

Unlocked: Gate 3C empirical-design specification, beginning with research question → estimand → variation → measurement → identification → model.

Locked: regression execution, pooled analytical-file construction, treatment-index creation, DiD, IV, causal/mechanism claims, and manuscript rewriting.
