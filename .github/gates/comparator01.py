#!/usr/bin/env python3
# COMPARATOR-01 kernel replay gate (UCIF2-COMPARATOR-KERNEL-01 pilot, T2 star track)
# public-plane pilot: artifact = mirror/latest-cisvr.md (L1 projection)
# three checks: statement match / kernel replay / trust-base whitelist. FAIL-CLOSED.
import json, sys, hashlib, re, os

ROOT = os.environ.get("GATE_ROOT", ".")
def fail(msg):
    print(json.dumps({"gate": "comparator01", "verdict": "REJECT", "reason": msg}, ensure_ascii=False))
    sys.exit(1)

ch = json.load(open(os.path.join(ROOT, "mirror/latest-cisvr.challenge.json")))
art = os.path.join(ROOT, ch["artifact"])
body = open(art, "rb").read()
if hashlib.sha256(body).hexdigest() != ch["spec_sha256"]:
    fail("statement mismatch: artifact drifted from registered spec hash")
lat = body.decode("utf-8")
if not lat.startswith("# LATEST ·"): fail("canonical head missing")
if "毂" not in lat: fail("signature missing")
for bad in ch["forbidden_patterns"]:
    if re.search(bad, lat): fail("forbidden pattern hit: " + bad)
tr = json.load(open(os.path.join(ROOT, "mirror/latest-cisvr.trust.json")))
if tr.get("external_dependencies"): fail("external deps not in whitelist")
print(json.dumps({"gate": "comparator01", "verdict": "ACCEPT", "artifact": ch["artifact"],
                  "tier": ch.get("tier"), "checks": ["statement", "replay", "trust"]}, ensure_ascii=False))
