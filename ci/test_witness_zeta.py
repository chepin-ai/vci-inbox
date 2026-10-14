# CLASSIFY: L1
# test_witness_zeta.py · WS-63 ζ 见证链验收（≥20 项；全绿为准入）
# 运行：PYTHONPATH=ci python3 -m pytest ci/test_witness_zeta.py -v
# 注意：test_full_verify_iso100 内含 T=100 围道绕数独立复算（约 6-7 分钟墙钟）。
import json
import os
import subprocess
import sys
from fractions import Fraction

import re

import pytest
from mpmath import mp, mpf, iv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import witness_zeta_verify as V  # noqa: E402

CERTS = {
    "iso100": "zeta-iso-100.witness.json",
    "iso1000": "zeta-iso-1000.witness.json",
    "trunc": "psi-trunc.witness.json",
}


def _path(name):
    return os.path.join(ROOT, "artifacts", "witnesses-zeta", CERTS[name])


def _load(name):
    with open(_path(name), encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------- CLASSIFY 纪律

def test_classify_first_line_gen():
    with open(os.path.join(HERE, "witness_zeta_gen.py"), encoding="utf-8") as fh:
        assert fh.readline().rstrip("\n") == "# CLASSIFY: L1"


def test_classify_first_line_verify():
    with open(os.path.join(HERE, "witness_zeta_verify.py"), encoding="utf-8") as fh:
        assert fh.readline().rstrip("\n") == "# CLASSIFY: L1"


def test_classify_first_line_tests():
    with open(os.path.abspath(__file__), encoding="utf-8") as fh:
        assert fh.readline().rstrip("\n") == "# CLASSIFY: L1"


@pytest.mark.parametrize("name", list(CERTS))
def test_cert_classify_first_field(name):
    with open(_path(name), encoding="utf-8") as fh:
        first = json.load(fh)
    # 首字段序：json 解析保序（py3.7+ dict 保插入序）
    assert list(first.keys())[0] == "CLASSIFY" and first["CLASSIFY"] == "L1"


# ---------------------------------------------------------- 结构与哈希

@pytest.mark.parametrize("name", list(CERTS))
def test_schema(name):
    V._check_schema(_load(name), V.CL())  # 枢线修补#6: 签名 drift 补 CL()


@pytest.mark.parametrize("name", list(CERTS))
def test_witness_sha256_recompute(name):
    w = _load(name)
    assert V._canon_sha256({k: v for k, v in w.items() if k != "witness_sha256"}) == w["witness_sha256"]  # 枢线修补#3 同律:剥自字段


@pytest.mark.parametrize("name", list(CERTS))
def test_generator_sha256_registered(name):
    w = _load(name)
    gh = w["provenance"]["generator"]["sha256"]
    assert gh == V._sha256_file(os.path.join(HERE, "witness_zeta_gen.py"))


def test_trunc_source_sha256_matches_iso1000():
    w = _load("trunc")
    assert w["inputs"]["zero_source"]["sha256"] == V._sha256_file(_path("iso1000"))


# ---------------------------------------------------------- 披露逐字

_REQ_DISC = "区间见证层 PASS、kernel 层未证、非 RH 证据"


def _has_req_disc(d):
    # 枢线修补#13 同律: 逐字全等或「逐字前缀+；」加性强化
    return any(x == _REQ_DISC or x.startswith(_REQ_DISC + "；") for x in d)


def test_disclosure_prefix_extension_semantics():
    # 枢线修补#13: 加性强化受理 / 减弱改写拒
    assert _has_req_disc([_REQ_DISC])
    assert _has_req_disc([_REQ_DISC + "；存在性 PASS ⊊ 计数 PASS"])
    assert not _has_req_disc([_REQ_DISC.replace("非 RH 证据", "RH 证据")])
    assert not _has_req_disc(["区间见证层 PASS"])


def test_disclosure_verbatim_iso100():
    d = _load("iso100")["disclosure"]
    assert "有限高度 T=100 截断" in d
    assert _has_req_disc(d)


def test_disclosure_verbatim_iso1000():
    d = _load("iso1000")["disclosure"]
    assert "有限高度 T=1000 截断" in d
    assert _has_req_disc(d)


def test_disclosure_verbatim_trunc():
    d = _load("trunc")["disclosure"]
    assert "有限高度 T=1000 截断" in d
    assert _has_req_disc(d)
    assert ("本证书为 Dudek 定理适用范围(x>e⁶⁰)之外的点态管道演练，非定理实例；"
            "零点输入由 ISO-1000 区间括号供给") in d


def test_iso1000_completeness_blocked_honest():
    c = _load("iso1000")["completeness"]
    assert c["status"] == "BLOCKED(B1-TB) time-box"  # SUP-01: 子码分账(B1-TB=time-box, 区别于结构性拒证)
    assert "B1-TB" in c["blocked_subcode"] and "重试预算" in c["retry_budget"]
    assert c["winding"] is None
    assert "熔断" in c["reason"]


def test_iso100_completeness_certified():
    c = _load("iso100")["completeness"]
    assert c["status"] == "CERTIFIED" and c["winding"] == 29 and c["winding_2NT"] == 58
    assert c["backlund"]["n_backlund"] == 29 and c["backlund"]["re_positive"] is True


# ---------------------------------------------------------- 单元：数学内核

def _ivlo(x):
    return mpf(x._mpi_[0])  # mpmath 1.3.0: ivmpf._mpi_ 为裸端点元组对


def _ivhi(x):
    return mpf(x._mpi_[1])


def test_patch17_point_eval_tight():
    """枢线修补#17: 结点紧求值钉档——ζ(2)=π²/6、ζ(1/2+100i) 与 mp 高精密值吻合、区间宽≪1e-60。"""
    mp.dps = 80
    Q, meth = V._point_eval_zeta_iv(Fraction(2), Fraction(0), 400, 200)
    assert meth == "cvz_pt"
    tru = mp.pi ** 2 / 6
    assert abs(_ivlo(Q[0]) - tru) < mpf("1e-60") and abs(_ivhi(Q[1])) < mpf("1e-60")
    Q2, _ = V._point_eval_zeta_iv(Fraction(1, 2), Fraction(100), 400, 200)
    z2 = mp.zeta(mp.mpc(mpf("0.5"), mpf(100)))
    assert abs(_ivlo(Q2[0]) - z2.real) < mpf("1e-60")
    assert abs(_ivlo(Q2[1]) - z2.imag) < mpf("1e-60")
    a0 = V._iv_arg_tight(Q)
    assert _ivlo(a0) <= 0 <= _ivhi(a0)
    assert _ivhi(a0) - _ivlo(a0) < mpf("1e-60")  # 锚点 arg ζ(2)=0


def test_patch17_wrap_pi():
    """主值包裹：近 ±π 边界的紧增量回卷正确；域内增量不动。"""
    iv.dps = 50
    d = V._wrap_pi_iv(iv.mpf("3.13") - iv.mpf("-3.13"))   # 真值 +0.0031… 回卷 −2π 侧? 3.13−(−3.13)=6.26>π → −2π
    assert abs(float(d.a) - (6.26 - 2 * float(mp.pi))) < 1e-12
    d2 = V._wrap_pi_iv(iv.mpf("-3.13") - iv.mpf("3.13"))  # −6.26 → +2π
    assert abs(float(d2.a) - (-6.26 + 2 * float(mp.pi))) < 1e-12
    d3 = V._wrap_pi_iv(iv.mpf("0.5") - iv.mpf("0.1"))
    assert abs(float(d3.a) - 0.4) < 1e-12




def test_theta_contains_siegeltheta():
    mp.dps = 60
    iv.dps = 50
    for ts in ("14.134725", "50.5", "99.9"):
        th = V.theta_iv(V._iv_of(ts))
        tr = mp.siegeltheta(mpf(ts))
        assert th.a < tr < th.b


def test_rs_envelope_contains_siegelz():
    mp.dps = 60
    iv.dps = 50
    c = V._iv_of("0.2")
    for ts in ("14.3", "57.77", "123.456", "999.9"):
        env, E = V.rs_envelope(V._iv_of(ts), c)
        tr = mp.siegelz(mpf(ts))
        assert env.a < tr < env.b
        assert env.b - env.a < 2 * E.b + mpf("1e-8")  # 枢线修补#7: A 内禀宽(θ Brent 余项认证 ~1.8e-9@t=14.3 实测)须计入; 包含性(上行)不受影响


def test_psi_function_matches_mp():
    mp.dps = 60
    iv.dps = 50
    for ps in ("0.1", "0.5", "0.9"):
        p = V._iv_of(ps)
        tr = mp.cos(2 * mp.pi * (mpf(ps) ** 2 - mpf(ps) - mpf(1) / 16)) / mp.cos(2 * mp.pi * mpf(ps))
        v = V._psi_iv(p)
        assert v.a < tr < v.b


def test_psi3_bounded():
    iv.dps = 50
    m = 0.0
    for j in range(51):
        v = V._psi3_iv(V._iv_of(str(Fraction(j, 50))))
        m = max(m, float(abs(v).b))
    assert m < 40.0  # 实测峰 ≈29；断界 40 含余量


def test_cvz_box_contains_mp_zeta():
    mp.dps = 300
    iv.dps = 220
    Z, E = V._zeta_cvz_box(iv.mpf("0.5"), iv.mpf("100"))
    tr = mp.zeta(mp.mpc("0.5", "100"))
    assert Z[0].a - E.b < tr.real < Z[0].b + E.b
    assert Z[1].a - E.b < tr.imag < Z[1].b + E.b


def test_em_box_contains_mp_zeta():
    mp.dps = 300
    iv.dps = 80
    Z, E = V._zeta_em_box(iv.mpf("0.5"), iv.mpf("1000"), 1200)
    tr = mp.zeta(mp.mpc("0.5", "1000"))
    assert Z[0].a - E.b < tr.real < Z[0].b + E.b
    assert Z[1].a - E.b < tr.imag < Z[1].b + E.b


def test_dirichlet_box_contains_mp_zeta():
    mp.dps = 300
    iv.dps = 80
    Z, E = V._zeta_dirichlet_box(iv.mpf("37.7"), 200)
    tr = mp.zeta(mp.mpc("2", "37.7"))
    assert Z[0].a - E.b < tr.real < Z[0].b + E.b
    assert Z[1].a - E.b < tr.imag < Z[1].b + E.b


def test_functional_equation_box_overlap():
    # 枢线修补#8: 原设计 FE 盒与 CVZ 直评交叠, 然 CVZ/EM 均设 σ≥1/2 门(σ=0.25 直评非法)。
    # 改为 FE 通道盒包含高精密真值, 与 cvz/em/dirichlet 三测试同律(包含断言)。
    mp.dps = 300
    iv.dps = 220
    sig, t = iv.mpf("0.25"), iv.mpf("60.5")
    Za, Ea, _ = V.zeta_box(sig, t, 400, 200)          # FE 通道(σ<1/2 调度器合法路径)
    tr = mp.zeta(mp.mpc("0.25", "60.5"))
    assert Za[0].a - Ea.b < tr.real < Za[0].b + Ea.b
    assert Za[1].a - Ea.b < tr.imag < Za[1].b + Ea.b


def test_known_zero_replay_consistency():
    """已知零点重放一致性闸：全部括号中点须落在 mp.zetazero 序列表 ±0.025 内。"""
    mp.dps = 50
    for name, n in (("iso100", 29), ("iso1000", 649)):
        brackets = _load(name)["existence"]["brackets"]
        assert len(brackets) == n
        for j, (lo, hi) in enumerate(brackets):
            mid = (Fraction(lo) + Fraction(hi)) / 2
            gz = mp.zetazero(j + 1).imag
            assert abs(float(mid) - float(gz)) < 0.025


def test_brackets_sorted_disjoint_narrow():
    for name in ("iso100", "iso1000"):
        bs = [tuple(map(Fraction, b)) for b in _load(name)["existence"]["brackets"]]
        for lo, hi in bs:
            assert hi - lo <= Fraction(5, 100)
        for a, b in zip(bs, bs[1:]):
            assert a[1] < b[0]


def test_endpoint_enclosures_opposite_signs():
    for e in _load("iso100")["existence"]["endpoint_enclosures"]:
        l = tuple(map(float, e[:2]))
        h = tuple(map(float, e[2:]))
        assert l[0] * l[1] > 0 and h[0] * h[1] > 0 and l[0] * h[0] < 0


# ---------------------------------------------------------- 负控

def test_fake_bracket_rejected():
    iv.dps = 50
    c = V._iv_of(_load("iso100")["bounds"]["remainder_low_t_constant"])
    ok, _detail, _e1, _e2 = V._certify_bracket("16.0", "16.04", 100, c)  # 枢线修补#9: 签名 drift (t_cap, c_low; 返回四元组)
    assert not ok


def test_tampered_iso100_bracket_fails_fast(tmp_path):
    import copy
    w = copy.deepcopy(_load("iso100"))
    lo, hi = w["existence"]["brackets"][0]
    w["existence"]["brackets"][0] = [str(Fraction(lo) + Fraction(1, 10)),
                                     str(Fraction(hi) + Fraction(1, 10))]
    w["witness_sha256"] = V._canon_sha256({k: v for k, v in w.items() if k != "witness_sha256"})  # 枢线修补#3 同律
    p = tmp_path / "tampered.json"  # 枢线修补#10: verify_witness 收路径; fail-closed 返 ok=False 非 raise
    p.write_text(json.dumps(w, ensure_ascii=False), encoding="utf-8")
    assert not V.verify_witness(str(p))["ok"]


def test_tampered_trunc_bound_rejected(tmp_path):
    import copy
    w = copy.deepcopy(_load("trunc"))
    w["bounds"]["trunc_metrics"]["bound"] = w["negative_control"]["tampered_bound"]
    w["witness_sha256"] = V._canon_sha256({k: v for k, v in w.items() if k != "witness_sha256"})  # 枢线修补#3 同律
    p = tmp_path / "tampered_trunc.json"  # 枢线修补#10 同律
    p.write_text(json.dumps(w, ensure_ascii=False), encoding="utf-8")
    assert not V.verify_witness(str(p))["ok"]


# ---------------------------------------------------------- 全量复算（慢）

@pytest.fixture(scope="module")
def full_results():
    return {name: V.verify_witness(_path(name)) for name in CERTS}  # 枢线修补#10: 路径


def test_full_verify_all_pass(full_results):
    # OBL-EXT11-a 关闭(枢线修补#17): Backlund 门升级——锚点 t=0 修正(KI-EXT11-1-ADD2 根因:
    # ε 起步缺锚段辐角 −0.0794691791…rad)+结点紧区间 Δarg(张角余量以分支认证纳入,
    # ±1e-9 浮点容忍移除)——三证全 PASS;KI-EXT11-1 关闭。
    assert full_results["iso1000"]["ok"], "iso1000"
    assert full_results["trunc"]["ok"], "trunc"
    r100 = full_results["iso100"]
    assert r100["ok"], f"iso100 应在 OBL-EXT11-a 关闭后 PASS: {r100}"


def test_backlund_obl_ext11a_closure(full_results):
    """OBL-EXT11-a 关闭钉档(逐字关闭条件): 张角余量纳入后 N_B 区间落入唯一整数窗;
    不得以放宽区间宽度绕过——区间宽须 ≪1 且 detail 载明锚点/方法/结点数。"""
    r = full_results["iso100"]
    chk = {c["check"]: c for c in r["checks"]}
    assert chk["backlund_unique_integer_window"]["ok"]
    d = chk["backlund_unique_integer_window"]["detail"]
    assert "锚点=t=0" in d and "junction_pointeval_interval" in d
    m = re.search(r"宽\[?([0-9.eE+-]+)", d)
    assert m and float(m.group(1)) < 1e-10


def test_full_verify_iso100_winding(full_results):
    chk = {c["check"]: c for c in full_results["iso100"]["checks"]}  # 枢线修补#11: 返回结构 {ok,checks,error}
    assert chk["winding_recompute"]["ok"] and "复算=29" in chk["winding_recompute"]["detail"]


def test_full_verify_trunc_residual(full_results):
    r = full_results["trunc"]  # 枢线修补#11 同律
    chk = {c["check"]: c for c in r["checks"]}
    assert chk["residual_within_dudek_form"]["ok"]
    lo, hi = _load("trunc")["bounds"]["trunc_metrics"]["residual"]
    assert float(lo) < 0 < float(hi)


def test_cli_fail_closed(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"CLASSIFY": "L1"}', encoding="utf-8")
    r = subprocess.run([sys.executable, os.path.join(HERE, "witness_zeta_verify.py"),
                        str(bad)], capture_output=True, text=True)
    assert r.returncode == 1


def test_cli_iso1000_pass():
    r = subprocess.run([sys.executable, os.path.join(HERE, "witness_zeta_verify.py"),
                        "--json", _path("iso1000")], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr[-400:]
    out = json.loads(r.stdout)  # 枢线修补#12: --json 输出 [{file,ok,error,failed}]
    assert out[0]["ok"] and out[0]["failed"] == []


def test_backlund_cert_fields(full_results):
    """v1.1.1（EXT15-SUP-02/qfa 修订项③）：证书 backlund 必载 nB_interval /
    nB_interval_width / width_budget / branch_exclusion_28_30；核验器复算逐字一致；
    N_B 区间唯一整数窗 ceil(lo)==floor(hi)==29。"""
    bk = _load("iso100")["completeness"]["backlund"]
    for k in ("nB_interval", "nB_interval_width", "width_budget", "branch_exclusion_28_30"):
        assert k in bk, f"证书缺字段 {k}"
    wb = bk["width_budget"]
    for k in ("w_theta_stirling_brent", "w_junction_args_total", "w_wrap", "w_round",
              "transfer", "total_equals_nB_width", "analytic_check"):
        assert k in wb, f"width_budget 缺子字段 {k}"
    assert wb["total_equals_nB_width"] == bk["nB_interval_width"]
    mp.dps = 60
    lo, hi = mpf(bk["nB_interval"][0]), mpf(bk["nB_interval"][1])
    assert int(mp.ceil(lo)) == int(mp.floor(hi)) == 29
    assert hi - lo < mpf("1e-10")
    chk = {c["check"]: c for c in full_results["iso100"]["checks"]}
    assert chk["backlund_cert_nB_interval_match"]["ok"]
    assert chk["backlund_cert_width_budget_match"]["ok"]
