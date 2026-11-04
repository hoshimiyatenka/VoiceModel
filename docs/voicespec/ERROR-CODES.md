# VoiceSpec 校验错误码表 · v0.3

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-VS-002 |
| 版本 | v0.3 |
| 日期 | 2026-11-04 |
| 关联 | [`configs/voicespec/voicespec.schema.json`](../../configs/voicespec/voicespec.schema.json)、[`docs/voicespec/README.md`](README.md)、技术栈方案 §5 / §9 |

## 1. 两层校验分工

| 层 | 负责 | 技术 | 失败阶段 |
| --- | --- | --- | --- |
| **S 层（Schema）** | 结构、类型、范围、枚举、`additionalProperties:false`、可静态判定的字段依赖 | JSON Schema draft 2020-12（本仓库 schema 文件） | `POST /v1/presets/validate` 与 `POST /v1/synthesize` 入口，**先于**语义层 |
| **C 层（Control）** | 跨字段语义冲突、preset 合并、能力探测、降级决策、审计填充 | L5 控制层代码（Phase 3 实现） | S 层通过后 |

**原则**：能用 Schema 静态表达的绝不放进 C 层手写 if；Schema 表达不了的（如「Σpauses < duration_ms × 0.4」这类跨字段算术）才落 C 层，并在此文档登记。`additionalProperties:false` 覆盖全部对象，拼错字段直接拒，禁止静默忽略。

## 2. 响应信封

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

- HTTP：`POST /v1/synthesize` 校验失败一律 **400**；`POST /v1/presets/validate` 失败 **422**（请求体本身合法，但内容不合规）。
- `valid=true` 时 `errors` 为 `[]`；`warnings` 不阻断合成，但必须进审计日志。
- 错误码稳定，**不得复用或改义**；新增只追加。

## 3. Schema 层错误码（S）

| 码 | 触发 | schema 落点 | 客户端修复 |
| --- | --- | --- | --- |
| `E-SCHEMA-001` | 请求体不是对象 / 缺 `text` / 缺 `identity` | 顶层 `type` / `required` | 补齐必填字段 |
| `E-SCHEMA-002` | 未知字段（任意层） | 各对象 `additionalProperties:false` | 删除或改正拼写；契约不忽略任何字段 |
| `E-SCHEMA-003` | 类型不符（string/int/bool/array/object） | 各 `type` | 按契约类型传值 |
| `E-SCHEMA-004` | 数值越界 | `minimum`/`maximum`/`enum` | 见 §6 参数范围速查 |
| `E-SCHEMA-005` | 枚举值不在集合内 | 各 `enum` | 改用合法枚举 |
| `E-SCHEMA-006` | `spec_version` 不等于 `0.3.0` | `const` | 升级客户端契约 |
| `E-DEPENDENCY-001` | 给了 `ref_text` 但没给 `ref_audio_uri` | `IdentitySpec.allOf[0]` | 成对给出或删除 |
| `E-DEPENDENCY-002` | `duration_mode=exact` 但缺 `duration_ms` | `ProsodySpec.allOf[0]` | 补 `duration_ms` |
| `E-DEPENDENCY-003` | `duration_mode=range` 但缺 `duration_range_ms` | `ProsodySpec.allOf[1]` | 补 `duration_range_ms` |
| `E-RANGE-001` | `duration_range_ms.min > max`，或 `Span.start >= end` | C 层（schema 无法表达跨字段比较） | 修正区间 |
| `E-FORMAT-001` | `ref_audio_uri` / `emotion_ref_uri` 非 URI，或用了 `data:` 内联二进制 | `Uri` format + description | 用对象存储 URI |
| `E-FORMAT-002` | `text` 为空 / 超 5000 字符 | `minLength`/`maxLength` | 分片或裁剪 |

## 4. 控制层错误码（C）

### 4.1 冲突类（对应 §5.5 冲突消解矩阵，一律显式）

| 码 | 冲突对 | 规则 | 来源 |
| --- | --- | --- | --- |
| `E-CONFLICT-001` | `rate` ↔ `duration_mode=exact/range` / `duration_ms` / `duration_ratio` / `duration_range_ms` | **互斥，同时显式给出即 400**（schema 的 `not` 也静态拦截一部分） | §5.5 第 1 行；v0.2 论文依据 IndexTTS2 `2506.21619` |
| `E-CONFLICT-002` | `duration_ms` ↔ `pauses[]` | 允许共存，但 `Σpauses.ms > duration_ms × 0.4` 报错 | §5.5 第 2 行 |
| `E-CONFLICT-003` | `energy_db` ↔ `loudness_lufs` | **不冲突**：前者表现力、后者交付响度；同时生效，loudness 最后做。仅当用户显式声明互斥意图时报错 | §5.5 第 3 行 |
| `E-CONFLICT-004` | `voice_blend` ↔ `speaker_lock=true` | 锁定时禁止 blend（只允许单一音色） | §5.5 第 7 行 |
| `E-CONFLICT-005` | `pitch_semitones` ↔ `pitch_contour`(曲线) | **不冲突**：contour 为相对形状，semitones 为全局偏移，叠加生效 | §5.5 第 6 行 |
| `W-CONFLICT-006` | `emotion` ↔ `style_prompt` | 离散优先；`style_prompt` 仅作修饰，写审计日志 | §5.3、§5.5 第 4 行 |
| `W-CONFLICT-007` | `scenario` ↔ 显式 L-B/L-C 参数 | 显式值覆盖 scenario 展开默认值（preset 是默认值集合，不是强制值） | §5.5 第 5 行 |

