# Upstream Bottom-Up Proteomics Software Ecosystem (DDA + DIA), 2024-2026

Method note (read first): Research done 2026-10-13. The GitHub API and bioconda/anaconda API were **blocked** in this session (proxy refused). Maintenance signals therefore come from (a) the **PyPI JSON API** (`https://pypi.org/pypi/<pkg>/json`) and **crates.io API** (`https://crates.io/api/v1/crates/<crate>`), queried live on 2026-10-13; (b) GitHub *release pages* fetched as HTML (these show day/month but often **not the year**, so years marked "(year inferred)" are my inference, not verified); (c) papers. Star counts were mostly NOT obtainable. Items marked "[background, unverified this session]" come from prior knowledge and should be re-checked before being quoted.

## Raw data access & conversion (vendor files, mzML/mzMLb/mzPeak, readers)

### Takeaway
Thermo access has largely been solved cross-platform (ThermoRawFileParser 2.0-dev on .NET 8, no Mono; DIA-NN 2.1 native .raw on Linux), and Bruker timsTOF is served by the Rust `timsrust` crate (now under MannLabs) plus `alphatims`/`alpharaw`. The format layer is in transition: mzML remains the lingua franca, while a Parquet-based successor, **mzPeak**, was published in JPR (Oct 2025) and is chartered by HUPO-PSI but is still work-in-progress with immature tooling — a clear opportunity area. Rust (mzdata ecosystem) and Python (pyteomics, pyOpenMS) readers are healthy and actively released.

