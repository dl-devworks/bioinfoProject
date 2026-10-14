# Labelling check: results on the full AI-annotated SDRF corpus

*Run 2026-10-13/14 with `sdrf-audit labels` and `sdrf-audit rawheaders` on bigbio/sdrf-annotated-datasets commit `a5c1623` (2026-10-12), PRIDE Archive v3 metadata, and raw-file headers fetched on the same days. Full outputs are in `results/labels/`.*

## Headline

**About 1 in 8 audited datasets (≈12%, about 1,370 datasets; conservative range 9.8–12.3%) is annotated as label-free even though the experiment was labelled with TMT, SILAC, iTRAQ or dimethyl.** For 905 of them, the deposited raw file's own acquisition method or sample name states the label, e.g. `TMTpro16_MS3_SPS10_90min…meth`. Most labelled experiments in the corpus are affected: only 654 SDRFs are annotated as labelled, so roughly two thirds of the labelled datasets we can detect carry a label-free annotation.

A reanalysis pipeline using these SDRFs would treat each multiplexed run as one label-free sample and would not search for the label modification. Quantification would then be meaningless for those datasets.

## Scope

| | Count |
|---|---:|
| PXD accessions in the corpus | 11,751 |
| Not in PRIDE (e.g. hosted on MassIVE or iProX) | 97 |
| PRIDE fetch errors (retryable) | 3 |
| **Accessions audited** | **11,651** |
| SDRF files audited | 12,024 |

What the SDRFs claim:

| Claimed label | SDRF files |
|---|---:|
| label-free | 11,364 |
| generic "isotope labeling" | 288 |
| TMT | 249 |
| SILAC | 80 |
| iTRAQ | 26 |
| dimethyl | 10 |
| other / unknown | 7 |

## Method

For every SDRF, the label claim (`comment[label]`) is compared with independent evidence:
- PRIDE's quantification-method field.
- PRIDE's identified PTMs, e.g. "TMT6plex-126 reporter+balance reagent acylated residue" or "Label:13C(6)15N(4)".
- Label statements in the sample- and data-processing protocols, with negations such as "without TMT" excluded.
- Deposited file names.
- The SDRF's own modification parameters.

A label-free SDRF is not flagged if a sibling SDRF of the same accession already covers the labelled part.

Confidence tiers:
- **strong:** two independent sources agree, or both protocol sections state the label.
- **probable:** one explicit protocol statement.
- **weak:** a single non-protocol hint, e.g. only PRIDE's quantification field.

## Findings

| Rule | Severity | Confidence | SDRF files |
|---|---|---|---:|
| Labelled experiment annotated as label-free | major | strong | 1,286 |
| | | probable | 134 |
| | | weak | 133 |
| Labelled SDRF lacks the label modification parameter | moderate | strong | 154 |
| Generic "isotope labeling" instead of specific channels | minor | strong | 288 |
| Isobaric SDRF with one row per file | moderate | weak | 60 |
| Claimed label contradicted by a different label | major | weak | 1 |

The strong and probable "annotated as label-free" flags cover **1,417 accessions**. By labelling chemistry:

| Chemistry | Flags |
|---|---:|
| TMT | 797 |
| SILAC | 384 |
| iTRAQ | 186 |
| dimethyl | 53 |

## Validation

**Known positives.** All 4 errors confirmed by hand in the earlier 60-dataset probe are flagged strong. The fifth, probable case (PXD015272) is flagged weak, as designed.

**Known negatives.** bigbio's 17 gold-standard datasets produce 0 flags across 19 SDRFs, including the TMT ones. Two of them, PXD026600 and PXD039859, are not in PRIDE and were skipped.

**Precision.** I read the full evidence for 30 randomly sampled strong or probable flags (seed 7, excluding probe datasets). For ambiguous cases I also checked the SDRF file list against the deposit and read the method name from the first 256 KB of a deposited `.raw` file.
- **28 of 30 are real errors.** In several, the raw file's acquisition method names the label, e.g. `TMTpro_…_MS3` (PXD079457), `TMT-90min-top20…` (PXD050432) and `TMT_3ul_NonP` (PXD035918). In one, the SDRF lists files literally named `…_TMT15plex_P1.raw` as label-free (PXD043294).
- **2 of 30 are undetermined:**
  - PXD000766: the protocol says an aliquot was iTRAQ 8-plex labelled, but the file pattern looks label-free and the raw header names no method.
  - PXD065186: the protocol states phospho dimethyl labelling, PRIDE also lists label-free quantification, and the raw header names no label.
