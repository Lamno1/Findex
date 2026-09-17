import hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
import patsy

ROOT=Path(r"D:/EconomicResearch")
P=ROOT/"projects/study_05_findex_crosscountry"
OUT=P/"results/stage5_estimation"
D=pd.read_csv(P/"results/stage4_build/analytical_dataset.csv")
I=pd.read_csv(P/"data/raw/wb_credit_information_by_country_year.csv")
I=I[I.year.eq(2019)].copy()
I["coverage"]=I[["credit_bureau_cov_pct","credit_registry_cov_pct"]].max(axis=1,skipna=True)
I=I[["iso3","coverage"]].drop_duplicates("iso3")
D=D.merge(I,left_on="economycode",right_on="iso3",validate="many_to_one")
D["lowcov_z"]=-(D.coverage-D.coverage.mean())/D.coverage.std(ddof=0)
D["age_c"]=D.age-D.age.mean(); D["age_c2"]=D.age_c**2; D["w_equal"]=D.wgt/D.groupby(["economycode","wave"]).wgt.transform("sum")
D["dig_x_lowcov"]=D.digital_payment*D.lowcov_z
base="female_binary + age_c + age_c2 + C(education) + C(income_quintile) + C(economycode)"
formula="formal_borrow ~ digital_payment + dig_x_lowcov + "+base
rows=[]
for wave in (2021,2024):
    q=D[D.wave.eq(wave)].copy()
    ydf,Xdf=patsy.dmatrices(formula,q,return_type="dataframe")
    y=np.asarray(ydf).ravel(); X=np.asarray(Xdf); w=q.loc[Xdf.index,"w_equal"].to_numpy(); groups=q.loc[Xdf.index,"economycode"].to_numpy()
    A=(X.T*w)@X; b=(X.T*w)@y; names=list(Xdf.columns); idx=names.index("dig_x_lowcov")
    for c in sorted(np.unique(groups)):
        keep=groups!=c; beta=np.linalg.pinv((X[keep].T*w[keep])@X[keep])@((X[keep].T*w[keep])@y[keep])
        rows.append({"specification":f"ROBUSTNESS_LOO_{wave}","term":"dig_x_lowcov","dropped_economy":c,"estimate":float(beta[idx]),"N":int(keep.sum()),"G":int(np.unique(groups[keep]).size),"weight":"w_equal","cluster":"economy","estimator":"WLS LPM coefficient-only leave-one-economy-out"})
pd.DataFrame(rows).to_csv(OUT/"leave_one_economy_out.csv",index=False)
print(json.dumps({"rows":len(rows),"file":str(OUT/"leave_one_economy_out.csv")},indent=2))
