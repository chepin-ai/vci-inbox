"""AD-25 三仓非强制 API 发布；blob→tree→commit→ref，凭证只从隔离存储读取。"""
import base64
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "/mnt/agents/output/.stash/ad21/run")
from ad21_publish import request, VAULT

S = Path("/mnt/agents/output/.stash/ad16")
A21 = Path("/mnt/agents/output/.stash/ad21/run")
A23 = Path("/mnt/agents/output/.stash/ad23/run")
A24 = Path("/mnt/agents/output/.stash/ad24/run")
R = Path("/mnt/agents/output/.stash/ad25/run")
L = R.parent / "literature"


def source_for(name):
    if name.startswith("run/"):
        return R / name[4:]
    if name.startswith("ad21/run/"):
        return A21 / name[9:]
    if name.startswith("ad23/run/"):
        return A23 / name[9:]
    if name.startswith("ad24/run/"):
        return A24 / name[9:]
    if name.startswith("literature/"):
        return L / name[11:]
    return S / name


def publish(repo, token_name, files, message, receipt_name, rounds=12):
    token = (VAULT / token_name).read_text().strip()
    assert token
    blobs = {}
    for target, src in sorted(files.items()):
        raw = src.read_bytes()
        blob = request("POST", f"/repos/{repo}/git/blobs", token,
                       {"content": base64.b64encode(raw).decode(), "encoding": "base64"}, attempts=3)
        blobs[target] = blob["sha"]
    race_attempts = 0
    for _ in range(rounds):
        head = request("GET", f"/repos/{repo}/git/ref/heads/main", token)["object"]["sha"]
        commit0 = request("GET", f"/repos/{repo}/git/commits/{head}", token)
        tree = request("POST", f"/repos/{repo}/git/trees", token,
                       {"base_tree": commit0["tree"]["sha"],
                        "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": sha}
                                 for p, sha in blobs.items()]}, attempts=3)
        commit = request("POST", f"/repos/{repo}/git/commits", token,
                         {"message": message, "tree": tree["sha"], "parents": [head]}, attempts=3)
        try:
            request("PATCH", f"/repos/{repo}/git/refs/heads/main", token,
                    {"sha": commit["sha"], "force": False}, attempts=1)
            observed = request("GET", f"/repos/{repo}/git/ref/heads/main", token)["object"]["sha"]
            assert observed == commit["sha"]
            receipt = {
                "repo": repo, "branch": "main", "commit": commit["sha"], "observed_head": observed,
                "parent": head, "tree": tree["sha"], "base_tree": commit0["tree"]["sha"],
                "race_attempts": race_attempts, "blob_shas": blobs,
                "file_sha256": {p: hashlib.sha256(src.read_bytes()).hexdigest() for p, src in files.items()},
            }
            (R / receipt_name).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
            return receipt
        except RuntimeError:
            race_attempts += 1
            time.sleep(3)
    raise RuntimeError(f"{repo}: non-fast-forward race did not settle")


def main():
    manifest = json.loads((R / "ad25_MANIFEST.json").read_text())
    cap = json.loads((S / "capsule-251.json").read_text())
    chain = json.loads((S / "chain_head.json").read_text())
    hub = json.loads((S / "hub_qlv_outbox.json").read_text())
    assert cap["prev"] == "57e4b840cb388071" and cap["seq"] == 251
    payload = hashlib.sha256(json.dumps(cap["body"], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    cid = hashlib.sha256((cap["prev"] + payload + cap["ts"]).encode()).hexdigest()[:16]
    assert payload == cap["payload_sha256"] and cid == cap["cid"] == manifest["cid"]
    assert chain == {"seq": 251, "cid": cid, "ts": cap["ts"]}
    assert hub["chain_head"]["cid"] == cid and hub["chain_head"]["seq"] == 251

    # 写前再核公仓链头，防止覆盖他线竞进；只读取链态字段，不回显正文。
    qi_token = (VAULT / "qi_pat.txt").read_text().strip()
    current = request("GET", "/repos/chepin-qi/qlv-pub/contents/outbox/qlv-outbox.json?ref=main", qi_token, attempts=3)
    current_hub = json.loads(base64.b64decode(current["content"]))
    assert current_hub["chain_head"]["seq"] == 250 and current_hub["chain_head"]["cid"] == cap["prev"]

    vci = {}
    for name, expected in manifest["files"].items():
        src = source_for(name)
        assert hashlib.sha256(src.read_bytes()).hexdigest() == expected
        vci["lanes/qlv/outbox-pending/" + name] = src
    vci["lanes/qlv/outbox-pending/run/ad25_MANIFEST.json"] = R / "ad25_MANIFEST.json"
    vci["lanes/qlv/outbox/qlv-outbox.json"] = S / "hub_qlv_outbox.json"

    prefix = f"拍AD-25(承AD-24 cid{cap['prev']}) @lvlu @cisvr @qfa @lgt: "
    msg_q = prefix + f"outbox刷seq251(cid{cid}); MAJ饱和等号+S2全球11CZ+board162+独立ALL_PASS+零真机/私域CI [skip ci]"
    msg_v = prefix + f"MAJ饱和等号+S2全球11CZ+序91横向528条; board162/capsule251 cid{cid} [skip ci]"
    msg_c = prefix + f"PLATEAU-08正件; 严格区间4<=k<=7不变; 11CZ非最优; RAC候件; capsule251 cid{cid} [skip ci]"
    for msg in (msg_v, msg_c, msg_q):
        assert all(a in msg[:200] for a in ("@lvlu", "@cisvr", "@qfa", "@lgt")) and "[skip ci]" in msg

    receipts = {}
    receipts["qlv-pub"] = publish("chepin-qi/qlv-pub", "qi_pat.txt",
                                  {"outbox/qlv-outbox.json": S / "hub_qlv_outbox.json"},
                                  msg_q, "ad25_qlvpub_receipt.json")
    receipts["vci-inbox"] = publish("chepin-ai/vci-inbox", "fed_pat.txt", vci,
                                    msg_v, "ad25_vci_receipt.json")
    discussion = (R / "ad25_discussion_name.txt").read_text().strip()
    ci = {
        "shared/field-engine/QRAC-TRIALS-01/QRAC-D8-TOFFOLI-PLATEAU-08.md": S / "QRAC-D8-TOFFOLI-PLATEAU-08.md",
        "讨论室/threads/" + discussion: S / discussion,
    }
    receipts["ci-inbox"] = publish("chepin-ai/ci-inbox", "fed_pat.txt", ci,
                                   msg_c, "ad25_ciinbox_receipt.json")
    print(json.dumps({k: {"repo": v["repo"], "commit": v["commit"], "parent": v["parent"],
                          "files": len(v["file_sha256"]), "race_attempts": v["race_attempts"]}
                      for k, v in receipts.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
