"""
Study 5  --  STAGE 4 INDEPENDENT REPRODUCTION
============================================
RUN_ID              : CLAUDE-S5R-20260910-001
Executed by         : Claude (Lead Co-Author) -- independent of Codex
Reproduces          : CODEX-S5-EXP-20260909-002 / CODEX-S5-M6-2-20260909-001 /
                      CODEX-S5-TABLES-20260909-001 / CODEX-S5-AUDIT-20260909-001
Integrity basis     : docs/EMPIRICAL_INTEGRITY_PROTOCOL.md ; CLAIM_CONTRACT.md lines 83-85 ;
                      CODEX_EXECUTION_BRIEF.md Stage 4.

This is a COLD re-implementation. No Codex source file was opened. The pipeline was written
only from the frozen contracts:
    papers/study_05/PREREGISTRATION.md      (b959ae5b...)
    papers/study_05/VARIABLE_CONTRACT.md    (9a71ee5f...)
    papers/study_05/CLAIM_CONTRACT.md       (d4d704be...)
    research_council/hypotheses/H-000500.json (5bcd560b...)
    data/STUDY_05_RAW_MANIFEST.json         (1bce876c...)
Codex's numeric outputs (result.json / tables / adversarial_checks.json) were read ONLY to
populate the comparison targets below -- never its code.

Estimator: hand-rolled weighted least squares via normal equations (numpy), economy fixed
effects as explicit dummies, CR1 cluster-robust covariance
    c1 = G/(G-1) * (N-1)/(N-rank(X))   ,   V = (X'WX)^-1  [sum_g s_g s_g']  (X'WX)^-1
Logit/probit (M6.2 only) via statsmodels GLM with dummy-variable fixed effects.
Wild-cluster bootstrap p-values are NOT recomputed here (seed-dependent secondary diagnostic);
the reproduction target is the point estimates and the cluster-robust standard errors.
"""
import json, hashlib, time, sys, platform, os
import numpy as np
import pandas as pd

ROOT   = r"D:\EconomicResearch"
SUB    = ROOT + r"\projects\study_05_findex_crosscountry"
FINDEX = ROOT + r"\data\raw\data_micro_findex_2024_vietnam.xlsx"
SHEET  = "findex_microdata_2025_labelled_"
SNAP   = SUB + r"\data\raw\wb_credit_information_latest_snapshot.csv"
GDP    = SUB + r"\data\raw\wdi_NY.GDP.PCAP.CD_2000_2023.json"
PC     = SUB + r"\data\raw\wdi_FS.AST.PRVT.GD.ZS_2000_2023.json"
OUTDIR = SUB + r"\results\stage4_repro\CLAUDE-S5R-20260910-001"
SEED   = 20260910

EXPECT_HASH = {
    FINDEX: "ca307a0c3dfd54dc945a18fb03c58b014143bc21c90761f71fe304e6a2f90fce",
    SNAP:   "ef0c67f9c7d44b67939e088f0aab2e578f7ba0d7f2eeadc4093c0103cc1bd06c",
    GDP:    "e7921b98db185e568c7d07dd5c094eb3dbf8e56ca11ba08a15f6d9abe34dcacd",
    PC:     "ad301883321da15e2cfcf6a0fefb569565d8efc7c77f1ba5ee3ae540c77dc953",
}

