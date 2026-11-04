# AI 智能体声音训练项目 · 技术栈方案（v0.2 · 论文与许可证核验版）

| 项目 | 内容 |
| --- | --- |
| 文档编号 | VM-TECH-001 |
| 版本 | **v0.2**（第二次迭代 / 待评审） |
| 前一版 | v0.1（初版，见 [`docs/AI智能体声音训练项目_技术栈方案_v0.1.md`](AI智能体声音训练项目_技术栈方案_v0.1.md)，保留存档） |
| 状态 | DRAFT — 供二轮评审 |
| 日期 | 2026-11-04 |
| 项目根目录 | `D:\.[Important Pro]\Voice_Model` |
| GitHub 仓库 | `https://github.com/hoshimiyatenka/VoiceModel` |

---

## v0.2 本次迭代的三项输入（对应用户第二轮指令）

| # | 用户指令（原意） | 本版响应 | 落点 |
| --- | --- | --- | --- |
| 1 | 「这个声音模型是开源的 但是保留一定权力 例如使用此模型的人 不得商业化」 | 新增**完整许可与权利保留策略**：术语澄清、许可选型、上游许可证传导分析、双授权/商业例外机制、技术侧约束、合规落地 | **第 2 章**（全新）、[`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md)、[`LICENSE`](../LICENSE)、[`NOTICE`](../NOTICE)、[`LICENSE-COMMERCIAL.md`](../LICENSE-COMMERCIAL.md)、ADR-0001 |
| 2 | 「寻找国内外权威的声音训练模型方法的论文作为参考进行第二次迭代」 | 核验并建立**权威论文体系**（52 篇，逐篇 arXiv ID / 标题 / 日期 / 发表会议），并把每篇映射到本方案的具体设计决策，用论文结论修正选型与控制层设计 | **第 3 章**（全新）、[`docs/references/PAPERS.md`](references/PAPERS.md)、第 4/6/8 章的「论文依据」小节 |
| 3 | 「在 github 上建立仓库 写入提交规范」 | 建立公开仓库并落地**提交规范**：Conventional Commits 定制版、scope/type 表、commitlint + CI 校验、分支/PR/版本联动、受保护路径 | **第 12 章**（全新）、[`CONTRIBUTING.md`](../CONTRIBUTING.md)、[`COMMIT_CONVENTION.md`](../COMMIT_CONVENTION.md)、[`.commitlintrc.yml`](../.commitlintrc.yml)、[`.github/`](../.github/) |

### 资料基准（v0.1 的 ⚠️ 已解除）

v0.1 编写时 `web_search` / `web_fetch` 通道返回 `HTTP 401`，所有第三方信息标注 `⚠️核验`。本版改用 **arXiv Atom API + GitHub REST API（`gh api`）+ Hugging Face Model API + 官方 LICENSE 原文** 逐项核验，日期 **2026-11-04**：

- ✅ 已核验：52 篇论文的 arXiv ID、标题、首发日期、部分期刊/会议信息（arXiv `journal_ref` / `comment` 字段）。
- ✅ 已核验：19 个上游仓库的 `license.spdx_id` 或 LICENSE 原文全文；8 个 Hugging Face 权重卡的 license tag。
- ✅ 已核验：[PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) 官方纯文本全文。
- ⚠️ 仍待核验：F5-TTS / GPT-SoVITS / HiFi-GAN 的**模型权重**（区别于代码）许可证、IndexTTS-2 权重卡条款、部分数据集（ESD / CASIA / EmoV-DB）的商用范围。这些不影响本版架构决策，但在 P0 定型前必须清零（登记为 R-14）。

> **仍未解除的限制**：`web_search` / `web_fetch` 工具通道依旧 401，本版数据来自可直接访问的 API 端点。所有核验结论均附原始 URL 与核验日期，可复核。

---

## 修订记录

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v0.1 | 2026-11-04 | 初版：需求拆解、五层参数化控制体系、双轨技术路线、数据工程、训练、评估门禁、服务化、排期、风险、决策点 |
| v0.2 | 2026-11-04 | ① 新增许可与权利保留策略（含「开源术语澄清」与上游许可证传导）② 新增权威论文体系与论文→设计决策映射 ③ 新增仓库与提交规范章节 ④ 用核验数据回填 v0.1 全部 ⚠️ 项 ⑤ 依据论文修正选型评分卡与控制手段优先级 ⑥ 新增 R-14/R-15 风险 |

---

## 目录

1. [摘要与一页决策](#1-摘要与一页决策)
2. **【v0.2 新增】[许可与权利保留策略](#2-许可与权利保留策略开源但不得商业化)**
3. **【v0.2 新增】[权威论文参考体系](#3-权威论文参考体系国内外)**
4. [候选模型核验结论与选型](#4-候选模型核验结论与选型)
5. [总体架构与参数化细调体系](#5-总体架构与参数化细调体系)
6. [数据工程](#6-数据工程)
7. [训练方案](#7-训练方案)
8. [质量保障与评估体系](#8-质量保障与评估体系)
9. [推理服务与工程实现](#9-推理服务与工程实现)
10. [里程碑、排期与成本](#10-里程碑排期与成本)
11. [风险登记表](#11-风险登记表)
12. **【v0.2 新增】[GitHub 仓库与提交规范](#12-github-仓库与提交规范)**
13. [待决策清单与 v0.3 迭代机制](#13-待决策清单与-v03-迭代机制)
14. [附录](#14-附录)

---

## 1. 摘要与一页决策

### 1.1 项目一句话

> 构建一套**可控、可复现、可评测**的 AI 智能体语音合成能力：以开源基座 + 授权数据微调得到专属音色，把「声音」抽象为一组**版本化、可单独调节、互不干扰的参数**；成果以**开放权重 / 非商业许可**公开，禁止未授权商业化，同时保留项目方单独授予商业许可的权利。

### 1.2 当前进度定位（诚实基线）

**技术路径位置：Phase 0（立项 / 选型核验期），尚未开始数据与训练，无任何实测指标。**

| 已完成 | 未完成 |
| --- | --- |
| 需求澄清；v0.1 方案骨架；五层参数化控制体系；评估门禁设计；许可证与论文的**在线核验**；GitHub 仓库与提交规范落地 | 算力确认、数据授权与采集、基座复现、任何训练产出、任何评测分数、许可条款的法务定稿 |

所有 Q* 阈值均为**目标门禁**，需在 Phase 2 用基线实测校准，不在本版虚报任何分数。

### 1.3 一页决策建议（v0.2 更新）

| 编号 | 建议 | 理由 | v0.2 变化 |
| --- | --- | --- | --- |
| R1 | **双轨路线**：可控基座（轨道 A）+ LoRA 定制（轨道 B），L5 参数契约解耦 | 兼顾快速出声与长期可控 | 维持 |
| R2 | 选型权重：**可控性 > 自然度**；精确时长控制列为强需求 | 参数化细调是第一需求 | 维持 |
| R3 | **许可采用「开放权重 + PolyForm Noncommercial 1.0.0 + 商业例外双授权」**，对外表述用「开放权重 / 源码可得」，**避免称 OSI 开源** | 用户要「开源但禁商用」，OSI 定义禁止用途歧视，二者术语冲突 | **新增，见第 2 章** |
| R4 | **上游基座优先选宽松许可（Apache-2.0 / MIT）的权重**，NC 条款只覆盖项目自有增量；避免直接采用带 SA 的 NC 权重 | CC-BY-NC-SA 会锁定衍生许可，剥夺项目方自由授权能力 | **新增，见 2.5** |
| R5 | 参数化分层实现，**pitch / rate 主控制禁用后处理 DSP** | DSP 变速变调损伤音质与说话人相似度 | 维持，论文依据见 3.4 |
| R6 | 评估体系与数据流水线**先于**训练落地 | 「保质量」依赖固定回归集与门禁 | 维持，论文依据见 3.5 |
| R7 | 排期以**档 B（16–20 周，灰度至 24 周）**为基线承诺 | 高质量 + 全参数可控无法在 8 周内同时达标 | 维持 |
| R8 | 仓库公开、提交走 Conventional Commits + commitlint CI 强制校验；`LICENSE` / `golden_set` / `configs/presets` 为受保护路径 | 对应第 3 项指令，且防止许可条款被无意改动 | **新增，见第 12 章** |

---

## 2. 许可与权利保留策略（「开源」但「不得商业化」）

> 本章是 v0.2 对第 1 项指令的完整答复。**含法律结论，须经法务复核后定稿**（登记为 D11 / R-15）。

### 2.1 先澄清术语：严格意义上这不是「开源」

用户表述为「开源的，但保留一定权力，例如使用者不得商业化」。这里存在一个必须澄清的术语冲突：

| 概念 | 定义 | 能否禁止商业化 |
| --- | --- | --- |
| **OSI 开源**（Open Source） | 符合 [Open Source Definition](https://opensource.org/osd)，第 6 条 **"No Discrimination Against Fields of Endeavor"** 明确禁止「不得用于商业用途」类条款 | ❌ **不能**。Apache-2.0 / MIT / GPL 都允许商用 |
| **源码可得 / 开放权重**（Source-available / Open-weight） | 代码或模型权重公开可获取，但许可附加用途限制 | ✅ 能，NC 条款即属此类 |
| **自由/开放文化许可**（CC BY-NC 等） | 允许复制、修改、分享，但禁止商业使用 | ✅ 能 |

**结论**：用户想要的东西，行业准确名称是 **「开放权重 + 非商业许可（Open-weight, Non-Commercial License）」**，不是 OSI 认证开源。v0.2 建议对外统一表述为：

> 「本项目**公开全部源代码与模型权重**，允许研究、个人、教育、非商业用途自由使用与二次开发；**商业化使用须取得项目方单独书面授权**。」

这样既满足「开源（公开可得）」的直觉，又精确保住「不得商业化」的权利，且不会因自称 "Open Source" 而在后续合作/审计中被质疑条款自相矛盾。

> **若评审坚持要 OSI 认证的「开源」**：那「禁止商业化」在法律上无法实现（Apache-2.0/MIT 不能限制用途），只能改为「商标 + 官方认证 + 服务条款」组合（限制冒名、不限制商用）。这属于方向性变更，需明确拍板（D11）。**本版按「开放权重 + NC」推进。**

### 2.2 许可选型对比（已核验原文）

| 候选许可 | 官方全文核验 | 覆盖对象 | 禁止商业化 | 专利授权 | 相同方式共享(SA) | 适合本项目 |
| --- | --- | --- | --- | --- | --- | --- |
| **PolyForm Noncommercial 1.0.0** | ✅ [polyformproject.org/licenses/noncommercial/1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)，2026-11-04 取回全文 | 软件（可涵盖代码、配置、权重包） | ✅ `Noncommercial Purposes` / `Personal Uses` / `Noncommercial Organizations` 为 permitted purpose，商用不在内 | ✅ 有专利许可 | ❌ 无 SA，不传染 | **✅ 推荐**：条款简短、为软件/模型设计、含专利授权、不锁定衍生许可 |
| CC BY-NC 4.0 | ⚠️ 本轮未取回原文全文 | 作品/素材，非为软件设计 | ✅ | ❌ 无明确专利条款 | ❌ 无 SA | 备选，适合单独发布的音频样本/数据集 |
| CC BY-NC-SA 4.0 | ⚠️ 本轮未取回原文全文 | 作品/素材 | ✅ | ❌ | ✅ **SA 会强制衍生作品同许可** | ❌ 不推荐（详见 2.5） |
| GPL / AGPL | 常见 OSI 许可 | 软件 | ❌ **允许商用**（ copyleft 不禁止收费） | ✅ | ✅ 强 | ❌ 达不到「禁商用」目的 |
| 自定义 NC 许可 | 需法务起草 | 自定义 | ✅ | 自定义 | 自定义 | 成本最高，仅在 PolyForm/CC 不满足时考虑 |

**推荐落地方案**：

```
LICENSE              → PolyForm Noncommercial License 1.0.0 官方全文（逐字，不修改）
NOTICE               → Required Notice + 上游归因清单 + 本项目附加声明
LICENSE-COMMERCIAL.md→ 商业授权申请入口、范围、流程、定价占位、联系方式
```

- `LICENSE` **保持官方原文逐字不改**（修改会破坏许可有效性）；项目特定信息全部放 `NOTICE`。PolyForm 明确要求：分发时必须随附条款或该 URL，以及 `Required Notice:` 开头的行——已按此设计。
- **双授权（Dual Licensing）**：项目方（版权持有人）保留向特定主体单独授予商业许可的权利；NC 许可面向公众，商业许可面向签约方。这是「保留一定权力」的核心机制，也是未来变现路径，PolyForm 的 `No Other Rights` 条款不禁止 licensor 自己另授他人（原文：`these terms do not ... prevent the licensor from granting licenses to anyone else`）。

### 2.3 「不得商业化」的边界定义（必须写清，否则不可执行）

PolyForm NC 1.0.0 原文对 permitted purpose 的界定（逐条映射）：

| 许可用途（允许） | 原文依据 | 项目示例 |
| --- | --- | --- |
| 任何非商业目的 | `Noncommercial Purposes` | 社区爱好者自建语音助手、非营利科普 |
| 个人研究/实验/测试、个人学习、私人娱乐、爱好项目、宗教活动，且无预期商业应用 | `Personal Uses` | 学生毕设、个人 demo |
| 慈善组织、教育机构、公共研究机构、公共安全/健康组织、环保组织、政府机构使用 | `Noncommercial Organizations`（无论资金来源） | 高校实验室、公立医院、政府项目 |
| 法律赋予的合理使用 | `Fair Use` | 引用、评论 |

| 需单独授权（禁止，除非签约） | 判定要点 |
| --- | --- |
| 以商业优势或金钱报酬为主要目的的产品/服务 | 嵌入付费 App、SaaS、收费 API |
| 企业内部业务运营使用 | 公司客服机器人、内部播报系统 |
| 直接或间接产生收入的用途 | 带广告的内容、直播、有声书售卖、游戏内角色语音 |
| 对外提供 Hosted / API 语音生成服务 | 参照 Fish Audio / bilibili 许可对 Hosted Service 的专门限制，本项目同样单列 |

> **待法务确认（D11）**：「商业化」是否包含 (a) 公益组织接受商业赞助、(b) 开源项目接受捐赠、(c) 个人作品后续意外走红产生收益。PolyForm 对非商业组织「无论资金来源」相对宽松，但需在 `LICENSE-COMMERCIAL.md` 里给出 FAQ 式解释以减少争议。

### 2.4 上游许可证传导分析（本轮核验最重要发现）

> **法律要点**：项目方只能对自己拥有版权的**增量部分**设定义务，**不能追溯撤销上游权利人已授予的权利**。因此「本模型禁止商业化」的实际覆盖范围取决于上游基座权重许可。

本轮通过 `gh api repos/*/license` 与 Hugging Face Model API 核验（2026-11-04）：

| 上游 | 代码许可 | **权重许可** | 商用 | 关键条款 / 风险 |
| --- | --- | --- | --- | --- |
| `QwenAudio/CosyVoice`（CosyVoice 2） | Apache-2.0 | `apache-2.0`（HF `FunAudioLLM/CosyVoice2-0.5B`） | ✅ | 宽松，最适合做基座 |
| `QwenLM/Qwen3-TTS` | Apache-2.0 | `apache-2.0`（HF `Qwen/Qwen3-TTS-12Hz-1.7B-Base`） | ✅ | 宽松；流式 + voice design + 克隆 |
| `OpenBMB/VoxCPM`（VoxCPM2） | Apache-2.0 | `apache-2.0`（HF `openbmb/VoxCPM2`） | ✅ | 宽松；tokenizer-free |
| **`SparkAudio/Spark-TTS`** | Apache-2.0 | **`cc-by-nc-sa-4.0`**（HF `SparkAudio/Spark-TTS-0.5B`） | ❌ | 权重卡原文：*"The model can only be used for non-commercial purposes."* 且 **SA 传染**（详见 2.5） |
| `index-tts/index-tts`（IndexTTS2） | `bilibili Model Use License Agreement`（GitHub 报 `NOASSERTION`） | 权重卡无 license tag，待核验 | 条件 | §2.2：MAU > 1 亿 或 上年营收 > RMB 10 亿须单独授权；§4(c)：**不得用于改进其他 AI 模型**（除自身衍生作品或**非商业** AI 模型） |
| `fishaudio/fish-speech` | `Fish Audio Community License v1.0`（2026-10-13，自定） | 待核验 | 有限 | 年营收 < USD 500,000 才有限商用；**Hosted Service 一律禁止**；禁止用输出训练/蒸馏其他基础语音模型 |
| `SWivid/F5-TTS` | MIT | 待核验 | 待定 | 代码宽松 |
| `RVC-Boss/GPT-SoVITS` | MIT | 待核验 | 待定 | 代码宽松 |

工具链（均为宽松许可，不构成障碍）：`openai/whisper` MIT、`m-bain/whisperX` BSD-2-Clause、`MontrealCorpusTools/Montreal-Forced-Aligner` MIT、`modelscope/FunASR` MIT、`wenet-e2e/wenet` Apache-2.0、`NVIDIA/BigVGAN` MIT、`speechbrain/speechbrain` Apache-2.0、`facebookresearch/audioseal` MIT、`coqui-ai/TTS` MPL-2.0（弱互惠，注意文件级 copyleft）。

> 完整表与核验命令见 [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md)。

**Apache-2.0 §4 的法律效果（关键）**：原文允许

> *"You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License."*

即：**基于 Apache-2.0 权重做 LoRA / 微调后，项目方可以对「自己的修改」乃至「衍生作品整体」加 NC 条款**，但必须保留上游的版权/专利/商标/归因声明与 Apache-2.0 副本，且**不能剥夺第三方对上游原作品本身依 Apache-2.0 享有的权利**。

因此本方案的许可边界写为：

```
┌─ 上游基座权重（Apache-2.0）──────────────┐  第三方仍可按 Apache-2.0 使用「原样上游」
│   版权归原作者；本项目不主张限制其商用      │
└──────────────────────────────────────┘
┌─ 本项目增量（PolyForm NC 1.0.0）────────┐  ★ 禁止商业化条款实际覆盖的部分
│   · 训练/推理/控制层代码                  │
│   · VoiceSpec 契约、preset、配置、词典     │
│   · 数据集标注、质检流程、golden_set       │
│   · LoRA / adapter / 微调后权重            │
│   · 模型卡、文档、评测报告                 │
│   · 生成的预设音色资产                     │
└──────────────────────────────────────┘
```

**这意味着**：使用者若自行取用上游原始权重、绕过本项目增量，可按 Apache-2.0 商用——这是无法用许可证阻止的（也不应试图阻止）。真正被保护的是**项目方投入产出的资产**：专属音色、参数化控制层、训练数据、评测体系。这一点必须在 README 与 `LICENSE-COMMERCIAL.md` 中说清，避免夸大权利范围。

### 2.5 为什么不建议选 NC-SA 权重做基座（重要决策）

核验发现 `SparkAudio/Spark-TTS-0.5B` 权重是 `CC-BY-NC-SA-4.0`，看似「天然满足禁商业化」，但有三个代价：

1. **SA（ShareAlike）传染**：衍生作品必须以**同一许可**发布，项目方**不能**改用 PolyForm NC 1.0.0，也不能自定义商业例外条款——直接削弱「保留一定权力」。
2. **商业例外的授权权不完整**：CC-BY-NC 的 NC 放宽需原权利人同意；项目方作为衍生方能否单独向第三方授予商用权存在不确定性，双授权变现路径受阻。
3. **代码/权重许可不一致**：代码 Apache-2.0、权重 CC-BY-NC-SA-4.0，合规审计需拆分两套义务，维护成本上升。

> **决策 ADR-0001**：选**宽松许可权重的基座**（CosyVoice 2 / Qwen3-TTS / VoxCPM2 三选一，Phase 2 实测定型），项目自有增量用 PolyForm NC 1.0.0。**不使用 Spark-TTS 权重作为发布基座**，但可将其属性级控制论文（arXiv:2503.01710）作为设计参考。
>
> 附带发现：`Spark-TTS` 代码 Apache-2.0 但权重 NC-SA，正是「代码开源 ≠ 权重可商用」的典型案例，已写入许可证矩阵用于团队培训。

### 2.6 权利保留的技术侧强化（许可证之外的执行手段）

许可证是法律手段，以下为工程手段，**不可替代许可证**，但能提高可执行性：

| 手段 | 作用 | 局限 |
| --- | --- | --- |
| **合成音频水印**（AudioSeal，arXiv:2401.17264，MIT） | 输出可溯源、可鉴伪，为侵权取证提供依据 | 不能阻止使用；`RenderSpec.watermark` 默认 `true` |
| 模型卡 + 权重卡 `license` 字段 | 分发时声明条款，避免「不知情」抗辩 | 需随每个 checkpoint / HF 仓库附带 |
| `NOTICE` + `Required Notice:` 行 | 满足 PolyForm 分发义务 | 必须随每次分发保留 |
| 音色注册鉴权 + `ref_audio_uri` 白名单 | 防止任意上传他人音频即克隆（伦理 + 合规） | 与商业化无关但同属「保留权力」 |
| 审计日志 `request_id → preset@version → model@commit → seed → text_hash → audio_hash → watermark_id` | 追溯使用链路 | 仅对自有服务有效 |
| 商业 SDK / 企业版单独分发 | 双授权落地形态 | 需与开源版代码组织分离（见 2.7） |

### 2.7 仓库与许可的文件级落地

| 文件 | 内容 | 保护级别 |
| --- | --- | --- |
| [`LICENSE`](../LICENSE) | PolyForm Noncommercial 1.0.0 官方全文（逐字） | **CODEOWNERS 保护，变更需法务 + maintainer 双人批准** |
| [`NOTICE`](../NOTICE) | `Required Notice:` 行、上游归因清单（Apache-2.0/MIT 各项目）、本项目声明 | 受保护 |
| [`LICENSE-COMMERCIAL.md`](../LICENSE-COMMERCIAL.md) | 商业授权范围、申请流程、FAQ、联系入口 | 受保护 |
| [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md) | 上游许可证核验表 + 传导分析 + 核验命令 | 每次升级基座必更新 |
| `docs/model-cards/*.md` | 每个发布 checkpoint 的模型卡，含 `license`、`base_model`、`base_license`、`derivative_license` | PR 模板强制填写 |
| `datasets/manifests/*.yaml` | 每条数据的 `license_id`、授权文件 hash | 缺字段即 CI 失败 |

**CI 强制项**（见第 12 章）：任何 PR 若修改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md`，或新增权重/数据集但缺 license 声明，`license-check` 工作流直接失败。

### 2.8 合规与伦理（沿用 v0.1 并强化）

1. **声音授权**：每个 speaker 书面授权，明确用途、期限、地域、可撤销条款；manifest 强制 `license_id`。
2. **NC 一致性**：训练数据若来自带 NC 条款的数据集（如部分情感库），其 NC 属性与本项目 NC 定位一致；**若数据来源允许商用，不因项目 NC 而受损**，但需在模型卡注明。
3. **输出标识**：对外音频/接口标注「AI 合成」。
4. **禁止滥用**：未授权克隆、冒充、去水印——写入 `NOTICE` 与模型卡，并参照 Fish Audio Community License §IV(b) 的写法（要求下游以同等保护力条款约束再分发）。
5. **个人信息**：原始录音按生物识别信息级别加密存储、访问审计、到期删除。

---

## 3. 权威论文参考体系（国内外）

> 本章是 v0.2 对第 2 项指令的答复。完整清单（52 篇，含 arXiv ID、日期、作者、发表会议、与本方案的关联）见 [`docs/references/PAPERS.md`](references/PAPERS.md)。以下为**用论文结论修正方案**的部分。

### 3.1 核验方法与可信度

- **数据源**：[arXiv Atom API](https://info.arxiv.org/help/api/index.html) `https://export.arxiv.org/api/query?id_list=...`，逐篇取回 `id` / `title` / `published` / `author` / `journal_ref` / `comment` 字段。
- **核验日期**：2026-11-04。**所有 ID 与标题均为 API 实际返回值**，未凭记忆填写。共 52 篇独立论文（含 2 处跨层引用占位），分组统计见 PAPERS.md。
- **权威性判据**：① 顶会/顶刊（NeurIPS / ICLR / ICML / ICASSP / INTERSPEECH / ACL / INTERSPEECH）；② 工业界实验室技术报告（Microsoft Research Asia / Alibaba / ByteDance Seed / bilibili / OpenBMB）；③ 被广泛复现且提供开源实现；④ 中文语音领域专用数据集/工具链论文。
- **国内外覆盖**：国内团队主导（微软亚洲研究院、阿里云/通义、字节 Seed、B 站、OpenBMB/面壁、希尔贝壳 AISHELL、WeNet 社区、Fish Audio）与国外团队主导（Google、Meta、OpenAI、NVIDIA、McGill、SaruLab、Carnegie Mellon 等）均纳入。
- ⚠️ 机构归属按论文作者署名与公开信息整理，**引用时请以论文首页为准**；部分技术报告未正式发表（已在清单标注）。

### 3.2 论文分层与「对本方案的意义」

| 层 | 代表论文（arXiv ID） | 本方案据此确立的设计 |
| --- | --- | --- |
| **L-0 基础架构** | WaveNet `1609.03499`、Tacotron 2 `1712.05884`(ICASSP 2018)、FastSpeech `1905.09263`(NeurIPS 2019)、FastSpeech 2 `2006.04558`(ICLR 2021)、Glow-TTS `2005.11129`、VITS `2106.06103`(ICML 2021) | **时长/音高显式建模是参数化细调的前提**：FastSpeech 系引入 duration predictor 与 F0/energy 条件，正是本方案 `ProsodySpec` 中 `rate` / `duration_*` / `pitch_*` / `energy_db` 可在**声学特征层**（M2）实现而非 DSP 的理论依据 |
| **L-0 声码器** | HiFi-GAN `2010.05646`(NeurIPS 2020)、BigVGAN `2206.04658`(ICLR 2023) | 音质门禁 Q4（DNSMOS ≥ 3.2）与 24k/48k 采样率选择 |
| **L-0 生成范式** | DDPM `2006.11239`、Flow Matching `2210.02747`、LoRA `2106.09685`、DPO `2305.18290` | 训练 Stage 1（LoRA）、Stage 2（偏好对齐）、F5-TTS 类 flow-matching 候选 |
| **L-1 神经编解码** | SoundStream `2107.03312`、AudioLM `2209.03143`、VALL-E `2301.02111`、SoundStorm `2305.09636`、SpeechTokenizer `2308.16692`(ICLR 2024) | 确立「语音 → 离散 token → LM」范式；支撑零样本克隆（ICL）与 `ref_audio_uri` 设计 |
| **L-2 零样本 / 大规模** | NaturalSpeech `2205.04421` / 2 `2304.09116` / 3 `2403.03100`、Voicebox `2306.15687`、VALL-E 2 `2406.05370`、UniAudio `2310.00704`、E2 TTS `2406.18009`、MaskGCT `2409.00750`、MegaTTS 3 `2502.18924`、VoiceCraft `2403.16973` | 「自然度上限 + 解耦表示」；NaturalSpeech 3 的 **factorized codec（内容/韵律/音色分解）** 直接支撑本方案「五层参数正交」与 `speaker_lock` 设计 |
| **L-3 可控 / 指令 / 情感**（★核心） | PromptTTS `2211.12171`、PromptTTS 2 `2309.02285`、InstructTTS `2301.13662`、Speak Read and Prompt `2302.03540`、Spark-TTS `2503.01710`(ACL 2025 投稿)、IndexTTS2 `2506.21619`、CosyVoice `2407.05407` / 2 `2412.10117`、Seed-TTS `2406.02430`、F5-TTS `2410.06885`、VoxCPM `2509.24650` | **本方案参数化体系的主要依据**，见 3.3 |
| **L-4 中文数据/工具链**（国内） | AISHELL-3 `2010.11567`、WenetSpeech `2110.03370`、WeNet `2102.01547`、Paraformer `2206.08317`、FunASR `2305.11013`、WhisperX `2303.00747`(INTERSPEECH 2023)、Whisper `2212.04356` | 数据流水线 §6：ASR 转写、强制对齐、G2P；中文 CER 门禁 Q1 的评测实现 |
| **L-5 评估 / 安全** | UTMOS `2204.02152`(INTERSPEECH 2022)、VoiceMOS Challenge `2203.11389`、DNSMOS `2010.15258`(ICASSP 2020)、SpeechBERTScore `2401.16812`、ECAPA-TDNN `2005.07143`(INTERSPEECH 2020)、WavLM `2110.13900`、AudioSeal `2401.17264`(ICML 2024) | 评估体系 §8 的全部客观指标来源；水印方案来源 |

### 3.3 用论文修正「参数化细调」设计（★ v0.2 实质迭代）

v0.1 凭工程经验设计了 M1–M6 控制手段。本版用论文逐条校正：

| 论文发现 | v0.1 设计 | **v0.2 修正** |
| --- | --- | --- |
| **FastSpeech 2** `2006.04558` 证明 F0 / energy / duration 可作为**显式条件**注入声学模型 | M2（特征编辑）优先级排在 M1 之后 | 对 `pitch_*` / `energy_db` / `rate` 这类**连续物理量**，**M2 提升为首选**（比自然语言指令更精确、可单调、可复现）；M1 用于离散/语义维度 |
| **IndexTTS2** `2506.21619` 标题即 *"Emotionally Expressive and **Duration-Controlled** Auto-Regressive Zero-Shot TTS"*，把**时长与情感作为两个独立输入** | F4 精确时长列为 P1，基座未定 | **确认 F4 有成熟论文与开源实现支撑，升为 P0 候选能力**；「音色参考 / 情感参考 / 时长」三路解耦输入直接映射为 `IdentitySpec` / `StyleSpec` / `ProsodySpec.duration_*` |
| **Spark-TTS** `2503.01710` 用 **single-stream decoupled speech tokens** 做属性级控制（性别/音高/语速等粗+细粒度属性） | `StyleSpec` 仅离散 emotion + 自然语言 | 新增 `AttributeSpec` 概念：把「属性即参数 schema」作为**候选实现路径**，Phase 2 需实测属性覆盖度与可插值性；但因权重 NC-SA（2.5）不采用其权重，仅参考方法 |
| **NaturalSpeech 3** `2403.03100` 的 factorized codec 把语音分解为内容/韵律/音色等因子 | 五层 VoiceSpec 靠「约定」正交 | 正交性不再只靠测试（5.6 参数扫描兜底），**优先选具备解耦表示的基座**，从模型结构上降低参数耦合；这是 R2 选型权重「可控性 > 自然度」的论文依据 |
| **PromptTTS 2 / InstructTTS** `2309.02285` / `2301.13662` 证明自然语言风格提示可控，但描述本身是**连续语义空间**、难以严格复现 | `style_prompt` 允许作为 preset 控制手段 | **收紧**：`style_prompt` 不得作为 preset 的唯一控制手段（已在 v0.1 规定，本版补上论文理由——文本描述的采样不确定性与指令遵循漂移） |
| **CosyVoice 2** `2412.10117` *"Scalable **Streaming** Speech Synthesis with Large Language Models"* | 流式列为 P1 | 确认流式在 LLM-based TTS 上有论文级方案；`RenderSpec.streaming` 与 chunk 边界韵律连续性测试（R-08）有了明确实现参照 |
| **UTMOS / VoiceMOS / DNSMOS / SpeechBERTScore** 四篇 | Q3/Q4 用 UTMOS + DNSMOS | **补入 SpeechBERTScore（参考感知）与 VoiceMOS Challenge 的评测协议**，主观评测规范（8.3）改按 VoiceMOS Challenge 的盲测/锚点做法组织 |
| **AudioSeal** `2401.17264` ICML 2024，局部化水印、鲁棒检测，MIT 许可 | `watermark: true` 一笔带过 | 明确为**本项目默认水印方案**，并写入 §2.6 权利保留技术措施；其「不得去除溯源信号」条款也写入 `NOTICE` |

### 3.4 用论文修正选型评分卡（第 4 章）

新增两个评分维度，直接来自论文：

- **「解耦表示」**（是否具备 factorized / decoupled tokens，参考 NaturalSpeech 3、Spark-TTS、IndexTTS2）——权重 10%，因为它是「调 A 不带动 B」的结构性保障。
- **「参数可枚举性」**（原生控制条件是离散属性 / 显式时长 / 指令，还是仅隐式 embedding，参考 PromptTTS 2、InstructTTS）——权重 10%，决定 `VoiceSpec` 能否有稳定映射。

### 3.5 用论文修正评估规范（第 8 章）

- 客观 MOS 代理不止 UTMOS 一种：补入 **DNSMOS（音质）/ SpeechBERTScore（参考感知）/ ECAPA-TDNN（说话人）**，形成「自然度—音质—相似度」三角，避免单一代理指标被 reward hacking（R-07）。
- 主观评测按 **VoiceMOS Challenge 2022** `2203.11389` 的协议：盲测、随机序、含锚点、报置信区间。
- **DPO** `2305.18290` 是 Stage 2 偏好对齐的直接依据；同时其已知风险（奖励优化≠人听更好）写入 R-07 与「人评为最终裁判」规则。

---

## 4. 候选模型核验结论与选型

### 4.1 已核验候选池（v0.1 的 ⚠️ 已清零或降级为「待权重核验」）

| 候选 | 论文 | 代码许可（核验） | 权重许可（核验） | 可控性要点 | 本项目结论 |
| --- | --- | --- | --- | --- | --- |
| **CosyVoice 2** | `2407.05407` / `2412.10117` | Apache-2.0 (`QwenAudio/CosyVoice`，注：`FunAudioLLM/CosyVoice` 现重定向至此) | apache-2.0 | 自然语言指令控情感/方言/语速；**流式** | **轨道 A 首选候选** |
| **Qwen3-TTS** | 技术报告（未取 arXiv ID） | Apache-2.0 | apache-2.0 | voice design + voice cloning + 流式 | **轨道 A 首选候选** |
| **VoxCPM2** | `2509.24650`（VoxCPM，Technical Report） | Apache-2.0 | apache-2.0 | tokenizer-free、上下文感知、克隆 | **轨道 A 备选** |
| **IndexTTS2** | `2506.21619` | `bilibili Model Use License`（非标准） | 待核验 | **精确时长 + 情感/音色解耦**（最契合 F4/五层正交） | **方法首选 / 许可需法务评估**；其 §4(c) 禁止用于改进其他 AI 模型（除自身或非商业模型），与本项目 NC 定位不冲突但须书面确认 |
| **Spark-TTS** | `2503.01710`(ACL 2025 投稿) | Apache-2.0 | **cc-by-nc-sa-4.0** | 属性级控制（最契合参数 schema） | **仅作方法参考，不用其权重**（2.5 / ADR-0001） |
| **Fish-Speech / OpenAudio S1** | 技术报告 | `Fish Audio Community License v1.0`（营收阈值 USD 500k / Hosted 禁止） | 待核验 | 标记/emoji 控情感 | 备选；合规负担重 |
| **F5-TTS** | `2410.06885` | MIT | 待核验 | flow matching，快 | 效率对照候选 |
| **GPT-SoVITS** | 社区项目 | MIT | 待核验 | 少样本音色定制 | **轨道 B 备选**（可控性弱，不作控制面） |
| **Seed-TTS** | `2406.02430` | 权重可得性待核验 | 待核验 | ICL / 指令 | 论文参考；不进评分（权重不可得则一票否决） |
| **MaskGCT / E2 TTS / MegaTTS 3** | `2409.00750` / `2406.18009` / `2502.18924` | 待核验 | 待核验 | 零样本 | 观察池 |

**声码器**：HiFi-GAN `2010.05646`(NeurIPS 2020)、BigVGAN `2206.04658`(ICLR 2023, MIT)、Vocos（待核验）。
**水印**：AudioSeal `2401.17264`(ICML 2024, MIT)。

### 4.2 选型评分卡（v0.2 修订版）

| 维度 | 权重 | 变化 | 论文依据 |
| --- | --- | --- | --- |
| 参数可控性（维度覆盖 / 解耦 / 单调性） | 25% | ↓5pp | FastSpeech 2 / IndexTTS2 |
| **解耦表示**（factorized / decoupled tokens） | **10%** | **新增** | NaturalSpeech 3 `2403.03100`、Spark-TTS `2503.01710` |
| **参数可枚举性**（原生控制条件是否可稳定映射） | **10%** | **新增** | PromptTTS 2 / InstructTTS |
| 中文自然度与可懂度 | 15% | ↓5pp | AISHELL-3 / WenetSpeech |
| 零样本相似度 | 10% | ↓5pp | VALL-E / Seed-TTS |
| 微调友好度（LoRA 支持 / 训练代码完整度） | 10% | — | LoRA `2106.09685` |
| 流式与延迟 | 10% | — | CosyVoice 2 `2412.10117` |
| **许可证**（商用可行性 + **可否叠加 NC 增量**） | **10%** | 内涵扩展 | 第 2 章 / ADR-0001 |
| 社区活跃 / 可维护性 | 5% | ↓ | — |

**一票否决**：权重不可获取、训练代码缺失导致无法复现、许可证与本项目 NC 定位冲突且无法通过法务确认。

### 4.3 双轨路线（维持 v0.1，补论文依据）

```
轨道 A · 基座轨（控制面）   CosyVoice 2 / Qwen3-TTS / VoxCPM2 三选一（Phase 2 实测）
   方法参考：IndexTTS2 的三路解耦、Spark-TTS 的属性 schema、NaturalSpeech 3 的因子分解
轨道 B · 定制轨（音色资产） LoRA / Adapter（arXiv:2106.09685），或 GPT-SoVITS 类少样本方案
汇合点：L5 VoiceSpec —— 换基座不动上层契约
```

---

## 5. 总体架构与参数化细调体系

> 本章沿用 v0.1 完整设计（五层 VoiceSpec、M1–M6、冲突矩阵、参数扫描、preset 版本化），此处保留骨架并标注 v0.2 修订点。逐参数定义以 [v0.1 第 5 章](AI智能体声音训练项目_技术栈方案_v0.1.md) 为准。

### 5.1 分层架构（不变）

```
L6 应用接入 → L5 控制层★(VoiceSpec/冲突消解/Preset版本化) → L4 推理层(流式/adapter热切换)
→ L3 模型层(基座+LoRA+声码器+水印) → L2 训练层(SFT→DPO→量化) → L1 数据层 → L0 基础设施
```

**L5 是项目核心资产**：模型可换，参数契约必须稳定。

### 5.2 五层 VoiceSpec（不变）

| 层 | 职责 | 代表参数 |
| --- | --- | --- |
| L-A `IdentitySpec` | 是谁在说 | `speaker_id` / `ref_audio_uri` / `speaker_lock` / `voice_blend` |
| L-B `ProsodySpec` | 怎么说（连续细调主战场） | `pitch_semitones` / `pitch_range` / `energy_db` / `rate` / `duration_mode` / `duration_ms` / `pauses` / `intonation_strength` |
| L-C `StyleSpec` | 什么状态说 | `emotion` / `emotion_strength` / `emotion_ref_uri` / `style_prompt` / `scenario` / `formality` / `style_adapter_mix` |
| L-D `LinguisticSpec` | 把字念对（零容忍） | `lang` / `text_normalize` / `pronunciation_dict` / `phoneme_overrides` / `emphasis` |
| L-E `RenderSpec` | 最后怎么送出去 | `sample_rate` / `format` / `loudness_lufs` / `seed` / `streaming` / `watermark` |

### 5.3 v0.2 修订点

1. **M1 → M2 优先级调整**：连续物理量（`pitch_*` / `energy_db` / `rate`）优先走 **M2 声学特征编辑**（依据 FastSpeech 2 `2006.04558`）；M1 原生条件用于离散/语义维度（`emotion` / `scenario` / 属性）。新优先级：
   `M4 文本确定性规则 > M2 特征编辑（连续量）> M1 原生条件（离散量）> M5 参考解耦 > M3 adapter 混合 > M6 DSP（仅限渲染层）`
2. **新增候选 `AttributeSpec`**：若 Phase 2 选定具备属性级控制的基座，把 Spark-TTS 式属性 schema 作为 L-C 的补充实现方式；需先过 5.6 单调性测试才开放。
3. **`duration_*` 升为 P0 候选能力**：依据 IndexTTS2 `2506.21619` 已有论文与开源实现。
4. **`style_prompt` 明确不得单独作为 preset 控制手段**（论文理由见 3.3）。
5. **冲突消解原则不变**：一律显式报错或显式优先级，禁止静默覆盖。
6. **参数扫描门禁不变**：5 点扫描，Spearman ρ ≥ 0.90、UTMOS 下降 ≤ 0.30、ECAPA cosine 漂移 ≤ 0.03、CER 上升 ≤ 1pp。

### 5.4 preset 版本化（不变）

```yaml
preset_id: warm_companion
version: 1.3.0
model: {base: <base>@<commit>, adapters: [{name: gentle_lora, weight: 0.8}], deps_lock: locks/infer-2026-11.lock}
identity:  {speaker_id: agent_main, speaker_lock: true}
prosody:   {rate: 0.92, pitch_semitones: -0.5, pause_profile: gentle}
style:     {emotion: tender, emotion_strength: 0.6, scenario: 陪伴}
linguistic:{lang: zh, pronunciation_dict: dicts/brand_v2}
render:    {sample_rate: 48000, loudness_lufs: -16, seed: 20261104, watermark: true}
audit:     {golden_set_passed: gs-2026-11-a, license: PolyForm-Noncommercial-1.0.0}
```

> v0.2 新增 `audit.license` 字段：每个 preset 携带许可标识，便于取证与商业授权核对。

---

## 6. 数据工程

> 「高质量」上限由数据决定。沿用 v0.1 流水线，补论文与许可证依据。

**流水线**：采集/授权 → 预处理(VAD/降噪/diarization) → 质检门禁 → 转写与强制对齐 → 标注 → 切片打包 → 版本冻结 → 划分(train/val/test/**golden_set**)。

**v0.2 论文/工具核验回填**：

| 环节 | 工具（已核验许可） | 论文依据 |
| --- | --- | --- |
| ASR 转写 | `openai/whisper` MIT `2212.04356`；`modelscope/FunASR` MIT `2305.11013`；Paraformer `2206.08317`；WeNet Apache-2.0 `2102.01547` | — |
| 字级对齐 | `m-bain/whisperX` BSD-2-Clause `2303.00747`(INTERSPEECH 2023)；`MontrealCorpusTools/Montreal-Forced-Aligner` MIT | 时间戳是 M2 特征编辑与 F4 时长控制的前提 |
| 说话人日志 / 嵌入 | `speechbrain/speechbrain` Apache-2.0 | ECAPA-TDNN `2005.07143`(INTERSPEECH 2020)、WavLM `2110.13900` |
| 中文语料 | AISHELL-3 `2010.11567`、WenetSpeech `2110.03370` | 仅用于流水线验证与评测对照，**不作商业音色** |
| 质检音质 | DNSMOS `2010.15258` | 门禁阈值见 6.2 |

**质检门禁**（v0.1 6.2，不变）：时长 2–15s、SNR ≥ 25dB、削波 0、非静音 40–95%、DNSMOS ≥ 3.3、转写人工校验 CER=0、单说话人概率 ≥ 0.98、字级对齐误差 ≤ 30ms。

**数据门槛**：零样本 3–10s → 少样本 1–5min → **LoRA 10–60min（推荐起点）** → 风格适配每风格 ≥ 30min → 全量 SFT 5–20h。仍坚持「先 10–60min 精标 + LoRA 打通全链路，别一上来录 20h」。

**v0.2 新增合规要求**：每条 manifest 必须含 `license_id` 与授权文件 hash；公开数据集与自有授权数据**物理隔离**（不同目录 / 不同 manifest 字段）；若数据集本身带 NC 条款，须在模型卡标注。

---

## 7. 训练方案

**硬件三档**（不变）：H-1 单卡 24GB / **H-2 单卡 80GB 或 4–8×24GB（推荐）** / H-3 8×80GB。存储 1–5TB 起步。

**三阶段**（补论文依据）：

| Stage | 内容 | 论文依据 |
| --- | --- | --- |
| 1 · SFT / 适配 | 冻结基座 + LoRA，目标 Q1/Q2 | LoRA `2106.09685`；GPT-SoVITS 少样本实践 |
| 2 · 偏好对齐 | 代理奖励 `w1·UTMOS + w2·相似度 + w3·(1−CER) + w4·参数遵循度` → DPO | DPO `2305.18290`；UTMOS `2204.02152` |
| 3 · 蒸馏 / 量化 / 部署化 | INT8/INT4、流式 chunk、热加载；**量化后强制重跑全量门禁** | Flow Matching `2210.02747`（若选 flow 类基座） |

**工程规范**（不变）：配置即代码、checkpoint 双命名、早停以 CER 为硬约束、冻结底层 + 通用语料 replay 10–20% 防灾难性遗忘、固定发音回归集、实验关联 `dataset@version + code@commit + config@hash + 门禁报告`、依赖锁 + Docker。

**R-07 强化**（依据 VoiceMOS `2203.11389`）：代理奖励不作为上线依据，人评盲测为最终裁判；UTMOS 与 CMOS 方向不一致时以 CMOS 为准。

---

## 8. 质量保障与评估体系

### 8.1 四套数据集（不变）

`train` / `val` ~200 / `test` ~300 / **`golden_set` ~100 + 100 难例（绝对冻结，PR 保护）**。golden_set 覆盖 8 类情感 × 3 语速 × 中英混 × 多音字 × 长数字/日期 × 专名 × 极短/极长句 × 疑问/感叹 × 停顿密集。

### 8.2 目标门禁（v0.2 不变，Phase 2 校准）

| ID | 维度 | 阈值 | 类型 |
| --- | --- | --- | --- |
| Q1 | 中文 CER ≤ 3%（英文 WER ≤ 5%） | 固定 ASR 回环 | 硬 |
| Q2 | ECAPA-TDNN cosine ≥ 0.82（不同说话人 < 0.70） | `2005.07143` | 硬 |
| Q3 | 主观 MOS ≥ 4.0 / UTMOS ≥ 3.8 | `2204.02152` / `2203.11389` | 软（盲测） |
| Q4 | DNSMOS ≥ 3.2、无削波/爆音/拖尾 | `2010.15258` | 硬 |
| Q5 | 情感分类 ≥ 85%、连续强度单调 ρ ≥ 0.90 | 参数扫描 | 软→硬 |
| Q6 | exact 时长误差 ≤ ±50ms 或 ±2% | IndexTTS2 `2506.21619` | 硬（启用 F4 时） |
| Q7 | 流式首包 P95 ≤ 300ms、RTF ≤ 0.3 | CosyVoice 2 `2412.10117` | 软（按场景） |
| Q8 | 1000 句回归 0 异常 | CI | 硬 |
| Q9 | 同 preset/模型/seed/文本 → 波形 byte-level 一致 | 依赖锁 | 硬 |
| Q10 | 单参数扫描其他层漂移 ≤ 阈值（cos ≤ 0.03） | 5.6 | 硬 |

**v0.2 新增**：`SpeechBERTScore` `2401.16812` 作为**参考感知**辅助指标（有参考音频时），与 UTMOS（无参考）/ DNSMOS（音质）构成三角，缓解单一代理指标被优化攻击（R-07）。

### 8.3 主观评测规范（按 VoiceMOS Challenge 2022 协议）

≥ 20 人、听力筛选、≥ 40 条/轮、随机序盲测、含隐藏锚点与重复项测一致性、报均值 + 95% CI、CMOS 差值 CI 不跨 0 才判定胜出、原始评分表归档。方法：MOS / CMOS / 相似度 ABX / 情感 MUSHRA。

### 8.4 CI 门禁流程（不变）

任意变更 → golden_set 全量合成 → 客观指标 → 参数扫描 → 门禁报告 → **硬指标任一不通过即阻断** → 主观盲测（重大版本）→ candidate → 人工批准 → production。

阈值单一真源见 [`configs/eval/thresholds.yaml`](../configs/eval/thresholds.yaml)（v0.2 已落地，代码与文档均引用它，禁止硬编码数字）。

---

## 9. 推理服务与工程实现

**API 契约**（不变）：`POST /v1/synthesize`（`preset` 与 `spec` 二选一/合并，spec 显式覆盖 preset）、`GET /v1/voices`、`GET /v1/presets`、`POST /v1/presets/validate`、`GET /v1/eval/reports/{id}`。`request_id` 全链路透传，日志关联 `preset@version + model@commit + seed + text_hash + audio_hash + watermark_id`。

**延迟预算**（不变）：解析 ≤10ms / 首 chunk 生成 ≤180ms / 声码+编码 ≤80ms / **首包 P95 ≤300ms**。

**v0.2 新增**：
- `watermark` 默认 `true`，实现参照 **AudioSeal** `2401.17264`（MIT），与 §2.6 权利保留联动。
- 每次响应头/元数据附 `license: PolyForm-Noncommercial-1.0.0` 与 `commercial_license_url`，让「不得商业化」在接口层可见。
- 降级链 `原生时长控制 → 特征编辑 → DSP（标记 degraded=true 并告警）` 不变。

---

## 10. 里程碑、排期与成本

**人力**：算法 1–2 / 工程 1 / 数据 0.5–1 / 评测协调 0.5（兼）；硬件按 H-2 估。

| Phase | 周 | 交付物 | 出口 |
| --- | --- | --- | --- |
| P0 立项与核验 | W1–W2 | 选型 ADR、**许可法务定稿（新增）**、D1–D11 决策表、v0.3 | 候选表无待核验项；LICENSE 经法务批准 |
| P1 数据底座 | W2–W6 | 数据流水线、10–60min 精标数据、golden_set v1 | 全量过质检门禁 |
| P2 基线复现与定型 | W3–W7（并行） | 3 候选同台实测、评分卡、阈值校准 | 指定基座 |
| P3 参数化控制层 v1 | W7–W11 | VoiceSpec schema、冲突消解、preset、参数扫描器 | 每个开放参数过单调性测试 |
| P4 微调与偏好对齐 | W11–W17 | speaker adapter、DPO 产物、模型卡、门禁报告 | Q1/Q2/Q3 达标 |
| P5 评估体系与 CI | W5–W18（贯穿） | Eval Harness、CI、盲测第一轮、许可证检查工作流 | 任意 PR 自动出报告 |
| P6 服务化与流式 | W16–W20 | API、流式、监控、水印、降级、回滚 | Q7 达标；1000 句 0 异常 |
| P7 灰度与迭代 | W20–W24 | 灰度报告、v1.0 | CMOS 不劣于基线 |

**三档排期**（不变）：A 6–8 周演示 / **B 16–20 周（基线承诺，灰度至 24 周）** / C 24–32 周规模化。W8 设档 A 内部检查点，不替代档 B 验收。

**v0.2 新增 P0 出口条件**：许可证条款需法务书面批准后才允许发布权重；这是「不得商业化」可执行的前提，避免先发布后改许可（改许可对已分发副本不溯及）。

**成本量级**（不变，仅结构）：GPU（H-2 × 4–6 月）、数据录制与授权、标注、主观评测、存储 1–5TB、人力 2.5–4 人 × 4–6 月、合规法务。省钱顺序：H-1 + 小数据跑通 P0–P3 → 拿基线 → 再决定升算力。

---

## 11. 风险登记表

沿用 v0.1 的 R-01～R-13，更新与新增：

| ID | 风险 | 变化 | 缓解 |
| --- | --- | --- | --- |
| R-01 | 选型基于未核验信息 | **已解除**（本版完成在线核验，附 URL/日期） | — |
| R-03 | 许可证不允许商用 → 一票否决 | **内涵反转**：本项目主动禁商用，风险变为「上游许可与 NC 定位冲突」 | 2.4 传导分析 + ADR-0001 + 法务复核 |
| R-07 | 奖励黑客 | **加重**（论文依据） | 三角客观指标 + VoiceMOS 协议盲测为最终裁判 |
| R-08 | 流式 chunk 边界跳变 | 有论文方案参照 | CosyVoice 2 `2412.10117` + 专项连续性测试 |
| **R-14** | **代码与权重许可证不一致**(Spark-TTS / IndexTTS2 / Fish-Speech)、部分权重/数据集许可未核验 | **新增** | P0 清零；`license-check` CI；模型卡强制 `base_license` 字段 |
| **R-15** | **「开源」表述与 NC 条款冲突**、NC 覆盖范围被夸大、许可条款未经法务批准即发布 | **新增** | 2.1 术语澄清、2.4 边界图、2.7 受保护路径、D11 法务签字 |
| **R-16** | 上游 NC-SA 权重传染导致项目失去商业例外授权能力 | **新增** | ADR-0001 排除 NC-SA 权重作发布基座 |

---

## 12. GitHub 仓库与提交规范

> 本章是 v0.2 对第 3 项指令的答复。仓库已建立：`https://github.com/hoshimiyatenka/VoiceModel`（**public**，与「公开可得」定位一致）。

### 12.1 仓库定位与可见性

| 项 | 决策 | 理由 |
| --- | --- | --- |
| 可见性 | **Public** | 「开源/公开可得」；NC 条款不要求私有 |
| 默认分支 | `main` | 受保护，禁止直推 |
| 许可文件 | `LICENSE` = PolyForm NC 1.0.0 官方全文 | 见第 2 章 |
| 仓库内容 | **仅代码 / 文档 / 配置 / manifest / 预设 / 测试**；音频实体、checkpoint 走对象存储 + DVC/HF | 避免大文件、避免未授权音频入库 |
| 发布前 | **强制 `leak_guard` 扫描** | 防 API key / token / 私钥 / 授权文件隐私入库 |

> 若后续要改为私有或改名，属于可逆操作，但**改名后须同步 `NOTICE` 与所有文档中的仓库 URL**。

### 12.2 目录结构

```
VoiceModel/
├── README.md                          # 入口、快速开始、文档索引、许可摘要
├── LICENSE                            # PolyForm NC 1.0.0 官方全文（受保护）
├── NOTICE                             # Required Notice + 上游归因（受保护）
├── LICENSE-COMMERCIAL.md              # 商业授权入口（受保护）
├── CONTRIBUTING.md                    # 贡献流程 + 提交规范（用户指令落点）
├── COMMIT_CONVENTION.md               # ★ 提交规范完整定义
├── CHANGELOG.md                       # 由 conventional-changelog 从提交生成
├── CODEOWNERS                         # 受保护路径
├── .commitlintrc.yml                  # commitlint 规则
├── .gitignore
├── .github/
│   ├── workflows/
│   │   ├── commitlint.yml             # PR 提交信息校验
│   │   ├── license-check.yml         # 许可与归因合规检查
│   │   └── eval-gate.yml             # 评估门禁（骨架）
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/{bug_report.yml,feature_request.yml,model_card.yml}
├── docs/
│   ├── AI智能体声音训练项目_技术栈方案_v0.1.md   # 归档
│   ├── AI智能体声音训练项目_技术栈方案_v0.2.md   # 本文件
│   ├── references/PAPERS.md          # ★ 权威论文清单
│   ├── licensing/UPSTREAM-LICENSE-MATRIX.md  # ★ 上游许可证核验表
│   ├── decisions/ADR-0001..0003.md  # 许可策略 / 基座选型 / 控制层
│   ├── model-cards/                 # 每个发布 checkpoint 一份
│   ├── eval/                        # 评测规范、盲测问卷、报告模板
│   └── runbooks/                    # 训练、回滚、发布手册
├── configs/
│   ├── eval/thresholds.yaml         # 阈值单一真源
│   ├── train/  base/  presets/      # preset 受保护
├── src/{frontend,control,models,train,eval,serve,data}/
├── datasets/{manifests,golden_set/}  # golden_set 受保护（PR 禁止改）
├── dicts/  scripts/  tests/{unit,integration,regression}/
├── experiments/  locks/  artifacts(gitignore)
```

### 12.3 提交规范（★ 完整定义见 [`COMMIT_CONVENTION.md`](../COMMIT_CONVENTION.md)）

采用 **Conventional Commits 1.0.0** + 项目定制：

```
<type>(<scope>): <subject>        # ≤ 72 字符，中文或英文，祈使句，无句号
                                  # 空行
<body>                            # 为什么（不是改了什么）
                                  # 空行
<footer>                          # BREAKING CHANGE / Refs / Gate-Report / Dataset / License
```

**type（穷举，CI 校验）**：

| type | 用途 | 版本影响 |
| --- | --- | --- |
| `feat` | 新能力 | minor |
| `fix` | 缺陷修复 | patch |
| `docs` | 文档（含方案、论文清单、模型卡） | — |
| `model` | 模型结构 / checkpoint / adapter 变更 | minor（需模型卡） |
| `voice` | 音色资产 / preset / 发音词典变更 | patch（需门禁报告） |
| `data` | 数据流水线 / manifest / golden_set | patch（golden_set 受保护） |
| `eval` | 指标实现 / 阈值 / 评测报告 | patch（阈值改动需评审） |
| `train` | 训练脚本 / 超参 / 实验配置 | patch |
| `perf` | 推理性能优化 | patch |
| `refactor` | 重构（无行为变化） | — |
| `test` | 测试 | — |
| `build` | 依赖 / 锁文件 / 镜像 | patch |
| `ci` | CI 工作流 | — |
| `chore` | 杂项 | — |
| `license` | **许可 / NOTICE / 归因 / 合规**（受保护，需法务 + 2 人批准） | — |
| `revert` | 回滚 | — |

**scope（穷举）**：`control` `frontend` `prosody` `style` `linguistic` `render` `preset` `speaker` `dataset` `golden-set` `train` `model` `serve` `api` `stream` `eval` `metrics` `gates` `license` `notice` `deps` `ci` `docs` `refs`。

**强制 footer**：
- 改 `configs/eval/thresholds.yaml` → `Gate-Report: <id>`
- 改 `configs/presets/**` 或 `dicts/**` → `Gate-Report: <id>` + `Preset: <name>@<version>`
- 新增/更新权重或数据集 → `Dataset: ds-YYYYMMDD-x` 或 `Model: <id>` + `License: <spdx>`
- 改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md` → `License-Review: <法务批准人>`
- 不兼容变更 → `BREAKING CHANGE: <说明>`（major）

**示例**：

```
feat(control): 新增 duration_mode=exact 与 rate 互斥校验

IndexTTS2 (arXiv:2506.21619) 把时长作为独立条件，若与 rate 同时给出会
产生两个互相冲突的时长来源。按冲突消解矩阵 5.5 改为显式 400 而非静默覆盖。

Refs: #42
Gate-Report: gs-2026-11-a
```

```
license(notice): 补充 Qwen3-TTS 权重 apache-2.0 归因条目

上游权重许可证核验（2026-11-04）后补全 NOTICE，避免分发时遗漏
Apache-2.0 §4 要求的归因声明。

License-Review: <待法务填写>
Refs: VM-TECH-001 v0.2 §2.4
```

### 12.4 CI 强制与受保护路径

- **commitlint**：PR 内所有提交 + PR 标题（squash 场景）必须合规，不合规直接失败。
- **license-check**：修改 `LICENSE`/`NOTICE`/`LICENSE-COMMERCIAL.md`、或新增权重/数据集缺 `License:` 声明 → 失败。
- **protected paths**（CODEOWNERS）：`LICENSE`、`NOTICE`、`LICENSE-COMMERCIAL.md`、`datasets/golden_set/**`、`configs/presets/**`、`configs/eval/thresholds.yaml` → 需 maintainer 批准；golden_set 的 hash 由 CI 校验，任何改动直接失败。
- **分支**：`main` 受保护；功能分支 `feat/<scope>-<slug>`、`fix/<...>`、`docs/<...>`、`model/<...>`、`exp/<...>`。
- **PR**：必须填模板（变更类型、是否影响门禁/许可/模型卡、关联 Gate-Report、许可影响勾选）。
- **版本**：tag `vX.Y.Z`，`CHANGELOG.md` 由 conventional-changelog 从提交生成，禁止手写。

### 12.5 提交前检查清单

```
[ ] 提交信息符合 COMMIT_CONVENTION.md（本地 commitlint 或 CI 校验）
[ ] 未提交音频实体 / checkpoint / 授权书扫描件 / .env / 密钥
[ ] 涉及 preset / 阈值 / 权重 / 数据集时已填对应 footer
[ ] 新增第三方依赖或基座已更新 docs/licensing/UPSTREAM-LICENSE-MATRIX.md 与 NOTICE
[ ] 涉及方案变更已同步 docs/ 方案文档与修订记录
[ ] git push 前已跑 leak_guard({action:"scan", path:"<绝对路径>"}) 且 ok=true
```

---

## 13. 待决策清单与 v0.3 迭代机制

### 13.1 待决策（D1–D11，v0.2 更新）

| ID | 决策点 | 变化 | 影响 |
| --- | --- | --- | --- |
| D1 | 声音来源：自录授权 / 采购 / 客户自带 / 合成 | — | 数据成本、周期、合规 |
| D2 | 首要场景：实时对话 vs 离线内容 | — | Q7 是否硬指标 |
| D3 | 1 个主音色 vs 多音色矩阵 | — | 是否走档 C |
| D4 | **是否需要精确时长控制** | **升为高优先**（IndexTTS2 已有论文与实现） | 直接决定基座 |
| D5 | 是否允许云端商业 TTS API 做质量对照 | — | 自建范围 |
| D6 | 算力档 H-1/H-2/H-3 | — | 档 B 可否承诺 |
| D7 | 商用许可要求 | **改为**：确认接受「开放权重 + NC」而非 OSI 开源 | 一票否决项 |
| D8 | 语言范围 | — | 数据与评测规模 |
| D9 | 情感粒度：离散 8 类 / 连续向量 / 自然语言 / 三者 | — | 参数体系 |
| D10 | 交付形态：权重 / 私有 API / SDK / 一体机 | — | 服务化工作量 |
| **D11** | **许可条款法务定稿**：PolyForm NC 1.0.0 采用、商业化边界 FAQ、双授权流程、`NOTICE` 归因清单 | **新增，P0 阻塞项** | 「不得商业化」能否执行 |

### 13.2 v0.3 必做（不依赖评审结论）

1. **法务复核** D11：确认 PolyForm NC 1.0.0 全文、商业化边界、`NOTICE` 归因清单、双授权文本。
2. **清零剩余待核验项**：F5-TTS / GPT-SoVITS / HiFi-GAN 权重许可、IndexTTS-2 权重卡、ESD / CASIA / EmoV-DB 商用范围（R-14）。
3. 产出 `VoiceSpec` 正式 JSON Schema + `validate` 接口错误码表。
4. 产出 ADR-0002（基座选型实测方法）、ADR-0003（参数化控制层实现路径）的实测回填。
5. 把 PAPERS.md 中「未取期刊/会议信息」的条目补齐发表状态。

### 13.3 迭代方式（不变）

| 反馈类型 | 处理 |
| --- | --- |
| 方向性调整 | 更新第 1/2/4/10 章 + 新增 ADR |
| 参数增删 | **四处同步**：§5 参数总表 / 控制手段映射 / 冲突矩阵 / 参数扫描项 |
| 指标/阈值调整 | 只改 `configs/eval/thresholds.yaml` 与引用处 |
| 许可/合规调整 | 只改 `LICENSE`/`NOTICE`/`LICENSE-COMMERCIAL.md` + 许可证矩阵 + 模型卡模板，需法务签字 |

---

## 14. 附录

### 14.1 术语（节选）

PolyForm NC / 开放权重 / Source-available / OSI OSD 第 6 条 / 双授权 / SA 传染 / Apache-2.0 §4 / VoiceSpec / preset / golden_set / TTS / ICL / SFT / LoRA / DPO / G2P / TN / F0 / CER / UTMOS / DNSMOS / ECAPA-TDNN / RTF / MUSHRA / CMOS / ABX。完整表见 v0.1 附录 A。

### 14.2 本版核验源（可复核）

| 源 | 用途 |
| --- | --- |
| [arXiv Atom API](https://info.arxiv.org/help/api/index.html) `export.arxiv.org/api/query` | 52 篇论文的 ID / 标题 / 日期 / 作者 / `journal_ref` / `comment` |
| GitHub REST API `gh api repos/<owner>/<repo>` / `/license` | 19 个仓库的 SPDX 与 LICENSE 原文 |
| Hugging Face Model API `huggingface.co/api/models/<id>` | 8 个权重卡的 license tag 与 gated 状态 |
| [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) | LICENSE 官方纯文本全文 |
| [Open Source Definition](https://opensource.org/osd) | 第 6 条「不得歧视用途领域」 |

### 14.3 关联文件索引

- 方案：v0.1（归档）、**v0.2（本文件）**
- 论文：[`docs/references/PAPERS.md`](references/PAPERS.md)
- 许可：[`LICENSE`](../LICENSE) · [`NOTICE`](../NOTICE) · [`LICENSE-COMMERCIAL.md`](../LICENSE-COMMERCIAL.md) · [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](licensing/UPSTREAM-LICENSE-MATRIX.md) · [`docs/decisions/ADR-0001.md`](decisions/ADR-0001.md)
- 提交规范：[`COMMIT_CONVENTION.md`](../COMMIT_CONVENTION.md) · [`CONTRIBUTING.md`](../CONTRIBUTING.md) · [`.commitlintrc.yml`](../.commitlintrc.yml) · [`.github/workflows/commitlint.yml`](../.github/workflows/commitlint.yml)
- 阈值：[`configs/eval/thresholds.yaml`](../configs/eval/thresholds.yaml)

---

**文档结束 · v0.2 · 待评审**
> 二轮评审重点：§2.1 术语澄清（是否接受「开放权重」而非「OSI 开源」）、§2.4 许可覆盖边界、§2.5 / ADR-0001 不选 NC-SA 权重、§3.3 论文驱动的设计修正、§12 提交规范、D11 法务阻塞项。
