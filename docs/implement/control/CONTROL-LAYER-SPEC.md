# C 层控制实现规格 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | docs/AI智能体声音训练项目_技术栈方案_v0.4.md |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 定义 L5 C 层（Control）纯函数接口、校验流水线、18 个 C 层错误码的判定逻辑与单测组织，供 Phase 3 直接编码 |

## 0. 边界与不变量

| # | 不变量 | 说明 |
| --- | --- | --- |
| 1 | **Phase 0** | 全项目无任何训练产出、无模型权重、无实测指标。本文件所有指标均为「目标值 / 待校准」，不含「已达 / 实测 / 已上线」表述。 |
| 2 | **不改契约** | v0.4 **不修改** [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json)、不升 `spec_version`（`const "0.3.0"` 保持不变）、无 `BREAKING CHANGE`。C 层是契约的**实现**，不是契约的修订。 |
| 3 | **错误码冻结** | 只使用 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) 已登记的码；**稳定、只追加、不得改义/复用、不得自造**。本文件不新增任何错误码。 |
| 4 | **需求编号冻结** | 仅引用 F1–F8 / Q1–Q10（v0.1 定义），不新增、不改义。 |
| 5 | **编号归属** | 既有 D1–D15 / R-01–R-18 / ADR-0001–0003 沿用；v0.4 新增决策与风险编号由 Lead 统一分配，本文件只引用已分配项（R-20 / R-21 / D18），其余一律写「建议新增决策（待 Lead 编号）」。 |
| 6 | **阈值单一真源** | 一切 Q1–Q10 数值写「见 [`thresholds.yaml`](../../../configs/eval/thresholds.yaml)」，该文件 `calibration.status=uncalibrated`，数字不得写成结论、不得硬编码进代码。 |
| 7 | **许可口径** | 对外称「开放权重 / 源码可得(source-available, open-weight)」，**不称 OSI 开源**；项目自有增量用 PolyForm Noncommercial 1.0.0（禁商用）+ 双授权；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游；ADR-0001 决定不用 Spark-TTS 权重（`cc-by-nc-sa-4.0` SA 传染）。 |
| 8 | **基座未定** | 轨道 A 候选 CosyVoice 2 / Qwen3-TTS / VoxCPM2（均 Apache-2.0），Phase 2 同台实测定型；本文件不写「已选定」。capability flags 按「候选能力集合」定义，不绑定具体模型。 |
| 9 | **控制手段优先级** | ADR-0003 正式确立：`M4 > M2(连续声学特征编辑) > M1(离散标签) > M5 > M3 > M6(DSP 仅降级)`；`pitch` / `rate` 主控制禁用 M6。 |
| 10 | **许可文件保护** | 不修改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md`；不写任何真实密钥 / token / 凭据。 |

> 本版**只定规格**。C 层实现代码、preset 注册中心运行时、API 服务均在 Phase 3 落地；本文件给出可直接翻译为代码的签名、判定表与测试组织。

## 1. 模块定位

| 项 | 内容 |
| --- | --- |
| 逻辑层 | L5 控制层（VoiceSpec 消费者），位于 S 层校验之后、合成引擎之前 |
| 上游输入 | 已通过 S 层（JSON Schema 2020-12）校验的 `spec` dict；由 [`validate_voicespec.py`](../../../scripts/validate_voicespec.py) 同款校验器前置保证 |
| 下游输出 | `ValidationResult`：可合成的有效 spec（含 preset 展开结果）、或阻断错误 / 告警 / 审计补丁 |
| 依赖 | [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json)、[`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md)、[`ADR-0003.md`](../../decisions/ADR-0003.md)、[`voicespec/README.md`](../../voicespec/README.md) §4、[`thresholds.yaml`](../../../configs/eval/thresholds.yaml) |
| 关联规格 | [`API-SPEC.md`](API-SPEC.md)（端点接入）、[`PRESET-REGISTRY-SPEC.md`](PRESET-REGISTRY-SPEC.md)（preset 解析与展开） |

C 层负责 S 层**表达不了**的部分：跨字段算术 / 比较、preset 合并后的语义、能力探测、降级决策、许可鉴权、审计填充。原则见 ADR-0003 §2：能用 Schema 静态表达的绝不放进 C 层手写 `if`。

## 2. 数据结构（dataclass）

以下为 Python 3.12 风格定义，字段名即协议字段名，Phase 3 实现不得改名。

