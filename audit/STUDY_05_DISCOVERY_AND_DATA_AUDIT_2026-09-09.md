# Study 5 — Research Discovery + Data Audit

**By:** Claude · **Date:** 2026-09-09 · **Skills:** `research-discovery`, `data-audit`
**Status:** pre-registration draft. **No estimation run.** Hand to owner + Codex.

---

## PART A — RESEARCH DISCOVERY

### A1. The question

Among adults in **developing / emerging economies** surveyed in the 2024 Global Findex wave:

1. **Main:** Is making or receiving a digital payment (`anydigpayment`) associated with
   having borrowed from a **formal financial institution** in the past 12 months (`fin22a`),
   after adjusting for account ownership, demographics, and country fixed effects?
2. **Mechanism split (from Galilea et al.):** Is the association driven by **receiving**
   payments into an account (`receive_wages/transfers/pensions/agriculture == 1`) rather than
   **making** payments (`merchantpay_dig`, `pay_utilities`)? Receiving reveals income capacity
   to a lender; making does not.
3. **Heterogeneity (the contribution):** Is the association **larger in economies with weaker
   credit-information systems** (low depth-of-credit-information index / low credit-bureau
   coverage)? If digital transaction records substitute for missing formal credit histories,
   the payment–borrowing link should be strongest where credit registries are thin.
4. **Local hook:** Where does **Vietnam** sit in this distribution, and what does the
   cross-country pattern imply for Vietnamese financial-inclusion policy?

### A2. Prior literature and the gap

- **Galilea, Farazi & Mare (2026)** — *Firm Credit Constraints and Electronic Payments: A
  Global Analysis* (World Bank; reproducibility package `reproducibility.worldbank.org/catalog/430`;
  blog "When digital payments unlock access to credit"). **Firm level**, 101 economies, World
  Bank Enterprise Surveys. Firms that **receive** electronic payments are ~3 pp less likely to
  be fully credit-constrained; effect strongest for **small, young, low-productivity, unaudited
  firms and in economies with weaker credit infrastructure / lower financial development**.
- **Berg, Burg, Gombović & Puri (2020, RFS)** — a consumer "digital footprint" predicts
  default and complements credit-bureau data. Individual level, one German firm.
- **Demirgüç-Kunt, Klapper, Singer & Ansar (2022; and the 2025 Findex report)** — descriptive:
  account owners who receive digital payments also save and borrow more.
- **Gap:** the **individual-level, cross-country** version of Galilea et al. — does an adult's
  digital-payment activity track formal borrowing, and does the credit-information-infrastructure
  moderation hold at the household level? Web search (2026-09-09) did not find this paper.
  Novelty is **moderate**: a credible "individual-level analog of an established firm-level
  finding" framing, adequate for a student competition; **not** a strong stand-alone journal
  novelty claim.

### A3. Estimand (prespecified, descriptive)

Linear probability model on the pooled developing-economy sample:

```
formal_borrow_i = b1*digpay_i + b2*(digpay_i x weakCIS_c) + g*X_i + d_c + e_i
```

- `formal_borrow_i` = 1 if `fin22a == 1`, else 0 (2/3/4 -> 0; document DK/refused handling).
- `digpay_i` = `anydigpayment` (primary); robustness with the receive-only and make-only splits.
- `weakCIS_c` = country credit-information weakness (see Part B; specified as a z-score and as
  a below-median indicator).
- `X_i` = `account_fin` (crucial control — see A4), `female`, `age`, `age^2`, `educ` (3),
  `inc_q` (5), `urbanicity`, `internet_use`, `emp_in`.
- `d_c` = economy fixed effects (so b1 is identified **within** country); the interaction
  carries the cross-country moderation.
- Weights `wgt`; standard errors **clustered by economy**; report wild-cluster-bootstrap
  given ~100 clusters.
- **b1, b2 are associations, not effects.**

### A4. Threats (state loudly in any output)

1. **Single cross-section, 2024 wave only** — no temporal ordering. Cannot say payments precede
   borrowing.
2. **Mechanical endogeneity** — `anydigpayment` essentially requires an account; formal
   borrowing often runs through an account. Controlling for `account_fin` absorbs the crudest
   channel but not all of it. The receive-into-account split partly mitigates (a wage recipient
   need not be a borrower) but remains endogenous (formal-sector employment predicts both).
3. **Reverse causality** — taking a formal loan can trigger account opening and digital-payment
   use.
4. **Moderator measurement** — depth-of-credit-information index was frozen when Doing Business
   ended (~2019/2020); credit-bureau coverage continues in WDI but with gaps. A pre-2024
   moderator against a 2024 outcome is defensible (infrastructure is slow-moving) but must be
   disclosed.
