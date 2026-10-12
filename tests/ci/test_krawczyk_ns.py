# CLASSIFY: L1
"""test_krawczyk_ns.py · WS-55「Krawczyk×Galerkin」证书（EXT-WAVE-10「融」）测试
（fail-closed / 默认拒绝律）

判定语义测试组（沿用 tests/ci/test_witness_ns.py 的 WS-43 范式）：
  1. 语料在场（4 证书 + manifest + run-log）与 manifest 一致性；
  2. 真证书全过（3 PASS + 1 诚实 FAIL 登记，验证器独立复算）；
  3. 解析解 sanity：B₃ 稳态全局唯一解析根 u2=f2/(νa2)、u0=(2u2f1/(νa1)+f0)/(4u2²/(νa1)+νa0)、
     u1=(f1−2u0u2)/(νa1)（Fraction 精确算），须落入各 PASS 证书认证盒内；
     P1 组解析根为精确有理 (3/5, 4/5, −1/4) 且 F=0 精确成立；
  4. 篡改必拒（重签哈希后仍必拒——复算分歧）：半径缩/扩、Y 扰动、外力翻号、
     候选移位（盒外）、参数非法（a₀<0）；
  5. schema 高 major / 缺字段 / 哈希未重签必拒；
  6. FAIL 证书语义：伪装 PASS（null box）必拒；盒外候选的存在性语义复算必假。

运行：python3 -m unittest tests.ci.test_krawczyk_ns -v   （或 pytest 直接收集）
"""
import glob
import json
import os
import tempfile
import unittest
from fractions import Fraction

import sys
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, "ci"))

import krawczyk_ns_verify  # noqa: E402

CERT_DIR = os.path.join(REPO_ROOT, "artifacts", "witnesses-cap")
ALL_CERTS = sorted(glob.glob(os.path.join(CERT_DIR, "*.cap.json")))
MANIFEST = os.path.join(CERT_DIR, "manifest.json")
RUNLOG = os.path.join(CERT_DIR, "run-log.json")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _resign(w):
    w["cert_sha256"] = krawczyk_ns_verify._canon_sha256(w)
    return w


def _verify_obj(w):
    """把（篡改后的）证书对象写入临时文件并跑验证器；返回 verdict dict。"""
    with tempfile.NamedTemporaryFile("w", suffix=".cap.json", delete=False,
                                     encoding="utf-8") as fh:
        json.dump(w, fh, ensure_ascii=False)
        tmp = fh.name
    try:
        return krawczyk_ns_verify.verify_cert(tmp)
    finally:
        os.unlink(tmp)


def _analytic_root(params):
    """B₃ 稳态的解析根（全局唯一；Fraction 精确）。"""
    nu = Fraction(params["nu"])
    a = [Fraction(s) for s in params["a"]]
    f = [Fraction(s) for s in params["f"]]
    u2 = f[2] / (nu * a[2])
    u0 = (2 * u2 * f[1] / (nu * a[1]) + f[0]) / (4 * u2 * u2 / (nu * a[1]) + nu * a[0])
    u1 = (f[1] - 2 * u0 * u2) / (nu * a[1])
    return [u0, u1, u2]


def _F_exact(params, u):
    nu = Fraction(params["nu"])
    a = [Fraction(s) for s in params["a"]]
    f = [Fraction(s) for s in params["f"]]
    u0, u1, u2 = u
    return [2 * u1 * u2 - nu * a[0] * u0 + f[0],
            -2 * u0 * u2 - nu * a[1] * u1 + f[1],
            -nu * a[2] * u2 + f[2]]


def _pass_certs():
    return [p for p in ALL_CERTS if _load(p)["verdict"]["status"] == "PASS"]


def _fail_certs():
    return [p for p in ALL_CERTS if _load(p)["verdict"]["status"] == "FAIL"]


