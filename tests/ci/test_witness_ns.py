# CLASSIFY: L1
"""test_witness_ns.py · WS-43 NS 见证（EXT-WAVE-09）生成/核验测试（fail-closed / 默认拒绝律）

五组判定语义测试（沿用 tests/ci/test_witness.py 的 WS-37 M0 范式）：
  1. 真见证全过（3 件：W-NS1 能量相消 / W-NS2 采样能量界 / W-NS3 阻塞登记，独立复算）；
  2. 扰动必拒（篡改包络宽度/输入坐标/采样点/界登记/负控谎报，重签哈希后仍必拒——复算分歧）；
  3. schema 高 major / 不可解析 / 缺省拒收；
  4. 缺字段 / 非 null lean_binding / 缺诚实边界拒收；
  5. W-NS3 阻塞登记口径：certified=true 或携带包络数值必拒；manifest 与见证哈希一致。

运行：python3 -m unittest tests.ci.test_witness_ns -v   （或 pytest 直接收集）
"""
import glob
import json
import os
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, "ci"))

import witness_ns_verify  # noqa: E402

WITNESS_DIR = os.path.join(REPO_ROOT, "artifacts", "witnesses-ns")
ALL_WITNESSES = sorted(glob.glob(os.path.join(WITNESS_DIR, "*.witness.json")))
NS1 = [p for p in ALL_WITNESSES if "ns-energy-cancellation" in os.path.basename(p)]
NS2 = [p for p in ALL_WITNESSES if "ns-galerkin-energy-bound" in os.path.basename(p)]
NS3 = [p for p in ALL_WITNESSES if "ns-trajectory-envelope-blocked" in os.path.basename(p)]
MANIFEST = os.path.join(WITNESS_DIR, "manifest.json")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _resign(w):
    w["witness_sha256"] = witness_ns_verify._canon_sha256(w)
    return w


class TestCorpusPresent(unittest.TestCase):
    def test_corpus_present(self):
        self.assertEqual(len(NS1), 1, "W-NS1 缺失")
        self.assertEqual(len(NS2), 1, "W-NS2 缺失")
        self.assertEqual(len(NS3), 1, "W-NS3 缺失")
        self.assertTrue(os.path.isfile(MANIFEST), "manifest.json 缺失")
        self.assertTrue(os.path.isfile(os.path.join(WITNESS_DIR, "run-log.json")), "run-log 缺失")

    def test_manifest_consistent(self):
        m = _load(MANIFEST)
        self.assertEqual(len(m["witnesses"]), 3)
        for entry in m["witnesses"]:
            w = _load(os.path.join(WITNESS_DIR, entry["file"]))
            self.assertEqual(w["witness_sha256"], entry["sha256"], entry["witness_id"])
            self.assertEqual(w["witness_id"], entry["witness_id"])
        self.assertEqual(m["counts"]["ns1_cases"], 288)
        self.assertEqual(m["counts"]["ns2_cases"], 56)
        self.assertEqual(m["counts"]["ns2_samples_total"], 56 * 65)
        self.assertEqual(len(m["blocked"]), 1)
        self.assertEqual(m["blocked"][0]["code"], "B1")
        self.assertIn("RadiiPolynomial", m["blocked"][0]["statement"])


class TestRealWitnessesPass(unittest.TestCase):
    """正例：三件真见证独立复算全部通过。"""

    def test_all_real_witnesses_pass(self):
        self.assertEqual(len(ALL_WITNESSES), 3)
        for path in ALL_WITNESSES:
            with self.subTest(witness=os.path.basename(path)):
                v = witness_ns_verify.verify_witness(path)
                self.assertTrue(v["ok"], json.dumps(
                    [c for c in v["checks"] if not c["ok"]], ensure_ascii=False, indent=1))


class _TamperBase(unittest.TestCase):
    def verify_tampered(self, w):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "tampered.witness.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(w, fh, ensure_ascii=False, indent=2)
            return witness_ns_verify.verify_witness(p)

    def assertCheckFailed(self, v, name):
        self.assertFalse(v["ok"], f"{name} 未触发但整体须拒")
        self.assertTrue(any(c["check"] == name and not c["ok"] for c in v["checks"]),
                        f"期望 {name} 失败; got: {[(c['check'], c['ok']) for c in v['checks'] if not c['ok']]}")


