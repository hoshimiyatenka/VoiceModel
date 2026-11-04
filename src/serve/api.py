"""L6 HTTP API · 端点签名占位（Phase 0）。

接口规格（唯一依据）：[`docs/implement/control/API-SPEC.md`](../../docs/implement/control/API-SPEC.md)
错误码 → HTTP 映射：[API-SPEC §8](../../docs/implement/control/API-SPEC.md)
响应信封：[`ERROR-CODES.md` §2](../../docs/voicespec/ERROR-CODES.md)

本文件只声明端点与返回形状，**不含框架绑定**（FastAPI / Starlette 选型留 Phase 4，见 DEPLOYMENT-SPEC）。
实现必须遵守：
  - 信封字段 ``valid / errors[] / warnings[]`` 不得增删（与 ``additionalProperties:false`` 同理）
  - ``E-INTERNAL-001`` 携带 ``request_id``，**不暴露堆栈**
  - 门禁未通过不得返回音频（阈值见 ``configs/eval/thresholds.yaml``，Phase 0 为占位）
  - 不静默降级：能力不支持时返回 ``E-CAPABILITY-001``（见 ADR-0003）
"""

from __future__ import annotations

from typing import Any, Literal

Endpoint = Literal[
    "POST /v1/presets/validate",
    "POST /v1/synthesize",
    "GET /v1/presets/{id}",
    "GET /v1/capabilities",
    "GET /v1/health",
]

#: 端点清单（API-SPEC §1.1）——Phase 4 实现时按此注册路由，不增删。
ENDPOINTS: tuple[Endpoint, ...] = (
    "POST /v1/presets/validate",
    "POST /v1/synthesize",
    "GET /v1/presets/{id}",
    "GET /v1/capabilities",
    "GET /v1/health",
)


def validate_presets(spec: dict, request_id: str | None = None) -> dict[str, Any]:
    """``POST /v1/presets/validate`` · 离线校验，不合成、不写门禁。

    流水线：解析 JSON → S 层 → preset 合并 → C 层 → 能力探测 → 降级决策 → 审计填充。
    ``200`` 返回信封（``audit_patch`` / ``resolved_spec`` 仅预览、不落库）；
    ``422`` 语义不合规；``400`` 连 S 层都过不了（``E-SCHEMA-*``）。

    Raises:
        NotImplementedError: Phase 0 占位。
    """
    raise NotImplementedError("Phase 4 实现；规格见 docs/implement/control/API-SPEC.md §3")


def synthesize(spec: dict, request_id: str | None = None) -> Any:
    """``POST /v1/synthesize`` · 校验通过后合成；``render.streaming=true`` 走 SSE / 分块。

    前置链：解析 → S 层 → preset 合并 → C 层 → 能力探测/降级 → 审计填充 → 合成 → 门禁 → 审计日志。
    非流式返回音频字节 + ``X-Request-Id`` / ``X-Audit-*``；流式返回 ``text/event-stream``。
    ``400`` 校验失败；``500`` 仅 ``E-INTERNAL-001``（带 ``request_id``，不暴露堆栈）。

    Raises:
        NotImplementedError: Phase 0 占位。
    """
    raise NotImplementedError("Phase 4 实现；规格见 docs/implement/control/API-SPEC.md §4")


def get_preset(preset_id: str, version: str | None = None) -> dict[str, Any]:
    """``GET /v1/presets/{id}`` · 读取已注册 preset（默认返回 production 版本）。

    生产准入见 PRESET-REGISTRY-SPEC / D18；Phase 0 ``registry.production == null``。

    Raises:
        NotImplementedError: Phase 0 占位。
    """
    raise NotImplementedError("Phase 4 实现；规格见 docs/implement/control/API-SPEC.md §5")


def capabilities() -> dict[str, Any]:
    """``GET /v1/capabilities`` · 返回 ``CapabilityFlags``（由基座实测回填，D19）。

    Phase 0 全部为声明值，**不是实测结果**（见 ``configs/base/base.template.yaml``）。

    Raises:
        NotImplementedError: Phase 0 占位。
    """
    raise NotImplementedError("Phase 4 实现；规格见 docs/implement/control/API-SPEC.md §6")


def health() -> dict[str, Any]:
    """``GET /v1/health`` · 存活与依赖状态（模型权重、词典、registry、水印密钥）。

    Raises:
        NotImplementedError: Phase 0 占位。
    """
    raise NotImplementedError("Phase 4 实现；规格见 docs/implement/control/API-SPEC.md §7")
