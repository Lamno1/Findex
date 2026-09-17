# Stage 16 — Narrative Coherence Review (Part C)

Method: `body_stage8.tex` read start to finish as a continuous document (not section-by-
section in isolation), specifically watching for the four things the brief names.

## C1 — Does the Abstract still match Results/Discussion after the Stage 14.1 additions?

**Mostly yes, with one asymmetry worth naming.** The Abstract's factual claims (positive
association in both waves; interaction −1.74pp/2021, −1.61pp/2024; wild-cluster p=0.002/
0.020; all LOO estimates negative; pooled model finds no detectable wave difference;
"persistent cross-level boundary in transportability") all match the body exactly — no
number or qualitative claim in the Abstract is contradicted by Results or Discussion.

The one asymmetry: the Abstract uses "transportability" and "persistent cross-level
boundary" without the population-scope qualifier that Stage 14.1 added to Discussion
("...should therefore be read as describing module-administered economies with
predominantly low-to-middle 2019 credit-information coverage, not economies in general")
and to Limitations. A reader who stopped at the Abstract would come away with a
slightly broader impression of what population the finding describes than a reader who
continued to Discussion or Limitations. This is not a contradiction — the Abstract does not
claim universal applicability — but it is an asymmetry in emphasis: four of the five
Stage-14.1 disclosures (module-administration scope, bootstrap naming, account_fin overlap,
LOO mechanical narrowness) are absent from the Abstract, which is conventional for an
abstract of this length, but the module-administration one is arguably the single most
consequential of the six Stage-14 findings (it is the reason Stage 14's verdict was "B," not
"A"), and it is the one most likely to change a reader's interpretation of "transportability"
specifically — the word the Abstract leads with. **Recommended, not required**: a single
clause added to the Abstract's last sentence, e.g. "...a persistent cross-level boundary in
the observed association's transportability across module-administered economies..." This is
a wording tightening, not a substantive fix — the underlying claim is not wrong as written.

## C2 — Do the five Stage-14.1-added passages read as integrated, or bolted-on?

Read as integrated. Specific checks:

- **Data §** (module-administration + Doing Business/CHN-SAU paragraphs): these are the
  second and fourth paragraphs of the Data section respectively, each following naturally
  from the paragraph introducing the 93-economy frame and the paragraph introducing the
  moderator. No repeated phrasing, no abrupt topic swing — the module-administration
  paragraph explicitly continues the "93 economies... 97... 140" thread from the paragraph
  before it rather than restarting it.
- **Empirical strategy §** (bootstrap-naming sentence): inserted as a relative clause
  immediately after the sentence introducing "wild-cluster bootstrap," reading as a single
  continuous sentence ("...Interaction inference uses a null-imposed, cluster-score
  Rademacher bootstrap... this is referred to below as the wild-cluster bootstrap, following
  common usage, though it is a one-step score-bootstrap variant and not a full-refit
  Cameron–Gelbach–Miller wild-cluster bootstrap"). Not a separate bolted-on sentence at all —
  it is grammatically part of the original sentence, which is the tightest possible
  integration.
- **Results §** (account_fin ~3% overlap; LOO mechanical-narrowness): both are appended as
  the final sentence of their respective paragraphs, each beginning with a connective ("so,"
  "which mechanically narrows") that ties them to the immediately preceding claim rather than
  introducing a new topic cold.
- **Discussion §** (population-scope paragraph): forms its own paragraph, which is
  appropriate given it is a distinct point from the persistence discussion before it and the
  explanations-review after it; it opens with "This finding also describes a narrower
  population..." which explicitly signals a continuation/qualification of the preceding
  paragraph's claim rather than an unrelated insertion.
- **Limitations §**: the module-administration and Doing Business/CHN-SAU sentences both use
  "(see Data)" cross-references rather than re-deriving the numbers, which is exactly the
  right pattern for a Limitations section (a compressed pointer back to the fuller
  disclosure) and avoids redundant restatement of the same figures twice in full.

**No redundant restatement without cross-referencing was found.** Every case where a fact
appears in more than one section (module-administration scope: Data, Discussion,
Limitations; Doing Business/CHN-SAU: Data, Limitations) uses either a "(see Data)" pointer or
a materially different framing suited to that section's purpose (Data = what happened and
why; Discussion = what it means for interpretation; Limitations = compressed caveat list) —
this is the correct pattern for a paper's own internal cross-referencing, not
duplication.

## C3 — Does any earlier section make a claim a later caveat contradicts, where the earlier section itself should have been revised?

One candidate was checked closely: **Data §'s original description of the 93-vs-97 economy
gap** — the manuscript's surviving sentence "The 2024 baseline is 97, not the raw release's
140, because the borrowing/digital-payment module was administered in only 97 economies; the
93-economy frame is the intersection of that 97-economy set with the 139 economies in the
2021 raw release" is itself already the corrected, fuller explanation (Stage 14 specifically
flagged the *pre-14.1* version of this sentence — which described only the 93-vs-97 gap
without saying why 97 rather than 140 — as the thing needing revision). Reading the current
text, the module-administration reason is now stated **in the same sentence**, not only in a
later caveat. This is the right outcome: Stage 14.1 revised the earlier section directly
rather than only patching Discussion/Limitations afterward. No unresolved
earlier-section/later-caveat contradiction was found elsewhere in the document.

