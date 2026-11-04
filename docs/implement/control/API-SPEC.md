# 推理服务 API 契约（OpenAPI 3.1 风格） · VoiceModel

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | docs/AI智能体声音训练项目_技术栈方案_v0.4.md |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 冻结 L5 控制层对外接口的端点、请求/响应 JSON、错误码→HTTP 映射、流式协议、鉴权与幂等策略，供 Phase 3 实现 |

## 0. 边界声明（先读）

| # | 声明 |
| --- | --- |
| 1 | **Phase 0 无服务实现**：本文件是**接口冻结草案**，不是已上线服务。无训练产出、无模型权重、无实测指标；所有延迟 / 质量数字均为目标值，写「见 thresholds.yaml」。 |
| 2 | **不改契约**：v0.4 不修改 [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json)、不升 `spec_version`（`const "0.3.0"`）、无 `BREAKING CHANGE`。 |
| 3 | **错误码冻结**：只使用 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) 已登记码，稳定、只追加、不改义/复用、不自造。 |
| 4 | **两层校验**：S 层（Schema）+ C 层（Control）。本文件端点接入顺序见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §4。 |
| 5 | **许可口径**：对外称「开放权重 / 源码可得(source-available, open-weight)」，**不称 OSI 开源**；项目自有增量 PolyForm Noncommercial 1.0.0（禁商用）+ 双授权；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游；ADR-0001 不用 Spark-TTS 权重（`cc-by-nc-sa-4.0` SA 传染）。 |
| 6 | **基座未定**：轨道 A 候选 CosyVoice 2 / Qwen3-TTS / VoxCPM2（均 Apache-2.0），Phase 2 同台实测定型；`capabilities` 返回的是声明值，非「已选定」。 |
| 7 | **阈值单一真源**：Q7 首包延迟、Q1–Q10 一律「见 [`thresholds.yaml`](../../../configs/eval/thresholds.yaml)」（`calibration.status=uncalibrated`），数字不写成结论。 |
| 8 | **许可文件保护**：不修改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md`；不写任何真实密钥 / token / 凭据。 |
| 9 | **编号归属**：沿用 F1–F8 / Q1–Q10、D1–D15、R-01–R-18、ADR-0001–0003；新增编号由 Lead 统一分配，本文件只引用已分配项（R-08 / R-20 / R-21）。

> 交叉引用：[`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md)（校验流水线）、[`PRESET-REGISTRY-SPEC.md`](PRESET-REGISTRY-SPEC.md)（preset 解析）、[`voicespec/README.md`](../../voicespec/README.md) §4（校验顺序）、[`ADR-0003.md`](../../decisions/ADR-0003.md)（决策）。

## 1. 总览

| 项 | 内容 |
| --- | --- |
| 协议 | HTTP/1.1 + JSON；流式用 SSE（Server-Sent Events）或二进制 chunk，见 §8 |
| 基址 | `/v1`（Phase 0 未部署，无真实 host） |
| OpenAPI | 3.1（本文为 Markdown 描述，Phase 3 落 `openapi.yaml` 时必须逐字映射，不得增删字段） |
| 请求体契约 | [VoiceSpec JSON Schema](../../../configs/voicespec/voicespec.schema.json)（单一真源） |
| 响应信封 | `valid` / `errors[]` / `warnings[]`，照抄 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) §2 |
| 审计 | `audit.*` 为**服务端只读**字段，由控制层填充（见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §8）；客户端传入 → `E-AUDIT-001` |
| 全链路标识 | `request_id`，客户端可传 `X-Request-Id`，缺省服务端生成；贯穿请求 / 错误 / 审计 / 日志 |

### 1.1 端点清单

