"""AD-26 RAC 差集复查：只记录元数据与布尔指纹；私有正文不回显；零机时、零CI。"""
import base64
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, "/mnt/agents/output/.stash/ad21/run")
from ad21_publish import request, VAULT

RUN = Path(__file__).resolve().parent
AD25 = RUN.parent.parent / "ad25/run/ad25_rac_check.json"
NUMERIC = re.compile(
    r"[\"']?S_sim[\"']?\s*[:=]\s*(?:[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?|0x[0-9a-fA-F]+)",
    re.I,
)
NAME = re.compile(r"RAC|LGT|〈RED〉", re.I)


def main():
    previous = json.loads(AD25.read_text())
    out = {
        "beat": "AD-26",
        "checked_at": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()),
        "previous_checked_at": previous["checked_at"],
        "repos": {},
        "fingerprint_arrived": False,
        "quantum_machine_actual_consumption_seconds": 0,
        "quantum_machine_launched": False,
        "quantum_account_quota_verified": False,
        "private_ci_consumption": 0,
    }
    for repo, old in previous["repos"].items():
        token = (VAULT / ("qi_pat.txt" if repo.startswith("chepin-qi/") else "fed_pat.txt")).read_text().strip()
        assert token
        head = request("GET", f"/repos/{repo}/git/ref/heads/main", token)["object"]["sha"]
        base = old["head"]
        comparison = request("GET", f"/repos/{repo}/compare/{base}...{head}", token)
        # compare 的文件列表在大差集上截断；递归树对拍覆盖全部增删改路径。
        base_tree = request("GET", f"/repos/{repo}/git/trees/{base}?recursive=1", token)
        head_tree = request("GET", f"/repos/{repo}/git/trees/{head}?recursive=1", token)
        assert not base_tree.get("truncated", False), (repo, "base recursive tree truncated")
        assert not head_tree.get("truncated", False), (repo, "head recursive tree truncated")
        base_blobs = {x["path"]: x["sha"] for x in base_tree.get("tree", []) if x.get("type") == "blob"}
        head_blobs = {x["path"]: x["sha"] for x in head_tree.get("tree", []) if x.get("type") == "blob"}
        paths = {}
        for name in sorted(set(base_blobs) | set(head_blobs)):
            if not NAME.search(name) or base_blobs.get(name) == head_blobs.get(name):
                continue
            status = "added" if name not in base_blobs else ("removed" if name not in head_blobs else "modified")
            paths[name] = status
        # AD-25 的 candidates 位于各 repo 下；保留旧候选以便跨拍持续复查。
        for item in old.get("candidates", []):
            paths.setdefault(item["path"], "recheck")
        candidates = []
        for name, status in sorted(paths.items()):
            item = {"path": name, "status": status, "has_numeric_S_sim": False, "queue_only": False}
            if status != "removed":
                doc = request("GET", f"/repos/{repo}/contents/{quote(name, safe='/')}?ref={head}", token)
                if doc.get("encoding") == "base64":
                    raw = base64.b64decode(doc["content"])
                    text = raw.decode(errors="replace")
                    source_code = Path(name).suffix.lower() in {".py", ".js", ".sh", ".ts"}
                    item["source_code_excluded_from_fingerprint"] = source_code
                    item["has_numeric_S_sim"] = bool(NUMERIC.search(text)) and not source_code
                    item["queue_only"] = Path(name).suffix.lower() in {".md", ".txt"} and "In Queue" in text and "returned_shots=0" in text
                    item["content_sha256"] = hashlib.sha256(raw).hexdigest()
                else:
                    item["read_status"] = "non_base64_content_not_claimed"
            out["fingerprint_arrived"] |= item["has_numeric_S_sim"]
            candidates.append(item)
        out["repos"][repo] = {
            "base": base, "head": head,
            "ahead_by": comparison.get("ahead_by"), "behind_by": comparison.get("behind_by"),
            "candidate_counts": len(candidates), "candidates": candidates,
        }
    out["verdict"] = "FINGERPRINT_CANDIDATE_REQUIRES_INDEPENDENT_REPLAY" if out["fingerprint_arrived"] else "WAITING_PEER_S_SIM"
    out["boundary"] = "仅复查对方数值指纹是否到件；源码队列字面量不充当指纹；QLV自身模拟S_sim不冒充跨线对拍；未触发任何真机或私域CI。"
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (RUN / "ad26_rac_check.json").write_bytes(raw)
    print(json.dumps({
        "checked_at": out["checked_at"], "verdict": out["verdict"],
        "fingerprint_arrived": out["fingerprint_arrived"],
        "heads": {k: v["head"] for k, v in out["repos"].items()},
        "candidate_counts": {k: v["candidate_counts"] for k, v in out["repos"].items()},
        "quantum_machine_actual_consumption_seconds": 0,
        "quantum_machine_launched": False,
        "quantum_account_quota_verified": False,
        "private_ci_consumption": 0,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
