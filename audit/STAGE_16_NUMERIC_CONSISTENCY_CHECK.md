# Stage 16 — Numeric Consistency Check (Part A)

Scope: every numeric claim in `body_stage8.tex` (the canonical manuscript per
`CANONICAL_MANUSCRIPT.md`), re-traced independently of Stage 15's own check, directly
against the immutable result files. This re-derives min/max/hash values from the CSVs and
JSON receipts on disk rather than trusting a prior stage's summary of them.

## A1 — Sample size / economy count claims

| Claim in text | Location | Source | Traced value | Match |
|---|---|---|---|---|
| "93 economies common to the 2021 and 2024 Global Findex waves" | Data §, abstract | `results/stage4_build/ANALYTICAL_DATASET_MANIFEST.json` (`primary_sample_economies: 93`) | 93 | MATCH |
| "194,558 respondents" | Data §, abstract, Limitations, provenance § | `ANALYTICAL_DATASET_MANIFEST.json` (`rows: 194558`); `results/stage5_estimation/run_receipt.json` (`rows: 194558`) | 194,558 | MATCH |
| N=96,711 (2021) / N=97,847 (2024) | Table 1, Results, provenance § | `run_receipt.json` `waves.2021=96711`, `waves.2024=97847`; `estimates.csv` `N` column, both PRIMARY rows | 96,711 / 97,847 (sum = 194,558) | MATCH |
| "97, not the raw release's 140" (2024 module-administered baseline) | Data § | `audit/STAGE_14_INDEPENDENT_ADVERSARIAL_REVIEW.md` §3 ("The 2024 Findex borrowing/digital-payment module was administered in 97 of the 140 raw 2024 economies"), `papers/study_05/PREREGISTRATION.md` §0 | 97 / 140 | MATCH |
| "133 economies... common to both raw releases," "40 excluded" | Data § | Stage 14 review §3 ("133 economies are common... 40 are excluded from the 93-economy frame") | 133, 40 | MATCH (Stage 14.1 states these figures were carried forward, not re-derived, from Stage 14; this audit did not re-run the raw-file cross-tab itself — flagged below as a residual verification gap, not a discrepancy) |
| "186 leave-one-economy-out signs" (provenance §) | provenance § | 93 (2021) + 93 (2024) = 186, `leave_one_economy_out.csv` (93 rows per `ROBUSTNESS_LOO_2021`/`2024` specification) | 186 | MATCH |

## A2 — Coefficient / p-value claims

Source: `results/stage5_estimation/estimates.csv`, `results/stage5_1_reconciliation/wild_cluster_bootstrap.csv`.

| Claim | estimates.csv value | Matches text? | wild_cluster_bootstrap.csv wild-p | Matches text? |
|---|---:|---|---:|---|
| 2021 interaction −1.74pp, wild p=0.002 | `dig_x_lowcov` PRIMARY_M1_M2_2021 = −0.017436 → −1.74pp | MATCH | 0.002 | MATCH |
| 2024 interaction −1.61pp, wild p=0.020 | `dig_x_lowcov` PRIMARY_M1_M2_2024 = −0.016085 → −1.61pp | MATCH | 0.02 | MATCH |
| Pooled interaction −1.98pp | `dig_x_lowcov` SECONDARY_POOLED = −0.019841 → −1.98pp | MATCH | 0.001 (not quoted in text; text only reports the triple-interaction wild-p, which is correct — the pooled-interaction wild-p is not asserted anywhere) | N/A |
| Triple interaction +0.58pp, wild p=0.305 | `dig_x_lowcov_x_wave` SECONDARY_POOLED = +0.005836 → +0.58pp | MATCH | 0.305 | MATCH |
| Pooled-implied 2021 gradient −1.98pp | = base term, same as pooled interaction above | MATCH | — | — |
| Pooled-implied 2024 gradient −1.40pp | −0.019841 + 0.005836 = −0.014005 → −1.40pp | MATCH (arithmetic re-verified) | — | — |
| Table 1 main effects 9.07 / 8.13 (pp) | `digital_payment` PRIMARY_M1_M2_2021 = 0.090725 → 9.07; 2024 = 0.081290 → 8.13 | MATCH | — | — |
| Table 1 clustered SEs (0.49) / (0.60) | `se_cluster` = 0.004932 → 0.49pp (2021); 0.005982 → 0.60pp (2024) | MATCH | — | — |
| Account-conditioning (SPECB): "slightly attenuates... in 2021" | SPECB dig_x_lowcov 2021 = −0.016329 vs. primary −0.017436 (less negative) | MATCH (attenuates) | — | — |
| Account-conditioning: "more negative... in 2024" | SPECB dig_x_lowcov 2024 = −0.021878 vs. primary −0.016085 (more negative) | MATCH | — | — |
| "digital-payment main effect roughly halves" under SPECB (only in Stage 14 doc, not asserted in body_stage8.tex) | 2021: 0.0907→0.0419 | N/A — not a body_stage8.tex claim, checked only for consistency; correct | — | — |