The Introduction and "Related literature and positioning" sections were also checked for any
claim about population scope or generalizability that the Data-section disclosure would
undercut; neither section asserts anything about the sample's representativeness of "all
economies" (the Introduction only says the paper "test[s] whether the conditional pattern
generalises to individuals... on a common-economy specification developed during exploratory
analysis"), so there is nothing there for the later caveat to contradict.

## C4 — Section-by-section purpose check

| Section | Purpose | Redundant with another section? |
|---|---|---|
| Abstract | Self-contained summary of design, headline numbers, and epistemic status | No |
| Introduction | Motivates the question from the firm-level benchmark; states the contrary result and contribution at a high level | No — states the "what" and "why," not the numbers or the caveats |
| Related literature and positioning | Distinguishes this paper's unit/outcome/moderator from the three closest papers | No |
| Data and measurement | Defines every variable, the sample-construction rule, and its provenance caveats | No — this is the only section that derives the module-administration and Doing Business facts from first principles; other sections reference it |
| Empirical strategy | States the estimating equation, weighting, clustering, and bootstrap mechanics | No |
| Results (3 subsections) | Reports the primary, pooled, and institutional/account-sensitivity estimates with their own immediate caveats | No — each subsection covers a distinct specification family |
| Discussion | Interprets what the pattern does and does not mean, and explicitly scopes the population the claim applies to | No — this is interpretation, not re-reporting of Data's facts, aside from the deliberate one-paragraph, cross-referenced recap |
| Conclusion | Restates the headline finding and contribution at the level of a takeaway, without re-deriving numbers | Borders on restating the Abstract, but this is conventional for a short empirical paper and each restates in different words tied to different framing (Abstract = summary for a reader who reads nothing else; Conclusion = closing statement after the full argument) — not flagged as a defect |
| Limitations | Compressed, cross-referenced list of every caveat established earlier | By design a recap section; correctly uses "(see Data)" rather than duplicating |
| AI-use disclosure | Governance/authorship statement | No overlap with any other section |
| Research provenance, exploratory status, and reproducibility | States the pre-registration status, dataset hash, and Stage 12/15 reproducibility chain | Some overlap with Limitations' pre-registration sentence, but this section is the fuller, primary statement and Limitations' version is the compressed pointer — same acceptable pattern as elsewhere |

## Verdict for Part C

The manuscript reads as a coherent, single-authored-feeling document despite the multi-stage,
multi-agent edit history. The five Stage-14.1 disclosures are integrated, not bolted on. The
one genuine (but non-blocking) narrative issue is the Abstract/Discussion asymmetry in C1:
the Abstract's "transportability" claim precedes its own scoping clause by several pages,
which is ordinary for an abstract but is worth a one-clause tightening given that this is the
specific finding that kept Stage 14's verdict at "B" rather than "A."
