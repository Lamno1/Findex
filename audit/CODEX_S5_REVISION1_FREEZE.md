# CODEX-S5-REV1-FREEZE-001

**Verdict:** `PASS_REVISION_1_STAGE_1_AUTHORIZED`  
**Date:** 2026-09-09  
**Outcome models run before freeze:** no

Codex checked Revision 1 against all ten blocking items in `CODEX_S5_STAGE0_REVIEW.md`.
The substantive contracts resolve them. Before freezing, Codex corrected three stale pieces
of surrounding documentation: README population/sample wording, raw-manifest coverage
wording, and the execution brief's gate wording. No estimand or specification was changed.

The authoritative byte hashes are recorded in `CODEX_S5_REVISION1_FREEZE.json`. Any change
to a frozen file invalidates this receipt.

> **INVALIDATED BEFORE STAGE 1:** a subsequent codebook check found that `fin24=4` combines
> loans from a financial institution, an employer, or a private lender. The contracted name
> `emergency_formal` is therefore false, and refused code 9 was omitted from the drop rule.
> No outcome model was run. See `CODEX_S5_PREBUILD_SEMANTIC_BLOCK.md`; Revision 2 and a new
> freeze are required.
