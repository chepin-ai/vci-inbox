# CLASSIFY: L1
"""validate_registry 最小校验器测试（PIVOT-01 WS-36 · A1 栈 P0-1/P0-3）。

覆盖（正例/缺字段/高版本拒收/非法 default 各一测 + fail-closed 补充）：
  * 正例：两交付模板本体全量通过；
  * 缺字段：DISPUTED 条目缺 §4a 八字段任一键 ⇒ 拒收（非零退出）；
  * 高版本拒收：schema_version 高 major ⇒ unsupported_schema（退出码 3）；
  * 非法 default：default_action_on_timeout 越域 ⇒ 拒收；
  * 补充：schema_version 缺失 ⇒ fail-closed 拒收。

运行：python3 -m unittest tests.governance.test_validate_registry -v
  或 python3 -m pytest tests/governance/test_validate_registry.py
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "governance" / "a1" / "validate_registry.py"
L0_TEMPLATE = REPO_ROOT / "governance" / "a1" / "l0-registry-template.json"
DISPUTED_REGISTER = REPO_ROOT / "governance" / "a1" / "disputed-register.json"


def run_validator(*paths):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *[str(p) for p in paths]],
        capture_output=True, text=True,
    )


def write_tmp(obj):
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(obj, f, ensure_ascii=False)
    f.close()
    return Path(f.name)


class TestValidateRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = json.loads(DISPUTED_REGISTER.read_text(encoding="utf-8"))

    def test_delivered_templates_pass(self):
        """正例：L0 确权登记模板与 DISPUTED 登记册（空册+示例条目）均通过。"""
        r = run_validator(L0_TEMPLATE, DISPUTED_REGISTER)
        self.assertEqual(r.returncode, 0, msg=r.stderr)
        self.assertIn("OK", r.stdout)

    def test_missing_required_field_rejected(self):
        """缺字段：删去条目 l2_record_ptr（§4a 八字段之一）⇒ 拒收。"""
        bad = copy.deepcopy(self.register)
        del bad["entries"][0]["l2_record_ptr"]
        p = write_tmp(bad)
        r = run_validator(p)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("l2_record_ptr", r.stderr)

    def test_higher_major_schema_rejected(self):
        """高版本拒收：schema_version=2.0 ⇒ unsupported_schema（退出码 3）。"""
        bad = copy.deepcopy(self.register)
        bad["schema_version"] = "2.0"
        p = write_tmp(bad)
        r = run_validator(p)
        self.assertEqual(r.returncode, 3, msg=r.stderr)
        self.assertIn("unsupported_schema", r.stderr)

    def test_illegal_default_action_rejected(self):
        """非法 default：default_action_on_timeout 越出 {hold,demote,escalate} ⇒ 拒收。"""
        bad = copy.deepcopy(self.register)
        bad["entries"][0]["default_action_on_timeout"] = "drop"
        p = write_tmp(bad)
        r = run_validator(p)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("default_action_on_timeout", r.stderr)

    def test_missing_schema_version_rejected(self):
        """fail-closed：schema_version 缺失即格式不合规拒收（§4b）。"""
        bad = copy.deepcopy(self.register)
        del bad["schema_version"]
        p = write_tmp(bad)
        r = run_validator(p)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("schema_version", r.stderr)


if __name__ == "__main__":
    unittest.main()
