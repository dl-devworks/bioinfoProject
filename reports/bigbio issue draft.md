<!--
DRAFT for review. Not posted.
Target: https://github.com/bigbio/sdrf-annotated-datasets/issues/new
Before posting: make the bioinfoProject repository public (or move sdrf-audit to a public repo) so
the links below work, and replace <REPO_URL>. Attaching header_confirmed.csv to the issue also works.
-->

# ~1,370 labelled datasets (≈12%) are annotated as label-free

Hi bigbio team, and thank you for this resource. I have been building **sdrf-audit**, a tool that checks SDRF claims against independent evidence from the deposit. I ran its first check, labelling design, over the whole corpus (commit `a5c1623`, 12 Oct 2026), and I think the results are worth a look.

## Summary

- 12,024 SDRFs in 11,651 PXD accessions were checked against PRIDE metadata. 97 PXDs not in PRIDE were skipped.
- **An estimated ~1,370 accessions (≈12%; conservative range 9.8–12.3%) are annotated `label free sample` but are TMT, SILAC, iTRAQ or dimethyl experiments.** By chemistry, the strong and probable flags are 797 TMT, 384 SILAC, 186 iTRAQ and 53 dimethyl.
- **For 905 of them, the deposited `.raw` file's own header names the label**, in the instrument-method path or the sample name. These are the most clear-cut and are listed in `header_confirmed.csv`.
- Reprocessing these with quantms would treat each multiplexed run as one label-free sample, without the label modification.

## Examples

| Accession | SDRF says | Raw-file header | Other evidence |
|---|---|---|---|
| PXD014967 | label free sample | sample name `… TMT6PLEX IEF 1` | PRIDE quantification: TMT; identified PTM: TMT6plex; protocol: "TMTsixplex reagents were used…" |
| PXD006894 | label free sample | method `…\iTRAQ_fast_20140630_Top15…` | PRIDE quantification: iTRAQ; identified PTM: iTRAQ8plex; protocol: "isobaric-tag based quantification using the iTRAQ approach" |
| PXD002384 | label free sample | file `…_internalisation_sorted_SILAC` | protocol: "SILAC labeling of Arg and Lys … were variable modifications" |
| PXD069116 | label free sample | file `…_DNA_PD_dimethyl_MHQ_7.raw` | PRIDE quantification: Dimethyl Labeling; protocol: "Dimethyl labeling on StageTips…" |
| PXD026196 | label free sample, Carbamidomethyl + Oxidation only | (checked by hand) | protocol: TMTpro labelling, with TMTpro set as a fixed modification |

## How it was checked

Each SDRF's `comment[label]` is compared with:
- PRIDE's quantification-method field and identified PTMs.
- Label statements in the sample and data-processing protocols, with negations excluded.
- Deposited file names.
- The SDRF's own modification parameters.
- For flagged datasets, the first 256 KB of one deposited Thermo `.raw` file, read over HTTPS. This is the same approach as your `known-issues.md`.

A label-free SDRF is not flagged when a sibling SDRF of the same accession covers the labelled part.

## Validation

- **Gold standard:** 0 flags across the 19 gold-standard SDRFs.
- **Hand check:** 28 of 30 random strong or probable flags are real errors; 2 are undetermined, possibly mixed-design projects.
- **Header calibration:**
  - Label words appear in 1.5% of headers from correctly label-free datasets and 67% from correctly labelled ones.
  - Strong-tier flags hit 67.1%, implying about 99.6% precision (conservative range 85–100%).
  - Single-source flags are much less reliable, roughly 30–45% precision, so they belong on a review list only.

## Not claimed

- No contact with submitters.
- Some projects mix label-free and labelled experiments in one PRIDE record; a few flags may be the label-free half.
- Bruker and SCIEX deposits get no header check.
- Two smaller rules have not been hand-validated yet: labelled SDRFs without the label modification (154), and 288 SDRFs using the generic `isotope labeling` term instead of channels.

## Offer

- Full results, code and method: `<REPO_URL>` (`reports/Labelling check results.md`, `results/labels/`).
- I'd be glad to:
  - share the full list in whatever form helps your curation workflow;
  - contribute fixes for the header-confirmed cases;
  - help wire a check like this into your CI, e.g. reading `known-issues.md`-style categories.

Does this look useful, and what would be the most convenient way to proceed?