| 方法 | 路径 | 用途 | 成功 | 校验失败 | 关联错误码 |
| --- | --- | --- | --- | --- | --- |
| `POST` | `/v1/presets/validate` | 仅校验 VoiceSpec（含 preset 展开）不合成 | `200` | **`422`** | S 层 + C 层全部码（请求体合法但内容不合规） |
| `POST` | `/v1/synthesize` | 合成（支持 `render.streaming`） | `200` / SSE 流 | **`400`** | S 层 + C 层全部码 |
| `GET` | `/v1/presets/{id}` | 读 preset 注册信息 | `200` | `404` | — |
| `GET` | `/v1/capabilities` | 读当前 capability flags（Phase 0 声明值） | `200` | — | — |
| `GET` | `/v1/health` | 存活性 / 版本 / 相位 | `200` | — | — |

> 状态码区分：`/v1/presets/validate` 请求体本身是合法 JSON Schema 实例但内容不合规 → **422**；`/v1/synthesize` 任何校验失败一律 **400**（见 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) §2）。`E-INTERNAL-001` 是唯一 500。

## 2. 公共结构

### 2.1 响应信封（照抄 ERROR-CODES.md §2）

```json
{
  "valid": false,
  "errors": [
    {
      "code": "E-CONFLICT-001",
      "layer": "control",
      "path": "prosody",
      "message": "rate 与 duration_mode=exact 互斥，不能同时给出",
      "detail": { "rate": 0.92, "duration_mode": "exact" },
      "hint": "二选一：删除 rate，或改用 duration_mode=free + rate",
      "doc": "https://github.com/hoshimiyatenka/VoiceModel/blob/main/docs/voicespec/ERROR-CODES.md#e-conflict-001"
    }
  ],
  "warnings": [
    {
      "code": "W-PRESET-001",
      "path": "style",
      "message": "style_prompt 仅作修饰，已写入审计日志；emotion 优先"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `valid` | bool | `errors == []` 为真；`warnings` 不阻断 |
| `errors[]` | object[] | `code` / `layer` / `path` / `message` / `detail` / `hint` / `doc`，见 `ValidationIssue`（[`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §2） |
| `warnings[]` | object[] | 同结构，`severity="warning"`；必须进审计日志 |

> 注意：上例 `W-PRESET-001` 仅为 ERROR-CODES.md §2 信封的**示意告警码**，不在 §4 控制层登记表内；Phase 3 实现必须以 §4 已登记码为准，不得自造。本文 §5 映射表只列 §3/§4 已登记码。

### 2.2 只读审计字段

`audit.*` 结构见 [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json) 的 `AuditSpec`：`request_id` / `license`（`const "PolyForm-Noncommercial-1.0.0"`）/ `model_commit` / `preset_resolved` / `gate_report` / `golden_set_passed` / `watermark_id` / `degraded`。

| 规则 | 说明 |
| --- | --- |
| 服务端填充 | 由 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §8 `AuditPatch` 生成，客户端不可写 |
| 客户端传入 | → `E-AUDIT-001`（合成 400 / 校验 422） |
| 默认值 | `render.watermark=true` 时 `watermark_id` 由服务端写入；`degraded` 由降级链汇总 |
| Phase 0 | 无 `model_commit` / `gate_report` / `golden_set_passed` 实测值，字段为 `None` / 不写入 |

## 3. POST /v1/presets/validate

| 项 | 内容 |
| --- | --- |
| 用途 | 离线校验：S 层 → preset 合并 → C 层语义 → 能力探测 → 降级决策 → 审计填充（**不合成、不写门禁**） |
| 请求体 | 一个 VoiceSpec JSON 实例（[schema](../../../configs/voicespec/voicespec.schema.json)），`Content-Type: application/json` |
| 成功 `200` | `{"valid": true, "errors": [], "warnings": [...], "audit_patch": {...}, "resolved_spec": {...}}`（`audit_patch` / `resolved_spec` 为服务端预览，不落库） |
| 失败 `422` | 标准信封，`valid=false`，`errors[]` 含具体码；请求体本身合法 JSON Schema 实例但语义不合规 |
| 失败 `400` | 仅当请求体**不是**合法 JSON / 不是 Schema 实例（连 S 层都过不了）时按 `E-SCHEMA-*` 归入 400；与 422 的边界由「是否通过 S 层」判定 |
| 调用链 | 见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §4 步骤 1–6 |

