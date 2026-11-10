"""AD-23 删门原始账独立复验：不导入求解器、规范器或 AD-22 验收器。"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parent
I8 = np.eye(8, dtype=complex)


def permutation_gate(controls, target):
    """在计算基上独立构造 Toffoli；controls 为集合，target 为整数。"""
    out = np.zeros((8, 8), dtype=complex)
    for column in range(8):
        bits = [(column >> 2) & 1, (column >> 1) & 1, column & 1]
        if all(bits[q] for q in controls):
            bits[target] = 1 - bits[target]
        row = 4 * bits[0] + 2 * bits[1] + bits[2]
        out[row, column] = 1.0
    return out


def cnot(control, target):
    out = np.zeros((8, 8), dtype=complex)
    for column in range(8):
        bits = [(column >> 2) & 1, (column >> 1) & 1, column & 1]
        if bits[control]:
            bits[target] = 1 - bits[target]
        row = 4 * bits[0] + 2 * bits[1] + bits[2]
        out[row, column] = 1.0
    return out


MAJ = permutation_gate({0, 2}, 1) @ cnot(1, 2) @ cnot(1, 0)


def su2(a, b, c):
    ca, sa = np.cos(a / 2), np.sin(a / 2)
    cb, sb = np.cos(b / 2), np.sin(b / 2)
    # 直接展开 Rz(a) Ry(b) Rz(c)，避免调用任何分析模块。
    return np.array([
        [np.exp(-0.5j * (a + c)) * cb, -np.exp(-0.5j * (a - c)) * sb],
        [np.exp(0.5j * (a - c)) * sb, np.exp(0.5j * (a + c)) * cb],
    ], dtype=complex)


def full_cz(a, b):
    diag = np.ones(8, dtype=complex)
    for basis in range(8):
        if ((basis >> (2 - a)) & 1) and ((basis >> (2 - b)) & 1):
            diag[basis] = -1
    return np.diag(diag)


def canonical_raw_coordinates(core, edges):
    k = len(edges)
    core = np.asarray(core, dtype=float)
    assert core.shape == (4 * k + 10,)
    p = np.zeros(1 + 9 * (k + 1), dtype=float)
    cursor = 0
    p[0] = core[cursor]
    cursor += 1
    for layer_index in range(k):
        a, b = edges[layer_index]
        for q in (a, b):
            offset = 1 + 9 * layer_index + 3 * q
            p[offset + 1:offset + 3] = core[cursor:cursor + 2]
            cursor += 2
    p[1 + 9 * k:] = core[cursor:]
    assert cursor + 9 == len(core)
    return p


def rebuild(core, edges):
    p = canonical_raw_coordinates(core, edges)
    k = len(edges)
    angles = p[1:].reshape(k + 1, 3, 3)
    layers = []
    for triple in angles:
        layers.append(np.kron(np.kron(su2(*triple[0]), su2(*triple[1])), su2(*triple[2])))
    # 从最右因子开始连乘，明确保持 L0, CZ0, L1, ... 的作用次序。
    u = np.exp(1j * p[0]) * layers[-1]
    for j in range(k - 1, -1, -1):
        u = u @ full_cz(*edges[j]) @ layers[j]
    return u


def source_core(hit):
    edges = [tuple(e) for e in hit["edges"]]
    k = len(edges)
    raw = np.concatenate(([hit["phase_pi_over_8"] * np.pi / 8],
                          np.asarray(hit["local_angles_pi_over_4"], dtype=float).ravel() * np.pi / 4))
    keep = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            keep.extend([1 + 9 * i + 3 * q + 1, 1 + 9 * i + 3 * q + 2])
    keep.extend(range(1 + 9 * k, 1 + 9 * (k + 1)))
    assert len(keep) == 4 * k + 10
    return raw[keep], edges


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    raw_path = RUN / "ad23_lower.jsonl"
    raw_bytes = raw_path.read_bytes()
    assert b"\x00" not in raw_bytes
    rows = [json.loads(line) for line in raw_bytes.decode("utf-8").splitlines()]
    certificate = json.loads((RUN / "ad23_maj_7cz_exact.json").read_text())
    sources = certificate["hits"]
    assert len(rows) == 784 and len(sources) == 7

    # 已知答案门：七个严格构造在独立浮点重建中仍应为机器零；错误目标必须被拒绝。
    known = []
    wrong_control = []
    for hit in sources:
        core, edges = source_core(hit)
        known.append(float(np.max(np.abs(rebuild(core, edges) - MAJ))))
        wrong_control.append(float(np.max(np.abs(rebuild(core, edges) - I8))))
    assert max(known) < 2e-12, max(known)
    assert min(wrong_control) > 0.5, min(wrong_control)

    expected_tasks = set(itertools.product(range(7), range(7), range(16)))
    actual_tasks = {(r["source_idx"], r["delete"], r["restart"]) for r in rows}
    assert actual_tasks == expected_tasks and len(actual_tasks) == len(rows)

    independent = []
    max_delta = 0.0
    max_abs_coordinate = 0.0
    worst_delta_task = None
    for ordinal, row in enumerate(rows):
        assert "error" not in row, (ordinal, row)
        s, delete, restart = row["source_idx"], row["delete"], row["restart"]
        hit = sources[s]
        original_edges = [tuple(e) for e in hit["edges"]]
        expected_edges = original_edges[:delete] + original_edges[delete + 1:]
        assert [tuple(e) for e in row["edges"]] == expected_edges
        assert row["source_seq_idx"] == hit["idx"] and row["source_restart"] == hit["restart"]
        assert len(row["x_core"]) == 34 and np.all(np.isfinite(row["x_core"]))
        e = float(np.max(np.abs(rebuild(row["x_core"], expected_edges) - MAJ)))
        delta = abs(e - row["e"])
        # 部分未约化角达 1e6 量级；直接展开与原 su2 矩阵乘法的 libm 求值次序不同。
        # 记录一致性阈远低于命中阈，命中判定只使用本次独立 e，不使用记录 e。
        assert delta < 1e-9, (ordinal, e, row["e"], delta)
        if delta > max_delta:
            max_delta = delta
            worst_delta_task = [s, delete, restart]
        max_abs_coordinate = max(max_abs_coordinate, float(np.max(np.abs(row["x_core"]))))
        independent.append((e, s, delete, restart, row["nfev"], row["status"]))

    hits = [r for r in independent if r[0] < 1e-9]
    best = min(independent)
    summary = json.loads((RUN / "ad23_lower_summary.json").read_text())
    assert summary["runs"] == len(rows) and summary["errors"] == 0
    assert len(hits) == summary["exact_e_lt_1e-9"] == 0
    assert abs(best[0] - summary["best"]["e"]) < 1e-9
    assert best[1:4] == (summary["best"]["source_idx"], summary["best"]["delete"], summary["best"]["restart"])

    report = {
        "beat": "AD-23",
        "status": "INDEPENDENT_LOWER_PASS",
        "method": "raw JSONL -> independent canonical expansion -> independent 8x8 circuit and basis-permutation MAJ",
        "known_answer_gate": {
            "exact_7cz_sources": len(known),
            "max_exact_source_e": max(known),
            "min_wrong_identity_target_e": min(wrong_control),
        },
        "runs": len(rows),
        "unique_tasks": len(actual_tasks),
        "errors": 0,
        "core_coordinates_per_run": 34,
        "max_recorded_e_delta": max_delta,
        "worst_delta_task_source_delete_restart": worst_delta_task,
        "max_abs_unreduced_coordinate": max_abs_coordinate,
        "record_delta_bound": 1e-9,
        "independent_exact_e_lt_1e-9": len(hits),
        "independent_best": {
            "e": best[0], "source_idx": best[1], "delete": best[2],
            "restart": best[3], "nfev": best[4], "optimizer_status_not_a_proof": best[5],
        },
        "strict_interval_unchanged": "4 <= k <= 7",
        "boundary": "784 次独立复核的零命中仅为本采样协议下的 L2 数值否证，不是 k=6 不存在的证明。",
        "input_sha256": sha256(raw_path),
        "summary_sha256": sha256(RUN / "ad23_lower_summary.json"),
        "private_ci_consumption": 0,
        "quantum_machine_consumption": 0,
    }
    (RUN / "ad23_lower_verify.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
