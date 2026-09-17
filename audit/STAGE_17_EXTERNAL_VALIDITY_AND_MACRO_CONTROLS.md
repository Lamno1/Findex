# Stage 17 — External-Validity Reweighting + Macro-Control Interactions

Date: 2026-09-17
Scope: ADDITIVE robustness analysis for the 93-economy/2021-2024 line, directed
by the owner after Stage 16's READY verdict, targeting journal submission
(JFSR / World Development / Financial Innovation per
`audit/STAGE_11_JOURNAL_FIT_MATRIX.md`). This is not remediation and does not
change the manuscript's existing exploratory/observational framing (Stage
13/14.1) — it adds new diagnostic evidence under that same framing.

No existing file in `results/stage5_estimation/`, `results/stage5_1_reconciliation/`,
or any number already in the manuscript's Results section (primary M2
estimates, pooled/triple interaction, LOO) was altered, deleted, or
re-estimated. Everything here is new, additive analysis in a new location
(`results/stage17_external_validity/`) and a new manuscript subsection.

## Methodology note on the item-2 adaptation (read before the numbers)

The directive asked for `lowcov_z × lgdppc` and `lowcov_z × acc_rate` as new
M2 regressors. **This is not estimable as specified.** M2 includes
`C(economycode)` fixed effects; `lowcov_z`, `lgdppc`, and (within a
single-wave regression) `acc_rate` are all constant within an economy. Any
covariate or interaction of covariates that is constant within economy is
perfectly collinear with the economy dummies and cannot be identified
alongside them (it is either dropped by the regression software for exact
collinearity, or the design matrix is rank-deficient). This is not a
judgment call the analysis got to skip — it is a linear-algebra fact of the
fixed-effects specification already frozen for the primary model.

