#!/usr/bin/env python3
"""Canonical same-generation CAS writer for the QF-OS stream ledger.

The caller supplies an event without authoritative seq/prev/hash.  Every attempt
reads one generation (text + blob sha), rebuilds the chain tip from that exact
text, and PUTs with that exact sha.  A conflict causes a complete reread; stale
text is never paired with a newer sha.  No ledger bytes are printed.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable, Optional

OWNER = "chepin-ai"
REPO = "HUB-CORE"
LEDGER_PATH = "bridge/stream-ledger.jsonl"
API_BASE = "https://api.github.com"
FULL_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class LedgerAppendError(RuntimeError):
    """Fail-closed append error; no alternate unsafe write is attempted."""


@dataclass(frozen=True)
class Generation:
    status: int
    text: Optional[str] = None
    sha: Optional[str] = None


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _validated_entries(text: str):
    if not isinstance(text, str) or not text.strip():
        raise LedgerAppendError("LEDGER-CAS-02 empty ledger; append refused")
    try:
        entries = [json.loads(line) for line in text.splitlines() if line.strip()]
    except Exception as exc:
        raise LedgerAppendError("LEDGER-CAS-02 parse failure; append refused") from exc
    if not entries or [e.get("seq") for e in entries] != list(range(1, len(entries) + 1)):
        raise LedgerAppendError("LEDGER-CAS-02 sequence failure; append refused")
    tip_hash = entries[-1].get("hash")
    if not isinstance(tip_hash, str) or not FULL_SHA256.fullmatch(tip_hash):
        raise LedgerAppendError("LEDGER-CAS-02 non-strict tip hash; append refused")
    return entries


def next_event(event: dict, tip: dict) -> dict:
    """Derive a fresh strict entry without mutating the caller's event."""
    if not isinstance(event, dict):
        raise TypeError("event must be a dict")
    result = copy.deepcopy(event)
    result.pop("hash", None)
    result["seq"] = tip["seq"] + 1
    result["prev"] = tip["hash"]
    result["hash"] = hashlib.sha256((result["prev"] + canon(result)).encode()).hexdigest()
    return result


class GitHubContentsTransport:
    """Contents API transport; authentication values are never logged or stored in events."""

    def __init__(self, headers, owner=OWNER, repo=REPO, path=LEDGER_PATH,
                 api_base=API_BASE, opener=None, timeout=25):
        self._headers = headers
        self.owner = owner
        self.repo = repo
        self.path = path
        self.api_base = api_base.rstrip("/")
        self.opener = opener or urllib.request.urlopen
        self.timeout = timeout
        self.last_commit_sha = None

    def headers(self):
        return self._headers() if callable(self._headers) else dict(self._headers)

    def url(self):
        return (f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/"
                f"{urllib.parse.quote(self.path, safe='')}")

    def read(self) -> Generation:
        request = urllib.request.Request(self.url(), headers=self.headers())
        try:
            with self.opener(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode())
                status = response.status
        except urllib.error.HTTPError as exc:
            return Generation(exc.code)
        except (OSError, TimeoutError):
            return Generation(0)
        if status != 200 or not isinstance(data, dict) or not data.get("content"):
            return Generation(status)
        try:
            text = base64.b64decode(data["content"]).decode()
        except Exception as exc:
            raise LedgerAppendError("LEDGER-CAS-02 undecodable generation; append refused") from exc
        return Generation(status, text, data.get("sha"))

    def write_same_generation(self, content: str, message: str, sha: str) -> int:
        self.last_commit_sha = None
        body = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "sha": sha,
        }
        request = urllib.request.Request(
            self.url(), data=json.dumps(body).encode(), method="PUT", headers=self.headers())
        try:
            with self.opener(request, timeout=self.timeout) as response:
                status = response.status
                if status in (200, 201):
                    try:
                        payload = json.loads(response.read().decode())
                        self.last_commit_sha = payload.get("commit", {}).get("sha")
                    except Exception:
                        self.last_commit_sha = None
                return status
        except urllib.error.HTTPError as exc:
            return exc.code
        except (OSError, TimeoutError):
            return 0


def append_ledger(event: dict, label: str, transport, retries=6,
                  sleep: Callable[[float], None] = time.sleep, stats: Optional[dict] = None):
    """Append one strict event and return the stored entry.

    stats, when supplied, receives monotonic attempt counters so tests and
    callers can prove that conflicts really exercised reread/rebuild behavior.
    """
    if retries < 1:
        raise ValueError("retries must be positive")
    if not isinstance(label, str) or not label.strip():
        raise ValueError("label must be nonempty")
    counters = {"reads": 0, "read_retries": 0, "writes": 0,
                "conflict_retries": 0, "write_retries": 0, "appended": 0}
    if stats is not None:
        stats.clear()
        stats.update(counters)

    def bump(key):
        counters[key] += 1
        if stats is not None:
            stats[key] = counters[key]

    for attempt in range(retries):
        generation = transport.read()
        bump("reads")
        if generation.status in (400, 401, 403):
            raise LedgerAppendError(f"LEDGER-CAS-02 fatal read status {generation.status}; append refused")
        if generation.status != 200 or generation.text is None or not generation.sha:
            bump("read_retries")
            if attempt + 1 < retries:
                sleep(2 * (attempt + 1))
            continue

        entries = _validated_entries(generation.text)
        stored = next_event(event, entries[-1])
        new_text = (generation.text +
                    ("" if generation.text.endswith("\n") else "\n") +
                    json.dumps(stored, ensure_ascii=False) + "\n")
        message = f"{label} seq{stored['seq']}"
        status = transport.write_same_generation(new_text, message, generation.sha)
        bump("writes")
        if status in (200, 201):
            bump("appended")
            return stored
        if status in (400, 401, 403):
            raise LedgerAppendError(f"LEDGER-CAS-02 fatal write status {status}; append refused")
        bump("conflict_retries" if status in (409, 412, 422) else "write_retries")
        if attempt + 1 < retries:
            sleep(2 * (attempt + 1))
    raise LedgerAppendError("LEDGER-CAS-02 append retries exhausted; no stale overwrite attempted")


