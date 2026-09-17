# Stage 13 — Coordinator decision on Stage 12's governance finding

Date: 2026-09-17
Author: owner (via coordinating Claude session), responding directly to
`audit/STAGE_12_GOVERNANCE_AUDIT.md` and `audit/STAGE_12_GATE_DECISION.md`.

## What Stage 12 found

Gate P0 = FAIL. Classification `UNDOCUMENTED_SCOPE_VIOLATION` /
`NO_HYPOTHESIS_RECORD_FOUND`. No hash-frozen pre-registration exists anywhere in
`research_council/` for the 93-economy, 2021+2024 common-frame panel/pooled design built by
the Stage 3-11 pipeline. The frozen `papers/study_05/PREREGISTRATION_H000501.md` Section 7
explicitly places "panel / multi-wave estimation of the outcome" out of scope pending a new
pre-registration process; that process never happened. Numerically, the pipeline's central
results independently re-reproduced cleanly (see Stage 12's Section B table) — this is not a
data-fabrication or coding-error finding. It is a provenance/confirmatory-status finding: the
manuscript (`body_stage8.tex`, loaded by `main.tex`) described this design and its result in
language that implied prospective pre-registration ("pre-registered Global Findex...",
"Contrary to the registered prediction", a "Registration and reproducibility" section stating
flatly "the pre-registration ... was hash-frozen before the relevant estimations"), when no
such pre-registration exists.

## Decision made, and the one explicitly rejected

Stage 12's own "Final Recommendation" suggested: *"Write and freeze a proper pre-registration
retroactively-labeled as such, then treat all current Stage 3-11 output as exploratory/pilot
evidence only, then re-run under the frozen spec."*

**The owner explicitly rejected the "write a retroactive pre-registration and then treat the
already-seen results as confirmatory" path.** The reasoning, recorded verbatim in spirit:
a pre-registration written after the researcher has already looked at the data and chosen
the sample/specification cannot honestly upgrade those same results to confirmatory status,
no matter how the document is labeled — pre-registration's entire evidentiary function is
that the specification was locked *before* results were seen. Retroactively freezing a
document that matches what was already found does not create that property; it only launders
an exploratory finding into the appearance of one.

**Decision adopted instead:**
1. Keep the current Stage 3-11 pipeline's results as **exploratory/observational evidence**,
   explicitly labeled as such in the manuscript — not confirmatory, not "pre-registered."
2. Make the research provenance **transparent** in the manuscript itself: the 93-economy,
   2021-2024 common-frame sample and specification were developed during exploratory
   analysis of the data, not fixed in advance; no pre-registration exists for this design;
   this design was not authorized as a scope-extension of the frozen `H-000501` protocol.
3. **Do not** write a new pre-registration that purports to retroactively confirm the
   current findings. A prospective pre-registration (a fresh hypothesis ID, e.g.
   `H-000502`) may legitimately be written in the future, but only to govern a genuinely
   new confirmatory test on data/specification choices not already informed by having seen
   these results — that is separate, future, optional work, not a relabeling of what already
   exists.
4. Fix every instance of misleading "registered"/"pre-registered" language in
   `body_stage8.tex` (abstract, introduction, related-literature positioning paragraph,
   conclusion, limitations, and the "Registration and reproducibility" section, which is
   renamed "Research provenance, exploratory status, and reproducibility") so the manuscript
   accurately states: the design was exploratory in origin, no pre-registration exists, the
   arithmetic is independently reproduced (Stage 12) which establishes computational
   reproducibility but not confirmatory status, and these are two different, non-substitutable
   properties.

## What this changes and does not change

- Does NOT change: any coefficient, standard error, p-value, sample construction, or
  classification. Stage 12 found the arithmetic clean; nothing here disputes that.
- DOES change: how the manuscript describes the *evidentiary status* of that arithmetic.
  "Independently reproduced exploratory finding" is an honest, still-useful description;
  "pre-registered confirmatory test" was not accurate and has been removed everywhere it
  appeared in `body_stage8.tex`.
- Stage 9's self-graded "adversarial review" status (flagged by Stage 12 as lacking the
  structural agent/namespace separation used for `H-000500`/`H-000501`) is unchanged by this
  decision and remains an open, lesser item — noted, not resolved, here.
- The hand-typed `tab_stage8_primary.tex`/`tab_stage8_pooled.tex` process gap (Stage 12
  Section C.3) is also unchanged by this decision and remains open.

## Provenance of this record

This file exists because the project's own discipline (visible throughout
`research_council/hypotheses/H-000500.json` and `H-000501.json`) is to record research
decisions as an append-only, dated trail rather than silently editing prior conclusions away.
This is that record for the Stage 12 → Stage 13 transition. No existing Stage 3-12 file was
modified to produce this note; only `papers/study_05/manuscript/body_stage8.tex` was edited,
as described above, and `main.pdf` was rebuilt from it (8 pages, no undefined references).