class TestCorpusPresent(unittest.TestCase):
    def test_corpus_present(self):
        self.assertEqual(len(ALL_CERTS), 4, "证书须恰为 4 件")
        self.assertTrue(os.path.isfile(MANIFEST), "manifest.json 缺失")
        self.assertTrue(os.path.isfile(RUNLOG), "run-log.json 缺失")

    def test_manifest_consistent(self):
        m = _load(MANIFEST)
        self.assertEqual(len(m["certificates"]), 4)
        for entry in m["certificates"]:
            w = _load(os.path.join(CERT_DIR, entry["file"]))
            self.assertEqual(w["cert_sha256"], entry["sha256"], entry["case_id"])
            self.assertEqual(w["case_id"], entry["case_id"])
            self.assertEqual(w["verdict"]["status"], entry["status"])
        self.assertEqual(m["counts"]["pass"], 3)
        self.assertEqual(m["counts"]["fail"], 1)


class TestGenuineCertsPass(unittest.TestCase):
    def test_all_certs_verify(self):
        for p in ALL_CERTS:
            v = krawczyk_ns_verify.verify_cert(p)
            bad = [c for c in v["checks"] if not c["ok"]]
            self.assertTrue(v["ok"], f"{p} 拒验: {bad[:3]}")

    def test_runlog_counts(self):
        rl = _load(RUNLOG)
        self.assertEqual(rl["counts"]["cases"], 4)
        self.assertEqual(rl["counts"]["pass"], 3)
        self.assertIn("passed", rl["consistency_gate"])


class TestAnalyticSanity(unittest.TestCase):
    def test_p1_exact_rational_root(self):
        """P1（ν=1, A=I, f=(1,1/2,−1/4)）解析根恰为 (3/5, 4/5, −1/4)，F=0 精确。"""
        p1 = next(_load(p) for p in ALL_CERTS if "p1" in p)
        root = _analytic_root(p1["params"])
        self.assertEqual(root, [Fraction(3, 5), Fraction(4, 5), Fraction(-1, 4)])
        self.assertEqual(_F_exact(p1["params"], root), [Fraction(0)] * 3)

    def test_analytic_root_inside_certified_box(self):
        """各 PASS 组：解析根（Fraction 精确）逐分量落入认证盒 [z−r, z+r]。"""
        for p in _pass_certs():
            w = _load(p)
            root = _analytic_root(w["params"])
            z = [Fraction(s) for s in w["box"]["center"]]
            r = Fraction(w["box"]["radius"])
            for i in range(3):
                self.assertLessEqual(abs(root[i] - z[i]), r,
                                     f"{w['case_id']} 分量 {i} 出盒")

    def test_analytic_root_unique_globally(self):
        """解析推导的分母 4u2²/(νa1)+νa0 > 0 ⟹ 稳态全局唯一（公式层 sanity）。"""
        for p in ALL_CERTS:
            w = _load(p)
            nu = Fraction(w["params"]["nu"])
            a = [Fraction(s) for s in w["params"]["a"]]
            f = [Fraction(s) for s in w["params"]["f"]]
            u2 = f[2] / (nu * a[2])
            self.assertGreater(4 * u2 * u2 / (nu * a[1]) + nu * a[0], 0)


