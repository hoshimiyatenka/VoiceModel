# v0.4 测试 / Phase 0 / 非实测 / 状态: unit-test
"""契约一致性单测（标准库 unittest，无第三方依赖）。

可直接运行：python -m unittest discover -s tests/unit -v
所有断言针对 Phase 0 的「契约/阈值单一真源」基线，不依赖任何训练产出。
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO / "configs" / "voicespec" / "voicespec.schema.json"
ERROR_CODES_PATH = REPO / "docs" / "voicespec" / "ERROR-CODES.md"
THRESHOLDS_PATH = REPO / "configs" / "eval" / "thresholds.yaml"


def load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


class TestSpecConsistency(unittest.TestCase):

    def test_spec_version_const(self):
        """spec_version.const 必须锁死为 0.3.0（v0.4 不升契约版本）。"""
        schema = load_schema()
        self.assertEqual(
            schema.get("properties", {}).get("spec_version", {}).get("const"),
            "0.3.0",
        )

    def test_additional_properties_false(self):
        """顶层 additionalProperties 必须为 False（禁止静默忽略未知字段）。"""
        schema = load_schema()
        self.assertIs(schema.get("additionalProperties"), False)

    def test_error_codes_no_duplicates(self):
        """ERROR-CODES.md 定义区（§3–§4）的错误码不得重复定义。

        注意：§5「错误码↔schema 对照表」会合法地再次引用已登记码，故重复
        校验只针对 §3/§4 的定义行（形如 `| `E-XXX-001` | ... |`）。
        """
        lines = ERROR_CODES_PATH.read_text(encoding="utf-8").splitlines()
        start = next(i for i, l in enumerate(lines) if l.startswith("## 3."))
        end = next(i for i, l in enumerate(lines) if l.startswith("## 5."))
        def_row = re.compile(r"^\|\s*`([EW]-[A-Z]+-\d{3})`\s*\|")
        defined = []
        for line in lines[start:end]:
            m = def_row.match(line)
            if m:
                defined.append(m.group(1))
        dup = sorted({c for c in defined if defined.count(c) > 1})
        self.assertEqual(dup, [], "错误码定义重复: %s" % dup)
        self.assertGreater(len(defined), 0, "§3–§4 未解析到任何错误码定义行")

    def test_five_layers_defs_present(self):
        """五层 $defs 必须齐全。"""
        schema = load_schema()
        defs = schema.get("$defs", {})
        for name in ("IdentitySpec", "ProsodySpec", "StyleSpec",
                     "LinguisticSpec", "RenderSpec"):
            self.assertIn(name, defs, "缺少 $defs.%s" % name)

    def test_thresholds_uncalibrated(self):
        """thresholds.yaml 的 calibration.status 仍为 uncalibrated（无实测）。"""
        text = THRESHOLDS_PATH.read_text(encoding="utf-8")
        m = re.search(r"(?m)^\s*status:\s*([A-Za-z_]+)\s*$", text)
        self.assertIsNotNone(m, "thresholds.yaml 缺少 calibration.status 行")
        self.assertEqual(m.group(1), "uncalibrated")


if __name__ == "__main__":
    unittest.main(verbosity=2)