```python
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
    attribute_scan_passed: frozenset[str] = frozenset()  # 已过 §5.6 单调性扫描的属性名
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
    doc: str = ""                    # 指向 ERROR-CODES.md 对应锚点

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
    def to_envelope(self) -> dict:
        """序列化为 ERROR-CODES.md §2 的响应信封 valid/errors[]/warnings[]。"""
        ...
```

| 约束 | 说明 |
| --- | --- |
| `ValidationResult.valid` | `errors == []` 时为真；`warnings` 不阻断 |
| `resolved_spec` | 只包含 schema 允许的字段；C 层**不得**注入新字段（禁止静默扩字段，呼应 `additionalProperties:false`） |
| `audit_patch` | 只在 `valid=True` 时要求非空；失败时可为 `None` |
| 不变性 | 全部 `frozen=True`，`validate_control` 不得原地修改入参 `spec` |

## 3. 纯函数签名与契约

```python
def validate_control(spec: dict, ctx: ControlContext) -> ValidationResult:
    ...
```

| 项 | 契约 |
| --- | --- |
| 前置条件 | `spec` 已通过 S 层校验（结构 / 类型 / 范围 / 枚举 / 静态依赖 / `additionalProperties:false` 全部合法）；`spec` 中 `spec_version == "0.3.0"` |
| 纯函数 | 无 I/O、无时钟读取、无随机数、不改 `spec`、不改 `ctx`；相同入参恒返回相同结果（支撑 Q9 可复现） |
| 副作用 | 无。审计落库、日志、水印注入由服务端在 `validate_control` 返回后执行 |
| 失败语义 | 任一 `errors` 非空即 `valid=False`；不抛业务异常。未预期异常由外层包装为 `E-INTERNAL-001`（`layer="control"`，带 `request_id`，不暴露堆栈） |
| 错误码来源 | 全部取自 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) §4；`doc` 字段指向该文档对应锚点 |
| HTTP 映射 | 由 [`API-SPEC.md`](API-SPEC.md) 负责；`validate_control` 自身不感知 HTTP |

> `E-INTERNAL-001` 不是由 `validate_control` 内部判定函数返回的码，而是**外层异常边界**统一包装的结果；单测仍需覆盖（见 §9）。

## 4. 校验流水线（编号步骤）

与 [`voicespec/README.md`](../../voicespec/README.md) §4 / ADR-0003 §2 完全一致，此处给出每步的输入、输出与失败码。

| 步 | 名称 | 输入 | 处理 | 输出 | 失败 / 告警码 |
| --- | --- | --- | --- | --- | --- |
| 1 | **S 层 Schema 校验** | 原始请求体 JSON | `Draft202012Validator` 全量校验（结构 / 类型 / 范围 / 枚举 / `additionalProperties:false` / `allOf.if/then` / `not`） | 合法 `spec` dict | `E-SCHEMA-001..006`、`E-DEPENDENCY-001..003`、`E-RANGE-001`（静态部分）、`E-FORMAT-001..002` |
| 2 | **preset 合并** | `spec`、`ctx.preset` | 解析 `preset` / `preset_version` → 取 `production` 或锁定版本 → 展开 `scenario` 默认值 → **spec 显式字段覆盖**默认值；按 W-CONFLICT-007 记告警 | 合并后的 `spec` | `E-PRESET-001`、`E-PRESET-002`、`W-CONFLICT-007` |
| 3 | **C 层语义校验** | 合并后 `spec` | 18 个判定函数按 §5 顺序执行；跨字段算术 / 比较、鉴权、审计只读检查 | `errors` / `warnings` 列表 | 见 §5 全表 |
| 4 | **能力探测** | 合并后 `spec`、`ctx.capabilities` | 逐 flag 比对请求字段（§6）；`exact_duration` 缺失直接报错，其余按降级链 | 可能改写 `resolved_spec`（仅降级路径） | `E-CAPABILITY-001`、`E-CAPABILITY-004`、`W-CAPABILITY-002/003` |
| 5 | **降级决策** | 步骤 4 结果 | 汇总所有降级，统一置 `audit.degraded=true` 并写审计；M6 DSP 兜底触发 `W-RENDER-001` | 最终 `resolved_spec` + `warnings` | `W-RENDER-001` |
| 6 | **审计填充** | 步骤 5 结果、`ctx` | 构造 `AuditPatch`；若客户端曾传 `audit.*` 则步骤 3 已报 `E-AUDIT-001` | `ValidationResult` | `E-AUDIT-001` |
| 7 | **合成 → 门禁 → 审计日志** | `resolved_spec` | 服务端行为，在 `validate_control` **之外**；门禁阈值见 `thresholds.yaml` | 音频 / 门禁报告 | 不属于 C 层 |

