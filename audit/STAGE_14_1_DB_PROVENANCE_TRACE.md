# Stage 14.1 — Doing Business / Getting Credit Provenance Trace (Item 6 detail)

Date: 2026-09-17. Traced in the exact order the owner specified: actual manifest/coverage
file → its role in the 93-economy/2021-2024 pipeline → cross-reference to the prior
H-000500/H-000501 investigation → which of the 93 sample economies are implicated → whether
the specific values are pre- or post-review. No data file was altered in producing this
trace.

## (a) Which exact dataset/version/vintage feeds the 2019 coverage moderator here

`code/study_05_crosscountry/stage5_estimation_audit.py` (line `INST = P /
"data/raw/wb_credit_information_by_country_year.csv"`) is the sole source of the coverage
moderator for the 93-economy/2021-2024 primary and secondary estimates.

- Path: `projects/study_05_findex_crosscountry/data/raw/wb_credit_information_by_country_year.csv`
- SHA-256 (independently recomputed in this trace):
  `2D7C9A27EFB59FF7BBCB894F3C0ECB51782DD8B1076C347868AAE047FE3D6288`
- File modification timestamp on disk: 2026-09-09 20:10:13 (local) — i.e. **not** touched by
  today's (2026-09-17) Stage 3-11 data-acquisition work, which acquired fresh raw Findex
  microdata but did not re-acquire this credit-information file.
- `data/STUDY_05_RAW_MANIFEST.json` records the identical SHA-256 for this path, with the
  note: *"long table iso3 x year 2003-2019 (0-8 depth index available from 2013)"*, acquired
  2026-09-09, described as sourced from the **Doing Business 2020 release**.
- **Conclusion: this is the exact same file, byte-for-byte, already used for the frozen
  H-000500/H-000501 single-wave design.** Nothing new was acquired; the Stage 3-11 pipeline
  reuses the pre-existing shared project resource.

## (b) Which exact indicator(s)

`stage5_estimation_audit.py`: `i = i[i.year.eq(2019)]`, then
`coverage = max(credit_bureau_cov_pct, credit_registry_cov_pct)`. Per
`data/STUDY_05_RAW_MANIFEST.json` and the H-000501 preregistration's own variable contract,
these two columns correspond to the World Bank Doing Business "Getting Credit" topic
indicators `IC.CRED.ACC.PRVT.CRD.ZS` (private credit bureau coverage) and
`IC.CRED.ACC.PUBL.CRD.REG.COVR.ZS` (public credit registry coverage) — the same pair used
as the primary moderator in H-000500/H-000501. The file also carries
`depth_credit_info_0_8` (`IC.CRED.ACC.DPTH.CISI.XD.08.DB1519`) and `legal_rights_0_12`
(`IC.CRED.ACC.LGL.RGHT.XD.012.DB1519`), used only as secondary/depth moderators in this
pipeline, matching H-000500/H-000501's usage.

## (c) Which of the 93 sample economies are among those the WB review flagged

This project's own prior investigation for H-000500/H-000501
(`audit/CODEX_S5_DB_INTEGRITY_SENSITIVITY.md`, `audit/CLAUDE_S5_DB_INTEGRITY_REPRODUCTION.md`)
records that the World Bank's review of Doing Business "Getting Credit" irregularities
publicly confirmed two economies: **China (DB2018 cycle)** and **Saudi Arabia (DB2020
cycle)**. Checking `data/manifests/findex_2021_2024_primary_93.csv`:

```
CHN,China,1,1,1,
SAU,Saudi Arabia,1,1,1,
```

Both `final_sample=1` — **both China and Saudi Arabia are inside the 93-economy sample**
used by the Stage 3-11 pipeline. No file available to this project documents any economy
beyond these two as flagged by the review; this trace does not assert that only two were
ever affected, only that only two are documented as confirmed in the materials this project
already holds.

## (d) Pre-correction or post-correction values — UNRESOLVED

This is the step that cannot be closed from available files.

- The file's own manifest note says "Doing Business 2020 release" and nothing more specific
  about a revision date, corrigendum, or correction pass.
- The World Bank's internal review of Getting Credit and other Doing Business irregularities
  was reported to the public around December 2020; the Doing Business report series was
  announced discontinued in September 2021.
- The acquired file's own recorded acquisition date (2026-09-09, i.e. this project's local
  download date, not the World Bank's original publication date) tells us nothing about
  which vintage of the underlying WB-published numbers it reflects.
- No corrigendum file, revision-log entry, "corrected" flag column, or paired
  before/after-correction value was found anywhere in
  `data/raw/wb_credit_information_by_country_year.csv`,
  `data/raw/wb_credit_information_latest_snapshot.csv`, or the associated
  `data/raw/wb_api_json/*.json` files.
- **Classification: `PROVENANCE_UNCERTAINTY`.** It cannot be determined, from files
  available to this project, whether the China/Saudi Arabia 2019 Getting Credit values used
  in this analysis are the originally-published (potentially irregular) figures or a
  subsequently corrected figure. No value was altered to force a resolution either way.

## (e) Overall

Steps (a)-(c) are fully resolved with direct file evidence. Step (d) is honestly
unresolved and disclosed as `PROVENANCE_UNCERTAINTY` rather than guessed. This exact
same unresolved status was already carried by the H-000500/H-000501 manuscript's own
Doing Business paragraph, which this pipeline's manuscript now mirrors rather than
contradicts or silently omits.

**This finding does not, by itself, warrant re-estimation.** It is the same disclosed,
carried-forward measurement-provenance caveat already accepted as a limitation (not a
blocking defect) in the parallel, independently-reproduced H-000500/H-000501 line, applied
to the same underlying file reused here. Re-estimation would only be warranted if a
corrected-vs-original value comparison became available and showed the two 2019 values
actually differ enough to matter for the interaction sign or significance — no such
comparison exists in this project's files.