# ---- Codex frozen targets (numbers only, from Stage 2/3 result artifacts) -----------------
TGT = {
    "M1_b1":        ( 0.03617476245390756,  0.005142845649763501),
    "M2_b1":        ( 0.03957086386180651,  0.004821203748286039),
    "M2_b3":        (-0.01974817527440055,  0.004742982808612062),
    "M2b_b3":       (-0.03958190071107486,  0.009702020596679014),
    "M3a_receive":  ( 0.04079643938286839,  0.005777957350239981),
    "M3a_make":     ( 0.05172496121993399,  0.005443059175505276),
    "M3b_recX":     (-0.0026924548716298793,0.004935763976953187),
    "M3b_makX":     (-0.02021063449891532,  0.004802047834081892),
    "M4_mobile_loan_app_b1":       ( 0.07374862432661605, 0.0070759039951687),
    "M4_mobile_loan_app_b3":       ( 0.01097060598146225, 0.006334299873124821),
    "M4_emergency_loan_source_b1": ( 0.0071752069935735905,0.00325852297750539),
    "M4_emergency_loan_source_b3": (-0.008833904224393539, 0.0038019648487095208),
    "M4_informal_borrow_b1":       ( 0.10661665556432433, 0.007303017741820746),
    "M4_informal_borrow_b3":       ( 0.017364836615067342,0.006089946356240596),
    "M6_1_unweighted":       (-0.021290337017515364, 0.004823897081632595),
    "M6_1_population":        (-0.027831828589299164, 0.007667529370687182),
    "M6_3_drop_high_income":  (-0.020503116420439248, 0.004873052036185022),
    "M6_4_lowdepth2019_z":    (-0.005250530445331064, 0.0039061515344464962),
    "M6_4_lowrights2019_z":   ( 0.007048339426139645, 0.005905426038774831),
    "M6_5_country_controls":  (-0.023540451556239277, 0.007859783104183386),
    "M6_6_n_ge_500":          (-0.01974817527440055,  0.004742982808612062),
    "M6_8_internet":          (-0.020477928293199193, 0.004793790573761657),
    "M6_10_inwork":           (-0.018960829845787876, 0.004844336633698045),
    "M6_2_logit_interaction_AME":  (-0.013480819978387548, 0.004383526323983909),
    "M6_2_probit_interaction_AME": (-0.013575300108900646, 0.0042013015265269914),
    "drop_account_fin": (-0.013948741332297858, None), "drop_female_d": (-0.01965120145091241, None),
    "drop_age_c": (-0.018616213858391933, None), "drop_age_c2": (-0.021905521447844634, None),
    "drop_educ": (-0.020725417635574325, None), "drop_inc_q": (-0.019811956114662018, None),
    "drop_urban_d": (-0.019908667851618968, None),
    "account_holders_only": (-0.008027068742551092, 0.006470899539937452),
    "drop_zero_coverage": (-0.021214914819590383, 0.00476228988417182),
    "drop_lowest_quartile": (-0.028797371851936912, 0.006696756692762958),
    "LORO_East Asia & Pacific (excluding high income)": (-0.020618172161947414, None),
    "LORO_Europe & Central Asia (excluding high income)": (-0.014118930097559473, None),
    "LORO_High income": (-0.020565975773485807, None),
    "LORO_Latin America & Caribbean (excluding high income)": (-0.020051886015385392, None),
    "LORO_Middle East & North Africa (excluding high income)": (-0.020257646031421692, None),
    "LORO_South Asia": (-0.017227410139709614, None),
    "LORO_Sub-Saharan Africa (excluding high income)": (-0.021871334607593045, None),
    "sign_reversal": (0.019748175274400565, 0.004742982808612063),
    "M2c_wald_chi2": (13.536841782539044, None),
}
CODEX_PANEL = dict(N=100560, G=97, N_m3=90118, G_m3=89, formal_borrow_valid_98=102644)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

# ------------------------------------------------------------------------------ build
def zscore0(s):  # population sd (ddof=0), per panel_receipt zscore_ddof
    return (s - s.mean()) / s.std(ddof=0)

def truth_receive(df):
    R = df[["receive_wages", "receive_transfers", "receive_pensions", "receive_agriculture"]]
    any1 = (R == 1).any(axis=1)
    any234 = R.isin([2, 3, 4]).any(axis=1)
    out = pd.Series(np.nan, index=df.index)
    out[any1] = 1.0
    out[(~any1) & any234] = 0.0
    return out

def truth_make(df):
    mp, pu = df["merchantpay_dig"], df["pay_utilities"]
    is1 = (mp == 1) | (pu == 1)
    is0 = (~is1) & ((mp == 0) | pu.isin([2, 3, 4]))
    out = pd.Series(np.nan, index=df.index)
    out[is1] = 1.0
    out[is0 & out.isna()] = 0.0
    return out

def wdi_latest(path, name):
    j = json.load(open(path))[1]
    rows = [(r["countryiso3code"], int(r["date"]), r["value"]) for r in j if r["value"] is not None]
    t = pd.DataFrame(rows, columns=["iso3", "year", name]).query("year <= 2023")
    return t.sort_values(["iso3", "year"]).groupby("iso3").tail(1)

