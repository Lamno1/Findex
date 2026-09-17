# STAGE 12 — FINAL GATE DECISION

## Gate status

| Gate | Status | Basis |
|---|---|---|
| P0 — Governance integrity | **FAIL** | `STAGE_12_GOVERNANCE_AUDIT.md`: `UNDOCUMENTED_SCOPE_VIOLATION`. No hash-frozen, council-registered pre-registration exists for the 93-economy 2021+2024 panel/pooled design; it contradicts the explicit "out of scope" clause in the frozen `PREREGISTRATION_H000501.md` Section 7; no owner/council authorization record was found anywhere; Stage 9's "adversarial" review is self-graded, not structurally independent. |
| P1 — Data integrity | **PASS (with one flagged item)** | Raw data provenance clear (World Bank catalogue IDs, source URLs, matching hashes); sample independently reproducible (93 economies, 96,711/97,847/194,558 rows all confirmed); analytical dataset hash matches the coordinator-supplied expected value exactly. One `UNVERIFIED` item: the economy manifest's hash is internally self-consistent but does not match the coordinator brief's separately stated "expected" manifest hash — flagged, not resolved. |
| P2 — Variable integrity | **PASS** | `formal_borrow`, `digital_payment`, moderator sign convention, and wave-comparability language all independently checked and found correctly constructed and consistently described; `educ`/`inc_q` category coding not cross-checked against the official codebook (flagged `UNVERIFIED`, not a failure). |
| P3 — Model integrity | **PASS** | Code's estimated equation matches the manuscript's stated equation term-for-term, including the correct treatment of the time-invariant moderator in the triple-interaction pooled model. |
| P4 — Estimation integrity | **PASS (point estimates); PARTIAL (bootstrap)** | Primary 2021/2024 coefficients, SEs, and p-values independently reproduced to 6 decimals with freshly written code. Leave-one-economy-out (93×2) independently re-tabulated and confirmed all-negative with matching ranges. Wild-cluster bootstrap implementation code-reviewed and found statistically sound (999 reps, seeded, correct null-imposed score/Rademacher construction, correct p-value formula) but not bit-for-bit re-executed with an independent RNG stream in this session. |
| P5 — Reporting integrity | **PASS (numerically); FLAG (process)** | Every manuscript number checked (Table "primary separate-wave estimates," LOO ranges, pooled/triple-interaction figures) matches the underlying CSVs exactly. However, no build script was found that generates `tables/tab_stage8_primary.tex` / `tab_stage8_pooled.tex` from `results/stage4_build`/`stage5_estimation`/`stage5_1_reconciliation` — these numbers were hand-transcribed into LaTeX, contradicting the pipeline's own documented promise ("no coefficient is typed into a .tex by hand"). Numerically correct, procedurally non-compliant with the project's own stated standard. |
| P6 — Interpretation integrity | **PASS (with one flagged sentence)** | No prohibited causal/mechanism/equality claims were found; hedging language is present essentially everywhere required (account access, three-way interaction non-significance, 2017 role, LOO sign-only robustness). One sentence — "Contrary to the registered prediction..." (body_stage8.tex line 11) — inappropriately borrows the credibility of the frozen H-000500/H-000501 pre-registration for a design that was never itself pre-registered; flagged as a required correction under Interpretation/Governance jointly. |
| P7 — Reproducibility | **PASS (with one flagged gap)** | Data→coefficient chain is executable and was independently spot-verified end to end for the two primary models and the LOO analysis. The last-mile CSV→manuscript-number step lacks an automated build script (see P5). |

## Overall verdict

Per the coordinator's explicit rule: **"A Gate P0 failure ALWAYS prevents VERIFIED and
VERIFIED WITH MINOR CORRECTIONS, no exceptions, regardless of numerical quality."** P0 is a
clear FAIL. P1-P7 are otherwise in materially good shape (numerically the strongest part of
this audit), but that numerical quality cannot lift the verdict past the ceiling P0 imposes.

**OVERALL VERDICT: MAJOR REVISION REQUIRED**

This is not a verdict that the arithmetic is wrong — independent re-estimation found the
headline coefficients, standard errors, wild-bootstrap-consistent p-value pattern, and
leave-one-out robustness claim to be genuine and reproducible from the data and code as
delivered. It is a verdict that **the design producing those numbers was run and then
written into the manuscript as a primary, "contrary to the registered prediction"
confirmatory result without ever being legitimately pre-registered**, in direct tension
with a clause in this project's own most recent frozen governing document
(`PREREGISTRATION_H000501.md` Section 7) that places exactly this design ("panel /
multi-wave estimation of the outcome") out of scope pending a new registration process that
never occurred.

## Recommended path (of the five allowed options)

**"Write and freeze a proper pre-registration retroactively-labeled as such, then treat all
current Stage 3-11 output as exploratory/pilot evidence only, then re-run under the frozen
spec."**

Concretely: (1) do not commit or submit the current manuscript body in its present framing;
(2) draft a genuine `H-000502` (or equivalent) hypothesis record covering the 93-economy,
2021+2024 design, explicitly citing and superseding the relevant clause of
`PREREGISTRATION_H000501.md` Section 7, and route it through the same owner-approval +
independent (Codex-equivalent, separate run-id) adversarial gate process that H-000501
itself went through; (3) once frozen, either re-run estimation under that frozen contract
(even though, per this audit, it would very likely reproduce the same numbers, since the
underlying computation was already found sound) or explicitly re-label all current Stage
3-11 / Stage 12 output as "exploratory / pilot, pre-dates registration" if the owner instead
chooses to keep the current numbers as background; (4) revise the "Contrary to the
registered prediction" framing in `body_stage8.tex` so it does not imply this specific
design was the one that was registered; (5) wire an actual `build_tables.py`-equivalent
script for `tab_stage8_primary.tex`/`tab_stage8_pooled.tex` so manuscript numbers are
machine-generated, closing the P5/P7 process gap independent of the governance question.
