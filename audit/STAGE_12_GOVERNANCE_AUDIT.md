# STAGE 12 — GOVERNANCE AND PRE-REGISTRATION AUDIT (Phase 0)

Auditor: independent Stage-12 replication reviewer (fresh context, no prior stake in this
pipeline). Date of audit: 2026-09-17 (same day as pipeline construction).

## G1 — Does a hypothesis/pre-registration record exist for the 93-economy, 2021+2024 design?

Searched exhaustively:
- `research_council/hypotheses/active/*.json` (H-000001 through H-000142+): no file
  mentions "93 econom", "2021" and "2024" jointly as a panel/pooled design, or
  `findex_2021_2024_primary_93`.
- `research_council/hypotheses/H-000500.json` / `H-000501.json`: both exist and are
  extensively documented, but both describe the **single-wave 2024, 97-economy** design
  (H-000500) and its firm/individual diagnostic follow-up (H-000501). Neither authorizes a
  93-economy 2021+2024 panel/pooled design.
- No `H-000502.json` or any higher-numbered hypothesis file exists anywhere in the repo.
- `research_council/decisions/`, `research_council/decisions/contracts/CC-000001..6`,
  `research_council/disputes/DISPUTE-000001..22`: none reference the 93-economy design.
- `grep -r "93 econom\|findex_2021_2024_primary_93" research_council/` returns **zero
  hits** anywhere outside the project's own `audit/` and `code/` and `data/manifests/`
  directories (i.e., the design is documented only inside itself — no entry point exists in
  the council's hypothesis/decision registry at all).

**Finding: no hash-frozen, council-registered hypothesis record of any kind exists for
this design.** The only "pre-registration-like" artifacts are the pipeline's own internal
stage files (`audit/STAGE_3D_ANALYSIS_CONTRACT_DECISION_2026-09-17.md`,
`audit/STAGE_3D1_FINAL_ANALYSIS_CONTRACT_CLOSURE_2026-09-17.md`), which are self-authored,
self-approved, and never entered as a numbered hypothesis or decision-contract object in
`research_council/`.

## G2 — Was any such record frozen BEFORE estimation?

There is no external pre-registration record to test (see G1). Examining the pipeline's own
internal "contract" documents instead:

| File | Timestamp (local) |
|---|---|
| STAGE_3D_PRE_ANALYSIS_PLAN...LOCK_PROMPT.md | 13:13:39 |
| STAGE_3D_ANALYSIS_CONTRACT_DECISION...md | 13:16:25 |
| STAGE_3D1_FINAL_ANALYSIS_CONTRACT_CLOSURE...md | 13:31:07 |
| `data/manifests/findex_2021_2024_primary_93.csv` (economy manifest) | 13:30:26 |
| `results/stage4_build/analytical_dataset.csv` (built dataset) | 13:30:35 |
| `results/stage4_build/SHA256.txt` | 13:30:44 |
| `results/stage5_estimation/estimates.csv` (headline coefficients) | 13:37:53 |
| `results/stage5_1_reconciliation/wild_cluster_bootstrap.csv` | 13:44:05 |
| `audit/STAGE_9_ADVERSARIAL_REVIEWER_AUDIT...md` | 14:25:50 |

Two things follow directly from this timeline:

1. The entire chain — "contract closure" through headline estimation through the
   self-styled "adversarial" Stage 9 review — was produced inside a single continuous
   ~90-minute working session on one day, by what all internal evidence indicates is one
   authoring process (see G4). There was no interval in which an outside party could
   review a frozen design before results existed.
2. Narrowly: the "final contract closure" file (13:31:07) — which states in its own text
   "Estimation is not yet authorized by this artifact" — is timestamped **after** the
   93-economy manifest (13:30:26) and the built analytical dataset (13:30:35) already
   existed on disk. The document that is supposed to gate dataset construction post-dates
   the dataset it is gating. This is most plausibly a file-write/touch artifact of how the
   agent authored files in sequence rather than proof of results-informed rewriting, but it
   is nonetheless the opposite of what a prospective freeze requires, and cannot be
   presented as a clean prospective lock.

Because no genuine external/council pre-registration exists at all (G1), this is not a case
of "hypothesis written after results" in the ordinary sense (there is no separate
hypothesis document to date) — it is closer to **no pre-registration ever having occurred**
for this specific design, with an internal, same-author "contract" standing in for one.

## G3 — Does this design contradict an existing frozen document's explicit scope?

`papers/study_05/PREREGISTRATION_H000501.md`, Section 7 ("Out of scope (exploratory only,
labelled if reported)"), verbatim:

> Panel / multi-wave estimation of the outcome; mediation; IV; ML heterogeneity; any
> moderator not listed; any outcome not listed; ...

and Section 0 (framing), verbatim:

> Reopening would require a genuinely new design (multi-wave panel, an institutional
> reform, or lender-level data) — out of scope here.

(a) **Yes, unambiguously.** The Stage 3–11 pipeline's primary design is exactly
"panel / multi-wave estimation of the outcome": separate-wave 2021 and 2024 models plus a
pooled 2021–2024 secondary model, on a common 93-economy frame, with `formal_borrow` as the
outcome in both waves. This is the precise thing Section 7 places out of scope without "a
genuinely new design" process.

(b) **No recorded authorization was found.** H-000501's own revision history (Section 9,
"R1 changelog (owner CONDITIONAL APPROVAL review, 2026-09-10)") shows what a real
contemporaneous owner-authorization record looks like in this project: a dated review, a
named decision ("owner CONDITIONAL APPROVAL"), and itemized must-fixes with resolutions.
No comparable entry exists anywhere — in H-000501.json's revision history, in
`research_council/decisions/`, or in `research_council/disputes/` — approving relaxation of
the "panel / multi-wave... out of scope" clause for this 93-economy design. The
`STAGE_3D1_FINAL_ANALYSIS_CONTRACT_CLOSURE` document self-certifies its own contract; it is
not an owner decision record and does not cite one.

