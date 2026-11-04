# 实施规格总索引 · v0.4

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | [docs/AI智能体声音训练项目_技术栈方案_v0.4.md](../AI智能体声音训练项目_技术栈方案_v0.4.md) §15 |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 九份实施规格的入口、状态表、阅读顺序与统一约束摘要 |

> **Phase 0 统一声明**：本目录下全部文件是**规格，不是实现**。全项目无训练产出、无模型权重、无实测指标、无运行中的服务。所有数值为**目标值 / 待校准**，阈值真源 [configs/eval/thresholds.yaml](../../configs/eval/thresholds.yaml)（`calibration.status=uncalibrated`）。对应 `src/**` 为签名占位并 `raise NotImplementedError`（[ADR-0004](../decisions/ADR-0004.md)）。

## 1. 九份规格状态表

| # | 文件 | 覆盖 | 主方案章节 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | [control/CONTROL-LAYER-SPEC.md](control/CONTROL-LAYER-SPEC.md) | C 层函数签名 / 18 码逐码判定 / capability flags / 降级 / 单测组织 | §7 | 规格已落盘，C 层 Phase 3 实现 |
| 2 | [control/API-SPEC.md](control/API-SPEC.md) | 5 端点 / 响应信封 / HTTP 映射 / SSE 流式 / 鉴权水印 | §7 / §11 | 接口冻结草案 |
| 3 | [control/PRESET-REGISTRY-SPEC.md](control/PRESET-REGISTRY-SPEC.md) | registry 字段 / semver / 默认值展开 / 生产准入 | §7.4 | 规格；registry `production: null` |
| 4 | [data/DATA-PIPELINE-SPEC.md](data/DATA-PIPELINE-SPEC.md) | ①–⑧ 流水线 / 工具链许可 / 授权 / 防泄漏 | §8 | 规格；D1 未拍板不采集 |
| 5 | [data/DATASET-MANIFEST-SPEC.md](data/DATASET-MANIFEST-SPEC.md) | manifest 字段 schema / golden_set 冻结与 CI hash | §8 | 字段规范已定，无实体数据 |
| 6 | [train/TRAINING-SPEC.md](train/TRAINING-SPEC.md) | SFT→DPO→量化 / 命名 / 回滚 / Q9 可复现 | §9 | 规格；三阶段模板已落盘 |
| 7 | [eval/EVAL-GATE-SPEC.md](eval/EVAL-GATE-SPEC.md) | 四套数据集 / 门禁流程 / 参数扫描 Harness / `gs-*` 报告 | §10 | 规格；自动门禁 Phase 2 |
| 8 | [serve/DEPLOYMENT-SPEC.md](serve/DEPLOYMENT-SPEC.md) | 交付形态 / 监控 / 降级 / 回滚 / 水印 / 模型卡 | §11 | 规格；Phase 4 实现 |
| 9 | [legal/LICENSING-IMPLEMENTATION-SPEC.md](legal/LICENSING-IMPLEMENTATION-SPEC.md) | D11 清单 / R-14b 九项 / 模型卡许可字段 / 发布前检查 | §12 | 清单；**D11 未签字** |

## 2. 阅读顺序

| 目的 | 顺序 |
| --- | --- |
| 从零接手实施 | 本索引 → 主方案 §3（阶段门）→ §5（决策）→ §13（风险）→ 下表按角色 |
| 控制层 / API / preset | 1 → 2 → 3 → [ERROR-CODES.md](../voicespec/ERROR-CODES.md) → [schema](../../configs/voicespec/voicespec.schema.json) |
| 数据 / 训练 | 4 → 5 → 6 → [thresholds.yaml](../../configs/eval/thresholds.yaml) |
| 评估 / 运维 | 7 → 8 → [COMMIT_CONVENTION.md](../../COMMIT_CONVENTION.md) |
| 法务 / 合规 | 9 → [许可证矩阵](../licensing/UPSTREAM-LICENSE-MATRIX.md) → [LICENSE](../../LICENSE) |

## 3. 统一约束摘要（九份规格共同遵守）

