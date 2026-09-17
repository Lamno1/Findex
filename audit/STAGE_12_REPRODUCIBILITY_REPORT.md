# STAGE 12 — REPRODUCIBILITY REPORT (Phase N)

## Chain tested

RAW DATA (hash-verified) → `build_stage4_dataset.py` → `analytical_dataset.csv`
(hash-verified, matches coordinator-supplied expected hash exactly) →
`stage5_estimation_audit.py` → `estimates.csv` → `stage5_leave_one_out.py` →
`leave_one_economy_out.csv` → `stage5_1_reconciliation.py` → wild-cluster bootstrap +
reconciliation outputs → manuscript numbers in `body_stage8.tex`.

## What was independently executed in this session

1. Recomputed SHA-256 of both raw Findex CSVs, the economy manifest, and the analytical
   dataset directly from the files on disk — all matched their sidecar/expected records
   except the manifest vs. the coordinator's stated expected value (see
   `STAGE_12_DATA_PROVENANCE_AUDIT.md`, classified `UNVERIFIED`, not a reproducibility
   failure of the pipeline itself since the manifest matches its own internal record).
2. Recomputed wave/economy/row counts directly from `analytical_dataset.csv` with an
   independently written script: 2021 = 96,711 rows / 93 economies; 2024 = 97,847 rows / 93
   economies; total = 194,558 rows / 93 economies common to both waves. **Exact match** to
   both the coordinator's brief and the pipeline's own reported figures.
3. Wrote a fresh, independently coded Python script (not copied from the project's own
   `stage5_estimation_audit.py`) that reloads the analytical dataset and the 2019 credit
   coverage file, reconstructs `lowcov_z` and the interaction from the documented
   transformation, and refits the WLS LPM with economy-clustered SEs for both waves. Result:
   coefficients matched the pipeline's own `estimates.csv` to 6 decimal places (see
   `STAGE_12_INDEPENDENT_REPLICATION_REPORT.md`).
4. Confirmed the leave-one-out file on disk (93 rows per wave, all negative, min/max
   matching manuscript-quoted ranges) directly from `leave_one_economy_out.csv`.

## What was NOT independently re-executed

- The `build_stage4_dataset.py` script itself was not re-run end-to-end from raw CSV in this
  session (it performs a full 40MB+50MB raw-file read/filter/transform); instead its logic
  was verified by code review plus independent recomputation of the row/economy counts
  *from its declared output*, which matched exactly. This is a reasonable but not maximal
  standard of reproducibility verification — full re-execution from raw data was not run due
  to session scope, and is recommended as a follow-up.
- The 999-draw wild-cluster bootstrap resampling loop was not independently re-executed
  (see `STAGE_12_BOOTSTRAP_AUDIT.md`).
- The table-generation step from `results/stage5_1_reconciliation/*` into
  `body_stage8.tex`'s specific LaTeX numbers was checked by direct text comparison (manual
  cross-reading), not by re-running a table-build script — no `build_tables.py`-equivalent
  script targeting Stage 3-11 outputs was found in `code/study_05_crosscountry/` (the
  `tables/build_tables.py` referenced in `main.tex`'s header comment targets the *earlier*
  `results/stage2`/`results/stage3` (H-000500/H-000501) pipeline, not the new Stage
  4/5/5.1 outputs). This means the numbers appearing in `body_stage8.tex` for the
  93-economy design were typed in by hand from the CSVs, not machine-generated via a
  documented build script — **this is itself a reproducibility gap**: the manuscript's own
  header comment promises "no coefficient is typed into a .tex by hand," but no build script
  wiring `results/stage4_build`/`stage5_estimation`/`stage5_1_reconciliation` into
  `body_stage8.tex` was found. The numbers were manually cross-checked in this audit and
  found to match the CSVs exactly, but the *process* does not meet the pipeline's own stated
  reproducibility bar.

## Overall reproducibility classification

**Reproducible with minor manual intervention** for the empirical results proper (the
data-to-coefficient chain is executable and was independently spot-checked with matching
output); but **not fully reproducible end-to-end into the manuscript**, because the last
mile (CSV numbers → LaTeX prose/table numbers) has no automated build script for this
specific pipeline, contrary to the pipeline's own documented promise. This is a process
finding, separate from and additional to the Phase 0 governance failure.