**顺序不可交换的两点**：① S 层必须早于 C 层，否则跨字段算术会作用在类型未校验的数据上；② preset 合并必须早于 C 层，否则显式字段覆盖默认值的语义（W-CONFLICT-007）无法正确判定冲突对。

## 5. C 层 18 个错误码 → 判定函数逐一映射

判定函数均为**纯函数**，签名统一 `fn(spec: dict, ctx: ControlContext) -> ValidationIssue | None`（告警类返回 `severity="warning"`）。`layer` 固定 `"control"`；`path` 用 JSON Pointer 风格；`hint` 给出可执行的客户端修复动作。`doc` 统一指向 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) 对应锚点。

| # | 判定函数 | 错误码 | 触发条件 | 判定逻辑（写清跨字段算术 / 比较） | 返回 layer / path / hint | 单测用例要点 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `check_rate_duration_conflict` | `E-CONFLICT-001` | `rate` 与任一 duration 控制同时显式给出 | `has(rate) and (has(duration_ms) or has(duration_ratio) or has(duration_range_ms) or duration_mode in {"exact","range"})`。Schema `ProsodySpec.not` 已静态拦截一部分；C 层兜底 `duration_mode="free" + duration_ms` 组合（`not` 未覆盖） | `control` / `prosody` / 「二选一：删除 `rate`，或改用 `duration_mode=free` + `rate`」 | ① `rate=0.9` + `duration_mode=exact` + `duration_ms=3000`（schema 已拦，C 层亦须拦）；② `rate=0.9` + `duration_mode=free` + `duration_ms=3000`（**仅 C 层能拦**，重点用例）；③ 仅 `rate` → 通过 |
| 2 | `check_pause_budget` | `E-CONFLICT-002` | `duration_ms` 与 `pauses[]` 共存且停顿超预算 | 允许共存；`sum(p.ms for p in prosody.pauses) > prosody.duration_ms * 0.4` 为真即报错。边界取严格大于（`==` 通过） | `control` / `prosody.pauses` / 「缩短停顿或增大 `duration_ms`，使 Σpauses.ms ≤ duration_ms × 0.4」 | ① Σ=0.41×d → 报错；② Σ=0.40×d → 通过（边界）；③ 无 `duration_ms` 时不触发；④ 多段 pauses 求和 |
| 3 | `check_energy_loudness_nonconflict` | `E-CONFLICT-003` | `energy_db` ↔ `loudness_lufs` | **已判定不冲突，正常不返回**：前者表现力、后者交付响度，同时生效、loudness 最后做。仅当用户显式声明互斥意图时才报错；实现须**禁止**误加互斥校验 | `control` / `render` / 「两者可同时给出，`loudness_lufs` 在渲染末段生效」 | ① 同时给出 → `valid=True` 且无此码（防误加互斥）；② 登记为「不返回」的守护用例 |
| 4 | `check_voice_blend_lock` | `E-CONFLICT-004` | `voice_blend` 与 `speaker_lock=true` 共存 | `has(identity.voice_blend) and identity.speaker_lock is not False`（`speaker_lock` 默认 `true`，缺省亦视为锁定） | `control` / `identity` / 「改用单一 `speaker_id`，或显式设 `speaker_lock=false` 且基座支持 `voice_blend`」 | ① `voice_blend` + 缺省 `speaker_lock` → 报错（覆盖默认值陷阱）；② `voice_blend` + `speaker_lock=false` → 通过；③ 无 `voice_blend` → 通过 |
| 5 | `check_pitch_offset_nonconflict` | `E-CONFLICT-005` | `pitch_semitones` ↔ `pitch_contour`(曲线) | **已判定不冲突，正常不返回**：contour 为相对形状、semitones 为全局偏移，叠加生效 | `control` / `prosody` / 「两者可同时给出，全局偏移叠加在相对形状之上」 | ① 曲线 + `pitch_semitones=3` → `valid=True`（防误加互斥）；② 守护用例 |
| 6 | `warn_emotion_prompt_priority` | `W-CONFLICT-006` | `emotion` 与 `style_prompt` 同时给出 | 离散 `emotion` 优先；`style_prompt` 仅作修饰，**不阻断**，写审计日志。返回 `severity="warning"` | `control` / `style` / 「`emotion` 已优先生效，`style_prompt` 仅作修饰并记入审计」 | ① 同时给出 → `valid=True` + 1 条 warning；② 仅 `style_prompt` → 与 #12 联动校验 |
| 7 | `warn_scenario_override` | `W-CONFLICT-007` | `scenario` 展开默认值与显式 L-B/L-C 字段相遇 | 步骤 2 合并时判定：**显式值覆盖** scenario / preset 展开的默认值（preset 是默认值集合，不是强制值）；不阻断，记告警 | `control` / `style` / 「显式字段已覆盖场景默认值」 | ① `scenario="播报"` + 显式 `rate=1.4` → 合并后 `rate=1.4` 且有告警；② 仅 `scenario` → 展开生效、无告警 |
| 8 | `probe_exact_duration` | `E-CAPABILITY-001` | `duration_mode=exact` 但 `ctx.capabilities.exact_duration=False` | **报错 400，不静默降级**（F4 升 P0 候选后属硬能力）。判定只看 flag，不做近似 | `control` / `prosody.duration_mode` / 「当前基座不支持显式时长头；改用 `duration_mode=free`，或等待 Phase 2 选定支持该能力的基座」 | ① flag=False + `exact` → 报错且 `resolved_spec` 未被静默改写；② flag=True + `exact` → 通过；③ 强调**不得**降级为 `free` |
| 9 | `probe_f0_contour` | `W-CAPABILITY-002` | `pitch_contour` 为曲线数组但 `ctx.capabilities.f0_contour=False` | 降级：`pitch_contour` → `"native"`，用 `pitch_range` 近似；`audit.degraded=true`；记 warning | `control` / `prosody.pitch_contour` / 「已降级为 `native` + `pitch_range` 近似，详见审计 `degraded`」 | ① 曲线 + flag=False → warning + `degraded=True` + `resolved_spec.pitch_contour="native"`；② 曲线 + flag=True → 无降级；③ 枚举档位 `"flat"` 时不触发（非曲线） |
| 10 | `probe_attribute_control` | `W-CAPABILITY-003` | `style.attributes` 中某属性不在 `ctx.attribute_scan_passed`，或 `attribute_control=False` | 逐属性检查：未过 §5.6 单参数 5 点单调性扫描（ρ 目标值见 `thresholds.yaml`）→ **拒绝该属性**（从 `resolved_spec` 移除）并告警，**不得进 production preset** | `control` / `style.attributes` / 「该属性未通过单调性扫描，已忽略；过扫描后方可进 production preset」 | ① 单属性未过 → warning + 该属性被移除；② 部分过 / 部分未过 → 只移除未过的；③ 全部过 + flag=True → 通过；④ 断言 production preset 不含被拒属性 |
| 11 | `check_style_prompt_sole_control` | `E-CAPABILITY-004` | `style_prompt` 作为 preset / spec 的**唯一**控制手段 | 判定「除 `text`、`identity.speaker_id`、`style.style_prompt` 外，L-B/L-C/L-D/L-E 无任何显式控制字段，且 preset 展开也未注入任何 L-B/L-C 默认值」→ 报错（PromptTTS 2 `arXiv:2309.02285` 描述不可严格复现） | `control` / `style.style_prompt` / 「补充至少一个确定性控制字段（如 `emotion` / `rate`）或引用带默认值的 preset」 | ① 仅 `style_prompt` → 报错；② `style_prompt` + `emotion` → 通过（与 #6 联动）；③ 引用 preset 展开出 L-B 默认值 → 通过 |
| 12 | `warn_dsp_fallback` | `W-RENDER-001` | 任何 `pitch` / `rate` 主控制落到 M6 DSP | 仅在降级链末端判定；必须 `degraded=True` + 告警。ADR-0003：`pitch`/`rate` 主控制禁用 M6，M6 仅限渲染层 / 降级路径 | `control` / `render` / 「已走 M6 DSP 降级路径，音质可能受损，详见审计」 | ① 触发降级 → warning + `degraded=True`；② 正常路径（M2 特征编辑）→ 无此告警 |
| 13 | `resolve_preset` | `E-PRESET-001` | `preset` 引用不存在的 ID / 版本 | 查注册中心（[`PRESET-REGISTRY-SPEC.md`](PRESET-REGISTRY-SPEC.md)）：ID 不存在或该 ID 下无请求版本 → 报错 | `control` / `preset` / 「改用已注册 preset_id，或省略 preset 走默认」 | ① 不存在的 ID → 报错；② 存在 ID 但版本不存在 → 报错；③ 无 preset → 不触发 |
| 14 | `validate_preset_version` | `E-PRESET-002` | `preset_version` 非法（不符 semver 正则）或与注册版本不符 | 先按 schema `pattern` 校验格式（S 层已保证），再比对注册中心该版本是否存在 / 状态是否允许引用 | `control` / `preset_version` / 「使用注册中心已登记的语义化版本」 | ① 合法格式但注册中心无此版本 → 报错；② 省略 `preset_version` → 取 `production` + 写 `audit.preset_resolved`；③ 锁定版本与 `production` 不同 → 以锁定版本为准 |
| 15 | `reject_client_audit` | `E-AUDIT-001` | 客户端请求体传入 `audit.*` 只读字段 | `has(spec, "audit")` → 报错。**注意**：`AuditSpec` 在 schema 中合法（否则无法通过 S 层），因此必须由 C 层显式拒绝 | `control` / `audit` / 「删除 `audit` 字段，该字段由服务端填充」 | ① 传 `audit: {}` → 报错；② 传 `audit.request_id` → 报错；③ 不传 → 通过且 `audit_patch` 非空 |
| 16 | `check_watermark_license` | `E-LICENSE-001` | `render.watermark=false` 且 `ctx.license.commercial_authorized=False` | 水印默认 `true`；关闭需商业授权凭证（双授权）。判定 `watermark is False and not commercial_authorized` | `control` / `render.watermark` / 「保持水印开启，或凭商业授权凭证关闭」 | ① `false` + 无授权 → 报错；② `false` + 有授权 → 通过且写审计；③ 缺省（默认 `true`）→ 通过；④ `true` + 无授权 → 通过 |
| 17 | `check_speaker_license` | `E-LICENSE-002` | `ref_audio_uri` 指向未注册 / 未授权说话人音频 | 由 URI 解析出的 speaker 须 ∈ `ctx.speaker_registry` 且 `ctx.license.speaker_registered=True`；未注册即拒绝（音色注册鉴权） | `control` / `identity.ref_audio_uri` / 「使用已注册且已授权的说话人参考音频」 | ① 未注册 URI → 报错；② 已注册但 `speaker_registered=False` → 报错；③ 已注册 + 已授权 → 通过；④ 无 `ref_audio_uri` → 不触发 |
| 18 | `wrap_internal_error`（外层边界） | `E-INTERNAL-001` | `validate_control` 抛出任何未预期异常 | 不在纯函数内部判定；由 API 层统一捕获，构造 `ValidationIssue(code="E-INTERNAL-001", layer="control", severity="error", path="<root>")`，携带 `request_id`，**不暴露堆栈**；HTTP 500 | `control` / `<root>` / 「携带 request_id 联系维护者」 | ① 注入异常 → 返回该码且无堆栈文本；② 断言 `request_id` 存在 |