| 项 | 约束 |
| --- | --- |
| 阶段 | Phase 0；规格 / 模板 / 骨架 / CI，不写实现（D16 / ADR-0004） |
| 契约 | VoiceSpec JSON Schema 2020-12、`spec_version="0.3.0"`、全对象 `additionalProperties:false`；**v0.4 不改 schema、不升版本、无 BREAKING CHANGE** |
| 校验 | S 层(Schema) → preset 合并 → C 层(Control) → 能力探测 → 降级 → 审计 |
| 错误码 | [ERROR-CODES.md](../voicespec/ERROR-CODES.md) 唯一真源，**只追加、不得自造 / 改义** |
| 控制优先级 | `M4 > M2(连续) > M1(离散) > M5 > M3 > M6(DSP 仅降级)`（ADR-0003） |
| 基座 | CosyVoice 2 / Qwen3-TTS / VoxCPM2（Apache-2.0），Phase 2 同台实测定型，**不写已选定**；不用 Spark-TTS 权重（ADR-0001） |
| 需求 / 质量编号 | F1–F8 / Q1–Q10 沿用 v0.1，不得新增 / 改义 |
| 决策 / 风险编号 | D1–D22（主方案 §5）/ R-01–R-24（主方案 §13）统一编号，规格不发明新号 |
| 阈值 | 一律「见 thresholds.yaml」，禁止复制数字；`uncalibrated` 期间不得写「实测 / 已达 / 达标」（R-22） |
| 许可 | 称「开放权重 / 源码可得(source-available, open-weight)」，**不称 OSI 开源**；自有增量 PolyForm NC 1.0.0 + 双授权；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游 |
| R-18 | 代码许可 ≠ 权重许可；矩阵拆两列、模型卡强制 `base_license` / `weight_license` / `delta_license` |
| preset | `registry.production=null`（Phase 0）；production 须 `gate_report` + golden_set + 2 人批准（D18 / R-21） |
| 数据 | 音频实体不入库；manifest 强制 `license_id`；golden_set 绝对冻结（D20） |
| 变更 | `docs/implement/**` / `configs/**` / `src/**` 骨架走 PR，带 `Impl:` footer（[COMMIT_CONVENTION.md](../../COMMIT_CONVENTION.md) §5）与 CODEOWNERS 保护 |

## 4. 与代码 / 配置 / CI 的对应

| 规格 | 对应骨架 / 模板 / CI |
| --- | --- |
| 1 / 2 | [src/control/validator.py](../../src/control/validator.py) · [src/serve/api.py](../../src/serve/api.py) |
| 3 | [configs/presets/registry.yaml](../../configs/presets/registry.yaml) · [warm_companion.template.yaml](../../configs/presets/examples/warm_companion.template.yaml) |
| 4 / 5 | `src/data/` · `datasets/manifests/`（无实体数据） · [.gitignore](../../.gitignore) |
| 6 | [configs/train/](../../configs/train/) 三模板 · [configs/base/base.template.yaml](../../configs/base/base.template.yaml) |
| 7 | [scripts/check_consistency.py](../../scripts/check_consistency.py) · [tests/unit/test_spec_consistency.py](../../tests/unit/test_spec_consistency.py) · [eval-gate.yml](../../.github/workflows/eval-gate.yml) |
| 8 | [src/serve/api.py](../../src/serve/api.py) · `docs/runbooks/`（Phase 4） |
| 9 | [NOTICE](../../NOTICE) · [LICENSE-COMMERCIAL.md](../../LICENSE-COMMERCIAL.md) · [license-check.yml](../../.github/workflows/license-check.yml) |

## 5. 已知缺口（v0.5 回填，不算本版失败）

| 缺口 | 归属 | 处理 |
| --- | --- | --- |
| C 层 18 码实现代码 | Phase 3 | [CONTROL-LAYER-SPEC](control/CONTROL-LAYER-SPEC.md) 定规格与单测组织 |
| `voice_blend` 且 `speaker_lock=false` 缺专用错误码 | 错误码表 | 规格已登记为缺口；**实现前须经 v0.5 评审追加**（只追加，不改义） |
| `W-PRESET-001` 出现在 ERROR-CODES.md §2 信封示意但未在 §4 登记 | 错误码表 | 信封示意加注「不得自造」；v0.5 决定是否正式登记 |
| golden_set 实体 / `datasets/golden_set/manifest.yaml` | Phase 1 | [DATASET-MANIFEST-SPEC](data/DATASET-MANIFEST-SPEC.md) 定生成与冻结流程 |
| capability_flags 真实值 | Phase 2 | [base.template.yaml](../../configs/base/base.template.yaml) 全部 `null` 待实测回填 |
| D1–D11 拍板 / D11 法务签字 / R-14b 九项 | G0 | 主方案 §3.3 / §5 / §12；v0.5 回填 |

## 6. 收敛

v0.4（规格全量）→ v0.5（评审回填 + D 拍板 + 法务清单）→ v1.0（冻结）→ 档 B 实施（主方案 §14.3 / D22）。历史归档只增不改。
