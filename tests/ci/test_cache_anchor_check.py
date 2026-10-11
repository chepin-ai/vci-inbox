# CLASSIFY: L1
"""cache_anchor_check v0.3 核查器测试（PIVOT-01 WS-27 · M3 试点）。

覆盖：DONE 全条件通过；缺任一 C ⇒ 非 DONE；TTL 超时/epoch 漂移 ⇒ B6；
未锚定 ⇒ 拒绝；否定例三类（锚定失效/越权引用/跨案污染）；B7 追溯降级；
优先级遮蔽（B2+B4 ⇒ 登记 B2）；fallthrough 穷举（≥200 随机向量）；
退出路径迁移序列。

运行：python3 -m pytest tests/ci/test_cache_anchor_check.py
"""
import copy
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "ci"))

import cache_anchor_check as cac  # noqa: E402

NOW = 1_800_000_000
ANCHOR = "be48a770dc0e"
CASE = "G6"

GOOD = {
    "case_id": CASE,
    "rev_hash": "9fe29c4b",
    "anchor_ref": ANCHOR,
    "evidence_class": "anchor_only",
    "run_mode": "hot",
    "structural_unverifiable": False,
    "anchor_overturned": False,
    "invalidated_by": None,
    "self_referential_anchor": False,
    "content_cert_use": False,
    "unclassifiable_error": False,
    "build_exit_code": None,
    "skip_requested": False,
    "cache_coverage": {"m": 0, "N": 8936},
    "dual_source": {
        "official": {"reachable": True, "hash_match": True, "epoch_drift_suspect": False},
        "relay": {"reachable": True, "hash_match": True, "epoch_drift_suspect": False},
        "ts_collect": NOW - 3600,
        "anchor_epoch": "rel-2026w41",
    },
    "anchor_epoch_registered": "rel-2026w41",
    "equivalence_ref": {"cell_id": "G1", "rev": "9fe29c4b", "rc": 0,
                        "crosscheck": "CROSSCHECK_OK", "log_digest_match": True},
    "verdict": "cold-fallthrough",
    "result_commit": "75f80054",
    "toolchain_version": "leancert v4.34.1",
    "env_hash": "env-aa11",
    "paired_run_id": "pivot-01-extwave05",
    "fallthrough_log": {"seq": 7, "contiguous": True},
    "b4_retry_count": 0,
    "ttl_s": 86400,
}


def good(**over):
    ev = copy.deepcopy(GOOD)
    ev.update(over)
    return ev


def adj(ev, **kw):
    kw.setdefault("now", NOW)
    return cac.adjudicate(ev, **kw)


class TestDoneConjunction(unittest.TestCase):
    def test_done_all_conditions(self):
        r = adj(good(), anchor_ref=ANCHOR, case_id=CASE)
        self.assertEqual(r["state"], "DONE", r)
        self.assertIsNone(r["trigger"])

    def test_missing_each_c_not_done(self):
        # ¬C1：实报非 0/N
        r = adj(good(cache_coverage={"m": 5, "N": 8936}))
        self.assertNotEqual(r["state"], "DONE")
        self.assertEqual(r["state"], "PENDING", r)
        # ¬C2：等价依据空指针 ⇒ B3（BLOCKED，非 DONE）
        r = adj(good(equivalence_ref=None))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B3"), r)
        # ¬C2：rc 共识不成立 ⇒ B3
        r = adj(good(equivalence_ref={"cell_id": "G1", "rev": "9fe29c4b", "rc": 1,
                                      "crosscheck": "CROSSCHECK_OK"}))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B3"), r)
        # ¬C3：verdict 未标 cold-fallthrough ⇒ PENDING
        r = adj(good(verdict="done"))
        self.assertEqual(r["state"], "PENDING", r)
        # ¬C3：build_exit_code 非 null ⇒ PENDING（rc=0 亦不升格，fallthrough 不产生编译证据）
        r = adj(good(build_exit_code=0))
        self.assertEqual(r["state"], "PENDING", r)
        # ¬C3：§2.5 事件日志序号断裂 ⇒ PENDING（未记录视同可能已发生）
        r = adj(good(fallthrough_log={"seq": 7, "contiguous": False}))
        self.assertEqual(r["state"], "PENDING", r)
        # ¬C4：TTL 超时 ⇒ B6（BLOCKED，非 DONE）
        ev = good()
        ev["dual_source"]["ts_collect"] = NOW - 90000
        r = adj(ev)
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B6"), r)


class TestC4Timeliness(unittest.TestCase):
    def test_ttl_timeout_b6(self):
        ev = good()
        ev["dual_source"]["ts_collect"] = NOW - 86401
        r = adj(ev)
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B6"), r)
        self.assertTrue(r["recoverable"])
        self.assertEqual(r["retry_after"], 0)  # 立即重验

    def test_epoch_drift_b6(self):
        r = adj(good(anchor_epoch_registered="rel-2026w42"))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B6"), r)
        self.assertIn("epoch", r["reason"])

    def test_missing_timeliness_fields_b6(self):
        ev = good()
        del ev["dual_source"]["ts_collect"]
        r = adj(ev)
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B6"), r)