def build():
    cols = ["economy", "economycode", "regionwb", "wgt", "pop_adult", "fin22a", "anydigpayment",
            "account_fin", "female", "age", "educ", "inc_q", "urbanicity", "internet_use", "emp_in",
            "fin20", "fin24", "fin22b", "merchantpay_dig", "pay_utilities",
            "receive_wages", "receive_transfers", "receive_pensions", "receive_agriculture"]
    df = pd.read_excel(FINDEX, sheet_name=SHEET, usecols=cols)
    df["iso3"] = df["economycode"].astype(str)
    df["formal_borrow"]        = np.where(df.fin22a == 1, 1.0, np.where(df.fin22a == 2, 0.0, np.nan))
    df["mobile_loan_app"]      = np.where(df.fin20 == 1, 1.0, np.where(df.fin20 == 2, 0.0, np.nan))
    df["emergency_loan_source"] = np.where(df.fin24 == 4, 1.0,
                                  np.where(df.fin24.isin([1, 2, 3, 5, 6, 7]), 0.0, np.nan))
    df["informal_borrow"]      = np.where(df.fin22b == 1, 1.0, np.where(df.fin22b == 2, 0.0, np.nan))
    df["receive_dig"] = truth_receive(df)
    df["make_dig"]    = truth_make(df)
    df["female_d"]  = (df.female == 1).astype(float)
    df["urban_d"]   = (df.urbanicity == 2).astype(float)
    df["inwork_d"]  = np.where(df.emp_in.notna(), (df.emp_in == 1).astype(float), np.nan)
    df["internet_d"] = df.internet_use.astype(float)

    steps, d = [], df.copy()
    def rec(name): steps.append(dict(step=name, rows=len(d), economies=int(d.iso3.nunique())))
    d = d[d.fin22a.isin([1, 2])];    rec("fin22a_valid_1_or_2")
    d = d[d.anydigpayment.notna()];  rec("anydigpayment_nonmissing")
    d = d[d.account_fin.notna()];    rec("account_fin_nonmissing")
    d = d[d.female.notna()];         rec("female_nonmissing")
    d = d[d.age.notna()];            rec("age_nonmissing")
    d = d[d.educ.notna()];           rec("educ_nonmissing")
    d = d[d.inc_q.notna()];          rec("inc_q_nonmissing")
    d = d[d.urbanicity.notna()];     rec("urbanicity_nonmissing")

    snap = pd.read_csv(SNAP)
    snap["any_cov"] = snap[["credit_bureau_cov_pct", "credit_registry_cov_pct"]].max(axis=1)
    mod = snap[["iso3", "credit_bureau_cov_pct", "credit_registry_cov_pct", "any_cov",
                "depth_credit_info_0_8", "legal_rights_0_12"]].rename(
        columns={"credit_bureau_cov_pct": "bureau_cov", "credit_registry_cov_pct": "registry_cov",
                 "depth_credit_info_0_8": "depth", "legal_rights_0_12": "rights"})
    d = d.merge(mod, on="iso3", how="inner");  rec("moderator_iso3_match")

    ec = d.groupby("iso3").agg(bureau_cov=("bureau_cov", "first"),
                               registry_cov=("registry_cov", "first"),
                               any_cov=("any_cov", "first"),
                               depth=("depth", "first"),
                               rights=("rights", "first")).reset_index()
    ec["lowcov2019_z"]      = -zscore0(ec.any_cov)
    ec["lowbureau2019_z"]   = -zscore0(ec.bureau_cov)
    ec["lowregistry2019_z"] = -zscore0(ec.registry_cov)
    ec["lowdepth2019_z"]    = -zscore0(ec.depth)
    ec["lowrights2019_z"]   = -zscore0(ec.rights)
    ec["lowcov2019_bmedian"] = (ec.any_cov < ec.any_cov.median()).astype(float)

    d = d.merge(ec[["iso3", "any_cov", "lowcov2019_z", "lowbureau2019_z", "lowregistry2019_z",
                    "lowdepth2019_z", "lowrights2019_z", "lowcov2019_bmedian"]], on="iso3", how="left",
                suffixes=("", "_ec"))
    d["age_c"]  = d.age - d.age.mean()
    d["age_c2"] = d.age_c ** 2
    d["w_equal"]      = d.wgt / d.groupby("iso3").wgt.transform("sum")
    d["w_population"]  = d.w_equal * d.pop_adult
    d["w_unweighted"]  = 1.0
    d["educ_2"] = (d.educ == 2).astype(float); d["educ_3"] = (d.educ == 3).astype(float)
    for q in (2, 3, 4, 5):
        d[f"incq_{q}"] = (d.inc_q == q).astype(float)

    g  = wdi_latest(GDP, "gdp_pc"); p = wdi_latest(PC, "privcredit_gdp")
    cc = ec[["iso3"]].merge(g, on="iso3", how="left").merge(p, on="iso3", how="left")
    acct = (d.assign(x=d.w_equal * d.account_fin).groupby("iso3").x.sum()
            / d.groupby("iso3").w_equal.sum())
    cc = cc.merge(acct.rename("acct_own_rate").reset_index(), on="iso3", how="left")
    cc["lgdppc"] = np.log(cc.gdp_pc)
    d = d.merge(cc[["iso3", "lgdppc", "privcredit_gdp", "acct_own_rate"]], on="iso3", how="left")
    return d, ec, cc, pd.DataFrame(steps)

