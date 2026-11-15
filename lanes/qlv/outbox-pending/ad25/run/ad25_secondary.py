"""AD-25 次级债：受控 W 的归一化 tr/8 二阶口径修正。

本件只证明 controlled_W(theta) 的归一化迹恒等式及其微分结论：
t=Re(tr(W)/8)=cos(theta/4)^2，lambda=t/2，
A=acos(sqrt(2 lambda))=theta/4（0<theta<pi）。
A^2 的 eps^2 系数为1/16，A''(0)=0。它不是目标保真角曲率，
也不构成±pi/8的全局或局部角刚性定理。
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)


def op(q, a):
    ms = [I2, I2, I2]
    ms[q] = a
    return np.kron(np.kron(ms[0], ms[1]), ms[2])


def rp(t, p):
    return np.cos(t/2)*I2 + 1j*np.sin(t/2)*p


def controlled_w(theta):
    pp = (I2+X)/2
    pm = (I2-X)/2
    return op(1, pm) + op(1, pp) @ op(0, rp(theta, X))


def normalized_trace(theta):
    z = np.trace(controlled_w(theta))/8
    assert abs(z.imag) < 2e-14
    return float(z.real)


def angle_from_lambda(lam):
    # 本件只在0<theta<pi的主分支使用；sqrt(2 lambda)=cos(theta/4)>=0。
    return float(np.arccos(np.clip(np.sqrt(2*lam), -1, 1)))


def second_order(theta):
    """返回归一化 tr/8 的严格零阶、一阶、二阶系数及数值交叉检查。"""
    th, eps = sp.symbols("theta eps", real=True)
    lam = sp.cos((th+eps)/4)**2/2
    # 在0<(theta+eps)<pi分支，acos(cos((theta+eps)/4))=(theta+eps)/4。
    angle = (th+eps)/4
    exact = {
        "lambda_0": sp.cos(th/4)**2/2,
        "lambda_prime_0": sp.diff(lam, eps).subs(eps, 0),
        "lambda_second_0": sp.diff(lam, eps, 2).subs(eps, 0),
        "A_0": th/4,
        "A_prime_0": sp.Rational(1, 4),
        "A_second_0": sp.Integer(0),
        "A_squared_epsilon_coefficients": [th**2/16, th/8, sp.Rational(1, 16)],
    }
    numeric = []
    for h in (1e-2, 1e-3, 1e-4):
        lp = normalized_trace(theta+h)/2
        l0 = normalized_trace(theta)/2
        lm = normalized_trace(theta-h)/2
        ap = angle_from_lambda(lp)
        a0 = angle_from_lambda(l0)
        am = angle_from_lambda(lm)
        numeric.append({
            "h": h,
            "lambda_prime_fd": (lp-lm)/(2*h),
            "lambda_second_fd": (lp-2*l0+lm)/h**2,
            "A_prime_fd": (ap-am)/(2*h),
            "A_second_fd": (ap-2*a0+am)/h**2,
            "A_squared_second_order_coefficient_fd": (ap**2-2*a0**2+am**2)/(2*h**2),
        })
    expected = {
        "lambda_0": float(exact["lambda_0"].subs(th, theta)),
        "lambda_prime_0": float(exact["lambda_prime_0"].subs(th, theta)),
        "lambda_second_0": float(exact["lambda_second_0"].subs(th, theta)),
        "A_0": theta/4, "A_prime_0": .25, "A_second_0": 0.,
        "A_squared_second_order_coefficient": 1/16,
    }
    last = numeric[-1]
    errors = {
        "lambda_prime": abs(last["lambda_prime_fd"]-expected["lambda_prime_0"]),
        "lambda_second": abs(last["lambda_second_fd"]-expected["lambda_second_0"]),
        "A_prime": abs(last["A_prime_fd"]-expected["A_prime_0"]),
        "A_second": abs(last["A_second_fd"]-expected["A_second_0"]),
        "A_squared_second_order_coefficient": abs(
            last["A_squared_second_order_coefficient_fd"]-expected["A_squared_second_order_coefficient"]),
    }
    assert max(errors.values()) < 2e-6, (theta, errors)
    return {"theta": theta,
            "exact": {k: str(v.subs(th, theta)) if hasattr(v, "subs") else str(v)
                      for k, v in exact.items() if k != "A_squared_epsilon_coefficients"},
            "A_squared_epsilon_coefficients": [str(v.subs(th, theta)) for v in exact["A_squared_epsilon_coefficients"]],
            "expected_float": expected, "finite_differences": numeric,
            "max_h1e-4_error": max(errors.values())}


def main():
    rows = [second_order(float(t)) for t in (np.pi/8, np.pi/2, .8451937126529602, 2.2)]
    trace_errors = []
    unitary_errors = []
    for theta in np.linspace(.03, np.pi-.03, 17):
        w = controlled_w(float(theta))
        trace_errors.append(abs(normalized_trace(float(theta))-np.cos(theta/4)**2))
        unitary_errors.append(float(np.max(abs(w@w.conj().T-np.eye(8)))))
    known = next(r for r in rows if r["theta"] == np.pi/2)
    assert abs(known["expected_float"]["A_0"]-np.pi/8) < 1e-15
    assert abs(known["expected_float"]["lambda_0"]-np.cos(np.pi/8)**2/2) < 1e-15
    out = {
        "beat": "AD-25", "status": "CONTROLLED_W_NORMALIZED_TRACE_SECOND_ORDER_L1_PASS",
        "normalization": "t(theta)=Re(tr(controlled_W(theta))/8)=cos(theta/4)^2; lambda=t/2; A=acos(sqrt(2 lambda))=acos(sqrt(t)) on 0<theta<pi",
        "theorem": "t(theta+eps)=cos((theta+eps)/4)^2; lambda(theta+eps)=t(theta+eps)/2; A(theta+eps)=(theta+eps)/4; A^2=theta^2/16+theta*eps/8+eps^2/16",
        "known_answer_pi_over_2": known,
        "rows": rows,
        "trace_identity_max_error": max(trace_errors),
        "unitary_max_error": max(unitary_errors),
        "major_honesty_correction": "撤回以未归一化迹导数冒充保真角曲率、以及cos^2(theta/2)/2的旧表述；本件仅保留tr/8下可复算恒等式。",
        "boundary": "该恒等式只描述受控W的归一化迹与人为定义的A映射；不是目标电路的保真角曲率，不证明±pi/8的全局或局部角刚性，也不排除其他电路模板。",
        "debts": ["DEBT-TOFFOLI-ANALYTIC-01"],
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_secondary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "rows": len(rows),
                      "known_A0": known["expected_float"]["A_0"],
                      "A_squared_second_order_coefficient": 1/16,
                      "trace_identity_max_error": out["trace_identity_max_error"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
