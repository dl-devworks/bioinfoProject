from pathlib import Path

import pytest

from sdrf_audit.labels import (
    LABEL_FREE, SILAC, TMT, check_labels, classify_label_value, collect_evidence, read_sdrf,
)

HEADER = ["source name", "comment[data file]", "comment[label]",
          "comment[modification parameters]", "comment[modification parameters]"]


def write_sdrf(tmp_path: Path, rows: list[list[str]], header=HEADER) -> Path:
    p = tmp_path / "PXD000001.sdrf.tsv"
    p.write_text("\n".join("\t".join(r) for r in [header, *rows]) + "\n")
    return p


LF = "AC=MS:1002038;NT=label free sample"
CAM = "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed"
OX = "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable"
TMT6 = "NT=TMT6plex;AC=UNIMOD:737;TA=K;MT=Fixed"


def lf_sdrf(tmp_path, n=3):
    return read_sdrf(write_sdrf(tmp_path, [[f"s{i}", f"run{i}.raw", LF, CAM, OX] for i in range(n)]))


@pytest.mark.parametrize("value,kind", [
    (LF, LABEL_FREE),
    ("NT=label free sample;AC=MS:1002038", LABEL_FREE),
    ("AC=MS:1002616;NT=TMT126", TMT),
    ("TMT 10-plexCN=130N", TMT),
    ("NT=SILAC heavy;AC=MS:1002039", SILAC),
    ("SILAC light R:12C(6)14N(4)", SILAC),
])
def test_classify_label_value(value, kind):
    assert classify_label_value(value) == kind


def test_label_free_with_tmtpro_protocol_is_flagged(tmp_path):
    # Mirrors PXD026196: TMTpro in protocols, annotated label-free.
    project = {
        "sampleProcessingProtocol": "Digested peptides were labelled using Tandem Mass Tag reagents (TMTpro).",
        "dataProcessingProtocol": "TMTpro-label modifications of N-terminal and lysine were selected.",
    }
    findings = check_labels("PXD026196", lf_sdrf(tmp_path), project, ["Lumos_200323_100.raw"])
    assert [f.rule for f in findings] == ["labelled-annotated-as-label-free"]
    assert findings[0].evidenced == TMT
    # The protocol states it in both protocol fields.
    assert findings[0].confidence == "strong"


def test_single_protocol_statement_is_probable(tmp_path):
    project = {"dataProcessingProtocol": "Protein extraction, iTRAQ labeling and mass spectrometry were done."}
    (f,) = check_labels("PXD010751", lf_sdrf(tmp_path), project, [])
    assert f.confidence == "probable"


def test_quant_field_alone_is_weak(tmp_path):
    (f,) = check_labels("PXD015272", lf_sdrf(tmp_path), {"quantificationMethods": [{"name": "SILAC"}]}, [])
    assert f.confidence == "weak"


def test_bare_dimethyl_modification_is_not_a_label(tmp_path):
    rows = [["s1", "a.raw", LF, CAM, "NT=Dimethyl;AC=UNIMOD:36;TA=K,R;MT=Variable"]]
    claim = read_sdrf(write_sdrf(tmp_path, rows))
    assert claim.mod_kinds == set()


def test_two_independent_sources_make_it_strong(tmp_path):
    project = {
        "quantificationMethods": [{"name": "SILAC"}],
        "sampleProcessingProtocol": "Cells were grown in Arg10/Lys8 heavy medium for SILAC labeling.",
    }
    (f,) = check_labels("PXD026728", lf_sdrf(tmp_path), project, [])
    assert (f.evidenced, f.confidence) == (SILAC, "strong")


def test_consistent_label_free_is_clean(tmp_path):
    project = {"quantificationMethods": [{"name": "Label free"}],
               "sampleProcessingProtocol": "Proteins were digested with trypsin."}
    assert check_labels("PXD1", lf_sdrf(tmp_path), project, ["a.raw"]) == []


def test_negated_label_mention_is_ignored(tmp_path):
    project = {"sampleProcessingProtocol": "Samples were analysed label-free, without TMT labelling."}
    assert check_labels("PXD1", lf_sdrf(tmp_path), project, []) == []


def test_biological_dimethylation_is_not_a_label():
    ev = collect_evidence({"identifiedPTMStrings": [{"name": "dimethylated residue"}]}, [])
    assert ev == []


def test_sibling_sdrf_covering_label_suppresses_flag(tmp_path):
    project = {"quantificationMethods": [{"name": "TMT"}], "sampleProcessingProtocol": "TMT10plex labelling."}
    assert check_labels("PXD1", lf_sdrf(tmp_path), project, [], sibling_kinds={TMT}) == []


def test_tmt_without_tmt_modification(tmp_path):
    rows = [["s1", "f1.raw", "TMT126", CAM, OX], ["s2", "f1.raw", "TMT127", CAM, OX]]
    claim = read_sdrf(write_sdrf(tmp_path, rows))
    project = {"sampleProcessingProtocol": "TMT6plex labelling"}
    rules = [f.rule for f in check_labels("PXD1", claim, project, [])]
    assert rules == ["label-modification-missing"]


def test_correct_tmt_sdrf_is_clean(tmp_path):
    rows = [["s1", "f1.raw", "TMT126", CAM, TMT6], ["s2", "f1.raw", "TMT127", CAM, TMT6]]
    claim = read_sdrf(write_sdrf(tmp_path, rows))
    project = {"quantificationMethods": [{"name": "TMT"}]}
    assert check_labels("PXD1", claim, project, []) == []
