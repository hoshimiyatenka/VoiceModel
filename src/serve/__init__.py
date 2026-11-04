"""L6 服务 / 交付面 · 签名占位。

接口规格：[`docs/implement/control/API-SPEC.md`](../../docs/implement/control/API-SPEC.md)（5 端点冻结草案）
部署规格：[`docs/implement/serve/DEPLOYMENT-SPEC.md`](../../docs/implement/serve/DEPLOYMENT-SPEC.md)（交付形态 D21：本地权重 + 私有 API）
状态：**Phase 0 签名占位**，实现留 Phase 4（[ADR-0004](../../docs/decisions/ADR-0004.md) / D16）。
"""

from .api import (
    ENDPOINTS,
    capabilities,
    get_preset,
    health,
    synthesize,
    validate_presets,
)

__all__ = [
    "ENDPOINTS",
    "capabilities",
    "get_preset",
    "health",
    "synthesize",
    "validate_presets",
]
