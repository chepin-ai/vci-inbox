"""AD-25 远端逐字节、main祖先、公网main终验，并从远端blob干净重建同哈希复验。"""
import base64
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, "/mnt/agents/output/.stash/ad21/run")
from ad21_publish import request, VAULT

S = Path("/mnt/agents/output/.stash/ad16")
A21 = Path("/mnt/agents/output/.stash/ad21/run")
A23 = Path("/mnt/agents/output/.stash/ad23/run")
A24 = Path("/mnt/agents/output/.stash/ad24/run")
R = Path("/mnt/agents/output/.stash/ad25/run")
L = R.parent / "literature"
OUT = Path("/mnt/agents/output")
RECEIPTS = {"qlv-pub": "ad25_qlvpub_receipt.json", "vci-inbox": "ad25_vci_receipt.json", "ci-inbox": "ad25_ciinbox_receipt.json"}
sha = lambda b: hashlib.sha256(b).hexdigest()


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


def local_for(repo, target):
    if repo == "chepin-qi/qlv-pub":
        assert target == "outbox/qlv-outbox.json"
        return S / "hub_qlv_outbox.json"
    if repo == "chepin-ai/ci-inbox":
        if target.endswith("QRAC-D8-TOFFOLI-PLATEAU-08.md"):
            return S / "QRAC-D8-TOFFOLI-PLATEAU-08.md"
        return S / Path(target).name
    prefix = "lanes/qlv/outbox-pending/"
    if target.startswith(prefix):
        return source_for(target[len(prefix):])
    assert target == "lanes/qlv/outbox/qlv-outbox.json"
    return S / "hub_qlv_outbox.json"


def blob_bytes(repo, blob, token):
    doc = request("GET", f"/repos/{repo}/git/blobs/{blob}", token, attempts=3)
    assert doc.get("encoding") == "base64"
    return base64.b64decode(doc["content"])


def public_bytes(url):
    last = None
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "qlv-ad25-public-verify"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as exc:
            last = exc
            time.sleep(2)
    raise last