**表内自洽性**：`E-CONFLICT-003` / `E-CONFLICT-005` 标「已判定不冲突，正常不返回」，ADR-0003 §3 登记目的就是防止实现误加互斥校验；单测须以守护用例覆盖「不返回」。

> 缺口登记（不自造新码）：`voice_blend` 能力缺失时的专用报错码在现有错误码表中**不存在**（`E-CONFLICT-004` 只管 `speaker_lock`）。本规格登记该缺口为「建议新增错误码 / 建议新增决策（待 Lead 编号）」，Phase 3 实现前须由 Lead 补齐；在此之前 `voice_blend` flag 为 `False` 时不得静默接受该字段。

## 6. Capability flags 表

`ctx.capabilities` 由 `GET /v1/capabilities` 暴露（见 [`API-SPEC.md`](API-SPEC.md)）。Phase 2 基座定型后回填实测值；Phase 0 全为声明值，**未实测**。

| flag | 请求字段 | 需要该 flag 的条件 | 不支持时的码与行为 |
| --- | --- | --- | --- |
| `exact_duration` | `prosody.duration_mode="exact"`、`duration_ms` | 任何精确时长请求 | **`E-CAPABILITY-001`，直接报错 400，不静默降级**（F4 升 P0 候选后属硬能力）。强调：不得降级为 `free` |
| `f0_contour` | `prosody.pitch_contour` 为 `F0Point[]` 曲线 | 仅曲线形式需要；枚举档位 `native/flat/expressive` 不需要 | `W-CAPABILITY-002`：降级 `native` + `pitch_range` 近似，`audit.degraded=true`，告警 |
| `attribute_control` | `style.attributes.*` | 任一属性出现 | `W-CAPABILITY-003`：逐属性核对 `attribute_scan_passed`，未过扫描者拒绝且不进 production preset；`degraded=true` |
| `style_prompt` | `style.style_prompt` | 任何自然语言风格指令 | `E-CAPABILITY-004`（作为唯一控制手段时报错）；`W-CONFLICT-006`（与 `emotion` 共存时降级为修饰）。flag=False 时 `style_prompt` 仅可修饰、不得单独生效 |
| `voice_blend` | `identity.voice_blend` | 多音色插值 | 与 `speaker_lock=true` 共存 → `E-CONFLICT-004`；flag=False 且 `speaker_lock=false` 时**现有错误码表无专用码**，见 §5 缺口登记：不得静默接受，须由 Lead 补码后再实现 |