def _entry(seq, previous, marker="kat"):
    body = {"seq": seq, "prev": previous, "marker": marker}
    body["hash"] = hashlib.sha256((previous + canon(body)).encode()).hexdigest()
    return body


def _ledger(count):
    entries = []
    previous = "0" * 64
    for seq in range(1, count + 1):
        item = _entry(seq, previous)
        entries.append(item)
        previous = item["hash"]
    return "\n".join(json.dumps(e) for e in entries) + "\n", entries


class FakeTransport:
    """Known-answer transport with real generation and prefix assertions."""
    def __init__(self, texts, write_statuses=None, read_statuses=None):
        self.generations = [Generation(200, text, f"blob-{i}") for i, text in enumerate(texts)]
        self.write_statuses = list(write_statuses or [])
        self.read_statuses = list(read_statuses or [])
        self.index = 0
        self.writes = []
        self.appended_text = None

    def read(self):
        if self.read_statuses:
            status = self.read_statuses.pop(0)
            if status != 200:
                return Generation(status)
        return self.generations[self.index]

    def write_same_generation(self, content, message, sha):
        generation = self.generations[self.index]
        assert sha == generation.sha, "stale text paired with another generation sha"
        assert content.startswith(generation.text), "append-only byte prefix violated"
        self.writes.append({"sha": sha, "content": content, "generation": self.index})
        status = self.write_statuses.pop(0) if self.write_statuses else 200
        if status in (200, 201):
            self.appended_text = content
        elif self.index + 1 < len(self.generations):
            self.index += 1
        return status


def selftest():
    results = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        results.append(name)

    text7, entries7 = _ledger(7)
    transport = FakeTransport([text7])
    original = {"kind": "KAT", "seq": 1, "prev": "attacker", "hash": "attacker"}
    snapshot = copy.deepcopy(original)
    stats = {}
    stored = append_ledger(original, "selftest", transport, sleep=lambda _: None, stats=stats)
    check("ok_rebinds_tip_and_preserves_input", stored["seq"] == 8 and
          stored["prev"] == entries7[-1]["hash"] and original == snapshot and stats["appended"] == 1)
    check("ok_prefix_and_hash", transport.appended_text.startswith(text7) and
          stored["hash"] == hashlib.sha256((stored["prev"] + canon({k: v for k, v in stored.items() if k != "hash"})).encode()).hexdigest())

    text8, entries8 = _ledger(8)
    transport = FakeTransport([text7, text8], [409, 200])
    stored = append_ledger({"kind": "KAT"}, "conflict", transport, sleep=lambda _: None, stats=stats)
    check("conflict_full_reread_rebuild", stored["seq"] == 9 and stored["prev"] == entries8[-1]["hash"] and
          len(transport.writes) == 2 and transport.writes[0]["generation"] == 0 and
          transport.writes[1]["generation"] == 1 and stats["conflict_retries"] == 1)

    for name, bad_text in [
        ("malformed_rejected", "{not-json}\n"),
        ("sequence_gap_rejected", _ledger(2)[0].replace('"seq": 2', '"seq": 3')),
        ("short_tip_rejected", json.dumps({"seq": 1, "hash": "abc123"}) + "\n"),
    ]:
        transport = FakeTransport([bad_text])
        try:
            append_ledger({"kind": "KAT"}, name, transport, sleep=lambda _: None)
            raised = False
        except LedgerAppendError:
            raised = True
        check(name, raised and not transport.writes)

    transport = FakeTransport([text7], read_statuses=[403])
    try:
        append_ledger({"kind": "KAT"}, "fatal-read", transport, sleep=lambda _: None)
        raised = False
    except LedgerAppendError:
        raised = True
    check("fatal_read_fail_closed", raised and not transport.writes)

    transport = FakeTransport([text7, text8], [409, 409])
    try:
        append_ledger({"kind": "KAT"}, "exhausted", transport, retries=2, sleep=lambda _: None)
        raised = False
    except LedgerAppendError:
        raised = True
    check("retry_exhaustion_never_reports_append", raised and len(transport.writes) == 2 and transport.appended_text is None)

    transport = FakeTransport([text7], read_statuses=[404, 200])
    stored = append_ledger({"kind": "KAT"}, "transient-404", transport, sleep=lambda _: None, stats=stats)
    check("transient_404_full_reread_then_append", stored["seq"] == 8 and stats["read_retries"] == 1 and len(transport.writes) == 1)

    transport = FakeTransport([text7], read_statuses=[404, 404])
    try:
        append_ledger({"kind": "KAT"}, "persistent-404", transport, retries=2, sleep=lambda _: None)
        raised = False
    except LedgerAppendError:
        raised = True
    check("persistent_404_zero_writes", raised and not transport.writes)

    return {"verdict": "PASS", "tests": results, "test_count": len(results),
            "real_remote_writes": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if not args.selftest:
        parser.error("only --selftest is available without an embedding workflow")
    print(json.dumps(selftest(), ensure_ascii=False))
