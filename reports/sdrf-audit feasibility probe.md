# sdrf-audit: background and feasibility probe

*Probe run 2026-10-13 against bigbio/sdrf-annotated-datasets commit `a5c1623` (2026-10-12) and the live PRIDE Archive v3 API. Scripts and raw output are in `scripts/sdrf_audit_probe/`.*

## Background: the problem

**What SDRF is.** SDRF-Proteomics is a tab-separated sample-and-data relationship file. Each row links one data file (and, for multiplexed runs, one label channel) to the sample it came from. It records organism, tissue, disease, instrument, label (label-free, TMT channel, SILAC heavy/light), enzyme, modifications and fractions. Reanalysis pipelines such as quantms read the SDRF to decide how to search and quantify a dataset. A wrong SDRF therefore produces a wrong reanalysis without any warning.

**Why it matters now.**
- Submitters almost never provided SDRFs: about 1.6% of PRIDE submissions in 2023 (lesSDRF paper).
- To close the gap, bigbio has annotated 11,907 accessions (27.8% of PRIDE) with help from AI agents. Every accession in that corpus is marked AI-assisted, and 3,930 come from an "unidentified agent".
- These SDRFs sync back to PRIDE and feed reanalysis efforts, so their errors spread downstream.

**What validation exists today.** The corpus has two CI gates:
1. `parse_sdrf validate-sdrf` (sdrf-pipelines) checks columns, templates and ontology terms.
2. A self-contained review gate (`.github/scripts/sdrf_review.py`) checks ragged rows, casing, collisions, missing factor values, and whether the instrument vendor matches the file extension.

Neither gate checks the SDRF against the data or the protocol text. Curators do some of that by hand. `docs/known-issues.md` lists 11 datasets found this way: fake `.raw` files, multiplexed runs annotated as label-free, and PRIDE instrument fields contradicted by the raw-file header. Each entry was found manually: reading raw headers over HTTP, comparing labels with protocols.

**The proposed solution.** `sdrf-audit` would automate and scale those manual checks. It would compare each claim in an SDRF with independent evidence (the PRIDE file list, raw/mzML headers, protocol text, deposited search results, file-name patterns). It would then produce a severity-ranked discrepancy report, using the same severity scale as `known-issues.md`, and could fill SDRF v1.1's validation-status column.

## The probe

I took a random sample of 60 of the 11,552 single-SDRF PXD accessions (seed 42). For each, I compared the SDRF with PRIDE's file list and project metadata. Where they disagreed, I read the first 256 KB of a deposited `.raw` file to get the instrument model and method names, and searched the PRIDE protocols for label terms.

## Results

### 1. Data availability: deep checks have limited reach, but cheap checks reach everything

| Deposit contains | Datasets (of 60) |
|---|---:|
| Vendor raw files | 60 (100%) |
| Raw only: no peak lists, no search results | 32 (53%) |
| Peak lists (mzML / MGF / mzXML) | 9 (15%) |
| Search results in an open, readable format (mzid, mzTab, MaxQuant txt, FragPipe, DIA-NN, pepXML) | 17 (28%) |
| Proteome Discoverer `.msf` only (proprietary) | 7 (12%) |

Checks that need identifications (modification frequencies, organism from identified proteins) can only run on about 28% of datasets. However, the **raw-header trick works on every Thermo deposit**: fetching the first 256 KB over HTTPS is enough to read the instrument model and the method name, which often names the label, e.g. "TMT".

### 2. File reconciliation: no problems found

0 of 60 SDRFs referenced a file that is missing from PRIDE. The AI agents already map files reliably, so this check is cheap but adds little.

### 3. Instrument: the SDRF was right and PRIDE was wrong

8 of 60 SDRFs disagreed with PRIDE's instrument field:
- 2 were naming differences only ("Orbitrap Elite" vs "LTQ Orbitrap Elite"; "timsTOF Pro" vs "timsTOF series").
- 1 SDRF used the generic term "mass spectrometer" where PRIDE had "timsTOF Pro". The SDRF value is vague but not wrong.
- 5 were real conflicts: PRIDE's model differed from the SDRF (for example Q Exactive vs Q Exactive Plus, HF vs HF-X, and Q Exactive Plus vs Exploris 480). **In all 5, the raw header confirmed the SDRF.**

