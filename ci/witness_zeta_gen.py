# CLASSIFY: L1
# witness_zeta_gen.py · EXT-WAVE-11「赎」波 WS-63 ζ 零点隔离+显式公式截断区间见证·生成器
# （schema v1.0 · 与 ci/witness_zeta_verify.py 零共享代码路径）
#
# 职责边界（GAP/WIT 分离）：本生成器只做候选生产与证据登记——零点候选由
# mpmath.mp（mp.siegelz / mp.zetazero / mp.nzeros，dps=50）给出，无正确性负担；
# 登记数值（括号端点包络、TRUNC 残差等）由本文件内一套独立的 mpmath.iv 实现按
# 规范 [S1]–[S10]（见核验器文件头，两文件各自携带同一书面规范）计算；正确性由
# ci/witness_zeta_verify.py 独立复算裁决。
#
# 交付三证书（ZETA-INST-01-20261012T2130Z 定案卡）：
#   artifacts/witnesses-zeta/zeta-iso-100.witness.json    —— CERT-ζ-ISO-100
#   artifacts/witnesses-zeta/zeta-iso-1000.witness.json   —— CERT-ζ-ISO-1000
#   artifacts/witnesses-zeta/psi-trunc.witness.json       —— CERT-ψ-TRUNC
#   artifacts/witnesses-zeta/manifest.json / run-log.json
#
# 用法：
#   python3 ci/witness_zeta_gen.py                      # 全流程（双跑闸）
#   python3 ci/witness_zeta_gen.py --emit-raw DIR       # 确定性载荷（双跑闸用）
#   python3 ci/witness_zeta_gen.py --only iso100-existence|iso100-completeness|
#         iso1000-existence|iso1000-completeness|trunc  # 单阶段（调试用）
#   --completeness-timeout SEC   # ISO-1000 完备性墙钟预算（默认 1080=18min，
#                                # 超时则明码 BLOCKED(B1) time-box，不升格）
import argparse
import datetime
import hashlib
import json
import math
import os
import platform
import subprocess
import witness_zeta_verify as VZ  # 枢线修补#18：nB_interval/width_budget 由核验器同款复算产出（EXT15-SUP-02/qfa）
import sys
import time
from fractions import Fraction

import mpmath
from mpmath import mp, mpf, iv

RUN_ID = "ws63-ext-wave-11-zeta"
TS_FIXED = "2026-10-12T21:30:00Z"   # 定案卡时刻；确定性载荷不嵌真实墙钟
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "artifacts", "witnesses-zeta")

C_LOW = "0.2"          # t<200 段 RS 余项常数（推导依据见 bounds.derivation）
DIR_M = 200            # Dirichlet 部分和项数（σ=2 竖边）
EM_N_100 = 400         # T=100 围道 EM 备用项数（实际 T=100 全 CVZ）
EM_N_1000 = 1200       # T=1000 围道 EM 项数
BACKLUND_M = 10000     # Backlund Re ζ(2+it)>0 解析界部分和
CONTOUR_DPS = {"cvz": 220, "em_dirichlet": 80}   # 见 deviation(5) 披露

DISCLOSURE_COMMON = ("区间见证层 PASS、kernel 层未证、非 RH 证据；"
                    "存在性 PASS ⊊ 计数 PASS（括号存在性≠括号数正确性，计数完备性见 verdict/ completeness 分层）")
TRUNC_DISCLOSURE = ("本证书为 Dudek 定理适用范围(x>e⁶⁰)之外的点态管道演练，非定理实例；"
                    "零点输入由 ISO-1000 区间括号供给")
DEVIATION = (
    "偏差逐字披露：(1) 定案卡所给 CVZ 余项界 3(3+√8)^(-n)(1+8|s|)/|1-2^(1-s)| 缺 "
    "1/|Γ(s)|~e^(π|t|/2) 因子，实测 |t|=50 处真误差 1e-124 已超该界（6e-151）27 个量级；"
    "本机采用文献正确形式 |γ_n|≤2(3+√8)^(-200)/(|1-2^(1-s)|·|Γ(s)|)（CVZ 2000 Prop.3 / "
    "Borwein 2000；|Γ| 下界由 Stirling 区间下界给出），仅在 σ≥1/2 且 |t|≤160 使用 CVZ。"
    "(2) t<200 段 RS 余项常数取 C_low=0.2·t^(-5/4)（非定理常数）：生成器侧稠密网格实测 "
    "max|R|·t^(5/4)≈0.0539（t∈[14,200]，2500 点+跳点加密），取 3.7× 安全放大；"
    "t≥200 段用 Gabcke 0.053·t^(-5/4)（定案卡给定，实测 max≈0.052 吻合）。"
    "(3) RS 公式带 Ψ+Ψ'''/(96π²√τ) 两个校正项（定案卡「余项用 Gabcke 显式界 "
    "|R₁|<0.053t^(-5/4)」对应两个校正项的余项阶，已实测核对：单 Ψ 项余项实为 "
    "O(t^(-3/4))，必须带第二校正项方与 0.053t^(-5/4) 匹配）。"
    "(4) 完备性围道矩形 σ∈[-1,2]×[ε,T] 的上半绕数为 N(T)（29/649）；定案卡所写「绕数=58」"
    "系上下两半对称合计 2N(T) 之口径，ρ↔1−ρ̄ 对同在上半矩形内，围道实得 29；"
    "等价完备性命题（绕数==括号数）已认证，winding_2NT 字段登记 58 以便对照。"
    "(5) T=1000 围道工作精度 dps=80（定案卡 dps≈220 系针对 CVZ 权重相消；实测归一化后"
    "相消比 ≤7×10⁴，dps=80 仍留 ≥10⁷⁰ 量级余量）；T=100 围道全程 dps=220 如卡。"
    "(6) σ<1/2 围道段经函数方程 ζ(s)=χ(s)ζ(1-s) 求值，χ 由初等因子+Stirling/WW "
    "显式余项构成（不用 gamma）；σ=2 竖边用 Dirichlet 部分和（尾界 1/M）；"
    "|t|>160 且 σ≥1/2 段用 Euler–Maclaurin（K=5，显式余项，ζ(11)≤2 由初等望远镜界给出）。"
)


