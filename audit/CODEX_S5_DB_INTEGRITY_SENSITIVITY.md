# CODEX-S5-DB-INTEGRITY-20260910-001

Date: 2026-09-10  
Concern: SELFREVIEW C6 — integrity history of the Doing Business moderator  
Verdict: **PASS_SENSITIVITY; MEASUREMENT_LIMITATION_REMAINS**

The World Bank's December 2020 review identified irregular changes affecting *Getting
Credit* for China in the Doing Business 2018 cycle and Saudi Arabia in the Doing Business
2020 cycle. Both economies are in Study 5. This sensitivity therefore excludes `CHN` and
`SAU` simultaneously and re-standardizes `any_cov` across the remaining economies (`ddof=0`)
before re-estimating the frozen M2 specification.

The restricted frame contains **95,909 adults in 95 economies**. The interaction of digital
payment activity with lower credit-information coverage is **−0.019548** per re-standardized
economy-level SD (economy-clustered SE **0.004820**, p = **0.000103**, 95% CI
**[−0.029119, −0.009977]**). The estimate is close to the baseline −0.019748 and retains the
same negative sign and inference.

This check shows that the registered coverage result is not driven by the two in-sample
economies specifically implicated in *Getting Credit* irregularities. It does not validate
the Doing Business production process or eliminate general moderator measurement error.

Artifacts:

- Code: `code/study_05_crosscountry/db_integrity_sensitivity.py`
- Result: `results/stage3/CODEX-S5-DB-INTEGRITY-20260910-001/result.json`
- Receipt: `results/stage3/CODEX-S5-DB-INTEGRITY-20260910-001/receipt.json`
- Immutable input panel SHA-256: `ac7077297c2c107f1354861f5c3c2d688d5c455cc013da39c7361f161bc3a8a9`

Source: World Bank (2020), *Review of Data Irregularities in Doing Business*, 16 December.