请求示例：

```http
POST /v1/presets/validate HTTP/1.1
Content-Type: application/json
X-Request-Id: req-20261104-0001

{
  "spec_version": "0.3.0",
  "text": "你好，我是你的智能助手。",
  "identity": { "speaker_id": "agent_main" }
}
```

## 4. POST /v1/synthesize

| 项 | 内容 |
| --- | --- |
| 用途 | 校验通过后合成音频；支持 `render.streaming=true` 走 §8 流式 |
| 请求体 | 一个 VoiceSpec JSON 实例（[schema](../../../configs/voicespec/voicespec.schema.json)） |
| 成功 `200`（非流式） | `Content-Type` 按 `render.format`（`wav` / `pcm_s16le` / `opus` / `mp3`）；`X-Request-Id` 回传；`X-Audit-*` 头带 `preset_resolved` / `watermark_id` / `degraded` |
| 成功 `200`（流式） | `text/event-stream` 或分块二进制，见 §8 |
| 校验失败 `400` | 标准信封；S 层 / C 层任一错误码 |
| 内部错误 `500` | `E-INTERNAL-001`，带 `request_id`，不暴露堆栈 |

**合成前置链**：解析 JSON → S 层 → preset 合并 → C 层 → 能力探测 / 降级 → 审计填充 → 合成 → 门禁（阈值见 `thresholds.yaml`）→ 审计日志。门禁未通过不得返回音频（Phase 0 门禁为占位，Phase 2 接入 golden_set）。

最小请求（同 [`minimal.json`](../../../configs/voicespec/examples/minimal.json)）：

```json
{
  "spec_version": "0.3.0",
  "text": "你好，我是你的智能助手。",
  "identity": { "speaker_id": "agent_main" }
}
```

## 5. GET /v1/presets/{id}

| 项 | 内容 |
| --- | --- |
| 用途 | 读 preset 注册信息（不含音频、不含权重） |
| 路径参数 | `id` = `preset_id`（小写 `[a-z0-9_-]`） |
| 成功 `200` | 返回注册条目：`preset_id` / `versions[]` / `production` / `schema_ref`，字段定义见 [`PRESET-REGISTRY-SPEC.md`](PRESET-REGISTRY-SPEC.md) |
| `404` | ID 未注册；与 `E-PRESET-001`（请求体引用不存在 ID）不同：这是读接口，不返回校验信封 |
| Phase 0 | 仅 `template` 状态示例，无 `production`；不得据此认为有可用 business preset |

## 6. GET /v1/capabilities