class TestAnchorOnlyEnforcement(unittest.TestCase):
    def test_unanchored_rejected(self):
        r = adj(good(), anchor_ref="deadbeef00")
        self.assertEqual(r["state"], "REJECTED", r)

    def test_missing_anchor_ref_rejected(self):
        ev = good()
        del ev["anchor_ref"]
        r = adj(ev)
        self.assertEqual(r["state"], "REJECTED", r)

    def test_missing_evidence_class_rejected(self):
        r = adj(good(evidence_class="compile"))
        self.assertEqual(r["state"], "REJECTED", r)

    # 否定例三类
    def test_negative_anchor_invalidated(self):
        # 锚定失效（§3.4 污染失效路径）⇒ B2 不可信阻断
        r = adj(good(invalidated_by="pollution-evt-01"))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B2"), r)
        self.assertFalse(r["recoverable"])

    def test_negative_overreach_citation(self):
        # 越权引用：anchor_only 充任内容认证依据（§3.1 违规）⇒ 自动 BLOCKED（B2 同级）+违规登记
        r = adj(good(content_cert_use=True))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B2"), r)
        self.assertTrue(r["violations"])

    def test_negative_cross_case_pollution(self):
        r = adj(good(case_id="OTHER-CASE"), case_id=CASE)
        self.assertEqual(r["state"], "REJECTED", r)
        self.assertIn("跨案污染", r["reason"])

    def test_self_referential_anchor_b2(self):
        r = adj(good(self_referential_anchor=True))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B2"), r)


class TestTriggerPriority(unittest.TestCase):
    def test_b2_shadows_b4(self):
        # 同时命中 B2（哈希不符）+ B4（双源不可达）⇒ 登记最高优先级 B2
        ev = good(unclassifiable_error=False)
        ev["dual_source"]["official"] = {"reachable": False, "hash_match": False}
        ev["dual_source"]["relay"] = {"reachable": False, "hash_match": True}
        r = adj(ev)
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B2"), r)
        self.assertFalse(r["recoverable"])  # B2 不可信，禁止重试自愈

    def test_b1_shadows_all(self):
        r = adj(good(structural_unverifiable=True, equivalence_ref=None))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B1"), r)
        self.assertFalse(r["recoverable"])

    def test_b3_shadows_b4(self):
        ev = good(equivalence_ref=None)
        ev["dual_source"]["official"]["reachable"] = False
        ev["dual_source"]["relay"]["reachable"] = False
        r = adj(ev)
        self.assertEqual(r["trigger"], "B3", r)

    def test_b4_retry_exhaustion(self):
        ev = good(b4_retry_count=4)
        ev["dual_source"]["official"]["reachable"] = False
        ev["dual_source"]["relay"]["reachable"] = False
        r = adj(ev)
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B4"), r)
        self.assertFalse(r["recoverable"])  # §2.4-2：退避 4 次用尽转不可恢复并上报

    def test_b5_cold_skip(self):
        r = adj(good(run_mode="cold", skip_requested=True))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B5"), r)

    def test_b7_retroactive_overturn(self):
        # B7：③§4a 追溯降级 ⇒ BLOCKED + 条目作废 + 回 PENDING 重走主链
        r = adj(good(anchor_overturned=True))
        self.assertEqual((r["state"], r["trigger"]), ("BLOCKED", "B7"), r)
        self.assertFalse(r["recoverable"])
        self.assertTrue(r["extra_invalidate"] if "extra_invalidate" in r else r["invalidate_entries"])
        self.assertEqual(r["next_state"], "PENDING")

    def test_b6_shadows_b7(self):
        # B6 优先级高于 B7：同时命中登记 B6
        ev = good(anchor_overturned=True)
        ev["dual_source"]["ts_collect"] = NOW - 90000
        r = adj(ev)
        self.assertEqual(r["trigger"], "B6", r)

    def test_fail_rc_nonzero(self):
        # §2.1 第五态 FAIL：rc≠0 编译裁决不得转 fallthrough
        r = adj(good(build_exit_code=1))
        self.assertEqual(r["state"], "FAIL", r)