> `E-CONFLICT-003` / `E-CONFLICT-005` 登记为「已判定不冲突」是为了避免后续实现误加互斥校验；正常不返回。

### 4.2 能力与降级类

| 码 | 触发 | 行为 |
| --- | --- | --- |
| `E-CAPABILITY-001` | 请求的 `duration_mode=exact` 但当前基座不支持显式时长头 | **报错 400**，不静默降级（F4 升 P0 后属硬能力） |
| `W-CAPABILITY-002` | 请求 `pitch_contour` 曲线但基座不暴露中间特征 | 降级为 `pitch_contour=native` + `pitch_range` 近似，`audit.degraded=true`，告警 |
| `W-CAPABILITY-003` | 请求 `attributes` 但该属性未过 §5.6 单调性扫描 | 拒绝该属性并告警，**不得进 production preset**（v0.2 §5.3 第 2 条） |
| `E-CAPABILITY-004` | `style_prompt` 作为 preset 唯一控制手段 | 违反 v0.2 §3.3 / §5.3 第 4 条，preset 校验失败 |
| `W-RENDER-001` | 任何 pitch/rate 主控制落到 M6 DSP | 仅允许作降级路径，必须 `degraded=true` + 告警（§5.4 禁忌） |

### 4.3 Preset 与审计类

| 码 | 触发 | 行为 |
| --- | --- | --- |
| `E-PRESET-001` | `preset` 引用不存在的 ID / 版本 | 400 |
| `E-PRESET-002` | `preset_version` 非法或与注册版本不符 | 400 |
| `E-AUDIT-001` | 客户端传入 `audit.*` 只读字段 | 拒绝（该字段只由服务端填充） |
| `E-LICENSE-001` | `render.watermark=false` 且无商业授权凭证 | 拒绝；水印默认 true，关闭需授权（§2.6 / LICENSE-COMMERCIAL.md） |
| `E-LICENSE-002` | `ref_audio_uri` 指向未注册 / 未授权说话人音频 | 拒绝（音色注册鉴权） |

### 4.4 内部错误

| 码 | 含义 |
| --- | --- |
| `E-INTERNAL-001` | 控制层未预期异常（500），携带 `request_id`，不暴露堆栈 |

## 5. 错误码 ↔ schema 约束对照（实现核对表）

| 错误码 | 由谁判定 | 是否已在本版 schema 实现 |
| --- | --- | --- |
| `E-DEPENDENCY-001/002/003` | Schema `allOf.if/then` | ✅ 已实现 |
| `E-CONFLICT-001`（部分） | Schema `ProsodySpec.not` | ✅ 静态部分已实现；`duration_mode=free + duration_ms` 组合留给 C 层 |
| `E-CONFLICT-004` | C 层（跨 identity 两字段） | ⏳ Phase 3 |
| `E-CONFLICT-002` / `E-RANGE-001` | C 层（跨字段算术/比较） | ⏳ Phase 3 |
| `E-CAPABILITY-*` / `E-PRESET-*` / `E-AUDIT-*` / `E-LICENSE-*` | C 层 | ⏳ Phase 3 |
| 全部 `E-SCHEMA-*` / `E-FORMAT-*` | Schema | ✅ 已实现 |

## 6. 参数范围速查（与 schema 单一真源同步）

| 参数 | 范围 / 默认 |
| --- | --- |
| `pitch_semitones` | `[-12, 12]` / `0` |
| `pitch_range` | `[0.5, 2.0]` / `1.0` |
| `energy_db` | `[-6, 6]` / `0` |
| `rate` | `[0.5, 2.0]` / `1.0` |
| `duration_ratio` | `[0.7, 1.5]` |
| `duration_ms` | `[100, 600000]` |
| `emotion_strength` / `formality` / `intonation_strength` | `[0, 1]` |
| `emphasis.weight` | `[-1, 1]` |
| `sample_rate` | `{16000,24000,32000,44100,48000}` / `24000` |
| `loudness_lufs` | `[-70, 0]` / `-16` |
| `peak_limit_dbtp` | `[-12, 0]` / `-1.0` |
| `chunk_ms` | `[20, 2000]` / `200` |
| `seed` | `[0, 2147483647]` |

> 阈值类数字（Q1–Q10 门禁）在 [`configs/eval/thresholds.yaml`](../../configs/eval/thresholds.yaml)，**不在此文件、不硬编码进代码**。

## 7. 版本演进规则

- 新增**可选**字段 → `spec_version` minor +1（如 `0.3.1`），旧 preset 不受影响。
- 新增**必填**字段 / 改枚举 / 收紧范围 → major +1（如 `1.0.0`），须同步 ADR + 全量 golden_set 回归。
- 删除字段 → major +1，且保留一个 minor 版本的兼容期。
- 每次 schema 变更必须：更新本错误码表 §5、补一个 `examples/` 用例、在 `CHANGELOG.md` 记录（由 conventional-changelog 从提交生成）。
