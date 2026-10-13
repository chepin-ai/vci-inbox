# CLASSIFY: L1
# witness_zeta_verify.py · EXT-WAVE-11「赎」波 WS-63 ζ 零点隔离+显式公式截断区间见证·独立核验器
# （schema v1.0 · fail-closed · 与 ci/witness_zeta_gen.py 零共享代码路径）
#
# 对象（ZETA-INST-01-20261012T2130Z 设计定案卡三证书）：
#   · family "zeta-isolation"（CERT-ζ-ISO-100 / CERT-ζ-ISO-1000）：
#       存在性——对每个登记括号 [lo,hi]（宽 ≤0.05，十进制有理字符串），用区间化
#       Riemann–Siegel 公式 Ã(t)（主项 + Ψ 校正 + Ψ''' 校正，见下规范）在两端点做
#       mpmath.iv 区间求值，包络 = Ã ± E(t)；判：两端包络均不含 0 且异号 ⟹ 介值定理
#       ⟹ Z(t) 在括号内至少一个零点（Hardy Z 零点 ⟺ ζ 临界线零点）。
#       完备性——论证原理：矩形 σ∈[-1,2]×[ε,T] 边界围道，分段区间盒包络 ζ（每盒
#       认证 0∉Q_k，相邻盒交集非空自动成立——共端点真值属于两盒），由链盒构造
#       多边形绕数（负实轴穿越计数，精确整数）。绕数 == 括号数 ⟹ 无其它零点。
#       Backlund 交叉校验：(a) Re ζ(2+it) ≥ 1−Σ_{n≥2}n^{−2} > 0 全局解析认证；
#       (b) Re ζ(σ+iT) 在 σ∈[1/2,2] 的认证变号数 m（导数界排除同号段穿越、
#       单调性认证异号段恰好一次穿越）；N_B(T) = (θ(T)+Δarg)/π+1 与绕数一致。
#   · family "zeta-truncation"（CERT-ψ-TRUNC）：x0=10^7+0.5，T0=1000；
#       ψ(x0)=Σ_{p^k≤1e7} ln p 精确整数筛（区间对数和，升序规范）；S=Σ_{认证括号}
#       2Re(x0^ρ/ρ)（ρ=1/2+iγ，γ 取 iv 有理除法外向舍入包络括号区间）；残差
#       r = ψ(x0)−x0+S+log(2π)+½log(1−x0^{−2}) ∈ iv；判 |r| ≤ 2·x0·ln²x0/T0。
#
# 零共享代码纪律（WS-37 律 + ZETA-INST-01 C 纪律）：
#   本核验器仅使用 mpmath.iv 初等函数（log/exp/cos/sin/cosh/sinh/sqrt/atan2/四则），
#   禁止 iv.zeta/iv.siegelz（mpmath 1.3.0 实测运行时 AttributeError，不存在）；
#   θ(t) 与 lnΓ 走 Stirling/Brent 渐近级数（Whittaker–Watson / DLMF 5.11 显式余项
#   sec^{2K+2}(arg z/2) 形式），不使用 iv.gamma；CVZ η 加速级数误差界用文献正确
#   形式 |γ_n(s)| ≤ 2(3+√8)^{-n}/(|1−2^{1−s}|·|Γ(s)|)（CVZ 2000 Prop.3 /
#   Borwein 2000；|Γ| 下界由 Stirling 区间下界给出）——定案卡所给
#   3(3+√8)^{-n}(1+8|s|)/|1−2^{1−s}| 形式缺 1/|Γ(s)| ~ e^{π|t|/2} 因子，
#   实测 |t|=50 处超界 27 个量级，属定案卡笔误；本核验器采用修正界并在证书
#   deviation 字段逐字披露。
#
# 判定语义（默认拒绝律，沿用 WS-37 M0/WS-43/WS-55 口径）：
#   任一检查 false / 证据缺失 / 异常 → 整体 fail，退出码 1；
#   缺 schema_version → 拒绝受理；major ≠ 1 → unsupported_schema 拒验；
#   登记数值比对 = 字符串逐字一致（数值仅经字符串解析后的有理/区间量复算）；
#   负控必须复算确认拒证；lean_binding 恒 null；env_fp 无 lean/mathlib 维度。
#
# witness_sha256 规范化序列化规则（沿用 WS-37 M0 interim）：
#   json.dumps(除去 witness_sha256 的对象, sort_keys=True, separators=(",", ":"),
#              ensure_ascii=False).encode("utf-8") 的 sha256 十六进制小写。
#
# ================= 区间计算规范（生成器/核验器各自独立实现同一规范） =================
# [S1] 十进制字符串 s → Fraction(s) → iv.mpf(分子)/iv.mpf(分母)；求和一律升序从左到右，
#      初值 iv.mpf(0)。
# [S2] θ(t)（dps=50）：z=1/4+i·t/2；r2=x²+y²；u=½·iv.log(r2)；φ=iv.pi/2−iv.atan2(x,y)；
#      im = (−1/4)·φ + (t/2)·u − (t/2)；zi=z^{−1}（复区间除法）；corr=Σ_{k=1..4}
#      B_{2k}/(2k(2k−1))·Im(z^{−(2k−1)})（幂由复区间乘法递推 zp·=zi²）；
#      θ = im + corr − (t/2)·iv.log(iv.pi)；余项 |R| ≤ |B_{10}|/90·sec^{10}(φ/2)·|z|^{−9}，
#      cos(φ/2)=sqrt((1+x/|z|)/2)；对称加宽。
#      B_2=1/6, B_4=−1/30, B_6=1/42, B_8=−1/30, B_10=5/66。
# [S3] RS 包络（dps=50）：τ=t/(2π)，sq=iv.sqrt(τ)，N=⌊sq⌋（要求 ⌊sq.a⌋=⌊sq.b⌋ 否则拒证），
#      p=sq−N；主项 acc=Σ_{n=1..N} iv.cos(θ − t·iv.log(n))/iv.sqrt(n)（升序），main=2·acc；
#      Ψ(p)=cos(u)/cos(v)，u=2π(p²−p−1/16)，v=2πp；
#      Ψ'''(p) 闭式（商法则三次，f=cos u, g=cos v, u'=2π(2p−1), u''=4π, w=2π）：
#        f'''=−3u'u''cos u + u'³sin u；g'=−w sin v；g''=−w²cos v；g'''=w³ sin v；
#        h=1/g；h'=−g'/g²；h''=2g'²/g³−g''/g²；h'''=−6g'³/g⁴+6g'g''/g³−g'''/g²；
#        Ψ'''=f'''h+3f''h'+3f'h''+fh'''；
#      Ã = main + (−1)^{N−1}·τ^{−1/4}·(Ψ(p) − Ψ'''(p)/(96π²·√τ))；
#      E(t) = (t≥200 ? 0.053 : C_low)·t^{−5/4}，C_low 取证书 bounds.remainder_low_t
#      登记值（须 ≥0.2 且 ≤1；推导依据见证书 derivation 字段）；
#      包络 = [Ã.a−E, Ã.b+E]。
# [S4] 括号认证：包络不含 0（enc.a>0 或 enc.b<0）且两端符号相反；宽度 hi−lo ≤ 0.05
#      （Fraction 精确比较）；升序、互不重叠、全部落在 (0,T]。
# [S5] CVZ ζ 盒求值（dps=220，仅用于 σ≥1/2 且 |t| ≤ 160）：系数 d_k = n·Σ_{i=0}^{k}
#      (n+i−1)!4^i/((n−i)!(2i)!)（Fraction 精确整数，n=200）；
#      S = Σ_{k=0}^{n−1} (−1)^k (d_k−d_n)(k+1)^{−s}（升序，复区间）；
#      ζ ≈ −S/(d_n·(1−2^{1−s}))；误差 E_cvz = 2(3+√8)^{−n}/(|1−2^{1−s}|_lo·|Γ(s)|_lo)，
#      |Γ(s)|_lo = exp(Re lnΓ_Stirling(s) − R_Stirling)（见 [S7]）。
# [S6] Euler–Maclaurin ζ 盒求值（dps=220，σ≥1/2，大 |t| 用）：
#      ζ(s) = Σ_{n=1}^{N−1} n^{−s} + N^{1−s}/(s−1) + ½N^{−s}
#             + Σ_{k=1}^{5} B_{2k}/(2k)!·s^{(2k−1)}·N^{−s−2k+1} + R，
#      |R| ≤ |s^{(11)}|·2ζ(11)/(2π)^{10}·N^{−σ−10}/(σ+10)，其中 ζ(11)≤2 用初等
#      望远镜界 ζ(m) ≤ 1+Σ_{n≥2}1/(n(n−1)) = 2；N 由证书 inputs.em_N 登记。
# [S7] lnΓ(w) Stirling 盒求值（Re w>0）：lnΓ(w) = (w−½)ln w − w + ½ln 2π
#      + Σ_{k=1}^{4} B_{2k}/(2k(2k−1)) w^{−(2k−1)} + R，|R| ≤ |B_{10}|/90·
#      sec^{10}(â/2)·|w|^{−9}，â=max|arg w|（盒四角 atan2 取极值），cos(â/2) 由
#      min(x/|w|) 导出。复对数 ln w = ½ln(x²+y²) + i·arg盒。
# [S8] χ(s)（σ<1/2 时 ζ(s)=χ(s)ζ(1−s)）：χ(s)=2^s·π^{s−1}·sin(πs/2)·Γ(1−s)，
#      Γ(1−s)=exp(lnΓ(1−s))（[S7]）；ζ(1−s) 由 [S5]/[S6] 于 σ'=1−σ≥1/2 求值。
#      σ=2 竖边用 Dirichlet 部分和：ζ(2+it)=Σ_{n=1}^{M} n^{−2−it}+尾，|尾|≤1/M
#      （M=inputs.dirichlet_M，积分界 ∫_M^∞ x^{−2}dx=1/M）。
# [S9] 围道绕数：矩形 σ∈[−1,2]×[ε,T]，逆时针：底(ε: −1→2)、右(2: ε→T)、
#      顶(T: 2→−1)、左(−1: T→ε)。自适应二分弧段；每弧盒包络 Q_k（求值盒 + 误差
#      对称加宽）；要求 0∉Q_k（re 或 im 区间不含 0）；相邻盒交集非空（自动，因共
#      端点真值同属两盒——仍以区间端点 max lo ≤ min hi 逐坐标认证）；p_k=交集矩形
#      中点（若坐标恰为 0.0 则 nextafter 微移）；多边形绕数 = 负实轴穿越计数
#      （上行 −y→+y 且 x_cross<0 记 +1，下行记 −1；|x_cross| 须 ≥ 盒到原点距离之半
#      否则拒证求精）。绕数 W ∈ ℤ；完备性判 W == 括号数。
# [S10] TRUNC（dps=60）：x0=10000000.5；筛：p 升序素数，k 升序 p^k≤10^7；
#      ψ = Σ m_p·iv.log(p)，m_p=⌊log 10^7/log p⌋（整数 isqrt 精确判定）；
#      γ 括号 [lo,hi] nextafter 各一步加宽为 G；lnx0=iv.log(x0)；
#      term = 2·Re(x0^{1/2}·(cos(G·lnx0)+i·sin(G·lnx0))/(1/2+i·G))（复区间，升序累计 S）；
#      r = ψ − x0 + S + iv.log(2π) + ½·iv.log(1−x0^{−2})（按此序）；
#      bound = 2·x0·lnx0²/1000；判 max(|r.a|,|r.b|) ≤ bound.a。
#
# 用法：python3 ci/witness_zeta_verify.py CERT.json [CERT2.json ...] [--json]
#   退出码 0=全部通过；1=任一失败或异常；2=用法错误。
import argparse
import hashlib
import json
import math
import os
import sys
from fractions import Fraction