(c) **No such authorization record exists.** Stated plainly: this pipeline ran a design
that the project's own most recent frozen governing document places out of scope pending "a
genuinely new design" process, and no evidence of that process (a new hash-frozen
hypothesis, an owner sign-off, a council decision) exists anywhere in the repository.

Compounding this: the current, git-modified manuscript (`main.tex` → `body_stage8.tex`,
already the tracked, uncommitted manuscript body) has **already promoted this unauthorized
design to the paper's headline confirmatory result** — e.g. body_stage8.tex line 11-13:
"Contrary to the registered prediction, the interaction with lower 2019 historical
credit-reporting coverage is negative in 2021 (−1.74 pp...) and 2024 (−1.61 pp...)". This
sentence explicitly frames the *unregistered* 93-economy panel result as a test outcome of
"the registered prediction" — i.e., it borrows the confirmatory credibility of the frozen
H-000500/H-000501 pre-registration for a design that pre-registration never covered and
explicitly excluded. It is not run and reported as an "exploratory only, labelled"
diagnostic as Section 7 requires for anything in its out-of-scope list — it is the paper's
primary result.

## G4 — Was there an independent (Codex-equivalent) adversarial gate, or was Stage 9 self-graded?

Comparison points:
- H-000500/H-000501 discipline (visible throughout `research_council/reports/CODEX-S5-*`,
  `audit/CODEX_S5_*`, and H-000501.json's revision history): a structurally separate actor
  with its own run-id namespace (`CODEX-S5-*`, `EXP-S5-002`) produces stage-0 adversarial
  reviews, data challenges, and independent freezes, cross-checked against Claude's own
  `CLAUDE-S5R-*` cold reproductions. Both namespaces coexist and are cross-referenced by ID.
- Stage 3–11 pipeline: `grep -l "CODEX-S5\|Codex agent\|independent agent\|separate
  agent\|separate implementation"` across every Stage 3A–11 markdown file returns **zero
  matches**. There is no second run-id namespace anywhere in this pipeline. Every stage
  gate (`GATE_3A_CLOSURE`, `GATE_3B...`, `GATE_3C...`, `STAGE_3D...`, `STAGE_4...`,
  `STAGE_41...`, `STAGE_5...`, `STAGE_51...`, `STAGE_6...`, `STAGE_7...`, `STAGE_9...`) is
  written in the same voice, the same terminology ("qualified-comparable," "boundary
  condition," "not an identified mechanism"), the same self-referential closure structure
  ("Unlocked: ..."), and was produced within the same single-day, single-session timeline
  documented under G2.
- Stage 9 itself is explicitly titled "Adversarial Reviewer Audit" and opens with "No new
  regression, dataset, hypothesis, IV/DiD design or manuscript edit was performed" — i.e.
  it presents itself as an independent referee pass, but nothing in the file identifies a
  separate authoring agent, a separate run id, or a separate implementation. Its own
  strongest-rejection-argument / strongest-evidence-against structure is internally
  self-consistent with the style of Stages 3–8, not a distinct external voice.

**Finding: Stage 9 is self-graded.** It simulates a referee's argument-counterargument
structure but shows none of the structural separation (distinct agent, distinct run-id
namespace, distinct implementation) that this project's own H-000500/H-000501 discipline
established as the standard for treating a review as genuinely adversarial rather than a
self-review.

## G5 — Governance classification

**`UNDOCUMENTED_SCOPE_VIOLATION`**

Rationale: a hash-frozen document that governs this exact research line
(`PREREGISTRATION_H000501.md`) explicitly places "panel / multi-wave estimation of the
outcome" out of scope pending a new design process; the Stage 3–11 pipeline ran precisely
that design; and no record anywhere in the repository — no new hypothesis file, no owner
decision, no council contract, no dispute resolution — authorizes relaxing that
restriction. This is compounded by (and overlaps with) `NO_HYPOTHESIS_RECORD_FOUND`: not
only was the restriction not lifted, no prospective pre-registration record for the new
design was ever created outside the pipeline's own self-authored, same-day, same-voice
"contract" documents, which cannot substitute for a genuine, external, prospectively-timed
freeze given the timeline in G2 and the absence of separation in G4.

## G6 — Binding effect on Phase P gates

Per the coordinator's Gate P0 rule, this classification means **Gate P0 = FAIL**, which
caps the maximum achievable overall verdict at **MAJOR REVISION REQUIRED** regardless of how
well the pipeline performs on data, variable, model, estimation, reporting, interpretation,
and reproducibility checks (Phases A–P below). In plain terms: even where the arithmetic in
this pipeline is independently reproducible (and Phases F/H below find that much of it is),
that numerical correctness cannot convert into evidentiary weight for this project's own
confirmatory purposes, because the design that produced it was never legitimately
authorized before its results were seen, and it currently occupies the position of the
manuscript's primary, "contrary to the registered prediction" confirmatory claim rather
than a clearly labelled exploratory/diagnostic side-analysis. The correct process failure
here is procedural, not (primarily) computational: the fix is to register the design
prospectively (or explicitly relabel all current 93-economy/2021+2024 output as exploratory
pilot evidence) before any of it is used to support a claim.

Note on the coordinator's framing: the coordinator's dispatch note characterized this
situation accurately. Independent verification confirms it: no H-000502 (or equivalent)
exists, and the out-of-scope clause in `PREREGISTRATION_H000501.md` is real, applicable, and
unwaived.