# ------------------------------------------------------------------------------ estimator
CTRL = ["female_d", "age_c", "age_c2", "educ_2", "educ_3",
        "incq_2", "incq_3", "incq_4", "incq_5", "urban_d"]

def design(d, terms):
    X = pd.DataFrame({"const": np.ones(len(d))}, index=d.index)
    for t in terms:
        X[t] = d[t].astype(float)
    X = pd.concat([X, pd.get_dummies(d["iso3"], prefix="fe", drop_first=True).astype(float)], axis=1)
    return X

def wls_cluster(y, X, w, groups):
    y = np.asarray(y, float); Xm = np.asarray(X, float); W = np.asarray(w, float)
    XtWX  = Xm.T @ (Xm * W[:, None])
    bread = np.linalg.pinv(XtWX)
    beta  = bread @ (Xm.T @ (y * W))
    e     = y - Xm @ beta
    codes = pd.factorize(groups)[0]; G = int(codes.max() + 1)
    k     = int(np.linalg.matrix_rank(XtWX))
    sw    = Xm * (W * e)[:, None]
    meat  = np.zeros((Xm.shape[1],) * 2)
    for gg in range(G):
        s = sw[codes == gg].sum(axis=0); meat += np.outer(s, s)
    N  = len(y)
    V  = bread @ meat @ bread * (G / (G - 1) * (N - 1) / (N - k))
    return beta, V, dict(N=N, G=G, k=k)

def C(X, b, V, name):
    j = list(X.columns).index(name)
    return float(b[j]), float(np.sqrt(V[j, j]))

def run_model(d, terms, y="formal_borrow", w="w_equal"):
    X = design(d, terms)
    b, V, info = wls_cluster(d[y], X, d[w], d["iso3"].values)
    return X, b, V, info