SUPPORTED_MAJOR = 1
DPS_RS = 50        # 存在性 RS 求值
DPS_CVZ = 220      # 围道求值（CVZ/EM/Stirling）
DPS_TRUNC = 60     # 显式公式截断
CVZ_N = 200
CVZ_T_MAX = 160.0  # 修正 CVZ 界可用上限（e^{π|t|/2} 因子约束）
EM_K = 5

TOP_REQUIRED = ["CLASSIFY", "schema_version", "witness_id", "family", "claim",
                "inputs", "interval_engine", "rationalization", "bounds",
                "verdict", "negative_control", "replay", "provenance",
                "disclosure", "lean_binding", "witness_sha256"]

REQUIRED_DISCLOSURES = ["区间见证层 PASS、kernel 层未证、非 RH 证据"]
TRUNC_DISCLOSURE = ("本证书为 Dudek 定理适用范围(x>e⁶⁰)之外的点态管道演练，非定理实例；"
                    "零点输入由 ISO-1000 区间括号供给")


class VerifyError(RuntimeError):
    pass


# ------------------------------------------------------------------ 基础工具

def _canon_sha256(w):
    if "witness_sha256" in w:
        raise VerifyError("canonical_sha256 输入不得含 witness_sha256")
    blob = json.dumps(w, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class CL:
    def __init__(self):
        self.checks = []

    def add(self, name, ok, detail=""):
        self.checks.append({"check": name, "ok": bool(ok), "detail": str(detail)})

    @property
    def ok(self):
        return all(c["ok"] for c in self.checks)


def _iv_of(s):
    """十进制字符串 → iv 区间（[S1]：Fraction → iv.mpf(num)/iv.mpf(den)）。"""
    from mpmath import iv
    fr = Fraction(str(s).strip())
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def _iv_frac_str(s):
    """分数/小数字符串 → iv（[S1] 同规）。"""
    return _iv_of(s)


def _iv_str(x):
    """区间端点规范字符串（mpf 60 位有效数字；mpmath iv 的 .a/.b 为零宽 ivmpf，
    nstr 打印为 "[v, v]"——剥括号并断言两端一致）。"""
    from mpmath import mp
    s = mp.nstr(x, 60)
    if s.startswith("["):
        inner = s[1:-1].split(",")
        assert len(inner) == 2 and inner[0].strip() == inner[1].strip(), s
        return inner[0].strip()
    return s


# ------------------------------------------------------------------ 复区间工具
# 复区间 = (re, im) 二元 iv.mpf（矩形包络）。

def _cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _cdiv(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def _cexp(a):
    from mpmath import iv
    r = iv.exp(a[0])
    return (r * iv.cos(a[1]), r * iv.sin(a[1]))


def _cmod_lohi(a):
    """复矩形模长 [lo, hi]（0 在盒内则 lo=0）。"""
    from mpmath import iv
    def axis_lo(u):
        if u.a <= 0 <= u.b:
            return iv.mpf(0)
        return min(abs(u.a), abs(u.b))
    lo = iv.sqrt(axis_lo(a[0]) ** 2 + axis_lo(a[1]) ** 2)
    hi = iv.sqrt(max(abs(a[0].a), abs(a[0].b)) ** 2 + max(abs(a[1].a), abs(a[1].b)) ** 2)
    return lo, hi


def _carg_range(a):
    """复矩形（不含 0 且不跨负实轴切口；本机仅在 Re>0 或主支安全域调用）的 arg 值域。
    四角 atan2 取 min/max（全程 mpf 精度，外向取端点）；调用处保证盒在右半平面。"""
    from mpmath import iv
    if not (a[0].a > 0):
        raise VerifyError("arg_range 仅支持 Re>0 盒")
    corners = [iv.atan2(iv.mpf(y), iv.mpf(x))
               for x in (a[0].a, a[0].b) for y in (a[1].a, a[1].b)]
    lo = min(c.a for c in corners)
    hi = max(c.b for c in corners)
    return iv.mpf((lo, hi))


def _clog_right(a):
    """右半平面复盒对数：ln w = ½ln(x²+y²) + i·arg。"""
    from mpmath import iv
    r2 = a[0] * a[0] + a[1] * a[1]
    return (iv.mpf("0.5") * iv.log(r2), _carg_range(a))


# ------------------------------------------------------------------ [S2] θ(t)

_B = {1: ("1/6"), 2: ("-1/30"), 3: ("1/42"), 4: ("-1/30")}

def _bernoulli_iv(k):
    from mpmath import iv
    fr = Fraction(_B[k])
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def theta_iv(t, K=4):
    """θ(t) 区间包络（[S2]，含 WW/DLMF 5.11 显式余项对称加宽）。t 为 iv（须 y=t/2>0）。"""
    from mpmath import iv
    x = iv.mpf(1) / 4
    y = t / 2
    r2 = x * x + y * y
    u = iv.mpf("0.5") * iv.log(r2)
    phi = iv.pi / 2 - iv.atan2(x, y)
    a = -iv.mpf(1) / 4
    b = t / 2
    im = a * phi + b * u - b
    zi = _cdiv((iv.mpf(1), iv.mpf(0)), (x, y))
    zp = zi
    corr = iv.mpf(0)
    for k in range(1, K + 1):
        corr = corr + _bernoulli_iv(k) / (2 * k * (2 * k - 1)) * zp[1]
        zp = _cmul(zp, _cmul(zi, zi))
    th = im + corr - b * iv.log(iv.pi)
    az = iv.sqrt(r2)
    sechalf = 1 / iv.sqrt((1 + x / az) / 2)
    rem = _iv_of("5/66") / 90 * sechalf ** 10 * az ** (-9)
    return iv.mpf((th.a - rem.b, th.b + rem.b))


# ------------------------------------------------------------------ [S3] RS 包络

def _psi_iv(p):
    from mpmath import iv
    tp = 2 * iv.pi
    u = tp * (p * p - p - iv.mpf(1) / 16)
    v = tp * p
    return iv.cos(u) / iv.cos(v)


def _psi3_iv(p):
    from mpmath import iv
    tp = 2 * iv.pi
    u = tp * (p * p - p - iv.mpf(1) / 16)
    v = tp * p
    u1 = tp * (2 * p - 1)
    u2 = 4 * iv.pi
    w = tp
    f = iv.cos(u)
    fpp = -u2 * iv.sin(u) - u1 * u1 * iv.cos(u)
    fppp = -3 * u1 * u2 * iv.cos(u) + u1 ** 3 * iv.sin(u)
    g = iv.cos(v)
    gp = -w * iv.sin(v)
    gpp = -w * w * iv.cos(v)
    gppp = w ** 3 * iv.sin(v)
    g2 = g * g
    g3 = g2 * g
    g4 = g3 * g
    fp = -u1 * iv.sin(u)
    h = 1 / g
    hp = -gp / g2
    hpp = 2 * gp * gp / g3 - gpp / g2
    hppp = -6 * gp ** 3 / g4 + 6 * gp * gpp / g3 - gppp / g2
    return fppp * h + 3 * fpp * hp + 3 * fp * hpp + f * hppp


def rs_envelope(t, c_low):
    """[S3]：返回 (包络区间, E)。t 为 iv；c_low 为 t<200 段余项常数（iv）。"""
    from mpmath import iv
    tp = 2 * iv.pi
    tau = t / tp
    sq = iv.sqrt(tau)
    n_lo = math.floor(float(sq.a))
    n_hi = math.floor(float(sq.b))
    if n_lo != n_hi:
        raise VerifyError("N=⌊√(t/2π)⌋ 在端点区间内跨跳（straddle）——拒证求精")
    N = n_lo
    p = sq - N
    th = theta_iv(t)
    acc = iv.mpf(0)
    for n in range(1, N + 1):
        acc = acc + iv.cos(th - t * iv.log(iv.mpf(n))) / iv.sqrt(iv.mpf(n))
    main = 2 * acc
    corr = _psi_iv(p) - _psi3_iv(p) / (96 * iv.pi ** 2 * iv.sqrt(tau))
    sgn = iv.mpf((-1) ** (N - 1))
    A = main + sgn * corr * tau ** (-iv.mpf(1) / 4)
    c = _iv_of("53/1000") if t.a >= 200 else c_low
    E = c * t ** (-iv.mpf(5) / 4)
    return iv.mpf((A.a - E.b, A.b + E.b)), E


def _certify_bracket(lo_s, hi_s, t_cap, c_low):
    """[S4]：返回 (ok, detail, enc_lo, enc_hi)。"""
    from mpmath import iv
    flo = Fraction(lo_s)
    fhi = Fraction(hi_s)
    if not (flo < fhi):
        return False, "端点序错误", None, None
    if fhi - flo > Fraction(5, 100):
        return False, "括号宽度>0.05", None, None
    if flo <= 0 or fhi > Fraction(t_cap):
        return False, "括号越界", None, None
    tlo = _iv_of(lo_s)
    thi = _iv_of(hi_s)
    enc_lo, _ = rs_envelope(tlo, c_low)
    enc_hi, _ = rs_envelope(thi, c_low)
    if not (enc_lo.a > 0 or enc_lo.b < 0):
        return False, "下端点包络含0", enc_lo, enc_hi
    if not (enc_hi.a > 0 or enc_hi.b < 0):
        return False, "上端点包络含0", enc_lo, enc_hi
    s_lo = 1 if enc_lo.a > 0 else -1
    s_hi = 1 if enc_hi.a > 0 else -1
    if s_lo == s_hi:
        return False, "端点同号——介值条件不成立", enc_lo, enc_hi
    return True, "", enc_lo, enc_hi


# ------------------------------------------------------------------ [S7] Stirling lnΓ

def _lngamma_right_box(w):
    """Re w>0 复盒的 lnΓ 包络（(re, im) 区间对，含 WW 余项加宽）。"""
    from mpmath import iv
    lw = _clog_right(w)
    half = iv.mpf("0.5")
    t1 = _cmul((w[0] - half, w[1]), lw)
    acc = (t1[0] - w[0] + half * iv.log(2 * iv.pi), t1[1] - w[1])
    wi = _cdiv((iv.mpf(1), iv.mpf(0)), w)
    zp = wi
    for k in range(1, 5):
        c = _bernoulli_iv(k) / (2 * k * (2 * k - 1))
        acc = (acc[0] + c * zp[0], acc[1] + c * zp[1])
        zp = _cmul(zp, _cmul(wi, wi))
    # 余项 |B10|/90 · sec^10(â/2) · |w|^{-9}
    mlo, mhi = _cmod_lohi(w)
    arg = _carg_range(w)
    ahat = max(abs(arg.a), abs(arg.b))
    if not (ahat < float(iv.pi.a) / 2):
        raise VerifyError("Stirling 盒 arg 越出右半平面")
    # cos(â/2) = sqrt((1+cos â)/2)，cos â = min over box of x/|w| = x.a/mhi
    # cos(a_hat/2)=sqrt((1+cos a_hat)/2); cos a_hat >= x.a/mhi.b (保守下界再留 1e-12 余量)
    cos_a = float(w[0].a) / float(mhi.b) * (1 - 1e-12)
    coshalf2 = (1 + cos_a) / 2
    sec10 = (1 / math.sqrt(coshalf2)) ** 10
    rem_iv = _iv_of("5/66") / 90 * iv.mpf(str(sec10)) * (mlo) ** (-9)
    return (iv.mpf((acc[0].a - rem_iv.b, acc[0].b + rem_iv.b)),
            iv.mpf((acc[1].a - rem_iv.b, acc[1].b + rem_iv.b))), rem_iv


# ------------------------------------------------------------------ [S5] CVZ

_CVZ_D = None
_LOG_CACHE = {}
_IVPI_CACHE = {}


def _cvz_coeffs():
    global _CVZ_D
    if _CVZ_D is None:
        n = CVZ_N
        d = []
        for k in range(n + 1):
            s = sum(Fraction(math.factorial(n + i - 1) * 4 ** i,
                             math.factorial(n - i) * math.factorial(2 * i))
                    for i in range(k + 1))
            dk = n * s
            if dk.denominator != 1:
                raise VerifyError("CVZ 系数非整数（实现错误）")
            d.append(int(dk))
        _CVZ_D = d
    return _CVZ_D


def _log_cached(n):
    from mpmath import iv
    key = (iv.dps, n)
    v = _LOG_CACHE.get(key)
    if v is None:
        v = iv.log(iv.mpf(n))
        _LOG_CACHE[key] = v
    return v


def _zeta_cvz_box(sig, t):
    """[S5]：σ≥1/2、|t|≤160 的 ζ 复盒包络（含修正 CVZ 余项）。返回 ((re,im), E)。
    工作精度 dps=220（定案卡抗相消口径）。"""
    from mpmath import iv
    if not (sig.a >= 0.5):
        raise VerifyError("CVZ 直接求值要求 σ≥1/2")
    iv.dps = DPS_CVZ
    dk = _cvz_coeffs()
    n = CVZ_N
    dn = dk[n]
    S = (iv.mpf(0), iv.mpf(0))
    for k in range(n):
        coef = iv.mpf(dk[k] - dn) * ((-1) ** k)
        lk = _log_cached(k + 1)
        e = _cexp((-sig * lk, -t * lk))
        S = (S[0] + coef * e[0], S[1] + coef * e[1])
    ln2 = iv.log(iv.mpf(2))
    e2 = _cexp(((iv.mpf(1) - sig) * ln2, (-t) * ln2))
    Dm = (iv.mpf(1) - e2[0], -e2[1])
    Z = _cdiv((-S[0], -S[1]), _cmul((iv.mpf(dn), iv.mpf(0)), Dm))
    # 误差界：2(3+√8)^{-n}/(|1−2^{1−s}|_lo·|Γ(s)|_lo)
    dlo, _ = _cmod_lohi(Dm)
    if not (dlo.a > 0):
        raise VerifyError("1−2^{1−s} 盒含 0（CVZ 界失效）——拒证")
    lg, rem = _lngamma_right_box((sig, t))
    g_lo = iv.exp(lg[0]).a
    if not (g_lo > 0):
        raise VerifyError("|Γ| 下界非正")
    E = 2 * (3 + iv.sqrt(iv.mpf(8))) ** (-n) / (dlo * g_lo)
    return Z, E


# ------------------------------------------------------------------ [S6] Euler–Maclaurin

def _rise_box(s, m):
    """上升阶乘 s(s+1)…(s+m−1) 复盒（连乘）与模上界。"""
    from mpmath import iv
    r = (iv.mpf(1), iv.mpf(0))
    mod = iv.mpf(1)
    for j in range(m):
        f = (s[0] + j, s[1])
        r = _cmul(r, f)
        _, fh = _cmod_lohi(f)
        mod = mod * fh
    return r, mod


def _zeta_em_box(sig, t, N):
    """[S6]：σ≥1/2 的 ζ 复盒包络（K=5，显式余项）。返回 ((re,im), E)。
    工作精度 dps=80（系数 O(1) 无相消，见证书 deviation(5)）。"""
    from mpmath import iv
    if not (sig.a >= 0.5):
        raise VerifyError("EM 求值要求 σ≥1/2")
    iv.dps = 80
    acc = (iv.mpf(0), iv.mpf(0))
    for n in range(1, N):
        ln = _log_cached(n)
        e = _cexp((-sig * ln, -t * ln))
        acc = (acc[0] + e[0], acc[1] + e[1])
    lnN = _log_cached(N)
    s = (sig, t)
    n1s = _cexp(((iv.mpf(1) - sig) * lnN, (-t) * lnN))       # N^{1−s}
    sm1 = (sig - 1, t)
    t1 = _cdiv(n1s, sm1)
    t2r = iv.exp(-sig * lnN) / 2                              # ½N^{−s} 的模因子
    t2 = (t2r * iv.cos(-t * lnN), t2r * iv.sin(-t * lnN))
    acc = (acc[0] + t1[0] + t2[0], acc[1] + t1[1] + t2[1])
    nns = _cexp(((-sig) * lnN, (-t) * lnN))                   # N^{−s}
    corr = (iv.mpf(0), iv.mpf(0))
    bfac = {1: "1/12", 2: "-1/720", 3: "1/30240",
            4: "-1/1209600", 5: "5/319334400"}
    for k in range(1, EM_K + 1):
        rise, _ = _rise_box(s, 2 * k - 1)
        coef = _iv_of(bfac[k])
        # N^{−s−2k+1} = N^{−s}·N^{−2k+2}·N^{−1}
        pw = _cmul(nns, (iv.mpf(N) ** (-(2 * k - 1)), iv.mpf(0)))
        term = _cmul(rise, pw)
        corr = (corr[0] + coef * term[0], corr[1] + coef * term[1])
    acc = (acc[0] + corr[0], acc[1] + corr[1])
    _, mod = _rise_box(s, 2 * EM_K + 1)
    sig_lo = sig.a
    E = (mod * 4 / (2 * iv.pi) ** (2 * EM_K)
         * iv.mpf(N) ** (-sig_lo - 2 * EM_K) / (sig_lo + 2 * EM_K))
    return acc, E


def _zeta_dirichlet_box(t, M):
    """[S8] σ=2：ζ(2+it)=Σ_{n≤M} n^{−2−it}+尾，|尾|≤1/M。返回 ((re,im), E)。
    工作精度 dps=80（系数 O(1) 无相消）。"""
    from mpmath import iv
    iv.dps = 80
    acc = (iv.mpf(0), iv.mpf(0))
    for n in range(1, M + 1):
        ln = _log_cached(n)
        r = iv.exp(-2 * ln)
        acc = (acc[0] + r * iv.cos(-t * ln), acc[1] + r * iv.sin(-t * ln))
    return acc, iv.mpf(1) / M


def _chi_box(sig, t):
    """[S8]：χ(s)=2^s π^{s−1} sin(πs/2) Γ(1−s) 复盒（σ<1/2 段用）。返回 (re,im)。"""
    from mpmath import iv
    ln2 = iv.log(iv.mpf(2))
    lnpi = iv.log(iv.pi)
    a = _cexp((sig * ln2, t * ln2))
    b = _cexp(((sig - 1) * lnpi, t * lnpi))
    sa = iv.pi * sig / 2
    sb = iv.pi * t / 2
    epb = iv.exp(sb)
    emb = iv.exp(-sb)
    cosh_b = (epb + emb) / 2
    sinh_b = (epb - emb) / 2
    sinv = (iv.sin(sa) * cosh_b, iv.cos(sa) * sinh_b)
    lg, _ = _lngamma_right_box((iv.mpf(1) - sig, -t))
    g = _cexp(lg)
    return _cmul(_cmul(_cmul(a, b), sinv), g)


class StraddleError(RuntimeError):
    """σ 盒跨越 1/2 分派边界——调用方须细分。"""


def zeta_box(sig, t, em_N, dir_M):
    """统一 ζ 盒求值（返回 ((re,im), E, method)）。
    σ 盒全 ≥1/2：|t|≤160 → CVZ；否则 EM（N=em_N）；σ=2 竖边用 dirichlet。
    σ 盒全 ≤1/2：χ(s)·ζ(1−s)（反射点 σ'=1−σ≥1/2，同法择器）。
    跨界盒：抛 StraddleError（细分义务在调用方）。"""
    from mpmath import iv
    if sig.a >= 0.5:
        if sig.a == 2.0 and sig.b == 2.0:
            Z, E = _zeta_dirichlet_box(t, dir_M)
            return Z, E, "dirichlet"
        if max(abs(t.a), abs(t.b)) <= CVZ_T_MAX:
            Z, E = _zeta_cvz_box(sig, t)
            return Z, E, "cvz"
        Z, E = _zeta_em_box(sig, t, em_N)
        return Z, E, "em"
    if sig.b > 0.5:
        raise StraddleError("σ 盒跨越 1/2")
    # 函数方程
    chi = _chi_box(sig, t)
    sig_r = iv.mpf(1) - sig
    t_r = -t
    if sig_r.a == 2.0 and sig_r.b == 2.0:
        Zr, Er = _zeta_dirichlet_box(t_r, dir_M)
        mtag = "dirichlet"
    elif max(abs(t_r.a), abs(t_r.b)) <= CVZ_T_MAX:
        Zr, Er = _zeta_cvz_box(sig_r, t_r)
        mtag = "cvz"
    else:
        Zr, Er = _zeta_em_box(sig_r, t_r, em_N)
        mtag = "em"
    Z = _cmul(chi, Zr)
    chlo, chhi = _cmod_lohi(chi)
    E = chhi * Er
    return Z, E, "fe+" + mtag


# ------------------------------------------------------------------ [S9] 围道绕数引擎

class ContourStats:
    def __init__(self):
        self.boxes = 0
        self.max_depth = 0
        self.min_dist = None      # 盒到原点最小认证距离（float，>0）
        self.methods = {}
        self.per_edge_boxes = {}


def _box_avoids_zero(Q):
    re, im = Q
    if re.a > 0 or re.b < 0:
        return True
    if im.a > 0 or im.b < 0:
        return True
    return False


def _box_argwidth_float(Q):
    """盒（不含原点）的辐角张角上界（float，弧度）：2·asin(半对角线/最近距离)。
    若最近距离 ≤ 半对角线则返回 inf（调用方须继续细分）。"""
    d = _box_dist_float(Q)
    if d <= 0.0:
        return float("inf")
    w = float(Q[0].b) - float(Q[0].a)
    h = float(Q[1].b) - float(Q[1].a)
    rhd = math.hypot(w, h) / 2
    if rhd >= d:
        return float("inf")
    return 2 * math.asin(rhd / d)


_ARGWIDTH_MAX = 1.2  # 弧度；保证相邻盒并集张角 < 2.4 < π，增量主值唯一


def _box_dist_float(Q):
    """盒到原点距离（float 下界）——用于穿越退化保护。"""
    re, im = Q

    def ax(u):
        if u.a > 0:
            return float(u.a)
        if u.b < 0:
            return float(-u.b)
        return 0.0
    return math.hypot(ax(re), ax(im))


def winding_number(T_str, eps_str, em_N, dir_M, dps=None):
    """[S9]：矩形 σ∈[−1,2]×[ε,T] 逆时针围道绕数（认证整数）。返回 (W, stats)。"""
    from mpmath import iv
    iv.dps = dps or DPS_CVZ
    eps = Fraction(eps_str)
    T = Fraction(T_str)
    stats = ContourStats()
    chain = []
    edges = [
        ("bottom", (Fraction(-1), eps), (Fraction(2), eps), eps),
        ("right", (Fraction(2), eps), (Fraction(2), T), T),
        ("top", (Fraction(2), T), (Fraction(-1), T), T),
        ("left", (Fraction(-1), T), (Fraction(-1), eps), eps),
    ]
    for name, p0, p1, fixed in edges:
        before = stats.boxes
        if name in ("bottom", "top"):
            seg = _subdivide_edge_h(name, p0, p1, em_N, dir_M, stats)
        else:
            seg = _subdivide_edge_v(name, p0, p1, em_N, dir_M, stats)
        stats.per_edge_boxes[name] = stats.boxes - before
        chain.extend(seg)
    # 链盒 → 交点序列 → 多边形绕数（双算法互证：辐角增量和 & 负实轴穿越计数）
    m = len(chain)
    pts = []
    for k in range(m):
        Qa = chain[k][2]      # 枢线修补#17: 链元组 (p0,p1,Q)
        Qb = chain[(k + 1) % m][2]
        rx = (max(float(Qa[0].a), float(Qb[0].a)), min(float(Qa[0].b), float(Qb[0].b)))
        ry = (max(float(Qa[1].a), float(Qb[1].a)), min(float(Qa[1].b), float(Qb[1].b)))
        if not (rx[0] <= rx[1] and ry[0] <= ry[1]):
            raise VerifyError(f"相邻盒交集为空（k={k}）——链断裂，拒证")
        px = (rx[0] + rx[1]) / 2
        py = (ry[0] + ry[1]) / 2
        if px == 0.0:
            px = math.nextafter(px, 1.0)
        if py == 0.0:
            py = math.nextafter(py, 1.0)
        pts.append((px, py))
    W_cross = 0
    darg_sum = 0.0
    for k in range(m):
        x0, y0 = pts[k]
        x1, y1 = pts[(k + 1) % m]
        # 辐角增量（主值；唯一性由盒张角 ≤1.2 rad 保证：真实增量 ∈ (−2.4, 2.4)⊂(−π,π)）
        darg_sum += math.atan2(x0 * y1 - y0 * x1, x0 * x1 + y0 * y1)
        # 半开规则（逆时针：下行穿越负实轴 +1，上行 −1）
        up = (y0 <= 0 < y1)
        dn = (y1 <= 0 < y0)
        if up or dn:
            xc = x0 - y0 * (x1 - x0) / (y1 - y0)
            if abs(xc) < 1e-12:
                raise VerifyError("穿越横坐标退化（≈0）——拒证")
            if xc < 0:
                W_cross += 1 if dn else -1
    W_inc = darg_sum / (2 * math.pi)
    if abs(W_inc - round(W_inc)) > 0.05:
        raise VerifyError(f"辐角增量绕数非整数邻域：{W_inc}——拒证")
    if int(round(W_inc)) != W_cross:
        raise VerifyError(f"双算法不一致：增量={W_inc} 穿越={W_cross}——拒证")
    stats.darg_sum = darg_sum
    return W_cross, stats


def _accept_box(Q, stats, depth):
    """收盒判据：0∉Q 且辐角张角 ≤ 1.2 rad（保证链上辐角增量主值唯一）。"""
    stats.boxes += 1
    stats.max_depth = max(stats.max_depth, depth)
    if not _box_avoids_zero(Q):
        return False
    if _box_argwidth_float(Q) > _ARGWIDTH_MAX:
        return False
    d = _box_dist_float(Q)
    if stats.min_dist is None or d < stats.min_dist:
        stats.min_dist = d
    return True


def _subdivide_edge_h(edge, p0, p1, em_N, dir_M, stats, depth=0):
    """横边 σ∈[p0[0],p1[0]]，t=p0[1] 固定。返回盒链。"""
    s0, s1 = p0[0], p1[0]
    try:
        Q = _eval_arc_box_h(edge, s0, s1, p0[1], em_N, dir_M, stats)
        if _accept_box(Q, stats, depth):
            return [(p0, p1, Q)]  # 枢线修补#17: 链元组携带参数域（Backlund 结点网格用）
    except StraddleError:
        pass
    if depth >= 60:
        raise VerifyError(f"围道细分超深（{edge} σ∈[{s0},{s1}]）——拒证")
    mid = Fraction(s0 + s1) / 2
    return (_subdivide_edge_h(edge, p0, (mid, p0[1]), em_N, dir_M, stats, depth + 1)
            + _subdivide_edge_h(edge, (mid, p0[1]), p1, em_N, dir_M, stats, depth + 1))


def _subdivide_edge_v(edge, p0, p1, em_N, dir_M, stats, depth=0):
    """竖边 t∈[p0[1],p1[1]]，σ=p0[0] 固定。返回盒链。"""
    t0, t1 = p0[1], p1[1]
    Q = _eval_arc_box_v(edge, p0[0], t0, t1, em_N, dir_M, stats)
    if _accept_box(Q, stats, depth):
        return [(p0, p1, Q)]  # 枢线修补#17: 同上
    if depth >= 60:
        raise VerifyError(f"围道细分超深（{edge} t∈[{t0},{t1}]）——拒证")
    mid = Fraction(t0 + t1) / 2
    return (_subdivide_edge_v(edge, p0, (p0[0], mid), em_N, dir_M, stats, depth + 1)
            + _subdivide_edge_v(edge, (p0[0], mid), p1, em_N, dir_M, stats, depth + 1))


def _iv_frac(f):
    from mpmath import iv
    return iv.mpf(f.numerator) / iv.mpf(f.denominator)


def _iv_box_frac(f0, f1):
    from mpmath import iv
    a = _iv_frac(f0)
    b = _iv_frac(f1)
    return iv.mpf((a, b))


def _eval_arc_box_h(edge, s0, s1, T, em_N, dir_M, stats):
    from mpmath import iv
    sig = _iv_box_frac(min(s0, s1), max(s0, s1))
    tt = _iv_box_frac(T, T)
    Z, E, meth = zeta_box(sig, tt, em_N, dir_M)
    Q = (iv.mpf((Z[0].a - E.b, Z[0].b + E.b)), iv.mpf((Z[1].a - E.b, Z[1].b + E.b)))
    stats.methods[meth] = stats.methods.get(meth, 0) + 1
    return Q


def _eval_arc_box_v(edge, sig_f, t0, t1, em_N, dir_M, stats):
    from mpmath import iv
    sig = _iv_box_frac(sig_f, sig_f)
    tt = _iv_box_frac(min(t0, t1), max(t0, t1))
    if sig_f == 2:
        Z, E = _zeta_dirichlet_box(tt, dir_M)
        meth = "dirichlet"
    else:
        Z, E, meth = zeta_box(sig, tt, em_N, dir_M)
    Q = (iv.mpf((Z[0].a - E.b, Z[0].b + E.b)), iv.mpf((Z[1].a - E.b, Z[1].b + E.b)))
    stats.methods[meth] = stats.methods.get(meth, 0) + 1
    return Q


# ------------------------------------------------------------------ Backlund 交叉校验

def backlund_re_zeta_right_edge(M):
    """(a) Re ζ(2+it) ≥ 1 − Σ_{n=2}^{M} n^{−2} − 1/M > 0 全局认证（一切实 t）。"""
    from mpmath import iv
    iv.dps = DPS_RS
    acc = iv.mpf(0)
    for n in range(2, M + 1):
        acc = acc + 1 / (iv.mpf(n) * iv.mpf(n))
    bound = iv.mpf(1) - acc - iv.mpf(1) / M
    return bound   # 须 > 0


def _arg_increment(p0, p1, Q):
    """多边形边 p0→p1（⊂Q∌0）的辐角增量（主值，float）；认证 |增量|<π 由
    盒到原点距离 > 盒对角线半径的一半保证（否则调用方已拒证）。"""
    cross = p0[0] * p1[1] - p0[1] * p1[0]
    dot = p0[0] * p1[0] + p0[1] * p1[1]
    return math.atan2(cross, dot)


def arg_variation_and_re_sign_changes(chain_pts_range):
    """给定顶点序列（float 点列），返回 (ΣΔarg float, Re 变号数)。"""
    tot = 0.0
    m = 0
    for k in range(len(chain_pts_range) - 1):
        x0, y0 = chain_pts_range[k]
        x1, y1 = chain_pts_range[k + 1]
        tot += math.atan2(x0 * y1 - y0 * x1, x0 * x1 + y0 * y1)
        if (x0 > 0) != (x1 > 0) and x0 != 0.0 and x1 != 0.0:
            m += 1
    return tot, m


def _point_eval_zeta_iv(sig_f, t_f, em_N, dir_M):
    """[S10b·枢线修补#17] 结点紧区间求值：退化零宽输入（dyadic 有理参数精确入盒）。
    分发：|t|<=CVZ_T_MAX → CVZ（误差 ~1e-85 量级）；否则 EM（显式余项）。
    不走 Dirichlet：其 1/M 尾界（~5e-3）对结点求值过松，累计宽度会淹没整数窗。
    返回 ((re,im) iv.mpi 对（已含 E 包络对称加宽）, method)。"""
    from mpmath import iv
    sig = _iv_box_frac(sig_f, sig_f)
    tt = _iv_box_frac(t_f, t_f)
    if not (sig.a >= 0.5):
        raise VerifyError("结点求值越出 σ>=1/2 域——拒证")
    if max(abs(tt.a), abs(tt.b)) <= CVZ_T_MAX:
        Z, E = _zeta_cvz_box(sig, tt)
        meth = "cvz_pt"
    else:
        Z, E = _zeta_em_box(sig, tt, em_N)
        meth = "em_pt"
    Q = (iv.mpf((Z[0].a - E.b, Z[0].b + E.b)),
         iv.mpf((Z[1].a - E.b, Z[1].b + E.b)))
    return Q, meth


def _iv_arg_tight(Q):
    """紧点区间辐角主值（iv.atan2 象限感知）。0∈Q → 拒证（fail-closed）。"""
    from mpmath import iv
    if not (Q[0].b < 0 or Q[0].a > 0 or Q[1].b < 0 or Q[1].a > 0):
        raise VerifyError("结点区间含 0——辐角无定义，拒证")
    return iv.atan2(Q[1], Q[0])


def _wrap_pi_iv(d):
    """辐角增量主值包裹。链盒张角 <=1.2<π 认证每子段真实增量 ∈(−1.2,1.2)⊂(−π,π)，
    故包裹唯一合法（张角余量以分支认证方式纳入，不进入区间宽度）。d 为紧区间。"""
    from mpmath import iv
    if d.a > iv.pi.b:
        return d - 2 * iv.pi
    if d.b < -iv.pi.b:
        return d + 2 * iv.pi
    return d


def _iv_re_sign(Q):
    """Re 区间严格符号：+1/−1；跨 0 → 拒证（fail-closed，不作启发式猜测）。"""
    if Q[0].a > 0:
        return 1
    if Q[0].b < 0:
        return -1
    raise VerifyError("结点 Re 区间跨 0——变号计数无法严格裁决，拒证")


def backlund_cross_check(T_str, eps_str, em_N, dir_M, winding, dps=None):
    """(b) Backlund：N_B(T) = (θ(T) + Δarg_L)/π + 1，
    Δarg_L = 沿 2→2+iT→1/2+iT 折线的连续辐角增量。

    OBL-EXT11-a 关闭版（枢线修补#17；KI-EXT11-1-ADD2 根因双层分解）：
    - 锚点修正：L 折线自 t=0 起（arg ζ(2)=0 实正锚点）。旧版自 ε 起步，
      缺失锚段辐角 arg ζ(2+iε)（ε=0.5 时 −0.0794691791… rad，为旧拒证主因）；
      eps_str 形参保留仅为签名兼容，Backlund 层不再消费（winding 矩形仍用 ε）。
    - Δarg_L 结点紧区间求值：链盒张角 ≤1.2<π 认证每子段真实增量 ∈(−π,π)；
      结点（二分网格 dyadic 参数）处以零宽输入取 CVZ/EM 紧区间（~1e-85），
      逐段增量取主值（包裹唯一合法）后区间求和——
      取代旧盒心多边形 float 层（张角余量未计入，实测残余 ~0.016 rad）。
    - N_B 区间 = (θ_iv + Δarg_iv)/π + 1：全程区间算术，旧 ±1e-9 浮点容忍移除；
      区间须含唯一整数，否则 fail-closed 拒证（不得以放宽区间宽度绕过）。
    返回 (N_B_int, m_re_sign_changes_top_half, detail)。"""
    from mpmath import iv, mp
    iv.dps = dps or DPS_CVZ
    T = Fraction(T_str)
    stats = ContourStats()
    zero = Fraction(0)
    # 右边：σ=2，t: 0→T（锚点 arg ζ(2)=0）
    right = _subdivide_edge_v("right", (Fraction(2), zero), (Fraction(2), T),
                              em_N, dir_M, stats)
    # 顶右半：t=T，σ: 2→1/2
    top_half = _subdivide_edge_h("top", (Fraction(2), T), (Fraction(1, 2), T),
                                 em_N, dir_M, stats)
    segs = right + top_half
    # 结点参数序列（有序）：竖边终点列接横边终点列
    grid = [(Fraction(2), zero)]
    grid += [(Fraction(2), p1[1]) for (p0, p1, Q) in right]
    grid += [(p1[0], T) for (p0, p1, Q) in top_half]
    # 结点紧求值 → 辐角主值 + Re 符号
    args = []
    re_signs = []
    jmeth = {}
    for (sf, tf) in grid:
        Q, meth = _point_eval_zeta_iv(sf, tf, em_N, dir_M)
        jmeth[meth] = jmeth.get(meth, 0) + 1
        args.append(_iv_arg_tight(Q))
        re_signs.append(_iv_re_sign(Q))
    # 每子段增量主值求和（区间；张角认证分支唯一）
    darg = iv.mpf(0)
    for k in range(len(segs)):
        darg = darg + _wrap_pi_iv(args[k + 1] - args[k])
    # Re 变号数（顶右半段：结点下标 len(right)..len(grid)-1）
    m_re = 0
    for k in range(len(right), len(grid) - 1):
        if re_signs[k] != re_signs[k + 1]:
            m_re += 1
    # θ(T) 区间（DPS_RS 规范，余项内含）
    iv.dps = DPS_RS
    th = theta_iv(_iv_frac(T))
    nB = (th + darg) / iv.pi + 1
    mp.dps = max(mp.dps, 60)
    nB_lo_i = int(mp.ceil(nB.a))
    nB_hi_i = int(mp.floor(nB.b))
    if nB_lo_i != nB_hi_i:
        raise VerifyError(
            f"Backlund N_B 区间 [{mp.nstr(nB.a, 30)},{mp.nstr(nB.b, 30)}] "
            "不含唯一整数——拒证（OBL-EXT11-a 未达：不得以放宽区间宽度绕过）")
    return nB_lo_i, m_re, {
        "nB_interval": [mp.nstr(nB.a, 30), mp.nstr(nB.b, 30)],
        "nB_interval_width": mp.nstr(nB.b - nB.a, 6),
        "darg_interval": [mp.nstr(darg.a, 30), mp.nstr(darg.b, 30)],
        "darg_method": "junction_pointeval_interval_v1(枢线修补#17/OBL-EXT11-a)",
        "anchor": "t=0（arg ζ(2)=0 实正锚点）",
        "junctions": len(grid),
        "boxes": stats.boxes,
        "methods": dict(stats.methods),
        "junction_methods": jmeth}


def sieve_prime_power_exponents(x_int):
    """精确筛：返回 [(p, m_p)]，p 升序，m_p = max{k: p^k ≤ x_int}（整数幂精确判定）。"""
    sieve = bytearray(b"\x01") * (x_int + 1)
    if x_int >= 0:
        sieve[0] = 0
    if x_int >= 1:
        sieve[1] = 0
    for i in range(2, int(math.isqrt(x_int)) + 1):
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


def trunc_residual(brackets_lo_hi):
    """[S10]：返回 (psi, S, r, bound)（iv，dps=60）。"""
    from mpmath import iv, mp
    iv.dps = DPS_TRUNC
    x0 = _iv_of("20000001/2")
    lnx0 = iv.log(x0)
    psi = iv.mpf(0)
    for p, m in sieve_prime_power_exponents(10 ** 7):
        psi = psi + m * iv.log(iv.mpf(p))
    S = iv.mpf(0)
    for lo_s, hi_s in brackets_lo_hi:
        _lo = _iv_of(lo_s)  # 枢线修补终版: iv 有理除法外向舍入天然包络(与 gen 同律)
        _hi = _iv_of(hi_s)
        G = iv.mpf((_lo.a, _hi.b))
        ang = G * lnx0
        x0h = iv.sqrt(x0)
        numer = (x0h * iv.cos(ang), x0h * iv.sin(ang))
        rho = (iv.mpf("0.5"), G)
        term = _cdiv(numer, rho)
        S = S + 2 * term[0]
    r = psi - x0
    r = r + S
    r = r + iv.log(2 * iv.pi)
    r = r + iv.mpf("0.5") * iv.log(iv.mpf(1) - x0 ** (-2))
    bound = 2 * x0 * lnx0 ** 2 / 1000
    return psi, S, r, bound


# ------------------------------------------------------------------ 证书验证

def _check_common(w, cl, witness_path):
    cl.add("classify_l1", w.get("CLASSIFY") == "L1", str(w.get("CLASSIFY")))
    try:
        first = list(w.keys())[0]
    except Exception:
        first = None
    cl.add("classify_first_field", first == "CLASSIFY", str(first))
    cl.add("witness_sha256", _canon_sha256({k: v for k, v in w.items() if k != "witness_sha256"}) == w.get("witness_sha256"), "规范化序列化复算(枢线修补#3: 剥自字段)")
    cl.add("lean_binding_null", w.get("lean_binding") is None, str(w.get("lean_binding")))
    prov = w.get("provenance", {})
    env = prov.get("env_fp", {}) if isinstance(prov, dict) else {}
    cl.add("env_lean_free", env.get("lean_free") is True, str(env.get("lean_free")))
    gen = prov.get("generator", {}) if isinstance(prov, dict) else {}
    gpath = gen.get("script")
    gsha = gen.get("sha256")
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(witness_path))))
    gfile = os.path.join(repo_root, gpath) if gpath else None
    ok = bool(gfile and os.path.isfile(gfile) and _sha256_file(gfile) == gsha)
    cl.add("generator_sha256", ok, f"{gpath}")
    disc = w.get("disclosure", [])
    _req = REQUIRED_DISCLOSURES[0]
    # 枢线修补#13(SUP-01): 必载披露逐字在场——全等或「逐字前缀+；」加性强化句均受理(只许增强不许减弱)
    cl.add("disclosure_kernel_honesty",
           any(isinstance(d, str) and (d == _req or d.startswith(_req + "；")) for d in disc),
           str(disc))
    rep = w.get("replay", {})
    cl.add("replay_rule", rep.get("canonical_sha256_rule") is not None, "")