class TestExitPathTransitions(unittest.TestCase):
    def test_full_exit_sequence(self):
        # BLOCKED → 重验 → PENDING → DONE/拒绝
        self.assertEqual(cac.transition("PENDING", "BLOCKED"), "BLOCKED")
        self.assertEqual(cac.transition("BLOCKED", "PENDING",
                                        reverify_evidence="ev-new-01"), "PENDING")
        self.assertEqual(cac.transition("PENDING", "DONE"), "DONE")
        self.assertEqual(cac.transition("PENDING", "REJECTED"), "REJECTED")

    def test_blocked_direct_done_forbidden(self):
        with self.assertRaises(cac.IllegalTransition):
            cac.transition("BLOCKED", "DONE")

    def test_blocked_to_pending_requires_new_evidence(self):
        with self.assertRaises(cac.IllegalTransition):
            cac.transition("BLOCKED", "PENDING")  # 无重验新证据

    def test_done_silent_rewrite_forbidden(self):
        with self.assertRaises(cac.IllegalTransition):
            cac.transition("DONE", "PENDING")  # 无判定席、无留痕
        with self.assertRaises(cac.IllegalTransition):
            cac.transition("DONE", "BLOCKED", by="adjudication_board", trace="t1")
        # 判定席复议撤销 + 留痕 ⇒ 允许降回 PENDING
        self.assertEqual(cac.transition("DONE", "PENDING", by="adjudication_board",
                                        trace="board-ruling-01"), "PENDING")

    def test_unknown_state_rejected(self):
        with self.assertRaises(cac.IllegalTransition):
            cac.transition("PENDING", "LIMBO")


class TestFallthroughImpossibility(unittest.TestCase):
    """fallthrough 不可能性：任何输入必落五态之一，无隐式允许。"""

    def test_exhaustive_random_vectors(self):
        rng = random.Random(27)
        states = {"PENDING", "BLOCKED", "DONE", "FAIL", "REJECTED"}
        seen = set()
        fields = ("case_id", "rev_hash", "anchor_ref", "evidence_class", "run_mode",
                  "structural_unverifiable", "anchor_overturned", "invalidated_by",
                  "self_referential_anchor", "content_cert_use", "unclassifiable_error",
                  "build_exit_code", "skip_requested", "cache_coverage", "dual_source",
                  "anchor_epoch_registered", "equivalence_ref", "verdict",
                  "result_commit", "toolchain_version", "env_hash", "paired_run_id",
                  "fallthrough_log", "b4_retry_count", "ttl_s")
        for i in range(300):
            # 一半从空白稀疏生成，一半以合格证据为底随机变异（保证 DONE/PENDING/FAIL
            # 亦被穷举覆盖）
            base = (i % 2 == 1)
            ev = copy.deepcopy(GOOD) if base else {}
            force_fail = base and rng.random() < 0.08
            for f in fields:
                if rng.random() < (0.85 if base else 0.5):
                    continue
                choice = rng.random()
                if choice < 0.4 and f in GOOD:  # 合法值
                    ev[f] = copy.deepcopy(GOOD[f])
                elif choice < 0.7:  # 类型错误值
                    ev[f] = rng.choice([None, 0, -1, "x", [], {}, True])
                else:  # 边界值
                    ev[f] = rng.choice([{"m": 0, "N": 1}, {"reachable": False},
                                        NOW, NOW - 10**9, "cold", "hot", 1, 86400])
            kw = dict(anchor_ref=rng.choice([None, ANCHOR, "zzz"]),
                      case_id=rng.choice([None, CASE, "OTHER"]),
                      now=rng.choice([NOW, 0, NOW + 10**9]),
                      ttl=rng.choice([None, 0, 86400]))
            if force_fail:
                ev = copy.deepcopy(GOOD)
                ev["build_exit_code"] = 1  # 定向覆盖 FAIL（§2.1 rc≠0）
                kw = dict(now=NOW)
            r = cac.adjudicate(ev, **kw)
            self.assertIn(r["state"], states, (i, ev, r))
            seen.add(r["state"])
            if r["state"] == "BLOCKED":
                if r["trigger"] is not None:
                    self.assertIn(r["trigger"], cac.TRIGGERS)
                    spec = cac.TRIGGERS[r["trigger"]]
                    self.assertIsNotNone(r["recoverable"])
        self.assertEqual(seen, states, "300 随机向量未覆盖全部五态：%r" % seen)

    def test_malformed_inputs(self):
        for bad in (None, [], "x", 42, {"dual_source": {"official": 1}}):
            r = cac.adjudicate(bad)
            self.assertIn(r["state"], {"PENDING", "BLOCKED", "DONE", "FAIL", "REJECTED"})


class TestCli(unittest.TestCase):
    def test_cli_adjudicate(self, ):
        ev_file = REPO_ROOT / "tests" / "ci" / "_tmp_evidence.json"
        try:
            ev_file.write_text(json.dumps(good()), encoding="utf-8")
            p = subprocess.run(
                [sys.executable, str(REPO_ROOT / "ci" / "cache_anchor_check.py"),
                 "adjudicate", str(ev_file), "--anchor-ref", ANCHOR,
                 "--case-id", CASE, "--now", str(NOW)],
                capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
            self.assertEqual(out["state"], "DONE", out)
            self.assertEqual(set(out) >= {"state", "trigger", "reason",
                                          "recoverable", "retry_after"}, True)
        finally:
            ev_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
