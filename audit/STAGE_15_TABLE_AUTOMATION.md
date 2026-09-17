# Stage 15 — Automated Results Pipeline for the Stage 8 tables

Date: 2026-09-17

## What was built

`code/study_05_crosscountry/tables/build_stage8_tables.py` — reads ONLY
`results/stage5_estimation/estimates.csv` and
`results/stage5_1_reconciliation/wild_cluster_bootstrap.csv`, and writes
`papers/study_05/manuscript/tables/tab_stage8_primary.tex` and
`tab_stage8_pooled.tex`. No number is typed by hand anywhere in the script;
every coefficient, SE, p-value, N and G is read from those two CSVs. The
script cross-checks that each wild-bootstrap row's `estimate` field matches
the corresponding `estimates.csv` row it is annotating (an `assert`), so the
two source files cannot silently drift apart without the script failing.

This script is independent of `code/study_05_crosscountry/tables/build_tables.py`
(the older H-000500/H-000501 table builder for `body.tex`) — that script was
not read in detail and was not modified; only its general file-header/module
docstring convention was used as a style reference.

## Diff-and-classify result: all numbers matched exactly

Ran the script, diffed its output against the previously-committed hand-typed
tables. **Every data cell was identical**: digital-payment coefficients (9.07,
8.13), interaction coefficients (-1.74, -1.61), clustered SEs (0.49, 0.60),
wild-cluster p-values (0.002, 0.020), N (96,711 / 97,847), G (93/93) in the
primary table; pooled interaction (-1.98), triple interaction (+0.58), wild-p
(0.305), N (194,558), G (93) in the pooled table. Significance stars matched
the existing convention (*** for clustered p<0.01) in every case that
appeared.

**Zero discrepancies of any kind** — no `FORMATTING_ONLY`, no
`HAND_TYPED_WAS_WRONG`, no `SCRIPT_MISREAD`. The person(s) who hand-typed the
original tables got every number right. The only textual difference between
the old and new files is in the Notes paragraph: the star legend was
extended to document all three tiers (`***`/`**`/`*`, matching the general
convention even though only `***` was actually triggered by any cell here),
and a provenance sentence was added naming the generating script and its
two source files.

## Bootstrap terminology check

The table notes already said "999 null-imposed cluster-score Rademacher
replications" before this pass — the Stage 14.1 terminology fix had already
been applied to the tables, not just the prose. The column header "Wild-cluster
$p$" was left as-is: this is a standard, compact econometrics-table column
label, and the full method name is already spelled out once in the notes
below each table. Renaming the column header itself to the full method name
would not fit the column width and is not how comparable tables in the field
are conventionally labelled (the notes line is exactly where that
disambiguation belongs). No change made to the header text.

## Manuscript change

Added one sentence to `body_stage8.tex`'s "Research provenance, exploratory
status, and reproducibility" section, immediately after the sentence
describing Stage 5/5.1 artifact traceability:

> Tables~\ref{tab:stage8primary} and~\ref{tab:stage8pooled} are generated
> directly from those Stage 5/5.1 artifacts by
> `code/study_05_crosscountry/tables/build_stage8_tables.py` (Stage 15); no
> coefficient, standard error, p-value or sample count in either table is
> typed by hand.

This mirrors how `body.tex` describes its own `build_tables.py`.

## Build

First build attempt failed: the script's auto-generated Notes text contained
unescaped `_` characters in file paths (e.g. `stage5_1_reconciliation`,
`build_stage8_tables.py`), which LaTeX outside math mode interprets as a
subscript operator, producing "Missing $ inserted" / "Double subscript"
errors. Fixed by wrapping every file-path mention in the generated tables in
`\texttt{}` with escaped underscores (`\_`), matching the convention already
used in the manually-edited part of `body_stage8.tex`. Rebuilt clean:
**9 pages, zero undefined references, zero errors.**

## Result

Stage 12's flagged process gap ("numbers correct, but hand-typed — not wired
into a build script") is closed. Re-running Stage 5/5.1 in the future and
then re-running `build_stage8_tables.py` will keep the manuscript tables in
sync automatically; the previous risk (a re-run producing -1.72 while the
table still says -1.74) no longer exists for these two tables.
