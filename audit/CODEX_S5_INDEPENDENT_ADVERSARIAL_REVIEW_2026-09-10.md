# Codex independent adversarial review — Study 5 manuscript v2

**Gate ID:** `CODEX-S5-MANUSCRIPT-GATE-20260910-001`  
**Date:** 2026-09-10  
**Target:** UEH student scientific-research competition / field-journal working paper  
**Verdict:** **PASS_TO_TYPESETTING_WITH_LIMITATIONS**  
**General-interest-Q1 verdict:** **MAJOR_REVISION / contribution ceiling remains**

## Independent conclusion

The manuscript accurately reports the frozen result: C1 is a positive conditional
cross-sectional association; H-000500/C2 is not supported and has the opposite registered
sign; C3 and C4 do not support the proposed mechanism. No reviewed defect changes those
verdicts. The paper is eligible for formatting for the realistic UEH target, provided the final
version preserves the current descriptive language and the post-registration labels.

## Checks performed

1. **Claims and numbers.** Reconciled the manuscript with the Stage-2 tables, Stage-3 audit,
   Stage-4 reproduction, the two table audits, and the C5/C6 reproduction artifacts. The M1,
   M2, M2b, mechanism, placebo, Vietnam, C5 and C6 quantities agree with their sources.
2. **C1-R precision.** The approximate 80%-power MDE of 1.33 pp/SD follows from the registered
   cluster SE. It is now surfaced in the abstract. The language remains explicitly model-based.
3. **C2-R closest paper.** Direct inspection of Galilea, Farazi and Mare, PRWP 11287, including
   its robustness section and appendix, found firm-level Enterprise Survey specifications only.
   It changes outcomes, instruments, controls and fixed effects; it does not use Global Findex
   or run an individual-level borrowing model. This supports `NOVELTY_CANDIDATE`, not a priority
   claim.
4. **C10 composition.** A hash-checked build-panel read records 97 economies across seven
   World Bank regions. Twenty-four economies below 10% coverage contribute 23,458 respondents
   (23.3% of rows). The manuscript now distinguishes row counts from its equal-economy weighting.
5. **C14-R citations.** Corrected Alok et al. to the current NBER 33259 title and DOI; completed
   Cornelli et al. as *Journal of Banking & Finance* 148, article 106742, DOI
   `10.1016/j.jbankfin.2022.106742`; confirmed the World Bank Findex 2025 bibliographic record;
   and completed Galilea et al. PRWP 11287 and DOI.
6. **Framing.** Removed a remaining unsupported superlative about digital payments. Causal,
   policy-effect, mechanism-identification and categorical novelty language remains absent.

## Residual limitations that must survive typesetting

- The design is a single cross-section; reverse causality and selection remain.
- The cross-level interaction is identified by 97 economy values of an archived 2019
  moderator, not by 100,560 independent country observations.
- The Doing Business checks establish agreement with archived profiles/live World Bank data,
  not validation against a fully independent measurement system. General non-classical
  measurement error remains possible.
- The depth and legal-rights proxies do not significantly reproduce the coverage result.
- The C5 fully interacted model is post-registration. Its coefficient is dual-implementation;
  its within-R² diagnostic is persisted but single-implementation.
- The MDE is a retrospective precision summary using the observed clustered SE, not an ex ante
  design guarantee or proof of a negative structural effect.
- The account-access channel is a plausible hypothesis only; it is not identified.
- `search_adequacy` remains `PARTIAL`, so the paper cannot claim to be the first study.

## Gate decision

For the UEH competition, no empirical or integrity blocker remains before typesetting. A final
typeset audit must ensure that tables are generated from the same immutable outputs and that
none of the limitations above is shortened into a stronger claim. For a general-interest Q1
journal, the lack of causal identification and the incremental external-population contribution
remain major limitations that copy-editing cannot solve.

## Sources reviewed

- `papers/study_05/MANUSCRIPT_DRAFT_v2.md`
- `research_council/reports/SELFREVIEW-20260910T120000Z-claude.{md,json}`
- `research_council/reports/TABLEAUDIT-20260910T113000Z-claude.json`
- root `research_council/literature/novelty_audit/LIT-20260910T053000Z-claude.{md,json}`
- World Bank PRWP 11287 and reproducibility record 430
- NBER Working Paper 33259
- Cornelli et al. (2023) publisher/repository record
- World Bank Global Findex 2025 report and microdata catalogue