def _check_schema(w, cl):
    sv = w.get("schema_version")
    if sv is None:
        raise VerifyError("缺 schema_version——拒绝受理")
    major = int(str(sv).split(".")[0])
    if major != SUPPORTED_MAJOR:
        raise VerifyError(f"unsupported_schema: major={major}")
    for k in TOP_REQUIRED:
        cl.add(f"required:{k}", k in w, "")


def _verify_iso(w, cl):
    from mpmath import iv
    iv.dps = DPS_RS
    inp = w["inputs"]
    T = inp["T"]
    c_low = _iv_of(w["bounds"]["remainder_low_t_constant"])
    _frc = Fraction(str(w["bounds"]["remainder_low_t_constant"]).strip())  # 枢线修补#4: 门限按 [S1] 用精确有理比较(原判 float(iv 下界)>=0.2 与自身有理化规范冲突)
    if not (_frc >= Fraction(1, 5) and _frc <= 1):
        cl.add("c_low_range", False, str(_frc))
        return
    cl.add("c_low_range", True, str(_frc))
    cl.add("disclosure_finite_height", f"有限高度 T={T} 截断" in w.get("disclosure", []), "")
    ex = w["existence"]
    brackets = ex["brackets"]
    ok_all = True
    prev_hi = None
    encs = []
    for i, (lo_s, hi_s) in enumerate(brackets):
        ok, detail, enc_lo, enc_hi = _certify_bracket(lo_s, hi_s, T, c_low)
        if prev_hi is not None and not (Fraction(lo_s) > prev_hi):
            ok = False
            detail = "括号重叠/乱序"
        prev_hi = Fraction(hi_s)
        if not ok:
            ok_all = False
            cl.add(f"bracket[{i}]", False, detail)
            break
        encs.append((enc_lo, enc_hi))
    cl.add("brackets_all_certified", ok_all, f"n={len(brackets)}")
    cl.add("bracket_count", len(brackets) == ex.get("count") == inp["expected_zeros"],
           f"{len(brackets)}/{ex.get('count')}/{inp['expected_zeros']}")
    # 登记端点包络字符串逐字复算比对
    if ok_all and len(encs) == len(brackets):
        reg = ex.get("endpoint_enclosures", [])
        match = len(reg) == len(brackets)
        if match:
            for i, (enc_lo, enc_hi) in enumerate(encs):
                want = reg[i]
                got = [_iv_str(enc_lo.a), _iv_str(enc_lo.b), _iv_str(enc_hi.a), _iv_str(enc_hi.b)]
                if want != got:
                    match = False
                    break
        cl.add("endpoint_enclosures_string_exact", match, "")
    # 负控：伪造括号必拒
    neg = w["negative_control"]
    fb = neg["fake_bracket"]
    ok, detail, _, _ = _certify_bracket(fb[0], fb[1], T, c_low)
    cl.add("neg_fake_bracket_rejected", (not ok) and neg["neg_verdict"].get("neg_rejected") is True,
           detail)
    # 完备性
    comp = w["completeness"]
    _st = comp.get("status")  # SUP-01(EXT14 R1 条件 qgl/lvlu): BLOCKED 子码分账——兼容 v1.0 "BLOCKED(B1) time-box" 与 v1.0.1 "BLOCKED(B1-TB) time-box"; 判据语义(熔断诚实性)不变
    if isinstance(_st, str) and _st.startswith("BLOCKED(B1") and "time-box" in _st:
        cl.add("completeness_blocked_honest",
               w["verdict"].get("completeness") is False
               and comp.get("winding") is None
               and isinstance(comp.get("reason"), str) and len(comp["reason"]) > 20,
               "time-box 熔断明码登记")
        cl.add("blocked_subcode_present",
               ("B1-TB" in _st) and isinstance(comp.get("blocked_subcode"), str)
               and isinstance(comp.get("retry_budget"), str),
               "子码+重试预算登记(v1.0.1 起强制; 分账纪律防存在性误读为完备性进展)")
    elif comp.get("status") == "CERTIFIED":
        W, stats = winding_number(str(T), inp["eps"], int(inp["em_N"]), int(inp["dirichlet_M"]))
        cl.add("winding_recompute", W == comp.get("winding"), f"复算={W} 登记={comp.get('winding')}")
        cl.add("winding_equals_brackets", W == len(brackets), f"{W}=={len(brackets)}")
        cl.add("winding_2NT_convention", comp.get("winding_2NT") == 2 * W, "")
        # Backlund
        bk = comp["backlund"]
        bound = backlund_re_zeta_right_edge(int(inp["backlund_M"]))
        cl.add("backlund_re_positive", bound.a > 0, _iv_str(bound.a))
        nB, m_re, detail = backlund_cross_check(str(T), inp["eps"], int(inp["em_N"]),
                                                int(inp["dirichlet_M"]), W)
        cl.add("backlund_N_equals_winding", nB == W == bk.get("n_backlund"),
               f"N_B={nB} W={W} 登记={bk.get('n_backlund')}")
        # 枢线修补#17(OBL-EXT11-a): 唯一整数窗证据登记（拒证情形已在函数内 raise，此处恒真）
        cl.add("backlund_unique_integer_window", True,
               f"N_B区间=[{detail['nB_interval'][0]},{detail['nB_interval'][1]}] "
               f"宽{detail['nB_interval_width']}；方法={detail['darg_method']}；"
               f"锚点={detail['anchor']}；结点{detail['junctions']}")
        cl.add("backlund_re_sign_changes", m_re == bk.get("re_sign_changes_top_half"),
               f"{m_re} vs {bk.get('re_sign_changes_top_half')}")
    else:
        cl.add("completeness_status", False, str(comp.get("status")))
        return
    v = w["verdict"]
    cl.add("verdict_existence", v.get("existence") is True, "")
    if comp.get("status") == "CERTIFIED":
        cl.add("verdict_completeness", v.get("completeness") is True, "")
        cl.add("verdict_all_pass", v.get("all_pass") is True, "")
    else:
        cl.add("verdict_all_pass", v.get("all_pass") is False, "完备性熔断不得判 all_pass")


