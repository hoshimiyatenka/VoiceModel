# 服务化部署与回滚 · 实施规格

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-IMPL-008 |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | [docs/AI智能体声音训练项目_技术栈方案_v0.4.md](../../AI智能体声音训练项目_技术栈方案_v0.4.md) §11 / §3.2 Phase 4 |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 定义交付形态、部署拓扑、监控、降级、回滚、水印与模型卡，衔接 API 契约与门禁报告 |

> **Phase 0 声明**：本文件是规格，**无运行中的服务**。[src/serve/api.py](../../../src/serve/api.py) 当前仅端点签名占位并 `raise NotImplementedError`。接口冻结草案见 [API-SPEC](../control/API-SPEC.md)。Q7 延迟 / RTF 等均为**目标值 / 待校准**，真源 [thresholds.yaml](../../../configs/eval/thresholds.yaml)。

## 1. 交付形态（D21 默认建议，provisional）

| 项 | 默认 | 说明 |
| --- | --- | --- |
| 主交付 | **本地权重 + 私有 API（Docker 镜像）** | 与禁商用许可一致；权重不发公有云托管 |
| 备选 | SDK / 一体机 | 视 D10 拍板结果；走 v0.5 变更评审 |
| 不入交付物 | 云端商业 TTS（D5 默认仅作质量上限对照 / 兜底） | 避免额外许可传导到发布权重 |
| 对外称谓 | 开放权重 / 源码可得（source-available, open-weight） | **不称 OSI 开源** |

> D2 若改为「离线内容生产优先」，Q7 首包延迟由软指标下调优先级，但 API 契约与 `render.streaming` 不变。

## 2. 部署拓扑（逻辑，Phase 4 实现）

| 组件 | 职责 | 依赖 | 状态 |
| --- | --- | --- | --- |
| API 网关 | 鉴权、`request_id` 注入、限流、幂等 | [API-SPEC](../control/API-SPEC.md) | 占位 |
| 控制层 | S 层 Schema → preset 合并 → C 层语义 → 能力探测 → 降级 → 审计 | [CONTROL-LAYER-SPEC](../control/CONTROL-LAYER-SPEC.md) | 占位 |
| 合成调度 | 实时 / 离线队列隔离、adapter 常驻显存、预热 | `configs/base/` capability_flags | 占位 |
| 基座 + adapter | 轨道 A 定型基座（Phase 2）+ 轨道 B 音色资产 | ADR-0002 / 模型卡 | 未选定 |
| 水印 | AudioSeal（`2401.17264`, ICML 2024, MIT）默认开 | `E-LICENSE-001` | 占位 |
| 对象存储 | 音频实体 / 权重 / checkpoint（**不入库**） | [.gitignore](../../../.gitignore) | 规划 |
| 审计日志 | `(preset_id@version, model@commit, seed, text_hash, 输出 hash)` | Q9 / F8 | 占位 |
| 监控 | 指标、告警、降级率、水印覆盖率 | §4 | 占位 |

## 3. 环境与可复现（Q9 / R-23 / R-09）

| 不变量 | 落点 |
| --- | --- |
| 依赖锁 | `locks/`（推理 / 训练分离），镜像构建时校验 hash |
| 推理栈固定 | Python / CUDA / 基座 commit / 声码器版本写进模型卡 |
| Docker digest | 门禁报告 `env` 字段（[EVAL-GATE-SPEC](../eval/EVAL-GATE-SPEC.md) §8） |
| 固定 seed | `render.seed`；同 (preset, model, seed, text) → 波形 byte-level 一致 |
| 模型卡 | 每个上线模型一份，含 `base_license` / `weight_license` / `delta_license`（[法务规格](../legal/LICENSING-IMPLEMENTATION-SPEC.md)） |

## 4. 监控与告警

