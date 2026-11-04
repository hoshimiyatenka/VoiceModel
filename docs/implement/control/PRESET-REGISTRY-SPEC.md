# Preset 注册中心规格 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | docs/AI智能体声音训练项目_技术栈方案_v0.4.md |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 定义 `configs/presets/registry.yaml` 结构、语义化版本解析、默认值展开算法、与 C 层错误码联动、变更流程与 Phase 0 冻结状态 |

## 0. 边界声明

| # | 声明 |
| --- | --- |
| 1 | **Phase 0**：全项目无训练产出、无模型权重、无实测指标。本文件所有阈值均为「目标值 / 待校准」，严禁「已达 / 实测 / 已上线」。 |
| 2 | **不改契约**：v0.4 不修改 [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json)、不升 `spec_version`（`const "0.3.0"`）、无 `BREAKING CHANGE`。preset 是**默认值集合**，其字段必须全部是 schema 允许的字段。 |
| 3 | **错误码冻结**：只使用 [`ERROR-CODES.md`](../../voicespec/ERROR-CODES.md) 已登记码（`W-CONFLICT-006/007`、`E-CAPABILITY-004`、`E-PRESET-001/002` 等），稳定、只追加、不改义/复用、不自造。 |
| 4 | **许可口径**：对外称「开放权重 / 源码可得(source-available, open-weight)」，**不称 OSI 开源**；项目自有增量 PolyForm Noncommercial 1.0.0（禁商用）+ 双授权；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游；ADR-0001 不用 Spark-TTS 权重（`cc-by-nc-sa-4.0` SA 传染）。 |
| 5 | **基座未定**：轨道 A 候选 CosyVoice 2 / Qwen3-TTS / VoxCPM2（均 Apache-2.0），Phase 2 同台实测定型；不写「已选定」。 |
| 6 | **控制手段优先级**：ADR-0003 `M4 > M2(连续) > M1(离散) > M5 > M3 > M6(DSP 仅降级)`；preset 默认值优先落在 M4/M2/M1 可覆盖的确定性字段，不依赖 `style_prompt`。 |
| 7 | **阈值单一真源**：单调性扫描 ρ、Q1–Q10 一律「见 [`thresholds.yaml`](../../../configs/eval/thresholds.yaml)」（`calibration.status=uncalibrated`），数字不写成结论。 |
| 8 | **许可文件保护**：不修改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md`；不写任何真实密钥 / token / 凭据。 |
| 9 | **编号归属**：沿用 F1–F8 / Q1–Q10、D1–D15、R-01–R-18、ADR-0001–0003；本文件只引用已分配项 **D18 / R-21**，其余写「建议新增决策（待 Lead 编号）」。 |

> 交叉引用：[`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md)（步骤 2 preset 合并、§5 #13/#14 判定）、[`API-SPEC.md`](API-SPEC.md)（`GET /v1/presets/{id}`）、[`voicespec/README.md`](../../voicespec/README.md) §3-2（preset 是默认值集合）、[`ADR-0003.md`](../../decisions/ADR-0003.md)（确定性优先）、[`COMMIT_CONVENTION.md`](../../../COMMIT_CONVENTION.md) §5（footer）。

## 1. 定位与不变量

| 项 | 内容 |
| --- | --- |
| 单一真源 | `configs/presets/registry.yaml`（Phase 0 仅为骨架 + 一个 `template` 示例） |
| 职责 | 登记 `preset_id`、各版本文件路径、门禁报告、审批人、状态、`production` 指针；为 C 层提供 `ExpandedPreset`（见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §2） |
| 不做的事 | 不存音频、不存权重、不存凭据、不执行合成、不替代 `thresholds.yaml` |
| 核心语义 | **preset 是默认值集合，不是强制值**：spec 显式字段覆盖 preset 展开值（W-CONFLICT-007） |

preset 文件本身（每个 `versions[].path` 指向的 YAML/JSON）只含 VoiceSpec 允许的**默认字段值**；禁止出现 schema 未登记字段（呼应 `additionalProperties:false`）。