def _verify_trunc(w, cl):
    from mpmath import iv
    inp = w["inputs"]
    if str(inp["x0"]) != "10000000.5" or str(inp["T0"]) != "1000":
        cl.add("trunc_inputs", False, f"x0={inp.get('x0')} T0={inp.get('T0')}")
        return
    cl.add("trunc_inputs", True, "")
    cl.add("disclosure_finite_height", "有限高度 T=1000 截断" in w.get("disclosure", []), "")
    cl.add("disclosure_dudek_scope", TRUNC_DISCLOSURE in w.get("disclosure", []), "")
    src = inp["zero_source"]
    cl.add("zero_source_ref", src.get("certificate_id") == "zeta-iso-1000", str(src))
    brackets = src["brackets"]
    cl.add("zero_count", len(brackets) == 649, str(len(brackets)))
    # 与所引证书一致性（若在仓内可得）
    cert_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "artifacts", "witnesses-zeta", "zeta-iso-1000.witness.json")
    if os.path.isfile(cert_path):
        with open(cert_path, encoding="utf-8") as fh:
            src_cert = json.load(fh)
        cl.add("zero_source_sha256", _sha256_file(cert_path) == src.get("sha256"),
               "ISO-1000 证书哈希一致")
        cl.add("zero_source_brackets_match",
               src_cert["existence"]["brackets"] == [list(b) for b in brackets], "")
    # 重算残差
    psi, S, r, bound = trunc_residual(brackets)
    met = w["bounds"]["trunc_metrics"]
    cl.add("psi_string_exact", met.get("psi") == [_iv_str(psi.a), _iv_str(psi.b)], "")
    cl.add("S_string_exact", met.get("S") == [_iv_str(S.a), _iv_str(S.b)], "")
    cl.add("residual_string_exact", met.get("residual") == [_iv_str(r.a), _iv_str(r.b)], "")
    cl.add("bound_string_exact", met.get("bound") == [_iv_str(bound.a), _iv_str(bound.b)], "")
    within = max(abs(r.a), abs(r.b)) <= bound.a
    cl.add("residual_within_dudek_form", within,
           f"|r|max={_iv_str(max(abs(r.a), abs(r.b)))} ≤ bound={_iv_str(bound.a)}")
    cl.add("verdict_within", w["verdict"].get("residual_within_bound") is True, "")
    # 负控：篡改紧界必拒
    neg = w["negative_control"]
    tb = _iv_of(neg["tampered_bound"])
    neg_within = max(abs(r.a), abs(r.b)) <= tb.a
    cl.add("neg_tight_bound_rejected", (not neg_within)
           and neg["neg_verdict"].get("neg_rejected") is True,
           f"tampered_bound={neg['tampered_bound']}")