# ------------------------------------------------------------------------------ pipeline
def main():
    t0 = time.time()
    print("== hash check ==")
    for p, exp in EXPECT_HASH.items():
        got = sha256(p); ok = got == exp
        print(f"  {'OK ' if ok else 'BAD'} {p.split(chr(92))[-1]:44s} {got[:16]}")
        assert ok, f"hash mismatch {p}"

    d, ec, cc, drop = build()
    os.makedirs(OUTDIR, exist_ok=True)
    drop.to_csv(OUTDIR + r"\drop_table.csv", index=False)
    print("\n== drop table ==\n", drop.to_string(index=False))

    panel_cols = ["iso3", "regionwb", "formal_borrow", "mobile_loan_app", "emergency_loan_source",
                  "informal_borrow", "anydigpayment", "receive_dig", "make_dig", "account_fin",
                  "female_d", "age_c", "age_c2", "educ", "inc_q", "urban_d", "internet_d", "inwork_d",
                  "any_cov", "lowcov2019_z", "lowbureau2019_z", "lowregistry2019_z", "lowdepth2019_z",
                  "lowrights2019_z", "lowcov2019_bmedian", "lgdppc", "privcredit_gdp", "acct_own_rate",
                  "w_equal", "w_population"]
    panel = d[panel_cols].reset_index(drop=True)
    panel.to_csv(OUTDIR + r"\analysis_panel.csv", index=False)

    R = {}   # results:  name -> (coef, se_or_None)
    d["dig_x_lowcov"] = d.anydigpayment * d.lowcov2019_z
    d["acc_x_lowcov"] = d.account_fin  * d.lowcov2019_z
    BASE = ["anydigpayment", "dig_x_lowcov", "account_fin", "acc_x_lowcov"] + CTRL

    X, b, V, i1 = run_model(d, ["anydigpayment", "account_fin"] + CTRL)
    R["M1_b1"] = C(X, b, V, "anydigpayment")
    panel_meta = dict(N=i1["N"], G=i1["G"], k_M1=i1["k"],
                      formal_borrow_sum=float(d.formal_borrow.sum()),
                      any_cov_median=float(ec.any_cov.median()))

    X, b, V, _ = run_model(d, BASE)
    R["M2_b1"] = C(X, b, V, "anydigpayment"); R["M2_b3"] = C(X, b, V, "dig_x_lowcov")
    d["dig_x_bmed"] = d.anydigpayment * d.lowcov2019_bmedian
    d["acc_x_bmed"] = d.account_fin  * d.lowcov2019_bmedian
    X, b, V, _ = run_model(d, ["anydigpayment", "dig_x_bmed", "account_fin", "acc_x_bmed"] + CTRL)
    R["M2b_b3"] = C(X, b, V, "dig_x_bmed")

    for tag, extra in [("with_acc", ["acc_x_bur", "acc_x_reg"]), ("no_acc", [])]:
        d["dig_x_bur"] = d.anydigpayment * d.lowbureau2019_z
        d["dig_x_reg"] = d.anydigpayment * d.lowregistry2019_z
        d["acc_x_bur"] = d.account_fin  * d.lowbureau2019_z
        d["acc_x_reg"] = d.account_fin  * d.lowregistry2019_z
        terms = ["anydigpayment", "dig_x_bur", "dig_x_reg", "account_fin"] + extra + CTRL
        X, b, V, _ = run_model(d, terms)
        ix = [list(X.columns).index(n) for n in ["dig_x_bur", "dig_x_reg"]]
        r = b[ix]; w = float(r @ np.linalg.inv(V[np.ix_(ix, ix)]) @ r)
        R[f"M2c_wald_chi2__{tag}"] = (w, None)
    R["M2c_wald_chi2"] = R["M2c_wald_chi2__with_acc"]

    m3 = d[d.receive_dig.notna() & d.make_dig.notna()].copy()
    m3_meta = dict(N=len(m3), G=int(m3.iso3.nunique()))
    X, b, V, _ = run_model(m3, ["receive_dig", "make_dig", "account_fin"] + CTRL)
    R["M3a_receive"] = C(X, b, V, "receive_dig"); R["M3a_make"] = C(X, b, V, "make_dig")
    m3["rec_x"] = m3.receive_dig * m3.lowcov2019_z
    m3["mak_x"] = m3.make_dig    * m3.lowcov2019_z
    m3["acc_x"] = m3.account_fin * m3.lowcov2019_z
    X, b, V, _ = run_model(m3, ["receive_dig", "rec_x", "make_dig", "mak_x", "account_fin", "acc_x"] + CTRL)
    R["M3b_recX"] = C(X, b, V, "rec_x"); R["M3b_makX"] = C(X, b, V, "mak_x")

    for yv in ["mobile_loan_app", "emergency_loan_source", "informal_borrow"]:
        dd = d[d[yv].notna()].copy()
        X, b, V, ii = run_model(dd, BASE, y=yv)
        R[f"M4_{yv}_b1"] = C(X, b, V, "anydigpayment")
        R[f"M4_{yv}_b3"] = C(X, b, V, "dig_x_lowcov")
        R[f"M4_{yv}_N"]  = (ii["N"], None)

    d["educ_lin"] = d.educ.astype(float); d["incq_lin"] = d.inc_q.astype(float)
    for nm, zz in [("inc_q", "incq_lin"), ("female_d", "female_d"), ("educ", "educ_lin"), ("region", None)]:
        if nm == "region":
            reg_d = pd.get_dummies(d["regionwb"], prefix="rg", drop_first=True).astype(float)
            tri = reg_d.mul(d.dig_x_lowcov, axis=0); tri.columns = [c + "_tri" for c in tri.columns]
            dz  = reg_d.mul(d.anydigpayment, axis=0); dz.columns = [c + "_dz" for c in dz.columns]
            dm  = pd.concat([d, tri, dz], axis=1)
            X, b, V, _ = run_model(dm, BASE + list(dz.columns) + list(tri.columns))
            ix = [list(X.columns).index(c) for c in tri.columns]
            r = b[ix]; w = float(r @ np.linalg.inv(V[np.ix_(ix, ix)]) @ r)
            R["M5_region_wald"] = (w, None)
        else:
            d[f"tri_{nm}"] = d.anydigpayment * d.lowcov2019_z * d[zz]
            d[f"dz_{nm}"]  = d.anydigpayment * d[zz]
            d[f"lz_{nm}"]  = d.lowcov2019_z  * d[zz]
            X, b, V, _ = run_model(d, BASE + [f"dz_{nm}", f"lz_{nm}", f"tri_{nm}"])
            R[f"M5_{nm}"] = C(X, b, V, f"tri_{nm}")

    R["M6_1_unweighted"] = C(*run_model(d, BASE, w="w_unweighted")[:3], "dig_x_lowcov")
    R["M6_1_population"]  = C(*run_model(d, BASE, w="w_population")[:3], "dig_x_lowcov")
    d3 = d[d.regionwb != "High income"].copy()
    e3 = d3.groupby("iso3").any_cov.first().reset_index()
    e3["z"] = -(e3.any_cov - e3.any_cov.mean()) / e3.any_cov.std(ddof=0)
    d3 = d3.merge(e3[["iso3", "z"]], on="iso3", how="left")
    d3["dig_x_lowcov"] = d3.anydigpayment * d3.z
    d3["acc_x_lowcov"] = d3.account_fin  * d3.z
    X, b, V, i63 = run_model(d3, BASE)
    R["M6_3_drop_high_income"] = C(X, b, V, "dig_x_lowcov")
    R["M6_3_N"] = (i63["N"], None); R["M6_3_G"] = (i63["G"], None)
    for zc, lbl in [("lowdepth2019_z", "M6_4_lowdepth2019_z"), ("lowrights2019_z", "M6_4_lowrights2019_z")]:
        d[f"dx_{zc}"] = d.anydigpayment * d[zc]; d[f"ax_{zc}"] = d.account_fin * d[zc]
        X, b, V, _ = run_model(d, ["anydigpayment", f"dx_{zc}", "account_fin", f"ax_{zc}"] + CTRL)
        R[lbl] = C(X, b, V, f"dx_{zc}")
    for cv in ["lgdppc", "privcredit_gdp", "acct_own_rate"]:
        d[f"dig_x_{cv}"] = d.anydigpayment * d[cv]
    X, b, V, _ = run_model(d, BASE + ["dig_x_lgdppc", "dig_x_privcredit_gdp", "dig_x_acct_own_rate"])
    R["M6_5_country_controls"] = C(X, b, V, "dig_x_lowcov")
    sz = d.groupby("iso3").size(); d6 = d[d.iso3.isin(sz[sz >= 500].index)].copy()
    X, b, V, i66 = run_model(d6, BASE)
    R["M6_6_n_ge_500"] = C(X, b, V, "dig_x_lowcov"); R["M6_6_G"] = (i66["G"], None)
    R["M6_8_internet"] = C(*run_model(d, BASE + ["internet_d"])[:3], "dig_x_lowcov")
    dw = d[d.inwork_d.notna()].copy()
    X, b, V, i610 = run_model(dw, BASE + ["inwork_d"])
    R["M6_10_inwork"] = C(X, b, V, "dig_x_lowcov")
    R["M6_10_N"] = (i610["N"], None); R["M6_10_G"] = (i610["G"], None)

    import statsmodels.api as sm
    Xg = design(d, ["anydigpayment", "dig_x_lowcov", "account_fin", "acc_x_lowcov"] + CTRL).astype(float)
    yv = d.formal_borrow.values
    for fam, lbl in [(sm.families.Binomial(sm.families.links.Logit()),  "M6_2_logit_interaction_AME"),
                     (sm.families.Binomial(sm.families.links.Probit()), "M6_2_probit_interaction_AME")]:
        m = sm.GLM(yv, Xg.values, family=fam).fit(maxiter=300)
        eta = Xg.values @ m.params
        dens = (1 / (1 + np.exp(-eta))) * (1 - 1 / (1 + np.exp(-eta))) if "logit" in lbl \
            else np.exp(-eta ** 2 / 2) / np.sqrt(2 * np.pi)
        j = list(Xg.columns).index("dig_x_lowcov")
        R[lbl] = (float(np.mean(dens) * m.params[j]), None)

    dropmap = {"account_fin": ["account_fin", "acc_x_lowcov"], "female_d": ["female_d"],
               "age_c": ["age_c"], "age_c2": ["age_c2"], "educ": ["educ_2", "educ_3"],
               "inc_q": ["incq_2", "incq_3", "incq_4", "incq_5"], "urban_d": ["urban_d"]}
    for nm, dr in dropmap.items():
        X, b, V, _ = run_model(d, [t for t in BASE if t not in dr])
        R[f"drop_{nm}"] = C(X, b, V, "dig_x_lowcov")
    X, b, V, iah = run_model(d[d.account_fin == 1].copy(), BASE)
    R["account_holders_only"] = C(X, b, V, "dig_x_lowcov"); R["account_holders_only_N"] = (iah["N"], None)
    X, b, V, izc = run_model(d[d.any_cov > 0].copy(), BASE)
    R["drop_zero_coverage"] = C(X, b, V, "dig_x_lowcov")
    R["drop_zero_coverage_N"] = (izc["N"], None); R["drop_zero_coverage_G"] = (izc["G"], None)
    q1 = d.groupby("iso3").any_cov.first().quantile(0.25)
    X, b, V, iq = run_model(d[d.any_cov > q1].copy(), BASE)
    R["drop_lowest_quartile"] = C(X, b, V, "dig_x_lowcov")
    R["drop_lowest_quartile_N"] = (iq["N"], None); R["drop_lowest_quartile_G"] = (iq["G"], None)
    for rn in sorted(d.regionwb.dropna().unique()):
        X, b, V, _ = run_model(d[d.regionwb != rn].copy(), BASE)
        R[f"LORO_{rn}"] = C(X, b, V, "dig_x_lowcov")
    d["dig_x_hi"] = d.anydigpayment * (-d.lowcov2019_z)
    d["acc_x_hi"] = d.account_fin  * (-d.lowcov2019_z)
    X, b, V, _ = run_model(d, ["anydigpayment", "dig_x_hi", "account_fin", "acc_x_hi"] + CTRL)
    R["sign_reversal"] = C(X, b, V, "dig_x_hi")
    loeo = []
    for iso in sorted(d.iso3.unique()):
        X, b, V, _ = run_model(d[d.iso3 != iso].copy(), BASE)
        loeo.append(C(X, b, V, "dig_x_lowcov")[0])
    R["LOEO_min"] = (min(loeo), None); R["LOEO_max"] = (max(loeo), None)
    R["LOEO_all_negative"] = (bool(all(x < 0 for x in loeo)), None); R["LOEO_n"] = (len(loeo), None)
    zv = float(ec.loc[ec.iso3 == "VNM", "lowcov2019_z"].iloc[0])
    X, b, V, _ = run_model(d, BASE)
    i1_, i3_ = list(X.columns).index("anydigpayment"), list(X.columns).index("dig_x_lowcov")
    slope = b[i1_] + b[i3_] * zv
    grad = np.zeros(len(b)); grad[i1_] = 1; grad[i3_] = zv
    R["M7_vnm_slope"] = (float(slope), float(np.sqrt(grad @ V @ grad)))

    rows = []
    for k, (est, se) in [(k, v) for k, v in R.items() if isinstance(v, tuple)]:
        t = TGT.get(k)
        if t is None:
            rows.append(dict(key=k, repro=est, codex=None, abs_diff=None, status="no_codex_target"))
            continue
        cx = t[0]; ad = abs(est - cx)
        if ad < 1e-8:                      st = "EXACT_MATCH"
        elif ad < 1e-4 and est * cx > 0:   st = "MATCH_MINOR_NUMERIC"
        elif est * cx > 0:                 st = "SAME_SIGN_DIFF"
        else:                              st = "SIGN_MISMATCH"
        rows.append(dict(key=k, repro=est, codex=cx, abs_diff=ad, status=st))
    comp = pd.DataFrame(rows)
    comp.to_csv(OUTDIR + r"\comparison.csv", index=False)

    panel_ok = (panel_meta["N"] == CODEX_PANEL["N"] and panel_meta["G"] == CODEX_PANEL["G"]
                and m3_meta["N"] == CODEX_PANEL["N_m3"] and m3_meta["G"] == CODEX_PANEL["G_m3"])
    core = ["M1_b1", "M2_b1", "M2_b3", "M2b_b3", "M3a_receive", "M3a_make", "M3b_recX", "M3b_makX",
            "M4_informal_borrow_b3", "M6_5_country_controls", "sign_reversal"]
    core_ok = all(comp.loc[comp.key == k, "status"].iloc[0] in ("EXACT_MATCH", "MATCH_MINOR_NUMERIC")
                  for k in core)
    verdict = "PASS" if (panel_ok and core_ok) else "REVIEW"

    receipt = dict(
        run_id="CLAUDE-S5R-20260910-001", stage=4, kind="independent_reproduction",
        executed_by="claude", reproduces=["CODEX-S5-EXP-20260909-002", "CODEX-S5-M6-2-20260909-001",
                                          "CODEX-S5-TABLES-20260909-001", "CODEX-S5-AUDIT-20260909-001"],
        verdict=verdict, evidence_status="INDEPENDENTLY_REPRODUCED" if verdict == "PASS" else "REPRODUCTION_INCOMPLETE",
        created_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        seed=SEED, code_file="code/study_05_crosscountry/CLAUDE-S5R-20260910-001_reproduce.py",
        code_sha256=sha256(__file__),
        input_sha256={p.replace(ROOT + chr(92), "").replace(chr(92), "/"): sha256(p) for p in EXPECT_HASH},
        outputs_sha256={f: sha256(OUTDIR + "\\" + f) for f in
                        ["analysis_panel.csv", "drop_table.csv", "comparison.csv"]},
        panel=dict(reproduced_primary=panel_meta,
                   reproduced_m3={"N": m3_meta["N"], "G": m3_meta["G"]},
                   codex=CODEX_PANEL, match=panel_ok),
        estimator="hand-rolled WLS normal-equations + explicit FE dummies + CR1 cluster cov; "
                  "logit/probit via statsmodels GLM dummy-variable FE",
        deviations=[
            "wild-cluster bootstrap p-values not recomputed (seed-dependent secondary diagnostic)",
            "M2c joint Wald reported in chi2 form (not F-form with G-1 dof); with/without account_fin "
            "interaction variants both in comparison.csv (M2c_wald_chi2__with_acc / __no_acc)",
            "M6.2 nonlinear interaction AME differs ~10% -- definition-sensitive cross-partial in a "
            "97-dummy FE GLM; sign and order of magnitude reproduce; Codex flagged M6.2 as "
            "sign-direction sensitivity only",
            "M5 has no Codex numeric baseline in the Stage-3 artifacts; reported for completeness",
        ],
        environment=dict(python=sys.version, numpy=np.__version__, pandas=pd.__version__,
                         platform=platform.platform()),
        runtime_seconds=round(time.time() - t0, 1),
    )
    json.dump({k: (list(v) if isinstance(v, tuple) else v) for k, v in R.items()},
              open(OUTDIR + r"\estimates.json", "w"), indent=2)
    json.dump(receipt, open(OUTDIR + r"\run_receipt.json", "w"), indent=2)

    print("\n== comparison ==")
    print(comp.to_string(index=False))
    print(f"\npanel match: {panel_ok}   core match: {core_ok}")
    print(f"\n================  STAGE 4 VERDICT: {verdict}  ================")
    print(f"runtime {time.time() - t0:.0f}s   outputs -> {OUTDIR}")

if __name__ == "__main__":
    main()
