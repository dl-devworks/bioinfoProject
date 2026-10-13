"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .pride import NotFound, PrideClient


def corpus_accessions(corpus: Path) -> list[str]:
    """PXD accessions that have at least one SDRF in a sdrf-annotated-datasets checkout."""
    return sorted(
        d.name for d in (corpus / "datasets").iterdir()
        if d.is_dir() and d.name.startswith("PXD") and any(d.glob("*.sdrf*"))
    )


def cmd_fetch(args: argparse.Namespace) -> int:
    client = PrideClient(args.cache, min_interval=args.min_interval)
    accs = corpus_accessions(Path(args.corpus))
    if args.limit:
        accs = accs[: args.limit]

    def fetch(acc: str) -> str:
        try:
            client.project(acc)
            client.files(acc)
            return "ok"
        except NotFound:
            return "not_found"
        except Exception as e:  # keep going; failures are retried on the next run
            return f"error: {e}"

    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch, a): a for a in accs}
        for i, fut in enumerate(as_completed(futures), 1):
            status = fut.result()
            key = status.split(":")[0]
            counts[key] = counts.get(key, 0) + 1
            if key == "error":
                print(futures[fut], status, file=sys.stderr, flush=True)
            if i % 500 == 0 or i == len(accs):
                print(f"{i}/{len(accs)} {counts}", flush=True)
    return 0 if not counts.get("error") else 1


def cmd_labels(args: argparse.Namespace) -> int:
    import csv
    import json
    from dataclasses import asdict

    from .labels import check_labels, read_sdrf

    client = PrideClient(args.cache)
    corpus = Path(args.corpus)
    accs = args.accessions or corpus_accessions(corpus)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    findings, audited, skipped = [], [], {}
    for acc in accs:
        if args.offline and not (client.cache_dir / f"{acc}.files.json").exists():
            skipped[acc] = "not cached"
            continue
        try:
            project, files = client.project(acc), client.files(acc)
        except NotFound:
            skipped[acc] = "not in PRIDE"
            continue
        names = [f["fileName"] for f in files]
        claims = []
        for path in sorted((corpus / "datasets" / acc).glob("*.sdrf*")):
            try:
                claims.append(read_sdrf(path))
            except Exception as e:  # malformed file: report, don't crash the run
                skipped[f"{acc}:{path.name}"] = f"unreadable: {e}"
        for claim in claims:
            siblings = {c.kind for c in claims if c is not claim}
            found = check_labels(acc, claim, project, names, siblings)
            findings.extend(found)
            audited.append({"accession": acc, "sdrf": Path(claim.path).name, "claimed": claim.kind,
                            "n_rows": claim.n_rows, "n_findings": len(found)})

    rel = lambda p: str(Path(p).relative_to(corpus)) if Path(p).is_relative_to(corpus) else p
    with open(out / "findings.json", "w") as f:
        json.dump([{**asdict(x), "sdrf": rel(x.sdrf)} for x in findings], f, indent=1)
    with open(out / "findings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["accession", "sdrf", "rule", "severity", "confidence", "claimed", "evidenced",
                    "sources", "message", "evidence"])
        for x in findings:
            w.writerow([x.accession, rel(x.sdrf), x.rule, x.severity, x.confidence, x.claimed, x.evidenced,
                        ";".join(sorted({e.source for e in x.evidence})), x.message,
                        " | ".join(f"[{e.source}] {e.detail}" for e in x.evidence)])
    with open(out / "audited.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["accession", "sdrf", "claimed", "n_rows", "n_findings"])
        w.writeheader()
        w.writerows(audited)
    (out / "skipped.json").write_text(json.dumps(skipped, indent=1))
    print(f"audited {len(audited)} SDRFs in {len({a['accession'] for a in audited})} accessions; "
          f"{len(findings)} findings; {len(skipped)} skipped -> {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sdrf-audit")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("fetch", help="cache PRIDE metadata for every accession in an SDRF corpus")
    p.add_argument("corpus", help="path to a sdrf-annotated-datasets checkout")
    p.add_argument("--cache", default="cache/pride")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--min-interval", type=float, default=0.15, help="seconds between requests")
    p.add_argument("--limit", type=int, default=0)
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("labels", help="check label annotations against PRIDE evidence")
    p.add_argument("corpus", help="path to a sdrf-annotated-datasets checkout")
    p.add_argument("accessions", nargs="*", help="limit to these accessions")
    p.add_argument("--cache", default="cache/pride")
    p.add_argument("--out", default="results/labels")
    p.add_argument("--offline", action="store_true", help="only audit accessions already cached")
    p.set_defaults(func=cmd_labels)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