class TestTamperRejected(unittest.TestCase):
    """篡改后即使重签 cert_sha256 也必须拒验（独立复算分歧）。"""

    def _mutant(self, mutate):
        w = _load(_pass_certs()[0])
        mutate(w)
        return _verify_obj(_resign(w))

    def test_radius_shrunk_rejected(self):
        def m(w):
            w["box"]["radius"] = str(float(Fraction(w["box"]["radius"])) / 4.0)
        v = self._mutant(m)
        self.assertFalse(v["ok"])

    def test_radius_enlarged_rejected(self):
        def m(w):
            w["box"]["radius"] = repr(float(Fraction(w["box"]["radius"])) * 1.5)
        v = self._mutant(m)
        self.assertFalse(v["ok"])

    def test_perturbed_preconditioner_rejected(self):
        def m(w):
            y00 = float(Fraction(w["preconditioner"]["Y"][0][0]))
            w["preconditioner"]["Y"][0][0] = repr(y00 * (1 + 1e-9))
        v = self._mutant(m)
        self.assertFalse(v["ok"])

    def test_flipped_forcing_rejected(self):
        def m(w):
            w["params"]["f"][0] = str(-Fraction(w["params"]["f"][0]))
        v = self._mutant(m)
        self.assertFalse(v["ok"])

    def test_shifted_candidate_rejected(self):
        """盒外拒绝：候选移位 3r（离开原认证盒）后登记数据与复算必然分歧。"""
        def m(w):
            r = float(Fraction(w["box"]["radius"]))
            z0 = float(Fraction(w["candidate"]["z"][0]))
            w["candidate"]["z"][0] = repr(z0 + 3 * r)
            w["box"]["center"] = w["candidate"]["z"]
        v = self._mutant(m)
        self.assertFalse(v["ok"])

    def test_inadmissible_params_rejected(self):
        def m(w):
            w["params"]["a"][0] = "-1"  # a₀>0 被破坏
        v = self._mutant(m)
        self.assertFalse(v["ok"])


class TestSchemaAndShape(unittest.TestCase):
    def test_missing_field_rejected(self):
        w = _load(_pass_certs()[0])
        del w["krawczyk"]
        v = _verify_obj(_resign(w))
        self.assertFalse(v["ok"])

    def test_schema_major_rejected(self):
        w = _load(_pass_certs()[0])
        w["schema_version"] = "2.0"
        v = _verify_obj(_resign(w))
        self.assertFalse(v["ok"])

    def test_schema_unparsable_rejected(self):
        w = _load(_pass_certs()[0])
        w["schema_version"] = "banana"
        v = _verify_obj(_resign(w))
        self.assertFalse(v["ok"])

    def test_unresigned_hash_rejected(self):
        """篡改但不重签：cert_sha256 复算不符必拒。"""
        w = _load(_pass_certs()[0])
        w["note"] = "tampered"
        v = _verify_obj(w)  # 不重签
        self.assertFalse(v["ok"])


class TestFailCertSemantics(unittest.TestCase):
    def test_fail_cert_present_and_verifies(self):
        self.assertEqual(len(_fail_certs()), 1, "诚实失败登记须恰 1 件")
        v = krawczyk_ns_verify.verify_cert(_fail_certs()[0])
        self.assertTrue(v["ok"])

    def test_fail_disguised_as_pass_rejected(self):
        """FAIL 证书伪装 PASS（box/krawczyk 为 null）必拒。"""
        w = _load(_fail_certs()[0])
        w["verdict"] = {"existence": True, "uniqueness": True, "status": "PASS"}
        v = _verify_obj(_resign(w))
        self.assertFalse(v["ok"])

    def test_offbox_candidate_existence_false(self):
        """盒外拒绝（语义级）：PASS 组候选移位 10r 后独立复算存在性条件必假。"""
        w = _load(_pass_certs()[0])
        r = float(Fraction(w["box"]["radius"]))
        z = [float(Fraction(s)) for s in w["candidate"]["z"]]
        z[0] += 10 * r
        rec = krawczyk_ns_verify._krawczyk_recompute(
            w["params"], [repr(v0) for v0 in z],
            w["preconditioner"]["Y"], w["box"]["radius"])
        self.assertFalse(rec["exists"], "移位 10r 后 K⊂int(U) 必须为假")

    def test_pass_certs_conditions_semantic(self):
        """PASS 组语义级复核：min_margin>0 且 ρ_hi<1（浮点读取登记值）。"""
        for p in _pass_certs():
            w = _load(p)
            self.assertGreater(float(w["krawczyk"]["min_margin"]), 0.0)
            self.assertLess(float(w["krawczyk"]["rho_hi"]), 1.0)


if __name__ == "__main__":
    unittest.main()
