# CLAUDE-S5R-DB-INTEGRITY-20260910-001 — Independent reproduction of the C6 sensitivity

**Date:** 2026-09-10 · **Reproduces:** `CODEX-S5-DB-INTEGRITY-20260910-001` (SELFREVIEW C6) ·
**Executed by:** Claude, independent of Codex · **Verdict: PASS**

## What was checked

`CODEX-S5-DB-INTEGRITY-20260910-001` (Codex-lineage: imports `estimate_stage2_codex`) drops the
two economies the World Bank's December 2020 *Review of Data Irregularities in Doing Business*
specifically implicates for *Getting Credit* — China (DB2018) and Saudi Arabia (DB2020) — both in
the Study 5 sample, re-standardizes the 2019 coverage moderator (population sd, ddof=0) across the
remaining 95 economies, and re-fits the frozen M2. It reports the digital-payment × lower-coverage
interaction at −0.019548.

This run re-does that from a **separate implementation** — Claude's Stage-4 cold estimator
(`CLAUDE-S5R-20260910-001_reproduce.py`: hand-rolled WLS normal equations + explicit economy-dummy
FE + CR1 `c₁ = G/(G−1)·(N−1)/(N−k)`), reusing only `build()` and the estimator; no Codex
estimation code imported.

## Result

| Quantity | Codex | Claude reproduction | \|Δ\| |
|---|---|---|---|
| interaction `dig × lowcov2019_z` | −0.019548385736877 | −0.019548385736825 | **5.2 × 10⁻¹⁴** |
| economy-clustered SE | 0.0048203545628621 | 0.0048203545628628 | 6.6 × 10⁻¹⁶ |
| moderator mean (95 economies) | 40.70421052631578 | 40.70421052631578 | 0 |
| moderator sd, ddof=0 (95 economies) | 31.45601412093928 | 31.45601412093928 | 0 |
| N / G | 95,909 / 95 | 95,909 / 95 | exact |
| baseline all-97 M2 `β₃` (sanity) | −0.019748175274401 | −0.019748175274366 | 3.4 × 10⁻¹⁴ |

t = −4.055; p (t, 94 df) = 1.03 × 10⁻⁴; 95% CI [−0.02912, −0.00998]. The manuscript Table 2 row
("Drop China and Saudi Arabia; re-standardize coverage | −1.955 | p ≈ 0.00010; 95,909 / 95") is
reproduced on both point estimate and inference.

## Status

`CODEX-S5-DB-INTEGRITY-20260910-001` interaction: `ESTIMATED_UNVERIFIED` → **`INDEPENDENTLY_REPRODUCED`**.
SELFREVIEW C6 is closed: the registered coverage reversal is not driven by the two economies with
documented *Getting Credit* irregularities. The general moderator measurement-risk limitation
(discontinued source, disclosed in manuscript §3.2 and §7) stands.

**Artifacts:** `code/study_05_crosscountry/CLAUDE-S5R-DB-INTEGRITY-20260910-001_reproduce.py`
(SHA-256 `0aea3d49…b090e`) · `results/stage4_repro/CLAUDE-S5R-DB-INTEGRITY-20260910-001/result.json`