**优先级**：能力探测失败时，`E-CAPABILITY-001`（硬能力）优先于一切降级告警；`exact_duration` 缺失直接终止后续降级，不进入 `resolved_spec` 改写。

## 7. 降级链

```
请求字段
  ├─ f0_contour=False + pitch_contour 曲线
  │    → W-CAPABILITY-002：pitch_contour="native" + pitch_range 近似
  ├─ attribute_control=False 或属性未过 §5.6 扫描
  │    → W-CAPABILITY-003：移除该属性，禁止进 production preset
  └─ pitch/rate 主控制无 M2/M1 可用，落 M6 DSP
       → W-RENDER-001：仅渲染层降级，必须 degraded=true
                 ↓ 汇总
        audit.degraded = true  （任一降级触发即置位）
                 ↓
        写审计日志（含触发码、原值、降级后值）
```

| 规则 | 内容 |
| --- | --- |
| 统一置位 | 任一 `W-CAPABILITY-002` / `W-CAPABILITY-003` / `W-RENDER-001` 触发，`AuditPatch.degraded=True` |
| 禁止静默 | 降级必须同时产生 warning；只允许改写 schema 已存在的字段值，**不得新增字段** |
| M6 红线 | `pitch` / `rate` 主控制禁用 M6（金属音、损相似度）；M6 仅作降级兜底 |
| 不降级例外 | `E-CAPABILITY-001` 明确**不静默降级**，属硬能力报错 |
| 阈值 | 降级后是否仍满足 Q1–Q10 由门禁判定，阈值见 `thresholds.yaml`；本规格不写数字结论 |
| 关联风险 | R-08（流式 chunk 边界韵律连续性）在流式路径另见 [`API-SPEC.md`](API-SPEC.md) §8；R-20（错误码 ↔ 实现漂移）由 §9 自动核对缓解 |

