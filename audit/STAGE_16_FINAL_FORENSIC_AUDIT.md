# Stage 16 — Final Manuscript Forensic Audit

Date: 2026-09-17. Scope: `papers/study_05/manuscript/body_stage8.tex`, confirmed canonical
via `CANONICAL_MANUSCRIPT.md` (compiled by `main.tex`'s `\input{body_stage8}` into
`main.pdf`; `body.tex` remains archived/untouched and out of scope except for cross-checks).
No Stage 3-15 artifact, `body.tex`, `H-000500.json`, or `H-000501.json` was modified in
producing this audit. `body_stage8.tex` itself was also not modified — this is a read-only
final gate, per the assignment.

This is the FINAL gate after Stage 12 (independent reproduction), Stage 13 (provenance
language correction), Stage 14 (blind adversarial review, verdict B), Stage 14.1
(remediation of Stage 14's 6 findings across five sections), and Stage 15 (table-automation
build script). The job here is narrower than Stages 12/14: verify the CURRENT, post-edit
manuscript is numerically correct, internally consistent, and does not overclaim — not to
re-litigate whether the underlying design or findings are sound.

## Part A — Numeric / table / figure consistency

Full claim-by-claim trace in `STAGE_16_NUMERIC_CONSISTENCY_CHECK.md`. Summary: every
coefficient, standard error, p-value, sample size, economy count, and hash checked against
its immutable source (`results/stage5_estimation/estimates.csv`,
`results/stage5_1_reconciliation/wild_cluster_bootstrap.csv`,
`results/stage5_estimation/leave_one_economy_out.csv`,
`results/stage4_build/ANALYTICAL_DATASET_MANIFEST.json`/`SHA256.txt`, and the Stage
14/14.1 disclosure documents for the newly-added population-scope, overlap, and
provenance figures) matched exactly, independently re-derived rather than assumed from
Stage 15's own diff report. The leave-one-economy-out ranges were independently
recomputed from the raw CSV (min/max scan) rather than trusted from any prior stage's
stated summary, and matched the manuscript's `[-1.97,-1.56]` / `[-1.83,-1.27]` pp ranges
exactly. Both `tab_stage8_primary.tex` and `tab_stage8_pooled.tex` match the prose and the
source CSVs cell-for-cell, and `main.pdf` (9 pages) was rebuilt after both the current
`body_stage8.tex` and the current table files (timestamp check confirms this), so the PDF
is not stale. `main.log` shows zero undefined references/citations and zero LaTeX errors.

**One build-hygiene finding** (not a numeric or content defect): `main.log` shows two
overfull-hbox warnings — 26.8pt in the Table 1 notes paragraph and 63.1pt in the Table 2
notes paragraph — both caused by the long, unbreakable `\texttt{}`-wrapped file paths
(`results/stage5_1_reconciliation/wild_cluster_bootstrap.csv`) that Stage 15's build script
auto-inserted into the Notes text. Visual inspection of the rendered PDF pages (5-6) shows
the notes text wraps without an obviously egregious bleed into the page margin, but the
underlying LaTeX warning is real and the 63pt figure is large enough that it is worth fixing
rather than leaving as a latent risk (e.g., if the page is ever resized or the font changed).
See Part D.4 and the recommended fix below.

## Part B — Claim-language final audit

Full risk-term table in `STAGE_16_CLAIM_LANGUAGE_FINAL_AUDIT.md`. A literal grep (not
memory) for "pre-registered"/"registered prediction"/"pre-registration" in the current
`body_stage8.tex` returns 8 hits, every one of which is a negation or scope statement (e.g.,
"no such pre-registration exists," "not a confirmatory pre-registered test") — none asserts
or implies that the current design is registered. This confirms the Stage 12 defect did not
recur during the Stage 14.1/Stage 15 edits. All other risk terms from the Stage 14 brief
("persistent," "boundary condition," "transportability," "complementarity," "stability,"
"replication," "effect," "mechanism," etc.) were re-checked in the current text and found
used only in hedged, negated, or explicitly-scoped form — consistent with, and in the case
of "boundary condition"/"transportability" now stronger than, Stage 14's own finding (their
population-scope risk is explicitly downgraded from Medium to Low given the Stage 14.1
scoping clause added to Discussion and Limitations).

