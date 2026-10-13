# Labelling check: results on the full AI-annotated SDRF corpus

*Run 2026-10-13 with `sdrf-audit labels` on bigbio/sdrf-annotated-datasets commit `a5c1623` (2026-10-12) and PRIDE Archive v3 metadata fetched the same day. Full outputs are in `results/labels/`.*

## Headline

**About 1 in 9 audited datasets (≈11%) is annotated as label-free even though the experiment was labelled (TMT, SILAC, iTRAQ or dimethyl).** That is roughly 1,320 datasets. Most labelled experiments in the corpus are affected: the corpus annotates only 654 SDRFs as labelled, so about two thirds of the labelled datasets we can detect carry a label-free annotation.

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

**Estimated number of real errors.** 1,417 × 0.93 ≈ **1,320 accessions, with a range of about 1,115–1,390. That is 9.6–11.9% of audited accessions.** This is a lower bound on the true rate: it excludes the 133 weak flags, and labelled datasets whose metadata never mentions the label are not detected at all.

## Caveats

- **Small precision sample.** 30 hand checks give a wide interval. A larger review, ideally by bigbio curators, would tighten it.
- **Mixed-design projects.** Some projects combine label-free and labelled experiments in one PRIDE record. The sibling-SDRF rule handles the case where the corpus splits them, but a single SDRF covering only the label-free half could still be flagged. Both undetermined cases may be of this kind.
- **Rules not yet hand-checked.** The "label modification missing" and "one row per file" rules have not been validated by hand.
- **"Confirmed" means** checked against protocols, file names and raw headers, not with the submitters.

## Reproducing

```bash
sdrf-audit fetch path/to/sdrf-annotated-datasets --cache cache/pride   # ~1.5 h, cached
sdrf-audit labels path/to/sdrf-annotated-datasets --cache cache/pride --out results/labels
```

`results/labels/findings.csv` lists every flag with its quoted evidence. `audited.csv` lists every SDRF checked, and `skipped.json` lists what was skipped and why.

## Suggested next steps

1. Share these results with bigbio, for example as an issue on `sdrf-annotated-datasets` with the strong-tier list. It is an actionable fix list and makes the case for adding `sdrf-audit` to their CI.
2. Add a raw-header check as an automatic second opinion for flagged Thermo datasets. It resolved most ambiguous cases in the hand check.
3. Hand-check the "label modification missing" rule, and handle mixed-design projects explicitly.
