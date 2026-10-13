# Pain points and unmet needs in bottom-up MS proteomics data analysis (2023-2026)

Method note: these notes come from web search result summaries, plus GitHub issue searches run through the GitHub API. Direct fetches of NCBI, PMC, bioRxiv and EBI full texts failed with DNS errors in this environment, so most claims rest on abstracts and search-result summaries rather than full-text reading. Statements that should be checked against the full text are flagged. Evidence strength key: **[Strong]** means a peer-reviewed or community study with data. **[Moderate]** means a preprint, a single study, or a position paper. **[Anecdotal]** means issue trackers or non-peer-reviewed web content.

## 1. Biggest computational gaps named in recent reviews, perspectives and community reports

### Takeaway
Community reports from 2023-2026 keep naming the same gaps:
- validation of DIA FDR
- standardized single-cell analysis
- FAIR metadata and interoperability, including across R and Python
- reproducible open-source software
- scalable processing as data sizes grow

I found no formal "top unmet needs" survey for proteomics software.

### Cited Findings
- **[Moderate]** The EuBIC-MS Developers Meeting 2025 (Novacella, Italy; commentary in J Proteomics vol. 331, 105708) held seven community-selected hackathons. Their topics were single-cell proteomics data analysis, FAIR metadata extraction, deep learning frameworks, R-Python interoperability and DIA validation. The commentary also stresses the need for "accurate, transparent, efficient, and reproducible data processing" as the scale and complexity of MS data grow. — [EuBIC 2025 record (unibz)](https://bia.unibz.it/esploro/outputs/journalArticle/Community-driven-advances-in-computational-mass-spectrometry/991007399553301241)
- **[Moderate]** The 2023 EuBIC-MS Developers Meeting (Ticino) centred its hackathons on "Artificial Intelligence in proteomics". — [Proceedings EuBIC-MS 2023 (TUM portal)](https://portal.fis.tum.de/en/publications/proceedings-of-the-eubic-ms-developers-meeting-2023/)
- **[Strong]** Perez-Riverol et al., "Open-Source and FAIR Research Software for Proteomics" (J Proteome Res 2025; 24(5):2222-2234), argues that the field "faces limited reproducibility due to proprietary software". It says closed-source, platform-specific tools "restrict innovation and impose hidden costs", and it addresses licensing and distribution challenges. — [PMC12053954](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12053954/); [ChemRxiv preprint](https://chemrxiv.org/engage/chemrxiv/article-details/675096d07be152b1d0f448a9); [PNNL listing](https://www.pnnl.gov/publications/open-source-and-fair-research-software-proteomics)
- **[Moderate]** The ProteoBench preprint (bioRxiv, Dec 2025) argues that "performance claims for new workflows are often incomplete and biased". It says comparisons tend to favour the tool described in the paper "because the authors have a better knowledge of their workflow", and it calls for continuous, transparent, community benchmarking. — [ProteoBench preprint](https://www.biorxiv.org/content/10.64898/2025.12.09.692895.full.pdf); [ProteoBench docs](https://proteobench.readthedocs.io/en/latest/)

### Inferences
- The topics the community chose at EuBIC 2025 (single-cell, FAIR metadata, R/Python interoperability, DIA validation) are a reasonable proxy for what method developers think is unsolved. They overlap with the domain-specific gaps below.
- "Open, cross-platform, reproducible" is now a stated community value, backed by a JPR perspective. A new tool that is closed or tied to Windows would cut against this trend.

### Gaps
- I could not retrieve a 2024-2026 Nature Methods, Nat Rev or MCP perspective that lists "grand challenges" in computational proteomics. No "Proteomics in 2025" outlook article appeared in my searches.
- I could not read the EuBIC 2025 commentary's specific hackathon outcomes because full text was not accessible.

## 2. Reproducibility and benchmarking: software variability, FDR inflation, lack of standard benchmarks

### Takeaway
This is the best-evidenced pain point. A 2024-2025 entrapment study found that **no DIA search tool consistently controls FDR**, and single-cell data was the worst case. Tool-to-tool variability is large and depends heavily on workflow choices. Community infrastructure is emerging (ProteoBench, FDRBench) but is young.

### Cited Findings
- **[Strong]** Wen et al., "Assessment of false discovery rate control in tandem mass spectrometry analysis using entrapment" (bioRxiv June 2024; published 2025, PMC12240826; Noble lab and collaborators). Findings:
  - No DIA search tool consistently controls FDR, and performance is particularly poor on single-cell datasets.
  - The tools evaluated were DIA-NN, Spectronaut and EncyclopeDIA.
  - The paper finds that of three common ways to validate FDR control with entrapment, one is invalid, one gives only a lower bound, and one is valid but under-powered. It proposes a more powerful estimator.

  The search summary did not confirm the journal; it may be Nature Methods, so verify before citing. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.06.01.596967.full.pdf); [PMC12240826](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12240826/); [PMC11185562 (preprint)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11185562/)
- **[Moderate]** FDRBench, a tool from the same group, builds entrapment databases and estimates the false discovery proportion. ProteoBench now has a "DIA Ion Entrapment – Astral" module that uses FDRBench, which turns the critique into a standing benchmark. — [FDRBench GitHub mirror](https://github.com/standardgalactic/FDRBench); [ProteoBench entrapment module](https://proteobench.readthedocs.io/en/latest/available-modules/active-modules/13-entrapment-ion-dia-astral/)
- **[Moderate]** ProteoBench modules cover:
  - label-free DDA and DIA quantification
  - DDA identification
  - de novo identification
  - single-cell proteomics
  - DIA entrapment FDR

  Several modules are active and others are "in development"/"proposed". The project says explicitly that it does not try to name a single best workflow. — [ProteoBench docs](https://proteobench.readthedocs.io/en/latest/); [About](https://proteobench.readthedocs.io/en/latest/general-information/0-about/)
- **[Strong, background]** Fröhlich et al. (Nat Commun 2022) combined spectral libraries, DIA software, sparsity reduction, normalization and statistical tests into **1,428 distinct workflows** for differential-abundance detection on a clinical FFPE benchmark with spiked-in E. coli. The best choices included gas-phase-fractionated libraries and permutation-based tests. The scale shows how far results can swing with workflow choices. — [PMC9098472](https://pmc.ncbi.nlm.nih.gov/articles/PMC9098472); [DOAJ record](https://doaj.org/article/17f2eb2214c94026859e0c88b1eb7fa8)
- **[Strong, background]** Navarro et al. (2016, LFQbench multicenter study) found that after optimization, OpenSWATH, SWATH 2.0, Skyline, Spectronaut and DIA-Umpire gave convergent results. Convergence depended on expert optimization. — [PubMed 27701404](https://pubmed.ncbi.nlm.nih.gov/27701404/)
- **[Strong]** The HUPO Human Glycoproteomics Initiative distributed the same LC-MS data to 22 institutions. The reported glycopeptides "differed and included misassigned results" (date unconfirmed, possibly pre-2024). — [PMC11291120](https://pmc.ncbi.nlm.nih.gov/articles/PMC11291120)

### Inferences
- An independent, tool-agnostic FDR validation layer would address a well-documented, high-severity problem that is not yet productized for end users. The current options are research code (FDRBench) and a benchmark site (ProteoBench). The gap is a user-facing QC report that answers "is my FDR trustworthy?", with entrapment, decoy diagnostics and cross-tool agreement.
- Benchmarking infrastructure exists but has few modules for PTMs, immunopeptidomics, TMT and large cohorts. Contributing modules is a lower-risk niche than building a new search engine.

### Gaps
- I found no 2024-2026 multi-lab study that quantifies inter-software variability for DIA beyond the entrapment work. A summary of ProteoBench submission statistics was not retrievable.
- I could not confirm how vendors or tool authors responded to the entrapment results, for example whether later DIA-NN releases changed FDR estimation.

## 3. Interoperability: output conversion, SDRF metadata adoption, reanalysis of public data

### Takeaway
Raw data deposition is routine, but sample and design metadata is still sparse. SDRF adoption is described as low, and reanalysis projects name file conversion, missing metadata and workflow restarts as their main bottlenecks. Moving tool outputs into downstream statistics is a recurring support issue.

### Cited Findings
- **[Moderate]** A position paper, "Unlocking the Next Decade of Proteomics with Standardized, Structured Metadata" (PMC12887984, c. 2025-2026), makes these points:
  - Metadata provision "remains limited, especially at the level of the biological samples and experimental design", which hampers large-scale reuse.
  - SDRF-Proteomics tools exist, but adoption is low. Causes include weak incentives and journals and repositories struggling to enforce it.
  - It assigns roles to funders, HUPO-PSI, ProteomeXchange repositories, vendors, software developers and journals.

  Exact adoption percentages were not retrieved. — [PMC12887984](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12887984/)
- **[Moderate]** A Swedish NAISS project (Edfors) reanalysing public DIA data for the Human Protein Atlas names **file conversion, metadata gaps and workflow restarts** as the major bottlenecks. Its planned remedy is SDRF curation for every dataset. — [NAISS project 7699](https://nim.nsc.liu.se/projects/7699)
- **[Moderate]** An ELIXIR implementation study aims "to assess the possibilities for performing more automated re-analyses using the metadata SDRF-encoded annotations of public datasets". — [ELIXIR](https://elixir-europe.org/about-us/commissioned-services/increasing-value-proteomics-datasets)
- **[Moderate]** A HUPO 2024 poster reports that SDRF-Proteomics is incomplete for metaproteomics. The Metaproteomics Initiative proposed pilot SDRF-Metaproteomics standards. — [HUPO 2024 poster](https://programme.conventus.de/hupo-2024/posters/cf648eb3-67be-48b7-9108-701f92509d9f)
- **[Strong]** quantms (Dai et al., Nat Methods 2024; 21:1603-1607) reanalysed 83 ProteomeXchange datasets: about 29,000 raw files from about 13,100 human samples, giving 16,599 proteins and 1.03 million unique peptides. Its rationale is that very large datasets strain workstations and that standard file formats help reproducibility. — [PMC11399091](https://pmc.ncbi.nlm.nih.gov/articles/PMC11399091)
- **[Anecdotal]** In the DIA-NN GitHub tracker, the most-discussed downstream-statistics issue is #1088, "error in DIANNtoMSstatsFormat 'column(s) not found: [FragmentQuantCorrected]'" (2024, 21 comments). Its root cause is output-format drift between DIA-NN versions breaking MSstats converters. Related threads cover:
  - DIA-NN with MSstats (#277, #596)
  - normalisation in downstream analysis (#1929, 2026)
  - requests for MaxQuant-like msms.txt output (#968)

  — [DiaNN #1088](https://github.com/vdemichev/DiaNN/issues/1088); [#1929](https://github.com/vdemichev/DiaNN/issues/1929); [#596](https://github.com/vdemichev/DiaNN/issues/596); [#968](https://github.com/vdemichev/DiaNN/issues/968)
- **[Moderate]** Interoperability between R and Python was a 2025 EuBIC hackathon topic. — [EuBIC 2025](https://bia.unibz.it/esploro/outputs/journalArticle/Community-driven-advances-in-computational-mass-spectrometry/991007399553301241)

### Inferences
- Two needs here are concrete and buildable by one developer. One is a robust, versioned output-normalization layer that turns DIA-NN, Spectronaut, FragPipe and MaxQuant outputs into a common long-format table plus SDRF and feeds MSstats, limma or Python tools. The other is SDRF authoring or auto-extraction, for example from manuscripts or raw-file headers. Both need maintenance against upstream format changes, which is the pain point itself.
- Partial solutions exist: quantms (SDRF-driven reanalysis), MSstats converters, and the SDRF-Proteomics tooling. Their remaining weaknesses are brittleness and low uptake, not absence.

### Gaps
- I found no quantitative figure (for example, the share of PRIDE datasets with SDRF) that I could verify.
- I did not check psm_utils, mzTab-M or mzTab 2.0 adoption issues directly.

## 4. Domains with weak tooling

### Takeaway
Weak tooling is best documented for single-cell proteomics, glycoproteomics, immunopeptidomics and metaproteomics. Each has a strong FDR or search-space component. Site-level PTM reporting and large-cohort batch correction have partial tools but no consensus.

### Cited Findings

**Single-cell proteomics (SCP)**
- **[Strong]** The community guidelines (Gatto, Slavov et al., Nat Methods, March 2023) give "initial recommendations" on design, data evaluation and reporting. They call for shared standards and metrics for cross-lab comparability. — [Springer ABC commentary](https://link.springer.com/article/10.1007/s00216-023-04759-8); [arXiv 2207.10815](https://arxiv.org/abs/2207.10815v1)
- **[Strong]** Vanderaa & Gatto review that SCP computational workflows "lack standardization". Their recommendations are careful tool choice, standardized data formats with rich annotation, and batch correction. — [arXiv 2210.01020](https://arxiv.org/pdf/2210.01020)
- **[Moderate]** Vanderaa & Gatto, "Revisiting the thorny issue of missing values in SCP" (2023), identify 5 main challenges around missing values and note that imputation is still widely used despite its drawbacks. — [arXiv 2304.06654](https://arxiv.org/abs/2304.06654v1)
- **[Strong]** scplainer (Genome Biology 2025, in Bioconductor `scp`) uses linear models with minimal preprocessing for variance analysis, differential abundance, component analysis and batch removal. It argues that imputation "introduces bias, ignores uncertainty… and masks inestimable contrast". — [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.12.14.571792.full.pdf); [PMC12330071](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12330071/); [scp vignette](https://bioc-release.r-universe.dev/scp/doc/scp_data_modelling.Rmd)
- **[Strong]** DIA FDR control is "particularly poor" on single-cell data. — [Entrapment paper](https://www.biorxiv.org/content/10.1101/2024.06.01.596967.full.pdf)
- **[Moderate]** A 2026 CSIAM review highlights high missingness, batch effects and low-input noise in SCP. It points to deep learning, foundation models and multimodal integration as future directions. — [CSIAM-LS review](https://www.global-sci.com/csiam-ls/article/view/24004)
- **[Anecdotal/press]** GenomeWeb reports that batch effects and missing values become more severe at the scale of thousands of cells. — [GenomeWeb](https://www.genomeweb.com/node/584976)

**Immunopeptidomics**
- **[Strong]** Non-tryptic search inflates the search space, and adding mutations, ORFs and PTMs inflates it further. The result is more random high-scoring matches and fewer identifications at a fixed FDR. A smaller share of spectra is confidently assigned than in tryptic data. ML rescoring is the main remedy: a 2024 Proteomics review, DOI 10.1002/pmic.202300336. — [ChemRxiv/Proteomics review](https://chemrxiv.org/engage/chemrxiv/article-details/64f75229dd1a73847f3f28b6)
- **[Strong, background]** MS2Rescore with immunopeptide-retrained MS2PIP, DeepLC and Percolator gave 46% more PSMs and 36% more unique peptides at 1% FDR (MCP 2022). — [ChemRxiv/Proteomics review](https://chemrxiv.org/engage/chemrxiv/article-details/64f75229dd1a73847f3f28b6)
- **[Anecdotal]** FragPipe issue #2492 (2025), "non-specific peptidome crash due to memory issue", shows that non-specific searches strain resources. — [FragPipe #2492](https://github.com/Nesvilab/FragPipe/issues/2492)

**PTMs, phosphoproteomics**
- **[Moderate]** The authors of msproteomics `sitereport` (2024) say that "Spectronaut and DIA-NN do not offer a common reporting scheme for phosphosites and phosphopeptides". They built a site-level reporter that uses MaxLFQ. — [PMC11239223](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11239223/)
- **[Moderate]** A 2023 Proteomics review lists open issues in localization: neutral losses, gas-phase rearrangement and estimation of the false localization rate (FLR). — [search-surfaced record](https://nufind.nu.edu.sa/EdsRecord/cmedm,37897210) (record only; title not verified)
- **[Moderate]** pyLucXor (2026 conference paper) adds alanine-decoy site-level FLR estimation, which suggests site-level FLR is still an active gap. — [BIO Web Conf 2026](https://www.bio-conferences.org/articles/bioconf/abs/2026/30/bioconf_icbb2026_01032/bioconf_icbb2026_01032.html)

**Glycoproteomics**
- **[Strong]** Different glycoproteomics tools use different target-decoy approaches, so "the meaning of FDR depends on the assumptions behind each algorithm". Tools are not directly comparable, and the authors call for community standards. — [PMC8398183](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8398183/)
- **[Moderate]** Hogan, Pepi, Riley & Chalkley (bioRxiv 2024) compared Byonic, Protein Prospector, MSFragger-Glyco, pGlyco3 and GlycoDecipher. A 2025 preprint on sialylated glycopeptides found that about half of the identified glycopeptides were unique to individual tools. — [bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.07.10.664079.full.pdf); [PMC11291120](https://pmc.ncbi.nlm.nih.gov/articles/PMC11291120)

**Proteogenomics and variant peptides**
- **[Moderate, 2022 background]** A Briefings in Bioinformatics review covers the trade-off between a compact database and an all-variant database. It recommends two-pass search or class-specific FDR. Variants other than single amino acid changes (indels, fusions, Ig genes) are poorly captured. — [Brief Bioinform 2022](https://academic.oup.com/bib/article/23/5/bbac163/6582880); [PMC4868822](https://pmc.ncbi.nlm.nih.gov/articles/PMC4868822)

**Metaproteomics**
- **[Moderate, 2023]** Miura & Okuda (CSBJ 2023) say metaproteomics still relies on extended standard-proteomics methods. Huge databases create problems, and the field needs a standard FDR method to replace plain target-decoy. — [PMC9925844](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9925844/)
- **[Anecdotal]** FragPipe issues show memory failures with large metaproteomics databases. Examples: #257, a 170M-sequence/136 GB database; #2843 (2026), a 6.4 GB FASTA that fails despite an 800 GB Java heap. — [FragPipe #257](https://github.com/Nesvilab/FragPipe/issues/257); [FragPipe #2843](https://github.com/Nesvilab/FragPipe/issues/2843)
- **[Moderate]** SDRF does not cover metaproteomics metadata (HUPO 2024 poster). — [HUPO 2024](https://programme.conventus.de/hupo-2024/posters/cf648eb3-67be-48b7-9108-701f92509d9f)

**Large-cohort, clinical and plasma proteomics: QC and batch correction**
- **[Strong, 2021 background]** Čuklina et al. (Mol Syst Biol 2021, proBatch) give a batch-effect tutorial. It covers intensity drift, missing values tied to technical factors, and checks on correction quality. — [PMC8447595](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8447595/)
- **[Moderate]** Batch effects in targeted clinical validation receive less attention than in discovery. Plate edge effects from temperature gradients are one example. — [PMC10251511](https://pmc.ncbi.nlm.nih.gov/articles/PMC10251511)
- **[Anecdotal]** Oliver et al. (ACS Meas Sci Au 2024) proposed QC sample categories for large-scale plasma sample prep. I saw this only through a vendor blog, so it is unverified. — [Metware blog](https://metwarebio.com/proteomics-quality-control-reproducible-data/)

### Inferences
- **Highest-signal niches for one developer:**
  1. Site-level PTM reporting and statistics that work across DIA-NN, Spectronaut and FragPipe outputs. The gap is explicit and the scope is tractable.
  2. Tool-agnostic FDR and FLR validation, for entrapment and for class-specific FDR in proteogenomics and immunopeptidomics.
  3. Batch and QC diagnostics for large cohorts that model missingness and batch jointly. This links to scplainer/proBatch ideas but would sit in the Python ecosystem.
- **Lower-feasibility niches:** new glycoproteomics or metaproteomics search engines. These need deep domain expertise and large compute.

### Gaps
- I did not find a 2024-2026 review dedicated to proteogenomics or glycoproteomics software gaps. The evidence is older or comes from preprints.
- I found no dedicated 2024-2026 review of batch correction in plasma proteomics.

## 5. Usability: wet-lab barriers, GUI vs CLI, Windows dependency, licensing

### Takeaway
Licensing restrictions are well documented: MSFragger and FragPipe components are academic-only, and Spectronaut and Proteome Discoverer are commercial. A peer-reviewed perspective frames proprietary and platform-specific tools as a reproducibility cost. Recurring resource and memory failures dominate FragPipe's tracker. I found no systematic user survey on usability.

### Cited Findings
- **[Strong]** Proprietary and closed tools limit reproducibility and impose hidden costs. — [Perez-Riverol et al. JPR 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12053954/)
- **[Strong, primary license docs]** MSFragger is free "for academic research, non-commercial or educational purposes" only. Commercial use needs a license, handled by Fragmatics LLC from 1 May 2025 (University of Michigan notice). The academic agreement restricts use to the licensee's department, and some copies "strictly prohibit" commercial use. — [MSFragger site](https://msfragger.nesvilab.org/); [UMich licensing page](https://available-inventions.umich.edu/product/msfragger-ultrafast-and-comprehensive-identification-of-peptides-from-tandem-mass-spectra); [IonQuant academic license](https://msfragger-upgrader.nesvilab.org/ionquant/LICENSE-ACADEMIC.pdf); [GitHub](https://github.com/Nesvilab/MSFragger)
- **[Anecdotal]** A vendor guide notes that commercial tools such as Proteome Discoverer and Spectronaut require paid licenses but come with support. It also says GUIs suit beginners while CLIs suit pipelines. Its claim that MaxQuant is "open-source" is inaccurate, since MaxQuant is free but closed source; treat this source with caution. — [Metware comparison](https://metwarebio.com/proteomics-software-comparison-lc-msms-lfq-tmt-silac-dia/)
- **[Anecdotal, community signal]** A FragPipe GitHub search for out-of-memory problems returns **41 issues**. Examples run from 2020 to 2026: #569 (38 comments), #2701 (2026), #2339 (2025) and #1859 (2024). — [FragPipe #569](https://github.com/Nesvilab/FragPipe/issues/569); [#2701](https://github.com/Nesvilab/FragPipe/issues/2701); [#2339](https://github.com/Nesvilab/FragPipe/issues/2339); [#1859](https://github.com/Nesvilab/FragPipe/issues/1859)
- **[Anecdotal]** DIA-NN users ask how to interpret output columns, for example Total.Quantity vs MS1 signal in stats.tsv (#1772), and about stats reports missing in 1.9.1 (#1192). This points to documentation gaps. — [DiaNN #1772](https://github.com/vdemichev/DiaNN/issues/1772); [#1192](https://github.com/vdemichev/DiaNN/issues/1192)

### Inferences
- A permissively licensed (MIT or Apache) tool that runs cross-platform would stand apart from academic-only alternatives, especially for industry or core-facility users. This is an inference; no survey quantifies the demand.
- Memory and scaling failures in mainstream Java pipelines on large FASTA and non-specific searches are a persistent, real-world pain point.

### Gaps
- I could not verify DIA-NN 2.x license terms (academic vs commercial) or MaxQuant's current license wording. No source was retrieved.
- I found no 2023-2026 survey that quantifies Windows dependency, GUI preference or learning-curve barriers among wet-lab users.

## 6. Community signals: GitHub, Reddit, Bioconductor, social media, core-facility surveys

### Takeaway
GitHub trackers show three recurring themes:
1. Memory and scaling failures (FragPipe).
2. Output-format drift breaking downstream converters (DIA-NN to MSstats).
3. Confusion over normalization, downstream statistics and column meanings.

I found no ABRF proteomics-specific survey on data-analysis bottlenecks for 2023-2026. I did not collect Reddit or Bluesky signals.

### Cited Findings
- **[Anecdotal]** FragPipe: 41 issues matched an out-of-memory search, including recent ones from 2025-2026. — [FragPipe #2843](https://github.com/Nesvilab/FragPipe/issues/2843); [#2701](https://github.com/Nesvilab/FragPipe/issues/2701)
- **[Anecdotal]** DIA-NN: converter breakage (#1088, 21 comments), normalization questions in downstream analysis (#1929, 2026), and requests for compatibility with MaxQuant formats (#968). — [DiaNN #1088](https://github.com/vdemichev/DiaNN/issues/1088); [#1929](https://github.com/vdemichev/DiaNN/issues/1929); [#968](https://github.com/vdemichev/DiaNN/issues/968)
- **[Moderate, background]** The ABRF bioinformatics core survey (2019; Dragon et al., J Biomol Tech 2020) found that the cost of -omics data generation fell about 10-fold while demand for analysis support grew "exponentially". Bioinformatics cores rely on cost recovery. The survey covers genomics, not proteomics specifically. — [PMC7192196](https://pmc.ncbi.nlm.nih.gov/articles/PMC7192196)

### Inferences
- Issue-tracker themes match the literature on interoperability and scaling. This convergence makes "glue and QC" tooling a credible target.

### Gaps
- I collected no evidence from Reddit r/proteomics, the MaxQuant Google group, the Bioconductor support site or Bluesky. These sources were not searched within the tool budget, so any claims about them would be unsupported.
- I found no 2023-2026 ABRF or proteomics core-facility survey on software needs.
- Issue counts are search-hit counts, not normalized rates, so they show recurrence, not prevalence.
