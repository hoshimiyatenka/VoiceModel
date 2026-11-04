# AI 智能体声音训练项目 · 技术栈方案（v0.3 · 契约落地版）

| 项目 | 内容 |
| --- | --- |
| 文档编号 | VM-TECH-001 |
| 版本 | **v0.3**（第三次迭代 / 待评审） |
| 前一版 | [v0.2（许可 / 论文 / 仓库规范）](AI智能体声音训练项目_技术栈方案_v0.2.md) · [v0.1（初版）](AI智能体声音训练项目_技术栈方案_v0.1.md)，均保留存档 |
| 状态 | DRAFT — 供三轮评审 |
| 日期 | 2026-11-04 |
| 项目根目录 | `D:\.[Important Pro]\Voice_Model` |
| GitHub 仓库 | `https://github.com/hoshimiyatenka/VoiceModel` |

---

## v0.3 本次迭代的输入与目标

用户第三轮指令（m00207）：**「继续迭代」**——在 v0.2 完成三项指令（许可策略 / 论文体系 / 仓库与提交规范）并成功建仓推送后，继续推进 v0.2 §13.2 登记的「v0.3 必做」项。

| # | v0.2 §13.2 承诺 | 本版响应 | 落点 |
| --- | --- | --- | --- |
| 1 | VoiceSpec 正式 JSON Schema + validate 接口错误码表 | **落地机器可读契约**：JSON Schema 2020-12 单一真源、两层校验（S/C）、错误码表、示例、本地/CI 校验脚本 | **第 2 章**（全新）、[`configs/voicespec/voicespec.schema.json`](../configs/voicespec/voicespec.schema.json)、[`docs/voicespec/`](voicespec/README.md)、[`scripts/validate_voicespec.py`](../scripts/validate_voicespec.py) |
| 2 | ADR-0003（参数化控制层实现路径） | 把 v0.1/v0.2 文字约定固化为正式决策，含 M1–M6 优先级修订、能力探测、许可联动、验收条件 | **第 3 章**（全新）、[`docs/decisions/ADR-0003.md`](decisions/ADR-0003.md) |
| 3 | 论文发表状态补齐 | 用 arXiv API 逐篇补齐 `journal_ref`/`comment`，补 Qwen3-TTS / Vocos / ESD / CASIA / EmoV-DB 的 ID 或明确「未找到」 | **第 4 章**、[`docs/references/PAPERS.md`](references/PAPERS.md) |
| 4 | R-14 剩余权重/数据集许可核验 | 继续用 HF Model/Dataset API + GitHub LICENSE 原文核验，能清零的清零，不能的降级并登记法务跟进 | **第 5 章**、[`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md) |
| 5 | （顺带）仓库一致性 | README / CHANGELOG / CONTRIBUTING / CODEOWNERS / 提交规范 / CI 全部同步到 v0.3；`eval-gate` 从纯占位升级为**真实校验 VoiceSpec 契约** | **第 6 章** |

### 诚实基线（不变）

**技术路径仍为 Phase 0（立项 / 选型核验期），尚未开始数据与训练，无任何实测指标。** v0.3 把「契约」从文字变成可执行代码，但没有产出任何模型、数据或分数。Q1–Q10 依旧是目标门禁，`configs/eval/thresholds.yaml` 仍标 `calibration.status=uncalibrated`。

> 一个重要区分：v0.3 的 `eval-gate` CI 里跑的 **VoiceSpec 契约校验是真实生效的代码**，不是占位；而 golden_set 合成 / Q1–Q10 门禁仍是 Phase 2 骨架。二者不要混淆。

---

## 修订记录

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v0.1 | 2026-11-04 | 初版：需求拆解、五层参数化控制体系、双轨路线、数据/训练/评估/排期、风险、决策点 |
| v0.2 | 2026-11-04 | 许可与权利保留策略、权威论文体系（52 篇）、GitHub 仓库与提交规范、在线核验回填、论文驱动的设计修正 |
| **v0.3** | 2026-11-04 | ① VoiceSpec 正式 JSON Schema + 错误码表 + 示例 + 校验脚本（文字约定 → 机器可执行契约）② ADR-0003 参数化控制层实现路径 ③ 论文发表状态与新增 ID 补齐 ④ R-14 剩余许可核验回填 ⑤ CI 契约校验真实生效、提交规范/受保护路径/文档全量同步 |

---

## 目录

1. [一页摘要与当前状态](#1-一页摘要与当前状态)
2. **【v0.3 核心】[VoiceSpec 正式契约](#2-voicespec-正式契约)**
3. **【v0.3 新增】[ADR-0003：参数化控制层实现路径](#3-adr-0003参数化控制层实现路径)**
4. [论文清单补齐](#4-论文清单补齐)
5. [R-14 剩余许可核验回填](#5-r-14-剩余许可核验回填)
6. [仓库一致性同步](#6-仓库一致性同步)
7. [架构与需求基线（指向 v0.1/v0.2）](#7-架构与需求基线指向-v01v02)
8. [风险与待决策更新](#8-风险与待决策更新)
9. [v0.4 迭代方向](#9-v04-迭代方向)
10. [附录：文件索引](#10-附录文件索引)

---

## 1. 一页摘要与当前状态

### 1.1 v0.3 一句话

> 把「所有声音可参数化细调」从**文档约定**升级为**机器可执行、可 CI 回归、可版本化、可取证**的正式契约 `VoiceSpec v0.3.0`，同时把 v0.2 遗留的核验尾巴（R-14 / 论文发表状态）尽量清零，并让仓库所有规范文件自洽。

### 1.2 三轮迭代的主线

```
v0.1  能不能做、怎么做        → 出完整技术路径 + 五层参数化设计
v0.2  凭什么这么做、能不能公开 → 论文核验 + 许可合规 + 仓库落地
v0.3  怎么保证不走样          → 契约机器可执行 + 冲突/错误显式 + CI 强校验
```

### 1.3 当前进度

| 已完成（累计） | 未完成 |
| --- | --- |
| 需求澄清；v0.1/v0.2 方案；52 篇论文核验；许可证传导分析；公开仓库 + 提交规范 + 3 个 CI 全绿；**VoiceSpec JSON Schema + 错误码表 + 示例 + 校验脚本 + ADR-0003** | 算力确认、数据授权与采集、基座复现、任何训练产出、任何评测分数、**许可条款法务定稿（D11）**、**部分权重/数据集许可（R-14）** |

### 1.4 一页决策（本版新增/变更项）

| 编号 | 决策 | 状态 |
| --- | --- | --- |
| D12 | VoiceSpec 用 **JSON Schema 2020-12** 作单一真源，全部对象 `additionalProperties:false` | **v0.3 新增，已落地** |
| D13 | 校验分 **S 层（Schema）+ C 层（Control）** 两层，错误码稳定只追加 | **v0.3 新增，契约层已落地，C 层 Phase 3 实现** |
| D14 | `eval-gate` CI 从纯占位升级为**真实校验 VoiceSpec 示例** | **v0.3 新增，已落地** |
| D15 | 每个契约变更须填 `Spec:` footer 并受 CODEOWNERS 保护 | **v0.3 新增，已落地** |

---

## 2. VoiceSpec 正式契约

> 本章是 v0.3 对 v0.2 §13.2 第 1 项的答复。完整机器可读定义在 [`configs/voicespec/voicespec.schema.json`](../configs/voicespec/voicespec.schema.json)，使用说明见 [`docs/voicespec/README.md`](voicespec/README.md)，错误码见 [`docs/voicespec/ERROR-CODES.md`](voicespec/ERROR-CODES.md)。

### 2.1 为什么必须落成 Schema

v0.1/v0.2 定义了五层 VoiceSpec 与冲突矩阵，但只有文字约定，存在三个「细调可信度杀手」：

1. 参数拼错被静默忽略 → 调了等于没调；
2. 冲突靠口头约定，实现时容易写成静默覆盖 → 复现结果不可预期；
3. 换基座时上层调用方要跟着改 → 违背「L5 契约稳定」的架构目标。

v0.3 把 L5 变成可校验、可版本化、可测试的正式契约。

### 2.2 五层结构（与 v0.1 §5.2 一致）

| 层 | `$defs` | 职责 | 必填 |
| --- | --- | --- | --- |
| L-A | `IdentitySpec` | 是谁在说 | 顶层必填，`speaker_id` 必填 |
| L-B | `ProsodySpec` | 怎么说（连续细调主战场） | 可选 |
| L-C | `StyleSpec` | 什么状态说（含候选 `AttributeSpec`） | 可选 |
| L-D | `LinguisticSpec` | 把字念对（确定性规则层） | 可选 |
| L-E | `RenderSpec` | 最后怎么送出去 | 可选 |
| — | `AuditSpec` | 审计元数据（服务端只读） | 客户端禁止传入 |

顶层必填 `text` + `identity`；其余层缺省时由控制层用注册默认值/preset 展开。

### 2.3 三条硬规则（写进 schema，不是口头约定）

1. **不静默**：所有对象 `additionalProperties:false`，未知字段直接报 `E-SCHEMA-002`。契约**绝不忽略任何字段**。
2. **preset 是默认值集合，不是强制值**：spec 中显式字段覆盖 preset 展开值；`scenario` 展开的默认值被显式 L-B/L-C 覆盖（`W-CONFLICT-007`）。
3. **确定性优先**：L-D 发音规则、M4 文本标记、M2 特征编辑优先于自然语言指令；`style_prompt` 不得单独作为 preset 唯一控制手段（`E-CAPABILITY-004`）。

### 2.4 两层校验分工

| 层 | 负责 | 技术 | 落地状态 |
| --- | --- | --- | --- |
| **S 层 Schema** | 结构 / 类型 / 范围 / 枚举 / 可静态判定的字段依赖 | JSON Schema 2020-12（标准库 `jsonschema`） | ✅ 本版已落地，本地 + CI 可跑 |
| **C 层 Control** | 跨字段语义冲突 / preset 合并 / 能力探测 / 降级 / 许可 / 审计填充 | L5 控制层代码 | ⏳ Phase 3 实现，错误码已全部登记 |

**原则**：能用 Schema 静态表达的绝不放进 C 层手写 if；Schema 表达不了的（如 `Σpauses < duration_ms × 0.4`）才落 C 层，并在错误码表登记。

校验顺序：

```
解析 JSON → S 层 → preset 解析合并 → C 层 → 能力探测/降级
→ 填充 audit.*（服务端只读）→ 合成 → 门禁 → 审计日志
```

HTTP：`POST /v1/synthesize` 校验失败一律 400；`POST /v1/presets/validate` 失败 422。响应信封统一 `valid` / `errors[]` / `warnings[]`。

### 2.5 Schema 已静态表达的约束（示例）

| 约束 | 错误码 | 实现 |
| --- | --- | --- |
| 缺 `text` / `identity`、类型/范围/枚举不符、未知字段 | `E-SCHEMA-001..006` | `required` / `type` / `minimum` / `enum` / `additionalProperties:false` |
| 给了 `ref_text` 却没给 `ref_audio_uri` | `E-DEPENDENCY-001` | `IdentitySpec.allOf[0].if/then` |
| `duration_mode=exact` 缺 `duration_ms` | `E-DEPENDENCY-002` | `ProsodySpec.allOf[0].if/then` |
| `duration_mode=range` 缺 `duration_range_ms` | `E-DEPENDENCY-003` | `ProsodySpec.allOf[1].if/then` |
| `rate` 与任何 duration 精确/区间控制同时显式给出 | `E-CONFLICT-001`（静态部分） | `ProsodySpec.not` |
| `spec_version` 不为 `0.3.0` | `E-SCHEMA-006` | `const` |

> **已验证**：故意构造 `rate + duration_mode=exact` 的非法用例，`scripts/validate_voicespec.py` 确实返回 1 并命中 `not` 约束；三个合法示例（minimal / full_tuned / duration_exact）全部通过。约束非摆设。

### 2.6 错误码体系（摘要）

S 层 10 个 + C 层 18 个，全部登记在 [`docs/voicespec/ERROR-CODES.md`](voicespec/ERROR-CODES.md)。关键语义冲突：

| 码 | 规则 | 是否报错 |
| --- | --- | --- |
| `E-CONFLICT-001` | `rate` ↔ `duration_*` | **报错 400**（互斥） |
| `E-CONFLICT-002` | `Σpauses > duration_ms × 0.4` | 报错 |
| `E-CONFLICT-003` | `energy_db` ↔ `loudness_lufs` | **不冲突**（表现力 vs 交付响度，同时生效） |
| `E-CONFLICT-004` | `voice_blend` ↔ `speaker_lock=true` | 报错 |
| `E-CONFLICT-005` | `pitch_semitones` ↔ `pitch_contour` | **不冲突**（全局偏移 + 相对形状，叠加） |
| `W-CONFLICT-006/007` | `emotion`↔`style_prompt`、`scenario`↔显式参数 | 告警，不阻断 |

把「已判定不冲突」的项也登记在案，是为了防止后续实现误加互斥校验。

### 2.7 与合规/可复现联动

- `render.watermark` 默认 `true`；无商业授权凭证时 `false` → `E-LICENSE-001`（v0.2 §2.6 + AudioSeal `arXiv:2401.17264`）。
- `ref_audio_uri` 须指向已注册且已授权说话人 → `E-LICENSE-002`。
- 每个 preset 携带 `audit.license = PolyForm-Noncommercial-1.0.0`；`audit.*` 服务端只读，客户端传入 → `E-AUDIT-001`。
- 固定 `preset@version + model@commit + seed + text + deps_lock` → 波形 byte-level 一致（Q9）。

### 2.8 版本演进规则

- 新增**可选**字段 → `spec_version` minor +1（如 `0.3.1`），旧 preset 不受影响。
- 新增**必填**字段 / 改枚举 / 收紧范围 → major +1（`1.0.0`），须同步 ADR + 全量 golden_set 回归。
- 删除字段 → major +1，保留一个 minor 版本兼容期。
- 每次变更必须：更新错误码表 §5、补 `examples/` 用例、CHANGELOG 记录、填 `Spec:` footer。

### 2.9 `AttributeSpec` 仍是候选

Spark-TTS（`arXiv:2503.01710`）式属性级控制作为 L-C 补充实现方式保留在 schema 中，但**每个属性必须先过 §5.6 单参数 5 点单调性扫描**（ρ ≥ 0.90）才允许进 production preset（`W-CAPABILITY-003`）。这是 v0.2 §5.3 第 2 条「需先过单调性测试才开放」的契约级落实。

---

## 3. ADR-0003：参数化控制层实现路径

> 完整 ADR 见 [`docs/decisions/ADR-0003.md`](decisions/ADR-0003.md)。状态：**Accepted（契约层）/ Phase 3 待实现**。

### 3.1 取代关系

ADR-0003 **取代 v0.1 §5.4 的 M1–M6 优先级**（`M4>M1>M2>M5>M3>M6`），正式确立 v0.2 §5.3 的修订版：

```
M4 文本确定性规则 > M2 声学特征编辑（连续量）> M1 原生条件（离散量）
> M5 参考解耦 > M3 adapter 混合 > M6 DSP（仅限渲染层/降级）
```

依据：FastSpeech 2（`arXiv:2006.04558`）证明 F0/energy/duration 可作显式条件注入，连续物理量走 M2 比自然语言指令更精确可复现；`pitch`/`rate` 主控制**禁用 M6 DSP**（金属音、损相似度），仅作降级并置 `audit.degraded=true` + `W-RENDER-001`。

### 3.2 关键决策点

| # | 决策 | 理由 |
| --- | --- | --- |
| 1 | JSON Schema 2020-12 单一真源 | 编辑器/CI 生态最成熟，API 本来就是 JSON，无需生成代码 |
| 2 | S 层 + C 层两层校验 | 静态约束进 Schema，跨字段算术/能力/许可进 C 层，避免手写 if 散落 |
| 3 | `additionalProperties:false` 全覆盖 | 禁止静默忽略，兼容靠显式版本升级 |
| 4 | 冲突一律显式（报错或优先级） | 静默覆盖是「参数化细调」最常见的可信度杀手 |
| 5 | 能力探测失败先报错、降级须告警 | F4 升 P0 后 `duration_mode=exact` 不支持直接报 `E-CAPABILITY-001`，不静默降级 |
| 6 | 许可/水印/音色鉴权进契约 | 让「不得商业化」「禁止去水印」「禁止未授权克隆」在接口层可执行 |
| 7 | 错误码稳定只追加 | 便于调用方与审计长期依赖 |

### 3.3 备选与否决

| 备选 | 否决理由 |
| --- | --- |
| Protobuf / 自定义 DSL | 需生成代码与运行时，可读性差 |
| 只写文档不落 schema | 无法防拼写错误与静默覆盖 |
| 全部冲突塞进 JSON Schema | `Σpauses < duration_ms × 0.4` 等跨字段算术表达不了，硬塞牺牲可读性 |
| 允许额外字段（前向兼容） | 与「禁止静默忽略」冲突，兼容走 `spec_version` |

### 3.4 验收条件（Phase 3）

- [ ] 两个 API 接入 S+C 两层校验，错误码与契约一致
- [ ] `examples/*.json` 全通过，故意非法用例被拦截
- [ ] 每个开放参数完成 §5.6 单参数 5 点扫描并归档报告
- [ ] preset 注册/版本解析可用；`audit.*` 服务端填充生效
- [ ] golden_set 回归 0 异常（Q8）

---

## 4. 论文清单补齐

> 完整清单见 [`docs/references/PAPERS.md`](references/PAPERS.md)。本节记录 v0.3 相对 v0.2 的补齐动作，结果以「核验回填」小节为准。

### 4.1 v0.2 遗留的论文 TODO

v0.2 的 PAPERS.md 末尾登记了 5 项待补齐：

1. 补齐标 `—` 条目的正式发表状态（部分为技术报告/预印本）
2. Qwen3-TTS 官方技术报告 arXiv ID（v0.2 未取到）
3. Vocos 声码器论文 ID
4. ESD / CASIA / EmoV-DB 情感数据集论文 ID 与许可证
5. 各论文 DOI / 会议主页链接

### 4.2 核验方法（不变）

arXiv Atom API `https://export.arxiv.org/api/query?id_list=...`，取 `journal_ref` / `comment` 字段；按标题 `search_query=ti:"..."` 查缺失 ID。核验日期 2026-11-04。`web_fetch` / `web_search` 通道依旧不可用，全部走 pwsh + `gh` / `Invoke-WebRequest`。

> **回填结果见 §4.3**：能查到的补 `journal_ref`/`comment` 与 ID；确实查不到的一律标 `[MISS]`，**不编造**。机构倾向仅用于说明国内外覆盖面，不作精确归属证明。
> 核验结果由**两条独立路径交叉印证**：subagent 委派核验 + Lead 本地独立跑 arXiv API，17 篇既有 ID 的 `journal_ref`/`comment`、6 个新增 ID、5 个 HF 权重卡、4 个数据集结论完全一致。

### 4.3 论文核验回填（2026-11-04）

#### 4.3.1 新增 arXiv ID（原 v0.2 待补，已取到）

| 项 | ID | 精确标题 | 首发 | `comment` | 核验 |
| --- | --- | --- | --- | --- | --- |
| Qwen3-TTS 技术报告 | **`2601.15621`** | Qwen3-TTS Technical Report | 2026-01-22 | `https://github.com/QwenLM/Qwen3-TTS` | [OK] `https://export.arxiv.org/api/query?id_list=2601.15621` |
| Qwen3-TTS 评测关联 | `2610.23678` | Beyond the Benchmark: Conditioning, Domains and Failure Modes of Qwen3-TTS | 2026-10-16 | — | [OK] `search_query=ti:"Qwen3-TTS"` 命中 2 条之一 |
| Vocos 声码器 | **`2306.00814`** | Vocos: Closing the gap between time-domain and Fourier-based neural vocoders for high-quality audio synthesis | 2023-06-01 | 空 | [OK] `id_list=2306.00814`，作者 Hubert Siuzdak |
| ESD 数据集论文 A | **`2010.14794`** | Seen and Unseen emotional style transfer for voice conversion with a new emotional speech dataset | 2020-10-28 | `Accepted by ICASSP 2021` | [OK] |
| ESD 数据集论文 B | **`2105.14762`** | Emotional Voice Conversion: Theory, Databases and ESD | 2021-05-31 | `Speech Communication` | [OK] |
| EmoV-DB 论文 | **`1806.09514`** | The Emotional Voices Database: Towards Controlling the Emotion Dimension in Voice Generation Systems | 2018-06-25 | `Submitted to SLSP 2018` | [OK] |

#### 4.3.2 纠错（重要）

- **`2111.01606` 不是 ESD 论文**：API 实际返回 `PolyTrack: Tracking with Bounding Polygons`（2021-11-02，NeurIPS 2021 MLAD Workshop）。**任何文档不得再把该 ID 关联到 ESD**；ESD 正确 ID 为 `2010.14794` / `2105.14762`。
- `[MISS]` **CASIA 中文情感语料论文**：arXiv `ti:"CASIA" AND all:"corpus"` 返回 `totalResults=0`；命中的 CASIA 条目均为 SER 方法论文（如 `2008.06667` / `2308.14568` / `2411.19803`），非语料本身。**标「未找到」，不猜 ID**。
- `[OK]` AISHELL-3 `2010.11567`（2020-10-22）、WenetSpeech `2110.03370`（2021-10-07）标题与日期复核一致，清单原记录无误。

#### 4.3.3 发表状态降级（影响 v0.2 表述）

对 13 个 ID 取 `arxiv:journal_ref` + `arxiv:comment`：**全部 13 个 `journal_ref` 字段为空**，仅 6 条有 `comment` 线索。核验源：`https://export.arxiv.org/api/query?id_list=1609.03499,2006.04558,2106.06103,2210.02747,2301.02111,2403.03100,2409.00750,2503.01710,2506.21619,2509.24650,2006.11239,2206.04658,2212.04356&max_results=20`

| ID | `comment`（原文线索） | v0.3 结论 |
| --- | --- | --- |
| `1609.03499` WaveNet | 空 | 预印本，arXiv 未记录正式发表 |
| `2006.04558` FastSpeech 2 | `Accepted by ICLR 2021` | **arXiv 自述**，未经 `journal_ref` 确认 |
| `2106.06103` VITS | `ICML 2021` | **arXiv 自述** |
| `2210.02747` Flow Matching | 空 | 预印本 |
| `2301.02111` VALL-E | `Working in progress` | 未正式发表 |
| `2403.03100` NaturalSpeech 3 | `Achieving human-level quality...`（成果描述，非会议） | 预印本 |
| `2409.00750` MaskGCT | 空 | 预印本 |
| `2503.01710` Spark-TTS | `Submitted to ACL 2025` | 投稿中 |
| `2506.21619` IndexTTS2 | 空 | 预印本 |
| `2509.24650` VoxCPM | `Technical Report` | 技术报告 |
| `2006.11239` DDPM | 空 | 预印本（实际 NeurIPS 2020，但 arXiv 无记录） |
| `2206.04658` BigVGAN | `To appear at ICLR 2023...` | **arXiv 自述** |
| `2212.04356` Whisper | 空 | 预印本 |

另 4 个复核：`2406.02430` Seed-TTS（comment 空）、`2306.15687` Voicebox（`Accepted to NeurIPS 2023`）、`2309.02285` PromptTTS 2（demo page）、`2301.13662` InstructTTS（`Submit to TASLP`），`journal_ref` 同样全空。

> **规则**：PAPERS.md 中「发表/状态」列今后一律区分两档——`arXiv comment 自述`（如 ICLR/ICML/NeurIPS）与 `journal_ref 确认`。**ICLR/ICML/NeurIPS 等会议归属未经 arXiv `journal_ref` 确认**，需从会议官网或 DBLP 二手核验后才可升级。v0.2 中把会议名写得像「已确认正式发表」的表述，以本版为准降级。
>
> 这不改变论文的技术参考价值（ID、标题、日期已核验），只收紧「发表状态」的可信度表述，符合项目「不虚报」的基线原则。

#### 4.3.4 清单篇数变更

PAPERS.md 由 **52 篇增至 58 篇**（v0.3 补录 6 篇：Qwen3-TTS 技术报告、Qwen3-TTS 评测、Vocos、ESD×2、EmoV-DB）。归档版 v0.2 正文仍记 52 篇，**以本版与 PAPERS.md 的 58 篇为准**。CASIA 语料论文 `[MISS]` 明确标「未找到」，不计入。

**仍待人工/法务跟进（论文侧）**：13 篇的正式会议/期刊归属需从会议官网或 DBLP 二手核验；各论文 DOI / 会议主页链接待补。

---

## 5. R-14 剩余许可核验回填

> 完整矩阵见 [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md)。核验日期 2026-11-04。

### 5.1 v0.2 登记的 R-14 待清零项

- F5-TTS / GPT-SoVITS / HiFi-GAN 的**模型权重**许可证（v0.2 仅核验代码 MIT）
- `IndexTeam/IndexTTS-2` 权重卡条款（HF 无 license tag）
- Fish Audio 权重许可证（与代码许可是否一致）
- ESD / CASIA / EmoV-DB / Common Voice 的商用范围
- Qwen3-TTS 技术报告 arXiv ID、Vocos 论文与许可

### 5.2 核验通道

Hugging Face Model/Dataset API（`https://huggingface.co/api/models/<id>` / `/api/datasets/<id>`，取 `tags[]` 中 `license:*`、`gated`，及 README 原文）；GitHub `gh api repos/<owner>/<repo>/license`；官方许可站点原文。

> **回填结果见 §5.3**：`[OK]` 项给出结论 + 依据原文 + URL；`[MISS]` 项明确原因，**不编造**；仍无法在线确认的列「需法务跟进」。
> 核验方法补充：HF API 对不存在/私有/受限的 model/dataset ID 统一返回 **HTTP 401**（已用不存在 ID、`meta-llama/Llama-2-7b`=200、`coqui/XTTS-v2`=200 对照验证），故所有 401 一律按「该 ID 不存在或不可公开访问」处理，不据此推断许可。

### 5.3 R-14 核验回填（2026-11-04）

#### 5.3.1 ★ 最重要的新发现：代码与权重许可不一致（商用不可用）

v0.2 主要按**代码**许可推断候选可用性，本轮逐项核验 HF 权重卡后发现多处「代码宽松、权重禁商用」。这类候选**不能作为可商用基座**，但对本项目 NC 定位需分别判断：

| 上游 | 代码许可 | **权重许可（核验）** | 商用 | 判定 |
| --- | --- | --- | --- | --- |
| `SWivid/F5-TTS` | MIT | **`cc-by-nc-4.0`**（HF `SWivid/F5-TTS`：`tags=license:cc-by-nc-4.0`、`cardData.license=cc-by-nc-4.0`、`gated=false`） | ❌ | **v0.2 记为「MIT，效率对照候选」须修正**：权重禁商用；本项目 NC 定位一致，但不可对外声称可商用 |
| `fishaudio/fish-speech` 家族 | Fish Audio Community License v1.0（2026-10-13；III(a) 年营收<USD 500k 有限商用、III(c) Hosted 须单独书面许可） | **不一致**：`fish-speech-1/1.2/1.2-sft/1.4/1.5`、`speech-lm-v1`、`s1-mini`、`fish-agent-v0.1-3b` 全为 **`cc-by-nc-sa-4.0`**；`s2-pro`/`drama-3`/`drama-3-int4` 为 `license:other, license_name=fish-audio-research-license`（**仅研究/非商用**，`business@fish.audio` 另议） | ❌ | 权重 **NC-SA 传染** → 依 ADR-0001 更不可作发布基座；`s1-mini` 权重卡另有 "I agree to use this model for non-commercial use ONLY" 勾选 |
| `coqui-ai/TTS` | MPL-2.0 | **额外权重限制**：`.models.json` 中 `xtts_v2`/`xtts_v1.1` = `"license":"CPML", "tos_required":true`、`your_tts` = `CC BY-NC-ND 4.0`；HF `coqui/XTTS-v2` = `license:other, license_name=coqui-public-model-license` | 条件 | 代码 MPL 不代表权重可商用；`CPML` 全文 `https://coqui.ai/cpml` 已 404（关站），**需法务从存档确认** |
| `RVC-Boss/GPT-SoVITS` | MIT | `[MISS]` HF 组织下 0 个模型、精确 ID HTTP 401；镜像 `lj1995/GPT-SoVITS` = `license:mit` | 未定 | 官方权重许可无法在线确认，**需人工确认是否独立于 MIT 代码** |
| `SparkAudio/Spark-TTS` | Apache-2.0 | `cc-by-nc-sa-4.0`（v0.2 已核验） | ❌ | 维持 ADR-0001：不用其权重作发布基座 |

> 依据 URL：`https://huggingface.co/api/models/SWivid/F5-TTS` · `https://huggingface.co/fishaudio/fish-speech-1.5/raw/main/README.md` · `https://huggingface.co/fishaudio/s2-pro/raw/main/LICENSE.md` · `https://raw.githubusercontent.com/coqui-ai/TTS/dev/TTS/.models.json` · `https://huggingface.co/coqui/XTTS-v2`
>
> **结论**：v0.2 §4.1 对 F5-TTS / Fish-Speech / coqui 的「商用」列按代码推断的部分已被本版修正。**轨道 A 首选仍为 CosyVoice 2 / Qwen3-TTS / VoxCPM2**（三者代码与权重均 Apache-2.0，v0.2 已核验），本轮发现反而**强化**了 ADR-0001「选宽松许可权重」的决策。

#### 5.3.2 其余权重/工具核验

| 项 | 结果 | 依据 |
| --- | --- | --- |
| `IndexTeam/IndexTTS-2` 权重卡 | **[OK] 确认 v0.2「无 license tag」**：`tags` 无 `license:*`、`cardData.license` 空、`gated=false`、README 全文无许可条款 | `https://huggingface.co/api/models/IndexTeam/IndexTTS-2` |
| ↳ 但 GitHub 有自定义权重协议 | **[OK] 新增约束（v0.2 未记）**：`index-tts/index-tts` spdx=`NOASSERTION`「bilibili Model Use License Agreement」§2.2 MAU>1亿 或上年营收>RMB 10亿须另行书面授权；§4.1(c) *"You may not Use ... to improve any AI model, except for ... non-commercial AI models"* | `https://github.com/index-tts/index-tts/blob/main/LICENSE` |
| ↳ 同组织对照 | `IndexTeam/Index-TTS`=apache-2.0、`IndexTTS-1.5`=apache-2.0、`IndexTTS-2.5`=license:other → **同组织许可不一致** | `https://huggingface.co/api/models?author=IndexTeam&limit=100` |
| HiFi-GAN 代码 | `jik876/hifi-gan` = MIT（Copyright (c) 2020 Jungil Kong） | `gh api repos/jik876/hifi-gan/license` |
| HiFi-GAN HF 权重 | **许可不统一**：`ntt123/hifigan_ljs_24k`=cc-by-nc-4.0、`hifigan_ljs_22k`=cc-by-nc-sa-4.0、两款 espnet=cc-by-4.0、`jaketae/hifigan-lj-v1` 无 tag | 各 HF Model API |
| Vocos | **代码与权重均 MIT**：`charactr/vocos-mel-24khz` / `vocos-encodec-24khz` = `license:mit`；GitHub `gemelo-ai/vocos` spdx=MIT | `https://huggingface.co/charactr/vocos-mel-24khz` · `https://github.com/gemelo-ai/vocos` |
| Vocos 精确 ID | `[MISS]` `charactr/vocos`（GitHub 404）/ HF `api/models/charactr/vocos`（401）→ 已迁 `gemelo-ai/vocos` | — |

#### 5.3.3 数据集商用范围（收紧）

| 数据集 | 结论 | 依据原文 |
| --- | --- | --- |
| **EmoV-DB** | **★ 仅非商用**，商用须单独联系 | OpenSLR 115 → `LICENSE.md`：*"By downloading or using the EmoV-DB Dataset, you are agreeing to the 'Non-commercial Purposes' condition... If you wish to make use of the EmoV-DB Dataset for Commercial Purpose, please contact Prof. Sarah Ostadabbas"*。`https://www.openslr.org/115/` · `https://raw.githubusercontent.com/numediart/EmoV-DB/master/LICENSE.md` |
| AISHELL-3 | **Apache-2.0，可商用** | OpenSLR 93 `License: Apache License v.2.0`；HF `AISHELL/AISHELL-3` `license:apache-2.0` |
| WenetSpeech | GitHub LICENSE = Apache-2.0；HF `wenet-e2e/WenetSpeech` **gated=auto 且无 license tag**（需申请 PASSWORD）；衍生 `WenetSpeech4TTS` = `cc-by-4.0`、gated=auto | `https://raw.githubusercontent.com/wenet-e2e/WenetSpeech/master/LICENSE` · HF dataset API |
| **ESD** | `[MISS]` 官方许可无法在线确认 | 官方页 `https://hlj-group.github.io/ESD/` 404；3 个 GitHub 组织仓库全 404；HF 同名 ID 401；第三方镜像互相矛盾（`oxschaos/esd_dataset`=apache-2.0 / `DynamicSuperb/...`=mit / `duanyu027/ESD` 无 tag） |
| **CASIA 中文情感语料** | `[MISS]` 官方许可无法在线确认 | `chineseldc.org` 超时、`casia.cn` SSL 信任失败；仅第三方 HF 镜像标 apache-2.0（非官方） |
| Common Voice | 未在本轮核验（保留待办） | — |

> **对 §6 数据工程的影响**：EmoV-DB 的 NC 属性与本项目 NC 定位**一致**（可作研究/评测数据），但**不得用于任何商业授权产物**；ESD / CASIA 在官方许可确认前**不得进入训练数据**（连 manifest 都不建），仅保留为「待法务跟进」；AISHELL-3 / WenetSpeech 可商用但后者需申请。v0.2 §6「公开数据仅作流水线验证/评测对照」的原则不变，且边界更清晰。

#### 5.3.4 R-14 未清零项（需人工/法务跟进，登记为 R-14b）

1. **ESD 官方许可**：官方页/GitHub/HF 全线 404/401，第三方镜像矛盾。
2. **CASIA 官方许可**：官方站点超时/SSL 失败，arXiv 无对应语料论文。
3. **Coqui CPML 全文**：`coqui.ai/cpml` 404（关站），仅 `.models.json` 与 XTTS-v2 README 间接证据。
4. **fishaudio 精确权重 ID**：`fishaudio/fish-speech` / `OpenAudio-S1` 401/404，需确认 `s2-pro` 与 OpenAudio-S1 对应关系。
5. **RVC-Boss/GPT-SoVITS 官方权重卡**：org 下 0 模型、精确 ID 401。
6. **IndexTTS-2**：HF 权重卡无条款但 GitHub 有 bilibili 自定义协议，需法务确认 HF 权重是否受其约束。
7. **WenetSpeech**：HF `gated=auto` 的申请条款与 PASSWORD 条件需确认。
8. **13 篇论文**正式会议/期刊归属（§4.3.3）。

> **R-14 结论：本版完成「分项核验 + 边界收窄」，但未清零**。已 `[OK]` 项回填进 [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md)，`[MISS]` 项降级为 R-14b 法务跟进清单，不再笼统标「待核验」。新增 **R-18**（代码/权重许可不一致风险）。

---

## 6. 仓库一致性同步

v0.3 把仓库所有规范文件同步到新版本，避免「文档说一套、CI 校验另一套」：

| 文件 | 变更 |
| --- | --- |
| [`README.md`](../README.md) | 当前方案指向 v0.3；新增 VoiceSpec 契约入口、本地校验命令、最小请求示例；文档索引补 schema/错误码/ADR-0003 |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | 文档索引同步 v0.3；受保护路径补 `configs/voicespec/**`；检查清单补契约校验命令 |
| [`COMMIT_CONVENTION.md`](../COMMIT_CONVENTION.md) | 新增 `Spec:` footer（改契约时必填）；受保护路径补契约文件 |
| [`.commitlintrc.yml`](../.commitlintrc.yml) | type/scope 枚举未变（本轮无需新增 scope，用 `control` / `deps` / `docs` / `refs` 覆盖） |
| [`CODEOWNERS`](../CODEOWNERS) | 新增 `configs/voicespec/` · `docs/voicespec/` · `ADR-0003.md` 受保护 |
| [`.github/workflows/commitlint.yml`](../.github/workflows/commitlint.yml) | 新增「改契约文件须带 `Spec:` footer」校验 |
| [`.github/workflows/eval-gate.yml`](../.github/workflows/eval-gate.yml) | **从纯占位升级**：新增 `python scripts/validate_voicespec.py configs/voicespec/examples/*.json` 真实校验；触发路径补契约文件；依赖补 `scripts/requirements.txt` |
| [`CHANGELOG.md`](../CHANGELOG.md) | 追加 v0.3.0 段（首次导入批次手工播种一次，之后由 conventional-changelog 生成） |

> `license-check.yml` 无需改动：本轮未改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md`。

---

## 7. 架构与需求基线（指向 v0.1/v0.2）

v0.3 **不改动** v0.1/v0.2 已确立的架构、需求、数据、训练、评估、排期、许可结论，仅把「参数化控制层」契约化。以下为索引，内容以原版为准：

| 主题 | 权威出处 |
| --- | --- |
| 需求 F1–F8 / Q1–Q10 / 五层架构 L6→L0 / 双轨路线 / 五层参数化细调 / 冲突矩阵 / 参数扫描 / preset | [v0.1 §1–5](AI智能体声音训练项目_技术栈方案_v0.1.md) |
| 数据工程 / 训练 SFT→DPO→量化 / 评估四套数据集与门禁 / 服务化 API / 排期三档 / R-01～R-13 / D1–D10 | [v0.1 §6–14](AI智能体声音训练项目_技术栈方案_v0.1.md) |
| 许可与权利保留策略（开放权重 + PolyForm NC + 双授权）/ 上游传导分析 / ADR-0001 | [v0.2 §2](AI智能体声音训练项目_技术栈方案_v0.2.md) |
| 权威论文体系（52 篇）与论文驱动的设计修正 | [v0.2 §3](AI智能体声音训练项目_技术栈方案_v0.2.md) |
| 选型评分卡 / ADR-0002 | [v0.2 §4](AI智能体声音训练项目_技术栈方案_v0.2.md) |
| GitHub 仓库与提交规范 / D11 / R-14～R-16 | [v0.2 §12–13](AI智能体声音训练项目_技术栈方案_v0.2.md) |

唯一实质修订：v0.1 §5.4 的 M1–M6 优先级由 **ADR-0003（本版 §3）** 取代。

---

## 8. 风险与待决策更新

### 8.1 风险表（相对 v0.2）

| ID | 变化 |
| --- | --- |
| R-01 | 已解除（v0.2 完成在线核验） |
| R-07 | 代理奖励黑客：v0.3 未改动，仍靠盲测为最终裁判 |
| R-14 | **本版分项核验、边界收窄但未清零**：已 `[OK]` 项回填 §5.3 / 许可证矩阵；`[MISS]` 项降级为 **R-14b** 法务跟进清单（ESD / CASIA / CPML / fishaudio 精确 ID / RVC-Boss 权重卡 / IndexTTS-2 HF 约束 / WenetSpeech 申请条款 / 论文会议归属） |
| R-15/R-16 | 未改动；D11 法务定稿仍是发布权重前阻塞项 |
| **R-17** | **新增**：契约与实现漂移风险——C 层 18 个错误码在 Phase 3 手写实现时可能与错误码表不一致。缓解：错误码稳定只追加、单测覆盖每个码、CI 对示例全量校验 |
| **R-18** | **新增（本轮核验发现）**：代码许可 ≠ 权重许可。F5-TTS（MIT / CC-BY-NC-4.0）、fishaudio（Community / CC-BY-NC-SA-4.0 或 Research）、coqui（MPL / CPML 或 CC-BY-NC-ND）均冲突；按代码推断可商用会出错。缓解：许可证矩阵拆分「代码/权重」两列 + 模型卡强制 `base_license` + `license-check` CI |

### 8.2 待决策（相对 v0.2）

| ID | 决策点 | 状态 |
| --- | --- | --- |
| D1–D10 | 声音来源 / 场景 / 音色数 / 精确时长 / 云端对照 / 算力 / 许可定位 / 语言 / 情感粒度 / 交付形态 | **仍待拍板** |
| **D11** | 许可条款法务定稿（P0 阻塞） | **仍待法务签字** |
| D12–D15 | 契约形式 / 两层校验 / CI 契约校验 / `Spec:` footer | **v0.3 新增，已决策落地** |

> 提醒：D11 未签字前**不发布模型权重**（许可一经分发不溯及既往）。v0.3 的契约与 CI 落地均在「文档/代码」层，不触碰权重发布，故不受 D11 阻塞。

---

## 9. v0.4 迭代方向（不依赖本轮评审结论）

1. **Phase 3 契约实现**：两个 API 接入 S+C 两层校验，18 个 C 层错误码全部实现 + 单测。
2. **preset 注册中心**：版本解析、默认值展开、审计填充。
3. **参数扫描 Harness**：把 §5.6 的 5 点单调性扫描做成可跑代码，对每个开放参数出报告，未过者不开放。
4. **D11 法务定稿**：商业化边界 FAQ、书面协议模板、`NOTICE` 归因清单签字。
5. **R-14 法务跟进项**：对在线无法确认的权重/数据集许可，走书面询问或替换方案。
6. **方案数字/引用全量自洽检查**：v0.1/v0.2/v0.3 + PAPERS.md + 许可证矩阵 + README 交叉核对。

---

## 10. 附录：文件索引

### 10.1 方案
- [`docs/AI智能体声音训练项目_技术栈方案_v0.1.md`](AI智能体声音训练项目_技术栈方案_v0.1.md)（初版归档）
- [`docs/AI智能体声音训练项目_技术栈方案_v0.2.md`](AI智能体声音训练项目_技术栈方案_v0.2.md)（许可/论文/仓库规范）
- [`docs/AI智能体声音训练项目_技术栈方案_v0.3.md`](AI智能体声音训练项目_技术栈方案_v0.3.md)（本文件）

### 10.2 契约（v0.3 新增）
- [`configs/voicespec/voicespec.schema.json`](../configs/voicespec/voicespec.schema.json) — 单一真源
- [`configs/voicespec/examples/`](../configs/voicespec/examples/) — minimal / full_tuned / duration_exact
- [`docs/voicespec/README.md`](voicespec/README.md) · [`docs/voicespec/ERROR-CODES.md`](voicespec/ERROR-CODES.md)
- [`scripts/validate_voicespec.py`](../scripts/validate_voicespec.py) · [`scripts/requirements.txt`](../scripts/requirements.txt)

### 10.3 论文 / 许可 / 决策
- [`docs/references/PAPERS.md`](references/PAPERS.md)
- [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md)
- [`docs/decisions/ADR-0001.md`](decisions/ADR-0001.md) · [`ADR-0002.md`](decisions/ADR-0002.md) · [`ADR-0003.md`](decisions/ADR-0003.md)
- [`LICENSE`](../LICENSE) · [`NOTICE`](../NOTICE) · [`LICENSE-COMMERCIAL.md`](../LICENSE-COMMERCIAL.md)

### 10.4 工程规范
- [`COMMIT_CONVENTION.md`](../COMMIT_CONVENTION.md) · [`CONTRIBUTING.md`](../CONTRIBUTING.md) · [`CODEOWNERS`](../CODEOWNERS) · [`.commitlintrc.yml`](../.commitlintrc.yml)
- [`.github/workflows/`](../.github/workflows/)（commitlint / license-check / eval-gate）
- [`configs/eval/thresholds.yaml`](../configs/eval/thresholds.yaml)（阈值单一真源）

---

**文档结束 · v0.3 · 待评审**
> 三轮评审重点：§2 契约是否满足「所有声音可参数化细调」且不过度约束、§3 M1–M6 优先级修订是否认可、§4/§5 核验回填是否足以清零 R-14、D1–D11 拍板、D11 法务阻塞项。
