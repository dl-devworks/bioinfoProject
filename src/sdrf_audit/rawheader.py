"""Evidence from the header of a deposited Thermo .raw file.

The first 256 KB of a Thermo .raw file hold UTF-16 strings written at acquisition: the
instrument model, the instrument-method path, the original file path and the sample
description, and on newer instruments a method summary. Reading them needs only an HTTP
range request, not the full multi-GB file.

Method and sample names are chosen by the operator, so a label word in them (``TMTpro_…``,
``…_SILAC_…``) is evidence of labelling, while its absence proves nothing.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

from .labels import DIMETHYL, ITRAQ, SILAC, TMT, Evidence
from .pride import USER_AGENT

HEADER_BYTES = 256 * 1024

_MODEL = re.compile(
    r"^(?:Orbitrap\b.*|Q Exactive.*|LTQ\b.*|Exactive.*|TSQ\b.*|Astral.*)$")
_LABEL_TOKENS = [
    (TMT, re.compile(r"(?<![A-Za-z])TMT|tandem[ _-]?mass[ _-]?tag", re.I)),
    (ITRAQ, re.compile(r"itraq", re.I)),
    (SILAC, re.compile(r"(?<![A-Za-z])SILAC", re.I)),
    (DIMETHYL, re.compile(r"dimethyl", re.I)),
]


def header_strings(data: bytes) -> list[str]:
    text = data.decode("utf-16-le", errors="ignore")
    return [s.strip() for s in re.findall(r"[\x20-\x7e]{4,}", text)]


def parse_header(data: bytes) -> dict:
    """Instrument models, method paths and label tokens found in a .raw header."""
    strings = header_strings(data)
    models = sorted({s for s in strings if _MODEL.match(s) and len(s) < 60})
    methods = sorted({s for s in strings if s.lower().endswith(".meth")})
    labels: dict[str, list[str]] = {}
    for s in strings:
        for kind, pat in _LABEL_TOKENS:
            if pat.search(s):
                labels.setdefault(kind, [])
                if s not in labels[kind] and len(labels[kind]) < 3:
                    labels[kind].append(s[:160])
    return {"models": models, "methods": methods, "labels": labels}


def evidence_from_header(parsed: dict, file_name: str) -> list[Evidence]:
    return [
        Evidence("raw_header", kind, f"{file_name}: {examples[0]}")
        for kind, examples in sorted(parsed.get("labels", {}).items())
    ]


def pick_raw_file(files: list[dict], prefer: list[str] | None = None) -> dict | None:
    """A real-sized Thermo .raw file from a PRIDE listing, preferring ones the SDRF names."""
    raws = [f for f in files
            if (f.get("fileName") or "").lower().endswith(".raw")
            and (f.get("fileSizeBytes") or 0) > 1_000_000 and f.get("ftp")]
    if not raws:
        return None
    wanted = set(prefer or [])
    raws.sort(key=lambda f: (f["fileName"] not in wanted, f["fileName"]))
    return raws[0]


class RawHeaderCache:
    """Fetches and caches parsed headers, one JSON file per accession."""

    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def path(self, acc: str) -> Path:
        return self.cache_dir / f"{acc}.json"

    def get(self, acc: str) -> dict | None:
        p = self.path(acc)
        return json.loads(p.read_text()) if p.exists() else None

    def fetch(self, acc: str, files: list[dict], prefer: list[str] | None = None) -> dict:
        cached = self.get(acc)
        if cached is not None:
            return cached
        raw = pick_raw_file(files, prefer)
        if raw is None:
            result = {"status": "no_thermo_raw"}
        else:
            url = raw["ftp"].replace("ftp://", "https://", 1)
            req = urllib.request.Request(
                url, headers={"Range": f"bytes=0-{HEADER_BYTES - 1}", "User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = resp.read(HEADER_BYTES)
                result = {"status": "ok", "file": raw["fileName"], **parse_header(data)}
            except Exception as e:  # transient failures are not cached
                return {"status": "error", "error": repr(e)}
        self.path(acc).write_text(json.dumps(result))
        return result
