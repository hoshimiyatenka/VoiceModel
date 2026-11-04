# v0.4 测试 / Phase 0 / 非实测 / 状态: unit-test
"""代码骨架契约单测（标准库 unittest，无第三方依赖）。

目的：把 D16 / ADR-0004 的「只落签名占位、不得偷偷实现」变成可执行断言，
并守住 R-19（规格↔骨架漂移）与 R-20（错误码表↔C 层漂移）的第一条防线：
字段名 / 函数名 / 端点清单一旦与规格不符，CI 直接失败。

可直接运行：python -m unittest discover -s tests/unit -v
"""
from __future__ import annotations

import dataclasses
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import src.control as control  # noqa: E402
import src.serve as serve      # noqa: E402


class TestControlSkeleton(unittest.TestCase):
    """C 层骨架：形状固定、实现未落地。"""

    def test_validate_control_is_placeholder(self):
        """Phase 0：validate_control 必须仍抛 NotImplementedError（D16）。"""
        ctx = control.ControlContext(
            capabilities=control.CapabilityFlags(),
            preset=None,
            license=control.LicenseCredential(
                commercial_authorized=False, speaker_registered=False
            ),
            speaker_registry=frozenset(),
            request_id="req-phase0-0001",
        )
        with self.assertRaises(NotImplementedError):
            control.validate_control({"spec_version": "0.3.0"}, ctx)

    def test_to_envelope_is_placeholder(self):
        """Phase 0：to_envelope 未实现，不得返回伪造信封。"""
        result = control.ValidationResult(valid=False)
        with self.assertRaises(NotImplementedError):
            result.to_envelope()

    def test_dataclasses_are_frozen(self):
        """全部结果结构 frozen=True（规格 §2 不变性要求）。"""
        for cls in (
            control.CapabilityFlags,
            control.ExpandedPreset,
            control.LicenseCredential,
            control.ControlContext,
            control.ValidationIssue,
            control.AuditPatch,
            control.ValidationResult,
        ):
            self.assertTrue(
                cls.__dataclass_params__.frozen, "%s 未设 frozen=True" % cls.__name__
            )

    def test_control_context_field_names(self):
        """ControlContext 字段名即协议字段名，Phase 3 不得改名（规格 §2）。"""
        names = [f.name for f in dataclasses.fields(control.ControlContext)]
        self.assertEqual(
            names,
            [
                "capabilities",
                "preset",
                "license",
                "speaker_registry",
                "request_id",
                "attribute_scan_passed",
                "model_commit",
                "watermark_id",
            ],
        )

    def test_validation_result_field_names(self):
        """ValidationResult 字段名固定（信封形状不得增删）。"""
        names = [f.name for f in dataclasses.fields(control.ValidationResult)]
        self.assertEqual(
            names, ["valid", "errors", "warnings", "audit_patch", "resolved_spec"]
        )

    def test_capability_flags_default_off(self):
        """Phase 0 能力全为声明值：默认必须全部关闭，防止误称「已支持」。"""
        flags = control.CapabilityFlags()
        for f in dataclasses.fields(flags):
            self.assertIs(getattr(flags, f.name), False, f.name)


class TestServeSkeleton(unittest.TestCase):
    """L6 骨架：5 端点清单冻结、实现未落地。"""

    def test_endpoints_frozen(self):
        """端点清单与 API-SPEC §1.1 一致，不得增删（Phase 0）。"""
        self.assertEqual(
            serve.ENDPOINTS,
            (
                "POST /v1/presets/validate",
                "POST /v1/synthesize",
                "GET /v1/presets/{id}",
                "GET /v1/capabilities",
                "GET /v1/health",
            ),
        )

    def test_endpoints_still_unimplemented(self):
        """Phase 0：所有端点函数必须仍抛 NotImplementedError。"""
        calls = {
            "validate_presets": lambda: serve.validate_presets({}),
            "synthesize": lambda: serve.synthesize({}),
            "get_preset": lambda: serve.get_preset("p"),
            "capabilities": lambda: serve.capabilities(),
            "health": lambda: serve.health(),
        }
        for name, call in calls.items():
            with self.assertRaises(NotImplementedError, msg=name):
                call()


if __name__ == "__main__":
    unittest.main(verbosity=2)
