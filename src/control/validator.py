"""C 层校验器 · 签名占位（Phase 0）。

规格单一依据：[`docs/implement/control/CONTROL-LAYER-SPEC.md`](../../docs/implement/control/CONTROL-LAYER-SPEC.md)
决策：[`ADR-0003`](../../docs/decisions/ADR-0003.md)（控制层路径）、[`ADR-0004`](../../docs/decisions/ADR-0004.md)（先规格后实现 / D16）
错误码真源：[`docs/voicespec/ERROR-CODES.md`](../../docs/voicespec/ERROR-CODES.md)，**只追加、不得自造或改义**

本文件只提供**协议形状**（dataclass 字段名与函数签名），实现留 Phase 3。
字段名即协议字段名，Phase 3 实现不得改名（R-19 / R-20）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Layer = Literal["schema", "control"]
Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class CapabilityFlags:
    """候选基座能力集合，由 GET /v1/capabilities 暴露；Phase 0 全为声明值，未实测。"""

    exact_duration: bool = False      # 支持显式时长头（duration_mode=exact）
    f0_contour: bool = False          # 暴露中间 F0 特征，支持 pitch_contour 曲线
    attribute_control: bool = False   # 支持 AttributeSpec 属性级控制
    style_prompt: bool = False        # 支持自然语言风格指令（仅作修饰）
    voice_blend: bool = False         # 支持多音色插值 voice_blend


@dataclass(frozen=True)
class ExpandedPreset:
    """PRESET-REGISTRY-SPEC.md 定义的展开结果。"""

    preset_id: str
    resolved_version: str             # 写入 audit.preset_resolved
    defaults: dict                    # scenario → L-B/L-C 默认值，可被 spec 显式字段覆盖
    status: Literal["template", "staging", "production"]
    gate_report: str | None


@dataclass(frozen=True)
class LicenseCredential:
    """鉴权凭证的抽象；不含任何真实密钥，仅携带布尔判定结果。"""

    commercial_authorized: bool      # render.watermark=false 的前置（E-LICENSE-001）
    speaker_registered: bool         # ref_audio_uri 已注册且已授权（E-LICENSE-002）
    speaker_ids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ControlContext:
    """只读上下文，由服务端在请求入口构造；validate_control 不得修改 ctx。"""

    capabilities: CapabilityFlags
    preset: ExpandedPreset | None     # 已解析/展开的 preset；无 preset 时为 None
    license: LicenseCredential
    speaker_registry: frozenset[str]  # 已注册说话人 ID 集合
    request_id: str                   # 全链路透传，写入 audit.request_id
    attribute_scan_passed: frozenset[str] = frozenset()  # 已过单调性扫描的属性名
    model_commit: str | None = None   # 写入 audit.model_commit
    watermark_id: str | None = None   # 写入 audit.watermark_id


@dataclass(frozen=True)
class ValidationIssue:
    code: str                         # 必须属于 ERROR-CODES.md 已登记集合
    layer: Layer
    severity: Severity
    path: str                         # JSON Pointer 风格，如 "prosody" / "style"
    message: str
    detail: dict = field(default_factory=dict)
    hint: str = ""
    doc: str = ""                     # 指向 ERROR-CODES.md 对应锚点


@dataclass(frozen=True)
class AuditPatch:
    """服务端只读审计字段；客户端传入 audit.* 会被 E-AUDIT-001 拒绝。"""

    request_id: str
    license: str = "PolyForm-Noncommercial-1.0.0"
    preset_resolved: str | None = None
    model_commit: str | None = None
    gate_report: str | None = None
    watermark_id: str | None = None
    degraded: bool = False
    golden_set_passed: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    audit_patch: AuditPatch | None = None
    resolved_spec: dict | None = None   # preset 合并 + 降级后的最终 spec；valid=True 时非空

    def to_envelope(self) -> dict[str, Any]:
        """序列化为 ERROR-CODES.md §2 的响应信封 valid/errors[]/warnings[]。

        Phase 3 实现；字段形状不得增删（`additionalProperties:false` 同理）。
        """
        raise NotImplementedError(
            "Phase 3 实现；规格见 docs/implement/control/CONTROL-LAYER-SPEC.md §2"
        )


def validate_control(spec: dict, ctx: ControlContext) -> ValidationResult:
    """C 层校验入口 · 签名占位。

    规格：[`CONTROL-LAYER-SPEC.md`](../../docs/implement/control/CONTROL-LAYER-SPEC.md) §3–§4

    契约（Phase 3 实现必须满足）：
      - 前置：``spec`` 已过 S 层（JSON Schema 2020-12）校验，``spec_version == "0.3.0"``
      - 纯函数：无 I/O、无时钟、无随机数、不改 ``spec``、不改 ``ctx``；相同入参恒返回相同结果（支撑 Q9）
      - 副作用：无。审计落库 / 日志 / 水印注入由服务端在返回后执行
      - 失败语义：``errors`` 非空即 ``valid=False``，不抛业务异常；
        未预期异常由外层包装为 ``E-INTERNAL-001``（不暴露堆栈）
      - 流水线顺序：见规格 §4 的 7 步（含 preset 合并 → 冲突消解 → 能力探测 → 降级 → 许可 → 审计）

    Args:
        spec: 已通过 S 层校验的 VoiceSpec dict。
        ctx: 服务端构造的只读上下文。

    Returns:
        ValidationResult: 成功时 ``resolved_spec`` 与 ``audit_patch`` 非空。

    Raises:
        NotImplementedError: Phase 0 占位；实现见 Phase 3。
    """
    raise NotImplementedError(
        "Phase 3 实现；规格见 docs/implement/control/CONTROL-LAYER-SPEC.md §3–§4，"
        "18 个 C 码判定表见同文件 §5"
    )
