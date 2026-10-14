"""Labelling-design check: does an SDRF's label annotation match the deposit?

An SDRF states a label per row (``comment[label]``): label-free, a TMT/iTRAQ channel, a
SILAC or dimethyl state. This module classifies that claim and compares it with
independent evidence from PRIDE (quantification methods, identified PTMs, protocol text),
the deposited file names, and the SDRF's own modification parameters.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

LABEL_FREE = "label-free"
TMT = "TMT"
ITRAQ = "iTRAQ"
SILAC = "SILAC"
DIMETHYL = "dimethyl"
ISOTOPE = "isotope (unspecified)"
UNKNOWN = "unknown"

LABELLED = (TMT, ITRAQ, SILAC, DIMETHYL)

# --- SDRF side -------------------------------------------------------------------------

_LABEL_VALUE_PATTERNS = [
    (TMT, re.compile(r"\btmt|tandem mass tag", re.I)),
    (ITRAQ, re.compile(r"itraq", re.I)),
    (SILAC, re.compile(r"silac|\b(heavy|medium|light)\b|lys\s*[-:]?\s*[48]\b|arg\s*[-:]?\s*(6|10)\b", re.I)),
    (DIMETHYL, re.compile(r"dimethyl", re.I)),
    (ISOTOPE, re.compile(r"isotope label", re.I)),
    (LABEL_FREE, re.compile(r"label[\s-]*free", re.I)),
]

# Modification parameter names (NT=...) that imply a labelling chemistry.
_MOD_PATTERNS = [
    (TMT, re.compile(r"^tmt", re.I)),
    (ITRAQ, re.compile(r"^itraq", re.I)),
    (SILAC, re.compile(r"^label:(13c|15n|2h)|^(arg|lys)\d+$|silac", re.I)),
    # Bare "Dimethyl" is also used for biological K/R methylation; only isotope forms imply a label.
    (DIMETHYL, re.compile(r"^dimethyl:", re.I)),
]


def _strip_cv(value: str) -> str:
    """'AC=MS:1002038;NT=label free sample' -> 'label free sample'."""
    nt = re.search(r"NT=([^;]*)", value)
    return (nt.group(1) if nt else value).strip()


def classify_label_value(value: str) -> str:
    text = _strip_cv(value)
    for kind, pat in _LABEL_VALUE_PATTERNS:
        if pat.search(text):
            return kind
    return UNKNOWN


@dataclass
class SdrfClaim:
    path: str
    n_rows: int
    label_values: list[str]
    label_kinds: set[str]
    mod_names: list[str]
    mod_kinds: set[str]
    data_files: list[str]
    max_rows_per_file: int

    @property
    def kind(self) -> str:
        """Overall label claim of the file."""
        labelled = self.label_kinds & set(LABELLED)
        if labelled:
            return "+".join(sorted(labelled))
        if ISOTOPE in self.label_kinds:
            return ISOTOPE
        if self.label_kinds == {LABEL_FREE}:
            return LABEL_FREE
        return UNKNOWN


def read_sdrf(path: str | Path) -> SdrfClaim:
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        rows = [r for r in csv.reader(f, delimiter="\t")]
    header = [h.strip().lower() for h in rows[0]]
    body = [r for r in rows[1:] if any(c.strip() for c in r)]

    def cells(pred) -> list[str]:
        idx = [i for i, h in enumerate(header) if pred(h)]
        return [r[i].strip() for r in body for i in idx if i < len(r) and r[i].strip()]

    labels = cells(lambda h: h == "comment[label]")
    mods = [_strip_cv(m) for m in cells(lambda h: "modification parameters" in h)]
    files = cells(lambda h: h == "comment[data file]")
    per_file: dict[str, int] = {}
    for f in files:
        per_file[f] = per_file.get(f, 0) + 1
    unique_labels = sorted(set(labels))
    unique_mods = sorted(set(mods))
    return SdrfClaim(
        path=str(path),
        n_rows=len(body),
        label_values=unique_labels,
        label_kinds={classify_label_value(v) for v in unique_labels},
        mod_names=unique_mods,
        mod_kinds={k for m in unique_mods for k, p in _MOD_PATTERNS if p.search(m)},
        data_files=sorted(per_file),
        max_rows_per_file=max(per_file.values(), default=0),
    )


# --- Evidence side ---------------------------------------------------------------------

_QUANT_PATTERNS = [
    (TMT, re.compile(r"\btmt|tandem mass tag", re.I)),
    (ITRAQ, re.compile(r"itraq", re.I)),
    (SILAC, re.compile(r"silac", re.I)),
    (DIMETHYL, re.compile(r"dimethyl", re.I)),
    (LABEL_FREE, re.compile(r"label[\s-]*free|spectrum count|spectral count|nsaf|emPAI|\bTIC\b|intensity", re.I)),
]

_PTM_PATTERNS = [
    (TMT, re.compile(r"\btmt", re.I)),
    (ITRAQ, re.compile(r"itraq", re.I)),
    # Heavy amino acids. Biological dimethylation ("dimethylated residue") is not a label.
    (SILAC, re.compile(r"\(13\)C.*labeled L-(arginine|lysine)|\(15\)N.*labeled L-(arginine|lysine)|^label:", re.I)),
    (DIMETHYL, re.compile(r"\(2\)H.*dimethyl|dimethyl.*\(2\)H|\(13\)C.*dimethyl", re.I)),
]

_PROTOCOL_PATTERNS = [
    (TMT, re.compile(
        r"\bTMT(?:pro|zero|\s*-?\s*(?:6|10|11|16|18|35)\s*-?\s*plex|\d*plex|\b)|tandem mass tag", re.I)),
    (ITRAQ, re.compile(r"\biTRAQ", re.I)),
    (SILAC, re.compile(
        r"\bSILAC\b|stable isotope label(?:l)?ing (?:by|with|using) amino acids"
        r"|\b(?:Lys|K)\s*-?\s*8\b|\b(?:Arg|R)\s*-?\s*10\b|13C6\s*-?\s*15N[24]"
        r"|heavy (?:isotope[- ]labell?ed )?(?:lysine|arginine)", re.I)),
    (DIMETHYL, re.compile(
        r"(?:reductive|stable isotope|triplex|duplex)\s+dimethyl|dimethyl(?:ation)?\s+label", re.I)),
]

# Phrases where a label word appears but no labelling was done on these samples.
_NEGATION = re.compile(
    r"\b(?:no|without|instead of|rather than|not)\b[^.;]{0,40}\b(?:TMT|iTRAQ|SILAC|label)", re.I)

_FILENAME_PATTERNS = [
    (TMT, re.compile(r"tmt", re.I)),
    (ITRAQ, re.compile(r"itraq", re.I)),
    (SILAC, re.compile(r"silac", re.I)),
    (DIMETHYL, re.compile(r"dimethyl|dime(?:th)?[-_]?lab", re.I)),
]


@dataclass
class Evidence:
    source: str  # quant_field | ptm | protocol | file_names | sdrf_mods | raw_header
    kind: str
    detail: str


def _snippet(text: str, m: re.Match, width: int = 90) -> str:
    start, end = max(0, m.start() - width), min(len(text), m.end() + width)
    return ("…" if start else "") + text[start:end].replace("\n", " ").strip() + ("…" if end < len(text) else "")


def collect_evidence(project: dict, file_names: list[str], claim: SdrfClaim | None = None) -> list[Evidence]:
    ev: list[Evidence] = []

    for q in project.get("quantificationMethods") or []:
        name = q.get("name", "")
        for kind, pat in _QUANT_PATTERNS:
            if pat.search(name):
                ev.append(Evidence("quant_field", kind, name))
                break

    for p in project.get("identifiedPTMStrings") or []:
        name = p.get("name", "") if isinstance(p, dict) else str(p)
        for kind, pat in _PTM_PATTERNS:
            if pat.search(name):
                ev.append(Evidence("ptm", kind, name))
                break

    for field_name in ("sampleProcessingProtocol", "dataProcessingProtocol"):
        text = project.get(field_name) or ""
        for kind, pat in _PROTOCOL_PATTERNS:
            for m in pat.finditer(text):
                snippet = _snippet(text, m)
                if _NEGATION.search(text[max(0, m.start() - 60): m.end()]):
                    continue
                ev.append(Evidence("protocol", kind, f"{field_name}: {snippet}"))
                break  # one quote per kind per field is enough

    for kind, pat in _FILENAME_PATTERNS:
        hits = [n for n in file_names if pat.search(n)]
        if hits:
            ev.append(Evidence("file_names", kind, f"{len(hits)} files, e.g. {hits[0]}"))

    if claim is not None:
        for kind in sorted(claim.mod_kinds):
            mods = [m for m in claim.mod_names if any(p.search(m) for k, p in _MOD_PATTERNS if k == kind)]
            ev.append(Evidence("sdrf_mods", kind, ", ".join(mods)))

    return ev


# --- Rules -----------------------------------------------------------------------------

@dataclass
class Finding:
    accession: str
    sdrf: str
    rule: str
    severity: str  # major | moderate | minor
    confidence: str  # strong | probable | weak
    claimed: str
    evidenced: str
    message: str
    evidence: list[Evidence] = field(default_factory=list)


def _support(ev: list[Evidence], kind: str) -> list[Evidence]:
    return [e for e in ev if e.kind == kind]


def _sources(ev: list[Evidence]) -> set[str]:
    return {e.source for e in ev}


def _confidence(support: list[Evidence]) -> str:
    """strong: two independent sources, or the protocol states it in both protocol fields.
    probable: an explicit protocol statement or a label in the raw file's method or sample
    name, alone. weak: a single indirect hint."""
    sources = _sources(support)
    protocol_fields = {e.detail.split(":", 1)[0] for e in support if e.source == "protocol"}
    if (len(sources) >= 2 and sources - {"sdrf_mods"}) or len(protocol_fields) >= 2:
        return "strong"
    if sources & {"protocol", "raw_header"}:
        return "probable"
    return "weak"


def check_labels(
    accession: str,
    claim: SdrfClaim,
    project: dict,
    file_names: list[str],
    sibling_kinds: set[str] | None = None,
    extra_evidence: list[Evidence] | None = None,
) -> list[Finding]:
    """Compare one SDRF's label claim with the deposit's evidence.

    ``sibling_kinds`` are the label kinds claimed by other SDRFs of the same accession. A
    label-free SDRF in a project whose other SDRF covers the labelled part is not an error.
    ``extra_evidence`` adds evidence gathered elsewhere, such as raw-file headers.
    """
    ev = collect_evidence(project, file_names, claim) + list(extra_evidence or [])
    labelled_ev = [e for e in ev if e.kind in LABELLED]
    lf_ev = [e for e in ev if e.kind == LABEL_FREE]
    evidenced_kinds = sorted({e.kind for e in labelled_ev})
    findings: list[Finding] = []
    sib = sibling_kinds or set()

    def add(rule, severity, confidence, evidenced, message, evidence):
        findings.append(Finding(accession, claim.path, rule, severity, confidence,
                                claim.kind, evidenced, message, evidence))

    if claim.kind == LABEL_FREE and labelled_ev:
        covered = {k for k in evidenced_kinds if any(k in s for s in sib)}
        uncovered = [k for k in evidenced_kinds if k not in covered]
        if uncovered:
            top = max(uncovered, key=lambda k: len(_sources(_support(labelled_ev, k))))
            support = _support(labelled_ev, top)
            mixed = " PRIDE also lists a label-free method, so the deposit may mix designs." if lf_ev else ""
            add("labelled-annotated-as-label-free", "major", _confidence(support), top,
                f"SDRF annotates every row as label-free, but the deposit indicates {top} labelling.{mixed}",
                support + lf_ev)

    elif claim.kind in LABELLED or "+" in claim.kind:
        claimed = set(claim.kind.split("+"))
        other = [k for k in evidenced_kinds if k not in claimed]
        agreeing = [e for e in labelled_ev if e.kind in claimed]
        if other and not agreeing:
            top = max(other, key=lambda k: len(_sources(_support(labelled_ev, k))))
            support = _support(labelled_ev, top)
            add("wrong-label-type", "major", _confidence(support), top,
                f"SDRF claims {claim.kind}, but the deposit indicates {top} and nothing supports {claim.kind}.",
                support)
        for kind in claimed:
            if kind in (TMT, ITRAQ, SILAC, DIMETHYL) and kind not in claim.mod_kinds:
                add("label-modification-missing", "moderate", "strong", kind,
                    f"SDRF claims {kind} labels but declares no {kind} modification parameter; "
                    "a search configured from this SDRF would not account for the label.",
                    [Evidence("sdrf_mods", "none", ", ".join(claim.mod_names) or "(no modification parameters)")])
        if claimed & {TMT, ITRAQ} and claim.max_rows_per_file == 1 and claim.n_rows > 1:
            add("multiplex-one-row-per-file", "moderate", "weak", claim.kind,
                f"SDRF claims {claim.kind} but has one row per data file; isobaric runs normally "
                "carry one row per channel.", [])

    if claim.kind == ISOTOPE:
        add("unspecified-isotope-label", "minor", "strong",
            ", ".join(evidenced_kinds) or "unknown",
            "SDRF uses the generic 'isotope labeling' term instead of the specific label channels.",
            labelled_ev)

    return findings
