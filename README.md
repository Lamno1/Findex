# Digital Payments, Formal Borrowing, and the Firm–Individual Boundary — Study 5 replication package

This repository accompanies the manuscript *"Digital Payments, Formal Borrowing, and the
Firm–Individual Boundary: Evidence from Two Global Findex Waves"* (author: Nguyen Van
Thong, University of Economics Ho Chi Minh City). It contains all estimation code,
aggregated (economy- and coefficient-level) results, and audit/provenance records needed
to reproduce every number reported in the manuscript.

## What is, and is not, included

**Included:** estimation and data-construction code (`code/`), aggregated results —
regression coefficients, standard errors, p-values, hashes, receipts, leave-one-economy-out
tables, reweighting and placebo estimates (`results/`) — audit/provenance notes
(`audit/`), and the manuscript source (`manuscript_src/`, LaTeX + compiled PDF).

**Not included:** the underlying Global Findex and World Bank Doing Business microdata.
The World Bank Microdata Library's dataset-use terms do not permit third-party
redistribution of the raw survey microdata; this repository instead provides exact
provenance (official catalogue links, reference IDs, and SHA-256 hashes of the files used)
so the microdata can be re-downloaded directly from the World Bank and the analysis
rebuilt from scratch.

## Re-acquiring the source data

| Wave | Official catalogue | Reference ID |
|---|---|---|
| Findex 2017 | https://microdata.worldbank.org/catalog/3324 | `WLD_2017_FINDEX_v02_M` |
| Findex 2021 | https://microdata.worldbank.org/catalog/4607 | `WLD_2021_FINDEX_v03_M` |
| Findex 2024 (released as "Global Findex Database 2025") | https://microdata.worldbank.org/catalog/7860 | `WLD_2024_FINDEX_v02_M`, DOI [10.48529/bk9n-8r43](https://doi.org/10.48529/bk9n-8r43) |
| Doing Business "Getting Credit" (2019 archived snapshot) | World Bank Doing Business archive | see `code/study_05_crosscountry/*.py` for the exact indicator columns used |

After downloading, place the raw files under `data/acquisition/FINDEX_<wave>/` and
`data/raw/wb_credit_information_by_country_year.csv` (matching the paths referenced by the
scripts in `code/`), then re-run the pipeline below. Expected SHA-256 hashes for the
originally-used files are recorded throughout `results/*/receipt.json` and
`audit/*.md`; a mismatch means a different data vintage was downloaded and results may
not reproduce exactly.

## Reproduction pipeline (order matters)

1. `build_stage1_codex.py` / `build_stage4_dataset.py` — build the analytical panel from
   raw microdata (93 economies common to 2021 and 2024, 194,558 respondents).
2. `stage5_estimation_audit.py` — primary two-wave estimation (Table: primary interaction,
   pooled/triple-interaction contrast).
3. `stage5_leave_one_out.py` — leave-one-economy-out robustness (93 economies x 2 waves).
4. `stage17_external_validity.py` — inclusion-propensity reweighting and macro-control
   (GDP per capita, account-ownership rate) interaction checks.
5. `stage18_placebo.py` — informal-borrowing placebo check.
6. `db_integrity_sensitivity_twowave.py`, `db_integrity_sensitivity_placebo_twowave.py`,
   `db_integrity_sensitivity_macro_twowave.py` — sensitivity of the primary, placebo, and
   macro-control results to excluding China (DB2018) and Saudi Arabia (DB2020), the two
   economies the World Bank's December 2020 *Review of Data Irregularities in Doing
   Business* implicates for the *Getting Credit* indicator used as the 2019 coverage
   moderator.

Each script is self-contained, reads only from the paths documented in its own docstring,
and fails closed (raises rather than silently proceeding) if an expected input hash or row
count does not match what is recorded in this package's `results/` and `audit/` artifacts.

## Estimator and inference

Weighted least squares linear probability model with economy fixed effects, economy-level
clustering, and a null-imposed cluster-score (Rademacher) wild-cluster bootstrap (999
replications). See the manuscript's Empirical Strategy section for the full specification
and `code/study_05_crosscountry/stage5_estimation_audit.py` for the exact control-variable
list.

## Citation

If you use this code or build on this analysis, please cite the manuscript (see
`manuscript_src/main.tex` for the current author/title) and the underlying Global Findex
data releases:

- Demirgüç-Kunt, A., Klapper, L., Singer, D., and Ansar, S. (2022). *The Global Findex
  Database 2021: Financial Inclusion, Digital Payments, and Resilience in the Age of
  COVID-19.* World Bank, Washington, DC.
- Klapper, L., Singer, D., Starita, L., and Norris, A. (2025). *The Global Findex Database
  2025: Connectivity and Financial Inclusion in the Digital Economy.* World Bank,
  Washington, DC. https://doi.org/10.1596/978-1-4648-2204-9

## License

Code in `code/` is released under the MIT License (see `LICENSE`). The manuscript text and
figures remain © the author; contact the corresponding author for reuse permissions beyond
standard academic citation.
