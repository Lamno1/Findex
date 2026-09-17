# CLAUDE-S5R-20260910-001 — Stage 4 Independent Reproduction

**Date:** 2026-09-10
**Study:** `study_05_findex_crosscountry` · Hypothesis `H-000500` · Experiment `EXP-S5-001`
**Executed by:** Claude (Lead Co-Author), independent of Codex
**Reproduces:** `CODEX-S5-EXP-20260909-002`, `CODEX-S5-M6-2-20260909-001`,
`CODEX-S5-TABLES-20260909-001`, `CODEX-S5-AUDIT-20260909-001`
**Integrity basis:** `docs/EMPIRICAL_INTEGRITY_PROTOCOL.md`; `CLAIM_CONTRACT.md` lines 83–85;
`CODEX_EXECUTION_BRIEF.md` Stage 4(a)

---

## Verdict

**PASS — the Stage 2/3 results are INDEPENDENTLY REPRODUCED.**

A cold re-implementation, written only from the frozen contracts and run under a distinct
run ID, reproduces **41 of 44** comparable quantities (those carrying a Codex target in
`comparison.csv`) to `|Δ| < 5 × 10⁻¹³` (floating-point noise from linear-algebra ordering).
This includes every number that a claim-contract verdict depends on. The three quantities
that differ belong to two secondary, non-primary diagnostics — the M2c joint-test statistic
form (1), and the fixed-effect logit and probit interaction marginal effects (2); all three
preserve sign and significance and none bears on a claim verdict.
*(Count corrected 2026-09-10 to match `comparison.csv`; an earlier "43 of 45" hand-count is
superseded — see `research_council/reports/TABLEAUDIT-20260910T045000Z` D1.)*

The Stage 3 substantive conclusion stands, now verified:

| Claim | Verdict | Status after Stage 4 |
|---|---|---|
| C1 — digital payment ↔ formal borrowing, within economy | `SUPPORTED_DESCRIPTIVE` | **reproduced** (+0.03617, cluster SE 0.00514) |
| **C2 / H-000500** — association larger where 2019 coverage lower | `NOT_SUPPORTED — OPPOSITE SIGN` | **reproduced** (b3 = −0.01975, cluster SE 0.00474, p ≈ 6.8e-5) |
| C3 — receive > make mechanism | `NOT_SUPPORTED` | **reproduced** (make 0.05172 > receive 0.04080; both interactions ≤ 0) |
| C4 — informal-borrowing placebo ≈ 0 | `NOT_SUPPORTED` | **reproduced** (informal b3 = +0.01736, p ≈ 0.005 — wrong direction for the substitution reading) |
| C5 — Vietnam positioning | descriptive only | fitted VNM slope +0.0507 (95% CI +0.039, +0.063) — descriptive, no Vietnam effect |

**H-000500 is not supported.** The pre-registered coverage-substitution prediction is
rejected with the interaction carrying the opposite sign, robustly. Causal, novelty,
mechanism, and "H-000500 supported" language remain prohibited (`CLAIM_CONTRACT.md`).

---

## What "independent" means here

| Dimension | Codex Stage 2/3 | This reproduction |
|---|---|---|
| Run ID | `CODEX-S5-EXP-20260909-002` etc. | `CLAUDE-S5R-20260910-001` |
| Agent | Codex | Claude |
| Code | `code/study_05_crosscountry/*_codex.py` (**not opened**) | `code/study_05_crosscountry/CLAUDE-S5R-20260910-001_reproduce.py` |
| Build | pandas pipeline | separately re-written pandas pipeline from `VARIABLE_CONTRACT.md` |
| Estimator | (not inspected) | hand-rolled WLS via normal equations + explicit economy-dummy FE + CR1 cluster covariance `c₁ = G/(G−1)·(N−1)/(N−k)`; logit/probit via `statsmodels` GLM dummy-variable FE |
| Codex numeric outputs | — | read **only** to populate comparison targets, never the code |

Frozen-contract SHA-256 re-verified identical to `CODEX-S5-REVISION2-FREEZE-001` for all 7
files (`CLAIM_CONTRACT.md`, `PREREGISTRATION.md`, `VARIABLE_CONTRACT.md`,
`REVISION_1_RESPONSE.md`, `REVISION_2_RESPONSE.md`, `H-000500.json`,
`STUDY_05_RAW_MANIFEST.json`). Raw-input SHA-256 re-verified identical to the manifest for
all 4 files (Findex workbook, 2019 Doing Business snapshot, 2 WDI controls).

