# Candidate project ideas for a new open-source bottom-up proteomics tool (2-4 weeks, one developer, CPU-only cloud container)

Research date: 2026-10-13. PyPI version/date data was pulled live from the PyPI JSON API (`https://pypi.org/pypi/<pkg>/json`) on that date. GitHub API star counts could not be retrieved from this environment, so stars are not reported unless a fetched page stated them.

## Q1. Which candidate directions are already well served and should be dropped?

### Takeaway
Four of the suggested directions are now largely covered by actively maintained packages. That makes a new 2-4 week tool there low-novelty. They are: (1) the universal converter to tidy parquet (bigbio **qpx**), (2) LLM-assisted SDRF annotation (bigbio's **sdrf-annotated-datasets**, with about 11.9k AI-assisted accessions), (3) Python MSstats/proDA/DEqMS/msqrob2 ports (**pymsstats**, **pyproda**, **pydeqms**, **MSqRobPy**) and (4) single-cell proteomics in scverse (**scpviz**). A generic interactive HTML QC report is also largely covered by **pmultiqc**.

### Cited Findings
**Universal converter / harmonizer (DROP)**
- `qpx` 1.1.6 was released on PyPI on 2026-10-13, the same day as this research. It describes itself as a "Quantitative proteomics data toolkit — convert, transform, query, and validate QPX Parquet datasets" — [PyPI qpx](https://pypi.org/project/qpx/)
- qpx converts "OpenMS (native QPX and consensusXML), DIA-NN, MaxQuant, Spectronaut, FragPipe, CPTAC CDAP (`.psm`), mzIdentML, and SDRF to QPX Parquet format". It adds protein quantification (DirectLFQ, MaxLFQ, iBAQ, TopN), SQL querying, schema validation and MuData export. Its repository is github.com/bigbio/qpx — [PyPI qpx description](https://pypi.org/project/qpx/); [GitHub bigbio/qpx](https://github.com/bigbio/qpx)
- The older `quantmsio` PyPI package (0.0.3, April 2024) was the predecessor "Convert multiple files into quantms.io format" — [PyPI quantmsio](https://pypi.org/project/quantmsio/)
- `psm-utils` 1.5.5 (June 2026) already provides "Common utilities for parsing and handling peptide-spectrum matches and search engine results" at the PSM level — [PyPI psm-utils](https://pypi.org/project/psm-utils/)
- Remaining niche: Sage is not in qpx's listed converters, though psm_utils covers Sage PSMs. That niche is too thin for a project — [PyPI qpx](https://pypi.org/project/qpx/)

**LLM / automatic SDRF annotation (DROP as a standalone project)**
- bigbio/sdrf-annotated-datasets (auto-generated stats dated 2026-10-12) reports 11,907 accessions, 12,288 SDRF files, "AI-assisted accessions 11,907" and "AI agents (named fingerprints) 5". It covers 20.7% of ProteomeXchange and 27.8% of PRIDE. It ships `llms.txt` and `AGENTS.md` for agents — [bigbio/sdrf-annotated-datasets README](https://github.com/bigbio/sdrf-annotated-datasets)
- The same README reports low sample-field completeness: "disease 43%, age 9%" — [bigbio/sdrf-annotated-datasets README](https://github.com/bigbio/sdrf-annotated-datasets)
- SDRF spec v1.1.0 (2026-01) added file-level metadata columns, including the annotation tool and validation status — [SDRF-Proteomics spec README](https://github.com/bigbio/proteomics-sample-metadata/blob/master/sdrf-proteomics/README.adoc)
- The OmicsFM preprint (2026) used an agentic extraction pipeline with a locally served LLM (Qwen3.5-35B-A3B). It read PRIDE descriptions and open-access papers to build run-level metadata for 1,397 reprocessed PRIDE projects — [bioRxiv OmicsFM](https://www.biorxiv.org/content/10.64898/2026.08.25.747021v1.full)
- Prior state: only 156 of 9,671 datasets (1.6%) submitted since mid-2022 had submitter SDRF. lesSDRF is the guided web annotator — [lesSDRF paper (PMC10598006)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10598006/)
- `sdrf-pipelines` 0.1.6 (July 2026) is the official validator and converter, with optional ontology validation — [PyPI sdrf-pipelines](https://pypi.org/project/sdrf-pipelines/); [README](https://github.com/bigbio/sdrf-pipelines)

**Python-native MSstats / msqrob2 / proDA / DEqMS (DROP)**
- `pymsstats` 0.3.0 (2026-05-20) is a "Pure-Python port of Bioconductor MSstats". It claims "100% coverage of the R MSstats 4.14.2 public API" and bit-for-bit reproduction of TMP summarization and log2FC. It ships nine vendor converters (DIA-NN, Spectronaut, FragPipe, OpenMS, Skyline, PD, Progenesis, OpenSWATH, DIA-Umpire) plus MaxQuant. It is mirrored from omicverse — [PyPI pymsstats](https://pypi.org/project/pymsstats/); [GitHub omicverse/py-MSstats](https://github.com/omicverse/py-MSstats)
- The same group published `pyproda` 0.1.1 (a proDA port) and `pydeqms` 0.1.1 (a DEqMS port), both on 2026-05-20 — [PyPI pyproda](https://pypi.org/project/pyproda/); [PyPI pydeqms](https://pypi.org/project/pydeqms/)
- CompOmics MSqRobPy is a "Python implementation of MSqRob2 R package" offering OLS/Huber fits, empirical Bayes and a hurdle model. However, "Mixed models are not fitted". It is not on PyPI and had 0 stars and 6 commits when fetched — [GitHub CompOmics/MSqRobPy](https://github.com/CompOmics/MSqRobPy)
- `pylimma` 0.2.0 (2026-09-30) is a Python limma port with a proteomics differential-abundance example — [PyPI pylimma](https://pypi.org/project/pylimma/); [pylimma docs](https://pylimma.readthedocs.io/en/stable/)
- `alphastats` 0.7.2 (Nov 2025) offers automated downstream statistics with a GUI and a Python API — [PyPI alphastats](https://pypi.org/project/alphastats/)
- `msreport` 0.0.34 (Feb 2026) handles "Post processing and analysis of quantitative proteomics data" — [PyPI msreport](https://pypi.org/project/msreport/)

**Single-cell proteomics Python toolkit (DROP)**
- scpviz (JOSS 2026, 11(122), 10303) extends AnnData to proteomics with a `pAnnData` class. It covers the path from peptides to protein summaries, plus DE, enrichment and networks. `scpviz` 1.1.2 was on PyPI in Aug 2026 — [JOSS scpviz](https://joss.theoj.org/papers/10.21105/joss.10303); [PyPI scpviz](https://pypi.org/project/scpviz/)

**Generic interactive HTML QC report (DROP as generic; see Idea 2 for the niche)**
- pmultiqc 0.0.48 (Sept 2026) is a MultiQC plugin that produces interactive HTML QC for quantms, MaxQuant, DIA-NN, FragPipe, mzIdentML, ProteoBench, nf-core/mhcquant and QPX outputs — [PyPI pmultiqc](https://pypi.org/project/pmultiqc/)
- Several USI spectrum viewers already exist: ProteomeCentral Quetzal, PRIDE, TPP viewer, PDV and Universal Spectrum Explorer — [PSI USI page](https://www.psidev.info/usi); [ProteomeCentral USI](https://proteomecentral.proteomexchange.org/quetzal/)
- `pyopenms-viz` 1.2.0 (Sept 2026) provides pandas-based MS plotting. `spectrum_utils` 0.5.0 provides spectrum annotation and plotting — [PyPI pyopenms-viz](https://pypi.org/project/pyopenms-viz/); [PyPI spectrum-utils](https://pypi.org/project/spectrum-utils/)

### Inferences
- The bigbio/quantms ecosystem (qpx, pmultiqc, sdrf-pipelines, sdrf-annotated-datasets, quantms) is releasing extremely actively, with qpx released today. Any project that overlaps that ecosystem's roadmap (formats, SDRF, QC reports, reanalysis) risks being made redundant within months. It is better to build tools that *consume* QPX/psm_utils rather than compete with them.
- omicverse appears to be porting R/Bioconductor proteomics packages to Python in bulk (three ports on one day). A "Python port of R package X" project risks being scooped unless X is niche.

### Gaps
- GitHub stars and last-commit dates for qpx, pmultiqc and the other repos could not be retrieved (the GitHub API was blocked in this environment).
- pymsstats's claims of bit-for-bit parity are self-reported and were not independently verified.

---

## Q2. Vetted project ideas (ranked), with gap, closest tools, feasibility, MVP and risks

### Takeaway
The best remaining gaps for a 2-4 week CPU-only project are:
- **(1) a Python entrapment-FDR validation library**, because FDRBench is Java/GUI-centric and the main paper shows that DIA tools fail FDR control;
- **(2) a cohort-scale longitudinal QC/drift detector that emits mzQC**, because MSstatsQC is R-only, pmultiqc does not advertise mzQC output and pymzqc is I/O-only;
- **(3) PTM site-level roll-up plus site-vs-protein-adjusted differential testing in Python**, because MSstatsPTM and msqrob2PTM are R-only and ProteoMeter targets LiP/structure;
- **(4) an SDRF-vs-data consistency auditor**, a new angle that complements the AI-annotated SDRF corpus.

Weaker but viable options are a Python normalization+imputation benchmarking harness, an immunopeptidomics QC report, and a "PXD quick-run" reanalysis helper.

### Idea 1 — `entrap`: a Python library and CLI for empirical FDR validation by entrapment (RECOMMENDED)
**(a) Description and users.** A pip-installable Python package with three parts:
- **Entrapment FASTA builder:** shuffled or foreign-species entrapment databases at a chosen fold r, with peptide-pair files.
- **FDP estimators:** the lower-bound, combined and paired estimators from Wen et al. 2025, applied at precursor, peptide and protein-group level.
- **Readers:** DIA-NN, FragPipe, Sage, Spectronaut, MaxQuant and Percolator/mokapot results via psm_utils/qpx.

It reports FDP-vs-FDR curves with bootstrap confidence bands, and outputs JSON/mzQC-style metrics and an HTML plot. Target users are search-engine and DIA tool developers, benchmarkers (ProteoBench contributors) and core facilities validating single-cell or DIA settings.

**(b) Gap and evidence.**
- Wen et al. (Nat Methods 2025) found three prevalent validation methods: "one invalid, one providing only a lower bound, and one valid but under-powered". They propose a more powerful method and find that "no DIA search tool consistently controls the FDR, with particularly poor performance on single-cell datasets" — [Europe PMC abstract / Nat Methods 22:1454 (doi 10.1038/s41592-025-02719-x)](https://www.nature.com/articles/s41592-025-02719-x); [PMC12240826](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12240826/)
- The reference implementation, FDRBench, is written in Java (Java 11+ CLI and a GUI). Its only non-Java helper is an R plotting function, it is not on PyPI, and it is tested on DIA-NN, MSFragger, Spectronaut, MaxQuant, Tide and Sage outputs — [GitHub Noble-Lab/FDRBench](https://github.com/Noble-Lab/FDRBench)
- No PyPI packages named `entrapment`, `fdrbench` or `pyentrapment` exist (checked via the PyPI JSON API on 2026-10-13) — [PyPI](https://pypi.org/)
- An alternative, the decoy-free "query mix-max" approach, also uses entrapment queries — [Madej & Lam 2025 (PMC11894652)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11894652/)

**(c) Closest tools.**
- FDRBench (Java) — [GitHub](https://github.com/Noble-Lab/FDRBench)
- ProteoBench "DIA Ion Entrapment – Astral" module, which is a hosted benchmark on a fixed dataset based on Wen et al. — [ProteoBench docs](https://proteobench.readthedocs.io/en/latest/available-modules/active-modules/13-entrapment-ion-dia-astral/)

The proposed tool differs in four ways: native Python/notebook/pipeline integration, direct reading of native tool outputs via psm_utils/qpx, protein-group-level handling, uncertainty bands, and batch evaluation across many runs or parameter sets. Positioning it as a library that ProteoBench or quantms could import reduces duplication.

**(d) Feasibility.**
- Purely tabular math plus FASTA manipulation, so CPU only.
- Libraries: pyteomics (digestion/parsing; 5.0.1, July 2026), psm_utils, polars, numpy and matplotlib/plotly — [PyPI pyteomics](https://pypi.org/project/pyteomics/); [PyPI psm-utils](https://pypi.org/project/psm-utils/)
- Test data: running a search requires a search engine. Sage is CPU-only Rust and runs on Linux — [GitHub lazear/sage](https://github.com/lazear/sage)
- Small public DDA test data: PXD001819 (yeast-UPS1, LTQ Orbitrap Velos) — [PRIDE PXD001819](https://www.ebi.ac.uk/pride/archive/projects/PXD001819)
- DIA test data: PXD028735 (LFQ benchmark, TripleTOF) — [PRIDE PXD028735](https://www.ebi.ac.uk/pride/archive/projects/PXD028735)
- Raw-to-mzML conversion for Thermo files needs ThermoRawFileParser, which runs on Linux (not verified here). Some PRIDE projects already deposit mzML.

**(e) MVP (2-3 weeks).**
1. Entrapment FASTA generator (shuffle and foreign, fold r, pair file).
2. The three FDP estimators at precursor and peptide level, validated against FDRBench output on the same input.
3. Readers for DIA-NN parquet, Sage and FragPipe.
4. CLI plus an HTML/PNG FDP-vs-FDR plot.
5. A worked example: Sage on a PXD001819 subset with a 1:1 shuffled entrapment.

**(f) Risks.**
- The Noble lab could release a Python port. FDRBench already covers the core math, so novelty rests on ecosystem integration and usability.
- The authors' entrapment raw search results may not be deposited for reuse, so check the paper's data-availability section.
- DIA validation needs DIA-NN, whose licence and academic use should be checked, or the open alternative alphaDIA (2.2.0, Oct 2026; CPU feasibility not verified) — [PyPI alphadia](https://pypi.org/project/alphadia/)

### Idea 2 — `qcdrift`: cohort-scale longitudinal QC and drift/batch detection that reads tool outputs and writes mzQC (RECOMMENDED)
**(a) Description and users.** The tool takes many runs from DIA-NN, FragPipe, MaxQuant, quantms/QPX or mzML. It computes per-run metrics such as ID counts, precursor intensity distributions, RT and mass-error drift, missingness and iRT/standard-peptide behaviour. It then applies statistical process control (Shewhart/CUSUM/EWMA, change-point detection) and batch diagnostics (PCA/PVCA against SDRF factors). Results are written as mzQC files plus a static HTML dashboard. Target users are core facilities, large-cohort clinical studies and instrument QC.

**(b) Gap and evidence.**
- MSstatsQC provides longitudinal statistical process control (control charts, change-point analysis), but it is an R/Bioconductor package with a web interface — [MSstatsQC vignette](https://bioc.r-universe.dev/articles/MSstatsQC/MSstatsQC.html)
- The pmultiqc README lists inputs and an HTML report but does not mention mzQC output. A text search of its PyPI description found 0 matches for "mzQC" — [PyPI pmultiqc](https://pypi.org/project/pmultiqc/)
- pymzqc (1.0.3, Sept 2026) is a library to "serialise, deserialise, check syntax, check semantics" mzQC files, so it is format I/O rather than analysis — [GitHub pymzqc README](https://github.com/MS-Quality-hub/pymzqc); [PyPI pymzqc](https://pypi.org/project/pymzqc/)
- The mzQC paper lists rmzqc, pymzqc and jmzqc as libraries. MsQuality (R) computes 43 mzQC metrics per single run, with no longitudinal analysis — [mzQC/QC tooling (PMC10580266)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10580266)
- The batch-effect tutorial by Čuklina et al. (MSB 2021) covers intensity drift and batch correction, implemented in R (proBatch) — [PMC8447595](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8447595/)

**(c) Closest tools.**
- MSstatsQC (R) — [vignette](https://bioc.r-universe.dev/articles/MSstatsQC/MSstatsQC.html)
- pmultiqc (Python, run-level QC HTML) — [PyPI](https://pypi.org/project/pmultiqc/)
- proBatch (R) — [PMC8447595](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8447595/)
- QCloud and QuiC (services cited as MSstatsQC data sources) — [MSstatsQC vignette](https://bioc.r-universe.dev/articles/MSstatsQC/MSstatsQC.html)

The proposed tool differs in being Python-native, multi-tool, cohort-scale, and in emitting standard mzQC plus drift/change-point alerts. It could be contributed as a pmultiqc companion.

**(d) Feasibility.**
- Inputs are tabular reports, so it runs on CPU.
- Libraries: polars, pymzqc, qpx (as a reader), ruptures (change-point; PyPI status not verified here), plotly, and sdrf-pipelines for factor parsing — [PyPI qpx](https://pypi.org/project/qpx/); [PyPI sdrf-pipelines](https://pypi.org/project/sdrf-pipelines/)
- Test data: any multi-batch PRIDE dataset with search results deposited. Curated SDRFs, including "gold standard" ones, exist in sdrf-annotated-datasets for batch/factor labels — [bigbio/sdrf-annotated-datasets](https://github.com/bigbio/sdrf-annotated-datasets)

**(e) MVP (2-3 weeks).**
1. Readers for DIA-NN report.parquet, FragPipe psm.tsv and MaxQuant evidence.txt.
2. About 15 run-level metrics, with mzQC export via pymzqc.
3. EWMA/CUSUM flags plus PCA-vs-batch plots.
4. A single static HTML report.

**(f) Risks.**
- The bigbio team could add mzQC export and longitudinal views to pmultiqc.
- Choosing mzQC controlled-vocabulary terms for custom metrics may require PSI-MS CV additions.
- Moderate novelty: the value is integration and statistics rather than a new method.

### Idea 3 — `sitequant`: PTM site-level roll-up and protein-adjusted differential site analysis in Python (RECOMMENDED, with scoping)
**(a) Description and users.** The tool would:
- map peptidoforms from DIA-NN, FragPipe, MaxQuant or Spectronaut (via qpx/psm_utils) to protein-residue sites using FASTA;
- filter by localization probability;
- aggregate to site level with sum, median or maxLFQ-style methods, handling multiply-modified peptides;
- test site changes adjusted for protein abundance (as MSstatsPTM and msqrob2PTM do), using pymsstats or pylimma internally;
- export site tables with sequence windows for kinase enrichment tools.

Target users are phospho-, ubiquitin- and acetyl-proteomics labs that work in Python.

**(b) Gap and evidence.**
- MSstatsPTM (R/Bioconductor) quantifies PTM sites and their proteins and integrates the two. It supports DDA, DIA and TMT and maps peptides to sites with FASTA — [MSstatsPTM manual](https://bioconductor.statistik.tu-dortmund.de/packages/3.16/bioc/manuals/MSstatsPTM/man/MSstatsPTM.pdf)
- msqrob2PTM (R) handles differential abundance and differential usage at PTM and peptidoform level — [bioRxiv msqrob2PTM](https://www.biorxiv.org/content/10.1101/2023.07.05.547780.full.pdf)
- The ProteoMeter authors note "a scarcity of proteomics data analysis pipelines implemented as a Python library". ProteoMeter focuses on integrating multi-PTM, LiP-MS and cross-linking data at residue resolution — [bioRxiv ProteoMeter](https://www.biorxiv.org/content/10.1101/2025.07.14.664747.full.pdf); [PyPI proteometer 0.5.0](https://pypi.org/project/proteometer/)
- A 2026 JPR paper from PNNL compares peptide-to-site roll-up strategies, which supports demand and provides a method reference — [PNNL publication page](https://www.pnnl.gov/publications/aggregation-methods-quantifying-ptm-and-structural-changes-bottom-proteomics)
- No `pymsstatsptm` or `pymsqrob2` exists on PyPI (checked 2026-10-13) — [PyPI](https://pypi.org/)

**(c) Closest tools.**
- MSstatsPTM (R) — [manual](https://bioconductor.statistik.tu-dortmund.de/packages/3.16/bioc/manuals/MSstatsPTM/man/MSstatsPTM.pdf)
- msqrob2PTM (R) — [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.07.05.547780.full.pdf)
- ProteoMeter (Python; LiP/structure focus) — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.07.14.664747.full.pdf)
- MSqRobPy's `aggregate_features` can group by PTM site, but it has no PTM workflow — [GitHub](https://github.com/CompOmics/MSqRobPy)
- pymsstats, for protein-level models — [PyPI](https://pypi.org/project/pymsstats/)

The proposed tool differs by being the Python-native, multi-tool site mapper plus protein-adjusted testing.

**(d) Feasibility.**
- CPU-only, tabular.
- Libraries: pyteomics (FASTA and modification parsing), psm_utils/qpx (readers), pymsstats or pylimma (models), polars.
- Test data: public phosphoproteomics datasets with deposited DIA-NN or FragPipe outputs. No specific PXD was verified in this research, so this is a gap.

**(e) MVP (3-4 weeks).**
1. Site mapping and localization filtering for DIA-NN and FragPipe.
2. Site roll-up.
3. Protein-adjusted contrast following the MSstatsPTM model (site log-fold-change minus protein log-fold-change, with combined variance).
4. Validation against MSstatsPTM output on its example data.

**(f) Risks.**
- omicverse could port MSstatsPTM, given it ported MSstats, proDA and DEqMS in May 2026 — [PyPI pymsstats](https://pypi.org/project/pymsstats/)
- The localization-score semantics differ per tool and need careful handling.
- Spectronaut site reports are proprietary-format tables but are readable.

### Idea 4 — `sdrf-audit`: an SDRF-vs-data consistency auditor (NEW ANGLE; RECOMMENDED as small, high-utility)
**(a) Description and users.** The tool checks a (possibly AI-generated) SDRF against the actual data and search results:
- instrument model and fragmentation recorded in mzML headers;
- run file names versus files deposited in PRIDE (via pridepy/ppx);
- declared modifications versus observed modification frequencies in the PSMs;
- TMT/label channels versus reporter-ion presence;
- organism versus taxonomy of identified proteins;
- fraction and replicate structure.

It outputs a scored discrepancy report. Target users are SDRF curators (human or AI), the PRIDE and bigbio curation teams, and reanalysis pipelines.

**(b) Gap and evidence.**
- All 11,907 accessions in bigbio's SDRF corpus are AI-assisted, with 5 named AI agents and 3,930 from an "Unidentified agent". The corpus validates via CI "gates", but sample-field completeness is low (disease 43%, age 9%). That makes independent, data-grounded verification valuable — [bigbio/sdrf-annotated-datasets](https://github.com/bigbio/sdrf-annotated-datasets)
- sdrf-pipelines validates structure and ontology terms. It does not compare annotations against the data — [sdrf-pipelines README](https://github.com/bigbio/sdrf-pipelines)
- SDRF v1.1.0 adds "validation status" and "annotation tool" columns, which this tool could populate — [SDRF spec README](https://github.com/bigbio/proteomics-sample-metadata/blob/master/sdrf-proteomics/README.adoc)
- A merged PR in that repository records a template-validation gap for acquisition-method terms, showing that validators miss semantic errors — [sdrf-annotated-datasets PR #641](https://github.com/bigbio/sdrf-annotated-datasets/pull/641)

**(c) Closest tools.**
- sdrf-pipelines (syntax and ontology validation) — [README](https://github.com/bigbio/sdrf-pipelines)
- lesSDRF (guided creation) — [PMC10598006](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10598006/)
- sdrfcheck (old, 2020) — [PyPI sdrfcheck](https://pypi.org/project/sdrfcheck/)

None of them cross-check annotations against spectra or identifications. This is an inference from their descriptions.

**(d) Feasibility.**
- Libraries: pridepy 0.0.16 (May 2026) and ppx 1.5.0 for file lists and downloads; pyteomics or pyopenms for mzML headers; psm_utils for results — [PyPI pridepy](https://pypi.org/project/pridepy/); [PyPI ppx](https://pypi.org/project/ppx/)
- Many checks (file names, instrument CV, organism) need only PRIDE metadata and the first kilobytes of mzML, which suits limited disk.
- Test data: the curated "gold standard" SDRFs in the bigbio repo, with deliberately corrupted copies as negative controls.

**(e) MVP (2 weeks).**
1. File-name and file-list reconciliation with PRIDE.
2. Instrument and dissociation check from a streaming mzML header read.
3. Organism and modification check from deposited search results where available.
4. A JSON/HTML report.
5. Run over about 200 corpus SDRFs to report an error-rate estimate (itself a publishable finding).

**(f) Risks.**
- The bigbio CI may add similar checks.
- Many PRIDE projects deposit only vendor RAW files. Reading Thermo RAW needs ThermoRawFileParser and full downloads, so the MVP should restrict deep checks to projects with mzML or search results.

### Idea 5 — `normbench`: a Python normalization and imputation benchmarking harness for LFQ/TMT matrices (VIABLE, moderate novelty)
**(a) Description and users.** The harness runs a grid of normalizations (median, quantile, VSN-like, LOESS, RLR) and imputations (MinProb, KNN, BPCA-like, RF/missForest, PIMMS models). It uses masking-based (MCAR/MNAR) error and ground-truth spike-in metrics (fold-change accuracy, DE recall/FDR on HYE or UPS1 benchmarks). Target users are method developers and analysts choosing a pipeline.

**(b) Gap and evidence.**
- PRONE (R/Bioconductor; Briefings in Bioinformatics 2025) systematically evaluates normalization. Its imputation support is minimal ("only a mixed imputation method") — [PRONE paper (PMC12058466)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12058466/)
- NAguideR (NAR 2020; R) evaluates 23 imputation methods — [PMC7641313](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7641313/)
- PIMMS (Nat Commun 2024; Python `pimms-learn` 0.5.2) includes "a workflow for comparison with other methods", focused on its deep-learning imputers — [GitHub RasmussenLab/pimms](https://github.com/RasmussenLab/pimms); [PyPI pimms-learn](https://pypi.org/project/pimms-learn/)
- ProteoBench benchmarks whole pipelines on fixed datasets, not normalization or imputation plug-ins — [PyPI proteobench 0.18.6](https://pypi.org/project/proteobench/)

**(c) Closest tools.** PRONE, NAguideR, PIMMS's comparison workflow and ProteoBench. The proposed tool differs by being Python-native with combined normalization × imputation × DE evaluation on spike-in ground truth.

**(d) Feasibility.** CPU-only. Uses scikit-learn, pimms-learn, pylimma/pydeqms for DE, and polars. Public ground truth: PXD028735 (LFQ benchmark, human/yeast/E. coli mixtures; TripleTOF) and PXD001819 (yeast-UPS1) — [PRIDE PXD028735](https://www.ebi.ac.uk/pride/archive/projects/PXD028735); [PRIDE PXD001819](https://www.ebi.ac.uk/pride/archive/projects/PXD001819). These would need re-searching, or use of deposited outputs.

**(e) MVP (2-3 weeks).** A plug-in registry with about 8 normalizers and 8 imputers, masking benchmarks, a spike-in DE benchmark on one dataset, and an HTML leaderboard.

**(f) Risks.** Crowded conceptually (PRONE, NAguideR). The novelty is the Python packaging and the combined evaluation. Results are dataset-specific: the PRONE authors report the impact of normalization is "highly dataset-specific" — [PMC12058466](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12058466/)

### Idea 6 — Immunopeptidomics dataset QC report (VIABLE, niche)
**(a) Description and users.** Given an immunopeptidomics result (FragPipe, Sage, mhcquant or MaxQuant) and HLA alleles from SDRF, the report computes:
- length distributions;
- predicted-binder fraction per allele (MHCflurry, CPU);
- unsupervised motif deconvolution;
- contaminant and non-specific cleavage rates.

Target users are HLA-peptidomics labs and neoantigen pipelines.

**(b) Gap and evidence.**
- IPTK, the Python immunopeptidomics toolkit, was last released on PyPI as 0.6.24 in Aug 2022 — [PyPI iptkl](https://pypi.org/project/IPTKL/); [IPTK paper (PMC8369717)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8369717/)
- pmultiqc already ingests nf-core/mhcquant results, which partly overlaps — [PyPI pmultiqc](https://pypi.org/project/pmultiqc/)
- MHCflurry 2.3.14 (Oct 2026) is maintained — [PyPI mhcflurry](https://pypi.org/project/mhcflurry/)

**(c) Closest tools.** IPTK (stale), pmultiqc mhcquant mode, and nf-core/mhcquant. The proposed tool differs by adding binding-prediction-based QC and motif summaries in a report.

**(d) Feasibility.** MHCflurry runs on CPU but needs model downloads of several hundred MB (size not verified). The SDRF corpus includes immunopeptidomics templates, though the count is not verified.

**(e) MVP.** 2 weeks.

**(f) Risks.** The pmultiqc/mhcquant teams may extend coverage. Community size is small.

### Idea 7 — `pxd-quickrun`: reanalysis helper from PXD to SDRF to small-subset Sage/quantms run (LOWER PRIORITY)
**(a) Description.** Given a PXD, the helper:
1. pulls the curated SDRF from bigbio, or drafts one;
2. selects N files;
3. fetches them via ppx/pridepy;
4. converts RAW to mzML;
5. runs Sage with parameters from the SDRF (via sdrf-pipelines converters);
6. emits QPX output and a pmultiqc report.

**(b)/(c) Evidence and closest tools.**
- quantms already reprocessed 83 datasets (about 29k files) driven by SDRF — [quantms Nat Methods 2024](https://link.springer.com/10.1038/s41592-024-02343-1)
- quantmsdiann runs DIA-NN from SDRF at scale — [Research Square preprint](https://www.researchsquare.com/article/rs-10319687)
- ppx and pridepy provide data access — [PyPI ppx](https://pypi.org/project/ppx/); [PyPI pridepy](https://pypi.org/project/pridepy/)
- The remaining gap is a lightweight, single-machine, "try 5 files in 10 minutes" UX, which is thin.

**(d)-(f).** The idea is feasible, but novelty is low and it depends on RAW conversion. The quantms and Nextflow ecosystem already covers this, so the main risk is redundancy.

### Ideas checked and dropped (summary)
- **Universal converter:** use qpx, see Q1 — [PyPI qpx](https://pypi.org/project/qpx/)
- **LLM SDRF annotation:** saturated by bigbio's AI-assisted corpus; see Q1 — [sdrf-annotated-datasets](https://github.com/bigbio/sdrf-annotated-datasets)
- **MSstats/msqrob2/proDA/DEqMS Python ports:** pymsstats, pyproda, pydeqms and MSqRobPy exist; see Q1 — [PyPI pymsstats](https://pypi.org/project/pymsstats/)
- **Single-cell Python toolkit:** scpviz exists — [JOSS](https://joss.theoj.org/papers/10.21105/joss.10303)
- **Generic HTML results report / USI viewer:** pmultiqc, alphastats GUI and multiple USI viewers exist — [PyPI pmultiqc](https://pypi.org/project/pmultiqc/); [PSI USI](https://www.psidev.info/usi)

### Inferences
- **Priority ranking for novelty × feasibility × testability on small public data:** Idea 1 (entrapment) ≈ Idea 4 (SDRF audit) > Idea 2 (QC drift/mzQC) > Idea 3 (PTM sites) > Idea 5 > Idea 6 > Idea 7.
- **Shared technical base:** all recommended ideas can consume QPX parquet or psm_utils as their input layer. Doing so avoids writing per-tool parsers and makes the tool complementary to the bigbio ecosystem rather than competing with it.
- Ideas 1 and 4 each produce a publishable "finding" in addition to software: FDP of tools on public data, and an error rate in AI-curated SDRFs. That helps adoption.
- None of the recommended ideas needs a GPU. Koina (`koinapy` 0.0.11, Aug 2026) could add optional spectral-similarity features remotely without local GPU — [PyPI koinapy](https://pypi.org/project/koinapy/)

### Gaps
- Whether the Wen et al. entrapment search results and raw files are deposited in PRIDE/MassIVE (accession numbers) was not verified.
- Specific public phosphoproteomics or immunopeptidomics PXDs with deposited DIA-NN/FragPipe outputs suitable for Ideas 3 and 6 were not identified.
- No verification of whether AlphaQuant (0.5.0, Aug 2026; [PyPI](https://pypi.org/project/alphaquant/)) already provides PTM site-level differential analysis. Check this before committing to Idea 3.
- The ProteoBench entrapment module page could not be fetched (JS/DNS issue), so its exact dataset and supported tools are unconfirmed beyond the search snippet.
- The licence and CPU runtime of DIA-NN in containers were not assessed.