So the AI annotators already read raw headers. Instrument checks mainly catch errors in PRIDE's own metadata, about 8% of datasets, not in the SDRFs.

### 4. Labelling design: real errors, none previously reported

| Dataset | SDRF says | Evidence | Verdict |
|---|---|---|---|
| PXD026196 | label-free, 15 rows; modifications only Carbamidomethyl and Oxidation | Protocol: "labelled using Tandem Mass Tag reagents (TMTpro)", TMTpro set as a search modification; raw header contains "TMT" | **Error**: TMTpro multiplex annotated as label-free, and the TMTpro modification is missing |
| PXD004009 | label-free, 86 rows | Protocol: "heavy" and "light" cells; file names `…DMSO_H_PK064_L…` | **Error**: SILAC annotated as label-free |
| PXD010660 | label-free, 4 rows | Protocol: Light Lys-0 / Medium Lys-4 / Heavy Lys-8, "triple SILAC" MaxQuant settings | **Error**: triple SILAC annotated as label-free |
| PXD026728 | label-free, 6 rows | Protocol: Arg0/Lys0 vs Arg10/Lys8 SILAC labelling | **Error**: SILAC annotated as label-free |
| PXD015272 | label-free, 8 rows | PRIDE quantification method: SILAC; files `C10vsC2FWD…/REV…` (a label-swap design) | **Probable error**: no protocol text to confirm |

That is 4 confirmed plus 1 probable labelling error in 60 random datasets: about 7–8%, with a rough 95% interval of 2–16% given the small sample. **None of these datasets appears in the corpus's `known-issues.md`**. These are "major" errors on bigbio's own scale: reprocessing with these SDRFs would treat several labelled samples pooled into one run as a single label-free sample.

The PRIDE quantification-method field caught all five, and each confirmed case also had supporting protocol text. A further flag (PXD048644, SDRF "isotope labeling" vs PRIDE "Label free, Dimethyl") is consistent: PRIDE lists both, so it is not an error.

## What this means for the design

1. **The useful checks are about experimental design, not deep spectra.** Label and plex versus protocol text, PRIDE's quantification field, raw method names and file-name patterns (H/L, FWD/REV, TMT channel numbers), plus whether the declared modifications fit the label (TMT/SILAC modifications present). These checks are cheap, run on raw-only deposits, and found the real errors.
2. **Two kinds of finding.** "SDRF probably wrong" and "PRIDE metadata wrong, SDRF right" are both worth reporting, to different audiences.
3. **This automates what bigbio curators already do by hand.** That favours building it as a tool their CI can call, developed together with them, not as a competing validator. They are very active (last commit the day before this probe), so it is worth contacting them first.
4. **Deep checks are an optional extra.** Modification frequencies and organism from deposited identifications would cover only about 28% of datasets.
5. **Check 1 needs text-based evidence.** Protocol text and file names call for rule-based matching first, with an optional LLM classifier later. Each flag should come with its evidence so curators can verify it quickly, as `known-issues.md` does.

## Caveats

- n = 60 is small. The error-rate interval is wide, and a 500-dataset run would tighten it.
- "Confirmed" means confirmed against the protocol and raw header, not checked by the submitters.
- The raw-header check works for Thermo `.raw` files. Bruker `.d` folders and SCIEX `.wiff` files need other methods.
- The instrument comparison used simple string normalisation. Synonym handling (e.g. the Elite naming) would need the PSI-MS ontology.

## Suggested next steps

1. Scale the labelling-design check to all 11,552 PXD SDRFs. It uses only metadata and the PRIDE API, takes roughly an hour, and gives a real error-rate estimate with candidate lists.
2. Share the five findings with bigbio (as an issue or pull request to `known-issues.md`) to test their appetite for an automated auditor.
3. Then build the MVP around the design-level checks above.