## 2. registry.yaml 结构

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `preset_id` | string | 是 | 与 VoiceSpec `preset` 字段同规则：`^[a-z0-9][a-z0-9_-]*$`，最长 64 |
| `versions[]` | list | 是 | 版本条目列表，见下表 |
| `versions[].version` | string | 是 | 语义化版本 `MAJOR.MINOR.PATCH`（可带 `-pre`/`+build`），与 VoiceSpec `preset_version` 的 `pattern` 一致 |
| `versions[].path` | string | 是 | 相对 `configs/presets/` 的默认值文件路径（YAML/JSON），内容为 VoiceSpec 字段子集 |
| `versions[].gate_report` | string \| null | 是 | 门禁报告 ID（格式 `gs-YYYY-MM-a`）；`template` / `staging` 可为 `null`，`production` **必须非 null** |
| `versions[].created_by` | string | 是 | 创建者标识（非凭据） |
| `versions[].approved_by` | string \| null | 是 | 审批人；`production` 必须非空；`template` 可为 `null` |
| `versions[].status` | enum | 是 | `template` \| `staging` \| `production`，见 §3 |
| `production` | string \| null | 是 | 指向某个 `status=production` 的 `version`；Phase 0 必须为 `null` |
| `schema_ref` | string | 是 | 指向 [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json)，声明本 preset 遵循的契约版本 |

**状态枚举**：

| status | 含义 | 可作 `production` 指针 | 允许 `/v1/synthesize` 引用 |
| --- | --- | --- | --- |
| `template` | 模板 / 示例，未过门禁 | 否 | 否（仅用于演示与 `GET /v1/presets/{id}`） |
| `staging` | 已提交待门禁 / 灰度 | 否 | 受限（仅内部，Phase 0 无此状态） |
| `production` | 已过 golden_set 门禁 + 审批 | 是 | 是 |

> **Phase 0 硬约束**：本轮只落 `registry.yaml` 骨架与一个 `template` 示例，`production` 必须为 `null`，**不得标 `production`、不得进 business preset**（R-21 / D18）。任何「已上线 / 已可用」表述都违反 §0-1。

骨架示例（示意，非已落地运行时数据）：

```yaml
preset_id: warm_companion
production: null            # Phase 0：无 production 指针
schema_ref: ../../configs/voicespec/voicespec.schema.json
versions:
  - version: 0.1.0-template
    path: warm_companion@0.1.0-template.yaml
    gate_report: null
    created_by: lead
    approved_by: null
    status: template
```

## 3. 语义化版本与 preset_version 解析

| 规则 | 内容 |
| --- | --- |
| 版本格式 | `MAJOR.MINOR.PATCH`，可带 `-pre` / `+build`；与 [`voicespec.schema.json`](../../../configs/voicespec/voicespec.schema.json) 的 `preset_version.pattern` 一致（S 层先校验格式） |
| MAJOR | preset 默认值发生**不兼容**变更（删除字段 / 改枚举 / 收紧范围）→ +1；须同步 ADR + 全量 golden_set 回归 |
| MINOR | 新增**可选**默认字段 / 调默认值（兼容）→ +1 |
| PATCH | 元数据 / 审批人 / `gate_report` 修订，不改变任何默认字段值 → +1 |
| 状态前缀 | `template` 示例用 `-template` 后缀区分，不计入 semver 正式序列 |

**解析算法（C 层步骤 2，见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 #13/#14）**：

| 客户端传入 | 解析行为 | 失败码 |
| --- | --- | --- |
| `preset` 给出且 `preset_version` 给出 | 查 `registry.yaml`：ID 存在 → 该版本存在 → 状态允许引用（`production`/受控 `staging`） | ID/版本不存在 → `E-PRESET-001`；版本格式/注册不符 → `E-PRESET-002` |
| `preset` 给出、`preset_version` **省略** | 取 `production` 指针指向的版本；**写入 `audit.preset_resolved`**（`AuditPatch.preset_resolved`） | `production=null`（Phase 0 常态）→ `E-PRESET-001`（无可解析版本） |
| `preset` 未给出 | `ctx.preset = None`，不展开默认值，spec 字段即最终值 | 不触发 |
| 锁定版本 ≠ `production` | 以**锁定版本**为准（可复现优先），`audit.preset_resolved` 记锁定值 | — |

| 不变量 | 说明 |
| --- | --- |
| 省略版本必写审计 | 解析到的 `production` 版本必须落 `audit.preset_resolved`，支撑 Q9 可复现 |
| Phase 0 无 production | 因 `production=null`，任何省略版本的引用都失败；这不是 bug，是 R-21 的刻意约束 |
| 不改 schema | 解析过程不修改 `spec_version`，不注入新字段 |
| 错误码稳定 | 只用 `E-PRESET-001` / `E-PRESET-002`，不新增 |

## 4. 默认值展开算法

### 4.1 三条硬规则（与契约一致）

1. **preset 是默认值集合，不是强制值**：spec 显式字段覆盖 preset 展开值（[`voicespec/README.md`](../../voicespec/README.md) §3-2、W-CONFLICT-007）。
2. **确定性优先**：`scenario` 展开的 L-B/L-C 默认值优先落在 M4/M2/M1 可覆盖字段；`style_prompt` 不得作唯一控制手段（E-CAPABILITY-004）。
3. **不注入新字段**：展开结果只能包含 schema 已登记字段，禁止静默扩字段。

