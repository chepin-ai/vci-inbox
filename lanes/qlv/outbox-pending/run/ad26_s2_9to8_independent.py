"""AD-26 S^2 9->8 独立重建：不导入构造器、删门器或求解器。"""
import hashlib
import json
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
THETA, PHI = np.pi/7, 0.31
ALPHA = np.pi/8


def bits(x):
    return [(x>>2)&1, (x>>1)&1, x&1]


def rz(a):
    return np.diag([np.exp(-0.5j*a), np.exp(0.5j*a)])


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], complex)


def su2(t):
    return rz(t[0])@ry(t[1])@rz(t[2])


def cz(edge):
    return np.diag([-1 if bits(x)[edge[0]] and bits(x)[edge[1]] else 1 for x in range(8)]).astype(complex)


def circuit(p, edges):
    p = np.asarray(p, float)
    th = p[1:].reshape(len(edges)+1, 3, 3)
    u = np.exp(1j*p[0])*np.kron(np.kron(su2(th[-1, 0]), su2(th[-1, 1])), su2(th[-1, 2]))
    for j in range(len(edges)-1, -1, -1):
        local = np.kron(np.kron(su2(th[j, 0]), su2(th[j, 1])), su2(th[j, 2]))
        u = u@cz(edges[j])@local
    return u


def raw_indices(edges):
    ans = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            ans += [1+(i*3+q)*3+1, 1+(i*3+q)*3+2]
    ans += list(range(1+9*len(edges), 1+9*(len(edges)+1)))
    assert len(ans) == 4*len(edges)+10
    return ans


def expand(core, edges):
    p = np.zeros(1+9*(len(edges)+1))
    p[raw_indices(edges)] = core
    return p


def pm(name):
    return np.kron(np.kron(PAULI[name[0]], PAULI[name[1]]), PAULI[name[2]])


def toffoli(controls, target):
    m = np.zeros((8, 8), complex)
    for x in range(8):
        b = bits(x)
        if all(b[q] for q in controls):
            b[target] ^= 1
        m[(b[0]<<2)|(b[1]<<1)|b[2], x] = 1
    return m


def target(theta, phi):
    u = (1+np.cos(theta))/2
    v = (np.cos(theta)-1)/2
    w = np.sin(theta)*np.cos(phi)/2
    t = np.sin(theta)*np.sin(phi)/2
    h = u*pm("ZXZ")+v*pm("ZIZ")+w*(pm("YIZ")+pm("YXZ"))+t*(pm("XIZ")+pm("XXZ"))
    return (np.cos(ALPHA)*np.eye(8)+1j*np.sin(ALPHA)*h)@toffoli({0, 2}, 1)


def main():
    T = target(THETA, PHI)
    sources = {}
    for stem in ("89", "010"):
        src = json.loads((R/f"ad26_s2_raw9_{stem}.json").read_text())
        p = np.asarray(src["x_raw"], float)
        edges = [tuple(e) for e in src["edges"]]
        e = float(np.max(abs(circuit(p, edges)-T)))
        assert e < 2e-12
        bad = p.copy()
        bad[2] += np.pi/4
        bad_e = float(np.max(abs(circuit(bad, edges)-T)))
        assert bad_e > 1e-3
        sources[stem] = {"source_9cz_max_abs": e, "changed_angle_counterexample_max_abs": bad_e}
    rows = [json.loads(s) for s in (R/"ad26_s2_9to8.jsonl").read_text().splitlines() if s.strip()]
    assert len(rows) == 36
    per = {}
    max_delta = 0.0
    for r in rows:
        assert "error" not in r
        edges = [tuple(e) for e in r["edges"]]
        assert len(edges) == 8
        p = expand(r["x_core"], edges)
        e = float(np.max(abs(circuit(p, edges)-T)))
        max_delta = max(max_delta, abs(e-r["target_max_abs"]))
        assert abs(e-r["target_max_abs"]) < 2e-9
        per.setdefault(r["topology"], []).append((r["deleted"], r["kick"], e))
    summary = {}
    for stem, vv in per.items():
        assert len(vv) == 18
        best = min(vv, key=lambda x: x[2])
        summary[stem] = {"runs": len(vv), "exact_numeric_hits": sum(e < 1e-9 for _, _, e in vv),
                         "best": {"deleted": best[0], "kick": best[1], "target_max_abs": best[2]}}
    out = {"beat": "AD-26", "status": "S2_TWO_9CZ_TO8_INDEPENDENT_REBUILD_PASS",
           "source_known_answer_gate_first": sources, "theta": THETA, "phi": PHI,
           "runs": len(rows), "per_topology": summary,
           "exact_numeric_hits": sum(v["exact_numeric_hits"] for v in summary.values()),
           "max_target_rebuild_difference": max_delta,
           "evidence_level": "L2 independent numerical rebuild of saved 8-CZ circuits",
           "boundary": "仅验收36条保存电路及两个原始9-CZ已知源；零命中不证明8-CZ不存在，任何数值命中也仍需全参数证书。",
           "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/"ad26_s2_9to8_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows),
                      "exact_numeric_hits": out["exact_numeric_hits"],
                      "per_topology": summary, "max_target_rebuild_difference": max_delta,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