- **Precision is 93% (28/30), with a 95% Wilson interval of 79–98%.**

### Raw-header confirmation

The first 256 KB of a deposited Thermo `.raw` file contain the acquisition method path, the original file path and the sample description. `sdrf-audit rawheaders` reads them with an HTTP range request and looks for label words: TMT, iTRAQ, SILAC, dimethyl. Operators choose these names, so a label word is evidence of labelling but its absence proves nothing.

**Calibration** on control groups the label check did not flag:

| Control group | Headers read | Header names a label |
|---|---:|---:|
| Correctly label-free datasets (random 150) | 131 | 2 (1.5%; 95% CI 0.4–5.4%) |
| Correctly labelled datasets (random 150) | 141 | 95 (67.4%; 95% CI 59–75%) |

One of the two label-free hits is a reused tune file named `…TMT_200mi.LTQTune`. The other may be a missed error.

**Flagged datasets.** Headers were readable for 1,528 of the 1,551 flagged accessions; 22 have no Thermo `.raw` file. The rate at which headers name the flagged label measures each tier's precision. True errors should name it at the labelled-control rate (67%), false alarms at the label-free-control rate (1.5%):

| Tier (before header evidence) | Headers read | Header names the label | Estimated precision | Conservative range |
|---|---:|---:|---:|---:|
| strong | 1,274 | 855 (67.1%) | **99.6%** | 85–100% |
| probable | 130 | 39 (30.0%) | 43% | 25–64% |
| weak | 122 | 24 (19.7%) | 28% | 12–46% |

The strong tier matches the hand check, which found 28 of 30 real errors. A single protocol mention (probable tier) is weaker evidence than the hand check suggested, so it should be treated as a review list rather than as confirmed errors.

**Estimated number of real errors.** Each tier's flag count times its precision gives **≈1,370 accessions (11.8% of those audited). The conservative range is about 1,145–1,430 (9.8–12.3%).** This is still a lower bound on the true rate: labelled datasets whose metadata and file names never mention the label are not detected at all.

With header evidence included, 59 flags moved up to strong and one moved down; 2 new flags come from headers alone. The current tiers are 1,341 strong, 101 probable and 109 weak.

The assumption behind this estimate is that operators of mis-annotated datasets name their methods the way operators of correctly annotated labelled datasets do. Nothing suggests otherwise, but it has not been tested independently.

## Caveats

- **Small hand-check sample.** 30 hand checks give a wide interval. The raw-header calibration is a larger, independent check, but it relies on the assumption stated above.
- **Mixed-design projects.** Some projects combine label-free and labelled experiments in one PRIDE record. The sibling-SDRF rule handles the case where the corpus splits them, but a single SDRF covering only the label-free half could still be flagged. Both undetermined cases may be of this kind.
- **Rules not yet hand-checked.** The "label modification missing" and "one row per file" rules have not been validated by hand.
- **"Confirmed" means** checked against protocols, file names and raw headers, not with the submitters.

## Reproducing

```bash
sdrf-audit fetch path/to/sdrf-annotated-datasets --cache cache/pride   # ~1.5 h, cached
sdrf-audit labels path/to/sdrf-annotated-datasets --cache cache/pride --out results/labels
sdrf-audit rawheaders path/to/sdrf-annotated-datasets --from-findings results/labels/findings.json \
    --cache cache/pride --raw-cache cache/rawheaders                     # ~1 h, 256 KB per dataset
sdrf-audit labels path/to/sdrf-annotated-datasets --cache cache/pride \
    --raw-cache cache/rawheaders --out results/labels                    # re-run with header evidence
```

`results/labels/findings.csv` lists every flag with its quoted evidence. `header_confirmed.csv` lists the 905 flags whose raw-file header names the label, which is the most actionable subset. `rawheader_calibration.json` holds the control-group headers. `audited.csv` lists every SDRF checked, and `skipped.json` lists what was skipped and why.

## Suggested next steps

1. Share these results with bigbio, for example as an issue on `sdrf-annotated-datasets` led by the header-confirmed list. It is an actionable fix list and makes the case for adding `sdrf-audit` to their CI.
2. Hand-check the "label modification missing" rule, and handle mixed-design projects explicitly.
3. Extend the header check to Bruker `.d` and SCIEX `.wiff` deposits, which this version cannot read.