| 指标 | 来源 | 告警条件 |
| --- | --- | --- |
| 首包 P95 / RTF / QPS / 显存峰值 | 服务端埋点 | 超 thresholds.yaml Q7 目标（**目标值，未校准**） |
| 硬指标回归 | 每次 checkpoint 跑 golden_set | 任一 Q1/Q2/Q4/Q8/Q9/Q10 不过 → 阻断发布 |
| 降级率 | `audit.degraded=true` 计数 | 突增 → 检查 capability_flags 回填是否失真 |
| 水印覆盖率 | `render.watermark` 实际生效比 | < 100% 且无商业授权 → 阻断（E-LICENSE-001） |
| 1000 句压测 | 发布前 | 任一 crash / 空音频 / 乱码 → 阻断（Q8） |
| 音色鉴权拒绝 | `E-LICENSE-002` | 异常频次 → 审计复核 |

> 监控阈值数字一律引用 thresholds.yaml，本文件不复制。

## 5. 降级链（与 C 层一致）

| 触发 | 行为 | 审计 |
| --- | --- | --- |
| `duration_mode=exact` 但基座无 `exact_duration` | **`E-CAPABILITY-001` 直接 400，不静默降级** | — |
| `pitch_contour` 曲线但基座不暴露中间特征 | `W-CAPABILITY-002` 降级为 native + `pitch_range` 近似 | `audit.degraded=true` |
| `attributes` 未过单调性扫描 | `W-CAPABILITY-003` 拒绝该属性，不进 production preset | `audit.degraded=true` |
| pitch/rate 主控制落到 M6 DSP | `W-RENDER-001`，仅降级路径 | `audit.degraded=true` |
| 服务过载 | 实时 / 离线队列隔离，离线排队不挤占实时 | 记录排队时长 |

> 任何降级都必须写 `audit.degraded` 并进审计日志；禁止「悄悄降级」。

## 6. 回滚

| 场景 | 回滚点 | 判定 |
| --- | --- | --- |
| 量化 / 蒸馏后质量越界（R-10） | 上一 `gs-*` 通过的 checkpoint | 全量门禁任一硬指标不过 |
| 新 preset 上线异常 | registry `production` 指针回退到上一 `gate_report` | 监控告警 + 人工确认 |
| 基座复现失败（R-09） | 锁定 commit + 依赖锁 + Docker digest 重建 | 环境 hash 不一致 |
| 服务版本异常 | 上一 Docker digest | 1000 句压测失败 |

- checkpoint 按 `step + 门禁分数` 双命名，只留 Top-K（Q1–Q4 综合分）+ 最近 3 个（[TRAINING-SPEC](../train/TRAINING-SPEC.md)）。
- 回滚手册落在 `docs/runbooks/`（Phase 4 补齐）；本版只冻结触发条件与回滚点。

## 7. 水印与合规联动

| 项 | 规则 |
| --- | --- |
| `render.watermark` | 默认 `true`（schema 单一真源） |
| 关闭水印 | 需商业授权凭证，否则 `E-LICENSE-001` 拒绝 |
| 水印 ID | 写 `audit.watermark_id`，进审计日志 |
| 音色鉴权 | `ref_audio_uri` 必须指向已注册 / 已授权说话人，否则 `E-LICENSE-002` |
| 发布前 | **D11 法务签字**（G0-2）；未签字不发布权重 |

## 8. Phase 4 准出（主方案 §3.2 / §14.2 P6）

| 条件 | 判定 |
| --- | --- |
| Q7 达标（目标值 / 待校准） | 指定硬件下压测报告 |
| 1000 句回归 0 异常 | golden_set 全量门禁报告 `gs-*` |
| 降级 / 回滚演练通过 | runbook 记录 |
| 水印覆盖率 100%（无授权场景） | 审计抽样 |
| 模型卡 + 许可字段齐全 | [法务规格](../legal/LICENSING-IMPLEMENTATION-SPEC.md) |
| D11 已签字 | G0-2 |

## 9. Phase 0 边界与待办

- 本版：仅规格 + `src/serve/api.py` 5 个端点签名占位；无容器、无编排、无监控实现。
- Phase 2：capability_flags 实测回填、基座定型。
- Phase 3：控制层与合成调度实现。
- Phase 4：容器化、监控、降级、回滚、水印、runbook。
