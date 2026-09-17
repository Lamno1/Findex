# Stage 19 — Falsification / empirical-puzzle reframing

Date: 2026-09-17
Author: owner-directed narrative reframing, executed by the coordinator directly
(not delegated), after reviewing the cumulative weight of Stage 17 (macro-control
attenuation) and Stage 18 (informal-borrowing placebo failure).

## What changed and why

No data, coefficient, sample, or classification changed. This is a narrative
reframing of four sections only, per the owner's explicit confirmed scope:
Abstract, Introduction, Discussion, Conclusion.

**Old framing:** the paper's contribution was described as a "persistent
cross-level external-validity and boundary-condition finding" — the reversal
replicates across waves, mechanism unidentified, several competing
explanations left open with equal standing.

**New framing:** the paper's contribution is a **falsification result**. The
informal-borrowing placebo (Stage 18) actively rejects the specific
credit-information-substitution mechanism, rather than merely failing to
confirm it — a stronger and more precise claim, and one the evidence
actually supports (the placebo interaction is same-magnitude,
opposite-signed, significant in both waves). The macro-control check
(Stage 17 item 2) is described precisely as *not separable* from
r=0.74 coverage/GDP-per-capita collinearity, so the general-development
explanation is presented as *not confirmed*, not as a replacement mechanism
that has been established. The result is framed throughout as an
**empirical puzzle**: the reversal is real and twice-replicated; its most
natural specific explanation is rejected; its most natural general
explanation is not identifiable with this design. Every other previously
disclosed limitation (sample selection, exploratory/non-pre-registered
status, moderator provenance, etc.) is left untouched and unchanged.

## Explicit guardrail followed (owner's instruction)

The owner specifically cautioned against letting the sharper "falsification"
framing tip into overclaiming the opposite mechanism (development-level
confounding) as established. Every new sentence referencing the Stage 17
macro-control result uses "consistent with," "cannot be separated from," or
"not identifiable" — never "confirms," "establishes," or "shows" — when
describing the general-development channel. Only the informal-borrowing
placebo result is described with stronger, "actively rejects" / "falsifies"
language, because that is the one check where the evidence supports a
confident negative claim (same-sign-as-formal near-zero interaction was
predicted; a same-magnitude, opposite-signed, significant interaction was
found instead).

## Sections touched (exact scope, per owner confirmation)

1. **Abstract** — rewritten to lead with the reversal, then both falsification
   checks and their results, then the puzzle framing and the external-validity
   caveat, ending with the open explanations list. Added "falsification test"
   to keywords.
2. **Introduction** — the "primary result" paragraph now foreshadows the two
   checks; the "contribution" paragraph is rewritten from "cross-level
   external-validity and boundary-condition finding" to "not a boundary
   condition in the usual sense but a falsification result."
3. **Discussion** — new paragraph inserted right after the two-wave-persistence
   paragraph (before the population-scope paragraph, which is unchanged),
   walking through both Stage 17/18 checks and concluding with the puzzle
   framing. The "does not choose among these explanations" paragraph is
   revised to state that credit-information-substitution specifically is now
   "actively disfavoured," while the remaining explanations (including general
   economic development) stay listed as merely compatible, not confirmed.
4. **Conclusion** — rewritten in the same spirit: leads with the reversal,
   states the falsification result plainly, keeps every existing disclaimer
   (does not establish a structural effect, complementarity, or any specific
   mechanism).

Not touched, deliberately (outside confirmed scope): the paper's title, the
Related Literature "Positioning" paragraph (already says "boundary-condition
result and a theory-generating puzzle," which is not inconsistent with the
new framing and needed no change), Data and measurement, Empirical strategy,
Results (including the Stage 17/18 subsections themselves, whose numbers and
per-check language were already accurate), and Limitations.

## Build verification

`main.pdf` rebuilt: **14 pages** (up from 13), zero overfull-hbox warnings,
zero undefined references.

## Consistency check performed

Grepped the full manuscript for "boundary condition" / "boundary-condition"
after the edit: six remaining instances, all consistent with the new framing
(the Abstract and Introduction explicitly say the contribution is "not a
boundary condition in the usual sense"; the Related Literature, Discussion
population-scope paragraph, and Limitations instances are descriptive
cross-references, not competing claims).

## Files touched

- `papers/study_05/manuscript/body_stage8.tex` (Abstract, Introduction,
  Discussion, Conclusion sections edited; nothing else)
- `papers/study_05/manuscript/main.pdf` (rebuilt)

`body.tex`, `main.tex`, `references.bib`, `H-000500.json`, `H-000501.json`,
all tables, all code, and every Stage 3-18 audit file are untouched. Nothing
committed to git as part of writing this file.
