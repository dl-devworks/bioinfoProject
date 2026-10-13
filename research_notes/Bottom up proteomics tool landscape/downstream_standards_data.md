# Downstream bottom-up MS proteomics: quantification, statistics, QC, visualization, pipelines, standards and public data (status as of Oct 2026)

Method note: Repository activity was taken from a GitHub repository search run on 2026-10-13. For most repos the date shown is `pushed_at` (the last push to any branch). For PTXQC, LFQ-Analyst and spectrum_utils, only `updated_at` was returned, and that field also moves on non-code events such as stars. "NOASSERTION" means GitHub could not classify the license file (often GPL/Artistic variants in R packages); "None" means no license file was detected. Direct GitHub API calls and WebFetch were blocked in this environment, so some papers were read through curl.

---

## 1. Quantification (LFQ, isobaric, DIA), normalization and imputation

### Takeaway
Protein roll-up from peptides is effectively solved and has several open implementations: MaxLFQ (in MaxQuant, and as the C++ `iq::fast_MaxLFQ`), directLFQ (Python, linear scaling), FlashLFQ (C#), TMT-Integrator (Java) and MSstatsTMT (R). The weak spots are imputation and normalization. There is no consensus benchmark for DIA and single-cell data, and the recent comparisons are mostly by tool authors or limited to one dataset type.

### Cited Findings
- **directLFQ** (MannLabs; Python; Apache-2.0; 63 stars; last push 2026-07-15) is actively maintained — [GitHub](https://github.com/MannLabs/directlfq)
- directLFQ reports quantifying 10,000 proteomes in 10 min and 100,000 in under 2 h, with runtime scaling linearly in sample number. It claims to be about 1000-fold faster than *some* MaxLFQ implementations, and better than MaxLFQ on both DDA and DIA data. These are the authors' own benchmarks — [MCP paper / PMC10315922](https://pmc.ncbi.nlm.nih.gov/articles/PMC10315922); [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.02.17.528962v1); [PyPI](https://pypi.org/project/directlfq)
- **iq** R package (tvpham; C++/R; BSD-3-Clause; last push 2026-03-21) provides `fast_MaxLFQ`, a C++ implementation whose results equal the R version up to floating-point precision. Its vignette demonstrates a run with 3.37M rows, 3,554 proteins and 24 samples — [GitHub](https://github.com/tvpham/iq); [CRAN vignette](https://repo.miserver.it.umich.edu/cran/web/packages/iq/vignettes/iq-fast.html)
- MaxQuant states that MaxLFQ handles experiments of 500+ samples in manageable time — [UCSD summary of MaxQuant docs](https://bpmsf.ucsd.edu/protein-based-analysis/protein-quantification/Label%20Free%20Quantitation.html)
- **FlashLFQ** (smith-chem-wisc; C#; LGPL-3.0; last push 2026-10-06) is active — [GitHub](https://github.com/smith-chem-wisc/FlashLFQ)
- **AlphaQuant** (MannLabs; Python; Apache-2.0; last push 2026-10-01) is a newer Python package for peptide- and protein-level quantification and differential analysis — [GitHub](https://github.com/MannLabs/alphaquant)
- **TMT-Integrator** (Nesvilab; Java; Apache-2.0; 15 stars; last push 2026-06-25) is the isobaric roll-up step inside FragPipe — [GitHub](https://github.com/Nesvilab/TMT-Integrator)
- **MSstatsTMT** (Vitek-Lab; R; no license file detected on GitHub; last push 2026-10-05) is active — [GitHub](https://github.com/Vitek-Lab/MSstatsTMT)
- **Imputation benchmarks**:
  - A 2025 Nature Communications benchmark of DIA single-cell workflows tested zero, half-row-minimum, mean, median, kNN and iterative SVD imputation. Clustering accuracy (ARI) was more sensitive to the normalization choice than to the imputation choice — [Nat Commun 2025](https://www.nature.com/articles/s41467-025-65174-4)
  - Lupine, a deep model trained across many datasets, reports test MSE on the ProCan DIA dataset of 0.35, versus 0.42 for DreamAI, 0.45 for MissForest and 0.55 for kNN. This is a single dataset and the authors' own comparison — [PMC12753234](https://pmc.ncbi.nlm.nih.gov/articles/PMC12753234/)
  - A DDA-only study found BPCA best at medium missingness and random forest best in several high-missingness sectors — [PMC12136770](https://pmc.ncbi.nlm.nih.gov/articles/PMC12136770/)
  - A 2025 bioRxiv preprint argues for imputing retention-time boundaries (then re-integrating) rather than imputing intensities. It is not peer-reviewed — [bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.05.27.656394v1.full)
  - A 2025 PROTEOMICS review covers integration and imputation across omics — [Schumann et al. 2025](https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/10.1002/pmic.202400100)
- **ibaqpy** (2025, J Proteomics) is a Python package for iBAQ baseline quantification that is driven by SDRF metadata — [cited in ProteomeXchange 2026 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)

### Inferences
- Roll-up algorithms are commoditized in R (iq), Python (directLFQ, AlphaQuant) and C# (FlashLFQ). A new tool gains little from another roll-up algorithm. It would gain more from consistent ingestion and from wiring roll-up, normalization, imputation and testing together with uncertainty propagated through the steps.
- The imputation evidence is fragmented: most benchmarks cover one dataset or one acquisition type, and are written by method authors. An independent, reproducible benchmarking harness across DDA, DIA, TMT and single-cell data is a plausible gap.

### Gaps
- I did not find an independent 2024–2026 head-to-head benchmark of MaxLFQ vs directLFQ vs iq vs FlashLFQ vs AlphaQuant.
- I did not get the timing numbers from the iq vignette.
- I did not verify a dedicated normalization benchmark from 2024–2026, beyond the single-cell DIA paper.

---

## 2. Statistics and downstream analysis (R and Python packages, web apps)

### Takeaway
The statistics layer is dominated by R/Bioconductor:
- MSstats family, msqrob2/QFeatures, prolfqua, proDA, DEqMS, limma and protti are actively maintained.
- DEP and Proteus have had no pushes since 2022–2023.

Python has only AlphaPeptStats and AlphaQuant as broad options. Web apps mostly accept a single upstream format, or a few at protein level only, and new Shiny apps keep appearing without consolidating.

### Cited Findings
**Activity snapshot** (pushed_at, license, stars) — [GitHub search 2026-10-13]:

| Tool | Language | License | Stars | Last push | Status |
|---|---|---|---|---|---|
| [MSstats](https://github.com/Vitek-Lab/MSstats) | R | NOASSERTION | 102 | 2026-10-04 | active |
| [MSstatsConvert](https://github.com/Vitek-Lab/MSstatsConvert) | R | — | — | 2026-10-13 | active |
| [MSstatsShiny](https://github.com/Vitek-Lab/MSstatsShiny) | R | — | 21 | 2026-10-07 | active |
| [msqrob2](https://github.com/statOmics/msqrob2) | R | — | 15 | 2026-10-13 | active |
| [QFeatures](https://github.com/rformassspectrometry/QFeatures) | R | — | — | 2026-09-03 | active |
| [prolfqua](https://github.com/fgcz/prolfqua) | R | NOASSERTION | 48 | 2026-10-09 | active |
| [proDA](https://github.com/const-ae/proDA) | R | none detected | — | 2026-04-01 | active |
| [protti](https://github.com/jpquast/protti) | R | NOASSERTION | 66 | 2026-03-03 | active |
| [DEqMS](https://github.com/yafeng/DEqMS) | R | — | — | 2025-04-16 | slow |
| [DEP](https://github.com/arnesmits/DEP) | R | none detected | 35 | 2022-09-28 | stale on GitHub |
| [Proteus](https://github.com/bartongroup/Proteus) | R | MIT | — | 2023-04-17 | stale; MaxQuant-oriented per its [preprint](https://www.biorxiv.org/content/10.1101/416511.full.pdf) |
| [AlphaPeptStats](https://github.com/MannLabs/alphapeptstats) | Python | Apache-2.0 | 89 | 2025-11-21 | no push for ~11 months as of Oct 2026 |

**MSstatsConvert converters** — its devel NAMESPACE exports converters for:
- DIA-NN, DIA-Umpire, FragPipe, MaxQuant (LFQ and TMT), MetaMorpheus, MZmine, OpenMS (LFQ and TMT), OpenSWATH, Proteome Discoverer (LFQ and TMT), Philosopher (TMT), Progenesis, ProteinProspector (TMT), Skyline, SpectroMine (TMT) and Spectronaut.
- It also exports anomaly scoring (`MSstatsAnomalyScores`) and `CheckDataHealth`.
- Source: [NAMESPACE](https://raw.githubusercontent.com/Vitek-Lab/MSstatsConvert/devel/NAMESPACE)

**AlphaPeptStats** (Python) loads AlphaPept, DIA-NN, FragPipe, MaxQuant, Spectronaut and mzTab:
- Each loader is custom and protein-group level. For example, DIA-NN input is `pg_matrix.tsv` and DIA-NN versions before 1.7 are not supported.
- Spectronaut can be read at peptide level.
- The docs warn that column defaults change with upstream software versions.
- Source: [AlphaPeptStats import docs](https://alphapeptstats.readthedocs.io/en/main/import_data.html)

**perseuspy**, the Python bridge for Perseus plugins, had its last PyPI release (0.3.9) in November 2019. Perseus plugins are installed as .dll files copied into the Perseus folder — [piwheels](https://www.piwheels.org/project/perseuspy/); [PyPI](https://pypi.python.org/project/perseuspy/); [Perseus plugin store](https://maxquant.org/perseus_plugins/)

**FragPipe-Analyst** (MonashProteomics; GPL-3.0; 28 stars; last push 2026-06-10):
- Built on LFQ-Analyst code.
- Supports FragPipe LFQ-MBR, spectral counts, TMT and DIA workflows at protein, peptide and PTM-site level.
- Inputs are FragPipe-specific: IonQuant `combined_proteins.tsv`, DIA-NN `pg_matrix`, and TMT-Integrator reports, each plus an `experiment_annotation.tsv`.
- Sources: [GitHub](https://github.com/MonashProteomics/FragPipe-Analyst); [docs](https://fragpipe-analyst-doc.nesvilab.org/Formatting.html)

**LFQ-Analyst** (MonashBioinformaticsPlatform) is a one-click Shiny app for MaxQuant `proteinGroups.txt` — [GitHub](https://github.com/MonashBioinformaticsPlatform/LFQ-Analyst); [listing](https://github.com/Zenteomics/awesome-proteomics)

**PolySTest** (statistical testing with missing values) is now a Bioconductor package with a GitHub home under computproteomics — [GitHub](https://github.com/computproteomics/PolySTest); [Bioc mirror](https://github.com/bioc/PolySTest)

**Newer Shiny apps** show continuing fragmentation:
- ProVision: MaxQuant LFQ and TMT — [GitHub](https://github.com/JamesGallant/ProVision)
- QProMS: label-free, multiple search engines — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13278766/)
- TraianProt: wide-format MaxQuant, MSFragger, DIA-NN or PD output — [arXiv 2412.15806](https://arxiv.org/pdf/2412.15806)
- ProtVis: compares DEP, limma, DEqMS, proDA and MSstats — [GitHub](https://github.com/anhuikylin/ProtVis)
- xOmicsShiny: multi-omics — [Bioinformatics Advances 2025](https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf097/8145566)
- Dexdash: downstream DE Shiny app — [Dundee](https://www.compbio.dundee.ac.uk/user/mgierlinski/dexdash/dexdash.html)

**Python readers are appearing.** For example, `proteopy` has a DIA-NN reader that takes TSV for one version and parquet for DIA-NN ≥1.9.1, matching on a version string — [proteopy docs](https://proteopy.readthedocs.io/en/stable/api/generated/proteopy.read.diann.html)

### Inferences
- **No Python MSstats or msqrob2 equivalent.** Python has no mature, peer-reviewed counterpart to MSstats or msqrob2 that does feature-level linear mixed models, handles TMT, and comes with a broad converter layer like MSstatsConvert. AlphaPeptStats works at protein level and has had no push for ~11 months.
- **Format drift.** Every downstream tool keeps its own per-vendor, per-version loader. AlphaPeptStats documents version-sensitive column names, and proteopy uses version-matched DIA-NN readers. A shared, versioned ingestion library (Python + R) that outputs one long-format schema such as quantms.io or QFeatures could serve many tools.
- **Web apps are coupled to one upstream tool.** FragPipe-Analyst reads FragPipe output and LFQ-Analyst reads MaxQuant. New Shiny apps keep reimplementing the same DE/volcano/enrichment loop.

### Gaps
- I did not verify the current status of StatsPro, OmicsQ, POMAresults or limma for this snapshot. "ProteoDisco" may be a proteogenomics variant-database package rather than a stats app, but that is unverified.
- I found no source confirming whether Perseus (2.x) is Windows-only, or its 2024–2026 release cadence.
- No formal 2024–2026 review compares the downstream DE tools' accuracy across upstream formats; ProtVis only offers a side-by-side comparison inside its app.

---

## 3. Quality control (QC)

### Takeaway
The mzQC 1.0.0 standard (Feb 2024) now has Python, R and Java libraries. Per-run QC report tools exist, though PTXQC is centred on MaxQuant and mzTab. Longitudinal and cohort-scale QC is still served by older systems (QCloud, SIMPATIQCO) plus MSstatsQC. I found no evidence of wide mzQC adoption by producer tools.

### Cited Findings
- **mzQC** v1.0.0 was released as final by HUPO-PSI on 2024-02-21 — [psidev.info/mzqc](https://www.psidev.info/mzqc)
- The 2024 JASMS paper presents pymzqc, rmzqc and jmzqc, with a shared data model plus serialization and validation — [JASMS 2024 / PMC11311537](https://pmc.ncbi.nlm.nih.gov/articles/PMC11311537/)
- Repo activity:
  - HUPO-PSI/mzQC: last push 2026-10-06 — [GitHub](https://github.com/HUPO-PSI/mzQC)
  - pymzqc: BSD-3-Clause, 9 stars, last push 2026-09-20 — [GitHub](https://github.com/MS-Quality-Hub/pymzqc)
- **PTXQC** (cbielow; R/CRAN) generates quality reports from MaxQuant and mzTab results. Its repo was updated 2026-09-01 (`updated_at`) — [GitHub](https://github.com/cbielow/PTXQC); [CRAN mirror](https://github.com/cran/PTXQC)
- The PTXQC Shiny web-interface repo is archived — [GitHub](https://github.com/BioinformaticsSolutionCenter/PTXQC-ShinyWebinterface)
- **RawTools** (C#; Apache-2.0; last push 2026-10-12) parses raw scan data and computes QC metrics — [GitHub](https://github.com/kevinkovalchik/RawTools)
- **pmultiqc** (bigbio; Python; MIT; last push 2026-10-09) is a MultiQC-based proteomics QC report library — [GitHub](https://github.com/bigbio/pmultiqc)
- **MSstatsQC** does longitudinal system-suitability monitoring with control charts and change-point analysis. Its vignette was updated through Bioc 3.22 — [Bioconductor vignette](https://bioconductor.statistik.tu-dortmund.de/packages/3.22/bioc/vignettes/MSstatsQC/inst/doc/MSstatsQC.html)
- **QCloud** is a cloud-based longitudinal QC system with automated searching and inter-lab comparison, published in 2017 — [PMC5764250](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5764250/)
- **SIMPATIQCO** is an older (2013-era) QC database with a web viewer — [paper PDF](https://repub.eur.nl/pub/73457/pr300163u.pdf)

### Inferences
- **Lightweight cohort QC dashboard.** There is room for one that ingests DIA-NN, FragPipe, MaxQuant and Spectronaut outputs plus raw-file metrics. It would write and read mzQC, and track drift over thousands of runs. Existing tools are either per-run (PTXQC, pmultiqc), dated or service-based (QCloud), or R-only (MSstatsQC).

### Gaps
- I found no count of tools that natively emit or consume mzQC.
- I did not verify AlphaPeptStats' QC features, or whether any DIA-NN/Spectronaut-native cohort QC exists.

---

## 4. Visualization (spectra, coverage, PTMs)

### Takeaway
Spectrum visualization is well served:
- PDV (Java) and spectrum_utils (Python) are both maintained.
- USI-based viewers run at PRIDE and ProteomeCentral, and PeptideAtlas has the new Quetzal annotator.

Interactive, upstream-agnostic viewers for peptide coverage and PTM sites are less evident.

### Cited Findings
- **PDV** (wenbostar; Java; GPL-3.0; 68 stars; last push 2026-09-22) is active — [GitHub](https://github.com/wenbostar/PDV)
- **spectrum_utils** (bittremieuxlab; Python; 169 stars; updated 2026-08-21) handles processing and annotated-spectrum plotting — [GitHub](https://github.com/bittremieuxlab/spectrum_utils)
- **PRIDE Archive USI viewer**:
  - It can extract a scan directly from Thermo raw files via ThermoRawFileParser, which covers more than 80% of raw files in PRIDE.
  - A new PRIDE viewer shows multiple interpretations of one spectrum and compares them with predicted spectra.
  - It also shows SDRF metadata when available.
  - Source: [ProteomeXchange 2026 / PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **ProteomeCentral USI** queries all PROXI-implementing resources and renders the spectrum with Lorikeet. **Quetzal** (PeptideAtlas) annotates HCD spectra and exports publication-quality PDF/SVG from USIs or pasted peak lists — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **ThermoRawFileParser** (CompOmics; C#; Apache-2.0; 251 stars; last push 2026-09-30) — [GitHub](https://github.com/CompOmics/ThermoRawFileParser)

### Inferences
- **Spectrum plotting is not a gap.** A useful contribution would instead link statistical results (volcano or protein table) to peptide evidence, coverage, PTM sites and USI spectra across upstream tools.

### Gaps
- I did not verify the current status of IPSA, AlphaMap, Skyline releases, or peptide-coverage/PTM viewers such as AlphaMap. AlphaMap appears on PyPI ([pypi](https://pypi.org/project/alphamap)), but its activity was not checked.

---

## 5. Workflow managers and pipelines

### Takeaway
quantms (nf-core/bigbio; Nextflow; MIT) is the main open, SDRF-driven, cloud/HPC reanalysis pipeline. It is built on OpenMS and DIA-NN and has been used at scale. nf-core/mhcquant and Galaxy proteomics tools are active, and FragPipe ships its own workflow files.

### Cited Findings
- **bigbio/quantms**: Nextflow, MIT, 85 stars, last push 2026-10-09 — [GitHub](https://github.com/bigbio/quantms)
- quantms is an nf-core pipeline built on OpenMS and DIA-NN for cloud/HPC reanalysis with BioContainers — [PRIDE 2025 NAR / PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- quantms has processed more than 103 large-scale human studies: over 29,000 raw files from over 13,000 samples, quantifying more than 16,000 proteins — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/); [quantms.org/datasets](https://quantms.org/datasets)
- **nf-core/mhcquant**: Nextflow, MIT, last push 2026-10-08 — [GitHub](https://github.com/nf-core/mhcquant)
- **Galaxy proteomics** (galaxyproteomics/tools-galaxyp): MIT, last push 2026-09-18 — [GitHub](https://github.com/galaxyproteomics/tools-galaxyp)
- **FragPipe** (Nesvilab; Java; license NOASSERTION; 325 stars; last push 2026-08-07) provides built-in workflows covering LFQ, TMT and DIA — [GitHub](https://github.com/Nesvilab/FragPipe); [workflows doc](https://fragpipe.nesvilab.org/docs/tutorial_fragpipe_workflows.html)
- Neighbouring engines that pipelines call:
  - DIA-NN (C++; license NOASSERTION; 484 stars; last push 2026-09-16) — [GitHub](https://github.com/vdemichev/DiaNN)
  - AlphaDIA (Python; Apache-2.0; last push 2026-10-13) — [GitHub](https://github.com/MannLabs/alphadia)
  - Sage (Rust; MIT; 313 stars; last push 2026-10-07) — [GitHub](https://github.com/lazear/sage)

### Inferences
- **Downstream integration is where a new tool fits.** Pipelines (quantms, FragPipe) end at quant tables plus an MSstats or Analyst step. A tool that consumes quantms.io/mzTab/SDRF outputs from these pipelines for stats, QC and reporting would integrate easily, without competing with the pipelines themselves.

### Gaps
- I did not check whether the nf-core/quantms repo is still the canonical home versus bigbio/quantms; the search did not return the nf-core repo.
- I found no Snakemake proteomics pipeline with notable 2024–2026 adoption.

---

## 6. Standards and interoperability

### Takeaway
The PSI formats (mzIdentML, mzTab, mzQC, USI, ProForma, SDRF) are supported by the repositories. In practice, downstream tools mostly read vendor/tool-specific tables, using MaxQuant txt, DIA-NN parquet/tsv, FragPipe TSVs and Spectronaut exports through per-tool loaders.

- **SDRF tooling** (sdrf-pipelines, lesSDRF, the annotation repo) is active, but submitter uptake was very low as of 2023.
- **quantms.io** (Parquet: PSM, feature, protein and differential tables keyed to SDRF) is the emerging columnar exchange format, with an OpenMS writer.

### Cited Findings
- **ProteomeXchange format support.** Resources support mzML, mzIdentML and mzTab, plus USI, ProForma 2.0 and PSI-MS CV, and maintain open-source parsers for them — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **PRIDE submission formats.** The PX Submission Tool accepts raw, processed results, mzTab, mzIdentML, peak lists and SDRF. SDRF has been supported since 2022 and is added by choosing the file type 'EXPERIMENTAL DESIGN' — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- **SDRF uptake.** Only 156 of 9,671 datasets (1.6%) submitted to PRIDE after SDRF was introduced in mid-2022 contained submitter-supplied SDRF — [lesSDRF, Nat Commun 2023](https://www.nature.com/articles/s41467-023-42543-5)
- The 2026 ProteomeXchange update says SDRF adoption "is growing" but gives no count — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **SDRF authoring tools:**
  - FragPipe exports an SDRF draft with search parameters and file names, but *not sample details* — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
  - MaxQuant is "starting to support" SDRF — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
  - PRIDE is working with MaxQuant and Proteome Discoverer on SDRF adoption — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- SDRF has been extended to crosslinking and top-down proteomics, and community annotation of existing datasets lives in the bigbio repo — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- Extensions to other subdomains such as metaproteomics are ongoing — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **jPOST / JPDM SDRF effort.** jPOST drafts SDRF ("jeSDRF") files for submitters, linked to data-descriptor papers in the Journal of Proteome Data and Methods (JPDM), and is converting lesSDRF-created PRIDE SDRFs to jeSDRF — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **SDRF repo activity:**
  - bigbio/proteomics-sample-metadata: GPL-2.0, 116 stars, last push 2026-10-13 — [GitHub](https://github.com/bigbio/proteomics-sample-metadata)
  - sdrf-pipelines: Python, Apache-2.0, last push 2026-10-10 — [GitHub](https://github.com/bigbio/sdrf-pipelines)
  - lesSDRF: Apache-2.0, 10 stars, last push 2025-10-15 — [GitHub](https://github.com/CompOmics/lesSDRF)
- **quantms.io.** The protein table is Parquet:
  - Required fields include accessions (list), best search-engine score, abundance, an SDRF-linked sample accession, global q-value and a decoy flag — [quantms.io protein docs](https://quantmsio.readthedocs.io/en/stable/protein.html)
  - A project manifest ties together feature, PSM, SDRF and differential-expression files — [quantms.io tools](https://quantmsio.readthedocs.io/en/latest/tools.html)
- **OpenMS QuantmsIO writer.** OpenMS has a `QuantmsIO` class that writes PSM Parquet per the quantms.io spec. Several fields (modifications, protein accessions, ion mobility) are currently written as null — [OpenMS docs](https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1QuantmsIO.html)
- **HUPO-PSI/mzTab** (Java reference): last push 2026-06-12 — [GitHub](https://github.com/HUPO-PSI/mzTab)
- **Upstream ingestion in practice:**
  - MSstatsConvert has the broadest converter set, listed in section 2 — [NAMESPACE](https://raw.githubusercontent.com/Vitek-Lab/MSstatsConvert/devel/NAMESPACE)
  - AlphaPeptStats reads 5 tools plus mzTab at protein level — [docs](https://alphapeptstats.readthedocs.io/en/main/import_data.html)
  - FragPipe-Analyst reads FragPipe output only — [docs](https://fragpipe-analyst-doc.nesvilab.org/Formatting.html)
  - DIA-NN moved to parquet reports around 1.9.x, and downstream Python readers branch on version — [proteopy](https://proteopy.readthedocs.io/en/stable/api/generated/proteopy.read.diann.html)
  - QFeatures has a `readQFeatures` vignette for multi-format ingestion — [QFeatures vignette](https://free.nchc.org.tw/bioconductor/devel/bioc/vignettes/QFeatures/inst/doc/readQFeatures2.html)

### Inferences
- **Converters are the main gap.** A versioned, tested converter layer with a stable column schema (quantms.io/Parquet or QFeatures-compatible) for MaxQuant txt, DIA-NN parquet, FragPipe and Spectronaut is the main interoperability need. MSstatsConvert covers it in R only, and its output is MSstats-specific.
- **Missing SDRF is the main barrier to automated reanalysis.** quantms relies on deposited SDRF. Tools that infer or draft SDRF from file names, the PRIDE project description and publications would add value; jPOST does this by hand today, and FragPipe drafts omit sample details.

### Gaps
- I could not find a 2025–2026 count or percentage of PRIDE/PX datasets with SDRF; the latest hard figure is the 1.6% from 2023.
- I could not confirm the exact DIA-NN 2.x report.parquet schema changes, or which downstream tools have updated for 2.x.
- I could not determine how many tools write mzTab 2.0/mzTab-M, or the current mzIdentML 1.3 status.

---

## 7. Public data resources and programmatic reuse

### Takeaway
ProteomeXchange holds about 64k datasets, 77% of them in PRIDE, and growth is accelerating (10,686 submissions in 2024). Programmatic access exists: PRIDE REST v2/v3, pridepy, PROXI/OpenAPI at ProteomeCentral, and USIs. Systematic quantitative reanalysis still covers only a small fraction of datasets:
- MassIVE.quant: 209 reanalyses of 105 datasets
- Expression Atlas: 109 proteomics datasets
- quantms: more than 103 human studies

Fewer than 10% of PRIDE datasets are mentioned as reanalysed.

### Cited Findings
- **ProteomeXchange totals (through June 2025):**
  - 64,330 datasets submitted: 44,248 (69%) public and 20,082 (31%) private.
  - 47% were submitted in the last 3 years.
  - 2024 was a record year with 10,686 datasets, about 890 per month.
  - Source: [ProteomeXchange 2026, NAR / PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **By resource:**

  | Resource | Datasets | Share |
  |---|---|---|
  | PRIDE | 49,528 | 77% |
  | iProX | 6,967 | 11% |
  | MassIVE | 4,770 | 7.4% |
  | jPOST | 2,443 | 3.8% |
  | Panorama Public | 478 | 0.7% |
  | PeptideAtlas/PASSEL | 144 | 0.2% |

  iProX is now the second-largest source of new PXDs — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
- **ProteomeCentral** was rewritten on a PROXI back-end, with faceted search and pagination through an OpenAPI endpoint — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/); [PROXI schemas](https://github.com/HUPO-PSI/proxi-schemas)
- **PRIDE REST API** (https://www.ebi.ac.uk/pride/ws/archive/v2/) supports queries by date, protein and file, plus SQL-like keyword combination. Newer additions include a file-streaming API — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- A v3 search endpoint also responds (`/pride/ws/archive/v3/search/projects`, checked via curl 2026-10-13) — [endpoint](https://www.ebi.ac.uk/pride/ws/archive/v3/search/projects?keyword=sdrf&pageSize=1)
- **pridepy** (PRIDE-Archive; Python; Apache-2.0; 42 stars; last push 2026-07-29) is the official Python client — [GitHub](https://github.com/PRIDE-Archive/pridepy)
- **PRIDE usage and reuse:**
  - Average submissions are about 534 datasets per month — [PRIDE 2025 NAR](https://academic.oup.com/nar/article/53/D1/D543/7874848)
  - More than 100 TB per month was downloaded on average from Jan 2022 to Jul 2024, peaking at over 450 TB in Sep 2022.
  - Datasets mentioned as reanalysed in EuropePMC are under 10% of public PRIDE datasets.
  - Transfers support FTP, Aspera and the newly added Globus.
  - Source for the last three points: [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- **Reanalysis resources:**
  - MassIVE.quant stores raw data, experimental design, scripts, intermediate files, and alternative reanalyses as branches. It holds 209 reanalyses of 105 datasets — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/); [MassIVE.quant](https://massive.ucsd.edu/ProteoSAFe/static/massive-quant.jsp)
  - Expression Atlas had protein abundance from 109 reanalysed proteomics datasets as of Aug 2024 — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
  - jPOST does repository-level quantitative reanalysis with a multi-search-engine indicator for DDA and emPAI-based spectral counting — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
  - PeptideAtlas builds (e.g. Arabidopsis, maize, *C. albicans*, rice) and PTMeXchange PTM builds feed UniProtKB, as of Aug 2025 — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
  - Other reusers include Scop3P, OpenProt, MatrisomeDB and ProteomeHD — [PMC11701690](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701690/)
- **Planned work:** ProteomeXchange plans controlled-access human proteomics resources and support for non-MS proteomics — [PMC12807779](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)

### Inferences
- **Reuse lags supply.** Reanalysis rate (under 10% of datasets; on the order of 100–300 for systematic quantitative reanalyses) lags far behind supply (about 44k public datasets). The low SDRF rate (1.6% in 2023) and heterogeneous processed-result formats are the obvious bottlenecks.
- **Opportunity.** A tool that turns a PXD into analysis-ready, SDRF-annotated quant tables, by retrieving and normalizing deposited search-engine outputs where present, could tap this large under-used pool without full raw reprocessing.

### Gaps
- I found no current count of PRIDE datasets carrying processed quantitative outputs by tool (MaxQuant txt vs DIA-NN vs FragPipe), nor of "complete" vs "partial" submissions.
- I did not verify current dataset counts or API details for PeptideAtlas, ProteomicsDB, iProX or jPOST APIs.
- I could not get rate limits or reliability metrics for the PRIDE APIs.
