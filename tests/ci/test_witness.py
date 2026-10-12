# CLASSIFY: L1
"""test_witness.py · M0 见证生成/核验测试（规格 board/CIRC-REWORK-M0-SPEC-01.md §3 AC1–AC4）

四组判定语义测试（fail-closed / 默认拒绝律）：
  1. 真见证全过（11 件：circulant 六例 + auction 五例，独立复算）；
  2. 扰动界必拒（篡改区间界/负控登记，重签哈希后仍必拒——复算分歧，非仅哈希失配）；
  3. schema 高 major 拒收（unsupported_schema，禁止静默降级）；
  4. 缺字段拒收（缺 negative_control / 缺 schema_version / 缺 honesty_boundary 等）。

运行：python3 -m unittest tests.ci.test_witness -v   （或 python3 -m pytest tests/ci/test_witness.py）
"""
import glob
import json
import os
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, "ci"))

import witness_verify  # noqa: E402

WITNESS_DIR = os.path.join(REPO_ROOT, "artifacts", "witnesses")
ALL_WITNESSES = sorted(glob.glob(os.path.join(WITNESS_DIR, "*.witness.json")))
CIRC = [p for p in ALL_WITNESSES if "circulant-sinkhorn" in os.path.basename(p)]
AUCT = [p for p in ALL_WITNESSES if "auction-dual" in os.path.basename(p)]


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _resign(w):
    """篡改后按规范化规则重签 witness_sha256（隔离哈希失配路径，专测复算分歧）。"""
    w["witness_sha256"] = witness_verify._canon_sha256(w)
    return w


class TestWitnessCorpus(unittest.TestCase):
    def test_corpus_present(self):
        self.assertEqual(len(CIRC), 6, f"circulant 六例不齐: {len(CIRC)}")
        self.assertEqual(len(AUCT), 5, f"auction 五例不齐: {len(AUCT)}")


class TestRealWitnessesPass(unittest.TestCase):
    """AC1–AC4 正例：全部真见证独立复算通过。"""

    def test_all_real_witnesses_pass(self):
        self.assertTrue(ALL_WITNESSES, "artifacts/witnesses/ 为空")
        for path in ALL_WITNESSES:
            with self.subTest(witness=os.path.basename(path)):
                v = witness_verify.verify_witness(path)
                self.assertTrue(v["ok"], json.dumps(
                    [c for c in v["checks"] if not c["ok"]], ensure_ascii=False, indent=1))


class _TamperBase(unittest.TestCase):
    def verify_tampered(self, w):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "tampered.witness.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(w, fh, ensure_ascii=False, indent=2)
            return witness_verify.verify_witness(p)

    def assertCheckFailed(self, v, name):
        self.assertFalse(v["ok"], f"{name} 未触发但整体须拒")
        self.assertTrue(any(c["check"] == name and not c["ok"] for c in v["checks"]),
                        f"期望 {name} 失败; got: {[(c['check'], c['ok']) for c in v['checks'] if not c['ok']]}")


class TestTamperedBoundsRejected(_TamperBase):
    """AC2/AC3/AC4 负向：扰动界/负控登记，重签后复算仍必拒。"""

    def test_tampered_circulant_margin_rejected(self):
        w = _load(CIRC[0])
        w["bounds"]["krawczyk_image"]["min_margin"] = "1e-3"  # 篡改裕度界
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "metric_K_min_margin")

    def test_tampered_circulant_center_rejected(self):
        w = _load(CIRC[0])
        g = witness_verify._parse_rational(w["bounds"]["center"]["g"])
        w["bounds"]["center"]["g"] = f"{g.numerator + 1}/{g.denominator}"  # 微扰有理中心
        v = self.verify_tampered(_resign(w))
        self.assertFalse(v["ok"])

    def test_tampered_circulant_neg_verdict_rejected(self):
        w = _load(CIRC[0])
        w["negative_control"]["neg_verdict"]["neg_inside"] = True  # 谎报负控通过
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "neg_registered_false")

    def test_tampered_auction_bracket_rejected(self):
        w = _load(AUCT[0])
        lo = float(w["bounds"]["bracket"]["lb_lo"])
        w["bounds"]["bracket"]["lb_lo"] = repr(lo / 2)  # 放宽括弧下界
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "metric_bracket")

    def test_tampered_auction_neg_cost_rejected(self):
        w = _load(AUCT[0])
        w["negative_control"]["neg_verdict"]["neg_cost"] = w["bounds"]["auction_cost"]  # 负控假称在界内
        v = self.verify_tampered(_resign(w))
        self.assertFalse(v["ok"])

    def test_hash_tamper_without_resign_rejected(self):
        w = _load(AUCT[0])
        w["bounds"]["gap"] = "0.0"  # 篡改且不重签 → 哈希失配必拒
        v = self.verify_tampered(w)
        self.assertCheckFailed(v, "witness_sha256")


class TestSchemaGateRejected(_TamperBase):
    """AC1 格式层 fail-closed：高 major / 不可解析 schema 拒收。"""

    def test_higher_major_schema_rejected(self):
        w = _load(CIRC[0])
        w["schema_version"] = "2.0"
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "schema_major_dispatch")
        detail = [c["detail"] for c in v["checks"] if c["check"] == "schema_major_dispatch"][0]
        self.assertIn("unsupported_schema", detail)

    def test_unparseable_schema_rejected(self):
        w = _load(CIRC[0])
        w["schema_version"] = "v1"
        v = self.verify_tampered(_resign(w))
        self.assertFalse(v["ok"])
        self.assertTrue(any(c["check"] == "schema_parse" and not c["ok"] for c in v["checks"]))


class TestMissingFieldsRejected(_TamperBase):
    """AC1 必填字段缺省即拒（默认拒绝律延伸至格式层）。"""

    def test_missing_schema_version_rejected(self):
        w = _load(CIRC[0])
        del w["schema_version"]
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "schema_version_present")

    def test_missing_negative_control_rejected(self):
        w = _load(CIRC[0])
        del w["negative_control"]
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "required_top_fields")

    def test_missing_honesty_boundary_rejected(self):
        w = _load(AUCT[0])
        del w["honesty_boundary"]  # C7：auction 诚实边界必携
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "honesty_boundary_present")

    def test_nonnull_lean_binding_rejected(self):
        w = _load(CIRC[0])
        w["lean_binding"] = {"status": "checked"}  # C3：M0 禁止任何 Lean 通过性声明
        v = self.verify_tampered(_resign(w))
        self.assertCheckFailed(v, "lean_binding_null")


if __name__ == "__main__":
    unittest.main()
