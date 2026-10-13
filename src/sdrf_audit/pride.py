"""Cached, rate-limited client for the PRIDE Archive v3 REST API."""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/"
USER_AGENT = "sdrf-audit/0.1 (+https://github.com/dl-devworks/bioinfoProject)"

# Fields kept from the project record; the full record carries much we never use.
PROJECT_FIELDS = (
    "accession", "title", "submissionDate", "publicationDate", "sampleProcessingProtocol",
    "dataProcessingProtocol", "instruments", "quantificationMethods", "experimentTypes",
    "softwares", "organisms", "identifiedPTMStrings", "keywords", "projectTags",
)


class NotFound(Exception):
    """PRIDE has no public record for the accession."""


class PrideClient:
    """Fetches project records and file lists, caching each response as JSON on disk.

    Requests are spaced at least ``min_interval`` seconds apart across all threads, so a
    thread pool raises throughput only up to that rate.
    """

    def __init__(self, cache_dir: str | Path, min_interval: float = 0.15, retries: int = 4):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.min_interval = min_interval
        self.retries = retries
        self._lock = threading.Lock()
        self._next_slot = 0.0

    def project(self, acc: str) -> dict:
        record = self._cached(f"{acc}.project.json", API + acc)
        return {k: record.get(k) for k in PROJECT_FIELDS}

    def files(self, acc: str) -> list[dict]:
        listing = self._cached(f"{acc}.files.json", API + acc + "/files/all")
        return [
            {
                "fileName": f.get("fileName"),
                "fileSizeBytes": f.get("fileSizeBytes"),
                "category": (f.get("fileCategory") or {}).get("value"),
                "ftp": next(
                    (loc["value"] for loc in f.get("publicFileLocations", [])
                     if loc.get("value", "").startswith("ftp://")),
                    None,
                ),
            }
            for f in listing
        ]

    def _cached(self, name: str, url: str):
        path = self.cache_dir / name
        if path.exists():
            data = json.loads(path.read_text())
            if data == {"__not_found__": True}:
                raise NotFound(url)
            return data
        try:
            data = self._get(url)
        except NotFound:
            path.write_text(json.dumps({"__not_found__": True}))
            raise
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        tmp.replace(path)
        return data

    def _wait_turn(self) -> None:
        with self._lock:
            now = time.monotonic()
            slot = max(now, self._next_slot)
            self._next_slot = slot + self.min_interval
        time.sleep(max(0.0, slot - now))

    def _get(self, url: str):
        err: Exception | None = None
        for attempt in range(self.retries):
            self._wait_turn()
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    return json.load(resp)
            except urllib.error.HTTPError as e:
                if e.code in (400, 404):
                    raise NotFound(url) from e
                err = e
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
                err = e
            time.sleep(2 ** attempt)
        raise RuntimeError(f"PRIDE request failed after {self.retries} attempts: {url}") from err
