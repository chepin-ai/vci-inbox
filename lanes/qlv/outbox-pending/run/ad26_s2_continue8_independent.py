"""AD-26 S^2 8-CZ 二维网格独立重建。"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ad26_s2_9to8_independent as ind

R = Path(__file__).resolve().parent
STEMS = ("89d2", "89d7", "010d1")


def main():
    per = {}
    max_delta = 0.0
    total = 0
    for stem in STEMS:
        summary = json.loads((R/f"ad26_s2_continue8_{stem}_summary.json").read_text())
        rows = [json.loads(s) for s in (R/f"ad26_s2_continue8_{stem}.jsonl").read_text().splitlines() if s.strip()]
        assert len(rows) == 25
        errors = []
        for r in rows:
            e = float(np.max(abs(ind.circuit(r["x_raw"], summary["edges"])-ind.target(r["theta"], r["phi"]))))
            max_delta = max(max_delta, abs(e-r["target_max_abs"]))
            assert abs(e-r["target_max_abs"]) < 2e-9
            errors.append(e)
        hits = sum(e < 1e-9 for e in errors)
        assert hits == summary["exact_numeric_hits"]
        worst = max(errors)
        assert abs(worst-summary["worst"]["target_max_abs"]) < 2e-9
        per[stem] = {"grid_points": len(rows), "exact_numeric_hits": hits,
                     "worst_max_abs": worst, "edges": summary["edges"]}
        total += len(rows)
    out = {"beat": "AD-26", "status": "S2_8CZ_GRID_INDEPENDENT_REBUILD_PASS",
           "grid_points": total, "per_topology": per,
           "exact_numeric_hits": sum(x["exact_numeric_hits"] for x in per.values()),
           "max_target_rebuild_difference": max_delta,
           "evidence_level": "L2 independent full-matrix rebuild on three finite 5x5 grids",
           "boundary": "75点命中不是全S^2符号恒等式，也不证明8-CZ最优。",
           "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/"ad26_s2_continue8_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "grid_points": total,
                      "exact_numeric_hits": out["exact_numeric_hits"],
                      "max_target_rebuild_difference": max_delta,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
