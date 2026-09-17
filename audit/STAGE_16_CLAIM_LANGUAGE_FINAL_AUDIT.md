# Stage 16 — Claim Language Final Audit (Part B)

Re-run of the same risk-term sweep Stage 14 used (`STAGE_14_CLAIM_LANGUAGE_REVIEW.md`), on
the CURRENT `body_stage8.tex` text — i.e., after the Stage 14.1 remediation and Stage 15
table-automation edits, not the pre-14.1 version Stage 14 itself reviewed. Method: literal
grep for each term across the file, then manual read of every hit in context.

## B1 — Literal grep results, current file

```
$ grep -ni "pre-registered\|pre-registration\|registered prediction\|preregist" body_stage8.tex
10:  ...rather than fixed by a prospective pre-registration...
292:  ...pre-registration; no such pre-registration exists for this design...
294:  ...out of scope pending a new pre-registration process...
296:  ...confirmatory pre-registered test...
298:  ...confirmatory in the pre-registration sense...
314:  ...prospective, hash-frozen pre-registration. No pre-registration record exists...
317:  ...pending a genuinely new pre-registration process...
319:  ...not a confirmatory pre-registered test...
```

**Every hit is a negation or scope statement** ("rather than," "no such pre-registration
exists," "pending a new... process," "not a confirmatory... test"). Zero hits assert or imply
that the 93-economy/2021-2024 design itself is pre-registered, confirmatory, or registered.
This confirms the Stage 12 defect ("Contrary to the registered prediction," a "Registration
and reproducibility" section asserting prospective freezing) did not recur during the Stage
14.1 or Stage 15 edit passes — no residual or reintroduced "registered"/"pre-registered"
language exists in the current canonical file.

## B2 — Risk-term table (terms from the Stage 14 brief)

| Term | Instances in current text | Assessment |
|---|---|---|
| "persistent" | Abstract ("persistent cross-level boundary"); Conclusion ("persistent cross-level external-validity and boundary-condition finding"); Discussion ("the same persistent selection or measurement structure could recur") | Consistently paired with the two-wave qualifier and explicit non-claims ("does not prove temporal stability," "does not identify an underlying economic mechanism"). No instance asserts persistence beyond the two observed waves. Unchanged from Stage 14's "Low risk" finding; Stage 14.1 did not touch these sentences. |
| "boundary condition" | Abstract, Discussion, Conclusion | Stage 14 flagged this as Medium risk for undisclosed population scope. Stage 14.1 added the scoping clause directly adjacent in Discussion ("...should therefore be read as describing module-administered economies with predominantly low-to-middle 2019 credit-information coverage, not economies in general") and in Limitations. **Risk downgraded from Medium to Low** — the term is now explicitly scoped where it is used. |
| "transportability" | Abstract only ("the observed association's transportability") | Same Medium→Low downgrade rationale as "boundary condition" applies, since the Discussion-section scoping clause immediately follows the sentence that reintroduces the underlying concept, and Limitations repeats the population-scope caveat. See Part C of the narrative review for a residual point: the Abstract itself, where "transportability" first appears, does not carry the population-scope clause — see `STAGE_16_NARRATIVE_COHERENCE_REVIEW.md` §1. |
| "information substitution" | Not found verbatim (paper uses "substitution prediction," "substitution pattern") | The word "substitution" is used only to describe the motivating hypothesis from the benchmark firm-level paper, consistently marked as a prediction that "did not materialize" / "is not supported." No claim that substitution was found. |
| "information value" | Not found verbatim | N/A |
| "credit information" | Data §, Related literature §, Discussion, Limitations | Used descriptively (the moderator's definition, "credit-information systems," "credit-information coverage"). Always qualified as breadth/coverage, never asserted as depth, accessibility, legal usability, or actual lender use — restated explicitly in Data § ("Coverage, depth and accessibility therefore remain separate constructs"). Low risk. |
| "complementarity" | Discussion only ("consistent with complementarity or access-selection accounts, but it does not establish either") | Explicitly non-asserted, listed as one of two unresolved candidate accounts. Low risk, matches Stage 14's finding exactly (unchanged). |
| "stability" | Results ("It does not prove temporal stability, equality, a structural effect or a common mechanism") | Used only in a negation. Low risk. |
| "replication" | Related literature § ("not a direct replication"); provenance § ("independent human replication," twice, both negated/contrasted against "computational reproducibility") | Every instance either denies replication status or explicitly distinguishes computational reproducibility from human replication. Low risk, unchanged from Stage 14. |
| "registered" / "pre-registered" | See B1 above | Zero assertive instances; all negations/scope statements. Low risk, confirmed by literal grep (not memory), as the brief specifically required. |
| "effect" | Empirical strategy ("not an effect of institutional change"); Conclusion ("does not establish that weak coverage causes a negative structural effect"); Limitations (implicitly, via "causal claims: false" logic) | All instances of "effect" are negated (i.e., stating what is NOT an effect / NOT established). No instance asserts a causal effect. Low risk. |
| "mechanism" | Introduction, Related literature, Results, Discussion, Conclusion (repeatedly) | Every instance is a negation or an explicit statement that mechanism is not identified/established ("not an identified mechanism," "does not identify an underlying economic mechanism," "Future mechanism claims would require lender- or application-level evidence"). Low risk. |

## B3 — Opposite-direction overclaim check (Stage 14.1 disclosures themselves)

The brief specifically asks whether the newly-added disclosure sentences overcorrect into an
overstated negative claim (e.g., "the sample is unrepresentative and unusable" instead of the
narrower, correct "scope should be read as module-administered economies, predominantly
low-to-middle coverage").

| Added disclosure sentence (paraphrased/located) | Exact framing used | Overclaim risk |
|---|---|---|
| Data §: "The 93-economy sample is therefore not a random or exhaustive cross-section... it is a population pre-filtered by Findex fieldwork decisions..." | "not a random or exhaustive cross-section" / "pre-filtered" | None — this is the precise, narrow claim; it does not say "unrepresentative," "invalid," or "unusable." |
| Discussion §: "...the boundary-condition and transportability language in this paper should therefore be read as describing module-administered economies with predominantly low-to-middle 2019 credit-information coverage, not economies in general." | "should... be read as describing [X], not economies in general" | None — this is exactly the narrow scoping the brief asks for, not a blanket "unrepresentative" claim. |
| Limitations §: "The 93-economy frame is not a random or exhaustive sample of economies with available 2019 coverage data: it excludes most near-universal-coverage economies..." | "excludes most near-universal-coverage economies," "narrowing the population to which the boundary-condition language applies" | None — consistent narrow framing; does not extend to claiming the in-sample estimates themselves are invalid or unreliable (a distinct claim the manuscript correctly avoids). |
| Results §: "~3% ... construction overlap ... a first-order collinearity risk for the account-conditioning specification in 2021 specifically" | scoped explicitly to "the account-conditioning specification in 2021 specifically" | None — does not extend the caveat to the primary specification (which does not condition on `account_fin`), correctly limiting blast radius. |
| Results §: LOO mechanical-narrowness sentence — "rules out a dominant-influence economy, not homogeneity of the underlying association across economies or economy groups" | explicit two-sided scoping (what it does vs. does not show) | None. |
| Empirical strategy §: bootstrap-naming sentence | states precisely what the procedure is and is not, without overstating that the precision issue undermines validity | None — Stage 14 already found the mechanics "statistically sound"; the manuscript does not claim otherwise nor understate the method's validity. |

**No instance of overcorrection was found.** Every Stage 14.1 addition uses the narrow,
scope-limiting phrasing the brief considers correct, not the broader "unrepresentative/
unusable" framing it warns against.

## Verdict for Part B

No risk term is used beyond what the design supports, in either direction (overclaiming the
finding's generality, or overclaiming the disclosures' severity). The single residual item —
"transportability"'s first appearance in the Abstract preceding its Discussion-section
scoping — is a narrative-sequencing observation, not a claim-language defect; see
`STAGE_16_NARRATIVE_COHERENCE_REVIEW.md`.
