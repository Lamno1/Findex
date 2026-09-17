# Stage 16 minor fixes — applied 2026-09-17

Per `audit/STAGE_16_GATE_DECISION.md` (READY WITH MINOR FIXES), the two
non-blocking, no-risk items were applied. The third item (5 unused
`references.bib` entries) was left as a note-only, no action, per the
Stage 16 report's own recommendation.

## Fix 1 — overfull \hbox in table Notes paragraphs

**Cause:** `code/study_05_crosscountry/tables/build_stage8_tables.py` inserted
long `\texttt{}` file-path strings into the Notes minipage with no legal
LaTeX break points, producing two overfull-hbox warnings (26.8pt and 63.1pt).

**Fix, in the build script, not the generated `.tex`:** added a
`texttt_path()` helper that escapes underscores and inserts `\allowbreak{}`
after every `/` in a path before wrapping it in `\texttt{}`. Both
`build_primary()` and `build_pooled()` now call this helper instead of
hand-formatting the path strings inline. Re-ran
`python code/study_05_crosscountry/tables/build_stage8_tables.py`;
`tab_stage8_primary.tex` and `tab_stage8_pooled.tex` regenerated with only
the three Notes-paragraph path lines changed in each file (six lines total)
— no coefficient, SE, p-value, N, or G changed.

**Verified:** `main.log` after rebuild has zero `Overfull` and zero
`undefined` matches; PDF still 9 pages.

## Fix 2 — Abstract missing the population-scope qualifier

**Cause:** Discussion and Limitations already scoped "transportability" /
"boundary condition" language to module-administered, predominantly
low-to-middle-coverage economies (added in Stage 14.1), but the Abstract's
use of the same terms carried no such qualifier — not an overclaim as
written, but an inconsistency in how tightly different sections hedge the
identical claim.

**Fix, in `papers/study_05/manuscript/body_stage8.tex` (Abstract):**

Before:
> We interpret the result as evidence of a persistent cross-level boundary
> in the observed association's transportability: the firm-level
> substitution pattern does not automatically generalise to individual
> formal borrowing.

After:
> We interpret the result as evidence of a persistent cross-level boundary
> in the observed association's transportability across module-administered
> economies with predominantly low-to-middle 2019 credit-information
> coverage: the firm-level substitution pattern does not automatically
> generalise to individual formal borrowing in this population.

**Verified:** rebuilt PDF, no new warnings, page count unchanged (9).

## Not actioned

5 unused `references.bib` entries (`WorldBankFindexMicrodata2025`,
`WorldBankDoingBusinessArchive`, `WorldBank2020Irregularities`,
`StiglitzWeiss1981`, `PaganoJappelli1993`) — Stage 16 classified this as a
note, not a defect; left as-is.

The manifest-hash documentation item Stage 16 re-raised was already
resolved in `audit/STAGE_4_DATASET_BUILD_INTEGRITY_REPORT_2026-09-17.md`'s
Stage 13 addendum (`MANIFEST_CHANGED_LEGITIMATELY`, committed in `e8c6bfe`)
— Stage 16's agent appears not to have checked that file's addendum. No
further action needed; the hash in question is not quoted anywhere in
`body_stage8.tex`.

## Status after these fixes

Both blocking-adjacent Stage 16 recommendations are closed. The manuscript
is now READY (no outstanding minor-fix items remain open).
