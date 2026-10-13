"""Feasibility probe for sdrf-audit: sample corpus SDRFs, compare against PRIDE.

Usage: python3 -I probe.py <corpus_dir> <n> <seed> <out.json>
"""
import csv, json, random, re, sys, time, urllib.request
from collections import Counter
from pathlib import Path

API = "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/"

RESULT_PATTERNS = {
    "mzid": r"\.mzid(\.gz)?$",
    "mztab": r"\.mztab(\.gz)?$",
    "maxquant": r"(evidence|proteinGroups|peptides|msms)\.txt$|txt\.zip$|combined.*\.zip$",
    "diann": r"report.*\.(tsv|parquet)$|pg_matrix|pr_matrix",
    "fragpipe": r"psm\.tsv$|combined_protein\.tsv$|ion\.tsv$",
    "pepxml": r"\.pep\.xml$|\.pepxml$",
    "spectronaut": r"spectronaut|\.sne$",
    "pd": r"\.msf$|\.pdresult$",
}
PEAK_PATTERNS = {"mzml": r"\.mzml(\.gz)?$", "mgf": r"\.mgf(\.gz)?$", "mzxml": r"\.mzxml(\.gz)?$"}


def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # retry transient API errors
            err = e
            time.sleep(2 ** i)
    raise err


def norm_instr(s):
    s = re.sub(r"^.*NT=", "", s or "").split(";")[0]
    return re.sub(r"[^a-z0-9]", "", s.lower())


def read_sdrf(path):
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    head = [h.strip().lower() for h in rows[0]]
    body = [r for r in rows[1:] if any(c.strip() for c in r)]

    def col(name):
        idx = [i for i, h in enumerate(head) if h == name]
        return [r[i].strip() for r in body for i in idx if i < len(r)]

    return {
        "data_files": set(col("comment[data file]")),
        "instruments": set(col("comment[instrument]")),
        "labels": set(col("comment[label]")),
        "n_rows": len(body),
    }


def strip_ext(name):
    return re.sub(r"\.(raw|wiff|d|mzml|mgf|zip|gz|wiff\.scan)+$", "", name.lower())


def probe(acc, sdrf_path):
    s = read_sdrf(sdrf_path)
    files = get(API + acc + "/files/all")
    proj = get(API + acc)
    names = [f["fileName"] for f in files]
    lower = [n.lower() for n in names]
    cats = Counter(f.get("fileCategory", {}).get("value", "?") for f in files)
    found = {k: sum(bool(re.search(p, n)) for n in lower) for k, p in {**RESULT_PATTERNS, **PEAK_PATTERNS}.items()}

    pride_exact = set(names)
    pride_stems = {strip_ext(n) for n in names}
    missing_exact = {d for d in s["data_files"] if d not in pride_exact}
    missing_stem = {d for d in missing_exact if strip_ext(d) not in pride_stems}

    pride_instr = {norm_instr(i.get("name", "")) for i in proj.get("instruments", [])}
    sdrf_instr = {norm_instr(i) for i in s["instruments"]}
    return {
        "acc": acc,
        "n_rows": s["n_rows"],
        "n_sdrf_files": len(s["data_files"]),
        "n_pride_files": len(files),
        "categories": dict(cats),
        "found": found,
        "has_peaklist": any(found[k] for k in PEAK_PATTERNS),
        "has_results": any(found[k] for k in RESULT_PATTERNS),
        "missing_exact": len(missing_exact),
        "missing_after_ext_norm": sorted(missing_stem)[:5],
        "n_missing_after_ext_norm": len(missing_stem),
        "sdrf_instruments": sorted(s["instruments"]),
        "pride_instruments": [i.get("name") for i in proj.get("instruments", [])],
        "instrument_agree": bool(sdrf_instr & pride_instr) if sdrf_instr and pride_instr else None,
        "labels": sorted(s["labels"]),
        "pride_quant": [q.get("name") for q in proj.get("quantificationMethods", [])],
    }


def main():
    corpus, n, seed, out = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    paths = sorted(corpus.glob("datasets/PXD*/PXD*.sdrf.tsv"))
    random.Random(seed).shuffle(paths)
    results = []
    for p in paths[:n]:
        acc = p.parent.name
        try:
            results.append(probe(acc, p))
        except Exception as e:
            results.append({"acc": acc, "error": repr(e)})
        print(acc, "ok" if "error" not in results[-1] else results[-1]["error"], flush=True)
    Path(out).write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
