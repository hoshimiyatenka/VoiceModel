"""L2 数据面 · 清洗 / 质检 / 对齐 / 标注 / 打包。Phase 0 目录占位。

规格：[`docs/implement/data/DATA-PIPELINE-SPEC.md`](../../docs/implement/data/DATA-PIPELINE-SPEC.md)、
[`DATASET-MANIFEST-SPEC.md`](../../docs/implement/data/DATASET-MANIFEST-SPEC.md)
约束：音频实体不入库（走 DVC / 对象存储）；manifest 强制 ``license_id``；D1 未拍板不采集。
实现留 Phase 1/2（[ADR-0004](../../docs/decisions/ADR-0004.md) / D16）：本包只有占位，无实现代码。
"""