| 项 | 内容 |
| --- | --- |
| 用途 | 返回 `CapabilityFlags`（[`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §2/§6），供客户端预判 `E-CAPABILITY-001` 等 |
| 成功 `200` | 见下 |
| Phase 0 | **全为声明值、未实测**；Phase 2 基座同台实测定型后回填 |

```json
{
  "phase": 0,
  "calibration": "uncalibrated",
  "base_candidate": ["CosyVoice 2", "Qwen3-TTS", "VoxCPM2"],
  "capabilities": {
    "exact_duration": false,
    "f0_contour": false,
    "attribute_control": false,
    "style_prompt": false,
    "voice_blend": false
  },
  "note": "声明值，非实测；Phase 2 同台实测定型后回填。"
}
```

| 字段 | 说明 |
| --- | --- |
| `exact_duration=false` | 此时请求 `duration_mode=exact` 必得 `E-CAPABILITY-001`（直接报错，不静默降级） |
| `base_candidate` | 轨道 A 三候选均 Apache-2.0，未写「已选定」 |

## 7. GET /v1/health

```json
{
  "status": "ok",
  "phase": 0,
  "spec_version": "0.3.0",
  "license": "PolyForm-Noncommercial-1.0.0",
  "license_positioning": "开放权重/源码可得(source-available, open-weight)，非 OSI 开源",
  "calibration": "uncalibrated",
  "trained_model": false,
  "measured_metrics": false
}
```

| 字段 | 含义 |
| --- | --- |
| `phase: 0` | 立项 / 选型核验期，无训练产出 |
| `trained_model: false` / `measured_metrics: false` | 明确「无模型权重、无实测指标」，禁止写成「已上线」 |
| `license_positioning` | 对外口径，见 §0-5 |

## 8. 错误码 → HTTP 状态映射

| HTTP | 适用端点 | 错误码集合 | 说明 |
| --- | --- | --- | --- |
| `400` | `/v1/synthesize` | `E-SCHEMA-001..006`、`E-DEPENDENCY-001..003`、`E-RANGE-001`、`E-FORMAT-001..002`、`E-CONFLICT-001..005`、`E-CAPABILITY-001/004`、`E-PRESET-001/002`、`E-AUDIT-001`、`E-LICENSE-001/002` | 校验失败一律 400；`W-*` 告警不在此列（不阻断） |
| `422` | `/v1/presets/validate` | 同上全部 S/C 层错误码 | 请求体是合法 Schema 实例但内容不合规 |
| `500` | 全部 | `E-INTERNAL-001` | 外层异常边界统一包装，带 `request_id`，不暴露堆栈 |
| `404` | `/v1/presets/{id}` | 无校验信封 | 读接口的资源不存在 |
| `200` + `warnings[]` | `/v1/synthesize`、`/v1/presets/validate` | `W-CONFLICT-006/007`、`W-CAPABILITY-002/003`、`W-RENDER-001` | 告警不阻断，`valid=true`，必须进审计日志 |

| 关键映射 | 码 | HTTP |
| --- | --- | --- |
| `rate` ↔ `duration_*` 互斥 | `E-CONFLICT-001` | 400 / 422 |
| `Σpauses > duration_ms × 0.4` | `E-CONFLICT-002` | 400 / 422 |
| `voice_blend` + `speaker_lock=true` | `E-CONFLICT-004` | 400 / 422 |
| 精确时长能力缺失 | `E-CAPABILITY-001` | 400 / 422（**不降级**） |
| `style_prompt` 唯一控制手段 | `E-CAPABILITY-004` | 400 / 422 |
| 关闭水印无授权 | `E-LICENSE-001` | 400 / 422 |
| `ref_audio_uri` 未注册 | `E-LICENSE-002` | 400 / 422 |
| 客户端传 `audit.*` | `E-AUDIT-001` | 400 / 422 |
| 已判定不冲突（正常不返回） | `E-CONFLICT-003` / `E-CONFLICT-005` | — |

完整逐码 `layer` / `path` / `hint` 见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 与 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) §3/§4。

## 9. request_id 全链路透传与幂等

| 项 | 内容 |
| --- | --- |
| 注入 | 客户端 `X-Request-Id`（可选）→ 服务端采用；缺省生成 UUID 形态 ID，**不得含凭据** |
| 透传 | `ControlContext.request_id` → `AuditPatch.request_id` → `audit.request_id` → 错误信封 `detail.request_id` → 访问日志 / 门禁报告 |
| 响应 | 所有响应回带 `X-Request-Id`；`E-INTERNAL-001` 必须携带 |
| 幂等键 | 非流式合成：幂等键 = `(spec_version, model_commit, preset_id, preset_resolved, seed, text, 规范化后 spec)` 的哈希；相同键 + 相同依赖锁 → 依 Q9 返回 byte-level 一致结果（目标值，待 Phase 2 校准，见 `thresholds.yaml`） |
| 重复请求 | 相同 `X-Request-Id` 在短窗口内命中缓存则复用结果，避免重复计费 / 重复审计；缓存键不含任何真实密钥 |
| 流式 | 流式请求**不做结果缓存**，但 `request_id` 仍贯穿每个 chunk 的元数据 |

## 10. 流式协议

| 项 | 内容 |
| --- | --- |
| 触发 | `render.streaming=true`；`render.chunk_ms` 默认 `200`（范围 `[20, 2000]`，见 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) §6 / [schema](../../../configs/voicespec/voicespec.schema.json) `RenderSpec`） |
| 传输 | SSE（`text/event-stream`）事件 `meta` / `audio` / `end` / `error`；或分块二进制（`render.format` 决定编码） |
| 首包延迟目标 | **见 `thresholds.yaml` Q7**（`first_packet_p95_ms`），Phase 0 为未校准目标值，不写数字结论 |
| 跨 chunk 韵律连续性 | 边界处 F0 跳变听审专项测试（R-08）；全局 duration 预算在首 chunk 前分配，不在 chunk 内重算 |
| exact 时长全局预算 | `duration_mode=exact` 时，**整句** `duration_ms` 在流式开始前一次性分配到各 chunk；跨 chunk 累计误差仍须满足 Q6（阈值见 `thresholds.yaml`）。呼应 R-08：禁止逐 chunk 独立计时 |
| 能力前置 | 流式 + `duration_mode=exact` 仍须过 `E-CAPABILITY-001` 能力探测；能力缺失直接 400，不进流式 |
| 错误中途中止 | 已发 `audio` 后遇内部错误 → 发 `error` 事件（`code=E-INTERNAL-001` + `request_id`），不伪造成功 `end` |

SSE 事件骨架：

```
event: meta
data: {"request_id":"req-20261104-0001","preset_resolved":"...","watermark_id":"..."}

event: audio
data: {"seq":0,"chunk_ms":200,"format":"opus","b64":"<base64 音频分片>"}

event: end
data: {"chunks":12,"degraded":false,"audit":{...}}
```

## 11. 鉴权、水印与合规联动

| 规则 | 码 | 行为 |
| --- | --- | --- |
| `render.watermark` 默认 `true` | — | 默认开启；水印方案见 AudioSeal `arXiv:2401.17264`（MIT），`audit.watermark_id` 由服务端填充 |
| 关闭水印（`watermark=false`）无商业授权凭证 | `E-LICENSE-001` | 拒绝（400 / 422）。商业授权走双授权，见 `LICENSE-COMMERCIAL.md`；本文件不写任何真实凭证 |
| `ref_audio_uri` 指向未注册 / 未授权说话人音频 | `E-LICENSE-002` | 拒绝（音色注册鉴权）；`ctx.speaker_registry` 判定见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 #17 |
| `audit.*` 客户端只读 | `E-AUDIT-001` | 拒绝；服务端填充 `audit.license = PolyForm-Noncommercial-1.0.0` |
| 上游权重 | — | 上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游；项目自有增量才受 NC 约束 |

## 12. Phase 0 冻结声明与开放项

| 项 | 状态 |
| --- | --- |
| 本文件 | **接口冻结草案**：字段、端点、状态码、映射表冻结，Phase 3 落 `openapi.yaml` 须逐字映射，不得增删 |
| 服务实现 | ⏳ 无。无训练产出、无模型权重、无实测指标 |
| capability flags | ⏳ Phase 2 基座同台实测定型后回填；Phase 0 全为声明值 |
| 流式 / 门禁 / 水印运行时 | ⏳ Phase 2–3；Q6/Q7/Q9 阈值见 `thresholds.yaml`（`uncalibrated`） |
| `W-PRESET-001` 示意码 | 仅出现在 §2.1 照抄的信封示例，不在 §4 登记表；实现以 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) §4 为准 |
| D11 许可法务定稿 | 仍为发布权重前阻塞项；本接口不触碰权重发布 |
| R-14b 法务跟进 | 仍开放 |
| R-20 错误码漂移 | 由 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §9 自动核对缓解 |
| R-21 / 未过门禁 preset | 见 [`PRESET-REGISTRY-SPEC.md`](PRESET-REGISTRY-SPEC.md)：Phase 0 只有 `template`，不得标 `production` |

**追溯**：F5 / F6 / F8（preset 复现、流式、版本化审计）、Q6 / Q7 / Q9（时长 / 实时性 / 可复现）、R-08（流式 chunk 边界）、ADR-0003 §6/§7（许可联动、可复现性）。