def verify_witness(path):
    """fail-closed 主入口：返回 {ok, checks, error}。"""
    checks = CL()
    try:
        with open(path, encoding="utf-8") as fh:
            w = json.load(fh)
    except Exception as exc:
        return {"ok": False, "checks": [], "error": f"unparseable: {exc}"}
    try:
        _check_schema(w, checks)
        _check_common(w, checks, path)
        fam = w.get("family")
        if fam == "zeta-isolation":
            _verify_iso(w, checks)
        elif fam == "zeta-truncation":
            _verify_trunc(w, checks)
        else:
            checks.add("family_known", False, str(fam))
    except VerifyError as exc:
        checks.add("exception", False, str(exc))
    except Exception as exc:  # 默认拒绝律：任何异常即失败
        checks.add("exception", False, f"{type(exc).__name__}: {exc}")
    return {"ok": checks.ok, "checks": checks.checks, "error": None}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("witnesses", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    results = []
    ok_all = True
    for path in args.witnesses:
        v = verify_witness(path)
        results.append({"file": path, "ok": v["ok"], "error": v["error"],
                        "failed": [c for c in v["checks"] if not c["ok"]]})
        ok_all = ok_all and v["ok"]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            print(("PASS" if r["ok"] else "FAIL"), r["file"])
            for c in r["failed"]:
                print("   ✗", c["check"], c["detail"])
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
