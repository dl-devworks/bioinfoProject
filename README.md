# sdrf-audit

Audit [SDRF-Proteomics](https://github.com/bigbio/proteomics-sample-metadata) metadata against the data that was actually deposited.

SDRF files tell reanalysis pipelines how each raw file was acquired, labelled and searched. Most public SDRFs are now written with AI help ([bigbio/sdrf-annotated-datasets](https://github.com/bigbio/sdrf-annotated-datasets)). Existing validators check syntax and ontology terms. `sdrf-audit` checks whether each claim is *true*, comparing it with independent evidence: PRIDE project metadata and protocols, deposited file names, and raw-file headers.

**Status:** early development. The first check covers labelling design: label-free vs TMT/iTRAQ/SILAC/dimethyl, plex, and label modifications.

## Install (development)

```bash
uv venv && uv pip install -e '.[dev]'
pytest
```

## Usage

```bash
# Cache PRIDE metadata for every accession in a sdrf-annotated-datasets checkout
sdrf-audit fetch path/to/sdrf-annotated-datasets --cache cache/pride
```

## Repository layout

- `src/sdrf_audit/`: the package.
- `tests/`: unit tests.
- `reports/`: the literature review and the feasibility study behind this project.
- `research_notes/`: source notes for the literature review.
- `scripts/sdrf_audit_probe/`: the original 60-dataset feasibility probe.
