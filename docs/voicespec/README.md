# VoiceSpec 契约使用说明 · v0.3

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-VS-001 |
| 版本 | v0.3 |
| 日期 | 2026-11-04 |
| 状态 | **契约定义完成，实现待 Phase 3** |

## 1. 这是什么

`VoiceSpec` 是本项目**核心资产 L5 控制层**的公开契约：把「声音」拆成五层互不干扰、可单独调节、版本化的参数。模型可换，契约必须稳定（技术栈方案 §5.1）。

- 机器可读单一真源：[`configs/voicespec/voicespec.schema.json`](../../configs/voicespec/voicespec.schema.json)（JSON Schema draft 2020-12）
- 错误码：[`docs/voicespec/ERROR-CODES.md`](ERROR-CODES.md)
- 用例：[`configs/voicespec/examples/`](../../configs/voicespec/examples/)

## 2. 五层与最小请求

| 层 | 文件内 `$defs` | 职责 |
| --- | --- | --- |
| L-A | `IdentitySpec` | 是谁在说（必填 `speaker_id`） |
| L-B | `ProsodySpec` | 怎么说（连续细调主战场） |
| L-C | `StyleSpec` | 什么状态说（含候选 `AttributeSpec`） |
| L-D | `LinguisticSpec` | 把字念对（确定性规则层，零容忍） |
| L-E | `RenderSpec` | 最后怎么送出去 |

最小可用请求（[`minimal.json`](../../configs/voicespec/examples/minimal.json)）：

```json
{
  "spec_version": "0.3.0",
  "text": "你好，我是你的智能助手。",
  "identity": { "speaker_id": "agent_main" }
}
```

完整细调参看 [`full_tuned.json`](../../configs/voicespec/examples/full_tuned.json)，精确时长看 [`duration_exact.json`](../../configs/voicespec/examples/duration_exact.json)。

## 3. 三条硬规则（实现时不得违反）

1. **不静默**：所有对象 `additionalProperties:false`，拼错字段直接 `E-SCHEMA-002`；冲突一律显式报错或显式优先级，禁止静默覆盖（§5.5）。
2. **preset 是默认值集合，不是强制值**：`preset` 展开后，spec 中显式字段覆盖它；`scenario` 展开的默认值被显式 L-B/L-C 覆盖（`W-CONFLICT-007`）。
3. **确定性优先**：L-D 发音、M4 文本标记、M2 特征编辑优先于自然语言指令；`style_prompt` 不得单独作为 preset 唯一控制手段（`E-CAPABILITY-004`）。

## 4. 校验顺序（服务端）

```
1. 解析 JSON                      → 失败 400 E-SCHEMA-001
2. JSON Schema 校验（S 层）        → 失败 400/422 E-SCHEMA-* / E-DEPENDENCY-* / E-FORMAT-*
3. 解析 preset 并合并（含版本）    → 失败 400 E-PRESET-*
4. 控制层语义校验（C 层）          → 失败 400 E-CONFLICT-* / E-CAPABILITY-* / E-LICENSE-*
5. 能力探测与降级决策              → W-* 告警 + audit.degraded
6. 填充 audit.*（服务端只读）      → 客户端传 audit 则 E-AUDIT-001
7. 合成 → 门禁 → 审计日志
```

## 5. 本地校验（Python，无第三方依赖也可做结构检查）

仓库提供 [`scripts/validate_voicespec.py`](../../scripts/validate_voicespec.py)（用 `jsonschema`，见 `scripts/requirements.txt`）：

```bash
python -m pip install -r scripts/requirements.txt
python scripts/validate_voicespec.py configs/voicespec/examples/full_tuned.json
```

CI 会在 `eval-gate` 工作流中对 `examples/*.json` 全量校验（Phase 3 起启用）。

## 6. 与阈值的关系

本契约只管**参数结构与语义**；Q1–Q10 的通过阈值在 [`configs/eval/thresholds.yaml`](../../configs/eval/thresholds.yaml)，代码与文档均引用该文件，禁止硬编码数字。参数扫描门禁（5 点、Spearman ρ ≥ 0.90、UTMOS 下降 ≤ 0.30、ECAPA cos 漂移 ≤ 0.03、CER 上升 ≤ 1pp）见技术栈方案 §5.6。

## 7. 版本规则

见 [`ERROR-CODES.md` §7](ERROR-CODES.md#7-版本演进规则)。当前 `spec_version = 0.3.0`。

## 8. 待办（Phase 3）

- [ ] 实现 S 层校验器并接入两个 API
- [ ] 实现 C 层全部 `E-CONFLICT-*` / `E-CAPABILITY-*` / `E-PRESET-*` / `E-LICENSE-*`
- [ ] 实现 preset 注册与版本解析
- [ ] 每个开放参数跑完 §5.6 单调性扫描后才允许进 production preset
- [ ] `AttributeSpec` 逐属性过扫描才开放（v0.2 §5.3 第 2 条）
