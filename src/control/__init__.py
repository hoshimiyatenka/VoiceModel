"""L5 控制层 · VoiceSpec 解析、S/C 两层校验、冲突消解、参数→条件映射。

Phase 0 接口占位 / 非实现 / 未实测。

职责（技术栈方案 v0.1 §10 / ADR-0003）：
  - VoiceSpec 解析与版本控制（spec_version=0.3.0，见 configs/voicespec/voicespec.schema.json）
  - S 层（JSON Schema）+ C 层（Control）两层校验，S 先于 C
  - 跨字段语义冲突消解、能力探测、降级决策、许可联动、审计填充
  - 错误码唯一真源 docs/voicespec/ERROR-CODES.md，只追加不改义

控制手段优先级（ADR-0003）：M4 > M2(连续) > M1(离散) > M5 > M3 > M6(DSP 仅降级)。
契约实现规格见 docs/implement/control/CONTROL-LAYER-SPEC.md（Phase 3 待实现）。
"""

from .validator import (
    AuditPatch,
    CapabilityFlags,
    ControlContext,
    ExpandedPreset,
    LicenseCredential,
    Severity,
    ValidationIssue,
    ValidationResult,
    validate_control,
)

__all__ = [
    "AuditPatch",
    "CapabilityFlags",
    "ControlContext",
    "ExpandedPreset",
    "LicenseCredential",
    "Severity",
    "ValidationIssue",
    "ValidationResult",
    "validate_control",
]