The opposite-direction check (do the new disclosures overclaim the *limitation*, e.g. saying
the sample is "unrepresentative and unusable") found no such overcorrection anywhere: every
Stage 14.1 addition uses the narrow, correct framing ("should be read as describing
module-administered economies... not economies in general"; "not a random or exhaustive
cross-section," never "invalid" or "unusable").

## Part C — Narrative coherence

Full review in `STAGE_16_NARRATIVE_COHERENCE_REVIEW.md`. The manuscript reads as a coherent
single document. The five Stage-14.1-added disclosure passages (Data, Empirical strategy,
Results, Discussion, Limitations) are integrated rather than bolted on — in particular, the
bootstrap-naming addition is grammatically part of its host sentence, not a separate
insertion, and every place a fact is repeated across sections (module-administration scope;
Doing Business/CHN-SAU provenance) uses a "(see Data)" cross-reference rather than a
redundant full restatement. Checking specifically for an earlier section making a claim a
later caveat undercuts: the one candidate (the 93-vs-97 economy explanation) was found to
have been fixed by revising the earlier Data-section sentence directly, not merely patched
downstream — the correct remediation pattern.

**One narrative asymmetry, not a defect**: the Abstract introduces "transportability" and
"persistent cross-level boundary" without the population-scope qualifier ("module-
administered economies... not economies in general") that Discussion and Limitations now
carry. This is ordinary for an abstract's length constraints and does not contradict the
body, but since the module-administration finding is the single most consequential of
Stage 14's six findings (the reason its verdict was "B" not "A"), a one-clause addition to
the Abstract's closing sentence would tighten this further. See Recommended fixes below.

## Part D — Residual governance/consistency sweep

1. **Pre-registered language, whole manuscript directory.** Grepped every file under
   `papers/study_05/manuscript/` for "pre-registered"/"registered prediction". All hits
   outside `body_stage8.tex` are either (a) in `body.tex` (legitimately describing the
   frozen H-000500/H-000501 design, which really was pre-registered) or its exclusively-used
   tables (`tables/tab_primary.tex` — confirmed via `\input{}` cross-check that this table is
   only ever loaded by `body.tex`, never by `body_stage8.tex`), or (b) in historical
   changelogs (`STAGE_10_CLAIM_LANGUAGE_AUDIT.md`, `STAGE_8_CHANGELOG.md`) correctly
   describing a past state, or (c) in `CANONICAL_MANUSCRIPT.md` correctly describing
   `body.tex`'s design. No stray live claim about the current 93-economy design was found
   anywhere in the directory.
2. **`CANONICAL_MANUSCRIPT.md` accuracy.** Confirmed accurate against `main.tex`'s actual
   `\input{body_stage8}` and the file layout on disk: canonical file, build entrypoint,
   generated PDF, and legacy-file status all match reality.
3. **Bibliography.** All four `\citep{}` keys in `body_stage8.tex` resolve to matching
   `\bibitem` entries in `main.bbl`, which contains exactly those four entries (clean build
   for the currently-compiled body). `references.bib` contains 9 additional entries not
   cited by `body_stage8.tex`; 4 of those are used by the archived `body.tex` (not a
   problem — shared bib file across two manuscripts), but 5
   (`WorldBankFindexMicrodata2025`, `WorldBankDoingBusinessArchive`,
   `WorldBank2020Irregularities`, `StiglitzWeiss1981`, `PaganoJappelli1993`) are unused by
   *either* manuscript body currently in the repository. Noted per the brief's instruction
   ("not necessarily a problem") — no action required.
4. **Build hygiene.** Two overfull-hbox warnings (see Part A). No underfull-hbox warnings of
   concern beyond ordinary `\onehalfspacing`/`\sloppy` justification noise. Zero undefined
   references or citations. No TODO/FIXME/XXX/placeholder/Lorem-ipsum text found anywhere in
   `body_stage8.tex` (literal grep, zero hits).

**One pre-existing, non-blocking governance note** (not part of the six-item Stage 14/14.1
scope, and not touching any number asserted in `body_stage8.tex`): Stage 12's P1 data-
integrity gate flagged that `data/manifests/findex_2021_2024_primary_93.csv`'s hash, while
internally self-consistent with its own sidecar file, does not match a separately-stated
"expected" hash in an earlier coordinator brief (classified `UNVERIFIED` by Stage 12). This
manifest hash is never quoted in `body_stage8.tex` (only the analytical-dataset hash is, and
that one matches across all three independent recordings checked in Part A), so it does not
create a numeric defect in the manuscript. It remains an open documentation-hygiene item for
the coordinator, mentioned here only for completeness.

## Part E — Final decision

**READY WITH MINOR FIXES.**

No numeric drift, no mistraced claim, no reintroduced pre-registration language, and no
overclaim (in either direction) was found anywhere in the current `body_stage8.tex`. The
manuscript is a materially strong, carefully-hedged final product. The items below are
genuinely minor, enumerable, and do not affect the substance of any claim:

### Recommended fixes (coordinator to apply; not applied by this audit)

1. **LaTeX overfull hbox (build hygiene).** `papers/study_05/manuscript/tables/
   tab_stage8_primary.tex` line 27-28 and `tab_stage8_pooled.tex` lines 24-26: the Notes
   paragraph's file-path mentions (e.g.
   `\texttt{results/stage5\_1\_reconciliation/wild\_cluster\_bootstrap.csv}`) cause overfull
   hboxes of 26.8pt and 63.1pt respectively (confirmed in `main.log`). Since these two files
   are generated by `code/study_05_crosscountry/tables/build_stage8_tables.py` (Stage 15),
   the fix belongs in that script's Notes-string template, not by hand-editing the .tex
   output: insert `\allowbreak` (or wrap the path in `\seqsplit{}`/a `\path{}`-style breakable
   macro) after each `/` in the generated file-path strings so LaTeX has a legal break point
   inside the long typewriter-font path.
2. **Abstract/Discussion scope asymmetry (wording tightening, optional).**
   `body_stage8.tex` line 20-22 (Abstract): "...a persistent cross-level boundary in the
   observed association's transportability: the firm-level substitution pattern does not
   automatically generalise to individual formal borrowing." Consider appending a short
   clause naming the population restriction that Discussion (line ~236-240) and Limitations
   (line ~283-286) already state, e.g.: "...transportability across module-administered
   economies with predominantly low-to-middle 2019 credit-information coverage: the
   firm-level substitution pattern..." This is not required — the Abstract does not
   currently overclaim — but it would remove the one place in the document where the
   population-scope caveat is not at least indirectly present.
3. **Orphaned bibliography entries (note only, no action required).** 5 entries in
   `references.bib` are unused by either manuscript body currently in the repository (listed
   in Part D.3). Leaving them is harmless; removing them is optional housekeeping.

None of these three items involve a numeric error, a contradiction between sections, or a
claim exceeding what the design supports — which is why the classification is READY WITH
MINOR FIXES rather than NEEDS REVISION.