## 8. 审计填充

| `AuditSpec` 字段 | 填充来源 | 说明 |
| --- | --- | --- |
| `request_id` | `ctx.request_id` | 全链路透传，见 [`API-SPEC.md`](API-SPEC.md) §7 |
| `license` | 常量 `PolyForm-Noncommercial-1.0.0` | 项目自有增量许可标识；上游 Apache-2.0 权重不受 NC 覆盖 |
| `preset_resolved` | `ctx.preset.resolved_version` | 省略 `preset_version` 时记录实际解析到的 `production` 版本 |
| `model_commit` | `ctx.model_commit` | Phase 2 基座定型后回填；Phase 0 为 `None` |
| `gate_report` | `ctx.preset.gate_report` / 门禁报告 ID | 过门禁后回填；Phase 0 为 `None` |
| `golden_set_passed` | 门禁运行器 | 格式 `gs-YYYY-MM-a`；Phase 0 无门禁，为 `None` |
| `watermark_id` | `ctx.watermark_id` | 水印启用时填充；默认 `render.watermark=true` |
| `degraded` | §7 汇总 | 任一降级即 `true` |

`audit.*` 为**服务端只读**字段：客户端传入 → `E-AUDIT-001`（§5 #15）。Q9 可复现依赖 `preset@version + model@commit + seed + text + deps_lock`，其中 `seed` 在 `RenderSpec`，`deps_lock` 由依赖锁文件保证，均在 `validate_control` 之外。

