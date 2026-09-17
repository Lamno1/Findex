# Stage 18 -- Placebo Test (Informal Borrowing)

Date: 2026-09-17
Scope: ADDITIVE robustness for the 93-economy/2021-2024 line, third item on
the owner's journal-hardening list after Stage 17's items #1 (external-
validity reweighting) and #2 (macro-control interactions). Feasibility was
confirmed separately before this run: `fin22b` is fully usable in both raw
waves (2021: 143,887 non-missing of 143,887; 2024: 102,954 non-missing,
matching the module-administered primary sample exactly).

No existing file in `results/stage5_estimation/`, `results/stage17_external_validity/`,
or any number already in the manuscript's Results section (primary M2
estimates, pooled/triple interaction, LOO, Stage 17 items) was altered,
deleted, or re-estimated. Everything here is new, additive analysis in a
new location (`results/stage18_placebo/`) and a new manuscript subsection.

## Construction

`informal_borrow` is built exactly analogous to the frozen H-000500
construction (`code/study_05_crosscountry/build_stage1_codex.py`, line
~127: `binary(fin22b, {1}, {2})`): 1 if `fin22b==1`, 0 if `fin22b==2`,
missing (dropped) for DK/refused (3/4) or physical missing.

`results/stage4_build/analytical_dataset.csv` does not retain a
respondent-level ID, so it cannot be safely joined back to `fin22b` at the
row level. The row-level sample was instead reconstructed by replicating
`code/study_05_crosscountry/build_stage4_dataset.py`'s `load()` filter
(raw Findex row, restricted to the frozen 93-economy manifest) directly
from `data/acquisition/FINDEX_{2021,2024}/raw_microdata.csv`, in a new
script `code/study_05_crosscountry/stage18_placebo.py`.

### Validation before reading the placebo result

Before informal_borrow's own missingness was applied, the reconstructed
sample's `formal_borrow`-based complete-case $N$ and $G$ (using the
identical covariate-completeness criteria as the primary specification:
`formal_borrow`, `digital_payment`, `wgt`, `female_binary`, `age`,
`education`, `income_quintile` all non-missing) were checked against
`results/stage5_estimation/estimates.csv`'s `PRIMARY_M1_M2_2021`/`_2024`
rows:

| Wave | Reconstructed N | Expected N | Match | Reconstructed G | Expected G | Match |
|---|---|---|---|---|---|---|
| 2021 | 96,711 | 96,711 | yes | 93 | 93 | yes |
| 2024 | 97,847 | 97,847 | yes | 93 | 93 | yes |

Exact match confirms the row-level reconstruction is faithful. The script
raises immediately if this check fails (it did not).

`informal_borrow`'s own missingness (dropping `fin22b` DK/refused/missing)
was then applied on top, giving the placebo estimation sample: **96,535
respondents / 93 economies (2021)** and **97,723 respondents / 93 economies
(2024)** -- smaller than the primary sample, as expected, since this is a
genuinely separate complete-case criterion, exactly as in the frozen
H-000500 record's own informal-borrowing placebo.

## Model

Identical M2 specification, weighting (`w_equal`, economy-wave-normalised),
economy-clustered SE, and null-imposed cluster-score Rademacher wild-cluster
bootstrap (999 replications, `code/study_05_crosscountry/stage17_external_validity.py`'s
`wild_cluster_p` implementation, generalised here to accept an arbitrary
outcome column) as the primary `formal_borrow` model, with
`informal_borrow` as the outcome, estimated separately for 2021 and 2024.

## Results

| Wave | Term | Estimate (pp) | Clustered SE (pp) | Cluster $p$ | Wild-cluster $p$ | N | G |
|---|---|---|---|---|---|---|---|
| 2021 | digital\_payment | +9.71 | 0.68 | $1.1\times10^{-46}$ | 0.001 | 96,535 | 93 |
| 2021 | dig\_x\_lowcov | **+1.95** | 0.72 | 0.0065 | **0.009** | 96,535 | 93 |
| 2024 | digital\_payment | +9.50 | 0.63 | $1.0\times10^{-51}$ | 0.001 | 97,723 | 93 |
| 2024 | dig\_x\_lowcov | **+1.75** | 0.59 | 0.0031 | **0.006** | 97,723 | 93 |

For comparison, the primary formal-borrowing interaction is $-1.74$ pp
(2021, wild $p=0.002$) and $-1.61$ pp (2024, wild $p=0.020$).

## Verdict: the placebo does not pass

The coverage interaction on informal borrowing is **positive and
significant in both waves**, opposite in sign to the formal-borrowing
interaction. This is the same qualitative "failure" the frozen H-000500
record's own single-wave informal-borrowing placebo showed (there:
$+1.7365$ pp, BH-rejected) -- but this is the first time it has been
checked across two independent waves of a different design, and it
replicates with similar magnitude (+1.95 and +1.75 pp, versus H-000500's
+1.74 pp on the older 2024-only design) and precision in both.

**Reported plainly, not reconciled or forced into an explanation**: this
pattern is consistent with a reallocation of borrowing activity toward
informal sources where coverage is thinner, but this single check does not
establish that reading on its own (it does not observe the same
individuals borrowing from both sources, and cannot rule out a shared
measurement or selection process driving both outcomes in the same
direction for reasons unrelated to reallocation). What it does establish,
plainly: a genuine credit-information-substitution effect specific to
formal, information-screened lending should not also appear, with similar
strength and in both waves, for an informal borrowing channel that
involves no credit-information screening at all. This further weakens
(does not by itself refute) the substitution reading, on top of Stage 17's
findings.

## What changed in `body_stage8.tex`

1. New `\subsection{Placebo check: informal borrowing}` inserted after the
   Stage 17 "Additional robustness" subsection (specifically after
   `\input{tables/tab_stage8_robustness}`) and before `\section{Discussion}`,
   presenting the construction, validation check, and both waves' results
   in full, plus `\input{tables/tab_stage8_placebo}`.
2. Limitations: one new sentence added immediately after the existing
   Doing Business provenance sentence, reporting the placebo's failure
   with both waves' point estimates and wild-cluster $p$-values.

No other section was edited. No existing sentence was deleted or softened.

## Build verification

`main.pdf` rebuilt: **13 pages** (up from 12 after Stage 17's refinement),
zero undefined references, zero overfull-hbox warnings.

## Files added (none pre-existing touched)

- `code/study_05_crosscountry/stage18_placebo.py` (analysis)
- `code/study_05_crosscountry/tables/build_stage8_placebo_table.py` (table generator; does not modify `build_stage8_tables.py` or `build_stage8_robustness_table.py`)
- `results/stage18_placebo/informal_borrow_estimates.csv`, `validation_check.json`
- `papers/study_05/manuscript/tables/tab_stage8_placebo.tex`
- `papers/study_05/manuscript/body_stage8.tex` (edited, not replaced)
- `papers/study_05/manuscript/main.pdf` (rebuilt)

`body.tex`, `main.tex`, `references.bib`, `H-000500.json`, `H-000501.json`,
`build_tables.py`, `build_stage8_tables.py`, `build_stage8_robustness_table.py`,
`stage17_external_validity.py`, and every Stage 3-17 audit file are
untouched. Nothing committed to git.