### 4.2 展开顺序

```
registry 解析出版本 → 读取 versions[].path 的默认字段集 D
   → 若 D 含 style.scenario：scenario → 一组 L-B/L-C 默认值 S
   → 合并 defaults = merge(D, S)（scenario 作为默认值来源之一）
   → 用 spec 显式字段逐层覆盖 defaults（identity/prosody/style/linguistic/render）
   → 合并后 spec = resolved_spec
   → 记录 W-CONFLICT-007（若有显式字段覆盖了 scenario/默认值）
   → 交给 C 层语义校验（CONTROL-LAYER-SPEC.md §4 步骤 3）
```

### 4.3 伪代码

```python
def expand_preset(spec: dict, preset: ExpandedPreset | None) -> tuple[dict, list[str]]:
    """返回 (合并后 spec, 被覆盖的路径列表)。纯函数，不修改入参。"""
    if preset is None:
        return deepcopy(spec), []
    D = load_preset_file(preset.path)              # VoiceSpec 字段子集
    # scenario → 一组 L-B/L-C 默认值（显式字段仍可覆盖）
    S = scenario_defaults(D.get("style", {}).get("scenario"))
    defaults = deep_merge(D, S)                    # 同层：D 显式优先于 S
    merged = deepcopy(defaults)
    overridden: list[str] = []
    for layer in ("identity", "prosody", "style", "linguistic", "render"):
        if layer in spec:
            for key, val in spec[layer].items():
                # 显式字段覆盖默认值（W-CONFLICT-007）
                if layer in merged and key in merged[layer]:
                    overridden.append(f"{layer}.{key}")
                merged.setdefault(layer, {})[key] = val
    # 顶层非分层字段（text / spec_version / preset / preset_version）以 spec 为准
    for key in ("text", "spec_version", "preset", "preset_version"):
        if key in spec:
            merged[key] = spec[key]
    return merged, overridden
```

| 要点 | 说明 |
| --- | --- |
| 覆盖方向 | **spec 显式 > preset/scenario 默认值**，绝不反向 |
| `scenario` 与显式参数 | 显式 L-B/L-C 覆盖 scenario 展开值 → `W-CONFLICT-007`（见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 #7） |
| `overridden` 列表 | 用于生成 `W-CONFLICT-007` 告警的 `path` / `detail` |
| 纯函数 | 与 `validate_control` 一致：不改入参、无 I/O 副作用（文件读取在注册中心层，展开函数接收已加载 dict） |
| 门禁 | 展开后的 `resolved_spec` 仍须过 S 层（字段合法性）+ C 层（语义）；preset 文件本身也须经 S 层等价校验 |

## 5. 与 C 层错误码联动

| 码 | 联动点 | 规则 |
| --- | --- | --- |
| `W-CONFLICT-006` | `emotion` ↔ `style_prompt` | 离散 `emotion` 优先；`style_prompt` 仅作修饰并写审计。若 preset 默认值里只有 `style_prompt` 而无确定性控制字段，展开后仍会触发 `E-CAPABILITY-004`，不能靠 preset「洗白」 |
| `E-CAPABILITY-004` | `style_prompt` 作为 preset / spec **唯一**控制手段 | 判定见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 #11：除 `text` / `identity.speaker_id` / `style.style_prompt` 外无任何 L-B/L-C/L-D/L-E 显式字段，且 preset 展开未注入任何 L-B/L-C 默认值 → 报错（PromptTTS 2 `arXiv:2309.02285` 描述不可严格复现） |
| `E-PRESET-001` | 引用不存在的 ID / 版本，或 `production=null` 时省略版本 | 见 §3 解析表；`GET /v1/presets/{id}` 的 `404` 是读接口语义，不返回校验信封 |
| `E-PRESET-002` | `preset_version` 非法或与注册版本不符 | S 层已校验格式，C 层比对注册中心 |
| `W-CONFLICT-007` | `scenario` / preset 默认值被显式字段覆盖 | 展开算法 `overridden` 列表驱动，见 §4 |

**确定性优先的推论**：preset 默认值必须至少包含一个可由 M4/M2/M1 覆盖的字段（如 `emotion`、`rate`、`pitch_semitones`），否则该 preset 在任何 spec 下都会因 `E-CAPABILITY-004` 失败。Phase 0 的 `template` 示例须遵守此约束，即便不得进 `production`。

## 6. Phase 0 状态声明（R-21 / D18）