**Adaptation (disclosed, not silently substituted):** interact
`digital_payment` — an individual-level variable that varies within economy,
so it is NOT absorbed by the fixed effects — with `lgdppc_z` and
`acc_rate_z` instead, using the exact same construction pattern already used
for the primary term (`dig_x_lowcov = digital_payment × lowcov_z`). This
answers the substantive question the directive posed ("does the interaction
survive once the moderator's association with general economic/financial
development is netted out") in the only form the fixed-effects specification
can actually estimate.

## Item 1 — External-validity reweighting

### Target frame construction

- Economies in raw `data/acquisition/FINDEX_2021/raw_microdata.csv`: 139.
- Economies in raw `data/acquisition/FINDEX_2024/raw_microdata.csv`: 140.
- Intersection (present in both raw releases): **133** — confirms Stage 14's
  approximate "~40 excluded" as exactly 40 before covariate-missingness
  handling.
- `data/manifests/findex_2021_2024_primary_93.csv` `final_sample == 1`: 93
  (verified — the manifest itself only lists the 93 included economies, with
  no machine-readable exclusion-reason column; the exclusion rationale lives
  in prose in `body_stage8.tex`'s Data section, not in this file).
- Excluded from 93 but present in both raw releases: **40**
  (`AUS, AUT, BEL, CAN, CHE, CHL, CYP, CZE, DEU, DNK, ESP, EST, FIN, FRA, GBR,
  GRC, HKG, HUN, IRL, ISL, ISR, ITA, JPN, KOR, LSO, LTU, LVA, MLT, NLD, NOR,
  NZL, PRT, RUS, SGP, SVK, SVN, SWE, TWN, URY, USA`) — overwhelmingly
  high-income/OECD, consistent with Stage 14's characterization, with a
  handful of exceptions (LSO, RUS, TWN).

### Covariates and missingness

- 2019 coverage: `data/raw/wb_credit_information_by_country_year.csv`, year
  2019, `max(credit_bureau_cov_pct, credit_registry_cov_pct)` — same file and
  construction `results/stage5_estimation/estimates.csv` already uses.
- Log GDP per capita: `data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json` (WDI
  indicator `NY.GDP.PCAP.CD`) — **already acquired with full provenance for
  H-000501; reused unmodified, no new acquisition was needed.**
- Region (`regionwb`) and log adult population: taken from the 2024 raw
  Findex release (both are economy-level static attributes, present
  identically in both waves for the economies checked).
- Only **TWN** is missing both coverage and GDP per capita (same finding as
  the frozen H-000501 Q5 precedent, for the same reason: Taiwan is absent
  from the World Bank series used). Dropped from the frame with the drop
  recorded, per the same rule H-000501 used. No other economy has any
  missingness in this covariate set — final frame **N = 132** (93 included,
  39 excluded).

### Inclusion logit and overlap

- Formula: `included ~ coverage + lgdppc + C(region, Treatment(reference='Sub-Saharan Africa (excluding high income)')) + log_pop_adult`.
- $c$-statistic: **0.982** (5-fold CV mean available in `results/stage17_external_validity/inclusion_logit.json`) — near-identical discrimination to H-000501 Q5's own inclusion logit (0.982 there too, on a different frame), suggesting module-administration selection is comparably predictable from economy-level development covariates in both exercises.
- Included propensity range: [0.142, 1.000]; excluded range: [0.019, 0.996]; common support: [0.142, 0.996].
- **Economies outside common support: 80 of 132.** This is a severe overlap failure — far above the 10-economy threshold used for the transportability classification.
- Max IPW weight: 7.03 before trim, 6.44 after 1st/99th trim (well-behaved, below the 10 threshold).
- Kish effective sample size: 60.9 of 93 included economies (~65% retained).

### Reweighted estimates vs. primary

| Wave | Primary (pp) | Reweighted (pp) | Relative change | Wild-cluster $p$ |
|---|---|---|---|---|
| 2021 | −1.74 | −1.77 | 1.3% | 0.002 |
| 2024 | −1.61 | −1.23 | 23.3% | 0.043 |

Both waves keep the same sign and stay within the ±50% stability band on the
point estimate alone.

### Classification: `not_transportable`

Per the same three-way rule the frozen H-000501 Q5 record used: common
support fails first (80 > 10 economies outside support), which forces
`not_transportable` **regardless of** the reweighted point estimates'
own apparent stability. This is not a contradiction — the classification
answers "can we credibly claim this generalizes to the excluded population,"
not "did the point estimate move a lot." The honest reading is: the excluded
economies are different enough from the included ones that reweighting
cannot manufacture credible external validity, even though the estimates
computed under reweighting happen to still look similar for 2021 and only
moderately smaller for 2024.

Notably, this is the **same qualitative outcome** the frozen H-000501 Q5
check reached (also `not_transportable`, with a comparable outside-support
count of 81 on a different, though related, target frame) — this
consistency across two independent module-selection exercises on
overlapping but not identical economy pools is itself evidence that the
module-administration restriction is a real, structural limit on this
line of work's external validity, not an artifact of one particular
target-frame definition.

## Item 2 — Macro-control interactions

Adding `digital_payment × lgdppc_z` and `digital_payment × acc_rate_z` to M2
(both economy-level covariates standardized within the relevant sample:
`lgdppc_z` across the 93 included economies; `acc_rate_z` computed
separately per wave from each wave's own survey-weighted `account_fin` mean
by economy):

| Wave | Term | Estimate (pp) | SE | $p$ |
|---|---|---|---|---|
| 2021 | `dig_x_lowcov` (with macro controls) | −1.21 | 0.70 | 0.087 |
| 2021 | `dig_x_lgdppc` | −0.24 | 0.76 | 0.747 |
| 2021 | `dig_x_accrate` | +1.17 | 0.79 | 0.138 |
| 2024 | `dig_x_lowcov` (with macro controls) | −0.98 | 0.97 | 0.311 |
| 2024 | `dig_x_lgdppc` | −0.35 | 0.74 | 0.637 |
| 2024 | `dig_x_accrate` | +1.29 | 0.73 | 0.074 |

Reported plainly, not softened: **the coverage interaction does not survive
at conventional significance** once digital-payment activity is also allowed
to interact with log GDP per capita and the account-ownership rate.
`dig_x_lowcov` attenuates by 30.9% (2021: −1.74 → −1.21 pp) and 39.0% (2024:
−1.61 → −0.98 pp), losing significance at the 5% level in both waves (2021
remains marginal at 10%; 2024 is not significant at any conventional
level). Neither new interaction term itself reaches conventional
significance individually, so this is not a case of a competing explanation
cleanly "winning" — it is a case of the primary interaction's precision and
significance being materially eroded once collinear macro-level variation is
absorbed elsewhere in the model. This is a genuine limitation, not a
technicality: **this design cannot rule out that part of the primary
gradient reflects general economic or financial-development confounding
rather than a credit-information-specific channel.**

## What changed in `body_stage8.tex`

1. New `\subsection{Additional robustness: external-validity reweighting and
   macro-control interactions}` inserted after the existing account-sensitivity
   paragraph and before `\section{Discussion}`, presenting both items above
   in full, including the item-2 methodology adaptation note and the
   not-significant item-2 result, plus `\input{tables/tab_stage8_robustness}`.
2. Limitations section: two new sentences added immediately after the
   existing module-administration-selection sentence, reporting (a) the
   80-of-132 common-support failure and its `not_transportable`
   classification, and (b) the 31–39% attenuation and loss of significance
   under the macro-control interactions.

No other section was edited. No existing sentence was deleted or softened.

## Build verification

`main.pdf` rebuilt: **11 pages** (up from 9), zero undefined references,
zero overfull-hbox warnings (the new table's Notes paragraph reuses the same
`texttt_path()`-style break-friendly path formatting Stage 16 required for
the primary tables).

## Files added (none pre-existing touched)

- `code/study_05_crosscountry/stage17_external_validity.py` (analysis)
- `code/study_05_crosscountry/tables/build_stage8_robustness_table.py` (table generator; does not modify `build_stage8_tables.py`)
- `results/stage17_external_validity/inclusion_logit.json`, `reweighted_estimates.csv`, `macro_control_estimates.csv`, `common_support.png`
- `papers/study_05/manuscript/tables/tab_stage8_robustness.tex`
- `papers/study_05/manuscript/body_stage8.tex` (edited, not replaced)
- `papers/study_05/manuscript/main.pdf` (rebuilt)

`body.tex`, `main.tex`, `references.bib`, `H-000500.json`, `H-000501.json`,
`build_tables.py`, `build_stage8_tables.py`, and every Stage 3-16 audit file
are untouched. Nothing committed to git.

## Addendum (coordinator, same day): the item-2 attenuation is largely mechanical

Before committing this checkpoint, the coordinator independently computed the
correlation between the 2019 coverage moderator and log GDP per capita across
the 93 included economies (source: `data/raw/wb_credit_information_by_country_year.csv`
2019 rows, deduplicated by `iso3`; `data/raw/wdi_NY.GDP.PCAP.CD_2000_2023.json`,
most recent available year per economy): **Pearson $r=0.7401$ ($R^2=0.5478$),
Spearman $\rho=0.7612$ ($p=8.4\times10^{-19}$), $N=93$.**

This matters for how Item 2's attenuation should be read. Asking a fixed-effects
model with only 93 economy clusters to separately identify
`digital_payment x lowcov_z` and `digital_payment x lgdppc_z` when `lowcov_z`
and `lgdppc_z` are correlated at $r=0.74$ across those same 93 economies is a
severe collinearity burden on its own terms — consistent with neither new
interaction term reaching individual significance, which is exactly what Item
2 found. The attenuation and loss of significance are therefore **consistent
with either genuine development-level confounding or with collinearity-driven
loss of precision**, and this design cannot adjudicate between the two
readings.

`body_stage8.tex`'s new Results subsection and the corresponding Limitations
sentence were both revised (not replaced) to state this precisely: the
coverage interaction's attenuation is disclosed in full as before, but the
manuscript now explicitly attributes part of it to the $r=0.74$
coverage/GDP-per-capita correlation and states that the design cannot
distinguish genuine confounding from collinearity-driven power loss — rather
than reading as an unqualified "cannot rule out confounding" statement that
would understate how mechanical the effect likely is. This is a refinement of
interpretation, not a retraction: the underlying Item 2 numbers (attenuation
percentages, p-values, new-term coefficients) are unchanged.

`main.pdf` rebuilt after this addition: 12 pages (up from 11), zero overfull
warnings, zero undefined references.