5. **Self-reported survey data**, one wave, ~1,000 respondents/economy — country-level
   estimates are noisy; lean on the pooled within-country design, not country rankings.
6. **Selective module coverage** — see B3; the analysis is developing-economy by construction.

### A5. Honest ceiling

A well-executed, large-sample, clearly-written descriptive study with a real comparative
hypothesis and a literature anchor. **Competitive for a student competition** if the execution
and writing are strong and the Vietnam framing is sharp. **Not Q1** (cross-section,
endogeneity, moderate novelty). Do not oversell.

---

## PART B — DATA AUDIT

### B1. Primary file (verified)

| Field | Value |
|---|---|
| Path | `data/raw/data_micro_findex_2024_vietnam.xlsx` (misnamed — it is the **global** release) |
| SHA-256 | `ca307a0c3dfd54dc945a18fb03c58b014143bc21c90761f71fe304e6a2f90fce` (matches `research_council/data_audit/raw_data_hashes.json` and `S1-FINDEX-MICRO-2025-V02.json`) |
| Sheet | `findex_microdata_2025_labelled_` |
| Shape | 144,090 rows x 199 cols; **`year` = 2024 only** (single wave) |
| Unit | individual respondent age 15+ |
| Coverage | **140 economies**, per-economy n 500–4,020 (median 1,000); China 4,020, India 3,000; Vietnam ("Viet Nam" / VNM) = 1,000 |
| Weight | `wgt` (0.078–7.55); `wpid_random` respondent id; `pop_adult` country adult population |
| Region | `regionwb` (7 groups incl. "High income" = 46,167 rows) |
| Docs | `data/external/GlobalFindex2025_DDI.xml`, `GlobalFindex2025_Microdata_Codebook.pdf` (hashes in the S1 manifest) |
| Provenance | `VERIFIED_RECONSTRUCTED` — release identified from DDI/codebook; original download receipt not preserved (inherited limitation from Study 1) |

### B2. Key variables — definitions verbatim from the DDI

| Var | DDI label / question | Coding | Non-null |
|---|---|---|---|
| `fin22a` | "Borrowed from a formal bank or similar financial institution" — *"In the past 12 months, have you borrowed any money from a bank or a similar financial institution?"* | 1 Yes / 2 No / 3 DK / 4 Refused | 102,954 (yes 10,457) |
| `anydigpayment` | "Made or received a digital payment" | 1 Yes (0 in data = No) | 102,954 (yes 57,753) |
| `dig_account` | "Has a digitally enabled account" | 1 Yes / 0 No | 102,954 |
| `account_fin` | "Has an account at a financial institution" | 1 / 0 | 144,090 (yes 95,972) |
| `account_mob` | "Has a mobile money account" | 1 / 0 | 81,924 |
| `receive_wages` | "Received a wage payment" | 1 Into an account / 2 Cash only / 3 Other way / 4 Did not receive / 5 DK-ref | 91,901 |
| `receive_transfers` | "Received a government transfer payment" | same scale | 91,901 |
| `receive_pensions` / `receive_agriculture` | pension / agricultural payments | same scale | 91,901 |
| `merchantpay_dig` | "Made a digital merchant payment" | 1 / 0 | 102,954 |
| `fin20` | "Applied for a loan using a mobile phone" (past 12 months) | 1/2/3/4 | 102,954 — *candidate secondary outcome* |
| `fin24` | "Main source of emergency money in 30 days" (4 = a loan from a financial institution / employer / private lender) | 1–8 | 102,954 — *candidate secondary outcome* |
| `fin22b` | "Borrowed from friends or family" | 1/2/3/4 | 102,954 — *placebo / contrast outcome* |
| Controls | `female` (0/1), `age` (15–99), `educ` (1–3), `inc_q` (1–5), `urbanicity` (2 levels), `internet_use` (0/1), `emp_in` (0/1) | — | 140,070–144,090 (educ 143,502; inc_q 143,070) |

### B3. Coverage / missingness — the binding structural fact