| 项 | Phase 0 状态 |
| --- | --- |
| `registry.yaml` | 仅骨架 + 一个 `template` 示例 |
| `production` 指针 | **必须为 `null`** |
| golden_set 门禁 | **未过**（Q8 回归、参数扫描均未执行，阈值见 `thresholds.yaml` `uncalibrated`） |
| `status=production` | **禁止**；不得标 production |
| business preset | **不得进**；不得被 `/v1/synthesize` 作为可用 preset 引用 |
| `AttributeSpec` 属性 | 逐属性过 §5.6 单参数 5 点单调性扫描前不得进 production preset（`W-CAPABILITY-003`，见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 #10） |
| 能力 flags | Phase 0 声明值、未实测；Phase 2 基座同台实测定型后回填 |
| 指标 | 全部「目标值 / 待校准」；无实测分数 |

> D18（Phase 0 不得标 production / 不得进 business preset）与 R-21（未过门禁 preset 被误用风险）为本版已分配编号；其余新增约束一律写「建议新增决策（待 Lead 编号）」，不自行发明 D / R 号。

## 7. 变更流程

| 步骤 | 要求 |
| --- | --- |
| 1. 改动路径 | `configs/presets/**`（含 `registry.yaml` 与各 `versions[].path` 文件）走 **PR**，禁止直推 `main`（[`COMMIT_CONVENTION.md`](../../../COMMIT_CONVENTION.md) §6） |
| 2. 强制 footer | 提交必须带 `Gate-Report:` + `Preset:`（[`COMMIT_CONVENTION.md`](../../../COMMIT_CONVENTION.md) §5）：`Gate-Report: gs-YYYY-MM-a`、`Preset: warm_companion@1.3.0`。`Gate-Report` 触发条件含 `configs/presets/**`；`Preset` 触发条件含改 preset |
| 3. CODEOWNERS | `configs/presets/` 受保护路径，需 maintainer 批准（见 [`CODEOWNERS`](../../../CODEOWNERS)） |
| 4. CI 校验 | `license-check` / `commitlint` 的 footer 校验；`eval-gate` 校验 VoiceSpec 契约（[`eval-gate.yml`](../../../.github/workflows/eval-gate.yml)）。Phase 3 起把 preset 展开用例纳入 |
| 5. 转 `production` 前置 | 过 golden_set 门禁（Q8）+ `gate_report` 非 null + `approved_by` 非空 + 参数扫描归档；阈值见 `thresholds.yaml` |
| 6. 审计 | `audit.preset_resolved` 记录实际解析版本，支撑 Q9 |

| 禁止 | 理由 |
| --- | --- |
| 在 `template` 上填 `gate_report` / `approved_by` 冒充已审批 | 违反 R-21 / D18 |
| 把 `production` 指向 `template` / `staging` 版本 | 状态枚举约束（§2） |
| 在 preset 文件里写 schema 未登记字段 | 违反 `additionalProperties:false`，会被 S 层 `E-SCHEMA-002` 拒绝 |
| 用 `style_prompt` 作唯一控制手段 | `E-CAPABILITY-004`（§5） |
| 改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md` | 受保护文件，需法务 + `License-Review:` |

## 8. Phase 3 边界与开放项

| 项 | 状态 |
| --- | --- |
| 注册中心运行时（解析 / 版本比对 / 展开） | ⏳ Phase 3，见 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §5 #13/#14 与本文 §3/§4 |
| `GET /v1/presets/{id}` 实现 | ⏳ Phase 3，见 [`API-SPEC.md`](API-SPEC.md) §5 |
| 参数扫描 Harness（§5.6 单调性） | ⏳ Phase 2–3；阈值见 `thresholds.yaml` |
| golden_set v1 冻结与门禁 | ⏳ Phase 2；未过前 `production` 恒为 `null` |
| `scenario` → 默认值映射表 | ⏳ 待 Phase 2 基座定型 + 单调性扫描后填写；Phase 0 只有接口，不写具体数值结论 |
| D11 许可法务定稿 | 仍为发布权重前阻塞项；preset 不触碰权重发布 |
| R-14b 法务跟进 | 仍开放 |
| 新增决策编号 | 本文未发明任何 D / R 号；未分配项写「建议新增决策（待 Lead 编号）」 |

**追溯**：F5（preset 一键复现）、F8（版本化审计）、Q9（可复现）、Q10（参数正交）、ADR-0003 §3/§7（确定性优先、可复现性）、R-17（契约与实现漂移）、R-20（错误码漂移，由 [`CONTROL-LAYER-SPEC.md`](CONTROL-LAYER-SPEC.md) §9 缓解）、R-21 / D18（Phase 0 preset 冻结）。