## A3 — Leave-one-economy-out ranges

Independently recomputed (not reused from Stage 12/14/15's stated figures) via a min/max scan
of `results/stage5_estimation/leave_one_economy_out.csv`:

```
ROBUSTNESS_LOO_2021: count=93, min=-0.019697, max=-0.015556  ->  [-1.97, -1.56] pp
ROBUSTNESS_LOO_2024: count=93, min=-0.018293, max=-0.012674  ->  [-1.83, -1.27] pp
```

Text states: "$[-1.97,-1.56]$ pp in 2021 and $[-1.83,-1.27]$ pp in 2024." **Exact match**, and
all 186 values are negative (confirmed by the min/max bounds both being negative in each
wave). This independently re-confirms Stage 15's check rather than assuming it still holds.

## A4 — Hashes

| Hash claim | Location | Traced source | Match |
|---|---|---|---|
| Analytical dataset SHA-256 `78938AFF518F3F3BC049A18E7B8CA5C1042996392B1ACDD6EAAB56FC555240C1` | provenance § (quoted twice, identically, in the Limitations-adjacent provenance section) | `results/stage4_build/SHA256.txt`, `ANALYTICAL_DATASET_MANIFEST.json` (`output_hashes.analytical_dataset_csv`), `results/stage5_estimation/run_receipt.json` (`dataset_sha256`) | MATCH across all three independent recordings; byte-for-byte identical string, verified length = 64 hex chars (valid SHA-256) |

## A5 — Disclosure numbers added at Stage 14.1

| Disclosure number | Text location | Source | Match |
|---|---|---|---|
| "24 of the 34 economies worldwide with 2019 coverage at or above 95% are excluded" | Data § | `audit/STAGE_14_INDEPENDENT_ADVERSARIAL_REVIEW.md` §3 ("24 of the 34 economies worldwide with near-universal coverage (≥95%) are excluded... vs. only 10 retained") | MATCH |
| IQR "11.7 to 60.7" in-sample vs. "1.2 to 92.6" excluded pool | Data § | Stage 14 review §3 (identical figures) | MATCH |
| "40 excluded" economies, named examples (Australia, Canada, France, Germany, Japan, Korea, Switzerland, UK, US) | Data § | Stage 14 review §3 full list (40 named economies; the manuscript's illustrative subset is a strict subset of that list) | MATCH — every named economy in the manuscript's illustrative list appears in Stage 14's full 40-economy list |
| "approximately 3%" `account_fin`=1 / `anydigpayment` construction overlap, 2021 only | Results § | `audit/STAGE_3A2_FINAL_CONSTRUCT_RECONCILIATION_2026-09-17.md` §2, as relayed by `STAGE_14_1_GOVERNANCE_EXTERNAL_VALIDITY_CLOSURE.md` Item 3 | MATCH (this audit did not re-open the underlying 2021 microdata to recompute the 3% figure directly; it traced to the two audit documents that state it identically — see residual gap below) |
| CHN (DB2018) / SAU (DB2020) confirmed-irregular, both `final_sample=1` in the 93-economy manifest | Data § | `audit/STAGE_14_1_DB_PROVENANCE_TRACE.md` §(c), which quotes `data/manifests/findex_2021_2024_primary_93.csv` rows `CHN,China,1,1,1,` and `SAU,Saudi Arabia,1,1,1,` | MATCH |
| `fin22a` exact question wording, single self-reported item | Data § | `STAGE_14_1_GOVERNANCE_EXTERNAL_VALIDITY_CLOSURE.md` Item 5, sourced to `data/external/GlobalFindex2025_DDI.xml` variable `V72` | MATCH (wording reproduced verbatim) |
| Bootstrap: "null-imposed, cluster-score Rademacher bootstrap... fixed bread matrix... not a full-refit Cameron–Gelbach–Miller wild-cluster bootstrap" | Empirical strategy § | `STAGE_14_INDEPENDENT_ADVERSARIAL_REVIEW.md` §2 ("Bootstrap" paragraph), `run_receipt.json` (`wild_cluster_bootstrap.method`) | MATCH |

## A6 — Table / figure consistency

- `tab_stage8_primary.tex` and `tab_stage8_pooled.tex` are confirmed, by direct inspection of
  `audit/STAGE_15_TABLE_AUTOMATION.md` and by re-reading the table files themselves, to be
  generated by `code/study_05_crosscountry/tables/build_stage8_tables.py` reading only
  `results/stage5_estimation/estimates.csv` and
  `results/stage5_1_reconciliation/wild_cluster_bootstrap.csv`. Every cell value in both
  tables was independently cross-checked against those two CSVs in A2 above (not merely
  re-trusted from Stage 15's own diff report) — all matched.
- `main.pdf` timestamp (2026-09-17 16:38:03) is later than `body_stage8.tex`
  (16:37:14) and both table files (16:38:02), confirming the PDF reflects the current text
  and tables, not a stale build.
- `main.log` confirms `main.pdf (9 pages, 254894 bytes)`, zero "undefined" reference/citation
  warnings, zero LaTeX errors. Two overfull-hbox warnings exist (26.8pt and 63.1pt, both in
  the auto-generated table Notes paragraphs listing source file paths) — a build-hygiene
  item, not a numeric or content defect; see `STAGE_16_FINAL_FORENSIC_AUDIT.md` Part D.4.
- Both `\ref{tab:stage8primary}` and `\ref{tab:stage8pooled}` resolve (labels defined in the
  respective table files; no "??" or undefined-reference warning in `main.log`).
- All four `\citep{}` keys in `body_stage8.tex` (`BergBurgGombovicPuri2020`,
  `DaltonPamukRamrattanUrasVanSoest2024`, `GalileaFaraziMare2026`, `Ghosh2026`) resolve to
  matching `\bibitem` entries in `main.bbl`; `main.bbl` contains exactly these four entries
  and no others, consistent with a clean bibliography build for the currently-compiled body.

## Residual verification gaps (not discrepancies)

Two Stage-14.1 disclosure numbers were traced to their originating audit documents but were
not independently re-derived from raw source files in this Stage 16 pass, consistent with
this stage's mandate (verify the current text against its stated sources; re-litigating
whether Stage 14's own from-scratch reconstruction was itself correct is Stage 14's job, not
Stage 16's):
1. The "133 common / 40 excluded / 24 of 34 ≥95%" sample-composition figures (Data §) were
   re-traced to `STAGE_14_INDEPENDENT_ADVERSARIAL_REVIEW.md`, which itself states these came
   from a direct cross-check of the raw acquisition files. This audit did not re-open the raw
   140/139-economy release files to re-run that cross-tab a third time.
2. The "~3%" `account_fin`/`anydigpayment` overlap figure was re-traced to
   `STAGE_3A2_FINAL_CONSTRUCT_RECONCILIATION_2026-09-17.md` via the Stage 14.1 closure note;
   this audit did not re-open the raw 2021 microdata codebook to recompute the percentage.

Neither gap constitutes a found discrepancy — both numbers are consistently repeated,
word-for-word/number-for-number, across every audit document that touches them, and neither
number was found to disagree with the manuscript text in any instance checked.

## Verdict for Part A

No numeric claim in `body_stage8.tex` was found to be stale, mistraced, or internally
contradictory. Every coefficient, standard error, p-value, sample count, hash, and
disclosure figure checked against its immutable source file matched exactly.