### Cited Findings
**ThermoRawFileParser (TRFP; C#, Apache-2.0 [background])**
- Latest is v2.0.0-dev ("Latest", 27 Oct; year not shown on page): moves to .NET 8 and drops Mono dependency; GitHub Actions builds self-contained binaries for major platforms; Parquet output format updated to 0.2; charge-state arrays in mzML/MGF; precursor/neutral-loss scan support; PSI-MS CV 4.1.204 — [TRFP releases](https://github.com/compomics/ThermoRawFileParser/releases)
- Prior stable line: v1.4.5 (PROXI CV fixes), v1.4.4, v1.4.3 (Thermo .NET assemblies 5.0.0.93, **Astral support**, PRM without MS1), outputs mzML, MGF, Parquet, JSON/text metadata, `xic` subcommand — [TRFP releases](https://github.com/compomics/ThermoRawFileParser/releases)
- Pain point: depends on Thermo's proprietary RawFileReader .NET assemblies (bundled under Thermo license) — [TRFP releases](https://github.com/compomics/ThermoRawFileParser/releases) (assembly versions listed); licensing details [background, unverified this session].

**ProteoWizard msconvert (C++, Apache-2.0 core + vendor DLLs)**
- Vendor reading (Thermo, Bruker, Sciex, Waters, Agilent) relies on Windows vendor DLLs; on Linux it is typically run via a Wine-based Docker image — [background, unverified this session; see https://proteowizard.sourceforge.io/download.html]. GitHub/SourceForge release activity could not be checked (API blocked).
- A PyPI package named `msconvert` (v1.3.post3, 2024-12-19, AGPL) exists but is a third-party wrapper, not ProteoWizard itself — [PyPI msconvert](https://pypi.org/pypi/msconvert/json)

**Bruker timsTOF (.d / TDF)**
- `timsrust` (Rust crate) v0.6.7 updated 2026-10-08, 32,360 downloads; repository now `github.com/MannLabs/timsrust` (moved from sweenylab) — [crates.io timsrust](https://crates.io/api/v1/crates/timsrust)
- An ASMS 2026 poster describes "timsRust" as a Rust crate ecosystem whose outputs are consumed by downstream tools such as Sage — [ASMS 2026 poster PDF](https://lcms.labrulez.com/labrulez-bucket-strapi-h3hsga3/asms_2026_thp_338_timsrust_6fd0fde290.pdf)
- Python binding `timsrust_pyo3` last release 0.4.1 on 2024-12-10 (lagging the core crate) — [PyPI timsrust_pyo3](https://pypi.org/pypi/timsrust_pyo3/json)
- `alphatims` (Python, Apache-2.0) v1.1.1, 2026-06-03 — [PyPI alphatims](https://pypi.org/pypi/alphatims/json)
- `alpharaw` (MannLabs, Python, Apache-2.0; Thermo/Sciex/Bruker readers used by AlphaDIA/AlphaPeptDeep) v0.7.1, 2026-08-31 — [PyPI alpharaw](https://pypi.org/pypi/alpharaw/json)
- Sage only added "unstable preliminary Bruker .d (ddaPASEF) reading" in v0.14.4, and diaPASEF search only in the v0.15.0 betas — [Sage releases](https://github.com/lazear/sage/releases)

**Open formats**
- mzPeak paper: "mzPeak: Designing a Scalable, Interoperable, and Future-Ready Mass Spectrometry Data Format," J Proteome Res, published 2025-10-02, DOI 10.1021/acs.jproteome.5c00435, co-authors include Deutsch, Martens, Vizcaíno, Kohlbacher — [PMC12604042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12604042/) (full text could not be fetched; DNS failure)
- HUPO-PSI MS working group charter lists as a goal a next-generation, faster and smaller MS run format based on Parquet, tentatively named mzPeak — [PSI MS WG charter](https://www.psidev.info/mass-spectrometry-standards-working-group-charter)
- No evidence found that mzPeak has been formally ratified as a PSI standard; no `mzpeak` crate on crates.io (queried) — [crates.io query](https://crates.io/api/v1/crates/mzpeak); third-party pages describe mzPeak as a ZIP of Parquet tables (spectrum metadata, signal, peaks, chromatograms), read-only Python implementation, and a Java reader with a FragPipe/MSFTBX adapter (low-quality sources, treat as unverified) — [gitblind mirror topic](https://gitblind.noratr.app/topics/mzpeak)
- TRFP already emits its own Parquet format (v0.2) — a parallel, non-mzPeak Parquet dialect — [TRFP releases](https://github.com/compomics/ThermoRawFileParser/releases); DIA-NN 1.9.1 saves empirical libraries as .parquet and DIA-NN 2.x writes report.parquet — [DIA-NN releases](https://github.com/vdemichev/DiaNN/releases); Sage writes parquet output — [Sage releases](https://github.com/lazear/sage/releases). Parquet is becoming de-facto, but each tool uses its own schema.
- mzSpecLib (HUPO-PSI spectral-library format) Python reference `mzspeclib` v1.0.7, 2025-06-19 — [PyPI mzspeclib](https://pypi.org/pypi/mzspeclib/json); mzPAF (peak-annotation format) `mzpaf` 0.2.0b0, 2024-12-06 (still beta) — [PyPI mzpaf](https://pypi.org/pypi/mzpaf/json)

**Readers / libraries**
- `mzdata` (Rust, mobiusklein): v0.67.4, updated 2026-10-10, 86,323 downloads — [crates.io mzdata](https://crates.io/api/v1/crates/mzdata); companion `mzpeaks` 1.0.9 (2025-05-25) and `mzsignal` 1.1.12 (2026-05-27) — [crates.io mzpeaks](https://crates.io/api/v1/crates/mzpeaks), [crates.io mzsignal](https://crates.io/api/v1/crates/mzsignal)
- `rustyms` (Rust, peptide/identified-peptide file handling, with Python bindings) 0.11.0 (2025-09-25); new `mzcore` crate under `rusteomics` org 0.2.0 (2026-08-04) — [crates.io rustyms](https://crates.io/api/v1/crates/rustyms), [crates.io mzcore](https://crates.io/api/v1/crates/mzcore)
- `pyteomics` 5.0.1, 2026-07-22 — [PyPI pyteomics](https://pypi.org/pypi/pyteomics/json)
- `pyopenms` 3.6.0, 2026-09-30 — [PyPI pyopenms](https://pypi.org/pypi/pyopenms/json); `pyopenms_viz` 1.2.0, 2026-09-10 — [PyPI pyopenms_viz](https://pypi.org/pypi/pyopenms_viz/json)
- `pymzml` 2.7.0, 2026-09-07 (MIT) — [PyPI pymzml](https://pypi.org/pypi/pymzml/json)
- `spectrum_utils` 0.5.0, 2025-11-27 (Apache-2.0) — [PyPI spectrum_utils](https://pypi.org/pypi/spectrum_utils/json)

### Inferences
- The vendor-access bottleneck is now mostly about **Sciex/Waters/Agilent and Bruker writing**, not Thermo reading; Thermo/Bruker reading is solved in .NET (TRFP), Rust (timsrust) and Python (alpharaw/alphatims).
- Parquet is converging as the storage substrate but schemas are fragmented (TRFP Parquet, Sage parquet, DIA-NN parquet, mzPeak). A well-tested mzPeak reader/writer (Rust core + Python bindings) and converters from mzML/TRFP-parquet are a plausible single-developer gap.
- Python bindings for timsrust lag the Rust crate by ~2 years (0.4.1 vs 0.6.7), an interop gap.

### Gaps
- Could not verify ProteoWizard release cadence, GitHub stars, or current Linux story (API blocked). mzPeak spec details, benchmarks and implementation list could not be read (PMC fetch failed).
- Bruker `timsdata` SDK status and license not checked. mzMLb adoption not checked.

## Database search engines (DDA, open/glyco/crosslink) and de novo

### Takeaway
The DDA search field is dominated by MSFragger (closed academic license, commercial via Fragmatics since May 2025) and Sage (MIT, Rust, very fast, but release cadence slowed — last stable v0.14.7 with v0.15 still in beta). Comet, MS-GF+, X!Tandem remain as open legacy workhorses (largely via OpenMS/quantms). De novo is an active ML area (Casanovo 5.x actively released; InstaNovo 1.2) with benchmarking inconsistency acknowledged.

### Cited Findings
**Sage (Rust, MIT)**
- Paper: Lazear MR, "Sage: An Open-Source Tool for Fast Proteomics Searching and Quantification at Scale," J Proteome Res 2023, 22(11):3652-3659, doi 10.1021/acs.jproteome.3c00486; covers search, RT prediction, isobaric & LFQ quantification, PSM rescoring and FDR — [Sage docs in quantms](https://quantms.readthedocs.io/en/latest/sage.html), [bioinformaticshome](https://bioinformaticshome.com/db/tool/Sage-proteomics)
- Releases: v0.14.7 (15 Mar, marked "Latest"; parquet semi_enzymatic/missed_cleavages columns), v0.14.6 (MGF reader, ion-mobility model feature), v0.14.5 (semi-enzymatic, `--annotate-matches`, opt-out telemetry), v0.14.4 (unstable Bruker ddaPASEF reading). v0.15.0-beta.1 adds initial LFQ for ion mobility, initial diaPASEF search, selectable hyperscore; notes it is "still in beta and not ready for production-use" — [Sage releases](https://github.com/lazear/sage/releases) (year of v0.14.7 believed 2024 [inferred])
- Within quantms, Sage is reported mid-pack vs MS-GF+ and Comet on PSM counts while being much faster — [quantms Sage docs](https://quantms.readthedocs.io/en/latest/sage.html)
- Sage is packaged as an nf-core module — [Nextflow registry](https://registry.nextflow.io/modules/nf-core/sageproteomics/sage)
- A separate Python ecosystem, `sagepy` (Python bindings to Sage core, used by e.g. timsTOF/imspy work [background]), is actively released: v0.4.6 on 2026-10-07 — [PyPI sagepy](https://pypi.org/pypi/sagepy/json)
- Name collision: crates.io `sage-core`/`sage-cli` belong to an unrelated project (majiayu000/sage) — [crates.io sage-core](https://crates.io/api/v1/crates/sage-core); Sage proteomics is not published as a reusable crate on crates.io under that name.

**MSFragger / FragPipe (Java; closed academic license)**
- MSFragger license: academic research, non-commercial or educational use only; from May 1, 2025 commercial licensing of the MSFragger suite is handled by Fragmatics, LLC, not U-Michigan — [MSFragger license PDF](https://abibuilder.cs.uni-tuebingen.de/archive/openms/private-thirdparties/All/MSFragger/MSFragger-LICENSE.pdf), [U-M available inventions](https://available-inventions.umich.edu/product/msfragger-ultrafast-and-comprehensive-identification-of-peptides-from-tandem-mass-spectra), [IonQuant academic license](https://msfragger-upgrader.nesvilab.org/ionquant/LICENSE-ACADEMIC.pdf)
- FragPipe releases: 24.0 (24 Dec; MSFragger 4.4, IonQuant 1.11.18, diaTracer 2.2.1; MSBooster transfer learning, Skyline quant with mProphet, Astral Zoom TMT, FragAnnotator, diaTracer Synchro-/Slice-PASEF); 23.1 (30 Jun; MSFragger 4.3; metaproteomics DB module; Prosit MultiFrag via MSBooster); 23.0 (03 May; MSFragger 4.2; Windows installer with bundled Python; TMT35-plex); 22.0 (diaTracer introduced; Koina support in MSBooster; DDA+; Skyline integration) — [FragPipe releases](https://github.com/Nesvilab/FragPipe/releases) (years not shown; 24.0 is likely Dec 2025 [inferred])

**Other search engines**
- OpenMS/quantms integrates Comet, MS-GF+ and Sage as DDA engines — [quantms Sage docs](https://quantms.readthedocs.io/en/latest/sage.html)
- Comet (C++, Apache-2.0), MS-GF+ (Java), X!Tandem (C++, legacy), MetaMorpheus (C#, open/G-PTM-D search, glyco, crosslink), MaxQuant/Andromeda (C#/.NET, free, closed source), Mascot (Matrix Science, commercial), PEAKS (Bioinformatics Solutions, commercial, includes de novo) — [background, unverified this session; repos: https://github.com/UWPR/Comet, https://github.com/MSGFPlus/msgfplus, https://github.com/smith-chem-wisc/MetaMorpheus]. Release dates could not be checked (GitHub API blocked).
- MaxQuant 2.7.5.0 exists and runs on Linux via `dotnet` on HPC (Manchester CSF3); 2.6.6.0 lists dotNET 8.0.404 as prerequisite — [Manchester CSF3](https://ri.itservices.manchester.ac.uk/csf3/software/applications/maxquant/), [Copenhagen](https://fssw.ku.dk/envmod/MaxQuant.html). MaxDIA (DIA in MaxQuant) dates from MaxQuant 2.0 (2021) — [MPG news](https://www.mpg.de/17057403/maxdia-taking-proteomics-to-the-next-level). No official 2.7 release notes found.

**De novo**
- Casanovo (Python/PyTorch, Apache-2.0) v5.2.1 released 2026-08-12 — [PyPI casanovo](https://pypi.org/pypi/casanovo/json)
- InstaNovo (InstaDeep) v1.2.2, 2025-12-05 — [PyPI instanovo](https://pypi.org/pypi/instanovo/json); transformer trained on 28M labelled ProteomeTools spectra, plus diffusion refinement InstaNovo+ — [InstaNovo bioRxiv](https://www.biorxiv.org/content/10.1101/2023.08.30.555055.full.pdf); developer claim of 41.8% more PSMs than Casanovo reported secondhand — [HPCwire 2025](https://www.hpcwire.com/2025/04/10/new-ai-tool-unlocks-hidden-proteins-in-sequencing-breakthrough/)
- NovoBench (2024) was created because "there is no consensus for the evaluation datasets" and results across de novo papers are often not comparable — [NovoBench arXiv](https://arxiv.org/pdf/2406.11906)

### Inferences
- The only fully open (OSI-licensed), modern, fast DDA engine is Sage; its main line has slowed (v0.15 in beta), and timsTOF/DIA support in it is incomplete. This leaves room for an open, library-first search engine (or contributions to Sage) with first-class ion mobility and DIA.
- FragPipe is the most feature-complete free academic stack but cannot be redistributed or used commercially without Fragmatics; this blocks inclusion in fully open pipelines (OpenMS keeps MSFragger in "private-thirdparties").
- De novo tools publish frequently but benchmark comparability is weak — standard evaluation infrastructure is a gap.

### Gaps
- No verified data on Comet/MS-GF+/MetaMorpheus/X!Tandem release dates or activity; glycan (MSFragger-Glyco, pGlyco3, O-Pair) and crosslink (XlinkX, xiSEARCH, Scout) tools not researched in this session.
- PEAKS/Mascot/Proteome Discoverer pricing and current versions not researched.

## DIA analysis and spectral library prediction

### Takeaway
DIA-NN 2.x (academic-only binaries; enterprise via Aptila Biotech; Linux builds incl. native .raw since 2.1) and Spectronaut (commercial) dominate; AlphaDIA (open, Apache-2.0, Nature Biotechnology 2025) is the leading open-source challenger and is released very actively (2.2.0 on 2026-10-08). FragPipe-DIA (diaTracer + MSFragger-DIA) and the OpenMS/quantms route (which itself delegates DIA to DIA-NN) round out the field.

### Cited Findings
- DIA-NN 2.0 (29 Jan 2025): binaries "for academic use"; industry distribution via Aptila Biotech; Linux zips provided; point releases 2.0.1/2.0.2 (Feb 2025), 2.1.0 (25 Mar 2025; native .raw on Linux), 2.2.0 (30 May 2025); features: proteoform confidence, DL model fine-tuning for specific data/PTMs, scanning PASEF, tunable decoy models, non-specific digests, QuantUMS — [DIA-NN releases](https://github.com/vdemichev/DiaNN/releases)
- DIA-NN 1.9.x: "free Academia-only version"; 1.9 Windows-first with Linux following; 1.9.1 saves empirical libraries as .parquet — [DIA-NN releases](https://github.com/vdemichev/DiaNN/releases)
- DIA-NN is closed source (binaries only) — implied by the binary-only academic release model — [DIA-NN releases](https://github.com/vdemichev/DiaNN/releases)
- AlphaDIA: "AlphaDIA enables DIA transfer learning for feature-free proteomics," Nature Biotechnology 2025, DOI 10.1038/s41587-025-02791-w — [Nature Index entry](https://www.nature.com/nature-index/article/10.1038/s41587-025-02791-w); end-to-end transfer learning with fully predicted libraries, enabling DIA search of any PTM — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.05.28.596182.full.pdf); open source, Windows/Linux/Mac — [AlphaDIA docs](https://alphadia.readthedocs.io/en/latest/); v2.2.0 on PyPI 2026-10-08, Apache — [PyPI alphadia](https://pypi.org/pypi/alphadia/json)
- FragPipe-DIA: diaTracer (pseudo-MS/MS from diaPASEF) introduced in FragPipe 22; diaTracer 2.2.1 adds Synchro-/Slice-PASEF in FragPipe 24.0; Skyline quant with mProphet scoring — [FragPipe releases](https://github.com/Nesvilab/FragPipe/releases)
- quantms (nf-core, Nat Methods 2024 21:1603-1607) reanalyzed 83 ProteomeXchange datasets / 29,354 files; its DIA route runs DIA-NN — [quantms paper](https://link.springer.com/10.1038/s41592-024-02343-1), [quantms GitHub](https://github.com/ypriverol/quantms); 2026 preprint "quantmsdiann" runs DIA-NN across cloud/HPC driven by SDRF and reports up to 59% more protein groups vs deposited results — [Research Square](https://www.researchsquare.com/article/rs-3002027/v1) (note: this URL may be the original quantms preprint; attribution from search summary, unverified)
- EncyclopeDIA, Skyline, OpenSWATH (OpenMS), Spectronaut (Biognosys, commercial) — [background, unverified this session]

**Library / property prediction**
- AlphaPeptDeep (`peptdeep`) 1.5.1, 2026-07-30 — [PyPI peptdeep](https://pypi.org/pypi/peptdeep/json)
- MS2PIP 4.2.0, 2026-07-13 — [PyPI ms2pip](https://pypi.org/pypi/ms2pip/json); DeepLC 4.5.0, 2026-09-11 — [PyPI deeplc](https://pypi.org/pypi/deeplc/json)
- Koina (model-serving for Prosit etc.) client `koinapy` 0.0.11, 2026-08-12 — [PyPI koinapy](https://pypi.org/pypi/koinapy/json); FragPipe's MSBooster supports Koina servers and Prosit MultiFrag — [FragPipe releases](https://github.com/Nesvilab/FragPipe/releases)

### Inferences
- The leading DIA engines (DIA-NN, Spectronaut) are closed; AlphaDIA is the only actively developed, peer-reviewed, permissively licensed full DIA search engine. Even the flagship open pipeline (quantms) relies on closed DIA-NN for DIA.
- DIA-NN licensing (academic-only, enterprise via Aptila) restricts commercial open pipelines — a structural gap for open DIA.

### Gaps
- Could not verify EncyclopeDIA/OpenSWATH maintenance status, Spectronaut version, or Skyline release cadence.

## Rescoring/ML and FDR control (incl. critiques)

### Takeaway
Rescoring is a mature, mostly-open Python ecosystem (MS2Rescore 4.x, Oktoberfest, MS2PIP, DeepLC, Koina), with Percolator as the classic backend and mokapot as the Python reimplementation (but mokapot's last PyPI release is 0.10.0 from Sept 2023). The biggest scientific issue is FDR validity: Wen et al. (Nat Methods 2025) showed no DIA tool tested (DIA-NN, Spectronaut, EncyclopeDIA) consistently controls peptide-level FDR, especially on single-cell data; ProteoBench now has an entrapment module.

### Cited Findings
- MS2Rescore 4.0.2, 2026-09-07 — [PyPI ms2rescore](https://pypi.org/pypi/ms2rescore/json)
- Oktoberfest (Prosit-based rescoring, Wilhelm lab) 0.11.1, 2026-07-16 — [PyPI oktoberfest](https://pypi.org/pypi/oktoberfest/json)
- mokapot latest PyPI release 0.10.0 on 2023-09-11 (Apache-2.0) — [PyPI mokapot](https://pypi.org/pypi/mokapot/json) — indicates stalled public releases
- inSPIRE (QuantSysBio rescoring for immunopeptidomics) — not found on PyPI under `inspire-ms` — [PyPI query](https://pypi.org/pypi/inspire-ms/json); status unverified.
- Wen B, Freestone J, Riffle M, MacCoss MJ, Noble WS, Keich U. "Assessment of false discovery rate control in tandem mass spectrometry analysis using entrapment," Nature Methods, 16 June 2025, DOI 10.1038/s41592-025-02719-x: of three common entrapment estimation methods, one is invalid, one only a lower bound, one valid but underpowered; proposes a more powerful method; finds no DIA tool consistently controls FDR, worst on single-cell data — [PMC12240826](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12240826/), [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.06.01.596967.full.pdf)
- DIA tools evaluated: DIA-NN, Spectronaut, EncyclopeDIA — [bioRxiv preprint PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11185562/)
- ProteoBench has a "DIA Ion Entrapment – Astral" module based on Wen et al. 2025 — [ProteoBench docs](https://proteobench.readthedocs.io/en/latest/available-modules/active-modules/13-entrapment-ion-dia-astral/); `proteobench` 0.18.6 released 2026-10-05 — [PyPI proteobench](https://pypi.org/pypi/proteobench/json)
- DIA-NN 2.0 added "tunable decoy models" and 1.9.2 an experimental "Conservative" ML mode — [DIA-NN releases](https://github.com/vdemichev/DiaNN/releases) (possibly responsive to FDR concerns; inference)

### Inferences
- An open, tool-agnostic FDR/entrapment validation library (implementing Wen et al.'s combined/paired estimators over psm_utils-readable outputs) and a well-maintained Percolator/mokapot successor are concrete gaps.

### Gaps
- Percolator (C++) latest release not verified (API blocked). Other DIA FDR critiques (e.g. library-size effects, MBR FDR) not researched this session.

## Protein inference & PTM localization

### Takeaway
Protein inference and PTM localization remain fragmented, largely embedded inside platforms (ProteinProphet/PTMProphet in TPP/Philosopher/FragPipe; Fido/EPIFANY in OpenMS; ptmRS in Proteome Discoverer; DIA-NN 1.9+ internal phosphosite localization). Standalone, well-benchmarked, Python-accessible localization tools are scarce; pyAscore last released Dec 2023.

### Cited Findings
- PTMProphet (TPP) uses Bayesian mixture models for site probabilities that can be combined into a global false localization rate; ptmRS is phosphoRS extended to other modifications — [PTMProphet bioRxiv](https://www.biorxiv.org/content/10.1101/679845.full.pdf)
- Conventional target-decoy often underestimates site-localization error rates (LuciPHOr2 context) — [PMC4382907](https://pmc.ncbi.nlm.nih.gov/articles/PMC4382907)
- HUPO 2024 poster (Chimerys, vendor authors) claims intensity-based localization beats PTMProphet and MaxQuant and that ptmRS did not reach 99% precision on a ground-truth phosphopeptide set — unreviewed — [HUPO 2024 poster](https://programme.conventus.de/hupo-2024/posters/ef814909-747e-41b9-a9e7-ea9ab26dfe2c)
- DIA-NN 1.9 added peptidoform scoring and phosphosite localisation; 2.0 proteoform confidence mode — [DIA-NN releases](https://github.com/vdemichev/DiaNN/releases)
- pyAscore (Python, MIT) last release 1.0.1 on 2023-12-15 — [PyPI pyAscore](https://pypi.org/pypi/pyAscore/json)

### Inferences
- A standalone, engine-agnostic localization + FLR module with Python bindings working off psm_utils/mzML would fill a visible gap.

### Gaps
- Fido, EPIFANY, Philosopher, LocalizerX status not verified in this session; no recent independent localization benchmark found (Wiese et al. referenced but not located).

## Full platforms and interop layers

### Takeaway
FragPipe (academic closed core), MaxQuant (free, closed, .NET runs on Linux), OpenMS/quantms (open, nf-core), Proteome Discoverer/PEAKS/Spectronaut (commercial), and the MannLabs Python stack (AlphaPept now stale at 0.5.3/Apr 2024, superseded by AlphaDIA/alpharaw/peptdeep; alphastats 0.7.2) are the platforms. psm_utils is the main Python PSM interop layer (reads 22 formats incl. DIA-NN parquet, Sage parquet, MaxQuant msms.txt, PD MSF), but writes only 9; there is no equivalent universal layer for quant-level outputs beyond quantms.io (stale on PyPI).

### Cited Findings
- psm_utils (Python, Apache-2.0, ~31 stars): reads 22 formats — read/write CBOR, FlashLFQ TSV, JSON, idXML, mzIdentML, Parquet, PeptideRecord, Percolator tab, TSV; read-only AlphaDIA, DIA-NN TSV/parquet, FragPipe PSM TSV, ionbot, MaxQuant msms.txt, MS Amanda, pepXML, PD MSF, Sage parquet/TSV, ProteoScape parquet, X!Tandem XML; built mainly for CompOmics tools (MS2PIP, DeepLC, MS2Rescore) — [psm_utils GitHub](https://github.com/compomics/psm_utils); v1.5.5, 2026-06-05 — [PyPI psm-utils](https://pypi.org/pypi/psm-utils/json)
- OpenMS: pyopenms 3.6.0 (2026-09-30) — [PyPI pyopenms](https://pypi.org/pypi/pyopenms/json); quantms integrates OpenMS, MSstats, pmultiqc, SDRF-driven — [quantms Nat Methods 2024](https://link.springer.com/10.1038/s41592-024-02343-1)
- quantms.io (`quantmsio`) last PyPI release 0.0.3, 2024-04-14 — [PyPI quantmsio](https://pypi.org/pypi/quantmsio/json)
- AlphaPept 0.5.3, 2024-04-19 (MIT) — [PyPI alphapept](https://pypi.org/pypi/alphapept/json); alphastats 0.7.2, 2025-11-06 — [PyPI alphastats](https://pypi.org/pypi/alphastats/json)
- pridepy (PRIDE access) 0.0.16, 2026-05-29 — [PyPI pridepy](https://pypi.org/pypi/pridepy/json)
- FragPipe 23.0 ships a Windows installer with bundled Python; Batch tab — [FragPipe releases](https://github.com/Nesvilab/FragPipe/releases)

### Inferences
- psm_utils is read-heavy and PSM-level only; no well-maintained open standard covers precursor/protein quant tables across DIA-NN/Spectronaut/AlphaDIA/FragPipe (quantms.io appears stalled on PyPI).
- Python-native platforms: MannLabs ecosystem (alpharaw → peptdeep → alphadia) is the most active; AlphaPept proper appears unmaintained.
- Main lock-in points for a new tool developer: MSFragger/DIA-NN/Spectronaut licensing; vendor SDK dependence (Thermo .NET, Bruker); Windows-centric GUIs (Proteome Discoverer, PEAKS, ProteoWizard vendor readers).

### Gaps
- Proteome Discoverer 3.x/PEAKS 12/Spectronaut 19-20 current versions and features not researched. Philosopher status unverified. Star counts and commit frequency across all GitHub repos unavailable (GitHub API blocked) — rerun with GitHub access for adoption metrics.