## 9. 单测组织

**Phase 3 才写实现代码**；本版只定测试组织与验收口径。

| 项 | 内容 |
| --- | --- |
| 测试文件 | `tests/unit/control/test_error_codes.py` |
| 覆盖要求 | §5 表中 **18 个码各 ≥1 用例**；`E-CONFLICT-003` / `E-CONFLICT-005` / `E-INTERNAL-001` 用守护用例（断言「不返回」或「异常包装」） |
| 每码断言 | `code` 精确匹配、`layer=="control"`、`path` 符合 §5、`hint` 非空、`severity` 与 error/warning 分类一致、`valid` 与预期一致 |
| 边界用例 | 算术边界（`Σpauses == duration_ms × 0.4` 通过）、默认值陷阱（`speaker_lock` 缺省视为 `true`）、`duration_mode=free + duration_ms`（仅 C 层能拦）、`audit` 空对象 |
| 纯函数性质 | 相同 `(spec, ctx)` 调用两次结果恒等；断言入参 `spec` / `ctx` 未被原地修改 |

**「错误码表 ↔ 实现」自动核对（防 R-20 漂移）**：

```python
# tests/unit/control/test_error_codes.py 中的守护测试（伪代码）
DOC_CODES = parse_md_table("docs/voicespec/ERROR-CODES.md", section="§4")
IMPL_CODES = {
    i.code for i in collect_all_issues_from_all_test_cases()
} | IMPLEMENTED_CODES  # 由 C 层模块导出 frozenset

def test_no_drift_between_error_code_table_and_impl():
    assert IMPL_CODES == DOC_CODES, (
        "错误码表与实现不一致："
        f"表有实现无={sorted(DOC_CODES - IMPL_CODES)}，"
        f"实现有表无={sorted(IMPL_CODES - DOC_CODES)}"
    )
```

| 核对项 | 失败含义 |
| --- | --- |
| 表有实现无 | 某个已登记码 Phase 3 未实现 → 阻断 |
| 实现有表无 | 自造 / 改义了错误码 → 阻断（违反 §0 不变量 3） |
| 码的 `severity` 分类 | `W-` 前缀必须是 warning、`E-` 前缀必须是 error → 阻断 |

CI 接入：见 [`eval-gate.yml`](../../../.github/workflows/eval-gate.yml)（Phase 3 起把 `tests/unit/control/` 纳入）；当前该工作流已真实校验 [`examples/`](../../../configs/voicespec/examples/) 下的契约用例，不跑 C 层单测。

## 10. Phase 3 边界与开放项

| 项 | 状态 |
| --- | --- |
| `validate_control` 实现代码 | ⏳ Phase 3，本版只有签名与判定表 |
| preset 注册中心运行时 | ⏳ Phase 3，见 [`PRESET-REGISTRY-SPEC.md`](PRESET-REGISTRY-SPEC.md) |
| 两个 API 接入 S+C | ⏳ Phase 3，见 [`API-SPEC.md`](API-SPEC.md) |
| capability flags 实测值 | ⏳ Phase 2 基座同台实测定型后回填；Phase 0 为声明值 |
| `AttributeSpec` 逐属性单调性扫描 | ⏳ 见 `thresholds.yaml`（`calibration.status=uncalibrated`），未过扫描不得进 production preset |
| `voice_blend` flag 缺失专用错误码 | 缺口登记，建议新增决策（待 Lead 编号），实现前须补齐 |
| 许可条款法务定稿（D11） | 仍为发布权重前阻塞项；本规格不触碰权重发布 |
| R-14b 法务跟进 | 仍开放；本规格不新增第三方依赖 |

**追溯**：F1 / F3 / F4 / F5 / F8（参数化细调、精确时长、preset 复现、版本化审计）、Q9（可复现）、Q10（参数正交）、ADR-0003 验收条件、R-17（契约与实现漂移）、R-18（代码许可 ≠ 权重许可）、R-20（错误码漂移，由 §9 缓解）。
