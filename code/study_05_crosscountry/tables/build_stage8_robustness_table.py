"""Study 5 -- Stage 17 robustness table builder.

Reads ONLY the immutable Stage 17 outputs (results/stage17_external_validity/)
and emits tab_stage8_robustness.tex, which papers/study_05/manuscript/
body_stage8.tex \\input{}s. No coefficient, SE, p-value or N is typed into a
.tex file by hand -- mirrors the "no hand-typed numbers" discipline Stage 15
established for build_stage8_tables.py (which this script does not modify;
the two scripts read disjoint result sets and serve different table sets).

Sources:
  results/stage17_external_validity/inclusion_logit.json
  results/stage17_external_validity/reweighted_estimates.csv
  results/stage17_external_validity/macro_control_estimates.csv

Output: papers/study_05/manuscript/tables/tab_stage8_robustness.tex

Usage: python code/study_05_crosscountry/tables/build_stage8_robustness_table.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parents[3]
S17 = PROJECT / "results/stage17_external_validity"
OUT_TAB = PROJECT / "papers/study_05/manuscript/tables"


def texttt_path(path: str) -> str:
    escaped = path.replace("_", "\\_").replace("/", "/\\allowbreak{}")
    return "\\texttt{" + escaped + "}"


def stars(p) -> str:
    if p is None or pd.isna(p):
        return ""
    p = float(p)
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def pp(v: float, signed: bool = False) -> str:
    val = float(v) * 100.0
    return f"{val:+.2f}" if signed else f"{val:.2f}"


def se(v: float) -> str:
    return f"({float(v) * 100.0:.2f})"


def build() -> str:
    logit = json.loads((S17 / "inclusion_logit.json").read_text(encoding="utf-8"))
    rw = pd.read_csv(S17 / "reweighted_estimates.csv").set_index("wave")
    mc = pd.read_csv(S17 / "macro_control_estimates.csv")

    ov = logit["overlap"]
    cls = logit["item1_classification"]

    def rw_row(wave: int, col: str) -> str:
        r = rw.loc[wave]
        return f"{pp(r[col])}"

    m21 = mc[(mc.wave == 2021)].set_index("term")
    m24 = mc[(mc.wave == 2024)].set_index("term")

    def mc_cell(m: pd.DataFrame, term: str) -> str:
        r = m.loc[term]
        return pp(r["estimate"]) + stars(r["p_cluster"])

    def mc_se(m: pd.DataFrame, term: str) -> str:
        return se(m.loc[term, "se_cluster"])

    return f"""\\begin{{table}}[htbp]
\\centering
\\caption{{Stage 17 additional robustness: external-validity reweighting and macro-control interactions}}
\\label{{tab:stage8robustness}}
\\begin{{adjustbox}}{{max width=\\textwidth}}
\\begin{{tabular}}{{lrr}}
\\toprule
\\multicolumn{{3}}{{l}}{{\\textit{{Panel A: IPW reweighting toward the {logit['excluded_n']} excluded, mostly high-coverage economies}}}} \\\\
 & 2021 & 2024 \\\\
