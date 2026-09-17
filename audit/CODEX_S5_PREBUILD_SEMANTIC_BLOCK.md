# CODEX-S5-PREBUILD-BLOCK-001 — `fin24` semantic defect

**Date:** 2026-09-09  
**Detected:** after Revision 1 verification, before Stage 1 build and before any outcome model  
**Status:** `BLOCKED_PENDING_REVISION_2`

## Evidence

The official Findex DDI defines `fin24` as the respondent's main source of emergency money
within 30 days. Category 4 is:

> A loan from a financial institution, an employer, or a private lender.

Codes 8 and 9 are Don't know and Refused. Revision 1 currently defines
`emergency_formal = 1(fin24 == 4)` and drops code 8 but not code 9.

## Why this blocks the build

Category 4 does not isolate formal credit. Calling it `emergency_formal` would misstate the
measured construct, and treating code 9 as a valid zero would silently turn refusal into a
substantive observation. Both violate the variable contract and fail-closed protocol.

## Required Revision 2

1. Rename the variable everywhere to a neutral construct such as `emergency_loan_source`.
2. Define it as 1 for `fin24 == 4`, 0 for `{1,2,3,5,6,7}`, and missing/drop for `{8,9}` or
   system missing.
3. Replace M4/C4 wording so it never calls this outcome formal borrowing or a formal-credit
   outcome. It is a secondary contrast only.
4. Update the frozen nine-hypothesis BH family names without changing its size or test order.
5. Add a dated Revision 2 response, update H-000500 only if it mentions this outcome, and
   request a new hash freeze.

The two downloaded WDI raw inputs may remain: they contain no outcome estimates and were
acquired under the already registered M6.5 plan. No analysis panel has been written.
