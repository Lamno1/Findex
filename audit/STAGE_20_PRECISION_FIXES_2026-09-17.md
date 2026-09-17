# Stage 20 — Precision fixes from external Stage-14B-style review

Date: 2026-09-17
Source: an independent reviewer (owner-supplied, using the current PDF plus
the Stage 14B prompt, explicitly scoped to manuscript/logic level — did not
re-run code/data, relied on the Stage 12/14 audit record for what the PDF
itself does not contain). Verdict: **B — EMPIRICALLY SOUND, INTERPRETATION
NEEDS LIMITATION**. Five required fixes before proceeding further, all
accepted and applied as described; none disputed.

## 1. Softened "falsification"/"actively rejects" language

The reviewer's point: informal borrowing is not a clean negative control —
it can still reflect social ties, reputation and selection — so the placebo
result is strong evidence against a *formal-credit-specific,
information-screening* interpretation, but does not "falsify" the broader
credit-information-substitution hypothesis outright. Every instance of
"actively falsif(ying/ies)", "falsification result", and "actively
rejecting the substitution mechanism" (Abstract, Introduction, Discussion,
Conclusion) is replaced with "evidence against a formal-credit-specific ...
interpretation," and every such sentence now also states plainly that
informal borrowing is not a clean negative control. No underlying number
changed.

## 2. "Twice-replicated" / "well established" softened

"Twice-replicated," "a real, replicated pattern," and "well established"
are replaced with "observed consistently across both waves" / "recurs
across both waves" throughout (Abstract, Discussion, Conclusion).
"Independent computational replication" is reserved for Stage 12 only, per
the reviewer's distinction (a second implementation reproducing the same
numbers is a different claim from two waves of the same survey program
showing the same pattern).

## 3. "Not transportable" qualified

Both instances (Results \S5.4, Limitations) now read "not credibly
transportable with the available covariate overlap," making explicit that
the common-support failure limits what the reweighting model can credibly
claim, not that the true coefficient in the excluded population is known to
differ.

## 4. Removed journal/editor-facing self-assessment sentence

Deleted from the Conclusion: "The current evidence supports a strong
specialist empirical paper without requiring IV or DiD." This was a
positioning claim about the paper, not an empirical finding, and did not
belong in a results-reporting Conclusion. Not replaced with anything.

## 5. Bibliography completeness

Found exactly what the reviewer suspected: `references.bib` already
contained `WorldBankFindexMicrodata2025`, `WorldBankDoingBusinessArchive`,
and `WorldBank2020Irregularities` (correct DOI/metadata, e.g. the Findex
entry carries DOI 10.48529/bk9n-8r43) but `body_stage8.tex` never cited any
of the three. Added `\citep{}` calls at the three natural points in Data
and measurement: the Findex-waves sentence, the Doing Business
"Getting Credit" source sentence, and the 2021 discontinuation/irregularities
sentence.

**Disclosed gap, not fixed:** no dedicated citation exists for the 2021
Global Findex wave specifically (only the 2024/2025-wave microdata entry is
in `references.bib`). Per this project's "do not invent citations" rule,
no new bibliography entry was fabricated to fill this gap. If a verified
2021-wave citation is added in a future session, it should be added the
same way — checked against a real DOI/catalogue entry, not guessed.

## What was NOT changed, and why

The reviewer explicitly said items 6 ("not transportable" logic itself),
7 (macro-control diagnostic wording), 8 (module-selection disclosure), 9
(`fin22a` description), 10 (Doing Business provenance-uncertainty framing),
and 11 (bootstrap terminology) are already handled correctly and need no
change beyond item 3's wording tweak (already applied) — confirmed by
re-reading each against the current manuscript text before touching
anything, so nothing was "fixed" that was already correct.

## Build verification

`main.pdf` rebuilt: **14 pages** (unchanged page count from Stage 19),
zero overfull-hbox warnings, zero undefined references, bibliography
resolved cleanly (3 newly-cited entries render correctly).

## Files touched

- `papers/study_05/manuscript/body_stage8.tex` (Abstract, Introduction,
  Discussion, Conclusion, Results \S5.4, Limitations, Data and measurement
  — wording precision only; no coefficient, sample, or classification
  changed anywhere)
- `papers/study_05/manuscript/main.pdf` (rebuilt)

`body.tex`, `main.tex`, `references.bib` (read, not edited — no new entries
added), `H-000500.json`, `H-000501.json`, all tables, all code, and every
Stage 3-19 audit file are untouched. Nothing committed to git as part of
writing this file.
