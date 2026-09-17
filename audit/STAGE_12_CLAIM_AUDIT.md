# STAGE 12 — CLAIM-BY-CLAIM AUDIT (Phase L)

| # | Claim | Empirical source | Independently reproduced? | Evidence | Interpretation valid? |
|---|---|---|---|---|---|
| 1 | Positive association: digital payments ↔ formal borrowing | `estimates.csv`, both waves | YES | +9.07pp (2021), +8.13pp (2024), independently reproduced (see Replication Report) | Valid as stated (association, not causal language used in body text) |
| 2 | Negative interaction with low 2019 credit-info coverage | `estimates.csv` / `wild_cluster_bootstrap.csv` | YES | -1.74pp (2021, wild p=0.002), -1.61pp (2024, wild p=0.020), independently reproduced point estimates; bootstrap code-reviewed, not bit-for-bit re-executed | Valid but see Gate P0 — governance status caps evidentiary weight regardless of numeric correctness |
| 3 | Replicated in both 2021 and 2024 | Same as #2 | YES (numerically) | Both waves independently reproduced | Valid descriptively; "replicated" is used loosely — see prohibited-interpretations note below |
| 4 | "Persistence across waves" | body_stage8.tex | Descriptive claim about the pattern, not a separate statistical test | N/A (not a coefficient) | Manuscript explicitly disclaims it as proof of a persistent mechanism ("does not distinguish a recurring economic relationship... from a recurring selection/measurement structure," line 148) — **appropriately hedged** |
| 5 | Leave-one-economy-out robustness (all 93 negative) | `leave_one_economy_out.csv` | YES | All 186 (93×2) independently tabulated as negative; ranges match manuscript | Valid; manuscript correctly frames this as sign-robustness only, not magnitude-stability |
| 6 | Pooled interaction ≈ -1.98pp | `estimates.csv` / `wild_cluster_bootstrap.csv` | YES (point estimate); bootstrap p=0.001 code-reviewed | -0.019841 independently confirmed via csv cross-check (not independently re-fit with fresh code in this session — lower priority than the two primary separate-wave models) | Valid |
| 7 | Non-significant three-way wave interaction (p=0.305) | Same | Bootstrap not re-executed; point estimate consistent | +0.0058, wild p=0.305 | Manuscript correctly does NOT claim this proves coefficient equality across waves ("no new equality hypothesis test was pre-specified," `stage5_1_receipt.json`) — **appropriately hedged, satisfies rule 9** |
| 8 | 2019 coverage as historical/fixed moderator | Design description | Confirmed in code: `lowcov_z` derived once from a 2019-only cross-section, applied identically to both waves | N/A | Valid; matches design |
| 9 | Account access as selection-sensitive, not mechanism | body_stage8.tex | Confirmed by direct text ("does not identify account access as the mechanism") | N/A | Valid, appropriately hedged |
| 10 | 2017 as contextual evidence only | body_stage8.tex + code | Confirmed — 2017 not used in any Stage 4/5 regression | N/A | Valid |

## Prohibited-interpretation scan (Section 16 of the brief)

Full-text scan of `body_stage8.tex` for causal/mechanism/proof language:
- No instance of "causal effect," "identifies the mechanism," "proves," "demonstrates
  supply-side rationing," or "universal" was found applied to the digital-payment/coverage
  result.
- The manuscript is explicit and repeated in disclaiming mechanism identification: "does not
  identify whether the boundary reflects access selection, lender processing, supply
  constraints, measurement, or distinct lending technologies" (Stage 9 audit text, echoed in
  body_stage8.tex's conclusion).
- One phrase warrants flagging: body_stage8.tex line 11, **"Contrary to the registered
  prediction, the interaction ... is negative in 2021 ... and 2024"** — this is not a
  causal/mechanism overclaim in the Section 16 sense, but it is a **governance-relevant
  overclaim**: it invokes the credibility of "the registered prediction" (from
  H-000500/H-000501, a single-wave 97-economy design) to frame the result of an
  *unregistered* 93-economy two-wave design, without disclosing that this specific design
  was never itself pre-registered. This is the clearest textual instance of the Phase 0
  violation surfacing inside the manuscript's own prose, and is flagged as a required
  manuscript correction (see Gate Decision).

## Overall claim-audit finding

At the level of individual numeric claims, the manuscript is unusually disciplined:
hedging language is present nearly everywhere the brief asks it to be checked, no
prohibited causal/mechanism/equality language was found, and every headline number that was
checked reproduced. **The failure in this project is not primarily in the individual
claims' wording — it is that the entire evidentiary base for those (accurately, honestly
worded) claims rests on a research design that was never legitimately authorized before its
results were seen (Gate P0), and the manuscript's own framing ("contrary to the registered
prediction") obscures that fact rather than disclosing it.**
