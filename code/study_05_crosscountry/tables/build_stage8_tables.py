"""Study 5 — Stage 8 manuscript table builder (Stage 15 automation).

Reads ONLY immutable Stage 5 / Stage 5.1 analysis outputs and emits the two
tab_stage8_*.tex fragments that papers/study_05/manuscript/body_stage8.tex
\\input{}s. No coefficient, SE, p-value or N is typed into a .tex file by
hand; every number here is read from a results file and formatted.

This script is independent of, and does not modify, code/study_05_crosscountry
/tables/build_tables.py, which builds the older tab_{sample,primary,...}.tex
set for the frozen H-000500/H-000501 manuscript (body.tex). The two table
sets serve different, non-interchangeable manuscripts.

Sources (all immutable Stage 5 / Stage 5.1 artifacts):
  results/stage5_estimation/estimates.csv               -> primary digital_payment /
                                                             dig_x_lowcov (2021, 2024);
                                                             pooled dig_x_lowcov,
                                                             dig_x_lowcov_x_wave
  results/stage5_1_reconciliation/wild_cluster_bootstrap.csv
                                                          -> wild_p_rademacher for the
                                                             same four (specification,
                                                             term) rows

Outputs: papers/study_05/manuscript/tables/tab_stage8_primary.tex
         papers/study_05/manuscript/tables/tab_stage8_pooled.tex

Usage:  python code/study_05_crosscountry/tables/build_stage8_tables.py
"""
from __future__ import annotations

import csv
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
S5 = PROJECT / "results/stage5_estimation"
S51 = PROJECT / "results/stage5_1_reconciliation"
OUT_TAB = PROJECT / "papers/study_05/manuscript/tables"


def read_csv_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def index_by_spec_term(rows: list[dict]) -> dict:
    return {(r["specification"], r["term"]): r for r in rows}


def stars(p_str: str) -> str:
    p = float(p_str)
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def fmt_pp(estimate_str: str, signed: bool = False) -> str:
    v = float(estimate_str) * 100.0
    if signed:
        return f"{v:+.2f}"
    return f"{v:.2f}"


def fmt_se(se_str: str) -> str:
    return f"({float(se_str) * 100.0:.2f})"


def fmt_int(n_str: str) -> str:
    return f"{int(n_str):,}"


def fmt_p(p_str: str) -> str:
    p = float(p_str)
    return f"{p:.3f}".lstrip("0") if p < 1 else f"{p:.3f}"


def texttt_path(path: str) -> str:
    """LaTeX \\texttt{} for a file path: escapes underscores and inserts
    \\allowbreak after each slash so long paths in the Notes minipage don't
    produce an overfull hbox (Stage 16 finding)."""
    escaped = path.replace("_", "\\_").replace("/", "/\\allowbreak{}")
    return "\\texttt{" + escaped + "}"


def build_primary(est: dict, boot: dict) -> str:
    dp21 = est[("PRIMARY_M1_M2_2021", "digital_payment")]
    dp24 = est[("PRIMARY_M1_M2_2024", "digital_payment")]
    ix21 = est[("PRIMARY_M1_M2_2021", "dig_x_lowcov")]
    ix24 = est[("PRIMARY_M1_M2_2024", "dig_x_lowcov")]
    w21 = boot[("PRIMARY_2021", "dig_x_lowcov")]
    w24 = boot[("PRIMARY_2024", "dig_x_lowcov")]

    assert ix21["N"] == dp21["N"] and ix21["G"] == dp21["G"]
    assert ix24["N"] == dp24["N"] and ix24["G"] == dp24["G"]
    assert w21["estimate"] == ix21["estimate"], "wild-bootstrap row does not match estimates.csv 2021 interaction"
    assert w24["estimate"] == ix24["estimate"], "wild-bootstrap row does not match estimates.csv 2024 interaction"

    dp21_s = fmt_pp(dp21["estimate"]) + stars(dp21["p_cluster"])
    dp24_s = fmt_pp(dp24["estimate"]) + stars(dp24["p_cluster"])
    ix21_s = fmt_pp(ix21["estimate"]) + stars(ix21["p_cluster"])
    ix24_s = fmt_pp(ix24["estimate"]) + stars(ix24["p_cluster"])

    wp21 = f"{float(w21['wild_p_rademacher']):.3f}"
    wp24 = f"{float(w24['wild_p_rademacher']):.3f}"

    return f"""\\begin{{table}}[htbp]
\\centering
\\caption{{Primary separate-wave estimates, 2021 and 2024}}
\\label{{tab:stage8primary}}
\\begin{{adjustbox}}{{max width=\\textwidth}}
\\begin{{tabular}}{{lrr}}
\\toprule
 & 2021 & 2024 \\\\
\\midrule
Digital payment association (pp) & {dp21_s} & {dp24_s} \\\\
Payment $\\times$ lower 2019 coverage (pp) & {ix21_s} & {ix24_s} \\\\
Clustered SE, interaction (pp) & {fmt_se(ix21['se_cluster'])} & {fmt_se(ix24['se_cluster'])} \\\\
Wild-cluster $p$, interaction & {wp21} & {wp24} \\\\
Observations & {fmt_int(ix21['N'])} & {fmt_int(ix24['N'])} \\\\
Economies & {ix21['G']} & {ix24['G']} \\\\
\\bottomrule
\\end{{tabular}}
\\end{{adjustbox}}
\\smallskip
\\begin{{minipage}}{{\\linewidth}}\\footnotesize \\emph{{Notes.}}
Survey-weighted WLS linear probability models with economy fixed effects and
economy-clustered standard errors. The exposure is qualified-comparable across
2021--2024, not asserted to be perfectly invariant. Coefficients are percentage
points. Wild-cluster inference uses 999 null-imposed cluster-score Rademacher
replications. *** denotes clustered $p<0.01$, ** $p<0.05$, * $p<0.10$.
Generated by {texttt_path('code/study_05_crosscountry/tables/build_stage8_tables.py')}
from {texttt_path('results/stage5_estimation/estimates.csv')} and
{texttt_path('results/stage5_1_reconciliation/wild_cluster_bootstrap.csv')}.\\end{{minipage}}
\\end{{table}}
"""


