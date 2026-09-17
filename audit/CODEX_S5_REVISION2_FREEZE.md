# CODEX-S5-REVISION2-FREEZE-001

Date: 2026-09-09  
Verdict: **PASS_REVISION_2_STAGE_1_AUTHORIZED**

## Scope

Codex re-checked Revision 1 and Revision 2 before any estimation. Revision 2 fixes the
`fin24` semantic defect fail-closed: `emergency_loan_source` equals one only for code 4,
equals zero for codes 1, 2, 3, 5, 6, and 7, and excludes codes 8, 9, and missing. The
construct is not described as formal credit. The frozen Benjamini-Hochberg family still
contains exactly nine tests in the same order; only members 3 and 4 were relabelled.

The two registered M6.5 WDI controls were added to the raw manifest before this freeze.
On the frozen primary complete-case frame (100,560 respondents, 97 economies), both
controls cover 97/97 economies under the rule “latest non-missing observation no later
than 2023.” GDP per capita uses 2023 everywhere. Private-credit vintages range from 2008
to 2023 and must be disclosed rather than silently treated as a common-year measure.

## Frozen contract hashes (SHA-256)

| Artifact | SHA-256 |
|---|---|
| `papers/study_05/CLAIM_CONTRACT.md` | `d4d704be0d8fe18f97b7d96e1ab1b47eb7fcaf05d2ec6c81c1a8e8a027f9932a` |
| `papers/study_05/CODEX_EXECUTION_BRIEF.md` | `05112419c85f428f87055c438d66890b9d152182126ea48e89b1fa184d7b0a1d` |
| `papers/study_05/PREREGISTRATION.md` | `b959ae5be5d3c9fbcfb2f469a6489d3add112202c8a7db81554c333086bc75bb` |
| `papers/study_05/REVISION_1_RESPONSE.md` | `7a5e9c727dedd5431839b0fec9c8814c3cac50826b9ba679f2b412ec763d20a4` |
| `papers/study_05/REVISION_2_RESPONSE.md` | `d6206a76e00330b789373ac24cbefb52b7467c463fb5c031139886bf87daf1c5` |
| `papers/study_05/VARIABLE_CONTRACT.md` | `9a71ee5f9232d174630663373e19466159e8040203206774e879f69d711e4d6e` |
| `research_council/hypotheses/H-000500.json` | `5bcd560baf8b4c9c1dfe790009c47c8e46abc7a38a79568c6f33cb758753e653` |
| `data/STUDY_05_RAW_MANIFEST.json` | `1bce876c10ed0f72281bee846b72efb7386ed8b8e17982639a2da5b2fd2e22f6` |

Any mismatch stops Stage 1. This authorization covers data construction only; it is not
an evidence admission, result verification, or permission for causal language.
