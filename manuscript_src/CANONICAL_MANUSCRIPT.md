# Canonical manuscript pointer

Canonical manuscript:
papers/study_05/manuscript/body_stage8.tex

Build entrypoint:
papers/study_05/manuscript/main.tex  (currently `\input{body_stage8}`)

Generated PDF:
papers/study_05/manuscript/main.pdf

Legacy manuscript:
papers/study_05/manuscript/body.tex

Status of legacy manuscript:
ARCHIVED / NOT FOR EDITING / NOT FOR SUBMISSION

## Why two bodies exist

`body.tex` is the manuscript for the frozen, cross-agent-reproduced `H-000500`/`H-000501`
design (97 economies, single 2024 wave; see `research_council/hypotheses/H-000500.json` and
`H-000501.json`). It is complete, independently reproduced, and intentionally left untouched
as a historical/archival record — it is not wrong, just no longer what `main.tex` compiles.

`body_stage8.tex` is the manuscript for a newer, broader design (93-economy common frame
across the 2021 and 2024 Global Findex waves) developed during exploratory analysis of the
data. Its central coefficients were independently re-derived from scratch and confirmed
clean by a separate forensic audit (`audit/STAGE_12_*`), but the design itself was never
pre-registered — see `audit/STAGE_13_COORDINATOR_PROVENANCE_DECISION_2026-09-17.md` for the
full governance finding and the decision to keep its results labeled exploratory rather
than retroactively pre-registering them as confirmatory.

## Rule for future agents/editors

Before editing "the manuscript" for Study 5, check `main.tex`'s `\input{}` target to confirm
which body is currently active — do not assume `body.tex` is current just because it is the
larger, older-named file. If `main.tex` is ever repointed back to `body.tex` (or to a third
file), update this pointer file in the same commit.
