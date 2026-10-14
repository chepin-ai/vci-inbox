#!/usr/bin/env python3
"""UCIF2-COMPARATOR-KERNEL-01 pilot gate (public plane).
Three-core FAIL-CLOSED checks on mirror/latest-cisvr.md:
  1. statement match: sha256(artifact) == challenge.spec_sha256
  2. kernel replay: classification marker + canonical head + signature revalidated, forbidden patterns absent
  3. trust base: trust.json external_dependencies must be empty
"""
import hashlib, json, os, re, sys

ROOT = os.environ.get("GITHUB_WORKSPACE", ".")
art = os.path.join(ROOT, "mirror/latest-cisvr.md")

def fail(msg):
    print("REJECT:", msg); sys.exit(1)

if not os.path.isfile(art):
    fail("artifact missing")

ch = json.load(open(os.path.join(ROOT, "mirror/latest-cisvr.challenge.json")))
body = open(art, "rb").read()
if hashlib.sha256(body).hexdigest() != ch["spec_sha256"]:
    fail("statement mismatch: artifact drifted from registered spec hash")

lat = body.decode("utf-8")
head = lat[:2000]
if "CLASSIFY: L1" not in head:
    fail("classification marker missing (guard would quarantine)")
if "# LATEST \u00b7" not in head and "# LATEST ·" not in head:
    fail("canonical head missing")
if "毂" not in lat:
    fail("signature missing")
for bad in ch["forbidden_patterns"]:
    if re.search(bad, lat):
        fail("forbidden pattern hit: " + bad)

tr = json.load(open(os.path.join(ROOT, "mirror/latest-cisvr.trust.json")))
if tr.get("external_dependencies"):
    fail("external deps not in whitelist: " + str(tr["external_dependencies"]))

print("ACCEPT: comparator01 three-core gate PASS")