---

## Panel — exact match

| Quantity | Codex Stage 1 | Reproduction |
|---|---|---|
| Rows after `fin22a ∈ {1,2}` | 102,644 (98 economies) | 102,644 (98) |
| Final primary frame | **100,560 rows, 97 economies** | **100,560 rows, 97 economies** |
| Economy that exits (all `inc_q` missing) | LSO at `inc_q` step | LSO at `inc_q` step |
| `formal_borrow` = 1 in frame | (10,214 implied) | 10,214 |
| `any_cov` median | 40.4 | 40.4 |
| M3 complete-case frame | 90,118 rows, 89 economies | 90,118, 89 |
| Secondary non-missing: mobile / emergency / informal | 100,452 / 97,540 / 100,428 | 100,452 / 97,540 / 100,428 |

Sequential drop table reproduced step for step
(`results/stage4_repro/CLAUDE-S5R-20260910-001/drop_table.csv`).

---

## Estimate comparison (all 41 exact-match quantities)

`EXACT_MATCH` = `|repro − codex| < 1e-8`. Full file:
`results/stage4_repro/CLAUDE-S5R-20260910-001/comparison.csv`.

### Primary + moderation
| Term | Codex | Reproduction | |Δ| |
|---|---|---|---|
| M1 `b1` (anydigpayment) | 0.036174762453908 | 0.036174762453943 | 3.5e-14 |
| M2 `b1` | 0.039570863861807 | 0.039570863861734 | 7.2e-14 |
| **M2 `b3` (anydigpayment × lowcov2019_z)** | **−0.019748175274401** | **−0.019748175274366** | **3.4e-14** |
| M2b `b3` (below-median moderator) | −0.039581900711075 | −0.039581900711005 | 7.0e-14 |

### Mechanism (M3)
| Term | Codex | Reproduction | |Δ| |
|---|---|---|---|
| M3a receive_dig | 0.040796439382868 | 0.040796439382873 | 5.0e-15 |
| M3a make_dig | 0.051724961219934 | 0.051724961219982 | 4.8e-14 |
| M3b receive × lowcov | −0.002692454871630 | −0.002692454871651 | 2.1e-14 |
| M3b make × lowcov | −0.020210634498915 | −0.020210634498909 | 6.8e-15 |

### Secondary / placebo (M4) — all `b1`, `b3`, and N exact
mobile_loan_app (N 100,452), emergency_loan_source (N 97,540), informal_borrow (N 100,428):
every coefficient matched to `≤ 5e-13`; the informal-borrow interaction reproduces at
**+0.017365** (positive — undermines the substitution reading, per C4).

### Robustness grid (M6) — all exact
`M6_1_unweighted` −0.021290, `M6_1_population` −0.027832, `M6_3_drop_high_income` −0.020503
(N 94,682 / G 91), `M6_4_lowdepth2019_z` −0.005251, `M6_4_lowrights2019_z` +0.007048,
`M6_5_country_controls` −0.023540, `M6_6_n≥500` −0.019748, `M6_8_internet` −0.020478,
`M6_10_inwork` −0.018961 (N 96,925 / G 96). Every |Δ| ≤ 4.3e-13. **b3 survives every M6
branch with the negative sign** — i.e. the H-000500 "supported" decision rule
(`PREREGISTRATION.md` §6) is not met, confirmed.

### Stage 3 adversarial — all exact
- Drop-one-control (7 checks): all reproduced, all negative, |Δ| ≤ 1.5e-13.
- `account_holders_only`: −0.008027 (N 55,429), p ≈ 0.22 — reproduced; precision does depend
  on including non-account-holders.
- `drop_zero_coverage` −0.021215 (N 99,059 / G 95); `drop_lowest_quartile` −0.028797
  (N 76,108 / G 72) — reproduced.
- Leave-one-region-out (7): all reproduced to ≤ 5.5e-14, range −0.02187 … −0.01412, all negative.
- `sign_reversal`: +0.019748175274366 = exact algebraic negation of M2 `b3` — reproduced;
  the direction is not a coding/label artifact.
- Leave-one-economy-out (97 fits): all 97 negative, range **−0.02164 … −0.01737** — matches
  Codex's reported range; the result is not driven by < 5 economies.

