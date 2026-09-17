# STAGE 12 — DATA PROVENANCE AUDIT (Phase A)

## A1/A2/A3 — Existence of analytical dataset, raw inputs, and build code

All exist and were located:
- Raw 2021: `data/acquisition/FINDEX_2021/raw_microdata.csv` (documented source:
  microdata.worldbank.org/catalog/4607, ref `WLD_2021_FINDEX_v03_M`)
- Raw 2024: `data/acquisition/FINDEX_2024/raw_microdata.csv` (documented source:
  microdata.worldbank.org/catalog/7860 / global-findex catalogue, ref `WLD_2024_FINDEX_v02_M`)
- Economy manifest: `data/manifests/findex_2021_2024_primary_93.csv`
- Build code: `code/study_05_crosscountry/build_stage4_dataset.py`
- Analytical dataset: `results/stage4_build/analytical_dataset.csv`
- Moderator source: `data/raw/wb_credit_information_by_country_year.csv` (file dated
  2026-09-09, i.e. carried over from the earlier, already-vetted H-000500/H-000501 data
  acquisition — not newly fabricated for this pipeline).

## A4 — Hash verification

| File | Recorded/expected hash | Independently computed | Match? |
|---|---|---|---|
| `data/acquisition/FINDEX_2021/raw_microdata.csv` | sidecar `sha256.txt`: `98EE1367D02F92B04D0933584A4620516B90ED5F9C554F867FA5037F3F721F7A` | `98ee1367d02f92b04d0933584a4620516b90ed5f9c554f867fa5037f3f721f7a` | **MATCH** |
| `data/acquisition/FINDEX_2024/raw_microdata.csv` | sidecar `sha256.txt`: `59F22173A99EDF1206504E50CB9329147EAE5E944BD6B75C16DF5C1B2034472A` | `59f22173a99edf1206504e50cb9329147eae5e944bd6b75c16df5c1b2034472a` | **MATCH** |
| `results/stage4_build/analytical_dataset.csv` | sidecar `SHA256.txt`: `78938AFF518F3F3BC049A18E7B8CA5C1042996392B1ACDD6EAAB56FC555240C1` | `78938aff...` (same) | **MATCH**; also matches the coordinator brief's stated expected hash exactly |
| `data/manifests/findex_2021_2024_primary_93.csv` | sidecar `.sha256`: `EBB226ABDD4D8AA2F4AC1D1CE99CA61EAB6196C5E7313ED1C296875A5640CA9F` | `ebb226abdd4d8aa2f4ac1d1ce99ca61eab6196c5e7313ed1c296875a5640ca9f` (same) | **Internally consistent (matches its own sidecar)**; **does NOT match** the coordinator brief's stated "expected" hash `D1850787B88CD1D39DC2386DC324457CB820E6F5365A18B91247A3489D5E80B0` |

**Discrepancy classification (manifest hash):** the manifest file is internally
self-consistent (its own recorded sidecar hash matches the file currently on disk, so there
is no evidence of undocumented post-hoc tampering with the manifest as delivered). The
mismatch is against the *coordinator's* stated expected value only. Two explanations are
possible and could not be distinguished with the evidence available: (i) the brief's
"expected" hash is simply stale/wrong (e.g., copied from an earlier manifest draft before a
later edit), or (ii) the manifest was regenerated at some point after an external
"expected" value had already been recorded elsewhere. **Classified `UNVERIFIED`** — flagged
for the coordinator rather than resolved, since no earlier manifest version was available in
this session to compare against.

## A5 — Can results be regenerated from source?

Yes, mechanically: `build_stage4_dataset.py` → `analytical_dataset.csv` →
`stage5_estimation_audit.py` → `estimates.csv` / `weight_sensitivity.csv` →
`stage5_leave_one_out.py` → `leave_one_economy_out.csv` → `stage5_1_reconciliation.py` →
wild-cluster bootstrap and reconciliation outputs. All scripts read only from files that
exist on disk with matching hashes (raw data, manifest, moderator file). See
`STAGE_12_REPRODUCIBILITY_REPORT.md` for the executed rebuild test.

## A6 — Hard-coded numbers, manual edits, random fallback, hidden transformations

- No `np.random`-style unconditional random fallback was found in the Stage 4/5/5.1 code
  (`build_stage4_dataset.py`, `stage5_estimation_audit.py`, `stage5_leave_one_out.py`,
  `stage5_1_reconciliation.py`). The only random-number use found is the wild-cluster
  bootstrap's Rademacher sign draws in `stage5_1_reconciliation.py`, which is expected and
  appropriately seeded (`seed=20260917 + offset`), not a data-fabrication fallback.
- **Pipeline defect (not fabrication, but sloppy):** `stage5_estimation_audit.py` line 76
  writes an **empty** `leave_one_economy_out.csv` (header row only) as part of its own run,
  and its own `run_receipt.json` records `"robustness_pending": ["leave_one_economy_out"]` —
  i.e., this script's receipt honestly discloses that LOO was not yet done when it ran. The
  actual 93x2 leave-one-out estimates are produced by a **separate** script,
  `stage5_leave_one_out.py`, run afterward, which overwrites the empty stub. This is
  confirmed by inspecting both files directly (see `STAGE_12_MODEL_RECONSTRUCTION.md`). This
  is not disclosed anywhere in the audit-facing Stage 5 markdown as a two-script,
  two-pass process; a reader of `STAGE_5_ESTIMATION_RESULT_INTEGRITY_2026-09-17.md` alone
  would not know the LOO file passed through an empty intermediate state. Classified as a
  **manuscript/process reporting gap**, not a numeric fabrication — the final LOO numbers
  were independently re-verified in Phase H below and are computed directly from data, not
  invented.
- No manually-edited CSV or hidden temp file was found feeding into the estimation chain.
  `.tmp/` at the repo root was not referenced by any Stage 3-11 script inspected.