def build_pooled(est: dict, boot: dict) -> str:
    ix = est[("SECONDARY_POOLED_2021_2024", "dig_x_lowcov")]
    triple = est[("SECONDARY_POOLED_2021_2024", "dig_x_lowcov_x_wave")]
    w_ix = boot[("SECONDARY_POOLED_2021_2024", "dig_x_lowcov")]
    w_triple = boot[("SECONDARY_POOLED_2021_2024", "dig_x_lowcov_x_wave")]

    assert w_ix["estimate"] == ix["estimate"], "wild-bootstrap row does not match estimates.csv pooled interaction"
    assert w_triple["estimate"] == triple["estimate"], "wild-bootstrap row does not match estimates.csv pooled triple interaction"
    assert ix["N"] == triple["N"] and ix["G"] == triple["G"]

    ix_s = fmt_pp(ix["estimate"], signed=False) + stars(ix["p_cluster"])
    triple_s = fmt_pp(triple["estimate"], signed=True) + stars(triple["p_cluster"])
    wp_triple = f"{float(w_triple['wild_p_rademacher']):.3f}"

    return f"""\\begin{{table}}[htbp]
\\centering
\\caption{{Secondary pooled repeated-cross-section parameterization}}
\\label{{tab:stage8pooled}}
\\begin{{tabular}}{{lr}}
\\toprule
Term & Estimate (pp) \\\\
\\midrule
Payment $\\times$ lower 2019 coverage & {ix_s} \\\\
Payment $\\times$ lower coverage $\\times$ 2024 & {triple_s} \\\\
Wild-cluster $p$, triple interaction & {wp_triple} \\\\
Observations & {fmt_int(ix['N'])} \\\\
Economies & {ix['G']} \\\\
\\bottomrule
\\end{{tabular}}
\\smallskip
\\begin{{minipage}}{{0.92\\linewidth}}\\footnotesize \\emph{{Notes.}}
This is a descriptive pooled parameterization. The 2019 moderator is fixed across
waves, so the triple interaction is a temporal contrast and not an institutional-change
effect. The pooled-implied gradients need not equal the separate-wave coefficients
because nuisance slopes and interaction terms are jointly estimated on the pooled sample.
*** denotes clustered $p<0.01$, ** $p<0.05$, * $p<0.10$; the triple interaction is not
significant at conventional levels. Generated by
{texttt_path('code/study_05_crosscountry/tables/build_stage8_tables.py')} from
{texttt_path('results/stage5_estimation/estimates.csv')} and
{texttt_path('results/stage5_1_reconciliation/wild_cluster_bootstrap.csv')}.
\\end{{minipage}}
\\end{{table}}
"""


def main() -> None:
    est = index_by_spec_term(read_csv_rows(S5 / "estimates.csv"))
    boot = index_by_spec_term(read_csv_rows(S51 / "wild_cluster_bootstrap.csv"))

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "tab_stage8_primary.tex").write_text(build_primary(est, boot), encoding="utf-8")
    (OUT_TAB / "tab_stage8_pooled.tex").write_text(build_pooled(est, boot), encoding="utf-8")
    print("Wrote tab_stage8_primary.tex and tab_stage8_pooled.tex from immutable Stage 5/5.1 artifacts.")


if __name__ == "__main__":
    main()