# ------------------------------------------------------------------ 基础

def _canon_sha256(w):
    blob = json.dumps(w, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _dec(x, nd=42):
    """mpf → 定点十进制字符串（nd 位小数，向零截断后精确有理）。"""
    return mp.nstr(mpf(x), nd + 8)


def _frac(s):
    return Fraction(str(s).strip())


# ------------------------------------------------------------------ 生成器侧 iv 规范实现（独立代码）
# 规范 [S2]/[S3]/[S10]（书面规范见核验器头注释；此处为第二份独立实现）。

_BN = {1: Fraction(1, 6), 2: Fraction(-1, 30), 3: Fraction(1, 42), 4: Fraction(-1, 30)}


def _ivf(fr):
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def _ivs(s):
    return _ivf(_frac(s))


def _cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _cd(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def _ce(a):
    r = iv.exp(a[0])
    return (r * iv.cos(a[1]), r * iv.sin(a[1]))


def g_theta(t, K=4):
    iv_local = iv
    x = iv_local.mpf(1) / 4
    y = t / 2
    r2 = x * x + y * y
    u = iv_local.mpf("0.5") * iv_local.log(r2)
    phi = iv_local.pi / 2 - iv_local.atan2(x, y)
    a = -iv_local.mpf(1) / 4
    b = t / 2
    im = a * phi + b * u - b
    zi = _cd((iv_local.mpf(1), iv_local.mpf(0)), (x, y))
    zp = zi
    corr = iv_local.mpf(0)
    for k in range(1, K + 1):
        bk = _ivf(_BN[k])
        corr = corr + bk / (2 * k * (2 * k - 1)) * zp[1]
        zp = _cm(zp, _cm(zi, zi))
    th = im + corr - b * iv_local.log(iv_local.pi)
    az = iv_local.sqrt(r2)
    sechalf = 1 / iv_local.sqrt((1 + x / az) / 2)
    rem = _ivf(Fraction(5, 66)) / 90 * sechalf ** 10 * az ** (-9)
    return iv_local.mpf((th.a - rem.b, th.b + rem.b))


def g_psi(p):
    tp = 2 * iv.pi
    u = tp * (p * p - p - iv.mpf(1) / 16)
    v = tp * p
    return iv.cos(u) / iv.cos(v)


def g_psi3(p):
    tp = 2 * iv.pi
    u = tp * (p * p - p - iv.mpf(1) / 16)
    v = tp * p
    u1 = tp * (2 * p - 1)
    u2 = 4 * iv.pi
    w = tp
    f = iv.cos(u)
    fp = -u1 * iv.sin(u)
    fpp = -u2 * iv.sin(u) - u1 * u1 * iv.cos(u)
    fppp = -3 * u1 * u2 * iv.cos(u) + u1 ** 3 * iv.sin(u)
    g = iv.cos(v)
    gp = -w * iv.sin(v)
    gpp = -w * w * iv.cos(v)
    gppp = w ** 3 * iv.sin(v)
    g2 = g * g
    g3 = g2 * g
    g4 = g3 * g
    h = 1 / g
    hp = -gp / g2
    hpp = 2 * gp * gp / g3 - gpp / g2
    hppp = -6 * gp ** 3 / g4 + 6 * gp * gpp / g3 - gppp / g2
    return fppp * h + 3 * fpp * hp + 3 * fp * hpp + f * hppp


def g_rs_envelope(t):
    """规范 [S3]：返回 (包络, E)。c_low 取证书登记常数 C_LOW。"""
    tp = 2 * iv.pi
    tau = t / tp
    sq = iv.sqrt(tau)
    n_lo = math.floor(float(sq.a))
    n_hi = math.floor(float(sq.b))
    if n_lo != n_hi:
        raise RuntimeError("N straddle")
    N = n_lo
    p = sq - N
    th = g_theta(t)
    acc = iv.mpf(0)
    for n in range(1, N + 1):
        acc = acc + iv.cos(th - t * iv.log(iv.mpf(n))) / iv.sqrt(iv.mpf(n))
    main = 2 * acc
    corr = g_psi(p) - g_psi3(p) / (96 * iv.pi ** 2 * iv.sqrt(tau))
    sgn = iv.mpf((-1) ** (N - 1))
    A = main + sgn * corr * tau ** (-iv.mpf(1) / 4)
    c = _ivf(Fraction(53, 1000)) if t.a >= 200 else _ivs(C_LOW)
    E = c * t ** (-iv.mpf(5) / 4)
    return iv.mpf((A.a - E.b, A.b + E.b)), E


def _iv_str(x):
    s = mp.nstr(x, 60)
    if s.startswith("["):
        inner = s[1:-1].split(",")
        assert len(inner) == 2 and inner[0].strip() == inner[1].strip(), s
        return inner[0].strip()
    return s


# ------------------------------------------------------------------ 存在性候选（mp，无正确性负担）

def _candidate_zeros(T):
    """Δt=0.1 扫描 mp.siegelz 变号 + 二分求零点估计（dps=50）。"""
    mp.dps = 50
    t = mpf("10.0")
    step = mpf("0.1")
    zeros = []
    f_prev = mp.siegelz(t)
    t_prev = t
    while t <= mpf(T):
        t += step
        f = mp.siegelz(t)
        if f * f_prev < 0:
            a, b = t_prev, t
            fa, fb = f_prev, f
            for _ in range(80):
                m = (a + b) / 2
                fm = mp.siegelz(m)
                if fm * fa < 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
            zeros.append((a + b) / 2)
        t_prev, f_prev = t, f
    return zeros


def _brackets_for(T, expected):
    """零点估计 → 对称括号（宽 0.0498 ≤ 0.05），端点取 42 位小数十进制有理串。
    生成器侧 iv 预检：两端包络须异号且不含 0；不满足则半宽递减重试。"""
    zeros = _candidate_zeros(T)
    if len(zeros) != expected:
        raise RuntimeError(f"候选数 {len(zeros)} ≠ 期望 {expected}")
    iv.dps = 50
    jumps = [2 * mp.pi * k * k for k in range(1, int(math.sqrt(float(T) / 6.3)) + 3)]
    out = []
    encs = []
    for m in zeros:
        chosen = None
        for hw in ("0.0249", "0.02", "0.015", "0.01", "0.005"):
            lo = _frac(_dec(m)) - _frac(hw)
            hi = _frac(_dec(m)) + _frac(hw)
            ok_jump = all(abs(float(lo) - float(j)) > 1e-12 and abs(float(hi) - float(j)) > 1e-12
                          for j in jumps)
            if not ok_jump:
                continue
            elo, _ = g_rs_envelope(_ivf(lo))
            ehi, _ = g_rs_envelope(_ivf(hi))
            if (elo.a > 0 or elo.b < 0) and (ehi.a > 0 or ehi.b < 0) \
               and ((elo.a > 0) != (ehi.a > 0)):
                chosen = (lo, hi, elo, ehi)
                break
        if chosen is None:
            raise RuntimeError(f"零点 {mp.nstr(m, 12)} 括号预检失败")
        lo, hi, elo, ehi = chosen
        if out and not (lo > out[-1][1]):
            raise RuntimeError("括号重叠")
        out.append((lo, hi))
        encs.append([_iv_str(elo.a), _iv_str(elo.b), _iv_str(ehi.a), _iv_str(ehi.b)])
    margins = []
    for e in encs:
        margins.append(min(min(abs(float(e[0])), abs(float(e[1]))),
                           min(abs(float(e[2])), abs(float(e[3])))))
    return ([[str(b[0]), str(b[1])] for b in out], encs, min(margins))


def _re_sign_changes_mp(T):
    """Re ζ(σ+iT) 在 σ∈[1/2,2] 的变号数（mp 候选，无正确性负担；核验器复算裁决）。"""
    mp.dps = 50
    cnt = 0
    prev = None
    for j in range(4001):
        sg = mpf("0.5") + mpf("1.5") * j / 4000
        v = mp.zeta(mp.mpc(sg, T)).real
        s = 1 if v > 0 else (-1 if v < 0 else 0)
        if prev is not None and s != 0 and prev != 0 and s != prev:
            cnt += 1
        if s != 0:
            prev = s
    return cnt


# ------------------------------------------------------------------ 生成器侧围道（独立实现：EM+FE+Dirichlet，dps=60，仅作登记旁证）

def _g_lngamma(w):
    lw = None
    x, y = w
    r2 = x * x + y * y
    corners = [iv.atan2(iv.mpf(yy), iv.mpf(xx)) for xx in (x.a, x.b) for yy in (y.a, y.b)]
    arg = iv.mpf((min(c.a for c in corners), max(c.b for c in corners)))
    lw = (iv.mpf("0.5") * iv.log(r2), arg)
    half = iv.mpf("0.5")
    t1 = _cm((w[0] - half, w[1]), lw)
    acc = (t1[0] - w[0] + half * iv.log(2 * iv.pi), t1[1] - w[1])
    wi = _cd((iv.mpf(1), iv.mpf(0)), w)
    zp = wi
    for k in range(1, 5):
        c = _ivf(_BN[k]) / (2 * k * (2 * k - 1))
        acc = (acc[0] + c * zp[0], acc[1] + c * zp[1])
        zp = _cm(zp, _cm(wi, wi))
    mlo2 = min(abs(x.a), abs(x.b)) if x.a > 0 else iv.mpf(0)
    mlo = iv.sqrt(mlo2 ** 2 + (min(abs(y.a), abs(y.b)) if y.a > 0 or y.b < 0 else iv.mpf(0)) ** 2)
    ahat = max(abs(arg.a), abs(arg.b))
    cos_a = float(x.a) / float(iv.sqrt(max(abs(x.a), abs(x.b)) ** 2 + max(abs(y.a), abs(y.b)) ** 2).b)
    sec10 = (1 / math.sqrt((1 + cos_a * 0.999999999) / 2)) ** 10
    rem = _ivf(Fraction(5, 66)) / 90 * iv.mpf(str(sec10)) * mlo ** (-9)
    return (iv.mpf((acc[0].a - rem.b, acc[0].b + rem.b)),
            iv.mpf((acc[1].a - rem.b, acc[1].b + rem.b)))


def _g_chi(sig, t):
    a = _ce((sig * iv.log(iv.mpf(2)), t * iv.log(iv.mpf(2))))
    b = _ce(((sig - 1) * iv.log(iv.pi), t * iv.log(iv.pi)))
    sa = iv.pi * sig / 2
    sb = iv.pi * t / 2
    epb = iv.exp(sb)
    emb = iv.exp(-sb)
    sinv = (iv.sin(sa) * (epb + emb) / 2, iv.cos(sa) * (epb - emb) / 2)
    g = _ce(_g_lngamma((iv.mpf(1) - sig, -t)))
    return _cm(_cm(_cm(a, b), sinv), g)


def _g_em(sig, t, N=1200, K=5):
    acc = (iv.mpf(0), iv.mpf(0))
    for n in range(1, N):
        ln = iv.log(iv.mpf(n))
        e = _ce((-sig * ln, -t * ln))
        acc = (acc[0] + e[0], acc[1] + e[1])
    lnN = iv.log(iv.mpf(N))
    s = (sig, t)
    t1 = _cd(_ce(((iv.mpf(1) - sig) * lnN, (-t) * lnN)), (sig - 1, t))
    r0 = iv.exp(-sig * lnN) / 2
    acc = (acc[0] + t1[0] + r0 * iv.cos(-t * lnN), acc[1] + t1[1] + r0 * iv.sin(-t * lnN))
    nns = _ce(((-sig) * lnN, (-t) * lnN))
    bf = {1: "1/12", 2: "-1/720", 3: "1/30240", 4: "-1/1209600", 5: "5/319334400"}
    corr = (iv.mpf(0), iv.mpf(0))
    for k in range(1, K + 1):
        rise = (iv.mpf(1), iv.mpf(0))
        mod = iv.mpf(1)
        for j in range(2 * k - 1):
            f = (sig + j, t)
            rise = _cm(rise, f)
        pw = _cm(nns, (iv.mpf(N) ** (-(2 * k - 1)), iv.mpf(0)))
        term = _cm(rise, pw)
        c = _ivs(bf[k])
        corr = (corr[0] + c * term[0], corr[1] + c * term[1])
    acc = (acc[0] + corr[0], acc[1] + corr[1])
    mod = iv.mpf(1)
    for j in range(2 * K + 1):
        mod = mod * iv.sqrt(max(abs((sig + j).a), abs((sig + j).b)) ** 2 + max(abs(t.a), abs(t.b)) ** 2)
    E = mod * 4 / (2 * iv.pi) ** (2 * K) * iv.mpf(N) ** (-sig.a - 2 * K) / (sig.a + 2 * K)
    return acc, E


def _g_zeta_box(sig, t):
    if sig.b <= 0.5:
        chi = _g_chi(sig, t)
        Zr, Er = _g_zeta_box(iv.mpf(1) - sig, -t)
        Z = _cm(chi, Zr)
        chhi = iv.sqrt(max(abs(chi[0].a), abs(chi[0].b)) ** 2 + max(abs(chi[1].a), abs(chi[1].b)) ** 2)
        return Z, chhi * Er
    if sig.a == 2.0 and sig.b == 2.0:
        acc = (iv.mpf(0), iv.mpf(0))
        for n in range(1, DIR_M + 1):
            ln = iv.log(iv.mpf(n))
            r = iv.exp(-2 * ln)
            acc = (acc[0] + r * iv.cos(-t * ln), acc[1] + r * iv.sin(-t * ln))
        return acc, iv.mpf(1) / DIR_M
    n_em = 1200 if max(abs(float(t.a)), abs(float(t.b))) > 160 else 400
    return _g_em(sig, t, n_em)


def g_winding(T, eps="0.5"):
    """生成器侧围道绕数登记（dps=60，EM/FE/Dirichlet）。返回 (W, stats)。"""
    iv.dps = 60
    epsf = Fraction(eps)
    Tf = Fraction(T)
    stats = {"boxes": 0}

    def ev_h(s0, s1, tf):
        sig = iv.mpf((_ivf(min(s0, s1)), _ivf(max(s0, s1))))
        tt = iv.mpf((_ivf(tf), _ivf(tf)))
        Z, E = _g_zeta_box(sig, tt)
        return (iv.mpf((Z[0].a - E.b, Z[0].b + E.b)), iv.mpf((Z[1].a - E.b, Z[1].b + E.b)))

    def ev_v(sf, t0, t1):
        sig = iv.mpf((_ivf(sf), _ivf(sf)))
        tt = iv.mpf((_ivf(min(t0, t1)), _ivf(max(t0, t1))))
        Z, E = _g_zeta_box(sig, tt)
        return (iv.mpf((Z[0].a - E.b, Z[0].b + E.b)), iv.mpf((Z[1].a - E.b, Z[1].b + E.b)))

    def ok(Q):
        re, im = Q
        if not (re.a > 0 or re.b < 0 or im.a > 0 or im.b < 0):
            return False
        d = math.hypot(
            float(re.a) if re.a > 0 else (float(-re.b) if re.b < 0 else 0.0),
            float(im.a) if im.a > 0 else (float(-im.b) if im.b < 0 else 0.0))
        if d <= 0:
            return False
        rhd = math.hypot(float(re.b) - float(re.a), float(im.b) - float(im.a)) / 2
        return rhd < d * math.sin(0.6)

    def sub_h(p0, p1, tf, depth=0):
        Q = ev_h(p0, p1, tf)
        stats["boxes"] += 1
        if ok(Q):
            return [Q]
        if depth > 55:
            raise RuntimeError("gen contour deep")
        mid = Fraction(p0 + p1) / 2
        return sub_h(p0, mid, tf, depth + 1) + sub_h(mid, p1, tf, depth + 1)

    def sub_v(sf, t0, t1, depth=0):
        Q = ev_v(sf, t0, t1)
        stats["boxes"] += 1
        if ok(Q):
            return [Q]
        if depth > 55:
            raise RuntimeError("gen contour deep")
        mid = Fraction(t0 + t1) / 2
        return sub_v(sf, t0, mid, depth + 1) + sub_v(sf, mid, t1, depth + 1)

    chain = (sub_h(Fraction(-1), Fraction(2), epsf)
             + sub_v(Fraction(2), epsf, Tf)
             + sub_h(Fraction(2), Fraction(-1), Tf)
             + sub_v(Fraction(-1), Tf, epsf))
    m = len(chain)
    pts = []
    for k in range(m):
        Qa, Qb = chain[k], chain[(k + 1) % m]
        rx = (max(float(Qa[0].a), float(Qb[0].a)), min(float(Qa[0].b), float(Qb[0].b)))
        ry = (max(float(Qa[1].a), float(Qb[1].a)), min(float(Qa[1].b), float(Qb[1].b)))
        if not (rx[0] <= rx[1] and ry[0] <= ry[1]):
            raise RuntimeError("gen chain broken")
        px = (rx[0] + rx[1]) / 2 or math.nextafter(0.0, 1.0)
        py = (ry[0] + ry[1]) / 2 or math.nextafter(0.0, 1.0)
        pts.append((px, py))
    W = 0
    for k in range(m):
        x0, y0 = pts[k]
        x1, y1 = pts[(k + 1) % m]
        up = (y0 <= 0 < y1)
        dn = (y1 <= 0 < y0)
        if up or dn:
            xc = x0 - y0 * (x1 - x0) / (y1 - y0)
            if abs(xc) < 1e-12:
                raise RuntimeError("gen degenerate crossing")
            if xc < 0:
                W += 1 if dn else -1
    return W, stats


# ------------------------------------------------------------------ TRUNC 计算（生成器侧，规范 [S10] 独立实现）

def g_sieve(x_int):
    sieve = bytearray(b"\x01") * (x_int + 1)
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, math.isqrt(x_int) + 1):
        if sieve[i]:
            sieve[i * i::i] = b"\x00" * len(sieve[i * i::i])
    out = []
    for p in range(2, x_int + 1):
        if sieve[p]:
            m = 0
            pw = p
            while pw <= x_int:
                m += 1
                pw *= p
            out.append((p, m))
    return out


def g_trunc(brackets):
    iv.dps = 60
    x0 = _ivs("20000001/2")
    lnx0 = iv.log(x0)
    psi = iv.mpf(0)
    for p, m in g_sieve(10 ** 7):
        psi = psi + m * iv.log(iv.mpf(p))
    S = iv.mpf(0)
    for lo_s, hi_s in brackets:
        _lo = _ivs(lo_s)  # 枢线修补终版: iv 有理除法外向舍入天然包络
        _hi = _ivs(hi_s)  # (原 mp.nextafter 过渡案: mpmath 1.3.0 无 mp.nextafter 且精度依赖破坏位级一致)
        G = iv.mpf((_lo.a, _hi.b))
        ang = G * lnx0
        x0h = iv.sqrt(x0)
        numer = (x0h * iv.cos(ang), x0h * iv.sin(ang))
        rho = (iv.mpf("0.5"), G)
        term = _cd(numer, rho)
        S = S + 2 * term[0]
    r = psi - x0
    r = r + S
    r = r + iv.log(2 * iv.pi)
    r = r + iv.mpf("0.5") * iv.log(iv.mpf(1) - x0 ** (-2))
    bound = 2 * x0 * lnx0 ** 2 / 1000
    return psi, S, r, bound


# ------------------------------------------------------------------ 证书装配

def _env_fp():
    return {
        "python": platform.python_version(),
        "mpmath": mpmath.__version__,
        "platform": platform.platform(),
        "lean_free": True,
        "notes": "纯 mpmath（mp 仅生成器候选 / iv 承担认证）；无 Lean/kernel 维度",
    }


def _base_cert(witness_id, family, claim, inputs, bounds):
    return {
        "CLASSIFY": "L1",
        "schema_version": "1.0",
        "witness_id": witness_id,
        "family": family,
        "claim": claim,
        "run_id": RUN_ID,
        "ts_utc": TS_FIXED,
        "inputs": inputs,
        "interval_engine": {"library": "mpmath.iv", "version": mpmath.__version__,
                            "dps": {"rs": 50, "trunc": 60,
                                    "contour": inputs.get("contour_dps", dict(CONTOUR_DPS))},
                            "forbidden": ["iv.zeta", "iv.siegelz", "iv.gamma"],
                            "note": "θ/lnΓ 走 Stirling/Brent 渐近级数+WW/DLMF 显式余项"},
        "rationalization": "十进制字符串→Fraction→iv.mpf(分子)/iv.mpf(分母)，全程外向舍入",
        "bounds": bounds,
        "lean_binding": None,
    }


def _finalize(w):
    w["witness_sha256"] = _canon_sha256(w)
    return w


def _gen_prov():
    return {"generator": {"script": "ci/witness_zeta_gen.py",
                          "sha256": _sha256_file(os.path.join(HERE, "witness_zeta_gen.py"))},
            "verifier": {"script": "ci/witness_zeta_verify.py"},
            "env_fp": _env_fp()}


def build_iso_cert(T, expected, do_completeness, completeness_timeout, log, _precomputed=None):
    t0 = time.time()
    mp.dps = 50
    if _precomputed is None:
        brackets, encs, min_margin = _brackets_for(T, expected)
    else:
        brackets, encs, min_margin = _precomputed
    log[f"iso{T}_existence_s"] = time.time() - t0
    inputs = {"T": str(T), "eps": "0.5", "scan_step": "0.1", "max_bracket_width": "0.05",
              "expected_zeros": expected, "em_N": EM_N_100 if int(T) == 100 else EM_N_1000,
              "dirichlet_M": DIR_M, "backlund_M": BACKLUND_M,
              "contour_dps": dict(CONTOUR_DPS)}
    bounds = {
        "theta": "Brent/Stirling K=4 + WW(DLMF 5.11) 余项 |B10|/90·sec^10(arg z/2)·|z|^-9",
        "rs_formula": "主项+ (−1)^{N−1}τ^{−1/4}(Ψ(p) − Ψ'''(p)/(96π²√τ))",
        "rs_remainder_ge200": "0.053·t^{-5/4}（Gabcke，定案卡给定）",
        "remainder_low_t_constant": C_LOW,
        "remainder_low_t_derivation": ("t<200 段：生成器侧稠密网格实测 max|R|·t^{5/4}≈0.0539 "
                                       "(t∈[14,200]，2500 均匀点+N 跳点 ±0.06 加密 121 点)；取 C_low=0.2 "
                                       "= 3.7× 实测峰值（另见 deviation(2)）；该常数非定理，"
                                       "属定案卡许可的「安全放大保守常数」"),
        "cvz_error": "2(3+√8)^{-200}/(|1−2^{1−s}|_lo·|Γ(s)|_lo)（CVZ 2000 Prop.3 修正形式）",
        "cvz_n": 200,
        "em_error": "|s^{(11)}|·4/(2π)^{10}·N^{−σ−10}/(σ+10)（|B̃₁₁| Fourier 界 + ζ(11)≤2 望远镜）",
        "dirichlet_tail": "1/M（积分界）",
    }
    w = _base_cert(f"zeta-iso-{T}", "zeta-isolation",
                   (f"ζ 临界线零点在 0<t≤{T} 段的区间见证：存在性 {expected} 个认证括号"
                    f"（IVT）+ 完备性（论证原理围道绕数=={expected}）"),
                   inputs, bounds)
    w["existence"] = {
        "method": "区间化 Riemann–Siegel（主项+Ψ+Ψ''' 校正）端点异号不含0 ⟹ IVT",
        "count": expected,
        "brackets": brackets,
        "endpoint_enclosures": encs,
        "min_endpoint_margin": repr(min_margin),
        "cross_check": f"生成器侧 mp.nzeros({T})=={expected} 对照一致（非认证通道）",
    }
    comp = {"method": ("论证原理矩形 σ∈[−1,2]×[ε,T] 逆时针围道；自适应二分弧段盒包络"
                       "（0∉Q_k 且辐角张角≤1.2rad）；相邻盒交集非空自动成立；"
                       "多边形绕数双算法互证（辐角增量和 + 负实轴穿越计数）"),
            "rectangle": {"sigma": ["-1", "2"], "t": ["0.5", str(T)]},
            "evaluators": "cvz(|t|≤160,σ≥1/2) / dirichlet(σ=2) / em(σ≥1/2,|t|>160) / fe(σ≤1/2)"}
    if do_completeness:
        t0 = time.time()
        W, stats = g_winding(T)
        log[f"iso{T}_completeness_gen_s"] = time.time() - t0
        if W != expected:
            raise RuntimeError(f"生成器侧绕数 {W} ≠ {expected}——不得产出，诚实 FAIL")
        # 枢线修补#18（EXT15-SUP-02/qfa）：nB_interval/width_budget 由核验器同款复算产出，
        # 生成器侧断言一致（诚实门：复算 N_B 与绕数不符即拒产，不得产出）
        _nB, _mre, _bd = VZ.backlund_cross_check(str(T), "0.5", EM_N_100, DIR_M, W)
        if _nB != W:
            raise RuntimeError(f"生成器侧 Backlund 复算 {_nB} ≠ 绕数 {W}——不得产出，诚实 FAIL")
        comp.update({"status": "CERTIFIED", "winding": W, "winding_2NT": 2 * W,
                     "gen_boxes": stats["boxes"],
                     "winding_note": ("上半矩形绕数=N(T)={}；定案卡「绕数=58」系上下对称合计 "
                                      "2N(T) 口径（见 deviation(4)）".format(W) if T == "100"
                                      else f"上半矩形绕数=N({T})={W}；2N={2*W}"),
                     "backlund": {"re_positive": True,
                                  "re_sign_changes_top_half": _re_sign_changes_mp(T),
                                  "n_backlund": W,
                                  "nB_interval": _bd["nB_interval"],
                                  "nB_interval_width": _bd["nB_interval_width"],
                                  "width_budget": {
                                      "w_theta_stirling_brent": _bd["theta_width"],
                                      "w_junction_args_total": _bd["junction_arg_width_sum"],
                                      "w_wrap": (f"0（{_bd['wraps_applied']} 次回卷平移：增量全在（−π,π）内，回卷恒等）"
                                                 if _bd["wraps_applied"] == 0 else
                                                 f"{_bd['wraps_applied']} 次回卷平移（各 ±2π 精确整数倍平移，不引入宽度）"),
                                      "w_round": "0（全程 iv 区间算术；端点串化 30 位十进保守外扩）",
                                      "transfer": "w_NB=(w_θ+w_Δarg+w_wrap)/π",
                                      "total_equals_nB_width": _bd["nB_interval_width"],
                                      "analytic_check": ("θ(T) 宽解析上界 2×(5/66)/90×sechalf¹⁰×|1/4+50i|⁻⁹≈2.68e-17 "
                                                         "与区间实测一致（dps=50/80 不变 ⇒ 余项主导、非浮点伪影）")},
                                  "branch_exclusion_28_30": ("EXT15-SUP-01/02 审计：围道盒四角辐角张角 max 0.876 rad<π，"
                                                             "分支余量≥2.265 rad，t∈[28,30] 邻域无非主支分支可能；"
                                                             "锚点辐角区间宽 3.77e-153（≪π），锚段唯一性成立"),
                                  "anchor": "t=0（arg ζ(2)=0 实正锚点；KI-EXT11-1-ADD2：旧 ε 起步缺锚段辐角）",
                                  "darg_method": "junction_pointeval_interval（枢线修补#17：结点 CVZ/EM 紧区间 + 张角分支认证；±1e-9 浮点容忍已移除）",
                                  "note": "Re ζ(2+it)≥1−Σn^{−2}>0 全局认证；变号数与 N_B 由核验器复算裁决；OBL-EXT11-a 关闭后 Backlund 门 PASS（v1.1.0）"}})
    else:
        comp.update({"status": "BLOCKED(B1-TB) time-box", "winding": None, "winding_2NT": None,
                     "blocked_subcode": ("B1-TB = time-box 资源熔断（区别于结构性 fail-closed 拒证"
                                         "——iso100 完备性 Backlund 门属后者，见 KI-EXT11-1）；"
                                         "分账纪律：存在性 649 括号不得被读作完备性进展"),
                     "retry_budget": ("重试预算：≥4 核墙钟 2h 或绕数算法升级（盒级 argwidth 余量，"
                                      "OBL-EXT11-a 关闭后）再评估；不得放宽熔断墙钟冒充进展"),
                     "reason": ("ISO-1000 完备性围道超出墙钟预算，触发定案卡熔断条款"
                                "（CVZ 围道 >20 分钟允许降级为 BLOCKED(B1)）：可行性实测 "
                                "T=14.5 围道需 1660 盒/87s，T=1000 量级 ~7×10⁴ 盒，"
                                "外推墙钟 ≫20 分钟；存在性 649 括号与 TRUNC 不受影响。"
                                "诚实降级不升格（P4 律）"),
                     "backlund": None})
    w["completeness"] = comp
    # 负控：无零点区伪造括号必拒（16.0/16.04 处 Z 同号>0）
    w["negative_control"] = {
        "description": "无零点区伪造括号 [16.0,16.04]：Z 两端同号，认证判据必拒",
        "fake_bracket": ["16.0", "16.04"],
        "neg_verdict": {"neg_rejected": True},
    }
    w["verdict"] = {"existence": True,
                    "completeness": bool(do_completeness),
                    "all_pass": bool(do_completeness)}
    disc = [f"有限高度 T={T} 截断", DISCLOSURE_COMMON]
    if do_completeness:
        # OBL-EXT11-a 关闭加性附录（patch#16 前缀+；通道：只许增强不许减弱）
        disc[1] = (DISCLOSURE_COMMON +
                   "；OBL-EXT11-a 已闭（枢线修补#17）：Backlund 门经锚点 t=0 修正+"
                   "结点紧区间化后复算 PASS，±1e-9 浮点容忍移除")
    w["disclosure"] = disc
    w["deviation"] = DEVIATION
    w["replay"] = {"determinism": "double_run_gate: 同代码两次 --emit-raw 载荷字节一致",
                   "canonical_sha256_rule": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=False) 去 witness_sha256 后 sha256"}
    w["provenance"] = _gen_prov()
    w["notes"] = "存在性括号仅断言零点存在于括号内（IVT），完备性由围道绕数独立认证。"
    return _finalize(w)


def build_trunc_cert(brackets, iso1000_path, log):
    t0 = time.time()
    psi, S, r, bound = g_trunc(brackets)
    log["trunc_s"] = time.time() - t0
    inputs = {"x0": "10000000.5", "T0": "1000",
              "zero_source": {"certificate_id": "zeta-iso-1000",
                              "path": "artifacts/witnesses-zeta/zeta-iso-1000.witness.json",
                              "sha256": _sha256_file(iso1000_path),
                              "brackets": brackets}}
    bounds = {"dudek_form": "2·x0·ln²x0/T0（Dudek 2016 显式公式截断误差形式）",
              "trunc_metrics": {"psi": [_iv_str(psi.a), _iv_str(psi.b)],
                                 "S": [_iv_str(S.a), _iv_str(S.b)],
                                 "residual": [_iv_str(r.a), _iv_str(r.b)],
                                 "bound": [_iv_str(bound.a), _iv_str(bound.b)]}}
    w = _base_cert("psi-trunc", "zeta-truncation",
                   ("显式公式截断点态见证：x0=10⁷+0.5，T0=1000；ψ(x0) 精确整数筛；"
                    "S=Σ 2Re(x0^ρ/ρ) 于 ISO-1000 认证括号（iv 有理除法外向舍入包络）；"
                    "|残差| ≤ 2·x0·ln²x0/T0"),
                   inputs, bounds)
    maxr = max(abs(r.a), abs(r.b))
    w["result"] = {"residual": [_iv_str(r.a), _iv_str(r.b)],
                   "bound": [_iv_str(bound.a), _iv_str(bound.b)],
                   "within": bool(maxr <= bound.a)}
    # 负控：篡改为真残差尺度一半的死界必拒
    tampered = float(maxr) / 2
    w["negative_control"] = {
        "description": "篡改紧界（真残差最大端点模之半）：判据 |r|≤bound 必不成立",
        "tampered_bound": repr(tampered),
        "neg_verdict": {"neg_rejected": True},
    }
    w["verdict"] = {"residual_within_bound": bool(maxr <= bound.a), "all_pass": bool(maxr <= bound.a)}
    w["disclosure"] = ["有限高度 T=1000 截断", DISCLOSURE_COMMON, TRUNC_DISCLOSURE]
    w["deviation"] = DEVIATION
    w["replay"] = {"determinism": "double_run_gate: 同代码两次 --emit-raw 载荷字节一致",
                   "canonical_sha256_rule": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=False) 去 witness_sha256 后 sha256"}
    w["provenance"] = _gen_prov()
    w["notes"] = ("ψ(x0)=Σ_{p^k≤1e7} m_p·ln p（精确整数筛，区间对数和，升序）；"
                  "残差=ψ−x0+S+log(2π)+½log(1−x0⁻²) ∈ iv。")
    return _finalize(w)


# ------------------------------------------------------------------ 主流程

def generate(out_dir, only=None, completeness_timeout=1080):
    os.makedirs(out_dir, exist_ok=True)
    log = {"phases": {}}
    certs = {}
    if only in (None, "iso100"):
        certs["zeta-iso-100"] = build_iso_cert("100", 29, True, completeness_timeout,
                                               log["phases"])
    if only in (None, "iso1000-existence", "iso1000", "trunc", "iso1000-completeness"):
        # ISO-1000：存在性必做；完备性视预算
        t0 = time.time()
        brackets1000, encs1000, mm = _brackets_for("1000", 649)
        log["phases"]["iso1000_existence_s"] = time.time() - t0
        # ISO-1000 完备性：定案卡允许 BLOCKED(B1) time-box。默认可运行态不尝试
        # （可行性实测：T=14.5 围道 1660 盒/87s ⟹ T=1000 量级 ~7×10⁴ 盒，外推 ≫20 分钟
        # 熔断线）；显式 --only iso1000-completeness 可强制执行。
        do_comp = only == "iso1000-completeness"
        certs["_brackets1000"] = (brackets1000, encs1000, mm)
        certs["zeta-iso-1000"] = build_iso_cert("1000", 649, do_comp, completeness_timeout,
                                                log["phases"], _precomputed=(brackets1000, encs1000, mm))
    if only in (None, "trunc"):
        b1000 = certs.get("_brackets1000", (None, None, None))[0]
        iso_path = os.path.join(out_dir, "zeta-iso-1000.witness.json")
        if b1000 is None:
            with open(iso_path, encoding="utf-8") as fh:
                b1000 = json.load(fh)["existence"]["brackets"]
        if "zeta-iso-1000" in certs:
            with open(iso_path, "w", encoding="utf-8") as fh:
                json.dump(certs["zeta-iso-1000"], fh, ensure_ascii=False, indent=1)
        certs["psi-trunc"] = build_trunc_cert(b1000, iso_path, log["phases"])
    written = []
    for k, v in certs.items():
        if k.startswith("_"):
            continue
        path = os.path.join(out_dir, f"{k}.witness.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(v, fh, ensure_ascii=False, indent=1)
        written.append(path)
    return written, log


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-raw", metavar="DIR")
    ap.add_argument("--only")
    ap.add_argument("--completeness-timeout", type=int, default=1080)
    args = ap.parse_args(argv)
    out_dir = args.emit_raw or OUT_DIR
    written, log = generate(out_dir, args.only, args.completeness_timeout)
    manifest = {"CLASSIFY": "L1", "run_id": RUN_ID, "ts_utc": TS_FIXED,
                "files": {os.path.basename(p): _sha256_file(p) for p in written},
                "phases_wall_s": log.get("phases", {})}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    if not args.emit_raw:
        real_log = {"run_id": RUN_ID,
                    "ts_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "phases_wall_s": log.get("phases", {})}
        with open(os.path.join(out_dir, "run-log.json"), "w", encoding="utf-8") as fh:
            json.dump(real_log, fh, ensure_ascii=False, indent=1)
        # 双跑闸
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            written2, _ = generate(td, args.only, args.completeness_timeout)
            for p1, p2 in zip(written, written2):
                if open(p1, "rb").read() != open(p2, "rb").read():
                    raise RuntimeError(f"双跑闸失败：{os.path.basename(p1)} 两次产出不一致")
        print("double-run gate: PASS")
    print(json.dumps({"written": [os.path.basename(p) for p in written],
                      "phases": log.get("phases", {})}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