def main():
    out = {"beat": "AD-25", "checked_at": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()),
           "status": "ALL_PASS", "repos": {}, "public_main": {},
           "private_ci_consumption": 0, "quantum_machine_consumption": 0}
    cache = {}
    for key, fn in RECEIPTS.items():
        rec = json.loads((R / fn).read_text())
        repo = rec["repo"]
        token = (VAULT / ("qi_pat.txt" if repo.startswith("chepin-qi/") else "fed_pat.txt")).read_text().strip()
        head = request("GET", f"/repos/{repo}/git/ref/heads/main", token)["object"]["sha"]
        comparison = request("GET", f"/repos/{repo}/compare/{head}...{rec['commit']}", token, attempts=3)
        assert comparison.get("ahead_by") == 0, (repo, comparison.get("status"), comparison.get("ahead_by"), comparison.get("behind_by"))
        assert comparison.get("status") in ("identical", "behind"), (repo, comparison.get("status"))
        commit = request("GET", f"/repos/{repo}/git/commits/{rec['commit']}", token)
        assert rec["parent"] in [p["sha"] for p in commit["parents"]]
        total = 0
        for target, expected in rec["file_sha256"].items():
            raw = blob_bytes(repo, rec["blob_shas"][target], token)
            cache[(repo, target)] = raw
            assert sha(raw) == expected == sha(local_for(repo, target).read_bytes()), target
            total += len(raw)
        out["repos"][key] = {
            "repo": repo, "commit": rec["commit"], "current_main": head,
            "delivery_is_ancestor": True, "ahead_by": comparison["ahead_by"], "behind_by": comparison["behind_by"],
            "compare_status": comparison["status"], "files": len(rec["file_sha256"]),
            "bytes": total, "byte_verdict": "ALL_MATCH",
        }

    url = "https://raw.githubusercontent.com/chepin-qi/qlv-pub/main/outbox/qlv-outbox.json"
    expected = (S / "hub_qlv_outbox.json").read_bytes()
    raw = public_bytes(url + "?ad25=" + out["repos"]["qlv-pub"]["commit"])
    assert raw == expected
    hub = json.loads(raw)
    cap = json.loads((S / "capsule-251.json").read_text())
    assert hub["chain_head"]["seq"] == 251 and hub["chain_head"]["cid"] == cap["cid"]
    out["public_main"] = {"url": url, "bytes": len(raw), "sha256": sha(raw),
                          "byte_verdict": "ALL_MATCH", "seq": 251, "cid": hub["chain_head"]["cid"]}
    (R / "ad25_remote_verify.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    # 仅使用远端vci blob重建ad21/ad23/ad24/ad25 siblings，不复用本地分析中间件。
    rec = json.loads((R / "ad25_vci_receipt.json").read_text())
    repo = rec["repo"]
    prefix = "lanes/qlv/outbox-pending/"
    parent = S / f"rebuild_ad25_remote_{rec['commit'][:12]}_{out['checked_at']}"
    parent.mkdir(exist_ok=False)
    pkg = parent / "ad25"
    pkg.mkdir()
    count = 0
    for target in sorted(rec["file_sha256"]):
        if not target.startswith(prefix):
            continue
        rel = target[len(prefix):]
        dst = (parent / rel) if rel.startswith(("ad21/", "ad23/", "ad24/")) else (pkg / rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(cache[(repo, target)])
        count += 1
    original_raw = (pkg / "run/ad25_verify.json").read_bytes()
    original = json.loads(original_raw)
    proc = subprocess.run([sys.executable, str(pkg / "run/ad25_verify.py")], cwd=pkg / "run",
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900, check=False)
    stdout = proc.stdout
    (pkg / "rebuilt_verify_stdout.txt").write_bytes(stdout)
    assert proc.returncode == 0, (proc.returncode, stdout[-2000:].decode(errors="replace"))
    rebuilt_raw = (pkg / "run/ad25_verify.json").read_bytes()
    rebuilt = json.loads(rebuilt_raw)
    assert rebuilt_raw == original_raw, (sha(rebuilt_raw), sha(original_raw))
    assert rebuilt["status"] == "ALL_PASS"
    rebuild = {
        "beat": "AD-25", "status": "ALL_PASS", "source": "remote vci-inbox blobs only",
        "remote_commit": rec["commit"], "clean_parent": str(parent), "files_rebuilt": count,
        "process_returncode": proc.returncode, "original_verify_sha256": sha(original_raw),
        "rebuilt_verify_file_sha256": sha(rebuilt_raw), "verify_json_byte_identical": True,
        "stdout_sha256": sha(stdout), "status_checks_inputs_boundaries_equal": True,
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    (R / "ad25_rebuild_verify.json").write_text(json.dumps(rebuild, ensure_ascii=False, indent=2) + "\n")
    final = {
        "beat": "AD-25", "status": "ALL_PASS", "remote": out, "rebuild": rebuild,
        "capsule": {"seq": 251, "cid": cap["cid"], "prev": cap["prev"]},
        "manifest_files": len(json.loads((R / "ad25_MANIFEST.json").read_text())["files"]),
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw_final = json.dumps(final, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad25_final_verify.json").write_bytes(raw_final)
    (OUT / "AD-25_远端与重建终验.json").write_bytes(raw_final)

    repo_rows = "\n".join(
        f"| {key} | `{val['commit']}` | {val['ahead_by']} | {val['behind_by']} | {val['files']} | {val['byte_verdict']} |"
        for key, val in out["repos"].items())
    final_md = f'''
## 八、三仓发布与远端干净重建终验

终验时间：`{out['checked_at']}`；状态：**ALL_PASS**。

| 仓库 | 交付提交 | ahead_by | behind_by | 核验文件数 | 字节 verdict |
|---|---|---:|---:|---:|---|
{repo_rows}

- 三个交付提交均为各自当前远端main的祖先，`ahead_by=0`；`behind_by`只记录其他线后续推进，不作强推追赶。
- 公网 `chepin-qi/qlv-pub/main/outbox/qlv-outbox.json` 逐字节匹配，seq=`251`，cid=`{cap['cid']}`，SHA-256=`{out['public_main']['sha256']}`。
- 干净目录仅从远端vci-inbox blob重建`{count}`个文件，未复用本地分析中间件；总验收进程返回码0。
- 重建前后`ad25_verify.json`逐字节一致，SHA-256=`{sha(rebuilt_raw)}`。
- 终验汇总=`AD-25_远端与重建终验.json`，其SHA-256=`{sha(raw_final)}`；量子真机机时=0、私域CI=0。
'''
    report_path = OUT / "AD-25_饱和攻击与独立验收报告.md"
    report = report_path.read_text()
    assert "<!-- AD25_REMOTE_FINAL -->" in report
    report_path.write_text(report.replace("<!-- AD25_REMOTE_FINAL -->", final_md))
    print(json.dumps({"status": "ALL_PASS",
                      "repos": {k: {x: v[x] for x in ["commit", "current_main", "ahead_by", "behind_by", "files", "byte_verdict"]}
                                for k, v in out["repos"].items()},
                      "public_main": out["public_main"], "rebuild": rebuild,
                      "final_verify_sha256": sha(raw_final)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