`fin22a`, `anydigpayment`, `dig_account`, `borrowed`, `saved`, `merchantpay_dig` all have
**exactly 102,954 non-null (41,136 missing)**. The missing block is concentrated in
**high-income economies** (46,167 high-income rows; ~41k lack the borrowing/digital-payment
module — high-income Findex uses a reduced questionnaire). **Consequence:** the study is a
**developing / emerging-economy study of ~100–110 economies (~103k adults)** by construction.
This is the correct frame anyway (matches Galilea et al.; matches Vietnam's peer group).

`receive_*` variables have 91,901 non-null — a further ~11k drop for the receive-split
specifications. `account_mob` (81,924) is thin; keep it secondary.

### B4. External moderator — ACQUIRED 2026-09-09 (pending Codex verification)

**Acquired by Claude** via the **World Bank API v2, source=1 (Doing Business indicators;
database archived, API `lastupdated` 2021-08-18)**. Files + SHA-256 in
`data/STUDY_05_RAW_MANIFEST.json`; raw API JSON retained under `data/raw/wb_api_json/`.

| short name | WB indicator ID | scale |
|---|---|---|
| `depth_credit_info_0_8` | `IC.CRED.ACC.DPTH.CISI.XD.08.DB1519` | Depth of credit information index, 0-8 |
| `credit_bureau_cov_pct` | `IC.CRED.ACC.PRVT.CRD.ZS` | Private credit-bureau coverage, % adults |
| `credit_registry_cov_pct` | `IC.CRED.ACC.PUBL.CRD.REG.COVR.ZS` | Public credit-registry coverage, % adults |
| `legal_rights_0_12` | `IC.CRED.ACC.LGL.RGHT.XD.012.DB1519` | Strength of legal rights index, 0-12 |

- **Vintage:** uniformly the **2019** observation (Doing Business 2020 release). Pre-2024
  moderator vs 2024 outcome - defensible (credit infrastructure is slow-moving), disclosed as
  a limitation. Long series 2003-2019 also retained.
- **Vietnam 2019:** depth 8/8; bureau coverage 20.6%; registry coverage 59.4%; legal rights 8/12.

### B4-OLD. (superseded candidate list, kept for the record) — country-level credit-information moderator

**Not in Findex.** Must be acquired (public, small). Candidates for Codex to verify
(availability, economy coverage vs the ~110 in-sample, vintage, licence):

| Source | Indicator | Note |
|---|---|---|
| World Bank WDI / former Doing Business | **Depth of credit information index (0–8)**, `IC.CRD.INFO.XQ` | Frozen ~2019–2020 when Doing Business ended; widest historical coverage |
| World Bank WDI | **Credit bureau coverage (% adults)** `IC.CRD.PRVT.ZS`; **Credit registry coverage** `IC.CRD.PUBL.ZS` | Continues past 2020 with gaps |
| World Bank **B-READY 2024** | Financial-services pillar, credit-information sub-indicators | New; check economy coverage |
| Global Financial Development Database (GFDD) | private credit bureau / registry coverage series | cross-check |

Merge key: ISO3 (`economycode`) -> source country code. Expect near-complete match for the
~110 developing economies; a few small economies may drop. **Merge loss to be quantified in
the data audit once the file is acquired.**

### B5. Merge — DONE (feasibility confirmed 2026-09-09)

- Findex rows with `fin22a` non-null: **102,954 individuals across 98 economies** (regions:
  35 Sub-Saharan Africa, 17 ECA, 16 LAC, 10 MENA, 9 EAP, 5 South Asia, 6 higher-income).
- ISO3 join Findex `economycode` to WB `iso3`: **98 / 98 matched, 0 unmatched, 100% of
  individuals retained.**
- **Moderator variation among the 98 economies:**
  - `depth_credit_info_0_8`: 14 at 0; then 2/4/5/6; 61 of 98 at 7-8 (ceiling-compressed).
  - `credit_bureau_cov_pct`: min 0 / median 19.4 / max 100.
  - `credit_registry_cov_pct`: min 0 / median 2.0 / max 100.
  - **`any_coverage` = max(bureau, registry): min 0 / median 40.3 / max 100; 24 economies
    <10%, 38 <25%** -> best spread. **Proposed primary moderator** (`weakCIS_c` = its negative
    z-score, plus a below-median indicator); depth and legal-rights indices as robustness.
- Country controls to attach (WDI/GFDD): log GDP per capita, private-credit-to-GDP,
  account-ownership rate - to show the moderation is not merely "poorer country".

### B6. Data-audit verdict

**`FEASIBLE`** for a descriptive cross-country association study (98 economies, ~103k adults,
moderator merged 100%), with these **disclosed limitations**:
- developing / emerging-economy scope only (B3);
- single 2024 cross-section; digital-payment activity and formal borrowing are mechanically
  linked through account ownership (A4) - **descriptive, not causal**;
- moderator vintage 2019 vs outcome 2024 (B4);
- depth index ceiling-compressed - lead with the continuous coverage moderator.

**No preregistration or estimation until Codex verifies** the moderator (indicator IDs,
sample values, archived-source provenance, vintage decision) **and clears the design (Part A).**

---

## Next steps (owner decides)

1. Owner + Codex review this document.
2. If cleared: acquire + audit the moderator file -> register hypothesis + claim contract ->
   preregister the spec (`econometrics-design`) -> Claude estimates (UNVERIFIED) -> Codex
   reproduces (different run id) -> literature review -> manuscript -> convert to the UEH
   competition template.
3. Study 1 (`study_01_rebuild/`) stays frozen throughout.