\\midrule
Primary $\\times$ lower-coverage interaction (pp) & {rw_row(2021,'primary_estimate')} & {rw_row(2024,'primary_estimate')} \\\\
IPW-reweighted interaction (pp) & {rw_row(2021,'reweighted_estimate')} & {rw_row(2024,'reweighted_estimate')} \\\\
Clustered SE, reweighted (pp) & {se(rw.loc[2021,'se_cluster'])} & {se(rw.loc[2024,'se_cluster'])} \\\\
Wild-cluster $p$, reweighted & {rw.loc[2021,'wild_p_rademacher']:.3f} & {rw.loc[2024,'wild_p_rademacher']:.3f} \\\\
Relative change vs.\\ primary & {rw.loc[2021,'relative_change_vs_primary']*100:.1f}\\% & {rw.loc[2024,'relative_change_vs_primary']*100:.1f}\\% \\\\
\\addlinespace
\\multicolumn{{3}}{{l}}{{Inclusion logit $c$-statistic: {logit['c_stat']:.3f}; economies outside common support: {ov['outside_count']} of {logit['frame_133_n']}}} \\\\
\\multicolumn{{3}}{{l}}{{Max IPW weight after 1st/99th trim: {ov['max_ipw_after_trim']:.2f}; Kish ESS: {ov['kish_ess']:.1f} of {logit['included_n']}}} \\\\
\\multicolumn{{3}}{{l}}{{\\textbf{{Classification: {cls.replace('_',' ')}}}}} \\\\
\\addlinespace
\\multicolumn{{3}}{{l}}{{\\textit{{Panel B: digital-payment interactions with log GDP per capita and account-ownership rate}}}} \\\\
 & 2021 & 2024 \\\\
\\midrule
Payment $\\times$ lower coverage (pp), with macro controls & {mc_cell(m21,'dig_x_lowcov')} & {mc_cell(m24,'dig_x_lowcov')} \\\\
 & {mc_se(m21,'dig_x_lowcov')} & {mc_se(m24,'dig_x_lowcov')} \\\\
Payment $\\times$ log GDP per capita (pp) & {mc_cell(m21,'dig_x_lgdppc')} & {mc_cell(m24,'dig_x_lgdppc')} \\\\
 & {mc_se(m21,'dig_x_lgdppc')} & {mc_se(m24,'dig_x_lgdppc')} \\\\
Payment $\\times$ account-ownership rate (pp) & {mc_cell(m21,'dig_x_accrate')} & {mc_cell(m24,'dig_x_accrate')} \\\\
 & {mc_se(m21,'dig_x_accrate')} & {mc_se(m24,'dig_x_accrate')} \\\\
\\addlinespace
\\multicolumn{{3}}{{l}}{{Primary (no macro controls) interaction (pp): {rw_row(2021,'primary_estimate')} (2021), {rw_row(2024,'primary_estimate')} (2024)}} \\\\
\\bottomrule
\\end{{tabular}}
\\end{{adjustbox}}
\\smallskip
\\begin{{minipage}}{{\\linewidth}}\\footnotesize \\emph{{Notes.}}
Panel A: inverse-selection weighting ($1/\\hat p$, trimmed at the 1st/99th percentile,
combined multiplicatively with the primary economy-equal weight), following the
same protocol as {texttt_path('H-000501')}'s Q5 module-selection check, adapted to a
different target frame (economies present in both raw 2021 and 2024 Findex releases).
Classification follows the same three-way rule: \\emph{{stable}} requires adequate common
support; the {ov['outside_count']}-of-{logit['frame_133_n']} economies outside common support here
force \\emph{{not transportable}} regardless of the reweighted point estimate's own stability.
Panel B: digital\\_payment $\\times$ log-GDP-per-capita and digital\\_payment $\\times$
account-ownership-rate terms are added \\emph{{in place of}} lower-coverage interactions
with these macro covariates, because the latter are collinear with the economy fixed
effects already in M2 (both a covariate constant within economy and its interaction with
another economy-constant covariate are absorbed by \\texttt{{C(economycode)}}). *** denotes
clustered $p<0.01$, ** $p<0.05$, * $p<0.10$. Both panels are exploratory/diagnostic
robustness, not pre-registered or confirmatory. Generated by
{texttt_path('code/study_05_crosscountry/tables/build_stage8_robustness_table.py')} from
{texttt_path('results/stage17_external_validity/')}.
\\end{{minipage}}
\\end{{table}}
"""


def main() -> None:
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "tab_stage8_robustness.tex").write_text(build(), encoding="utf-8")
    print("Wrote tab_stage8_robustness.tex from Stage 17 immutable artifacts.")


if __name__ == "__main__":
    main()