---

## The two differences (both non-material, both documented)

### 1. M2c joint bureau+registry Wald statistic
Codex `wald_chi2 = 13.537` (df 2). Reproduction: 15.531 with `account_fin × {lowbureau,
lowregistry}` interactions retained (paralleling M2's `account_fin × moderator`), 3.296
without them. Codex's `PREREGISTRATION.md` §3 asks for "F-form with G-1 denominator df"; this
reproduction computed the χ² form and the account-interaction treatment is under-specified in
the contract. **All three variants reject H₀ decisively** (χ²(2) ≫ critical value), and M2b,
M6.4 and the base M2 all independently confirm the negative direction. No claim verdict
depends on M2c. Logged as a specification-ambiguity difference, not a reproduction failure.

### 2. M6.2 fixed-effect logit / probit interaction AME
Codex: logit −0.013481, probit −0.013575. Reproduction: −0.015018, −0.014738 (≈ 11% larger
in magnitude, same sign). The average marginal effect of a **product term** in a 97-dummy FE
GLM is definition-sensitive (whether the cross-partial includes the β_dig term; dummy vs
demeaned FE; density evaluation point; solver tolerance). Codex's own Stage 3 audit flags
M6.2 as "sign-direction sensitivity only … should not be used as primary inference"
(`CODEX_S5_STAGE3_FINAL_AUDIT.md`). Both implementations agree the non-linear interaction is
**negative**, consistent with the LPM. Non-material.

### Not compared
- **Wild-cluster bootstrap p-values** were not recomputed (seed-dependent; the reproduction
  target is the point estimates and cluster-robust SEs, both matched). Codex's wild p-values
  were all ≈ 0.001–0.003.
- **M5 heterogeneity** (BH secondary family) has no numeric baseline in the Stage-3
  artifacts; the reproduction computed it for completeness (`estimates.json`): x`educ` triple
  −0.0211, x`inc_q` −0.0038, x`female_d` +0.0076 (ns), x`region` joint Wald 79.9. No Codex
  value to check against.

---

## Artifacts (write-once, `results/stage4_repro/CLAUDE-S5R-20260910-001/`)

| File | Contents |
|---|---|
| `code/study_05_crosscountry/CLAUDE-S5R-20260910-001_reproduce.py` | the cold implementation (`code_sha256` in the receipt) |
| `analysis_panel.csv` | reproduced 100,560-row analysis frame |
| `drop_table.csv` | sequential sample-construction table |
| `comparison.csv` | every reproduced quantity vs Codex + `abs_diff` + status |
| `estimates.json` | full reproduction coefficient set |
| `run_receipt.json` | run metadata, input/output SHA-256, environment, verdict |

Environment: Python 3.13.2, numpy 2.4.4, pandas 2.3.1, statsmodels 0.15.0, Windows 11.
Seed 20260910. Runtime ≈ 126 s.

---

## Evidence-status change

`EXP-S5-001` LPM results (M1–M6, Stage-3 checks): `ESTIMATED_UNVERIFIED` →
**`INDEPENDENTLY_REPRODUCED`**. The evidence chain in `CLAIM_CONTRACT.md` lines 83–85 is now
complete through `INDEPENDENT_RUN_ID = CLAUDE-S5R-20260910-001`.

The M6.2 non-linear AME magnitude remains `ESTIMATED_UNVERIFIED` (sign reproduced, magnitude
not); it is a non-primary diagnostic and Codex already down-weighted it.

## Recommended next steps (held pending owner review — the requested stop point)

1. Append a `revision_history` entry to `H-000500.json` recording Stages 1–3 completion, the
   Stage-4 reproduction, `tests_completed`, and `reproduction_status = INDEPENDENTLY_REPRODUCED`
   (currently still says `NOT_APPLICABLE_NO_ESTIMATION`).
2. Register the reproduction in the evidence ledger (`evidence-management`).
3. Only then: draft the UEH competition manuscript **strictly within `CLAIM_CONTRACT.md`** —
   an honest paper about a positive individual-level association plus a cleanly rejected
   pre-registered moderation hypothesis — then run `literature-review` and
   `peer-reviewer-simulation-q1`, then convert to the UEH template.

**No manuscript text, evidence-ledger entry, or hypothesis-file edit has been made in this
session.** Study 1 untouched.