class TestTamperedNS1Rejected(_TamperBase):
    """W-NS1 负向：扰动包络宽度/输入坐标/负控登记，重签后复算仍必拒。"""

    def test_tampered_ns1_max_width_rejected(self):
        w = _load(NS1[0])
        w["verdict"]["metrics"]["max_width"] = "1e-60"  # 谎报更窄包络
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "metric_max_width")

    def test_tampered_ns1_input_coordinate_rejected(self):
        w = _load(NS1[0])
        c0 = w["inputs"]["cases"][0]
        c0["u"][0] = repr(float(c0["u"][0]) + 1e-6)  # 微扰输入坐标
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "recompute_all_contain_zero")

    def test_tampered_ns1_neg_verdict_lie_rejected(self):
        w = _load(NS1[0])
        w["negative_control"]["neg_verdict"]["neg_rejected"] = False  # 谎报负控未拒
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "neg_registered_true")


class TestTamperedNS2Rejected(_TamperBase):
    """W-NS2 负向：扰动采样点/界登记/负控登记，重签后复算仍必拒。"""

    def test_tampered_ns2_sample_rejected(self):
        w = _load(NS2[0])
        c0 = w["inputs"]["cases"][0]
        c0["x"][1][0] = repr(float(c0["x"][1][0]) + 1e-3)  # 篡改一个采样点坐标
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "candidate_consistency")

    def test_tampered_ns2_bound_rejected(self):
        w = _load(NS2[0])
        c0 = w["inputs"]["cases"][0]
        c0["bound_hi"] = repr(float(c0["bound_hi"]) / 2)  # 压低登记界
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "recompute_all_within_bound")

    def test_tampered_ns2_neg_verdict_lie_rejected(self):
        w = _load(NS2[0])
        w["negative_control"]["neg_verdict"]["neg_rejected"] = False
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "neg_registered_true")

    def test_tampered_ns2_max_defect_rejected(self):
        w = _load(NS2[0])
        w["verdict"]["metrics"]["max_defect"] = "-1.0"  # 谎报裕度
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "metric_max_defect")


class TestTamperedNS3Rejected(_TamperBase):
    """W-NS3 阻塞登记口径：任何认证/包络宣称必拒。"""

    def test_ns3_certified_claim_rejected(self):
        w = _load(NS3[0])
        w["verdict"]["certified"] = True  # 阻塞登记严禁宣称认证通过
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "verdict_not_certified")

    def test_ns3_envelope_claim_rejected(self):
        w = _load(NS3[0])
        w["bounds"]["envelope"] = {"radius": "1e-6"}  # 禁止携带包络数值
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "no_envelope_claimed")

    def test_ns3_blocked_code_tamper_rejected(self):
        w = _load(NS3[0])
        w["blocked"]["code"] = "B0"
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "blocked_code_B1")


class TestSchemaAndFieldsRejected(_TamperBase):
    """格式层 fail-closed：schema/必填字段/lean_binding/诚实边界。"""

    def test_hash_tamper_without_resign_rejected(self):
        w = _load(NS1[0])
        w["verdict"]["metrics"]["max_width"] = "0.0"  # 篡改且不重签 → 哈希失配必拒
        v = self.verify_tampered(w)
        self.assertCheckFailed(v, "witness_sha256")

    def test_higher_major_schema_rejected(self):
        w = _load(NS1[0])
        w["schema_version"] = "2.0"
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "schema_major_dispatch")
        detail = [c["detail"] for c in v["checks"] if c["check"] == "schema_major_dispatch"][0]
        self.assertIn("unsupported_schema", detail)

    def test_unparseable_schema_rejected(self):
        w = _load(NS2[0])
        w["schema_version"] = "v1"
        v = self.verify_tampered(_resign(w))
        self.assertFalse(v["ok"])
        self.assertTrue(any(c["check"] == "schema_parse" and not c["ok"] for c in v["checks"]))

    def test_missing_schema_version_rejected(self):
        w = _load(NS1[0])
        del w["schema_version"]
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "schema_version_present")

    def test_missing_negative_control_rejected(self):
        w = _load(NS2[0])
        del w["negative_control"]
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "required_top_fields")

    def test_nonnull_lean_binding_rejected(self):
        w = _load(NS3[0])
        w["lean_binding"] = {"status": "checked"}  # C3：禁止任何 Lean 通过性声明
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "lean_binding_null")

    def test_missing_honesty_boundary_rejected(self):
        w = _load(NS2[0])
        del w["honesty_boundary"]  # W-NS2 必须携带「非轨道包络」披露
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "honesty_boundary_present")


if __name__ == "__main__":
    unittest.main()
